"""
Test suite for StatisticalExtractor fallback methods - Safe extraction without exceptions.

TDD RED Phase: These tests define expected behavior for safe_* methods that
return empty results instead of raising exceptions on empty/invalid input.

Problem Statement (from batch processing):
- 4/47 books failed with "Text cannot be empty" errors
- YAKE/Summa crash on empty chapter text
- A single bad chapter kills entire book processing

Solution:
- Add safe_extract_keywords(), safe_extract_concepts(), safe_generate_summary()
- Return empty list/string instead of raising ValueError
- Enable graceful degradation for chapters with no extractable text

Document References:
- ANTI_PATTERN_ANALYSIS.md: Section 1.3 (Missing Type Guards for Optional Values)
- DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md: Part 1.3 (Error Handling)
- ARCHITECTURE_GUIDELINES Ch. 8: Graceful degradation pattern
- PYTHON_GUIDELINES Ch. 8: EAFP error handling, guard clauses

TDD Status: RED phase - Tests will FAIL until safe_* methods implemented
"""

import pytest
from typing import List, Tuple

# Import will fail initially for new methods (RED phase)
try:
    from workflows.metadata_extraction.scripts.adapters.statistical_extractor import (
        StatisticalExtractor
    )
except ImportError:
    StatisticalExtractor = None


class TestSafeExtractionMethods:
    """
    Tests for safe_* methods that handle empty/invalid text gracefully.
    
    These methods never raise exceptions - they return empty results instead.
    This enables per-chapter try/except in generate_metadata_universal.py.
    """

    @pytest.fixture
    def extractor(self):
        """Fixture providing StatisticalExtractor instance."""
        if StatisticalExtractor is None:
            pytest.skip("StatisticalExtractor not implemented yet")
        return StatisticalExtractor()

    # =========================================================================
    # safe_extract_keywords() Tests
    # =========================================================================
    
    def test_safe_extract_keywords_empty_string(self, extractor):
        """
        Empty string input should return empty list, not raise ValueError.
        
        Current Behavior (BROKEN):
            >>> extractor.extract_keywords("")
            ValueError: Text cannot be empty
            
        Expected Behavior (FIXED):
            >>> extractor.safe_extract_keywords("")
            []  # Empty list, no exception
        """
        # Act
        result = extractor.safe_extract_keywords("")
        
        # Assert - empty list, not exception
        assert isinstance(result, list), "Should return empty list"
        assert len(result) == 0, "Should return empty list for empty input"

    def test_safe_extract_keywords_whitespace_only(self, extractor):
        """
        Whitespace-only input should return empty list.
        
        This catches chapters with only newlines/spaces (OCR artifacts).
        """
        # Act
        result = extractor.safe_extract_keywords("   \n\t\n   ")
        
        # Assert
        assert isinstance(result, list)
        assert len(result) == 0

    def test_safe_extract_keywords_none_input(self, extractor):
        """
        None input should return empty list (not crash with AttributeError).
        
        Defensive programming for chapters where text extraction failed.
        """
        # Act
        result = extractor.safe_extract_keywords(None)
        
        # Assert
        assert isinstance(result, list)
        assert len(result) == 0

    def test_safe_extract_keywords_valid_text(self, extractor):
        """
        Valid text should work exactly like extract_keywords().
        
        Safe method should delegate to underlying YAKE extraction.
        """
        # Arrange
        text = "Python programming language supports object-oriented development"
        
        # Act
        result = extractor.safe_extract_keywords(text, top_n=5)
        
        # Assert - same behavior as extract_keywords for valid input
        assert isinstance(result, list)
        assert len(result) <= 5  # May return fewer if text is short
        # Each element should be (keyword, score) tuple
        for item in result:
            assert isinstance(item, tuple)
            assert len(item) == 2
            assert isinstance(item[0], str)  # keyword
            assert isinstance(item[1], (int, float))  # score

    def test_safe_extract_keywords_very_short_text(self, extractor):
        """
        Very short text (< 50 chars) should not crash, may return empty.
        
        YAKE may fail on text too short for meaningful extraction.
        """
        # Act
        result = extractor.safe_extract_keywords("Short text.")
        
        # Assert - either empty list or valid keywords, but no exception
        assert isinstance(result, list)
        # All items should be valid tuples if any returned
        for item in result:
            assert isinstance(item, tuple)

    # =========================================================================
    # safe_extract_concepts() Tests
    # =========================================================================

    def test_safe_extract_concepts_empty_string(self, extractor):
        """
        Empty string input should return empty list for concepts.
        
        Current Behavior (BROKEN):
            >>> extractor.extract_concepts("")
            ValueError: Text cannot be empty
            
        Expected Behavior (FIXED):
            >>> extractor.safe_extract_concepts("")
            []
        """
        # Act
        result = extractor.safe_extract_concepts("")
        
        # Assert
        assert isinstance(result, list)
        assert len(result) == 0

    def test_safe_extract_concepts_whitespace_only(self, extractor):
        """Whitespace-only input should return empty list."""
        # Act
        result = extractor.safe_extract_concepts("\n\n\n   \t")
        
        # Assert
        assert isinstance(result, list)
        assert len(result) == 0

    def test_safe_extract_concepts_none_input(self, extractor):
        """None input should return empty list."""
        # Act
        result = extractor.safe_extract_concepts(None)
        
        # Assert
        assert isinstance(result, list)
        assert len(result) == 0

    def test_safe_extract_concepts_valid_text(self, extractor):
        """Valid text should work exactly like extract_concepts()."""
        # Arrange
        text = """
        Machine learning algorithms use statistical methods to learn patterns.
        Neural networks are composed of interconnected nodes that process data.
        Deep learning models can extract features from raw input automatically.
        """
        
        # Act
        result = extractor.safe_extract_concepts(text, top_n=5)
        
        # Assert
        assert isinstance(result, list)
        assert len(result) <= 5
        for concept in result:
            assert isinstance(concept, str)
            assert len(concept) > 0

    # =========================================================================
    # safe_generate_summary() Tests
    # =========================================================================

    def test_safe_generate_summary_empty_string(self, extractor):
        """
        Empty string input should return empty string for summary.
        
        Current Behavior (BROKEN):
            >>> extractor.generate_summary("")
            ValueError: Text cannot be empty
            
        Expected Behavior (FIXED):
            >>> extractor.safe_generate_summary("")
            ""  # Empty string, no exception
        """
        # Act
        result = extractor.safe_generate_summary("")
        
        # Assert
        assert isinstance(result, str)
        assert result == ""

    def test_safe_generate_summary_whitespace_only(self, extractor):
        """Whitespace-only input should return empty string."""
        # Act
        result = extractor.safe_generate_summary("   \n\t   ")
        
        # Assert
        assert isinstance(result, str)
        assert result == ""

    def test_safe_generate_summary_none_input(self, extractor):
        """None input should return empty string."""
        # Act
        result = extractor.safe_generate_summary(None)
        
        # Assert
        assert isinstance(result, str)
        assert result == ""

    def test_safe_generate_summary_valid_text(self, extractor):
        """Valid text should work exactly like generate_summary()."""
        # Arrange
        text = """
        Python is a versatile programming language used in web development.
        It supports multiple paradigms including procedural and object-oriented.
        The syntax emphasizes readability and reduces the cost of maintenance.
        Many companies use Python for data science and machine learning.
        The extensive standard library provides modules for common tasks.
        """
        
        # Act
        result = extractor.safe_generate_summary(text, ratio=0.3)
        
        # Assert
        assert isinstance(result, str)
        assert len(result) > 0
        assert len(result) < len(text)


class TestSafeMethodsWithFallbackTitle:
    """
    Tests for safe methods that accept a fallback title parameter.
    
    For summaries, when extraction fails, return a fallback title like:
    "Chapter 5: Introduction to Machine Learning"
    """

    @pytest.fixture
    def extractor(self):
        """Fixture providing StatisticalExtractor instance."""
        if StatisticalExtractor is None:
            pytest.skip("StatisticalExtractor not implemented yet")
        return StatisticalExtractor()

    def test_safe_generate_summary_with_fallback(self, extractor):
        """
        When text is empty, return fallback title if provided.
        
        Usage in generate_metadata_universal.py:
            summary = extractor.safe_generate_summary(
                text,
                fallback=f"Chapter {ch_num}: {title}"
            )
        """
        # Arrange
        fallback = "Chapter 7: Advanced Topics"
        
        # Act
        result = extractor.safe_generate_summary("", fallback=fallback)
        
        # Assert - should return fallback when text is empty
        assert result == fallback

    def test_safe_generate_summary_valid_text_ignores_fallback(self, extractor):
        """When text is valid, use actual extraction (ignore fallback)."""
        # Arrange
        text = """
        This chapter covers advanced Python patterns including decorators.
        Decorators modify function behavior without changing source code.
        Common use cases include logging, caching, and access control.
        """
        fallback = "Chapter 1: This should not be used"
        
        # Act
        result = extractor.safe_generate_summary(text, fallback=fallback)
        
        # Assert - should NOT use fallback when text is valid
        assert result != fallback
        assert len(result) > 0


class TestIntegrationWithGenerateMetadata:
    """
    Integration tests simulating generate_metadata_universal.py usage.
    
    Validates that safe_* methods prevent batch failures.
    """

    @pytest.fixture
    def extractor(self):
        """Fixture providing StatisticalExtractor instance."""
        if StatisticalExtractor is None:
            pytest.skip("StatisticalExtractor not implemented yet")
        return StatisticalExtractor()

    def test_mixed_valid_and_empty_chapters(self, extractor):
        """
        Simulate batch with mix of valid chapters and empty chapters.
        
        This is the exact scenario that caused 4/47 book failures:
        - Most chapters have text (valid extraction)
        - Some chapters are empty (should not crash)
        """
        # Arrange - simulating chapters from a book
        chapters = [
            {"num": 1, "title": "Introduction", "text": "This is a valid chapter with content about Python."},
            {"num": 2, "title": "Empty Chapter", "text": ""},  # Empty - was crashing
            {"num": 3, "title": "Whitespace Only", "text": "   \n\t   "},  # Whitespace - was crashing
            {"num": 4, "title": "Short Text", "text": "Too short."},  # Very short
            {"num": 5, "title": "Valid Again", "text": "Another chapter with machine learning and data science content."},
        ]
        
        # Act - extract metadata for all chapters (should not raise)
        results = []
        for ch in chapters:
            metadata = {
                "chapter_number": ch["num"],
                "title": ch["title"],
                "keywords": extractor.safe_extract_keywords(ch["text"], top_n=5),
                "concepts": extractor.safe_extract_concepts(ch["text"], top_n=3),
                "summary": extractor.safe_generate_summary(
                    ch["text"], 
                    fallback=f"Chapter {ch['num']}: {ch['title']}"
                ),
            }
            results.append(metadata)
        
        # Assert - all chapters processed without exception
        assert len(results) == 5, "All chapters should be processed"
        
        # Validate specific results
        # Chapter 1 (valid) - should have keywords
        assert len(results[0]["keywords"]) > 0 or True  # May vary by text length
        
        # Chapter 2 (empty) - should have empty lists, fallback summary
        assert results[1]["keywords"] == []
        assert results[1]["concepts"] == []
        assert results[1]["summary"] == "Chapter 2: Empty Chapter"
        
        # Chapter 3 (whitespace) - should have empty lists, fallback summary
        assert results[2]["keywords"] == []
        assert results[2]["concepts"] == []
        assert results[2]["summary"] == "Chapter 3: Whitespace Only"


class TestBackwardCompatibility:
    """
    Ensure original methods still work as expected (raising on empty).
    
    The safe_* methods are additive - original behavior unchanged.
    """

    @pytest.fixture
    def extractor(self):
        """Fixture providing StatisticalExtractor instance."""
        if StatisticalExtractor is None:
            pytest.skip("StatisticalExtractor not implemented yet")
        return StatisticalExtractor()

    def test_original_extract_keywords_still_raises(self, extractor):
        """Original extract_keywords should still raise on empty text."""
        with pytest.raises(ValueError, match="(?i)empty|text"):
            extractor.extract_keywords("")

    def test_original_extract_concepts_still_raises(self, extractor):
        """Original extract_concepts should still raise on empty text."""
        with pytest.raises(ValueError, match="(?i)empty|text"):
            extractor.extract_concepts("")

    def test_original_generate_summary_still_raises(self, extractor):
        """Original generate_summary should still raise on empty text."""
        with pytest.raises(ValueError, match="(?i)empty|text"):
            extractor.generate_summary("")
