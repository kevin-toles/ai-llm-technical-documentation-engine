"""
Tests for retry logic.
"""

import pytest
import time
from unittest.mock import Mock, patch

from src.retry import (
    RetryConfig,
    call_llm_with_retry,
    call_with_retry,
    RetryExhaustedError,
)
from src.providers.base import LLMError, LLMResponse


class TestRetryConfig:
    """Tests for RetryConfig."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = RetryConfig()
        
        assert config.max_attempts == 3
        assert config.backoff_factor == pytest.approx(2.0)
        assert config.initial_delay == pytest.approx(1.0)
        assert config.max_delay == pytest.approx(60.0)
        assert config.constraint_tightening_factor == pytest.approx(0.8)
    
    def test_custom_config(self):
        """Test creating custom configuration."""
        config = RetryConfig(
            max_attempts=5,
            backoff_factor=3.0,
            initial_delay=0.5,
        )
        
        assert config.max_attempts == 5
        assert config.backoff_factor == pytest.approx(3.0)
        assert config.initial_delay == pytest.approx(0.5)
    
    def test_get_delay_exponential_backoff(self):
        """Test exponential backoff delay calculation."""
        config = RetryConfig(initial_delay=1.0, backoff_factor=2.0)
        
        assert config.get_delay(0) == pytest.approx(1.0)   # 1 * 2^0
        assert config.get_delay(1) == pytest.approx(2.0)   # 1 * 2^1
        assert config.get_delay(2) == pytest.approx(4.0)   # 1 * 2^2
        assert config.get_delay(3) == pytest.approx(8.0)   # 1 * 2^3
    
    def test_get_delay_max_cap(self):
        """Test that delay is capped at max_delay."""
        config = RetryConfig(initial_delay=10.0, backoff_factor=2.0, max_delay=15.0)
        
        assert config.get_delay(0) == pytest.approx(10.0)
        assert config.get_delay(1) == pytest.approx(15.0)  # Would be 20, capped at 15
        assert config.get_delay(2) == pytest.approx(15.0)  # Would be 40, capped at 15
    
    def test_get_adjusted_max_tokens_no_change_first_attempt(self):
        """Test that first attempt uses original max_tokens."""
        config = RetryConfig(constraint_tightening_factor=0.8)
        
        assert config.get_adjusted_max_tokens(1000, 0) == 1000
    
    def test_get_adjusted_max_tokens_progressive_tightening(self):
        """Test progressive constraint tightening on retries."""
        config = RetryConfig(constraint_tightening_factor=0.8)
        
        # Attempt 0: 1000 (original)
        assert config.get_adjusted_max_tokens(1000, 0) == 1000
        
        # Attempt 1: 1000 * 0.8 = 800
        assert config.get_adjusted_max_tokens(1000, 1) == 800
        
        # Attempt 2: 1000 * 0.8^2 = 640
        assert config.get_adjusted_max_tokens(1000, 2) == 640
        
        # Attempt 3: 1000 * 0.8^3 = 512
        assert config.get_adjusted_max_tokens(1000, 3) == 512
    
    def test_get_adjusted_max_tokens_minimum(self):
        """Test that adjusted tokens never go below 100."""
        config = RetryConfig(constraint_tightening_factor=0.1)
        
        # Even with aggressive tightening, minimum is 100
        assert config.get_adjusted_max_tokens(200, 5) >= 100


class TestCallLLMWithRetry:
    """Tests for call_llm_with_retry."""
    
    def test_successful_first_attempt(self):
        """Test successful call on first attempt."""
        mock_provider = Mock()
        mock_response = LLMResponse(
            content="Success",
            model="test-model",
            input_tokens=10,
            output_tokens=5,
        )
        mock_provider.call.return_value = mock_response
        
        result = call_llm_with_retry(
            provider=mock_provider,
            prompt="Test",
            max_tokens=100,
        )
        
        assert result == mock_response
        assert mock_provider.call.call_count == 1
    
    def test_retry_on_llm_error(self):
        """Test retry on LLMError."""
        mock_provider = Mock()
        mock_provider.call.side_effect = [
            LLMError("First attempt failed"),
            LLMResponse("Success", "model", 10, 5),
        ]
        
        config = RetryConfig(initial_delay=0.01)  # Fast retry for testing
        
        result = call_llm_with_retry(
            provider=mock_provider,
            prompt="Test",
            max_tokens=100,
            config=config,
        )
        
        assert result.content == "Success"
        assert mock_provider.call.call_count == 2
    
    def test_exhausted_retries(self):
        """Test RetryExhaustedError when all attempts fail."""
        mock_provider = Mock()
        mock_provider.call.side_effect = LLMError("Always fails")
        
        config = RetryConfig(max_attempts=3, initial_delay=0.01)
        
        with pytest.raises(RetryExhaustedError) as exc_info:
            call_llm_with_retry(
                provider=mock_provider,
                prompt="Test",
                max_tokens=100,
                config=config,
            )
        
        assert exc_info.value.attempts == 3
        assert "Always fails" in str(exc_info.value.last_error)
        assert mock_provider.call.call_count == 3
    
    def test_progressive_max_tokens_adjustment(self):
        """Test that max_tokens is adjusted on retry attempts."""
        mock_provider = Mock()
        mock_provider.call.side_effect = [
            LLMError("Fail 1"),
            LLMError("Fail 2"),
            LLMResponse("Success", "model", 10, 5),
        ]
        
        config = RetryConfig(
            max_attempts=3,
            initial_delay=0.01,
            constraint_tightening_factor=0.8,
        )
        
        call_llm_with_retry(
            provider=mock_provider,
            prompt="Test",
            max_tokens=1000,
            config=config,
        )
        
        # Check that max_tokens was adjusted for each attempt
        calls = mock_provider.call.call_args_list
        assert calls[0][1]['max_tokens'] == 1000  # Attempt 1: original
        assert calls[1][1]['max_tokens'] == 800   # Attempt 2: 1000 * 0.8
        assert calls[2][1]['max_tokens'] == 640   # Attempt 3: 1000 * 0.8^2
    
    def test_on_retry_callback(self):
        """Test that on_retry callback is called."""
        mock_provider = Mock()
        mock_provider.call.side_effect = [
            LLMError("Fail 1"),
            LLMResponse("Success", "model", 10, 5),
        ]
        
        retry_callback = Mock()
        config = RetryConfig(initial_delay=0.01)
        
        call_llm_with_retry(
            provider=mock_provider,
            prompt="Test",
            max_tokens=100,
            config=config,
            on_retry=retry_callback,
        )
        
        # Callback should be called once (for first failure)
        assert retry_callback.call_count == 1
        
        # Check callback arguments
        attempt, error, delay = retry_callback.call_args[0]
        assert attempt == 0
        assert isinstance(error, LLMError)
        assert delay > 0
    
    def test_system_prompt_passed_through(self):
        """Test that system_prompt is passed to provider."""
        mock_provider = Mock()
        mock_provider.call.return_value = LLMResponse("Success", "model", 10, 5)
        
        call_llm_with_retry(
            provider=mock_provider,
            prompt="Test",
            max_tokens=100,
            system_prompt="You are a helpful assistant.",
        )
        
        call_args = mock_provider.call.call_args[1]
        assert call_args['system_prompt'] == "You are a helpful assistant."
    
    def test_temperature_passed_through(self):
        """Test that temperature is passed to provider."""
        mock_provider = Mock()
        mock_provider.call.return_value = LLMResponse("Success", "model", 10, 5)
        
        call_llm_with_retry(
            provider=mock_provider,
            prompt="Test",
            max_tokens=100,
            temperature=0.7,
        )
        
        call_args = mock_provider.call.call_args[1]
        assert call_args['temperature'] == pytest.approx(0.7)


class TestCallWithRetry:
    """Tests for generic call_with_retry decorator."""
    
    def test_successful_call(self):
        """Test successful function call."""
        mock_func = Mock(return_value="success")
        
        wrapped = call_with_retry(mock_func)
        result = wrapped("arg1", kwarg1="value1")
        
        assert result == "success"
        assert mock_func.call_count == 1
        mock_func.assert_called_once_with("arg1", kwarg1="value1")
    
    def test_retry_on_exception(self):
        """Test retry on exception."""
        mock_func = Mock(side_effect=[
            ValueError("Fail 1"),
            ValueError("Fail 2"),
            "success",
        ])
        
        config = RetryConfig(initial_delay=0.01)
        wrapped = call_with_retry(
            mock_func,
            config=config,
            retry_on=(ValueError,),
        )
        
        result = wrapped()
        
        assert result == "success"
        assert mock_func.call_count == 3
    
    def test_exhausted_retries_generic(self):
        """Test RetryExhaustedError on generic function."""
        mock_func = Mock(side_effect=ValueError("Always fails"))
        
        config = RetryConfig(max_attempts=2, initial_delay=0.01)
        wrapped = call_with_retry(mock_func, config=config, retry_on=(ValueError,))
        
        with pytest.raises(RetryExhaustedError) as exc_info:
            wrapped()
        
        assert exc_info.value.attempts == 2
        assert mock_func.call_count == 2
    
    def test_no_retry_on_different_exception(self):
        """Test that function doesn't retry on non-specified exceptions."""
        mock_func = Mock(side_effect=RuntimeError("Different error"))
        
        wrapped = call_with_retry(mock_func, retry_on=(ValueError,))
        
        # Should raise immediately without retry
        with pytest.raises(RuntimeError):
            wrapped()
        
        assert mock_func.call_count == 1


class TestRetryExhaustedError:
    """Tests for RetryExhaustedError."""
    
    def test_error_attributes(self):
        """Test error has correct attributes."""
        original_error = ValueError("Original")
        error = RetryExhaustedError(5, original_error)
        
        assert error.attempts == 5
        assert error.last_error == original_error
        assert "5 attempts" in str(error)
        assert "Original" in str(error)
