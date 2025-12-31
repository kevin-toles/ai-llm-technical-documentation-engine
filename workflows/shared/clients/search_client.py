"""
Semantic Search Client - WBS 3.2.3

Async HTTP client for semantic-search-service microservice with connection pooling.

Reference Documents:
- GUIDELINES p. 2313: "Different connection pools for each downstream service" (Newman)
- GUIDELINES p. 2145: Connection pooling, graceful degradation, circuit breaker patterns
- CODING_PATTERNS line 67: Anti-Pattern - new httpx.AsyncClient per request
- semantic-search-service/docs/ARCHITECTURE.md: API endpoints (/v1/embed, /v1/search)

Anti-Patterns Avoided:
- §1.1: Optional types use Optional[T] with explicit None default
- Connection Pooling: Single httpx.AsyncClient reused via context manager

Usage:
    async with SemanticSearchClient() as client:
        # Generate embeddings
        embeddings = await client.embed("domain driven design")
        
        # Search for similar content
        results = await client.search("repository pattern", limit=5)
        
        # Hybrid search with focus areas
        results = await client.hybrid_search(
            query="microservices",
            focus_areas=["architecture", "patterns"],
            limit=10
        )
"""

import asyncio
import os
from typing import Any, Optional

import httpx


# =============================================================================
# Constants - SonarQube S1192: Extract duplicated literals
# =============================================================================

_CLIENT_NOT_INITIALIZED_ERROR = "Client not initialized. Use async context manager."
_DEFAULT_COLLECTION = "chapters"


# =============================================================================
# Custom Exceptions - WBS 3.2.3
# Pattern: Domain-specific exceptions (CODING_PATTERNS §2.3)
# =============================================================================


class SearchError(Exception):
    """Base exception for Semantic Search errors."""

    pass


class SearchTimeoutError(SearchError):
    """
    Raised when search request times out.

    GUIDELINES p. 2145: Graceful degradation, timeout handling.
    """

    pass


class SearchConnectionError(SearchError):
    """Raised when unable to connect to search service."""

    pass


class SearchAPIError(SearchError):
    """Raised when search service returns an error response."""

    def __init__(self, message: str, status_code: int, response_body: Optional[dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


# =============================================================================
# SemanticSearchClient - WBS 3.2.3
# Pattern: Connection pooling via context manager (GUIDELINES p. 2313)
# =============================================================================


class SemanticSearchClient:
    """
    Async HTTP client for semantic-search-service microservice.

    Implements connection pooling to avoid creating new httpx.AsyncClient per request.
    Uses async context manager pattern for proper resource cleanup.

    Reference:
    - GUIDELINES p. 2313: "using separate connection pools for different downstream services"
    - CODING_PATTERNS line 67: Anti-Pattern - new httpx.AsyncClient per request

    Attributes:
        base_url: Search service base URL (default: http://localhost:8081)
        timeout: Request timeout in seconds (default: 30.0)
        max_connections: Maximum connections in pool (default: 10)

    Example:
        async with SemanticSearchClient() as client:
            embeddings = await client.embed("domain driven design")
            results = await client.search("repository pattern", limit=5)
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
        Initialize Semantic Search client.

        Args:
            base_url: Search service base URL. Defaults to SEARCH_SERVICE_URL env or localhost:8081
            timeout: Request timeout in seconds. Defaults to SEARCH_SERVICE_TIMEOUT env or 30.0
            max_connections: Max connections in pool. Default 10.
            max_retries: Maximum retry attempts for transient failures. Default 3.
            retry_delay: Base delay between retries in seconds. Default 1.0.

        Pattern: Environment variable configuration with sensible defaults
        Reference: CODING_PATTERNS §2.3 (exponential backoff pattern)
        """
        # Read from environment with fallback to defaults
        self.base_url: str = base_url or os.getenv("SEARCH_SERVICE_URL", "http://localhost:8081") or "http://localhost:8081"
        self.timeout: float = timeout or float(os.getenv("SEARCH_SERVICE_TIMEOUT", "30.0") or "30.0")
        self.max_connections: int = max_connections
        self.max_retries: int = max_retries
        self.retry_delay: float = retry_delay

        # Lazy initialization - client created in __aenter__
        # Pattern: Avoid creating httpx.AsyncClient per request (CODING_PATTERNS line 67)
        self._client: Optional[httpx.AsyncClient] = None

    def _is_retryable_status(self, status_code: int) -> bool:
        """
        Check if HTTP status code is retryable.

        Args:
            status_code: HTTP status code to check.

        Returns:
            True if the status code represents a transient error.
        """
        return status_code in self.RETRYABLE_STATUS_CODES

    async def __aenter__(self) -> "SemanticSearchClient":
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

    def _ensure_client(self) -> httpx.AsyncClient:
        """
        Ensure client is initialized.

        Returns:
            The initialized httpx.AsyncClient.

        Raises:
            RuntimeError: If client not initialized via context manager.
        """
        if self._client is None:
            raise RuntimeError(_CLIENT_NOT_INITIALIZED_ERROR)
        return self._client

    def _handle_error_response(self, response: Any) -> None:
        """Raise appropriate error for HTTP error responses."""
        try:
            error_body = response.json()
        except Exception:
            error_body = {"detail": response.text}
        raise SearchAPIError(
            f"Search service error: {response.status_code}",
            status_code=response.status_code,
            response_body=error_body,
        )

    def _wrap_exception(self, e: Exception) -> Exception:
        """Wrap exception in appropriate SearchError type."""
        if isinstance(e, httpx.TimeoutException):
            return SearchTimeoutError(f"Request timed out: {e}")
        if isinstance(e, httpx.ConnectError):
            return SearchConnectionError(f"Connection failed: {e}")
        return SearchError(f"Unexpected error: {e}")

    async def _attempt_request(
        self,
        client: Any,
        method: str,
        endpoint: str,
        json_data: Optional[dict],
    ) -> Optional[dict]:
        """Attempt a single request, return response or None if retryable."""
        response = await client.request(
            method=method,
            url=endpoint,
            json=json_data,
        )

        if self._is_retryable_status(response.status_code):
            return None

        if response.status_code >= 400:
            self._handle_error_response(response)

        return response.json()

    async def _request_with_retry(
        self,
        method: str,
        endpoint: str,
        json_data: Optional[dict] = None,
    ) -> dict:
        """
        Make HTTP request with exponential backoff retry logic.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            json_data: Optional JSON request body

        Returns:
            JSON response as dictionary

        Raises:
            SearchTimeoutError: If all retry attempts time out
            SearchConnectionError: If unable to connect to service
            SearchAPIError: If service returns an error response
        """
        client = self._ensure_client()
        last_exception: Optional[Exception] = None

        for attempt in range(self.max_retries):
            try:
                result = await self._attempt_request(client, method, endpoint, json_data)
                if result is not None:
                    return result
            except SearchAPIError:
                raise
            except Exception as e:
                last_exception = self._wrap_exception(e)

            if attempt < self.max_retries - 1:
                delay = self.retry_delay * (2 ** attempt)
                await asyncio.sleep(delay)

        if last_exception is not None:
            raise last_exception
        raise SearchError("Request failed after all retries")

    # =========================================================================
    # Embed - WBS 3.2.3.3
    # Pattern: Text embedding via semantic-search-service
    # =========================================================================

    async def embed(self, text: str | list[str]) -> list[list[float]]:
        """
        Generate embeddings for text using semantic-search-service.

        Args:
            text: Single text string or list of texts to embed

        Returns:
            List of embedding vectors (768 dimensions each for all-mpnet-base-v2)

        Raises:
            SearchTimeoutError: If request times out
            SearchConnectionError: If unable to connect to service
            SearchAPIError: If service returns an error

        Example:
            async with SemanticSearchClient() as client:
                # Single text
                embeddings = await client.embed("domain driven design")
                # embeddings = [[0.123, 0.456, ...]]  # 768 dimensions
                
                # Batch texts
                embeddings = await client.embed(["text1", "text2", "text3"])
                # embeddings = [[...], [...], [...]]  # 3 x 768 dimensions
        """
        response = await self._request_with_retry(
            method="POST",
            endpoint="/v1/embed",
            json_data={"text": text},
        )
        return response.get("embeddings", [])

    # =========================================================================
    # Search - WBS 3.2.3.4
    # Pattern: Vector search via semantic-search-service
    # =========================================================================

    async def search(
        self,
        query: str,
        limit: int = 10,
        collection: str = _DEFAULT_COLLECTION,
        filters: Optional[dict[str, Any]] = None,
    ) -> list[dict]:
        """
        Search for similar content using semantic similarity.

        Args:
            query: Search query text
            limit: Maximum number of results to return (default: 10)
            collection: Qdrant collection to search (default: "chapters")
            filters: Optional filters to apply (e.g., {"tier": 1})

        Returns:
            List of search results with id, score, and payload

        Raises:
            SearchTimeoutError: If request times out
            SearchConnectionError: If unable to connect to service
            SearchAPIError: If service returns an error

        Example:
            async with SemanticSearchClient() as client:
                results = await client.search(
                    query="repository pattern",
                    limit=5,
                    collection="chapters"
                )
                for result in results:
                    print(f"{result['payload']['title']}: {result['score']:.4f}")
        """
        request_data: dict[str, Any] = {
            "query": query,
            "limit": limit,
            "collection": collection,
        }
        if filters:
            request_data["filters"] = filters

        response = await self._request_with_retry(
            method="POST",
            endpoint="/v1/search",
            json_data=request_data,
        )
        return response.get("results", [])

    # =========================================================================
    # Hybrid Search - WBS 3.2.3.5
    # Pattern: Combined semantic + keyword search with focus areas
    # =========================================================================

    async def hybrid_search(
        self,
        query: str,
        focus_areas: Optional[list[str]] = None,
        limit: int = 10,
        collection: str = _DEFAULT_COLLECTION,
        filters: Optional[dict[str, Any]] = None,
    ) -> list[dict]:
        """
        Perform hybrid search combining semantic similarity with focus area filtering.

        Args:
            query: Search query text
            focus_areas: Optional list of focus areas to prioritize (e.g., ["architecture", "patterns"])
            limit: Maximum number of results to return (default: 10)
            collection: Qdrant collection to search (default: "chapters")
            filters: Optional additional filters

        Returns:
            List of search results with id, score, and payload

        Raises:
            SearchTimeoutError: If request times out
            SearchConnectionError: If unable to connect to service
            SearchAPIError: If service returns an error

        Example:
            async with SemanticSearchClient() as client:
                results = await client.hybrid_search(
                    query="microservices communication",
                    focus_areas=["architecture", "integration"],
                    limit=10
                )
        """
        request_data: dict[str, Any] = {
            "query": query,
            "limit": limit,
            "collection": collection,
        }
        if focus_areas:
            request_data["focus_areas"] = focus_areas
        if filters:
            request_data["filters"] = filters

        response = await self._request_with_retry(
            method="POST",
            endpoint="/v1/hybrid-search",
            json_data=request_data,
        )
        return response.get("results", [])

    # =========================================================================
    # Health Check
    # Pattern: Service health verification
    # =========================================================================

    async def health_check(self) -> dict:
        """
        Check health of semantic-search-service.

        Returns:
            Health status dictionary

        Example:
            async with SemanticSearchClient() as client:
                health = await client.health_check()
                print(f"Status: {health.get('status')}")
        """
        return await self._request_with_retry(
            method="GET",
            endpoint="/health",
        )
