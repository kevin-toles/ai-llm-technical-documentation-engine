"""Tests for ExtractionSettings - WBS-2.1.

AC-1.4: ExtractionSettings instantiated + EXTRACTION_* env vars override defaults.

TDD Phase: RED - Tests written before implementation.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING
from unittest.mock import patch

import pytest

if TYPE_CHECKING:
    pass


# =============================================================================
# WBS-2.1.1: ExtractionSettings exists and can be imported
# =============================================================================


class TestExtractionSettingsImport:
    """Test that ExtractionSettings can be imported."""

    def test_can_import_extraction_settings(self) -> None:
        """AC-1.4: ExtractionSettings class exists."""
        from config.extraction_settings import ExtractionSettings

        assert ExtractionSettings is not None

    def test_can_instantiate_extraction_settings(self) -> None:
        """AC-1.4: ExtractionSettings can be instantiated."""
        from config.extraction_settings import ExtractionSettings

        settings = ExtractionSettings()
        assert settings is not None


# =============================================================================
# WBS-2.1.2: Default values
# =============================================================================


class TestExtractionSettingsDefaults:
    """Test default values for ExtractionSettings."""

    def test_use_orchestrator_extraction_default_false(self) -> None:
        """AC-1.3: Default behavior uses local StatisticalExtractor."""
        from config.extraction_settings import ExtractionSettings

        settings = ExtractionSettings()
        assert settings.use_orchestrator_extraction is False

    def test_orchestrator_url_default(self) -> None:
        """Default orchestrator URL is localhost:8083."""
        from config.extraction_settings import ExtractionSettings

        settings = ExtractionSettings()
        assert settings.orchestrator_url == "http://localhost:8083"

    def test_orchestrator_timeout_default(self) -> None:
        """Default timeout is 30 seconds."""
        from config.extraction_settings import ExtractionSettings

        settings = ExtractionSettings()
        assert settings.orchestrator_timeout == 30.0

    def test_orchestrator_max_retries_default(self) -> None:
        """Default max retries is 3."""
        from config.extraction_settings import ExtractionSettings

        settings = ExtractionSettings()
        assert settings.orchestrator_max_retries == 3

    def test_fallback_on_error_default_true(self) -> None:
        """Default fallback on error is True."""
        from config.extraction_settings import ExtractionSettings

        settings = ExtractionSettings()
        assert settings.fallback_on_error is True

    def test_min_keyword_confidence_default(self) -> None:
        """Default min keyword confidence is 0.3."""
        from config.extraction_settings import ExtractionSettings

        settings = ExtractionSettings()
        assert settings.min_keyword_confidence == 0.3

    def test_min_concept_confidence_default(self) -> None:
        """Default min concept confidence is 0.3."""
        from config.extraction_settings import ExtractionSettings

        settings = ExtractionSettings()
        assert settings.min_concept_confidence == 0.3

    def test_top_k_keywords_default(self) -> None:
        """Default top_k_keywords is 15."""
        from config.extraction_settings import ExtractionSettings

        settings = ExtractionSettings()
        assert settings.top_k_keywords == 15

    def test_top_k_concepts_default(self) -> None:
        """Default top_k_concepts is 10."""
        from config.extraction_settings import ExtractionSettings

        settings = ExtractionSettings()
        assert settings.top_k_concepts == 10


# =============================================================================
# WBS-2.1.3: Environment variable overrides (AC-1.4)
# =============================================================================


class TestExtractionSettingsEnvOverrides:
    """Test EXTRACTION_* environment variables override defaults."""

    def test_use_orchestrator_extraction_env_override(self) -> None:
        """AC-1.4: EXTRACTION_USE_ORCHESTRATOR_EXTRACTION overrides default."""
        with patch.dict(os.environ, {"EXTRACTION_USE_ORCHESTRATOR_EXTRACTION": "true"}):
            from config.extraction_settings import ExtractionSettings

            settings = ExtractionSettings()
            assert settings.use_orchestrator_extraction is True

    def test_orchestrator_url_env_override(self) -> None:
        """AC-1.4: EXTRACTION_ORCHESTRATOR_URL overrides default."""
        with patch.dict(os.environ, {"EXTRACTION_ORCHESTRATOR_URL": "http://orchestrator:9000"}):
            from config.extraction_settings import ExtractionSettings

            settings = ExtractionSettings()
            assert settings.orchestrator_url == "http://orchestrator:9000"

    def test_orchestrator_timeout_env_override(self) -> None:
        """AC-1.4: EXTRACTION_ORCHESTRATOR_TIMEOUT overrides default."""
        with patch.dict(os.environ, {"EXTRACTION_ORCHESTRATOR_TIMEOUT": "60.0"}):
            from config.extraction_settings import ExtractionSettings

            settings = ExtractionSettings()
            assert settings.orchestrator_timeout == 60.0

    def test_orchestrator_max_retries_env_override(self) -> None:
        """AC-1.4: EXTRACTION_ORCHESTRATOR_MAX_RETRIES overrides default."""
        with patch.dict(os.environ, {"EXTRACTION_ORCHESTRATOR_MAX_RETRIES": "5"}):
            from config.extraction_settings import ExtractionSettings

            settings = ExtractionSettings()
            assert settings.orchestrator_max_retries == 5

    def test_fallback_on_error_env_override(self) -> None:
        """AC-1.4: EXTRACTION_FALLBACK_ON_ERROR overrides default."""
        with patch.dict(os.environ, {"EXTRACTION_FALLBACK_ON_ERROR": "false"}):
            from config.extraction_settings import ExtractionSettings

            settings = ExtractionSettings()
            assert settings.fallback_on_error is False

    def test_min_keyword_confidence_env_override(self) -> None:
        """AC-1.4: EXTRACTION_MIN_KEYWORD_CONFIDENCE overrides default."""
        with patch.dict(os.environ, {"EXTRACTION_MIN_KEYWORD_CONFIDENCE": "0.5"}):
            from config.extraction_settings import ExtractionSettings

            settings = ExtractionSettings()
            assert settings.min_keyword_confidence == 0.5

    def test_top_k_keywords_env_override(self) -> None:
        """AC-1.4: EXTRACTION_TOP_K_KEYWORDS overrides default."""
        with patch.dict(os.environ, {"EXTRACTION_TOP_K_KEYWORDS": "20"}):
            from config.extraction_settings import ExtractionSettings

            settings = ExtractionSettings()
            assert settings.top_k_keywords == 20


# =============================================================================
# WBS-2.1.4: Singleton pattern
# =============================================================================


class TestExtractionSettingsSingleton:
    """Test get_extraction_settings returns cached instance."""

    def test_get_extraction_settings_returns_instance(self) -> None:
        """get_extraction_settings() returns ExtractionSettings instance."""
        from config.extraction_settings import get_extraction_settings

        settings = get_extraction_settings()
        assert settings is not None

    def test_get_extraction_settings_returns_same_instance(self) -> None:
        """get_extraction_settings() returns cached singleton."""
        from config.extraction_settings import get_extraction_settings

        settings1 = get_extraction_settings()
        settings2 = get_extraction_settings()
        assert settings1 is settings2
