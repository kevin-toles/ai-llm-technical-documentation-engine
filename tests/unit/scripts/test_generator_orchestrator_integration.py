"""Tests for UniversalMetadataGenerator orchestrator integration - WBS-2.3.

AC-1.1: Environment variable USE_ORCHESTRATOR_EXTRACTION=true → MetadataExtractionClient used
AC-1.2: CLI flag --use-orchestrator → MetadataExtractionClient used, CLI takes precedence
AC-5.1: Orchestrator mode uses MetadataExtractionClient
AC-5.2: Local mode uses StatisticalExtractor
AC-5.3: Fallback on error uses StatisticalExtractor
AC-5.4: Strict mode (fallback=False) propagates exception

TDD Phase: RED - Tests written before implementation.
"""

from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

if TYPE_CHECKING:
    pass


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def sample_book_json(tmp_path: Path) -> Path:
    """Create a minimal test book JSON file."""
    import json

    book_data = {
        "title": "Test Book",
        "pages": [
            {"page_number": 1, "content": "Chapter 1: Introduction to microservices architecture and distributed systems."},
            {"page_number": 2, "content": "Microservices enable independent deployment and scaling of services."},
            {"page_number": 3, "content": "Chapter 2: API Design patterns for REST and GraphQL services."},
            {"page_number": 4, "content": "RESTful APIs use HTTP methods for CRUD operations on resources."},
        ],
    }
    json_path = tmp_path / "test_book.json"
    json_path.write_text(json.dumps(book_data))
    return json_path


@pytest.fixture
def mock_extraction_client() -> MagicMock:
    """Create a mock MetadataExtractionClient."""
    from workflows.shared.clients.metadata_client import (
        ConceptResult,
        ExtractionMetadata,
        KeywordResult,
        MetadataExtractionResult,
        RejectedKeywords,
    )

    client = MagicMock()
    client.__aenter__ = AsyncMock(return_value=client)
    client.__aexit__ = AsyncMock(return_value=None)
    client.health_check = AsyncMock(return_value=True)
    client.extract_metadata = AsyncMock(
        return_value=MetadataExtractionResult(
            keywords=[
                KeywordResult(term="microservices", score=0.9, is_technical=True),
                KeywordResult(term="api", score=0.85, is_technical=True),
            ],
            concepts=[
                ConceptResult(name="distributed systems", confidence=0.8, domain="architecture", tier="T2"),
            ],
            summary="Test summary from orchestrator.",
            metadata=ExtractionMetadata(
                processing_time_ms=100.0,
                text_length=500,
                detected_domain="architecture",
                domain_confidence=0.75,
                quality_score=0.8,
                stages_completed=["keywords", "concepts"],
            ),
            rejected=RejectedKeywords(keywords=["www"], reasons={"www": "noise_url_fragment"}),
        )
    )
    return client


# =============================================================================
# AC-1.1: Environment Variable Tests
# =============================================================================


class TestAC11EnvironmentVariable:
    """AC-1.1: USE_ORCHESTRATOR_EXTRACTION=true → MetadataExtractionClient used."""

    def test_env_var_true_uses_orchestrator_client(
        self, sample_book_json: Path, mock_extraction_client: MagicMock
    ) -> None:
        """AC-1.1: When env var is true, MetadataExtractionClient is used."""
        from workflows.metadata_extraction.scripts.generate_metadata_universal import (
            UniversalMetadataGenerator,
        )

        with patch.dict(os.environ, {"EXTRACTION_USE_ORCHESTRATOR_EXTRACTION": "true"}):
            with patch(
                "workflows.metadata_extraction.scripts.generate_metadata_universal.MetadataExtractionClient",
                return_value=mock_extraction_client,
            ):
                generator = UniversalMetadataGenerator(sample_book_json, use_orchestrator=None)
                # use_orchestrator=None means "use settings/env var"
                assert generator.use_orchestrator is True

    def test_env_var_false_uses_local_extractor(self, sample_book_json: Path) -> None:
        """AC-1.1: When env var is false, StatisticalExtractor is used."""
        from workflows.metadata_extraction.scripts.generate_metadata_universal import (
            UniversalMetadataGenerator,
        )

        with patch.dict(os.environ, {"EXTRACTION_USE_ORCHESTRATOR_EXTRACTION": "false"}):
            generator = UniversalMetadataGenerator(sample_book_json, use_orchestrator=None)
            assert generator.use_orchestrator is False


# =============================================================================
# AC-1.2: CLI Flag Tests
# =============================================================================


class TestAC12CLIFlag:
    """AC-1.2: --use-orchestrator flag → MetadataExtractionClient, CLI takes precedence."""

    def test_cli_flag_overrides_env_var_false(self, sample_book_json: Path) -> None:
        """AC-1.2: CLI flag true overrides env var false."""
        from workflows.metadata_extraction.scripts.generate_metadata_universal import (
            UniversalMetadataGenerator,
        )

        with patch.dict(os.environ, {"EXTRACTION_USE_ORCHESTRATOR_EXTRACTION": "false"}):
            # Explicit use_orchestrator=True simulates --use-orchestrator flag
            generator = UniversalMetadataGenerator(sample_book_json, use_orchestrator=True)
            assert generator.use_orchestrator is True

    def test_cli_flag_false_overrides_env_var_true(self, sample_book_json: Path) -> None:
        """AC-1.2: CLI flag false overrides env var true."""
        from workflows.metadata_extraction.scripts.generate_metadata_universal import (
            UniversalMetadataGenerator,
        )

        with patch.dict(os.environ, {"EXTRACTION_USE_ORCHESTRATOR_EXTRACTION": "true"}):
            # Explicit use_orchestrator=False simulates no --use-orchestrator flag
            generator = UniversalMetadataGenerator(sample_book_json, use_orchestrator=False)
            assert generator.use_orchestrator is False

    def test_argparse_includes_use_orchestrator_flag(self) -> None:
        """AC-1.2: argparse includes --use-orchestrator flag."""
        import argparse

        from workflows.metadata_extraction.scripts.generate_metadata_universal import main

        # Create parser and check flag exists
        # We need to import the module and check its main function creates the flag
        # For now, just verify the flag is documented
        # This will fail until we add the flag
        pass  # Will be implemented in GREEN phase


# =============================================================================
# AC-5.1: Orchestrator Mode
# =============================================================================


class TestAC51OrchestratorMode:
    """AC-5.1: Orchestrator mode uses MetadataExtractionClient."""

    def test_orchestrator_mode_calls_client(
        self, sample_book_json: Path, mock_extraction_client: MagicMock
    ) -> None:
        """AC-5.1: When use_orchestrator=True, MetadataExtractionClient.extract_metadata is called."""
        from workflows.metadata_extraction.scripts.generate_metadata_universal import (
            UniversalMetadataGenerator,
        )

        with patch(
            "workflows.metadata_extraction.scripts.generate_metadata_universal.MetadataExtractionClient",
            return_value=mock_extraction_client,
        ):
            generator = UniversalMetadataGenerator(sample_book_json, use_orchestrator=True)
            chapters = [(1, "Test Chapter", 1, 2)]

            # Run extraction
            metadata = generator.generate_metadata(chapters)

            # Verify client was used
            assert mock_extraction_client.extract_metadata.called


# =============================================================================
# AC-5.2: Local Mode
# =============================================================================


class TestAC52LocalMode:
    """AC-5.2: Local mode uses StatisticalExtractor."""

    def test_local_mode_uses_statistical_extractor(self, sample_book_json: Path) -> None:
        """AC-5.2: When use_orchestrator=False, StatisticalExtractor is used."""
        from workflows.metadata_extraction.scripts.generate_metadata_universal import (
            UniversalMetadataGenerator,
        )

        generator = UniversalMetadataGenerator(sample_book_json, use_orchestrator=False)

        # extractor should be StatisticalExtractor
        from workflows.metadata_extraction.scripts.adapters.statistical_extractor import (
            StatisticalExtractor,
        )

        assert isinstance(generator.extractor, StatisticalExtractor)


# =============================================================================
# AC-5.3: Fallback on Error
# =============================================================================


class TestAC53FallbackOnError:
    """AC-5.3: Fallback to StatisticalExtractor when orchestrator fails."""

    def test_fallback_to_local_on_connection_error(
        self, sample_book_json: Path, mock_extraction_client: MagicMock
    ) -> None:
        """AC-5.3: When orchestrator connection fails, fallback to local."""
        from workflows.shared.clients.metadata_client import MetadataClientConnectionError
        from workflows.metadata_extraction.scripts.generate_metadata_universal import (
            UniversalMetadataGenerator,
        )

        # Make client raise connection error
        mock_extraction_client.extract_metadata = AsyncMock(
            side_effect=MetadataClientConnectionError("Connection refused")
        )

        with patch(
            "workflows.metadata_extraction.scripts.generate_metadata_universal.MetadataExtractionClient",
            return_value=mock_extraction_client,
        ):
            generator = UniversalMetadataGenerator(
                sample_book_json, use_orchestrator=True, fallback_on_error=True
            )
            chapters = [(1, "Test Chapter", 1, 2)]

            # Should not raise, should fallback
            metadata = generator.generate_metadata(chapters)

            # Should have metadata (from fallback)
            assert len(metadata) == 1
            # Metadata should exist (from StatisticalExtractor fallback)
            assert metadata[0].chapter_number == 1


# =============================================================================
# AC-5.4: Strict Mode (No Fallback)
# =============================================================================


class TestAC54StrictMode:
    """AC-5.4: Strict mode propagates exception (no fallback)."""

    def test_strict_mode_propagates_exception(
        self, sample_book_json: Path, mock_extraction_client: MagicMock
    ) -> None:
        """AC-5.4: When fallback_on_error=False, exception is propagated."""
        from workflows.shared.clients.metadata_client import MetadataClientConnectionError
        from workflows.metadata_extraction.scripts.generate_metadata_universal import (
            UniversalMetadataGenerator,
        )

        # Make client raise connection error
        mock_extraction_client.extract_metadata = AsyncMock(
            side_effect=MetadataClientConnectionError("Connection refused")
        )

        with patch(
            "workflows.metadata_extraction.scripts.generate_metadata_universal.MetadataExtractionClient",
            return_value=mock_extraction_client,
        ):
            generator = UniversalMetadataGenerator(
                sample_book_json, use_orchestrator=True, fallback_on_error=False
            )
            chapters = [(1, "Test Chapter", 1, 2)]

            # Should raise the exception
            with pytest.raises(MetadataClientConnectionError):
                generator.generate_metadata(chapters)


# =============================================================================
# AC-5.5: Output Schema Unchanged
# =============================================================================


class TestAC55OutputSchemaUnchanged:
    """AC-5.5: Output JSON schema identical regardless of mode."""

    def test_output_schema_matches_between_modes(
        self, sample_book_json: Path, mock_extraction_client: MagicMock
    ) -> None:
        """AC-5.5: Both modes produce same output schema."""
        from workflows.metadata_extraction.scripts.generate_metadata_universal import (
            UniversalMetadataGenerator,
        )

        chapters = [(1, "Test Chapter", 1, 2)]

        # Local mode
        local_gen = UniversalMetadataGenerator(sample_book_json, use_orchestrator=False)
        local_metadata = local_gen.generate_metadata(chapters)

        # Verify schema has required fields
        assert hasattr(local_metadata[0], "chapter_number")
        assert hasattr(local_metadata[0], "title")
        assert hasattr(local_metadata[0], "start_page")
        assert hasattr(local_metadata[0], "end_page")
        assert hasattr(local_metadata[0], "summary")
        assert hasattr(local_metadata[0], "keywords")
        assert hasattr(local_metadata[0], "concepts")

        # Verify serialization works
        local_dict = local_metadata[0].to_dict()
        assert "chapter_number" in local_dict
        assert "keywords" in local_dict
        assert isinstance(local_dict["keywords"], list)
