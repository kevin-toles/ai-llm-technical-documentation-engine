"""
Unit tests for ContentSelectionService._mock_metadata_response (CC 8)

Tests focus on _mock_metadata_response method with CC 8:
- Mock response generation using Python keyword matching
- Fallback behavior when LLM unavailable
- Content request building from concept matches

Architecture Patterns Applied:
- Factory Pattern: Test mock data generation (Architecture Patterns Ch. 9)
- Strategy Pattern: Test algorithm selection logic (Architecture Patterns Ch. 13)
- Service Layer Pattern: Test business logic encapsulation (Architecture Patterns Ch. 4)

Sprint: Batch #2 File #7 (HIGH priority, CC 8, tests only)
"""

import pytest
import sys
from pathlib import Path
from typing import List, Dict
from unittest.mock import Mock, MagicMock, patch

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from workflows.llm_enhancement.scripts.phases.content_selection_impl import (
    ContentSelectionService
)
from workflows.llm_enhancement.scripts.models.analysis_models import (
    ContentRequest,
    LLMMetadataResponse
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def mock_metadata_service():
    """Create mock MetadataExtractionService for testing."""
    service = Mock()
    service._repo = Mock()
    service._repo.get_all = Mock(return_value=[])
    return service


@pytest.fixture
def content_service(mock_metadata_service):
    """Create ContentSelectionService instance for testing."""
    return ContentSelectionService(metadata_service=mock_metadata_service, llm_available=False)


@pytest.fixture
def mock_metadata_package():
    """Sample metadata package with concept mapping."""
    return {
        'books': [
            {'file_name': 'Fluent Python 2nd', 'relevance_to_chapter': 0.8},
            {'file_name': 'Python Distilled', 'relevance_to_chapter': 0.7}
        ],
        'concept_mapping': {
            'Fluent Python 2nd': {
                10: ['decorator', 'generator'],
                11: ['decorator'],
                12: ['generator', 'iterator']
            },
            'Python Distilled': {
                5: ['decorator'],
                6: ['generator']
            }
        },
        'total_books': 2
    }


# ============================================================================
# TEST CLASS: _mock_metadata_response (CC 8)
# ============================================================================

class TestMockMetadataResponse:
    """
    Test ContentSelectionService._mock_metadata_response method.
    
    This method generates mock LLMMetadataResponse when LLM unavailable:
    - Uses actual Python keyword matching results
    - Builds content requests from concept matches
    - Provides fallback strategy
    
    Complexity: CC 8 (conditional logic for concept selection and request building)
    Pattern: Factory Pattern for mock data generation
    """
    
    def test_mock_response_with_no_metadata_package(self, content_service):
        """Test mock response when no metadata package available (fallback)."""
        # Arrange - no _last_metadata_package
        concepts = ["decorator", "generator"]
        
        # Act
        result = content_service._mock_metadata_response(concepts)
        
        # Assert - should return fallback request
        assert isinstance(result, LLMMetadataResponse)
        assert len(result.content_requests) >= 1
        assert result.content_requests[0].book_name == "Python Distilled"
        assert result.validation_summary != ""
        assert result.analysis_strategy != ""
    
    @patch('workflows.llm_enhancement.scripts.phases.content_selection_impl.settings')
    def test_mock_response_with_metadata_package(self, mock_settings, content_service, mock_metadata_package):
        """Test mock response uses metadata package concept mapping."""
        # Arrange
        mock_settings.taxonomy.max_books = 10
        content_service._last_metadata_package = mock_metadata_package
        concepts = ["decorator", "generator", "iterator"]
        
        # Act
        result = content_service._mock_metadata_response(concepts)
        
        # Assert - should build requests from concept mapping
        assert isinstance(result, LLMMetadataResponse)
        assert len(result.content_requests) > 0
        # Should attempt to process books from concept_mapping
        book_names = [req.book_name for req in result.content_requests]
        assert any(name in book_names for name in ['Fluent Python 2nd', 'Python Distilled'])
    
    def test_mock_response_empty_concepts_list(self, content_service):
        """Test mock response with empty concepts (edge case)."""
        # Arrange
        concepts = []
        
        # Act
        result = content_service._mock_metadata_response(concepts)
        
        # Assert - should still return valid response
        assert isinstance(result, LLMMetadataResponse)
        assert len(result.content_requests) >= 1  # Fallback request
        assert result.validation_summary != ""
    
    def test_mock_response_structure_matches_real(self, content_service):
        """Test mock response has same structure as real LLMMetadataResponse."""
        # Arrange
        concepts = ["async", "await"]
        
        # Act
        result = content_service._mock_metadata_response(concepts)
        
        # Assert - verify all required fields present
        assert hasattr(result, 'validation_summary')
        assert hasattr(result, 'gap_analysis')
        assert hasattr(result, 'content_requests')
        assert hasattr(result, 'analysis_strategy')
        assert isinstance(result.content_requests, list)
    
    def test_mock_response_content_requests_have_required_fields(self, content_service):
        """Test that generated content requests have all required fields."""
        # Arrange
        concepts = ["metaclass"]
        
        # Act
        result = content_service._mock_metadata_response(concepts)
        
        # Assert - each request should have required fields
        for req in result.content_requests:
            assert isinstance(req, ContentRequest)
            assert hasattr(req, 'book_name')
            assert hasattr(req, 'pages')
            assert hasattr(req, 'rationale')
            assert hasattr(req, 'priority')
            assert isinstance(req.pages, list)
            assert len(req.pages) > 0
    
    @patch('workflows.llm_enhancement.scripts.phases.content_selection_impl.settings')
    def test_mock_response_validation_summary_describes_results(self, mock_settings, content_service, mock_metadata_package):
        """Test validation summary reflects the number of books/pages."""
        # Arrange
        mock_settings.taxonomy.max_books = 10
        content_service._last_metadata_package = mock_metadata_package
        concepts = ["decorator"]
        
        # Act
        result = content_service._mock_metadata_response(concepts)
        
        # Assert - validation summary should mention books
        assert "book" in result.validation_summary.lower() or len(result.validation_summary) > 20
        assert result.validation_summary != ""
    
    def test_mock_response_handles_missing_concept_mapping(self, content_service):
        """Test behavior when metadata package missing concept_mapping."""
        # Arrange
        content_service._last_metadata_package = {'books': [], 'total_books': 0}
        concepts = ["generator"]
        
        # Act
        result = content_service._mock_metadata_response(concepts)
        
        # Assert - should fallback gracefully
        assert isinstance(result, LLMMetadataResponse)
        assert len(result.content_requests) >= 1
    
    @patch('workflows.llm_enhancement.scripts.phases.content_selection_impl.settings')
    def test_mock_response_with_many_concepts(self, mock_settings, content_service, mock_metadata_package):
        """Test mock response with large number of concepts."""
        # Arrange
        mock_settings.taxonomy.max_books = 10
        content_service._last_metadata_package = mock_metadata_package
        concepts = ["decorator", "generator", "iterator", "async", "await", 
                   "coroutine", "metaclass", "descriptor", "closure"]
        
        # Act
        result = content_service._mock_metadata_response(concepts)
        
        # Assert - should handle many concepts without error
        assert isinstance(result, LLMMetadataResponse)
        assert len(result.content_requests) > 0
    
    def test_mock_response_strategy_describes_approach(self, content_service):
        """Test analysis_strategy field is substantive."""
        # Arrange
        concepts = ["class", "method"]
        
        # Act
        result = content_service._mock_metadata_response(concepts)
        
        # Assert - strategy should describe synthesis approach
        assert len(result.analysis_strategy) > 20
        assert any(keyword in result.analysis_strategy.lower() 
                  for keyword in ['synthesize', 'cross-reference', 'keyword', 'match'])


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestContentSelectionIntegration:
    """Integration tests for ContentSelectionService with _mock_metadata_response."""
    
    def test_service_initialization_with_llm_unavailable(self, mock_metadata_service):
        """Test service can be initialized when LLM unavailable."""
        # Act
        service = ContentSelectionService(
            metadata_service=mock_metadata_service,
            llm_available=False
        )
        
        # Assert
        assert service._llm_available is False
        assert service._metadata_service is not None
    
    def test_mock_response_used_when_llm_unavailable(self, content_service):
        """Test _mock_metadata_response is appropriate fallback."""
        # Arrange
        concepts = ["pattern"]
        
        # Act - call mock directly (simulates fallback behavior)
        result = content_service._mock_metadata_response(concepts)
        
        # Assert - should return valid response suitable for workflow continuation
        assert isinstance(result, LLMMetadataResponse)
        assert len(result.content_requests) > 0
        assert all(isinstance(req, ContentRequest) for req in result.content_requests)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
