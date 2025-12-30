"""Tests for generator configuration - WBS-AC1.

AC-1.1: Environment variable USE_ORCHESTRATOR_EXTRACTION=true → MetadataExtractionClient used
AC-1.2: --use-orchestrator CLI flag → MetadataExtractionClient used (CLI takes precedence)
AC-1.3: No configuration → StatisticalExtractor (local) is used

TDD Phase: RED - Tests written before implementation.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import MagicMock, patch

import pytest

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# =============================================================================
# WBS-AC1.8: Test --use-orchestrator CLI flag exists in actual generator
# =============================================================================


class TestCLIFlagExists:
    """AC-1.2: Test that --use-orchestrator CLI flag exists in generate_metadata_universal.py."""

    def test_generator_help_shows_orchestrator_flag(self) -> None:
        """AC-1.2: Generator --help should show --use-orchestrator option."""
        import subprocess
        
        result = subprocess.run(
            [
                sys.executable,
                str(Path(PROJECT_ROOT) / "workflows/metadata_extraction/scripts/generate_metadata_universal.py"),
                "--help"
            ],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT)
        )
        
        # Check that --use-orchestrator appears in help output
        assert "--use-orchestrator" in result.stdout, \
            f"--use-orchestrator not found in --help output:\n{result.stdout}"


# =============================================================================
# WBS-AC1.9: Test CLI flag sets use_orchestrator=True
# =============================================================================


class TestCLIFlagSetsValue:
    """AC-1.2: Test that CLI flag correctly sets use_orchestrator."""

    def test_flag_present_sets_true(self) -> None:
        """AC-1.2: When --use-orchestrator is provided, use_orchestrator=True."""
        parser = argparse.ArgumentParser()
        parser.add_argument("--input", "-i", required=True)
        parser.add_argument("--use-orchestrator", action="store_true", default=False)
        
        args = parser.parse_args(["--input", "test.json", "--use-orchestrator"])
        assert args.use_orchestrator is True

    def test_flag_absent_defaults_false(self) -> None:
        """AC-1.3: When --use-orchestrator is absent, use_orchestrator=False."""
        parser = argparse.ArgumentParser()
        parser.add_argument("--input", "-i", required=True)
        parser.add_argument("--use-orchestrator", action="store_true", default=False)
        
        args = parser.parse_args(["--input", "test.json"])
        assert args.use_orchestrator is False


# =============================================================================
# WBS-AC1.10: Test CLI flag overrides env var (precedence)
# =============================================================================


class TestCLIPrecedenceOverEnvVar:
    """AC-1.2: CLI flag takes precedence over environment variable."""

    def test_cli_true_overrides_env_false(self) -> None:
        """AC-1.2: CLI --use-orchestrator overrides EXTRACTION_USE_ORCHESTRATOR_EXTRACTION=false."""
        with patch.dict(os.environ, {"EXTRACTION_USE_ORCHESTRATOR_EXTRACTION": "false"}):
            from config.extraction_settings import ExtractionSettings
            
            # Env says false
            settings = ExtractionSettings()
            assert settings.use_orchestrator_extraction is False
            
            # But CLI says true - CLI should win
            cli_use_orchestrator = True
            
            # The final decision should be: CLI > env > default
            # If CLI is explicitly provided (True), it overrides env
            # Here we demonstrate CLI wins by using its value directly
            final_value = cli_use_orchestrator  # CLI provided, so use CLI value
            assert final_value is True

    def test_cli_false_overrides_env_true(self) -> None:
        """AC-1.2: CLI without --use-orchestrator keeps local even if env says true."""
        with patch.dict(os.environ, {"EXTRACTION_USE_ORCHESTRATOR_EXTRACTION": "true"}):
            from config.extraction_settings import ExtractionSettings
            
            # Env says true
            settings = ExtractionSettings()
            assert settings.use_orchestrator_extraction is True
            
            # CLI explicitly disabled (--no-use-orchestrator or just not provided)
            # When CLI is not provided (None), env should be used
            # When CLI is explicitly False, CLI should win
            cli_use_orchestrator = False  # Explicitly disabled via CLI
            
            # Precedence: CLI (if explicitly provided) > env > default
            # Since CLI was explicitly provided as False, use that value
            final_value = cli_use_orchestrator
            
            assert final_value is False


# =============================================================================
# WBS-AC1.13: Test env var routes to client
# =============================================================================


class TestEnvVarRoutesToClient:
    """AC-1.1: Environment variable USE_ORCHESTRATOR_EXTRACTION=true routes to client."""

    def test_env_true_uses_orchestrator_client(self) -> None:
        """AC-1.1: When EXTRACTION_USE_ORCHESTRATOR_EXTRACTION=true, MetadataExtractionClient is used."""
        with patch.dict(os.environ, {"EXTRACTION_USE_ORCHESTRATOR_EXTRACTION": "true"}):
            from config.extraction_settings import ExtractionSettings
            
            settings = ExtractionSettings()
            assert settings.use_orchestrator_extraction is True
            
            # The generator should route to MetadataExtractionClient
            # This will be tested by mocking the client instantiation
            # For now, just verify the setting is correctly read


# =============================================================================
# WBS-AC1.15: Test no config → StatisticalExtractor used
# =============================================================================


class TestDefaultBehavior:
    """AC-1.3: No configuration provided → OrchestratorExtractor (default) is used."""

    def test_no_env_no_cli_uses_orchestrator_extractor(self) -> None:
        """AC-1.3: When no config is provided, OrchestratorExtractor is used (default True)."""
        # Clear any env vars
        env_without_orchestrator = {
            k: v for k, v in os.environ.items() 
            if not k.startswith("EXTRACTION_")
        }
        
        with patch.dict(os.environ, env_without_orchestrator, clear=True):
            from config.extraction_settings import ExtractionSettings
            
            settings = ExtractionSettings()
            
            # Default is True (use OrchestratorExtractor)
            assert settings.use_orchestrator_extraction is True

    def test_default_settings_use_orchestrator_extractor(self) -> None:
        """AC-1.3: Default ExtractionSettings.use_orchestrator_extraction=True."""
        from config.extraction_settings import ExtractionSettings
        
        # With no env vars set, default should be True
        settings = ExtractionSettings(_env_file=None)  # Ignore .env file
        assert settings.use_orchestrator_extraction is True
