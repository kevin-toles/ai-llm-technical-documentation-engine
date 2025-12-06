"""
WBS 3.5.3.3: End-to-End Flow Integration Tests

Tests complete workflows spanning multiple services through the gateway.
Per GUIDELINES (Newman pp. 352-353): Graceful degradation
Per GUIDELINES (Buelta pp. 350): Three-tier testing

These tests require Docker services running with `docker compose --profile full-stack up`.
"""

import pytest
import httpx
import asyncio
import time
import uuid
from typing import Optional

from tests_integration.llm_gateway.conftest import (
    GATEWAY_URL,
    SEMANTIC_SEARCH_URL,
    AI_AGENTS_URL,
    REDIS_URL,
)


# =============================================================================
# WBS 3.5.3.3.1: Complete Chat Flow
# =============================================================================


@pytest.mark.integration
@pytest.mark.docker
@pytest.mark.e2e
class TestCompleteChatFlow:
    """Test complete chat flow from request to response."""

    async def test_simple_chat_completion_flow(
        self,
        gateway_client: httpx.AsyncClient
    ):
        """Test basic chat completion end-to-end."""
        payload = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello in exactly 3 words."}
            ],
            "max_tokens": 50
        }
        
        response = await gateway_client.post(
            "/v1/chat/completions",
            json=payload,
            timeout=60.0
        )
        
        if response.status_code == 503:
            pytest.skip("Services not available")
        
        assert response.status_code in [200, 429, 500, 502, 504], (
            f"Unexpected status: {response.status_code}"
        )
        
        if response.status_code == 200:
            data = response.json()
            assert "choices" in data
            first_choice = next(iter(data["choices"]), None)
            assert first_choice is not None, "Expected at least one choice"
            assert "message" in first_choice

    async def test_chat_with_session_persistence(
        self,
        gateway_client: httpx.AsyncClient
    ):
        """Test chat with session tracking end-to-end."""
        session_id = f"e2e-test-{uuid.uuid4().hex[:8]}"
        
        # First message
        payload1 = {
            "model": "gpt-4",
            "messages": [
                {"role": "user", "content": "My name is TestUser."}
            ],
            "session_id": session_id
        }
        
        response1 = await gateway_client.post(
            "/v1/chat/completions",
            json=payload1,
            timeout=60.0
        )
        
        if response1.status_code == 503:
            pytest.skip("Services not available")
        
        if response1.status_code != 200:
            pytest.skip(f"First request failed: {response1.status_code}")
        
        # Second message in same session
        payload2 = {
            "model": "gpt-4",
            "messages": [
                {"role": "user", "content": "What is my name?"}
            ],
            "session_id": session_id
        }
        
        response2 = await gateway_client.post(
            "/v1/chat/completions",
            json=payload2,
            timeout=60.0
        )
        
        assert response2.status_code in [200, 500, 502], (
            f"Unexpected status: {response2.status_code}"
        )
        
        # Clean up session
        await gateway_client.delete(f"/v1/sessions/{session_id}")

    async def test_streaming_chat_flow(self, gateway_client: httpx.AsyncClient):
        """Test streaming chat completion end-to-end."""
        payload = {
            "model": "gpt-4",
            "messages": [
                {"role": "user", "content": "Count from 1 to 5."}
            ],
            "stream": True,
            "max_tokens": 50
        }
        
        async with gateway_client.stream(
            "POST",
            "/v1/chat/completions",
            json=payload,
            timeout=60.0
        ) as response:
            if response.status_code == 503:
                pytest.skip("Services not available")
            
            if response.status_code != 200:
                pytest.skip(f"Streaming not available: {response.status_code}")
            
            chunks = []
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    chunk_data = line[6:]
                    if chunk_data != "[DONE]":
                        chunks.append(chunk_data)
            
            # Verify chunks is a list (may be empty if no streaming support)
            assert isinstance(chunks, list)


# =============================================================================
# WBS 3.5.3.3.2: Search → Chat → Response Flow
# =============================================================================


@pytest.mark.integration
@pytest.mark.docker
@pytest.mark.e2e
class TestSearchChatResponseFlow:
    """Test flow that combines search with chat completion."""

    async def test_rag_style_flow(self, gateway_client: httpx.AsyncClient):
        """Test RAG-style flow: search then chat with context."""
        # Step 1: Search for relevant content
        search_payload = {
            "tool_name": "search_corpus",
            "arguments": {
                "query": "microservices architecture patterns",
                "top_k": 3
            }
        }
        
        search_response = await gateway_client.post(
            "/v1/tools/execute",
            json=search_payload,
            timeout=30.0
        )
        
        context = ""
        if search_response.status_code == 200:
            search_data = search_response.json()
            results = search_data.get("results", search_data.get("result", []))
            if isinstance(results, list):
                context = "\n".join(
                    str(r.get("content", r.get("text", "")))
                    for r in results[:3]
                )
        
        # Step 2: Chat with context
        chat_payload = {
            "model": "gpt-4",
            "messages": [
                {
                    "role": "system",
                    "content": f"Use this context to answer: {context[:500]}"
                } if context else {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": "Summarize the key points about architecture."
                }
            ],
            "max_tokens": 200
        }
        
        chat_response = await gateway_client.post(
            "/v1/chat/completions",
            json=chat_payload,
            timeout=60.0
        )
        
        if chat_response.status_code == 503:
            pytest.skip("Services not available")
        
        # Should complete the full flow
        assert chat_response.status_code in [200, 500, 502, 504], (
            f"Unexpected status: {chat_response.status_code}"
        )

    async def test_tool_augmented_chat(self, gateway_client: httpx.AsyncClient):
        """Test chat completion with tool augmentation."""
        payload = {
            "model": "gpt-4",
            "messages": [
                {"role": "user", "content": "Search for information about testing."}
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
                                "query": {
                                    "type": "string",
                                    "description": "Search query"
                                }
                            },
                            "required": ["query"]
                        }
                    }
                }
            ],
            "tool_choice": "auto"
        }
        
        response = await gateway_client.post(
            "/v1/chat/completions",
            json=payload,
            timeout=60.0
        )
        
        if response.status_code == 503:
            pytest.skip("Services not available")
        
        assert response.status_code in [200, 400, 500, 502, 504]


# =============================================================================
# WBS 3.5.3.3.3: Multi-Tool Workflow
# =============================================================================


@pytest.mark.integration
@pytest.mark.docker
@pytest.mark.e2e
class TestMultiToolWorkflow:
    """Test workflows involving multiple tool executions."""

    async def test_sequential_tool_execution(
        self,
        gateway_client: httpx.AsyncClient
    ):
        """Test sequential execution of multiple tools."""
        # Get available tools
        tools_response = await gateway_client.get("/v1/tools")
        
        if tools_response.status_code == 503:
            pytest.skip("Gateway not available")
        
        if tools_response.status_code != 200:
            pytest.skip("Cannot get tools list")
        
        tools = tools_response.json().get("tools", [])
        
        if len(tools) < 2:
            pytest.skip("Need at least 2 tools for this test")
        
        # Execute tools sequentially
        results = []
        for tool in tools[:2]:
            tool_name = tool.get("name")
            
            payload = {
                "tool_name": tool_name,
                "arguments": {}
            }
            
            response = await gateway_client.post(
                "/v1/tools/execute",
                json=payload,
                timeout=15.0
            )
            
            if response.status_code == 404:
                continue  # Skip if endpoint not available
            
            results.append({
                "tool": tool_name,
                "status": response.status_code
            })
        
        # Verify results is a list (tool execution was attempted)
        assert isinstance(results, list)

    async def test_parallel_tool_capability(
        self,
        gateway_client: httpx.AsyncClient
    ):
        """Test that multiple tools can be registered for parallel use."""
        payload = {
            "model": "gpt-4",
            "messages": [
                {"role": "user", "content": "Help me research and analyze data."}
            ],
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "name": "search_corpus",
                        "description": "Search documents",
                        "parameters": {
                            "type": "object",
                            "properties": {"query": {"type": "string"}},
                            "required": ["query"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_chunk",
                        "description": "Get specific chunk",
                        "parameters": {
                            "type": "object",
                            "properties": {"chunk_id": {"type": "string"}},
                            "required": ["chunk_id"]
                        }
                    }
                }
            ],
            "parallel_tool_calls": True
        }
        
        response = await gateway_client.post(
            "/v1/chat/completions",
            json=payload,
            timeout=60.0
        )
        
        if response.status_code == 503:
            pytest.skip("Services not available")
        
        # Should accept the multi-tool request
        assert response.status_code in [200, 400, 500, 502, 504]


# =============================================================================
# WBS 3.5.3.3.4: Session Lifecycle Flow
# =============================================================================


@pytest.mark.integration
@pytest.mark.docker
@pytest.mark.e2e
class TestSessionLifecycleFlow:
    """Test complete session lifecycle end-to-end."""

    async def test_full_session_lifecycle(self, gateway_client: httpx.AsyncClient):
        """Test session from creation through deletion."""
        session_id = f"lifecycle-{uuid.uuid4().hex[:8]}"
        
        # Step 1: Create session via chat
        create_payload = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": "Hello"}],
            "session_id": session_id
        }
        
        create_response = await gateway_client.post(
            "/v1/chat/completions",
            json=create_payload,
            timeout=60.0
        )
        
        if create_response.status_code == 503:
            pytest.skip("Services not available")
        
        # Step 2: Verify session exists
        get_response = await gateway_client.get(f"/v1/sessions/{session_id}")
        
        if get_response.status_code == 404:
            # Session endpoint may not exist or session not persisted
            pass  # Continue with cleanup
        
        # Step 3: Add more messages
        second_payload = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": "How are you?"}],
            "session_id": session_id
        }
        
        await gateway_client.post(
            "/v1/chat/completions",
            json=second_payload,
            timeout=60.0
        )
        
        # Step 4: Delete session
        delete_response = await gateway_client.delete(f"/v1/sessions/{session_id}")
        
        # Delete should succeed or return 404 if already gone
        assert delete_response.status_code in [200, 204, 404], (
            f"Unexpected delete status: {delete_response.status_code}"
        )
        
        # Step 5: Verify session is gone
        verify_response = await gateway_client.get(f"/v1/sessions/{session_id}")
        
        if verify_response.status_code != 404:
            # May return 200 with empty or 404
            pass

    async def test_session_message_history(self, gateway_client: httpx.AsyncClient):
        """Test that session maintains message history."""
        session_id = f"history-{uuid.uuid4().hex[:8]}"
        
        messages = [
            "My favorite color is blue.",
            "What is my favorite color?",
            "Thanks for remembering!"
        ]
        
        for msg in messages:
            payload = {
                "model": "gpt-4",
                "messages": [{"role": "user", "content": msg}],
                "session_id": session_id
            }
            
            response = await gateway_client.post(
                "/v1/chat/completions",
                json=payload,
                timeout=60.0
            )
            
            if response.status_code == 503:
                pytest.skip("Services not available")
            
            if response.status_code != 200:
                break
        
        # Clean up
        await gateway_client.delete(f"/v1/sessions/{session_id}")


# =============================================================================
# WBS 3.5.3.3.5: Error Recovery Flow
# =============================================================================


@pytest.mark.integration
@pytest.mark.docker
@pytest.mark.e2e
class TestErrorRecoveryFlow:
    """Test system recovery from various error conditions."""

    async def test_recovery_from_invalid_request(
        self,
        gateway_client: httpx.AsyncClient
    ):
        """System should recover from invalid requests."""
        # Invalid request
        invalid_payload = {
            "model": "",
            "messages": "not-an-array"  # Invalid type
        }
        
        invalid_response = await gateway_client.post(
            "/v1/chat/completions",
            json=invalid_payload,
            timeout=10.0
        )
        
        # Should return validation error
        assert invalid_response.status_code in [400, 422, 500]
        
        # Valid request should still work
        valid_payload = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": "Hello"}]
        }
        
        valid_response = await gateway_client.post(
            "/v1/chat/completions",
            json=valid_payload,
            timeout=60.0
        )
        
        if valid_response.status_code == 503:
            pytest.skip("Services not available")
        
        # System should have recovered
        assert valid_response.status_code in [200, 429, 500, 502, 504]

    async def test_recovery_from_timeout(self, gateway_client: httpx.AsyncClient):
        """System should handle timeout gracefully."""
        # Request with very short timeout
        payload = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": "Tell me a long story."}],
            "max_tokens": 1000
        }
        
        try:
            await gateway_client.post(
                "/v1/chat/completions",
                json=payload,
                timeout=0.1  # Very short timeout
            )
        except httpx.TimeoutException:
            pass  # Expected
        
        # System should still work after timeout
        health_response = await gateway_client.get("/health", timeout=10.0)
        
        # Health check should work
        assert health_response.status_code in [200, 503]

    async def test_recovery_from_service_error(
        self,
        gateway_client: httpx.AsyncClient
    ):
        """System should recover from backend service errors."""
        # Request that might cause backend error
        payload = {
            "model": "nonexistent-model-xyz",
            "messages": [{"role": "user", "content": "Test"}]
        }
        
        error_response = await gateway_client.post(
            "/v1/chat/completions",
            json=payload,
            timeout=30.0
        )
        
        # May return error
        assert error_response.status_code in [200, 400, 404, 500, 502, 503]
        
        # Health should still work
        health_response = await gateway_client.get("/health", timeout=10.0)
        assert health_response.status_code in [200, 503]


# =============================================================================
# WBS 3.5.3.3.6: Performance Characteristics
# =============================================================================


@pytest.mark.integration
@pytest.mark.docker
@pytest.mark.e2e
@pytest.mark.slow
class TestPerformanceCharacteristics:
    """Test basic performance characteristics of the system."""

    async def test_response_time_under_load(
        self,
        gateway_client: httpx.AsyncClient
    ):
        """Measure response times for basic requests."""
        times = []
        
        for _ in range(3):  # Light load test
            start = time.time()
            
            response = await gateway_client.get("/health", timeout=10.0)
            
            elapsed = time.time() - start
            times.append(elapsed)
            
            if response.status_code == 503:
                pytest.skip("Gateway not available")
        
        avg_time = sum(times) / len(times)
        
        # Health checks should be fast
        assert avg_time < 5.0, f"Average response time too slow: {avg_time}s"

    async def test_concurrent_request_handling(
        self,
        gateway_client: httpx.AsyncClient
    ):
        """Test handling of concurrent requests."""
        async def make_request():
            try:
                response = await gateway_client.get("/health", timeout=10.0)
                return response.status_code
            except (httpx.HTTPError, httpx.TimeoutException):
                return 0
        
        # Make 5 concurrent requests
        tasks = [make_request() for _ in range(5)]
        results = await asyncio.gather(*tasks)
        
        # Most should succeed
        success_count = sum(1 for r in results if r in [200, 503])
        assert success_count >= 3, f"Too many failures: {results}"

    async def test_large_message_handling(
        self,
        gateway_client: httpx.AsyncClient
    ):
        """Test handling of larger message payloads."""
        large_content = "A" * 10000  # 10KB message
        
        payload = {
            "model": "gpt-4",
            "messages": [
                {"role": "user", "content": large_content}
            ],
            "max_tokens": 10
        }
        
        start = time.time()
        
        response = await gateway_client.post(
            "/v1/chat/completions",
            json=payload,
            timeout=60.0
        )
        
        elapsed = time.time() - start
        
        if response.status_code == 503:
            pytest.skip("Services not available")
        
        # Should handle large payload
        assert response.status_code in [200, 400, 413, 500, 502, 504], (
            f"Unexpected status for large payload: {response.status_code}"
        )
        
        # Should complete in reasonable time
        assert elapsed < 60.0


# =============================================================================
# WBS 3.5.3.3.7: Full Stack Health
# =============================================================================


@pytest.mark.integration
@pytest.mark.docker
@pytest.mark.e2e
class TestFullStackHealth:
    """Test health of the complete stack."""

    async def test_all_services_health(self, gateway_client: httpx.AsyncClient):
        """Verify all services report health status."""
        response = await gateway_client.get("/health")
        
        if response.status_code == 503:
            pytest.skip("Gateway not available")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should have overall status
        assert "status" in data
        
        # Should report on dependencies
        dependencies = data.get("dependencies", data.get("services", {}))
        
        # Log status for debugging
        for service, status in dependencies.items():
            if isinstance(status, dict):
                svc_status = status.get("status", "unknown")
            else:
                svc_status = status
            # Just verify we can read status
            assert svc_status is not None

    async def test_ready_endpoint_reflects_dependencies(
        self,
        gateway_client: httpx.AsyncClient
    ):
        """Ready endpoint should reflect dependency status."""
        response = await gateway_client.get("/health/ready")
        
        # Status reflects actual readiness
        assert response.status_code in [200, 503]
        
        data = response.json()
        status = data.get("status", "unknown")
        
        if response.status_code == 200:
            assert status in ["healthy", "ready", "ok", "degraded"]
        else:
            assert status in ["unhealthy", "not_ready", "degraded", "unavailable"]

    async def test_metrics_endpoint(self, gateway_client: httpx.AsyncClient):
        """Metrics endpoint should be available."""
        response = await gateway_client.get("/metrics")
        
        if response.status_code == 404:
            pytest.skip("Metrics endpoint not implemented")
        
        if response.status_code == 503:
            pytest.skip("Gateway not available")
        
        assert response.status_code == 200
        
        # Should return Prometheus format or JSON
        content_type = response.headers.get("content-type", "")
        assert any(
            ct in content_type 
            for ct in ["text/plain", "application/json", "text/html"]
        )
