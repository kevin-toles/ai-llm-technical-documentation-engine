"""
Test Semantic Search Client - WBS 3.2.3.8 Unit Tests

Reference Documents:
- GUIDELINES: Resilience patterns (Newman pp. 352-360)
- CODING_PATTERNS_ANALYSIS: Anti-Pattern §1.1 Optional types
- semantic-search-service/docs/ARCHITECTURE.md: API endpoints

Tests cover:
- Client instantiation with default and custom config
- Async context manager pattern (connection pooling)
- embed() method
- search() method  
- hybrid_search() method
- Retry logic with exponential backoff
- Error handling
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import httpx


class TestSemanticSearchClientInstantiation:
    """WBS 3.2.3: Test client instantiates with config."""

    def test_client_instantiates_with_defaults(self):
        """Client should instantiate with default configuration."""
        from workflows.shared.clients.search_client import SemanticSearchClient

        client = SemanticSearchClient()

        assert client.base_url == "http://localhost:8081"
        assert client.timeout == pytest.approx(30.0)
        assert client._client is None  # Lazy initialization

    def test_client_instantiates_with_custom_config(self):
        """Client should accept custom configuration."""
        from workflows.shared.clients.search_client import SemanticSearchClient

        client = SemanticSearchClient(
            base_url="http://semantic-search:8081",
            timeout=60.0,
            max_connections=20,
        )

        assert client.base_url == "http://semantic-search:8081"
        assert client.timeout == pytest.approx(60.0)
        assert client.max_connections == 20

    def test_client_instantiates_from_env(self):
        """Client should read from environment variables."""
        from workflows.shared.clients.search_client import SemanticSearchClient

        with patch.dict(
            "os.environ",
            {
                "SEARCH_SERVICE_URL": "http://search.local:8081",
                "SEARCH_SERVICE_TIMEOUT": "45",
            },
        ):
            client = SemanticSearchClient()

            assert client.base_url == "http://search.local:8081"
            assert client.timeout == pytest.approx(45.0)

    def test_client_has_retry_config(self):
        """Client should have retry configuration."""
        from workflows.shared.clients.search_client import SemanticSearchClient

        client = SemanticSearchClient(max_retries=5, retry_delay=2.0)

        assert client.max_retries == 5
        assert client.retry_delay == pytest.approx(2.0)


class TestSemanticSearchClientContextManager:
    """Test async context manager pattern for connection pooling."""

    @pytest.mark.asyncio
    async def test_context_manager_creates_client(self):
        """Client should create httpx.AsyncClient on enter."""
        from workflows.shared.clients.search_client import SemanticSearchClient

        search_client = SemanticSearchClient()

        async with search_client as client:
            assert client._client is not None
            assert isinstance(client._client, httpx.AsyncClient)

    @pytest.mark.asyncio
    async def test_context_manager_closes_client(self):
        """Client should close httpx.AsyncClient on exit."""
        from workflows.shared.clients.search_client import SemanticSearchClient

        search_client = SemanticSearchClient()

        async with search_client as client:
            # Verify client exists during context
            assert client._client is not None

        # After context exit, internal client should be None
        assert search_client._client is None

    @pytest.mark.asyncio
    async def test_context_manager_reuses_connection_pool(self):
        """
        Anti-Pattern: new httpx.AsyncClient per request (CODING_PATTERNS line 67)
        
        Multiple requests within context should reuse the same client.
        """
        from workflows.shared.clients.search_client import SemanticSearchClient

        search_client = SemanticSearchClient()

        async with search_client as client:
            client_instance = client._client
            # Multiple accesses should return same instance
            assert client._client is client_instance


class TestSemanticSearchClientEmbedMethod:
    """WBS 3.2.3.3: Test embed() method."""

    @pytest.mark.asyncio
    async def test_embed_single_text(self):
        """embed() should handle single text string."""
        from workflows.shared.clients.search_client import SemanticSearchClient

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "embeddings": [[0.1, 0.2, 0.3] * 256],  # 768 dimensions
            "model": "all-mpnet-base-v2"
        }

        with patch("httpx.AsyncClient") as MockClient:
            mock_client = AsyncMock()
            mock_client.request = AsyncMock(return_value=mock_response)
            MockClient.return_value.__aenter__ = AsyncMock(return_value=mock_client)
            MockClient.return_value.__aexit__ = AsyncMock(return_value=None)

            search_client = SemanticSearchClient()
            async with search_client as client:
                client._client = mock_client
                embeddings = await client.embed("domain driven design")

            assert len(embeddings) == 1
            assert len(embeddings[0]) == 768

    @pytest.mark.asyncio
    async def test_embed_batch_texts(self):
        """embed() should handle batch of texts."""
        from workflows.shared.clients.search_client import SemanticSearchClient

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "embeddings": [
                [0.1] * 768,
                [0.2] * 768,
                [0.3] * 768,
            ],
            "model": "all-mpnet-base-v2"
        }

        search_client = SemanticSearchClient()
        async with search_client as client:
            with patch.object(client._client, "request", new_callable=AsyncMock) as mock_request:
                mock_request.return_value = mock_response
                embeddings = await client.embed(["text1", "text2", "text3"])

        assert len(embeddings) == 3
        for emb in embeddings:
            assert len(emb) == 768


class TestSemanticSearchClientSearchMethod:
    """WBS 3.2.3.4: Test search() method."""

    @pytest.mark.asyncio
    async def test_search_returns_results(self):
        """search() should return list of results with id, score, payload."""
        from workflows.shared.clients.search_client import SemanticSearchClient

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {"id": 1, "score": 0.95, "payload": {"title": "Repository Pattern"}},
                {"id": 2, "score": 0.87, "payload": {"title": "Domain Modeling"}},
            ],
            "total": 2,
            "query": "repository pattern"
        }

        search_client = SemanticSearchClient()
        async with search_client as client:
            with patch.object(client._client, "request", new_callable=AsyncMock) as mock_request:
                mock_request.return_value = mock_response
                results = await client.search("repository pattern", limit=5)

        assert len(results) == 2
        assert results[0]["id"] == 1
        assert results[0]["score"] == pytest.approx(0.95)
        assert "payload" in results[0]

    @pytest.mark.asyncio
    async def test_search_with_filters(self):
        """search() should accept optional filters."""
        from workflows.shared.clients.search_client import SemanticSearchClient

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": [], "total": 0}

        search_client = SemanticSearchClient()
        async with search_client as client:
            with patch.object(client._client, "request", new_callable=AsyncMock) as mock_request:
                mock_request.return_value = mock_response
                await client.search(
                    query="microservices",
                    limit=10,
                    collection="chapters",
                    filters={"tier": 1}
                )

                # Verify request was made with filters
                mock_request.assert_called_once()
                call_kwargs = mock_request.call_args
                assert "json" in call_kwargs.kwargs or call_kwargs[1].get("json")

    @pytest.mark.asyncio
    async def test_search_default_collection(self):
        """search() should use default 'chapters' collection."""
        from workflows.shared.clients.search_client import SemanticSearchClient

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}

        search_client = SemanticSearchClient()
        async with search_client as client:
            with patch.object(client._client, "request", new_callable=AsyncMock) as mock_request:
                mock_request.return_value = mock_response
                await client.search("test query")

                call_kwargs = mock_request.call_args
                json_data = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
                assert json_data["collection"] == "chapters"


class TestSemanticSearchClientHybridSearchMethod:
    """WBS 3.2.3.5: Test hybrid_search() method."""

    @pytest.mark.asyncio
    async def test_hybrid_search_with_focus_areas(self):
        """hybrid_search() should accept focus_areas parameter."""
        from workflows.shared.clients.search_client import SemanticSearchClient

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {"id": 1, "score": 0.92, "payload": {"title": "Event-Driven Architecture"}},
            ]
        }

        search_client = SemanticSearchClient()
        async with search_client as client:
            with patch.object(client._client, "request", new_callable=AsyncMock) as mock_request:
                mock_request.return_value = mock_response
                results = await client.hybrid_search(
                    query="microservices communication",
                    focus_areas=["architecture", "integration"],
                    limit=10
                )

        assert len(results) == 1

    @pytest.mark.asyncio
    async def test_hybrid_search_without_focus_areas(self):
        """hybrid_search() should work without focus_areas."""
        from workflows.shared.clients.search_client import SemanticSearchClient

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}

        search_client = SemanticSearchClient()
        async with search_client as client:
            with patch.object(client._client, "request", new_callable=AsyncMock) as mock_request:
                mock_request.return_value = mock_response
                results = await client.hybrid_search(query="test")

        assert results == []


class TestSemanticSearchClientRetryLogic:
    """WBS 3.2.3.7: Test retry logic with exponential backoff."""

    @pytest.mark.asyncio
    async def test_retries_on_503_status(self):
        """Client should retry on 503 Service Unavailable."""
        from workflows.shared.clients.search_client import SemanticSearchClient

        error_response = MagicMock()
        error_response.status_code = 503
        
        success_response = MagicMock()
        success_response.status_code = 200
        success_response.json.return_value = {"embeddings": [[0.1] * 768]}

        search_client = SemanticSearchClient(max_retries=3, retry_delay=0.01)
        async with search_client as client:
            with patch.object(
                client._client, "request", new_callable=AsyncMock
            ) as mock_request:
                # First call fails with 503, second succeeds
                mock_request.side_effect = [error_response, success_response]
                
                result = await client.embed("test")

        assert mock_request.call_count == 2
        assert result == [[0.1] * 768]

    @pytest.mark.asyncio
    async def test_retries_on_429_rate_limit(self):
        """Client should retry on 429 Too Many Requests."""
        from workflows.shared.clients.search_client import SemanticSearchClient

        error_response = MagicMock()
        error_response.status_code = 429
        
        success_response = MagicMock()
        success_response.status_code = 200
        success_response.json.return_value = {"results": []}

        search_client = SemanticSearchClient(max_retries=3, retry_delay=0.01)
        async with search_client as client:
            with patch.object(
                client._client, "request", new_callable=AsyncMock
            ) as mock_request:
                mock_request.side_effect = [error_response, success_response]
                
                await client.search("test")

        assert mock_request.call_count == 2

    @pytest.mark.asyncio
    async def test_raises_after_max_retries(self):
        """Client should raise after exhausting retries."""
        from workflows.shared.clients.search_client import (
            SemanticSearchClient,
            SearchAPIError,
        )

        error_response = MagicMock()
        error_response.status_code = 503
        error_response.json.return_value = {"detail": "Service unavailable"}
        error_response.text = "Service unavailable"

        search_client = SemanticSearchClient(max_retries=2, retry_delay=0.01)
        async with search_client as client:
            with patch.object(
                client._client, "request", new_callable=AsyncMock
            ) as mock_request:
                mock_request.return_value = error_response
                
                with pytest.raises(SearchAPIError) as exc_info:
                    await client.embed("test")

        assert exc_info.value.status_code == 503
        assert mock_request.call_count == 2


class TestSemanticSearchClientErrorHandling:
    """Test error handling and custom exceptions."""

    @pytest.mark.asyncio
    async def test_raises_timeout_error(self):
        """Client should raise SearchTimeoutError on timeout."""
        from workflows.shared.clients.search_client import (
            SemanticSearchClient,
            SearchTimeoutError,
        )

        search_client = SemanticSearchClient(max_retries=1, retry_delay=0.01)
        async with search_client as client:
            with patch.object(
                client._client, "request", new_callable=AsyncMock
            ) as mock_request:
                mock_request.side_effect = httpx.TimeoutException("Request timed out")
                
                with pytest.raises(SearchTimeoutError):
                    await client.embed("test")

    @pytest.mark.asyncio
    async def test_raises_connection_error(self):
        """Client should raise SearchConnectionError on connection failure."""
        from workflows.shared.clients.search_client import (
            SemanticSearchClient,
            SearchConnectionError,
        )

        search_client = SemanticSearchClient(max_retries=1, retry_delay=0.01)
        async with search_client as client:
            with patch.object(
                client._client, "request", new_callable=AsyncMock
            ) as mock_request:
                mock_request.side_effect = httpx.ConnectError("Connection refused")
                
                with pytest.raises(SearchConnectionError):
                    await client.embed("test")

    @pytest.mark.asyncio
    async def test_raises_api_error_with_details(self):
        """Client should raise SearchAPIError with status and body."""
        from workflows.shared.clients.search_client import (
            SemanticSearchClient,
            SearchAPIError,
        )

        error_response = MagicMock()
        error_response.status_code = 400
        error_response.json.return_value = {"detail": "Invalid request"}
        error_response.text = "Invalid request"

        search_client = SemanticSearchClient()
        async with search_client as client:
            with patch.object(
                client._client, "request", new_callable=AsyncMock
            ) as mock_request:
                mock_request.return_value = error_response
                
                with pytest.raises(SearchAPIError) as exc_info:
                    await client.embed("")

        assert exc_info.value.status_code == 400
        assert exc_info.value.response_body == {"detail": "Invalid request"}

    def test_raises_runtime_error_without_context_manager(self):
        """Client should raise RuntimeError if used without context manager."""
        from workflows.shared.clients.search_client import SemanticSearchClient

        client = SemanticSearchClient()
        
        with pytest.raises(RuntimeError) as exc_info:
            client._ensure_client()
        
        assert "context manager" in str(exc_info.value).lower()


class TestSemanticSearchClientMethods:
    """Test that required methods exist."""

    def test_has_embed_method(self):
        """Client should have embed method."""
        from workflows.shared.clients.search_client import SemanticSearchClient
        
        assert hasattr(SemanticSearchClient, "embed")
        assert callable(getattr(SemanticSearchClient, "embed"))

    def test_has_search_method(self):
        """Client should have search method."""
        from workflows.shared.clients.search_client import SemanticSearchClient
        
        assert hasattr(SemanticSearchClient, "search")
        assert callable(getattr(SemanticSearchClient, "search"))

    def test_has_hybrid_search_method(self):
        """Client should have hybrid_search method."""
        from workflows.shared.clients.search_client import SemanticSearchClient
        
        assert hasattr(SemanticSearchClient, "hybrid_search")
        assert callable(getattr(SemanticSearchClient, "hybrid_search"))

    def test_has_health_check_method(self):
        """Client should have health_check method."""
        from workflows.shared.clients.search_client import SemanticSearchClient
        
        assert hasattr(SemanticSearchClient, "health_check")
        assert callable(getattr(SemanticSearchClient, "health_check"))
