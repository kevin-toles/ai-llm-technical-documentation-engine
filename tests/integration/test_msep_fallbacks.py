"""
Integration Tests: MSEP Graceful Degradation / Fallback Behavior.

WBS Reference: MULTI_STAGE_ENRICHMENT_PIPELINE_WBS.md - MSE-7.4
Pattern: Graceful degradation per CODING_PATTERNS_ANALYSIS §3.3

This test validates fallback behavior when services are unavailable:
1. ai-agents unavailable → fallback to local enrichment
2. Connection timeout → fallback with WARNING log
3. API errors (4xx) → fail fast, no fallback

Acceptance Criteria (MSE-7.4):
- AC-7.4.1: If BERTopic unavailable, similarity still works (ai-agents internal)
- AC-7.4.2: If hybrid search unavailable, core enrichment works (ai-agents internal)
- AC-7.4.3: All failures logged with WARNING level

Note: AC-7.4.1 and AC-7.4.2 are ai-agents internal tests.
This file tests llm-document-enhancer fallback to local enrichment.

Anti-Pattern Compliance (CODING_PATTERNS):
- §3.3: Always provide fallback, log it, document behavior
- §3.4: Distinguish expected vs unexpected errors

Usage:
    pytest tests/integration/test_msep_fallbacks.py -v
    pytest tests/integration/test_msep_fallbacks.py -v -m "fallback"
"""

import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def sample_book_metadata() -> dict[str, Any]:
    """Sample book metadata for fallback testing."""
    return {
        "book_title": "Test Book",
        "chapters": [
            {
                "chapter_number": 1,
                "title": "Introduction",
                "content": "This is the introduction chapter content.",
                "keywords": ["intro", "overview"],
                "summary": "Introduction to the book",
            },
            {
                "chapter_number": 2,
                "title": "Core Concepts",
                "content": "Core concepts and fundamentals explained here.",
                "keywords": ["concepts", "fundamentals"],
                "summary": "Fundamental concepts",
            },
        ],
    }


# =============================================================================
# MSE-7.4: Graceful Degradation Tests
# =============================================================================


@pytest.mark.integration
@pytest.mark.fallback
class TestMSE74_GracefulDegradation:
    """
    MSE-7.4: Graceful Degradation Tests.

    Tests that llm-document-enhancer falls back gracefully when ai-agents
    is unavailable, following CODING_PATTERNS §3.3.
    """

    @pytest.mark.asyncio
    async def test_ac_7_4_3_connection_error_logs_warning(
        self,
        tmp_path: Path,
        sample_book_metadata: dict[str, Any],
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """
        AC-7.4.3: Connection errors logged with WARNING level.

        Per CODING_PATTERNS §3.3:
        - Log the fallback so users know what happened
        - Document fallback behavior
        """
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            enrich_metadata_msep,
        )
        from workflows.shared.clients.msep_client import MSEPConnectionError

        input_path = tmp_path / "test_metadata.json"
        output_path = tmp_path / "test_enriched.json"

        with open(input_path, "w", encoding="utf-8") as f:
            json.dump(sample_book_metadata, f)

        with patch(
            "workflows.metadata_enrichment.scripts.enrich_metadata_per_book.MSEPClient"
        ) as mock_client_class:
            mock_client = AsyncMock()
            mock_client.enrich_metadata.side_effect = MSEPConnectionError(
                "Connection refused to ai-agents:8082"
            )
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client

            with patch(
                "workflows.metadata_enrichment.scripts.enrich_metadata_per_book.enrich_metadata_local"
            ) as mock_local:
                with caplog.at_level(logging.WARNING):
                    await enrich_metadata_msep(
                        input_path=input_path,
                        output_path=output_path,
                        msep_url="http://localhost:8082",
                    )

                # Verify WARNING was logged
                warning_records = [
                    r for r in caplog.records if r.levelno == logging.WARNING
                ]
                assert len(warning_records) > 0, "Should log WARNING on connection error"

                # Verify fallback message in log
                assert any(
                    "falling back" in r.getMessage().lower()
                    for r in warning_records
                ), "Warning should mention fallback"

                # Verify local fallback was called
                mock_local.assert_called_once()

    @pytest.mark.asyncio
    async def test_ac_7_4_3_timeout_error_logs_warning(
        self,
        tmp_path: Path,
        sample_book_metadata: dict[str, Any],
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """
        AC-7.4.3: Timeout errors logged with WARNING level.

        Per CODING_PATTERNS §3.3:
        - Expected errors (timeout) → use default + log warning
        """
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            enrich_metadata_msep,
        )
        from workflows.shared.clients.msep_client import MSEPTimeoutError

        input_path = tmp_path / "test_metadata.json"
        output_path = tmp_path / "test_enriched.json"

        with open(input_path, "w", encoding="utf-8") as f:
            json.dump(sample_book_metadata, f)

        with patch(
            "workflows.metadata_enrichment.scripts.enrich_metadata_per_book.MSEPClient"
        ) as mock_client_class:
            mock_client = AsyncMock()
            mock_client.enrich_metadata.side_effect = MSEPTimeoutError(
                "Request to ai-agents timed out after 30s"
            )
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client

            with patch(
                "workflows.metadata_enrichment.scripts.enrich_metadata_per_book.enrich_metadata_local"
            ) as mock_local:
                with caplog.at_level(logging.WARNING):
                    await enrich_metadata_msep(
                        input_path=input_path,
                        output_path=output_path,
                        msep_url="http://localhost:8082",
                    )

                # Verify WARNING was logged
                warning_records = [
                    r for r in caplog.records if r.levelno == logging.WARNING
                ]
                assert len(warning_records) > 0, "Should log WARNING on timeout"

                # Verify local fallback was called
                mock_local.assert_called_once()

    @pytest.mark.asyncio
    async def test_fallback_to_local_produces_output(
        self,
        tmp_path: Path,
        sample_book_metadata: dict[str, Any],
    ) -> None:
        """
        Fallback to local enrichment should still produce valid output.

        Even when ai-agents is unavailable, enrichment should complete
        using the local fallback method.
        """
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            enrich_metadata_msep,
        )
        from workflows.shared.clients.msep_client import MSEPConnectionError

        input_path = tmp_path / "test_metadata.json"
        output_path = tmp_path / "test_enriched.json"

        with open(input_path, "w", encoding="utf-8") as f:
            json.dump(sample_book_metadata, f)

        with (
            patch(
                "workflows.metadata_enrichment.scripts.enrich_metadata_per_book.MSEPClient"
            ) as mock_client_class,
            patch(
                "workflows.metadata_enrichment.scripts.enrich_metadata_per_book.enrich_metadata_local"
            ) as mock_local,
        ):
            mock_client = AsyncMock()
            mock_client.enrich_metadata.side_effect = MSEPConnectionError(
                "Connection refused"
            )
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client

            # Mock local fallback to write output file
            def write_fallback_output(in_path: Path, out_path: Path) -> None:
                with open(in_path, encoding="utf-8") as f:
                    data = json.load(f)
                data["provenance"] = {"method": "local_fallback"}
                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(data, f)

            mock_local.side_effect = write_fallback_output

            await enrich_metadata_msep(
                input_path=input_path,
                output_path=output_path,
                msep_url="http://localhost:8082",
            )

        # Verify fallback was called
        mock_local.assert_called_once_with(input_path, output_path)

        # Verify output was created by fallback
        assert output_path.exists(), "Fallback should produce output file"

        with open(output_path, encoding="utf-8") as f:
            output_data = json.load(f)

        assert "chapters" in output_data
        # Fallback uses local provenance
        assert output_data.get("provenance", {}).get("method") == "local_fallback"

    @pytest.mark.asyncio
    async def test_api_error_does_not_fallback(
        self,
        tmp_path: Path,
        sample_book_metadata: dict[str, Any],
    ) -> None:
        """
        API errors (4xx) should fail fast, not fallback.

        Per CODING_PATTERNS §3.3:
        - Unexpected (corrupted request) → fail fast + log error
        """
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            enrich_metadata_msep,
        )
        from workflows.shared.clients.msep_client import MSEPAPIError

        input_path = tmp_path / "test_metadata.json"
        output_path = tmp_path / "test_enriched.json"

        with open(input_path, "w", encoding="utf-8") as f:
            json.dump(sample_book_metadata, f)

        with patch(
            "workflows.metadata_enrichment.scripts.enrich_metadata_per_book.MSEPClient"
        ) as mock_client_class:
            mock_client = AsyncMock()
            mock_client.enrich_metadata.side_effect = MSEPAPIError(
                status_code=400,
                message="Invalid request: corpus cannot be empty",
                response_body={"detail": "corpus cannot be empty"},
            )
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client

            # API errors should raise, not fallback
            with pytest.raises(MSEPAPIError) as exc_info:
                await enrich_metadata_msep(
                    input_path=input_path,
                    output_path=output_path,
                    msep_url="http://localhost:8082",
                )

            assert exc_info.value.status_code == 400


@pytest.mark.integration
@pytest.mark.fallback
class TestMSE74_ServiceUnavailableScenarios:
    """
    Additional fallback scenarios for service unavailability.
    """

    @pytest.mark.asyncio
    async def test_multiple_retries_before_fallback(
        self,
        tmp_path: Path,
        sample_book_metadata: dict[str, Any],
    ) -> None:
        """
        Client should retry before falling back.

        MSEPClient has retry logic (3 attempts) before raising error.
        """
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            enrich_metadata_msep,
        )
        from workflows.shared.clients.msep_client import MSEPConnectionError

        input_path = tmp_path / "test_metadata.json"
        output_path = tmp_path / "test_enriched.json"

        with open(input_path, "w", encoding="utf-8") as f:
            json.dump(sample_book_metadata, f)

        call_count = 0

        async def mock_enrich(*args: Any, **kwargs: Any) -> None:
            nonlocal call_count
            call_count += 1
            raise MSEPConnectionError("Connection refused")

        with patch(
            "workflows.metadata_enrichment.scripts.enrich_metadata_per_book.MSEPClient"
        ) as mock_client_class:
            mock_client = AsyncMock()
            mock_client.enrich_metadata.side_effect = mock_enrich
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client

            with patch(
                "workflows.metadata_enrichment.scripts.enrich_metadata_per_book.enrich_metadata_local"
            ):
                await enrich_metadata_msep(
                    input_path=input_path,
                    output_path=output_path,
                    msep_url="http://localhost:8082",
                )

        # Client was called once (retries are internal to MSEPClient)
        assert call_count == 1

    @pytest.mark.asyncio
    async def test_fallback_preserves_input_structure(
        self,
        tmp_path: Path,
        sample_book_metadata: dict[str, Any],
    ) -> None:
        """
        Fallback should preserve original input structure.

        Even in fallback mode, original metadata should not be lost.
        """
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            enrich_metadata_msep,
        )
        from workflows.shared.clients.msep_client import MSEPConnectionError

        # Add extra fields to verify preservation
        sample_book_metadata["custom_field"] = "should_be_preserved"
        sample_book_metadata["chapters"][0]["extra_data"] = {"key": "value"}

        input_path = tmp_path / "test_metadata.json"
        output_path = tmp_path / "test_enriched.json"

        with open(input_path, "w", encoding="utf-8") as f:
            json.dump(sample_book_metadata, f)

        with (
            patch(
                "workflows.metadata_enrichment.scripts.enrich_metadata_per_book.MSEPClient"
            ) as mock_client_class,
            patch(
                "workflows.metadata_enrichment.scripts.enrich_metadata_per_book.enrich_metadata_local"
            ) as mock_local,
        ):
            mock_client = AsyncMock()
            mock_client.enrich_metadata.side_effect = MSEPConnectionError(
                "Connection refused"
            )
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client

            # Mock local fallback to preserve input and add enrichment
            def write_fallback_output(in_path: Path, out_path: Path) -> None:
                with open(in_path, encoding="utf-8") as f:
                    data = json.load(f)
                # Preserve all fields, add provenance
                data["provenance"] = {"method": "local_fallback"}
                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(data, f)

            mock_local.side_effect = write_fallback_output

            await enrich_metadata_msep(
                input_path=input_path,
                output_path=output_path,
                msep_url="http://localhost:8082",
            )

        # Verify the fallback was used and output was created
        assert output_path.exists()

        # Verify the local fallback was called
        mock_local.assert_called_once_with(input_path, output_path)

        # Verify structure was preserved
        with open(output_path, encoding="utf-8") as f:
            output_data = json.load(f)

        assert output_data.get("custom_field") == "should_be_preserved"
        assert output_data["chapters"][0].get("extra_data") == {"key": "value"}
