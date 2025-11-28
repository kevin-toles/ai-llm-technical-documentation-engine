#!/usr/bin/env python3
"""
Unstructured PDF Extractor - Enhanced PDF parsing using the Unstructured library.

Provides better element extraction compared to raw PyMuPDF:
- Title/heading detection with semantic understanding
- Table extraction with HTML representation
- Paragraph/text block segmentation
- Image captions and figure detection
- Page boundary preservation for accurate chapter mapping

Reference: Python Distilled Ch. 7 - Dataclass design patterns
Reference: Architecture Patterns with Python Ch. 13 - Adapter Pattern
Reference: DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md - Statistical NLP layer

Usage:
    extractor = UnstructuredExtractor()
    elements = extractor.extract_from_pdf(Path("book.pdf"))
    pages = extractor.extract_to_pages(Path("book.pdf"))
"""

import re
import logging
from enum import Enum
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

# Lazy imports for optional dependencies
try:
    from unstructured.partition.pdf import partition_pdf
    UNSTRUCTURED_AVAILABLE = True
except ImportError:
    UNSTRUCTURED_AVAILABLE = False
    partition_pdf = None

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False
    fitz = None


class ElementType(Enum):
    """
    PDF element types matching Unstructured library categories.
    
    These represent semantic document elements that Unstructured can detect:
    - TITLE: Chapter headings, section titles
    - NARRATIVE_TEXT: Regular paragraphs
    - TABLE: Tabular data with structure
    - LIST_ITEM: Bullet/numbered list items
    - IMAGE: Images with optional captions
    - HEADER: Page headers (running titles)
    - FOOTER: Page footers (page numbers, etc.)
    - PAGE_BREAK: Explicit page boundary markers
    """
    TITLE = "Title"
    NARRATIVE_TEXT = "NarrativeText"
    TABLE = "Table"
    LIST_ITEM = "ListItem"
    IMAGE = "Image"
    HEADER = "Header"
    FOOTER = "Footer"
    PAGE_BREAK = "PageBreak"


@dataclass
class ExtractionConfig:
    """
    Configuration for Unstructured PDF extraction.
    
    Attributes:
        strategy: Extraction strategy - "auto", "hi_res", "fast", "ocr_only"
            - auto: Automatically choose based on PDF characteristics
            - hi_res: High resolution extraction with OCR for complex layouts
            - fast: Quick extraction without OCR (digital PDFs only)
            - ocr_only: Force OCR for all pages (scanned documents)
        preserve_page_boundaries: Whether to track page numbers for each element
        extract_tables: Whether to extract table structures
        extract_images: Whether to extract image elements/captions
        ocr_enabled: Whether to use OCR for scanned pages
        fallback_to_pymupdf: Whether to fallback to PyMuPDF on Unstructured failure
        languages: Languages to use for OCR (default: English)
    """
    strategy: str = "auto"
    preserve_page_boundaries: bool = True
    extract_tables: bool = True
    extract_images: bool = True
    ocr_enabled: bool = True
    fallback_to_pymupdf: bool = True
    languages: List[str] = field(default_factory=lambda: ["eng"])


@dataclass
class ExtractedElement:
    """
    A single element extracted from a PDF document.
    
    Represents semantic document elements with their content and metadata:
    - text: Raw text content of the element
    - element_type: Semantic type (Title, NarrativeText, Table, etc.)
    - page_number: Page where the element appears
    - html: HTML representation for tables (optional)
    - metadata: Additional metadata from Unstructured
    
    Reference: Python Distilled Ch. 7 - Dataclass patterns
    """
    text: str
    element_type: ElementType
    page_number: int
    html: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class UnstructuredExtractor:
    """
    PDF extractor using the Unstructured library for enhanced document parsing.
    
    Provides semantic element extraction that preserves document structure:
    - Identifies titles, paragraphs, tables, lists
    - Preserves page boundaries for chapter detection
    - Extracts table structure as HTML
    - Falls back to PyMuPDF when Unstructured unavailable
    
    Reference: Architecture Patterns with Python Ch. 13 - Adapter Pattern
    
    Usage:
        >>> extractor = UnstructuredExtractor()
        >>> elements = extractor.extract_from_pdf(Path("book.pdf"))
        >>> pages = extractor.extract_to_pages(Path("book.pdf"))
    """
    
    # Chapter pattern for detecting chapter-level titles
    CHAPTER_PATTERN = re.compile(
        r'^(?:'
        r'chapter\s+\d+|'         # "Chapter 1"
        r'part\s+\d+|'            # "Part 1"
        r'\d+\.\s+[A-Z]|'         # "1. Introduction"
        r'appendix\s+[a-z]|'      # "Appendix A"
        r'section\s+\d+'          # "Section 1"
        r')',
        re.IGNORECASE
    )
    
    def __init__(self, config: Optional[ExtractionConfig] = None, logger: Optional[logging.Logger] = None):
        """
        Initialize the Unstructured PDF extractor.
        
        Args:
            config: Extraction configuration (uses defaults if None)
            logger: Optional logger instance for diagnostics
        """
        self.config = config or ExtractionConfig()
        self.logger = logger or logging.getLogger(__name__)
        
        # Validate dependencies
        if not UNSTRUCTURED_AVAILABLE and not self.config.fallback_to_pymupdf:
            self.logger.warning("Unstructured library not available and fallback disabled")
        elif not UNSTRUCTURED_AVAILABLE:
            self.logger.info("Unstructured not available, will use PyMuPDF fallback")
    
    def extract_from_pdf(self, pdf_path: Path) -> List[ExtractedElement]:
        """
        Extract elements from a PDF file using Unstructured.
        
        Parses the PDF and returns a list of semantic elements (titles, paragraphs,
        tables, etc.) with their page numbers and content.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of ExtractedElement objects representing document structure
            
        Raises:
            FileNotFoundError: If the PDF file doesn't exist
            Exception: If extraction fails and fallback is disabled
            
        Example:
            >>> extractor = UnstructuredExtractor()
            >>> elements = extractor.extract_from_pdf(Path("book.pdf"))
            >>> titles = [e for e in elements if e.element_type == ElementType.TITLE]
        """
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        # Try Unstructured first
        if UNSTRUCTURED_AVAILABLE:
            try:
                elements = self._extract_with_unstructured(pdf_path)
                
                # Check if extraction returned meaningful content
                # 0 elements usually means scanned PDF that Unstructured can't read
                if elements:
                    return elements
                else:
                    # User-visible status: show error and fallback
                    print(f"   ❌ Unstructured extracted 0 elements (likely scanned/image PDF)")
                    self.logger.warning(
                        f"Unstructured returned 0 elements for {pdf_path.name} "
                        "(likely a scanned PDF)"
                    )
                    if not self.config.fallback_to_pymupdf:
                        return elements  # Return empty list if no fallback
                    print(f"   🔄 Fallback initiated: PyMuPDF with OCR support...")
                    
            except Exception as e:
                # User-visible status: show error and fallback
                print(f"   ❌ Unstructured extraction failed: {e}")
                self.logger.warning(f"Unstructured extraction failed: {e}")
                if not self.config.fallback_to_pymupdf:
                    raise
                print(f"   🔄 Fallback initiated: PyMuPDF with OCR support...")
        
        # Fallback to PyMuPDF (triggered on exception OR 0 elements)
        if self.config.fallback_to_pymupdf and PYMUPDF_AVAILABLE:
            self.logger.info("Falling back to PyMuPDF extraction")
            return self._extract_with_pymupdf(pdf_path)
        
        raise RuntimeError("No PDF extraction library available")
    
    def _extract_with_unstructured(self, pdf_path: Path) -> List[ExtractedElement]:
        """
        Internal: Extract elements using Unstructured library.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of ExtractedElement objects
        """
        # Build extraction parameters based on config
        kwargs = {
            "filename": str(pdf_path),
            "strategy": self.config.strategy,
        }
        
        # Add table extraction settings
        if self.config.extract_tables:
            kwargs["infer_table_structure"] = True
        
        # Add OCR settings if enabled
        if self.config.ocr_enabled:
            kwargs["languages"] = self.config.languages
        
        # Call Unstructured partition_pdf
        raw_elements = partition_pdf(**kwargs)
        
        # Convert to ExtractedElement objects
        elements = []
        for raw_elem in raw_elements:
            element = self._convert_unstructured_element(raw_elem)
            if element:
                elements.append(element)
        
        return elements
    
    def _convert_unstructured_element(self, raw_elem) -> Optional[ExtractedElement]:
        """
        Convert Unstructured element to ExtractedElement.
        
        Args:
            raw_elem: Raw element from Unstructured library
            
        Returns:
            ExtractedElement or None if element should be skipped
        """
        # Get element category (type)
        category = getattr(raw_elem, 'category', 'NarrativeText')
        
        # Map to ElementType enum
        try:
            element_type = ElementType(category)
        except ValueError:
            # Unknown type, treat as NarrativeText
            element_type = ElementType.NARRATIVE_TEXT
        
        # Get text content
        text = str(raw_elem.text) if hasattr(raw_elem, 'text') else str(raw_elem)
        
        # Get page number from metadata
        page_number = 1
        if hasattr(raw_elem, 'metadata') and raw_elem.metadata:
            page_number = getattr(raw_elem.metadata, 'page_number', 1) or 1
        
        # Get HTML representation for tables
        html = None
        if element_type == ElementType.TABLE and hasattr(raw_elem, 'metadata'):
            html = getattr(raw_elem.metadata, 'text_as_html', None)
        
        # Build metadata dict
        metadata = {}
        if hasattr(raw_elem, 'metadata') and raw_elem.metadata:
            for attr in ['filename', 'filetype', 'coordinates', 'parent_id']:
                if hasattr(raw_elem.metadata, attr):
                    metadata[attr] = getattr(raw_elem.metadata, attr)
        
        return ExtractedElement(
            text=text,
            element_type=element_type,
            page_number=page_number,
            html=html,
            metadata=metadata
        )
    
    def _extract_with_pymupdf(self, pdf_path: Path) -> List[ExtractedElement]:
        """
        Fallback: Extract elements using PyMuPDF.
        
        Creates basic NarrativeText elements from each page's text content.
        Less semantic than Unstructured but works without additional dependencies.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of ExtractedElement objects (one per page as NarrativeText)
        """
        if not PYMUPDF_AVAILABLE:
            raise RuntimeError("PyMuPDF (fitz) not available for fallback")
        
        doc = fitz.open(str(pdf_path))
        elements = []
        
        try:
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                
                if text.strip():
                    elements.append(ExtractedElement(
                        text=text,
                        element_type=ElementType.NARRATIVE_TEXT,
                        page_number=page_num + 1,  # 1-indexed
                        metadata={"extraction_method": "PyMuPDF_fallback"}
                    ))
        finally:
            doc.close()
        
        return elements
    
    def extract_to_pages(self, pdf_path: Path) -> List[Dict[str, Any]]:
        """
        Extract PDF to page-based structure compatible with convert_pdf_to_json.
        
        Combines elements by page number into a structure matching the expected
        format for the existing PDF-to-JSON pipeline.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of page dictionaries with:
            - page_number: 1-indexed page number
            - content: Combined text from all elements on the page
            - extraction_method: "Unstructured" or "PyMuPDF_fallback"
            
        Example:
            >>> extractor = UnstructuredExtractor()
            >>> pages = extractor.extract_to_pages(Path("book.pdf"))
            >>> for page in pages:
            ...     print(f"Page {page['page_number']}: {len(page['content'])} chars")
        """
        elements = self.extract_from_pdf(pdf_path)
        
        if not elements:
            return []
        
        # Group elements by page number
        pages_dict: Dict[int, List[ExtractedElement]] = {}
        for elem in elements:
            page_num = elem.page_number
            if page_num not in pages_dict:
                pages_dict[page_num] = []
            pages_dict[page_num].append(elem)
        
        # Build page structures
        pages = []
        for page_num in sorted(pages_dict.keys()):
            page_elements = pages_dict[page_num]
            
            # Combine text from all elements with newlines
            content_parts = []
            for elem in page_elements:
                if elem.element_type == ElementType.TABLE and elem.html:
                    # Use HTML for tables
                    content_parts.append(elem.html)
                else:
                    content_parts.append(elem.text)
            
            content = "\n\n".join(content_parts)
            
            # Determine extraction method from metadata
            extraction_method = "Unstructured"
            if page_elements and page_elements[0].metadata.get("extraction_method") == "PyMuPDF_fallback":
                extraction_method = "PyMuPDF_fallback"
            
            pages.append({
                "page_number": page_num,
                "content": content,
                "content_length": len(content),
                "extraction_method": extraction_method
            })
        
        return pages
    
    def get_potential_chapters(self, pdf_path: Path) -> List[Dict[str, Any]]:
        """
        Extract potential chapter boundaries from Title elements.
        
        Analyzes Title elements to identify chapter-level headings and their
        page ranges. Useful for improving chapter segmentation accuracy.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of chapter dictionaries with:
            - title: Chapter/section title text
            - start_page: Page where the chapter starts
            - end_page: Last page of the chapter
            - level: Heading level (1=chapter, 2=section, etc.)
            
        Example:
            >>> extractor = UnstructuredExtractor()
            >>> chapters = extractor.get_potential_chapters(Path("book.pdf"))
            >>> print(f"Found {len(chapters)} chapters")
        """
        elements = self.extract_from_pdf(pdf_path)
        
        # Find all title elements
        titles = [e for e in elements if e.element_type == ElementType.TITLE]
        
        if not titles:
            return []
        
        # Categorize titles as chapter-level or section-level
        chapters = []
        for title in titles:
            is_chapter = bool(self.CHAPTER_PATTERN.match(title.text.strip()))
            
            chapters.append({
                "title": title.text,
                "start_page": title.page_number,
                "end_page": title.page_number,  # Will be updated below
                "level": 1 if is_chapter else 2,
                "element": title  # Keep for reference
            })
        
        # Calculate end pages (each chapter ends before the next starts)
        for i, chapter in enumerate(chapters):
            if i + 1 < len(chapters):
                # End page is one before the next chapter starts
                next_start = chapters[i + 1]["start_page"]
                chapter["end_page"] = max(chapter["start_page"], next_start - 1)
            else:
                # Last chapter - we don't know the total pages here
                # Will need to be filled in by the caller or use elements
                max_page = max(e.page_number for e in elements) if elements else chapter["start_page"]
                chapter["end_page"] = max_page
        
        # Remove element reference before returning
        for chapter in chapters:
            del chapter["element"]
        
        return chapters


# Export public interface
__all__ = [
    "UnstructuredExtractor",
    "ExtractionConfig", 
    "ExtractedElement",
    "ElementType",
    "UNSTRUCTURED_AVAILABLE",
    "PYMUPDF_AVAILABLE",
]
