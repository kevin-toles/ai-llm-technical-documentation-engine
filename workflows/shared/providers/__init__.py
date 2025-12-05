"""
LLM Provider Abstraction

Exports:
- LLMProvider: Protocol for LLM providers
- LLMResponse: Standardized response data structure
- LLMError: Base exception for provider errors
- AnthropicProvider: Anthropic Claude implementation (direct SDK)
- GatewayProvider: LLM Gateway provider (via llm-gateway microservice)
- create_llm_provider: Factory function for creating providers
- get_provider: Factory function to get provider by name
"""

from workflows.shared.providers.base import LLMProvider, LLMResponse, LLMError
from workflows.shared.providers.anthropic_provider import AnthropicProvider
from workflows.shared.providers.gateway_provider import GatewayProvider
from workflows.shared.providers.factory import create_llm_provider, get_provider

__all__ = [
    "LLMProvider",
    "LLMResponse", 
    "LLMError",
    "AnthropicProvider",
    "GatewayProvider",
    "create_llm_provider",
    "get_provider",
]
