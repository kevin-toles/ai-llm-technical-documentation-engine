#!/usr/bin/env python3
"""
TDD Tests for TopicClusterer - BERTopic-based Topic Clustering for Chapters.

Reference: BERTOPIC_SENTENCE_TRANSFORMERS_DESIGN.md - Option C Architecture
Pattern: Service Layer Pattern (Architecture Patterns Ch. 4)
TDD Phase: RED - All tests expected to FAIL initially

Tests cover:
1. Topic assignment for chapters
2. Confidence score validation
3. Topic name generation
4. Clustering consistency
5. Edge cases (empty corpus, single chapter)
6. Fallback behavior when BERTopic unavailable
"""

import pytest
from typing import List, Dict, Any
from dataclasses import dataclass
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# Sample chapter texts from different domains (reused from existing tests)
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


class TestTopicClustererBasicFunctionality:
    """Test basic topic clustering functionality."""

    def test_import_topic_clusterer_module(self):
        """TopicClusterer module should be importable."""
        # TDD RED: Module doesn't exist yet
        from workflows.metadata_enrichment.scripts.topic_clusterer import TopicClusterer
        assert TopicClusterer

    def test_topic_clusterer_instantiation_default_config(self):
        """TopicClusterer should instantiate with default configuration."""
        from workflows.metadata_enrichment.scripts.topic_clusterer import TopicClusterer
        
        clusterer = TopicClusterer()
        
        assert clusterer
        assert hasattr(clusterer, 'embedding_model')
        assert clusterer.embedding_model == "all-MiniLM-L6-v2"

    def test_topic_clusterer_instantiation_custom_model(self):
        """TopicClusterer should accept custom embedding model."""
        from workflows.metadata_enrichment.scripts.topic_clusterer import TopicClusterer
        
        clusterer = TopicClusterer(embedding_model="paraphrase-MiniLM-L3-v2")
        
        assert clusterer.embedding_model == "paraphrase-MiniLM-L3-v2"

    def test_cluster_chapters_returns_topic_results(self):
        """cluster_chapters() should return TopicResults dataclass."""
        from workflows.metadata_enrichment.scripts.topic_clusterer import (
            TopicClusterer,
            TopicResults
        )
        
        corpus = [PYTHON_CHAPTER, ARCHITECTURE_CHAPTER, TESTING_CHAPTER]
        index = [
            {"book": "learning_python.json", "chapter": 1, "title": "Decorators"},
            {"book": "arch_patterns.json", "chapter": 2, "title": "Repository"},
            {"book": "learning_python.json", "chapter": 3, "title": "Testing"}
        ]
        
        clusterer = TopicClusterer()
        results = clusterer.cluster_chapters(corpus, index)
        
        assert isinstance(results, TopicResults)
        assert hasattr(results, 'topic_assignments')
        assert hasattr(results, 'topics')
        assert hasattr(results, 'topic_count')


class TestTopicAssignment:
    """Test topic assignment to individual chapters."""

    def test_get_topic_for_chapter_returns_topic_info(self):
        """get_topic_for_chapter() should return TopicInfo dataclass."""
        from workflows.metadata_enrichment.scripts.topic_clusterer import (
            TopicClusterer,
            TopicInfo
        )
        
        corpus = [PYTHON_CHAPTER, ARCHITECTURE_CHAPTER, TESTING_CHAPTER]
        index = [
            {"book": "learning_python.json", "chapter": 1, "title": "Decorators"},
            {"book": "arch_patterns.json", "chapter": 2, "title": "Repository"},
            {"book": "learning_python.json", "chapter": 3, "title": "Testing"}
        ]
        
        clusterer = TopicClusterer()
        clusterer.cluster_chapters(corpus, index)
        
        topic_info = clusterer.get_topic_for_chapter(0)
        
        assert isinstance(topic_info, TopicInfo)
        assert hasattr(topic_info, 'topic_id')
        assert hasattr(topic_info, 'topic_name')
        assert hasattr(topic_info, 'confidence')

    def test_topic_id_is_non_negative_integer(self):
        """Topic IDs should be non-negative integers (-1 allowed for outliers)."""
        from workflows.metadata_enrichment.scripts.topic_clusterer import TopicClusterer
        
        corpus = [PYTHON_CHAPTER, ARCHITECTURE_CHAPTER, TESTING_CHAPTER]
        index = [
            {"book": "learning_python.json", "chapter": 1, "title": "Decorators"},
            {"book": "arch_patterns.json", "chapter": 2, "title": "Repository"},
            {"book": "learning_python.json", "chapter": 3, "title": "Testing"}
        ]
        
        clusterer = TopicClusterer()
        clusterer.cluster_chapters(corpus, index)
        
        for idx in range(len(corpus)):
            topic_info = clusterer.get_topic_for_chapter(idx)
            assert isinstance(topic_info.topic_id, int)
            assert topic_info.topic_id >= -1  # -1 is valid (outlier/no topic)

    def test_topic_confidence_in_valid_range(self):
        """Topic confidence should be between 0.0 and 1.0."""
        from workflows.metadata_enrichment.scripts.topic_clusterer import TopicClusterer
        
        corpus = [PYTHON_CHAPTER, ARCHITECTURE_CHAPTER, TESTING_CHAPTER]
        index = [
            {"book": "learning_python.json", "chapter": 1, "title": "Decorators"},
            {"book": "arch_patterns.json", "chapter": 2, "title": "Repository"},
            {"book": "learning_python.json", "chapter": 3, "title": "Testing"}
        ]
        
        clusterer = TopicClusterer()
        clusterer.cluster_chapters(corpus, index)
        
        for idx in range(len(corpus)):
            topic_info = clusterer.get_topic_for_chapter(idx)
            assert 0.0 <= topic_info.confidence <= 1.0

    def test_topic_name_is_descriptive_string(self):
        """Topic names should be non-empty strings."""
        from workflows.metadata_enrichment.scripts.topic_clusterer import TopicClusterer
        
        corpus = [PYTHON_CHAPTER, ARCHITECTURE_CHAPTER, TESTING_CHAPTER]
        index = [
            {"book": "learning_python.json", "chapter": 1, "title": "Decorators"},
            {"book": "arch_patterns.json", "chapter": 2, "title": "Repository"},
            {"book": "learning_python.json", "chapter": 3, "title": "Testing"}
        ]
        
        clusterer = TopicClusterer()
        clusterer.cluster_chapters(corpus, index)
        
        for idx in range(len(corpus)):
            topic_info = clusterer.get_topic_for_chapter(idx)
            assert isinstance(topic_info.topic_name, str)
            assert len(topic_info.topic_name) > 0


class TestTopicMetadata:
    """Test topic-level metadata generation."""

    def test_topics_contain_keywords(self):
        """Each topic should have associated keywords."""
        from workflows.metadata_enrichment.scripts.topic_clusterer import TopicClusterer
        
        corpus = [PYTHON_CHAPTER, ARCHITECTURE_CHAPTER, TESTING_CHAPTER,
                  MICROSERVICES_CHAPTER, DATABASE_CHAPTER]
        index = [
            {"book": "book.json", "chapter": i, "title": f"Chapter {i}"}
            for i in range(len(corpus))
        ]
        
        clusterer = TopicClusterer()
        results = clusterer.cluster_chapters(corpus, index)
        
        for topic in results.topics:
            assert 'keywords' in topic
            assert isinstance(topic['keywords'], list)
            assert len(topic['keywords']) > 0

    def test_topics_contain_representative_chapters(self):
        """Each topic should list representative chapters."""
        from workflows.metadata_enrichment.scripts.topic_clusterer import TopicClusterer
        
        corpus = [PYTHON_CHAPTER, ARCHITECTURE_CHAPTER, TESTING_CHAPTER,
                  MICROSERVICES_CHAPTER, DATABASE_CHAPTER]
        index = [
            {"book": "book.json", "chapter": i, "title": f"Chapter {i}"}
            for i in range(len(corpus))
        ]
        
        clusterer = TopicClusterer()
        results = clusterer.cluster_chapters(corpus, index)
        
        for topic in results.topics:
            assert 'representative_chapters' in topic
            assert isinstance(topic['representative_chapters'], list)

    def test_topic_count_reflects_actual_topics(self):
        """topic_count should match number of discovered topics."""
        from workflows.metadata_enrichment.scripts.topic_clusterer import (
            TopicClusterer,
            BERTOPIC_AVAILABLE
        )
        
        corpus = [PYTHON_CHAPTER, ARCHITECTURE_CHAPTER, TESTING_CHAPTER,
                  MICROSERVICES_CHAPTER, DATABASE_CHAPTER]
        index = [
            {"book": "book.json", "chapter": i, "title": f"Chapter {i}"}
            for i in range(len(corpus))
        ]
        
        clusterer = TopicClusterer()
        results = clusterer.cluster_chapters(corpus, index)
        
        assert results.topic_count == len(results.topics)
        # When BERTopic is available, at least one topic should be found
        # When in fallback mode, topic_count is 0 (all chapters are outliers)
        if BERTOPIC_AVAILABLE:
            assert results.topic_count >= 1
        else:
            assert results.topic_count == 0  # Fallback mode: no topics


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_corpus_returns_empty_results(self):
        """Empty corpus should return empty results, not crash."""
        from workflows.metadata_enrichment.scripts.topic_clusterer import TopicClusterer
        
        clusterer = TopicClusterer()
        results = clusterer.cluster_chapters([], [])
        
        assert results.topic_count == 0
        assert len(results.topics) == 0
        assert len(results.topic_assignments) == 0

    def test_single_chapter_handles_gracefully(self):
        """Single chapter should be handled gracefully (no clustering possible)."""
        from workflows.metadata_enrichment.scripts.topic_clusterer import TopicClusterer
        
        corpus = [PYTHON_CHAPTER]
        index = [{"book": "book.json", "chapter": 1, "title": "Chapter 1"}]
        
        clusterer = TopicClusterer()
        results = clusterer.cluster_chapters(corpus, index)
        
        # Single chapter should get assigned to a topic (possibly -1 for outlier)
        assert len(results.topic_assignments) == 1
        topic_info = clusterer.get_topic_for_chapter(0)
        assert topic_info.topic_id >= -1

    def test_very_short_text_handles_gracefully(self):
        """Very short texts should not crash the clusterer."""
        from workflows.metadata_enrichment.scripts.topic_clusterer import TopicClusterer
        
        corpus = ["Hello.", "World.", "Test."]
        index = [
            {"book": "book.json", "chapter": i, "title": f"Ch {i}"}
            for i in range(3)
        ]
        
        clusterer = TopicClusterer()
        results = clusterer.cluster_chapters(corpus, index)
        
        # Should handle gracefully (all might be outliers)
        assert len(results.topic_assignments) == 3

    def test_invalid_chapter_index_raises_error(self):
        """Requesting topic for invalid chapter index should raise error."""
        from workflows.metadata_enrichment.scripts.topic_clusterer import TopicClusterer
        
        corpus = [PYTHON_CHAPTER]
        index = [{"book": "book.json", "chapter": 1, "title": "Chapter 1"}]
        
        clusterer = TopicClusterer()
        clusterer.cluster_chapters(corpus, index)
        
        with pytest.raises(IndexError):
            clusterer.get_topic_for_chapter(999)

    def test_cluster_chapters_not_called_raises_error(self):
        """Calling get_topic_for_chapter before clustering should raise error."""
        from workflows.metadata_enrichment.scripts.topic_clusterer import TopicClusterer
        
        clusterer = TopicClusterer()
        
        with pytest.raises(ValueError, match="cluster_chapters.*first"):
            clusterer.get_topic_for_chapter(0)


class TestFallbackBehavior:
    """Test fallback when BERTopic is unavailable."""

    def test_fallback_when_bertopic_unavailable(self):
        """Should fall back gracefully when BERTopic import fails."""
        from workflows.metadata_enrichment.scripts.topic_clusterer import (
            TopicClusterer,
            BERTOPIC_AVAILABLE
        )
        
        # This test verifies the fallback flag exists
        assert isinstance(BERTOPIC_AVAILABLE, bool)

    def test_fallback_assigns_topic_negative_one(self):
        """When BERTopic unavailable, all chapters get topic_id=-1."""
        # Mock BERTopic as unavailable
        with patch.dict('sys.modules', {'bertopic': None}):
            # Force reimport to test fallback
            import importlib
            from workflows.metadata_enrichment.scripts import topic_clusterer
            importlib.reload(topic_clusterer)
            
            if not topic_clusterer.BERTOPIC_AVAILABLE:
                clusterer = topic_clusterer.TopicClusterer()
                corpus = [PYTHON_CHAPTER, ARCHITECTURE_CHAPTER]
                index = [
                    {"book": "book.json", "chapter": 1, "title": "Ch 1"},
                    {"book": "book.json", "chapter": 2, "title": "Ch 2"}
                ]
                
                results = clusterer.cluster_chapters(corpus, index)
                
                # All should be assigned -1 (no topic)
                for assignment in results.topic_assignments:
                    assert assignment == -1


class TestIntegrationWithEnrichment:
    """Test integration with Tab 4 enrichment workflow."""

    def test_output_format_compatible_with_enrichment(self):
        """TopicResults should be serializable to JSON for enrichment output."""
        from workflows.metadata_enrichment.scripts.topic_clusterer import TopicClusterer
        import json
        
        corpus = [PYTHON_CHAPTER, ARCHITECTURE_CHAPTER, TESTING_CHAPTER]
        index = [
            {"book": "learning_python.json", "chapter": 1, "title": "Decorators"},
            {"book": "arch_patterns.json", "chapter": 2, "title": "Repository"},
            {"book": "learning_python.json", "chapter": 3, "title": "Testing"}
        ]
        
        clusterer = TopicClusterer()
        results = clusterer.cluster_chapters(corpus, index)
        
        # Should be JSON serializable
        json_str = json.dumps({
            "topic_count": results.topic_count,
            "topics": results.topics,
            "topic_assignments": results.topic_assignments
        })
        
        assert len(json_str) > 0
        parsed = json.loads(json_str)
        assert parsed["topic_count"] == results.topic_count

    def test_similar_chapters_grouped_in_same_topic(self):
        """Semantically similar chapters should be assigned same topic."""
        from workflows.metadata_enrichment.scripts.topic_clusterer import TopicClusterer
        
        # Two Python-related chapters
        python1 = "Functions and decorators in Python programming language."
        python2 = "Python decorators and function wrappers for metaprogramming."
        
        # Two architecture-related chapters
        arch1 = "Repository pattern and domain-driven design principles."
        arch2 = "Domain models and repository abstraction layers."
        
        corpus = [python1, python2, arch1, arch2]
        index = [
            {"book": "book.json", "chapter": i, "title": f"Ch {i}"}
            for i in range(4)
        ]
        
        clusterer = TopicClusterer()
        _results = clusterer.cluster_chapters(corpus, index)
        
        # Python chapters should have same topic (or both outliers)
        topic_py1 = clusterer.get_topic_for_chapter(0).topic_id
        topic_py2 = clusterer.get_topic_for_chapter(1).topic_id
        
        # Architecture chapters should have same topic (or both outliers)
        topic_arch1 = clusterer.get_topic_for_chapter(2).topic_id
        topic_arch2 = clusterer.get_topic_for_chapter(3).topic_id
        
        # At minimum, similar chapters shouldn't be in different non-outlier topics
        if topic_py1 != -1 and topic_py2 != -1:
            assert topic_py1 == topic_py2, "Similar Python chapters should cluster together"
        
        if topic_arch1 != -1 and topic_arch2 != -1:
            assert topic_arch1 == topic_arch2, "Similar architecture chapters should cluster together"


# Run tests with: pytest tests/unit/metadata_enrichment/test_topic_clusterer.py -v
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
