"""
Configuration module for LLM Document Enhancer.

Provides type-safe, validated configuration using dataclasses + environment variables.
"""

from .settings import settings, Settings, LLMConfig, PromptConstraints

# CacheConfig removed (Task 5.2) - see DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md Part 2

__all__ = [
    'settings',
    'Settings',
    'LLMConfig',
    'PromptConstraints',
]
