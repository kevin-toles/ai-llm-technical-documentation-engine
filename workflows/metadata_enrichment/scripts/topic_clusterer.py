#!/usr/bin/env python3
"""
TopicClusterer - BERTopic-based Topic Clustering for Chapters.

Reference: BERTOPIC_SENTENCE_TRANSFORMERS_DESIGN.md - Option C Architecture
Pattern: Service Layer Pattern (Architecture Patterns Ch. 4)
Fallback: Returns topic_id=-1 when BERTopic unavailable

This module provides semantic topic clustering for chapters using BERTopic.
It groups chapters by semantic similarity into topics, enabling enhanced
cross-referencing in Tab 5 based on topic membership.

Dependencies:
    - bertopic>=0.16.0 (optional, falls back gracefully)
    - sentence-transformers>=2.2.2 (optional, falls back gracefully)
    - hdbscan>=0.8.29 (required by BERTopic)
    - umap-learn>=0.5.3 (required by BERTopic)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check if BERTopic is available
try:
    from bertopic import BERTopic  # type: ignore[import-untyped]
    from sentence_transformers import SentenceTransformer  # type: ignore[import-untyped]
    BERTOPIC_AVAILABLE = True
    logger.info("BERTopic and SentenceTransformers available")
except ImportError as e:
    BERTOPIC_AVAILABLE = False
    logger.warning(f"BERTopic/SentenceTransformers not available: {e}. Using fallback mode.")


@dataclass
class TopicInfo:
    """
    Information about a chapter's topic assignment.
    
    Pattern: Value Object (Architecture Patterns Ch. 1)
    Immutable data structure representing topic assignment.
    
    Attributes:
        topic_id: Integer topic ID (-1 for outliers/no topic)
        topic_name: Human-readable topic name
        confidence: Probability that chapter belongs to this topic (0.0-1.0)
    """
    topic_id: int
    topic_name: str
    confidence: float


@dataclass
class TopicResults:
    """
    Results from topic clustering operation.
    
    Pattern: Data Transfer Object (Architecture Patterns Ch. 4)
    Carries clustering results between layers.
    
    Attributes:
        topic_assignments: List of topic IDs for each chapter (index-aligned)
        topics: List of topic metadata dicts (keywords, representative chapters)
        topic_count: Total number of discovered topics
    """
    topic_assignments: List[int] = field(default_factory=list)
    topics: List[Dict[str, Any]] = field(default_factory=list)
    topic_count: int = 0


class TopicClusterer:
    """
    BERTopic-based topic clustering for chapters.
    
    Pattern: Service Layer Pattern (Architecture Patterns Ch. 4)
    Provides topic clustering as a domain service.
    
    Handles topic discovery and assignment using BERTopic when available,
    with graceful fallback to no-topic assignment when dependencies missing.
    
    Example:
        >>> clusterer = TopicClusterer()
        >>> corpus = ["Chapter about decorators...", "Chapter about testing..."]
        >>> index = [{"book": "book.json", "chapter": 1, "title": "Ch 1"}, ...]
        >>> results = clusterer.cluster_chapters(corpus, index)
        >>> topic_info = clusterer.get_topic_for_chapter(0)
        >>> print(f"Topic: {topic_info.topic_name}, Confidence: {topic_info.confidence}")
    """
    
    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize TopicClusterer.
        
        Args:
            embedding_model: Name of sentence-transformers model to use.
                            Default: all-MiniLM-L6-v2 (~80MB, fast inference)
        """
        self.embedding_model = embedding_model
        self._model: Optional[Any] = None
        self._topic_info: List[TopicInfo] = []
        self._results: Optional[TopicResults] = None
        self._is_fitted = False
    
    def _initialize_model(self) -> None:
        """
        Lazy-load the BERTopic model.
        
        Pattern: Lazy Initialization (Python Distilled Ch. 7)
        Defers expensive model loading until first use.
        """
        if self._model is not None:
            return
        
        if not BERTOPIC_AVAILABLE:
            logger.warning("BERTopic not available, using fallback mode")
            return
        
        try:
            # Initialize SentenceTransformer for embeddings
            embedding_model = SentenceTransformer(self.embedding_model)
            
            # Initialize BERTopic with the embedding model
            self._model = BERTopic(
                embedding_model=embedding_model,
                verbose=False,
                calculate_probabilities=True,
                min_topic_size=2  # Allow small topics for small corpora
            )
            logger.info(f"BERTopic initialized with model: {self.embedding_model}")
        except Exception as e:
            logger.error(f"Failed to initialize BERTopic: {e}")
            self._model = None
    
    def cluster_chapters(
        self,
        corpus: List[str],
        index: List[Dict[str, Any]]
    ) -> TopicResults:
        """
        Cluster chapters into topics based on semantic similarity.
        
        Args:
            corpus: List of chapter text content
            index: List of chapter metadata dicts with keys:
                   - book: Book filename
                   - chapter: Chapter number
                   - title: Chapter title
        
        Returns:
            TopicResults with topic assignments and topic metadata
        
        Example:
            >>> clusterer = TopicClusterer()
            >>> results = clusterer.cluster_chapters(
            ...     ["Decorators in Python...", "Repository pattern..."],
            ...     [{"book": "book.json", "chapter": 1, "title": "Ch 1"}, ...]
            ... )
            >>> print(f"Found {results.topic_count} topics")
        """
        # Handle empty corpus
        if not corpus:
            self._results = TopicResults(
                topic_assignments=[],
                topics=[],
                topic_count=0
            )
            self._topic_info = []
            self._is_fitted = True
            return self._results
        
        # Initialize model if needed
        self._initialize_model()
        
        # Use fallback if BERTopic not available
        if self._model is None:
            return self._fallback_clustering(corpus, index)
        
        try:
            # Fit BERTopic model
            topics, probs = self._model.fit_transform(corpus)
            
            # Build topic metadata
            topic_info_dict = self._model.get_topic_info()
            topics_list = self._build_topics_list(topic_info_dict, index, topics)
            
            # Build TopicInfo for each chapter
            self._topic_info = []
            for idx, (topic_id, prob_dist) in enumerate(zip(topics, probs)):
                topic_name = self._get_topic_name(topic_id)
                # Get confidence for assigned topic
                if topic_id >= 0 and prob_dist is not None:
                    confidence = float(prob_dist[topic_id]) if topic_id < len(prob_dist) else 0.5
                else:
                    confidence = 0.0 if topic_id == -1 else 0.5
                
                self._topic_info.append(TopicInfo(
                    topic_id=int(topic_id),
                    topic_name=topic_name,
                    confidence=min(1.0, max(0.0, confidence))  # Clamp to [0, 1]
                ))
            
            self._results = TopicResults(
                topic_assignments=[int(t) for t in topics],
                topics=topics_list,
                topic_count=len(topics_list)
            )
            self._is_fitted = True
            
            logger.info(f"Clustered {len(corpus)} chapters into {self._results.topic_count} topics")
            return self._results
            
        except Exception as e:
            logger.error(f"BERTopic clustering failed: {e}")
            return self._fallback_clustering(corpus, index)
    
    def _fallback_clustering(
        self,
        corpus: List[str],
        _index: List[Dict[str, Any]]
    ) -> TopicResults:
        """
        Fallback clustering when BERTopic unavailable.
        
        Assigns all chapters to topic_id=-1 (no topic).
        
        Args:
            corpus: List of chapter text content
            _index: List of chapter metadata (unused in fallback)
        
        Returns:
            TopicResults with all chapters assigned to topic -1
        """
        logger.info("Using fallback clustering (no BERTopic)")
        
        # Assign all to outlier topic
        self._topic_info = [
            TopicInfo(topic_id=-1, topic_name="Uncategorized", confidence=0.0)
            for _ in corpus
        ]
        
        self._results = TopicResults(
            topic_assignments=[-1] * len(corpus),
            topics=[],
            topic_count=0
        )
        self._is_fitted = True
        
        return self._results
    
    def _build_topics_list(
        self,
        _topic_info_dict: Any,
        index: List[Dict[str, Any]],
        topic_assignments: List[int]
    ) -> List[Dict[str, Any]]:
        """
        Build topic metadata list from BERTopic results.
        
        Args:
            _topic_info_dict: DataFrame from BERTopic.get_topic_info() (unused - reserved for future)
            index: Chapter metadata
            topic_assignments: Topic ID for each chapter
        
        Returns:
            List of topic dicts with keywords and representative chapters
        """
        topics_list = []
        
        # Get unique topic IDs (excluding -1 outliers)
        unique_topics = {t for t in topic_assignments if t >= 0}
        
        for topic_id in sorted(unique_topics):
            try:
                # Get topic keywords from BERTopic
                # Type guard for _model being set
                if self._model is None:
                    continue
                topic_words = self._model.get_topic(topic_id)
                keywords = [word for word, _ in topic_words[:10]] if topic_words else []
                
                # Get representative chapters for this topic
                rep_chapters = []
                for idx, t in enumerate(topic_assignments):
                    if t == topic_id and idx < len(index):
                        rep_chapters.append({
                            "book": index[idx].get("book", "unknown.json"),
                            "chapter": index[idx].get("chapter", idx),
                            "title": index[idx].get("title", f"Chapter {idx}")
                        })
                
                # Get topic name (first few keywords)
                topic_name = self._get_topic_name(topic_id)
                
                topics_list.append({
                    "topic_id": int(topic_id),
                    "name": topic_name,
                    "keywords": keywords,
                    "representative_chapters": rep_chapters[:5]  # Limit to 5
                })
            except Exception as e:
                logger.warning(f"Error building topic {topic_id} metadata: {e}")
        
        return topics_list
    
    def _get_topic_name(self, topic_id: int) -> str:
        """
        Get human-readable name for a topic.
        
        Args:
            topic_id: Topic ID
        
        Returns:
            Topic name string
        """
        if topic_id == -1:
            return "Uncategorized"
        
        if self._model is None:
            return f"Topic {topic_id}"
        
        try:
            topic_words = self._model.get_topic(topic_id)
            if topic_words:
                # Use top 3 keywords as topic name
                top_words = [word for word, _ in topic_words[:3]]
                return "_".join(top_words)
            return f"Topic {topic_id}"
        except Exception:
            return f"Topic {topic_id}"
    
    def get_topic_for_chapter(self, chapter_idx: int) -> TopicInfo:
        """
        Get topic information for a specific chapter.
        
        Args:
            chapter_idx: Index of chapter in corpus (0-based)
        
        Returns:
            TopicInfo with topic_id, topic_name, and confidence
        
        Raises:
            ValueError: If cluster_chapters() not called yet
            IndexError: If chapter_idx out of range
        
        Example:
            >>> clusterer = TopicClusterer()
            >>> clusterer.cluster_chapters(corpus, index)
            >>> topic = clusterer.get_topic_for_chapter(0)
            >>> print(f"Topic: {topic.topic_name}")
        """
        if not self._is_fitted:
            raise ValueError("Must call cluster_chapters() first before getting topic info")
        
        if chapter_idx < 0 or chapter_idx >= len(self._topic_info):
            raise IndexError(f"Chapter index {chapter_idx} out of range [0, {len(self._topic_info)})")
        
        return self._topic_info[chapter_idx]


# Module-level exports
__all__ = [
    "TopicClusterer",
    "TopicInfo",
    "TopicResults",
    "BERTOPIC_AVAILABLE"
]
