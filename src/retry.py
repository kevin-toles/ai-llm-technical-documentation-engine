"""
Retry logic wrapper for LLM calls with exponential backoff.

Handles transient failures with configurable retry attempts,
backoff strategies, and progressive constraint tightening.
"""

import time
import logging
from typing import Optional, Callable, TypeVar, Any
from dataclasses import dataclass

from .providers.base import LLMProvider, LLMResponse, LLMError


logger = logging.getLogger(__name__)

T = TypeVar('T')


@dataclass
class RetryConfig:
    """Configuration for retry behavior."""
    max_attempts: int = 3
    backoff_factor: float = 2.0
    initial_delay: float = 1.0
    max_delay: float = 60.0
    constraint_tightening_factor: float = 0.8
    
    def get_delay(self, attempt: int) -> float:
        """
        Calculate delay for a given attempt using exponential backoff.
        
        Args:
            attempt: Attempt number (0-indexed)
            
        Returns:
            Delay in seconds, capped at max_delay
        """
        delay = self.initial_delay * (self.backoff_factor ** attempt)
        return min(delay, self.max_delay)
    
    def get_adjusted_max_tokens(self, original: int, attempt: int) -> int:
        """
        Calculate adjusted max_tokens for retry attempts.
        
        Progressive constraint tightening: reduce max_tokens on each retry
        to encourage more concise responses that might parse better.
        
        Args:
            original: Original max_tokens value
            attempt: Attempt number (0-indexed)
            
        Returns:
            Adjusted max_tokens value (minimum 100)
        """
        if attempt == 0:
            return original
        
        # Reduce by constraint_tightening_factor for each retry
        factor = self.constraint_tightening_factor ** attempt
        adjusted = int(original * factor)
        
        # Ensure minimum of 100 tokens
        return max(100, adjusted)


class RetryExhaustedError(Exception):
    """Raised when all retry attempts have been exhausted."""
    
    def __init__(self, attempts: int, last_error: Exception):
        self.attempts = attempts
        self.last_error = last_error
        super().__init__(
            f"Retry exhausted after {attempts} attempts. "
            f"Last error: {last_error}"
        )


def call_llm_with_retry(
    provider: LLMProvider,
    prompt: str,
    max_tokens: int,
    temperature: float = 0.0,
    system_prompt: Optional[str] = None,
    config: Optional[RetryConfig] = None,
    on_retry: Optional[Callable[[int, Exception, float], None]] = None,
) -> LLMResponse:
    """
    Call LLM provider with automatic retry logic.
    
    Implements exponential backoff and progressive constraint tightening
    on retry attempts. Retries on LLMError exceptions.
    
    Args:
        provider: LLM provider to use
        prompt: User prompt
        max_tokens: Maximum tokens to generate
        temperature: Sampling temperature
        system_prompt: Optional system prompt
        config: Retry configuration (uses defaults if not provided)
        on_retry: Optional callback called on retry (attempt, error, delay)
        
    Returns:
        LLMResponse from successful call
        
    Raises:
        RetryExhaustedError: If all retry attempts fail
        
    Example:
        >>> provider = AnthropicProvider(api_key="...")
        >>> config = RetryConfig(max_attempts=5, backoff_factor=2.0)
        >>> response = call_llm_with_retry(
        ...     provider=provider,
        ...     prompt="Summarize this text",
        ...     max_tokens=1000,
        ...     config=config,
        ... )
    """
    if config is None:
        config = RetryConfig()
    
    last_error: Optional[Exception] = None
    
    for attempt in range(config.max_attempts):
        try:
            # Adjust max_tokens for retry attempts
            adjusted_max_tokens = config.get_adjusted_max_tokens(max_tokens, attempt)
            
            if attempt > 0:
                logger.info(
                    f"Retry attempt {attempt + 1}/{config.max_attempts} "
                    f"(max_tokens adjusted: {max_tokens} -> {adjusted_max_tokens})"
                )
            
            # Make the LLM call
            response = provider.call(
                prompt=prompt,
                max_tokens=adjusted_max_tokens,
                temperature=temperature,
                system_prompt=system_prompt,
            )
            
            logger.info(
                f"LLM call successful (attempt {attempt + 1}, "
                f"tokens: {response.total_tokens})"
            )
            
            return response
            
        except LLMError as e:
            last_error = e
            
            # If this was the last attempt, raise
            if attempt >= config.max_attempts - 1:
                break
            
            # Calculate delay and wait
            delay = config.get_delay(attempt)
            
            logger.warning(
                f"LLM call failed (attempt {attempt + 1}/{config.max_attempts}): {e}. "
                f"Retrying in {delay:.1f}s..."
            )
            
            # Call retry callback if provided
            if on_retry:
                on_retry(attempt, e, delay)
            
            time.sleep(delay)
    
    # All attempts exhausted
    raise RetryExhaustedError(config.max_attempts, last_error)


def call_with_retry(
    func: Callable[..., T],
    config: Optional[RetryConfig] = None,
    on_retry: Optional[Callable[[int, Exception, float], None]] = None,
    retry_on: tuple[type[Exception], ...] = (Exception,),
) -> Callable[..., T]:
    """
    Generic retry decorator for any function.
    
    Args:
        func: Function to wrap with retry logic
        config: Retry configuration
        on_retry: Optional callback on retry
        retry_on: Tuple of exception types to retry on
        
    Returns:
        Wrapped function with retry logic
        
    Example:
        >>> @call_with_retry
        ... def unreliable_function():
        ...     # might fail sometimes
        ...     return result
    """
    if config is None:
        config = RetryConfig()
    
    def wrapper(*args: Any, **kwargs: Any) -> T:
        last_error: Optional[Exception] = None
        
        for attempt in range(config.max_attempts):
            try:
                return func(*args, **kwargs)
            except retry_on as e:
                last_error = e
                
                if attempt >= config.max_attempts - 1:
                    break
                
                delay = config.get_delay(attempt)
                
                func_name = getattr(func, '__name__', 'function')
                logger.warning(
                    f"Function {func_name} failed (attempt {attempt + 1}): {e}. "
                    f"Retrying in {delay:.1f}s..."
                )
                
                if on_retry:
                    on_retry(attempt, e, delay)
                
                time.sleep(delay)
        
        raise RetryExhaustedError(config.max_attempts, last_error)
    
    return wrapper
