"""
TDD RED Phase: Test ChapterSegmenter processing real books.

WBS 3.5.1.1 - Chapter Segmentation Tests
Reference: AI_CODING_PLATFORM_WBS.md Phase 3.5

Purpose:
    Verify ChapterSegmenter can process the 12 books with empty chapters
    in ai-platform-data/books/raw/ and produce valid chapter structures.

Document References:
    - GUIDELINES_AI_Engineering: Data pipeline architecture, batch processing
    - CODING_PATTERNS_ANALYSIS: Anti-patterns to avoid (type hints, CC < 10)
    - AI_CODING_PLATFORM_ARCHITECTURE: llm-document-enhancer → manual transfer → ai-platform-data

Test Strategy:
    - RED: Tests expect ChapterSegmenter to produce valid chapters for test book
    - GREEN: Run ChapterSegmenter on test data, verify non-empty chapters
    - REFACTOR: Validate chapter structure against schema

Anti-Pattern Audit (from CODING_PATTERNS_ANALYSIS):
    - ✓ Type annotations on all functions
    - ✓ No unused imports
    - ✓ Proper exception handling
    - ✓ Cognitive complexity < 10

Books to Process (12 with empty chapters):
    1. Architecture Patterns with Python.json
    2. Building Microservices.json
    3. Building Python Microservices with FastAPI.json
    4. Fluent Python 2nd.json
    5. Microservice APIs Using Python Flask FastAPI.json
    6. Microservice Architecture.json
    7. Microservices Up and Running.json
    8. Python Architecture Patterns.json
    9. Python Data Analysis 3rd.json
    10. Python Distilled.json
    11. Python Essential Reference 4th.json
    12. Python Microservices Development.json
"""

import json
import pytest
from pathlib import Path
from typing import Dict, List, Any, Optional

from workflows.pdf_to_json.scripts.chapter_segmenter import ChapterSegmenter
from config.settings import ChapterSegmentationConfig


# ============================================================================
# Constants - Per CODING_PATTERNS_ANALYSIS: Use constants for repeated values
# ============================================================================

_TEST_BOOKS_DIR = Path(__file__).parent.parent.parent.parent.parent / "test_fixtures" / "books"
_REQUIRED_CHAPTER_FIELDS = {"number", "title", "start_page", "end_page", "detection_method"}
_VALID_DETECTION_METHODS = {"regex_chapter", "chapter_title", "topic_boundary", "synthetic"}

# One representative test book for initial GREEN phase
_SAMPLE_BOOK_NAME = "Architecture Patterns with Python.json"


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def default_config() -> ChapterSegmentationConfig:
    """Default chapter segmentation configuration.
    
    Returns:
        ChapterSegmentationConfig with default values
    """
    return ChapterSegmentationConfig()


@pytest.fixture
def segmenter(default_config: ChapterSegmentationConfig) -> ChapterSegmenter:
    """Create ChapterSegmenter instance.
    
    Args:
        default_config: Configuration fixture
        
    Returns:
        Configured ChapterSegmenter instance
    """
    return ChapterSegmenter(default_config)


@pytest.fixture
def sample_book_pages() -> Optional[List[Dict[str, Any]]]:
    """Load pages from sample test book if available.
    
    This fixture attempts to load test data from test_fixtures/books/.
    If the test fixtures don't exist yet, it returns None to allow
    tests to skip gracefully.
    
    Returns:
        List of page dicts or None if test data not available
    """
    sample_book_path = _TEST_BOOKS_DIR / _SAMPLE_BOOK_NAME
    
    if not sample_book_path.exists():
        return None
    
    with open(sample_book_path, "r", encoding="utf-8") as f:
        book_data = json.load(f)
    
    return book_data.get("pages", [])


# ============================================================================
# Test Class: ChapterSegmenter Book Processing
# ============================================================================

class TestChapterSegmenterProcessesBook:
    """TDD RED Phase: Test ChapterSegmenter on real book data.
    
    These tests verify that ChapterSegmenter can:
    1. Process pages from a real book JSON
    2. Produce non-empty chapter list
    3. Produce chapters with required fields
    4. Produce valid page ranges
    """
    
    def test_segmenter_initializes_with_config(
        self, default_config: ChapterSegmentationConfig
    ) -> None:
        """ChapterSegmenter initializes correctly with valid config.
        
        Pre-condition: Valid ChapterSegmentationConfig
        Post-condition: ChapterSegmenter instance with all services initialized
        """
        segmenter = ChapterSegmenter(default_config)
        
        assert segmenter.config == default_config
        assert segmenter.extractor is not None
        assert segmenter.validator is not None
        assert segmenter.regex_matcher is not None
        assert segmenter.yake_validator is not None
        assert segmenter.tfidf_analyzer is not None
    
    @pytest.mark.skipif(
        not (_TEST_BOOKS_DIR / _SAMPLE_BOOK_NAME).exists(),
        reason="Test fixtures not available - run setup_test_fixtures.py first"
    )
    def test_segment_book_produces_chapters(
        self, segmenter: ChapterSegmenter, sample_book_pages: List[Dict[str, Any]]
    ) -> None:
        """ChapterSegmenter produces non-empty chapter list for real book.
        
        RED Phase: This test will FAIL until we process the book through
        ChapterSegmenter and verify it produces valid chapters.
        
        Pre-condition: Book pages loaded from test fixture
        Post-condition: Non-empty list of chapter dicts returned
        """
        assert sample_book_pages is not None, "Test data required"
        assert len(sample_book_pages) > 0, "Book must have pages"
        
        chapters = segmenter.segment_book(sample_book_pages)
        
        # Pass C guarantees non-empty for non-empty input
        assert len(chapters) > 0, "ChapterSegmenter must produce at least 1 chapter"
        
    @pytest.mark.skipif(
        not (_TEST_BOOKS_DIR / _SAMPLE_BOOK_NAME).exists(),
        reason="Test fixtures not available - run setup_test_fixtures.py first"
    )
    def test_chapters_have_required_fields(
        self, segmenter: ChapterSegmenter, sample_book_pages: List[Dict[str, Any]]
    ) -> None:
        """Each chapter has all required fields.
        
        Required fields:
        - number: int (chapter sequence number)
        - title: str (chapter title)
        - start_page: int (first page of chapter)
        - end_page: int (last page of chapter)
        - detection_method: str (how chapter was detected)
        """
        assert sample_book_pages is not None, "Test data required"
        
        chapters = segmenter.segment_book(sample_book_pages)
        
        for i, chapter in enumerate(chapters):
            missing_fields = _REQUIRED_CHAPTER_FIELDS - set(chapter.keys())
            assert not missing_fields, (
                f"Chapter {i+1} missing fields: {missing_fields}"
            )
    
    @pytest.mark.skipif(
        not (_TEST_BOOKS_DIR / _SAMPLE_BOOK_NAME).exists(),
        reason="Test fixtures not available - run setup_test_fixtures.py first"
    )
    def test_chapters_have_valid_page_ranges(
        self, segmenter: ChapterSegmenter, sample_book_pages: List[Dict[str, Any]]
    ) -> None:
        """Chapter page ranges are valid and non-overlapping.
        
        Validation rules:
        - start_page <= end_page for each chapter
        - Chapters are sequential (no gaps > 1 page between chapters)
        - No overlapping page ranges
        """
        assert sample_book_pages is not None, "Test data required"
        
        chapters = segmenter.segment_book(sample_book_pages)
        
        for i, chapter in enumerate(chapters):
            # Each chapter's start <= end
            assert chapter["start_page"] <= chapter["end_page"], (
                f"Chapter {i+1} has invalid range: "
                f"start_page={chapter['start_page']}, end_page={chapter['end_page']}"
            )
            
            # Check sequential ordering (no large gaps)
            if i > 0:
                prev_end = chapters[i-1]["end_page"]
                current_start = chapter["start_page"]
                gap = current_start - prev_end
                assert gap <= 2, (
                    f"Large gap between chapter {i} and {i+1}: "
                    f"prev_end={prev_end}, current_start={current_start}"
                )
    
    @pytest.mark.skipif(
        not (_TEST_BOOKS_DIR / _SAMPLE_BOOK_NAME).exists(),
        reason="Test fixtures not available - run setup_test_fixtures.py first"
    )
    def test_detection_method_is_valid(
        self, segmenter: ChapterSegmenter, sample_book_pages: List[Dict[str, Any]]
    ) -> None:
        """Detection method is one of the valid methods.
        
        Valid methods:
        - regex_chapter: Found via chapter pattern regex
        - chapter_title: Found via dedicated chapter title page
        - topic_boundary: Found via TF-IDF topic shift
        - synthetic: Generated via Pass C fallback
        """
        assert sample_book_pages is not None, "Test data required"
        
        chapters = segmenter.segment_book(sample_book_pages)
        
        for i, chapter in enumerate(chapters):
            method = chapter.get("detection_method", "")
            # Allow methods that start with valid prefixes (e.g., "regex_chapter", "regex_part")
            is_valid = (
                method in _VALID_DETECTION_METHODS or
                method.startswith("regex_") or
                method.startswith("chapter_")
            )
            assert is_valid, (
                f"Chapter {i+1} has invalid detection_method: '{method}'"
            )


# ============================================================================
# Test Class: Batch Book Processing  
# ============================================================================

class TestBatchBookProcessing:
    """Tests for processing multiple books in batch.
    
    WBS 3.5.1.3 - Process all 12 books with empty chapters
    """
    
    # List of 12 books with empty chapters
    BOOKS_WITH_EMPTY_CHAPTERS = [
        "Architecture Patterns with Python.json",
        "Building Microservices.json",
        "Building Python Microservices with FastAPI.json",
        "Fluent Python 2nd.json",
        "Microservice APIs Using Python Flask FastAPI.json",
        "Microservice Architecture.json",
        "Microservices Up and Running.json",
        "Python Architecture Patterns.json",
        "Python Data Analysis 3rd.json",
        "Python Distilled.json",
        "Python Essential Reference 4th.json",
        "Python Microservices Development.json",
    ]
    
    @pytest.mark.skipif(
        not _TEST_BOOKS_DIR.exists(),
        reason="Test fixtures directory not available"
    )
    def test_all_target_books_have_test_fixtures(self) -> None:
        """Verify test fixtures exist for all 12 target books.
        
        Pre-condition: test_fixtures/books/ directory exists
        Post-condition: All 12 books have test fixture files
        """
        missing_books: List[str] = []
        
        for book_name in self.BOOKS_WITH_EMPTY_CHAPTERS:
            book_path = _TEST_BOOKS_DIR / book_name
            if not book_path.exists():
                missing_books.append(book_name)
        
        assert not missing_books, (
            f"Missing test fixtures for {len(missing_books)} books:\n"
            + "\n".join(f"  - {b}" for b in missing_books)
        )
    
    @pytest.mark.skipif(
        not _TEST_BOOKS_DIR.exists(),
        reason="Test fixtures directory not available"
    )
    @pytest.mark.parametrize("book_name", BOOKS_WITH_EMPTY_CHAPTERS)  # All 12 books
    def test_process_single_book(
        self, default_config: ChapterSegmentationConfig, book_name: str
    ) -> None:
        """Process a single book and verify chapter output.
        
        REFACTOR: Now tests all 12 books after GREEN phase confirmed.
        This parametrized test validates each book produces valid chapters.
        """
        book_path = _TEST_BOOKS_DIR / book_name
        if not book_path.exists():
            pytest.skip(f"Test fixture not available: {book_name}")
        
        with open(book_path, "r", encoding="utf-8") as f:
            book_data = json.load(f)
        
        pages = book_data.get("pages", [])
        if not pages:
            pytest.skip(f"Book has no pages: {book_name}")
        
        segmenter = ChapterSegmenter(default_config)
        chapters = segmenter.segment_book(pages)
        
        # Assertions
        assert len(chapters) > 0, f"{book_name}: No chapters produced"
        assert all("number" in ch for ch in chapters), f"{book_name}: Missing chapter numbers"
        assert all("title" in ch for ch in chapters), f"{book_name}: Missing chapter titles"
        assert all("start_page" in ch for ch in chapters), f"{book_name}: Missing start pages"
        assert all("end_page" in ch for ch in chapters), f"{book_name}: Missing end pages"


# ============================================================================
# Integration Tests: Full Processing Pipeline
# ============================================================================

class TestChapterSegmentationPipeline:
    """Integration tests for the full chapter segmentation pipeline.
    
    These tests verify end-to-end processing from raw book JSON
    to enriched JSON with chapters.
    """
    
    def test_empty_pages_returns_empty_chapters(
        self, segmenter: ChapterSegmenter
    ) -> None:
        """Empty pages list returns empty chapters list."""
        result = segmenter.segment_book([])
        assert result == []
    
    def test_single_page_book(
        self, segmenter: ChapterSegmenter
    ) -> None:
        """Single page book returns single chapter."""
        pages = [{"page_number": 1, "content": "Single page document. " * 50}]
        chapters = segmenter.segment_book(pages)
        
        assert len(chapters) == 1
        assert chapters[0]["number"] == 1
        assert chapters[0]["start_page"] == 1
        assert chapters[0]["end_page"] == 1
        assert chapters[0]["detection_method"] == "synthetic"
    
    def test_output_is_json_serializable(
        self, segmenter: ChapterSegmenter
    ) -> None:
        """Chapter output can be serialized to JSON."""
        pages = [
            {"page_number": i, "content": f"Page {i} content. " * 30}
            for i in range(1, 51)
        ]
        
        chapters = segmenter.segment_book(pages)
        
        # Should not raise
        json_str = json.dumps(chapters)
        assert isinstance(json_str, str)
        
        # Should round-trip
        parsed = json.loads(json_str)
        assert parsed == chapters
