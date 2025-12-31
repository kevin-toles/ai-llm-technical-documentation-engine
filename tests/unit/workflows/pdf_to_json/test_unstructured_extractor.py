#!/usr/bin/env python3
"""
Unit tests for UnstructuredExtractor - TDD GREEN phase.

Tests PDF parsing using the Unstructured library for improved element extraction:
- Title/heading detection
- Table extraction
- Paragraph/text blocks
- Image captions
- Page boundary preservation

Reference: Python Testing with pytest Ch. 4 - Fixtures
Reference: DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md - TDD approach
Reference: Architecture Patterns with Python Ch. 5 - Service Layer testing
"""

import pytest
from pathlib import Path
from typing import List, Dict, Any
from unittest.mock import Mock, patch, MagicMock
from dataclasses import dataclass


# TDD: Import will fail until implementation exists
try:
    from workflows.pdf_to_json.scripts.adapters.unstructured_extractor import (
        UnstructuredExtractor,
        ExtractionConfig,
        ExtractedElement,
        ElementType,
        UNSTRUCTURED_AVAILABLE,
        PYMUPDF_AVAILABLE,
    )
except ImportError:
    # Placeholder for TDD - will fail until implementation
    UnstructuredExtractor = None
    ExtractionConfig = None
    ExtractedElement = None
    ElementType = None
    UNSTRUCTURED_AVAILABLE = False
    PYMUPDF_AVAILABLE = False


# Module path for patching
MODULE_PATH = 'workflows.pdf_to_json.scripts.adapters.unstructured_extractor'


@pytest.fixture
def sample_pdf_path(tmp_path) -> Path:
    """Create a temp file path for testing (actual PDF not needed for mocked tests)."""
    pdf_path = tmp_path / "test_document.pdf"
    pdf_path.write_bytes(b"%PDF-1.4 mock content")
    return pdf_path


@pytest.fixture
def mock_unstructured_elements_raw():
    """
    Create raw mock element data that simulates Unstructured library output.
    
    These represent the element types Unstructured can extract:
    - Title: Chapter/section headings
    - NarrativeText: Regular paragraphs
    - Table: Extracted tables with structure
    - ListItem: Bullet/numbered list items
    """
    return [
        {"type": "Title", "text": "Chapter 1: Introduction", "metadata": {"page_number": 1}},
        {"type": "NarrativeText", "text": "This is the introduction paragraph with important content about the topic.", "metadata": {"page_number": 1}},
        {"type": "NarrativeText", "text": "Another paragraph explaining key concepts in detail.", "metadata": {"page_number": 1}},
        {"type": "Title", "text": "1.1 Background", "metadata": {"page_number": 2}},
        {"type": "NarrativeText", "text": "Background information about the subject matter.", "metadata": {"page_number": 2}},
        {"type": "Table", "text": "| Name | Value |\n| Item1 | 100 |", "metadata": {"page_number": 2, "text_as_html": "<table><tr><td>Name</td><td>Value</td></tr></table>"}},
        {"type": "ListItem", "text": "First bullet point", "metadata": {"page_number": 3}},
        {"type": "ListItem", "text": "Second bullet point", "metadata": {"page_number": 3}},
        {"type": "Title", "text": "Chapter 2: Methods", "metadata": {"page_number": 4}},
        {"type": "NarrativeText", "text": "Description of the methodology used in this work.", "metadata": {"page_number": 4}},
    ]


@pytest.fixture
def mock_partition_elements(mock_unstructured_elements_raw):
    """Convert raw element data to mock objects that simulate Unstructured's output."""
    mock_elements = []
    for elem_data in mock_unstructured_elements_raw:
        mock_elem = Mock()
        mock_elem.category = elem_data["type"]
        mock_elem.text = elem_data["text"]
        mock_elem.metadata = Mock()
        mock_elem.metadata.page_number = elem_data["metadata"]["page_number"]
        mock_elem.metadata.text_as_html = elem_data["metadata"].get("text_as_html")
        # Add other metadata attributes that might be accessed
        mock_elem.metadata.filename = None
        mock_elem.metadata.filetype = None
        mock_elem.metadata.coordinates = None
        mock_elem.metadata.parent_id = None
        mock_elements.append(mock_elem)
    return mock_elements


class TestUnstructuredExtractorImport:
    """Test that the module can be imported correctly."""
    
    def test_unstructured_extractor_class_exists(self):
        """Verify UnstructuredExtractor class is importable."""
        assert UnstructuredExtractor is not None, "UnstructuredExtractor class not found - implement the class first"
    
    def test_extraction_config_exists(self):
        """Verify ExtractionConfig dataclass is importable."""
        assert ExtractionConfig is not None, "ExtractionConfig dataclass not found"
    
    def test_extracted_element_exists(self):
        """Verify ExtractedElement dataclass is importable."""
        assert ExtractedElement is not None, "ExtractedElement dataclass not found"
    
    def test_element_type_enum_exists(self):
        """Verify ElementType enum is importable."""
        assert ElementType is not None, "ElementType enum not found"


@pytest.mark.skipif(UnstructuredExtractor is None, reason="UnstructuredExtractor not implemented yet")
class TestExtractionConfig:
    """Test ExtractionConfig dataclass with default and custom values."""
    
    def test_default_config_values(self):
        """Verify default configuration values are sensible."""
        config = ExtractionConfig()
        
        # Default extraction strategy
        assert config.strategy == "auto"  # auto, hi_res, fast, ocr_only
        
        # Page boundaries should be preserved by default
        assert config.preserve_page_boundaries is True
        
        # Table extraction should be enabled
        assert config.extract_tables is True
        
        # Image extraction (captions) should be enabled
        assert config.extract_images is True
        
        # OCR fallback should be enabled
        assert config.ocr_enabled is True
    
    def test_custom_config_values(self):
        """Verify custom configuration is applied."""
        config = ExtractionConfig(
            strategy="hi_res",
            preserve_page_boundaries=False,
            extract_tables=False,
            extract_images=False,
            ocr_enabled=False
        )
        
        assert config.strategy == "hi_res"
        assert config.preserve_page_boundaries is False
        assert config.extract_tables is False
        assert config.extract_images is False
        assert config.ocr_enabled is False


@pytest.mark.skipif(UnstructuredExtractor is None, reason="UnstructuredExtractor not implemented yet")
class TestElementType:
    """Test ElementType enum for PDF element classification."""
    
    def test_element_types_defined(self):
        """Verify all expected element types are defined."""
        expected_types = ["TITLE", "NARRATIVE_TEXT", "TABLE", "LIST_ITEM", "IMAGE", "HEADER", "FOOTER", "PAGE_BREAK"]
        
        for type_name in expected_types:
            assert hasattr(ElementType, type_name), f"ElementType.{type_name} not found"
    
    def test_element_type_values(self):
        """Verify element type values are strings matching Unstructured output."""
        assert ElementType.TITLE.value == "Title"
        assert ElementType.NARRATIVE_TEXT.value == "NarrativeText"
        assert ElementType.TABLE.value == "Table"
        assert ElementType.LIST_ITEM.value == "ListItem"


@pytest.mark.skipif(UnstructuredExtractor is None, reason="UnstructuredExtractor not implemented yet")
class TestUnstructuredExtractorInitialization:
    """Test UnstructuredExtractor initialization."""
    
    def test_default_initialization(self):
        """Verify extractor initializes with default config."""
        extractor = UnstructuredExtractor()
        
        assert extractor.config is not None
        assert isinstance(extractor.config, ExtractionConfig)
    
    def test_custom_config_initialization(self):
        """Verify extractor initializes with custom config."""
        config = ExtractionConfig(strategy="fast", extract_tables=False)
        extractor = UnstructuredExtractor(config=config)
        
        assert extractor.config.strategy == "fast"
        assert extractor.config.extract_tables is False


@pytest.mark.skipif(UnstructuredExtractor is None, reason="UnstructuredExtractor not implemented yet")
class TestUnstructuredExtractorExtraction:
    """Test UnstructuredExtractor PDF extraction methods."""
    
    def test_extract_from_pdf_returns_elements(self, sample_pdf_path, mock_partition_elements, mock_unstructured_elements_raw):
        """Verify extraction returns list of ExtractedElement objects."""
        with patch(f'{MODULE_PATH}.UNSTRUCTURED_AVAILABLE', True):
            with patch(f'{MODULE_PATH}.partition_pdf', return_value=mock_partition_elements):
                extractor = UnstructuredExtractor()
                elements = extractor.extract_from_pdf(sample_pdf_path)
        
        assert isinstance(elements, list)
        assert len(elements) == len(mock_unstructured_elements_raw)
        assert all(isinstance(e, ExtractedElement) for e in elements)
    
    def test_extract_preserves_page_numbers(self, sample_pdf_path, mock_partition_elements, mock_unstructured_elements_raw):
        """Verify page numbers are preserved in extracted elements."""
        with patch(f'{MODULE_PATH}.UNSTRUCTURED_AVAILABLE', True):
            with patch(f'{MODULE_PATH}.partition_pdf', return_value=mock_partition_elements):
                extractor = UnstructuredExtractor()
                elements = extractor.extract_from_pdf(sample_pdf_path)
        
        # Verify page numbers match expected values
        page_numbers = [e.page_number for e in elements]
        expected_pages = [elem["metadata"]["page_number"] for elem in mock_unstructured_elements_raw]
        assert page_numbers == expected_pages
    
    def test_extract_identifies_titles(self, sample_pdf_path, mock_partition_elements):
        """Verify title elements are correctly identified."""
        with patch(f'{MODULE_PATH}.UNSTRUCTURED_AVAILABLE', True):
            with patch(f'{MODULE_PATH}.partition_pdf', return_value=mock_partition_elements):
                extractor = UnstructuredExtractor()
                elements = extractor.extract_from_pdf(sample_pdf_path)
        
        titles = [e for e in elements if e.element_type == ElementType.TITLE]
        assert len(titles) == 3  # "Chapter 1", "1.1 Background", "Chapter 2"
        assert titles[0].text == "Chapter 1: Introduction"
    
    def test_extract_identifies_tables(self, sample_pdf_path, mock_partition_elements):
        """Verify table elements are correctly extracted with HTML representation."""
        with patch(f'{MODULE_PATH}.UNSTRUCTURED_AVAILABLE', True):
            with patch(f'{MODULE_PATH}.partition_pdf', return_value=mock_partition_elements):
                extractor = UnstructuredExtractor()
                elements = extractor.extract_from_pdf(sample_pdf_path)
        
        tables = [e for e in elements if e.element_type == ElementType.TABLE]
        assert len(tables) == 1
        assert tables[0].html is not None  # Tables should have HTML representation


@pytest.mark.skipif(UnstructuredExtractor is None, reason="UnstructuredExtractor not implemented yet")
class TestUnstructuredExtractorToPages:
    """Test conversion of extracted elements to page-based structure."""
    
    def test_convert_to_pages_structure(self, sample_pdf_path, mock_partition_elements):
        """Verify elements can be converted to page-based dict structure."""
        with patch(f'{MODULE_PATH}.UNSTRUCTURED_AVAILABLE', True):
            with patch(f'{MODULE_PATH}.partition_pdf', return_value=mock_partition_elements):
                extractor = UnstructuredExtractor()
                pages = extractor.extract_to_pages(sample_pdf_path)
        
        assert isinstance(pages, list)
        # Should have 4 pages based on mock data (pages 1, 2, 3, 4)
        assert len(pages) == 4
        
        # Each page should have page_number and content
        for page in pages:
            assert "page_number" in page
            assert "content" in page
            assert "extraction_method" in page
            assert page["extraction_method"] == "Unstructured"
    
    def test_pages_content_combined_from_elements(self, sample_pdf_path, mock_partition_elements):
        """Verify page content is correctly combined from multiple elements."""
        with patch(f'{MODULE_PATH}.UNSTRUCTURED_AVAILABLE', True):
            with patch(f'{MODULE_PATH}.partition_pdf', return_value=mock_partition_elements):
                extractor = UnstructuredExtractor()
                pages = extractor.extract_to_pages(sample_pdf_path)
        
        # Page 1 should contain content from Title and two NarrativeText elements
        page_1 = pages[0]
        assert "Chapter 1: Introduction" in page_1["content"]
        assert "introduction paragraph" in page_1["content"]
        assert "key concepts" in page_1["content"]


@pytest.mark.skipif(UnstructuredExtractor is None, reason="UnstructuredExtractor not implemented yet")
class TestUnstructuredExtractorErrorHandling:
    """Test error handling in UnstructuredExtractor."""
    
    def test_file_not_found_raises_error(self, tmp_path):
        """Verify FileNotFoundError for missing PDF."""
        extractor = UnstructuredExtractor()
        non_existent = tmp_path / "missing.pdf"
        
        with pytest.raises(FileNotFoundError):
            extractor.extract_from_pdf(non_existent)
    
    def test_invalid_pdf_raises_error(self, tmp_path):
        """Verify appropriate error for corrupted/invalid PDF."""
        config = ExtractionConfig(fallback_to_pymupdf=False)  # Disable fallback
        invalid_pdf = tmp_path / "invalid.pdf"
        invalid_pdf.write_text("This is not a PDF file")
        
        with patch(f'{MODULE_PATH}.UNSTRUCTURED_AVAILABLE', True):
            with patch(f'{MODULE_PATH}.partition_pdf') as mock_partition:
                mock_partition.side_effect = Exception("Invalid PDF format")
                
                extractor = UnstructuredExtractor(config=config)
                with pytest.raises(Exception) as exc_info:
                    extractor.extract_from_pdf(invalid_pdf)
                
                assert "Invalid PDF" in str(exc_info.value)
    
    def test_empty_pdf_returns_empty_list(self, sample_pdf_path):
        """Verify empty PDF returns empty element list without error.
        
        When Unstructured returns 0 elements and fallback is disabled,
        we should get an empty list back instead of triggering PyMuPDF.
        """
        config = ExtractionConfig(fallback_to_pymupdf=False)  # Disable fallback
        with patch(f'{MODULE_PATH}.UNSTRUCTURED_AVAILABLE', True):
            with patch(f'{MODULE_PATH}.partition_pdf', return_value=[]):
                extractor = UnstructuredExtractor(config=config)
                elements = extractor.extract_from_pdf(sample_pdf_path)
        
        assert elements == []


@pytest.mark.skipif(UnstructuredExtractor is None, reason="UnstructuredExtractor not implemented yet")
class TestUnstructuredExtractorWithPyMuPDFFallback:
    """Test fallback to PyMuPDF when Unstructured fails."""
    
    def test_fallback_on_extraction_failure(self, sample_pdf_path):
        """Verify fallback to PyMuPDF extraction when Unstructured fails."""
        config = ExtractionConfig(fallback_to_pymupdf=True)
        
        with patch(f'{MODULE_PATH}.UNSTRUCTURED_AVAILABLE', True):
            with patch(f'{MODULE_PATH}.partition_pdf') as mock_partition:
                mock_partition.side_effect = Exception("Unstructured failed")
                
                with patch(f'{MODULE_PATH}.PYMUPDF_AVAILABLE', True):
                    with patch(f'{MODULE_PATH}.fitz') as mock_fitz:
                        # Mock PyMuPDF fallback
                        mock_doc = Mock()
                        mock_doc.__len__ = Mock(return_value=1)
                        mock_page = Mock()
                        mock_page.get_text.return_value = "Fallback content from PyMuPDF"
                        mock_doc.__getitem__ = Mock(return_value=mock_page)
                        mock_doc.close = Mock()
                        mock_fitz.open.return_value = mock_doc
                        
                        extractor = UnstructuredExtractor(config=config)
                        elements = extractor.extract_from_pdf(sample_pdf_path)
        
        assert len(elements) >= 1
        assert any("Fallback" in e.text for e in elements)
    
    def test_fallback_on_zero_elements(self, sample_pdf_path):
        """Verify fallback to PyMuPDF when Unstructured returns 0 elements.
        
        TDD RED Phase: This tests the scenario where Unstructured successfully
        parses a PDF but returns no elements (e.g., scanned/image PDF).
        The fallback should be triggered to try PyMuPDF with OCR support.
        
        Reference: CODING_PATTERNS_ANALYSIS - proper test coverage for edge cases
        """
        config = ExtractionConfig(fallback_to_pymupdf=True)
        
        with patch(f'{MODULE_PATH}.UNSTRUCTURED_AVAILABLE', True):
            with patch(f'{MODULE_PATH}.partition_pdf', return_value=[]):  # Empty result
                with patch(f'{MODULE_PATH}.PYMUPDF_AVAILABLE', True):
                    with patch(f'{MODULE_PATH}.fitz') as mock_fitz:
                        # Mock PyMuPDF fallback
                        mock_doc = Mock()
                        mock_doc.__len__ = Mock(return_value=1)
                        mock_page = Mock()
                        mock_page.get_text.return_value = "OCR fallback content"
                        mock_doc.__getitem__ = Mock(return_value=mock_page)
                        mock_doc.close = Mock()
                        mock_fitz.open.return_value = mock_doc
                        
                        extractor = UnstructuredExtractor(config=config)
                        elements = extractor.extract_from_pdf(sample_pdf_path)
        
        # Fallback should produce elements from PyMuPDF
        assert len(elements) >= 1
        assert any("OCR fallback" in e.text for e in elements)
    
    def test_no_fallback_when_disabled(self, sample_pdf_path):
        """Verify no fallback when disabled in config."""
        config = ExtractionConfig(fallback_to_pymupdf=False)
        
        with patch(f'{MODULE_PATH}.UNSTRUCTURED_AVAILABLE', True):
            with patch(f'{MODULE_PATH}.partition_pdf') as mock_partition:
                mock_partition.side_effect = Exception("Unstructured failed")
                
                extractor = UnstructuredExtractor(config=config)
                with pytest.raises(Exception) as exc_info:
                    extractor.extract_from_pdf(sample_pdf_path)
                
                assert "Unstructured failed" in str(exc_info.value)


@pytest.mark.skipif(UnstructuredExtractor is None, reason="UnstructuredExtractor not implemented yet")  
class TestUnstructuredExtractorTitleDetection:
    """Test chapter/title detection from extracted elements."""
    
    def test_get_potential_chapters(self, sample_pdf_path, mock_partition_elements):
        """Verify extraction of potential chapter boundaries from titles."""
        with patch(f'{MODULE_PATH}.UNSTRUCTURED_AVAILABLE', True):
            with patch(f'{MODULE_PATH}.partition_pdf', return_value=mock_partition_elements):
                extractor = UnstructuredExtractor()
                chapters = extractor.get_potential_chapters(sample_pdf_path)
        
        # Should identify "Chapter 1" and "Chapter 2" as chapter-level headings
        # "1.1 Background" should be section-level (but still included)
        assert isinstance(chapters, list)
        assert len(chapters) == 3  # All three titles are returned
        
        chapter_titles = [ch["title"] for ch in chapters]
        assert "Chapter 1: Introduction" in chapter_titles
        assert "Chapter 2: Methods" in chapter_titles
    
    def test_chapter_detection_includes_page_ranges(self, sample_pdf_path, mock_partition_elements):
        """Verify chapter detection includes start/end page ranges."""
        with patch(f'{MODULE_PATH}.UNSTRUCTURED_AVAILABLE', True):
            with patch(f'{MODULE_PATH}.partition_pdf', return_value=mock_partition_elements):
                extractor = UnstructuredExtractor()
                chapters = extractor.get_potential_chapters(sample_pdf_path)
        
        for chapter in chapters:
            assert "start_page" in chapter
            assert "end_page" in chapter
            assert chapter["start_page"] <= chapter["end_page"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
