"""
Example: Using the configuration system

Demonstrates how to use the hybrid .env + dataclasses configuration.
"""

from config.settings import settings

def example_basic_usage():
    """Basic configuration access."""
    print("\n=== Basic Usage ===")
    
    # Access LLM settings
    print(f"LLM Model: {settings.llm.model}")
    print(f"Max Tokens: {settings.llm.max_tokens}")
    print(f"Temperature: {settings.llm.temperature}")
    
    # Access taxonomy settings
    print(f"Max Books: {settings.taxonomy.max_books}")
    print(f"Min Relevance: {settings.taxonomy.min_relevance}")
    
    # Access cache settings
    print(f"Cache Enabled: {settings.cache.enabled}")
    print(f"Cache Directory: {settings.cache.cache_dir}")
    
    # Access paths
    print(f"Textbooks JSON Dir: {settings.paths.textbooks_json_dir}")


def example_validation():
    """Configuration validation."""
    print("\n=== Validation ===")
    
    # Settings are validated on initialization
    try:
        settings.validate()
        print("✓ Configuration valid")
    except Exception as e:
        print(f"✗ Configuration error: {e}")


def example_type_safety():
    """Type-safe access with IDE autocomplete."""
    print("\n=== Type Safety ===")
    
    # IDE knows these are specific types
    max_tokens: int = settings.llm.max_tokens
    temperature: float = settings.llm.temperature
    cache_enabled: bool = settings.cache.enabled
    
    print(f"max_tokens type: {type(max_tokens).__name__}")
    print(f"temperature type: {type(temperature).__name__}")
    print(f"cache_enabled type: {type(cache_enabled).__name__}")


def example_runtime_override():
    """Override settings at runtime (for testing)."""
    print("\n=== Runtime Override ===")
    
    import os
    from config.settings import Settings
    
    # Save original
    original_max_tokens = settings.llm.max_tokens
    print(f"Original max_tokens: {original_max_tokens}")
    
    # Override via environment
    os.environ["LLM_MAX_TOKENS"] = "4096"
    
    # Create new settings instance
    test_settings = Settings()
    print(f"Test max_tokens: {test_settings.llm.max_tokens}")
    
    # Restore
    os.environ["LLM_MAX_TOKENS"] = str(original_max_tokens)


def example_display_config():
    """Display full configuration."""
    print("\n=== Full Configuration ===")
    settings.display()


if __name__ == "__main__":
    example_basic_usage()
    example_validation()
    example_type_safety()
    example_runtime_override()
    # example_display_config()  # Uncomment to see full config
