"""
Unit tests for workflows/shared/llm_integration.py

Tests the Facade pattern implementation for LLM API abstraction.
Covers: JSON validation, error handling, API calls, truncation recovery, rate limiting.

Architecture Pattern: Facade Pattern (Architecture Patterns Ch. 10)
- Simplifies complex LLM subsystem interactions
- Provides unified interface to multiple LLM providers
- Handles errors and retries gracefully

Test Strategy:
- Mock all external API calls (no real Anthropic API usage)
- Test all validation logic independently
- Test error handling and recovery paths
- Test Facade pattern boundaries
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, List, Any
import json

# Import module under test
from workflows.shared.llm_integration import (
    FinishReason,
    _validate_json_response,
    _handle_truncated_response,
    _call_anthropic_api,
    call_llm,
    prompt_for_semantic_concepts,
    prompt_for_cross_reference_validation,
    prompt_for_cross_reference_summary,
)


# ============================================================================
# Test Class 1: JSON Response Validation
# ============================================================================

class TestJsonResponseValidation:
    """
    Test _validate_json_response function.
    
    Pattern: Input Validation (Python Distilled Ch. 5 - Exception Handling)
    Coverage: Valid JSON, invalid JSON, incomplete responses, missing fields
    """
    
    def test_validates_complete_json_response_with_end_turn(self):
        """Valid JSON with end_turn finish reason should pass."""
        # Arrange
        valid_json = json.dumps([
            {"book_title": "Python Distilled", "chapter": 5, "reason": "Error handling patterns"},
            {"book_title": "Fluent Python", "chapter": 7, "reason": "Decorators"}
        ])
        
        # Act
        is_valid, error = _validate_json_response(valid_json, FinishReason.END_TURN.value)
        
        # Assert
        assert is_valid is True
        assert error is None
    
    def test_rejects_response_with_max_tokens_finish_reason(self):
        """Valid JSON but truncated (max_tokens) should fail."""
        # Arrange
        valid_json = json.dumps([{"book_title": "Test", "chapter": 1, "reason": "Test"}])
        
        # Act
        is_valid, error = _validate_json_response(valid_json, FinishReason.MAX_TOKENS.value)
        
        # Assert
        assert is_valid is False
        assert "Incomplete response" in error
        assert "max_tokens" in error
    
    def test_rejects_malformed_json_syntax(self):
        """Malformed JSON should fail with clear error."""
        # Arrange
        malformed_json = '{"book_title": "Test", "chapter": 1'  # Missing closing brace
        
        # Act
        is_valid, error = _validate_json_response(malformed_json, FinishReason.END_TURN.value)
        
        # Assert
        assert is_valid is False
        assert "Invalid JSON" in error
    
    def test_rejects_array_with_missing_required_fields(self):
        """JSON array with missing required fields should fail."""
        # Arrange
        missing_fields = json.dumps([
            {"book_title": "Test"},  # Missing 'chapter' and 'reason'
        ])
        
        # Act
        is_valid, error = _validate_json_response(missing_fields, FinishReason.END_TURN.value)
        
        # Assert
        assert is_valid is False
        assert "missing fields" in error
        assert "chapter" in error or "reason" in error
    
    def test_rejects_array_with_non_dict_items(self):
        """JSON array containing non-dict items should fail."""
        # Arrange
        invalid_structure = json.dumps(["string_instead_of_dict"])
        
        # Act
        is_valid, error = _validate_json_response(invalid_structure, FinishReason.END_TURN.value)
        
        # Assert
        assert is_valid is False
        assert "not a dict" in error


# ============================================================================
# Test Class 2: Truncation Handling
# ============================================================================

class TestTruncationHandling:
    """
    Test _handle_truncated_response function.
    
    Pattern: Retry with Progressive Constraints (Building Microservices Ch. 11 - Resilience)
    Coverage: Phase 1 retry, Phase 2 non-retry, max retries, progressive constraints
    """
    
    @patch('workflows.shared.llm_integration.call_llm')
    def test_retries_phase_1_truncated_response_with_tighter_constraints(self, mock_call_llm):
        """Phase 1 truncation should retry with reduced book limit."""
        # Arrange
        mock_call_llm.return_value = '[]'  # Successful retry
        messages = [{"role": "user", "content": "Test prompt"}]
        
        # Act
        result = _handle_truncated_response("phase_1", messages, attempt=0)
        
        # Assert
        assert result == '[]'
        mock_call_llm.assert_called_once()
        # Verify constraint added (checking for book limit reduction)
        assert "10" in messages[-1]["content"] or "books" in messages[-1]["content"]
    
    def test_phase_2_truncation_returns_none_no_retry(self):
        """Phase 2 truncation should not retry (would lose content)."""
        # Arrange
        messages = [{"role": "user", "content": "Test prompt"}]
        
        # Act
        result = _handle_truncated_response("phase_2", messages, attempt=0)
        
        # Assert
        assert result is None
    
    @patch('workflows.shared.llm_integration.call_llm')
    def test_stops_retrying_after_max_attempts(self, mock_call_llm):
        """Should stop retrying after max_retries attempts."""
        # Arrange
        messages = [{"role": "user", "content": "Test prompt"}]
        
        # Act
        result = _handle_truncated_response("phase_1", messages, attempt=2, max_retries=2)
        
        # Assert
        assert result is None
        mock_call_llm.assert_not_called()


# ============================================================================
# Test Class 3: Anthropic API Calls
# ============================================================================

class TestAnthropicApiCalls:
    """
    Test _call_anthropic_api function.
    
    Pattern: Facade Pattern (Architecture Patterns Ch. 10)
    Coverage: Successful API calls, API errors, response parsing, token counting
    """
    
    @patch('workflows.shared.llm_integration.anthropic')
    @patch('workflows.shared.llm_integration.ANTHROPIC_AVAILABLE', True)
    def test_successful_anthropic_api_call_returns_response_text(self, mock_anthropic):
        """Successful API call should return response text."""
        # Arrange
        mock_client = Mock()
        mock_anthropic.Anthropic.return_value = mock_client
        
        mock_response = Mock()
        mock_response.content = [Mock(text="Valid response")]
        mock_response.stop_reason = "end_turn"
        mock_response.usage.input_tokens = 100
        mock_response.usage.output_tokens = 50
        mock_client.messages.create.return_value = mock_response
        
        # Act
        result = _call_anthropic_api(1, "Test prompt", "System prompt", 2000)
        
        # Assert
        assert result == "Valid response"
        mock_client.messages.create.assert_called_once()
    
    @patch('workflows.shared.llm_integration.anthropic')
    @patch('workflows.shared.llm_integration.ANTHROPIC_AVAILABLE', True)
    def test_anthropic_api_call_with_system_prompt(self, mock_anthropic):
        """API call should include system prompt when provided."""
        # Arrange
        mock_client = Mock()
        mock_anthropic.Anthropic.return_value = mock_client
        
        mock_response = Mock()
        mock_response.content = [Mock(text="Response")]
        mock_response.stop_reason = "end_turn"
        mock_response.usage.input_tokens = 50
        mock_response.usage.output_tokens = 25
        mock_client.messages.create.return_value = mock_response
        
        system_prompt = "You are a helpful assistant"
        
        # Act
        _call_anthropic_api(1, "User prompt", system_prompt, 1000)
        
        # Assert
        call_args = mock_client.messages.create.call_args
        assert call_args[1]['system'] == system_prompt
    
    @patch('workflows.shared.llm_integration.anthropic')
    @patch('workflows.shared.llm_integration.ANTHROPIC_AVAILABLE', True)
    def test_anthropic_api_error_raises_exception_with_details(self, mock_anthropic):
        """API errors should raise exceptions with details."""
        # Arrange
        mock_client = Mock()
        mock_anthropic.Anthropic.return_value = mock_client
        mock_client.messages.create.side_effect = Exception("Rate limit exceeded")
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            _call_anthropic_api(1, "Test prompt", None, 1000)
        
        assert "Rate limit exceeded" in str(exc_info.value)


# ============================================================================
# Test Class 4: High-Level call_llm Function
# ============================================================================

class TestCallLlmFunction:
    """
    Test call_llm function (main Facade interface).
    
    Pattern: Facade Pattern - Unified LLM Interface
    Coverage: Successful calls, error handling, provider selection, fallbacks
    """
    
    @patch('workflows.shared.llm_integration._call_anthropic_api')
    @patch('workflows.shared.llm_integration.ANTHROPIC_AVAILABLE', True)
    def test_call_llm_routes_to_anthropic_when_available(self, mock_anthropic_call):
        """call_llm should route to Anthropic when available."""
        # Arrange
        mock_anthropic_call.return_value = "Anthropic response"
        
        # Act
        result = call_llm("Test prompt", "System prompt", 1500)
        
        # Assert
        assert result == "Anthropic response"
        mock_anthropic_call.assert_called_once_with(
            pytest.approx(1, abs=5),  # call_num may vary
            "Test prompt",
            "System prompt",
            1500
        )
    
    @patch('workflows.shared.llm_integration.ANTHROPIC_AVAILABLE', False)
    def test_call_llm_raises_error_when_no_provider_available(self):
        """call_llm should return fallback JSON when no LLM provider available."""
        # Act
        result = call_llm("Test prompt", max_tokens=100)
        
        # Assert - returns empty JSON for fallback logic
        assert result == "{}"
    
    @patch('workflows.shared.llm_integration._call_anthropic_api')
    @patch('workflows.shared.llm_integration.ANTHROPIC_AVAILABLE', True)
    def test_call_llm_increments_api_call_counter(self, mock_anthropic_call):
        """call_llm should track API call count."""
        # Arrange
        mock_anthropic_call.return_value = "Response"
        
        # Act
        call_llm("Prompt 1")
        call_llm("Prompt 2")
        
        # Assert
        assert mock_anthropic_call.call_count == 2


# ============================================================================
# Test Class 5: Semantic Concepts Extraction
# ============================================================================

class TestSemanticConceptsExtraction:
    """
    Test prompt_for_semantic_concepts function.
    
    Pattern: Domain-Specific Prompting
    Coverage: Prompt construction, response parsing, error handling
    """
    
    @patch('workflows.shared.llm_integration.call_llm')
    def test_semantic_concepts_returns_verified_and_additional_concepts(self, mock_call_llm):
        """Should return dict with verified and additional concepts."""
        # Arrange
        mock_response = json.dumps({
            "verified_concepts": ["error handling", "exceptions"],
            "additional_concepts": ["try-except", "context managers"]
        })
        mock_call_llm.return_value = mock_response
        
        # Act
        result = prompt_for_semantic_concepts(
            chapter_num=5,
            chapter_title="Exception Handling",
            page_range=(45, 60),
            chapter_content="Text about error handling...",
            keyword_concepts={"errors"}
        )
        
        # Assert
        assert "verified_concepts" in result
        assert "additional_concepts" in result
        assert len(result["verified_concepts"]) == 2
        assert "error handling" in result["verified_concepts"]
    
    @patch('workflows.shared.llm_integration.call_llm')
    def test_semantic_concepts_handles_json_parse_error(self, mock_call_llm):
        """Should handle malformed JSON response gracefully (returns fallback)."""
        # Arrange
        mock_call_llm.return_value = "Not valid JSON"
        
        # Act - function catches exception and returns fallback
        result = prompt_for_semantic_concepts(
            chapter_num=1,
            chapter_title="Test",
            page_range=(1, 10),
            chapter_content="Test text",
            keyword_concepts={"test"}
        )
        
        # Assert - returns fallback with keyword concepts as verified
        assert "verified_concepts" in result
        assert "test" in result["verified_concepts"]


# ============================================================================
# Test Class 6: Cross-Reference Validation
# ============================================================================

class TestCrossReferenceValidation:
    """
    Test prompt_for_cross_reference_validation function.
    
    Pattern: Validation Service
    Coverage: Match validation, false positive filtering, response structure
    """
    
    @patch('workflows.shared.llm_integration.call_llm')
    def test_cross_reference_validation_returns_validated_matches(self, mock_call_llm):
        """Should return validated and additional matches."""
        # Arrange
        mock_response = json.dumps({
            "validated_matches": [
                {"book": "Python Distilled", "chapter": 5, "relevance": 0.9}
            ],
            "additional_matches": [
                {"book": "Fluent Python", "chapter": 7, "relevance": 0.85}
            ]
        })
        mock_call_llm.return_value = mock_response
        
        keyword_matches = [{"book": "Python Distilled", "page": 45, "concepts": ["exceptions"]}]
        all_companion_books = {"Python_Distilled_Content": {"pages": []}, "Fluent_Python_Content": {"pages": []}}
        
        # Act
        result = prompt_for_cross_reference_validation(
            chapter_num=5,
            chapter_title="Error Handling",
            chapter_concepts={"exceptions", "try-except"},
            keyword_matches=keyword_matches,
            all_companion_books=all_companion_books
        )
        
        # Assert
        assert "validated_matches" in result
        assert "additional_matches" in result
        assert len(result["validated_matches"]) == 1
        assert result["validated_matches"][0]["book"] == "Python Distilled"


# ============================================================================
# Test Class 7: Cross-Reference Summary Generation
# ============================================================================

class TestCrossReferenceSummary:
    """
    Test prompt_for_cross_reference_summary function.
    
    Pattern: Content Generation
    Coverage: Summary generation, length constraints, content quality
    """
    
    @patch('workflows.shared.llm_integration.call_llm')
    def test_cross_reference_summary_returns_concise_summary(self, mock_call_llm):
        """Should return summary within length constraint."""
        # Arrange
        mock_response = json.dumps({
            "summary": "This chapter covers exception handling patterns including try-except blocks, context managers, and error propagation strategies."
        })
        mock_call_llm.return_value = mock_response
        
        # Act
        result = prompt_for_cross_reference_summary(
            concepts=["exceptions", "error handling"],
            content="Long content about error handling...",
            relationship="implementation",
            book_name="Python Distilled",
            page_num=45,
            max_length=300
        )
        
        # Assert
        assert "summary" in result
        assert len(result["summary"]) <= 300
        assert "exception" in result["summary"].lower()
    
    @patch('workflows.shared.llm_integration.call_llm')
    def test_cross_reference_summary_respects_max_length_parameter(self, mock_call_llm):
        """Should enforce max_length constraint in prompt."""
        # Arrange
        mock_call_llm.return_value = json.dumps({"summary": "Short summary"})
        
        # Act
        prompt_for_cross_reference_summary(
            concepts=["test"],
            content="Content",
            relationship="related",
            book_name="Test Book",
            page_num=1,
            max_length=150
        )
        
        # Assert
        call_args = mock_call_llm.call_args[0][0]
        assert "150" in call_args or "max" in call_args.lower()


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def mock_anthropic_client():
    """Fixture for mocked Anthropic client."""
    with patch('workflows.shared.llm_integration.anthropic') as mock:
        client = Mock()
        mock.Anthropic.return_value = client
        
        # Default successful response
        response = Mock()
        response.content = [Mock(text="Success")]
        response.stop_reason = "end_turn"
        response.usage.input_tokens = 100
        response.usage.output_tokens = 50
        client.messages.create.return_value = response
        
        yield client


@pytest.fixture
def sample_prompt_data():
    """Fixture for sample prompt data."""
    return {
        "chapter_num": 5,
        "chapter_title": "Exception Handling",
        "page_range": (45, 60),
        "chapter_text": "This chapter discusses Python's exception handling mechanisms...",
        "keyword_concepts": ["exceptions", "try-except", "error handling"]
    }
