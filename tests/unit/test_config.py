"""
Tests for configuration system.

Tests the hybrid .env + dataclasses configuration approach.
"""

import os
import pytest
from pathlib import Path
from unittest.mock import patch
from config.settings import (
    LLMConfig,
    PromptConstraints,
    RetryConfig,
    CacheConfig,
    PathConfig,
    reload_settings,
    settings  # Global singleton
)

# Note: TaxonomyConfig removed - was for hardcoded book_taxonomy.py system
# New system uses data-driven concept taxonomy from generate_concept_taxonomy.py


class TestLLMConfig:
    """Test LLM configuration."""
    
    def test_defaults(self):
        """Test default values."""
        os.environ.pop("ANTHROPIC_API_KEY", None)
        os.environ["ANTHROPIC_API_KEY"] = "test-key"
        
        config = LLMConfig()
        assert config.provider == "anthropic"
        assert config.temperature == pytest.approx(0.2)
        assert config.max_tokens == 8192
    
    def test_env_override(self):
        """Test environment variable override."""
        os.environ["LLM_MAX_TOKENS"] = "4096"
        os.environ["LLM_TEMPERATURE"] = "0.5"
        os.environ["ANTHROPIC_API_KEY"] = "test-key"
        
        config = LLMConfig()
        assert config.max_tokens == 4096
        assert config.temperature == pytest.approx(0.5)
        
        # Cleanup
        os.environ.pop("LLM_MAX_TOKENS")
        os.environ.pop("LLM_TEMPERATURE")
    
    def test_validation_max_tokens(self):
        """Test max_tokens validation."""
        os.environ["LLM_MAX_TOKENS"] = "10000"  # Exceeds limit
        os.environ["ANTHROPIC_API_KEY"] = "test-key"
        
        with pytest.raises(ValueError, match="exceeds Claude Sonnet 4.5 limit"):
            LLMConfig()
        
        # Cleanup
        os.environ.pop("LLM_MAX_TOKENS")
    
    def test_validation_temperature(self):
        """Test temperature validation."""
        os.environ["LLM_TEMPERATURE"] = "1.5"  # > 1.0
        os.environ["ANTHROPIC_API_KEY"] = "test-key"
        
        with pytest.raises(ValueError, match="must be between 0.0 and 1.0"):
            LLMConfig()
        
        # Cleanup
        os.environ.pop("LLM_TEMPERATURE")
    
    def test_missing_api_key(self):
        """Test missing API key validation."""
        os.environ.pop("ANTHROPIC_API_KEY", None)
        
        with pytest.raises(ValueError, match="ANTHROPIC_API_KEY not set"):
            LLMConfig()



class TestPromptConstraints:
    """Test prompt constraints configuration."""
    
    def test_defaults(self):
        """Test default values (AC-2)."""
        config = PromptConstraints()
        assert config.max_content_requests == 10
        assert config.max_sections_per_request == 5
        assert config.max_rationale_chars == 350
        assert config.max_pages_per_section == 10
    
    def test_env_override(self):
        """Test environment variable override."""
        os.environ["PROMPT_MAX_CONTENT_REQUESTS"] = "8"
        os.environ["PROMPT_MAX_RATIONALE_CHARS"] = "300"
        
        config = PromptConstraints()
        assert config.max_content_requests == 8
        assert config.max_rationale_chars == 300
        
        # Cleanup
        os.environ.pop("PROMPT_MAX_CONTENT_REQUESTS")
        os.environ.pop("PROMPT_MAX_RATIONALE_CHARS")
    
    def test_validation_rationale_too_small(self):
        """Test rationale length validation."""
        os.environ["PROMPT_MAX_RATIONALE_CHARS"] = "10"  # Too small
        
        with pytest.raises(ValueError, match="too small"):
            PromptConstraints()
        
        # Cleanup
        os.environ.pop("PROMPT_MAX_RATIONALE_CHARS")


class TestRetryConfig:
    """Test retry policy configuration."""
    
    def test_defaults(self):
        """Test default values (AC-3)."""
        config = RetryConfig()
        assert config.max_attempts == 2
        assert config.backoff_factor == pytest.approx(0.8)
        assert config.constraint_factor == pytest.approx(0.5)
    
    def test_env_override(self):
        """Test environment variable override."""
        os.environ["RETRY_MAX_ATTEMPTS"] = "3"
        os.environ["RETRY_BACKOFF_FACTOR"] = "0.7"
        
        config = RetryConfig()
        assert config.max_attempts == 3
        assert config.backoff_factor == pytest.approx(0.7)
        
        # Cleanup
        os.environ.pop("RETRY_MAX_ATTEMPTS")
        os.environ.pop("RETRY_BACKOFF_FACTOR")
    
    def test_validation_max_attempts(self):
        """Test max_attempts validation."""
        os.environ["RETRY_MAX_ATTEMPTS"] = "10"  # Too high
        
        with pytest.raises(ValueError, match="must be between 0 and 5"):
            RetryConfig()
        
        # Cleanup
        os.environ.pop("RETRY_MAX_ATTEMPTS")


class TestCacheConfig:
    """Test cache configuration."""
    
    def test_defaults(self):
        """Test default values (AC-4)."""
        config = CacheConfig()
        assert config.enabled is True
        assert config.cache_dir == Path("cache")
        assert config.phase1_ttl_days == 30
        assert config.phase2_ttl_days == 30
    
    def test_env_override(self):
        """Test environment variable override."""
        os.environ["CACHE_ENABLED"] = "false"
        os.environ["CACHE_DIR"] = "test_cache"
        os.environ["CACHE_PHASE1_TTL_DAYS"] = "7"
        
        config = CacheConfig()
        assert config.enabled is False
        assert config.cache_dir == Path("test_cache")
        assert config.phase1_ttl_days == 7
        
        # Cleanup
        os.environ.pop("CACHE_ENABLED")
        os.environ.pop("CACHE_DIR")
        os.environ.pop("CACHE_PHASE1_TTL_DAYS")
    
    def test_cache_dir_creation(self, tmp_path):
        """Test cache directory is created."""
        test_cache = tmp_path / "test_cache"
        os.environ["CACHE_ENABLED"] = "true"
        os.environ["CACHE_DIR"] = str(test_cache)
        
        _ = CacheConfig()  # Create config to trigger directory creation
        assert test_cache.exists()
        assert test_cache.is_dir()
        
        # Cleanup
        os.environ.pop("CACHE_ENABLED")
        os.environ.pop("CACHE_DIR")


class TestSettings:
    """Test full settings integration."""
    
    def test_initialization(self):
        """Test settings singleton."""
        from config.settings import settings
        
        assert settings.llm is not None
        assert settings.constraints is not None
        assert settings.retry is not None
        assert settings.cache is not None
        assert settings.paths is not None
    
    def test_type_safety(self):
        """Test type-safe access."""
        from config.settings import settings
        
        # These should have correct types
        assert isinstance(settings.llm.max_tokens, int)
        assert isinstance(settings.llm.temperature, float)
        assert isinstance(settings.cache.enabled, bool)
        assert isinstance(settings.paths.repo_root, Path)
    
    def test_reload_settings(self):
        """Test settings reload.
        
        Note: reload_settings() loads from .env file, which takes precedence.
        This test verifies reload_settings() creates a new instance.
        """
        # Get current settings
        current_max_tokens = settings.llm.max_tokens
        
        # Reload should create new instance (ensure API key is in env)
        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test_key'}):
            new_settings = reload_settings()
        
        # Verify it's a new instance (not the same object)
        assert new_settings is not settings
        
        # Verify it has the same config values (from .env)
        assert new_settings.llm.max_tokens == current_max_tokens
        assert new_settings.llm.provider == settings.llm.provider


class TestPathConfig:
    """Test path configuration."""
    
    def test_auto_detection(self):
        """Test auto-detection of paths."""
        config = PathConfig()
        
        # Should auto-detect repository root
        assert config.repo_root.exists()
        assert config.data_dir.exists()
        assert config.textbooks_json_dir.exists()
    
    def test_env_override(self, tmp_path):
        """Test environment variable override for paths."""
        test_repo = tmp_path / "repo"
        test_repo.mkdir()
        
        os.environ["REPO_ROOT"] = str(test_repo)
        
        config = PathConfig()
        assert config.repo_root == test_repo
        
        # Cleanup
        os.environ.pop("REPO_ROOT")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
