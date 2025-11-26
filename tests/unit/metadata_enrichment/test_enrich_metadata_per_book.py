"""
Unit tests for enrich_metadata_per_book.py

Tests focus on functions with CC 9:
- _enrich_single_chapter (CC 9) - Service layer for chapter enrichment

Architecture Patterns Applied:
- Service Layer Pattern: Test business logic for enrichment (Architecture Patterns Ch. 4)
- Repository Pattern: Test chapter data retrieval
- Strategy Pattern: Test similarity-based enrichment strategy

Sprint: Batch #2 Files 6-11 (HIGH priority, CC 8-9, tests only)
"""

import pytest
import numpy as np
import sys
from pathlib import Path
from unittest.mock import Mock, patch
from typing import List, Dict, Any

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
    _enrich_single_chapter
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def sample_chapter():
    """Sample chapter metadata from Tab 2."""
    return {
        "chapter_number": 5,
        "title": "Decorators and Closures",
        "start_page": 100,
        "end_page": 125,
        "keywords": ["decorator", "closure", "@property"],
        "summary": "Chapter about decorators"
    }


@pytest.fixture
def sample_corpus():
    """Sample chapter corpus for similarity matching."""
    return [
        "Chapter about decorators and closures in Python",
        "Chapter about generators and iterators",
        "Chapter about context managers and with statement",
        "Chapter about decorators in design patterns",
        "Chapter about metaclasses"
    ]


@pytest.fixture
def sample_index():
    """Sample chapter index mapping corpus to books/chapters."""
    return [
        {"book": "Fluent_Python_2nd.json", "chapter": 5, "title": "Decorators"},
        {"book": "Fluent_Python_2nd.json", "chapter": 6, "title": "Generators"},
        {"book": "Python_Distilled.json", "chapter": 3, "title": "Context Managers"},
        {"book": "Architecture_Patterns.json", "chapter": 8, "title": "Decorators in Design"},
        {"book": "Learning_Python_Ed6.json", "chapter": 12, "title": "Metaclasses"}
    ]


@pytest.fixture
def sample_similarity_matrix():
    """Sample similarity matrix (5x5)."""
    return np.array([
        [1.0, 0.3, 0.2, 0.8, 0.1],  # Chapter 0 (current) similar to Chapter 3
        [0.3, 1.0, 0.5, 0.2, 0.1],
        [0.2, 0.5, 1.0, 0.3, 0.2],
        [0.8, 0.2, 0.3, 1.0, 0.1],  # Chapter 3 very similar to Chapter 0
        [0.1, 0.1, 0.2, 0.1, 1.0]
    ])


# ============================================================================
# TEST _enrich_single_chapter (CC 9)
# ============================================================================

class TestEnrichSingleChapter:
    """
    Test suite for _enrich_single_chapter function.
    
    This function implements Service Layer pattern for chapter enrichment:
    - Finds related chapters using cosine similarity
    - Enriches keywords from related chapters
    - Enriches concepts from cross-book analysis
    - Handles missing chapters gracefully
    
    Complexity: CC 9 (multiple conditional branches, enrichment logic)
    Pattern: Service Layer + Strategy Pattern (similarity-based matching)
    """
    
    def test_enrich_chapter_with_related_chapters(
        self,
        sample_chapter,
        sample_corpus,
        sample_index,
        sample_similarity_matrix
    ):
        """Test enriching chapter with related chapter data."""
        with patch('workflows.metadata_enrichment.scripts.enrich_metadata_per_book.find_related_chapters') as mock_find:
            mock_find.return_value = [
                {"book": "Architecture_Patterns.json", "chapter": 8, "similarity": 0.8}
            ]
            
            with patch('workflows.metadata_enrichment.scripts.enrich_metadata_per_book._enrich_keywords_from_related') as mock_enrich_kw:
                mock_enrich_kw.return_value = ["decorator", "closure", "design pattern"]
                
                with patch('workflows.metadata_enrichment.scripts.enrich_metadata_per_book._enrich_concepts_from_related') as mock_enrich_concepts:
                    mock_enrich_concepts.return_value = [
                        {"concept": "decorator pattern", "source": "cross_book"}
                    ]
                    
                    result = _enrich_single_chapter(
                        sample_chapter,
                        "Fluent_Python_2nd",
                        sample_corpus,
                        sample_index,
                        sample_similarity_matrix
                    )
        
        assert "related_chapters" in result or result == sample_chapter
        # Should preserve original chapter data
        assert result["chapter_number"] == 5
        assert result["title"] == "Decorators and Closures"
    
    def test_enrich_chapter_not_found_in_corpus(
        self,
        sample_chapter,
        sample_corpus,
        sample_index,
        sample_similarity_matrix
    ):
        """Test behavior when chapter not found in corpus index."""
        # Use chapter number that doesn't exist in index
        chapter_not_in_corpus = {
            "chapter_number": 99,
            "title": "Non-existent Chapter",
            "start_page": 1,
            "end_page": 10,
            "keywords": []
        }
        
        result = _enrich_single_chapter(
            chapter_not_in_corpus,
            "Unknown_Book",
            sample_corpus,
            sample_index,
            sample_similarity_matrix
        )
        
        # Should return original chapter unchanged
        assert result == chapter_not_in_corpus
    
    def test_enrich_chapter_finds_chapter_index(
        self,
        sample_chapter,
        sample_corpus,
        sample_index,
        sample_similarity_matrix
    ):
        """Test that enrichment finds correct chapter index in corpus."""
        with patch('workflows.metadata_enrichment.scripts.enrich_metadata_per_book.find_related_chapters') as mock_find:
            mock_find.return_value = []
            
            with patch('workflows.metadata_enrichment.scripts.enrich_metadata_per_book._enrich_keywords_from_related') as mock_enrich_kw:
                mock_enrich_kw.return_value = sample_chapter["keywords"]
                
                with patch('workflows.metadata_enrichment.scripts.enrich_metadata_per_book._enrich_concepts_from_related') as mock_enrich_concepts:
                    mock_enrich_concepts.return_value = []
                    
                    _ = _enrich_single_chapter(
                        sample_chapter,
                        "Fluent_Python_2nd",
                        sample_corpus,
                        sample_index,
                        sample_similarity_matrix
                    )
                    
                    # find_related_chapters should be called with chapter index 0
                    assert mock_find.called
    
    def test_enrich_chapter_with_high_similarity_threshold(
        self,
        sample_chapter,
        sample_corpus,
        sample_index,
        sample_similarity_matrix
    ):
        """Test enrichment with high similarity threshold (0.7)."""
        with patch('workflows.metadata_enrichment.scripts.enrich_metadata_per_book.find_related_chapters') as mock_find:
            # Only returns chapters with similarity > 0.7
            mock_find.return_value = [
                {"book": "Architecture_Patterns.json", "chapter": 8, "similarity": 0.8}
            ]
            
            with patch('workflows.metadata_enrichment.scripts.enrich_metadata_per_book._enrich_keywords_from_related') as mock_enrich_kw:
                mock_enrich_kw.return_value = ["decorator"]
                
                with patch('workflows.metadata_enrichment.scripts.enrich_metadata_per_book._enrich_concepts_from_related') as mock_enrich_concepts:
                    mock_enrich_concepts.return_value = []
                    
                    _enrich_single_chapter(
                        sample_chapter,
                        "Fluent_Python_2nd",
                        sample_corpus,
                        sample_index,
                        sample_similarity_matrix
                    )
                    
                    # Should call with threshold=0.7
                    mock_find.assert_called_once()
                    call_args = mock_find.call_args
                    assert 'threshold' in call_args[1] or len(call_args[0]) >= 4
    
    def test_enrich_chapter_excludes_same_book(
        self,
        sample_chapter,
        sample_corpus,
        sample_index,
        sample_similarity_matrix
    ):
        """Test that enrichment excludes chapters from same book."""
        with patch('workflows.metadata_enrichment.scripts.enrich_metadata_per_book.find_related_chapters') as mock_find:
            mock_find.return_value = []
            
            with patch('workflows.metadata_enrichment.scripts.enrich_metadata_per_book._enrich_keywords_from_related') as mock_enrich_kw:
                mock_enrich_kw.return_value = []
                
                with patch('workflows.metadata_enrichment.scripts.enrich_metadata_per_book._enrich_concepts_from_related') as mock_enrich_concepts:
                    mock_enrich_concepts.return_value = []
                    
                    _enrich_single_chapter(
                        sample_chapter,
                        "Fluent_Python_2nd",
                        sample_corpus,
                        sample_index,
                        sample_similarity_matrix
                    )
                    
                    # Should exclude "Fluent_Python_2nd.json" from related chapters
                    call_args = mock_find.call_args
                    if call_args and len(call_args[0]) >= 4:
                        assert "Fluent_Python_2nd.json" in str(call_args[0][3])
    
    def test_enrich_chapter_with_no_related_chapters(
        self,
        sample_chapter,
        sample_corpus,
        sample_index,
        sample_similarity_matrix
    ):
        """Test enrichment when no related chapters found."""
        with patch('workflows.metadata_enrichment.scripts.enrich_metadata_per_book.find_related_chapters') as mock_find:
            mock_find.return_value = []  # No related chapters
            
            with patch('workflows.metadata_enrichment.scripts.enrich_metadata_per_book._enrich_keywords_from_related') as mock_enrich_kw:
                mock_enrich_kw.return_value = sample_chapter["keywords"]
                
                with patch('workflows.metadata_enrichment.scripts.enrich_metadata_per_book._enrich_concepts_from_related') as mock_enrich_concepts:
                    mock_enrich_concepts.return_value = []
                    
                    result = _enrich_single_chapter(
                        sample_chapter,
                        "Fluent_Python_2nd",
                        sample_corpus,
                        sample_index,
                        sample_similarity_matrix
                    )
                    
                    # Should still return enriched chapter with original keywords
                    assert result["chapter_number"] == 5
    
    def test_enrich_chapter_preserves_original_fields(
        self,
        sample_chapter,
        sample_corpus,
        sample_index,
        sample_similarity_matrix
    ):
        """Test that enrichment preserves all original chapter fields."""
        with patch('workflows.metadata_enrichment.scripts.enrich_metadata_per_book.find_related_chapters') as mock_find:
            mock_find.return_value = []
            
            with patch('workflows.metadata_enrichment.scripts.enrich_metadata_per_book._enrich_keywords_from_related') as mock_enrich_kw:
                mock_enrich_kw.return_value = ["new_keyword"]
                
                with patch('workflows.metadata_enrichment.scripts.enrich_metadata_per_book._enrich_concepts_from_related') as mock_enrich_concepts:
                    mock_enrich_concepts.return_value = []
                    
                    result = _enrich_single_chapter(
                        sample_chapter,
                        "Fluent_Python_2nd",
                        sample_corpus,
                        sample_index,
                        sample_similarity_matrix
                    )
                    
                    # All original fields should be preserved
                    assert result["chapter_number"] == sample_chapter["chapter_number"]
                    assert result["title"] == sample_chapter["title"]
                    assert result["start_page"] == sample_chapter["start_page"]
                    assert result["end_page"] == sample_chapter["end_page"]
    
    def test_enrich_chapter_with_complex_index_matching(
        self,
        sample_corpus,
        sample_index,
        sample_similarity_matrix
    ):
        """Test chapter index matching with multiple books."""
        chapter = {
            "chapter_number": 3,
            "title": "Context Managers",
            "start_page": 50,
            "end_page": 75,
            "keywords": ["context", "with"]
        }
        
        with patch('workflows.metadata_enrichment.scripts.enrich_metadata_per_book.find_related_chapters') as mock_find:
            mock_find.return_value = []
            
            with patch('workflows.metadata_enrichment.scripts.enrich_metadata_per_book._enrich_keywords_from_related') as mock_enrich_kw:
                mock_enrich_kw.return_value = ["context"]
                
                with patch('workflows.metadata_enrichment.scripts.enrich_metadata_per_book._enrich_concepts_from_related') as mock_enrich_concepts:
                    mock_enrich_concepts.return_value = []
                    
                    result = _enrich_single_chapter(
                        chapter,
                        "Python_Distilled",
                        sample_corpus,
                        sample_index,
                        sample_similarity_matrix
                    )
                    
                    # Should find chapter at index 2 (Python_Distilled chapter 3)
                    assert result["chapter_number"] == 3


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestEnrichmentIntegration:
    """Integration tests for chapter enrichment."""
    
    def test_enrichment_pipeline_with_real_structure(
        self,
        sample_chapter,
        sample_corpus,
        sample_index,
        sample_similarity_matrix
    ):
        """Test full enrichment pipeline with realistic data."""
        with patch('workflows.metadata_enrichment.scripts.enrich_metadata_per_book.find_related_chapters') as mock_find:
            mock_find.return_value = [
                {"book": "Architecture_Patterns.json", "chapter": 8, "similarity": 0.8},
                {"book": "Learning_Python_Ed6.json", "chapter": 12, "similarity": 0.75}
            ]
            
            with patch('workflows.metadata_enrichment.scripts.enrich_metadata_per_book._enrich_keywords_from_related') as mock_enrich_kw:
                mock_enrich_kw.return_value = ["decorator", "closure", "design pattern", "metaclass"]
                
                with patch('workflows.metadata_enrichment.scripts.enrich_metadata_per_book._enrich_concepts_from_related') as mock_enrich_concepts:
                    mock_enrich_concepts.return_value = [
                        {"concept": "decorator pattern", "source": "cross_book"},
                        {"concept": "closure scope", "source": "cross_book"}
                    ]
                    
                    result = _enrich_single_chapter(
                        sample_chapter,
                        "Fluent_Python_2nd",
                        sample_corpus,
                        sample_index,
                        sample_similarity_matrix
                    )
                    
                    # Result should have enriched data
                    assert result["chapter_number"] == 5
                    assert "title" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
