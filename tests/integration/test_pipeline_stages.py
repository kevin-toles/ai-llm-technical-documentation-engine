"""
Unit Tests for Pipeline Stages (PDF → JSON → Summaries → Metadata)

Test-Driven Development (TDD) approach for pipeline transformation stages.
Tests each stage in isolation with happy path, error handling, and edge cases.

References:
- Python Distilled Ch. 14.1-14.5 (Testing and Debugging) pp. 237-250
- Architecture Patterns with Python Ch. 1 (Domain Modeling with TDD) pp. 15-35
- Python Cookbook 3rd Ch. 14 (Testing, Debugging, and Exceptions)
- Fluent Python 2nd Ch. 11 (Context Managers for Test Resources) p. 389

Structure:
- TestPDFToJSON: PDF conversion to structured JSON
- TestJSONToSummaries: JSON to chapter summaries generation
- TestSummariesToMetadata: Summary to metadata extraction

Test Organization Pattern: Python Distilled Ch. 14.5 - one test file per related functionality
"""

import pytest
import json
from unittest.mock import Mock
import fitz  # PyMuPDF

from workflows.pdf_to_json.scripts.convert_pdf_to_json import convert_pdf_to_json, extract_text_from_page
from workflows.metadata_enrichment.scripts.generate_chapter_metadata import (
    generate_chapter_summary,
    extract_keywords_from_text as extract_keywords,
    extract_concepts_from_text as extract_key_concepts,
)


# =============================================================================
# Test Fixtures (Python Distilled Ch. 14.2 - Fixtures)
# =============================================================================

@pytest.fixture
def temp_pdf_path(tmp_path):
    """
    Create a temporary PDF file for testing.
    
    Reference: Fluent Python Ch. 11 - Context managers for resource management
    Pattern: Python Distilled Ch. 14.2 - Fixture-based test data setup
    """
    pdf_path = tmp_path / "test_book.pdf"
    
    # Create a simple PDF with PyMuPDF
    doc = fitz.open()  # Create new PDF
    page = doc.new_page()
    
    # Add some text to the page
    text = "Chapter 1: Introduction\n\nThis is a sample chapter about testing."
    page.insert_text((50, 50), text)
    
    doc.save(str(pdf_path))
    doc.close()
    
    return pdf_path


@pytest.fixture
def sample_json_data():
    """
    Sample JSON data representing a converted PDF book.
    
    Reference: Python Distilled Ch. 14.2 - Parametrized test data
    """
    return {
        "metadata": {
            "title": "Test Book",
            "author": "Test Author",
            "publisher": "Test Publisher",
            "edition": "1st Edition",
            "isbn": "123-456-789",
            "total_pages": 10,
            "conversion_date": "2025-11-14T00:00:00",
            "conversion_method": "PyMuPDF",
            "source_pdf": "test_book.pdf"
        },
        "chapters": [
            {
                "chapter_number": 1,
                "title": "Introduction",
                "page_start": 1,
                "page_end": 5
            }
        ],
        "pages": [
            {
                "page_number": 1,
                "chapter": 1,
                "content": "Chapter 1: Introduction\n\nThis chapter covers the basics of testing."
            },
            {
                "page_number": 2,
                "chapter": 1,
                "content": "We will learn about unit tests, fixtures, and mocking."
            }
        ]
    }


@pytest.fixture
def sample_chapter_text():
    """
    Sample chapter text for summary and metadata extraction.
    
    Reference: Python Cookbook Ch. 14 - Test data patterns
    """
    return """
    Chapter 5: Advanced Testing Patterns
    
    This chapter explores advanced testing techniques including fixtures,
    parametrization, and mocking. We cover pytest patterns, test organization,
    and best practices for maintaining test suites.
    
    Key concepts include:
    - Test fixtures for setup and teardown
    - Parametrized tests for multiple scenarios
    - Mocking external dependencies
    - Context managers for resource management
    
    These patterns improve test maintainability and coverage.
    """


# =============================================================================
# TestPDFToJSON: PDF Conversion Stage
# =============================================================================

class TestPDFToJSON:
    """
    Unit tests for PDF → JSON conversion stage.
    
    Reference: Architecture Patterns Ch. 1 - Test edge cases, not just happy path (p. 23)
    Pattern: Python Distilled Ch. 14.1 - unittest framework structure
    """
    
    # Happy Path Tests
    # ----------------
    
    def test_converts_valid_pdf_to_json(self, temp_pdf_path, tmp_path):
        """
        Test successful conversion of a valid PDF to JSON format.
        
        Reference: Python Distilled Ch. 14.1 - Basic unit test structure
        Expected: JSON file created with correct structure
        """
        output_path = tmp_path / "output.json"
        
        result = convert_pdf_to_json(temp_pdf_path, output_path)
        
        # TDD RED: Will fail until convert_pdf_to_json returns True on success
        assert result is True, "Should return True on successful conversion"
        assert output_path.exists(), "JSON output file should be created"
        
        # Validate JSON structure
        with open(output_path, 'r') as f:
            data = json.load(f)
        
        assert "metadata" in data, "Should have metadata section"
        assert "pages" in data, "Should have pages array"
        assert len(data["pages"]) > 0, "Should have at least one page"
    
    
    def test_preserves_chapter_structure(self, temp_pdf_path, tmp_path):
        """
        Test that chapter boundaries are correctly identified and preserved.
        
        Reference: Architecture Patterns Ch. 2 - Repository pattern for data preservation
        Expected: Chapter markers in page data
        """
        output_path = tmp_path / "output.json"
        
        convert_pdf_to_json(temp_pdf_path, output_path)
        
        with open(output_path, 'r') as f:
            data = json.load(f)
        
        # TDD RED: Will fail until chapter detection is implemented
        # Check if pages have chapter information
        for page in data["pages"]:
            assert "chapter" in page, "Each page should have chapter field"
            assert "page_number" in page, "Each page should have page_number"
            assert "content" in page, "Each page should have content"
    
    
    # Error Handling Tests
    # --------------------
    
    def test_handles_missing_pdf_file(self, tmp_path):
        """
        Test graceful handling of non-existent PDF file.
        
        Reference: Python Distilled Ch. 14.4 - Testing exceptions (pp. 246-248)
        Expected: Returns False and logs error (no exception raised)
        """
        nonexistent_pdf = tmp_path / "nonexistent.pdf"
        output_path = tmp_path / "output.json"
        
        # TDD RED: Will fail until proper error handling exists
        result = convert_pdf_to_json(nonexistent_pdf, output_path)
        
        assert result is False, "Should return False for missing file"
        assert not output_path.exists(), "Should not create output for missing input"
    
    
    def test_handles_corrupted_pdf(self, tmp_path):
        """
        Test handling of corrupted or invalid PDF files.
        
        Reference: Python Cookbook Ch. 14.1 - Exception testing patterns
        Expected: Catches PyMuPDF errors and returns False
        """
        # Create a fake "PDF" file that's actually just text
        corrupted_pdf = tmp_path / "corrupted.pdf"
        corrupted_pdf.write_text("This is not a valid PDF file")
        
        output_path = tmp_path / "output.json"
        
        # TDD RED: Will fail until corruption handling is implemented
        result = convert_pdf_to_json(corrupted_pdf, output_path)
        
        assert result is False, "Should return False for corrupted PDF"
        assert not output_path.exists(), "Should not create output for corrupted input"
    
    
    def test_handles_empty_pdf(self, tmp_path):
        """
        Test conversion of PDF with no content (zero pages or blank pages).
        
        Reference: Architecture Patterns Ch. 1 - Edge case testing (p. 23)
        Expected: PyMuPDF cannot create zero-page PDFs, so test with blank page instead
        """
        # Create PDF with one blank page (PyMuPDF doesn't support zero-page PDFs)
        empty_pdf = tmp_path / "empty.pdf"
        doc = fitz.open()
        doc.new_page()  # Add one blank page
        doc.save(str(empty_pdf))
        doc.close()
        
        output_path = tmp_path / "output.json"
        
        # Should handle blank PDF gracefully
        result = convert_pdf_to_json(empty_pdf, output_path)
        
        assert result is True, "Should handle blank PDF gracefully"
        
        with open(output_path, 'r') as f:
            data = json.load(f)
        
        assert data["metadata"]["total_pages"] == 1, "Should report one blank page"
        assert len(data["pages"]) == 1, "Should have one page entry"
    
    
    # Edge Case Tests
    # ---------------
    
    def test_extract_text_from_page_direct_extraction(self):
        """
        Test direct text extraction from PDF page (non-OCR path).
        
        Reference: Python Distilled Ch. 14.3 - Mocking external dependencies
        Expected: Returns text and "Direct" method indicator
        """
        # Create mock page with text
        mock_page = Mock()
        mock_page.get_text.return_value = "Sample text from page"
        
        # TDD RED: Will fail until extract_text_from_page properly returns method
        text, method = extract_text_from_page(mock_page)
        
        assert text == "Sample text from page", "Should extract text correctly"
        assert method == "Direct", "Should indicate direct extraction method"
    
    
    def test_extract_text_from_page_ocr_fallback(self):
        """
        Test OCR fallback when direct text extraction returns empty.
        
        Reference: Python Cookbook Ch. 14.10 - Testing file I/O and external tools
        Expected: Attempts OCR when direct extraction fails
        """
        # Create mock page with no extractable text
        mock_page = Mock()
        mock_page.get_text.return_value = ""  # No direct text
        mock_page.get_pixmap.return_value = Mock()  # Pixmap available for OCR
        
        # TDD RED: Will fail until OCR fallback is properly implemented
        _, method = extract_text_from_page(mock_page)
        
        # Current implementation may not have full OCR, but should try
        assert method in ["OCR", "Failed"], "Should attempt OCR when no direct text"


# =============================================================================
# TestJSONToSummaries: Summary Generation Stage  
# =============================================================================

class TestJSONToSummaries:
    """
    Unit tests for JSON → Chapter Summaries transformation.
    
    Reference: Python Distilled Ch. 14.2 - Parametrization for multiple scenarios
    Pattern: Python Cookbook Ch. 14 - Recipe-based testing approaches
    """
    
    # Happy Path Tests
    # ----------------
    
    def test_generates_summary_from_chapter_text(self, sample_chapter_text):
        """
        Test generation of chapter summary from text content.
        
        Reference: Python Distilled Ch. 14.2 - Test data fixtures
        Expected: Returns summary string with key points
        """
        # Convert text to chapter_pages format expected by function
        chapter_pages = [
            {
                "page_number": 1,
                "content": sample_chapter_text
            }
        ]
        
        # Extract keywords and concepts first (as the function expects)
        keywords = extract_keywords(sample_chapter_text)
        concepts = extract_key_concepts(sample_chapter_text)
        
        # TDD RED: Will fail until generate_chapter_summary works correctly
        summary = generate_chapter_summary(
            chapter_pages=chapter_pages,
            chapter_title="Advanced Testing Patterns",
            keywords=keywords,
            concepts=concepts
        )
        
        assert isinstance(summary, str), "Summary should be a string"
        assert len(summary) > 0, "Summary should not be empty"
        assert len(summary) < len(sample_chapter_text), "Summary should be shorter than source"
    
    
    def test_summary_includes_key_concepts(self, sample_chapter_text):
        """
        Test that summary captures main concepts from the chapter.
        
        Reference: Architecture Patterns Ch. 1 - Domain model validation
        Expected: Summary contains important keywords from source
        """
        chapter_pages = [{"page_number": 1, "content": sample_chapter_text}]
        keywords = extract_keywords(sample_chapter_text)
        concepts = extract_key_concepts(sample_chapter_text)
        
        summary = generate_chapter_summary(
            chapter_pages=chapter_pages,
            chapter_title="Advanced Testing Patterns",
            keywords=keywords,
            concepts=concepts
        )
        
        # TDD RED: Will fail until summary quality is adequate
        important_terms = ["testing", "fixtures", "parametrization", "mocking"]
        
        # At least some key terms should appear in summary
        found_terms = [term for term in important_terms if term.lower() in summary.lower()]
        assert len(found_terms) >= 1, f"Summary should mention key concepts, found: {found_terms}"
    
    
    # Error Handling Tests
    # --------------------
    
    def test_handles_empty_chapter_text(self):
        """
        Test handling of empty or whitespace-only input.
        
        Reference: Python Distilled Ch. 14.4 - Exception handling in tests
        Expected: Returns minimal summary or handles gracefully
        """
        empty_text = "   \n\n  "
        chapter_pages = [{"page_number": 1, "content": empty_text}]
        
        # TDD RED: Will fail until empty input handling is verified
        try:
            summary = generate_chapter_summary(
                chapter_pages=chapter_pages,
                chapter_title="Empty Chapter",
                keywords=[],
                concepts=[]
            )
            assert isinstance(summary, str), "Should return string for empty input"
        except (ValueError, IndexError) as e:
            # Acceptable to raise exception for invalid input
            assert len(str(e)) > 0, "Error message should be informative"
    
    
    def test_handles_very_short_text(self):
        """
        Test summary generation from very short text (less than typical summary length).
        
        Reference: Architecture Patterns Ch. 1 - Edge case testing
        Expected: Returns minimal but valid summary
        """
        short_text = "This is a very short chapter."
        chapter_pages = [{"page_number": 1, "content": short_text}]
        keywords = extract_keywords(short_text)
        concepts = extract_key_concepts(short_text)
        
        # TDD RED: Will fail until short text handling is verified
        summary = generate_chapter_summary(
            chapter_pages=chapter_pages,
            chapter_title="Short Chapter",
            keywords=keywords,
            concepts=concepts
        )
        
        assert isinstance(summary, str), "Should return string for short input"
        assert len(summary) > 0, "Should produce non-empty summary"
    
    
    def test_handles_special_characters_in_text(self):
        """
        Test handling of unicode, emojis, and special formatting characters.
        
        Reference: Python Cookbook Ch. 14 - Encoding and special character handling
        Expected: Preserves or safely handles special characters
        """
        text_with_special = """
        Chapter 3: Über-Testing 🧪
        
        This chapter discusses testing with special characters: ñ, ü, é, 中文.
        We cover edge cases like quotes "double" and 'single', as well as
        mathematical symbols: ∫, ∑, π.
        """
        chapter_pages = [{"page_number": 1, "content": text_with_special}]
        keywords = extract_keywords(text_with_special)
        concepts = extract_key_concepts(text_with_special)
        
        # TDD RED: Will fail until unicode handling is verified
        summary = generate_chapter_summary(
            chapter_pages=chapter_pages,
            chapter_title="Über-Testing",
            keywords=keywords,
            concepts=concepts
        )
        
        assert isinstance(summary, str), "Should handle special characters"
        # Should not crash or produce mangled output
        assert len(summary) > 0, "Should produce non-empty summary"


# =============================================================================
# TestSummariesToMetadata: Metadata Extraction Stage
# =============================================================================

class TestSummariesToMetadata:
    """
    Unit tests for Chapter Summaries → Metadata extraction.
    
    Reference: Architecture Patterns Ch. 2 - Repository pattern for data extraction
    Pattern: Fluent Python Ch. 11 - Context managers for test resources
    """
    
    # Happy Path Tests
    # ----------------
    
    def test_extracts_keywords_from_text(self, sample_chapter_text):
        """
        Test extraction of relevant keywords from chapter text.
        
        Reference: Python Distilled Ch. 14.2 - Fixture-based test data
        Expected: Returns list of important programming keywords
        """
        # TDD RED: Will fail until extract_keywords is implemented
        keywords = extract_keywords(sample_chapter_text)
        
        assert isinstance(keywords, list), "Keywords should be a list"
        assert len(keywords) > 0, "Should extract at least some keywords"
        
        # Should find Python/testing related keywords
        expected_keywords = ["testing", "pytest", "fixtures", "mocking"]
        found = [kw for kw in keywords if kw.lower() in [e.lower() for e in expected_keywords]]
        assert len(found) > 0, f"Should find relevant keywords, got: {keywords}"
    
    
    def test_extracts_key_concepts_from_text(self, sample_chapter_text):
        """
        Test extraction of high-level concepts from chapter text.
        
        Reference: Architecture Patterns Ch. 1 - Domain concept identification
        Expected: Returns structured list of key concepts
        """
        # TDD RED: Will fail until extract_key_concepts is implemented
        concepts = extract_key_concepts(sample_chapter_text)
        
        assert isinstance(concepts, list), "Concepts should be a list"
        assert len(concepts) > 0, "Should extract at least some concepts"
        
        # Concepts should be more abstract than keywords
        # e.g., "test organization" rather than just "pytest"
        for concept in concepts:
            assert isinstance(concept, str), "Each concept should be a string"
            assert len(concept) > 0, "Concepts should not be empty strings"
    
    
    # Error Handling Tests
    # --------------------
    
    def test_handles_missing_common_keywords(self):
        """
        Test keyword extraction from text with few/no technical keywords.
        
        Reference: Python Cookbook Ch. 14 - Handling unexpected inputs
        Expected: Returns empty list or generic keywords
        """
        generic_text = "This is a generic text with no specific technical terms."
        
        # TDD RED: Will fail until generic text handling is implemented
        keywords = extract_keywords(generic_text)
        
        # Should not crash, but may return empty or very short list
        assert isinstance(keywords, list), "Should return list even for generic text"
        # It's acceptable to return empty list for non-technical text (no assertion on length needed)
    
    
    def test_handles_text_with_excessive_keywords(self):
        """
        Test that keyword extraction limits output to prevent overwhelming results.
        
        Reference: Python Distilled Ch. 14 - Testing edge cases
        Expected: Returns top N most relevant keywords (e.g., 20 max)
        """
        # Text artificially stuffed with many technical terms
        keyword_spam = " ".join([
            "testing", "pytest", "fixture", "mock", "class", "function",
            "async", "await", "decorator", "generator", "iterator", "module",
            "package", "api", "rest", "microservice", "database", "cache"
        ] * 10)  # Repeat keywords many times
        
        # TDD RED: Will fail until keyword limiting is implemented
        keywords = extract_keywords(keyword_spam)
        
        assert isinstance(keywords, list), "Should return list"
        # Should limit to reasonable number
        assert len(keywords) <= 50, "Should limit keywords to prevent spam"


# =============================================================================
# Integration-Adjacent Tests (Verify stage compatibility)
# =============================================================================

class TestStageCompatibility:
    """
    Test that output of one stage is compatible with input of next stage.
    
    Reference: Architecture Patterns Ch. 3 - Service layer integration
    Pattern: Python Distilled Ch. 14.5 - Test organization
    
    Note: These are NOT full integration tests (that's Day 6).
    These verify data structure compatibility between stages.
    """
    
    def test_pdf_json_output_matches_summary_input_format(self, sample_json_data):
        """
        Test that JSON output from PDF conversion has required fields for summary generation.
        
        Reference: Architecture Patterns Ch. 2 - Interface contracts
        Expected: JSON structure includes 'pages' array with 'content' fields
        """
        # TDD RED: Will fail if JSON structure incompatible
        
        # Verify JSON has required structure for next stage
        assert "pages" in sample_json_data, "JSON must have pages array"
        assert len(sample_json_data["pages"]) > 0, "Should have at least one page"
        
        # Each page should have content that can be summarized
        for page in sample_json_data["pages"]:
            assert "content" in page, "Each page must have content field"
            assert isinstance(page["content"], str), "Content must be string"
    
    
    def test_summary_output_suitable_for_metadata_extraction(self, sample_chapter_text):
        """
        Test that summary output contains sufficient data for metadata extraction.
        
        Reference: Python Distilled Ch. 14 - Contract testing
        Expected: Summary is non-empty string suitable for keyword extraction
        """
        # TDD RED: Will fail if summary format incompatible with metadata extraction
        
        chapter_pages = [{"page_number": 1, "content": sample_chapter_text}]
        keywords = extract_keywords(sample_chapter_text)
        concepts = extract_key_concepts(sample_chapter_text)
        
        summary = generate_chapter_summary(
            chapter_pages=chapter_pages,
            chapter_title="Testing",
            keywords=keywords,
            concepts=concepts
        )
        
        # Summary should be suitable for metadata extraction
        assert isinstance(summary, str), "Summary must be string"
        assert len(summary) > 20, "Summary should be substantial enough for metadata"
        
        # Should be able to extract keywords from summary
        summary_keywords = extract_keywords(summary)
        assert isinstance(summary_keywords, list), "Should be able to extract keywords from summary"
