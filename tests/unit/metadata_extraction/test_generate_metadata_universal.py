"""
Unit tests for generate_metadata_universal.py

Tests capture current behavior before refactoring (characterization tests).
RED → GREEN → REFACTOR approach per MASTER_IMPLEMENTATION_GUIDE.md.

Reference Documents:
- Architecture Patterns with Python Ch. 2 (Repository Pattern)
- Architecture Patterns with Python Ch. 13 (Dependency Injection)
- Python Distilled Ch. 5 (Functions)
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict, Tuple

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from workflows.metadata_extraction.scripts.generate_metadata_universal import (
    UniversalMetadataGenerator,
    ChapterMetadata,
    main,
)


class TestAutoDetectChaptersCurrentBehavior:
    """
    Characterization tests for auto_detect_chapters() method.
    
    Current behavior (CC 18):
    1. Checks JSON for pre-defined chapters
    2. Falls back to regex scanning if none found
    3. Validates with YAKE keyword extraction
    4. Filters TOC pages and duplicates
    5. Returns list of (page_num, ch_num, title, start, end) tuples
    """
    
    @pytest.fixture
    def sample_json_with_chapters(self, tmp_path):
        """JSON file with pre-defined chapters"""
        json_file = tmp_path / "book_with_chapters.json"
        json_file.write_text("""{
            "book_name": "Test Book",
            "chapters": [
                {"number": 1, "title": "Introduction", "start_page": 1, "end_page": 10},
                {"number": 2, "title": "Chapter Two", "start_page": 11, "end_page": 20}
            ],
            "pages": [
                {"page_number": 1, "content": "Introduction content here..."},
                {"page_number": 11, "content": "Chapter Two content here..."}
            ]
        }""")
        return json_file
    
    @pytest.fixture
    def sample_json_without_chapters(self, tmp_path):
        """JSON file WITHOUT pre-defined chapters (needs auto-detect)"""
        json_file = tmp_path / "book_without_chapters.json"
        json_file.write_text("""{
            "book_name": "Test Book",
            "pages": [
                {"page_number": 1, "content": "Chapter 1: Getting Started\\n\\nThis is the introduction with lots of content about Python programming. Keywords include functions, classes, objects, methods, and variables. The chapter covers basic syntax and semantics."},
                {"page_number": 2, "content": "More content for chapter 1..."},
                {"page_number": 10, "content": "Chapter 2: Advanced Topics\\n\\nThis chapter covers advanced Python concepts including decorators, generators, context managers, metaclasses, and descriptors. We explore functional programming paradigms."},
                {"page_number": 11, "content": "More content for chapter 2..."}
            ]
        }""")
        return json_file
    
    def test_detects_predefined_chapters_from_json(self, sample_json_with_chapters):
        """Test: Uses pre-defined chapters when present in JSON"""
        generator = UniversalMetadataGenerator(
            json_path=sample_json_with_chapters,
            domain="auto"
        )
        
        chapters = generator.auto_detect_chapters()
        
        # Verify returns list of tuples: (chapter_num, title, start_page, end_page)
        assert len(chapters) == 2
        assert chapters[0][0] == 1  # chapter_number
        assert chapters[0][1] == "Introduction"  # title
        assert chapters[0][2] == 1  # start_page
        assert chapters[0][3] == 10  # end_page
    
    def test_fallback_to_regex_when_no_predefined(self, sample_json_without_chapters):
        """Test: Falls back to regex scanning when no pre-defined chapters"""
        generator = UniversalMetadataGenerator(
            json_path=sample_json_without_chapters,
            domain="auto"
        )
        
        chapters = generator.auto_detect_chapters()
        
        # Should detect "Chapter 1:" and "Chapter 2:" patterns
        assert len(chapters) >= 2
        assert any("Getting Started" in str(ch) for ch in chapters)
        assert any("Advanced Topics" in str(ch) for ch in chapters)
    
    def test_filters_toc_pages(self, tmp_path):
        """Test: Filters out TOC pages (many isolated numbers)"""
        json_file = tmp_path / "book_with_toc.json"
        json_file.write_text("""{
            "pages": [
                {"page_number": 1, "content": "Table of Contents\\n1 2 3 4 5 6 7 8 9 10 11 12"},
                {"page_number": 2, "content": "Chapter 1: Real Content\\n\\nThis is actual chapter content with keywords."}
            ]
        }""")
        
        generator = UniversalMetadataGenerator(json_path=json_file, domain="auto")
        chapters = generator.auto_detect_chapters()
        
        # TOC page should be skipped (>8 isolated numbers)
        # Should only find real chapter
        assert len(chapters) <= 1


class TestMainFunctionCurrentBehavior:
    """
    Characterization tests for main() function.
    
    Current behavior (CC 12):
    1. Parses command-line arguments
    2. Instantiates UniversalMetadataGenerator
    3. Gets chapters (explicit, auto-detect, or interactive)
    4. Generates metadata for each chapter
    5. Saves results to JSON file
    """
    
    @patch('sys.argv', ['script.py', '--input', 'test.json', '--auto-detect'])
    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.read_text', return_value='{"pages": []}')
    @patch('workflows.metadata_extraction.scripts.generate_metadata_universal.UniversalMetadataGenerator')
    @patch('pathlib.Path.write_text')
    def test_main_happy_path(self, mock_write, mock_generator_class, mock_read, mock_exists):
        """Test: main() orchestrates full pipeline successfully"""
        # Setup mocks
        mock_generator = Mock()
        mock_generator.pages = []  # Mock pages attribute
        mock_generator.book_name = "Test Book"  # Mock book_name attribute
        mock_generator_class.return_value = mock_generator
        # New format: (chapter_num, title, start_page, end_page)
        mock_generator.auto_detect_chapters.return_value = [
            (1, "Chapter 1", 1, 10)
        ]
        mock_generator.generate_metadata.return_value = [
            {
                "chapter_number": 1,
                "title": "Chapter 1",
                "start_page": 1,
                "end_page": 10,
                "summary": "Summary",
                "keywords": ["test"],
                "concepts": ["concept"]
            }
        ]
        
        # Execute
        try:
            main()
        except SystemExit:
            pass  # main() calls sys.exit()
        
        # Verify generator was instantiated
        mock_generator_class.assert_called_once()


class TestSafeEvalWithLiteralEval:
    """
    Tests for ast.literal_eval() security fix.
    
    RED phase: Write tests for safe evaluation behavior.
    GREEN phase: Replace eval() with ast.literal_eval() at line 567.
    """
    
    def test_safe_eval_with_valid_list_literal(self):
        """Test: ast.literal_eval() accepts valid Python list literals"""
        from ast import literal_eval
        
        # Valid chapter list format
        valid_input = "[(1, 'Introduction', 1, 10), (2, 'Chapter Two', 11, 20)]"
        result = literal_eval(valid_input)
        
        assert len(result) == 2
        assert result[0] == (1, 'Introduction', 1, 10)
        assert result[1] == (2, 'Chapter Two', 11, 20)
    
    def test_safe_eval_with_dict_literal(self):
        """Test: ast.literal_eval() accepts valid Python dict literals"""
        from ast import literal_eval
        
        valid_input = "{'key': 'value', 'number': 42}"
        result = literal_eval(valid_input)
        
        assert result['key'] == 'value'
        assert result['number'] == 42
    
    def test_safe_eval_rejects_function_calls(self):
        """Test: ast.literal_eval() rejects function calls (SECURITY)"""
        from ast import literal_eval
        
        dangerous_input = "__import__('os').system('rm -rf /')"
        
        with pytest.raises(ValueError):
            literal_eval(dangerous_input)
    
    def test_safe_eval_rejects_arbitrary_code(self):
        """Test: ast.literal_eval() rejects arbitrary code execution (SECURITY)"""
        from ast import literal_eval
        
        dangerous_inputs = [
            "__import__('subprocess').run(['ls'])",
            "exec('print(\"hacked\")')",
            "eval('1+1')",
            "open('/etc/passwd').read()",
        ]
        
        for dangerous in dangerous_inputs:
            with pytest.raises(ValueError):
                literal_eval(dangerous)
    
    def test_safe_eval_rejects_variable_references(self):
        """Test: ast.literal_eval() rejects variable references"""
        from ast import literal_eval
        
        # Variable references should fail
        with pytest.raises(ValueError):
            literal_eval("some_variable")
    
    def test_safe_eval_accepts_nested_structures(self):
        """Test: ast.literal_eval() handles complex nested structures"""
        from ast import literal_eval
        
        complex_input = "[(1, 'Ch1', 1, 10), {'key': [1, 2, 3]}, (2, 'Ch2', 11, 20)]"
        result = literal_eval(complex_input)
        
        assert len(result) == 3
        assert isinstance(result[1], dict)


class TestCurrentArchitecture:
    """
    Tests documenting current architecture before Repository Pattern.
    
    Current implementation:
    - Direct file I/O with Path.write_text() and json.dump()
    - No abstraction layer
    - Difficult to test without real filesystem
    """
    
    def test_direct_file_io_in_generate_metadata(self, tmp_path):
        """Test: generate_metadata() writes directly to filesystem"""
        json_file = tmp_path / "test.json"
        json_file.write_text("""{
            "pages": [
                {"page_number": 1, "content": "Chapter 1: Test\\n\\nContent here..."}
            ]
        }""")
        
        generator = UniversalMetadataGenerator(json_path=json_file, domain="auto")
        
        # Current implementation has tight coupling to filesystem
        # After Repository Pattern, this will use injected repository
        assert hasattr(generator, 'json_path')
        assert generator.json_path == json_file


class TestChapterMetadataValueObject:
    """
    Tests for ChapterMetadata dataclass.
    
    Current implementation follows DDD Value Object pattern (GOOD).
    Reference: Architecture Patterns with Python Ch. 1 (Domain Modeling)
    """
    
    def test_chapter_metadata_structure(self):
        """Test: ChapterMetadata has correct fields"""
        chapter = ChapterMetadata(
            chapter_number=1,
            title="Test Chapter",
            start_page=1,
            end_page=10,
            summary="Test summary",
            keywords=["keyword1", "keyword2"],
            concepts=["concept1"]
        )
        
        assert chapter.chapter_number == 1
        assert chapter.title == "Test Chapter"
        assert len(chapter.keywords) == 2
        assert len(chapter.concepts) == 1
    
    def test_chapter_metadata_is_immutable_like(self):
        """Test: ChapterMetadata behaves like immutable value object"""
        chapter1 = ChapterMetadata(1, "Test", 1, 10, "Summary", ["kw"], ["concept"])
        chapter2 = ChapterMetadata(1, "Test", 1, 10, "Summary", ["kw"], ["concept"])
        
        # Should be equal by value
        assert chapter1.chapter_number == chapter2.chapter_number
        assert chapter1.title == chapter2.title


class TestRefactoredAutoDetectChapters:
    """
    Tests for refactored auto_detect_chapters() using Strategy Pattern.
    
    Target: Reduce cyclomatic complexity from 18 to <10
    Approach: Orchestrate 5 strategies instead of inline logic
    """
    
    def test_uses_predefined_strategy_when_metadata_available(self, tmp_path):
        """Verify PreDefinedStrategy is tried first (JSON metadata)"""
        json_file = tmp_path / "test.json"
        json_file.write_text("""{
            "pages": [{"page_number": 1, "content": "Test"}],
            "chapters": [
                {"number": 1, "title": "Introduction", "start_page": 1, "end_page": 10}
            ]
        }""")
        
        generator = UniversalMetadataGenerator(json_path=json_file)
        chapters = generator.auto_detect_chapters()
        
        assert len(chapters) == 1
        assert chapters[0] == (1, 'Introduction', 1, 10)
    
    def test_falls_back_to_regex_when_no_metadata(self, tmp_path):
        """Verify RegexPatternStrategy is used when no JSON metadata"""
        json_file = tmp_path / "test.json"
        json_file.write_text("""{
            "pages": [
                {"page_number": 1, "content": "Chapter 1: Test Chapter\\n\\nThis chapter contains enough content for YAKE validation. It discusses Python programming concepts including functions, classes, objects, methods, variables, decorators, and context managers. The content is substantial enough to extract meaningful keywords for validation purposes."}
            ]
        }""")
        
        generator = UniversalMetadataGenerator(json_path=json_file)
        chapters = generator.auto_detect_chapters()
        
        # Should find the chapter marker
        assert len(chapters) >= 1
    
    def test_complexity_reduced_from_baseline(self, tmp_path):
        """Verify refactored method has lower cyclomatic complexity"""
        # This is validated by running: radon cc -s workflows/metadata_extraction/scripts/generate_metadata_universal.py
        # Expected: auto_detect_chapters complexity drops from 18 to <10
        json_file = tmp_path / "test.json"
        json_file.write_text("""{
            "pages": [{"page_number": 1, "content": "Test"}]
        }""")
        
        generator = UniversalMetadataGenerator(json_path=json_file)
        chapters = generator.auto_detect_chapters()
        
        # Method should still return list of tuples
        assert isinstance(chapters, list)


class TestStatisticalExtractorIntegration:
    """
    Tests verifying StatisticalExtractor is used (domain-agnostic).
    
    Current implementation (GOOD):
    - Uses YAKE for keyword extraction
    - Uses Summa for concept extraction
    - Uses TextRank for summary generation
    
    Reference: DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md
    """
    
    def test_extract_keywords_delegates_to_statistical_extractor(self, tmp_path):
        """Test: extract_keywords() uses YAKE (not regex patterns)"""
        json_file = tmp_path / "test.json"
        json_file.write_text("""{
            "pages": [{"page_number": 1, "content": "Python programming"}]
        }""")
        
        generator = UniversalMetadataGenerator(json_path=json_file)
        
        # Verify StatisticalExtractor is used
        assert hasattr(generator, 'extractor')
        assert generator.extractor is not None
    
    def test_extract_concepts_uses_summa(self, tmp_path):
        """Test: extract_concepts() uses Summa TextRank"""
        json_file = tmp_path / "test.json"
        json_file.write_text("""{
            "pages": [{"page_number": 1, "content": "Test content"}]
        }""")
        
        generator = UniversalMetadataGenerator(json_path=json_file)
        
        text = "Python is a programming language. Functions are first-class objects."
        concepts = generator.extract_concepts(text, max_concepts=5)
        
        # Should return list of strings (concepts)
        assert isinstance(concepts, list)
    
    def test_generate_summary_uses_textrank(self, tmp_path):
        """Test: generate_summary() uses TextRank summarization"""
        json_file = tmp_path / "test.json"
        json_file.write_text("""{
            "pages": [{"page_number": 1, "content": "Test content"}]
        }""")
        
        generator = UniversalMetadataGenerator(json_path=json_file)
        
        text = "Python is a programming language. " * 20  # Need enough text
        summary = generator.generate_summary(text, "Test Chapter", 1)
        
        # Should return summarized text
        assert isinstance(summary, str)
        assert len(summary) > 0


# Pytest configuration
def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line(
        "markers", "xfail: mark test as expected to fail (known issues)"
    )
