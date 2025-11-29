"""
Semantic Similarity Engine using Sentence Transformers.

This module provides semantic similarity computation for chapter content,
enabling intelligent cross-referencing and related content discovery.
It gracefully falls back to TF-IDF when Sentence Transformers is unavailable.

Architecture: Service Layer Pattern (Architecture Patterns Ch. 4)
Integration: Tab 4 (enrichment) -> computes similarities -> Tab 5 consumes
"""

from dataclasses import dataclass
from typing import Any, Optional

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


@dataclass
class SimilarityConfig:
    """Configuration for the SemanticSimilarityEngine.

    Attributes:
        model_name: Sentence Transformer model name (default: all-MiniLM-L6-v2)
        similarity_threshold: Minimum similarity score to consider chapters related
        top_k: Maximum number of similar chapters to return
        use_cache: Whether to cache embeddings for reuse
        fallback_to_tfidf: Whether to use TF-IDF when Sentence Transformers unavailable
    """

    model_name: str = "all-MiniLM-L6-v2"
    similarity_threshold: float = 0.0  # Default to 0 to include all matches
    top_k: int = 5
    use_cache: bool = True
    fallback_to_tfidf: bool = True


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

    Uses Sentence Transformers for high-quality semantic embeddings,
    with graceful fallback to TF-IDF when the library is unavailable.

    Example:
        >>> engine = SemanticSimilarityEngine()
        >>> corpus = ["Chapter 1 about Python", "Chapter 2 about decorators"]
        >>> embeddings = engine.compute_embeddings(corpus)
        >>> index = [{"book": "b.json", "chapter": 1, "title": "Ch1"}, ...]
        >>> similar = engine.find_similar(0, embeddings, index, top_k=2)
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        config: Optional[SimilarityConfig] = None,
    ) -> None:
        """Initialize the SemanticSimilarityEngine.

        Args:
            model_name: Name of the Sentence Transformer model to use.
            config: Configuration options. Uses defaults if not provided.
        """
        self.model_name = model_name
        self.config = config or SimilarityConfig(model_name=model_name)
        self._model: Optional[SentenceTransformer] = None  # type: ignore[assignment]
        self._vectorizer: Optional[TfidfVectorizer] = None
        self._embedding_cache: dict[str, NDArray[np.float64]] = {}
        self._using_fallback: bool = False

        # Initialize the appropriate model
        self._initialize_model()

    def _initialize_model(self) -> None:
        """Initialize the embedding model (Sentence Transformers or TF-IDF fallback)."""
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                self._model = SentenceTransformer(self.model_name)
                self._using_fallback = False
            except Exception:
                # Model loading failed, use fallback
                if self.config.fallback_to_tfidf:
                    self._setup_tfidf_fallback()
                else:
                    raise
        elif self.config.fallback_to_tfidf:
            self._setup_tfidf_fallback()
        else:
            raise ImportError(
                "sentence-transformers is not installed and fallback is disabled. "
                "Install with: pip install sentence-transformers"
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

    def compute_embeddings(
        self, corpus: list[str]
    ) -> NDArray[np.float64]:
        """Compute embeddings for a list of chapter texts.

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
        else:
            embeddings = self._compute_transformer_embeddings(corpus)

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

        # Determine method used
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
