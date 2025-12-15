"""
Shared pytest fixtures for metadata_enrichment tests.

This module provides reusable fixtures for semantic similarity testing:
- Mode-aware fixtures that adapt to SBERT_FALLBACK_MODE
- FakeSBERTClient for unit testing without HTTP
- Baseline fixtures for parity testing
"""

import os
import sys
from pathlib import Path

# Add project root to Python path for imports (before other imports)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from typing import Dict, Any, List
from unittest.mock import MagicMock

# Import core dependencies
from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
    SemanticSimilarityEngine,
)
from workflows.shared.clients.sbert_client import FakeSBERTClient, EMBEDDING_DIMENSIONS


# =============================================================================
# Mode Detection Helpers
# =============================================================================

def get_current_mode() -> str:
    """Get the current SBERT_FALLBACK_MODE from environment."""
    return os.environ.get("SBERT_FALLBACK_MODE", "local")


def is_api_mode() -> bool:
    """Check if running in API mode."""
    return get_current_mode() == "api"


def is_tfidf_mode() -> bool:
    """Check if running in TF-IDF mode."""
    return get_current_mode() == "tfidf"


def is_local_mode() -> bool:
    """Check if running in local SBERT mode."""
    return get_current_mode() == "local"


# =============================================================================
# Sample Data Fixtures
# =============================================================================

@pytest.fixture
def sample_chapters() -> List[Dict[str, Any]]:
    """
    Sample chapter data for testing similarity operations.
    
    Returns 5 chapters with varying semantic content for testing
    embeddings, similarity scores, and clustering.
    """
    return [
        {
            "chapter_id": "ch1",
            "title": "Introduction to Machine Learning",
            "description": "Basics of ML algorithms and neural networks",
            "content": "Machine learning is a subset of artificial intelligence that enables systems to learn from data."
        },
        {
            "chapter_id": "ch2", 
            "title": "Deep Learning Fundamentals",
            "description": "Neural network architectures and training",
            "content": "Deep learning uses multi-layer neural networks to model complex patterns in data."
        },
        {
            "chapter_id": "ch3",
            "title": "Natural Language Processing",
            "description": "Text analysis and language models",
            "content": "NLP combines linguistics and machine learning to process human language."
        },
        {
            "chapter_id": "ch4",
            "title": "Computer Vision Basics",
            "description": "Image recognition and processing",
            "content": "Computer vision enables machines to interpret visual information from images and video."
        },
        {
            "chapter_id": "ch5",
            "title": "Reinforcement Learning",
            "description": "Learning through trial and error",
            "content": "Reinforcement learning trains agents to make decisions by rewarding desired behaviors."
        },
    ]


@pytest.fixture
def sample_texts() -> List[str]:
    """Simple text samples for embedding tests."""
    return [
        "Machine learning enables computers to learn from data.",
        "Deep neural networks process information in layers.",
        "Natural language processing understands human text.",
    ]


# =============================================================================
# FakeSBERTClient Fixture
# =============================================================================

@pytest.fixture
def fake_sbert_client() -> FakeSBERTClient:
    """
    Provides a FakeSBERTClient for unit testing.
    
    This fixture creates a FakeSBERTClient instance that generates
    deterministic embeddings without HTTP calls, suitable for
    isolated unit tests.
    
    Usage:
        def test_something(fake_sbert_client):
            embeddings = fake_sbert_client.generate_embeddings(["text"])
            assert len(embeddings[0]) == 384
    """
    return FakeSBERTClient()


@pytest.fixture
def mock_sbert_client() -> MagicMock:
    """
    Provides a MagicMock SBERTClient for controlling test behavior.
    
    Usage:
        def test_api_error(mock_sbert_client):
            mock_sbert_client.generate_embeddings.side_effect = Exception("API Error")
    """
    client = MagicMock()
    client.generate_embeddings = MagicMock(return_value=[[0.1] * EMBEDDING_DIMENSIONS])
    client.health_check = MagicMock(return_value={"status": "healthy"})
    return client


# =============================================================================
# Engine Fixtures
# =============================================================================

@pytest.fixture
def engine_with_fake_client(fake_sbert_client) -> SemanticSimilarityEngine:
    """
    Creates a SemanticSimilarityEngine with FakeSBERTClient injected.
    
    This fixture provides an engine that uses FakeSBERTClient for
    predictable, isolated unit testing without mode dependencies.
    """
    engine = SemanticSimilarityEngine()
    engine._api_client = fake_sbert_client
    return engine


@pytest.fixture
def fresh_engine() -> SemanticSimilarityEngine:
    """
    Creates a fresh SemanticSimilarityEngine instance.
    
    The engine will use the current SBERT_FALLBACK_MODE setting
    from the environment, making this suitable for mode-aware tests.
    """
    return SemanticSimilarityEngine()


# =============================================================================
# Baseline Fixtures for Parity Testing
# =============================================================================

@pytest.fixture
def local_sbert_baseline(sample_chapters) -> Dict[str, Any]:
    """
    Generate baseline embeddings and similarity scores using local SBERT.
    
    This fixture is intended for use with M4.1 functional parity tests.
    It forces local mode to generate reference outputs that other modes
    should match (within tolerance).
    
    Returns:
        Dict containing:
        - embeddings: List of embedding vectors
        - similarity_scores: Matrix of pairwise similarities
        - method: The method used ('sbert')
    """
    # Force local mode for baseline generation
    original_mode = os.environ.get("SBERT_FALLBACK_MODE")
    os.environ["SBERT_FALLBACK_MODE"] = "local"
    
    try:
        engine = SemanticSimilarityEngine()
        texts = [
            f"{ch['title']} {ch.get('description', '')} {ch.get('content', '')}"
            for ch in sample_chapters
        ]
        
        embeddings = engine.generate_embeddings(texts)
        
        # Calculate similarity matrix
        similarity_matrix = []
        for i, emb1 in enumerate(embeddings):
            row = []
            for j, emb2 in enumerate(embeddings):
                if i == j:
                    row.append(1.0)
                else:
                    # Cosine similarity
                    import numpy as np
                    vec1 = np.array(emb1)
                    vec2 = np.array(emb2)
                    similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
                    row.append(float(similarity))
            similarity_matrix.append(row)
        
        return {
            "embeddings": embeddings,
            "similarity_matrix": similarity_matrix,
            "method": engine._last_method,
            "texts": texts,
        }
    finally:
        # Restore original mode
        if original_mode is not None:
            os.environ["SBERT_FALLBACK_MODE"] = original_mode
        elif "SBERT_FALLBACK_MODE" in os.environ:
            del os.environ["SBERT_FALLBACK_MODE"]


# =============================================================================
# Skip Markers for Mode-Specific Tests
# =============================================================================

skip_if_api_mode = pytest.mark.skipif(
    is_api_mode(),
    reason="Test not applicable in API mode"
)

skip_if_tfidf_mode = pytest.mark.skipif(
    is_tfidf_mode(),
    reason="Test not applicable in TF-IDF mode"
)

skip_if_local_mode = pytest.mark.skipif(
    is_local_mode(),
    reason="Test not applicable in local SBERT mode"
)

requires_local_sbert = pytest.mark.skipif(
    not is_local_mode(),
    reason="Test requires local SBERT mode"
)


# =============================================================================
# Constants
# =============================================================================

# Re-export for convenience
EXPECTED_EMBEDDING_DIM = EMBEDDING_DIMENSIONS

# Tolerance values for parity testing
EMBEDDING_TOLERANCE = 0.01  # 1% tolerance for embedding values
SIMILARITY_TOLERANCE = 0.05  # 5% tolerance for similarity scores
LATENCY_THRESHOLD_MS = 100  # Max acceptable latency in milliseconds
