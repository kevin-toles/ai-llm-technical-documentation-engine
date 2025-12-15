"""
Semantic Similarity Engine using Sentence Transformers.

This module provides semantic similarity computation for chapter content,
enabling intelligent cross-referencing and related content discovery.

Architecture: Service Layer Pattern (Architecture Patterns Ch. 4)
Integration: Tab 4 (enrichment) -> computes similarities -> Tab 5 consumes

WBS M3.2: Three-tier fallback strategy:
    1. API (Code-Orchestrator SBERT API) - primary path
    2. Local SBERT (sentence-transformers) - first fallback
    3. TF-IDF - final fallback for offline scenarios

Reference Documents:
- SBERT_EXTRACTION_MIGRATION_WBS.md: M3.2 SemanticSimilarityEngine Refactor
- CODING_PATTERNS_ANALYSIS: #7 Exception naming, #12 Connection pooling
"""

from __future__ import annotations

import logging
import os
import warnings
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Optional

import numpy as np
from numpy.typing import NDArray

# Try to import sentence-transformers, fall back to TF-IDF if unavailable
try:
    from sentence_transformers import SentenceTransformer

    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    SentenceTransformer = None  # type: ignore[misc, assignment]

# TF-IDF fallback imports
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Type checking imports for SBERTClient
if TYPE_CHECKING:
    from workflows.shared.clients.sbert_client import SBERTClientProtocol

# =============================================================================
# Module Constants - SonarQube S1192
# =============================================================================

_DEFAULT_SBERT_API_URL = "http://localhost:8083"
_DEFAULT_SBERT_API_TIMEOUT = 30.0

# Logger for fallback warnings
_logger = logging.getLogger(__name__)


@dataclass
class SimilarityConfig:
    """Configuration for the SemanticSimilarityEngine.

    WBS M3.2: Extended for three-tier fallback (API → Local SBERT → TF-IDF).

    Attributes:
        model_name: Sentence Transformer model name (default: all-MiniLM-L6-v2)
        similarity_threshold: Minimum similarity score to consider chapters related
        top_k: Maximum number of similar chapters to return
        use_cache: Whether to cache embeddings for reuse
        fallback_to_tfidf: Whether to use TF-IDF when Sentence Transformers unavailable
        use_api: Whether to use Code-Orchestrator SBERT API (M3.2.1)
        sbert_api_url: Code-Orchestrator SBERT API URL (M3.3)
        sbert_api_timeout: API request timeout in seconds (M3.3)
        fallback_to_local: Fallback to local SBERT when API unavailable (M3.2.3)
        fallback_mode: Primary computation mode (api, local, tfidf) (M3.2.6)
    """

    model_name: str = "all-MiniLM-L6-v2"
    similarity_threshold: float = 0.0  # Default to 0 to include all matches
    top_k: int = 5
    use_cache: bool = True
    fallback_to_tfidf: bool = True
    # M3.2 API Client Configuration
    use_api: bool = field(
        default_factory=lambda: os.getenv("SBERT_FALLBACK_MODE", "local") == "api"
    )
    sbert_api_url: str = field(
        default_factory=lambda: os.getenv("SBERT_API_URL", _DEFAULT_SBERT_API_URL)
    )
    sbert_api_timeout: float = field(
        default_factory=lambda: float(
            os.getenv("SBERT_API_TIMEOUT", str(_DEFAULT_SBERT_API_TIMEOUT))
        )
    )
    fallback_to_local: bool = True
    fallback_mode: str = field(
        default_factory=lambda: os.getenv("SBERT_FALLBACK_MODE", "local")
    )


@dataclass
class SimilarityResult:
    """Result of a similarity computation between chapters.

    Attributes:
        book: Source book filename
        chapter: Chapter number
        title: Chapter title
        score: Cosine similarity score (0.0 to 1.0)
        method: Method used for similarity (sentence_transformers or tfidf)
    """

    book: str
    chapter: int
    title: str
    score: float
    method: str = "sentence_transformers"


class SemanticSimilarityEngine:
    """Engine for computing semantic similarity between chapter contents.

    WBS M3.2: Three-tier fallback strategy:
        1. API (Code-Orchestrator SBERT API) - primary path when use_api=True
        2. Local SBERT (sentence-transformers) - fallback when API unavailable
        3. TF-IDF - final fallback for offline scenarios

    Uses Sentence Transformers for high-quality semantic embeddings,
    with graceful fallback to TF-IDF when the library is unavailable.

    Example:
        >>> engine = SemanticSimilarityEngine()
        >>> corpus = ["Chapter 1 about Python", "Chapter 2 about decorators"]
        >>> embeddings = engine.compute_embeddings(corpus)
        >>> index = [{"book": "b.json", "chapter": 1, "title": "Ch1"}, ...]
        >>> similar = engine.find_similar(0, embeddings, index, top_k=2)

    Example with API client (M3.2):
        >>> from workflows.shared.clients.sbert_client import SBERTClient
        >>> config = SimilarityConfig(use_api=True)
        >>> async with SBERTClient() as client:
        ...     engine = SemanticSimilarityEngine(config=config, sbert_client=client)
        ...     embeddings = await engine.compute_embeddings_async(corpus)
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        config: Optional[SimilarityConfig] = None,
        sbert_client: Optional["SBERTClientProtocol"] = None,
    ) -> None:
        """Initialize the SemanticSimilarityEngine.

        Args:
            model_name: Name of the Sentence Transformer model to use.
            config: Configuration options. Uses defaults if not provided.
            sbert_client: Optional SBERTClient for API mode (M3.2.1).
        """
        self.model_name = model_name
        self.config = config or SimilarityConfig(model_name=model_name)
        self._model: Optional[SentenceTransformer] = None  # type: ignore[assignment]
        self._vectorizer: Optional[TfidfVectorizer] = None
        self._embedding_cache: dict[str, NDArray[np.float64]] = {}
        self._using_fallback: bool = False

        # M3.2: API Client and fallback tracking
        self._sbert_client = sbert_client
        self._use_api: bool = self.config.use_api
        self._fallback_mode: str = self.config.fallback_mode
        self._last_method: str = ""  # Track which method was used
        self._logger = _logger

        # Initialize the appropriate model based on fallback_mode
        self._initialize_model()

    def _initialize_model(self) -> None:
        """Initialize embedding model based on fallback_mode.

        WBS M3.2: Three-tier fallback initialization:
            - mode="api": No local model needed (API handles it)
            - mode="local": Initialize SentenceTransformer
            - mode="tfidf": Initialize TF-IDF vectorizer

        Falls back through the chain if initialization fails.
        """
        mode = self._fallback_mode

        # Mode: API - Skip local model initialization (API will handle it)
        if mode == "api" and self._use_api:
            self._logger.info("Using API mode - deferring to Code-Orchestrator SBERT API")
            # Still set up TF-IDF as emergency fallback
            if self.config.fallback_to_tfidf:
                self._setup_tfidf_fallback()
            return

        # Mode: Local or fallback from API
        if mode in ("local", "api"):
            if SENTENCE_TRANSFORMERS_AVAILABLE:
                try:
                    # M3.2.7: Deprecation warning for local SBERT
                    if mode == "local":
                        warnings.warn(
                            "Local SBERT is deprecated. Consider using API mode "
                            "(SBERT_FALLBACK_MODE=api) for better resource utilization.",
                            DeprecationWarning,
                            stacklevel=2,
                        )
                    self._model = SentenceTransformer(self.model_name)
                    self._using_fallback = False
                    return
                except Exception as e:
                    self._logger.warning(f"Local SBERT init failed: {e}")
                    if not self.config.fallback_to_tfidf:
                        raise

            # Local SBERT not available, fall through to TF-IDF
            if not self.config.fallback_to_tfidf:
                raise ImportError(
                    "sentence-transformers is not installed and fallback is disabled. "
                    "Install with: pip install sentence-transformers"
                )

        # Mode: TF-IDF (or fallback from local)
        if self.config.fallback_to_tfidf:
            self._setup_tfidf_fallback()
        else:
            raise ImportError(
                "No embedding method available. Enable fallback_to_tfidf or install "
                "sentence-transformers."
            )

    def _setup_tfidf_fallback(self) -> None:
        """Set up TF-IDF vectorizer as fallback."""
        self._vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words="english",
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95,
        )
        self._using_fallback = True

    @property
    def is_using_fallback(self) -> bool:
        """Check if the engine is using TF-IDF fallback instead of Sentence Transformers."""
        return self._using_fallback

    # =========================================================================
    # Async API Methods - WBS M3.2
    # Pattern: Three-tier fallback (API → Local SBERT → TF-IDF)
    # =========================================================================

    async def compute_embeddings_async(
        self, corpus: list[str]
    ) -> NDArray[np.float64]:
        """Compute embeddings asynchronously with three-tier fallback.

        WBS M3.2: Three-tier fallback strategy:
            1. API (Code-Orchestrator SBERT API) - if use_api=True
            2. Local SBERT - if API fails and fallback_to_local=True
            3. TF-IDF - if both fail and fallback_to_tfidf=True

        Args:
            corpus: List of chapter text strings.

        Returns:
            2D numpy array of shape (n_chapters, embedding_dim) with embeddings.
            Returns empty array if corpus is empty.

        Raises:
            RuntimeError: If all fallback methods fail.
        """
        if not corpus:
            return np.array([], dtype=np.float64)

        # Check cache if enabled
        if self.config.use_cache:
            cache_key = self._compute_cache_key(corpus)
            if cache_key in self._embedding_cache:
                return self._embedding_cache[cache_key]

        embeddings: Optional[NDArray[np.float64]] = None

        # Tier 1: Try API if enabled
        if self._use_api and self._sbert_client is not None:
            embeddings = await self._compute_api_embeddings(corpus)

        # Tier 2: Fallback to local SBERT
        if embeddings is None and self.config.fallback_to_local:
            embeddings = self._try_local_sbert(corpus)

        # Tier 3: Fallback to TF-IDF
        if embeddings is None and self.config.fallback_to_tfidf:
            embeddings = self._compute_tfidf_embeddings(corpus)
            self._last_method = "tfidf"

        if embeddings is None:
            raise RuntimeError("All embedding methods failed")

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

        try:
            if self._sbert_client is None:
                return None

            embeddings_list = await self._sbert_client.get_embeddings(corpus)
            self._last_method = "api"
            return np.array(embeddings_list, dtype=np.float64)

        except (SBERTConnectionError, SBERTTimeoutError) as e:
            self._logger.warning(
                f"SBERT API unavailable ({type(e).__name__}): {e}. "
                f"Falling back to local SBERT."
            )
            return None
        except SBERTClientError as e:
            self._logger.warning(f"SBERT API error: {e}. Falling back to local SBERT.")
            return None

    def _try_local_sbert(self, corpus: list[str]) -> Optional[NDArray[np.float64]]:
        """Try computing embeddings with local SBERT.

        Args:
            corpus: List of texts to embed.

        Returns:
            Embedding array or None if local SBERT unavailable.
        """
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            self._logger.warning(
                "Local SBERT unavailable (sentence-transformers not installed). "
                "Falling back to TF-IDF."
            )
            return None

        if self._model is None:
            # Try to initialize model
            try:
                self._model = SentenceTransformer(self.model_name)
            except Exception as e:
                self._logger.warning(f"Failed to initialize local SBERT: {e}")
                return None

        try:
            embeddings = self._compute_transformer_embeddings(corpus)
            self._last_method = "local_sbert"
            return embeddings
        except Exception as e:
            self._logger.warning(f"Local SBERT embedding failed: {e}")
            return None

    def compute_embeddings(
        self, corpus: list[str]
    ) -> NDArray[np.float64]:
        """Compute embeddings for a list of chapter texts (synchronous).

        Note: For API mode, use compute_embeddings_async() instead.

        Args:
            corpus: List of chapter text strings.

        Returns:
            2D numpy array of shape (n_chapters, embedding_dim) with embeddings.
            Returns empty array if corpus is empty.
        """
        if not corpus:
            return np.array([], dtype=np.float64)

        # Check cache if enabled
        if self.config.use_cache:
            cache_key = self._compute_cache_key(corpus)
            if cache_key in self._embedding_cache:
                return self._embedding_cache[cache_key]

        # Compute embeddings
        if self._using_fallback:
            embeddings = self._compute_tfidf_embeddings(corpus)
            self._last_method = "tfidf"
        else:
            embeddings = self._compute_transformer_embeddings(corpus)
            self._last_method = "local_sbert"

        # Cache if enabled
        if self.config.use_cache:
            cache_key = self._compute_cache_key(corpus)
            self._embedding_cache[cache_key] = embeddings

        return embeddings

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

    def _compute_transformer_embeddings(
        self, texts: list[str]
    ) -> NDArray[np.float64]:
        """Compute embeddings using Sentence Transformers.

        Args:
            texts: List of text strings.

        Returns:
            Embedding matrix as numpy array.
        """
        if self._model is None:
            raise RuntimeError("Sentence Transformer model not initialized")

        embeddings = self._model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return np.array(embeddings, dtype=np.float64)

    def _compute_tfidf_embeddings(self, texts: list[str]) -> NDArray[np.float64]:
        """Compute embeddings using TF-IDF vectorization.

        Args:
            texts: List of text strings.

        Returns:
            TF-IDF matrix as numpy array.
        """
        if self._vectorizer is None:
            raise RuntimeError("TF-IDF vectorizer not initialized")

        # Handle empty texts
        if all(not t.strip() for t in texts):
            # Return zero embeddings for empty texts
            return np.zeros((len(texts), 1), dtype=np.float64)

        # Fit and transform
        tfidf_matrix = self._vectorizer.fit_transform(texts)
        return np.array(tfidf_matrix.toarray(), dtype=np.float64)

    def compute_similarity_matrix(
        self, embeddings: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Compute pairwise cosine similarity matrix for embeddings.

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

        # Determine method used - prefer _last_method (set by compute_embeddings_async)
        # Fall back to checking _using_fallback for synchronous compute_embeddings
        if self._last_method:
            method = self._last_method
        else:
            method = "tfidf" if self._using_fallback else "sentence_transformers"

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
