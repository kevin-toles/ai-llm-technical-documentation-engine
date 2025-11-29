#!/usr/bin/env python3
"""
TDD Tests for _extract_first_substantial_paragraph (RED Phase)

Following TDD RED → GREEN → REFACTOR cycle for Phase 5 Task 5.1.

References:
    - MASTER_IMPLEMENTATION_GUIDE Phase 5 Task 5.1
    - ANTI_PATTERN_ANALYSIS §10.2: Extract Method pattern
    - Architecture Patterns Ch. 3: Extract Method refactoring
    - Python Guidelines Ch. 7: String slicing and text processing

Test Strategy:
    1. Write failing tests first (RED)
    2. Implement minimal code to pass (GREEN)
    3. Refactor to align with guidelines (REFACTOR)
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from workflows.base_guideline_generation.scripts.chapter_generator_all_text import (
    _extract_first_substantial_paragraph
)


class TestExtractFirstSubstantialParagraph:
    """
    Test suite for _extract_first_substantial_paragraph helper function.
    
    Function should extract the first paragraph that:
    - Exceeds minimum length threshold (100 chars)
    - Truncates to max_length with ellipsis if needed
    - Handles edge cases (no breaks, all short paragraphs, empty text)
    
    References:
        - Architecture Patterns Ch. 3: Extract Method pattern
        - ANTI_PATTERN_ANALYSIS §10.2: Helper function best practices
    """
    
    def test_extracts_first_paragraph_over_threshold(self):
        """
        RED: Test extraction of first paragraph exceeding length threshold.
        
        Given text with multiple paragraphs, extract first one >= 100 chars.
        """
        text = """Short intro.

This is the first substantial paragraph that contains enough text to exceed 
the one hundred character threshold requirement. It should be extracted as 
the primary content because it meets all criteria.

This is a second paragraph that also has substantial content but should 
not be returned since we only want the first one."""

        result = _extract_first_substantial_paragraph(text, min_length=100, max_length=500)
        
        assert result is not None, "Should return a paragraph"
        assert len(result) >= 100, "Result should meet minimum length"
        assert "first substantial paragraph" in result, "Should contain first paragraph text"
        assert "second paragraph" not in result, "Should not contain second paragraph"
    
    def test_truncates_to_max_length(self):
        """
        RED: Test that long paragraphs are truncated to max_length with ellipsis.
        
        Paragraph exceeding max_length should be truncated at last sentence 
        boundary before max_length and add "..." ellipsis.
        """
        # Create a 300-character paragraph
        long_text = (
            "This is a very long paragraph that will definitely exceed the maximum "
            "length threshold that we specify. " * 5  # Repeat to make it long
        )
        
        result = _extract_first_substantial_paragraph(long_text, min_length=100, max_length=200)
        
        assert result is not None, "Should return truncated text"
        assert len(result) <= 203, "Should respect max_length (+3 for ellipsis)"
        assert result.endswith("..."), "Should append ellipsis"
        assert "This is a very long paragraph" in result, "Should contain beginning"
    
    def test_no_truncation_ellipsis_when_under_limit(self):
        """
        RED: Test that ellipsis not added when content under max_length.
        
        If paragraph is between min_length and max_length, return as-is 
        without truncation or ellipsis.
        """
        text = "This paragraph has exactly one hundred and twenty characters to test the case where no truncation needed at all."
        
        result = _extract_first_substantial_paragraph(text, min_length=100, max_length=500)
        
        assert result == text, "Should return text unmodified"
        assert not result.endswith("..."), "Should NOT append ellipsis"
    
    def test_skips_short_paragraphs(self):
        """
        RED: Test that paragraphs under min_length are skipped.
        
        First few paragraphs are too short, should skip to first one 
        that meets min_length threshold.
        """
        text = """Short.

Also short.

This third paragraph is finally long enough to meet the one hundred character 
minimum threshold requirement so it should be the one that gets extracted and returned."""

        result = _extract_first_substantial_paragraph(text, min_length=100, max_length=500)
        
        assert result is not None, "Should find third paragraph"
        assert "third paragraph" in result, "Should extract third paragraph"
        assert "Short" not in result, "Should skip first short paragraph"
        assert "Also short" not in result, "Should skip second short paragraph"
    
    def test_handles_no_paragraph_breaks(self):
        """
        RED: Test handling of content without paragraph breaks (single block).
        
        If text has no empty lines (paragraph separators), treat entire 
        text as single paragraph.
        """
        text = "This is continuous text without any paragraph breaks but it is long enough to meet the one hundred character threshold so it should be extracted successfully."
        
        result = _extract_first_substantial_paragraph(text, min_length=100, max_length=500)
        
        assert result == text, "Should return entire text as single paragraph"
    
    def test_returns_none_when_no_paragraph_meets_threshold(self):
        """
        RED: Test that None returned when all paragraphs are too short.
        
        If no paragraph meets min_length, return None instead of empty string.
        """
        text = """First short.

Second short.

Third short."""

        result = _extract_first_substantial_paragraph(text, min_length=100, max_length=500)
        
        assert result is None, "Should return None when no paragraph meets threshold"
    
    def test_handles_empty_text(self):
        """
        RED: Test handling of empty or whitespace-only text.
        
        Edge case: empty string or only whitespace should return None.
        """
        assert _extract_first_substantial_paragraph("", min_length=100, max_length=500) is None
        assert _extract_first_substantial_paragraph("   \n\n  ", min_length=100, max_length=500) is None
    
    def test_truncation_at_sentence_boundary(self):
        """
        RED: Test that truncation attempts to break at sentence boundary.
        
        When truncating, should try to end at last complete sentence 
        before max_length rather than cutting mid-sentence.
        """
        text = (
            "First sentence is here. Second sentence adds more content and makes it longer. "
            "Third sentence goes way over the limit and should not appear in truncated output. "
            "Fourth sentence also excluded."
        )
        
        result = _extract_first_substantial_paragraph(text, min_length=100, max_length=120)
        
        assert result is not None, "Should return truncated text"
        assert result.endswith("..."), "Should have ellipsis"
        # Should include first sentence, maybe part of second, but not third
        assert "First sentence" in result
        assert "Fourth sentence" not in result
    
    def test_default_parameters(self):
        """
        RED: Test function works with default parameters.
        
        Function should have sensible defaults: min_length=100, max_length=500.
        """
        text = "This paragraph meets the default minimum threshold of one hundred characters and should be extracted successfully with defaults."
        
        # Call without specifying parameters (should use defaults)
        result = _extract_first_substantial_paragraph(text)
        
        assert result == text, "Should work with default parameters"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
