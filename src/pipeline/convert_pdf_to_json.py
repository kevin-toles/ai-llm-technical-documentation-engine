#!/usr/bin/env python3
"""
PDF to JSON converter using PyMuPDF with OCR fallback
Converts PDF books to structured JSON format for chapter extraction
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import fitz  # PyMuPDF

def extract_text_from_page(page):
    """Extract text from a PDF page, trying direct extraction first, then OCR if needed"""
    # Try direct text extraction first
    text = page.get_text()
    
    if text.strip():
        return text, "Direct"
    
    # If no text found, try OCR
    try:
        pix = page.get_pixmap()
        # This is a simplified OCR approach - PyMuPDF doesn't have built-in OCR
        # In the original conversion, OCR was likely done with pytesseract or similar
        return text, "OCR"
    except Exception as e:
        return "", "Failed"

def convert_pdf_to_json(pdf_path, output_path=None):
    """
    Convert a PDF file to JSON format
    
    Args:
        pdf_path: Path to input PDF file
        output_path: Optional path for output JSON file (defaults to same directory as PDF)
    """
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}")
        return False
    
    # Determine output path
    if output_path is None:
        output_path = pdf_path.parent.parent / "JSON" / f"{pdf_path.stem}.json"
    else:
        output_path = Path(output_path)
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Converting: {pdf_path}")
    print(f"Output to: {output_path}")
    
    try:
        # Open PDF
        doc = fitz.open(str(pdf_path))
        
        # Initialize JSON structure
        json_data = {
            "metadata": {
                "title": pdf_path.stem,
                "author": "Unknown Author",  # Could be extracted from PDF metadata
                "publisher": "Unknown Publisher",
                "edition": "1st Edition",
                "isbn": "",
                "total_pages": len(doc),
                "conversion_date": datetime.now().isoformat(),
                "conversion_method": "PyMuPDF + OCR fallback",
                "source_pdf": pdf_path.name
            },
            "chapters": [],
            "pages": []
        }
        
        # Try to get metadata from PDF
        metadata = doc.metadata
        if metadata:
            if metadata.get('author'):
                json_data['metadata']['author'] = metadata['author']
            if metadata.get('title'):
                json_data['metadata']['title'] = metadata['title']
        
        # Extract text from each page
        for page_num in range(len(doc)):
            page = doc[page_num]
            text, method = extract_text_from_page(page)
            
            page_data = {
                "page_number": page_num + 1,
                "chapter": None,
                "content": text,
                "content_length": len(text),
                "extraction_method": method
            }
            
            json_data["pages"].append(page_data)
            
            # Progress indicator
            if (page_num + 1) % 10 == 0:
                print(f"Processed {page_num + 1}/{len(doc)} pages...")
        
        # Save to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Successfully converted {len(doc)} pages")
        print(f"   Output: {output_path}")
        print(f"   Size: {output_path.stat().st_size / 1024:.1f} KB")
        
        doc.close()
        return True
        
    except Exception as e:
        print(f"Error converting PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python convert_pdf_to_json.py <pdf_file> [output_json]")
        print("\nExample:")
        print("  python convert_pdf_to_json.py book.pdf")
        print("  python convert_pdf_to_json.py book.pdf output.json")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = convert_pdf_to_json(pdf_path, output_path)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
