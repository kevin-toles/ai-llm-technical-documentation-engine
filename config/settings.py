"""
Application settings using .env + Python dataclasses.

Architecture:
- Environment variables (.env) for runtime/secret config
- Dataclasses for type safety, validation, IDE support
- References: Microservices Up and Running Ch. 7 (12-Factor Config)
              Python Distilled Ch. 7 (Dataclasses)
              Fluent Python 2nd Ch. 5 (Data Class Builders)

Usage:
    from config.settings import settings
    
    max_tokens = settings.llm.max_tokens
    api_key = settings.llm.api_key
    cache_enabled = settings.cache.enabled
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class LLMConfig:
    """LLM API configuration from environment variables.
    
    Environment Variables:
        LLM_PROVIDER: LLM provider (default: anthropic)
        ANTHROPIC_API_KEY: Anthropic API key (required if provider=anthropic)
        ANTHROPIC_MODEL: Model name (default: claude-sonnet-4-5-20250929)
        LLM_TEMPERATURE: Sampling temperature 0.0-1.0 (default: 0.2)
        LLM_MAX_TOKENS: Max output tokens (default: 8192, Claude Sonnet 4.5 limit)
        ENABLE_API_LOGGING: Enable detailed API logging (default: true)
    """
    provider: str = field(default_factory=lambda: os.getenv("LLM_PROVIDER", "anthropic"))
    model: str = field(default_factory=lambda: os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929"))
    api_key: str = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))
    temperature: float = field(default_factory=lambda: float(os.getenv("LLM_TEMPERATURE", "0.2")))
    max_tokens: int = field(default_factory=lambda: int(os.getenv("LLM_MAX_TOKENS", "8192")))
    enable_logging: bool = field(default_factory=lambda: os.getenv("ENABLE_API_LOGGING", "true").lower() == "true")
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.provider == "anthropic" and not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not set in environment. "
                "Please add it to .env file or set as environment variable."
            )
        
        if self.max_tokens > 8192:
            raise ValueError(
                f"LLM_MAX_TOKENS={self.max_tokens} exceeds Claude Sonnet 4.5 limit (8192). "
                "Please set LLM_MAX_TOKENS <= 8192 in .env"
            )
        
        if not 0.0 <= self.temperature <= 1.0:
            raise ValueError(
                f"LLM_TEMPERATURE={self.temperature} must be between 0.0 and 1.0"
            )


@dataclass
class PromptConstraints:
    """JSON response field constraints (Acceptance Criteria AC-2).
    
    These enforce deterministic size limits on LLM responses to prevent
    truncation and ensure parseable JSON.
    
    Environment Variables:
        PROMPT_MAX_CONTENT_REQUESTS: Max content_requests array size (default: 10)
        PROMPT_MAX_SECTIONS: Max sections per content request (default: 5)
        PROMPT_MAX_RATIONALE_CHARS: Max characters in rationale field (default: 350)
        PROMPT_MAX_PAGES: Max pages per section (default: 10)
    """
    max_content_requests: int = field(default_factory=lambda: int(os.getenv("PROMPT_MAX_CONTENT_REQUESTS", "10")))
    max_sections_per_request: int = field(default_factory=lambda: int(os.getenv("PROMPT_MAX_SECTIONS", "5")))
    max_rationale_chars: int = field(default_factory=lambda: int(os.getenv("PROMPT_MAX_RATIONALE_CHARS", "350")))
    max_pages_per_section: int = field(default_factory=lambda: int(os.getenv("PROMPT_MAX_PAGES", "10")))
    
    def __post_init__(self):
        """Validate constraints."""
        if self.max_content_requests < 1:
            raise ValueError("PROMPT_MAX_CONTENT_REQUESTS must be >= 1")
        
        if self.max_sections_per_request < 1:
            raise ValueError("PROMPT_MAX_SECTIONS must be >= 1")
        
        if self.max_rationale_chars < 50:
            raise ValueError(
                f"PROMPT_MAX_RATIONALE_CHARS={self.max_rationale_chars} too small, "
                "must be >= 50 characters"
            )
        
        if self.max_pages_per_section < 1:
            raise ValueError("PROMPT_MAX_PAGES must be >= 1")


@dataclass
class RetryConfig:
    """LLM API retry policy configuration.
    
    Environment Variables:
        RETRY_MAX_ATTEMPTS: Maximum retry attempts (default: 2)
        RETRY_BACKOFF_FACTOR: Token reduction per retry (default: 0.8 = 20% reduction)
        RETRY_CONSTRAINT_FACTOR: Book/section reduction per retry (default: 0.5 = 50% reduction)
    """
    max_attempts: int = field(default_factory=lambda: int(os.getenv("RETRY_MAX_ATTEMPTS", "2")))
    backoff_factor: float = field(default_factory=lambda: float(os.getenv("RETRY_BACKOFF_FACTOR", "0.8")))
    constraint_factor: float = field(default_factory=lambda: float(os.getenv("RETRY_CONSTRAINT_FACTOR", "0.5")))
    
    def __post_init__(self):
        """Validate retry configuration."""
        if self.max_attempts < 0 or self.max_attempts > 5:
            raise ValueError(
                f"RETRY_MAX_ATTEMPTS={self.max_attempts} must be between 0 and 5"
            )
        
        if not 0.5 <= self.backoff_factor <= 1.0:
            raise ValueError(
                f"RETRY_BACKOFF_FACTOR={self.backoff_factor} must be between 0.5 and 1.0"
            )
        
        if not 0.3 <= self.constraint_factor <= 0.8:
            raise ValueError(
                f"RETRY_CONSTRAINT_FACTOR={self.constraint_factor} must be between 0.3 and 0.8"
            )


@dataclass
class CacheConfig:
    """Caching configuration (Acceptance Criteria AC-4).
    
    Environment Variables:
        CACHE_ENABLED: Enable caching (default: true)
        CACHE_DIR: Cache directory path (default: cache)
        CACHE_PHASE1_TTL_DAYS: Phase 1 cache TTL in days (default: 30)
        CACHE_PHASE2_TTL_DAYS: Phase 2 cache TTL in days (default: 30)
    """
    enabled: bool = field(default_factory=lambda: os.getenv("CACHE_ENABLED", "true").lower() == "true")
    cache_dir: Path = field(default_factory=lambda: Path(os.getenv("CACHE_DIR", "cache")))
    phase1_ttl_days: int = field(default_factory=lambda: int(os.getenv("CACHE_PHASE1_TTL_DAYS", "30")))
    phase2_ttl_days: int = field(default_factory=lambda: int(os.getenv("CACHE_PHASE2_TTL_DAYS", "30")))
    
    def __post_init__(self):
        """Validate and setup cache directory."""
        if self.phase1_ttl_days < 1:
            raise ValueError("CACHE_PHASE1_TTL_DAYS must be >= 1")
        
        if self.phase2_ttl_days < 1:
            raise ValueError("CACHE_PHASE2_TTL_DAYS must be >= 1")
        
        # Create cache directory if enabled
        if self.enabled:
            self.cache_dir.mkdir(parents=True, exist_ok=True)


@dataclass
class PathConfig:
    """File path configuration.
    
    Environment Variables:
        REPO_ROOT: Repository root directory (default: auto-detect)
        DATA_DIR: Data directory (default: {REPO_ROOT}/data)
        GUIDELINES_DIR: Guidelines directory (default: {REPO_ROOT}/guidelines)
        OUTPUT_DIR: Output directory (default: {REPO_ROOT}/outputs)
        LOGS_DIR: Logs directory (default: {REPO_ROOT}/logs)
        CACHE_DIR: Cache directory (default: {REPO_ROOT}/cache)
    """
    repo_root: Path = field(default_factory=lambda: Path(os.getenv("REPO_ROOT", Path(__file__).parent.parent)))
    
    def __post_init__(self):
        """Initialize derived paths."""
        # Legacy data_dir for backward compatibility
        self.data_dir = Path(os.getenv("DATA_DIR", self.repo_root / "data"))
        
        # New workflow-based paths
        self.textbooks_json_dir = Path(os.getenv(
            "TEXTBOOKS_JSON_DIR", 
            self.repo_root / "workflows" / "pdf_to_json" / "output" / "textbooks_json"
        ))
        self.metadata_dir = Path(os.getenv(
            "METADATA_DIR",
            self.repo_root / "workflows" / "metadata_extraction" / "output"
        ))
        
        self.guidelines_dir = Path(os.getenv("GUIDELINES_DIR", self.repo_root / "guidelines"))
        self.output_dir = Path(os.getenv("OUTPUT_DIR", self.repo_root / "outputs"))
        self.logs_dir = Path(os.getenv("LOGS_DIR", self.repo_root / "logs"))
        self.cache_dir = Path(os.getenv("CACHE_DIR", self.repo_root / "cache"))
        
        # Create output, logs, and cache directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)


@dataclass
class Settings:
    """Application settings (singleton).
    
    Aggregates all configuration from environment variables into type-safe
    dataclass structure with validation.
    
    Usage:
        from config.settings import settings
        
        # Access configuration
        max_tokens = settings.llm.max_tokens
        cache_enabled = settings.cache.enabled
        
        # Override in tests
        test_settings = Settings()
        test_settings.llm.max_tokens = 4096
    """
    llm: LLMConfig = field(default_factory=LLMConfig)
    constraints: PromptConstraints = field(default_factory=PromptConstraints)
    retry: RetryConfig = field(default_factory=RetryConfig)
    cache: CacheConfig = field(default_factory=CacheConfig)
    paths: PathConfig = field(default_factory=PathConfig)
    
    def validate(self):
        """Run cross-config validation checks.
        
        Validates relationships between different config sections.
        """
        # Cross-config validation (if needed in future)
        pass
    
    def display(self):
        """Display current configuration (useful for debugging)."""
        print("\n" + "="*60)
        print("LLM Document Enhancer - Configuration")
        print("="*60)
        
        print("\n[LLM]")
        print(f"  Provider: {self.llm.provider}")
        print(f"  Model: {self.llm.model}")
        print(f"  API Key: {'***' + self.llm.api_key[-4:] if self.llm.api_key else 'NOT SET'}")
        print(f"  Temperature: {self.llm.temperature}")
        print(f"  Max Tokens: {self.llm.max_tokens:,}")
        print(f"  Logging Enabled: {self.llm.enable_logging}")
        
        print("\n[Taxonomy]")
        print(f"  Min Relevance: {self.taxonomy.min_relevance}")
        print(f"  Max Books: {self.taxonomy.max_books}")
        print(f"  Cascade Depth: {self.taxonomy.cascade_depth}")
        print(f"  Pre-filter Enabled: {self.taxonomy.enable_prefilter}")
        
        print("\n[Constraints]")
        print(f"  Max Content Requests: {self.constraints.max_content_requests}")
        print(f"  Max Sections/Request: {self.constraints.max_sections_per_request}")
        print(f"  Max Rationale Chars: {self.constraints.max_rationale_chars}")
        print(f"  Max Pages/Section: {self.constraints.max_pages_per_section}")
        
        print("\n[Retry Policy]")
        print(f"  Max Attempts: {self.retry.max_attempts}")
        print(f"  Backoff Factor: {self.retry.backoff_factor}")
        print(f"  Constraint Factor: {self.retry.constraint_factor}")
        
        print("\n[Cache]")
        print(f"  Enabled: {self.cache.enabled}")
        print(f"  Directory: {self.cache.cache_dir}")
        print(f"  Phase 1 TTL: {self.cache.phase1_ttl_days} days")
        print(f"  Phase 2 TTL: {self.cache.phase2_ttl_days} days")
        
        print("\n[Paths]")
        print(f"  Repo Root: {self.paths.repo_root}")
        print(f"  Data Dir: {self.paths.data_dir}")
        print(f"  Textbooks JSON: {self.paths.textbooks_json_dir}")
        print(f"  Metadata: {self.paths.metadata_dir}")
        print(f"  Guidelines: {self.paths.guidelines_dir}")
        print(f"  Output: {self.paths.output_dir}")
        print(f"  Logs: {self.paths.logs_dir}")
        
        print("\n" + "="*60 + "\n")


# ============================================================================
# Global Settings Instance (Singleton)
# ============================================================================

# Initialize global settings on module import
settings = Settings()

# Validate configuration
try:
    settings.validate()
except Exception as e:
    import warnings
    warnings.warn(f"Configuration validation warning: {e}")


# ============================================================================
# Convenience Functions
# ============================================================================

def reload_settings() -> Settings:
    """Reload settings from environment variables.
    
    Useful for tests or runtime configuration changes.
    
    Returns:
        New Settings instance with current environment values
    """
    load_dotenv(override=True)
    new_settings = Settings()
    new_settings.validate()
    return new_settings


def get_settings() -> Settings:
    """Get current settings instance.
    
    Returns:
        Global settings singleton
    """
    return settings


# Display configuration on import (only if not in test mode)
if os.getenv("PYTEST_CURRENT_TEST") is None and os.getenv("SHOW_CONFIG", "false").lower() == "true":
    settings.display()
