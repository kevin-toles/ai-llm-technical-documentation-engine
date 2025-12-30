"""Tests for MetadataExtractionClient - WBS-2.2.

AC-3: MetadataExtractionClient with protocol, connection pooling, retry, health check.

TDD Phase: RED - Tests written before implementation.
"""

from __future__ import annotations

import asyncio

import pytest


# =============================================================================
# WBS-2.2.1: Protocol and Import Tests (AC-3.1)
# =============================================================================


class TestMetadataClientImport:
    """Test that client classes can be imported."""

    def test_can_import_metadata_extraction_client(self) -> None:
        """AC-3.1: MetadataExtractionClient exists."""
        from workflows.shared.clients.metadata_client import MetadataExtractionClient

        assert MetadataExtractionClient  # Class exists and is truthy

    def test_can_import_protocol(self) -> None:
        """AC-3.1: MetadataExtractionClientProtocol exists."""
        from workflows.shared.clients.metadata_client import (
            MetadataExtractionClientProtocol,
        )

        assert MetadataExtractionClientProtocol  # Protocol exists and is truthy

    def test_can_import_result_types(self) -> None:
        """Result dataclasses can be imported."""
        from workflows.shared.clients.metadata_client import (
            MetadataExtractionResult,
            KeywordResult,
            ConceptResult,
        )

        assert MetadataExtractionResult  # Class exists and is truthy
        assert KeywordResult  # Class exists and is truthy
        assert ConceptResult  # Class exists and is truthy


# =============================================================================
# WBS-2.2.2: Protocol Compliance (AC-3.1)
# =============================================================================


class TestProtocolCompliance:
    """Test MetadataExtractionClient satisfies protocol."""

    def test_client_has_extract_metadata_method(self) -> None:
        """AC-3.1: Client has extract_metadata async method."""
        from workflows.shared.clients.metadata_client import MetadataExtractionClient

        client = MetadataExtractionClient()
        assert hasattr(client, "extract_metadata")
        assert asyncio.iscoroutinefunction(client.extract_metadata)

    def test_client_has_health_check_method(self) -> None:
        """AC-3.5: Client has health_check async method."""
        from workflows.shared.clients.metadata_client import MetadataExtractionClient

        client = MetadataExtractionClient()
        assert hasattr(client, "health_check")
        assert asyncio.iscoroutinefunction(client.health_check)

    def test_protocol_is_runtime_checkable(self) -> None:
        """AC-3.1: Protocol supports isinstance checks."""
        from workflows.shared.clients.metadata_client import (
            MetadataExtractionClient,
            MetadataExtractionClientProtocol,
        )

        client = MetadataExtractionClient()
        assert isinstance(client, MetadataExtractionClientProtocol)


# =============================================================================
# WBS-2.2.3: Async Context Manager (AC-3.3)
# =============================================================================


class TestAsyncContextManager:
    """Test client works as async context manager."""

    @pytest.mark.asyncio
    async def test_client_supports_async_with(self) -> None:
        """AC-3.3: Client can be used with async with."""
        from workflows.shared.clients.metadata_client import MetadataExtractionClient

        async with MetadataExtractionClient() as client:
            assert client is not None

    @pytest.mark.asyncio
    async def test_client_has_aenter(self) -> None:
        """AC-3.3: Client has __aenter__ method."""
        from workflows.shared.clients.metadata_client import MetadataExtractionClient

        client = MetadataExtractionClient()
        assert hasattr(client, "__aenter__")
        assert asyncio.iscoroutinefunction(client.__aenter__)

    @pytest.mark.asyncio
    async def test_client_has_aexit(self) -> None:
        """AC-3.3: Client has __aexit__ method."""
        from workflows.shared.clients.metadata_client import MetadataExtractionClient

        client = MetadataExtractionClient()
        assert hasattr(client, "__aexit__")
        assert asyncio.iscoroutinefunction(client.__aexit__)


# =============================================================================
# WBS-2.2.4: Connection Pooling (AC-3.2)
# =============================================================================


class TestConnectionPooling:
    """Test httpx.AsyncClient is reused (Anti-Pattern #12)."""

    @pytest.mark.asyncio
    async def test_client_reuses_http_client(self) -> None:
        """AC-3.2: Same httpx.AsyncClient reused across calls."""
        from workflows.shared.clients.metadata_client import MetadataExtractionClient

        async with MetadataExtractionClient() as client:
            # Access internal http client
            http_client_1 = client._http_client
            http_client_2 = client._http_client
            assert http_client_1 is http_client_2


# =============================================================================
# WBS-2.2.5: Configuration (AC-3.4)
# =============================================================================


class TestClientConfiguration:
    """Test client accepts configuration parameters."""

    def test_client_accepts_base_url(self) -> None:
        """Client accepts base_url parameter."""
        from workflows.shared.clients.metadata_client import MetadataExtractionClient

        client = MetadataExtractionClient(base_url="http://custom:9000")
        assert client._base_url == "http://custom:9000"

    def test_client_accepts_timeout(self) -> None:
        """Client accepts timeout parameter."""
        from workflows.shared.clients.metadata_client import MetadataExtractionClient

        client = MetadataExtractionClient(timeout=60.0)
        assert client._timeout == pytest.approx(60.0)

    def test_client_accepts_max_retries(self) -> None:
        """AC-3.4: Client accepts max_retries parameter."""
        from workflows.shared.clients.metadata_client import MetadataExtractionClient

        client = MetadataExtractionClient(max_retries=5)
        assert client._max_retries == 5


# =============================================================================
# WBS-2.2.6: Exception Classes
# =============================================================================


class TestExceptionClasses:
    """Test exception classes follow naming conventions."""

    def test_can_import_client_error(self) -> None:
        """AC-6.3: MetadataClientError exists."""
        from workflows.shared.clients.metadata_client import MetadataClientError

        assert MetadataClientError  # Exception class exists and is truthy

    def test_can_import_timeout_error(self) -> None:
        """AC-6.3: MetadataClientTimeoutError exists."""
        from workflows.shared.clients.metadata_client import MetadataClientTimeoutError

        assert MetadataClientTimeoutError  # Exception class exists and is truthy

    def test_can_import_connection_error(self) -> None:
        """AC-6.3: MetadataClientConnectionError exists."""
        from workflows.shared.clients.metadata_client import MetadataClientConnectionError

        assert MetadataClientConnectionError  # Exception class exists and is truthy

    def test_timeout_error_inherits_from_client_error(self) -> None:
        """Timeout error inherits from base error."""
        from workflows.shared.clients.metadata_client import (
            MetadataClientError,
            MetadataClientTimeoutError,
        )

        assert issubclass(MetadataClientTimeoutError, MetadataClientError)

    def test_connection_error_inherits_from_client_error(self) -> None:
        """Connection error inherits from base error."""
        from workflows.shared.clients.metadata_client import (
            MetadataClientError,
            MetadataClientConnectionError,
        )

        assert issubclass(MetadataClientConnectionError, MetadataClientError)

    def test_can_import_api_error(self) -> None:
        """AC-6.3: MetadataClientAPIError exists."""
        from workflows.shared.clients.metadata_client import MetadataClientAPIError

        assert MetadataClientAPIError  # Exception class exists and is truthy

    def test_api_error_inherits_from_client_error(self) -> None:
        """API error inherits from base error."""
        from workflows.shared.clients.metadata_client import (
            MetadataClientError,
            MetadataClientAPIError,
        )

        assert issubclass(MetadataClientAPIError, MetadataClientError)


# =============================================================================
# WBS-2.2.7: Retry Logic (AC-3.4)
# =============================================================================


class TestRetryLogic:
    """Test retry with exponential backoff on 503."""

    @pytest.mark.asyncio
    async def test_retries_on_503_status(self) -> None:
        """AC-3.4: Client retries on 503 Service Unavailable."""
        import httpx
        from unittest.mock import AsyncMock, patch, MagicMock

        from workflows.shared.clients.metadata_client import MetadataExtractionClient

        # Mock httpx response with 503 first, then 200
        mock_response_503 = MagicMock()
        mock_response_503.status_code = 503
        mock_response_503.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Service Unavailable",
            request=MagicMock(),
            response=mock_response_503,
        )

        mock_response_200 = MagicMock()
        mock_response_200.status_code = 200
        mock_response_200.raise_for_status.return_value = None
        mock_response_200.json.return_value = {"keywords": [], "concepts": []}

        async with MetadataExtractionClient(max_retries=3) as client:
            with patch.object(
                client._http_client,
                "post",
                new_callable=AsyncMock,
                side_effect=[mock_response_503, mock_response_200],
            ) as mock_post:
                _result = await client.extract_metadata("test text")
                assert mock_post.call_count == 2  # Retried once

    @pytest.mark.asyncio
    async def test_raises_after_max_retries_exceeded(self) -> None:
        """AC-3.4: Client raises after max_retries on 503."""
        import httpx
        from unittest.mock import AsyncMock, patch, MagicMock

        from workflows.shared.clients.metadata_client import (
            MetadataExtractionClient,
            MetadataClientAPIError,
        )

        # Mock httpx response with 503 every time
        mock_response_503 = MagicMock()
        mock_response_503.status_code = 503
        mock_response_503.content = b'{"error": "Service Unavailable"}'
        mock_response_503.json.return_value = {"error": "Service Unavailable"}
        mock_response_503.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Service Unavailable",
            request=MagicMock(),
            response=mock_response_503,
        )

        async with MetadataExtractionClient(max_retries=2) as client:
            with patch.object(
                client._http_client,
                "post",
                new_callable=AsyncMock,
                return_value=mock_response_503,
            ) as mock_post:
                with pytest.raises(MetadataClientAPIError) as exc_info:
                    await client.extract_metadata("test text")
                # Should have retried max_retries times
                assert mock_post.call_count == 3  # 1 initial + 2 retries
                assert exc_info.value.status_code == 503

    @pytest.mark.asyncio
    async def test_no_retry_on_400_error(self) -> None:
        """AC-3.4: Client does NOT retry on 4xx client errors."""
        import httpx
        from unittest.mock import AsyncMock, patch, MagicMock

        from workflows.shared.clients.metadata_client import (
            MetadataExtractionClient,
            MetadataClientAPIError,
        )

        mock_response_400 = MagicMock()
        mock_response_400.status_code = 400
        mock_response_400.content = b'{"error": "Bad Request"}'
        mock_response_400.json.return_value = {"error": "Bad Request"}
        mock_response_400.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Bad Request",
            request=MagicMock(),
            response=mock_response_400,
        )

        async with MetadataExtractionClient(max_retries=3) as client:
            with patch.object(
                client._http_client,
                "post",
                new_callable=AsyncMock,
                return_value=mock_response_400,
            ) as mock_post:
                with pytest.raises(MetadataClientAPIError):
                    await client.extract_metadata("test text")
                # Should NOT retry on 4xx
                assert mock_post.call_count == 1

    @pytest.mark.asyncio
    async def test_retry_uses_exponential_backoff(self) -> None:
        """AC-3.4: Retry uses exponential backoff."""
        import httpx
        import time
        from unittest.mock import AsyncMock, patch, MagicMock

        from workflows.shared.clients.metadata_client import MetadataExtractionClient

        mock_response_503 = MagicMock()
        mock_response_503.status_code = 503
        mock_response_503.content = b'{"error": "Service Unavailable"}'
        mock_response_503.json.return_value = {"error": "Service Unavailable"}
        mock_response_503.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Service Unavailable",
            request=MagicMock(),
            response=mock_response_503,
        )

        mock_response_200 = MagicMock()
        mock_response_200.status_code = 200
        mock_response_200.raise_for_status.return_value = None
        mock_response_200.json.return_value = {"keywords": [], "concepts": []}

        async with MetadataExtractionClient(max_retries=3) as client:
            call_times: list[float] = []

            async def track_calls(*args, **kwargs):
                call_times.append(time.time())
                await asyncio.sleep(0)  # Yield to event loop
                if len(call_times) < 3:
                    raise httpx.HTTPStatusError(
                        "Service Unavailable",
                        request=MagicMock(),
                        response=mock_response_503,
                    )
                return mock_response_200

            with patch.object(
                client._http_client,
                "post",
                new_callable=AsyncMock,
                side_effect=track_calls,
            ):
                await client.extract_metadata("test text")
                # Verify delays increase (exponential backoff)
                if len(call_times) >= 3:
                    delay1 = call_times[1] - call_times[0]
                    delay2 = call_times[2] - call_times[1]
                    # Second delay should be >= first delay (exponential)
                    assert delay2 >= delay1 * 0.9  # Allow some tolerance


# =============================================================================
# WBS-2.2.8: Health Check (AC-3.5)
# =============================================================================


class TestHealthCheck:
    """Test health_check returns bool, never raises."""

    @pytest.mark.asyncio
    async def test_health_check_returns_true_when_service_up(self) -> None:
        """AC-3.5: health_check returns True when service is healthy."""
        from unittest.mock import AsyncMock, patch, MagicMock

        from workflows.shared.clients.metadata_client import MetadataExtractionClient

        mock_response = MagicMock()
        mock_response.status_code = 200

        async with MetadataExtractionClient() as client:
            with patch.object(
                client._http_client,
                "get",
                new_callable=AsyncMock,
                return_value=mock_response,
            ):
                result = await client.health_check()
                assert result is True

    @pytest.mark.asyncio
    async def test_health_check_returns_false_when_service_down(self) -> None:
        """AC-3.5: health_check returns False when service is unhealthy."""
        from unittest.mock import AsyncMock, patch, MagicMock

        from workflows.shared.clients.metadata_client import MetadataExtractionClient

        mock_response = MagicMock()
        mock_response.status_code = 503

        async with MetadataExtractionClient() as client:
            with patch.object(
                client._http_client,
                "get",
                new_callable=AsyncMock,
                return_value=mock_response,
            ):
                result = await client.health_check()
                assert result is False

    @pytest.mark.asyncio
    async def test_health_check_returns_false_on_connection_error(self) -> None:
        """AC-3.5: health_check returns False on connection error."""
        import httpx
        from unittest.mock import AsyncMock, patch

        from workflows.shared.clients.metadata_client import MetadataExtractionClient

        async with MetadataExtractionClient() as client:
            with patch.object(
                client._http_client,
                "get",
                new_callable=AsyncMock,
                side_effect=httpx.ConnectError("Connection refused"),
            ):
                result = await client.health_check()
                assert result is False

    @pytest.mark.asyncio
    async def test_health_check_returns_false_on_timeout(self) -> None:
        """AC-3.5: health_check returns False on timeout."""
        import httpx
        from unittest.mock import AsyncMock, patch

        from workflows.shared.clients.metadata_client import MetadataExtractionClient

        async with MetadataExtractionClient() as client:
            with patch.object(
                client._http_client,
                "get",
                new_callable=AsyncMock,
                side_effect=httpx.TimeoutException("Timeout"),
            ):
                result = await client.health_check()
                assert result is False

    @pytest.mark.asyncio
    async def test_health_check_never_raises_exceptions(self) -> None:
        """AC-3.5: health_check NEVER raises, always returns bool."""
        from unittest.mock import AsyncMock, patch

        from workflows.shared.clients.metadata_client import MetadataExtractionClient

        async with MetadataExtractionClient() as client:
            # Test various exception types
            exceptions = [
                Exception("Generic error"),
                RuntimeError("Runtime error"),
                ValueError("Value error"),
            ]
            for exc in exceptions:
                with patch.object(
                    client._http_client,
                    "get",
                    new_callable=AsyncMock,
                    side_effect=exc,
                ):
                    # Should NOT raise, should return False
                    result = await client.health_check()
                    assert result is False

    @pytest.mark.asyncio
    async def test_health_check_returns_false_without_context_manager(self) -> None:
        """AC-3.5: health_check returns False if client not initialized."""
        from workflows.shared.clients.metadata_client import MetadataExtractionClient

        client = MetadataExtractionClient()
        # Not using async with, so _http_client is None
        result = await client.health_check()
        assert result is False


# =============================================================================
# WBS-2.2.9: Extract Metadata with Mocks (Coverage)
# =============================================================================


class TestExtractMetadataWithMocks:
    """Test extract_metadata with mocked responses for coverage."""

    @pytest.mark.asyncio
    async def test_extract_metadata_success(self) -> None:
        """Test successful metadata extraction."""
        from unittest.mock import AsyncMock, patch, MagicMock

        from workflows.shared.clients.metadata_client import MetadataExtractionClient

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "keywords": [
                {"term": "python", "score": 0.9, "is_technical": True, "sources": ["tfidf"]}
            ],
            "concepts": [
                {"name": "Machine Learning", "confidence": 0.85, "domain": "AI/ML", "tier": "core"}
            ],
            "summary": "Test summary",
            "metadata": {
                "processing_time_ms": 150.5,
                "text_length": 100,
                "detected_domain": "AI/ML",
                "domain_confidence": 0.9,
                "quality_score": 0.8,
                "stages_completed": ["keywords", "concepts"],
            },
            "rejected": {
                "keywords": ["the", "a"],
                "reasons": {"the": "stopword", "a": "stopword"},
            },
        }

        async with MetadataExtractionClient() as client:
            with patch.object(
                client._http_client,
                "post",
                new_callable=AsyncMock,
                return_value=mock_response,
            ):
                result = await client.extract_metadata(
                    text="Test text about python and machine learning",
                    title="Test Chapter",
                    book_title="Test Book",
                )
                assert len(result.keywords) == 1
                assert result.keywords[0].term == "python"
                assert result.keywords[0].score == pytest.approx(0.9)
                assert result.keywords[0].is_technical is True
                assert len(result.concepts) == 1
                assert result.concepts[0].name == "Machine Learning"
                assert result.summary == "Test summary"
                assert result.metadata is not None
                assert result.metadata.processing_time_ms == pytest.approx(150.5)
                assert result.metadata.detected_domain == "AI/ML"
                assert result.rejected is not None
                assert "the" in result.rejected.keywords

    @pytest.mark.asyncio
    async def test_extract_metadata_minimal_response(self) -> None:
        """Test extraction with minimal response (empty keywords/concepts)."""
        from unittest.mock import AsyncMock, patch, MagicMock

        from workflows.shared.clients.metadata_client import MetadataExtractionClient

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"keywords": [], "concepts": []}

        async with MetadataExtractionClient() as client:
            with patch.object(
                client._http_client,
                "post",
                new_callable=AsyncMock,
                return_value=mock_response,
            ):
                result = await client.extract_metadata("short")
                assert result.keywords == []
                assert result.concepts == []
                assert result.metadata is None
                assert result.rejected is None

    @pytest.mark.asyncio
    async def test_extract_metadata_raises_without_context_manager(self) -> None:
        """Test extract_metadata raises if client not initialized."""
        from workflows.shared.clients.metadata_client import (
            MetadataExtractionClient,
            MetadataClientError,
        )

        client = MetadataExtractionClient()
        with pytest.raises(MetadataClientError, match="not initialized"):
            await client.extract_metadata("test")

    @pytest.mark.asyncio
    async def test_extract_metadata_connection_error(self) -> None:
        """Test extract_metadata raises on connection error."""
        import httpx
        from unittest.mock import AsyncMock, patch

        from workflows.shared.clients.metadata_client import (
            MetadataExtractionClient,
            MetadataClientConnectionError,
        )

        async with MetadataExtractionClient() as client:
            with patch.object(
                client._http_client,
                "post",
                new_callable=AsyncMock,
                side_effect=httpx.ConnectError("Connection refused"),
            ):
                with pytest.raises(MetadataClientConnectionError):
                    await client.extract_metadata("test")

    @pytest.mark.asyncio
    async def test_extract_metadata_timeout_error(self) -> None:
        """Test extract_metadata raises on timeout."""
        import httpx
        from unittest.mock import AsyncMock, patch

        from workflows.shared.clients.metadata_client import (
            MetadataExtractionClient,
            MetadataClientTimeoutError,
        )

        async with MetadataExtractionClient() as client:
            with patch.object(
                client._http_client,
                "post",
                new_callable=AsyncMock,
                side_effect=httpx.TimeoutException("Timeout"),
            ):
                with pytest.raises(MetadataClientTimeoutError):
                    await client.extract_metadata("test")

    @pytest.mark.asyncio
    async def test_extract_metadata_with_custom_options(self) -> None:
        """Test extract_metadata passes custom options."""
        from unittest.mock import AsyncMock, patch, MagicMock

        from workflows.shared.clients.metadata_client import (
            MetadataExtractionClient,
            MetadataExtractionOptions,
        )

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"keywords": [], "concepts": []}

        options = MetadataExtractionOptions(
            min_keyword_confidence=0.5,
            min_concept_confidence=0.4,
            filter_noise=False,
        )

        async with MetadataExtractionClient() as client:
            with patch.object(
                client._http_client,
                "post",
                new_callable=AsyncMock,
                return_value=mock_response,
            ) as mock_post:
                await client.extract_metadata("test", options=options)
                # Verify options were passed in payload
                call_args = mock_post.call_args
                payload = call_args.kwargs.get("json") or call_args[1].get("json")
                assert payload["options"]["min_keyword_confidence"] == pytest.approx(0.5)
                assert payload["options"]["filter_noise"] is False


# =============================================================================
# WBS-2.2.10: FakeMetadataExtractionClient Tests (AC-4)
# =============================================================================


class TestFakeMetadataExtractionClient:
    """Test FakeMetadataExtractionClient for testing purposes."""

    def test_can_import_fake_client(self) -> None:
        """AC-4.1: FakeMetadataExtractionClient exists."""
        from workflows.shared.clients.metadata_client import FakeMetadataExtractionClient

        assert FakeMetadataExtractionClient  # Class exists and is truthy

    def test_fake_client_passes_protocol(self) -> None:
        """AC-4.1: FakeClient passes protocol check."""
        from workflows.shared.clients.metadata_client import (
            FakeMetadataExtractionClient,
            MetadataExtractionClientProtocol,
        )

        client = FakeMetadataExtractionClient()
        assert isinstance(client, MetadataExtractionClientProtocol)

    @pytest.mark.asyncio
    async def test_fake_client_default_response(self) -> None:
        """AC-4.3: FakeClient returns empty result by default."""
        from workflows.shared.clients.metadata_client import FakeMetadataExtractionClient

        client = FakeMetadataExtractionClient()
        result = await client.extract_metadata("any text")
        assert result.keywords == []
        assert result.concepts == []

    @pytest.mark.asyncio
    async def test_fake_client_set_response(self) -> None:
        """AC-4.2: FakeClient returns configured response."""
        import hashlib
        from workflows.shared.clients.metadata_client import (
            FakeMetadataExtractionClient,
            MetadataExtractionResult,
            KeywordResult,
        )

        client = FakeMetadataExtractionClient()
        text = "test input"
        text_hash = hashlib.md5(text.encode()).hexdigest()

        expected_result = MetadataExtractionResult(
            keywords=[KeywordResult(term="test", score=0.9)],
        )
        client.set_response(text_hash, expected_result)

        result = await client.extract_metadata(text)
        assert len(result.keywords) == 1
        assert result.keywords[0].term == "test"

    @pytest.mark.asyncio
    async def test_fake_client_health_check_always_true(self) -> None:
        """AC-4.1: FakeClient health_check always returns True."""
        from workflows.shared.clients.metadata_client import FakeMetadataExtractionClient

        client = FakeMetadataExtractionClient()
        result = await client.health_check()
        assert result is True

    @pytest.mark.asyncio
    async def test_fake_client_async_context_manager(self) -> None:
        """AC-4.1: FakeClient works as async context manager."""
        from workflows.shared.clients.metadata_client import FakeMetadataExtractionClient

        async with FakeMetadataExtractionClient() as client:
            assert client is not None
            result = await client.extract_metadata("test")
            assert result is not None

    def test_fake_client_tracks_call_count(self) -> None:
        """FakeClient tracks number of calls."""
        from workflows.shared.clients.metadata_client import FakeMetadataExtractionClient

        client = FakeMetadataExtractionClient()
        assert client._call_count == 0

    @pytest.mark.asyncio
    async def test_fake_client_increments_call_count(self) -> None:
        """FakeClient increments call count on each extract_metadata."""
        from workflows.shared.clients.metadata_client import FakeMetadataExtractionClient

        client = FakeMetadataExtractionClient()
        await client.extract_metadata("test1")
        await client.extract_metadata("test2")
        assert client._call_count == 2
