"""
LLM Provider Abstraction

Exports:
- LLMProvider: Protocol for LLM providers
- LLMResponse: Standardized response data structure
- LLMError: Base exception for provider errors
- AnthropicProvider: Anthropic Claude implementation
- create_llm_provider: Factory function for creating providers
"""

from shared.providers.base import LLMProvider, LLMResponse, LLMError
from shared.providers.anthropic_provider import AnthropicProvider
from shared.providers.factory import create_llm_provider

__all__ = [
    "LLMProvider",
    "LLMResponse", 
    "LLMError",
    "AnthropicProvider",
    "create_llm_provider",
]
