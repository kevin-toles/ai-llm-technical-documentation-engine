"""
TDD RED Phase: Search Client Gateway Routing Tests

WBS Reference: GATEWAY_ROUTING_REFACTOR_WBS.md - Phase 2.2
Pattern: TDD RED → GREEN → REFACTOR

These tests verify that search operations route through the LLM Gateway
using the `search_corpus` tool instead of calling semantic-search directly.

Expected Behavior:
- Search requests should go through Gateway :8080
- NOT directly to semantic-search :8081
- Use Gateway tool execution endpoint

Reference Documents:
- ARCHITECTURE.md: Kitchen Brigade "Router" pattern, Tool Proxy Pattern
- llm-gateway/config/tools.json: search_corpus tool definition
- CODING_PATTERNS_ANALYSIS.md: Anti-Pattern #12 (connection pooling)
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import httpx


class TestSearchViaGateway:
    """
    TDD RED Phase: Tests for search routing through Gateway.
    
    These tests verify that search operations use the Gateway's
    search_corpus tool instead of calling semantic-search directly.
    """

    @pytest.mark.asyncio
    async def test_search_calls_gateway_tool(self):
        """
        RED TEST: Search should call Gateway search_corpus tool.
        
        Current behavior: Calls semantic-search:8081 directly (WRONG)
        Expected behavior: Calls Gateway:8080 /v1/tools/execute (CORRECT)
        
        WBS 2.2.1: test_search_calls_gateway_tool
        """
        # This test expects a GatewaySearchClient that routes through Gateway
        # Currently this client doesn't exist - will be created in GREEN phase
        
        try:
            from workflows.shared.clients.gateway_search_client import GatewaySearchClient
        except ImportError:
            pytest.fail(
                "GatewaySearchClient not found. "
                "Create workflows/shared/clients/gateway_search_client.py "
                "that routes search requests through the Gateway."
            )
        
        # Mock the Gateway HTTP client
        mock_response = {
            "results": [
                {"chunk_id": "ch1", "content": "Test content", "score": 0.95},
                {"chunk_id": "ch2", "content": "More content", "score": 0.85}
            ]
        }
        
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client.post = AsyncMock(return_value=MagicMock(
                status_code=200,
                json=MagicMock(return_value=mock_response),
                raise_for_status=MagicMock()
            ))
            mock_client_class.return_value = mock_client
            
            async with GatewaySearchClient(gateway_url="http://localhost:8080") as client:
                await client.search("domain driven design", limit=5)
            
            # Verify Gateway was called, NOT semantic-search directly
            mock_client.post.assert_called()
            call_args = mock_client.post.call_args
            
            # Should call Gateway tool execution endpoint
            assert "/v1/tools/execute" in str(call_args) or "/v1/tools" in str(call_args), (
                "Search should use Gateway /v1/tools/execute endpoint, not direct :8081 call"
            )
            
            # Verify search_corpus tool was invoked
            if call_args.kwargs.get("json"):
                payload = call_args.kwargs["json"]
                assert payload.get("tool") == "search_corpus" or payload.get("name") == "search_corpus", (
                    "Should invoke search_corpus tool via Gateway"
                )

    @pytest.mark.asyncio
    async def test_hybrid_search_via_gateway(self):
        """
        RED TEST: Hybrid search should route through Gateway.
        
        Current behavior: Calls semantic-search:8081/v1/search directly (WRONG)
        Expected behavior: Calls Gateway:8080 /v1/tools/execute (CORRECT)
        
        WBS 2.2.2: test_hybrid_search_via_gateway
        """
        try:
            from workflows.shared.clients.gateway_search_client import GatewaySearchClient
        except ImportError:
            pytest.fail(
                "GatewaySearchClient not found. "
                "This client should route hybrid_search through Gateway."
            )
        
        mock_response = {
            "results": [
                {"chunk_id": "ch1", "content": "Architecture content", "score": 0.92}
            ]
        }
        
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client.post = AsyncMock(return_value=MagicMock(
                status_code=200,
                json=MagicMock(return_value=mock_response),
                raise_for_status=MagicMock()
            ))
            mock_client_class.return_value = mock_client
            
            async with GatewaySearchClient(gateway_url="http://localhost:8080") as client:
                await client.hybrid_search(
                    query="microservices architecture",
                    focus_areas=["design", "patterns"],
                    limit=10
                )
            
            # Should route through Gateway
            mock_client.post.assert_called()
            call_url = str(mock_client.post.call_args)
            
            # Must NOT contain direct :8081 URL
            assert ":8081" not in call_url, (
                "hybrid_search should NOT call semantic-search:8081 directly. "
                "It should route through Gateway:8080."
            )

    @pytest.mark.asyncio
    async def test_embed_via_gateway(self):
        """
        RED TEST: Embedding generation should route through Gateway.
        
        WBS 2.2.3: test_embed_via_gateway
        """
        try:
            from workflows.shared.clients.gateway_search_client import GatewaySearchClient
        except ImportError:
            pytest.fail("GatewaySearchClient not found.")
        
        mock_response = {
            "embeddings": [[0.1, 0.2, 0.3, 0.4]],
            "model": "text-embedding-3-small"
        }
        
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client.post = AsyncMock(return_value=MagicMock(
                status_code=200,
                json=MagicMock(return_value=mock_response),
                raise_for_status=MagicMock()
            ))
            mock_client_class.return_value = mock_client
            
            async with GatewaySearchClient(gateway_url="http://localhost:8080") as client:
                await client.embed("domain driven design")
            
            # Should route through Gateway
            mock_client.post.assert_called()

    @pytest.mark.asyncio
    async def test_no_direct_semantic_search_calls(self):
        """
        RED TEST: Verify no direct calls to semantic-search:8081.
        
        This is a critical test - the GatewaySearchClient should NEVER
        make direct HTTP calls to :8081. All traffic must go through
        the Gateway at :8080.
        """
        try:
            from workflows.shared.clients.gateway_search_client import GatewaySearchClient
        except ImportError:
            pytest.fail("GatewaySearchClient not found.")
        
        # Create client with explicit Gateway URL
        client = GatewaySearchClient(gateway_url="http://localhost:8080")
        
        # Verify the base_url is Gateway, not semantic-search
        assert hasattr(client, "_gateway_url") or hasattr(client, "gateway_url"), (
            "GatewaySearchClient should have gateway_url attribute"
        )
        
        url = getattr(client, "_gateway_url", None) or getattr(client, "gateway_url", None)
        
        assert ":8080" in url, (
            f"GatewaySearchClient should use Gateway:8080, not {url}"
        )
        assert ":8081" not in url, (
            f"GatewaySearchClient should NOT use semantic-search:8081 directly. Got: {url}"
        )


class TestGatewaySearchClientInterface:
    """Tests for GatewaySearchClient interface compliance."""

    def test_gateway_search_client_has_search_method(self):
        """GatewaySearchClient should have search() method."""
        try:
            from workflows.shared.clients.gateway_search_client import GatewaySearchClient
            
            assert hasattr(GatewaySearchClient, "search"), (
                "GatewaySearchClient must have search() method"
            )
        except ImportError:
            pytest.fail("GatewaySearchClient not found.")

    def test_gateway_search_client_has_hybrid_search_method(self):
        """GatewaySearchClient should have hybrid_search() method."""
        try:
            from workflows.shared.clients.gateway_search_client import GatewaySearchClient
            
            assert hasattr(GatewaySearchClient, "hybrid_search"), (
                "GatewaySearchClient must have hybrid_search() method"
            )
        except ImportError:
            pytest.fail("GatewaySearchClient not found.")

    def test_gateway_search_client_is_async_context_manager(self):
        """GatewaySearchClient should support async context manager."""
        try:
            from workflows.shared.clients.gateway_search_client import GatewaySearchClient
            
            assert hasattr(GatewaySearchClient, "__aenter__"), (
                "GatewaySearchClient must support async context manager (__aenter__)"
            )
            assert hasattr(GatewaySearchClient, "__aexit__"), (
                "GatewaySearchClient must support async context manager (__aexit__)"
            )
        except ImportError:
            pytest.fail("GatewaySearchClient not found.")
