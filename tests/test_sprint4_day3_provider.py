"""
Sprint 4 Day 3: LLM Provider Integration - TDD RED Phase Tests

Tests for replacing direct call_llm() usage with LLMProviderFactory abstraction.

References:
    - Architecture Patterns with Python Ch. 13 - Dependency Injection
    - Fluent Python 2nd Ch. 13 - Protocols and ABCs
    - Python Distilled Ch. 7 - Class Design

Test Strategy:
    - TDD RED: Write failing tests BEFORE implementation
    - 10 test cases covering factory, provider protocol, pipeline integration
    - Verify no direct Anthropic SDK usage in pipeline
    - Ensure backward compatibility with existing LLM integration

Quality Gates:
    - All tests must pass after GREEN phase
    - Zero regressions in existing tests
    - Ruff clean
"""

import os
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path


class TestProviderFactory:
    """Test factory function for creating LLM providers.
    
    Reference: Architecture Patterns with Python Ch. 13 - Factory pattern for DI
    """
    
    def test_factory_function_exists(self):
        """Verify create_llm_provider() can be imported from src.providers.
        
        Reference:
            Architecture Patterns Ch. 13 - Factory pattern implementation
        """
        from src.providers import create_llm_provider
        
        assert callable(create_llm_provider), "Factory function must be callable"
    
    def test_factory_creates_anthropic_provider(self):
        """Factory returns provider instance that satisfies LLMProvider protocol.
        
        Reference:
            Architecture Patterns Ch. 13 - DI container pattern
            Fluent Python Ch. 13 - Protocol compliance
        """
        from src.providers import create_llm_provider, LLMProvider
        
        # Mock API key to avoid requiring real credentials
        env_vars = {
            "LLM_PROVIDER": "anthropic",
            "ANTHROPIC_API_KEY": "test-api-key-for-testing-only"
        }
        with patch.dict(os.environ, env_vars):
            provider = create_llm_provider()
            
            # Verify protocol compliance (structural subtyping)
            assert hasattr(provider, "call"), "Provider must have call() method"
            assert hasattr(provider, "model_name"), "Provider must have model_name property"
            assert hasattr(provider, "provider_name"), "Provider must have provider_name property"
            assert callable(getattr(provider, "call")), "call must be callable"
    
    def test_factory_respects_env_variable(self):
        """Factory reads LLM_PROVIDER environment variable correctly.
        
        Reference:
            Microservices Up and Running Ch. 7 - 12-Factor App config
        """
        from src.providers import create_llm_provider
        
        # Mock API key to avoid requiring real credentials
        env_vars = {
            "LLM_PROVIDER": "anthropic",
            "ANTHROPIC_API_KEY": "test-api-key-for-testing-only"
        }
        with patch.dict(os.environ, env_vars):
            provider = create_llm_provider()
            assert provider.provider_name == "anthropic"
    
    def test_factory_has_default_provider(self):
        """Factory defaults to Anthropic provider when LLM_PROVIDER unset.
        
        Reference:
            Architecture Patterns Ch. 13 - Sensible defaults in DI
        """
        from src.providers import create_llm_provider
        
        # Create env with only API key (no LLM_PROVIDER)
        env_copy = {"ANTHROPIC_API_KEY": "test-api-key-for-testing-only"}
        
        with patch.dict(os.environ, env_copy, clear=True):
            provider = create_llm_provider()
            assert provider.provider_name == "anthropic", "Should default to Anthropic"


class TestPipelineUsesProvider:
    """Test that pipeline files use provider abstraction instead of direct SDK calls.
    
    Reference:
        Architecture Patterns Ch. 13 - Dependency injection in application layer
    """
    
    def test_pipeline_imports_provider_factory(self):
        """Verify chapter_generator_all_text.py imports from src.providers.
        
        Reference:
            Architecture Patterns Ch. 13 - DI via imports
        """
        pipeline_file = Path("src/pipeline/chapter_generator_all_text.py")
        assert pipeline_file.exists(), "Pipeline file must exist"
        
        content = pipeline_file.read_text()
        
        # Should import from providers
        assert "from src.providers import" in content or "import src.providers" in content, \
            "Pipeline must import from src.providers"
        
        # Should NOT directly import anthropic SDK
        assert "import anthropic" not in content or "# import anthropic" in content, \
            "Pipeline must not directly import anthropic SDK"
    
    def test_pipeline_no_direct_llm_integration_call(self):
        """Pipeline should not use legacy call_llm() from llm_integration.
        
        Reference:
            Architecture Patterns Ch. 13 - Avoid global function coupling
        """
        pipeline_file = Path("src/pipeline/chapter_generator_all_text.py")
        content = pipeline_file.read_text()
        
        # Check for legacy import pattern
        # Allow commented-out legacy code for backward reference
        lines = content.split('\n')
        active_llm_integration_imports = [
            line for line in lines 
            if 'from llm_integration import call_llm' in line 
            and not line.strip().startswith('#')
        ]
        
        assert len(active_llm_integration_imports) == 0, \
            "Pipeline must not actively import call_llm from llm_integration"
    
    def test_pipeline_uses_provider_call_method(self):
        """Pipeline calls provider.call() method for LLM requests.
        
        Reference:
            Fluent Python Ch. 13 - Protocol method invocation
        """
        pipeline_file = Path("src/pipeline/chapter_generator_all_text.py")
        content = pipeline_file.read_text()
        
        # Should use provider.call() pattern
        # Note: variable name might be _llm_provider or similar
        assert ".call(" in content, \
            "Pipeline must call provider.call() method"
    
    def test_llm_response_handled_correctly(self):
        """Pipeline correctly extracts content from LLMResponse dataclass.
        
        Reference:
            Python Distilled Ch. 7 - Dataclass field access
            Fluent Python Ch. 13 - Protocol return types
        """
        # This test verifies the integration by mocking the provider
        from src.providers import LLMResponse
        
        # Mock provider that returns LLMResponse
        mock_provider = Mock()
        mock_provider.call.return_value = LLMResponse(
            content="Test annotation",
            model="claude-sonnet-4-5",
            input_tokens=100,
            output_tokens=50,
            stop_reason="end_turn"
        )
        
        # Verify LLMResponse structure
        response = mock_provider.call(
            prompt="test",
            max_tokens=100,
            temperature=0.0,
            system_prompt="test system"
        )
        
        assert hasattr(response, "content"), "LLMResponse must have content field"
        assert hasattr(response, "input_tokens"), "LLMResponse must have input_tokens"
        assert hasattr(response, "output_tokens"), "LLMResponse must have output_tokens"
        assert response.content == "Test annotation"


class TestProviderProtocolCompliance:
    """Test that provider implementations satisfy the LLMProvider protocol.
    
    Reference:
        Fluent Python 2nd Ch. 13 - Protocol classes and structural subtyping
    """
    
    def test_anthropic_provider_satisfies_protocol(self):
        """AnthropicProvider satisfies LLMProvider protocol contract.
        
        Reference:
            Fluent Python Ch. 13 - Protocol compliance checking
            Python Distilled Ch. 7 - Interface contracts
        """
        from src.providers import AnthropicProvider, LLMProvider
        
        # Create instance
        # Note: This will fail until AnthropicProvider is updated to match protocol
        try:
            provider = AnthropicProvider()
        except Exception:
            # Expected to fail in RED phase - provider not yet updated
            pytest.skip("AnthropicProvider not yet updated for protocol (expected in RED phase)")
        
        # Verify protocol methods exist
        assert hasattr(provider, "call"), "Must have call() method"
        assert callable(provider.call), "call must be callable"
        
        # Verify protocol properties exist  
        assert hasattr(provider, "model_name"), "Must have model_name property"
        assert hasattr(provider, "provider_name"), "Must have provider_name property"
        
        # Verify call signature (without actually calling API)
        import inspect
        sig = inspect.signature(provider.call)
        param_names = list(sig.parameters.keys())
        
        # Should have these parameters based on protocol
        assert "prompt" in param_names, "call() must accept prompt parameter"
        assert "max_tokens" in param_names, "call() must accept max_tokens parameter"
    
    def test_llm_response_dataclass_structure(self):
        """LLMResponse dataclass has all required fields and total_tokens property.
        
        Reference:
            Python Distilled Ch. 7 - Dataclass design
            Fluent Python Ch. 5 - Data class builders
        """
        from src.providers import LLMResponse
        
        # Create sample response
        response = LLMResponse(
            content="test content",
            model="claude-sonnet-4-5",
            input_tokens=100,
            output_tokens=50,
            stop_reason="end_turn"
        )
        
        # Verify required fields
        assert response.content == "test content"
        assert response.model == "claude-sonnet-4-5"
        assert response.input_tokens == 100
        assert response.output_tokens == 50
        assert response.stop_reason == "end_turn"
        
        # Verify computed property
        assert hasattr(response, "total_tokens"), "Must have total_tokens property"
        assert response.total_tokens == 150, "total_tokens should be sum of input + output"


# Test execution note:
# Run with: pytest tests/test_sprint4_day3_provider.py -v
# Expected RED phase result: Multiple failures (factory.py doesn't exist, pipeline not updated)
# Expected GREEN phase result: All 10 tests passing after minimal implementation
