"""
WBS M3.1: SBERT Client Unit Tests

TDD tests for SBERTClient - HTTP client for Code-Orchestrator SBERT API.

Reference Documents:
- SBERT_EXTRACTION_MIGRATION_WBS.md: M3.1 API Client Implementation
- CODING_PATTERNS_ANALYSIS.md: Anti-Pattern #12 (connection pooling), #7 (exception shadowing)
- Code-Orchestrator-Service/docs/ARCHITECTURE.md: SBERT API endpoints

Anti-Patterns Validated:
- #7: Exception naming follows *Error suffix pattern
- #12: Connection pooling via shared httpx.AsyncClient
- S1172: No unused parameters
- S1192: No duplicated literals
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


# =============================================================================
# M3.1.1: RED Test - SBERTClient Class Exists
# =============================================================================


class TestSBERTClientExists:
    """M3.1.1: Test that SBERTClient class exists."""

    def test_sbert_client_class_exists(self):
        """
        RED TEST: SBERTClient class can be imported.
        
        Acceptance Criteria: `SBERTClient` class exists in clients module.
        """
        try:
            from workflows.shared.clients.sbert_client import SBERTClient
            assert SBERTClient is not None
        except ImportError:
            pytest.fail("SBERTClient class not found - create workflows/shared/clients/sbert_client.py")

    def test_sbert_client_protocol_exists(self):
        """
        RED TEST: SBERTClientProtocol exists for duck typing.
        
        Reference: CODING_PATTERNS §4.4 - Protocol compliance for interface contracts.
        """
        try:
            from workflows.shared.clients.sbert_client import SBERTClientProtocol
            assert SBERTClientProtocol is not None
        except ImportError:
            pytest.fail("SBERTClientProtocol not found")

    def test_sbert_client_error_exists(self):
        """
        RED TEST: SBERTClientError base exception exists.
        
        Anti-Pattern #7: Use namespaced exceptions (not ConnectionError/TimeoutError).
        """
        try:
            from workflows.shared.clients.sbert_client import SBERTClientError
            assert issubclass(SBERTClientError, Exception)
        except ImportError:
            pytest.fail("SBERTClientError not found")

    def test_sbert_timeout_error_exists(self):
        """
        RED TEST: SBERTTimeoutError exception exists.
        
        Anti-Pattern #7: Namespaced exception, not shadowing builtins.TimeoutError.
        """
        try:
            from workflows.shared.clients.sbert_client import SBERTTimeoutError
            from workflows.shared.clients.sbert_client import SBERTClientError
            assert issubclass(SBERTTimeoutError, SBERTClientError)
        except ImportError:
            pytest.fail("SBERTTimeoutError not found")

    def test_sbert_connection_error_exists(self):
        """
        RED TEST: SBERTConnectionError exception exists.
        
        Anti-Pattern #7: Namespaced exception, not shadowing builtins.ConnectionError.
        """
        try:
            from workflows.shared.clients.sbert_client import SBERTConnectionError
            from workflows.shared.clients.sbert_client import SBERTClientError
            assert issubclass(SBERTConnectionError, SBERTClientError)
        except ImportError:
            pytest.fail("SBERTConnectionError not found")

    def test_sbert_api_error_exists(self):
        """
        RED TEST: SBERTAPIError exception for 4xx/5xx responses.
        """
        try:
            from workflows.shared.clients.sbert_client import SBERTAPIError
            from workflows.shared.clients.sbert_client import SBERTClientError
            assert issubclass(SBERTAPIError, SBERTClientError)
        except ImportError:
            pytest.fail("SBERTAPIError not found")


# =============================================================================
# M3.1.3: RED Test - Client Can Call /v1/embeddings
# =============================================================================


class TestSBERTClientEmbeddings:
    """M3.1.3: Test client can call /v1/embeddings endpoint."""

    @pytest.mark.asyncio
    async def test_get_embeddings_method_exists(self):
        """
        RED TEST: Client has async get_embeddings() method.
        """
        try:
            from workflows.shared.clients.sbert_client import SBERTClient
            client = SBERTClient(base_url="http://localhost:8083")
            assert hasattr(client, "get_embeddings"), "Client should have get_embeddings() method"
            assert callable(client.get_embeddings)
        except ImportError:
            pytest.fail("SBERTClient not found")

    @pytest.mark.asyncio
    async def test_get_embeddings_accepts_texts(self):
        """
        GREEN TEST: get_embeddings() accepts list of texts using FakeSBERTClient.
        
        API: POST /v1/embeddings {"texts": ["text1", "text2"]}
        Pattern: Use FakeSBERTClient to avoid real HTTP calls.
        """
        try:
            from workflows.shared.clients.sbert_client import FakeSBERTClient
            
            fake = FakeSBERTClient()
            fake.set_embeddings({"test text": [0.1] * 384})
            
            async with fake:
                embeddings = await fake.get_embeddings(texts=["test text"])
                    
            assert isinstance(embeddings, list)
            assert len(embeddings) == 1
            assert len(embeddings[0]) == 384
        except ImportError:
            pytest.fail("FakeSBERTClient not found")

    @pytest.mark.asyncio
    async def test_get_embeddings_returns_384_dimensions(self):
        """
        GREEN TEST: Embeddings have 384 dimensions (MiniLM-L6-v2).
        
        Reference: SBERT_EXTRACTION_MIGRATION_WBS.md M2.2.6
        Pattern: Use FakeSBERTClient to verify dimensions.
        """
        try:
            from workflows.shared.clients.sbert_client import FakeSBERTClient, EMBEDDING_DIMENSIONS
            
            fake = FakeSBERTClient()
            fake.set_embeddings({
                "text1": [0.1] * EMBEDDING_DIMENSIONS,
                "text2": [0.2] * EMBEDDING_DIMENSIONS,
            })
            
            async with fake:
                embeddings = await fake.get_embeddings(texts=["text1", "text2"])
                    
            for embedding in embeddings:
                assert len(embedding) == 384, f"Expected 384 dimensions, got {len(embedding)}"
        except ImportError:
            pytest.fail("FakeSBERTClient not found")


# =============================================================================
# M3.1.5: RED Test - Client Can Call /v1/similarity
# =============================================================================


class TestSBERTClientSimilarity:
    """M3.1.5: Test client can call /v1/similarity endpoint."""

    @pytest.mark.asyncio
    async def test_get_similarity_method_exists(self):
        """
        RED TEST: Client has async get_similarity() method.
        """
        try:
            from workflows.shared.clients.sbert_client import SBERTClient
            client = SBERTClient(base_url="http://localhost:8083")
            assert hasattr(client, "get_similarity"), "Client should have get_similarity() method"
            assert callable(client.get_similarity)
        except ImportError:
            pytest.fail("SBERTClient not found")

    @pytest.mark.asyncio
    async def test_get_similarity_accepts_text_pair(self):
        """
        GREEN TEST: get_similarity() accepts text1 and text2 parameters.
        
        API: POST /v1/similarity {"text1": "...", "text2": "..."}
        Pattern: Use FakeSBERTClient to avoid real HTTP calls.
        """
        try:
            from workflows.shared.clients.sbert_client import FakeSBERTClient
            
            fake = FakeSBERTClient()
            fake.set_similarity("cat", "dog", 0.85)
            
            async with fake:
                score = await fake.get_similarity(text1="cat", text2="dog")
                    
            assert isinstance(score, float)
            assert 0.0 <= score <= 1.0
        except ImportError:
            pytest.fail("FakeSBERTClient not found")

    @pytest.mark.asyncio
    async def test_get_similarity_returns_score_in_range(self):
        """
        GREEN TEST: Similarity score is between 0.0 and 1.0.
        
        Pattern: Use FakeSBERTClient to verify score range.
        """
        try:
            from workflows.shared.clients.sbert_client import FakeSBERTClient
            
            fake = FakeSBERTClient()
            fake.set_similarity("hello", "hi", 0.72)
            
            async with fake:
                score = await fake.get_similarity(text1="hello", text2="hi")
                    
            assert 0.0 <= score <= 1.0, f"Score {score} not in valid range [0.0, 1.0]"
        except ImportError:
            pytest.fail("FakeSBERTClient not found")


# =============================================================================
# M3.1.7: RED Test - Connection Pooling
# =============================================================================


class TestSBERTClientConnectionPooling:
    """M3.1.7: Test client implements connection pooling."""

    def test_client_has_client_attribute(self):
        """
        RED TEST: Client has _client attribute for connection pooling.
        
        Anti-Pattern #12: Must not create new client per request.
        """
        try:
            from workflows.shared.clients.sbert_client import SBERTClient
            client = SBERTClient(base_url="http://localhost:8083")
            assert hasattr(client, "_client"), "Client should have _client attribute"
        except ImportError:
            pytest.fail("SBERTClient not found")

    @pytest.mark.asyncio
    async def test_client_uses_context_manager(self):
        """
        RED TEST: Client uses async context manager pattern.
        
        Pattern: Connection pooling via context manager (GUIDELINES p. 2313)
        """
        try:
            from workflows.shared.clients.sbert_client import SBERTClient
            client = SBERTClient(base_url="http://localhost:8083")
            
            assert hasattr(client, "__aenter__"), "Client should support async context manager"
            assert hasattr(client, "__aexit__"), "Client should support async context manager"
        except ImportError:
            pytest.fail("SBERTClient not found")

    @pytest.mark.asyncio
    async def test_client_creates_single_httpx_client(self):
        """
        RED TEST: Client creates single httpx.AsyncClient on __aenter__.
        
        Anti-Pattern #12: Avoid creating new httpx.AsyncClient per request.
        """
        try:
            from workflows.shared.clients.sbert_client import SBERTClient
            import httpx
            
            client = SBERTClient(base_url="http://localhost:8083")
            
            # Before entering context, _client should be None
            assert client._client is None, "Client should be None before context entry"
            
            async with client:
                # After entering, _client should be httpx.AsyncClient
                assert client._client is not None, "Client should be initialized after context entry"
                assert isinstance(client._client, httpx.AsyncClient)
                
            # After exiting, _client should be None again
            assert client._client is None, "Client should be None after context exit"
        except ImportError:
            pytest.fail("SBERTClient not found")


# =============================================================================
# Error Handling Tests
# =============================================================================


class TestSBERTClientErrorHandling:
    """Test error handling follows anti-pattern guidelines."""

    @pytest.mark.asyncio
    async def test_connection_error_on_unreachable_host(self):
        """
        RED TEST: SBERTConnectionError raised when host unreachable.
        """
        try:
            from workflows.shared.clients.sbert_client import (
                SBERTClient,
                SBERTConnectionError
            )
            import httpx
            
            client = SBERTClient(base_url="http://localhost:9999")
            
            with patch.object(client, "_client") as mock_client:
                mock_client.post = AsyncMock(side_effect=httpx.ConnectError("Connection refused"))
                
                async with client:
                    with pytest.raises(SBERTConnectionError):
                        await client.get_embeddings(texts=["test"])
        except ImportError:
            pytest.fail("SBERTClient or SBERTConnectionError not found")

    @pytest.mark.asyncio
    async def test_timeout_error_on_slow_response(self):
        """
        GREEN TEST: SBERTTimeoutError raised on timeout.
        
        Pattern: Use httpx.AsyncClient patch for proper mocking.
        """
        try:
            from workflows.shared.clients.sbert_client import (
                SBERTClient,
                SBERTTimeoutError
            )
            import httpx
            
            with patch("httpx.AsyncClient") as MockClient:
                mock_instance = AsyncMock()
                mock_instance.request = AsyncMock(side_effect=httpx.TimeoutException("Timeout"))
                mock_instance.aclose = AsyncMock()
                MockClient.return_value = mock_instance
                
                client = SBERTClient(base_url="http://localhost:8083", timeout=0.001)
                
                async with client:
                    with pytest.raises(SBERTTimeoutError):
                        await client.get_embeddings(texts=["test"])
        except ImportError:
            pytest.fail("SBERTClient or SBERTTimeoutError not found")

    @pytest.mark.asyncio
    async def test_api_error_on_4xx_response(self):
        """
        GREEN TEST: SBERTAPIError raised on 4xx responses.
        
        Pattern: Use httpx.AsyncClient patch for proper mocking.
        """
        try:
            from workflows.shared.clients.sbert_client import (
                SBERTClient,
                SBERTAPIError
            )
            
            with patch("httpx.AsyncClient") as MockClient:
                mock_response = MagicMock()
                mock_response.status_code = 400
                mock_response.text = "Bad Request"
                mock_response.json.return_value = {"detail": "Invalid input"}
                
                mock_instance = AsyncMock()
                mock_instance.request = AsyncMock(return_value=mock_response)
                mock_instance.aclose = AsyncMock()
                MockClient.return_value = mock_instance
                
                client = SBERTClient(base_url="http://localhost:8083")
                
                async with client:
                    with pytest.raises(SBERTAPIError) as exc_info:
                        await client.get_embeddings(texts=["test"])
                    
                assert exc_info.value.status_code == 400
        except ImportError:
            pytest.fail("SBERTClient or SBERTAPIError not found")


# =============================================================================
# Constants Tests (S1192 Prevention)
# =============================================================================


class TestSBERTClientConstants:
    """Test that constants are properly extracted (S1192 prevention)."""

    def test_default_embeddings_endpoint_constant(self):
        """
        S1192 Prevention: Default embeddings endpoint as constant.
        """
        try:
            from workflows.shared.clients.sbert_client import _DEFAULT_EMBEDDINGS_ENDPOINT
            assert _DEFAULT_EMBEDDINGS_ENDPOINT == "/v1/embeddings"
        except ImportError:
            pytest.fail("_DEFAULT_EMBEDDINGS_ENDPOINT constant not found")

    def test_default_similarity_endpoint_constant(self):
        """
        S1192 Prevention: Default similarity endpoint as constant.
        """
        try:
            from workflows.shared.clients.sbert_client import _DEFAULT_SIMILARITY_ENDPOINT
            assert _DEFAULT_SIMILARITY_ENDPOINT == "/v1/similarity"
        except ImportError:
            pytest.fail("_DEFAULT_SIMILARITY_ENDPOINT constant not found")

    def test_embedding_dimensions_constant(self):
        """
        S1192 Prevention: Embedding dimensions as constant.
        """
        try:
            from workflows.shared.clients.sbert_client import EMBEDDING_DIMENSIONS
            assert EMBEDDING_DIMENSIONS == 384
        except ImportError:
            pytest.fail("EMBEDDING_DIMENSIONS constant not found")
