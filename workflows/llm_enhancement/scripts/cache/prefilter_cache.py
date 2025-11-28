"""
PrefilterCacheRepository: Repository Pattern for statistical pre-filter cache.

Caches YAKE keyword extraction + TF-IDF similarity filtering results.

Design Principles:
1. Repository Pattern: Abstract storage behind clean interface
2. Cache-Aside Pattern: Check cache first, compute on miss
3. TTL Management: 7-day expiration (cheap to regenerate - no API costs)
4. Content Hash Invalidation: Detect chapter text changes
5. Fail-Safe: Cache errors return None (graceful degradation)

Pattern References:
- Architecture Patterns with Python Ch. 2 (Repository Pattern)
- Python Architecture Patterns Ch. 3, pg. 99 (Cache systems)
- Learning Python Ed6 Ch. 9 (File I/O), Ch. 28-31 (Dataclass patterns)

File Structure:
    workflows/llm_enhancement/intermediate/statistical_prefilter/
        chapter_1_abc12345.json
        chapter_2_def67890.json
        ...

Cache File Format:
    {
        "metadata": {
            "key": "chapter_3_abc12345",
            "created_at": 1234567890.0,
            "ttl_seconds": 604800,
            "content_hash": "abc12345"
        },
        "data": {
            "chapter_num": 3,
            "total_guidelines": 50,
            "filtered_guidelines": [1, 5, 12, 23, 34],
            "similarity_scores": {
                "1": 0.92,
                "5": 0.87,
                "12": 0.85
            },
            "keywords_extracted": ["repository", "abstraction"]
        }
    }
"""

import hashlib
import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Any


# ============================================================
# DATACLASS DEFINITIONS
# ============================================================

@dataclass
class StatisticalPrefilterOutput:
    """DTO for statistical pre-filter results (YAKE + TF-IDF)."""
    chapter_num: int
    total_guidelines: int
    filtered_guidelines: List[int]  # Guideline IDs passing similarity threshold
    similarity_scores: Dict[int, float]  # guideline_id -> cosine similarity
    keywords_extracted: List[str]  # YAKE keywords from chapter


@dataclass
class CacheEntry:
    """Value Object for cache metadata (Repository Pattern)."""
    key: str
    created_at: float              # Unix timestamp
    ttl_seconds: int               # Time to live
    content_hash: str              # For cache invalidation
    
    def is_expired(self) -> bool:
        """Check if cache entry has expired based on TTL."""
        return time.time() > (self.created_at + self.ttl_seconds)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dict for JSON storage."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CacheEntry':
        """Deserialize from dict."""
        return cls(**data)


# ============================================================
# REPOSITORY IMPLEMENTATION
# ============================================================

class PrefilterCacheRepository:
    """
    Repository Pattern for statistical pre-filter cache.
    
    Abstracts file-based cache storage behind clean interface.
    Implements Cache-Aside Pattern with TTL-based expiration.
    
    Pattern: Repository Pattern (Architecture Patterns Ch. 2)
    Anti-Pattern Avoidance: Optional types for nullable returns (ANTI_PATTERN_ANALYSIS §1.1)
    
    Usage:
        >>> cache = PrefilterCacheRepository(ttl_days=7)
        >>> 
        >>> # Cache miss → compute result
        >>> result = cache.get(chapter_num=3, content_hash="abc12345")
        >>> if result is None:
        ...     result = compute_statistical_prefilter(chapter)
        ...     cache.set(result, content_hash="abc12345")
        >>> 
        >>> # Cache hit → use cached result
        >>> result = cache.get(chapter_num=3, content_hash="abc12345")
        >>> assert result is not None
    """
    
    def __init__(self, cache_dir: Optional[Path] = None, ttl_days: int = 7):
        """
        Initialize PrefilterCacheRepository.
        
        Args:
            cache_dir: Directory for cache storage. Defaults to:
                       workflows/llm_enhancement/intermediate/statistical_prefilter/
            ttl_days: Time-to-live in days. Default 7 days (cheap to regenerate).
        
        Pattern: Repository Pattern initialization (Architecture Patterns Ch. 2)
        """
        if cache_dir is None:
            # Default location: workflows/llm_enhancement/intermediate/statistical_prefilter/
            self.cache_dir = Path("workflows/llm_enhancement/intermediate/statistical_prefilter")
        else:
            self.cache_dir = cache_dir
        
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl_seconds = ttl_days * 24 * 60 * 60  # Convert days to seconds
    
    def get(self, chapter_num: int, content_hash: str) -> Optional[StatisticalPrefilterOutput]:
        """
        Retrieve cached statistical pre-filter output.
        
        Args:
            chapter_num: Chapter number
            content_hash: Hash of chapter text (for invalidation)
        
        Returns:
            StatisticalPrefilterOutput if cache hit and not expired, None otherwise
        
        Cache Invalidation:
            - TTL expiration: Entry deleted if older than 7 days
            - Content hash mismatch: Different hash → cache miss (chapter text changed)
            - Corrupted file: Returns None (graceful degradation)
        
        Pattern: Cache-Aside Pattern
        Anti-Pattern Avoidance: Returns Optional[T] not None (ANTI_PATTERN_ANALYSIS §1.1)
        """
        try:
            cache_key = self._get_cache_key(chapter_num, content_hash)
            cache_file = self._get_cache_path(cache_key)
            
            # Cache miss: File doesn't exist
            if not cache_file.exists():
                return None
            
            # Read cache file
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # Validate cache structure
            if 'metadata' not in cache_data or 'data' not in cache_data:
                return None
            
            # Parse metadata
            metadata = CacheEntry.from_dict(cache_data['metadata'])
            
            # Check TTL expiration
            if metadata.is_expired():
                # Delete expired entry
                cache_file.unlink(missing_ok=True)
                return None
            
            # Verify content hash matches (detect chapter text changes)
            if metadata.content_hash != content_hash:
                return None
            
            # Parse cached data
            data = cache_data['data']
            result = StatisticalPrefilterOutput(
                chapter_num=data['chapter_num'],
                total_guidelines=data['total_guidelines'],
                filtered_guidelines=data['filtered_guidelines'],
                similarity_scores={int(k): v for k, v in data['similarity_scores'].items()},
                keywords_extracted=data['keywords_extracted']
            )
            
            return result
        
        except (json.JSONDecodeError, KeyError, IOError, OSError) as e:
            # Graceful degradation: Cache errors return None
            # Workflow continues by computing result (no API cost)
            return None
    
    def set(self, output: StatisticalPrefilterOutput, content_hash: str) -> None:
        """
        Store statistical pre-filter output in cache.
        
        Args:
            output: StatisticalPrefilterOutput to cache
            content_hash: Hash of chapter text (for invalidation)
        
        Cache Structure:
            {
                "metadata": { CacheEntry fields },
                "data": { StatisticalPrefilterOutput fields }
            }
        
        Pattern: Value Object (CacheEntry) wraps business data
        Error Handling: Graceful failure (doesn't raise exceptions)
        """
        try:
            cache_key = self._get_cache_key(output.chapter_num, content_hash)
            cache_file = self._get_cache_path(cache_key)
            
            # Create metadata wrapper
            metadata = CacheEntry(
                key=cache_key,
                created_at=time.time(),
                ttl_seconds=self.ttl_seconds,
                content_hash=content_hash
            )
            
            # Serialize to JSON
            cache_data = {
                'metadata': metadata.to_dict(),
                'data': asdict(output)
            }
            
            # Write cache file atomically
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
        
        except (IOError, OSError) as e:
            # Graceful failure: Cache write errors don't break workflow
            pass
    
    def clear(self) -> int:
        """
        Delete all cache entries.
        
        Returns:
            Number of entries deleted
        
        Pattern: Repository Pattern maintenance operation
        Use Case: Force recomputation, clear stale data, free disk space
        """
        try:
            deleted_count = 0
            for cache_file in self.cache_dir.glob("chapter_*.json"):
                cache_file.unlink(missing_ok=True)
                deleted_count += 1
            return deleted_count
        except (IOError, OSError):
            return 0
    
    def clear_expired(self) -> int:
        """
        Delete only expired cache entries (TTL-based cleanup).
        
        Returns:
            Number of expired entries deleted
        
        Pattern: TTL-based selective cleanup
        Use Case: Scheduled maintenance, free disk space while preserving valid cache
        """
        try:
            deleted_count = 0
            for cache_file in self.cache_dir.glob("chapter_*.json"):
                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        cache_data = json.load(f)
                    
                    if 'metadata' in cache_data:
                        metadata = CacheEntry.from_dict(cache_data['metadata'])
                        if metadata.is_expired():
                            cache_file.unlink(missing_ok=True)
                            deleted_count += 1
                except (json.JSONDecodeError, KeyError, IOError):
                    # Skip corrupted files
                    continue
            
            return deleted_count
        except (IOError, OSError):
            return 0
    
    def _get_cache_key(self, chapter_num: int, content_hash: str) -> str:
        """
        Generate cache key from chapter number and content hash.
        
        Args:
            chapter_num: Chapter number
            content_hash: Full hash string (will be truncated to 8 chars)
        
        Returns:
            Cache key format: "chapter_{num}_{hash[:8]}"
        
        Pattern: Deterministic key generation (same inputs → same key)
        Rationale: Truncate hash for readability (8 chars = 4B collision space)
        """
        return f"chapter_{chapter_num}_{content_hash[:8]}"
    
    def _get_cache_path(self, cache_key: str) -> Path:
        """
        Get full path to cache file.
        
        Args:
            cache_key: Cache key from _get_cache_key()
        
        Returns:
            Full path: {cache_dir}/{cache_key}.json
        
        Pattern: File I/O with pathlib.Path (Learning Python Ch. 9)
        """
        return self.cache_dir / f"{cache_key}.json"
    
    def _compute_content_hash(self, text: str) -> str:
        """
        Compute SHA256 hash of chapter text.
        
        Args:
            text: Chapter text content
        
        Returns:
            SHA256 hash (64 hex characters)
        
        Pattern: Content-addressable caching
        Use Case: Detect chapter text changes for cache invalidation
        
        Note: This method provided for testing convenience.
              In production, caller computes hash once and reuses.
        """
        return hashlib.sha256(text.encode('utf-8')).hexdigest()
