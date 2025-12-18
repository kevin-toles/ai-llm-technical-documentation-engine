"""
Semantic Similarity Engine - API-Only Implementation.

This module provides semantic similarity computation for chapter content
via the ai-agents MSEP API. NO local ML processing.

Architecture: Kitchen Brigade Pattern
- llm-document-enhancer is CUSTOMER only
- Delegates embeddings/similarity to ai-agents via SBERT/MSEP API
- NO local sentence-transformers, NO local TF-IDF vectorization

WBS MSE-6.4: Remove Local TF-IDF
- Removed: Local TF-IDF vectorization (sklearn feature extraction)
- Removed: Local sentence-transformers model loading
- Removed: _compute_tfidf_embeddings(), _try_local_sbert()
- Removed: fallback_to_tfidf, fallback_to_local config options

Reference Documents:
- MULTI_STAGE_ENRICHMENT_PIPELINE_ARCHITECTURE.md: Kitchen Brigade
- CODING_PATTERNS_ANALYSIS: #7 Exception naming, #12 Connection pooling
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Optional

import numpy as np
from numpy.typing import NDArray
from sklearn.metrics.pairwise import cosine_similarity  # type: ignore[import-untyped]

# Type checking imports for SBERTClient
if TYPE_CHECKING:
    from workflows.shared.clients.sbert_client import SBERTClientProtocol

# =============================================================================
# Module Constants - SonarQube S1192
# =============================================================================

_DEFAULT_SBERT_API_URL = "http://localhost:8083"
_DEFAULT_SBERT_API_TIMEOUT = 30.0

# Logger for API warnings
_logger = logging.getLogger(__name__)


@dataclass
class SimilarityConfig:
    """Configuration for the SemanticSimilarityEngine.

    WBS MSE-6.4: API-only configuration (removed local ML options).

    Attributes:
        model_name: Model name for API requests (default: all-MiniLM-L6-v2)
        similarity_threshold: Minimum similarity score to consider chapters related
        top_k: Maximum number of similar chapters to return
        use_cache: Whether to cache embeddings for reuse
        sbert_api_url: Code-Orchestrator SBERT API URL
        sbert_api_timeout: API request timeout in seconds
    """

    model_name: str = "all-MiniLM-L6-v2"
    similarity_threshold: float = 0.0  # Default to 0 to include all matches
    top_k: int = 5
    use_cache: bool = True
    # API Configuration - only supported mode per Kitchen Brigade
    sbert_api_url: str = field(
        default_factory=lambda: _DEFAULT_SBERT_API_URL
    )
    sbert_api_timeout: float = field(
        default_factory=lambda: float(_DEFAULT_SBERT_API_TIMEOUT)
    )


@dataclass
class SimilarityResult:
    """Result of a similarity computation between chapters.

    Attributes:
        book: Source book filename
        chapter: Chapter number
        title: Chapter title
        score: Cosine similarity score (0.0 to 1.0)
        method: Method used for similarity (always 'api' per Kitchen Brigade)
    """

    book: str
    chapter: int
    title: str
    score: float
    method: str = "api"


class SemanticSimilarityEngine:
    """Engine for computing semantic similarity between chapter contents.

    WBS MSE-6.4: API-Only Implementation (Kitchen Brigade Pattern)
    - Delegates ALL embedding computation to ai-agents via SBERT API
    - NO local sentence-transformers
    - NO local TF-IDF fallback

    Example with API client:
        >>> from workflows.shared.clients.sbert_client import SBERTClient
        >>> config = SimilarityConfig()
        >>> async with SBERTClient() as client:
        ...     engine = SemanticSimilarityEngine(config=config, sbert_client=client)
        ...     embeddings = await engine.compute_embeddings_async(corpus)
        ...     similar = engine.find_similar(0, embeddings, index)
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        config: Optional[SimilarityConfig] = None,
        sbert_client: Optional["SBERTClientProtocol"] = None,
    ) -> None:
        """Initialize the SemanticSimilarityEngine.

        Args:
            model_name: Name of the model to use for API requests.
            config: Configuration options. Uses defaults if not provided.
            sbert_client: Required SBERTClient for API mode (Kitchen Brigade).

        Raises:
            ValueError: If sbert_client is not provided (API-only mode).
        """
        self.model_name = model_name
        self.config = config or SimilarityConfig(model_name=model_name)
        self._embedding_cache: dict[str, NDArray[np.float64]] = {}

        # API Client - required per Kitchen Brigade
        self._sbert_client = sbert_client
        self._last_method: str = "api"  # Always API per Kitchen Brigade
        self._logger = _logger

        if self._sbert_client is None:
            self._logger.warning(
                "No SBERT client provided. API calls will fail. "
                "Use async context manager with SBERTClient for embeddings."
            )

    # =========================================================================
    # Async API Methods - WBS MSE-6.4 (API-Only)
    # =========================================================================

    async def compute_embeddings_async(
        self, corpus: list[str]
    ) -> NDArray[np.float64]:
        """Compute embeddings asynchronously via SBERT API.

        WBS MSE-6.4: API-only implementation (Kitchen Brigade Pattern).
        Delegates to ai-agents SBERT API - NO local ML processing.

        Args:
            corpus: List of chapter text strings.

        Returns:
            2D numpy array of shape (n_chapters, embedding_dim) with embeddings.
            Returns empty array if corpus is empty.

        Raises:
            RuntimeError: If API client not available or API call fails.
        """
        if not corpus:
            return np.array([], dtype=np.float64)

        # Check cache if enabled
        if self.config.use_cache:
            cache_key = self._compute_cache_key(corpus)
            if cache_key in self._embedding_cache:
                return self._embedding_cache[cache_key]

        # API-only: No fallback per Kitchen Brigade
        embeddings = await self._compute_api_embeddings(corpus)

        if embeddings is None:
            raise RuntimeError(
                "SBERT API call failed. Ensure ai-agents service is running. "
                "Kitchen Brigade: llm-document-enhancer is CUSTOMER only - "
                "no local ML fallback."
            )

        # Cache if enabled
        if self.config.use_cache:
            cache_key = self._compute_cache_key(corpus)
            self._embedding_cache[cache_key] = embeddings

        return embeddings

    async def _compute_api_embeddings(
        self, corpus: list[str]
    ) -> Optional[NDArray[np.float64]]:
        """Compute embeddings via Code-Orchestrator SBERT API.

        Args:
            corpus: List of texts to embed.

        Returns:
            Embedding array or None if API call fails.
        """
        # Import here to avoid circular dependency
        from workflows.shared.clients.sbert_client import (
            SBERTClientError,
            SBERTConnectionError,
            SBERTTimeoutError,
        )

        if self._sbert_client is None:
            self._logger.error(
                "No SBERT client configured. Cannot compute embeddings."
            )
            return None

        try:
            embeddings_list = await self._sbert_client.get_embeddings(corpus)
            self._last_method = "api"
            return np.array(embeddings_list, dtype=np.float64)

        except (SBERTConnectionError, SBERTTimeoutError) as e:
            self._logger.error(
                f"SBERT API unavailable ({type(e).__name__}): {e}. "
                "Kitchen Brigade: No local fallback - ai-agents service required."
            )
            return None
        except SBERTClientError as e:
            self._logger.error(
                f"SBERT API error: {e}. "
                "Kitchen Brigade: No local fallback - ai-agents service required."
            )
            return None

    def _compute_cache_key(self, texts: list[str]) -> str:
        """Compute a cache key for a list of texts.

        Args:
            texts: List of text strings.

        Returns:
            Hash-based cache key.
        """
        import hashlib

        combined = "|||".join(texts)
        return hashlib.md5(combined.encode()).hexdigest()

    def compute_similarity_matrix(
        self, embeddings: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Compute pairwise cosine similarity matrix for embeddings.

        Note: Uses sklearn.metrics.pairwise.cosine_similarity for matrix math.
        This is NOT ML processing - just matrix operations on API-provided embeddings.

        Args:
            embeddings: 2D numpy array of shape (n_chapters, embedding_dim).

        Returns:
            2D numpy array of shape (n_chapters, n_chapters) with similarity scores.
            Diagonal elements are 1.0 (self-similarity).
            All values are clipped to [-1.0, 1.0] range.

        Raises:
            ValueError: If embeddings array is empty.
        """
        if embeddings.size == 0:
            raise ValueError("Cannot compute similarity matrix for empty embeddings")

        # Handle 1D case (single embedding)
        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)

        # Compute cosine similarity
        similarity_matrix = cosine_similarity(embeddings)

        # Clip to valid range to handle floating-point precision issues
        similarity_matrix = np.clip(similarity_matrix, -1.0, 1.0)

        return np.array(similarity_matrix, dtype=np.float64)

    def find_similar(
        self,
        query_idx: int,
        embeddings: NDArray[np.float64],
        index: list[dict[str, Any]],
        top_k: Optional[int] = None,
        threshold: Optional[float] = None,
    ) -> list[SimilarityResult]:
        """Find the most similar chapters to a given chapter.

        Args:
            query_idx: Index of the source chapter in embeddings.
            embeddings: Pre-computed embeddings array.
            index: List of chapter info dicts with 'book', 'chapter', 'title' keys.
            top_k: Number of similar chapters to return. Uses config default if None.
            threshold: Minimum similarity score. Uses config default if None.

        Returns:
            List of SimilarityResult objects, sorted by similarity (descending).

        Raises:
            ValueError: If query_idx is out of bounds.
        """
        if len(embeddings) == 0 or len(index) == 0:
            return []

        if query_idx < 0 or query_idx >= len(embeddings):
            raise ValueError(
                f"query_idx {query_idx} out of bounds for {len(embeddings)} chapters"
            )

        # Use config defaults if not specified
        k = top_k if top_k is not None else self.config.top_k
        min_threshold = threshold if threshold is not None else self.config.similarity_threshold

        # Compute similarity matrix
        similarity_matrix = self.compute_similarity_matrix(embeddings)

        # Get similarities for the target chapter
        similarities = similarity_matrix[query_idx]

        # Always API method per Kitchen Brigade
        method = self._last_method or "api"

        # Find top-k similar chapters (excluding self)
        results: list[SimilarityResult] = []
        for idx, score in enumerate(similarities):
            if idx == query_idx:
                continue  # Skip self

            if score >= min_threshold:
                chapter_info = index[idx]
                results.append(
                    SimilarityResult(
                        book=chapter_info.get("book", ""),
                        chapter=chapter_info.get("chapter", idx + 1),
                        title=chapter_info.get("title", f"Chapter {idx + 1}"),
                        score=float(score),
                        method=method,
                    )
                )

        # Sort by similarity score (descending) and limit to top_k
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:k]

    def clear_cache(self) -> None:
        """Clear the embedding cache."""
        self._embedding_cache.clear()
