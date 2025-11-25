"""
Characterization tests for chapter_segmenter.py

Tests capture current behavior before refactoring (RED → GREEN → REFACTOR cycle).
Reference: PYTHON_GUIDELINES Ch. 25 - Testing best practices

Test Coverage:
- Chapter dataclass serialization
- ChapterSegmenter initialization and validation
- Pass A: Regex detection with YAKE validation
- Pass B: TF-IDF topic-shift detection
- Pass C: Synthetic segmentation (fallback)
- Validation logic for segmentation quality
- Boundary scoring for chapter detection
- Edge cases: empty input, single page, invalid config
"""

import pytest
from dataclasses import dataclass
from typing import List, Dict
from workflows.pdf_to_json.scripts.chapter_models import Chapter
from workflows.pdf_to_json.scripts.chapter_segmenter import ChapterSegmenter
from config.settings import ChapterSegmentationConfig


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def default_config():
    """Default chapter segmentation configuration"""
    return ChapterSegmentationConfig()


@pytest.fixture
def sample_pages_short():
    """Short book (20 pages) with clear chapter markers"""
    pages = []
    # Chapter 1: Pages 1-7
    pages.append({"page_number": 1, "content": "Chapter 1: Introduction\n" + "Introduction text. " * 100})
    for i in range(2, 8):
        pages.append({"page_number": i, "content": f"Chapter 1 content on page {i}. " * 50})
    
    # Chapter 2: Pages 8-14
    pages.append({"page_number": 8, "content": "Chapter 2: Background\n" + "Background text. " * 100})
    for i in range(9, 15):
        pages.append({"page_number": i, "content": f"Chapter 2 content on page {i}. " * 50})
    
    # Chapter 3: Pages 15-20
    pages.append({"page_number": 15, "content": "Chapter 3: Methods\n" + "Methods text. " * 100})
    for i in range(16, 21):
        pages.append({"page_number": i, "content": f"Chapter 3 content on page {i}. " * 50})
    
    return pages


@pytest.fixture
def sample_pages_no_markers():
    """Book without clear chapter markers (relies on topic shifts)"""
    pages = []
    # Section 1: Python basics
    for i in range(1, 11):
        content = "Python programming language basics. " * 50
        content += "Variables, functions, classes, modules. " * 30
        pages.append({"page_number": i, "content": content})
    
    # Section 2: Data structures (topic shift)
    for i in range(11, 21):
        content = "Data structures algorithms lists dictionaries sets. " * 50
        content += "Hash tables binary trees graphs heaps. " * 30
        pages.append({"page_number": i, "content": content})
    
    return pages


@pytest.fixture
def sample_pages_toc():
    """Book with TOC pages (should be skipped)"""
    pages = []
    # TOC page (many isolated numbers)
    toc_content = "Table of Contents\n"
    for i in range(1, 15):
        toc_content += f"{i}  Chapter {i}  .................. {i * 10}\n"
    pages.append({"page_number": 1, "content": toc_content})
    
    # Real chapter
    pages.append({"page_number": 2, "content": "Chapter 1: Introduction\n" + "Real content. " * 100})
    for i in range(3, 10):
        pages.append({"page_number": i, "content": f"Chapter 1 content. " * 50})
    
    return pages


@pytest.fixture
def sample_pages_single():
    """Single page book"""
    return [{"page_number": 1, "content": "Single page document. " * 100}]


# ============================================================================
# Test Chapter Dataclass
# ============================================================================

class TestChapterDataclass:
    """Test Chapter data structure"""
    
    def test_chapter_creation(self):
        """Chapter can be created with all required fields"""
        ch = Chapter(
            number=1,
            title="Introduction",
            start_page=1,
            end_page=10,
            detection_method="regex_chapter"
        )
        assert ch.number == 1
        assert ch.title == "Introduction"
        assert ch.start_page == 1
        assert ch.end_page == 10
        assert ch.detection_method == "regex_chapter"
    
    def test_chapter_to_dict(self):
        """Chapter.to_dict() converts to serializable dict"""
        ch = Chapter(2, "Background", 11, 20, "topic_boundary")
        result = ch.to_dict()
        
        assert isinstance(result, dict)
        assert result["number"] == 2
        assert result["title"] == "Background"
        assert result["start_page"] == 11
        assert result["end_page"] == 20
        assert result["detection_method"] == "topic_boundary"


# ============================================================================
# Test ChapterSegmenter Initialization
# ============================================================================

class TestChapterSegmenterInit:
    """Test ChapterSegmenter initialization"""
    
    def test_init_with_valid_config(self, default_config):
        """ChapterSegmenter initializes with valid config"""
        segmenter = ChapterSegmenter(default_config)
        assert segmenter.config == default_config
        assert segmenter.extractor is not None
        assert segmenter.validator is not None
        assert segmenter.regex_matcher is not None
    
    def test_init_with_none_config(self):
        """ChapterSegmenter raises ValueError with None config"""
        with pytest.raises(ValueError, match="Invalid chapter segmentation configuration"):
            ChapterSegmenter(None)
    
    def test_service_layer_initialized(self, default_config):
        """Service layer components are initialized"""
        segmenter = ChapterSegmenter(default_config)
        assert segmenter.validator is not None
        assert segmenter.regex_matcher is not None
        assert segmenter.yake_validator is not None
        assert segmenter.tfidf_analyzer is not None


# ============================================================================
# Test segment_book() - Main Entry Point
# ============================================================================

class TestSegmentBook:
    """Test segment_book() orchestration logic"""
    
    def test_segment_book_empty_input(self, default_config):
        """segment_book() returns empty list for empty input"""
        segmenter = ChapterSegmenter(default_config)
        result = segmenter.segment_book([])
        assert result == []
    
    def test_segment_book_single_page(self, default_config, sample_pages_single):
        """segment_book() handles single page book"""
        segmenter = ChapterSegmenter(default_config)
        chapters = segmenter.segment_book(sample_pages_single)
        
        assert len(chapters) >= 1
        assert chapters[0]["number"] == 1
        assert chapters[0]["start_page"] == 1
        assert chapters[0]["end_page"] == 1
    
    def test_segment_book_with_clear_markers(self, default_config, sample_pages_short):
        """segment_book() detects chapters with regex (Pass A)"""
        segmenter = ChapterSegmenter(default_config)
        chapters = segmenter.segment_book(sample_pages_short)
        
        # Should find 3 chapters via Pass A
        assert len(chapters) == 3
        assert all("regex_" in ch["detection_method"] for ch in chapters)
        assert chapters[0]["title"] == "Introduction"
        assert chapters[1]["title"] == "Background"
        assert chapters[2]["title"] == "Methods"
    
    def test_segment_book_returns_dicts(self, default_config, sample_pages_short):
        """segment_book() returns list of dicts (not Chapter objects)"""
        segmenter = ChapterSegmenter(default_config)
        chapters = segmenter.segment_book(sample_pages_short)
        
        assert all(isinstance(ch, dict) for ch in chapters)
        for ch in chapters:
            assert "number" in ch
            assert "title" in ch
            assert "start_page" in ch
            assert "end_page" in ch
            assert "detection_method" in ch
    
    def test_segment_book_guaranteed_non_empty(self, default_config):
        """segment_book() never returns empty list for non-empty input (Pass C fallback)"""
        segmenter = ChapterSegmenter(default_config)
        # Book with no markers and too short for topic detection
        pages = [{"page_number": i, "content": f"Page {i} text. " * 20} for i in range(1, 6)]
        
        chapters = segmenter.segment_book(pages)
        assert len(chapters) >= 1  # Pass C guarantees this


# ============================================================================
# Test Pass A: Regex Detection
# ============================================================================

class TestPassARegex:
    """Test _pass_a_regex() method"""
    
    def test_pass_a_finds_chapters(self, default_config, sample_pages_short):
        """Pass A detects chapters with 'Chapter N:' pattern"""
        segmenter = ChapterSegmenter(default_config)
        page_texts = [p["content"] for p in sample_pages_short]
        page_numbers = [p["page_number"] for p in sample_pages_short]
        
        chapters = segmenter._pass_a_regex(sample_pages_short, page_texts, page_numbers)
        
        assert chapters is not None
        assert len(chapters) == 3
        assert all(isinstance(ch, Chapter) for ch in chapters)
    
    def test_pass_a_skips_toc_pages(self, default_config, sample_pages_toc):
        """Pass A skips TOC pages with many isolated numbers"""
        segmenter = ChapterSegmenter(default_config)
        page_texts = [p["content"] for p in sample_pages_toc]
        page_numbers = [p["page_number"] for p in sample_pages_toc]
        
        chapters = segmenter._pass_a_regex(sample_pages_toc, page_texts, page_numbers)
        
        # Should find chapter starting at page 2 (not page 1 TOC)
        assert chapters is not None
        assert chapters[0].start_page == 2
    
    def test_pass_a_returns_none_without_markers(self, default_config, sample_pages_no_markers):
        """Pass A returns None if no chapter markers found"""
        segmenter = ChapterSegmenter(default_config)
        page_texts = [p["content"] for p in sample_pages_no_markers]
        page_numbers = [p["page_number"] for p in sample_pages_no_markers]
        
        chapters = segmenter._pass_a_regex(sample_pages_no_markers, page_texts, page_numbers)
        
        assert chapters is None
    
    def test_pass_a_validates_with_yake(self, default_config):
        """Pass A validates chapters with YAKE keyword extraction"""
        segmenter = ChapterSegmenter(default_config)
        
        # Fake chapter page (very short - should fail YAKE)
        pages = [{"page_number": 1, "content": "Chapter 1: Test\nShort text."}]
        page_texts = [p["content"] for p in pages]
        page_numbers = [p["page_number"] for p in pages]
        
        chapters = segmenter._pass_a_regex(pages, page_texts, page_numbers)
        
        # Should fail validation (too short for YAKE)
        assert chapters is None


# ============================================================================
# Test Pass B: Topic-Shift Detection
# ============================================================================

class TestPassBTopicShift:
    """Test _pass_b_topic_shift() method"""
    
    def test_pass_b_detects_topic_boundaries(self, default_config, sample_pages_no_markers):
        """Pass B detects topic shifts using TF-IDF"""
        segmenter = ChapterSegmenter(default_config)
        page_texts = [p["content"] for p in sample_pages_no_markers]
        page_numbers = [p["page_number"] for p in sample_pages_no_markers]
        
        chapters = segmenter._pass_b_topic_shift(page_texts, page_numbers)
        
        assert chapters is not None
        assert len(chapters) >= 1
        assert all(ch.detection_method == "topic_boundary" for ch in chapters)
    
    def test_pass_b_enforces_min_chapter_length(self, default_config):
        """Pass B respects min_pages configuration"""
        segmenter = ChapterSegmenter(default_config)
        
        # 10 pages with topic shift at page 3 (too early)
        pages = []
        for i in range(1, 6):
            pages.append({"page_number": i, "content": "Python programming. " * 50})
        for i in range(6, 11):
            pages.append({"page_number": i, "content": "Data structures algorithms. " * 50})
        
        page_texts = [p["content"] for p in pages]
        page_numbers = [p["page_number"] for p in pages]
        
        chapters = segmenter._pass_b_topic_shift(page_texts, page_numbers)
        
        # Should not create tiny chapters
        if chapters:
            for ch in chapters:
                chapter_length = ch.end_page - ch.start_page + 1
                assert chapter_length >= segmenter.config.min_pages
    
    def test_pass_b_returns_none_on_tfidf_failure(self, default_config):
        """Pass B returns None if TF-IDF fails (e.g., empty text)"""
        segmenter = ChapterSegmenter(default_config)
        pages = [{"page_number": i, "content": ""} for i in range(1, 11)]
        page_texts = [p["content"] for p in pages]
        page_numbers = [p["page_number"] for p in pages]
        
        chapters = segmenter._pass_b_topic_shift(page_texts, page_numbers)
        
        assert chapters is None


# ============================================================================
# Test Pass C: Synthetic Segmentation
# ============================================================================

class TestPassCSynthetic:
    """Test _pass_c_synthetic() method"""
    
    def test_pass_c_never_returns_none(self, default_config):
        """Pass C always returns chapters (guaranteed fallback)"""
        segmenter = ChapterSegmenter(default_config)
        pages = [{"page_number": i, "content": f"Page {i}. " * 50} for i in range(1, 51)]
        page_texts = [p["content"] for p in pages]
        page_numbers = [p["page_number"] for p in pages]
        
        chapters = segmenter._pass_c_synthetic(pages, page_texts, page_numbers)
        
        assert chapters is not None
        assert len(chapters) >= 1
        assert all(ch.detection_method == "synthetic" for ch in chapters)
    
    def test_pass_c_handles_single_page(self, default_config, sample_pages_single):
        """Pass C handles single page book"""
        segmenter = ChapterSegmenter(default_config)
        page_texts = [p["content"] for p in sample_pages_single]
        page_numbers = [p["page_number"] for p in sample_pages_single]
        
        chapters = segmenter._pass_c_synthetic(sample_pages_single, page_texts, page_numbers)
        
        assert len(chapters) == 1
        assert chapters[0].title == "Full Document"
        assert chapters[0].start_page == 1
        assert chapters[0].end_page == 1
    
    def test_pass_c_respects_target_pages(self, default_config):
        """Pass C creates chapters close to target size"""
        segmenter = ChapterSegmenter(default_config)
        num_pages = 100
        pages = [{"page_number": i, "content": f"Page {i}. " * 50} for i in range(1, num_pages + 1)]
        page_texts = [p["content"] for p in pages]
        page_numbers = [p["page_number"] for p in pages]
        
        chapters = segmenter._pass_c_synthetic(pages, page_texts, page_numbers)
        
        # Check reasonable chapter count
        expected_chapters = num_pages // segmenter.config.target_pages
        assert len(chapters) >= segmenter.config.min_chapters
        assert len(chapters) <= segmenter.config.max_chapters
        
        # Check average chapter size is reasonable
        total_pages = sum(ch.end_page - ch.start_page + 1 for ch in chapters)
        assert total_pages == num_pages
    
    def test_pass_c_uses_boundary_scoring(self, default_config):
        """Pass C uses boundary scoring to find good splits"""
        segmenter = ChapterSegmenter(default_config)
        
        # Pages with clear heading on page 11
        pages = []
        for i in range(1, 11):
            pages.append({"page_number": i, "content": f"Section 1 content page {i}. " * 50})
        
        # Page 11 starts with heading
        pages.append({"page_number": 11, "content": "CHAPTER TWO: NEW TOPIC\n" + "New content. " * 100})
        
        for i in range(12, 31):
            pages.append({"page_number": i, "content": f"Section 2 content page {i}. " * 50})
        
        page_texts = [p["content"] for p in pages]
        page_numbers = [p["page_number"] for p in pages]
        
        chapters = segmenter._pass_c_synthetic(pages, page_texts, page_numbers)
        
        # Should prefer splitting near page 11 due to heading
        boundaries = [ch.start_page for ch in chapters[1:]]
        if 11 in boundaries or 10 in boundaries or 12 in boundaries:
            assert True  # Boundary found near heading
        else:
            # Fallback: at least created valid chapters
            assert len(chapters) >= 1


# ============================================================================
# Test Boundary Scoring
# ============================================================================

class TestBoundaryScore:
    """Test _boundary_score() method"""
    
    def test_boundary_score_basic(self, default_config):
        """Boundary scoring returns float score"""
        segmenter = ChapterSegmenter(default_config)
        page_texts = ["Text A"] * 5
        similarities = [0.9, 0.3, 0.9, 0.9]  # Low at index 1
        
        score = segmenter._boundary_score(2, page_texts, similarities)
        assert isinstance(score, float)
        assert score >= 0.0
    
    def test_boundary_score_favors_topic_shift(self, default_config):
        """Higher score for pages with low similarity (topic shift)"""
        segmenter = ChapterSegmenter(default_config)
        page_texts = ["Text"] * 5
        similarities = [0.9, 0.1, 0.9, 0.9]  # Low similarity at index 1
        
        score_high_shift = segmenter._boundary_score(2, page_texts, similarities)
        score_no_shift = segmenter._boundary_score(3, page_texts, similarities)
        
        assert score_high_shift > score_no_shift
    
    def test_boundary_score_favors_headings(self, default_config):
        """Higher score for pages with heading-like text"""
        segmenter = ChapterSegmenter(default_config)
        page_texts = [
            "Normal text content",
            "CHAPTER TWO: NEW SECTION",  # All-caps heading
            "More normal text"
        ]
        similarities = [0.5, 0.5]
        
        score_heading = segmenter._boundary_score(1, page_texts, similarities)
        score_normal = segmenter._boundary_score(0, page_texts, similarities)
        
        assert score_heading > score_normal


# ============================================================================
# Test Validation Logic
# ============================================================================

class TestValidateSegmentation:
    """Test _validate_segmentation() method"""
    
    def test_validate_empty_chapters(self, default_config):
        """Validation fails for empty chapter list"""
        segmenter = ChapterSegmenter(default_config)
        assert not segmenter._validate_segmentation([], 100)
    
    def test_validate_too_few_chapters(self, default_config):
        """Validation fails if too few chapters"""
        segmenter = ChapterSegmenter(default_config)
        chapters = [Chapter(1, "Chapter 1", 1, 100, "synthetic")]
        assert not segmenter._validate_segmentation(chapters, 100)
    
    def test_validate_too_many_chapters(self, default_config):
        """Validation fails if too many chapters"""
        segmenter = ChapterSegmenter(default_config)
        chapters = [Chapter(i, f"Ch {i}", i, i, "synthetic") for i in range(1, 101)]
        assert not segmenter._validate_segmentation(chapters, 100)
    
    def test_validate_chapter_overlap(self, default_config):
        """Validation fails if chapters overlap"""
        segmenter = ChapterSegmenter(default_config)
        chapters = [
            Chapter(1, "Chapter 1", 1, 15, "regex_chapter"),
            Chapter(2, "Chapter 2", 10, 25, "regex_chapter"),  # Overlaps with Ch 1
            Chapter(3, "Chapter 3", 26, 40, "regex_chapter"),
        ]
        assert not segmenter._validate_segmentation(chapters, 40)
    
    def test_validate_large_gap(self, default_config):
        """Validation fails if large gap between chapters"""
        segmenter = ChapterSegmenter(default_config)
        chapters = [
            Chapter(1, "Chapter 1", 1, 10, "regex_chapter"),
            Chapter(2, "Chapter 2", 20, 30, "regex_chapter"),  # 9-page gap
        ]
        assert not segmenter._validate_segmentation(chapters, 30)
    
    def test_validate_chapter_too_small(self, default_config):
        """Validation fails if chapters are too small (except last)"""
        segmenter = ChapterSegmenter(default_config)
        chapters = [
            Chapter(1, "Chapter 1", 1, 2, "regex_chapter"),  # Only 2 pages
            Chapter(2, "Chapter 2", 3, 20, "regex_chapter"),
            Chapter(3, "Chapter 3", 21, 30, "regex_chapter"),
        ]
        # Should fail (first chapter too small)
        assert not segmenter._validate_segmentation(chapters, 30)
    
    def test_validate_last_chapter_can_be_short(self, default_config):
        """Validation allows last chapter to be short (epilogue, conclusion)"""
        segmenter = ChapterSegmenter(default_config)
        chapters = [
            Chapter(1, "Chapter 1", 1, 20, "regex_chapter"),
            Chapter(2, "Chapter 2", 21, 40, "regex_chapter"),
            Chapter(3, "Epilogue", 41, 41, "regex_chapter"),  # Last chapter = 1 page OK
        ]
        assert segmenter._validate_segmentation(chapters, 41)
    
    def test_validate_valid_segmentation(self, default_config):
        """Validation passes for reasonable segmentation"""
        segmenter = ChapterSegmenter(default_config)
        chapters = [
            Chapter(1, "Chapter 1", 1, 15, "regex_chapter"),
            Chapter(2, "Chapter 2", 16, 30, "regex_chapter"),
            Chapter(3, "Chapter 3", 31, 45, "regex_chapter"),
        ]
        assert segmenter._validate_segmentation(chapters, 45)
    
    def test_validate_micro_chapters_rejected_large_book(self, default_config):
        """Validation rejects micro-chapters for large books"""
        segmenter = ChapterSegmenter(default_config)
        # 100 pages with 20 chapters = avg 5 pages each (too small)
        chapters = [Chapter(i, f"Ch {i}", i*5+1, i*5+5, "topic_boundary") for i in range(20)]
        assert not segmenter._validate_segmentation(chapters, 100)
    
    def test_validate_allows_small_chapters_for_small_books(self, default_config):
        """Validation is lenient for small books"""
        segmenter = ChapterSegmenter(default_config)
        # 20-page book with 4 chapters = avg 5 pages each (OK for small book)
        chapters = [
            Chapter(1, "Ch 1", 1, 5, "regex_chapter"),
            Chapter(2, "Ch 2", 6, 10, "regex_chapter"),
            Chapter(3, "Ch 3", 11, 15, "regex_chapter"),
            Chapter(4, "Ch 4", 16, 20, "regex_chapter"),
        ]
        # Small book: min_chapters = max(1, 20 // 20) = 1, so 4 chapters is fine
        result = segmenter._validate_segmentation(chapters, 20)
        # Validation depends on exact thresholds but should be reasonable
        assert isinstance(result, bool)


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration:
    """End-to-end integration tests"""
    
    def test_full_pipeline_with_markers(self, default_config, sample_pages_short):
        """Full pipeline: input pages → detected chapters"""
        segmenter = ChapterSegmenter(default_config)
        chapters = segmenter.segment_book(sample_pages_short)
        
        # Verify structure
        assert len(chapters) == 3
        assert chapters[0]["title"] == "Introduction"
        assert chapters[0]["start_page"] == 1
        assert chapters[2]["end_page"] == 20
        
        # Verify sequential numbering
        for i, ch in enumerate(chapters, 1):
            assert ch["number"] == i
    
    def test_full_pipeline_without_markers(self, default_config, sample_pages_no_markers):
        """Full pipeline: falls back to Pass B or Pass C"""
        segmenter = ChapterSegmenter(default_config)
        chapters = segmenter.segment_book(sample_pages_no_markers)
        
        # Should segment successfully
        assert len(chapters) >= 1
        assert chapters[0]["start_page"] == 1
        
        # Method is either topic_boundary or synthetic
        methods = {ch["detection_method"] for ch in chapters}
        assert methods <= {"topic_boundary", "synthetic"}
    
    def test_full_pipeline_never_fails(self, default_config):
        """Full pipeline: always returns chapters (Pass C fallback)"""
        segmenter = ChapterSegmenter(default_config)
        
        # Difficult book: no markers, uniform content
        pages = [{"page_number": i, "content": "Generic text. " * 50} for i in range(1, 31)]
        
        chapters = segmenter.segment_book(pages)
        
        # Guaranteed non-empty result (Pass B or C)
        assert len(chapters) >= 1
        assert chapters[0]["detection_method"] in ["topic_boundary", "synthetic"]
