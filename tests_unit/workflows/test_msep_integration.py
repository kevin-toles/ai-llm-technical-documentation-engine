"""
Unit tests for MSE-6.2 and MSE-6.3: MSEP Integration with Enrichment Workflow.

WBS References:
- MSE-6.2: Integration with Enrichment Workflow
  - AC-6.2.1: `enrich_metadata_per_book.py` uses `MSEPClient` when `--use-msep` flag
  - AC-6.2.2: Fallback to existing local enrichment when ai-agents unavailable
  - AC-6.2.3: No enrichment logic in llm-document-enhancer (verified by MSE-6.4)
- MSE-6.3: Response Handling
  - AC-6.3.1: Writes `{book}_enriched.json` with MSEP results
  - AC-6.3.2: Preserves existing metadata structure
  - AC-6.3.3: Adds provenance to output JSON

Architecture Pattern:
- Kitchen Brigade: llm-document-enhancer (CUSTOMER) → ai-agents (EXPEDITOR)
- CUSTOMER delegates ALL enrichment to EXPEDITOR
- Fallback to local ONLY when ai-agents unavailable

Anti-Patterns Avoided (CODING_PATTERNS):
- §3.3: Always provide fallback, log it, document behavior
- S1172: No unused parameters
- S3776: Cognitive complexity < 15

TDD Phase: RED - Write failing tests first
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import aiofiles
import pytest

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# =============================================================================
# MSE-6.2: Integration with Enrichment Workflow Tests
# =============================================================================


class TestMSE62UseMSEPFlag:
    """
    AC-6.2.1: `enrich_metadata_per_book.py` uses `MSEPClient` when `--use-msep` flag.

    Tests the CLI argument parsing and routing to MSEP integration.
    """

    def test_create_argument_parser_has_use_msep_flag(self) -> None:
        """Parser should accept --use-msep flag."""
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            create_argument_parser,
        )

        parser = create_argument_parser()
        # Parse with --use-msep flag
        args = parser.parse_args([
            "--input", "test.json",
            "--output", "out.json",
            "--use-msep",
        ])

        assert args.use_msep is True

    def test_create_argument_parser_has_msep_url_flag(self) -> None:
        """Parser should accept --msep-url flag with default."""
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            create_argument_parser,
        )

        parser = create_argument_parser()
        # Parse without explicit URL - should use default
        args = parser.parse_args([
            "--input", "test.json",
            "--output", "out.json",
            "--use-msep",
        ])

        assert args.msep_url == "http://localhost:8082"

    def test_create_argument_parser_custom_msep_url(self) -> None:
        """Parser should accept custom --msep-url value."""
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            create_argument_parser,
        )

        parser = create_argument_parser()
        args = parser.parse_args([
            "--input", "test.json",
            "--output", "out.json",
            "--use-msep",
            "--msep-url", "http://custom-agent:9000",
        ])

        assert args.msep_url == "http://custom-agent:9000"

    def test_use_msep_flag_defaults_to_false(self) -> None:
        """--use-msep flag should default to False when not specified."""
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            create_argument_parser,
        )

        parser = create_argument_parser()
        args = parser.parse_args([
            "--input", "test.json",
            "--output", "out.json",
        ])

        assert args.use_msep is False


class TestMSE62MSEPClientIntegration:
    """
    AC-6.2.1: enrich_metadata_per_book.py routes to MSEPClient.

    Tests that the main function routes to enrich_metadata_msep when --use-msep.
    """

    def test_enrich_metadata_msep_function_exists(self) -> None:
        """enrich_metadata_msep async function should exist."""
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            enrich_metadata_msep,
        )

        assert callable(enrich_metadata_msep)
        assert asyncio.iscoroutinefunction(enrich_metadata_msep)

    def test_msep_client_available_constant_exists(self) -> None:
        """MSEP_CLIENT_AVAILABLE constant should exist for import checking."""
        from workflows.metadata_enrichment.scripts import enrich_metadata_per_book

        assert hasattr(enrich_metadata_per_book, "MSEP_CLIENT_AVAILABLE")

    @pytest.mark.asyncio
    async def test_enrich_metadata_msep_calls_client(
        self, tmp_path: Path
    ) -> None:
        """enrich_metadata_msep should use MSEPClient to call ai-agents."""
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            enrich_metadata_msep,
        )
        from workflows.shared.clients.msep_client import (
            EnrichedMetadataResponse,
            EnrichedChapter,
            CrossReference,
            MergedKeywords,
            Provenance,
        )

        # Create sample input file
        input_data = {
            "book_title": "Test Book",
            "chapters": [
                {
                    "chapter_number": 1,
                    "title": "Introduction",
                    "content": "This is chapter 1 content about testing.",
                    "keywords": ["test", "intro"],
                    "summary": "Introduction chapter",
                }
            ],
        }
        input_path = tmp_path / "test_metadata.json"
        output_path = tmp_path / "test_enriched.json"

        async with aiofiles.open(input_path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(input_data))

        # Mock MSEP response
        mock_response = EnrichedMetadataResponse(
            chapters=[
                EnrichedChapter(
                    chapter_id="Test Book::1",
                    cross_references=[
                        CrossReference(
                            target="Other Book::2",
                            score=0.85,
                            base_score=0.80,
                            topic_boost=0.05,
                            method="sbert",
                        )
                    ],
                    keywords=MergedKeywords(
                        tfidf=["test"],
                        semantic=["testing"],
                        merged=["test", "testing"],
                    ),
                    topic_id=1,
                    provenance=Provenance(
                        methods_used=["sbert", "tfidf"],
                        sbert_score=0.85,
                        topic_boost=0.05,
                        timestamp="2025-01-01T00:00:00Z",
                    ),
                )
            ],
            processing_time_ms=150.0,
            total_cross_references=1,
        )

        # Patch MSEPClient
        with patch(
            "workflows.metadata_enrichment.scripts.enrich_metadata_per_book.MSEPClient"
        ) as mock_client_class:
            mock_client = AsyncMock()
            mock_client.enrich_metadata.return_value = mock_response
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client

            await enrich_metadata_msep(
                input_path=input_path,
                output_path=output_path,
                msep_url="http://localhost:8082",
            )

            # Verify MSEPClient was called with correct signature
            mock_client.enrich_metadata.assert_called_once()
            call_kwargs = mock_client.enrich_metadata.call_args
            # Should have corpus, chapter_index, config args
            assert "corpus" in call_kwargs.kwargs or len(call_kwargs.args) >= 1


class TestMSE62Fallback:
    """
    AC-6.2.2: Fallback to existing local enrichment when ai-agents unavailable.

    Per CODING_PATTERNS §3.3:
    - Always provide fallback
    - Log the fallback
    - Document fallback behavior
    """

    @pytest.mark.asyncio
    async def test_fallback_on_connection_error(self, tmp_path: Path) -> None:
        """Should fallback to local when MSEPConnectionError."""
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            enrich_metadata_msep,
        )
        from workflows.shared.clients.msep_client import MSEPConnectionError

        # Create sample input
        input_data = {
            "book_title": "Test Book",
            "chapters": [
                {
                    "chapter_number": 1,
                    "title": "Introduction",
                    "content": "Chapter content",
                    "keywords": ["test"],
                    "summary": "Test summary",
                }
            ],
        }
        input_path = tmp_path / "test_metadata.json"
        output_path = tmp_path / "test_enriched.json"

        async with aiofiles.open(input_path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(input_data))

        # Patch MSEPClient to raise connection error
        with patch(
            "workflows.metadata_enrichment.scripts.enrich_metadata_per_book.MSEPClient"
        ) as mock_client_class:
            mock_client = AsyncMock()
            mock_client.enrich_metadata.side_effect = MSEPConnectionError(
                "Connection refused"
            )
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client

            # Patch local fallback
            with patch(
                "workflows.metadata_enrichment.scripts.enrich_metadata_per_book.enrich_metadata_local"
            ) as mock_local:
                await enrich_metadata_msep(
                    input_path=input_path,
                    output_path=output_path,
                    msep_url="http://localhost:8082",
                )

                # Should have called local fallback
                mock_local.assert_called_once()

    @pytest.mark.asyncio
    async def test_fallback_on_timeout_error(self, tmp_path: Path) -> None:
        """Should fallback to local when MSEPTimeoutError."""
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            enrich_metadata_msep,
        )
        from workflows.shared.clients.msep_client import MSEPTimeoutError

        input_data = {
            "book_title": "Test Book",
            "chapters": [
                {
                    "chapter_number": 1,
                    "title": "Introduction",
                    "content": "Chapter content",
                    "keywords": ["test"],
                    "summary": "Test summary",
                }
            ],
        }
        input_path = tmp_path / "test_metadata.json"
        output_path = tmp_path / "test_enriched.json"

        async with aiofiles.open(input_path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(input_data))

        with patch(
            "workflows.metadata_enrichment.scripts.enrich_metadata_per_book.MSEPClient"
        ) as mock_client_class:
            mock_client = AsyncMock()
            mock_client.enrich_metadata.side_effect = MSEPTimeoutError(
                "Request timed out"
            )
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client

            with patch(
                "workflows.metadata_enrichment.scripts.enrich_metadata_per_book.enrich_metadata_local"
            ) as mock_local:
                await enrich_metadata_msep(
                    input_path=input_path,
                    output_path=output_path,
                    msep_url="http://localhost:8082",
                )

                mock_local.assert_called_once()

    @pytest.mark.asyncio
    async def test_fallback_logs_warning(
        self, tmp_path: Path, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Should log warning when falling back to local (CODING_PATTERNS §3.3)."""
        import logging

        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            enrich_metadata_msep,
        )
        from workflows.shared.clients.msep_client import MSEPConnectionError

        input_data = {
            "book_title": "Test Book",
            "chapters": [
                {
                    "chapter_number": 1,
                    "title": "Introduction",
                    "content": "Chapter content",
                    "keywords": ["test"],
                    "summary": "Test summary",
                }
            ],
        }
        input_path = tmp_path / "test_metadata.json"
        output_path = tmp_path / "test_enriched.json"

        async with aiofiles.open(input_path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(input_data))

        with patch(
            "workflows.metadata_enrichment.scripts.enrich_metadata_per_book.MSEPClient"
        ) as mock_client_class:
            mock_client = AsyncMock()
            mock_client.enrich_metadata.side_effect = MSEPConnectionError(
                "Connection refused"
            )
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client

            with patch(
                "workflows.metadata_enrichment.scripts.enrich_metadata_per_book.enrich_metadata_local"
            ):
                with caplog.at_level(logging.WARNING):
                    await enrich_metadata_msep(
                        input_path=input_path,
                        output_path=output_path,
                        msep_url="http://localhost:8082",
                    )

                # Should have logged fallback warning (check for "falling back")
                assert any(
                    "falling back" in record.getMessage().lower()
                    for record in caplog.records
                ), f"Expected 'falling back' in log messages, got: {[r.getMessage() for r in caplog.records]}"


# =============================================================================
# MSE-6.3: Response Handling Tests
# =============================================================================


class TestMSE63OutputFile:
    """
    AC-6.3.1: Writes `{book}_enriched.json` with MSEP results.
    """

    @pytest.mark.asyncio
    async def test_writes_enriched_json_file(self, tmp_path: Path) -> None:
        """Should write enriched JSON to output path."""
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            enrich_metadata_msep,
        )
        from workflows.shared.clients.msep_client import (
            EnrichedMetadataResponse,
            EnrichedChapter,
            CrossReference,
            MergedKeywords,
            Provenance,
        )

        input_data = {
            "book_title": "Test Book",
            "chapters": [
                {
                    "chapter_number": 1,
                    "title": "Introduction",
                    "content": "Chapter content",
                    "keywords": ["test"],
                    "summary": "Test summary",
                }
            ],
        }
        input_path = tmp_path / "test_metadata.json"
        output_path = tmp_path / "test_enriched.json"

        async with aiofiles.open(input_path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(input_data))

        mock_response = EnrichedMetadataResponse(
            chapters=[
                EnrichedChapter(
                    chapter_id="Test Book::1",
                    cross_references=[],
                    keywords=MergedKeywords(
                        tfidf=["test"],
                        semantic=["testing"],
                        merged=["test", "testing"],
                    ),
                    topic_id=1,
                    provenance=Provenance(
                        methods_used=["sbert"],
                        sbert_score=0.0,
                        topic_boost=0.0,
                        timestamp="2025-01-01T00:00:00Z",
                    ),
                )
            ],
            processing_time_ms=100.0,
            total_cross_references=0,
        )

        with patch(
            "workflows.metadata_enrichment.scripts.enrich_metadata_per_book.MSEPClient"
        ) as mock_client_class:
            mock_client = AsyncMock()
            mock_client.enrich_metadata.return_value = mock_response
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client

            await enrich_metadata_msep(
                input_path=input_path,
                output_path=output_path,
                msep_url="http://localhost:8082",
            )

        # Verify output file exists
        assert output_path.exists()

        # Verify JSON content
        async with aiofiles.open(output_path, encoding="utf-8") as f:
            content = await f.read()
            output_data = json.loads(content)

        assert "chapters" in output_data


class TestMSE63MetadataPreservation:
    """
    AC-6.3.2: Preserves existing metadata structure.

    Merged output should contain original metadata fields plus enrichment.
    """

    @pytest.mark.asyncio
    async def test_preserves_original_metadata_fields(self, tmp_path: Path) -> None:
        """Original metadata fields should be preserved in output."""
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            enrich_metadata_msep,
        )
        from workflows.shared.clients.msep_client import (
            EnrichedMetadataResponse,
            EnrichedChapter,
            CrossReference,
            MergedKeywords,
            Provenance,
        )

        input_data = {
            "book_title": "Test Book",
            "author": "Test Author",
            "custom_field": "should_be_preserved",
            "chapters": [
                {
                    "chapter_number": 1,
                    "title": "Introduction",
                    "content": "Chapter content",
                    "keywords": ["original_keyword"],
                    "summary": "Original summary",
                    "start_page": 1,
                    "end_page": 25,
                }
            ],
        }
        input_path = tmp_path / "test_metadata.json"
        output_path = tmp_path / "test_enriched.json"

        async with aiofiles.open(input_path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(input_data))

        mock_response = EnrichedMetadataResponse(
            chapters=[
                EnrichedChapter(
                    chapter_id="Test Book::1",
                    cross_references=[],
                    keywords=MergedKeywords(
                        tfidf=["test"],
                        semantic=["testing"],
                        merged=["test", "testing"],
                    ),
                    topic_id=1,
                    provenance=Provenance(
                        methods_used=["sbert"],
                        sbert_score=0.0,
                        topic_boost=0.0,
                        timestamp="2025-01-01T00:00:00Z",
                    ),
                )
            ],
            processing_time_ms=100.0,
            total_cross_references=0,
        )

        with patch(
            "workflows.metadata_enrichment.scripts.enrich_metadata_per_book.MSEPClient"
        ) as mock_client_class:
            mock_client = AsyncMock()
            mock_client.enrich_metadata.return_value = mock_response
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client

            await enrich_metadata_msep(
                input_path=input_path,
                output_path=output_path,
                msep_url="http://localhost:8082",
            )

        async with aiofiles.open(output_path, encoding="utf-8") as f:
            content = await f.read()
            output_data = json.loads(content)

        # Book-level fields preserved
        assert output_data.get("book_title") == "Test Book"
        assert output_data.get("author") == "Test Author"
        assert output_data.get("custom_field") == "should_be_preserved"

        # Chapter-level fields preserved
        chapter = output_data["chapters"][0]
        assert chapter.get("chapter_number") == 1
        assert chapter.get("title") == "Introduction"
        assert chapter.get("start_page") == 1
        assert chapter.get("end_page") == 25


class TestMSE63Provenance:
    """
    AC-6.3.3: Adds provenance to output JSON.

    Output should include enrichment_provenance field with method and source info.
    """

    @pytest.mark.asyncio
    async def test_adds_enrichment_provenance(self, tmp_path: Path) -> None:
        """Output should have enrichment_provenance field."""
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            enrich_metadata_msep,
        )
        from workflows.shared.clients.msep_client import (
            EnrichedMetadataResponse,
            EnrichedChapter,
            CrossReference,
            MergedKeywords,
            Provenance,
        )

        input_data = {
            "book_title": "Test Book",
            "chapters": [
                {
                    "chapter_number": 1,
                    "title": "Introduction",
                    "content": "Chapter content",
                    "keywords": ["test"],
                    "summary": "Test summary",
                }
            ],
        }
        input_path = tmp_path / "test_metadata.json"
        output_path = tmp_path / "test_enriched.json"

        async with aiofiles.open(input_path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(input_data))

        mock_response = EnrichedMetadataResponse(
            chapters=[
                EnrichedChapter(
                    chapter_id="Test Book::1",
                    cross_references=[],
                    keywords=MergedKeywords(
                        tfidf=["test"],
                        semantic=["testing"],
                        merged=["test", "testing"],
                    ),
                    topic_id=1,
                    provenance=Provenance(
                        methods_used=["sbert", "bertopic"],
                        sbert_score=0.85,
                        topic_boost=0.05,
                        timestamp="2025-01-01T00:00:00Z",
                    ),
                )
            ],
            processing_time_ms=150.0,
            total_cross_references=0,
        )

        with patch(
            "workflows.metadata_enrichment.scripts.enrich_metadata_per_book.MSEPClient"
        ) as mock_client_class:
            mock_client = AsyncMock()
            mock_client.enrich_metadata.return_value = mock_response
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client

            await enrich_metadata_msep(
                input_path=input_path,
                output_path=output_path,
                msep_url="http://localhost:8082",
            )

        async with aiofiles.open(output_path, encoding="utf-8") as f:
            content = await f.read()
            output_data = json.loads(content)

        # Top-level provenance
        assert "enrichment_provenance" in output_data
        provenance = output_data["enrichment_provenance"]
        assert provenance.get("enrichment_method") == "msep"
        assert "enrichment_date" in provenance
        assert provenance.get("source_metadata_file") == "test_metadata.json"

    @pytest.mark.asyncio
    async def test_chapter_provenance_from_response(self, tmp_path: Path) -> None:
        """Chapter-level provenance from MSEP response should be included."""
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            enrich_metadata_msep,
        )
        from workflows.shared.clients.msep_client import (
            EnrichedMetadataResponse,
            EnrichedChapter,
            CrossReference,
            MergedKeywords,
            Provenance,
        )

        input_data = {
            "book_title": "Test Book",
            "chapters": [
                {
                    "chapter_number": 1,
                    "title": "Introduction",
                    "content": "Chapter content",
                    "keywords": ["test"],
                    "summary": "Test summary",
                }
            ],
        }
        input_path = tmp_path / "test_metadata.json"
        output_path = tmp_path / "test_enriched.json"

        async with aiofiles.open(input_path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(input_data))

        mock_response = EnrichedMetadataResponse(
            chapters=[
                EnrichedChapter(
                    chapter_id="Test Book::1",
                    cross_references=[
                        CrossReference(
                            target="Other Book::2",
                            score=0.85,
                            base_score=0.80,
                            topic_boost=0.05,
                            method="sbert",
                        )
                    ],
                    keywords=MergedKeywords(
                        tfidf=["test"],
                        semantic=["testing"],
                        merged=["test", "testing"],
                    ),
                    topic_id=1,
                    provenance=Provenance(
                        methods_used=["sbert", "bertopic"],
                        sbert_score=0.85,
                        topic_boost=0.05,
                        timestamp="2025-01-01T00:00:00Z",
                    ),
                )
            ],
            processing_time_ms=150.0,
            total_cross_references=1,
        )

        with patch(
            "workflows.metadata_enrichment.scripts.enrich_metadata_per_book.MSEPClient"
        ) as mock_client_class:
            mock_client = AsyncMock()
            mock_client.enrich_metadata.return_value = mock_response
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client

            await enrich_metadata_msep(
                input_path=input_path,
                output_path=output_path,
                msep_url="http://localhost:8082",
            )

        async with aiofiles.open(output_path, encoding="utf-8") as f:
            content = await f.read()
            output_data = json.loads(content)

        # Chapter should have cross_references from MSEP
        chapter = output_data["chapters"][0]
        assert "cross_references" in chapter
        assert len(chapter["cross_references"]) > 0

        # Chapter should have enriched keywords
        assert "keywords" in chapter or "enriched_keywords" in chapter
