"""
Unit tests for GatewayConfig - WBS 3.1.3.1

Tests environment configuration for llm-gateway integration.
"""

import os
import pytest
from unittest.mock import patch


class TestGatewayConfig:
    """Tests for GatewayConfig dataclass."""

    def test_default_values(self) -> None:
        """GatewayConfig should have sensible defaults."""
        # Clear env vars that might affect defaults
        env_vars_to_clear = [
            "DOC_ENHANCER_LLM_GATEWAY_URL",
            "DOC_ENHANCER_LLM_GATEWAY_TIMEOUT",
            "DOC_ENHANCER_USE_GATEWAY",
            "DOC_ENHANCER_SESSION_TTL",
        ]
        with patch.dict(os.environ, {k: "" for k in env_vars_to_clear}, clear=False):
            # Need to reimport to pick up new env
            from config.settings import GatewayConfig
            
            config = GatewayConfig()
            
            assert config.gateway_url == "http://localhost:8080"
            assert config.timeout == 30.0
            assert config.use_gateway is False
            assert config.session_ttl == 3600

    def test_loads_from_env(self) -> None:
        """GatewayConfig should load values from environment."""
        env = {
            "DOC_ENHANCER_LLM_GATEWAY_URL": "http://gateway:9000",
            "DOC_ENHANCER_LLM_GATEWAY_TIMEOUT": "60.0",
            "DOC_ENHANCER_USE_GATEWAY": "true",
            "DOC_ENHANCER_SESSION_TTL": "7200",
        }
        with patch.dict(os.environ, env, clear=False):
            from config.settings import GatewayConfig
            
            config = GatewayConfig()
            
            assert config.gateway_url == "http://gateway:9000"
            assert config.timeout == 60.0
            assert config.use_gateway is True
            assert config.session_ttl == 7200

    def test_validates_timeout_positive(self) -> None:
        """GatewayConfig should reject non-positive timeout."""
        with patch.dict(os.environ, {"DOC_ENHANCER_LLM_GATEWAY_TIMEOUT": "0"}, clear=False):
            from config.settings import GatewayConfig
            
            with pytest.raises(ValueError, match="must be > 0"):
                GatewayConfig()

    def test_validates_session_ttl_minimum(self) -> None:
        """GatewayConfig should reject session TTL < 60."""
        with patch.dict(os.environ, {"DOC_ENHANCER_SESSION_TTL": "30"}, clear=False):
            from config.settings import GatewayConfig
            
            with pytest.raises(ValueError, match="must be >= 60"):
                GatewayConfig()

    def test_validates_url_scheme(self) -> None:
        """GatewayConfig should reject invalid URL schemes."""
        with patch.dict(os.environ, {"DOC_ENHANCER_LLM_GATEWAY_URL": "ftp://gateway"}, clear=False):
            from config.settings import GatewayConfig
            
            with pytest.raises(ValueError, match="http:// or https://"):
                GatewayConfig()

    def test_accepts_https_url(self) -> None:
        """GatewayConfig should accept HTTPS URLs."""
        with patch.dict(os.environ, {"DOC_ENHANCER_LLM_GATEWAY_URL": "https://gateway.example.com"}, clear=False):
            from config.settings import GatewayConfig
            
            config = GatewayConfig()
            assert config.gateway_url == "https://gateway.example.com"


class TestSettingsWithGateway:
    """Tests for Settings class including gateway config."""

    def test_settings_includes_gateway_config(self) -> None:
        """Settings should have gateway attribute."""
        from config.settings import Settings, GatewayConfig
        
        settings = Settings()
        
        assert hasattr(settings, "gateway")
        assert isinstance(settings.gateway, GatewayConfig)

    def test_settings_display_includes_gateway(self) -> None:
        """Settings.display() should show gateway configuration."""
        from config.settings import Settings
        from io import StringIO
        import sys
        
        settings = Settings()
        
        # Capture stdout
        captured = StringIO()
        sys.stdout = captured
        try:
            settings.display()
        finally:
            sys.stdout = sys.__stdout__
        
        output = captured.getvalue()
        assert "[Gateway]" in output
        assert "Gateway URL:" in output
        assert "Use Gateway:" in output
