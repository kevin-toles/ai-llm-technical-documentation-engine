"""
Test MSEP API Client - WBS MSE-6.1 Unit Tests

Phase MSE-6: llm-document-enhancer Cleanup & API Client
TDD Testing for MSEP API Client

Reference Documents:
- ai-agents/src/api/routes/enrich_metadata.py: POST /v1/agents/enrich-metadata endpoint
- WBS MSE-6.1 AC-6.1.1: enrich_metadata(corpus, chapter_index, config) method
- CODING_PATTERNS_ANALYSIS: Anti-Pattern #12 (single httpx.AsyncClient)
- GUIDELINES p. 2313: Connection pooling (Newman)

Tests cover:
- AC-6.1.1: MSEPClient has enrich_metadata(corpus, chapter_index, config) method
- AC-6.1.2: Calls POST /v1/agents/enrich-metadata on ai-agents:8082 DIRECTLY
- AC-6.1.3: Returns EnrichedMetadata (or equivalent dict)
- AC-6.1.4: Handles timeout and errors gracefully
- AC-6.1.5: Default base_url is http://localhost:8082

Kitchen Brigade Pattern:
- llm-document-enhancer is CUSTOMER only
- Calls ai-agents MSEP endpoint via this client
- NO local ML processing
"""

from __future__ import annotations

import pytest
from typing import TYPE_CHECKING
from unittest.mock import AsyncMock, patch, MagicMock

import httpx


# =============================================================================
# TestMSEPClientInstantiation - AC-6.1.5
# =============================================================================


class TestMSEPClientInstantiation:
    """AC-6.1.5: Test client instantiates with correct defaults."""

    def test_client_default_base_url_is_8080(self) -> None:
        """AC-6.1.5: Default base_url is http://localhost:8080 (Gateway port, routes to ai-agents)."""
        from workflows.shared.clients.msep_client import MSEPClient

        client = MSEPClient()

        assert client.base_url == "http://localhost:8080"

    def test_client_instantiates_with_defaults(self) -> None:
        """AC-6.1.1: Client should instantiate with default configuration."""
        from workflows.shared.clients.msep_client import MSEPClient

        client = MSEPClient()

        assert client.timeout == pytest.approx(30.0)
        assert client._client is None  # Lazy initialization (connection pooling)

    def test_client_instantiates_with_custom_config(self) -> None:
        """Client should accept custom configuration."""
        from workflows.shared.clients.msep_client import MSEPClient

        client = MSEPClient(
            base_url="http://ai-agents:8082",
            timeout=60.0,
            max_connections=20,
        )

        assert client.base_url == "http://ai-agents:8082"
        assert client.timeout == pytest.approx(60.0)
        assert client.max_connections == 20

    def test_client_instantiates_from_env(self) -> None:
        """Client should read MSEP_BASE_URL from environment."""
        from workflows.shared.clients.msep_client import MSEPClient

        with patch.dict(
            "os.environ",
            {"MSEP_BASE_URL": "http://msep.local:8082"},
        ):
            client = MSEPClient()

            assert client.base_url == "http://msep.local:8082"

    def test_client_has_retry_config(self) -> None:
        """AC-6.1.4: Client should have retry configuration."""
        from workflows.shared.clients.msep_client import MSEPClient

        client = MSEPClient(max_retries=5, retry_delay=2.0)

        assert client.max_retries == 5
        assert client.retry_delay == pytest.approx(2.0)


# =============================================================================
# TestMSEPClientContextManager - AC-6.1.1 (connection pooling)
# =============================================================================


class TestMSEPClientContextManager:
    """AC-6.1.1: Test async context manager for connection pooling."""

    @pytest.mark.asyncio
    async def test_context_manager_creates_client(self) -> None:
        """Client should create httpx.AsyncClient on enter."""
        from workflows.shared.clients.msep_client import MSEPClient

        msep_client = MSEPClient()

        async with msep_client as client:
            assert client._client is not None
            assert isinstance(client._client, httpx.AsyncClient)

    @pytest.mark.asyncio
    async def test_context_manager_closes_client(self) -> None:
        """Client should close httpx.AsyncClient on exit."""
        from workflows.shared.clients.msep_client import MSEPClient

        msep_client = MSEPClient()

        async with msep_client as client:
            internal_client = client._client
            assert internal_client is not None

        # After context, _client should be None (closed)
        assert msep_client._client is None

    @pytest.mark.asyncio
    async def test_context_manager_returns_self(self) -> None:
        """Context manager should return client instance."""
        from workflows.shared.clients.msep_client import MSEPClient

        msep_client = MSEPClient()

        async with msep_client as client:
            assert client is msep_client

    @pytest.mark.asyncio
    async def test_connection_pooling_single_client(self) -> None:
        """Should reuse single httpx.AsyncClient (no per-request creation)."""
        from workflows.shared.clients.msep_client import MSEPClient

        msep_client = MSEPClient()

        async with msep_client as client:
            first_client = client._client
            # Multiple accesses should return same client
            second_client = client._client
            assert first_client is second_client


# =============================================================================
# TestMSEPClientEnrichMetadata - AC-6.1.1, AC-6.1.2, AC-6.1.3
# =============================================================================


class TestMSEPClientEnrichMetadata:
    """AC-6.1.1: Test enrich_metadata(corpus, chapter_index, config) method."""

    @pytest.mark.asyncio
    async def test_enrich_metadata_returns_response_dataclass(self) -> None:
        """AC-6.1.3: Should return EnrichedMetadataResponse dataclass."""
        from workflows.shared.clients.msep_client import (
            MSEPClient,
            EnrichedMetadataResponse,
            ChapterMeta,
        )

        # Mock response matching ai-agents EnrichMetadataResponse schema
        mock_response = {
            "chapters": [
                {
                    "chapter_id": "ch1",
                    "cross_references": [
                        {
                            "target": "Book2_Ch3",
                            "score": 0.85,
                            "base_score": 0.75,
                            "topic_boost": 0.10,
                            "method": "sbert",
                        }
                    ],
                    "keywords": {
                        "tfidf": ["pattern", "design"],
                        "semantic": ["architecture", "structure"],
                        "merged": ["pattern", "design", "architecture"],
                    },
                    "topic_id": 1,
                    "provenance": {
                        "methods_used": ["sbert", "topic_boost"],
                        "sbert_score": 0.85,
                        "topic_boost": 0.10,
                        "timestamp": "2025-01-16T12:00:00Z",
                    },
                }
            ],
            "processing_time_ms": 100.5,
            "total_cross_references": 1,
        }

        msep_client = MSEPClient()

        with patch.object(
            MSEPClient,
            "_post",
            new_callable=AsyncMock,
            return_value=mock_response,
        ):
            async with msep_client as client:
                response = await client.enrich_metadata(
                    corpus=["Chapter 1 content"],
                    chapter_index=[
                        ChapterMeta(book="TestBook", chapter=1, title="Introduction")
                    ],
                )

        assert isinstance(response, EnrichedMetadataResponse)
        assert len(response.chapters) == 1
        assert response.chapters[0].chapter_id == "ch1"
        assert response.chapters[0].keywords.merged == ["pattern", "design", "architecture"]

    @pytest.mark.asyncio
    async def test_enrich_metadata_sends_correct_payload(self) -> None:
        """AC-6.1.2: Should send correct request payload to /v1/agents/enrich-metadata."""
        from workflows.shared.clients.msep_client import MSEPClient, ChapterMeta, MSEPConfig

        mock_response = {
            "chapters": [],
            "processing_time_ms": 50.0,
            "total_cross_references": 0,
        }

        msep_client = MSEPClient()

        with patch.object(
            MSEPClient,
            "_post",
            new_callable=AsyncMock,
            return_value=mock_response,
        ) as mock_post:
            async with msep_client as client:
                await client.enrich_metadata(
                    corpus=["Ch1 content", "Ch2 content"],
                    chapter_index=[
                        ChapterMeta(book="ArchPatterns", chapter=1, title="Chapter 1", id="ch1"),
                        ChapterMeta(book="ArchPatterns", chapter=2, title="Chapter 2", id="ch2"),
                    ],
                    config=MSEPConfig(threshold=0.5, top_k=10),
                )

        # Verify endpoint
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert call_args[0][0] == "/v1/agents/enrich-metadata"

        # Verify payload structure matches ai-agents schema
        payload = call_args[1]["json"]
        assert payload["corpus"] == ["Ch1 content", "Ch2 content"]
        assert len(payload["chapter_index"]) == 2
        assert payload["chapter_index"][0]["book"] == "ArchPatterns"
        assert payload["chapter_index"][0]["chapter"] == 1
        assert payload["chapter_index"][0]["title"] == "Chapter 1"
        assert payload["chapter_index"][0]["id"] == "ch1"
        assert payload["config"]["threshold"] == pytest.approx(0.5)
        assert payload["config"]["top_k"] == 10

    @pytest.mark.asyncio
    async def test_enrich_metadata_optional_config(self) -> None:
        """AC-6.1.1: Config parameter should be optional."""
        from workflows.shared.clients.msep_client import MSEPClient, ChapterMeta

        mock_response = {
            "chapters": [],
            "processing_time_ms": 50.0,
            "total_cross_references": 0,
        }

        msep_client = MSEPClient()

        with patch.object(
            MSEPClient,
            "_post",
            new_callable=AsyncMock,
            return_value=mock_response,
        ) as mock_post:
            async with msep_client as client:
                await client.enrich_metadata(
                    corpus=["Content"],
                    chapter_index=[ChapterMeta(book="Book", chapter=1, title="Title")],
                    # config not provided - should be optional
                )

        # Config should not be in payload when not provided
        payload = mock_post.call_args[1]["json"]
        assert "config" not in payload

    @pytest.mark.asyncio
    async def test_enrich_metadata_validates_lengths(self) -> None:
        """Should raise ValueError if corpus and chapter_index lengths mismatch."""
        from workflows.shared.clients.msep_client import MSEPClient, ChapterMeta

        msep_client = MSEPClient()

        async with msep_client as client:
            with pytest.raises(ValueError) as exc_info:
                await client.enrich_metadata(
                    corpus=["Ch1", "Ch2", "Ch3"],  # 3 items
                    chapter_index=[
                        ChapterMeta(book="Book", chapter=1, title="Title")
                    ],  # 1 item
                )

        assert "must match" in str(exc_info.value)


# =============================================================================
# TestMSEPClientErrorHandling - AC-6.1.4
# =============================================================================


class TestMSEPClientErrorHandling:
    """AC-6.1.4: Test error handling."""

    @pytest.mark.asyncio
    async def test_timeout_raises_msep_timeout_error(self) -> None:
        """AC-6.1.4: Should raise MSEPTimeoutError on timeout."""
        from workflows.shared.clients.msep_client import (
            MSEPClient,
            MSEPTimeoutError,
            ChapterMeta,
        )

        msep_client = MSEPClient(timeout=0.1, max_retries=0)

        with patch.object(
            httpx.AsyncClient,
            "post",
            side_effect=httpx.TimeoutException("Request timed out"),
        ):
            async with msep_client as client:
                with pytest.raises(MSEPTimeoutError) as exc_info:
                    await client.enrich_metadata(
                        corpus=["Content"],
                        chapter_index=[ChapterMeta(book="Book", chapter=1, title="Title")],
                    )

        assert "timed out" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_connection_error_raises_msep_connection_error(self) -> None:
        """AC-6.1.4: Should raise MSEPConnectionError on connection failure."""
        from workflows.shared.clients.msep_client import (
            MSEPClient,
            MSEPConnectionError,
            ChapterMeta,
        )

        msep_client = MSEPClient(max_retries=0)

        with patch.object(
            httpx.AsyncClient,
            "post",
            side_effect=httpx.ConnectError("Connection refused"),
        ):
            async with msep_client as client:
                with pytest.raises(MSEPConnectionError) as exc_info:
                    await client.enrich_metadata(
                        corpus=["Content"],
                        chapter_index=[ChapterMeta(book="Book", chapter=1, title="Title")],
                    )

        assert "connection" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_api_error_raises_msep_api_error(self) -> None:
        """AC-6.1.4: Should raise MSEPAPIError on 4xx/5xx response."""
        from workflows.shared.clients.msep_client import (
            MSEPClient,
            MSEPAPIError,
            ChapterMeta,
        )

        msep_client = MSEPClient(max_retries=0)

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"detail": "Internal server error"}
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server Error",
            request=MagicMock(),
            response=mock_response,
        )

        with patch.object(
            httpx.AsyncClient,
            "post",
            return_value=mock_response,
        ):
            async with msep_client as client:
                with pytest.raises(MSEPAPIError) as exc_info:
                    await client.enrich_metadata(
                        corpus=["Content"],
                        chapter_index=[ChapterMeta(book="Book", chapter=1, title="Title")],
                    )

        assert exc_info.value.status_code == 500

    @pytest.mark.asyncio
    async def test_api_error_422_validation(self) -> None:
        """AC-6.1.4: Should raise MSEPAPIError with validation details."""
        from workflows.shared.clients.msep_client import (
            MSEPClient,
            MSEPAPIError,
            ChapterMeta,
        )

        msep_client = MSEPClient(max_retries=0)

        mock_response = MagicMock()
        mock_response.status_code = 422
        mock_response.json.return_value = {
            "detail": [{"loc": ["body", "corpus"], "msg": "field required"}]
        }
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Unprocessable Entity",
            request=MagicMock(),
            response=mock_response,
        )

        with patch.object(
            httpx.AsyncClient,
            "post",
            return_value=mock_response,
        ):
            async with msep_client as client:
                with pytest.raises(MSEPAPIError) as exc_info:
                    await client.enrich_metadata(
                        corpus=["Content"],
                        chapter_index=[ChapterMeta(book="Book", chapter=1, title="Title")],
                    )

        assert exc_info.value.status_code == 422
        assert exc_info.value.response_body is not None


# =============================================================================
# TestMSEPClientRetry - AC-6.1.4
# =============================================================================


class TestMSEPClientRetry:
    """AC-6.1.4: Test retry logic with exponential backoff."""

    @pytest.mark.asyncio
    async def test_retries_on_timeout(self) -> None:
        """AC-6.1.4: Should retry on timeout errors."""
        from workflows.shared.clients.msep_client import MSEPClient, ChapterMeta

        call_count = 0

        async def mock_post(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0)  # Make async meaningful
            if call_count < 3:
                raise httpx.TimeoutException("Timeout")
            # Success on 3rd attempt
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = {
                "chapters": [],
                "processing_time_ms": 50.0,
                "total_cross_references": 0,
            }
            mock_resp.raise_for_status = MagicMock()
            return mock_resp

        msep_client = MSEPClient(max_retries=3, retry_delay=0.01)

        with patch.object(httpx.AsyncClient, "post", side_effect=mock_post):
            async with msep_client as client:
                await client.enrich_metadata(
                    corpus=["Content"],
                    chapter_index=[ChapterMeta(book="Book", chapter=1, title="Title")],
                )

        assert call_count == 3

    @pytest.mark.asyncio
    async def test_retries_on_503_service_unavailable(self) -> None:
        """AC-6.1.4: Should retry on 503 Service Unavailable."""
        from workflows.shared.clients.msep_client import MSEPClient, ChapterMeta

        call_count = 0

        async def mock_post(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0)  # Make async meaningful
            mock_resp = MagicMock()
            if call_count < 2:
                mock_resp.status_code = 503
                mock_resp.json.return_value = {"detail": "Service Unavailable"}
                mock_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
                    "Service Unavailable",
                    request=MagicMock(),
                    response=mock_resp,
                )
            else:
                mock_resp.status_code = 200
                mock_resp.json.return_value = {
                    "chapters": [],
                    "processing_time_ms": 50.0,
                    "total_cross_references": 0,
                }
                mock_resp.raise_for_status = MagicMock()
            return mock_resp

        msep_client = MSEPClient(max_retries=3, retry_delay=0.01)

        with patch.object(httpx.AsyncClient, "post", side_effect=mock_post):
            async with msep_client as client:
                await client.enrich_metadata(
                    corpus=["Content"],
                    chapter_index=[ChapterMeta(book="Book", chapter=1, title="Title")],
                )

        assert call_count == 2

    @pytest.mark.asyncio
    async def test_no_retry_on_400_bad_request(self) -> None:
        """AC-6.1.4: Should NOT retry on 400 Bad Request (client error)."""
        from workflows.shared.clients.msep_client import MSEPClient, MSEPAPIError, ChapterMeta

        call_count = 0

        async def mock_post(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0)  # Make async meaningful
            mock_resp = MagicMock()
            mock_resp.status_code = 400
            mock_resp.json.return_value = {"detail": "Bad Request"}
            mock_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
                "Bad Request",
                request=MagicMock(),
                response=mock_resp,
            )
            return mock_resp

        msep_client = MSEPClient(max_retries=3, retry_delay=0.01)

        with patch.object(httpx.AsyncClient, "post", side_effect=mock_post):
            async with msep_client as client:
                with pytest.raises(MSEPAPIError):
                    await client.enrich_metadata(
                        corpus=["Content"],
                        chapter_index=[ChapterMeta(book="Book", chapter=1, title="Title")],
                    )

        # Should only be called once - no retry on 4xx
        assert call_count == 1


# =============================================================================
# TestMSEPClientProtocol - AC-6.1.1
# =============================================================================


class TestMSEPClientProtocol:
    """AC-6.1.1: Test Protocol compliance for dependency injection."""

    def test_client_implements_protocol(self) -> None:
        """MSEPClient should implement MSEPClientProtocol."""
        from workflows.shared.clients.msep_client import (
            MSEPClient,
            MSEPClientProtocol,
        )

        client = MSEPClient()

        # Protocol compliance check
        assert isinstance(client, MSEPClientProtocol)

    def test_protocol_is_runtime_checkable(self) -> None:
        """Protocol should be @runtime_checkable for isinstance()."""
        from workflows.shared.clients.msep_client import MSEPClientProtocol

        # Should be a Protocol that is runtime checkable
        assert hasattr(MSEPClientProtocol, "__protocol_attrs__") or hasattr(
            MSEPClientProtocol, "_is_runtime_protocol"
        )


# =============================================================================
# TestRequestDataclasses - AC-6.1.1
# =============================================================================


class TestRequestDataclasses:
    """Test request dataclasses match ai-agents schema."""

    def test_chapter_meta_dataclass(self) -> None:
        """ChapterMeta should be a dataclass with correct fields."""
        from dataclasses import is_dataclass
        from workflows.shared.clients.msep_client import ChapterMeta

        assert is_dataclass(ChapterMeta)

        meta = ChapterMeta(book="TestBook", chapter=1, title="Introduction", id="ch1")
        assert meta.book == "TestBook"
        assert meta.chapter == 1
        assert meta.title == "Introduction"
        assert meta.id == "ch1"

    def test_chapter_meta_to_dict(self) -> None:
        """ChapterMeta.to_dict should produce correct JSON structure."""
        from workflows.shared.clients.msep_client import ChapterMeta

        meta = ChapterMeta(book="TestBook", chapter=1, title="Intro", id="ch1")
        result = meta.to_dict()

        assert result == {
            "book": "TestBook",
            "chapter": 1,
            "title": "Intro",
            "id": "ch1",
        }

    def test_chapter_meta_to_dict_without_id(self) -> None:
        """ChapterMeta.to_dict should omit id if None."""
        from workflows.shared.clients.msep_client import ChapterMeta

        meta = ChapterMeta(book="TestBook", chapter=1, title="Intro")
        result = meta.to_dict()

        assert "id" not in result
        assert result == {"book": "TestBook", "chapter": 1, "title": "Intro"}

    def test_msep_config_dataclass(self) -> None:
        """MSEPConfig should be a dataclass with correct defaults."""
        from dataclasses import is_dataclass
        from workflows.shared.clients.msep_client import MSEPConfig

        assert is_dataclass(MSEPConfig)

        config = MSEPConfig()
        assert config.threshold == pytest.approx(0.45)
        assert config.top_k == 5
        assert config.timeout == pytest.approx(30.0)

    def test_msep_config_to_dict(self) -> None:
        """MSEPConfig.to_dict should produce correct JSON structure."""
        from workflows.shared.clients.msep_client import MSEPConfig

        config = MSEPConfig(threshold=0.6, top_k=10)
        result = config.to_dict()

        assert result["threshold"] == pytest.approx(0.6)
        assert result["top_k"] == 10
        assert "enable_hybrid_search" in result


# =============================================================================
# TestResponseDataclasses - AC-6.1.3
# =============================================================================


class TestResponseDataclasses:
    """AC-6.1.3: Test response dataclasses match ai-agents schema."""

    def test_enriched_metadata_response_dataclass(self) -> None:
        """EnrichedMetadataResponse should be a dataclass."""
        from dataclasses import is_dataclass
        from workflows.shared.clients.msep_client import EnrichedMetadataResponse

        assert is_dataclass(EnrichedMetadataResponse)

    def test_enriched_chapter_dataclass(self) -> None:
        """EnrichedChapter should be a dataclass."""
        from dataclasses import is_dataclass
        from workflows.shared.clients.msep_client import EnrichedChapter

        assert is_dataclass(EnrichedChapter)

    def test_merged_keywords_dataclass(self) -> None:
        """MergedKeywords should be a dataclass."""
        from dataclasses import is_dataclass
        from workflows.shared.clients.msep_client import MergedKeywords

        assert is_dataclass(MergedKeywords)

    def test_provenance_dataclass(self) -> None:
        """Provenance should be a dataclass."""
        from dataclasses import is_dataclass
        from workflows.shared.clients.msep_client import Provenance

        assert is_dataclass(Provenance)

    def test_cross_reference_dataclass(self) -> None:
        """CrossReference should be a dataclass."""
        from dataclasses import is_dataclass
        from workflows.shared.clients.msep_client import CrossReference

        assert is_dataclass(CrossReference)

    def test_enriched_metadata_from_dict(self) -> None:
        """AC-6.1.3: Should parse from API response dict (ai-agents schema)."""
        from workflows.shared.clients.msep_client import EnrichedMetadataResponse

        response_dict = {
            "chapters": [
                {
                    "chapter_id": "ch1",
                    "cross_references": [
                        {
                            "target": "Book2_Ch3",
                            "score": 0.85,
                            "base_score": 0.75,
                            "topic_boost": 0.10,
                            "method": "sbert",
                        }
                    ],
                    "keywords": {
                        "tfidf": ["pattern"],
                        "semantic": ["architecture"],
                        "merged": ["pattern", "architecture"],
                    },
                    "topic_id": 1,
                    "provenance": {
                        "methods_used": ["sbert", "topic_boost"],
                        "sbert_score": 0.85,
                        "topic_boost": 0.10,
                        "timestamp": "2025-01-16T12:00:00Z",
                    },
                }
            ],
            "processing_time_ms": 150.5,
            "total_cross_references": 1,
        }

        response = EnrichedMetadataResponse.from_dict(response_dict)

        assert len(response.chapters) == 1
        assert response.chapters[0].chapter_id == "ch1"
        assert response.chapters[0].topic_id == 1
        assert response.chapters[0].keywords.tfidf == ["pattern"]
        assert response.chapters[0].keywords.semantic == ["architecture"]
        assert response.chapters[0].keywords.merged == ["pattern", "architecture"]
        assert response.chapters[0].provenance.methods_used == ["sbert", "topic_boost"]
        assert response.chapters[0].provenance.sbert_score == pytest.approx(0.85)
        assert len(response.chapters[0].cross_references) == 1
        assert response.chapters[0].cross_references[0].target == "Book2_Ch3"
        assert response.processing_time_ms == pytest.approx(150.5)
        assert response.total_cross_references == 1


# =============================================================================
# TestMSEPClientExceptions
# =============================================================================


class TestMSEPClientExceptions:
    """Test custom exception classes."""

    def test_msep_client_error_base_class(self) -> None:
        """Base MSEPClientError should have status_code attribute."""
        from workflows.shared.clients.msep_client import MSEPClientError

        error = MSEPClientError("Test error", status_code=500)

        assert str(error) == "Test error"
        assert error.status_code == 500

    def test_msep_timeout_error_inherits(self) -> None:
        """MSEPTimeoutError should inherit from MSEPClientError."""
        from workflows.shared.clients.msep_client import (
            MSEPClientError,
            MSEPTimeoutError,
        )

        error = MSEPTimeoutError("Timeout occurred")

        assert isinstance(error, MSEPClientError)
        assert isinstance(error, Exception)

    def test_msep_connection_error_inherits(self) -> None:
        """MSEPConnectionError should inherit from MSEPClientError."""
        from workflows.shared.clients.msep_client import (
            MSEPClientError,
            MSEPConnectionError,
        )

        error = MSEPConnectionError("Connection refused")

        assert isinstance(error, MSEPClientError)
        assert isinstance(error, Exception)

    def test_msep_api_error_has_response_body(self) -> None:
        """MSEPAPIError should have response_body attribute."""
        from workflows.shared.clients.msep_client import MSEPAPIError

        error = MSEPAPIError(
            "API Error",
            status_code=422,
            response_body={"detail": "Validation failed"},
        )

        assert error.status_code == 422
        assert error.response_body == {"detail": "Validation failed"}
