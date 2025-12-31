#!/usr/bin/env python3
"""
PDF to JSON converter using Unstructured library with PyMuPDF fallback.

Converts PDF books to structured JSON format using:
- Unstructured library for semantic element extraction (titles, paragraphs, tables)
- PyMuPDF/OCR fallback for scanned or problematic PDFs
- 3-pass chapter detection (regex → topic-shift → synthetic)
- YAKE keyword validation for chapter boundaries
- TF-IDF cosine similarity for topic shift detection

Reference: Python Distilled Ch. 9 - pathlib.Path operations
Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md - Tab 1 statistical methods only
Reference: DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md - Unstructured integration
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple

import fitz  # type: ignore[import-untyped]  # PyMuPDF

# OCR support for scanned PDFs
try:
    import pytesseract  # type: ignore[import-untyped]
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("Warning: pytesseract not available. Install with: pip install pytesseract pillow")

# Add project root to path for config access
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Configuration management (Microservices Up and Running Ch. 7 - 12-Factor Config)
from config.settings import settings  # noqa: E402

# Import statistical chapter segmenter (NEW - replaces detect_chapters_intelligent)
from workflows.pdf_to_json.scripts.chapter_segmenter import ChapterSegmenter  # noqa: E402

# Import Unstructured extractor for enhanced PDF parsing
from workflows.pdf_to_json.scripts.adapters.unstructured_extractor import (  # noqa: E402
    UnstructuredExtractor,
    ExtractionConfig,
    UNSTRUCTURED_AVAILABLE,
)


def _extract_pdf_metadata(doc, pdf_path: Path) -> Dict:
    """Extract metadata from PDF document.
    
    Args:
        doc: PyMuPDF document object
        pdf_path: Path to source PDF file
        
    Returns:
        Dictionary with metadata fields
    """
    metadata = {
        "title": pdf_path.stem,
        "author": "Unknown Author",
        "publisher": "Unknown Publisher",
        "edition": "1st Edition",
        "isbn": "",
        "total_pages": len(doc),
        "conversion_date": datetime.now().isoformat(),
        "conversion_method": "PyMuPDF + OCR fallback",
        "source_pdf": pdf_path.name
    }
    
    # Try to get metadata from PDF (author only - title always uses filename for consistency)
    # Note: PDF embedded titles are often inconsistent (e.g., "AI Engineering (for True Epub)")
    # Using filename ensures consistency with taxonomy and cross-reference systems
    pdf_metadata = doc.metadata
    if pdf_metadata and pdf_metadata.get('author'):
        metadata['author'] = pdf_metadata['author']
        # Intentionally NOT using pdf_metadata['title'] - filename is the canonical title
    
    return metadata


def _populate_chapter_content(chapters: List[Dict], pages: List[Dict]) -> None:
    """Populate chapter content from page ranges.
    
    Args:
        chapters: List of chapter dictionaries to populate
        pages: List of page dictionaries with content
    """
    print("\n📝 Extracting chapter content from pages...")
    for chapter in chapters:
        start_page = chapter.get("start_page", 1)
        end_page = chapter.get("end_page", start_page)
        
        # Extract content from all pages in the chapter range
        chapter_text = []
        for page_num in range(start_page, end_page + 1):
            # Pages are 1-indexed in chapter metadata, 0-indexed in array
            page_idx = page_num - 1
            if 0 <= page_idx < len(pages):
                page_content = pages[page_idx].get("content", "")
                if page_content.strip():
                    chapter_text.append(page_content)
        
        # Join all page content with double newline separator
        chapter["content"] = "\n\n".join(chapter_text)
        chapter["page_number"] = start_page  # Add page_number field for compatibility


def _print_chapter_summary(chapters: List[Dict]) -> None:
    """Print summary of detected chapters.
    
    Args:
        chapters: List of chapter dictionaries
    """
    print(f"✅ Detected {len(chapters)} chapters:")
    for ch in chapters[:5]:
        method_emoji = {
            'regex_chapter': '📝', 
            'regex_item': '📋',
            'regex_numeric': '🔢',
            'topic_boundary': '🎯',
            'synthetic': '⚙️'
        }.get(ch['detection_method'], '❓')
        print(f"   {method_emoji} Chapter {ch['number']}: {ch['title'][:50]}... (pages {ch['start_page']}-{ch['end_page']})")
    if len(chapters) > 5:
        print(f"   ... and {len(chapters) - 5} more chapters")


def extract_text_from_page(page) -> Tuple[str, str]:
    """
    Extract text from a PDF page using direct extraction or OCR fallback.
    
    Handles both digital PDFs (with embedded text) and scanned PDFs (images).
    Uses Tesseract OCR for scanned pages when pytesseract is available.
    
    Args:
        page: PyMuPDF page object
        
    Returns:
        Tuple of (text_content, extraction_method)
        - text_content: Extracted text string
        - extraction_method: "Direct", "OCR", or "Failed"
        
    Reference: Python Distilled Ch. 9 - I/O operations with fallback strategies
    """
    # Try direct text extraction first (fastest for digital PDFs)
    text = page.get_text()
    
    if text.strip():
        return text, "Direct"
    
    # No text found - likely a scanned page, try OCR
    if not OCR_AVAILABLE:
        return "", "Failed"
    
    try:
        # Convert PDF page to image
        # Reference: PyMuPDF docs - higher DPI = better OCR accuracy
        pix = page.get_pixmap(dpi=300)  # 300 DPI for good OCR quality
        
        # Convert to PIL Image for pytesseract
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        
        # Run OCR with English language model
        # Reference: pytesseract docs - PSM 3 is more reliable than PSM 1 for batch processing
        # PSM 1 (OSD) can hang on blank pages, rotated pages, or complex layouts
        # PSM 3 (fully automatic) is faster and more robust for books
        ocr_text = pytesseract.image_to_string(
            img,
            lang='eng',
            config='--psm 3',  # PSM 3 = Fully automatic page segmentation (no OSD)
            timeout=30  # 30 second timeout as safety net
        )
        
        # Explicit cleanup to prevent resource leaks over hundreds of pages
        del img
        del pix
        
        return ocr_text.strip(), "OCR"
        
    except pytesseract.TesseractError as e:
        print(f"Warning: Tesseract error for page {page.number + 1}: {e}")
        return "", "Failed"
    except Exception as e:
        print(f"Warning: OCR failed for page {page.number + 1}: {e}")
        return "", "Failed"

def convert_pdf_to_json(pdf_path, output_path=None, use_unstructured=True):
    """
    Convert a PDF file to JSON format.
    
    Uses Unstructured library for enhanced semantic extraction (titles, paragraphs,
    tables) with PyMuPDF fallback for scanned or problematic PDFs.
    
    Args:
        pdf_path: Path to input PDF file
        output_path: Optional path for output JSON file (defaults to same directory as PDF)
        use_unstructured: Whether to try Unstructured first (default: True)
    """
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}")
        return False
    
    # Determine output path
    # Reference: Python Distilled Ch. 9 pp. 225-230 - Path operations
    if output_path is None:
        # Use PathConfig for centralized path management (12-Factor App)
        output_path = settings.paths.textbooks_json_dir / f"{pdf_path.stem}.json"
    else:
        output_path = Path(output_path)
        # If output_path is a directory, append the filename
        if output_path.is_dir():
            output_path = output_path / f"{pdf_path.stem}.json"
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Converting: {pdf_path}")
    print(f"Output to: {output_path}")
    
    try:
        # Try Unstructured extraction first (better semantic parsing)
        if use_unstructured and UNSTRUCTURED_AVAILABLE:
            print("\n📚 Using Unstructured library for enhanced PDF parsing...")
            pages, extraction_method = _extract_with_unstructured(pdf_path)
        else:
            # Fall back to PyMuPDF extraction
            if use_unstructured:
                print("\n⚠️ Unstructured not available, falling back to PyMuPDF...")
            else:
                print("\n📄 Using PyMuPDF for PDF extraction...")
            pages, extraction_method = _extract_with_pymupdf(pdf_path)
        
        # Open PDF for metadata extraction (always use PyMuPDF for this)
        doc = fitz.open(str(pdf_path))
        
        # Initialize JSON structure
        json_data = {
            "metadata": _extract_pdf_metadata(doc, pdf_path),
            "chapters": [],
            "pages": pages
        }
        
        # Update metadata with extraction method
        json_data["metadata"]["extraction_method"] = extraction_method
        
        doc.close()
        
        # Auto-detect chapters from page content using 3-pass statistical algorithm
        print("\n🔍 Detecting chapters (3-pass: regex → topic-shift → synthetic)...")
        segmenter = ChapterSegmenter(settings.chapter_segmentation)
        detected_chapters = segmenter.segment_book(json_data["pages"])
        
        # ChapterSegmenter already returns dicts (converted internally)
        json_data["chapters"] = detected_chapters
        
        # Populate chapter content from page ranges
        _populate_chapter_content(json_data["chapters"], json_data["pages"])
        
        # Print summary of detected chapters
        _print_chapter_summary(json_data["chapters"])
        
        # Save to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Successfully converted {len(pages)} pages")
        print(f"   Output: {output_path}")
        print(f"   Size: {output_path.stat().st_size / 1024:.1f} KB")
        
        return True
        
    except Exception as e:
        print(f"Error converting PDF: {e}")
        import traceback
        traceback.print_exc()
        return False


def _extract_with_unstructured(pdf_path: Path) -> Tuple[List[Dict], str]:
    """
    Extract pages using Unstructured library for enhanced semantic parsing.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Tuple of (pages list, extraction_method string)
    """
    config = ExtractionConfig(
        strategy="fast",  # Use fast strategy for quicker processing
        extract_tables=True,
        extract_images=False,  # Skip image extraction for speed
        ocr_enabled=False,  # Disable OCR for speed (use PyMuPDF fallback for scanned PDFs)
        fallback_to_pymupdf=True
    )
    extractor = UnstructuredExtractor(config=config)
    
    # Get pages with combined element content
    pages = extractor.extract_to_pages(pdf_path)
    
    # Determine extraction method from first page metadata
    if pages and pages[0].get("extraction_method") == "PyMuPDF_fallback":
        print(f"   ✅ Fallback successful: Extracted {len(pages)} pages with PyMuPDF")
        return pages, "PyMuPDF_fallback (Unstructured failed)"
    elif not pages:
        print("   ⚠️ Warning: No pages extracted from PDF")
        return pages, "Failed - No content extracted"
    else:
        print(f"   📄 Extracted {len(pages)} pages with Unstructured")
        return pages, "Unstructured"


def _extract_with_pymupdf(pdf_path: Path) -> Tuple[List[Dict], str]:
    """
    Extract pages using PyMuPDF with OCR fallback for scanned pages.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Tuple of (pages list, extraction_method string)
    """
    doc = fitz.open(str(pdf_path))
    pages = []
    ocr_count = 0
    direct_count = 0
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text, method = extract_text_from_page(page)
        
        # Track extraction methods
        if method == "OCR":
            ocr_count += 1
        elif method == "Direct":
            direct_count += 1
        
        page_data = {
            "page_number": page_num + 1,
            "chapter": None,
            "content": text,
            "content_length": len(text),
            "extraction_method": method
        }
        
        pages.append(page_data)
        
        # Progress indicator (more frequent for OCR pages since they're slower)
        if method == "OCR" or (page_num + 1) % 10 == 0:
            progress = f"Processed {page_num + 1}/{len(doc)} pages"
            if ocr_count > 0:
                progress += f" (OCR: {ocr_count}, Direct: {direct_count})"
            print(progress)
    
    doc.close()
    
    # Summary of extraction methods
    failed_count = len(pages) - direct_count - ocr_count
    print(f"\n📄 Extraction complete: {direct_count} direct, {ocr_count} OCR, {failed_count} failed")
    
    return pages, f"PyMuPDF (Direct: {direct_count}, OCR: {ocr_count})"

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
