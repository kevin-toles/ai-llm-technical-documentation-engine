"""
Caching layer for LLM responses.

Provides disk-based caching of expensive LLM calls with TTL support,
allowing phase results to be persisted and reused across sessions.
"""

import json
import hashlib
import time
import logging
from pathlib import Path
from typing import Any, Dict, Optional, TypeVar
from dataclasses import dataclass, asdict


logger = logging.getLogger(__name__)

T = TypeVar('T')

# Constants
CACHE_FILE_EXTENSION = "*.json"


@dataclass
class CacheEntry:
    """A cached entry with metadata."""
    key: str
    data: Dict[str, Any]
    created_at: float  # Unix timestamp
    phase: str
    
    def is_expired(self, ttl_seconds: int) -> bool:
        """
        Check if this cache entry has expired.
        
        Args:
            ttl_seconds: Time-to-live in seconds
            
        Returns:
            True if expired, False otherwise
        """
        if ttl_seconds <= 0:
            return False  # Never expires
        
        age = time.time() - self.created_at
        return age > ttl_seconds
    
    def age_minutes(self) -> float:
        """Get age of entry in minutes."""
        return (time.time() - self.created_at) / 60
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CacheEntry':
        """Create from dictionary."""
        return cls(**data)


class ChapterCache:
    """
    Disk-based cache for LLM phase results.
    
    Stores results keyed by content hash, with separate TTLs
    for different phases and automatic expiration.
    """
    
    def __init__(
        self,
        cache_dir: Path,
        enabled: bool = True,
        phase1_ttl: int = 86400,  # 24 hours
        phase2_ttl: int = 86400,  # 24 hours
    ):
        """
        Initialize the cache.
        
        Args:
            cache_dir: Directory to store cache files
            enabled: Whether caching is enabled
            phase1_ttl: TTL for phase 1 results (seconds, 0 = no expiration)
            phase2_ttl: TTL for phase 2 results (seconds, 0 = no expiration)
        """
        self.cache_dir = Path(cache_dir)
        self.enabled = enabled
        self.phase1_ttl = phase1_ttl
        self.phase2_ttl = phase2_ttl
        
        # Create cache directory if needed
        if self.enabled:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Cache initialized at {self.cache_dir}")
    
    def _get_cache_key(self, content: str, phase: str, **kwargs: Any) -> str:
        """
        Generate a cache key from content and parameters.
        
        Args:
            content: Primary content to hash
            phase: Phase identifier
            **kwargs: Additional parameters to include in hash
            
        Returns:
            SHA256 hex digest as cache key
        """
        # Build a stable string representation
        key_parts = [content, phase]
        
        # Add sorted kwargs for stability
        for k in sorted(kwargs.keys()):
            key_parts.append(f"{k}={kwargs[k]}")
        
        key_str = "|".join(str(p) for p in key_parts)
        return hashlib.sha256(key_str.encode('utf-8')).hexdigest()
    
    def _get_cache_file(self, cache_key: str, phase: str) -> Path:
        """Get the cache file path for a given key and phase."""
        return self.cache_dir / f"{phase}_{cache_key}.json"
    
    def _get_ttl(self, phase: str) -> int:
        """Get TTL for a given phase."""
        if phase == "phase1":
            return self.phase1_ttl
        elif phase == "phase2":
            return self.phase2_ttl
        else:
            return 86400  # Default 24 hours
    
    def get(
        self,
        content: str,
        phase: str,
        **kwargs: Any
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached data if available and not expired.
        
        Args:
            content: Primary content to look up
            phase: Phase identifier
            **kwargs: Additional parameters for cache key
            
        Returns:
            Cached data if found and valid, None otherwise
        """
        if not self.enabled:
            return None
        
        cache_key = self._get_cache_key(content, phase, **kwargs)
        cache_file = self._get_cache_file(cache_key, phase)
        
        if not cache_file.exists():
            logger.debug(f"Cache miss: {phase} ({cache_key[:8]}...)")
            return None
        
        try:
            # Load cache entry
            with open(cache_file, 'r', encoding='utf-8') as f:
                entry_dict = json.load(f)
                entry = CacheEntry.from_dict(entry_dict)
            
            # Check expiration
            ttl = self._get_ttl(phase)
            if entry.is_expired(ttl):
                logger.debug(
                    f"Cache expired: {phase} ({cache_key[:8]}...) "
                    f"age={entry.age_minutes():.1f}min"
                )
                # Delete expired cache file
                cache_file.unlink(missing_ok=True)
                return None
            
            logger.info(
                f"Cache hit: {phase} ({cache_key[:8]}...) "
                f"age={entry.age_minutes():.1f}min"
            )
            return entry.data
            
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            logger.warning(f"Cache read error: {e}")
            # Delete corrupted cache file
            cache_file.unlink(missing_ok=True)
            return None
    
    def set(
        self,
        content: str,
        phase: str,
        data: Dict[str, Any],
        **kwargs: Any
    ) -> None:
        """
        Store data in cache.
        
        Args:
            content: Primary content key
            phase: Phase identifier
            data: Data to cache
            **kwargs: Additional parameters for cache key
        """
        if not self.enabled:
            return
        
        cache_key = self._get_cache_key(content, phase, **kwargs)
        cache_file = self._get_cache_file(cache_key, phase)
        
        # Create cache entry
        entry = CacheEntry(
            key=cache_key,
            data=data,
            created_at=time.time(),
            phase=phase,
        )
        
        try:
            # Write to disk
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(entry.to_dict(), f, indent=2)
            
            logger.info(f"Cached: {phase} ({cache_key[:8]}...)")
            
        except (OSError, TypeError) as e:
            logger.error(f"Cache write error: {e}")
    
    def clear_phase(self, phase: str) -> int:
        """
        Clear all cache entries for a specific phase.
        
        Args:
            phase: Phase identifier
            
        Returns:
            Number of entries cleared
        """
        if not self.enabled:
            return 0
        
        pattern = f"{phase}_*.json"
        files = list(self.cache_dir.glob(pattern))
        
        count = 0
        for file in files:
            try:
                file.unlink()
                count += 1
            except OSError:
                pass
        
        logger.info(f"Cleared {count} cache entries for {phase}")
        return count
    
    def clear_all(self) -> int:
        """
        Clear all cache entries.
        
        Returns:
            Number of entries cleared
        """
        if not self.enabled:
            return 0
        
        files = list(self.cache_dir.glob(CACHE_FILE_EXTENSION))
        
        count = 0
        for file in files:
            try:
                file.unlink()
                count += 1
            except OSError:
                pass
        
        logger.info(f"Cleared {count} cache entries")
        return count
    
    def clear_expired(self) -> int:
        """
        Clear all expired cache entries.
        
        Returns:
            Number of expired entries cleared
        """
        if not self.enabled:
            return 0
        
        count = 0
        for file in self.cache_dir.glob(CACHE_FILE_EXTENSION):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    entry_dict = json.load(f)
                    entry = CacheEntry.from_dict(entry_dict)
                
                ttl = self._get_ttl(entry.phase)
                if entry.is_expired(ttl):
                    file.unlink()
                    count += 1
                    
            except (OSError, json.JSONDecodeError, KeyError):
                # Delete corrupted files
                try:
                    file.unlink()
                    count += 1
                except OSError:
                    pass
        
        if count > 0:
            logger.info(f"Cleared {count} expired cache entries")
        
        return count
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache stats
        """
        if not self.enabled:
            return {
                "enabled": False,
                "total_entries": 0,
            }
        
        files = list(self.cache_dir.glob(CACHE_FILE_EXTENSION))
        
        stats = {
            "enabled": True,
            "cache_dir": str(self.cache_dir),
            "total_entries": len(files),
            "phase1_entries": len(list(self.cache_dir.glob("phase1_*.json"))),
            "phase2_entries": len(list(self.cache_dir.glob("phase2_*.json"))),
            "phase1_ttl": self.phase1_ttl,
            "phase2_ttl": self.phase2_ttl,
        }
        
        # Calculate total disk usage
        total_size = sum(f.stat().st_size for f in files)
        stats["total_size_mb"] = total_size / (1024 * 1024)
        
        return stats
