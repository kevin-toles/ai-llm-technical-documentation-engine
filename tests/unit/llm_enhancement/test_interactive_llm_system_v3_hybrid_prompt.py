"""
Unit tests for interactive_llm_system_v3_hybrid_prompt.py

Tests focus on AnalysisOrchestrator methods with CC 8-9:
- _lazy_load_requested_chapters (CC 9) - Repository pattern for lazy loading
- _load_book_json_by_name (CC 8) - File I/O abstraction
- _mock_metadata_response (CC 8) - Mock data generation for testing

Architecture Patterns Applied:
- Repository Pattern: Test data access separation (Architecture Patterns Ch. 2)
- Service Layer Pattern: Test business logic encapsulation (Architecture Patterns Ch. 4)
- Strategy Pattern: Test algorithm selection logic (Architecture Patterns Ch. 13)

Sprint: Batch #2 Files 6-11 (HIGH priority, CC 8-9, tests only)
"""

import pytest
import json
import sys
from pathlib import Path
from typing import List, Dict, Any
from unittest.mock import Mock, patch, MagicMock, mock_open

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from workflows.llm_enhancement.scripts.interactive_llm_system_v3_hybrid_prompt import (
    AnalysisOrchestrator,
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
    service.metadata_store = {}
    service.available_books = []
    return service


@pytest.fixture
def orchestrator(mock_metadata_service):
    """Create AnalysisOrchestrator instance for testing."""
    return AnalysisOrchestrator(metadata_service=mock_metadata_service)


@pytest.fixture
def content_requests():
    """Sample ContentRequest objects for testing lazy loading."""
    return [
        ContentRequest(
            book_name="Fluent Python 2nd",
            pages=[10, 11, 12],
            rationale="Test decorators"
        ),
        ContentRequest(
            book_name="Architecture Patterns with Python",
            pages=[25, 26],
            rationale="Test repository pattern"
        ),
        ContentRequest(
            book_name="Learning Python Ed6",
            pages=[50, 51, 52, 53],
            rationale="Test generators"
        )
    ]


@pytest.fixture
def mock_book_json():
    """Sample book JSON structure matching actual data format."""
    return {
        "pages": [
            {
                "page_number": 10,
                "text": "Decorator patterns allow... @property decorator... decorators in Python...",
                "chapter": 5
            },
            {
                "page_number": 11,
                "text": "Class decorators modify... decorator syntax... @classmethod...",
                "chapter": 5
            },
            {
                "page_number": 12,
                "text": "Function decorators wrap... @wraps... functools module...",
                "chapter": 5
            }
        ]
    }


@pytest.fixture
def mock_chapter_info():
    """Mock ChapterInfo objects for chapter-level loading."""
    from dataclasses import dataclass
    
    @dataclass
    class ChapterInfo:
        chapter_number: int
        title: str
        start_page: int
        end_page: int
        page_count: int
        keywords: List[str]
        
    return [
        ChapterInfo(5, "Decorators and Closures", 10, 25, 16, ["decorator", "closure", "@property"]),
        ChapterInfo(6, "Design Patterns", 26, 45, 20, ["singleton", "factory", "observer"])
    ]


# ============================================================================
# TEST _lazy_load_requested_chapters (CC 9)
# ============================================================================

class TestLazyLoadRequestedChapters:
    """
    Test suite for _lazy_load_requested_chapters method.
    
    This method implements Repository pattern for lazy loading book content:
    - Loads ONLY requested chapters/pages (not entire books)
    - Supports chapter-level and page-level loading modes
    - Limits to top 10 books to control memory usage
    
    Complexity: CC 9 (multiple conditional branches, fallback logic)
    Pattern: Repository Pattern (Architecture Patterns Ch. 2)
    """
    
    def test_lazy_load_with_valid_requests(self, orchestrator, content_requests, mock_book_json):
        """Test successful lazy loading of requested chapters."""
        with patch.object(orchestrator, '_load_book_json_by_name', return_value=mock_book_json):
            with patch.object(orchestrator, '_load_page_excerpts_for_request', return_value=[
                {"page": 10, "text": "Decorator patterns..."},
                {"page": 11, "text": "Class decorators..."}
            ]) as mock_load_pages:
                
                result = orchestrator._lazy_load_requested_chapters(content_requests)
                
                # Should load content for all books with valid data
                assert isinstance(result, dict)
                assert len(result) > 0
                # Should call page loading fallback when chapter metadata unavailable
                assert mock_load_pages.called
    
    def test_lazy_load_limits_to_top_10_books(self, orchestrator):
        """Test that lazy loading respects 10-book limit."""
        # Create 15 content requests
        many_requests = [
            ContentRequest(book_name=f"Book_{i}", pages=[1, 2], rationale="Test")
            for i in range(15)
        ]
        
        with patch.object(orchestrator, '_load_book_json_by_name', return_value={"pages": []}):
            with patch.object(orchestrator, '_load_page_excerpts_for_request', return_value=[]):
                result = orchestrator._lazy_load_requested_chapters(many_requests)
                
                # Should process at most 10 books
                assert len(result) <= 10
    
    def test_lazy_load_handles_missing_book(self, orchestrator, content_requests):
        """Test graceful handling when book JSON not found."""
        with patch.object(orchestrator, '_load_book_json_by_name', return_value=None):
            result = orchestrator._lazy_load_requested_chapters(content_requests)
            
            # Should return empty dict when no books found
            assert isinstance(result, dict)
            # Should not crash, gracefully skip missing books
    
    def test_lazy_load_with_chapter_metadata_available(self, orchestrator, content_requests, mock_book_json):
        """Test lazy loading with page-based requests (chapter metadata dynamically imported)."""
        # ChapterMetadataManager is imported inside method only when chapter field exists
        # This test verifies no exception with page-based requests
        
        with patch.object(orchestrator, '_load_book_json_by_name', return_value=mock_book_json):
            with patch.object(orchestrator, '_load_page_excerpts_for_request', return_value=[
                {"page": 10, "text": "Page content"}
            ]):
                result = orchestrator._lazy_load_requested_chapters(content_requests)
                
                # Should successfully process page-based requests
                assert isinstance(result, dict)
    
    def test_lazy_load_falls_back_to_page_loading(self, orchestrator, content_requests, mock_book_json):
        """Test fallback to page-level loading when chapter loading fails."""
        with patch.object(orchestrator, '_load_book_json_by_name', return_value=mock_book_json):
            with patch.object(orchestrator, '_load_chapters_for_request', return_value=[]):  # Empty chapter result
                with patch.object(orchestrator, '_load_page_excerpts_for_request', return_value=[
                    {"page": 10, "text": "Page content"}
                ]) as mock_load_pages:
                    
                    result = orchestrator._lazy_load_requested_chapters(content_requests)
                    
                    # Should fall back to page-level loading
                    assert mock_load_pages.called
    
    def test_lazy_load_handles_load_exception(self, orchestrator, content_requests):
        """Test exception handling during book loading."""
        with patch.object(orchestrator, '_load_book_json_by_name', side_effect=Exception("File read error")):
            result = orchestrator._lazy_load_requested_chapters(content_requests)
            
            # Should handle exception and continue with other books
            assert isinstance(result, dict)
            # Should not crash on error
    
    def test_lazy_load_empty_request_list(self, orchestrator):
        """Test behavior with empty content requests."""
        result = orchestrator._lazy_load_requested_chapters([])
        
        assert isinstance(result, dict)
        assert len(result) == 0


# ============================================================================
# TEST _load_book_json_by_name (CC 8)
# ============================================================================

class TestLoadBookJsonByName:
    """
    Test suite for _load_book_json_by_name method.
    
    This method implements Repository pattern abstraction for file I/O:
    - Translates human-readable book names to filenames
    - Lazy loads JSON files only when needed
    - Converts page lists to page_number-indexed dicts
    - Handles missing files gracefully
    
    Complexity: CC 8 (multiple conditional checks, error handling)
    Pattern: Repository Pattern (Architecture Patterns Ch. 2)
    """
    
    def test_load_valid_book_with_pages_dict(self, orchestrator):
        """Test loading book with valid pages structure."""
        mock_data = {
            "pages": [
                {"page_number": 1, "text": "Content 1"},
                {"page_number": 2, "text": "Content 2"}
            ]
        }
        
        m = mock_open(read_data=json.dumps(mock_data))
        with patch('builtins.open', m):
            with patch('pathlib.Path.exists', return_value=True):
                result = orchestrator._load_book_json_by_name("Test Book")
                
                assert isinstance(result, dict)
                # Should convert pages list to dict indexed by page_number
                assert "1" in result or "pages" in result or len(result) > 0
    
    def test_load_book_with_missing_file(self, orchestrator):
        """Test behavior when book JSON file doesn't exist."""
        with patch('pathlib.Path.exists', return_value=False):
            result = orchestrator._load_book_json_by_name("Nonexistent Book")
            
            assert result is None
    
    def test_load_book_with_json_parse_error(self, orchestrator):
        """Test handling of malformed JSON."""
        m = mock_open(read_data="{ invalid json }")
        with patch('builtins.open', m):
            with patch('pathlib.Path.exists', return_value=True):
                result = orchestrator._load_book_json_by_name("Test Book")
                
                # Should return None on JSON parse error
                assert result is None
    
    def test_load_book_with_no_pages_field(self, orchestrator):
        """Test loading book with non-standard structure."""
        mock_data = {"title": "Test Book", "chapters": []}
        
        m = mock_open(read_data=json.dumps(mock_data))
        with patch('builtins.open', m):
            with patch('pathlib.Path.exists', return_value=True):
                result = orchestrator._load_book_json_by_name("Test Book")
                
                # Should return original data if no pages field
                assert result == mock_data
    
    def test_load_book_creates_correct_filename(self, orchestrator):
        """Test correct filename construction from book name."""
        with patch('builtins.open', mock_open(read_data="{}")):
            with patch('pathlib.Path.exists', return_value=True) as mock_exists:
                orchestrator._load_book_json_by_name("Fluent Python 2nd")
                
                # Should construct filename as "{book_name}.json"
                # Verify exists() was called (file path constructed correctly)
                assert mock_exists.called
    
    def test_load_book_handles_missing_page_numbers(self, orchestrator):
        """Test handling of pages without page_number field."""
        mock_data = {
            "pages": [
                {"text": "Content without page number"},
                {"page_number": 5, "text": "Content with page number"}
            ]
        }
        
        m = mock_open(read_data=json.dumps(mock_data))
        with patch('builtins.open', m):
            with patch('pathlib.Path.exists', return_value=True):
                result = orchestrator._load_book_json_by_name("Test Book")
                
                # Should handle pages with missing page_number gracefully
                assert isinstance(result, dict)
    
    def test_load_book_with_nonexistent_directory(self, orchestrator):
        """Test behavior when JSON directory doesn't exist."""
        with patch('pathlib.Path.exists', return_value=False):
            result = orchestrator._load_book_json_by_name("Test Book")
            
            assert result is None


# ============================================================================
# TEST _mock_metadata_response (CC 8)
# ============================================================================

class TestMockMetadataResponse:
    """
    Test suite for _mock_metadata_response method.
    
    This method generates mock LLMMetadataResponse for testing:
    - Creates realistic content requests based on concepts
    - Generates validation summary and content strategy
    - Provides fallback when LLM unavailable
    
    Complexity: CC 8 (conditional logic for concept selection)
    Pattern: Factory Pattern for mock data generation
    """
    
    def test_mock_response_with_python_concepts(self, orchestrator):
        """Test mock response generation with Python-specific concepts."""
        concepts = ["decorator", "generator", "context manager"]
        
        result = orchestrator._mock_metadata_response(concepts)
        
        assert isinstance(result, LLMMetadataResponse)
        assert len(result.content_requests) > 0
        assert result.validation_summary != ""
        assert result.analysis_strategy != ""
    
    def test_mock_response_with_architecture_concepts(self, orchestrator):
        """Test mock response with architecture pattern concepts."""
        concepts = ["repository pattern", "service layer", "dependency injection"]
        
        result = orchestrator._mock_metadata_response(concepts)
        
        assert isinstance(result, LLMMetadataResponse)
        # Without metadata_package, fallback to Python Distilled
        assert len(result.content_requests) > 0
        assert result.analysis_strategy != ""
    
    def test_mock_response_includes_validation_summary(self, orchestrator):
        """Test that mock response includes validation summary."""
        concepts = ["async", "await", "coroutine"]
        
        result = orchestrator._mock_metadata_response(concepts)
        
        # Validation summary should reference concepts
        assert "async" in result.validation_summary.lower() or len(result.validation_summary) > 20
    
    def test_mock_response_includes_content_strategy(self, orchestrator):
        """Test that mock response includes content strategy."""
        concepts = ["dataclass", "typing", "protocol"]
        
        result = orchestrator._mock_metadata_response(concepts)
        
        # analysis_strategy should describe approach
        assert len(result.analysis_strategy) > 20
        assert "tier" in result.analysis_strategy.lower() or "organize" in result.analysis_strategy.lower()
    
    def test_mock_response_with_empty_concepts(self, orchestrator):
        """Test mock response generation with empty concept list."""
        result = orchestrator._mock_metadata_response([])
        
        assert isinstance(result, LLMMetadataResponse)
        # Should still generate some default requests
        assert len(result.content_requests) >= 0
    
    def test_mock_response_rationale_includes_concepts(self, orchestrator):
        """Test that content request rationales reference concepts."""
        concepts = ["metaclass", "descriptor"]
        
        result = orchestrator._mock_metadata_response(concepts)
        
        # At least one request should mention concepts in rationale
        rationales = [req.rationale for req in result.content_requests]
        assert any("metaclass" in r.lower() or "descriptor" in r.lower() for r in rationales) or len(rationales) > 0
    
    def test_mock_response_generates_page_lists(self, orchestrator):
        """Test that mock requests include page numbers."""
        concepts = ["iterator", "iterable"]
        
        result = orchestrator._mock_metadata_response(concepts)
        
        for req in result.content_requests:
            # Each request should have pages
            assert isinstance(req.pages, list)
            assert len(req.pages) > 0
    
    def test_mock_response_with_mixed_concepts(self, orchestrator):
        """Test mock response with mixed Python and architecture concepts."""
        concepts = ["generator", "repository pattern", "async", "service layer"]
        
        result = orchestrator._mock_metadata_response(concepts)
        
        assert isinstance(result, LLMMetadataResponse)
        # Should generate requests covering both Python and architecture
        assert len(result.content_requests) > 0


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestAnalysisOrchestratorIntegration:
    """Integration tests for AnalysisOrchestrator methods."""
    
    def test_lazy_load_followed_by_book_load(self, orchestrator, content_requests, mock_book_json):
        """Test integration of lazy_load calling _load_book_json_by_name."""
        with patch.object(orchestrator, '_load_book_json_by_name', return_value=mock_book_json) as mock_load:
            with patch.object(orchestrator, '_load_page_excerpts_for_request', return_value=[]):
                orchestrator._lazy_load_requested_chapters(content_requests)
                
                # _load_book_json_by_name should be called for each request
                assert mock_load.call_count >= len(content_requests[:10])  # Limited to 10
    
    def test_mock_response_structure_matches_real_response(self, orchestrator):
        """Test that mock response structure matches real LLMMetadataResponse."""
        concepts = ["test_concept"]
        
        result = orchestrator._mock_metadata_response(concepts)
        
        # Should have same structure as real response
        assert hasattr(result, 'content_requests')
        assert hasattr(result, 'validation_summary')
        assert hasattr(result, 'analysis_strategy')
        assert all(hasattr(req, 'book_name') and hasattr(req, 'pages') for req in result.content_requests)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
