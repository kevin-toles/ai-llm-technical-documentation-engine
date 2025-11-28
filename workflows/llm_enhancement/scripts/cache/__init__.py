"""
Cache implementations for LLM Enhancement workflows.

Implements Repository Pattern for dual cache system:
1. PrefilterCacheRepository: Statistical pre-filter cache (7-day TTL)
2. LLMCacheRepository: LLM response cache (30-day TTL)

Pattern References:
- Architecture Patterns with Python Ch. 2 (Repository Pattern)
- Python Architecture Patterns Ch. 3, pg. 99 (Cache systems)
- Learning Python Ed6 Ch. 28-31 (Dataclass patterns)
"""

from workflows.llm_enhancement.scripts.cache.prefilter_cache import (
    PrefilterCacheRepository,
    CacheEntry,
    StatisticalPrefilterOutput,
)
from workflows.llm_enhancement.scripts.cache.llm_cache import (
    LLMCacheRepository,
    LLMResponse,
)

__all__ = [
    "PrefilterCacheRepository",
    "CacheEntry",
    "StatisticalPrefilterOutput",
    "LLMCacheRepository",
    "LLMResponse",
]
