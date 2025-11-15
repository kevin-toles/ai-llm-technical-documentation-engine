"""
LLM Provider abstraction layer.

Provides a clean interface for interacting with different LLM providers
(Anthropic, OpenAI, etc.) with consistent error handling and response formats.

Reference:
    Architecture Patterns with Python Ch. 13 - Dependency injection via providers
"""

from .base import LLMProvider, LLMResponse, LLMError
from .anthropic_provider import AnthropicProvider
from .factory import create_llm_provider

__all__ = [
    'LLMProvider',
    'LLMResponse',
    'LLMError',
    'AnthropicProvider',
    'create_llm_provider',
]
