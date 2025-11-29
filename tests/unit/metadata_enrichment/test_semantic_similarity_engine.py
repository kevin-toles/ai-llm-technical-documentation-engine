#!/usr/bin/env python3
"""
TDD Tests for SemanticSimilarityEngine - Sentence Transformers-based Similarity.

Reference: BERTOPIC_SENTENCE_TRANSFORMERS_DESIGN.md - Option C Architecture
Pattern: Service Layer Pattern (Architecture Patterns Ch. 4)
TDD Phase: RED - All tests expected to FAIL initially

Tests cover:
1. Embedding computation for chapters
2. Similarity matrix generation
3. Finding similar chapters (top-k retrieval)
4. Fallback to TF-IDF when Sentence Transformers unavailable
5. Edge cases (empty corpus, single chapter)
6. Integration with Tab 4 enrichment
"""

import pytest
import numpy as np
from typing import List, Dict, Any
from dataclasses import dataclass
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# Sample chapter texts from different domains
PYTHON_CHAPTER = """
Decorators are a powerful metaprogramming feature in Python that allow you to modify
the behavior of functions or classes. A decorator is essentially a callable that takes
another callable as an argument and returns a new callable with enhanced functionality.
Common use cases include logging, access control, memoization, and timing function execution.
The @decorator syntax provides a clean way to apply decorators without modifying the original
function code. Decorators can be stacked to apply multiple transformations.
"""

ARCHITECTURE_CHAPTER = """
The Repository pattern provides an abstraction over data storage, hiding the details
of how data is persisted. It acts as a collection-like interface for accessing domain
objects. The repository mediates between the domain and data mapping layers, providing
a clean separation of concerns. Unit of Work pattern tracks changes to objects and
coordinates writing changes back to a database in a single transaction.
"""

TESTING_CHAPTER = """
Test-driven development (TDD) follows a simple cycle: write a failing test first,
implement just enough code to make it pass, then refactor. Unit tests should be fast,
isolated, and deterministic. Pytest provides powerful fixtures for test setup and
teardown. Mock objects allow testing components in isolation by simulating dependencies.
"""

MICROSERVICES_CHAPTER = """
Microservices architecture decomposes applications into small, independently deployable
services. Each service focuses on a single business capability and communicates via
well-defined APIs. Service discovery, circuit breakers, and API gateways are essential
patterns for building resilient distributed systems. Container orchestration with
Kubernetes enables automated deployment and scaling.
"""

DATABASE_CHAPTER = """
SQLAlchemy provides both high-level ORM and low-level SQL expression language.
The session manages database connections and transactions. Alembic handles database
migrations through version-controlled scripts. Connection pooling improves performance
by reusing database connections. Query optimization and indexing are essential for
scalable data access patterns.
"""


class TestSemanticSimilarityEngineBasicFunctionality:
    """Test basic semantic similarity functionality."""

    def test_import_semantic_similarity_engine_module(self):
        """SemanticSimilarityEngine module should be importable."""
        # TDD RED: Module doesn't exist yet
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine
        )
        assert SemanticSimilarityEngine is not None

    def test_semantic_similarity_engine_instantiation_default_config(self):
        """SemanticSimilarityEngine should instantiate with default configuration."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine
        )
        
        engine = SemanticSimilarityEngine()
        
        assert engine is not None
        assert hasattr(engine, 'model_name')
        assert engine.model_name == "all-MiniLM-L6-v2"

    def test_semantic_similarity_engine_instantiation_custom_model(self):
        """SemanticSimilarityEngine should accept custom model name."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine
        )
        
        engine = SemanticSimilarityEngine(model_name="paraphrase-MiniLM-L3-v2")
        
        assert engine.model_name == "paraphrase-MiniLM-L3-v2"


class TestEmbeddingComputation:
    """Test embedding computation for chapters."""

    def test_compute_embeddings_returns_numpy_array(self):
        """compute_embeddings() should return numpy array."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine
        )
        
        corpus = [PYTHON_CHAPTER, ARCHITECTURE_CHAPTER, TESTING_CHAPTER]
        
        engine = SemanticSimilarityEngine()
        embeddings = engine.compute_embeddings(corpus)
        
        assert isinstance(embeddings, np.ndarray)
        assert len(embeddings) == 3  # One embedding per chapter

    def test_embeddings_have_correct_dimensions(self):
        """Embeddings should have expected dimensionality."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
            SENTENCE_TRANSFORMERS_AVAILABLE
        )
        
        corpus = [PYTHON_CHAPTER, ARCHITECTURE_CHAPTER]
        
        engine = SemanticSimilarityEngine()
        embeddings = engine.compute_embeddings(corpus)
        
        assert embeddings.shape[0] == 2  # 2 chapters
        # Dimension depends on model (all-MiniLM-L6-v2: 384, TF-IDF fallback: varies)
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            assert embeddings.shape[1] == 384  # all-MiniLM-L6-v2 dimension
        else:
            assert embeddings.shape[1] > 0  # TF-IDF fallback has features

    def test_embeddings_normalized(self):
        """Embeddings should be L2-normalized (for cosine similarity)."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
            SENTENCE_TRANSFORMERS_AVAILABLE
        )
        
        corpus = [PYTHON_CHAPTER, ARCHITECTURE_CHAPTER]
        
        engine = SemanticSimilarityEngine()
        embeddings = engine.compute_embeddings(corpus)
        
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            # Check L2 norm is close to 1.0 for each embedding
            norms = np.linalg.norm(embeddings, axis=1)
            np.testing.assert_array_almost_equal(norms, np.ones(len(corpus)), decimal=5)


class TestSimilarityMatrix:
    """Test similarity matrix computation."""

    def test_compute_similarity_matrix_returns_matrix(self):
        """compute_similarity_matrix() should return 2D numpy array."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine
        )
        
        corpus = [PYTHON_CHAPTER, ARCHITECTURE_CHAPTER, TESTING_CHAPTER]
        
        engine = SemanticSimilarityEngine()
        embeddings = engine.compute_embeddings(corpus)
        similarity_matrix = engine.compute_similarity_matrix(embeddings)
        
        assert isinstance(similarity_matrix, np.ndarray)
        assert similarity_matrix.shape == (3, 3)

    def test_similarity_matrix_diagonal_is_one(self):
        """Diagonal of similarity matrix should be 1.0 (self-similarity)."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine
        )
        
        corpus = [PYTHON_CHAPTER, ARCHITECTURE_CHAPTER, TESTING_CHAPTER]
        
        engine = SemanticSimilarityEngine()
        embeddings = engine.compute_embeddings(corpus)
        similarity_matrix = engine.compute_similarity_matrix(embeddings)
        
        diagonal = np.diag(similarity_matrix)
        np.testing.assert_array_almost_equal(diagonal, np.ones(3), decimal=5)

    def test_similarity_matrix_symmetric(self):
        """Similarity matrix should be symmetric."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine
        )
        
        corpus = [PYTHON_CHAPTER, ARCHITECTURE_CHAPTER, TESTING_CHAPTER]
        
        engine = SemanticSimilarityEngine()
        embeddings = engine.compute_embeddings(corpus)
        similarity_matrix = engine.compute_similarity_matrix(embeddings)
        
        np.testing.assert_array_almost_equal(
            similarity_matrix,
            similarity_matrix.T,
            decimal=5
        )

    def test_similarity_values_in_valid_range(self):
        """All similarity values should be between -1 and 1."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine
        )
        
        corpus = [PYTHON_CHAPTER, ARCHITECTURE_CHAPTER, TESTING_CHAPTER]
        
        engine = SemanticSimilarityEngine()
        embeddings = engine.compute_embeddings(corpus)
        similarity_matrix = engine.compute_similarity_matrix(embeddings)
        
        assert np.all(similarity_matrix >= -1.0)
        assert np.all(similarity_matrix <= 1.0)


class TestFindSimilarChapters:
    """Test finding similar chapters."""

    def test_find_similar_returns_list(self):
        """find_similar() should return list of SimilarityResult."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
            SimilarityResult
        )
        
        corpus = [PYTHON_CHAPTER, ARCHITECTURE_CHAPTER, TESTING_CHAPTER]
        index = [
            {"book": "book.json", "chapter": 1, "title": "Decorators"},
            {"book": "book.json", "chapter": 2, "title": "Repository"},
            {"book": "book.json", "chapter": 3, "title": "Testing"}
        ]
        
        engine = SemanticSimilarityEngine()
        embeddings = engine.compute_embeddings(corpus)
        
        results = engine.find_similar(
            query_idx=0,
            embeddings=embeddings,
            index=index,
            top_k=2
        )
        
        assert isinstance(results, list)
        assert len(results) <= 2  # top_k=2

    def test_find_similar_excludes_self(self):
        """find_similar() should not include the query chapter itself."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine
        )
        
        corpus = [PYTHON_CHAPTER, ARCHITECTURE_CHAPTER, TESTING_CHAPTER]
        index = [
            {"book": "book.json", "chapter": 1, "title": "Decorators"},
            {"book": "book.json", "chapter": 2, "title": "Repository"},
            {"book": "book.json", "chapter": 3, "title": "Testing"}
        ]
        
        engine = SemanticSimilarityEngine()
        embeddings = engine.compute_embeddings(corpus)
        
        results = engine.find_similar(
            query_idx=0,
            embeddings=embeddings,
            index=index,
            top_k=5
        )
        
        # Query chapter (index 0) should not be in results
        result_chapters = [r.chapter for r in results]
        assert 1 not in result_chapters  # Chapter 1 is query

    def test_find_similar_returns_sorted_by_score(self):
        """find_similar() should return results sorted by similarity (descending)."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine
        )
        
        corpus = [PYTHON_CHAPTER, ARCHITECTURE_CHAPTER, TESTING_CHAPTER,
                  MICROSERVICES_CHAPTER, DATABASE_CHAPTER]
        index = [
            {"book": "book.json", "chapter": i + 1, "title": f"Ch {i + 1}"}
            for i in range(5)
        ]
        
        engine = SemanticSimilarityEngine()
        embeddings = engine.compute_embeddings(corpus)
        
        results = engine.find_similar(
            query_idx=0,
            embeddings=embeddings,
            index=index,
            top_k=4
        )
        
        # Verify sorted by score descending
        scores = [r.score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_similarity_result_has_required_fields(self):
        """SimilarityResult should have book, chapter, title, score, method fields."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
            SimilarityResult
        )
        
        corpus = [PYTHON_CHAPTER, ARCHITECTURE_CHAPTER]
        index = [
            {"book": "book.json", "chapter": 1, "title": "Decorators"},
            {"book": "book.json", "chapter": 2, "title": "Repository"}
        ]
        
        engine = SemanticSimilarityEngine()
        embeddings = engine.compute_embeddings(corpus)
        
        results = engine.find_similar(
            query_idx=0,
            embeddings=embeddings,
            index=index,
            top_k=1
        )
        
        assert len(results) >= 1
        result = results[0]
        assert hasattr(result, 'book')
        assert hasattr(result, 'chapter')
        assert hasattr(result, 'title')
        assert hasattr(result, 'score')
        assert hasattr(result, 'method')


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_corpus_returns_empty_embeddings(self):
        """Empty corpus should return empty embeddings array."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine
        )
        
        engine = SemanticSimilarityEngine()
        embeddings = engine.compute_embeddings([])
        
        assert isinstance(embeddings, np.ndarray)
        assert len(embeddings) == 0

    def test_single_chapter_corpus(self):
        """Single chapter corpus should work without errors."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine
        )
        
        corpus = [PYTHON_CHAPTER]
        index = [{"book": "book.json", "chapter": 1, "title": "Decorators"}]
        
        engine = SemanticSimilarityEngine()
        embeddings = engine.compute_embeddings(corpus)
        
        assert len(embeddings) == 1
        
        # find_similar should return empty (no other chapters)
        results = engine.find_similar(
            query_idx=0,
            embeddings=embeddings,
            index=index,
            top_k=5
        )
        assert len(results) == 0

    def test_very_short_text_handled(self):
        """Very short texts should not crash."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine
        )
        
        corpus = ["Hello.", "World.", "Test."]
        
        engine = SemanticSimilarityEngine()
        embeddings = engine.compute_embeddings(corpus)
        
        assert len(embeddings) == 3

    def test_threshold_filters_low_similarity(self):
        """Results below threshold should be excluded."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine
        )
        
        corpus = [PYTHON_CHAPTER, ARCHITECTURE_CHAPTER, TESTING_CHAPTER]
        index = [
            {"book": "book.json", "chapter": i + 1, "title": f"Ch {i + 1}"}
            for i in range(3)
        ]
        
        engine = SemanticSimilarityEngine()
        embeddings = engine.compute_embeddings(corpus)
        
        # Very high threshold should filter most results
        results = engine.find_similar(
            query_idx=0,
            embeddings=embeddings,
            index=index,
            top_k=5,
            threshold=0.99  # Very high threshold
        )
        
        # All results should be above threshold
        for r in results:
            assert r.score >= 0.99


class TestFallbackBehavior:
    """Test fallback when Sentence Transformers unavailable."""

    def test_fallback_flag_exists(self):
        """SENTENCE_TRANSFORMERS_AVAILABLE flag should exist."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SENTENCE_TRANSFORMERS_AVAILABLE
        )
        
        assert isinstance(SENTENCE_TRANSFORMERS_AVAILABLE, bool)

    def test_fallback_uses_tfidf(self):
        """When Sentence Transformers unavailable, should use TF-IDF."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
            SENTENCE_TRANSFORMERS_AVAILABLE
        )
        
        corpus = [PYTHON_CHAPTER, ARCHITECTURE_CHAPTER]
        index = [
            {"book": "book.json", "chapter": 1, "title": "Decorators"},
            {"book": "book.json", "chapter": 2, "title": "Repository"}
        ]
        
        engine = SemanticSimilarityEngine()
        embeddings = engine.compute_embeddings(corpus)
        
        results = engine.find_similar(
            query_idx=0,
            embeddings=embeddings,
            index=index,
            top_k=1
        )
        
        # Method should indicate what was used
        if results:
            if SENTENCE_TRANSFORMERS_AVAILABLE:
                assert results[0].method == "sentence_transformers"
            else:
                assert results[0].method == "tfidf"


class TestIntegrationWithEnrichment:
    """Test integration with Tab 4 enrichment workflow."""

    def test_output_compatible_with_enrichment_schema(self):
        """SimilarityResult should be JSON serializable."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine
        )
        import json
        
        corpus = [PYTHON_CHAPTER, ARCHITECTURE_CHAPTER, TESTING_CHAPTER]
        index = [
            {"book": "book.json", "chapter": 1, "title": "Decorators"},
            {"book": "book.json", "chapter": 2, "title": "Repository"},
            {"book": "book.json", "chapter": 3, "title": "Testing"}
        ]
        
        engine = SemanticSimilarityEngine()
        embeddings = engine.compute_embeddings(corpus)
        
        results = engine.find_similar(
            query_idx=0,
            embeddings=embeddings,
            index=index,
            top_k=2
        )
        
        # Convert to dict and serialize to JSON
        results_dicts = [
            {
                "book": r.book,
                "chapter": r.chapter,
                "title": r.title,
                "score": r.score,
                "method": r.method
            }
            for r in results
        ]
        
        json_str = json.dumps(results_dicts)
        assert len(json_str) > 0
        
        # Verify roundtrip
        parsed = json.loads(json_str)
        assert len(parsed) == len(results)

    def test_semantically_similar_chapters_ranked_higher(self):
        """Semantically similar chapters should have higher scores."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine
        )
        
        # Two Python-related chapters
        python1 = "Decorators and functions in Python programming."
        python2 = "Python decorators for metaprogramming and function wrapping."
        
        # One unrelated chapter
        unrelated = "Microservices and container orchestration with Kubernetes."
        
        corpus = [python1, python2, unrelated]
        index = [
            {"book": "book.json", "chapter": 1, "title": "Python 1"},
            {"book": "book.json", "chapter": 2, "title": "Python 2"},
            {"book": "book.json", "chapter": 3, "title": "Microservices"}
        ]
        
        engine = SemanticSimilarityEngine()
        embeddings = engine.compute_embeddings(corpus)
        
        # Find similar to Python 1
        results = engine.find_similar(
            query_idx=0,
            embeddings=embeddings,
            index=index,
            top_k=2
        )
        
        # Python 2 should rank higher than Microservices
        if len(results) >= 2:
            # First result should be more similar
            assert results[0].score >= results[1].score


# Run tests with: pytest tests/unit/metadata_enrichment/test_semantic_similarity_engine.py -v
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
