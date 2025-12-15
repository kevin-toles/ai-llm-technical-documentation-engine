"""
Orchestrator Client - WBS 5.1.2 Client Module Setup

Async HTTP client for Code-Orchestrator-Service microservice with connection pooling.

Reference Documents:
- GUIDELINES p. 2313: "Different connection pools for each downstream service" (Newman)
- GUIDELINES p. 2145: Connection pooling, graceful degradation, circuit breaker patterns
- CODING_PATTERNS_ANALYSIS line 67: Anti-Pattern - new httpx.AsyncClient per request
- Code-Orchestrator-Service/docs/ARCHITECTURE.md: API endpoints (/v1/search)
- WBS_IMPLEMENTATION.md: Phase 5.1.2 - OrchestratorClient
- WBS_IMPLEMENTATION.md: Phase 6.1/6.2 - Caching and Observability

Anti-Patterns Avoided:
- §12: Single httpx.AsyncClient reused via context manager (connection pooling)
- §2.3: Exponential backoff retry for transient failures
- §7/§13: Exception naming follows *Error suffix pattern
- §4.4: Protocol compliance via OrchestratorClientProtocol

Usage:
    async with OrchestratorClient() as client:
        results = await client.search(
            query="domain driven design",
            top_k=5,
            threshold=0.3
        )
"""

from __future__ import annotations

import asyncio
import os
from typing import TYPE_CHECKING, Any, Optional, Protocol, runtime_checkable

import httpx

if TYPE_CHECKING:
    from workflows.shared.clients.cache import ResultCache
    from workflows.shared.clients.metrics import MetricsCollector, PerformanceLogger


# =============================================================================
# Constants - SonarQube S1192: Extract duplicated literals
# =============================================================================

_CLIENT_NOT_INITIALIZED_ERROR = "Client not initialized. Use async context manager."
_DEFAULT_SEARCH_ENDPOINT = "/v1/search"

# WBS 5.1.4: Semantic similarity threshold (down from 0.7 TF-IDF to 0.3 semantic)
# Reference: WBS_IMPLEMENTATION.md - Phase 5.1.4
SEMANTIC_SIMILARITY_THRESHOLD = 0.3


# =============================================================================
# Custom Exceptions - WBS 5.1.2
# Pattern: Domain-specific exceptions (CODING_PATTERNS §7/§13)
# =============================================================================


class OrchestratorClientError(Exception):
    """
    Base exception for Orchestrator Client errors.

    Reference: CODING_PATTERNS §7/§13 - Exception naming follows *Error pattern.
    """

    def __init__(
        self, message: str, status_code: Optional[int] = None
    ):
        super().__init__(message)
        self.status_code = status_code


class OrchestratorTimeoutError(OrchestratorClientError):
    """
    Raised when orchestrator request times out.

    GUIDELINES p. 2145: Graceful degradation, timeout handling.
    """

    pass


class OrchestratorConnectionError(OrchestratorClientError):
    """Raised when unable to connect to orchestrator service."""

    pass


class OrchestratorAPIError(OrchestratorClientError):
    """Raised when orchestrator service returns an error response."""

    def __init__(
        self, message: str, status_code: int, response_body: Optional[dict] = None
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


# =============================================================================
# Protocol - WBS 5.1.2
# Pattern: Duck typing via Protocol (CODING_PATTERNS §4.4)
# =============================================================================


@runtime_checkable
class OrchestratorClientProtocol(Protocol):
    """
    Protocol for OrchestratorClient to enable duck typing and testing.

    Reference: CODING_PATTERNS §4.4 - Protocol compliance for interface contracts.
    Pattern: Dependency Injection via Protocol (Architecture Patterns Ch. 13)
    """

    async def search(
        self,
        query: str,
        domain: Optional[str] = None,
        top_k: int = 5,
        threshold: float = SEMANTIC_SIMILARITY_THRESHOLD,
    ) -> list[dict[str, Any]]:
        """Search for semantically similar content."""
        ...

    async def __aenter__(self) -> "OrchestratorClientProtocol":
        """Enter async context manager."""
        ...

    async def __aexit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any],
    ) -> None:
        """Exit async context manager."""
        ...


# =============================================================================
# OrchestratorClient - WBS 5.1.2
# Pattern: Connection pooling via context manager (GUIDELINES p. 2313)
# =============================================================================


class OrchestratorClient:
    """
    Async HTTP client for Code-Orchestrator-Service microservice.

    Implements connection pooling to avoid creating new httpx.AsyncClient per request.
    Uses async context manager pattern for proper resource cleanup.

    Reference:
    - GUIDELINES p. 2313: Connection pooling for downstream services
    - CODING_PATTERNS line 67: Anti-Pattern - new httpx.AsyncClient per request

    Attributes:
        base_url: Orchestrator service base URL (default: http://localhost:8083)
        timeout: Request timeout in seconds (default: 30.0)
        max_connections: Maximum connections in pool (default: 10)

    Example:
        async with OrchestratorClient() as client:
            results = await client.search(
                query="domain driven design",
                top_k=5,
                threshold=0.3
            )
    """

    # Retryable status codes - GUIDELINES p. 2309 (rate limiting)
    RETRYABLE_STATUS_CODES: frozenset[int] = frozenset({429, 502, 503, 504})

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        max_connections: int = 10,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        cache: Optional["ResultCache"] = None,
        metrics: Optional["MetricsCollector"] = None,
        perf_logger: Optional["PerformanceLogger"] = None,
    ) -> None:
        """
        Initialize Orchestrator client.

        Args:
            base_url: Service base URL. Defaults to ORCHESTRATOR_URL env.
            timeout: Request timeout in seconds. Defaults to 30.0.
            max_connections: Max connections in pool. Default 10.
            max_retries: Maximum retry attempts for transient failures. Default 3.
            retry_delay: Base delay between retries in seconds. Default 1.0.
            cache: Optional ResultCache for caching search results (WBS 6.1.2).
            metrics: Optional MetricsCollector for observability (WBS 6.2.1).
            perf_logger: Optional PerformanceLogger for timing logs (WBS 6.2.3).

        Pattern: Environment variable configuration with sensible defaults
        Reference: CODING_PATTERNS §2.3 (exponential backoff pattern)
        """
        # Read from environment with fallback to defaults
        self.base_url: str = (
            base_url
            or os.getenv("ORCHESTRATOR_URL", "http://localhost:8083")
            or "http://localhost:8083"
        )
        self.timeout: float = timeout or float(
            os.getenv("ORCHESTRATOR_TIMEOUT", "30.0") or "30.0"
        )
        self.max_connections: int = max_connections
        self.max_retries: int = max_retries
        self.retry_delay: float = retry_delay

        # WBS 6.1/6.2: Observability components
        self.cache = cache
        self.metrics = metrics
        self.perf_logger = perf_logger

        # Lazy initialization - client created in __aenter__
        # Pattern: Avoid creating httpx.AsyncClient per request
        self._client: Optional[httpx.AsyncClient] = None

    def _is_retryable_status(self, status_code: int) -> bool:
        """
        Check if HTTP status code is retryable.

        Extracted to reduce cognitive complexity (CODING_PATTERNS §2.3).

        Args:
            status_code: HTTP status code to check.

        Returns:
            True if the status code represents a transient error.
        """
        return status_code in self.RETRYABLE_STATUS_CODES

    async def __aenter__(self) -> "OrchestratorClient":
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

    # =========================================================================
    # Search - WBS 5.1.2 + 6.1/6.2 (caching, metrics)
    # Pattern: POST /v1/search (Code-Orchestrator-Service API)
    # =========================================================================

    async def search(
        self,
        query: str,
        domain: Optional[str] = None,
        top_k: int = 5,
        threshold: float = SEMANTIC_SIMILARITY_THRESHOLD,
        skip_cache: bool = False,
    ) -> list[dict[str, Any]]:
        """
        Search for semantically similar content via Code-Orchestrator-Service.

        Reference: Code-Orchestrator-Service/docs/ARCHITECTURE.md - POST /api/v1/search

        Args:
            query: Search query text
            domain: Optional domain filter (e.g., "ai-ml", "architecture")
            top_k: Maximum number of results to return (default: 5)
            threshold: Minimum similarity threshold (default: 0.3)
            skip_cache: If True, bypass cache (WBS 6.1.2)

        Returns:
            List of search result dicts with keys:
            - id: Unique result identifier
            - content: Matched content text
            - metadata: Dict with source, chapter, title info
            - score: Similarity score (0.0-1.0)

        Raises:
            ValueError: If query is empty
            OrchestratorTimeoutError: On request timeout
            OrchestratorConnectionError: On connection failure
            OrchestratorAPIError: On 4xx API errors (not 5xx - those degrade gracefully)
        """
        import time
        start_time = time.time()

        # Track request count (WBS 6.2.1)
        if self.metrics:
            self.metrics.increment_counter("orchestrator_requests_total")

        # Validate query - Pattern: Input validation
        if not query or not query.strip():
            raise ValueError("query must not be empty")

        # WBS 6.1.2: Check cache first
        cache_key = f"search:{query}:{domain or ''}:{top_k}:{threshold}"
        if self.cache and not skip_cache:
            cached = self.cache.get(cache_key)
            if cached is not None:
                # Track cache hit (WBS 6.2.1)
                if self.metrics:
                    self.metrics.increment_counter("orchestrator_cache_hits_total")
                self._record_timing(start_time, "search")
                return cached

        # Build request payload
        payload: dict[str, Any] = {
            "query": query,
            "top_k": top_k,
            "threshold": threshold,
        }

        # Add optional domain filter
        if domain is not None:
            payload["domain"] = domain

        # Make request with error handling and retry
        # Pattern: Timeout handling for graceful degradation (GUIDELINES p. 2145)
        # Pattern: Retry with exponential backoff (CODING_PATTERNS §2.3)
        try:
            response = await self._request_with_retry(
                method="POST",
                endpoint=_DEFAULT_SEARCH_ENDPOINT,
                json_data=payload,
            )
        except OrchestratorAPIError as e:
            # Graceful degradation: return empty on 5xx (service unavailable)
            if e.status_code and e.status_code >= 500:
                self._record_timing(start_time, "search")
                return []
            raise  # Re-raise 4xx errors

        # Extract results from response
        # Code-Orchestrator-Service returns {"results": [...], "total": int}
        results = response.get("results", [])

        # WBS 6.1.2: Store in cache
        if self.cache:
            self.cache.set(cache_key, results)

        # WBS 6.2: Record timing
        self._record_timing(start_time, "search")

        return results

    def _record_timing(self, start_time: float, operation: str) -> None:
        """Record timing metrics and logs (WBS 6.2)."""
        import time
        duration_s = time.time() - start_time
        duration_ms = duration_s * 1000

        # Record histogram (WBS 6.2.1)
        if self.metrics:
            self.metrics.observe_histogram("orchestrator_latency_seconds", duration_s)

        # Log timing (WBS 6.2.3)
        if self.perf_logger:
            self.perf_logger.log_timing(operation, duration_ms=duration_ms)

    # =========================================================================
    # Batch Search - WBS 6.1.3
    # =========================================================================

    async def batch_search(
        self,
        queries: list[dict[str, Any]],
    ) -> list[list[dict[str, Any]]]:
        """
        Execute multiple searches in batch.

        WBS 6.1.3: Batch inference support.

        Args:
            queries: List of query dicts with keys: query, domain, top_k, threshold

        Returns:
            List of result lists, one per input query
        """
        results = []
        for q in queries:
            r = await self.search(
                query=q.get("query", ""),
                domain=q.get("domain"),
                top_k=q.get("top_k", 5),
                threshold=q.get("threshold", SEMANTIC_SIMILARITY_THRESHOLD),
            )
            results.append(r)
        return results

    async def _request_with_retry(
        self,
        method: str,
        endpoint: str,
        json_data: Optional[dict] = None,
    ) -> dict:
        """
        Make HTTP request with exponential backoff retry logic.

        WBS 5.1.2: Retry logic for transient failures (503, 429, 502, 504).
        Pattern: Exponential backoff (CODING_PATTERNS §2.3)
        Reference: GUIDELINES p. 466 (fail fast then retry at higher level)

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            json_data: Optional JSON request body

        Returns:
            JSON response as dictionary

        Raises:
            OrchestratorTimeoutError: If all retry attempts time out
            OrchestratorConnectionError: If unable to connect to service
            OrchestratorAPIError: If service returns an error response
        """
        client = self._ensure_client()
        last_exception: Optional[Exception] = None

        for attempt in range(self.max_retries):
            try:
                response = await client.request(
                    method=method,
                    url=endpoint,
                    json=json_data,
                )

                # Check for retryable status codes
                if self._is_retryable_status(response.status_code):
                    if attempt < self.max_retries - 1:
                        delay = self.retry_delay * (2**attempt)  # Exponential backoff
                        await asyncio.sleep(delay)
                        continue

                # Handle error responses
                if response.status_code >= 400:
                    try:
                        error_body = response.json()
                    except Exception:
                        error_body = {"detail": response.text}
                    raise OrchestratorAPIError(
                        f"Orchestrator service error: {response.status_code}",
                        status_code=response.status_code,
                        response_body=error_body,
                    )

                return response.json()

            except httpx.TimeoutException as e:
                last_exception = OrchestratorTimeoutError(f"Request timed out: {e}")
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2**attempt)
                    await asyncio.sleep(delay)
                    continue

            except httpx.ConnectError as e:
                last_exception = OrchestratorConnectionError(
                    f"Connection failed: {e}"
                )
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2**attempt)
                    await asyncio.sleep(delay)
                    continue

            except OrchestratorAPIError:
                raise

            except Exception as e:
                last_exception = OrchestratorClientError(f"Unexpected error: {e}")
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2**attempt)
                    await asyncio.sleep(delay)
                    continue

        # All retries exhausted
        if last_exception is not None:
            raise last_exception
        raise OrchestratorClientError("Request failed after all retries")


# =============================================================================
# FakeOrchestratorClient - Testing Support
# Pattern: Test Double (Architecture Patterns Ch. 13)
# =============================================================================


class FakeOrchestratorClient:
    """
    Fake implementation of OrchestratorClient for unit testing.

    Reference: Architecture Patterns with Python Ch. 13 - Test Doubles
    Pattern: Dependency Injection via Protocol compliance

    Example:
        fake_client = FakeOrchestratorClient(results=[
            {"id": "1", "content": "DDD", "score": 0.9, "metadata": {}}
        ])
        async with fake_client as client:
            results = await client.search("domain driven design")
    """

    def __init__(
        self,
        results: Optional[list[dict[str, Any]]] = None,
        error: Optional[OrchestratorClientError] = None,
        should_fail: bool = False,
    ) -> None:
        """
        Initialize fake client.

        Args:
            results: Results to return from search() calls
            error: Optional exception to raise on search() calls
            should_fail: If True, raises OrchestratorClientError on search()
        """
        self.results = results or []
        self.error = error
        self.should_fail = should_fail
        self.search_calls: list[dict[str, Any]] = []

    async def search(
        self,
        query: str,
        domain: Optional[str] = None,
        top_k: int = 5,
        threshold: float = SEMANTIC_SIMILARITY_THRESHOLD,
        skip_cache: bool = False,
    ) -> list[dict[str, Any]]:
        """
        Fake search implementation.

        Records call parameters for assertion and returns configured results.
        """
        self.search_calls.append({
            "query": query,
            "domain": domain,
            "top_k": top_k,
            "threshold": threshold,
        })

        if self.should_fail:
            raise OrchestratorClientError("Simulated failure", status_code=500)

        if self.error is not None:
            raise self.error

        return self.results

    async def batch_search(
        self,
        queries: list[dict[str, Any]],
    ) -> list[list[dict[str, Any]]]:
        """
        Fake batch search implementation.

        Returns configured results for each query.
        """
        results = []
        for q in queries:
            r = await self.search(
                query=q.get("query", ""),
                domain=q.get("domain"),
                top_k=q.get("top_k", 5),
                threshold=q.get("threshold", SEMANTIC_SIMILARITY_THRESHOLD),
            )
            results.append(r)
        return results

    async def __aenter__(self) -> "FakeOrchestratorClient":
        """Enter async context (no-op for fake)."""
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any],
    ) -> None:
        """Exit async context (no-op for fake)."""
        pass
