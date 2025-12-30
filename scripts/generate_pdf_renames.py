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


def _extract_metadata_title(metadata: dict) -> tuple[str, str]:
    """Extract title from PDF metadata if valid.
    
    Returns:
        Tuple of (title or None, confidence level)
    """
    if not metadata or not metadata.get('title'):
        return None, 'low'
    
    title = metadata['title'].strip()
    if title and len(title) > 3 and not title.startswith('/'):
        return title, 'high'
    return None, 'low'


def _extract_first_page_title(doc) -> tuple[str, str]:
    """Extract title from first page text if valid.
    
    Returns:
        Tuple of (title or None, confidence level)
    """
    if len(doc) == 0:
        return None, 'low'
    
    first_page = doc[0]
    text = first_page.get_text()
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    if not lines:
        return None, 'low'
    
    potential_title = ' '.join(lines[:2])
    if 5 < len(potential_title) < 200:
        return potential_title, 'medium'
    return None, 'low'


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
        
        # Try metadata title first
        title, confidence = _extract_metadata_title(doc.metadata)
        if title:
            result['metadata_title'] = title
            result['confidence'] = confidence
        else:
            # Fall back to first page text
            title, confidence = _extract_first_page_title(doc)
            if title:
                result['first_page_text'] = title
                result['confidence'] = confidence
        
        doc.close()
        
        # Set suggested title from best source
        source_title = result['metadata_title'] or result['first_page_text']
        if source_title:
            result['suggested_title'] = sanitize_filename(source_title)
        
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


def _process_single_pdf(pdf_path: Path) -> dict | None:
    """Process a single PDF file for rename suggestion.
    
    Returns:
        Suggestion dict if file needs renaming, None if already clean
    """
    filename = pdf_path.name
    
    # Check if filename looks messy
    if not is_messy_filename(filename):
        return None
    
    # Extract metadata
    info = extract_title_from_pdf(pdf_path)
    
    if not info['suggested_title']:
        return {
            'original': filename,
            'suggested': None,
            'confidence': 'none',
            'source': 'manual_needed'
        }
    
    new_filename = info['suggested_title'] + '.pdf'
    
    # Don't suggest if same as original
    if new_filename.lower() == filename.lower():
        return None
    
    return {
        'original': filename,
        'suggested': new_filename,
        'confidence': info['confidence'],
        'source': 'metadata' if info['metadata_title'] else 'first_page'
    }


def _print_suggestions_summary(suggestions: list, needs_rename: list, already_clean: list) -> None:
    """Print summary of rename suggestions."""
    print("=" * 80)
    print("RENAME SUGGESTIONS SUMMARY")
    print("=" * 80)
    print(f"\n✅ Already clean filenames: {len(already_clean)}")
    print(f"🔄 Need renaming: {len(needs_rename)}")
    print(f"   - Auto-suggested: {len([s for s in suggestions if s['suggested']])}")
    print(f"   - Manual needed: {len([s for s in needs_rename if not s.get('suggested')])}")


def _print_suggestions_by_confidence(suggestions: list, needs_rename: list) -> None:
    """Print suggestions grouped by confidence level."""
    print("\n" + "=" * 80)
    print("HIGH CONFIDENCE RENAMES (from PDF metadata)")
    print("=" * 80)
    for s in [s for s in suggestions if s['confidence'] == 'high']:
        print(f"\n📄 {s['original']}")
        print(f"   → {s['suggested']}")
    
    print("\n" + "=" * 80)
    print("MEDIUM CONFIDENCE RENAMES (from first page text)")
    print("=" * 80)
    for s in [s for s in suggestions if s['confidence'] == 'medium']:
        print(f"\n📄 {s['original']}")
        print(f"   → {s['suggested']}")
    
    print("\n" + "=" * 80)
    print("MANUAL REVIEW NEEDED (no title found)")
    print("=" * 80)
    for s in [s for s in needs_rename if not s.get('suggested')]:
        print(f"\n❓ {s['original']}")


def _save_suggestions_to_json(
    output_file: str, books_dir: str, already_clean: list, 
    suggestions: list, manual: list
) -> None:
    """Save suggestions to JSON file."""
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


def _print_shell_commands(books_dir: str, suggestions: list) -> None:
    """Print shell commands for renaming files."""
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
        result = _process_single_pdf(pdf_path)
        if result is None:
            already_clean.append(pdf_path.name)
        else:
            needs_rename.append(result)
            if result['suggested']:
                suggestions.append(result)
    
    _print_suggestions_summary(suggestions, needs_rename, already_clean)
    _print_suggestions_by_confidence(suggestions, needs_rename)
    
    manual = [s for s in needs_rename if not s.get('suggested')]
    
    if output_file:
        _save_suggestions_to_json(output_file, books_dir, already_clean, suggestions, manual)
    
    _print_shell_commands(books_dir, suggestions)
    
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
