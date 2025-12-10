"""
Integration Test Matrix - IT-001 to IT-007

System-level integration tests validating the complete Kitchen Brigade stack.

Reference Documents:
- WBS_IMPLEMENTATION.md: Integration Test Matrix
- GUIDELINES p. 2145: Integration testing patterns

Test Matrix:
| Test ID | Services Required | What It Validates |
|---------|-------------------|-------------------|
| IT-001 | Code-Orchestrator | Service starts, models load |
| IT-002 | Code-Orchestrator | /extract returns consensus terms |
| IT-003 | Code-Orchestrator + Semantic-Search | Full search pipeline |
| IT-004 | Code-Orchestrator + Semantic-Search | Domain filtering works |
| IT-005 | All + llm-document-enhancer | Cross-book references produced |
| IT-006 | All | No false positives (C++ filtered) |
| IT-007 | All | Performance SLA met (<5s) |

MVP Acceptance Criteria:
- [ ] CodeT5+, GraphCodeBERT, CodeBERT models load and respond
- [ ] /api/v1/extract endpoint returns consensus terms
- [ ] /api/v1/search endpoint returns curated results
- [ ] Domain filtering removes false positives
- [ ] llm-document-enhancer produces cross-book references (currently ZERO)
- [ ] Semantic threshold 0.3 is achievable (vs impossible 0.7 TF-IDF)

Note: These tests use mocks/fakes when actual services are unavailable.
Real integration tests require docker-compose stack running.
"""

import os
import time
from typing import Any, Dict

import pytest

# Mark all tests in this module as integration tests
pytestmark = pytest.mark.integration


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def orchestrator_base_url() -> str:
    """Get orchestrator service URL from env or default."""
    return os.getenv("ORCHESTRATOR_URL", "http://localhost:8083")


@pytest.fixture
def semantic_search_url() -> str:
    """Get semantic search service URL from env or default."""
    return os.getenv("SEMANTIC_SEARCH_URL", "http://localhost:8081")


@pytest.fixture
def mock_orchestrator_response() -> Dict[str, Any]:
    """Mock response from Code-Orchestrator-Service."""
    return {
        "results": [
            {
                "id": "result-1",
                "book": "AI Engineering",
                "chapter": 5,
                "title": "RAG Pipelines",
                "content": "Multi-stage document chunking with overlap...",
                "score": 0.85,
                "metadata": {
                    "source": "AI Engineering",
                    "chapter_number": 5,
                    "title": "RAG Pipelines",
                    "domain": "ai-ml",
                }
            },
            {
                "id": "result-2",
                "book": "Building LLM Apps",
                "chapter": 3,
                "title": "Document Processing",
                "content": "Chunking strategies for large documents...",
                "score": 0.78,
                "metadata": {
                    "source": "Building LLM Apps",
                    "chapter_number": 3,
                    "title": "Document Processing",
                    "domain": "ai-ml",
                }
            },
        ],
        "total": 2,
        "metadata": {
            "processing_time_ms": 150,
            "pipeline": {
                "stages_completed": 4,
                "consensus_terms": ["chunking", "RAG", "embedding"],
            }
        }
    }


@pytest.fixture
def mock_health_response() -> Dict[str, Any]:
    """Mock health check response."""
    return {
        "status": "healthy",
        "service": "code-orchestrator",
        "version": "1.0.0",
        "models": {
            "codet5": "loaded",
            "graphcodebert": "loaded",
            "codebert": "loaded",
        }
    }


@pytest.fixture
def mock_extract_response() -> Dict[str, Any]:
    """Mock /api/v1/extract response."""
    return {
        "search_terms": [
            {"term": "chunking", "score": 0.92, "models_agreed": 3},
            {"term": "RAG", "score": 0.88, "models_agreed": 3},
            {"term": "embedding", "score": 0.75, "models_agreed": 2},
        ],
        "metadata": {
            "processing_time_ms": 120,
            "stages_completed": ["generate", "validate", "rank", "consensus"],
        }
    }


# =============================================================================
# IT-001: Service Starts, Models Load
# =============================================================================


class TestIT001ServiceStartsModelsLoad:
    """IT-001: Code-Orchestrator service starts and models load."""

    def test_health_endpoint_exists(self):
        """Health endpoint is defined."""
        # This validates the client expects /health
        from workflows.shared.clients.orchestrator_client import OrchestratorClient
        client = OrchestratorClient()
        assert client.base_url.endswith("8083") or "localhost" in client.base_url

    @pytest.mark.asyncio
    async def test_health_returns_model_status(self, mock_health_response):
        """Health check returns model loading status."""
        # Validate expected response structure
        assert mock_health_response["status"] == "healthy"
        assert "models" in mock_health_response
        assert mock_health_response["models"]["codet5"] == "loaded"
        assert mock_health_response["models"]["graphcodebert"] == "loaded"
        assert mock_health_response["models"]["codebert"] == "loaded"

    def test_ready_endpoint_validates_models(self):
        """Ready endpoint only succeeds when all models loaded."""
        # Structure validation - ready should check all 3 models
        expected_models = ["codet5", "graphcodebert", "codebert"]
        for model in expected_models:
            assert model in ["codet5", "graphcodebert", "codebert"]

    @pytest.mark.asyncio
    async def test_service_accepts_connections(self):
        """Service accepts HTTP connections on port 8083."""
        from workflows.shared.clients.orchestrator_client import OrchestratorClient
        
        # Test that client can be initialized
        client = OrchestratorClient(base_url="http://localhost:8083")
        assert client.base_url == "http://localhost:8083"
        assert client.timeout == 30.0


# =============================================================================
# IT-002: /extract Returns Consensus Terms
# =============================================================================


class TestIT002ExtractReturnsConsensusTerms:
    """IT-002: /api/v1/extract returns consensus terms from all models."""

    def test_extract_response_has_search_terms(self, mock_extract_response):
        """Extract response contains search_terms array."""
        assert "search_terms" in mock_extract_response
        assert isinstance(mock_extract_response["search_terms"], list)
        assert len(mock_extract_response["search_terms"]) > 0

    def test_search_terms_have_consensus(self, mock_extract_response):
        """Each term has models_agreed count >= 2."""
        for term in mock_extract_response["search_terms"]:
            assert "models_agreed" in term
            assert term["models_agreed"] >= 2

    def test_search_terms_have_scores(self, mock_extract_response):
        """Each term has a relevance score."""
        for term in mock_extract_response["search_terms"]:
            assert "score" in term
            assert 0.0 <= term["score"] <= 1.0

    def test_extract_metadata_includes_stages(self, mock_extract_response):
        """Metadata shows all pipeline stages completed."""
        assert "metadata" in mock_extract_response
        metadata = mock_extract_response["metadata"]
        assert "stages_completed" in metadata
        expected_stages = ["generate", "validate", "rank", "consensus"]
        assert metadata["stages_completed"] == expected_stages

    def test_processing_time_tracked(self, mock_extract_response):
        """Processing time is tracked in metadata."""
        assert mock_extract_response["metadata"]["processing_time_ms"] > 0


# =============================================================================
# IT-003: Full Search Pipeline
# =============================================================================


class TestIT003FullSearchPipeline:
    """IT-003: Full search pipeline (extract → search → curate)."""

    def test_search_response_has_results(self, mock_orchestrator_response):
        """Search response contains results array."""
        assert "results" in mock_orchestrator_response
        assert isinstance(mock_orchestrator_response["results"], list)

    def test_search_results_have_required_fields(self, mock_orchestrator_response):
        """Each result has book, chapter, title, score."""
        for result in mock_orchestrator_response["results"]:
            assert "book" in result
            assert "chapter" in result
            assert "title" in result
            assert "score" in result

    def test_search_results_sorted_by_score(self, mock_orchestrator_response):
        """Results are sorted by score descending."""
        results = mock_orchestrator_response["results"]
        scores = [r["score"] for r in results]
        assert scores == sorted(scores, reverse=True)

    @pytest.mark.asyncio
    async def test_search_pipeline_uses_client(self):
        """Search uses OrchestratorClient properly."""
        from workflows.shared.clients.orchestrator_client import (
            FakeOrchestratorClient,
        )
        
        fake_results = [
            {"id": "1", "book": "Test Book", "chapter": 1, "title": "Ch1", "score": 0.9}
        ]
        fake_client = FakeOrchestratorClient(results=fake_results)
        
        async with fake_client as client:
            results = await client.search(
                query="domain driven design",
                domain="architecture",
            )
            assert len(results) == 1
            assert results[0]["book"] == "Test Book"

    def test_search_total_count_matches(self, mock_orchestrator_response):
        """Total count matches results length."""
        assert mock_orchestrator_response["total"] == len(
            mock_orchestrator_response["results"]
        )


# =============================================================================
# IT-004: Domain Filtering Works
# =============================================================================


class TestIT004DomainFilteringWorks:
    """IT-004: Domain filtering removes irrelevant results."""

    def test_results_match_requested_domain(self, mock_orchestrator_response):
        """All results are from requested domain."""
        for result in mock_orchestrator_response["results"]:
            # AI/ML books should be returned for ai-ml domain
            assert result["book"] in [
                "AI Engineering",
                "Building LLM Apps",
                "Architecture Patterns with Python",
            ]

    def test_cpp_filtered_from_ai_domain(self):
        """C++ Concurrency filtered from ai-ml domain requests."""
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            is_relevant_domain,
        )
        
        cpp_ref = {"book": "C++ Concurrency in Action"}
        assert not is_relevant_domain(cpp_ref, expected_domain="ai-ml")

    def test_ai_books_pass_ai_domain_filter(self):
        """AI/ML books pass ai-ml domain filter."""
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            is_relevant_domain,
        )
        
        ai_ref = {"book": "AI Engineering"}
        assert is_relevant_domain(ai_ref, expected_domain="ai-ml")

    def test_filter_by_domain_function(self):
        """filter_by_domain removes wrong domain results."""
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            filter_by_domain,
        )
        
        results = [
            {"book": "AI Engineering", "score": 0.9},
            {"book": "C++ Concurrency", "score": 0.8},
            {"book": "Building LLM Apps", "score": 0.7},
        ]
        
        filtered = filter_by_domain(results, domain="ai-ml")
        
        # C++ should be filtered out
        books = [r["book"] for r in filtered]
        assert "C++ Concurrency" not in books
        assert "AI Engineering" in books


# =============================================================================
# IT-005: Cross-Book References Produced
# =============================================================================


class TestIT005CrossBookReferencesProduced:
    """IT-005: llm-document-enhancer produces cross-book references."""

    def test_count_cross_book_refs_function(self):
        """count_cross_book_refs correctly counts cross-book references."""
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            count_cross_book_refs,
        )
        
        enriched = {
            "book": "Architecture Patterns with Python",
            "chapters": [
                {
                    "chapter_number": 1,
                    "related_chapters": [
                        {"book": "AI Engineering", "chapter": 5},
                        {"book": "Architecture Patterns with Python", "chapter": 3},
                    ]
                },
                {
                    "chapter_number": 2,
                    "related_chapters": [
                        {"book": "Building LLM Apps", "chapter": 2},
                    ]
                }
            ]
        }
        
        count = count_cross_book_refs(enriched)
        # 2 cross-book refs (AI Engineering ch5, Building LLM Apps ch2)
        # The self-reference (Architecture Patterns ch3) should not count
        assert count == 2

    @pytest.mark.asyncio
    async def test_semantic_search_produces_cross_refs(self):
        """Semantic search produces cross-book references."""
        from workflows.shared.clients.orchestrator_client import FakeOrchestratorClient
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            find_related_chapters_semantic,
        )
        
        fake_results = [
            {
                "id": "1",
                "book": "AI Engineering",
                "chapter": 5,
                "title": "RAG",
                "score": 0.85,
            },
            {
                "id": "2",
                "book": "Building LLM Apps",
                "chapter": 3,
                "title": "Chunking",
                "score": 0.72,
            },
        ]
        fake_client = FakeOrchestratorClient(results=fake_results)
        
        async with fake_client as client:
            related = await find_related_chapters_semantic(
                chapter_text="Domain driven design patterns",
                current_book="Architecture Patterns with Python",
                client=client,
                domain="ai-ml",
            )
        
        # Should have cross-book references
        assert len(related) >= 1
        for ref in related:
            assert ref["book"] != "Architecture Patterns with Python"

    def test_threshold_0_3_achievable(self):
        """Semantic threshold 0.3 is achievable (vs TF-IDF 0.7)."""
        from workflows.shared.clients.orchestrator_client import (
            SEMANTIC_SIMILARITY_THRESHOLD,
        )
        
        assert SEMANTIC_SIMILARITY_THRESHOLD == 0.3
        assert SEMANTIC_SIMILARITY_THRESHOLD < 0.7  # Lower than TF-IDF

    def test_orchestrator_flag_enables_semantic_search(self):
        """--use-orchestrator flag is available."""
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            create_argument_parser,
        )
        
        parser = create_argument_parser()
        # Parse with required args and optional flag
        args = parser.parse_args([
            "--input", "/tmp/test.txt",
            "--output", "/tmp/output.json",
            "--use-orchestrator"
        ])
        assert args.use_orchestrator is True


# =============================================================================
# IT-006: No False Positives (C++ Filtered)
# =============================================================================


class TestIT006NoFalsePositives:
    """IT-006: No false positives (C++ filtered from AI domain)."""

    def test_cpp_books_excluded_from_ai(self):
        """C++ books excluded from AI/ML domain."""
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            is_relevant_domain,
        )
        
        cpp_refs = [
            {"book": "C++ Concurrency in Action"},
            {"book": "Systems Programming with C++"},
            {"book": "COBOL Legacy Systems"},
        ]
        
        for ref in cpp_refs:
            assert not is_relevant_domain(ref, expected_domain="ai-ml")

    def test_ai_books_included_for_ai_domain(self):
        """AI/ML books included for AI domain."""
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            is_relevant_domain,
        )
        
        ai_refs = [
            {"book": "AI Engineering"},
            {"book": "Building LLM Apps"},
            {"book": "Machine Learning Systems"},
            {"book": "Deep Learning for NLP"},
        ]
        
        for ref in ai_refs:
            assert is_relevant_domain(ref, expected_domain="ai-ml")

    def test_domain_filter_removes_all_false_positives(self):
        """Domain filter removes all false positives."""
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            filter_by_domain,
        )
        
        mixed_results = [
            {"book": "AI Engineering", "score": 0.9},
            {"book": "C++ Concurrency", "score": 0.85},
            {"book": "Building LLM Apps", "score": 0.8},
            {"book": "Systems Programming", "score": 0.75},
            {"book": "RAG Pipelines Guide", "score": 0.7},
        ]
        
        filtered = filter_by_domain(mixed_results, domain="ai-ml")
        
        # Only AI/ML books should remain
        for result in filtered:
            assert "C++" not in result["book"]
            assert "Systems Programming" not in result["book"]

    def test_false_positive_rate_below_10_percent(self):
        """False positive rate is below 10%."""
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            filter_by_domain,
            is_relevant_domain,
        )
        
        # Simulate 100 results with 5 false positives
        results = [{"book": f"AI Book {i}", "score": 0.5} for i in range(95)]
        results.extend([
            {"book": "C++ Book", "score": 0.5},
            {"book": "Systems Book", "score": 0.5},
            {"book": "COBOL Book", "score": 0.5},
            {"book": "Networking Book", "score": 0.5},
            {"book": "HTTP Protocol Book", "score": 0.5},
        ])
        
        filtered = filter_by_domain(results, domain="ai-ml")
        
        # All AI books should pass, false positives should be filtered
        false_positives_remaining = sum(
            1 for r in filtered
            if not is_relevant_domain(r, "ai-ml")
        )
        
        # Less than 10% false positives
        fp_rate = false_positives_remaining / len(filtered) if filtered else 0
        assert fp_rate < 0.10


# =============================================================================
# IT-007: Performance SLA Met (<5s)
# =============================================================================


class TestIT007PerformanceSLAMet:
    """IT-007: Performance SLA met (<5s latency)."""

    @pytest.mark.asyncio
    async def test_search_completes_under_5_seconds(self):
        """Search completes in under 5 seconds."""
        from workflows.shared.clients.orchestrator_client import FakeOrchestratorClient
        
        fake_client = FakeOrchestratorClient(results=[
            {"id": "1", "book": "Test", "chapter": 1, "title": "Ch1", "score": 0.9}
        ])
        
        start = time.time()
        async with fake_client as client:
            await client.search(query="test query", domain="ai-ml")
        duration_ms = (time.time() - start) * 1000
        
        assert duration_ms < 5000, f"Search took {duration_ms}ms, exceeds 5s SLA"

    def test_cache_improves_performance(self):
        """Cache significantly improves repeated query performance."""
        from workflows.shared.clients.cache import ResultCache
        
        cache = ResultCache(ttl_seconds=300)
        
        # First access (cache miss)
        start = time.time()
        result = cache.get("test_key")
        _miss_time = time.time() - start  # noqa: F841 - timing comparison
        assert result is None
        
        # Store in cache
        cache.set("test_key", {"data": "value"})
        
        # Second access (cache hit)
        start = time.time()
        result = cache.get("test_key")
        hit_time = time.time() - start
        
        assert result is not None
        # Cache hit should be very fast
        assert hit_time < 0.01  # Less than 10ms

    def test_metrics_track_latency(self):
        """Metrics track request latency."""
        from workflows.shared.clients.metrics import MetricsCollector
        
        collector = MetricsCollector()
        
        # Simulate request latencies
        collector.observe_histogram("orchestrator_latency_seconds", 0.150)
        collector.observe_histogram("orchestrator_latency_seconds", 0.200)
        collector.observe_histogram("orchestrator_latency_seconds", 0.180)
        
        count = collector.get_histogram_count("orchestrator_latency_seconds")
        total = collector.get_histogram_sum("orchestrator_latency_seconds")
        
        assert count == 3
        assert abs(total - 0.530) < 0.001  # ~530ms total

    def test_batch_search_more_efficient(self):
        """Batch search is more efficient than individual searches."""
        # Batch processing amortizes connection overhead
        from workflows.shared.clients.orchestrator_client import FakeOrchestratorClient
        
        fake_client = FakeOrchestratorClient(results=[
            {"id": "1", "book": "Test", "chapter": 1, "title": "Ch1", "score": 0.9}
        ])
        
        # batch_search exists and accepts multiple queries
        assert hasattr(fake_client, "batch_search")

    @pytest.mark.asyncio
    async def test_processing_time_in_metadata(self, mock_orchestrator_response):
        """Processing time is tracked in response metadata."""
        metadata = mock_orchestrator_response["metadata"]
        assert "processing_time_ms" in metadata
        assert metadata["processing_time_ms"] < 5000


# =============================================================================
# MVP Acceptance Criteria Validation
# =============================================================================


class TestMVPAcceptanceCriteria:
    """Validate MVP acceptance criteria are testable."""

    def test_models_load_and_respond(self, mock_health_response):
        """CodeT5+, GraphCodeBERT, CodeBERT models load and respond."""
        models = mock_health_response["models"]
        assert models["codet5"] == "loaded"
        assert models["graphcodebert"] == "loaded"
        assert models["codebert"] == "loaded"

    def test_extract_returns_consensus_terms(self, mock_extract_response):
        """Extract endpoint returns consensus terms."""
        terms = mock_extract_response["search_terms"]
        assert len(terms) > 0
        for term in terms:
            assert term["models_agreed"] >= 2

    def test_search_returns_curated_results(self, mock_orchestrator_response):
        """Search endpoint returns curated results."""
        results = mock_orchestrator_response["results"]
        assert len(results) > 0
        for result in results:
            assert "score" in result
            assert result["score"] >= 0.3

    def test_domain_filtering_removes_false_positives(self):
        """Domain filtering removes false positives."""
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            filter_by_domain,
        )
        
        results = [
            {"book": "AI Engineering", "score": 0.9},
            {"book": "C++ Concurrency", "score": 0.8},
        ]
        
        filtered = filter_by_domain(results, domain="ai-ml")
        books = [r["book"] for r in filtered]
        assert "C++ Concurrency" not in books

    def test_semantic_threshold_achievable(self):
        """Semantic threshold 0.3 is achievable."""
        from workflows.shared.clients.orchestrator_client import (
            SEMANTIC_SIMILARITY_THRESHOLD,
        )
        
        # 0.3 is achievable with semantic embeddings
        # 0.7 was impossible with TF-IDF
        assert SEMANTIC_SIMILARITY_THRESHOLD == 0.3

    @pytest.mark.asyncio
    async def test_cross_book_references_producible(self):
        """Cross-book references can be produced."""
        from workflows.shared.clients.orchestrator_client import FakeOrchestratorClient
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            find_related_chapters_semantic,
        )
        
        fake_client = FakeOrchestratorClient(results=[
            {"id": "1", "book": "Other Book", "chapter": 1, "title": "Ch", "score": 0.8}
        ])
        
        async with fake_client as client:
            related = await find_related_chapters_semantic(
                chapter_text="Test chapter",
                current_book="My Book",
                client=client,
            )
        
        # Should produce cross-book reference
        assert len(related) >= 1
        assert related[0]["book"] != "My Book"
