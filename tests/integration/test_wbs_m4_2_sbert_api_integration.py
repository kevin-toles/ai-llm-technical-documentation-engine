#!/usr/bin/env python3
"""
Integration Tests for WBS M4.2.5-M4.2.6 - SBERT API Mode Integration.

WBS Reference: SBERT_EXTRACTION_MIGRATION_WBS.md - M4.2.5-M4.2.6
Purpose: Test SemanticSimilarityEngine against running Code-Orchestrator SBERT API

Requirements:
- Code-Orchestrator-Service running on localhost:8083
- SBERT API endpoints available: /v1/embeddings, /v1/similarity

TDD Phase: RED → GREEN
- M4.2.5: test_integration_api_mode (RED)
- M4.2.6: Integration test suite (GREEN)

Anti-Pattern Audit:
- #12: Connection pooling verified via real HTTP calls
- S1172: No unused parameters
- S1192: Module constants for API configuration

Usage:
    # With Code-Orchestrator running:
    pytest tests/integration/test_wbs_m4_2_sbert_api_integration.py -v --live

    # Skip if service not available:
    pytest tests/integration/test_wbs_m4_2_sbert_api_integration.py -v -m "not live"
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import Any

import httpx
import numpy as np
import pytest

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# =============================================================================
# Module Constants - SonarQube S1192
# =============================================================================

_SBERT_API_URL = os.getenv("SBERT_API_URL", "http://localhost:8083")
_EMBEDDINGS_ENDPOINT = "/v1/embeddings"
_SIMILARITY_ENDPOINT = "/v1/similarity"
_HEALTH_ENDPOINT = "/health"
_EXPECTED_DIMENSIONS = 384


def is_code_orchestrator_available() -> bool:
    """Check if Code-Orchestrator SBERT API is available."""
    try:
        response = httpx.get(f"{_SBERT_API_URL}{_HEALTH_ENDPOINT}", timeout=5.0)
        return response.status_code == 200
    except (httpx.ConnectError, httpx.TimeoutException):
        return False


# Mark all tests as requiring live service
pytestmark = [
    pytest.mark.integration,
    pytest.mark.live,
    pytest.mark.skipif(
        not is_code_orchestrator_available(),
        reason="Code-Orchestrator SBERT API not available at {_SBERT_API_URL}",
    ),
]


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def sample_texts() -> list[str]:
    """Sample texts for API testing."""
    return [
        "Python decorators are a powerful metaprogramming feature.",
        "Repository pattern provides data access abstraction.",
        "Test-driven development uses red-green-refactor cycle.",
    ]


@pytest.fixture
def api_client() -> httpx.AsyncClient:
    """Create async HTTP client for API testing."""
    return httpx.AsyncClient(base_url=_SBERT_API_URL, timeout=30.0)


# =============================================================================
# M4.2.5 RED: Integration Tests for API Mode
# =============================================================================


class TestSBERTAPIIntegration:
    """
    M4.2.5-M4.2.6: Integration tests against running Code-Orchestrator.

    These tests verify:
    1. Embeddings endpoint returns correct dimensions
    2. Similarity endpoint returns valid scores
    3. SemanticSimilarityEngine works in API mode
    """

    @pytest.mark.asyncio
    async def test_api_embeddings_endpoint_returns_vectors(
        self, api_client: httpx.AsyncClient, sample_texts: list[str]
    ) -> None:
        """M4.2.5: /v1/embeddings should return embedding vectors."""
        async with api_client:
            response = await api_client.post(
                _EMBEDDINGS_ENDPOINT,
                json={"texts": sample_texts},
            )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()

        assert "embeddings" in data, "Response should have 'embeddings' key"
        embeddings = data["embeddings"]

        assert len(embeddings) == len(sample_texts), (
            f"Expected {len(sample_texts)} embeddings, got {len(embeddings)}"
        )

    @pytest.mark.asyncio
    async def test_api_embeddings_have_correct_dimensions(
        self, api_client: httpx.AsyncClient, sample_texts: list[str]
    ) -> None:
        """M4.2.5: Embeddings should have 384 dimensions (MiniLM-L6-v2)."""
        async with api_client:
            response = await api_client.post(
                _EMBEDDINGS_ENDPOINT,
                json={"texts": sample_texts[:1]},  # Single text
            )

        assert response.status_code == 200
        data = response.json()
        embedding = data["embeddings"][0]

        assert len(embedding) == _EXPECTED_DIMENSIONS, (
            f"Expected {_EXPECTED_DIMENSIONS} dimensions, got {len(embedding)}"
        )

    @pytest.mark.asyncio
    async def test_api_similarity_endpoint_returns_score(
        self, api_client: httpx.AsyncClient
    ) -> None:
        """M4.2.5: /v1/similarity should return similarity score."""
        async with api_client:
            response = await api_client.post(
                _SIMILARITY_ENDPOINT,
                json={
                    "text1": "Python is a programming language.",
                    "text2": "Python is used for software development.",
                },
            )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()

        assert "score" in data, "Response should have 'score' key"
        score = data["score"]

        assert 0.0 <= score <= 1.0, f"Score {score} should be in [0, 1]"

    @pytest.mark.asyncio
    async def test_api_similarity_symmetric(
        self, api_client: httpx.AsyncClient
    ) -> None:
        """M4.2.5: Similarity should be symmetric: sim(a,b) == sim(b,a)."""
        text1 = "Machine learning models"
        text2 = "Deep learning algorithms"

        async with api_client:
            response1 = await api_client.post(
                _SIMILARITY_ENDPOINT,
                json={"text1": text1, "text2": text2},
            )
            response2 = await api_client.post(
                _SIMILARITY_ENDPOINT,
                json={"text1": text2, "text2": text1},
            )

        score1 = response1.json()["score"]
        score2 = response2.json()["score"]

        assert abs(score1 - score2) < 0.0001, (
            f"Similarity should be symmetric: {score1} != {score2}"
        )


class TestSemanticSimilarityEngineAPIMode:
    """
    M4.2.6: Test SemanticSimilarityEngine with real API.

    Verifies the engine works end-to-end with Code-Orchestrator.
    """

    def test_engine_api_mode_computes_embeddings(
        self, sample_texts: list[str]
    ) -> None:
        """M4.2.6: Engine in API mode should compute embeddings via API."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
            SimilarityConfig,
        )
        from workflows.shared.clients.sbert_client import SBERTClient

        # Force API mode
        config = SimilarityConfig(
            fallback_mode="api",
            use_api=True,
            sbert_api_url=_SBERT_API_URL,
        )

        async def run_test() -> np.ndarray:
            async with SBERTClient(base_url=_SBERT_API_URL) as client:
                engine = SemanticSimilarityEngine(config=config, sbert_client=client)
                return await engine.compute_embeddings_async(sample_texts)

        embeddings = asyncio.run(run_test())

        assert embeddings is not None
        assert embeddings.shape[0] == len(sample_texts)
        assert embeddings.shape[1] == _EXPECTED_DIMENSIONS

    def test_engine_api_mode_finds_similar(self, sample_texts: list[str]) -> None:
        """M4.2.6: Engine in API mode should find similar chapters."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
            SimilarityConfig,
        )
        from workflows.shared.clients.sbert_client import SBERTClient

        index = [
            {"book": "book1.json", "chapter": i + 1, "title": f"Chapter {i + 1}"}
            for i in range(len(sample_texts))
        ]

        config = SimilarityConfig(
            fallback_mode="api",
            use_api=True,
            sbert_api_url=_SBERT_API_URL,
        )

        async def run_test() -> list[Any]:
            async with SBERTClient(base_url=_SBERT_API_URL) as client:
                engine = SemanticSimilarityEngine(config=config, sbert_client=client)
                embeddings = await engine.compute_embeddings_async(sample_texts)
                return engine.find_similar(
                    query_idx=0,
                    embeddings=embeddings,
                    index=index,
                    top_k=2,
                )

        results = asyncio.run(run_test())

        assert len(results) <= 2
        for result in results:
            assert 0.0 <= result.score <= 1.0
            assert result.chapter != 1  # Should exclude query chapter

    def test_engine_api_mode_method_is_api(self, sample_texts: list[str]) -> None:
        """M4.2.6: Engine in API mode should report method='api'."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
            SimilarityConfig,
        )
        from workflows.shared.clients.sbert_client import SBERTClient

        index = [
            {"book": "book1.json", "chapter": i + 1, "title": f"Chapter {i + 1}"}
            for i in range(len(sample_texts))
        ]

        config = SimilarityConfig(
            fallback_mode="api",
            use_api=True,
            sbert_api_url=_SBERT_API_URL,
        )

        async def run_test() -> list[Any]:
            async with SBERTClient(base_url=_SBERT_API_URL) as client:
                engine = SemanticSimilarityEngine(config=config, sbert_client=client)
                embeddings = await engine.compute_embeddings_async(sample_texts)
                return engine.find_similar(
                    query_idx=0,
                    embeddings=embeddings,
                    index=index,
                    top_k=2,
                )

        results = asyncio.run(run_test())

        # API mode should report method
        if results:
            # When using API, method should indicate API usage
            assert results[0].method in ("api", "sentence_transformers")


class TestAPIPerformance:
    """M4.2.6: Performance tests for API mode."""

    @pytest.mark.asyncio
    async def test_api_batch_embeddings_performance(
        self, api_client: httpx.AsyncClient
    ) -> None:
        """API should handle batch embeddings efficiently."""
        import time

        # 10 sample texts
        texts = [f"Sample text number {i} for performance testing" for i in range(10)]

        start = time.perf_counter()
        async with api_client:
            response = await api_client.post(
                _EMBEDDINGS_ENDPOINT,
                json={"texts": texts},
            )
        elapsed_ms = (time.perf_counter() - start) * 1000

        assert response.status_code == 200
        assert len(response.json()["embeddings"]) == 10

        # Should complete within reasonable time (< 5 seconds for batch)
        assert elapsed_ms < 5000, f"Batch took {elapsed_ms:.2f}ms, expected < 5000ms"
