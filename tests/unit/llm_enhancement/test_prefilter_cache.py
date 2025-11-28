"""
Unit tests for PrefilterCacheRepository (Statistical Pre-Filter Cache).

Tests cover Repository Pattern implementation for caching YAKE + TF-IDF results.

Pattern References:
- Architecture Patterns with Python Ch. 2 (Repository Pattern)
- Python Architecture Patterns Ch. 3, pg. 99 (Cache systems)
- Learning Python Ed6 Ch. 28-31 (Dataclass patterns)

Design Principles:
1. Repository Pattern: Abstract storage behind interface
2. Cache-Aside Pattern: Check cache first, compute on miss
3. TTL Management: 7-day expiration (cheap to regenerate)
4. Content Hash Invalidation: Detect chapter text changes
5. Fail-Safe: Cache errors return None (graceful degradation)

TDD Phase: RED (failing tests)
"""

import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Any

import pytest


# ============================================================
# DATACLASS DEFINITIONS (from DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md)
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
# FIXTURES
# ============================================================

@pytest.fixture
def cache_dir(tmp_path: Path) -> Path:
    """Temporary cache directory for testing."""
    cache_path = tmp_path / "test_cache"
    cache_path.mkdir(parents=True, exist_ok=True)
    return cache_path


@pytest.fixture
def sample_prefilter_output() -> StatisticalPrefilterOutput:
    """Sample statistical pre-filter output for testing."""
    return StatisticalPrefilterOutput(
        chapter_num=3,
        total_guidelines=50,
        filtered_guidelines=[1, 5, 12, 23, 34],
        similarity_scores={
            1: 0.92,
            5: 0.87,
            12: 0.85,
            23: 0.81,
            34: 0.78
        },
        keywords_extracted=["repository", "abstraction", "orm", "persistence", "database"]
    )


@pytest.fixture
def content_hash_v1() -> str:
    """Content hash for chapter text version 1."""
    return "abc12345"


@pytest.fixture
def content_hash_v2() -> str:
    """Content hash for chapter text version 2 (modified)."""
    return "def67890"


# ============================================================
# TEST 1: Cache hit returns cached data
# ============================================================

def test_cache_hit_returns_cached_data(
    cache_dir: Path,
    sample_prefilter_output: StatisticalPrefilterOutput,
    content_hash_v1: str
):
    """
    Test Repository Pattern cache hit behavior.
    
    Given:
      - Cache directory with stored pre-filter output
      - Valid content hash matching cached entry
      - Non-expired cache entry (within 7-day TTL)
    
    When:
      - get() is called with chapter_num and content_hash
    
    Then:
      - Returns cached StatisticalPrefilterOutput
      - Data matches original stored output
      - No file system writes occur (read-only operation)
    
    Pattern: Repository Pattern (Architecture Patterns Ch. 2)
    """
    from workflows.llm_enhancement.scripts.cache.prefilter_cache import PrefilterCacheRepository
    
    # Arrange: Create cache with stored entry
    cache_repo = PrefilterCacheRepository(cache_dir=cache_dir, ttl_days=7)
    cache_repo.set(sample_prefilter_output, content_hash_v1)
    
    # Act: Retrieve cached data
    result = cache_repo.get(
        chapter_num=sample_prefilter_output.chapter_num,
        content_hash=content_hash_v1
    )
    
    # Assert: Cache hit returns exact data
    assert result is not None, "Cache hit should return data, not None"
    assert result.chapter_num == sample_prefilter_output.chapter_num
    assert result.total_guidelines == sample_prefilter_output.total_guidelines
    assert result.filtered_guidelines == sample_prefilter_output.filtered_guidelines
    assert result.similarity_scores == sample_prefilter_output.similarity_scores
    assert result.keywords_extracted == sample_prefilter_output.keywords_extracted


# ============================================================
# TEST 2: Cache miss returns None
# ============================================================

def test_cache_miss_returns_none(cache_dir: Path, content_hash_v1: str):
    """
    Test Repository Pattern cache miss behavior.
    
    Given:
      - Empty cache directory
      - Chapter number not yet cached
    
    When:
      - get() is called for non-existent chapter
    
    Then:
      - Returns None (cache miss)
      - No exception raised (graceful handling)
      - Caller should compute result and call set()
    
    Pattern: Cache-Aside Pattern
    """
    from workflows.llm_enhancement.scripts.cache.prefilter_cache import PrefilterCacheRepository
    
    # Arrange: Empty cache
    cache_repo = PrefilterCacheRepository(cache_dir=cache_dir, ttl_days=7)
    
    # Act: Try to retrieve non-existent data
    result = cache_repo.get(chapter_num=99, content_hash=content_hash_v1)
    
    # Assert: Cache miss returns None
    assert result is None, "Cache miss should return None"


# ============================================================
# TEST 3: Expired cache entry deleted automatically
# ============================================================

def test_expired_cache_entry_deleted(
    cache_dir: Path,
    sample_prefilter_output: StatisticalPrefilterOutput,
    content_hash_v1: str
):
    """
    Test TTL management (7-day expiration).
    
    Given:
      - Cache entry created 8 days ago (expired)
      - TTL set to 7 days
    
    When:
      - get() is called on expired entry
    
    Then:
      - Returns None (entry expired)
      - Cache file deleted from disk (cleanup)
      - is_expired() returns True
    
    Pattern: TTL-based cache invalidation
    """
    from workflows.llm_enhancement.scripts.cache.prefilter_cache import PrefilterCacheRepository
    
    # Arrange: Create cache entry with fake old timestamp
    cache_repo = PrefilterCacheRepository(cache_dir=cache_dir, ttl_days=7)
    cache_repo.set(sample_prefilter_output, content_hash_v1)
    
    # Manually edit cache file to set old timestamp (8 days ago)
    cache_key = cache_repo._get_cache_key(sample_prefilter_output.chapter_num, content_hash_v1)
    cache_file = cache_repo._get_cache_path(cache_key)
    
    with open(cache_file, 'r') as f:
        cache_data = json.load(f)
    
    eight_days_ago = time.time() - (8 * 24 * 60 * 60)
    cache_data['metadata']['created_at'] = eight_days_ago
    
    with open(cache_file, 'w') as f:
        json.dump(cache_data, f)
    
    # Act: Try to retrieve expired data
    result = cache_repo.get(sample_prefilter_output.chapter_num, content_hash_v1)
    
    # Assert: Expired entry returns None and is deleted
    assert result is None, "Expired cache entry should return None"
    assert not cache_file.exists(), "Expired cache file should be deleted"


# ============================================================
# TEST 4: Content hash mismatch invalidates cache
# ============================================================

def test_content_hash_mismatch_invalidates_cache(
    cache_dir: Path,
    sample_prefilter_output: StatisticalPrefilterOutput,
    content_hash_v1: str,
    content_hash_v2: str
):
    """
    Test cache invalidation on chapter text change.
    
    Given:
      - Cache entry for chapter 3 with content_hash_v1
      - Chapter text modified (new content_hash_v2)
    
    When:
      - get() is called with new content_hash_v2
    
    Then:
      - Returns None (cache invalidated)
      - Old cache file remains (different key)
      - Caller should recompute with new chapter text
    
    Pattern: Content hash invalidation (detect chapter changes)
    """
    from workflows.llm_enhancement.scripts.cache.prefilter_cache import PrefilterCacheRepository
    
    # Arrange: Cache entry with old content hash
    cache_repo = PrefilterCacheRepository(cache_dir=cache_dir, ttl_days=7)
    cache_repo.set(sample_prefilter_output, content_hash_v1)
    
    # Act: Try to retrieve with different content hash
    result = cache_repo.get(sample_prefilter_output.chapter_num, content_hash_v2)
    
    # Assert: Content hash mismatch returns None (cache miss)
    assert result is None, "Content hash mismatch should return None (cache invalidated)"
    
    # Old cache entry still exists (different key)
    old_result = cache_repo.get(sample_prefilter_output.chapter_num, content_hash_v1)
    assert old_result is not None, "Old cache entry should still exist"


# ============================================================
# TEST 5: Cache set stores data with metadata
# ============================================================

def test_cache_set_stores_data_with_metadata(
    cache_dir: Path,
    sample_prefilter_output: StatisticalPrefilterOutput,
    content_hash_v1: str
):
    """
    Test CacheEntry metadata wrapper creation.
    
    Given:
      - StatisticalPrefilterOutput to cache
      - Content hash for chapter
    
    When:
      - set() is called
    
    Then:
      - Cache file created with correct structure:
        {
          "metadata": {
            "key": "chapter_3_abc12345",
            "created_at": 1234567890.0,
            "ttl_seconds": 604800,
            "content_hash": "abc12345"
          },
          "data": { ... StatisticalPrefilterOutput ... }
        }
      - File stored in correct location
      - Subsequent get() retrieves exact data
    
    Pattern: Value Object (CacheEntry) wraps business data
    """
    from workflows.llm_enhancement.scripts.cache.prefilter_cache import PrefilterCacheRepository
    
    # Arrange & Act: Store data in cache
    cache_repo = PrefilterCacheRepository(cache_dir=cache_dir, ttl_days=7)
    cache_repo.set(sample_prefilter_output, content_hash_v1)
    
    # Assert: Cache file exists with correct structure
    cache_key = cache_repo._get_cache_key(sample_prefilter_output.chapter_num, content_hash_v1)
    cache_file = cache_repo._get_cache_path(cache_key)
    
    assert cache_file.exists(), "Cache file should exist after set()"
    
    with open(cache_file, 'r') as f:
        cache_data = json.load(f)
    
    # Verify metadata structure
    assert 'metadata' in cache_data, "Cache file should have 'metadata' field"
    assert 'data' in cache_data, "Cache file should have 'data' field"
    
    metadata = cache_data['metadata']
    assert metadata['key'] == cache_key
    assert metadata['content_hash'] == content_hash_v1
    assert metadata['ttl_seconds'] == 7 * 24 * 60 * 60  # 7 days
    assert 'created_at' in metadata
    
    # Verify data structure matches StatisticalPrefilterOutput
    data = cache_data['data']
    assert data['chapter_num'] == sample_prefilter_output.chapter_num
    assert data['total_guidelines'] == sample_prefilter_output.total_guidelines
    assert data['filtered_guidelines'] == sample_prefilter_output.filtered_guidelines


# ============================================================
# TEST 6: Cache clear deletes all entries
# ============================================================

def test_cache_clear_deletes_all_entries(
    cache_dir: Path,
    sample_prefilter_output: StatisticalPrefilterOutput,
    content_hash_v1: str
):
    """
    Test maintenance operations (clear all).
    
    Given:
      - Cache with multiple entries (chapters 1, 2, 3)
    
    When:
      - clear() is called
    
    Then:
      - All cache files deleted
      - Returns count of deleted entries (3)
      - Subsequent get() returns None for all chapters
    
    Pattern: Repository Pattern maintenance operation
    """
    from workflows.llm_enhancement.scripts.cache.prefilter_cache import PrefilterCacheRepository
    
    # Arrange: Create multiple cache entries
    cache_repo = PrefilterCacheRepository(cache_dir=cache_dir, ttl_days=7)
    
    for chapter_num in [1, 2, 3]:
        output = StatisticalPrefilterOutput(
            chapter_num=chapter_num,
            total_guidelines=50,
            filtered_guidelines=[1, 2, 3],
            similarity_scores={1: 0.9, 2: 0.85, 3: 0.8},
            keywords_extracted=["test", "keywords"]
        )
        cache_repo.set(output, content_hash_v1)
    
    # Act: Clear all cache entries
    deleted_count = cache_repo.clear()
    
    # Assert: All entries deleted
    assert deleted_count == 3, f"Expected 3 deleted entries, got {deleted_count}"
    
    for chapter_num in [1, 2, 3]:
        result = cache_repo.get(chapter_num, content_hash_v1)
        assert result is None, f"Chapter {chapter_num} should be None after clear()"


# ============================================================
# TEST 7: Cache clear_expired deletes only expired
# ============================================================

def test_cache_clear_expired_deletes_only_expired(
    cache_dir: Path,
    sample_prefilter_output: StatisticalPrefilterOutput,
    content_hash_v1: str
):
    """
    Test selective cleanup (expired only).
    
    Given:
      - Cache with 3 entries:
        - Chapter 1: Expired (8 days old)
        - Chapter 2: Valid (3 days old)
        - Chapter 3: Valid (1 day old)
    
    When:
      - clear_expired() is called
    
    Then:
      - Only expired entry (chapter 1) deleted
      - Returns count of deleted entries (1)
      - Valid entries (chapters 2, 3) still retrievable
    
    Pattern: TTL-based selective cleanup
    """
    from workflows.llm_enhancement.scripts.cache.prefilter_cache import PrefilterCacheRepository
    
    # Arrange: Create cache entries with different ages
    cache_repo = PrefilterCacheRepository(cache_dir=cache_dir, ttl_days=7)
    
    # Chapter 1: Expired (8 days old)
    output_ch1 = StatisticalPrefilterOutput(
        chapter_num=1,
        total_guidelines=50,
        filtered_guidelines=[1],
        similarity_scores={1: 0.9},
        keywords_extracted=["test"]
    )
    cache_repo.set(output_ch1, content_hash_v1)
    
    cache_key_ch1 = cache_repo._get_cache_key(1, content_hash_v1)
    cache_file_ch1 = cache_repo._get_cache_path(cache_key_ch1)
    
    with open(cache_file_ch1, 'r') as f:
        cache_data_ch1 = json.load(f)
    cache_data_ch1['metadata']['created_at'] = time.time() - (8 * 24 * 60 * 60)
    with open(cache_file_ch1, 'w') as f:
        json.dump(cache_data_ch1, f)
    
    # Chapter 2: Valid (3 days old)
    output_ch2 = StatisticalPrefilterOutput(
        chapter_num=2,
        total_guidelines=50,
        filtered_guidelines=[2],
        similarity_scores={2: 0.85},
        keywords_extracted=["test2"]
    )
    cache_repo.set(output_ch2, content_hash_v1)
    
    # Chapter 3: Valid (current time)
    output_ch3 = StatisticalPrefilterOutput(
        chapter_num=3,
        total_guidelines=50,
        filtered_guidelines=[3],
        similarity_scores={3: 0.8},
        keywords_extracted=["test3"]
    )
    cache_repo.set(output_ch3, content_hash_v1)
    
    # Act: Clear only expired entries
    deleted_count = cache_repo.clear_expired()
    
    # Assert: Only expired entry deleted
    assert deleted_count == 1, f"Expected 1 expired entry, got {deleted_count}"
    
    # Chapter 1 should be gone
    result_ch1 = cache_repo.get(1, content_hash_v1)
    assert result_ch1 is None, "Expired chapter 1 should be None"
    
    # Chapters 2 and 3 should still exist
    result_ch2 = cache_repo.get(2, content_hash_v1)
    assert result_ch2 is not None, "Valid chapter 2 should still exist"
    
    result_ch3 = cache_repo.get(3, content_hash_v1)
    assert result_ch3 is not None, "Valid chapter 3 should still exist"


# ============================================================
# TEST 8: Cache graceful error handling
# ============================================================

def test_cache_graceful_error_handling(
    cache_dir: Path,
    sample_prefilter_output: StatisticalPrefilterOutput,
    content_hash_v1: str
):
    """
    Test fail-safe behavior (invalid JSON, missing files).
    
    Given:
      - Cache file with corrupted JSON
      - Cache file with missing fields
      - Non-existent cache directory
    
    When:
      - get() is called on corrupted entry
    
    Then:
      - Returns None (graceful degradation)
      - No exception raised
      - Workflow continues without cache
    
    Pattern: Fail-safe design (ANTI_PATTERN_ANALYSIS best practices)
    """
    from workflows.llm_enhancement.scripts.cache.prefilter_cache import PrefilterCacheRepository
    
    # Arrange: Create cache with valid entry, then corrupt it
    cache_repo = PrefilterCacheRepository(cache_dir=cache_dir, ttl_days=7)
    cache_repo.set(sample_prefilter_output, content_hash_v1)
    
    cache_key = cache_repo._get_cache_key(sample_prefilter_output.chapter_num, content_hash_v1)
    cache_file = cache_repo._get_cache_path(cache_key)
    
    # Corrupt the JSON file
    with open(cache_file, 'w') as f:
        f.write("{ INVALID JSON }")
    
    # Act: Try to retrieve corrupted data
    result = cache_repo.get(sample_prefilter_output.chapter_num, content_hash_v1)
    
    # Assert: Gracefully returns None (no exception)
    assert result is None, "Corrupted cache entry should return None (fail-safe)"


# ============================================================
# TEST 9: Cache key generation
# ============================================================

def test_cache_key_generation():
    """
    Test _get_cache_key() format: "chapter_{num}_{hash[:8]}".
    
    Given:
      - Chapter number 5
      - Content hash "abcdef123456"
    
    When:
      - _get_cache_key(5, "abcdef123456") is called
    
    Then:
      - Returns "chapter_5_abcdef12"
      - Key format deterministic (same inputs → same key)
      - Truncates hash to 8 characters (readability)
    
    Pattern: Cache key design for file-based storage
    """
    from workflows.llm_enhancement.scripts.cache.prefilter_cache import PrefilterCacheRepository
    
    # Arrange
    cache_repo = PrefilterCacheRepository(ttl_days=7)
    
    # Act
    cache_key = cache_repo._get_cache_key(chapter_num=5, content_hash="abcdef123456")
    
    # Assert
    assert cache_key == "chapter_5_abcdef12", f"Expected 'chapter_5_abcdef12', got '{cache_key}'"
    
    # Verify deterministic (same inputs → same output)
    cache_key_2 = cache_repo._get_cache_key(chapter_num=5, content_hash="abcdef123456")
    assert cache_key == cache_key_2, "Cache key generation should be deterministic"
