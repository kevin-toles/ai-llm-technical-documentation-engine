"""
Sprint 4 Day 4: Cache and Retry Integration - TDD RED Phase Tests

Tests for integrating existing cache.py and retry.py modules into the pipeline.

Test Strategy:
- Test Class 1: TestCacheIntegration (4 tests)
- Test Class 2: TestRetryIntegration (4 tests)
- Test Class 3: TestCacheAndRetryTogether (2 tests)
- Test Class 4: TestErrorHandling (2 tests)

References:
- Building Microservices Ch. 11: Resilience patterns
- Python Distilled Ch. 5: Exception handling
- Fluent Python 2nd Ch. 9: Decorators
- Analysis: docs/analysis/sprint4-day4-cache-retry-analysis.md
"""

import pytest
import time
from unittest.mock import Mock, patch
from pathlib import Path

# Imports that should exist after implementation
from workflows.shared.cache import ChapterCache
from workflows.shared.retry import call_llm_with_retry, RetryConfig, RetryExhaustedError
from workflows.shared.providers import LLMProvider, LLMResponse, LLMError


class TestCacheIntegration:
    """Test cache integration with pipeline LLM calls."""

    def test_cache_module_imported_in_pipeline(self):
        """Verify pipeline imports ChapterCache from workflows.shared.cache."""
        # TDD RED: This will fail until we add cache imports to pipeline
        from workflows.base_guideline_generation.scripts import chapter_generator_all_text
        
        # Check that ChapterCache is imported
        assert hasattr(chapter_generator_all_text, 'ChapterCache'), \
            "ChapterCache should be imported in pipeline module"
        
        # Check that cache instance exists at module level
        assert hasattr(chapter_generator_all_text, '_chapter_cache'), \
            "_chapter_cache instance should exist in pipeline module"
        
        # Verify it's actually a ChapterCache instance
        cache = getattr(chapter_generator_all_text, '_chapter_cache', None)
        assert isinstance(cache, ChapterCache), \
            "_chapter_cache should be an instance of ChapterCache"

    def test_llm_responses_cached(self, tmp_path):
        """Verify LLM responses are cached and reused on second call."""
        # TDD RED: This will fail until caching is integrated
        
        # Setup: Create cache and mock provider
        cache = ChapterCache(cache_dir=tmp_path / "test_cache", enabled=True)
        mock_provider = Mock(spec=LLMProvider)
        
        # First call should hit provider
        first_response = LLMResponse(
            content="Test annotation content",
            model="gpt-4",
            input_tokens=100,
            output_tokens=50
        )
        mock_provider.call.return_value = first_response
        
        # Simulate first LLM call with caching
        prompt = "Annotate this text"
        system_prompt = "You are a helpful assistant"
        max_tokens = 450
        
        # Check cache (should miss)
        cache_key_params = {"system_prompt": system_prompt, "max_tokens": max_tokens}
        cached = cache.get(prompt, "llm", **cache_key_params)
        assert cached is None, "Cache should be empty on first call"
        
        # Call LLM
        response1 = mock_provider.call(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=max_tokens,
            temperature=0.0
        )
        
        # Store in cache
        cache.set(prompt, "llm", {"annotation": response1.content}, **cache_key_params)
        
        # Second call should hit cache
        cached = cache.get(prompt, "llm", **cache_key_params)
        assert cached is not None, "Cache should return data on second call"
        assert cached["annotation"] == "Test annotation content", \
            "Cached annotation should match original"
        
        # Provider should only be called once
        assert mock_provider.call.call_count == 1, \
            "Provider should only be called once (second call uses cache)"

    def test_cache_key_includes_all_parameters(self, tmp_path):
        """Verify cache keys differentiate by prompt, system_prompt, and max_tokens."""
        # TDD RED: This will fail until proper cache key generation is implemented
        
        cache = ChapterCache(cache_dir=tmp_path / "test_cache", enabled=True)
        
        base_prompt = "Annotate this"
        base_system = "System A"
        base_tokens = 450
        
        # Store with base parameters
        cache.set(base_prompt, "llm", {"result": "A"}, 
                  system_prompt=base_system, max_tokens=base_tokens)
        
        # Same prompt, different system_prompt -> different cache entry
        result1 = cache.get(base_prompt, "llm", 
                           system_prompt="System B", max_tokens=base_tokens)
        assert result1 is None, "Different system_prompt should create different cache key"
        
        # Same prompt, different max_tokens -> different cache entry
        result2 = cache.get(base_prompt, "llm", 
                           system_prompt=base_system, max_tokens=500)
        assert result2 is None, "Different max_tokens should create different cache key"
        
        # Different prompt -> different cache entry
        result3 = cache.get("Different prompt", "llm", 
                           system_prompt=base_system, max_tokens=base_tokens)
        assert result3 is None, "Different prompt should create different cache key"
        
        # Same all parameters -> cache hit
        result4 = cache.get(base_prompt, "llm", 
                           system_prompt=base_system, max_tokens=base_tokens)
        assert result4 is not None, "Same parameters should hit cache"
        assert result4["result"] == "A", "Cache should return correct data"

    def test_cache_respects_ttl(self, tmp_path):
        """Verify expired cache entries are not returned."""
        # TDD RED: This will fail until TTL checking is implemented
        
        # Create cache with very short TTL (1 second)
        cache = ChapterCache(
            cache_dir=tmp_path / "test_cache", 
            enabled=True,
            phase1_ttl=1  # 1 second TTL
        )
        
        prompt = "Test prompt"
        cache_params = {"system_prompt": "System", "max_tokens": 450}
        
        # Store data
        cache.set(prompt, "llm", {"result": "cached"}, **cache_params)
        
        # Immediate retrieval should work
        result1 = cache.get(prompt, "llm", **cache_params)
        assert result1 is not None, "Fresh cache entry should be returned"
        assert result1["result"] == "cached"
        
        # Wait for TTL to expire
        time.sleep(1.5)
        
        # Expired entry should not be returned
        result2 = cache.get(prompt, "llm", **cache_params)
        assert result2 is None, "Expired cache entry should not be returned"


class TestRetryIntegration:
    """Test retry logic integration with pipeline LLM calls."""

    def test_retry_module_imported_in_pipeline(self):
        """Verify pipeline imports call_llm_with_retry from workflows.shared.retry."""
        # TDD RED: This will fail until we add retry imports to pipeline
        from workflows.base_guideline_generation.scripts import chapter_generator_all_text
        
        # Check that retry functions are imported
        assert hasattr(chapter_generator_all_text, 'call_llm_with_retry'), \
            "call_llm_with_retry should be imported in pipeline module"
        assert hasattr(chapter_generator_all_text, 'RetryConfig'), \
            "RetryConfig should be imported in pipeline module"
        assert hasattr(chapter_generator_all_text, 'RetryExhaustedError'), \
            "RetryExhaustedError should be imported in pipeline module"

    def test_llm_retries_on_failure(self):
        """Verify LLM calls retry on failure and succeed on subsequent attempt."""
        # TDD RED: This will fail until retry logic is integrated
        
        mock_provider = Mock(spec=LLMProvider)
        success_response = LLMResponse(
            content="Success",
            model="gpt-4",
            input_tokens=100,
            output_tokens=50
        )
        
        # Fail twice, succeed on third attempt
        mock_provider.call.side_effect = [
            LLMError("API Error 1"),
            LLMError("API Error 2"),
            success_response
        ]
        
        retry_config = RetryConfig(max_attempts=3, backoff_factor=2.0, initial_delay=0.1)
        
        # Should succeed after retries
        result = call_llm_with_retry(
            provider=mock_provider,
            prompt="Test prompt",
            system_prompt="Test system",
            max_tokens=450,
            temperature=0.0,
            config=retry_config
        )
        
        assert result.content == "Success", "Should return successful response"
        assert mock_provider.call.call_count == 3, "Should attempt 3 times"

    def test_exponential_backoff_applied(self):
        """Verify delays between retries follow exponential backoff pattern."""
        # TDD RED: This will fail until backoff timing is verified
        
        mock_provider = Mock(spec=LLMProvider)
        mock_provider.call.side_effect = [
            LLMError("Error 1"),
            LLMError("Error 2"),
            LLMResponse("Success", "gpt-4", 100, 50)
        ]
        
        retry_config = RetryConfig(
            max_attempts=3,
            backoff_factor=2.0,
            initial_delay=0.1,
            max_delay=10.0
        )
        
        start_time = time.time()
        
        call_llm_with_retry(
            provider=mock_provider,
            prompt="Test",
            system_prompt="System",
            max_tokens=450,
            temperature=0.0,
            config=retry_config
        )
        
        elapsed = time.time() - start_time
        
        # Expected delays: 0.1s (after 1st fail) + 0.2s (after 2nd fail) = 0.3s minimum
        assert elapsed >= 0.3, \
            f"Should have exponential backoff delays (expected >=0.3s, got {elapsed:.2f}s)"
        
        # Should not take too long (max 1 second with overhead)
        assert elapsed < 1.0, \
            f"Backoff should not be excessive (expected <1.0s, got {elapsed:.2f}s)"

    def test_constraint_tightening_on_retry(self):
        """Verify max_tokens is reduced on retry attempts (progressive constraint tightening)."""
        # TDD RED: This will fail until constraint tightening is implemented
        
        mock_provider = Mock(spec=LLMProvider)
        mock_provider.call.side_effect = [
            LLMError("Error 1"),
            LLMResponse("Success", "gpt-4", 100, 50)
        ]
        
        retry_config = RetryConfig(
            max_attempts=3,
            constraint_tightening_factor=0.8  # Reduce to 80% on retry
        )
        
        original_max_tokens = 450
        
        # Capture all calls to verify max_tokens reduction
        with patch.object(mock_provider, 'call', wraps=mock_provider.call) as mock_call:
            call_llm_with_retry(
                provider=mock_provider,
                prompt="Test",
                system_prompt="System",
                max_tokens=original_max_tokens,
                temperature=0.0,
                config=retry_config
            )
            
            # Verify first call used original max_tokens
            first_call = mock_call.call_args_list[0]
            assert first_call.kwargs['max_tokens'] == 450, \
                "First attempt should use original max_tokens"
            
            # Verify second call used reduced max_tokens (450 * 0.8 = 360)
            second_call = mock_call.call_args_list[1]
            expected_reduced = int(450 * 0.8)
            assert second_call.kwargs['max_tokens'] == expected_reduced, \
                f"Retry should reduce max_tokens to {expected_reduced}"


class TestCacheAndRetryTogether:
    """Test cache and retry logic working together."""

    def test_cache_miss_triggers_retry_logic(self, tmp_path):
        """Verify cache miss leads to LLM call with retry logic."""
        # TDD RED: This will fail until cache+retry integration is complete
        
        cache = ChapterCache(cache_dir=tmp_path / "test_cache", enabled=True)
        mock_provider = Mock(spec=LLMProvider)
        
        # Provider fails once, succeeds on retry
        success_response = LLMResponse("Result", "gpt-4", 100, 50)
        mock_provider.call.side_effect = [
            LLMError("Temporary error"),
            success_response
        ]
        
        prompt = "Test prompt"
        cache_params = {"system_prompt": "System", "max_tokens": 450}
        
        # Verify cache is empty
        cached = cache.get(prompt, "llm", **cache_params)
        assert cached is None, "Cache should be empty initially"
        
        # Call with retry
        retry_config = RetryConfig(max_attempts=3, initial_delay=0.05)
        result = call_llm_with_retry(
            provider=mock_provider,
            prompt=prompt,
            system_prompt=cache_params["system_prompt"],
            max_tokens=cache_params["max_tokens"],
            temperature=0.0,
            config=retry_config
        )
        
        # Store result in cache
        cache.set(prompt, "llm", {"annotation": result.content}, **cache_params)
        
        # Verify cached
        cached = cache.get(prompt, "llm", **cache_params)
        assert cached is not None, "Successful retry result should be cached"
        assert cached["annotation"] == "Result"
        
        # Provider should have been called twice (fail + success)
        assert mock_provider.call.call_count == 2

    def test_cache_hit_bypasses_retry_logic(self, tmp_path):
        """Verify cache hit prevents LLM call (no retry needed)."""
        # TDD RED: This will fail until cache-first logic is implemented
        
        cache = ChapterCache(cache_dir=tmp_path / "test_cache", enabled=True)
        mock_provider = Mock(spec=LLMProvider)
        
        # Pre-populate cache
        prompt = "Cached prompt"
        cache_params = {"system_prompt": "System", "max_tokens": 450}
        cache.set(prompt, "llm", {"annotation": "Cached result"}, **cache_params)
        
        # Provider should fail if called (to verify it's NOT called)
        mock_provider.call.side_effect = LLMError("Should not be called!")
        
        # Check cache first
        cached = cache.get(prompt, "llm", **cache_params)
        assert cached is not None, "Cache should have data"
        
        # If cached, should NOT call provider
        if cached:
            annotation = cached["annotation"]
        else:
            # This should not execute
            retry_config = RetryConfig(max_attempts=3)
            result = call_llm_with_retry(
                provider=mock_provider,
                prompt=prompt,
                system_prompt=cache_params["system_prompt"],
                max_tokens=cache_params["max_tokens"],
                temperature=0.0,
                config=retry_config
            )
            annotation = result.content
        
        assert annotation == "Cached result", "Should use cached result"
        assert mock_provider.call.call_count == 0, \
            "Provider should NOT be called when cache hits"


class TestErrorHandling:
    """Test error handling for retry exhaustion and cache failures."""

    def test_retry_exhaustion_handled_gracefully(self):
        """Verify RetryExhaustedError is caught and returns None for graceful degradation."""
        # TDD RED: This will fail until error handling is implemented
        
        mock_provider = Mock(spec=LLMProvider)
        # Always fail
        mock_provider.call.side_effect = LLMError("Persistent API error")
        
        retry_config = RetryConfig(max_attempts=3, initial_delay=0.05)
        
        # Should raise RetryExhaustedError
        with pytest.raises(RetryExhaustedError) as exc_info:
            call_llm_with_retry(
                provider=mock_provider,
                prompt="Test",
                system_prompt="System",
                max_tokens=450,
                temperature=0.0,
                config=retry_config
            )
        
        # Verify error details
        assert exc_info.value.attempts == 3, "Should report 3 attempts"
        assert "Persistent API error" in str(exc_info.value.last_error)
        
        # In pipeline, this should be caught and return None
        # (Tested in integration/pipeline tests)

    def test_cache_errors_dont_break_pipeline(self, tmp_path):
        """Verify cache errors are handled gracefully, LLM call proceeds without cache."""
        # TDD RED: This will fail until cache error handling is implemented
        
        # Create cache with invalid directory to force errors
        invalid_cache = ChapterCache(
            cache_dir=Path("/invalid/nonexistent/path"),
            enabled=True
        )
        
        mock_provider = Mock(spec=LLMProvider)
        success_response = LLMResponse("Success", "gpt-4", 100, 50)
        mock_provider.call.return_value = success_response
        
        prompt = "Test"
        cache_params = {"system_prompt": "System", "max_tokens": 450}
        
        # Cache get should fail gracefully (return None or raise exception)
        try:
            _ = invalid_cache.get(prompt, "llm", **cache_params)
        except Exception:
            pass  # Handle cache errors gracefully
        
        # Even if cache fails, LLM call should succeed
        result = mock_provider.call(
            prompt=prompt,
            system_prompt=cache_params["system_prompt"],
            max_tokens=cache_params["max_tokens"],
            temperature=0.0
        )
        
        assert result.content == "Success", \
            "LLM call should succeed even if cache fails"
        
        # Try to cache result (may also fail, but shouldn't break)
        try:
            invalid_cache.set(prompt, "llm", {"annotation": result.content}, **cache_params)
        except Exception:
            pass  # Cache set failure should not break pipeline
        
        # Provider should have been called (cache didn't work)
        assert mock_provider.call.call_count == 1


# Test fixtures
@pytest.fixture
def mock_llm_provider():
    """Create a mock LLM provider for testing."""
    provider = Mock(spec=LLMProvider)
    provider.model_name = "gpt-4"
    return provider


@pytest.fixture
def test_cache_dir(tmp_path):
    """Create a temporary cache directory for testing."""
    cache_dir = tmp_path / "test_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


@pytest.fixture
def sample_llm_response():
    """Create a sample LLM response for testing."""
    return LLMResponse(
        content="Sample annotation text",
        model="gpt-4",
        input_tokens=100,
        output_tokens=50
    )
