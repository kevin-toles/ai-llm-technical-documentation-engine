"""
TDD RED Phase: Factory Gateway Default Tests

WBS Reference: GATEWAY_ROUTING_REFACTOR_WBS.md - Phase 2.1
Pattern: TDD RED → GREEN → REFACTOR

These tests verify that the LLM provider factory defaults to GatewayProvider
per Kitchen Brigade architecture (ARCHITECTURE.md).

Expected Behavior:
- Factory should return GatewayProvider by default (no env var)
- LLM_PROVIDER=anthropic should still work as override
- LLM_GATEWAY_URL should configure GatewayProvider

Reference Documents:
- ARCHITECTURE.md: Kitchen Brigade "Router" pattern
- CODING_PATTERNS_ANALYSIS.md: Anti-Pattern #12 prevention
- workflows/shared/providers/factory.py: Factory implementation
"""

import os
import pytest
from unittest.mock import patch, MagicMock


class TestFactoryGatewayDefault:
    """
    TDD RED Phase: Tests for factory defaulting to GatewayProvider.
    
    These tests should FAIL initially because factory.py currently
    defaults to "anthropic" instead of "gateway".
    """

    def test_default_provider_is_gateway(self):
        """
        RED TEST: Factory should return GatewayProvider by default.
        
        Current behavior: Returns AnthropicProvider (WRONG)
        Expected behavior: Returns GatewayProvider (CORRECT)
        
        WBS 2.1.1: test_default_provider_is_gateway
        """
        # Clear any existing LLM_PROVIDER env var
        with patch.dict(os.environ, {}, clear=True):
            # Remove LLM_PROVIDER if it exists
            os.environ.pop("LLM_PROVIDER", None)
            
            # Import fresh to avoid cached imports
            from workflows.shared.providers.factory import create_llm_provider
            from workflows.shared.providers.gateway_provider import GatewayProvider
            
            provider = create_llm_provider()
            
            # This should pass when factory defaults to gateway
            assert isinstance(provider, GatewayProvider), (
                f"Expected GatewayProvider but got {type(provider).__name__}. "
                "Factory should default to 'gateway' per Kitchen Brigade architecture."
            )
            assert provider.provider_name == "gateway"

    def test_env_override_to_anthropic_still_works(self):
        """
        RED TEST: LLM_PROVIDER=anthropic should override default.
        
        Users should still be able to use AnthropicProvider directly
        by setting LLM_PROVIDER=anthropic environment variable.
        
        WBS 2.1.2: test_env_override_still_works
        """
        with patch.dict(os.environ, {"LLM_PROVIDER": "anthropic", "ANTHROPIC_API_KEY": "test-key"}):
            # Mock anthropic to avoid actual API calls
            with patch("workflows.shared.providers.anthropic_provider.anthropic") as mock_anthropic:
                mock_anthropic.Anthropic = MagicMock()
                
                from workflows.shared.providers.factory import create_llm_provider
                from workflows.shared.providers.anthropic_provider import AnthropicProvider
                
                provider = create_llm_provider()
                
                assert isinstance(provider, AnthropicProvider), (
                    f"Expected AnthropicProvider when LLM_PROVIDER=anthropic, got {type(provider).__name__}"
                )
                assert provider.provider_name == "anthropic"

    def test_gateway_url_from_env(self):
        """
        RED TEST: LLM_GATEWAY_URL should configure GatewayProvider.
        
        When using GatewayProvider, the gateway URL should be configurable
        via LLM_GATEWAY_URL environment variable.
        
        WBS 2.1.3: test_gateway_url_from_env
        """
        custom_url = "http://custom-gateway:9090"
        
        with patch.dict(os.environ, {
            "LLM_PROVIDER": "gateway",
            "LLM_GATEWAY_URL": custom_url
        }, clear=True):
            from workflows.shared.providers.factory import create_llm_provider
            from workflows.shared.providers.gateway_provider import GatewayProvider
            
            provider = create_llm_provider()
            
            assert isinstance(provider, GatewayProvider)
            # GatewayProvider should use the custom URL
            assert provider._gateway_url == custom_url, (
                f"Expected gateway URL '{custom_url}' but got '{provider._gateway_url}'"
            )

    def test_factory_returns_correct_provider_name(self):
        """
        Verify provider_name property matches expected value.
        
        Gateway provider should identify as "gateway".
        """
        with patch.dict(os.environ, {"LLM_PROVIDER": "gateway"}, clear=True):
            from workflows.shared.providers.factory import create_llm_provider
            
            provider = create_llm_provider()
            
            assert provider.provider_name == "gateway", (
                f"Expected provider_name 'gateway' but got '{provider.provider_name}'"
            )


class TestFactoryValidation:
    """Tests for factory input validation."""

    def test_unknown_provider_raises_error(self):
        """Unknown provider names should raise ValueError."""
        with patch.dict(os.environ, {"LLM_PROVIDER": "unknown_provider"}):
            from workflows.shared.providers.factory import create_llm_provider
            
            with pytest.raises(ValueError, match="Unknown LLM provider"):
                create_llm_provider()

    def test_case_insensitive_provider_name(self):
        """Provider names should be case-insensitive."""
        with patch.dict(os.environ, {"LLM_PROVIDER": "GATEWAY"}, clear=True):
            from workflows.shared.providers.factory import create_llm_provider
            from workflows.shared.providers.gateway_provider import GatewayProvider
            
            provider = create_llm_provider()
            
            assert isinstance(provider, GatewayProvider), (
                "Factory should handle uppercase provider names"
            )
