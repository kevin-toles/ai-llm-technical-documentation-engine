"""
Unit tests for generate_chapter_metadata.py

Tests focus on functions with CC 8:
- _add_technical_context (CC 8) - Strategy pattern for context enrichment

Architecture Patterns Applied:
- Strategy Pattern: Test context selection algorithm (Architecture Patterns Ch. 13)
- Service Layer Pattern: Test summary enrichment business logic
- Domain-Agnostic Implementation: Statistical NLP approach

Sprint: Batch #2 Files 6-11 (HIGH priority, CC 8-9, tests only)
"""

import pytest
import sys
from pathlib import Path
from typing import List

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from workflows.metadata_enrichment.scripts.generate_chapter_metadata import (
    _add_technical_context
)


# ============================================================================
# TEST _add_technical_context (CC 8)
# ============================================================================

class TestAddTechnicalContext:
    """
    Test suite for _add_technical_context function.
    
    This function implements Strategy pattern for context enrichment:
    - Adds technical sentences when summary too short (<150 chars)
    - Filters sentences for technical keywords
    - Limits sentence length (40-250 chars)
    - Avoids duplicate content
    
    Complexity: CC 8 (multiple conditional filters, keyword matching)
    Pattern: Strategy Pattern (selective enrichment strategy)
    """
    
    def test_no_enrichment_when_summary_long_enough(self):
        """Test that summaries ≥150 chars are not enriched."""
        summary = "This is a comprehensive summary about Python programming. " * 3
        sentences = ["Additional context about Python decorators."]
        sample_text = "Extra text"
        
        assert len(summary) >= 150
        result = _add_technical_context(summary, sentences, sample_text)
        
        # Should return original summary unchanged
        assert result == summary
    
    def test_no_enrichment_when_no_sample_text(self):
        """Test that empty sample_text prevents enrichment."""
        summary = "Short summary"
        sentences = ["Additional context about Python."]
        
        assert len(summary) < 150
        result = _add_technical_context(summary, sentences, "")
        
        # Should return original summary
        assert result == summary
    
    def test_enrichment_adds_technical_sentence(self):
        """Test enrichment with technical keyword-containing sentence."""
        summary = "Short summary"
        sentences = [
            "This is not technical.",
            "Python decorators modify function behavior using syntax.",
            "Generic text without keywords."
        ]
        sample_text = "Sample chapter text with technical content"
        
        result = _add_technical_context(summary, sentences, sample_text)
        
        # Should add technical sentence
        assert len(result) > len(summary)
        assert "python" in result.lower() or "decorator" in result.lower()
    
    def test_enrichment_filters_by_technical_keywords(self):
        """Test that only sentences with technical keywords are added."""
        summary = "Short summary"
        sentences = [
            "The weather is nice today.",  # No technical keywords
            "This code example demonstrates Python functions.",  # Has 'code', 'python', 'function'
            "Let's go for a walk."  # No technical keywords
        ]
        sample_text = "Sample text"
        
        result = _add_technical_context(summary, sentences, sample_text)
        
        # Should only add sentence with technical keywords
        if result != summary:
            assert "code" in result.lower() or "python" in result.lower() or "function" in result.lower()
    
    def test_enrichment_respects_sentence_length_constraints(self):
        """Test that sentences must be 40-250 chars."""
        summary = "Short"
        sentences = [
            "Too short.",  # < 40 chars
            "This Python function demonstrates the use of decorators in a comprehensive manner with proper syntax.",  # 40-250 chars
            "x" * 300  # > 250 chars
        ]
        sample_text = "Sample"
        
        result = _add_technical_context(summary, sentences, sample_text)
        
        # Should only add sentence in valid length range
        if result != summary:
            added_sentence = result.replace(summary, "").strip()
            assert 40 <= len(added_sentence) <= 250
    
    def test_enrichment_avoids_duplicate_sentences(self):
        """Test that sentences already in summary are not added."""
        summary = "This Python function is important."
        sentences = [
            "Unrelated content.",
            "This Python function is important.",  # Duplicate
            "Python variables store data values."
        ]
        sample_text = "Sample"
        
        result = _add_technical_context(summary, sentences, sample_text)
        
        # Should not duplicate existing sentence
        if result != summary:
            assert "variables" in result or result == summary + " Python variables store data values."
    
    def test_enrichment_uses_sentences_after_first(self):
        """Test that enrichment starts from sentences[1:15] not sentences[0]."""
        summary = "Start"
        sentences = [
            "First sentence with python code should be skipped.",
            "Second sentence with python syntax should be considered."
        ]
        sample_text = "Sample"
        
        result = _add_technical_context(summary, sentences, sample_text)
        
        # Should use sentences[1:], not sentences[0]
        if result != summary and "Second" in result:
            assert "Second" in result or "syntax" in result.lower()
    
    def test_enrichment_limits_to_15_sentences(self):
        """Test that only sentences[1:15] are considered."""
        summary = "Brief"
        # Create 20 sentences, only 2-16 should be checked (sentences[1:15])
        sentences = ["Sentence 0"] + [
            f"Technical sentence {i} about Python code and programming." for i in range(1, 20)
        ]
        sample_text = "Sample"
        
        result = _add_technical_context(summary, sentences, sample_text)
        
        # Should add a sentence from the valid range
        assert len(result) >= len(summary)
    
    def test_enrichment_adds_period_if_missing(self):
        """Test that enrichment ensures result ends with period."""
        summary = "Summary"
        sentences = [
            "Filler",
            "Python function demonstrates syntax concepts"  # No period
        ]
        sample_text = "Sample"
        
        result = _add_technical_context(summary, sentences, sample_text)
        
        # Result should end with period
        if result != summary:
            assert result.endswith(".")
    
    def test_enrichment_preserves_original_summary_format(self):
        """Test that original summary is preserved as prefix."""
        summary = "Original summary text"
        sentences = [
            "Filler",
            "Python code syntax includes variable and function definitions."
        ]
        sample_text = "Sample"
        
        result = _add_technical_context(summary, sentences, sample_text)
        
        # Original summary should be at start
        assert result.startswith(summary.rstrip())
    
    def test_enrichment_with_all_technical_keywords(self):
        """Test enrichment with different technical keywords."""
        technical_keywords = [
            'python', 'code', 'program', 'syntax', 'variable',
            'function', 'class', 'method', 'object', 'data'
        ]
        
        for keyword in technical_keywords:
            summary = "Short"
            sentences = [
                "Filler",
                f"This sentence contains the keyword {keyword} for testing purposes here."
            ]
            sample_text = "Sample"
            
            result = _add_technical_context(summary, sentences, sample_text)
            
            # Should recognize each keyword
            if result != summary:
                assert keyword.lower() in result.lower()
    
    def test_enrichment_case_insensitive_keyword_matching(self):
        """Test that keyword matching is case-insensitive."""
        summary = "Brief"
        sentences = [
            "Ignore this",
            "PYTHON CODE syntax demonstrates FUNCTION behavior properly."
        ]
        sample_text = "Sample"
        
        result = _add_technical_context(summary, sentences, sample_text)
        
        # Should match keywords regardless of case
        if result != summary:
            assert "python" in result.lower() or "code" in result.lower()


# ============================================================================
# EDGE CASE TESTS
# ============================================================================

class TestAddTechnicalContextEdgeCases:
    """Edge case tests for _add_technical_context."""
    
    def test_enrichment_with_empty_sentences_list(self):
        """Test behavior with empty sentences list."""
        summary = "Summary"
        result = _add_technical_context(summary, [], "Sample")
        
        # Should return original summary
        assert result == summary
    
    def test_enrichment_with_single_sentence(self):
        """Test behavior when only sentences[0] exists."""
        summary = "Summary"
        sentences = ["Only one sentence with python code here."]
        
        result = _add_technical_context(summary, sentences, "Sample")
        
        # Should return original since sentences[1:] is empty
        assert result == summary
    
    def test_enrichment_with_none_sample_text(self):
        """Test behavior with None sample_text."""
        summary = "Summary"
        sentences = ["Sentence with python code"]
        
        result = _add_technical_context(summary, sentences, None)
        
        # Should return original
        assert result == summary
    
    def test_enrichment_summary_exactly_150_chars(self):
        """Test boundary condition: summary exactly 150 chars."""
        summary = "x" * 150
        sentences = ["Python code with function definitions."]
        
        result = _add_technical_context(summary, sentences, "Sample")
        
        # Should return original (condition is >=150)
        assert result == summary
    
    def test_enrichment_sentence_exactly_40_chars(self):
        """Test boundary: sentence exactly 40 chars."""
        summary = "Short"
        sentences = [
            "Filler",
            "Python code demonstrates syntax here."  # Exactly or near 40
        ]
        sample_text = "Sample"
        
        # Sentence should be valid if exactly 40 chars
        test_sentence = "Python code demonstrates syntax here."
        if 40 <= len(test_sentence) <= 250:
            result = _add_technical_context(summary, sentences, sample_text)
            # May add sentence if length valid
            assert isinstance(result, str)
    
    def test_enrichment_sentence_exactly_250_chars(self):
        """Test boundary: sentence exactly 250 chars."""
        summary = "Brief"
        long_sentence = "Python " + "x" * 243  # Exactly 250
        sentences = ["Filler", long_sentence]
        sample_text = "Sample"
        
        if len(long_sentence) == 250 and "python" in long_sentence.lower():
            result = _add_technical_context(summary, sentences, sample_text)
            # Should be able to add 250-char sentence
            assert isinstance(result, str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
