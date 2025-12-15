"""
Gateway Search Client - WBS GATEWAY_ROUTING_REFACTOR Phase 3.2

Async HTTP client that routes search operations through the LLM Gateway
using the `search_corpus` tool instead of calling semantic-search directly.

Reference Documents:
- ARCHITECTURE.md: Kitchen Brigade "Router" pattern - Gateway is single entry point
- llm-gateway/config/tools.json: search_corpus, get_chunk tool definitions
- CODING_PATTERNS_ANALYSIS.md: Anti-Pattern #12 (connection pooling)

Pattern: Adapter Pattern
- Adapts Gateway tool execution to SearchClient interface
- Routes ALL search traffic through Gateway:8080
- NO direct calls to semantic-search:8081

Usage:
    async with GatewaySearchClient() as client:
        # Search via Gateway tool
        results = await client.search("domain driven design", limit=5)
        
        # Hybrid search via Gateway
        results = await client.hybrid_search(
            query="microservices",
            focus_areas=["architecture"],
            limit=10
        )
"""

import asyncio
import os
from typing import Any, Optional

import httpx


# =============================================================================
# Constants
# =============================================================================

_CLIENT_NOT_INITIALIZED_ERROR = "Client not initialized. Use async context manager."
_DEFAULT_GATEWAY_URL = "http://localhost:8080"


# =============================================================================
# Custom Exceptions
# =============================================================================


class GatewaySearchError(Exception):
    """Base exception for Gateway Search errors."""
    pass


class GatewaySearchTimeoutError(GatewaySearchError):
    """Raised when gateway request times out."""
    pass


class GatewaySearchConnectionError(GatewaySearchError):
    """Raised when unable to connect to gateway."""
    pass


class GatewaySearchAPIError(GatewaySearchError):
    """Raised when gateway returns an error response."""

    def __init__(self, message: str, status_code: int, response_body: Optional[dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


# =============================================================================
# GatewaySearchClient
# =============================================================================


class GatewaySearchClient:
    """
    Async HTTP client that routes search through LLM Gateway.

    Implements the same interface as SemanticSearchClient but routes
    all requests through the Gateway using tool execution.

    Reference:
    - ARCHITECTURE.md: Kitchen Brigade "Router" pattern
    - llm-gateway/config/tools.json: search_corpus tool

    Attributes:
        gateway_url: Gateway base URL (default: http://localhost:8080)
        timeout: Request timeout in seconds (default: 30.0)

    Example:
        async with GatewaySearchClient() as client:
            results = await client.search("domain driven design", limit=5)
    """

    # Retryable status codes
    RETRYABLE_STATUS_CODES: frozenset[int] = frozenset({429, 502, 503, 504})

    def __init__(
        self,
        gateway_url: Optional[str] = None,
        timeout: Optional[float] = None,
        max_connections: int = 10,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ) -> None:
        """
        Initialize Gateway Search client.

        Args:
            gateway_url: Gateway base URL. Defaults to LLM_GATEWAY_URL env or localhost:8080
            timeout: Request timeout in seconds. Defaults to 30.0
            max_connections: Max connections in pool. Default 10.
            max_retries: Maximum retry attempts for transient failures. Default 3.
            retry_delay: Base delay between retries in seconds. Default 1.0.

        Pattern: Environment variable configuration with sensible defaults
        """
        self._gateway_url: str = gateway_url or os.getenv("LLM_GATEWAY_URL", _DEFAULT_GATEWAY_URL) or _DEFAULT_GATEWAY_URL
        self._timeout: float = timeout or float(os.getenv("LLM_GATEWAY_TIMEOUT", "30.0") or "30.0")
        self._max_connections: int = max_connections
        self._max_retries: int = max_retries
        self._retry_delay: float = retry_delay

        # Lazy initialization - client created in __aenter__
        # Pattern: Avoid creating httpx.AsyncClient per request (CODING_PATTERNS #12)
        self._client: Optional[httpx.AsyncClient] = None

    @property
    def gateway_url(self) -> str:
        """The gateway URL being used."""
        return self._gateway_url

    async def __aenter__(self) -> "GatewaySearchClient":
        """
        Async context manager entry - create pooled HTTP client.

        Pattern: Connection pooling via context manager (GUIDELINES p. 2313)
        """
        limits = httpx.Limits(
            max_connections=self._max_connections,
            max_keepalive_connections=self._max_connections,
        )
        self._client = httpx.AsyncClient(
            base_url=self._gateway_url,
            timeout=httpx.Timeout(self._timeout),
            limits=limits,
        )
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """
        Async context manager exit - close HTTP client.
        """
        if self._client:
            await self._client.aclose()
            self._client = None

    def _ensure_client(self) -> httpx.AsyncClient:
        """Ensure client is initialized."""
        if self._client is None:
            raise GatewaySearchError(_CLIENT_NOT_INITIALIZED_ERROR)
        return self._client

    async def _execute_tool(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Execute a Gateway tool.

        Args:
            tool_name: Tool name (e.g., "search_corpus")
            arguments: Tool arguments

        Returns:
            Tool execution result

        Raises:
            GatewaySearchError: If tool execution fails
        """
        client = self._ensure_client()

        payload = {
            "name": tool_name,
            "arguments": arguments,
        }

        for attempt in range(self._max_retries):
            try:
                response = await client.post("/v1/tools/execute", json=payload)

                if response.status_code in self.RETRYABLE_STATUS_CODES:
                    if attempt < self._max_retries - 1:
                        await asyncio.sleep(self._retry_delay * (2 ** attempt))
                        continue
                    raise GatewaySearchAPIError(
                        f"Gateway returned {response.status_code}",
                        response.status_code,
                    )

                response.raise_for_status()
                return response.json()

            except httpx.TimeoutException as e:
                if attempt < self._max_retries - 1:
                    await asyncio.sleep(self._retry_delay * (2 ** attempt))
                    continue
                raise GatewaySearchTimeoutError(f"Gateway request timed out: {e}") from e
            except httpx.ConnectError as e:
                raise GatewaySearchConnectionError(f"Failed to connect to gateway: {e}") from e
            except httpx.HTTPStatusError as e:
                raise GatewaySearchAPIError(
                    f"Gateway error: {e}",
                    e.response.status_code,
                    e.response.json() if e.response.content else None,
                ) from e

        raise GatewaySearchError("Max retries exceeded")

    async def search(
        self,
        query: str,
        limit: int = 10,
        collection: str = "chapters",
    ) -> list[dict[str, Any]]:
        """
        Search using Gateway search_corpus tool.

        Args:
            query: Search query
            limit: Maximum results (default: 10)
            collection: Collection to search (default: "chapters")

        Returns:
            List of search results with chunk_id, content, score

        Example:
            results = await client.search("domain driven design", limit=5)
        """
        result = await self._execute_tool(
            "search_corpus",
            {
                "query": query,
                "top_k": limit,
                "collection": collection,
            },
        )

        # Extract results from tool response
        # Gateway returns: {"name": "...", "result": {"results": [...]}, "success": true}
        if isinstance(result, dict):
            inner_result = result.get("result", result)
            if isinstance(inner_result, dict):
                return inner_result.get("results", [])
            return result.get("results", [])
        return []

    async def hybrid_search(
        self,
        query: str,
        focus_areas: Optional[list[str]] = None,
        limit: int = 10,
        collection: str = "chapters",
    ) -> list[dict[str, Any]]:
        """
        Hybrid search using Gateway search_corpus tool.

        Note: Focus areas are included in the query for semantic matching.

        Args:
            query: Search query
            focus_areas: Focus areas to include in search
            limit: Maximum results (default: 10)
            collection: Collection to search

        Returns:
            List of search results
        """
        # Enhance query with focus areas for semantic search
        enhanced_query = query
        if focus_areas:
            enhanced_query = f"{query} {' '.join(focus_areas)}"

        return await self.search(enhanced_query, limit=limit, collection=collection)

    async def embed(self, text: str) -> list[float]:
        """
        Generate embeddings via Gateway.

        Note: This routes through Gateway's embedding endpoint.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        client = self._ensure_client()

        payload = {
            "input": text,
            "model": "text-embedding-3-small",
        }

        try:
            response = await client.post("/v1/embeddings", json=payload)
            response.raise_for_status()
            result = response.json()

            # Extract embedding from OpenAI-compatible response
            data = result.get("data", [])
            if data:
                return data[0].get("embedding", [])
            return []

        except httpx.TimeoutException as e:
            raise GatewaySearchTimeoutError(f"Embedding request timed out: {e}") from e
        except httpx.ConnectError as e:
            raise GatewaySearchConnectionError(f"Failed to connect to gateway: {e}") from e
        except httpx.HTTPStatusError as e:
            raise GatewaySearchAPIError(
                f"Embedding error: {e}",
                e.response.status_code,
            ) from e

    async def get_chunk(self, chunk_id: str) -> Optional[dict[str, Any]]:
        """
        Get a specific chunk by ID via Gateway get_chunk tool.

        Args:
            chunk_id: Chunk identifier

        Returns:
            Chunk data or None if not found
        """
        try:
            result = await self._execute_tool(
                "get_chunk",
                {"chunk_id": chunk_id},
            )
            return result
        except GatewaySearchAPIError as e:
            if e.status_code == 404:
                return None
            raise
