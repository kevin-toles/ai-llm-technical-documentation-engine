"""
Cache Module - WBS 6.1.2 Result Caching

In-memory cache with TTL for search results.

Reference Documents:
- WBS_IMPLEMENTATION.md: Phase 6.1.2 - Result caching for 5 mins
- GUIDELINES p. 2145: Caching patterns for performance
- CODING_PATTERNS §2.3: Cache expiration strategies

Anti-Patterns Avoided:
- §4.4: Simple in-memory cache (no external dependency for MVP)
- §7: Clear TTL handling with thread-safe operations

Usage:
    cache = ResultCache(ttl_seconds=300)
    cache.set("key", {"data": "value"})
    result = cache.get("key")  # Returns None if expired
"""

import threading
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional


# =============================================================================
# Constants
# =============================================================================

DEFAULT_TTL_SECONDS = 300  # 5 minutes


# =============================================================================
# GPU Detection - WBS 6.1.4
# =============================================================================


def is_gpu_available() -> bool:
    """
    Check if GPU (CUDA or MPS) is available.

    Reference: WBS 6.1.4 - GPU optimization

    Returns:
        True if GPU is available, False otherwise.
    """
    try:
        import torch
        return torch.cuda.is_available() or (
            hasattr(torch.backends, "mps") and torch.backends.mps.is_available()
        )
    except ImportError:
        return False


def get_device() -> str:
    """
    Get the best available compute device.

    Reference: WBS 6.1.4 - GPU optimization

    Returns:
        Device string: 'cuda', 'mps', or 'cpu'
    """
    try:
        import torch
        if torch.cuda.is_available():
            return "cuda"
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return "mps"
        return "cpu"
    except ImportError:
        return "cpu"


# =============================================================================
# Cache Key Generation
# =============================================================================


def generate_cache_key(
    query: str,
    domain: Optional[str] = None,
    top_k: int = 5,
    threshold: float = 0.3,
) -> str:
    """
    Generate a consistent cache key from query parameters.

    Reference: WBS 6.1.2 - Result caching

    Args:
        query: Search query text
        domain: Optional domain filter
        top_k: Number of results
        threshold: Similarity threshold

    Returns:
        Cache key string
    """
    key_parts = [
        "search",
        query,
        str(domain or ""),
        str(top_k),
        str(threshold),
    ]
    return ":".join(key_parts)


# =============================================================================
# Cache Entry
# =============================================================================


@dataclass
class CacheEntry:
    """
    Cache entry with value and expiration time.

    Attributes:
        value: Cached data
        expires_at: Unix timestamp when entry expires
    """

    value: Any
    expires_at: float

    def is_expired(self) -> bool:
        """Check if entry has expired."""
        return time.time() > self.expires_at


# =============================================================================
# ResultCache - WBS 6.1.2
# =============================================================================


class ResultCache:
    """
    Thread-safe in-memory cache with TTL support.

    Reference: WBS 6.1.2 - Cache search results for 5 mins

    Attributes:
        ttl_seconds: Time-to-live for cache entries (default 300s)

    Example:
        cache = ResultCache(ttl_seconds=300)
        cache.set("key", {"results": [...]})
        data = cache.get("key")  # Returns None if expired
    """

    def __init__(self, ttl_seconds: int = DEFAULT_TTL_SECONDS) -> None:
        """
        Initialize cache with TTL.

        Args:
            ttl_seconds: Time-to-live for entries in seconds. Default 300 (5 min).
        """
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, CacheEntry] = {}
        self._lock = threading.RLock()

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache if not expired.

        Args:
            key: Cache key

        Returns:
            Cached value or None if missing/expired
        """
        with self._lock:
            entry = self._cache.get(key)
            if entry is None:
                return None
            if entry.is_expired():
                del self._cache[key]
                return None
            return entry.value

    def set(self, key: str, value: Any) -> None:
        """
        Store value in cache with TTL.

        Args:
            key: Cache key
            value: Value to cache
        """
        expires_at = time.time() + self.ttl_seconds
        with self._lock:
            self._cache[key] = CacheEntry(value=value, expires_at=expires_at)

    def delete(self, key: str) -> bool:
        """
        Delete entry from cache.

        Args:
            key: Cache key

        Returns:
            True if entry was deleted, False if not found
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def clear(self) -> None:
        """Clear all cache entries."""
        with self._lock:
            self._cache.clear()

    def size(self) -> int:
        """Get number of entries in cache (including expired)."""
        with self._lock:
            return len(self._cache)

    def cleanup_expired(self) -> int:
        """
        Remove all expired entries.

        Returns:
            Number of entries removed
        """
        removed = 0
        with self._lock:
            expired_keys = [
                key for key, entry in self._cache.items()
                if entry.is_expired()
            ]
            for key in expired_keys:
                del self._cache[key]
                removed += 1
        return removed
