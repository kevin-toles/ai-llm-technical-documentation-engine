"""
Comprehensive tests for workflows/shared/retry.py

Tests the Retry Pattern with Exponential Backoff implementation.

Architecture Pattern: Retry Pattern + Exponential Backoff (Building Microservices Ch. 11)
- Exponential backoff for progressive delay (1s, 2s, 4s, 8s...)
- Progressive constraint tightening (reduce max_tokens on retries)
- Configurable retry attempts with max delay cap
- Exception filtering (retry only on specific errors)
- Decorator pattern for wrapping functions

Key Responsibilities:
- Retry failed LLM calls with exponential backoff
- Adjust max_tokens progressively on retries (constraint tightening)
- Track retry attempts and raise RetryExhaustedError when exhausted
- Generic retry decorator for any function

Test Coverage:
- Test exponential backoff timing
- Test retry exhaustion
- Test successful retry scenarios
- Test constraint tightening (max_tokens adjustment)
- Test exception filtering
- Test retry callbacks
"""

import pytest
import time
from unittest.mock import Mock, patch, call
from workflows.shared.retry import (
    RetryConfig,
    RetryExhaustedError,
    call_llm_with_retry,
    call_with_retry,
)
from workflows.shared.providers.base import LLMProvider, LLMResponse, LLMError


@pytest.fixture
def mock_provider():
    """Create mock LLM provider."""
    provider = Mock(spec=LLMProvider)
    return provider


@pytest.fixture
def mock_response():
    """Create mock LLM response."""
    return LLMResponse(
        content="Test response",
        model="test-model",
        input_tokens=50,
        output_tokens=50,
        stop_reason="end_turn",
    )


@pytest.fixture
def retry_config():
    """Create retry configuration with fast timing for tests."""
    return RetryConfig(
        max_attempts=3,
        backoff_factor=2.0,
        initial_delay=0.1,  # Fast for testing
        max_delay=1.0,
        constraint_tightening_factor=0.8,
    )


class TestRetryConfig:
    """
    Test RetryConfig dataclass.
    
    Pattern: Configuration Object
    Coverage: Exponential backoff calculation, constraint tightening
    """
    
    def test_exponential_backoff_calculation(self):
        """Delay should increase exponentially with each attempt."""
        # Arrange
        config = RetryConfig(
            initial_delay=1.0,
            backoff_factor=2.0,
            max_delay=60.0
        )
        
        # Act & Assert
        assert math.isclose(config.get_delay(0), 1.0, abs_tol=1e-9)
        assert config.get_delay(1) == 2.0  # 1 * 2^1 = 2
        assert config.get_delay(2) == 4.0  # 1 * 2^2 = 4
        assert config.get_delay(3) == 8.0  # 1 * 2^3 = 8
    
    def test_backoff_respects_max_delay(self):
        """Delay should be capped at max_delay."""
        # Arrange
        config = RetryConfig(
            initial_delay=1.0,
            backoff_factor=2.0,
            max_delay=5.0
        )
        
        # Act
        delay_10 = config.get_delay(10)  # Would be 1024s without cap
        
        # Assert
        assert delay_10 == 5.0
    
    def test_constraint_tightening_reduces_max_tokens(self):
        """max_tokens should decrease on each retry attempt."""
        # Arrange
        config = RetryConfig(constraint_tightening_factor=0.8)
        original_tokens = 1000
        
        # Act & Assert
        assert config.get_adjusted_max_tokens(original_tokens, 0) == 1000  # No change on first attempt
        assert config.get_adjusted_max_tokens(original_tokens, 1) == 800   # 1000 * 0.8
        assert config.get_adjusted_max_tokens(original_tokens, 2) == 640   # 1000 * 0.8^2
    
    def test_constraint_tightening_enforces_minimum(self):
        """Adjusted max_tokens should never go below 100."""
        # Arrange
        config = RetryConfig(constraint_tightening_factor=0.1)
        original_tokens = 200
        
        # Act
        adjusted = config.get_adjusted_max_tokens(original_tokens, 5)  # Would be very small
        
        # Assert
        assert adjusted >= 100


class TestSuccessfulRetry:
    """
    Test successful retry scenarios.
    
    Pattern: Retry Pattern (Building Microservices Ch. 11)
    Coverage: Retry succeeds on 2nd attempt, retry succeeds on final attempt
    """
    
    def test_retry_succeeds_on_second_attempt(self, mock_provider, mock_response, retry_config):
        """LLM call should succeed on second attempt after first failure."""
        # Arrange
        mock_provider.call.side_effect = [
            LLMError("Rate limit"),  # First call fails
            mock_response,           # Second call succeeds
        ]
        
        # Act
        result = call_llm_with_retry(
            provider=mock_provider,
            prompt="Test prompt",
            max_tokens=1000,
            config=retry_config,
        )
        
        # Assert
        assert result == mock_response
        assert mock_provider.call.call_count == 2
    
    def test_retry_succeeds_on_final_attempt(self, mock_provider, mock_response, retry_config):
        """LLM call should succeed on final attempt."""
        # Arrange
        mock_provider.call.side_effect = [
            LLMError("Transient error 1"),
            LLMError("Transient error 2"),
            mock_response,  # Third (final) attempt succeeds
        ]
        
        # Act
        result = call_llm_with_retry(
            provider=mock_provider,
            prompt="Test prompt",
            max_tokens=1000,
            config=retry_config,
        )
        
        # Assert
        assert result == mock_response
        assert mock_provider.call.call_count == 3
    
    def test_no_retry_on_first_success(self, mock_provider, mock_response, retry_config):
        """No retry should occur if first call succeeds."""
        # Arrange
        mock_provider.call.return_value = mock_response
        
        # Act
        result = call_llm_with_retry(
            provider=mock_provider,
            prompt="Test prompt",
            max_tokens=1000,
            config=retry_config,
        )
        
        # Assert
        assert result == mock_response
        assert mock_provider.call.call_count == 1  # Only one call


class TestRetryExhaustion:
    """
    Test retry exhaustion scenarios.
    
    Pattern: Circuit Breaker (fail fast after max attempts)
    Coverage: Max retries reached, RetryExhaustedError raised
    """
    
    def test_retry_exhausted_raises_error(self, mock_provider, retry_config):
        """All retry attempts exhausted should raise RetryExhaustedError."""
        # Arrange
        error = LLMError("Persistent error")
        mock_provider.call.side_effect = error
        
        # Act & Assert
        with pytest.raises(RetryExhaustedError) as exc_info:
            call_llm_with_retry(
                provider=mock_provider,
                prompt="Test prompt",
                max_tokens=1000,
                config=retry_config,
            )
        
        # Verify error details
        assert exc_info.value.attempts == 3
        assert exc_info.value.last_error == error
        assert mock_provider.call.call_count == 3
    
    def test_retry_exhausted_error_message(self, mock_provider, retry_config):
        """RetryExhaustedError should contain helpful message."""
        # Arrange
        mock_provider.call.side_effect = LLMError("Test error")
        
        # Act & Assert
        with pytest.raises(RetryExhaustedError) as exc_info:
            call_llm_with_retry(
                provider=mock_provider,
                prompt="Test prompt",
                max_tokens=1000,
                config=retry_config,
            )
        
        error_msg = str(exc_info.value)
        assert "3 attempts" in error_msg
        assert "Test error" in error_msg


class TestExponentialBackoffTiming:
    """
    Test exponential backoff timing implementation.
    
    Pattern: Exponential Backoff (Building Microservices Ch. 11)
    Coverage: Backoff timing verified, delays increase exponentially
    """
    
    def test_exponential_backoff_delays_verified(self, mock_provider, retry_config):
        """Verify exponential backoff delays are actually applied."""
        # Arrange
        mock_provider.call.side_effect = LLMError("Always fails")
        start_time = time.time()
        
        # Act
        try:
            call_llm_with_retry(
                provider=mock_provider,
                prompt="Test prompt",
                max_tokens=1000,
                config=retry_config,
            )
        except RetryExhaustedError:
            pass
        
        elapsed = time.time() - start_time
        
        # Assert - should have delays of 0.1s and 0.2s (2 delays for 3 attempts)
        # Total expected: ~0.3s + overhead
        assert 0.25 < elapsed < 0.5, f"Expected ~0.3s, got {elapsed:.3f}s"
    
    def test_retry_callback_receives_correct_delays(self, mock_provider, retry_config):
        """Retry callback should receive exponentially increasing delays."""
        # Arrange
        mock_provider.call.side_effect = LLMError("Always fails")
        callback = Mock()
        
        # Act
        try:
            call_llm_with_retry(
                provider=mock_provider,
                prompt="Test prompt",
                max_tokens=1000,
                config=retry_config,
                on_retry=callback,
            )
        except RetryExhaustedError:
            pass
        
        # Assert - callback called twice (for 2 retries after first failure)
        assert callback.call_count == 2
        
        # First retry: attempt=0, delay=0.1
        first_call = callback.call_args_list[0]
        assert first_call[0][0] == 0  # attempt
        assert first_call[0][2] == 0.1  # delay
        
        # Second retry: attempt=1, delay=0.2
        second_call = callback.call_args_list[1]
        assert second_call[0][0] == 1  # attempt
        assert second_call[0][2] == 0.2  # delay


class TestConstraintTightening:
    """
    Test progressive constraint tightening on retries.
    
    Pattern: Adaptive Retry Strategy
    Coverage: max_tokens adjustment on retries
    """
    
    def test_max_tokens_reduced_on_retry(self, mock_provider, mock_response, retry_config):
        """max_tokens should be progressively reduced on each retry."""
        # Arrange
        mock_provider.call.side_effect = [
            LLMError("First failure"),
            mock_response,
        ]
        
        # Act
        call_llm_with_retry(
            provider=mock_provider,
            prompt="Test prompt",
            max_tokens=1000,
            config=retry_config,
        )
        
        # Assert
        calls = mock_provider.call.call_args_list
        
        # First call: original max_tokens
        assert calls[0][1]["max_tokens"] == 1000
        
        # Second call: reduced by constraint_tightening_factor (0.8)
        assert calls[1][1]["max_tokens"] == 800
    
    def test_constraint_tightening_all_attempts(self, mock_provider, retry_config):
        """Verify constraint tightening across all retry attempts."""
        # Arrange
        mock_provider.call.side_effect = LLMError("Always fails")
        
        # Act
        try:
            call_llm_with_retry(
                provider=mock_provider,
                prompt="Test prompt",
                max_tokens=1000,
                config=retry_config,
            )
        except RetryExhaustedError:
            pass
        
        # Assert - check max_tokens for all 3 attempts
        calls = mock_provider.call.call_args_list
        assert calls[0][1]["max_tokens"] == 1000  # Attempt 1: original
        assert calls[1][1]["max_tokens"] == 800   # Attempt 2: 1000 * 0.8
        assert calls[2][1]["max_tokens"] == 640   # Attempt 3: 1000 * 0.8^2


class TestGenericRetryDecorator:
    """
    Test generic retry decorator for any function.
    
    Pattern: Decorator Pattern (Python Distilled Ch. 7)
    Coverage: Generic function retry, exception filtering
    """
    
    def test_generic_retry_succeeds_on_second_attempt(self, retry_config):
        """Generic retry should succeed on second attempt."""
        # Arrange
        mock_func = Mock(side_effect=[
            ValueError("First failure"),
            "Success",
        ])
        
        wrapped = call_with_retry(
            mock_func,
            config=retry_config,
            retry_on=(ValueError,),
        )
        
        # Act
        result = wrapped()
        
        # Assert
        assert result == "Success"
        assert mock_func.call_count == 2
    
    def test_generic_retry_does_not_retry_other_exceptions(self, retry_config):
        """Should not retry exceptions not in retry_on tuple."""
        # Arrange
        mock_func = Mock(side_effect=TypeError("Not retryable"))
        
        wrapped = call_with_retry(
            mock_func,
            config=retry_config,
            retry_on=(ValueError,),  # Only retry ValueError
        )
        
        # Act & Assert
        with pytest.raises(TypeError):
            wrapped()
        
        # Should fail immediately, no retry
        assert mock_func.call_count == 1
    
    def test_generic_retry_exhaustion_raises_error(self, retry_config):
        """Generic retry should raise RetryExhaustedError when exhausted."""
        # Arrange
        mock_func = Mock(side_effect=ValueError("Always fails"))
        
        wrapped = call_with_retry(
            mock_func,
            config=retry_config,
            retry_on=(ValueError,),
        )
        
        # Act & Assert
        with pytest.raises(RetryExhaustedError) as exc_info:
            wrapped()
        
        assert exc_info.value.attempts == 3
        assert mock_func.call_count == 3


class TestRetryPatternCompliance:
    """
    Test Retry Pattern compliance (Building Microservices Ch. 11).
    
    Validates:
    - Exponential backoff with configurable base delay
    - Max attempts limit (circuit breaker)
    - Progressive constraint tightening
    - Exception filtering (transient vs permanent errors)
    - Observability (callbacks, logging)
    """
    
    def test_retry_pattern_exponential_backoff(self):
        """
        Validate exponential backoff implementation.
        
        Pattern: Delays should increase exponentially (1s, 2s, 4s, 8s...)
        """
        # Arrange
        config = RetryConfig(
            initial_delay=1.0,
            backoff_factor=2.0,
            max_delay=60.0
        )
        
        # Act & Assert - verify exponential growth
        delays = [config.get_delay(i) for i in range(5)]
        assert delays == [1.0, 2.0, 4.0, 8.0, 16.0]
    
    def test_retry_pattern_max_attempts_circuit_breaker(self, mock_provider, retry_config):
        """
        Validate circuit breaker (fail fast after max attempts).
        
        Pattern: Stop retrying after max_attempts to prevent infinite loops
        """
        # Arrange
        mock_provider.call.side_effect = LLMError("Always fails")
        
        # Act & Assert
        with pytest.raises(RetryExhaustedError):
            call_llm_with_retry(
                provider=mock_provider,
                prompt="Test",
                max_tokens=1000,
                config=retry_config,
            )
        
        # Verify circuit breaker triggered
        assert mock_provider.call.call_count == retry_config.max_attempts
    
    def test_retry_pattern_progressive_constraint_tightening(self):
        """
        Validate progressive constraint tightening.
        
        Pattern: Reduce resource demands on retries (adaptive retry)
        """
        # Arrange
        config = RetryConfig(constraint_tightening_factor=0.8)
        
        # Act - simulate multiple retry attempts
        tokens = [config.get_adjusted_max_tokens(1000, i) for i in range(4)]
        
        # Assert - should decrease progressively
        assert tokens[0] == 1000  # Original
        assert tokens[1] == 800   # 80% of original
        assert tokens[2] == 640   # 80% of previous
        assert tokens[3] == 512   # 80% of previous
        assert tokens[3] < tokens[2] < tokens[1] < tokens[0]
    
    def test_retry_pattern_observability_via_callbacks(self, mock_provider, retry_config):
        """
        Validate observability through retry callbacks.
        
        Pattern: Callbacks provide visibility into retry behavior
        """
        # Arrange
        mock_provider.call.side_effect = [
            LLMError("Error 1"),
            LLMError("Error 2"),
            LLMError("Error 3"),
        ]
        
        callback = Mock()
        
        # Act
        try:
            call_llm_with_retry(
                provider=mock_provider,
                prompt="Test",
                max_tokens=1000,
                config=retry_config,
                on_retry=callback,
            )
        except RetryExhaustedError:
            pass
        
        # Assert - callback provides observability
        assert callback.call_count == 2  # Called on each retry (not on final failure)
        
        # Verify callback receives: attempt, error, delay
        for i, call_args in enumerate(callback.call_args_list):
            assert call_args[0][0] == i  # attempt number
            assert isinstance(call_args[0][1], LLMError)  # error object
            assert call_args[0][2] > 0  # delay value
    
    def test_retry_pattern_idempotency_safe(self, mock_provider, mock_response, retry_config):
        """
        Validate retry is safe for idempotent operations.
        
        Pattern: Retries should not cause duplicate side effects
        (LLM calls are naturally idempotent)
        """
        # Arrange
        mock_provider.call.side_effect = [
            LLMError("Transient failure"),
            mock_response,
        ]
        
        # Act
        result1 = call_llm_with_retry(
            provider=mock_provider,
            prompt="Test prompt",
            max_tokens=1000,
            config=retry_config,
        )
        
        # Reset and call again
        mock_provider.call.reset_mock()
        mock_provider.call.side_effect = [mock_response]
        
        result2 = call_llm_with_retry(
            provider=mock_provider,
            prompt="Test prompt",  # Same prompt
            max_tokens=1000,
            config=retry_config,
        )
        
        # Assert - same input produces same output (idempotent)
        assert result1.content == result2.content
