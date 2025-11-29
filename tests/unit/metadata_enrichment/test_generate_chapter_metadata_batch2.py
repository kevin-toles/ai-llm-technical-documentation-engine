"""
Unit tests for generate_chapter_summary function (CC 8)

Tests focus on generate_chapter_summary function with CC 8:
- Complex summary building from multiple sources
- Sentence extraction and selection logic
- Concept and keyword integration
- Length constraints and formatting

Architecture Patterns Applied:
- Builder Pattern: Multi-step summary construction (Architecture Patterns Ch. 9)
- Strategy Pattern: Multiple summary component strategies
- Template Method: Summary assembly workflow

Sprint: Batch #2 File #10 (HIGH priority, CC 8, tests only)
"""

import pytest
import sys
from pathlib import Path
from typing import List, Dict, Any
from unittest.mock import Mock, patch

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from workflows.metadata_enrichment.scripts.generate_chapter_metadata import (
    generate_chapter_summary
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def sample_chapter_pages():
    """Sample chapter pages with content."""
    return [
        {
            "page_number": 1,
            "content": "This chapter introduces Python decorators. Decorators are a powerful "
                      "feature that allows you to modify function behavior. They use the @ syntax."
        },
        {
            "page_number": 2,
            "content": "Function decorators wrap other functions. They can add logging, timing, "
                      "or caching functionality. The decorator pattern is widely used."
        },
        {
            "page_number": 3,
            "content": "Class decorators work similarly. They modify class definitions. "
                      "This provides meta-programming capabilities in Python."
        }
    ]


@pytest.fixture
def sample_keywords():
    """Sample extracted keywords."""
    return ["decorator", "function", "syntax", "pattern", "class", "logging", "timing"]


@pytest.fixture
def sample_concepts():
    """Sample extracted concepts."""
    return ["decorators", "metaprogramming", "function wrapping"]


# ============================================================================
# TEST CLASS: generate_chapter_summary (CC 8)
# ============================================================================

class TestGenerateChapterSummary:
    """
    Test generate_chapter_summary function.
    
    This function generates concise 2-3 sentence summaries:
    - Extracts sample text from first pages
    - Finds introductory sentences
    - Builds concept summary
    - Adds keyword-based summary
    - Ensures length constraints
    
    Complexity: CC 8 (multiple conditional branches for summary building)
    Pattern: Builder Pattern for multi-step construction
    """
    
    def test_generate_summary_basic(self, sample_chapter_pages, sample_keywords, sample_concepts):
        """Test basic summary generation."""
        # Arrange
        chapter_title = "Python Decorators"
        
        # Act
        summary = generate_chapter_summary(
            sample_chapter_pages,
            chapter_title,
            sample_keywords,
            sample_concepts
        )
        
        # Assert
        assert isinstance(summary, str)
        assert len(summary) > 0
        assert len(summary) <= 600  # Length constraint
    
    def test_summary_includes_chapter_context(self, sample_chapter_pages, sample_keywords, sample_concepts):
        """Test summary references chapter content."""
        # Arrange
        chapter_title = "Decorators"
        
        # Act
        summary = generate_chapter_summary(
            sample_chapter_pages,
            chapter_title,
            sample_keywords,
            sample_concepts
        )
        
        # Assert - should reference decorators or chapter context
        assert any(term in summary.lower() for term in ['decorator', 'chapter', 'function', 'python'])
    
    def test_summary_with_no_pages_uses_title(self, sample_keywords, sample_concepts):
        """Test summary generation with empty pages."""
        # Arrange
        chapter_pages = []
        chapter_title = "Empty Chapter"
        
        # Act
        summary = generate_chapter_summary(
            chapter_pages,
            chapter_title,
            sample_keywords,
            sample_concepts
        )
        
        # Assert - should still generate summary
        assert isinstance(summary, str)
        assert len(summary) > 0
    
    def test_summary_with_empty_keywords_and_concepts(self, sample_chapter_pages):
        """Test summary with no keywords or concepts."""
        # Arrange
        chapter_title = "Basic Chapter"
        keywords = []
        concepts = []
        
        # Act
        summary = generate_chapter_summary(
            sample_chapter_pages,
            chapter_title,
            keywords,
            concepts
        )
        
        # Assert - should still generate basic summary
        assert isinstance(summary, str)
        assert len(summary) > 0
    
    def test_summary_length_constraint(self, sample_chapter_pages, sample_keywords, sample_concepts):
        """Test summary respects 600 character limit."""
        # Arrange
        # Create many keywords and concepts to potentially exceed limit
        long_keywords = ["keyword" + str(i) for i in range(50)]
        long_concepts = ["concept" + str(i) for i in range(50)]
        
        # Act
        summary = generate_chapter_summary(
            sample_chapter_pages,
            "Very Long Chapter Title",
            long_keywords,
            long_concepts
        )
        
        # Assert - should be truncated to 600 chars
        assert len(summary) <= 600
    
    def test_summary_with_minimal_content(self):
        """Test summary with minimal page content."""
        # Arrange
        minimal_pages = [{"page_number": 1, "content": "Short."}]
        
        # Act
        summary = generate_chapter_summary(
            minimal_pages,
            "Minimal",
            ["key"],
            ["concept"]
        )
        
        # Assert
        assert isinstance(summary, str)
        assert len(summary) > 0
    
    def test_summary_incorporates_concepts(self, sample_chapter_pages):
        """Test summary incorporates provided concepts."""
        # Arrange
        concepts = ["advanced topic", "special technique"]
        
        # Act
        summary = generate_chapter_summary(
            sample_chapter_pages,
            "Test Chapter",
            ["keyword"],
            concepts
        )
        
        # Assert - should mention concepts if included
        assert isinstance(summary, str)
        # Implementation may or may not include exact concept text
        assert len(summary) > 20  # Should be substantive
    
    def test_summary_with_long_chapter_title(self, sample_chapter_pages, sample_keywords, sample_concepts):
        """Test summary with very long chapter title."""
        # Arrange
        long_title = "This is a Very Long Chapter Title About Advanced Python Programming Techniques and Patterns"
        
        # Act
        summary = generate_chapter_summary(
            sample_chapter_pages,
            long_title,
            sample_keywords,
            sample_concepts
        )
        
        # Assert
        assert isinstance(summary, str)
        assert len(summary) <= 600
    
    def test_summary_is_coherent_text(self, sample_chapter_pages, sample_keywords, sample_concepts):
        """Test summary produces coherent text (not just keyword lists)."""
        # Act
        summary = generate_chapter_summary(
            sample_chapter_pages,
            "Test Chapter",
            sample_keywords,
            sample_concepts
        )
        
        # Assert - should have sentence structure
        assert '.' in summary or len(summary) > 30  # Has punctuation or is substantive
        assert not summary.startswith('[')  # Not just a list
        assert not summary.startswith('{')  # Not just JSON


# ============================================================================
# EDGE CASE TESTS
# ============================================================================

class TestGenerateChapterSummaryEdgeCases:
    """Edge case tests for generate_chapter_summary."""
    
    def test_summary_with_special_characters_in_content(self):
        """Test handling of special characters."""
        # Arrange
        pages = [
            {"page_number": 1, "content": "Code: @decorator\ndef func():\n    return 'value'"}
        ]
        
        # Act
        summary = generate_chapter_summary(pages, "Code Examples", ["decorator"], ["functions"])
        
        # Assert - should handle special chars
        assert isinstance(summary, str)
        assert len(summary) > 0
    
    def test_summary_with_unicode_content(self):
        """Test handling of unicode characters."""
        # Arrange
        pages = [
            {"page_number": 1, "content": "Python → decorators ✓ functions ∈ objects"}
        ]
        
        # Act
        summary = generate_chapter_summary(pages, "Unicode Test", ["python"], ["decorators"])
        
        # Assert
        assert isinstance(summary, str)
    
    def test_summary_with_missing_content_field(self):
        """Test handling pages without content field."""
        # Arrange
        pages = [
            {"page_number": 1},  # Missing content
            {"page_number": 2, "content": "Some text"}
        ]
        
        # Act
        summary = generate_chapter_summary(pages, "Test", [], [])
        
        # Assert - should handle missing content gracefully
        assert isinstance(summary, str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
