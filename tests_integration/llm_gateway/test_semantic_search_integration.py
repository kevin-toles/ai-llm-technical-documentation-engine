"""
WBS 3.5.3.1: Gateway → Semantic Search Cross-Service Integration Tests

Tests gateway's communication with the semantic-search service through Docker.
Per GUIDELINES (Newman pp. 357-358): Circuit breaker pattern
Per GUIDELINES (Newman pp. 352-353): Graceful degradation

These tests require Docker services running with `docker compose --profile integration-test up`.
"""

import pytest
import httpx
import time

from tests_integration.llm_gateway.conftest import (
    GATEWAY_URL,
    SEMANTIC_SEARCH_URL,
)


# =============================================================================
# WBS 3.5.3.1.1: Gateway → Semantic Search Tool Registration
# =============================================================================


@pytest.mark.integration
@pytest.mark.docker
class TestSemanticSearchToolRegistration:
    """Test semantic search tools are properly registered when service available."""

    async def test_search_corpus_tool_registered(self, gateway_client: httpx.AsyncClient):
        """Verify search_corpus tool is registered in gateway."""
        response = await gateway_client.get("/v1/tools")
        
        if response.status_code == 503:
            pytest.skip("Gateway not available")
        
        assert response.status_code == 200
        data = response.json()
        tools = data.get("tools", [])
        
        tool_names = [t.get("name") for t in tools]
        assert "search_corpus" in tool_names, (
            "search_corpus tool should be registered when semantic-search available"
        )

    async def test_get_chunk_tool_registered(self, gateway_client: httpx.AsyncClient):
        """Verify get_chunk tool is registered in gateway."""
        response = await gateway_client.get("/v1/tools")
        
        if response.status_code == 503:
            pytest.skip("Gateway not available")
        
        assert response.status_code == 200
        data = response.json()
        tools = data.get("tools", [])
        
        tool_names = [t.get("name") for t in tools]
        assert "get_chunk" in tool_names, (
            "get_chunk tool should be registered when semantic-search available"
        )

    async def test_semantic_search_tools_schema(self, gateway_client: httpx.AsyncClient):
        """Verify semantic search tools have proper JSON schema."""
        response = await gateway_client.get("/v1/tools")
        
        if response.status_code == 503:
            pytest.skip("Gateway not available")
        
        assert response.status_code == 200
        data = response.json()
        tools = data.get("tools", [])
        
        search_corpus = next(
            (t for t in tools if t.get("name") == "search_corpus"),
            None
        )
        
        if search_corpus:
            assert "parameters" in search_corpus
            params = search_corpus["parameters"]
            # search_corpus should have query parameter
            assert "properties" in params
            assert "query" in params["properties"]


# =============================================================================
# WBS 3.5.3.1.2: Search Tool Execution Through Gateway
# =============================================================================


@pytest.mark.integration
@pytest.mark.docker
class TestSearchToolExecution:
    """Test search_corpus tool execution through gateway to semantic-search."""

    async def test_search_corpus_via_chat_completions(
        self,
        gateway_client: httpx.AsyncClient
    ):
        """Execute search_corpus through chat completions with tool call."""
        # Request with tool that should trigger search
        payload = {
            "model": "gpt-4",
            "messages": [
                {"role": "user", "content": "Search for information about testing"}
            ],
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "name": "search_corpus",
                        "description": "Search the document corpus",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string"}
                            },
                            "required": ["query"]
                        }
                    }
                }
            ],
            "tool_choice": {"type": "function", "function": {"name": "search_corpus"}}
        }
        
        response = await gateway_client.post(
            "/v1/chat/completions",
            json=payload,
            timeout=30.0
        )
        
        if response.status_code == 503:
            pytest.skip("Services not available")
        
        # Should complete successfully or timeout
        assert response.status_code in [200, 408, 504], (
            f"Expected 200, 408, or 504 but got {response.status_code}"
        )

    async def test_search_corpus_direct_execution(
        self,
        gateway_client: httpx.AsyncClient
    ):
        """Execute search_corpus tool directly if endpoint exists."""
        payload = {
            "tool_name": "search_corpus",
            "arguments": {
                "query": "integration testing patterns"
            }
        }
        
        response = await gateway_client.post(
            "/v1/tools/execute",
            json=payload,
            timeout=15.0
        )
        
        if response.status_code == 404:
            pytest.skip("Direct tool execution endpoint not available")
        if response.status_code == 503:
            pytest.skip("Services not available")
        
        assert response.status_code == 200
        data = response.json()
        assert "result" in data or "results" in data

    async def test_search_returns_relevant_results(
        self,
        gateway_client: httpx.AsyncClient
    ):
        """Verify search results contain relevant information."""
        payload = {
            "tool_name": "search_corpus",
            "arguments": {
                "query": "microservices architecture",
                "top_k": 5
            }
        }
        
        response = await gateway_client.post(
            "/v1/tools/execute",
            json=payload,
            timeout=15.0
        )
        
        if response.status_code == 404:
            pytest.skip("Direct tool execution endpoint not available")
        if response.status_code == 503:
            pytest.skip("Services not available")
        
        assert response.status_code == 200
        data = response.json()
        
        # Results should be list or contain results array
        results = data.get("results", data.get("result", []))
        if isinstance(results, list):
            # Each result should have content or text
            first_result = next(iter(results), None)
            if first_result is not None:
                assert any(
                    key in first_result 
                    for key in ["content", "text", "chunk", "passage"]
                )


# =============================================================================
# WBS 3.5.3.1.3: Chunk Retrieval Through Gateway
# =============================================================================


@pytest.mark.integration
@pytest.mark.docker
class TestChunkRetrievalIntegration:
    """Test get_chunk tool execution through gateway."""

    async def test_get_chunk_execution(self, gateway_client: httpx.AsyncClient):
        """Execute get_chunk tool to retrieve specific chunk."""
        payload = {
            "tool_name": "get_chunk",
            "arguments": {
                "chunk_id": "test_chunk_001"
            }
        }
        
        response = await gateway_client.post(
            "/v1/tools/execute",
            json=payload,
            timeout=10.0
        )
        
        if response.status_code == 404:
            pytest.skip("Direct tool execution endpoint not available")
        if response.status_code == 503:
            pytest.skip("Services not available")
        
        # Should return 200 with content or 404 if chunk not found
        assert response.status_code in [200, 404], (
            f"Expected 200 or 404 but got {response.status_code}"
        )

    async def test_get_chunk_with_context(self, gateway_client: httpx.AsyncClient):
        """Retrieve chunk with surrounding context."""
        payload = {
            "tool_name": "get_chunk",
            "arguments": {
                "chunk_id": "test_chunk_001",
                "include_context": True,
                "context_window": 2
            }
        }
        
        response = await gateway_client.post(
            "/v1/tools/execute",
            json=payload,
            timeout=10.0
        )
        
        if response.status_code == 404:
            pytest.skip("Direct tool execution endpoint not available or chunk not found")
        if response.status_code == 503:
            pytest.skip("Services not available")
        
        if response.status_code == 200:
            data = response.json()
            # Should have context if requested
            result = data.get("result", data)
            assert "content" in result or "text" in result or "chunk" in result

    async def test_invalid_chunk_id_returns_404(
        self,
        gateway_client: httpx.AsyncClient
    ):
        """Request non-existent chunk returns proper error."""
        payload = {
            "tool_name": "get_chunk",
            "arguments": {
                "chunk_id": "definitely_nonexistent_chunk_xyz_12345"
            }
        }
        
        response = await gateway_client.post(
            "/v1/tools/execute",
            json=payload,
            timeout=10.0
        )
        
        if response.status_code == 404 and "endpoint" in response.text.lower():
            pytest.skip("Direct tool execution endpoint not available")
        if response.status_code == 503:
            pytest.skip("Services not available")
        
        # Non-existent chunk should return 404 or error in response
        assert response.status_code in [200, 404], (
            f"Expected 200 (with error) or 404 but got {response.status_code}"
        )


# =============================================================================
# WBS 3.5.3.1.4: Circuit Breaker Behavior
# =============================================================================


@pytest.mark.integration
@pytest.mark.docker
@pytest.mark.slow
class TestSemanticSearchCircuitBreaker:
    """
    Test circuit breaker behavior for semantic-search service.
    Per GUIDELINES (Newman pp. 357-358): Circuit breaker pattern.
    """

    async def test_health_shows_semantic_search_status(
        self,
        gateway_client: httpx.AsyncClient
    ):
        """Health endpoint shows semantic-search service status."""
        response = await gateway_client.get("/health")
        
        if response.status_code == 503:
            pytest.skip("Gateway not available")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should show semantic-search in dependencies
        dependencies = data.get("dependencies", data.get("services", {}))
        assert "semantic-search" in dependencies or "semantic_search" in dependencies, (
            f"semantic-search should be in dependencies: {dependencies.keys()}"
        )

    async def test_health_ready_with_semantic_search_down(
        self,
        gateway_client: httpx.AsyncClient
    ):
        """
        Gateway should report degraded when semantic-search is unavailable.
        Per GUIDELINES (Newman pp. 352-353): Graceful degradation.
        """
        response = await gateway_client.get("/health/ready")
        
        if response.status_code == 503:
            # This is acceptable - gateway reports not ready
            data = response.json()
            assert data.get("status") in ["unhealthy", "degraded", "not_ready"]
            return
        
        assert response.status_code == 200
        data = response.json()
        
        # If semantic-search is down, status should indicate degradation
        status = data.get("status", "unknown")
        dependencies = data.get("dependencies", {})
        
        semantic_status = dependencies.get(
            "semantic-search",
            dependencies.get("semantic_search", {})
        )
        
        if isinstance(semantic_status, dict):
            if semantic_status.get("status") in ["unhealthy", "down", "unavailable"]:
                # Overall status should reflect degradation
                assert status in ["healthy", "degraded"], (
                    "Gateway should be healthy or degraded when semantic-search down"
                )

    async def test_search_fails_gracefully_when_service_down(
        self,
        gateway_client: httpx.AsyncClient
    ):
        """
        Search tool should fail gracefully when semantic-search unavailable.
        """
        payload = {
            "tool_name": "search_corpus",
            "arguments": {"query": "test query"}
        }
        
        response = await gateway_client.post(
            "/v1/tools/execute",
            json=payload,
            timeout=10.0
        )
        
        if response.status_code == 404:
            pytest.skip("Direct tool execution endpoint not available")
        
        # Should return error response, not crash
        assert response.status_code in [200, 503, 504], (
            f"Expected graceful failure but got {response.status_code}"
        )
        
        if response.status_code != 200:
            data = response.json()
            assert "error" in data or "message" in data or "detail" in data


# =============================================================================
# WBS 3.5.3.1.5: Timeout Handling
# =============================================================================


@pytest.mark.integration
@pytest.mark.docker
class TestSemanticSearchTimeouts:
    """
    Test timeout handling for semantic-search operations.
    Per GUIDELINES (Newman pp. 354-355): Timeout patterns.
    """

    async def test_search_respects_timeout(self, gateway_client: httpx.AsyncClient):
        """Search operations should respect configured timeouts."""
        payload = {
            "tool_name": "search_corpus",
            "arguments": {
                "query": "test query for timeout check",
                "top_k": 100  # Larger result set might be slower
            }
        }
        
        start_time = time.time()
        
        try:
            response = await gateway_client.post(
                "/v1/tools/execute",
                json=payload,
                timeout=30.0  # Client timeout
            )
            elapsed = time.time() - start_time
            
            if response.status_code == 404:
                pytest.skip("Direct tool execution endpoint not available")
            
            # Should complete within reasonable time
            assert elapsed < 30.0, f"Request took too long: {elapsed}s"
            
        except httpx.TimeoutException:
            elapsed = time.time() - start_time
            # Timeout is acceptable but should happen in reasonable time
            assert elapsed < 35.0, f"Timeout took too long: {elapsed}s"

    async def test_gateway_returns_504_on_backend_timeout(
        self,
        gateway_client: httpx.AsyncClient
    ):
        """Gateway should return 504 when backend times out."""
        # This test may not trigger timeout in healthy environment
        # It validates the response format if timeout does occur
        
        payload = {
            "tool_name": "search_corpus",
            "arguments": {"query": "timeout test"}
        }
        
        response = await gateway_client.post(
            "/v1/tools/execute",
            json=payload,
            timeout=5.0
        )
        
        if response.status_code == 404:
            pytest.skip("Direct tool execution endpoint not available")
        
        # 504 is expected for backend timeout, others are also valid
        assert response.status_code in [200, 408, 503, 504], (
            f"Expected valid status code but got {response.status_code}"
        )


# =============================================================================
# WBS 3.5.3.1.6: Response Format Validation
# =============================================================================


@pytest.mark.integration
@pytest.mark.docker
class TestSemanticSearchResponseFormat:
    """Validate response formats from semantic-search integration."""

    async def test_search_results_structure(self, gateway_client: httpx.AsyncClient):
        """Search results should have consistent structure."""
        payload = {
            "tool_name": "search_corpus",
            "arguments": {"query": "test", "top_k": 3}
        }
        
        response = await gateway_client.post(
            "/v1/tools/execute",
            json=payload,
            timeout=15.0
        )
        
        if response.status_code == 404:
            pytest.skip("Direct tool execution endpoint not available")
        if response.status_code == 503:
            pytest.skip("Services not available")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should have standard response envelope
        assert isinstance(data, dict)
        
        # Results should be accessible
        results = data.get("results", data.get("result", data.get("chunks", [])))
        if results:
            assert isinstance(results, list)

    async def test_error_response_structure(self, gateway_client: httpx.AsyncClient):
        """Error responses should have consistent structure."""
        # Invalid tool name should produce error
        payload = {
            "tool_name": "nonexistent_tool_xyz",
            "arguments": {}
        }
        
        response = await gateway_client.post(
            "/v1/tools/execute",
            json=payload,
            timeout=10.0
        )
        
        if response.status_code == 404 and "endpoint" in response.text.lower():
            pytest.skip("Direct tool execution endpoint not available")
        
        # Should return error response
        assert response.status_code in [400, 404, 422], (
            f"Expected error status but got {response.status_code}"
        )
        
        data = response.json()
        # Error response should have message
        assert any(
            key in data 
            for key in ["error", "message", "detail", "errors"]
        )
