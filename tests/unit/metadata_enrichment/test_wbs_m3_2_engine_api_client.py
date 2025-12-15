#!/usr/bin/env python3
"""
TDD Tests for SemanticSimilarityEngine API Client Integration - WBS M3.2.

Reference: SBERT_EXTRACTION_MIGRATION_WBS.md M3.2 SemanticSimilarityEngine Refactor
TDD Phase: RED - Tests for API client integration, fallback logic

Tests cover:
1. M3.2.1: Engine uses API client when available
2. M3.2.3: Engine falls back to local SBERT when API unavailable
3. M3.2.5: Engine falls back to TF-IDF when both API and local unavailable

Anti-Patterns Avoided:
- #7: Exception naming (SBERTConnectionError, not ConnectionError)
- #12: Connection pooling via SBERTClient context manager
- S1172: No unused parameters
"""

import pytest
import numpy as np
from unittest.mock import AsyncMock, patch
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import the FakeSBERTClient for testing
from workflows.shared.clients.sbert_client import (  # noqa: E402
    FakeSBERTClient,
    SBERTConnectionError,
    SBERTTimeoutError,
    EMBEDDING_DIMENSIONS,
)


# =============================================================================
# Sample Data
# =============================================================================

PYTHON_CHAPTER = """
Decorators are a powerful metaprogramming feature in Python that allow you to modify
the behavior of functions or classes. A decorator is essentially a callable that takes
another callable as an argument and returns a new callable with enhanced functionality.
"""

ARCHITECTURE_CHAPTER = """
The Repository pattern provides an abstraction over data storage, hiding the details
of how data is persisted. It acts as a collection-like interface for accessing domain
objects.
"""

TESTING_CHAPTER = """
Test-driven development (TDD) follows a simple cycle: write a failing test first,
implement just enough code to make it pass, then refactor.
"""


# =============================================================================
# M3.2.1 RED: Test Engine Uses API Client
# Acceptance Criteria: Test engine calls API when available
# =============================================================================


class TestEngineUsesAPIClient:
    """M3.2.1: Test that SemanticSimilarityEngine uses API client when available."""

    def test_engine_has_api_mode_attribute(self):
        """Engine should have use_api attribute to enable API mode."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
            SimilarityConfig,
        )

        # Create config with API mode enabled
        config = SimilarityConfig(use_api=True)  # New attribute
        engine = SemanticSimilarityEngine(config=config)

        assert hasattr(engine, "_use_api")
        assert engine._use_api is True

    def test_engine_accepts_sbert_client(self):
        """Engine should accept an SBERTClient instance for API calls."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
            SimilarityConfig,
        )

        fake_client = FakeSBERTClient()

        # Create engine with API client
        config = SimilarityConfig(use_api=True)
        engine = SemanticSimilarityEngine(config=config, sbert_client=fake_client)

        assert hasattr(engine, "_sbert_client")
        assert engine._sbert_client is fake_client

    @pytest.mark.asyncio
    async def test_engine_calls_api_for_embeddings(self):
        """Engine should call API client for embeddings when in API mode."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
            SimilarityConfig,
        )

        # Set up fake client with expected embeddings
        fake_client = FakeSBERTClient()
        fake_client.set_embeddings({
            PYTHON_CHAPTER: [0.1] * EMBEDDING_DIMENSIONS,
            ARCHITECTURE_CHAPTER: [0.2] * EMBEDDING_DIMENSIONS,
        })

        # Create engine in API mode
        config = SimilarityConfig(use_api=True)
        engine = SemanticSimilarityEngine(config=config, sbert_client=fake_client)

        corpus = [PYTHON_CHAPTER, ARCHITECTURE_CHAPTER]

        # Use async context manager for client
        async with fake_client:
            embeddings = await engine.compute_embeddings_async(corpus)

        assert isinstance(embeddings, np.ndarray)
        assert embeddings.shape == (2, EMBEDDING_DIMENSIONS)

    @pytest.mark.asyncio
    async def test_engine_api_embeddings_returns_correct_values(self):
        """Engine API embeddings should match what client returns."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
            SimilarityConfig,
        )

        # Set up fake client with specific embeddings
        fake_client = FakeSBERTClient()
        expected_embedding = [0.5] * EMBEDDING_DIMENSIONS
        fake_client.set_embeddings({PYTHON_CHAPTER: expected_embedding})

        config = SimilarityConfig(use_api=True)
        engine = SemanticSimilarityEngine(config=config, sbert_client=fake_client)

        async with fake_client:
            embeddings = await engine.compute_embeddings_async([PYTHON_CHAPTER])

        # First embedding should match expected
        np.testing.assert_array_almost_equal(embeddings[0], expected_embedding)

    def test_engine_config_has_api_url(self):
        """SimilarityConfig should have sbert_api_url attribute."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SimilarityConfig,
        )

        config = SimilarityConfig(sbert_api_url="http://code-orchestrator:8083")

        assert hasattr(config, "sbert_api_url")
        assert config.sbert_api_url == "http://code-orchestrator:8083"

    def test_engine_config_default_api_url(self):
        """SimilarityConfig should have default sbert_api_url."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SimilarityConfig,
        )

        config = SimilarityConfig()

        assert hasattr(config, "sbert_api_url")
        # Default from environment or localhost
        assert config.sbert_api_url is not None

    def test_engine_config_has_api_timeout(self):
        """M3.3.3: SimilarityConfig should have sbert_api_timeout attribute."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SimilarityConfig,
        )

        config = SimilarityConfig(sbert_api_timeout=60.0)

        assert hasattr(config, "sbert_api_timeout")
        assert config.sbert_api_timeout == 60.0

    def test_engine_config_default_api_timeout(self):
        """M3.3.3: SimilarityConfig should have default sbert_api_timeout of 30 seconds."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SimilarityConfig,
        )

        config = SimilarityConfig()

        assert hasattr(config, "sbert_api_timeout")
        assert config.sbert_api_timeout == 30.0  # Default per WBS M3.3.4


# =============================================================================
# M3.2.3 RED: Test Engine Fallback to Local SBERT
# Acceptance Criteria: Test fallback to local SBERT when API unavailable
# =============================================================================


class TestEngineFallbackLocal:
    """M3.2.3: Test fallback to local SBERT when API unavailable."""

    @pytest.mark.asyncio
    async def test_engine_falls_back_to_local_on_connection_error(self):
        """Engine should use local SBERT when API connection fails."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
            SimilarityConfig,
            SENTENCE_TRANSFORMERS_AVAILABLE,
        )

        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            pytest.skip("Sentence transformers not available for local fallback test")

        # Create a mock client that raises connection error
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get_embeddings = AsyncMock(
            side_effect=SBERTConnectionError("Connection refused")
        )

        # Create engine with fallback enabled
        config = SimilarityConfig(use_api=True, fallback_to_local=True)
        engine = SemanticSimilarityEngine(config=config, sbert_client=mock_client)

        corpus = [PYTHON_CHAPTER]

        async with mock_client:
            embeddings = await engine.compute_embeddings_async(corpus)

        # Should have used local SBERT, not API
        assert isinstance(embeddings, np.ndarray)
        assert embeddings.shape[1] == 384  # MiniLM-L6-v2 dimensions
        assert engine._last_method == "local_sbert"  # Track which method was used

    @pytest.mark.asyncio
    async def test_engine_falls_back_to_local_on_timeout(self):
        """Engine should use local SBERT when API times out."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
            SimilarityConfig,
            SENTENCE_TRANSFORMERS_AVAILABLE,
        )

        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            pytest.skip("Sentence transformers not available for local fallback test")

        # Create a mock client that raises timeout
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get_embeddings = AsyncMock(
            side_effect=SBERTTimeoutError("Request timed out")
        )

        config = SimilarityConfig(use_api=True, fallback_to_local=True)
        engine = SemanticSimilarityEngine(config=config, sbert_client=mock_client)

        corpus = [PYTHON_CHAPTER]

        async with mock_client:
            embeddings = await engine.compute_embeddings_async(corpus)

        assert isinstance(embeddings, np.ndarray)
        assert engine._last_method == "local_sbert"

    def test_engine_config_has_fallback_to_local(self):
        """SimilarityConfig should have fallback_to_local attribute."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SimilarityConfig,
        )

        config = SimilarityConfig(fallback_to_local=True)

        assert hasattr(config, "fallback_to_local")
        assert config.fallback_to_local is True

    @pytest.mark.asyncio
    async def test_engine_logs_fallback_warning(self):
        """Engine should log warning when falling back to local."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
            SimilarityConfig,
            SENTENCE_TRANSFORMERS_AVAILABLE,
        )

        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            pytest.skip("Sentence transformers not available for local fallback test")

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get_embeddings = AsyncMock(
            side_effect=SBERTConnectionError("Connection refused")
        )

        config = SimilarityConfig(use_api=True, fallback_to_local=True)
        engine = SemanticSimilarityEngine(config=config, sbert_client=mock_client)

        with patch.object(engine, "_logger") as mock_logger:
            async with mock_client:
                await engine.compute_embeddings_async([PYTHON_CHAPTER])

            # Should have logged a warning about fallback
            mock_logger.warning.assert_called()


# =============================================================================
# M3.2.5 RED: Test Engine Fallback to TF-IDF
# Acceptance Criteria: Test fallback to TF-IDF when both API and local unavailable
# =============================================================================


class TestEngineFallbackTfidf:
    """M3.2.5: Test fallback to TF-IDF when API and local unavailable."""

    @pytest.mark.asyncio
    async def test_engine_falls_back_to_tfidf_when_all_fail(self):
        """Engine should use TF-IDF when API and local SBERT both fail."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
            SimilarityConfig,
        )

        # Mock client that fails
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get_embeddings = AsyncMock(
            side_effect=SBERTConnectionError("Connection refused")
        )

        # Config with all fallbacks enabled, but local SBERT "unavailable"
        config = SimilarityConfig(
            use_api=True,
            fallback_to_local=True,
            fallback_to_tfidf=True,
        )

        # Patch SENTENCE_TRANSFORMERS_AVAILABLE to simulate unavailable
        with patch(
            "workflows.metadata_enrichment.scripts.semantic_similarity_engine.SENTENCE_TRANSFORMERS_AVAILABLE",
            False,
        ):
            engine = SemanticSimilarityEngine(config=config, sbert_client=mock_client)

            async with mock_client:
                embeddings = await engine.compute_embeddings_async(
                    [PYTHON_CHAPTER, ARCHITECTURE_CHAPTER]
                )

            assert isinstance(embeddings, np.ndarray)
            assert embeddings.shape[0] == 2
            assert engine._last_method == "tfidf"

    @pytest.mark.asyncio
    async def test_engine_tfidf_fallback_maintains_similarity(self):
        """TF-IDF fallback should still produce valid similarity results."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
            SimilarityConfig,
        )

        # Mock client that fails
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get_embeddings = AsyncMock(
            side_effect=SBERTConnectionError("Connection refused")
        )

        config = SimilarityConfig(
            use_api=True,
            fallback_to_local=True,
            fallback_to_tfidf=True,
        )

        with patch(
            "workflows.metadata_enrichment.scripts.semantic_similarity_engine.SENTENCE_TRANSFORMERS_AVAILABLE",
            False,
        ):
            engine = SemanticSimilarityEngine(config=config, sbert_client=mock_client)

            corpus = [PYTHON_CHAPTER, ARCHITECTURE_CHAPTER, TESTING_CHAPTER]
            # Note: index not needed for embedding computation test

            async with mock_client:
                embeddings = await engine.compute_embeddings_async(corpus)

            # Compute similarity matrix
            similarity_matrix = engine.compute_similarity_matrix(embeddings)

            # Should produce valid similarity matrix
            assert similarity_matrix.shape == (3, 3)
            np.testing.assert_array_almost_equal(np.diag(similarity_matrix), [1, 1, 1])

    def test_engine_tracks_method_used(self):
        """Engine should track which computation method was used."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
            SimilarityConfig,
        )

        config = SimilarityConfig(fallback_to_tfidf=True)

        with patch(
            "workflows.metadata_enrichment.scripts.semantic_similarity_engine.SENTENCE_TRANSFORMERS_AVAILABLE",
            False,
        ):
            engine = SemanticSimilarityEngine(config=config)
            # TF-IDF needs at least 2 documents to avoid min_df/max_df error
            _ = engine.compute_embeddings([PYTHON_CHAPTER, ARCHITECTURE_CHAPTER])

            assert hasattr(engine, "_last_method")
            assert engine._last_method == "tfidf"


# =============================================================================
# Three-Tier Fallback Integration Test
# Pattern: API → Local SBERT → TF-IDF
# =============================================================================


class TestThreeTierFallback:
    """Integration tests for three-tier fallback: API → Local SBERT → TF-IDF."""

    def test_engine_config_has_fallback_mode(self):
        """SimilarityConfig should have fallback_mode attribute."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SimilarityConfig,
        )

        config = SimilarityConfig(fallback_mode="api")

        assert hasattr(config, "fallback_mode")
        assert config.fallback_mode in ["api", "local", "tfidf"]

    def test_engine_supports_mode_api(self):
        """Engine with mode=api should try API first."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
            SimilarityConfig,
        )

        config = SimilarityConfig(fallback_mode="api", use_api=True)
        engine = SemanticSimilarityEngine(config=config)

        assert engine._fallback_mode == "api"

    def test_engine_supports_mode_local(self):
        """Engine with mode=local should skip API, use local SBERT."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
            SimilarityConfig,
        )

        config = SimilarityConfig(fallback_mode="local")
        engine = SemanticSimilarityEngine(config=config)

        assert engine._fallback_mode == "local"

    def test_engine_supports_mode_tfidf(self):
        """Engine with mode=tfidf should skip API and local, use TF-IDF."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
            SimilarityConfig,
        )

        config = SimilarityConfig(fallback_mode="tfidf")
        engine = SemanticSimilarityEngine(config=config)

        assert engine._fallback_mode == "tfidf"
        assert engine._using_fallback is True

    @pytest.mark.asyncio
    async def test_full_fallback_chain_api_to_local_to_tfidf(self):
        """Test complete fallback chain: API fails → local fails → TF-IDF succeeds."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
            SimilarityConfig,
        )

        # Mock client that always fails
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get_embeddings = AsyncMock(
            side_effect=SBERTConnectionError("Connection refused")
        )

        config = SimilarityConfig(
            fallback_mode="api",
            use_api=True,
            fallback_to_local=True,
            fallback_to_tfidf=True,
        )

        # Simulate local SBERT unavailable too
        with patch(
            "workflows.metadata_enrichment.scripts.semantic_similarity_engine.SENTENCE_TRANSFORMERS_AVAILABLE",
            False,
        ):
            engine = SemanticSimilarityEngine(config=config, sbert_client=mock_client)

            async with mock_client:
                # TF-IDF needs at least 2 documents
                embeddings = await engine.compute_embeddings_async(
                    [PYTHON_CHAPTER, ARCHITECTURE_CHAPTER]
                )

            # Should have fallen back to TF-IDF
            assert embeddings.shape[0] == 2
            assert engine._last_method == "tfidf"
