"""SBERT Client - WBS M3.1 API Client Implementation.

Async HTTP client for Code-Orchestrator-Service SBERT API with connection pooling.

Reference Documents:
- SBERT_EXTRACTION_MIGRATION_WBS.md: M3.1 API Client Implementation
- GUIDELINES p. 2313: Connection pooling (Newman)
- GUIDELINES p. 2145: Connection pooling, graceful degradation
- CODING_PATTERNS_ANALYSIS: Anti-Pattern #12 - new httpx.AsyncClient per request
- Code-Orchestrator-Service: SBERT API endpoints (/v1/embeddings, /v1/similarity)

Anti-Patterns Avoided:
- #7/#13: Exception naming follows *Error suffix pattern
- #12: Single httpx.AsyncClient reused via context manager (connection pooling)
- S1172: No unused parameters
- S1192: Constants for endpoints, dimensions

Usage:
    async with SBERTClient() as client:
        # Get embeddings
        embeddings = await client.get_embeddings(texts=["hello", "world"])

        # Get similarity score
        score = await client.get_similarity(text1="cat", text2="dog")
"""

from __future__ import annotations

import asyncio
import os
from typing import Any, Optional, Protocol, runtime_checkable

import httpx

# =============================================================================
# Constants - SonarQube S1192: Extract duplicated literals
# =============================================================================

_CLIENT_NOT_INITIALIZED_ERROR = "Client not initialized. Use async context manager."
_DEFAULT_EMBEDDINGS_ENDPOINT = "/v1/embeddings"
_DEFAULT_SIMILARITY_ENDPOINT = "/v1/similarity"
_DEFAULT_SIMILAR_CHAPTERS_ENDPOINT = "/v1/similar-chapters"
_DEFAULT_BASE_URL = "http://localhost:8083"
_DEFAULT_TIMEOUT = 30.0

# MiniLM-L6-v2 embedding dimensions
EMBEDDING_DIMENSIONS = 384


# =============================================================================
# Custom Exceptions - WBS M3.1
# Pattern: Domain-specific exceptions (CODING_PATTERNS §7/§13)
# Anti-Pattern #7: Never shadow builtins like ConnectionError, TimeoutError
# =============================================================================


class SBERTClientError(Exception):
    """
    Base exception for SBERT Client errors.

    Reference: CODING_PATTERNS §7/§13 - Exception naming follows *Error pattern.
    """

    def __init__(
        self, message: str, status_code: Optional[int] = None
    ) -> None:
        super().__init__(message)
        self.status_code = status_code


class SBERTTimeoutError(SBERTClientError):
    """
    Raised when SBERT API request times out.

    GUIDELINES p. 2145: Graceful degradation, timeout handling.
    Anti-Pattern #7: Named SBERTTimeoutError, not TimeoutError (avoids shadowing).
    """

    pass


class SBERTConnectionError(SBERTClientError):
    """Raised when unable to connect to SBERT API service.

    Anti-Pattern #7: Named SBERTConnectionError, not ConnectionError (avoids shadowing).
    """

    pass


class SBERTAPIError(SBERTClientError):
    """Raised when SBERT API returns an error response (4xx/5xx)."""

    def __init__(
        self, message: str, status_code: int, response_body: Optional[dict] = None
    ) -> None:
        super().__init__(message, status_code)
        self.status_code = status_code
        self.response_body = response_body


# =============================================================================
# Protocol - WBS M3.1
# Pattern: Duck typing via Protocol (CODING_PATTERNS §4.4)
# =============================================================================


@runtime_checkable
class SBERTClientProtocol(Protocol):
    """
    Protocol for SBERTClient to enable duck typing and testing.

    Reference: CODING_PATTERNS §4.4 - Protocol compliance for interface contracts.
    Pattern: Dependency Injection via Protocol (Architecture Patterns Ch. 13)
    """

    async def get_embeddings(
        self, texts: list[str]
    ) -> list[list[float]]:
        """Get embeddings for list of texts."""
        ...

    async def get_similarity(
        self, text1: str, text2: str
    ) -> float:
        """Get similarity score between two texts."""
        ...

    async def __aenter__(self) -> "SBERTClientProtocol":
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
# SBERTClient - WBS M3.1
# Pattern: Connection pooling via context manager (GUIDELINES p. 2313)
# =============================================================================


class SBERTClient:
    """
    Async HTTP client for Code-Orchestrator-Service SBERT API.

    Implements connection pooling to avoid creating new httpx.AsyncClient per request.
    Uses async context manager pattern for proper resource cleanup.

    Reference:
    - GUIDELINES p. 2313: Connection pooling for downstream services
    - CODING_PATTERNS line 67: Anti-Pattern - new httpx.AsyncClient per request
    - Code-Orchestrator-Service: /v1/embeddings, /v1/similarity endpoints

    Attributes:
        base_url: SBERT API base URL (default: http://localhost:8083)
        timeout: Request timeout in seconds (default: 30.0)
        max_connections: Maximum connections in pool (default: 10)

    Example:
        async with SBERTClient() as client:
            embeddings = await client.get_embeddings(texts=["hello", "world"])
            score = await client.get_similarity(text1="cat", text2="dog")
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
    ) -> None:
        """
        Initialize SBERT client.

        Args:
            base_url: Service base URL. Defaults to SBERT_API_URL env or localhost:8083.
            timeout: Request timeout in seconds. Defaults to 30.0.
            max_connections: Max connections in pool. Default 10.
            max_retries: Maximum retry attempts for transient failures. Default 3.
            retry_delay: Base delay between retries in seconds. Default 1.0.

        Pattern: Environment variable configuration with sensible defaults
        Reference: CODING_PATTERNS §2.3 (exponential backoff pattern)
        """
        # Read from environment with fallback to defaults
        self.base_url: str = (
            base_url
            or os.getenv("SBERT_API_URL", _DEFAULT_BASE_URL)
            or _DEFAULT_BASE_URL
        )
        timeout_env = os.getenv("SBERT_API_TIMEOUT", str(_DEFAULT_TIMEOUT))
        self.timeout: float = timeout or float(timeout_env or str(_DEFAULT_TIMEOUT))
        self.max_connections: int = max_connections
        self.max_retries: int = max_retries
        self.retry_delay: float = retry_delay

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

    async def __aenter__(self) -> "SBERTClient":
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
    # Embeddings API - WBS M3.1.3/M3.1.4
    # Pattern: POST /v1/embeddings (Code-Orchestrator-Service SBERT API)
    # =========================================================================

    async def get_embeddings(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Get embeddings for a list of texts via Code-Orchestrator SBERT API.

        Reference: Code-Orchestrator-Service API - POST /v1/embeddings

        Args:
            texts: List of texts to embed.

        Returns:
            List of embedding vectors (384 dimensions each for MiniLM-L6-v2).

        Raises:
            SBERTConnectionError: If unable to connect to service.
            SBERTTimeoutError: If request times out.
            SBERTAPIError: If service returns error response.
            RuntimeError: If client not initialized via context manager.
        """
        self._ensure_client()

        try:
            response = await self._request_with_retry(
                method="POST",
                endpoint=_DEFAULT_EMBEDDINGS_ENDPOINT,
                json_data={"texts": texts},
            )

            data = response.json()
            return data.get("embeddings", [])

        except httpx.ConnectError as e:
            raise SBERTConnectionError(f"Failed to connect to SBERT API: {e}") from e
        except httpx.TimeoutException as e:
            raise SBERTTimeoutError(f"SBERT API request timed out: {e}") from e

    # =========================================================================
    # Similarity API - WBS M3.1.5/M3.1.6
    # Pattern: POST /v1/similarity (Code-Orchestrator-Service SBERT API)
    # =========================================================================

    async def get_similarity(
        self,
        text1: str,
        text2: str,
    ) -> float:
        """
        Get cosine similarity between two texts via Code-Orchestrator SBERT API.

        Reference: Code-Orchestrator-Service API - POST /v1/similarity

        Args:
            text1: First text.
            text2: Second text.

        Returns:
            Similarity score between 0.0 and 1.0.

        Raises:
            SBERTConnectionError: If unable to connect to service.
            SBERTTimeoutError: If request times out.
            SBERTAPIError: If service returns error response.
            RuntimeError: If client not initialized via context manager.
        """
        self._ensure_client()

        try:
            response = await self._request_with_retry(
                method="POST",
                endpoint=_DEFAULT_SIMILARITY_ENDPOINT,
                json_data={"text1": text1, "text2": text2},
            )

            data = response.json()
            return float(data.get("similarity", 0.0))

        except httpx.ConnectError as e:
            raise SBERTConnectionError(f"Failed to connect to SBERT API: {e}") from e
        except httpx.TimeoutException as e:
            raise SBERTTimeoutError(f"SBERT API request timed out: {e}") from e

    # =========================================================================
    # Retry Logic - CODING_PATTERNS §2.3
    # Pattern: Exponential backoff for transient failures
    # =========================================================================

    async def _request_with_retry(
        self,
        method: str,
        endpoint: str,
        json_data: Optional[dict] = None,
    ) -> httpx.Response:
        """
        Make HTTP request with exponential backoff retry.

        Reference: CODING_PATTERNS §2.3 - Exponential backoff pattern

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            json_data: Optional JSON body

        Returns:
            httpx.Response object

        Raises:
            SBERTAPIError: If all retries exhausted or non-retryable error
        """
        client = self._ensure_client()
        last_error: Optional[Exception] = None

        for attempt in range(self.max_retries):
            try:
                response = await client.request(
                    method=method,
                    url=endpoint,
                    json=json_data,
                )

                # Success
                if response.status_code < 400:
                    return response

                # Client error (4xx) - don't retry
                if 400 <= response.status_code < 500:
                    raise SBERTAPIError(
                        message=f"SBERT API error: {response.status_code}",
                        status_code=response.status_code,
                        response_body=self._safe_json(response),
                    )

                # Server error (5xx) - retry if retryable
                if self._is_retryable_status(response.status_code):
                    last_error = SBERTAPIError(
                        message=f"SBERT API error: {response.status_code}",
                        status_code=response.status_code,
                        response_body=self._safe_json(response),
                    )
                    await asyncio.sleep(self.retry_delay * (2 ** attempt))
                    continue

                # Non-retryable server error
                raise SBERTAPIError(
                    message=f"SBERT API error: {response.status_code}",
                    status_code=response.status_code,
                    response_body=self._safe_json(response),
                )

            except (httpx.ConnectError, httpx.TimeoutException):
                raise
            except SBERTAPIError:
                raise
            except Exception as e:
                last_error = e
                await asyncio.sleep(self.retry_delay * (2 ** attempt))

        # All retries exhausted
        if last_error:
            raise last_error
        raise SBERTAPIError(
            message="All retry attempts exhausted",
            status_code=500,
        )

    def _safe_json(self, response: httpx.Response) -> Optional[dict]:
        """Safely parse JSON response, returning None on failure."""
        try:
            return response.json()
        except Exception:
            return None


# =============================================================================
# FakeSBERTClient - For Unit Testing
# Pattern: FakeClient for testing (Anti-Pattern #12 Prevention)
# =============================================================================


class FakeSBERTClient:
    """
    In-memory fake SBERT client for unit testing.

    Avoids real HTTP connections in tests.
    Reference: CODING_PATTERNS - FakeClient for Testing pattern.

    Example:
        fake = FakeSBERTClient()
        fake.set_embeddings({"hello": [0.1] * 384})

        async with fake:
            embeddings = await fake.get_embeddings(texts=["hello"])
    """

    def __init__(self) -> None:
        """Initialize fake client with empty data."""
        self._embeddings: dict[str, list[float]] = {}
        self._similarity_scores: dict[tuple[str, str], float] = {}
        self._client: Optional[object] = None  # For protocol compliance

    def set_embeddings(self, embeddings: dict[str, list[float]]) -> None:
        """Set fake embeddings for specific texts."""
        self._embeddings = embeddings

    def set_similarity(self, text1: str, text2: str, score: float) -> None:
        """Set fake similarity score for a text pair."""
        self._similarity_scores[(text1, text2)] = score
        self._similarity_scores[(text2, text1)] = score  # Symmetric

    async def __aenter__(self) -> "FakeSBERTClient":
        """Enter async context (no-op for fake)."""
        self._client = object()  # Simulate initialized client
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any],
    ) -> None:
        """Exit async context (no-op for fake)."""
        self._client = None

    async def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        """
        Get fake embeddings for texts.

        Returns default 384-dimension vectors if not pre-configured.
        """
        await asyncio.sleep(0)  # Proper async behavior per SonarLint
        return [
            self._embeddings.get(text, [0.0] * EMBEDDING_DIMENSIONS)
            for text in texts
        ]

    async def get_similarity(self, text1: str, text2: str) -> float:
        """
        Get fake similarity score.

        Returns 0.5 if not pre-configured.
        """
        await asyncio.sleep(0)  # Proper async behavior per SonarLint
        return self._similarity_scores.get((text1, text2), 0.5)
