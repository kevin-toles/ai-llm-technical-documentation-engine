"""
Configuration module for LLM Document Enhancer.

Provides type-safe, validated configuration using dataclasses + environment variables.
"""

from .settings import settings, Settings, LLMConfig, CacheConfig, PromptConstraints

__all__ = [
    'settings',
    'Settings',
    'LLMConfig',
    'CacheConfig',
    'PromptConstraints',
]
