"""MSEP Client - WBS MSE-6.1 API Client Implementation.

Async HTTP client for Gateway -> ai-agents MSEP API with connection pooling.

Reference Documents:
- llm-gateway/src/api/routes/tools.py: POST /v1/tools/execute endpoint
- llm-gateway/src/tools/builtin/enrich_metadata.py: Gateway tool proxy
- ai-agents/src/api/routes/enrich_metadata.py: POST /v1/agents/enrich-metadata endpoint
- WBS MSE-6.1 AC-6.1.1: enrich_metadata(corpus, chapter_index, config) method
- CODING_PATTERNS_ANALYSIS: Anti-Pattern #12 (single httpx.AsyncClient)
- GUIDELINES p. 2313: Connection pooling (Newman)

Kitchen Brigade Pattern:
- llm-document-enhancer (CUSTOMER) calls Gateway (MANAGER)
- Gateway routes to ai-agents (EXPEDITOR) for enrichment
- NO direct ai-agents calls from external applications

Architecture Flow:
    External App (llm-document-enhancer)
        → Gateway:8080 POST /v1/tools/execute {"name": "enrich_metadata", ...}
        → ai-agents:8082 POST /v1/agents/enrich-metadata

Anti-Patterns Avoided:
- #7/#13: Exception naming follows *Error suffix pattern
- #12: Single httpx.AsyncClient reused via context manager (connection pooling)
- S1172: No unused parameters
- S1192: Constants for endpoints, URLs

Usage:
    async with MSEPClient() as client:
        # Build chapter index per WBS MSE-2 schema
        chapter_index = [
            ChapterMeta(book="Architecture Patterns", chapter=1, title="Introduction"),
            ChapterMeta(book="Architecture Patterns", chapter=2, title="Fundamentals"),
        ]
        corpus = ["Chapter 1 content...", "Chapter 2 content..."]
        config = MSEPConfig(threshold=0.45, top_k=5)

        response = await client.enrich_metadata(corpus, chapter_index, config)
        for chapter in response.chapters:
            print(f"Chapter {chapter.chapter_id}: {chapter.keywords.merged}")
"""

from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass, field
from typing import Any, Optional, Protocol, runtime_checkable

import httpx


# =============================================================================
# Constants - SonarQube S1192
# =============================================================================

_CLIENT_NOT_INITIALIZED_ERROR = "Client not initialized. Use async context manager."
_DEFAULT_ENRICH_ENDPOINT = "/v1/tools/execute"
_DEFAULT_BASE_URL = "http://localhost:8080"
_DEFAULT_TIMEOUT = 30.0
_DEFAULT_MAX_CONNECTIONS = 10
_DEFAULT_MAX_RETRIES = 3
_DEFAULT_RETRY_DELAY = 1.0


# =============================================================================
# Custom Exceptions - MSE-6.1
# Pattern: Domain-specific exceptions (CODING_PATTERNS §7/§13)
# Anti-Pattern #7: Never shadow builtins like ConnectionError, TimeoutError
# =============================================================================


class MSEPClientError(Exception):
    """
    Base exception for MSEP Client errors.

    Reference: CODING_PATTERNS §7/§13 - Exception naming follows *Error pattern.

    Attributes:
        status_code: Optional HTTP status code from the response.
    """

    def __init__(
        self, message: str, status_code: Optional[int] = None
    ) -> None:
        super().__init__(message)
        self.status_code = status_code


class MSEPTimeoutError(MSEPClientError):
    """
    Raised when MSEP API request times out.

    Anti-Pattern #7: Named MSEPTimeoutError, not TimeoutError (avoids shadowing).
    """

    pass


class MSEPConnectionError(MSEPClientError):
    """
    Raised when unable to connect to MSEP API service.

    Anti-Pattern #7: Named MSEPConnectionError, not ConnectionError (avoids shadowing).
    """

    pass


class MSEPAPIError(MSEPClientError):
    """
    Raised when MSEP API returns an error response (4xx/5xx).

    Attributes:
        status_code: HTTP status code from the response.
        response_body: Parsed JSON response body if available.
    """

    def __init__(
        self,
        message: str,
        status_code: int,
        response_body: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, status_code)
        self.status_code = status_code
        self.response_body = response_body


# =============================================================================
# Request Dataclasses - MSE-6.1 / MSE-2.1 Schema
# Pattern: Typed dataclasses matching ai-agents endpoint schema
# Reference: WBS AC-2.1.3 - MSEPRequest schema
# =============================================================================


@dataclass
class ChapterMeta:
    """Chapter metadata for MSEP request.

    Reference: WBS AC-2.1.2 - ChapterMeta dataclass
    Maps to: ai-agents ChapterMetaRequest model

    Attributes:
        book: Book title.
        chapter: Chapter number (1-indexed).
        title: Chapter title.
        id: Optional chapter identifier.
    """

    book: str
    chapter: int
    title: str
    id: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict for JSON serialization."""
        result: dict[str, Any] = {
            "book": self.book,
            "chapter": self.chapter,
            "title": self.title,
        }
        if self.id is not None:
            result["id"] = self.id
        return result


@dataclass
class MSEPConfig:
    """Configuration for MSEP enrichment.

    Reference: WBS AC-2.1.4 - MSEPConfig dataclass
    Maps to: ai-agents MSEPConfigRequest model

    Attributes:
        threshold: Similarity threshold (0.0-1.0).
        top_k: Maximum cross-references per chapter.
        timeout: Service timeout in seconds.
        same_topic_boost: Boost for same-topic chapters.
        use_dynamic_threshold: Enable dynamic threshold adjustment.
        enable_hybrid_search: Enable hybrid search.
    """

    threshold: float = 0.45
    top_k: int = 5
    timeout: float = 30.0
    same_topic_boost: float = 0.15
    use_dynamic_threshold: bool = True
    enable_hybrid_search: bool = True

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict for JSON serialization."""
        return {
            "threshold": self.threshold,
            "top_k": self.top_k,
            "timeout": self.timeout,
            "same_topic_boost": self.same_topic_boost,
            "use_dynamic_threshold": self.use_dynamic_threshold,
            "enable_hybrid_search": self.enable_hybrid_search,
        }


# =============================================================================
# Response Dataclasses - MSE-6.2.1
# Pattern: Return typed dataclasses, not dicts (#2.2)
# Maps to: ai-agents EnrichMetadataResponse model
# =============================================================================


@dataclass
class CrossReference:
    """Cross-reference to a related chapter.

    Maps to: ai-agents CrossReferenceResponse model
    """

    target: str
    score: float
    base_score: float
    topic_boost: float
    method: str


@dataclass
class MergedKeywords:
    """Merged keywords from multiple extraction methods.

    Maps to: ai-agents MergedKeywordsResponse model
    """

    tfidf: list[str]
    semantic: list[str]
    merged: list[str]


@dataclass
class Provenance:
    """Provenance information for enrichment decisions.

    Maps to: ai-agents ProvenanceResponse model
    """

    methods_used: list[str]
    sbert_score: float
    topic_boost: float
    timestamp: str


@dataclass
class EnrichedChapter:
    """Enriched metadata for a single chapter.

    Maps to: ai-agents EnrichedChapterResponse model
    Per MULTI_STAGE_ENRICHMENT_PIPELINE_ARCHITECTURE.md Schema Definitions.
    """

    book: str
    chapter: int
    title: str
    chapter_id: str
    cross_references: list[CrossReference]
    keywords: MergedKeywords
    topic_id: int | None
    topic_name: str | None
    graph_relationships: list[str]
    provenance: Provenance


@dataclass
class EnrichedMetadataResponse:
    """Response from MSEP enrich_metadata endpoint.

    Maps to: ai-agents EnrichMetadataResponse model

    Attributes:
        chapters: List of enriched chapter metadata.
        processing_time_ms: Time taken to process the request.
        total_cross_references: Total number of cross-references found.
    """

    chapters: list[EnrichedChapter]
    processing_time_ms: float
    total_cross_references: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EnrichedMetadataResponse":
        """Parse response from API dict.

        Args:
            data: API response dictionary from ai-agents.

        Returns:
            EnrichedMetadataResponse instance.
        """
        chapters = []
        for ch in data.get("chapters", []):
            # Parse cross references
            cross_refs = [
                CrossReference(
                    target=xr["target"],
                    score=xr["score"],
                    base_score=xr["base_score"],
                    topic_boost=xr["topic_boost"],
                    method=xr["method"],
                )
                for xr in ch.get("cross_references", [])
            ]

            # Parse keywords
            kw_data = ch.get("keywords", {})
            keywords = MergedKeywords(
                tfidf=kw_data.get("tfidf", []),
                semantic=kw_data.get("semantic", []),
                merged=kw_data.get("merged", []),
            )

            # Parse provenance
            prov_data = ch.get("provenance", {})
            provenance = Provenance(
                methods_used=prov_data.get("methods_used", []),
                sbert_score=prov_data.get("sbert_score", 0.0),
                topic_boost=prov_data.get("topic_boost", 0.0),
                timestamp=prov_data.get("timestamp", ""),
            )

            chapters.append(
                EnrichedChapter(
                    book=ch.get("book", ""),
                    chapter=ch.get("chapter", 0),
                    title=ch.get("title", ""),
                    chapter_id=ch.get("chapter_id", ""),
                    cross_references=cross_refs,
                    keywords=keywords,
                    topic_id=ch.get("topic_id"),
                    topic_name=ch.get("topic_name"),
                    graph_relationships=ch.get("graph_relationships", []),
                    provenance=provenance,
                )
            )

        return cls(
            chapters=chapters,
            processing_time_ms=data.get("processing_time_ms", 0.0),
            total_cross_references=data.get("total_cross_references", 0),
        )


# =============================================================================
# Protocol - MSE-6.1
# Pattern: Duck typing via Protocol (CODING_PATTERNS §4.4)
# =============================================================================


@runtime_checkable
class MSEPClientProtocol(Protocol):
    """
    Protocol for MSEPClient to enable duck typing and testing.

    Reference: CODING_PATTERNS §4.4 - Protocol compliance for interface contracts.
    Pattern: Dependency Injection via Protocol (Architecture Patterns Ch. 13)
    WBS: AC-6.1.1 - enrich_metadata(corpus, chapter_index, config) method
    """

    async def enrich_metadata(
        self,
        corpus: list[str],
        chapter_index: list[ChapterMeta],
        config: Optional[MSEPConfig] = None,
    ) -> EnrichedMetadataResponse:
        """Enrich chapter metadata via ai-agents MSEP endpoint."""
        ...

    async def __aenter__(self) -> "MSEPClientProtocol":
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
# MSEPClient - MSE-6.1
# Pattern: Connection pooling via context manager (GUIDELINES p. 2313)
# Anti-Pattern #12: Single httpx.AsyncClient instance
# =============================================================================


class MSEPClient:
    """
    Async HTTP client for Gateway -> ai-agents MSEP API.

    Kitchen Brigade Pattern:
    - llm-document-enhancer is CUSTOMER only
    - Calls Gateway (MANAGER) at port 8080
    - Gateway routes to ai-agents (EXPEDITOR) at port 8082
    - NO direct ai-agents calls from external applications

    WBS References:
    - AC-6.1.1: enrich_metadata(corpus, chapter_index, config) method
    - AC-6.1.2: Calls Gateway POST /v1/tools/execute with tool name "enrich_metadata"
    - AC-6.1.5: Default base_url is http://localhost:8080 (Gateway)

    Anti-Patterns Avoided:
    - #12: Single httpx.AsyncClient with connection pooling
    - #7/#13: Exception naming follows *Error pattern

    Usage:
        async with MSEPClient() as client:
            chapter_index = [
                ChapterMeta(book="Book", chapter=1, title="Intro"),
            ]
            response = await client.enrich_metadata(
                corpus=["Chapter content..."],
                chapter_index=chapter_index,
                config=MSEPConfig(threshold=0.5),
            )
    """

    # Retryable HTTP status codes (server errors, rate limiting)
    RETRYABLE_STATUS_CODES: frozenset[int] = frozenset({429, 500, 502, 503, 504})

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: float = _DEFAULT_TIMEOUT,
        max_connections: int = _DEFAULT_MAX_CONNECTIONS,
        max_retries: int = _DEFAULT_MAX_RETRIES,
        retry_delay: float = _DEFAULT_RETRY_DELAY,
    ) -> None:
        """Initialize MSEP client.

        Args:
            base_url: Base URL for Gateway service.
                     Defaults to MSEP_BASE_URL env var or http://localhost:8080.
            timeout: Request timeout in seconds.
            max_connections: Maximum concurrent connections.
            max_retries: Maximum retry attempts for retryable errors.
            retry_delay: Base delay between retries (exponential backoff).
        """
        self.base_url: str = base_url or os.getenv("MSEP_BASE_URL") or _DEFAULT_BASE_URL
        self.timeout = timeout
        self.max_connections = max_connections
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self) -> "MSEPClient":
        """Enter async context manager - initialize connection pool.

        Reference: GUIDELINES p. 2313 - Connection pooling (Newman)
        Anti-Pattern #12: Single client instance for connection reuse

        Returns:
            Self for use in async with block.
        """
        limits = httpx.Limits(max_connections=self.max_connections)
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            limits=limits,
        )
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any],
    ) -> None:
        """Exit async context manager - close connection pool.

        Args:
            exc_type: Exception type if raised.
            exc_val: Exception value if raised.
            exc_tb: Exception traceback if raised.
        """
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def enrich_metadata(
        self,
        corpus: list[str],
        chapter_index: list[ChapterMeta],
        config: Optional[MSEPConfig] = None,
    ) -> EnrichedMetadataResponse:
        """Enrich chapter metadata via Gateway -> ai-agents MSEP endpoint.

        Kitchen Brigade: 
        - llm-document-enhancer (CUSTOMER) calls Gateway (MANAGER)
        - Gateway routes to ai-agents (EXPEDITOR) for enrichment
        - NO direct ai-agents calls from external apps

        WBS Reference: AC-6.1.1 - enrich_metadata(corpus, chapter_index, config) method
        Architecture: External App -> Gateway:8080 -> ai-agents:8082

        Args:
            corpus: List of document/chapter text content.
            chapter_index: List of ChapterMeta with book, chapter, title, id.
            config: Optional MSEPConfig for enrichment parameters.

        Returns:
            EnrichedMetadataResponse with chapter metadata.

        Raises:
            MSEPTimeoutError: Request timed out.
            MSEPConnectionError: Unable to connect to Gateway.
            MSEPAPIError: API returned 4xx/5xx error.
            ValueError: corpus and chapter_index length mismatch.
        """
        # Validate input lengths match (required by ai-agents endpoint)
        if len(corpus) != len(chapter_index):
            raise ValueError(
                f"corpus length ({len(corpus)}) must match "
                f"chapter_index length ({len(chapter_index)})"
            )

        # Build tool arguments for Gateway /v1/tools/execute
        tool_arguments: dict[str, Any] = {
            "corpus": corpus,
            "chapter_index": [ch.to_dict() for ch in chapter_index],
        }

        # Add config if provided
        if config is not None:
            tool_arguments["config"] = config.to_dict()

        # Gateway tool execute format: {"name": "tool_name", "arguments": {...}}
        gateway_payload: dict[str, Any] = {
            "name": "enrich_metadata",
            "arguments": tool_arguments,
        }

        response_data = await self._post(
            _DEFAULT_ENRICH_ENDPOINT,
            json=gateway_payload,
        )

        # Gateway returns: {"name": "...", "result": {...}, "success": bool}
        # Extract the actual result from Gateway response
        if not response_data.get("success", False):
            error_msg = response_data.get("error", "Unknown Gateway error")
            raise MSEPAPIError(f"Gateway tool execution failed: {error_msg}", 500)

        result_data = response_data.get("result", {})
        return EnrichedMetadataResponse.from_dict(result_data)

    async def _post(
        self,
        endpoint: str,
        json: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute POST request with retry logic.

        Args:
            endpoint: API endpoint path.
            json: Request body as dict.

        Returns:
            Parsed JSON response.

        Raises:
            MSEPTimeoutError: Request timed out after retries.
            MSEPConnectionError: Unable to connect after retries.
            MSEPAPIError: API returned non-retryable error.
        """
        if self._client is None:
            raise MSEPClientError(_CLIENT_NOT_INITIALIZED_ERROR)

        last_exception: Optional[Exception] = None

        for attempt in range(self.max_retries + 1):
            try:
                response = await self._client.post(endpoint, json=json)
                response.raise_for_status()
                return response.json()  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                last_exception = e
                if attempt < self.max_retries:
                    await self._wait_before_retry(attempt)
                    continue
                raise MSEPTimeoutError(
                    f"Request to {endpoint} timed out after {self.max_retries + 1} attempts"
                ) from e

            except httpx.ConnectError as e:
                last_exception = e
                if attempt < self.max_retries:
                    await self._wait_before_retry(attempt)
                    continue
                raise MSEPConnectionError(
                    f"Connection to {self.base_url} failed after {self.max_retries + 1} attempts"
                ) from e

            except httpx.HTTPStatusError as e:
                status_code = e.response.status_code
                response_body = self._safe_parse_json(e.response)

                # Only retry on retryable status codes
                if status_code in self.RETRYABLE_STATUS_CODES:
                    last_exception = e
                    if attempt < self.max_retries:
                        await self._wait_before_retry(attempt)
                        continue

                # Don't retry 4xx client errors
                raise MSEPAPIError(
                    f"MSEP API error: {e.response.status_code}",
                    status_code=status_code,
                    response_body=response_body,
                ) from e

        # Should not reach here, but handle edge case
        raise MSEPClientError(
            f"Request failed after {self.max_retries + 1} attempts"
        ) from last_exception

    async def _wait_before_retry(self, attempt: int) -> None:
        """Wait with exponential backoff before retry.

        Args:
            attempt: Current attempt number (0-indexed).
        """
        delay = self.retry_delay * (2**attempt)
        await asyncio.sleep(delay)

    def _safe_parse_json(self, response: httpx.Response) -> Optional[dict[str, Any]]:
        """Safely parse JSON response body.

        Args:
            response: HTTP response object.

        Returns:
            Parsed JSON dict or None if parsing fails.
        """
        try:
            return response.json()  # type: ignore[no-any-return]
        except Exception:
            return None
