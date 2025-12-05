"""
LLM Gateway Client - WBS 3.1.1.1 Client Module Setup

Async HTTP client for llm-gateway microservice with connection pooling.

Reference Documents:
- GUIDELINES p. 2313: "Different connection pools for each downstream service" (Newman)
- GUIDELINES p. 2145: Connection pooling, graceful degradation, circuit breaker patterns
- CODING_PATTERNS_ANALYSIS line 67: Anti-Pattern - new httpx.AsyncClient per request
- llm-gateway/docs/ARCHITECTURE.md: API endpoints (/v1/chat/completions, /health)
- llm-gateway/src/models/requests.py: ChatCompletionRequest model

Anti-Patterns Avoided:
- §1.1: Optional types use Optional[T] with explicit None default
- Connection Pooling: Single httpx.AsyncClient reused via context manager

Usage:
    async with LLMGatewayClient() as client:
        response = await client.chat_completion(
            model="claude-sonnet-4-5-20250929",
            messages=[{"role": "user", "content": "Hello"}]
        )
"""

import asyncio
import os
from typing import Any, Optional

import httpx


# =============================================================================
# Custom Exceptions - WBS 3.1.1.1.5
# Pattern: Domain-specific exceptions (CODING_PATTERNS §2.3)
# =============================================================================


class GatewayError(Exception):
    """Base exception for LLM Gateway errors."""

    pass


class GatewayTimeoutError(GatewayError):
    """
    Raised when gateway request times out.

    GUIDELINES p. 2145: Graceful degradation, timeout handling.
    """

    pass


class GatewayConnectionError(GatewayError):
    """Raised when unable to connect to gateway."""

    pass


class GatewayAPIError(GatewayError):
    """Raised when gateway returns an error response."""

    def __init__(self, message: str, status_code: int, response_body: Optional[dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


# =============================================================================
# LLMGatewayClient - WBS 3.1.1.1.4
# Pattern: Connection pooling via context manager (GUIDELINES p. 2313)
# =============================================================================


class LLMGatewayClient:
    """
    Async HTTP client for llm-gateway microservice.

    Implements connection pooling to avoid creating new httpx.AsyncClient per request.
    Uses async context manager pattern for proper resource cleanup.

    Reference:
    - GUIDELINES p. 2313: "using separate connection pools for different downstream services"
    - CODING_PATTERNS line 67: Anti-Pattern - new httpx.AsyncClient per request

    Attributes:
        base_url: Gateway base URL (default: http://localhost:8080)
        timeout: Request timeout in seconds (default: 30.0)
        max_connections: Maximum connections in pool (default: 10)

    Example:
        async with LLMGatewayClient() as client:
            response = await client.chat_completion(
                model="claude-sonnet-4-5-20250929",
                messages=[{"role": "user", "content": "Hello"}]
            )
    """

    # Retryable status codes - Reference: GUIDELINES p. 2309 (rate limiting operational reality)
    RETRYABLE_STATUS_CODES: frozenset[int] = frozenset({429, 502, 503, 504})

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        max_connections: int = 10,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ) -> None:
        """
        Initialize LLM Gateway client.

        Args:
            base_url: Gateway base URL. Defaults to LLM_GATEWAY_URL env or localhost:8080
            timeout: Request timeout in seconds. Defaults to LLM_GATEWAY_TIMEOUT env or 30.0
            max_connections: Max connections in pool. Default 10.
            max_retries: Maximum retry attempts for transient failures. Default 3.
            retry_delay: Base delay between retries in seconds. Default 1.0.

        Pattern: Environment variable configuration with sensible defaults
        Reference: CODING_PATTERNS §2.3 (exponential backoff pattern)
        """
        # Read from environment with fallback to defaults
        # Type annotations ensure these are never None after initialization
        self.base_url: str = base_url or os.getenv("LLM_GATEWAY_URL", "http://localhost:8080") or "http://localhost:8080"
        self.timeout: float = timeout or float(os.getenv("LLM_GATEWAY_TIMEOUT", "30.0") or "30.0")
        self.max_connections: int = max_connections
        self.max_retries: int = max_retries
        self.retry_delay: float = retry_delay

        # Lazy initialization - client created in __aenter__
        # Pattern: Avoid creating httpx.AsyncClient per request (CODING_PATTERNS line 67)
        self._client: Optional[httpx.AsyncClient] = None

    def _is_retryable_status(self, status_code: int) -> bool:
        """
        Check if HTTP status code is retryable.

        Extracted to reduce cognitive complexity (CODING_PATTERNS §2.3).

        Args:
            status_code: HTTP status code to check.

        Returns:
            True if the status code represents a transient error.

        Reference: GUIDELINES p. 2309 (rate limits, 5xx errors are operational realities)
        """
        return status_code in self.RETRYABLE_STATUS_CODES

    async def __aenter__(self) -> "LLMGatewayClient":
        """
        Enter async context and create HTTP client with connection pool.

        Pattern: Connection pooling (GUIDELINES p. 2313)
        """
        limits = httpx.Limits(max_connections=self.max_connections)
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(self.timeout),
            limits=limits,
            headers={"Content-Type": "application/json"},
        )
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any],
    ) -> None:
        """
        Exit async context and close HTTP client.

        Pattern: Proper resource cleanup via context manager
        """
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    # =========================================================================
    # Chat Completion - WBS 3.1.1.1.5-8
    # Pattern: OpenAI-compatible API (llm-gateway/docs/ARCHITECTURE.md)
    # =========================================================================

    async def chat_completion(
        self,
        model: str,
        messages: list[dict[str, Any]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        tools: Optional[list[dict[str, Any]]] = None,
        tool_choice: Optional[str | dict[str, Any]] = None,
        session_id: Optional[str] = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Send chat completion request to llm-gateway.

        Reference: llm-gateway/src/models/requests.py ChatCompletionRequest

        Args:
            model: Model identifier (e.g., "claude-sonnet-4-5-20250929")
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            stream: Enable streaming (not yet implemented)
            tools: Tool definitions for function calling
            tool_choice: Tool selection strategy
            session_id: Session ID for conversation continuity
            **kwargs: Additional parameters passed to the API

        Returns:
            dict: Chat completion response

        Raises:
            ValueError: If messages is empty
            GatewayTimeoutError: On request timeout
            GatewayConnectionError: On connection failure
            GatewayAPIError: On API error response
        """
        # Validate messages - Pattern: Input validation (llm-gateway/models/requests.py)
        if not messages:
            raise ValueError("messages must not be empty")

        # Build request payload
        payload: dict[str, Any] = {
            "model": model,
            "messages": messages,
        }

        # Add optional parameters - Pattern: Optional[T] with None (ANTI_PATTERN §1.1)
        if temperature is not None:
            payload["temperature"] = temperature
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if stream:
            payload["stream"] = stream
        if tools is not None:
            payload["tools"] = tools
        if tool_choice is not None:
            payload["tool_choice"] = tool_choice
        if session_id is not None:
            payload["session_id"] = session_id

        # Add any additional kwargs
        payload.update(kwargs)

        # Make request with error handling and retry
        # Pattern: Timeout handling for graceful degradation (GUIDELINES p. 2145)
        # Pattern: Retry with exponential backoff (CODING_PATTERNS §2.3)
        return await self._post_with_retry("/v1/chat/completions", payload)

    async def _post_with_retry(
        self, endpoint: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Make POST request with retry logic for transient failures.

        WBS 3.1.1.2.6: Retry logic for transient failures (503, 429, 502, 504).
        Pattern: Exponential backoff (CODING_PATTERNS §2.3)
        Reference: GUIDELINES p. 466 (fail fast then retry at higher level)

        Args:
            endpoint: API endpoint path
            payload: Request payload

        Returns:
            dict: JSON response

        Raises:
            GatewayTimeoutError: On timeout
            GatewayConnectionError: On connection failure
            GatewayAPIError: On API error after exhausting retries
        """
        last_error: Optional[GatewayAPIError] = None

        for attempt in range(self.max_retries):
            try:
                return await self._post(endpoint, payload)
            except GatewayAPIError as e:
                # Check if error is retryable
                if not self._is_retryable_status(e.status_code):
                    raise  # Non-retryable: fail immediately

                last_error = e

                # Wait before retry (exponential backoff)
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2**attempt)
                    await asyncio.sleep(delay)

        # Exhausted retries - raise last error
        if last_error is not None:
            raise last_error
        raise GatewayAPIError("Request failed after retries", status_code=500)

    async def _post(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        """
        Make POST request with error handling.

        Pattern: Centralized error handling (CODING_PATTERNS §2.3)

        Args:
            endpoint: API endpoint path
            payload: Request payload

        Returns:
            dict: JSON response

        Raises:
            GatewayTimeoutError: On timeout
            GatewayConnectionError: On connection failure
            GatewayAPIError: On API error
        """
        if self._client is None:
            raise RuntimeError("Client not initialized. Use async context manager.")

        try:
            response = await self._client.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()

        except httpx.TimeoutException as e:
            raise GatewayTimeoutError(f"Request to {endpoint} timed out: {e}") from e

        except httpx.ConnectError as e:
            raise GatewayConnectionError(f"Failed to connect to gateway: {e}") from e

        except httpx.HTTPStatusError as e:
            # Try to parse error response body
            try:
                body = e.response.json()
            except Exception:
                body = None

            raise GatewayAPIError(
                f"Gateway API error: {e.response.status_code}",
                status_code=e.response.status_code,
                response_body=body,
            ) from e

    # =========================================================================
    # Health Check - WBS 3.1.1.1.6
    # Pattern: Health endpoint (llm-gateway/docs/ARCHITECTURE.md)
    # =========================================================================

    async def health_check(self) -> bool:
        """
        Check if llm-gateway is healthy.

        Reference: llm-gateway/docs/ARCHITECTURE.md GET /health

        Returns:
            bool: True if gateway is healthy, False otherwise
        """
        if self._client is None:
            raise RuntimeError("Client not initialized. Use async context manager.")

        try:
            response = await self._client.get("/health")
            return response.status_code == 200

        except (httpx.ConnectError, httpx.TimeoutException):
            return False

    # =========================================================================
    # Session Management - WBS 3.1.1.1.7 (Future)
    # Reference: llm-gateway/docs/ARCHITECTURE.md Session endpoints
    # =========================================================================

    async def create_session(
        self,
        ttl_seconds: Optional[int] = None,
        context: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Create a new session for conversation continuity.

        Reference: llm-gateway/src/models/requests.py SessionCreateRequest

        Args:
            ttl_seconds: Session TTL in seconds (uses gateway default if None)
            context: Initial context data for the session

        Returns:
            dict: Session creation response with session_id
        """
        payload: dict[str, Any] = {}
        if ttl_seconds is not None:
            payload["ttl_seconds"] = ttl_seconds
        if context is not None:
            payload["context"] = context

        return await self._post("/v1/sessions", payload)

    async def get_session(self, session_id: str) -> dict[str, Any]:
        """
        Get session state.

        Reference: llm-gateway/docs/ARCHITECTURE.md GET /v1/sessions/{id}

        Args:
            session_id: Session ID to retrieve

        Returns:
            dict: Session state
        """
        if self._client is None:
            raise RuntimeError("Client not initialized. Use async context manager.")

        try:
            response = await self._client.get(f"/v1/sessions/{session_id}")
            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            raise GatewayAPIError(
                f"Failed to get session: {e.response.status_code}",
                status_code=e.response.status_code,
            ) from e

    async def delete_session(self, session_id: str) -> None:
        """
        Delete a session.

        WBS 3.1.1.3.6-7: Delete session by ID.
        Reference: llm-gateway/docs/ARCHITECTURE.md DELETE /v1/sessions/{id}

        Args:
            session_id: Session ID to delete

        Raises:
            RuntimeError: If client not initialized
            GatewayAPIError: On API error (e.g., 404 Not Found)
        """
        if self._client is None:
            raise RuntimeError("Client not initialized. Use async context manager.")

        try:
            response = await self._client.delete(f"/v1/sessions/{session_id}")
            response.raise_for_status()
            # 204 No Content on success - no body to return

        except httpx.HTTPStatusError as e:
            raise GatewayAPIError(
                f"Failed to delete session: {e.response.status_code}",
                status_code=e.response.status_code,
            ) from e

    # =========================================================================
    # Tool Execution - WBS 3.1.1.4
    # Reference: llm-gateway/docs/ARCHITECTURE.md POST /v1/tools/execute
    # =========================================================================

    async def execute_tool(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        tool_call_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Execute a registered tool on the gateway.

        WBS 3.1.1.4.1-3: Execute tool and handle errors.
        Reference: llm-gateway/docs/ARCHITECTURE.md POST /v1/tools/execute

        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments
            tool_call_id: Optional tool call ID for tracking

        Returns:
            dict: Tool execution result with keys:
                - tool_call_id: ID of the tool call
                - result: Tool execution result (or None on error)
                - error: Error message (or None on success)

        Raises:
            GatewayAPIError: On API error (5xx)
            GatewayTimeoutError: On request timeout
            GatewayConnectionError: On connection failure
        """
        payload: dict[str, Any] = {
            "tool_name": tool_name,
            "arguments": arguments,
        }
        if tool_call_id is not None:
            payload["tool_call_id"] = tool_call_id

        return await self._post_with_retry("/v1/tools/execute", payload)
