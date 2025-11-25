"""
Tests for Chapter Detection Strategy Pattern

RED → GREEN → REFACTOR approach to extract detection logic from auto_detect_chapters().
Target: Reduce CC from 18 to <10 using Strategy Pattern.

Reference: Architecture Patterns with Python Ch. 13 (Dependency Injection)
"""
import pytest
from typing import List, Dict, Protocol
from pathlib import Path


class ChapterDetectionStrategy(Protocol):
    """
    Protocol for chapter detection strategies.
    
    All strategies must implement detect() method per Liskov Substitution Principle.
    Reference: Architecture Patterns with Python Ch. 4 (Adapter Pattern)
    """
    
    def detect(self, pages: List[Dict], **kwargs) -> List[tuple]:
        """
        Detect chapters from pages.
        
        Args:
            pages: List of page dicts with {page_number, content}
            **kwargs: Strategy-specific parameters
        
        Returns:
            List of (chapter_num, title, start_page, end_page) tuples
        """
        ...


class TestPreDefinedStrategy:
    """
    Tests for PreDefinedStrategy - extracts chapters from JSON metadata.
    
    This is the FIRST strategy tried (highest priority).
    """
    
    def test_extracts_predefined_chapters_from_metadata(self):
        """Test: Extracts chapters when present in JSON"""
        from workflows.metadata_extraction.scripts.strategies.predefined_strategy import PreDefinedStrategy
        
        metadata = {
            "chapters": [
                {"number": 1, "title": "Introduction", "start_page": 1, "end_page": 10},
                {"number": 2, "title": "Chapter Two", "start_page": 11, "end_page": 20}
            ]
        }
        
        strategy = PreDefinedStrategy(metadata)
        chapters = strategy.detect(pages=[])  # Pages not needed for pre-defined
        
        assert len(chapters) == 2
        # Format: (chapter_num, title, start_page, end_page)
        assert chapters[0] == (1, "Introduction", 1, 10)
        assert chapters[1] == (2, "Chapter Two", 11, 20)
    
    def test_returns_empty_when_no_metadata(self):
        """Test: Returns empty list when no pre-defined chapters"""
        from workflows.metadata_extraction.scripts.strategies.predefined_strategy import PreDefinedStrategy
        
        metadata = {}  # No chapters key
        
        strategy = PreDefinedStrategy(metadata)
        chapters = strategy.detect(pages=[])
        
        assert len(chapters) == 0
    
    def test_handles_malformed_metadata(self):
        """Test: Gracefully handles malformed chapter metadata"""
        from workflows.metadata_extraction.scripts.strategies.predefined_strategy import PreDefinedStrategy
        
        metadata = {
            "chapters": [
                {"number": 1},  # Missing required fields
                {"title": "Bad", "start_page": 10}  # Missing number
            ]
        }
        
        strategy = PreDefinedStrategy(metadata)
        chapters = strategy.detect(pages=[])
        
        # Should skip malformed entries
        assert len(chapters) == 0


class TestRegexPatternStrategy:
    """
    Tests for RegexPatternStrategy - finds chapter markers using regex.
    
    Detects patterns like:
    - "Chapter 1: Title"
    - "CHAPTER 1: Title"
    - "Item 1: Title"
    """
    
    def test_detects_chapter_pattern(self):
        """Test: Finds 'Chapter N: Title' pattern"""
        from workflows.metadata_extraction.scripts.strategies.regex_pattern_strategy import RegexPatternStrategy
        
        pages = [
            {"page_number": 1, "content": "Chapter 1: Getting Started\n\nLots of content here to meet minimum length requirements for detection."},
            {"page_number": 10, "content": "Chapter 2: Advanced Topics\n\nMore content to ensure proper detection works."}
        ]
        
        strategy = RegexPatternStrategy()
        chapters = strategy.detect(pages)
        
        assert len(chapters) >= 2
        assert any("Getting Started" in str(ch) for ch in chapters)
        assert any("Advanced Topics" in str(ch) for ch in chapters)
    
    def test_detects_uppercase_chapter_pattern(self):
        """Test: Handles CHAPTER (uppercase) variant"""
        from workflows.metadata_extraction.scripts.strategies.regex_pattern_strategy import RegexPatternStrategy
        
        pages = [
            {"page_number": 1, "content": "CHAPTER 1: INTRODUCTION\n\nContent with enough text to meet minimum requirements."}
        ]
        
        strategy = RegexPatternStrategy()
        chapters = strategy.detect(pages)
        
        assert len(chapters) >= 1
        assert any("INTRODUCTION" in str(ch) for ch in chapters)
    
    def test_detects_item_pattern(self):
        """Test: Detects 'Item N: Title' pattern (for Effective Python style)"""
        from workflows.metadata_extraction.scripts.strategies.regex_pattern_strategy import RegexPatternStrategy
        
        pages = [
            {"page_number": 1, "content": "Item 1: Know Which Version of Python You're Using\n\nDetails with enough content..."}
        ]
        
        strategy = RegexPatternStrategy()
        chapters = strategy.detect(pages)
        
        assert len(chapters) >= 1
        assert any("Which Version" in str(ch) for ch in chapters)
    
    def test_returns_empty_for_no_patterns(self):
        """Test: Returns empty list when no chapter markers found"""
        from workflows.metadata_extraction.scripts.strategies.regex_pattern_strategy import RegexPatternStrategy
        
        pages = [
            {"page_number": 1, "content": "Just regular text with no chapter markers."}
        ]
        
        strategy = RegexPatternStrategy()
        chapters = strategy.detect(pages)
        
        assert len(chapters) == 0


class TestYAKEValidationStrategy:
    """
    Tests for YAKEValidationStrategy - validates chapters have real content.
    
    Uses YAKE keyword extraction to filter out TOC pages and other noise.
    Reference: DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md
    """
    
    def test_validates_chapter_has_keywords(self):
        """Test: Accepts chapters with sufficient keywords (real content)"""
        from workflows.metadata_extraction.scripts.strategies.yake_validation_strategy import YAKEValidationStrategy
        from workflows.metadata_extraction.scripts.adapters.statistical_extractor import StatisticalExtractor
        
        candidate_chapters = [
            (1, "Real Chapter", 1, 10)
        ]
        
        # Need substantial content for YAKE to work (800+ chars minimum)
        content = " ".join([
            "Python programming language includes functions classes objects methods variables decorators generators",
            "iterators comprehensions metaclasses descriptors context managers protocols type hints annotations",
            "asyncio coroutines async await concurrency parallelism threads processes multiprocessing threading",
            "data structures lists tuples dictionaries sets frozensets collections namedtuple deque defaultdict",
            "algorithms sorting searching recursion dynamic programming memoization caching optimization performance",
            "testing unittest pytest fixtures mocks assertions parametrize coverage integration unit tests",
            "documentation docstrings type hints annotations sphinx autodoc napoleon google style pep257",
            "error handling exceptions try except finally raise custom exceptions traceback debugging logging",
        ])
        
        pages = [
            {"page_number": 1, "content": content}
        ]
        
        extractor = StatisticalExtractor()
        strategy = YAKEValidationStrategy(extractor, min_keywords=3)
        validated = strategy.validate(candidate_chapters, pages)
        
        assert len(validated) >= 1  # Should pass validation
    
    def test_rejects_chapters_with_few_keywords(self):
        """Test: Rejects chapters with insufficient keywords (likely TOC)"""
        from workflows.metadata_extraction.scripts.strategies.yake_validation_strategy import YAKEValidationStrategy
        from workflows.metadata_extraction.scripts.adapters.statistical_extractor import StatisticalExtractor
        
        candidate_chapters = [
            (1, "TOC Entry", 1, 1)
        ]
        
        pages = [
            {"page_number": 1, "content": "Chapter 1....5"}  # Too short, no real keywords
        ]
        
        extractor = StatisticalExtractor()
        strategy = YAKEValidationStrategy(extractor, min_keywords=5)
        validated = strategy.validate(candidate_chapters, pages)
        
        assert len(validated) == 0  # Should fail validation


class TestTOCFilterStrategy:
    """
    Tests for TOCFilterStrategy - removes Table of Contents pages.
    
    TOC pages have many isolated numbers (page references).
    Heuristic: >8 isolated digits = TOC page
    """
    
    def test_filters_toc_pages(self):
        """Test: Removes pages with many isolated numbers"""
        from workflows.metadata_extraction.scripts.strategies.toc_filter_strategy import TOCFilterStrategy
        
        candidate_chapters = [
            (1, "TOC", 1, 1),
            (2, "Real Chapter", 2, 10)
        ]
        
        pages = [
            {"page_number": 1, "content": "Table of Contents\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15"},  # More numbers for clear TOC
            {"page_number": 2, "content": "Chapter 1: Real Content\n\nLots of text here..."}
        ]
        
        strategy = TOCFilterStrategy(threshold=8)
        filtered = strategy.filter(candidate_chapters, pages)
        
        assert len(filtered) == 1
        assert filtered[0][1] == "Real Chapter"
    
    def test_keeps_normal_pages(self):
        """Test: Keeps pages with few isolated numbers"""
        from workflows.metadata_extraction.scripts.strategies.toc_filter_strategy import TOCFilterStrategy
        
        candidate_chapters = [
            (1, "Chapter 1", 1, 10)
        ]
        
        pages = [
            {"page_number": 1, "content": "Chapter 1 discusses Python 3.11 features."}
        ]
        
        strategy = TOCFilterStrategy(threshold=8)
        filtered = strategy.filter(candidate_chapters, pages)
        
        assert len(filtered) == 1


class TestDuplicateFilterStrategy:
    """
    Tests for DuplicateFilterStrategy - removes duplicate chapter numbers.
    
    Duplicates occur in headers/footers across pages.
    Keep FIRST valid occurrence only.
    """
    
    def test_removes_duplicate_chapter_numbers(self):
        """Test: Keeps only first occurrence of each chapter number"""
        from workflows.metadata_extraction.scripts.strategies.duplicate_filter_strategy import DuplicateFilterStrategy
        
        candidate_chapters = [
            (1, "Chapter 1", 1, 10),
            (1, "Chapter 1", 5, 10),  # Duplicate (header on page 5)
            (1, "Chapter 1", 8, 10),  # Duplicate (header on page 8)
            (2, "Chapter 2", 11, 20)
        ]
        
        strategy = DuplicateFilterStrategy()
        unique = strategy.filter(candidate_chapters)
        
        assert len(unique) == 2
        assert unique[0] == (1, "Chapter 1", 1, 10)  # First occurrence kept
        assert unique[1] == (2, "Chapter 2", 11, 20)
    
    def test_preserves_order(self):
        """Test: Sorts by page number (ascending)"""
        from workflows.metadata_extraction.scripts.strategies.duplicate_filter_strategy import DuplicateFilterStrategy
        
        candidate_chapters = [
            (20, "Chapter 3", 20, 30),
            (1, "Chapter 1", 1, 10),
            (11, "Chapter 2", 11, 20)
        ]
        
        strategy = DuplicateFilterStrategy()
        unique = strategy.filter(candidate_chapters)
        
        # Should be sorted by start_page (ascending)
        assert unique[0][0] == 1  # First chapter
        assert unique[1][0] == 11  # Second chapter
        assert unique[2][0] == 20  # Third chapter


class TestStrategyComposition:
    """
    Integration tests for strategy composition.
    
    Tests that strategies can be chained together:
    PreDefined → Regex → YAKE → TOC Filter → Duplicate Filter
    """
    
    def test_strategy_pipeline_with_all_filters(self):
        """Test: Full strategy pipeline reduces noise effectively"""
        # This will be integration test after all strategies implemented
        pass
    
    def test_strategies_follow_protocol(self):
        """Test: All strategies implement ChapterDetectionStrategy protocol"""
        from workflows.metadata_extraction.scripts.strategies.predefined_strategy import PreDefinedStrategy
        from workflows.metadata_extraction.scripts.strategies.regex_pattern_strategy import RegexPatternStrategy
        
        # All strategies should have detect/filter/validate methods
        assert hasattr(PreDefinedStrategy, 'detect') or hasattr(PreDefinedStrategy, '__call__')
        assert hasattr(RegexPatternStrategy, 'detect') or hasattr(RegexPatternStrategy, '__call__')
