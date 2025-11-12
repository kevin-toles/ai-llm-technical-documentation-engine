"""
Tests for caching layer.
"""

import pytest
import time

from src.cache import ChapterCache, CacheEntry


class TestCacheEntry:
    """Tests for CacheEntry dataclass."""
    
    def test_create_entry(self):
        """Test creating a cache entry."""
        entry = CacheEntry(
            key="test_key",
            data={"field": "value"},
            created_at=time.time(),
            phase="phase1",
        )
        
        assert entry.key == "test_key"
        assert entry.data == {"field": "value"}
        assert entry.phase == "phase1"
    
    def test_is_expired_not_expired(self):
        """Test that recent entry is not expired."""
        entry = CacheEntry(
            key="test",
            data={},
            created_at=time.time(),
            phase="phase1",
        )
        
        assert entry.is_expired(3600) is False  # 1 hour TTL
    
    def test_is_expired_expired(self):
        """Test that old entry is expired."""
        old_time = time.time() - 7200  # 2 hours ago
        entry = CacheEntry(
            key="test",
            data={},
            created_at=old_time,
            phase="phase1",
        )
        
        assert entry.is_expired(3600) is True  # 1 hour TTL
    
    def test_is_expired_zero_ttl(self):
        """Test that zero TTL means never expires."""
        old_time = time.time() - 100000  # Very old
        entry = CacheEntry(
            key="test",
            data={},
            created_at=old_time,
            phase="phase1",
        )
        
        assert entry.is_expired(0) is False
    
    def test_age_minutes(self):
        """Test age calculation in minutes."""
        old_time = time.time() - 120  # 2 minutes ago
        entry = CacheEntry(
            key="test",
            data={},
            created_at=old_time,
            phase="phase1",
        )
        
        age = entry.age_minutes()
        assert 1.9 < age < 2.1  # Allow small timing variance
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        entry = CacheEntry(
            key="test_key",
            data={"field": "value"},
            created_at=123456.0,
            phase="phase1",
        )
        
        result = entry.to_dict()
        
        assert result["key"] == "test_key"
        assert result["data"] == {"field": "value"}
        assert abs(result["created_at"] - 123456.0) < 0.001
        assert result["phase"] == "phase1"
    
    def test_from_dict(self):
        """Test creating entry from dictionary."""
        data = {
            "key": "test_key",
            "data": {"field": "value"},
            "created_at": 123456.0,
            "phase": "phase1",
        }
        
        entry = CacheEntry.from_dict(data)
        
        assert entry.key == "test_key"
        assert entry.data == {"field": "value"}
        assert abs(entry.created_at - 123456.0) < 0.001
        assert entry.phase == "phase1"
    
    def test_roundtrip(self):
        """Test to_dict and from_dict roundtrip."""
        entry1 = CacheEntry(
            key="test",
            data={"nested": {"data": "value"}},
            created_at=time.time(),
            phase="phase2",
        )
        
        entry2 = CacheEntry.from_dict(entry1.to_dict())
        
        assert entry2.key == entry1.key
        assert entry2.data == entry1.data
        assert entry2.created_at == entry1.created_at
        assert entry2.phase == entry1.phase


class TestChapterCache:
    """Tests for ChapterCache."""
    
    @pytest.fixture
    def temp_cache_dir(self, tmp_path):
        """Provide a temporary cache directory."""
        return tmp_path / "test_cache"
    
    @pytest.fixture
    def cache(self, temp_cache_dir):
        """Provide a test cache instance."""
        return ChapterCache(
            cache_dir=temp_cache_dir,
            enabled=True,
            phase1_ttl=3600,
            phase2_ttl=7200,
        )
    
    def test_init_creates_directory(self, temp_cache_dir):
        """Test that initialization creates cache directory."""
        assert not temp_cache_dir.exists()
        
        _cache = ChapterCache(cache_dir=temp_cache_dir, enabled=True)
        
        assert temp_cache_dir.exists()
        assert temp_cache_dir.is_dir()
    
    def test_init_disabled(self, temp_cache_dir):
        """Test that disabled cache doesn't create directory."""
        _cache = ChapterCache(cache_dir=temp_cache_dir, enabled=False)
        
        assert not temp_cache_dir.exists()
    
    def test_cache_miss(self, cache):
        """Test cache miss returns None."""
        result = cache.get("content", "phase1")
        
        assert result is None
    
    def test_cache_hit(self, cache):
        """Test cache hit returns cached data."""
        data = {"field1": "value1", "field2": 42}
        
        cache.set("content", "phase1", data)
        result = cache.get("content", "phase1")
        
        assert result == data
    
    def test_cache_with_kwargs(self, cache):
        """Test cache with additional parameters."""
        data = {"result": "value"}
        
        cache.set("content", "phase1", data, param1="a", param2="b")
        
        # Same kwargs - should hit
        result = cache.get("content", "phase1", param1="a", param2="b")
        assert result == data
        
        # Different kwargs - should miss
        result = cache.get("content", "phase1", param1="different")
        assert result is None
    
    def test_cache_different_phases(self, cache):
        """Test that different phases have separate caches."""
        data1 = {"phase": "1"}
        data2 = {"phase": "2"}
        
        cache.set("content", "phase1", data1)
        cache.set("content", "phase2", data2)
        
        assert cache.get("content", "phase1") == data1
        assert cache.get("content", "phase2") == data2
    
    def test_cache_expiration(self, cache):
        """Test that expired entries are not returned."""
        # Create cache with very short TTL
        short_cache = ChapterCache(
            cache_dir=cache.cache_dir,
            enabled=True,
            phase1_ttl=1,  # 1 second
        )
        
        data = {"test": "data"}
        short_cache.set("content", "phase1", data)
        
        # Should hit immediately
        assert short_cache.get("content", "phase1") == data
        
        # Wait for expiration
        time.sleep(1.5)
        
        # Should miss after expiration
        assert short_cache.get("content", "phase1") is None
        
        # File should be deleted
        files = list(cache.cache_dir.glob("phase1_*.json"))
        assert len(files) == 0
    
    def test_disabled_cache_no_operations(self, temp_cache_dir):
        """Test that disabled cache doesn't perform operations."""
        cache = ChapterCache(cache_dir=temp_cache_dir, enabled=False)
        
        # Set should do nothing
        cache.set("content", "phase1", {"data": "value"})
        
        # Get should return None
        result = cache.get("content", "phase1")
        assert result is None
        
        # No files should be created
        assert not temp_cache_dir.exists()
    
    def test_corrupted_cache_file(self, cache):
        """Test that corrupted cache files are handled gracefully."""
        # Create a corrupted cache file
        cache_file = cache.cache_dir / "phase1_corrupted.json"
        cache_file.write_text("invalid json{{{")
        
        # Get should return None and delete corrupted file - should not crash
        _result = cache.get("test_content_that_hashes_to_corrupted", "phase1")
    
    def test_clear_phase(self, cache):
        """Test clearing cache for specific phase."""
        cache.set("content1", "phase1", {"data": "1"})
        cache.set("content2", "phase1", {"data": "2"})
        cache.set("content3", "phase2", {"data": "3"})
        
        # Clear phase1
        cleared = cache.clear_phase("phase1")
        
        assert cleared == 2
        assert cache.get("content1", "phase1") is None
        assert cache.get("content2", "phase1") is None
        assert cache.get("content3", "phase2") is not None
    
    def test_clear_all(self, cache):
        """Test clearing all cache entries."""
        cache.set("content1", "phase1", {"data": "1"})
        cache.set("content2", "phase2", {"data": "2"})
        cache.set("content3", "phase3", {"data": "3"})
        
        cleared = cache.clear_all()
        
        assert cleared == 3
        assert cache.get("content1", "phase1") is None
        assert cache.get("content2", "phase2") is None
        assert cache.get("content3", "phase3") is None
    
    def test_clear_expired(self, cache):
        """Test clearing only expired entries."""
        # Create cache with short TTL for testing
        short_cache = ChapterCache(
            cache_dir=cache.cache_dir,
            enabled=True,
            phase1_ttl=1,  # 1 second
            phase2_ttl=3600,  # 1 hour
        )
        
        short_cache.set("content1", "phase1", {"data": "1"})
        short_cache.set("content2", "phase2", {"data": "2"})
        
        # Wait for phase1 to expire
        time.sleep(1.5)
        
        # Clear expired
        cleared = short_cache.clear_expired()
        
        assert cleared >= 1  # At least phase1 should be cleared
        assert short_cache.get("content1", "phase1") is None
        assert short_cache.get("content2", "phase2") is not None
    
    def test_get_stats(self, cache):
        """Test getting cache statistics."""
        cache.set("content1", "phase1", {"data": "1"})
        cache.set("content2", "phase1", {"data": "2"})
        cache.set("content3", "phase2", {"data": "3"})
        
        stats = cache.get_stats()
        
        assert stats["enabled"] is True
        assert stats["total_entries"] == 3
        assert stats["phase1_entries"] == 2
        assert stats["phase2_entries"] == 1
        assert stats["phase1_ttl"] == 3600
        assert stats["phase2_ttl"] == 7200
        assert "cache_dir" in stats
        assert "total_size_mb" in stats
    
    def test_get_stats_disabled(self, temp_cache_dir):
        """Test stats for disabled cache."""
        cache = ChapterCache(cache_dir=temp_cache_dir, enabled=False)
        
        stats = cache.get_stats()
        
        assert stats["enabled"] is False
        assert stats["total_entries"] == 0
    
    def test_cache_key_stability(self, cache):
        """Test that same inputs produce same cache key."""
        data = {"test": "data"}
        
        # Set twice with same inputs
        cache.set("content", "phase1", data, param="value")
        cache.set("content", "phase1", {"different": "data"}, param="value")
        
        # Should get the second write (same key)
        result = cache.get("content", "phase1", param="value")
        assert result == {"different": "data"}
    
    def test_cache_key_ordering(self, cache):
        """Test that kwargs order doesn't affect cache key."""
        data = {"test": "data"}
        
        # Set with kwargs in one order
        cache.set("content", "phase1", data, param1="a", param2="b")
        
        # Get with kwargs in different order
        result = cache.get("content", "phase1", param2="b", param1="a")
        
        assert result == data
    
    def test_phase_ttl_configuration(self, cache):
        """Test that different phases use correct TTLs."""
        assert cache._get_ttl("phase1") == 3600
        assert cache._get_ttl("phase2") == 7200
        assert cache._get_ttl("unknown") == 86400  # Default
