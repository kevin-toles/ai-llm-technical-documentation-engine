"""
Comprehensive tests for workflows/shared/cache.py

Tests the Cache-Aside pattern implementation for disk-based caching.

Architecture Pattern: Cache-Aside Pattern (Architecture Patterns Ch. 12)
- Read-through cache pattern (check cache → fetch on miss → store)
- TTL-based expiration for automatic cache invalidation
- Repository pattern for storage abstraction (hides file system details)
- Graceful error handling for disk I/O failures
- Supports multiple phases with separate TTLs

Key Responsibilities:
- Cache hit/miss detection
- Automatic TTL expiration
- Cache key generation (content hashing)
- Disk-based persistence
- Cache statistics and management

Test Coverage:
- Test Cache-Aside read pattern
- Test TTL expiration logic
- Test cache invalidation
- Test error recovery (corrupted files, disk errors)
- Test cache statistics
"""

import json
import time
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
from workflows.shared.cache import ChapterCache, CacheEntry


@pytest.fixture
def temp_cache_dir(tmp_path):
    """Create temporary cache directory."""
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    return cache_dir


@pytest.fixture
def cache(temp_cache_dir):
    """Create ChapterCache instance with temp directory."""
    return ChapterCache(
        cache_dir=temp_cache_dir,
        enabled=True,
        phase1_ttl=3600,  # 1 hour
        phase2_ttl=7200,  # 2 hours
    )


@pytest.fixture
def sample_content():
    """Sample content for testing."""
    return "This is test content for caching."


@pytest.fixture
def sample_data():
    """Sample data to cache."""
    return {
        "result": "test result",
        "metadata": {"timestamp": "2025-11-25", "version": "1.0"}
    }


class TestCacheEntry:
    """
    Test CacheEntry dataclass.
    
    Pattern: Data Transfer Object (DTO)
    Coverage: TTL expiration, age calculation, serialization
    """
    
    def test_cache_entry_not_expired_within_ttl(self):
        """CacheEntry should not be expired if within TTL."""
        # Arrange
        entry = CacheEntry(
            key="test_key",
            data={"result": "test"},
            created_at=time.time(),
            phase="phase1"
        )
        
        # Act
        is_expired = entry.is_expired(ttl_seconds=3600)
        
        # Assert
        assert not is_expired
    
    def test_cache_entry_expired_after_ttl(self):
        """CacheEntry should be expired if beyond TTL."""
        # Arrange
        old_timestamp = time.time() - 7200  # 2 hours ago
        entry = CacheEntry(
            key="test_key",
            data={"result": "test"},
            created_at=old_timestamp,
            phase="phase1"
        )
        
        # Act
        is_expired = entry.is_expired(ttl_seconds=3600)  # 1 hour TTL
        
        # Assert
        assert is_expired
    
    def test_cache_entry_never_expires_with_zero_ttl(self):
        """CacheEntry with TTL=0 should never expire."""
        # Arrange
        old_timestamp = time.time() - 86400  # 24 hours ago
        entry = CacheEntry(
            key="test_key",
            data={"result": "test"},
            created_at=old_timestamp,
            phase="phase1"
        )
        
        # Act
        is_expired = entry.is_expired(ttl_seconds=0)  # Never expires
        
        # Assert
        assert not is_expired
    
    def test_cache_entry_age_minutes_calculated_correctly(self):
        """CacheEntry.age_minutes() should return correct age."""
        # Arrange
        timestamp = time.time() - 600  # 10 minutes ago
        entry = CacheEntry(
            key="test_key",
            data={"result": "test"},
            created_at=timestamp,
            phase="phase1"
        )
        
        # Act
        age = entry.age_minutes()
        
        # Assert
        assert 9.5 < age < 10.5  # Allow small timing variance
    
    def test_cache_entry_serialization_roundtrip(self):
        """CacheEntry should serialize and deserialize correctly."""
        # Arrange
        original = CacheEntry(
            key="test_key",
            data={"result": "test", "nested": {"value": 42}},
            created_at=1234567890.123,
            phase="phase1"
        )
        
        # Act
        dict_repr = original.to_dict()
        restored = CacheEntry.from_dict(dict_repr)
        
        # Assert
        assert restored.key == original.key
        assert restored.data == original.data
        assert restored.created_at == original.created_at
        assert restored.phase == original.phase


class TestCacheOperations:
    """
    Test core cache operations (get/set).
    
    Pattern: Cache-Aside Pattern (Architecture Patterns Ch. 12)
    Coverage: Cache hit, cache miss, cache write, key generation
    """
    
    def test_cache_miss_returns_none(self, cache, sample_content):
        """Cache miss should return None."""
        # Act
        result = cache.get(sample_content, "phase1")
        
        # Assert
        assert result is None
    
    def test_cache_hit_returns_data(self, cache, sample_content, sample_data):
        """Cache hit should return stored data."""
        # Arrange
        cache.set(sample_content, "phase1", sample_data)
        
        # Act
        result = cache.get(sample_content, "phase1")
        
        # Assert
        assert result == sample_data
        assert result["result"] == "test result"
    
    def test_cache_set_creates_file(self, cache, sample_content, sample_data):
        """Cache.set() should create cache file on disk."""
        # Act
        cache.set(sample_content, "phase1", sample_data)
        
        # Assert
        cache_files = list(cache.cache_dir.glob("phase1_*.json"))
        assert len(cache_files) == 1
        
        # Verify file contents
        with open(cache_files[0], 'r') as f:
            entry_dict = json.load(f)
            assert entry_dict["data"] == sample_data
            assert entry_dict["phase"] == "phase1"
    
    def test_cache_key_generation_is_deterministic(self, cache):
        """Same content should generate same cache key."""
        # Arrange
        content1 = "test content"
        content2 = "test content"
        
        # Act
        key1 = cache._get_cache_key(content1, "phase1")
        key2 = cache._get_cache_key(content2, "phase1")
        
        # Assert
        assert key1 == key2
    
    def test_cache_key_generation_includes_kwargs(self, cache):
        """Different kwargs should generate different cache keys."""
        # Arrange
        content = "test content"
        
        # Act
        key1 = cache._get_cache_key(content, "phase1", param1="value1")
        key2 = cache._get_cache_key(content, "phase1", param1="value2")
        
        # Assert
        assert key1 != key2
    
    def test_cache_disabled_returns_none_on_get(self, temp_cache_dir, sample_content):
        """Disabled cache should always return None on get."""
        # Arrange
        disabled_cache = ChapterCache(cache_dir=temp_cache_dir, enabled=False)
        
        # Act
        result = disabled_cache.get(sample_content, "phase1")
        
        # Assert
        assert result is None
    
    def test_cache_disabled_skips_set(self, temp_cache_dir, sample_content, sample_data):
        """Disabled cache should not write files on set."""
        # Arrange
        disabled_cache = ChapterCache(cache_dir=temp_cache_dir, enabled=False)
        
        # Act
        disabled_cache.set(sample_content, "phase1", sample_data)
        
        # Assert
        cache_files = list(temp_cache_dir.glob("*.json"))
        assert len(cache_files) == 0


class TestTTLManagement:
    """
    Test TTL (Time-To-Live) expiration logic.
    
    Pattern: Cache-Aside with TTL-based eviction
    Coverage: TTL expiration, expired entry removal, different phase TTLs
    """
    
    def test_expired_entry_returns_none(self, cache, sample_content, sample_data):
        """Expired cache entry should return None."""
        # Arrange
        cache.phase1_ttl = 1  # 1 second TTL
        cache.set(sample_content, "phase1", sample_data)
        
        # Wait for expiration
        time.sleep(1.5)
        
        # Act
        result = cache.get(sample_content, "phase1")
        
        # Assert
        assert result is None
    
    def test_expired_entry_is_deleted_on_get(self, cache, sample_content, sample_data):
        """Expired cache file should be deleted when accessed."""
        # Arrange
        cache.phase1_ttl = 1  # 1 second TTL
        cache.set(sample_content, "phase1", sample_data)
        
        # Wait for expiration
        time.sleep(1.5)
        
        # Act
        cache.get(sample_content, "phase1")
        
        # Assert - file should be deleted
        cache_files = list(cache.cache_dir.glob("phase1_*.json"))
        assert len(cache_files) == 0
    
    def test_different_phases_have_different_ttls(self, cache, sample_content, sample_data):
        """Different phases should use different TTLs."""
        # Arrange
        cache.phase1_ttl = 3600  # 1 hour
        cache.phase2_ttl = 7200  # 2 hours
        
        # Act
        ttl1 = cache._get_ttl("phase1")
        ttl2 = cache._get_ttl("phase2")
        
        # Assert
        assert ttl1 == 3600
        assert ttl2 == 7200
        assert ttl1 != ttl2
    
    def test_cache_refresh_updates_ttl(self, cache, sample_content, sample_data):
        """Re-caching should update TTL timestamp."""
        # Arrange
        cache.set(sample_content, "phase1", sample_data)
        
        # Get first timestamp
        result1 = cache.get(sample_content, "phase1")
        assert result1 is not None
        
        # Wait a bit
        time.sleep(0.5)
        
        # Re-cache with new data
        new_data = {"result": "updated"}
        cache.set(sample_content, "phase1", new_data)
        
        # Act
        result2 = cache.get(sample_content, "phase1")
        
        # Assert - should have new data
        assert result2 == new_data
        assert result2 != sample_data


class TestErrorHandling:
    """
    Test error recovery and graceful degradation.
    
    Pattern: Defensive Programming + Error Recovery
    Coverage: Corrupted files, disk I/O errors, missing directories
    """
    
    def test_corrupted_cache_file_returns_none(self, cache, sample_content):
        """Corrupted cache file should return None and be deleted."""
        # Arrange - create corrupted cache file
        cache_key = cache._get_cache_key(sample_content, "phase1")
        cache_file = cache._get_cache_file(cache_key, "phase1")
        
        with open(cache_file, 'w') as f:
            f.write("This is not valid JSON {{{")
        
        # Act
        result = cache.get(sample_content, "phase1")
        
        # Assert
        assert result is None
        assert not cache_file.exists()  # Corrupted file deleted
    
    def test_missing_cache_directory_disables_cache(self, tmp_path):
        """Missing cache directory that cannot be created should disable cache."""
        # Arrange - use a path that cannot be created (read-only parent)
        with patch('pathlib.Path.mkdir', side_effect=OSError("Permission denied")):
            cache = ChapterCache(cache_dir=tmp_path / "readonly" / "cache", enabled=True)
        
        # Assert
        assert not cache.enabled
    
    def test_disk_write_error_logs_but_continues(self, cache, sample_content, sample_data):
        """Disk write errors should be logged but not crash."""
        # Arrange - mock open to raise OSError
        with patch('builtins.open', side_effect=OSError("Disk full")):
            # Act - should not raise exception
            cache.set(sample_content, "phase1", sample_data)
        
        # Assert - operation completes without error
        # (cache write failed, but no exception raised)


class TestCacheInvalidation:
    """
    Test cache invalidation operations.
    
    Pattern: Cache Invalidation Strategies
    Coverage: Clear phase, clear all, clear expired
    """
    
    def test_clear_phase_removes_only_specified_phase(self, cache, sample_content, sample_data):
        """clear_phase() should only remove entries for specified phase."""
        # Arrange
        cache.set(sample_content, "phase1", sample_data)
        cache.set(sample_content, "phase2", sample_data)
        
        # Act
        count = cache.clear_phase("phase1")
        
        # Assert
        assert count == 1
        assert cache.get(sample_content, "phase1") is None
        assert cache.get(sample_content, "phase2") is not None
    
    def test_clear_all_removes_all_entries(self, cache, sample_content, sample_data):
        """clear_all() should remove all cache entries."""
        # Arrange
        cache.set(sample_content, "phase1", sample_data)
        cache.set(sample_content, "phase2", sample_data)
        cache.set("other content", "phase1", sample_data)
        
        # Act
        count = cache.clear_all()
        
        # Assert
        assert count == 3
        assert cache.get(sample_content, "phase1") is None
        assert cache.get(sample_content, "phase2") is None
    
    def test_clear_expired_only_removes_expired_entries(self, cache, sample_content, sample_data):
        """clear_expired() should only remove expired entries."""
        # Arrange
        cache.phase1_ttl = 1  # 1 second TTL
        cache.set(sample_content, "phase1", sample_data)
        cache.set("fresh content", "phase2", sample_data)  # phase2 has longer TTL
        
        # Wait for phase1 to expire
        time.sleep(1.5)
        
        # Act
        count = cache.clear_expired()
        
        # Assert
        assert count >= 1  # At least the phase1 entry
        assert cache.get(sample_content, "phase1") is None
        assert cache.get("fresh content", "phase2") is not None


class TestCacheStatistics:
    """
    Test cache statistics and monitoring.
    
    Pattern: Observability + Monitoring
    Coverage: Entry counts, disk usage, phase-specific stats
    """
    
    def test_get_stats_returns_correct_counts(self, cache, sample_content, sample_data):
        """get_stats() should return accurate entry counts."""
        # Arrange
        cache.set(sample_content, "phase1", sample_data)
        cache.set("content2", "phase1", sample_data)
        cache.set("content3", "phase2", sample_data)
        
        # Act
        stats = cache.get_stats()
        
        # Assert
        assert stats["enabled"] is True
        assert stats["total_entries"] == 3
        assert stats["phase1_entries"] == 2
        assert stats["phase2_entries"] == 1
    
    def test_get_stats_calculates_disk_usage(self, cache, sample_content, sample_data):
        """get_stats() should calculate total disk usage."""
        # Arrange
        cache.set(sample_content, "phase1", sample_data)
        
        # Act
        stats = cache.get_stats()
        
        # Assert
        assert "total_size_mb" in stats
        assert stats["total_size_mb"] > 0
    
    def test_get_stats_includes_ttl_values(self, cache):
        """get_stats() should include TTL configuration."""
        # Act
        stats = cache.get_stats()
        
        # Assert
        assert stats["phase1_ttl"] == 3600
        assert stats["phase2_ttl"] == 7200
    
    def test_get_stats_disabled_cache_returns_minimal_stats(self, temp_cache_dir):
        """get_stats() for disabled cache should return minimal info."""
        # Arrange
        disabled_cache = ChapterCache(cache_dir=temp_cache_dir, enabled=False)
        
        # Act
        stats = disabled_cache.get_stats()
        
        # Assert
        assert stats["enabled"] is False
        assert stats["total_entries"] == 0


class TestCacheAsidePatternCompliance:
    """
    Test Cache-Aside pattern compliance (Architecture Patterns Ch. 12).
    
    Validates:
    - Read pattern: Check cache → miss → fetch from source → store
    - Separation of concerns: Cache doesn't fetch data
    - TTL-based eviction policy
    - Storage abstraction (Repository pattern)
    """
    
    def test_cache_aside_read_pattern(self, cache, sample_content, sample_data):
        """
        Validate Cache-Aside read pattern.
        
        Pattern: Check cache → if miss, caller fetches → caller stores
        """
        # Step 1: Check cache (miss)
        result = cache.get(sample_content, "phase1")
        assert result is None
        
        # Step 2: Caller "fetches from source" (simulated)
        fetched_data = sample_data
        
        # Step 3: Caller stores in cache
        cache.set(sample_content, "phase1", fetched_data)
        
        # Step 4: Subsequent read hits cache
        cached_result = cache.get(sample_content, "phase1")
        assert cached_result == fetched_data
    
    def test_cache_does_not_fetch_data(self, cache, sample_content):
        """
        Cache should NOT fetch data itself (Cache-Aside pattern).
        
        Cache-Aside: Application controls fetch logic
        vs Read-Through: Cache controls fetch logic
        """
        # Act
        result = cache.get(sample_content, "phase1")
        
        # Assert - cache returns None, doesn't fetch
        assert result is None
    
    def test_storage_abstraction_hides_file_details(self, cache, sample_content, sample_data):
        """
        Cache should abstract storage details (Repository pattern).
        
        Caller shouldn't know about file paths, JSON serialization, etc.
        """
        # Act - simple API, no file path knowledge needed
        cache.set(sample_content, "phase1", sample_data)
        result = cache.get(sample_content, "phase1")
        
        # Assert - caller gets data without knowing implementation
        assert result == sample_data
        # Internal detail: file exists, but caller doesn't know/care
        assert any(cache.cache_dir.glob("*.json"))
    
    def test_ttl_based_eviction_policy(self, cache, sample_content, sample_data):
        """
        Cache should use TTL-based eviction (not LRU, LFU, etc.).
        
        Architecture Patterns Ch. 12: Time-based invalidation
        """
        # Arrange
        cache.phase1_ttl = 1  # 1 second TTL
        cache.set(sample_content, "phase1", sample_data)
        
        # Act - wait for TTL expiration
        time.sleep(1.5)
        result = cache.get(sample_content, "phase1")
        
        # Assert - entry evicted by TTL, not by access pattern
        assert result is None
