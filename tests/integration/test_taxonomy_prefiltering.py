"""
Tests for book taxonomy pre-filtering.

This test suite covers Sprint 1 section 1.2 per REFACTORING_PLAN.md:
- _prefilter_books_by_taxonomy() - Pre-filter books by domain/concepts
- _extract_concepts_from_text() - Extract key concepts from chapter text

Following TDD: Tests written BEFORE implementation.

Expected token savings: 40% by reducing book metadata sent to LLM
"""

import pytest
from unittest.mock import Mock, patch

# Note: Import will fail until we implement the functions
# This is expected in TDD - write tests first, then make them pass
try:
    from workflows.w07_llm_enhancement.scripts.interactive_llm_system_v3_hybrid_prompt import (
        _extract_concepts_from_text,
        _prefilter_books_by_taxonomy
    )
except (ImportError, AttributeError):
    # Allow tests to load even if functions don't exist yet
    _extract_concepts_from_text = None
    _prefilter_books_by_taxonomy = None


class TestExtractConceptsFromText:
    """
    Tests for _extract_concepts_from_text() function.
    
    Per REFACTORING_PLAN.md section 1.2:
    - Extracts key programming concepts from text
    - Identifies design patterns mentioned
    - Captures Python-specific terms (decorators, generators, etc.)
    - Extracts capitalized terms (proper nouns/concepts)
    """
    
    @pytest.mark.skipif(_extract_concepts_from_text is None, reason="Function not implemented yet")
    def test_extract_python_concepts(self):
        """Test extraction of Python-specific concepts."""
        text = """
        This chapter covers decorators and generators in Python.
        We'll explore how to use context managers effectively.
        """
        
        concepts = _extract_concepts_from_text(text)
        
        assert "decorator" in concepts or "decorators" in concepts
        assert "generator" in concepts or "generators" in concepts
        assert "context manager" in concepts or "context managers" in concepts
    
    @pytest.mark.skipif(_extract_concepts_from_text is None, reason="Function not implemented yet")
    def test_extract_design_patterns(self):
        """Test extraction of design pattern names."""
        text = """
        This section demonstrates the Factory Pattern and Singleton Pattern.
        We'll also discuss the Observer pattern for event handling.
        """
        
        concepts = _extract_concepts_from_text(text)
        
        # Should extract pattern names
        pattern_found = any(p in concepts for p in ["factory", "singleton", "observer", "Factory", "Singleton", "Observer"])
        assert pattern_found, f"No patterns found in: {concepts}"
    
    @pytest.mark.skipif(_extract_concepts_from_text is None, reason="Function not implemented yet")
    def test_extract_architecture_terms(self):
        """Test extraction of architecture-related terms."""
        text = """
        Microservices architecture relies on DDD (Domain-Driven Design).
        We use the Repository pattern for data access.
        """
        
        concepts = _extract_concepts_from_text(text)
        
        # Should find architecture terms
        arch_found = any(term in concepts for term in ["microservice", "ddd", "repository", "architecture"])
        assert arch_found, f"No architecture terms found in: {concepts}"
    
    @pytest.mark.skipif(_extract_concepts_from_text is None, reason="Function not implemented yet")
    def test_extract_capitalized_terms(self):
        """Test extraction of capitalized terms (proper nouns)."""
        text = """
        Django and Flask are popular Python frameworks.
        FastAPI is gaining popularity for building APIs.
        """
        
        concepts = _extract_concepts_from_text(text)
        
        # Should extract capitalized framework names
        assert any(term in concepts for term in ["Django", "Flask", "FastAPI"])
    
    @pytest.mark.skipif(_extract_concepts_from_text is None, reason="Function not implemented yet")
    def test_empty_text(self):
        """Test handling of empty text."""
        concepts = _extract_concepts_from_text("")
        
        assert isinstance(concepts, list)
        assert len(concepts) == 0
    
    @pytest.mark.skipif(_extract_concepts_from_text is None, reason="Function not implemented yet")
    def test_limits_capitalized_terms(self):
        """Test that capitalized terms are limited to avoid noise."""
        # Create text with many capitalized terms
        text = " ".join([f"Term{i}" for i in range(100)])
        
        concepts = _extract_concepts_from_text(text)
        
        # Should limit capitalized terms (plan says max 10)
        capitalized_count = sum(1 for c in concepts if c[0].isupper())
        assert capitalized_count <= 15, f"Too many capitalized terms: {capitalized_count}"


class TestPrefilterBooksByTaxonomy:
    """
    Tests for _prefilter_books_by_taxonomy() function.
    
    Per REFACTORING_PLAN.md section 1.2:
    - Pre-filters books by matching domain and concepts
    - Uses book_taxonomy.py scoring
    - Reduces token usage by 40%
    - Returns top N most relevant books
    """
    
    @pytest.fixture
    def mock_orchestrator(self):
        """Create a mock orchestrator with book metadata."""
        orchestrator = Mock()
        orchestrator.metadata_service = Mock()
        
        # Mock book metadata
        orchestrator.metadata_service.books_metadata = {
            "fluent_python_2nd": {
                "title": "Fluent Python 2nd",
                "domain": "python_language",
                "concepts_covered": {"decorator", "generator", "context manager", "metaclass"}
            },
            "python_cookbook_3rd": {
                "title": "Python Cookbook 3rd",
                "domain": "python_language",
                "concepts_covered": {"data structure", "algorithm", "decorator", "testing"}
            },
            "microservices_up_and_running": {
                "title": "Microservices Up and Running",
                "domain": "architecture",
                "concepts_covered": {"microservice", "docker", "kubernetes", "api"}
            },
            "building_microservices": {
                "title": "Building Microservices",
                "domain": "architecture",
                "concepts_covered": {"microservice", "ddd", "event driven", "api gateway"}
            },
            "python_distilled": {
                "title": "Python Distilled",
                "domain": "python_language",
                "concepts_covered": {"function", "class", "module", "package"}
            }
        }
        
        return orchestrator
    
    @pytest.mark.skipif(_prefilter_books_by_taxonomy is None, reason="Function not implemented yet")
    def test_filters_by_python_concepts(self, mock_orchestrator):
        """Test filtering for Python-specific concepts."""
        guideline_text = """
        This chapter covers decorators and context managers in Python.
        We'll learn how to create custom decorators.
        """
        
        # Call the method on orchestrator (it's an instance method)
        books = _prefilter_books_by_taxonomy(
            mock_orchestrator,
            guideline_text=guideline_text,
            max_books=3
        )
        
        # Should prefer books with matching concepts
        assert "Fluent Python 2nd" in books
        assert len(books) <= 3
    
    @pytest.mark.skipif(_prefilter_books_by_taxonomy is None, reason="Function not implemented yet")
    def test_filters_by_architecture_domain(self, mock_orchestrator):
        """Test filtering for architecture-related content."""
        guideline_text = """
        This chapter discusses microservices architecture.
        We'll explore API gateways and event-driven design.
        """
        
        books = _prefilter_books_by_taxonomy(
            mock_orchestrator,
            guideline_text=guideline_text,
            max_books=3
        )
        
        # Should prefer architecture books
        assert "Microservices Up and Running" in books or "Building Microservices" in books
        assert len(books) <= 3
    
    @pytest.mark.skipif(_prefilter_books_by_taxonomy is None, reason="Function not implemented yet")
    def test_respects_max_books_limit(self, mock_orchestrator):
        """Test that max_books limit is enforced."""
        guideline_text = "Python programming concepts"
        
        books = _prefilter_books_by_taxonomy(
            mock_orchestrator,
            guideline_text=guideline_text,
            max_books=2
        )
        
        assert len(books) <= 2
    
    @pytest.mark.skipif(_prefilter_books_by_taxonomy is None, reason="Function not implemented yet")
    def test_returns_list_of_titles(self, mock_orchestrator):
        """Test that function returns list of book titles (strings)."""
        guideline_text = "Python decorators"
        
        books = _prefilter_books_by_taxonomy(
            mock_orchestrator,
            guideline_text=guideline_text,
            max_books=5
        )
        
        assert isinstance(books, list)
        assert all(isinstance(book, str) for book in books)
    
    @pytest.mark.skipif(_prefilter_books_by_taxonomy is None, reason="Function not implemented yet")
    def test_empty_guideline_returns_all_books(self, mock_orchestrator):
        """Test that empty guideline text returns top-ranked books."""
        books = _prefilter_books_by_taxonomy(
            mock_orchestrator,
            guideline_text="",
            max_books=3
        )
        
        # Should still return books (fall back to ranking)
        assert isinstance(books, list)
        assert len(books) > 0
    
    @pytest.mark.skipif(_prefilter_books_by_taxonomy is None, reason="Function not implemented yet")
    def test_uses_book_taxonomy_scoring(self, mock_orchestrator):
        """Test that function uses book_taxonomy.py for scoring."""
        guideline_text = "Python decorators and generators"
        
        with patch('src.book_taxonomy.score_books_for_concepts') as mock_score:
            # Mock scoring function to return scored books
            mock_score.return_value = [
                ("Fluent Python 2nd", 0.9),
                ("Python Cookbook 3rd", 0.7),
                ("Python Distilled", 0.5)
            ]
            
            books = _prefilter_books_by_taxonomy(
                mock_orchestrator,
                guideline_text=guideline_text,
                max_books=3
            )
            
            # Should have called scoring function with concepts  
            assert mock_score.called
            assert len(books) <= 3


class TestTaxonomyIntegration:
    """
    Integration tests for taxonomy pre-filtering in the LLM workflow.
    
    Tests that pre-filtering actually reduces token usage and improves results.
    """
    
    @pytest.mark.skipif(_prefilter_books_by_taxonomy is None, reason="Function not implemented yet")
    def test_reduces_book_metadata_size(self):
        """Test that pre-filtering reduces the number of books sent to LLM."""
        # This would be tested with actual metadata size calculation
        # Expect ~40% reduction per REFACTORING_PLAN.md
        pass  # Implementation will be added in integration testing
    
    @pytest.mark.skipif(_prefilter_books_by_taxonomy is None, reason="Function not implemented yet")
    def test_maintains_relevance(self):
        """Test that pre-filtered books are still relevant to the chapter."""
        # This would be tested with actual LLM responses
        # Filtered books should still cover the chapter's concepts
        pass  # Implementation will be added in integration testing


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
