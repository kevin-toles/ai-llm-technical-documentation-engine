"""
Factory for creating LLM provider instances.

Reference:
    Architecture Patterns with Python Ch. 13 - Factory pattern for dependency injection
    Microservices Up and Running Ch. 7 - 12-Factor App configuration
"""

import os
from .base import LLMProvider
from .anthropic_provider import AnthropicProvider
from .gateway_provider import GatewayProvider


# Supported provider names
SUPPORTED_PROVIDERS = ("anthropic", "gateway")


def create_llm_provider() -> LLMProvider:
    """
    Create LLM provider based on environment configuration.
    
    Uses the factory pattern to instantiate the appropriate LLM provider
    based on the LLM_PROVIDER environment variable. This decouples the
    application code from specific provider implementations.
    
    Returns:
        LLMProvider instance (default: AnthropicProvider)
    
    Environment Variables:
        LLM_PROVIDER: Provider name ("anthropic", "gateway", etc.)
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
    return get_provider(provider_name)


def get_provider(provider_name: str) -> LLMProvider:
    """
    Get LLM provider instance by name.
    
    Factory method that creates the appropriate provider based on name.
    
    Args:
        provider_name: Provider identifier ("anthropic", "gateway")
    
    Returns:
        LLMProvider instance
    
    Raises:
        ValueError: If unknown provider specified
    
    Reference:
        WBS 3.1.2.1 - Replace Direct LLM Calls
    """
    name = provider_name.lower()
    
    if name == "anthropic":
        return AnthropicProvider()
    
    if name == "gateway":
        return GatewayProvider()
    
    raise ValueError(
        f"Unknown LLM provider: {provider_name}. "
        f"Supported providers: {', '.join(SUPPORTED_PROVIDERS)}"
    )
