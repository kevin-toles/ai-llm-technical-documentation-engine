#!/usr/bin/env python3
"""
Generate PDF rename suggestions by extracting titles from PDF metadata.
Outputs a list of suggested renames for user review before execution.
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

# Try to import PyMuPDF (fitz)
try:
    import fitz  # PyMuPDF
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False
    print("⚠️  PyMuPDF not installed. Install with: pip install PyMuPDF")


def sanitize_filename(title: str) -> Optional[str]:
    """Convert a title to a safe filename."""
    if not title:
        return None
    
    # Remove or replace problematic characters
    # Keep letters, numbers, spaces, hyphens, and common punctuation
    sanitized = re.sub(r'[<>:"/\\|?*]', '', title)
    
    # Replace multiple spaces with single space
    sanitized = re.sub(r'\s+', ' ', sanitized)
    
    # Remove leading/trailing whitespace and dots
    sanitized = sanitized.strip(' .')
    
    # Limit length (leave room for .pdf extension)
    if len(sanitized) > 200:
        sanitized = sanitized[:200].rsplit(' ', 1)[0]
    
    return sanitized if sanitized else None


def extract_title_from_pdf(pdf_path: Path) -> dict:
    """Extract title and other metadata from a PDF file."""
    result = {
        'original_filename': pdf_path.name,
        'metadata_title': None,
        'first_page_text': None,
        'suggested_title': None,
        'confidence': 'low'
    }
    
    if not HAS_PYMUPDF:
        return result
    
    try:
        doc = fitz.open(pdf_path)
        
        # Get metadata title
        metadata = doc.metadata
        if metadata and metadata.get('title'):
            title = metadata['title'].strip()
            if title and len(title) > 3 and not title.startswith('/'):
                result['metadata_title'] = title
                result['confidence'] = 'high'
        
        # If no metadata title, try to extract from first page
        if not result['metadata_title'] and len(doc) > 0:
            first_page = doc[0]
            text = first_page.get_text()
            
            # Get first non-empty lines (potential title)
            lines = [l.strip() for l in text.split('\n') if l.strip()]
            if lines:
                # Take first 1-3 lines as potential title
                potential_title = ' '.join(lines[:2])
                if len(potential_title) > 5 and len(potential_title) < 200:
                    result['first_page_text'] = potential_title
                    result['confidence'] = 'medium'
        
        doc.close()
        
        # Determine suggested title
        if result['metadata_title']:
            result['suggested_title'] = sanitize_filename(result['metadata_title'])
        elif result['first_page_text']:
            result['suggested_title'] = sanitize_filename(result['first_page_text'])
        
    except Exception as e:
        result['error'] = str(e)
    
    return result


def is_messy_filename(filename: str) -> bool:
    """Check if a filename looks messy and needs renaming."""
    messy_patterns = [
        r'^_',  # Starts with underscore
        r'^[a-f0-9]{32}',  # MD5 hash
        r'^\d{5,}',  # Long numeric ID
        r'OceanofPDF',
        r'dokumen\.pub',
        r'libgen',
        r'z-lib',
        r'epdf\.pub',
        r'\(\d+\)$',  # Ends with (1), (2), etc.
        r'_-_',  # Underscore-dash-underscore pattern
        r'%20',  # URL encoded spaces
    ]
    
    for pattern in messy_patterns:
        if re.search(pattern, filename, re.IGNORECASE):
            return True
    
    return False


def generate_rename_suggestions(books_dir: str, output_file: str = None) -> list:
    """Generate rename suggestions for all PDFs in a directory."""
    books_path = Path(books_dir)
    
    if not books_path.exists():
        print(f"❌ Directory not found: {books_dir}")
        return []
    
    pdf_files = list(books_path.glob('*.pdf'))
    print(f"\n📚 Found {len(pdf_files)} PDF files in {books_dir}\n")
    
    suggestions = []
    needs_rename = []
    already_clean = []
    
    for pdf_path in sorted(pdf_files):
        filename = pdf_path.name
        
        # Check if filename looks messy
        if not is_messy_filename(filename):
            already_clean.append(filename)
            continue
        
        # Extract metadata
        info = extract_title_from_pdf(pdf_path)
        
        if info['suggested_title']:
            new_filename = info['suggested_title'] + '.pdf'
            
            # Don't suggest if same as original
            if new_filename.lower() != filename.lower():
                suggestion = {
                    'original': filename,
                    'suggested': new_filename,
                    'confidence': info['confidence'],
                    'source': 'metadata' if info['metadata_title'] else 'first_page'
                }
                suggestions.append(suggestion)
                needs_rename.append(suggestion)
        else:
            needs_rename.append({
                'original': filename,
                'suggested': None,
                'confidence': 'none',
                'source': 'manual_needed'
            })
    
    # Print summary
    print("=" * 80)
    print("RENAME SUGGESTIONS SUMMARY")
    print("=" * 80)
    print(f"\n✅ Already clean filenames: {len(already_clean)}")
    print(f"🔄 Need renaming: {len(needs_rename)}")
    print(f"   - Auto-suggested: {len([s for s in suggestions if s['suggested']])}")
    print(f"   - Manual needed: {len([s for s in needs_rename if not s.get('suggested')])}")
    
    # Print suggestions grouped by confidence
    print("\n" + "=" * 80)
    print("HIGH CONFIDENCE RENAMES (from PDF metadata)")
    print("=" * 80)
    high_conf = [s for s in suggestions if s['confidence'] == 'high']
    for s in high_conf:
        print(f"\n📄 {s['original']}")
        print(f"   → {s['suggested']}")
    
    print("\n" + "=" * 80)
    print("MEDIUM CONFIDENCE RENAMES (from first page text)")
    print("=" * 80)
    med_conf = [s for s in suggestions if s['confidence'] == 'medium']
    for s in med_conf:
        print(f"\n📄 {s['original']}")
        print(f"   → {s['suggested']}")
    
    print("\n" + "=" * 80)
    print("MANUAL REVIEW NEEDED (no title found)")
    print("=" * 80)
    manual = [s for s in needs_rename if not s.get('suggested')]
    for s in manual:
        print(f"\n❓ {s['original']}")
    
    # Save to JSON for later use
    if output_file:
        output_path = Path(output_file)
        output_data = {
            'generated_at': datetime.now().isoformat(),
            'source_directory': str(books_dir),
            'already_clean': already_clean,
            'suggestions': suggestions,
            'manual_needed': manual
        }
        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"\n💾 Saved suggestions to: {output_file}")
    
    # Generate shell commands
    print("\n" + "=" * 80)
    print("SHELL COMMANDS TO EXECUTE (copy and review)")
    print("=" * 80)
    print(f"\ncd '{books_dir}'")
    
    for s in suggestions:
        if s['suggested']:
            # Escape single quotes in filenames
            orig = s['original'].replace("'", "'\\''")
            new = s['suggested'].replace("'", "'\\''")
            print(f"mv '{orig}' '{new}'")
    
    return suggestions


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate PDF rename suggestions')
    parser.add_argument('--dir', '-d', 
                        default='/Users/kevintoles/POC/llm-document-enhancer/books',
                        help='Directory containing PDFs')
    parser.add_argument('--output', '-o',
                        default='/Users/kevintoles/POC/llm-document-enhancer/rename_suggestions.json',
                        help='Output JSON file for suggestions')
    
    args = parser.parse_args()
    
    generate_rename_suggestions(args.dir, args.output)
