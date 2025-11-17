"""
Tests for LLM integration functions.

This test suite covers Sprint 1 critical fixes per REFACTORING_PLAN.md:
- JSON response validation (_validate_json_response)
- Truncated response handling (_handle_truncated_response)
- Finish reason validation (FinishReason enum)

Following TDD: Tests written BEFORE implementation.
"""

import json
import pytest
from unittest.mock import patch

# Note: Import will fail until we implement the functions
# This is expected in TDD - write tests first, then make them pass
try:
    from shared.llm_integration import (
        _validate_json_response,
        _handle_truncated_response,
        FinishReason
    )
except ImportError:
    # Allow tests to load even if functions don't exist yet
    _validate_json_response = None
    _handle_truncated_response = None
    FinishReason = None


class TestValidateJsonResponse:
    """
    Tests for _validate_json_response() function.
    
    Per REFACTORING_PLAN.md section 1.1:
    - Validates finish_reason (must be "end_turn")
    - Validates JSON syntax
    - Validates structure for Phase 1 responses
    - Validates required fields
    """
    
    @pytest.mark.skipif(_validate_json_response is None, reason="Function not implemented yet")
    def test_valid_phase1_response(self):
        """Test valid Phase 1 response with all required fields."""
        response = json.dumps([
            {
                "book_title": "Fluent Python 2nd",
                "chapter": "Chapter 3",
                "reason": "Covers decorators and closures"
            }
        ])
        
        is_valid, error = _validate_json_response(response, "end_turn")
        assert is_valid is True
        assert error is None
    
    @pytest.mark.skipif(_validate_json_response is None, reason="Function not implemented yet")
    def test_invalid_finish_reason(self):
        """Test rejection of incomplete responses (finish_reason != 'end_turn')."""
        response = json.dumps([{"book_title": "Test", "chapter": "Ch1", "reason": "Test"}])
        
        is_valid, error = _validate_json_response(response, "max_tokens")
        assert is_valid is False
        assert "Incomplete response" in error
        assert "max_tokens" in error
    
    @pytest.mark.skipif(_validate_json_response is None, reason="Function not implemented yet")
    def test_invalid_json_syntax(self):
        """Test rejection of malformed JSON."""
        response = '{"book_title": "Test", "chapter": "Ch1"'  # Missing closing brace
        
        is_valid, error = _validate_json_response(response, "end_turn")
        assert is_valid is False
        assert "Invalid JSON" in error
    
    @pytest.mark.skipif(_validate_json_response is None, reason="Function not implemented yet")
    def test_missing_required_fields(self):
        """Test rejection when required fields are missing."""
        response = json.dumps([
            {
                "book_title": "Fluent Python 2nd",
                # Missing "chapter" and "reason"
            }
        ])
        
        is_valid, error = _validate_json_response(response, "end_turn")
        assert is_valid is False
        assert "missing fields" in error.lower()
        assert "chapter" in error or "reason" in error
    
    @pytest.mark.skipif(_validate_json_response is None, reason="Function not implemented yet")
    def test_item_not_dict(self):
        """Test rejection when array item is not a dict."""
        response = json.dumps([
            "This should be a dict, not a string"
        ])
        
        is_valid, error = _validate_json_response(response, "end_turn")
        assert is_valid is False
        assert "not a dict" in error.lower()
    
    @pytest.mark.skipif(_validate_json_response is None, reason="Function not implemented yet")
    def test_multiple_items_valid(self):
        """Test validation with multiple valid items."""
        response = json.dumps([
            {
                "book_title": "Fluent Python 2nd",
                "chapter": "Chapter 3",
                "reason": "Decorators"
            },
            {
                "book_title": "Python Cookbook 3rd",
                "chapter": "Chapter 7",
                "reason": "Functions"
            }
        ])
        
        is_valid, error = _validate_json_response(response, "end_turn")
        assert is_valid is True
        assert error is None
    
    @pytest.mark.skipif(_validate_json_response is None, reason="Function not implemented yet")
    def test_multiple_items_one_invalid(self):
        """Test rejection when one item in array is invalid."""
        response = json.dumps([
            {
                "book_title": "Fluent Python 2nd",
                "chapter": "Chapter 3",
                "reason": "Decorators"
            },
            {
                "book_title": "Python Cookbook 3rd",
                # Missing "chapter" and "reason"
            }
        ])
        
        is_valid, error = _validate_json_response(response, "end_turn")
        assert is_valid is False
        assert "Item 1" in error  # Second item (index 1) is invalid


class TestHandleTruncatedResponse:
    """
    Tests for _handle_truncated_response() function.
    
    Per REFACTORING_PLAN.md section 1.1:
    - Progressive constraint tightening (15 -> 10 -> 5 books)
    - Phase 1: Retryable with constraints
    - Phase 2: Not retryable (would lose content)
    - Max retries limit
    """
    
    @pytest.mark.skipif(_handle_truncated_response is None, reason="Function not implemented yet")
    @patch('src.llm_integration.call_llm')
    def test_phase1_retry_with_constraint(self, mock_call_llm):
        """Test Phase 1 retry adds constraint to system message."""
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Analyze this chapter"}
        ]
        mock_call_llm.return_value = "Successful retry response"
        
        result = _handle_truncated_response("phase_1", messages, attempt=0)
        
        # Verify retry was attempted
        assert mock_call_llm.called
        assert result == "Successful retry response"
        
        # Verify constraint was added to system message
        call_args = mock_call_llm.call_args[0][0]  # First positional arg (messages)
        system_msg = call_args[0]["content"]
        assert "TOP 10" in system_msg or "10 most relevant" in system_msg.lower()
    
    @pytest.mark.skipif(_handle_truncated_response is None, reason="Function not implemented yet")
    def test_phase2_no_retry(self):
        """Test Phase 2 cannot retry (would lose content)."""
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Generate annotation"}
        ]
        
        result = _handle_truncated_response("phase_2", messages, attempt=0)
        
        assert result is None  # Should not retry
    
    @pytest.mark.skipif(_handle_truncated_response is None, reason="Function not implemented yet")
    def test_max_retries_exceeded(self):
        """Test max retries limit is enforced."""
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Analyze this chapter"}
        ]
        
        result = _handle_truncated_response("phase_1", messages, attempt=2, max_retries=2)
        
        assert result is None  # Should not retry past limit
    
    @pytest.mark.skipif(_handle_truncated_response is None, reason="Function not implemented yet")
    @patch('src.llm_integration.call_llm')
    def test_progressive_constraints(self, mock_call_llm):
        """Test progressive constraint tightening (15 -> 10 -> 5)."""
        messages_template = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Analyze this chapter"}
        ]
        mock_call_llm.return_value = "Success"
        
        # First retry: Should limit to 10 books
        messages_0 = [{"role": msg["role"], "content": msg["content"]} for msg in messages_template]
        _handle_truncated_response("phase_1", messages_0, attempt=0)
        call_args_0 = mock_call_llm.call_args[0][0]
        assert "10" in call_args_0[0]["content"]
        
        # Second retry: Should limit to 5 books
        messages_1 = [{"role": msg["role"], "content": msg["content"]} for msg in messages_template]
        _handle_truncated_response("phase_1", messages_1, attempt=1)
        call_args_1 = mock_call_llm.call_args[0][0]
        assert "5" in call_args_1[0]["content"]
        
        # Third retry: Should limit to 3 books (need max_retries=3 to allow attempt=2)
        messages_2 = [{"role": msg["role"], "content": msg["content"]} for msg in messages_template]
        _handle_truncated_response("phase_1", messages_2, attempt=2, max_retries=3)
        call_args_2 = mock_call_llm.call_args[0][0]
        assert "3" in call_args_2[0]["content"]


class TestFinishReasonEnum:
    """
    Tests for FinishReason enum.
    
    Per REFACTORING_PLAN.md section 1.3:
    - Enum for all possible finish_reason values
    - Type safety for validation
    """
    
    @pytest.mark.skipif(FinishReason is None, reason="Enum not implemented yet")
    def test_enum_has_end_turn(self):
        """Test FinishReason has END_TURN value."""
        assert hasattr(FinishReason, 'END_TURN')
        assert FinishReason.END_TURN.value == "end_turn"
    
    @pytest.mark.skipif(FinishReason is None, reason="Enum not implemented yet")
    def test_enum_has_max_tokens(self):
        """Test FinishReason has MAX_TOKENS value."""
        assert hasattr(FinishReason, 'MAX_TOKENS')
        assert FinishReason.MAX_TOKENS.value == "max_tokens"
    
    @pytest.mark.skipif(FinishReason is None, reason="Enum not implemented yet")
    def test_enum_has_stop_sequence(self):
        """Test FinishReason has STOP_SEQUENCE value."""
        assert hasattr(FinishReason, 'STOP_SEQUENCE')
        assert FinishReason.STOP_SEQUENCE.value == "stop_sequence"
    
    @pytest.mark.skipif(FinishReason is None, reason="Enum not implemented yet")
    def test_enum_from_string(self):
        """Test converting string to FinishReason."""
        finish_reason = FinishReason("end_turn")
        assert finish_reason == FinishReason.END_TURN


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
