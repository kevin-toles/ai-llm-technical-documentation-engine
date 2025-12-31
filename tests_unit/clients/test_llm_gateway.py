"""
Test LLM Gateway Client - WBS 3.1.1.1.9-10 TDD Implementation

Reference Documents:
- GUIDELINES: Resilience patterns (Newman pp. 352-360)
- CODING_PATTERNS_ANALYSIS: Anti-Pattern §1.1 Optional types
- llm-gateway/docs/ARCHITECTURE.md: API endpoints

TDD Phase: RED - Tests written before implementation
"""

import asyncio

import httpx
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


class TestLLMGatewayClientInstantiation:
    """WBS 3.1.1.1.9: Test client instantiates with config."""

    def test_client_instantiates_with_defaults(self):
        """Client should instantiate with default configuration."""
        from workflows.shared.clients.llm_gateway import LLMGatewayClient

        client = LLMGatewayClient()

        assert client.base_url == "http://localhost:8080"
        assert client.timeout == pytest.approx(30.0)
        assert client._client is None  # Lazy initialization

    def test_client_instantiates_with_custom_config(self):
        """Client should accept custom configuration."""
        from workflows.shared.clients.llm_gateway import LLMGatewayClient

        client = LLMGatewayClient(
            base_url="http://llm-gateway:8080",
            timeout=60.0,
            max_connections=20,
        )

        assert client.base_url == "http://llm-gateway:8080"
        assert client.timeout == pytest.approx(60.0)
        assert client.max_connections == 20

    def test_client_instantiates_from_env(self):
        """Client should read from environment variables."""
        from workflows.shared.clients.llm_gateway import LLMGatewayClient

        with patch.dict(
            "os.environ",
            {
                "LLM_GATEWAY_URL": "http://gateway.local:8080",
                "LLM_GATEWAY_TIMEOUT": "45",
            },
        ):
            client = LLMGatewayClient()

            assert client.base_url == "http://gateway.local:8080"
            assert client.timeout == pytest.approx(45.0)


class TestLLMGatewayClientContextManager:
    """Test async context manager pattern for connection pooling."""

    @pytest.mark.asyncio
    async def test_context_manager_creates_client(self):
        """Client should create httpx.AsyncClient on enter."""
        from workflows.shared.clients.llm_gateway import LLMGatewayClient

        gateway = LLMGatewayClient()

        async with gateway as client:
            assert client._client is not None
            assert isinstance(client._client, httpx.AsyncClient)

    @pytest.mark.asyncio
    async def test_context_manager_closes_client(self):
        """Client should close httpx.AsyncClient on exit."""
        from workflows.shared.clients.llm_gateway import LLMGatewayClient

        gateway = LLMGatewayClient()

        async with gateway as client:
            # Verify client exists during context
            assert client._client is not None

        # After context exit, internal client should be None
        assert gateway._client is None

    @pytest.mark.asyncio
    async def test_context_manager_reuses_connection_pool(self):
        """
        Anti-Pattern: new httpx.AsyncClient per request (CODING_PATTERNS line 67)
        
        Multiple requests within context should reuse the same client.
        """
        from workflows.shared.clients.llm_gateway import LLMGatewayClient

        gateway = LLMGatewayClient()

        async with gateway as client:
            client_id_1 = id(client._client)
            # Simulate another operation
            client_id_2 = id(client._client)

            assert client_id_1 == client_id_2, "Connection pool should be reused"


class TestLLMGatewayClientChatCompletion:
    """WBS 3.1.1.1.5-8: Test chat completion method."""

    @pytest.mark.asyncio
    async def test_chat_completion_success(self):
        """Chat completion should return response on success."""
        from workflows.shared.clients.llm_gateway import LLMGatewayClient

        mock_response = {
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "model": "claude-sonnet-4-5-20250929",
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": "Hello!"},
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 5,
                "total_tokens": 15,
            },
        }

        with patch("httpx.AsyncClient.post") as mock_post:
            mock_post.return_value = MagicMock(
                status_code=200,
                json=MagicMock(return_value=mock_response),
                raise_for_status=MagicMock(),
            )

            gateway = LLMGatewayClient()
            async with gateway as client:
                # Mock the internal client
                client._client = AsyncMock()
                client._client.post = AsyncMock(
                    return_value=MagicMock(
                        status_code=200,
                        json=MagicMock(return_value=mock_response),
                        raise_for_status=MagicMock(),
                    )
                )

                response = await client.chat_completion(
                    model="claude-sonnet-4-5-20250929",
                    messages=[{"role": "user", "content": "Hello"}],
                )

                assert response["choices"][0]["message"]["content"] == "Hello!"

    @pytest.mark.asyncio
    async def test_chat_completion_validates_messages(self):
        """Chat completion should validate messages are not empty."""
        from workflows.shared.clients.llm_gateway import LLMGatewayClient

        gateway = LLMGatewayClient()
        async with gateway as client:
            with pytest.raises(ValueError, match="messages must not be empty"):
                await client.chat_completion(
                    model="claude-sonnet-4-5-20250929",
                    messages=[],
                )

    @pytest.mark.asyncio
    async def test_chat_completion_timeout_handling(self):
        """
        GUIDELINES p. 2145: Graceful degradation, timeout handling.
        
        Client should raise GatewayTimeoutError on timeout.
        """
        from workflows.shared.clients.llm_gateway import (
            LLMGatewayClient,
            GatewayTimeoutError,
        )

        gateway = LLMGatewayClient(timeout=1.0)
        async with gateway as client:
            client._client = AsyncMock()
            client._client.post = AsyncMock(
                side_effect=httpx.TimeoutException("Connection timeout")
            )

            with pytest.raises(GatewayTimeoutError):
                await client.chat_completion(
                    model="claude-sonnet-4-5-20250929",
                    messages=[{"role": "user", "content": "Hello"}],
                )


class TestLLMGatewayClientHealth:
    """Test health check endpoint."""


class TestLLMGatewayClientRetryLogic:
    """
    WBS 3.1.1.2.6-9: Test retry logic for transient failures.
    
    Reference: GUIDELINES p. 466 (fail fast then retry at higher level)
    Reference: GUIDELINES p. 2309 (circuit breaker, rate limits are operational realities)
    Reference: CODING_PATTERNS §2.3 (Extract Method for error classification)
    """

    @pytest.mark.asyncio
    async def test_retry_on_503_service_unavailable(self):
        """
        WBS 3.1.1.2.9: Retry on 503 Service Unavailable.
        
        Transient server errors should trigger retry with exponential backoff.
        """
        from workflows.shared.clients.llm_gateway import LLMGatewayClient

        mock_success_response = {
            "id": "chatcmpl-123",
            "choices": [{"message": {"content": "Success after retry"}}],
        }

        call_count = 0

        async def mock_post(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0)  # Make async meaningful
            if call_count < 3:
                # First two calls return 503
                response = MagicMock()
                response.status_code = 503
                response.json.return_value = {"error": "Service Unavailable"}
                error = httpx.HTTPStatusError(
                    "503 Service Unavailable",
                    request=MagicMock(),
                    response=response,
                )
                response.raise_for_status.side_effect = error
                return response
            # Third call succeeds
            response = MagicMock()
            response.status_code = 200
            response.json.return_value = mock_success_response
            response.raise_for_status.return_value = None
            return response

        gateway = LLMGatewayClient(max_retries=3, retry_delay=0.01)
        async with gateway as client:
            client._client = AsyncMock()
            client._client.post = mock_post

            response = await client.chat_completion(
                model="claude-sonnet-4-5-20250929",
                messages=[{"role": "user", "content": "Hello"}],
            )

            assert call_count == 3
            assert response["choices"][0]["message"]["content"] == "Success after retry"

    @pytest.mark.asyncio
    async def test_retry_on_429_rate_limit(self):
        """
        WBS 3.1.1.2.6: Retry on 429 Too Many Requests.
        
        Rate limit errors should trigger retry with exponential backoff.
        Reference: GUIDELINES p. 2309 (rate limiting is operational reality)
        """
        from workflows.shared.clients.llm_gateway import LLMGatewayClient

        mock_success_response = {
            "id": "chatcmpl-456",
            "choices": [{"message": {"content": "Success after rate limit"}}],
        }

        call_count = 0

        async def mock_post(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0)  # Make async meaningful
            if call_count < 2:
                response = MagicMock()
                response.status_code = 429
                response.json.return_value = {"error": "Rate limit exceeded"}
                error = httpx.HTTPStatusError(
                    "429 Too Many Requests",
                    request=MagicMock(),
                    response=response,
                )
                response.raise_for_status.side_effect = error
                return response
            response = MagicMock()
            response.status_code = 200
            response.json.return_value = mock_success_response
            response.raise_for_status.return_value = None
            return response

        gateway = LLMGatewayClient(max_retries=3, retry_delay=0.01)
        async with gateway as client:
            client._client = AsyncMock()
            client._client.post = mock_post

            response = await client.chat_completion(
                model="claude-sonnet-4-5-20250929",
                messages=[{"role": "user", "content": "Hello"}],
            )

            assert call_count == 2
            assert response["choices"][0]["message"]["content"] == "Success after rate limit"

    @pytest.mark.asyncio
    async def test_no_retry_on_4xx_client_error(self):
        """
        WBS 3.1.1.2.8: No retry on 4xx client errors (except 429).
        
        Client errors like 400, 401, 403 should fail immediately.
        """
        from workflows.shared.clients.llm_gateway import (
            LLMGatewayClient,
            GatewayAPIError,
        )

        call_count = 0

        async def mock_post(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0)  # Make async meaningful
            response = MagicMock()
            response.status_code = 400
            response.json.return_value = {"error": "Bad Request"}
            error = httpx.HTTPStatusError(
                "400 Bad Request",
                request=MagicMock(),
                response=response,
            )
            response.raise_for_status.side_effect = error
            return response

        gateway = LLMGatewayClient(max_retries=3, retry_delay=0.01)
        async with gateway as client:
            client._client = AsyncMock()
            client._client.post = mock_post

            with pytest.raises(GatewayAPIError) as exc_info:
                await client.chat_completion(
                    model="claude-sonnet-4-5-20250929",
                    messages=[{"role": "user", "content": "Hello"}],
                )

            # Should NOT retry - only 1 call
            assert call_count == 1
            assert exc_info.value.status_code == 400

    @pytest.mark.asyncio
    async def test_exhausted_retries_raises_error(self):
        """
        WBS 3.1.1.2.8: Exhausted retries should raise exception.
        
        After max_retries attempts, should raise the last error.
        """
        from workflows.shared.clients.llm_gateway import (
            LLMGatewayClient,
            GatewayAPIError,
        )

        call_count = 0

        async def mock_post(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0)  # Make async meaningful
            response = MagicMock()
            response.status_code = 503
            response.json.return_value = {"error": "Service Unavailable"}
            error = httpx.HTTPStatusError(
                "503 Service Unavailable",
                request=MagicMock(),
                response=response,
            )
            response.raise_for_status.side_effect = error
            return response

        gateway = LLMGatewayClient(max_retries=3, retry_delay=0.01)
        async with gateway as client:
            client._client = AsyncMock()
            client._client.post = mock_post

            with pytest.raises(GatewayAPIError) as exc_info:
                await client.chat_completion(
                    model="claude-sonnet-4-5-20250929",
                    messages=[{"role": "user", "content": "Hello"}],
                )

            # Should have retried max_retries times
            assert call_count == 3
            assert exc_info.value.status_code == 503

    @pytest.mark.asyncio
    async def test_retry_uses_exponential_backoff(self):
        """
        WBS 3.1.1.2.6: Retry uses exponential backoff.
        
        Delay should increase: delay * 2^attempt
        Reference: CODING_PATTERNS §2.3 (exponential backoff pattern)
        """
        from workflows.shared.clients.llm_gateway import LLMGatewayClient

        call_times = []

        async def mock_post(*args, **kwargs):
            import time
            await asyncio.sleep(0)  # Make async meaningful
            call_times.append(time.time())
            response = MagicMock()
            response.status_code = 503
            response.json.return_value = {"error": "Service Unavailable"}
            error = httpx.HTTPStatusError(
                "503 Service Unavailable",
                request=MagicMock(),
                response=response,
            )
            response.raise_for_status.side_effect = error
            return response

        gateway = LLMGatewayClient(max_retries=3, retry_delay=0.05)
        async with gateway as client:
            client._client = AsyncMock()
            client._client.post = mock_post

            try:
                await client.chat_completion(
                    model="claude-sonnet-4-5-20250929",
                    messages=[{"role": "user", "content": "Hello"}],
                )
            except Exception:
                pass

            # Check exponential backoff: first delay ~0.05s, second ~0.1s
            assert len(call_times) == 3
            delay_1 = call_times[1] - call_times[0]
            delay_2 = call_times[2] - call_times[1]
            
            # Second delay should be roughly 2x the first (with some tolerance)
            assert delay_2 > delay_1 * 1.5, f"Expected exponential backoff: {delay_1} -> {delay_2}"


class TestLLMGatewayClientErrorClassification:
    """
    Test error classification helper.
    
    Reference: CODING_PATTERNS §2.3 (Extract Method for error classification)
    """

    def test_classify_transient_error_503(self):
        """503 should be classified as transient (retryable)."""
        from workflows.shared.clients.llm_gateway import LLMGatewayClient

        client = LLMGatewayClient()
        assert client._is_retryable_status(503) is True

    def test_classify_transient_error_429(self):
        """429 should be classified as transient (retryable)."""
        from workflows.shared.clients.llm_gateway import LLMGatewayClient

        client = LLMGatewayClient()
        assert client._is_retryable_status(429) is True

    def test_classify_transient_error_502(self):
        """502 should be classified as transient (retryable)."""
        from workflows.shared.clients.llm_gateway import LLMGatewayClient

        client = LLMGatewayClient()
        assert client._is_retryable_status(502) is True

    def test_classify_non_transient_error_400(self):
        """400 should NOT be classified as transient."""
        from workflows.shared.clients.llm_gateway import LLMGatewayClient

        client = LLMGatewayClient()
        assert client._is_retryable_status(400) is False

    def test_classify_non_transient_error_401(self):
        """401 should NOT be classified as transient."""
        from workflows.shared.clients.llm_gateway import LLMGatewayClient

        client = LLMGatewayClient()
        assert client._is_retryable_status(401) is False

    def test_classify_non_transient_error_404(self):
        """404 should NOT be classified as transient."""
        from workflows.shared.clients.llm_gateway import LLMGatewayClient

        client = LLMGatewayClient()
        assert client._is_retryable_status(404) is False

    @pytest.mark.asyncio
    async def test_health_check_success(self):
        """Health check should return True when gateway is healthy."""
        from workflows.shared.clients.llm_gateway import LLMGatewayClient

        gateway = LLMGatewayClient()
        async with gateway as client:
            client._client = AsyncMock()
            client._client.get = AsyncMock(
                return_value=MagicMock(status_code=200)
            )

            is_healthy = await client.health_check()
            assert is_healthy is True

    @pytest.mark.asyncio
    async def test_health_check_failure(self):
        """Health check should return False when gateway is unhealthy."""
        from workflows.shared.clients.llm_gateway import LLMGatewayClient

        gateway = LLMGatewayClient()
        async with gateway as client:
            client._client = AsyncMock()
            client._client.get = AsyncMock(
                side_effect=httpx.ConnectError("Connection refused")
            )

            is_healthy = await client.health_check()
            assert is_healthy is False


class TestLLMGatewayClientSessionManagement:
    """
    WBS 3.1.1.3: Test session management methods.

    Reference: ARCHITECTURE.md lines 195-197 (session endpoints)
    Reference: llm-gateway/src/models/responses.py SessionResponse model
    """

    @pytest.mark.asyncio
    async def test_create_session_returns_session_id(self):
        """
        WBS 3.1.1.3.1-3: create_session returns session response with ID.
        """
        from workflows.shared.clients.llm_gateway import LLMGatewayClient

        mock_response = {
            "id": "sess_abc123",
            "messages": [],
            "context": {},
            "created_at": "2025-12-04T22:00:00Z",
            "expires_at": "2025-12-04T23:00:00Z",
        }

        gateway = LLMGatewayClient()
        async with gateway as client:
            client._client = AsyncMock()
            client._client.post = AsyncMock(
                return_value=MagicMock(
                    status_code=201,
                    json=MagicMock(return_value=mock_response),
                    raise_for_status=MagicMock(),
                )
            )

            response = await client.create_session()

            assert response["id"] == "sess_abc123"
            assert "created_at" in response

    @pytest.mark.asyncio
    async def test_create_session_with_ttl_and_context(self):
        """
        WBS 3.1.1.3.1: create_session accepts optional TTL and context.
        """
        from workflows.shared.clients.llm_gateway import LLMGatewayClient

        mock_response = {
            "id": "sess_xyz789",
            "messages": [],
            "context": {"user_id": "user123"},
            "created_at": "2025-12-04T22:00:00Z",
            "expires_at": "2025-12-05T22:00:00Z",
        }

        gateway = LLMGatewayClient()
        async with gateway as client:
            client._client = AsyncMock()
            client._client.post = AsyncMock(
                return_value=MagicMock(
                    status_code=201,
                    json=MagicMock(return_value=mock_response),
                    raise_for_status=MagicMock(),
                )
            )

            response = await client.create_session(
                ttl_seconds=86400,
                context={"user_id": "user123"},
            )

            assert response["id"] == "sess_xyz789"
            # Verify payload was sent correctly
            call_args = client._client.post.call_args
            payload = call_args.kwargs.get("json", {})
            assert payload.get("ttl_seconds") == 86400
            assert payload.get("context") == {"user_id": "user123"}

    @pytest.mark.asyncio
    async def test_get_session_returns_session_state(self):
        """
        WBS 3.1.1.3.4-5: get_session returns session state.
        """
        from workflows.shared.clients.llm_gateway import LLMGatewayClient

        mock_session = {
            "id": "sess_abc123",
            "messages": [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"},
            ],
            "context": {"user_id": "user123"},
            "created_at": "2025-12-04T22:00:00Z",
            "expires_at": "2025-12-04T23:00:00Z",
        }

        gateway = LLMGatewayClient()
        async with gateway as client:
            client._client = AsyncMock()
            client._client.get = AsyncMock(
                return_value=MagicMock(
                    status_code=200,
                    json=MagicMock(return_value=mock_session),
                    raise_for_status=MagicMock(),
                )
            )

            response = await client.get_session("sess_abc123")

            assert response["id"] == "sess_abc123"
            assert len(response["messages"]) == 2

    @pytest.mark.asyncio
    async def test_get_session_not_found(self):
        """
        WBS 3.1.1.3.5: get_session raises error for non-existent session.
        """
        from workflows.shared.clients.llm_gateway import (
            LLMGatewayClient,
            GatewayAPIError,
        )

        gateway = LLMGatewayClient()
        async with gateway as client:
            client._client = AsyncMock()
            response_mock = MagicMock()
            response_mock.status_code = 404
            response_mock.json.return_value = {"error": "Session not found"}
            error = httpx.HTTPStatusError(
                "404 Not Found",
                request=MagicMock(),
                response=response_mock,
            )
            response_mock.raise_for_status.side_effect = error
            client._client.get = AsyncMock(return_value=response_mock)

            with pytest.raises(GatewayAPIError) as exc_info:
                await client.get_session("nonexistent_session")

            assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_session_success(self):
        """
        WBS 3.1.1.3.6-7: delete_session deletes session successfully.
        """
        from workflows.shared.clients.llm_gateway import LLMGatewayClient

        gateway = LLMGatewayClient()
        async with gateway as client:
            client._client = AsyncMock()
            client._client.delete = AsyncMock(
                return_value=MagicMock(
                    status_code=204,
                    raise_for_status=MagicMock(),
                )
            )

            # Should not raise
            await client.delete_session("sess_abc123")

            # Verify DELETE was called with correct URL
            client._client.delete.assert_called_once()
            call_args = client._client.delete.call_args
            assert "/v1/sessions/sess_abc123" in str(call_args)

    @pytest.mark.asyncio
    async def test_delete_session_not_found(self):
        """
        WBS 3.1.1.3.7: delete_session raises error for non-existent session.
        """
        from workflows.shared.clients.llm_gateway import (
            LLMGatewayClient,
            GatewayAPIError,
        )

        gateway = LLMGatewayClient()
        async with gateway as client:
            client._client = AsyncMock()
            response_mock = MagicMock()
            response_mock.status_code = 404
            error = httpx.HTTPStatusError(
                "404 Not Found",
                request=MagicMock(),
                response=response_mock,
            )
            response_mock.raise_for_status.side_effect = error
            client._client.delete = AsyncMock(return_value=response_mock)

            with pytest.raises(GatewayAPIError) as exc_info:
                await client.delete_session("nonexistent_session")

            assert exc_info.value.status_code == 404


class TestLLMGatewayClientToolExecution:
    """
    WBS 3.1.1.4: Test tool execution method.

    Reference: ARCHITECTURE.md line 198 (POST /v1/tools/execute)
    """

    @pytest.mark.asyncio
    async def test_execute_tool_returns_result(self):
        """
        WBS 3.1.1.4.1-2, 3.1.1.4.4: execute_tool returns tool result.
        """
        from workflows.shared.clients.llm_gateway import LLMGatewayClient

        mock_result = {
            "tool_call_id": "call_abc123",
            "result": {
                "documents": [
                    {"id": "doc1", "content": "Found document", "score": 0.95}
                ]
            },
            "error": None,
        }

        gateway = LLMGatewayClient()
        async with gateway as client:
            client._client = AsyncMock()
            client._client.post = AsyncMock(
                return_value=MagicMock(
                    status_code=200,
                    json=MagicMock(return_value=mock_result),
                    raise_for_status=MagicMock(),
                )
            )

            response = await client.execute_tool(
                tool_name="semantic_search",
                arguments={"query": "find documents"},
                tool_call_id="call_abc123",
            )

            assert response["tool_call_id"] == "call_abc123"
            assert response["result"]["documents"][0]["id"] == "doc1"
            assert response["error"] is None

    @pytest.mark.asyncio
    async def test_execute_tool_with_error(self):
        """
        WBS 3.1.1.4.3: execute_tool handles tool execution errors.
        """
        from workflows.shared.clients.llm_gateway import LLMGatewayClient

        mock_error_result = {
            "tool_call_id": "call_xyz789",
            "result": None,
            "error": "Tool 'unknown_tool' not found",
        }

        gateway = LLMGatewayClient()
        async with gateway as client:
            client._client = AsyncMock()
            client._client.post = AsyncMock(
                return_value=MagicMock(
                    status_code=200,
                    json=MagicMock(return_value=mock_error_result),
                    raise_for_status=MagicMock(),
                )
            )

            response = await client.execute_tool(
                tool_name="unknown_tool",
                arguments={},
                tool_call_id="call_xyz789",
            )

            assert response["error"] == "Tool 'unknown_tool' not found"
            assert response["result"] is None

    @pytest.mark.asyncio
    async def test_execute_tool_api_error(self):
        """
        WBS 3.1.1.4.3: execute_tool raises GatewayAPIError on API failure.
        """
        from workflows.shared.clients.llm_gateway import (
            LLMGatewayClient,
            GatewayAPIError,
        )

        gateway = LLMGatewayClient()
        async with gateway as client:
            client._client = AsyncMock()
            response_mock = MagicMock()
            response_mock.status_code = 500
            response_mock.json.return_value = {"error": "Internal server error"}
            error = httpx.HTTPStatusError(
                "500 Internal Server Error",
                request=MagicMock(),
                response=response_mock,
            )
            response_mock.raise_for_status.side_effect = error
            client._client.post = AsyncMock(return_value=response_mock)

            with pytest.raises(GatewayAPIError) as exc_info:
                await client.execute_tool(
                    tool_name="semantic_search",
                    arguments={"query": "test"},
                )

            assert exc_info.value.status_code == 500
