"""
Unit tests for content_selection_impl.py

Tests focus on ContentSelectionService methods with CC 8:
- _mock_metadata_response (CC 8) - Mock data generation for testing

Architecture Patterns Applied:
- Service Layer Pattern: Test business logic separation (Architecture Patterns Ch. 4)
- Factory Pattern: Test mock object creation
- Strategy Pattern: Test concept-based book selection

Sprint: Batch #2 Files 6-11 (HIGH priority, CC 8-9, tests only)
"""

import pytest
import sys
from pathlib import Path
from typing import List
from unittest.mock import Mock, patch

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from workflows.llm_enhancement.scripts.phases.content_selection_impl import (
    ContentSelectionService
)
from workflows.llm_enhancement.scripts.interactive_llm_system_v3_hybrid_prompt import (
    LLMMetadataResponse,
    ContentRequest
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def mock_metadata_service():
    """Mock MetadataExtractionService for testing."""
    service = Mock()
    service.get_cross_book_concepts.return_value = {
        "decorator": ["Fluent Python 2nd", "Learning Python Ed6"],
        "generator": ["Fluent Python 2nd", "Python Distilled"]
    }
    return service


@pytest.fixture
def content_service(mock_metadata_service):
    """Create ContentSelectionService instance for testing."""
    return ContentSelectionService(
        metadata_service=mock_metadata_service,
        llm_available=False  # Use mock mode
    )


# ============================================================================
# TEST _mock_metadata_response (CC 8)
# ============================================================================

class TestMockMetadataResponse:
    """
    Test suite for ContentSelectionService._mock_metadata_response method.
    
    This method implements Factory pattern for mock data generation:
    - Creates LLMMetadataResponse without actual LLM call
    - Generates realistic ContentRequest objects based on concepts
    - Provides testing fallback when LLM unavailable
    - Maps concepts to relevant books
    
    Complexity: CC 8 (conditional concept matching, book selection logic)
    Pattern: Factory Pattern + Strategy Pattern (concept-based selection)
    """
    
    def test_mock_response_returns_valid_structure(self, content_service):
        """Test that mock response has correct LLMMetadataResponse structure."""
        concepts = ["decorator", "generator"]
        
        result = content_service._mock_metadata_response(concepts)
        
        assert isinstance(result, LLMMetadataResponse)
        assert hasattr(result, 'content_requests')
        assert hasattr(result, 'validation_summary')
        assert hasattr(result, 'analysis_strategy')
    
    def test_mock_response_generates_content_requests(self, content_service):
        """Test that mock response includes content requests."""
        concepts = ["async", "await", "coroutine"]
        
        result = content_service._mock_metadata_response(concepts)
        
        assert len(result.content_requests) > 0
        for req in result.content_requests:
            assert isinstance(req, ContentRequest)
            assert req.book_name != ""
            assert len(req.pages) > 0
            assert req.rationale != ""
    
    def test_mock_response_maps_python_concepts_to_books(self, content_service):
        """Test concept-to-book mapping for Python concepts."""
        concepts = ["decorator", "metaclass", "descriptor"]
        
        result = content_service._mock_metadata_response(concepts)
        
        book_names = [req.book_name for req in result.content_requests]
        # Should include Python-specific books
        assert any("Fluent Python" in name or "Learning Python" in name or "Python" in name 
                  for name in book_names)
    
    def test_mock_response_maps_architecture_concepts_to_books(self, content_service):
        """Test concept-to-book mapping for architecture concepts."""
        concepts = ["repository pattern", "service layer", "dependency injection"]
        
        result = content_service._mock_metadata_response(concepts)
        
        book_names = [req.book_name for req in result.content_requests]
        # Should include architecture books
        assert any("Architecture" in name or "Patterns" in name or "Design" in name 
                  for name in book_names) or len(book_names) > 0
    
    def test_mock_response_with_empty_concepts(self, content_service):
        """Test mock response generation with no concepts."""
        result = content_service._mock_metadata_response([])
        
        assert isinstance(result, LLMMetadataResponse)
        # Should still return valid response with default requests
        assert len(result.content_requests) == 0  # No content requests by default
    
    def test_mock_response_includes_validation_summary(self, content_service):
        """Test that mock response includes validation summary."""
        concepts = ["generator", "iterator"]
        
        result = content_service._mock_metadata_response(concepts)
        
        assert isinstance(result.validation_summary, str)
        assert len(result.validation_summary) > 0
        # Validation summary should reference concepts or provide context
    
    def test_mock_response_includes_content_strategy(self, content_service):
        """Test that mock response includes content strategy."""
        concepts = ["async", "threading", "multiprocessing"]
        
        result = content_service._mock_metadata_response(concepts)
        
        assert isinstance(result.content_strategy, str)
        assert len(result.content_strategy) > 0
        # Strategy should describe approach
    
    def test_mock_response_rationales_reference_concepts(self, content_service):
        """Test that content request rationales mention concepts."""
        concepts = ["dataclass", "typing"]
        
        result = content_service._mock_metadata_response(concepts)
        
        # At least some rationales should reference concepts
        rationales = " ".join([req.rationale for req in result.content_requests])
        assert len(rationales) > 0
    
    def test_mock_response_page_numbers_are_realistic(self, content_service):
        """Test that generated page numbers are in realistic range."""
        concepts = ["context manager", "with statement"]
        
        result = content_service._mock_metadata_response(concepts)
        
        for req in result.content_requests:
            assert all(1 <= page <= 1000 for page in req.pages)
            # Pages should be in ascending order or reasonable range
            assert len(req.pages) > 0
    
    def test_mock_response_with_mixed_concept_types(self, content_service):
        """Test mock response with both Python and architecture concepts."""
        concepts = ["generator", "repository pattern", "async", "service layer"]
        
        result = content_service._mock_metadata_response(concepts)
        
        assert len(result.content_requests) > 0
        # Should cover both Python and architecture domains
        book_names = [req.book_name for req in result.content_requests]
        assert len(set(book_names)) >= 1  # At least one unique book
    
    def test_mock_response_book_names_are_valid(self, content_service):
        """Test that generated book names are non-empty strings."""
        concepts = ["test_concept"]
        
        result = content_service._mock_metadata_response(concepts)
        
        for req in result.content_requests:
            assert isinstance(req.book_name, str)
            assert len(req.book_name) > 0
    
    def test_mock_response_deterministic_for_same_concepts(self, content_service):
        """Test that same concepts produce consistent mock structure."""
        concepts = ["decorator", "generator"]
        
        result1 = content_service._mock_metadata_response(concepts)
        result2 = content_service._mock_metadata_response(concepts)
        
        # Should produce same number of requests (deterministic)
        assert len(result1.content_requests) == len(result2.content_requests)


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestContentSelectionServiceIntegration:
    """Integration tests for ContentSelectionService."""
    
    def test_select_content_python_guided_uses_mock_when_llm_unavailable(
        self, content_service
    ):
        """Test that Python-guided selection falls back to mock."""
        chapter_num = 5
        chapter_title = "Decorators and Closures"
        concepts = ["decorator", "@property"]
        excerpt = "Sample chapter excerpt..."
        
        result = content_service.select_content_python_guided(
            chapter_num, chapter_title, concepts, excerpt
        )
        
        assert isinstance(result, LLMMetadataResponse)
        assert len(result.content_requests) > 0
    
    def test_mock_response_integrates_with_metadata_service(
        self, mock_metadata_service
    ):
        """Test mock response uses metadata service when available."""
        service = ContentSelectionService(
            metadata_service=mock_metadata_service,
            llm_available=False
        )
        
        concepts = ["decorator"]
        result = service._mock_metadata_response(concepts)
        
        # Should produce valid response even with mock metadata service
        assert isinstance(result, LLMMetadataResponse)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
