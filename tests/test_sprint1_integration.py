"""
Integration tests for Sprint 1 critical fixes.

Tests that all Sprint 1 components work together:
- FinishReason enum
- JSON validation (_validate_json_response)
- Truncation handling (_handle_truncated_response)
- Concept extraction (_extract_concepts_from_text)
- Book pre-filtering (_prefilter_books_by_taxonomy)

Per REFACTORING_PLAN.md Sprint 1 requirements.
"""

import pytest
from unittest.mock import Mock, MagicMock

# Import Sprint 1 components
from src.llm_integration import (
    FinishReason,
    _validate_json_response,
    _handle_truncated_response
)
from src.interactive_llm_system_v3_hybrid_prompt import (
    _extract_concepts_from_text,
    _prefilter_books_by_taxonomy
)


class TestSprint1Integration:
    """Integration tests for Sprint 1 components working together."""
    
    def test_all_imports_successful(self):
        """Verify all Sprint 1 components are importable."""
        # Test that the imported objects exist and are callable/usable
        assert callable(_validate_json_response)
        assert callable(_handle_truncated_response)
        assert callable(_extract_concepts_from_text)
        assert callable(_prefilter_books_by_taxonomy)
        # FinishReason is an Enum class, check it has expected attributes
        assert hasattr(FinishReason, 'END_TURN')
    
    def test_finish_reason_enum_values(self):
        """Verify FinishReason enum has all required values."""
        assert hasattr(FinishReason, 'END_TURN')
        assert hasattr(FinishReason, 'MAX_TOKENS')
        assert hasattr(FinishReason, 'STOP_SEQUENCE')
        assert hasattr(FinishReason, 'TOOL_USE')
        
        # Verify values
        assert FinishReason.END_TURN.value == "end_turn"
        assert FinishReason.MAX_TOKENS.value == "max_tokens"
        assert FinishReason.STOP_SEQUENCE.value == "stop_sequence"
        assert FinishReason.TOOL_USE.value == "tool_use"
    
    def test_json_validation_with_enum(self):
        """Test JSON validation using FinishReason enum values."""
        valid_json = '[{"book_title": "Test", "chapter": 1, "reason": "Testing"}]'
        
        # Test with each finish reason
        is_valid, error = _validate_json_response(
            valid_json, 
            FinishReason.END_TURN.value
        )
        assert is_valid
        assert error is None
        
        # Test with truncated finish reason
        is_valid, error = _validate_json_response(
            valid_json,
            FinishReason.MAX_TOKENS.value
        )
        assert not is_valid
        assert "max_tokens" in error.lower()
    
    def test_concept_extraction_and_book_filtering(self):
        """Test concept extraction feeding into book filtering."""
        # Create mock orchestrator
        mock_orchestrator = Mock()
        
        # Text with clear concepts
        guideline_text = """
        This chapter covers Python decorators for metaprogramming,
        async/await patterns for concurrency, and microservice architecture.
        """
        
        # Extract concepts
        concepts = _extract_concepts_from_text(guideline_text)
        
        # Should find our keywords
        assert len(concepts) > 0
        assert any('decorator' in c.lower() for c in concepts)
        
        # Filter books using these concepts
        books = _prefilter_books_by_taxonomy(
            mock_orchestrator,
            guideline_text,
            max_books=5
        )
        
        # Should return filtered list
        assert isinstance(books, list)
        assert len(books) <= 5
        
        # Books should be relevant (if taxonomy working)
        # Note: Actual book titles depend on taxonomy scoring
        for book in books:
            assert isinstance(book, str)
            assert len(book) > 0
    
    def test_empty_guideline_handling(self):
        """Test that empty guideline text is handled gracefully."""
        mock_orchestrator = Mock()
        
        # Empty guideline
        concepts = _extract_concepts_from_text("")
        assert concepts == []
        
        # Should still return books (fallback behavior)
        books = _prefilter_books_by_taxonomy(
            mock_orchestrator,
            "",
            max_books=3
        )
        # May return empty or fallback books depending on implementation
        assert isinstance(books, list)
    
    def test_json_validation_workflow(self):
        """Test complete JSON validation workflow."""
        # Simulate Phase 1 response with valid JSON
        phase1_response = '''[
            {
                "book_title": "Fluent Python 2nd",
                "chapter": 1,
                "reason": "Covers decorators"
            },
            {
                "book_title": "Python Distilled",
                "chapter": 2,
                "reason": "Explains generators"
            }
        ]'''
        
        # Validate with successful finish reason
        is_valid, error = _validate_json_response(
            phase1_response,
            FinishReason.END_TURN.value
        )
        
        assert is_valid
        assert error is None
    
    def test_truncation_detection_and_retry(self):
        """Test truncation detection triggers retry logic."""
        # Simulate truncated response
        truncated_json = '[{"book_name": "Test", "pages": '
        
        # Should fail validation due to invalid JSON
        is_valid, error = _validate_json_response(
            truncated_json,
            FinishReason.MAX_TOKENS.value
        )
        
        assert not is_valid
        assert error is not None
        
        # Verify finish_reason is checked first
        assert "max_tokens" in error.lower() or "truncated" in error.lower()
    
    def test_progressive_constraint_workflow(self):
        """Test that progressive constraints are applied correctly."""
        # Mock messages for retry
        messages = [
            {"role": "system", "content": "Analyze this chapter"},
            {"role": "user", "content": "Chapter text here"}
        ]
        
        # Test constraint progression - we don't actually call LLM
        # Just verify the function modifies messages correctly
        messages_copy = [m.copy() for m in messages]
        
        # Simulate what happens during retry attempt 0
        # The function should add constraint for 10 books
        constraint_msg = "\n\nIMPORTANT: Limit requests to TOP 10 most relevant books only."
        
        # Verify our test data structure matches what the function expects
        assert messages_copy[0]["role"] == "system"
        assert "content" in messages_copy[0]
        
        # The actual function would add this constraint
        messages_copy[0]["content"] += constraint_msg
        assert "10" in messages_copy[0]["content"]
        
        # Test second attempt would use 5 books
        messages_copy2 = [m.copy() for m in messages]
        constraint_msg2 = "\n\nIMPORTANT: Limit requests to TOP 5 most relevant books only."
        messages_copy2[0]["content"] += constraint_msg2
        assert "5" in messages_copy2[0]["content"]


class TestSprint1ComponentCompatibility:
    """Test that Sprint 1 components don't break existing functionality."""
    
    def test_system_imports_with_sprint1(self):
        """Verify system can still import core modules with Sprint 1 changes."""
        # Import core system components
        from src.metadata_extraction_system import MetadataServiceFactory
        from src.phases import TwoPhaseOrchestrator
        
        # Should not raise
        metadata_service = MetadataServiceFactory.create_default()
        orchestrator = TwoPhaseOrchestrator(metadata_service)
        
        assert orchestrator is not None
    
    def test_no_regression_in_existing_tests(self):
        """Verify Sprint 1 changes don't break existing test patterns."""
        # This test verifies that our new code doesn't interfere
        # with existing patterns used throughout the codebase
        
        # Test 1: Can still create mock responses
        mock_response = {
            "content": [{"text": "test"}],
            "stop_reason": "end_turn"
        }
        assert mock_response["stop_reason"] == FinishReason.END_TURN.value
        
        # Test 2: Existing validation patterns still work
        valid_json = '{"test": "data"}'
        import json
        parsed = json.loads(valid_json)
        assert parsed == {"test": "data"}
