"""Metadata Extraction Client - WBS-2.2.

Async HTTP client for Code-Orchestrator-Service metadata extraction endpoint.

AC Reference:
- AC-3.1: Protocol compliance (duck typing)
- AC-3.2: Connection pooling (httpx.AsyncClient reused)
- AC-3.3: Async context manager (__aenter__/__aexit__)
- AC-3.4: Retry logic with exponential backoff
- AC-3.5: Health check returns True/False (no raise)

Anti-Patterns Avoided:
- S1192: Constants extracted to module level
- Anti-Pattern #12: httpx.AsyncClient created once and reused
- Anti-Pattern #7/#13: Exception classes end in "Error"
"""

from __future__ import annotations

import asyncio
import hashlib
from dataclasses import dataclass, field
from typing import Any, Final, Protocol, runtime_checkable

import httpx


# =============================================================================
# Module Constants (S1192 compliance)
# =============================================================================

DEFAULT_BASE_URL: Final[str] = "http://localhost:8083"
DEFAULT_TIMEOUT: Final[float] = 30.0
DEFAULT_MAX_RETRIES: Final[int] = 3
DEFAULT_RETRY_BASE_DELAY: Final[float] = 0.5
ENDPOINT_EXTRACT: Final[str] = "/api/v1/metadata/extract"
ENDPOINT_HEALTH: Final[str] = "/api/v1/health"

# HTTP status codes that trigger retry (5xx server errors)
RETRYABLE_STATUS_CODES: Final[frozenset[int]] = frozenset({502, 503, 504})


# =============================================================================
# Custom Exceptions (Anti-Pattern #7/#13)
# =============================================================================


class MetadataClientError(Exception):
    """Base exception for metadata client errors."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class MetadataClientTimeoutError(MetadataClientError):
    """Raised when request times out."""

    pass


class MetadataClientConnectionError(MetadataClientError):
    """Raised when unable to connect to orchestrator service."""

    pass


class MetadataClientAPIError(MetadataClientError):
    """Raised when orchestrator returns an error response."""

    def __init__(
        self,
        message: str,
        status_code: int,
        response_body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, status_code)
        self.response_body = response_body


# =============================================================================
# Result Data Classes
# =============================================================================


@dataclass
class KeywordResult:
    """A single keyword extraction result."""

    term: str
    score: float
    is_technical: bool = False
    sources: list[str] = field(default_factory=list)


@dataclass
class ConceptResult:
    """A single concept extraction result."""

    name: str
    confidence: float
    domain: str
    tier: str


@dataclass
class ExtractionMetadata:
    """Metadata about the extraction process."""

    processing_time_ms: float
    text_length: int
    detected_domain: str | None = None
    domain_confidence: float | None = None
    quality_score: float = 0.0
    stages_completed: list[str] = field(default_factory=list)


@dataclass
class RejectedKeywords:
    """Keywords rejected during noise filtering."""

    keywords: list[str] = field(default_factory=list)
    reasons: dict[str, str] = field(default_factory=dict)


@dataclass
class MetadataExtractionResult:
    """Result of metadata extraction from orchestrator."""

    keywords: list[KeywordResult] = field(default_factory=list)
    concepts: list[ConceptResult] = field(default_factory=list)
    summary: str | None = None
    metadata: ExtractionMetadata | None = None
    rejected: RejectedKeywords | None = None


@dataclass
class MetadataExtractionOptions:
    """Options for metadata extraction request."""

    top_k_keywords: int = 15
    top_k_concepts: int = 10
    min_keyword_confidence: float = 0.3
    min_concept_confidence: float = 0.3
    enable_summary: bool = False
    summary_ratio: float = 0.2
    validate_dictionary: bool = True
    filter_noise: bool = True


# =============================================================================
# Protocol (AC-3.1)
# =============================================================================


@runtime_checkable
class MetadataExtractionClientProtocol(Protocol):
    """Protocol for metadata extraction - enables FakeClient testing.

    AC Reference:
        - AC-3.1: Protocol compliance via duck typing
    """

    async def extract_metadata(
        self,
        text: str,
        title: str | None = None,
        book_title: str | None = None,
        options: MetadataExtractionOptions | None = None,
    ) -> MetadataExtractionResult:
        """Extract metadata from text."""
        ...

    async def health_check(self) -> bool:
        """Check if orchestrator service is healthy."""
        ...


# =============================================================================
# MetadataExtractionClient (AC-3.2, AC-3.3, AC-3.4, AC-3.5)
# =============================================================================


class MetadataExtractionClient:
    """Production client using httpx.AsyncClient with connection pooling.

    AC Reference:
        - AC-3.2: Connection pooling (httpx.AsyncClient reused)
        - AC-3.3: Async context manager (__aenter__/__aexit__)
        - AC-3.4: Retry logic with exponential backoff
        - AC-3.5: Health check returns True/False (no raise)

    Anti-Patterns Avoided:
        - Anti-Pattern #12: Single httpx.AsyncClient reused
    """

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        """Initialize client.

        Args:
            base_url: Base URL of orchestrator service.
            timeout: Request timeout in seconds.
            max_retries: Max retries for failed requests.
        """
        self._base_url = base_url
        self._timeout = timeout
        self._max_retries = max_retries
        self._http_client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "MetadataExtractionClient":
        """Enter async context - create HTTP client."""
        self._http_client = httpx.AsyncClient(
            base_url=self._base_url,
            timeout=self._timeout,
        )
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        """Exit async context - close HTTP client."""
        if self._http_client:
            await self._http_client.aclose()
            self._http_client = None

    async def extract_metadata(
        self,
        text: str,
        title: str | None = None,
        book_title: str | None = None,
        options: MetadataExtractionOptions | None = None,
    ) -> MetadataExtractionResult:
        """Extract metadata from text via orchestrator.

        AC Reference:
            - AC-3.4: Retry logic with exponential backoff on 5xx errors

        Args:
            text: Text to extract metadata from.
            title: Optional chapter title.
            book_title: Optional book title.
            options: Extraction options.

        Returns:
            MetadataExtractionResult with keywords, concepts, etc.

        Raises:
            MetadataClientConnectionError: If cannot connect.
            MetadataClientTimeoutError: If request times out.
            MetadataClientAPIError: If API returns error after retries.
        """
        if self._http_client is None:
            raise MetadataClientError("Client not initialized. Use async context manager.")

        opts = options or MetadataExtractionOptions()
        payload = {
            "text": text,
            "title": title,
            "book_title": book_title,
            "options": {
                "top_k_keywords": opts.top_k_keywords,
                "top_k_concepts": opts.top_k_concepts,
                "min_keyword_confidence": opts.min_keyword_confidence,
                "min_concept_confidence": opts.min_concept_confidence,
                "enable_summary": opts.enable_summary,
                "summary_ratio": opts.summary_ratio,
                "validate_dictionary": opts.validate_dictionary,
                "filter_noise": opts.filter_noise,
            },
        }

        last_exception: httpx.HTTPStatusError | None = None

        for attempt in range(self._max_retries + 1):
            try:
                response = await self._http_client.post(ENDPOINT_EXTRACT, json=payload)
                response.raise_for_status()
                return self._parse_response(response.json())
            except httpx.ConnectError as e:
                raise MetadataClientConnectionError(str(e)) from e
            except httpx.TimeoutException as e:
                raise MetadataClientTimeoutError(str(e)) from e
            except httpx.HTTPStatusError as e:
                # Only retry on 5xx server errors (AC-3.4)
                if e.response.status_code in RETRYABLE_STATUS_CODES:
                    last_exception = e
                    if attempt < self._max_retries:
                        # Exponential backoff: 0.5s, 1s, 2s, ...
                        delay = DEFAULT_RETRY_BASE_DELAY * (2 ** attempt)
                        await asyncio.sleep(delay)
                        continue
                # Non-retryable error (4xx) or max retries exceeded
                raise MetadataClientAPIError(
                    str(e),
                    e.response.status_code,
                    e.response.json() if e.response.content else None,
                ) from e

        # Should only reach here if all retries exhausted
        if last_exception is not None:
            raise MetadataClientAPIError(
                str(last_exception),
                last_exception.response.status_code,
                last_exception.response.json() if last_exception.response.content else None,
            ) from last_exception

        # Fallback (should never reach)
        raise MetadataClientError("Unexpected error in extract_metadata")

    def _parse_response(self, data: dict[str, Any]) -> MetadataExtractionResult:
        """Parse API response to MetadataExtractionResult."""
        keywords = [
            KeywordResult(
                term=kw["term"],
                score=kw["score"],
                is_technical=kw.get("is_technical", False),
                sources=kw.get("sources", []),
            )
            for kw in data.get("keywords", [])
        ]

        concepts = [
            ConceptResult(
                name=c["name"],
                confidence=c["confidence"],
                domain=c["domain"],
                tier=c["tier"],
            )
            for c in data.get("concepts", [])
        ]

        metadata = None
        if "metadata" in data:
            m = data["metadata"]
            metadata = ExtractionMetadata(
                processing_time_ms=m.get("processing_time_ms", 0.0),
                text_length=m.get("text_length", 0),
                detected_domain=m.get("detected_domain"),
                domain_confidence=m.get("domain_confidence"),
                quality_score=m.get("quality_score", 0.0),
                stages_completed=m.get("stages_completed", []),
            )

        rejected = None
        if "rejected" in data:
            r = data["rejected"]
            rejected = RejectedKeywords(
                keywords=r.get("keywords", []),
                reasons=r.get("reasons", {}),
            )

        return MetadataExtractionResult(
            keywords=keywords,
            concepts=concepts,
            summary=data.get("summary"),
            metadata=metadata,
            rejected=rejected,
        )

    async def health_check(self) -> bool:
        """Check if orchestrator service is healthy.

        AC Reference:
            - AC-3.5: Returns True/False (no raise)

        Returns:
            True if service is healthy, False otherwise.
        """
        if self._http_client is None:
            return False

        try:
            response = await self._http_client.get(ENDPOINT_HEALTH)
            return response.status_code == 200
        except Exception:
            return False


# =============================================================================
# FakeMetadataExtractionClient (AC-4)
# =============================================================================


class FakeMetadataExtractionClient:
    """In-memory fake for unit testing.

    AC Reference:
        - AC-4.1: Protocol compliance
        - AC-4.2: Pre-configured responses
        - AC-4.3: Default empty response
        - AC-4.4: No network calls
    """

    def __init__(self) -> None:
        """Initialize fake client."""
        self._responses: dict[str, MetadataExtractionResult] = {}
        self._call_count = 0

    def set_response(
        self,
        text_hash: str,
        result: MetadataExtractionResult,
    ) -> None:
        """Pre-configure response for specific input.

        Args:
            text_hash: Hash of input text.
            result: Result to return for this input.
        """
        self._responses[text_hash] = result

    async def extract_metadata(
        self,
        text: str,
        title: str | None = None,
        book_title: str | None = None,
        options: MetadataExtractionOptions | None = None,
    ) -> MetadataExtractionResult:
        """Return pre-configured or default response.

        AC Reference:
            - AC-4.2: Pre-configured responses
            - AC-4.3: Default empty response
            - AC-4.4: No network calls
        """
        self._call_count += 1
        text_hash = hashlib.md5(text.encode()).hexdigest()

        if text_hash in self._responses:
            return self._responses[text_hash]

        # Default empty response (AC-4.3)
        return MetadataExtractionResult()

    async def health_check(self) -> bool:
        """Always returns True for fake client."""
        return True

    async def __aenter__(self) -> "FakeMetadataExtractionClient":
        """Enter async context (no-op for fake)."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        """Exit async context (no-op for fake)."""
        pass
