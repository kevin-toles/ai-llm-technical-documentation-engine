"""
Factory for creating LLM provider instances.

Reference:
    Architecture Patterns with Python Ch. 13 - Factory pattern for dependency injection
    Microservices Up and Running Ch. 7 - 12-Factor App configuration
"""

import os
from .base import LLMProvider
from .anthropic_provider import AnthropicProvider


def create_llm_provider() -> LLMProvider:
    """
    Create LLM provider based on environment configuration.
    
    Uses the factory pattern to instantiate the appropriate LLM provider
    based on the LLM_PROVIDER environment variable. This decouples the
    application code from specific provider implementations.
    
    Returns:
        LLMProvider instance (default: AnthropicProvider)
    
    Environment Variables:
        LLM_PROVIDER: Provider name ("anthropic", "openai", etc.)
                     Default: "anthropic"
    
    Raises:
        ValueError: If unknown provider specified
    
    Example:
        >>> provider = create_llm_provider()
        >>> response = provider.call(
        ...     prompt="Explain dependency injection",
        ...     max_tokens=100
        ... )
    
    Reference:
        Architecture Patterns with Python Ch. 13 - Factory pattern simplifies DI
        Microservices Up and Running Ch. 7 - Environment-based configuration
    """
    provider_name = os.getenv("LLM_PROVIDER", "anthropic").lower()
    
    if provider_name == "anthropic":
        return AnthropicProvider()
    
    raise ValueError(
        f"Unknown LLM provider: {provider_name}. "
        f"Supported providers: anthropic"
    )
