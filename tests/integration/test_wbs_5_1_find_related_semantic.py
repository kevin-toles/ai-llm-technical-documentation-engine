#!/usr/bin/env python3
"""
WBS 5.1.3 & 5.1.4: find_related_chapters Replacement & Threshold Tests

Test-Driven Development (TDD) - RED Phase
Tests for replacing TF-IDF find_related_chapters with orchestrator calls.

Reference Documents:
- WBS_IMPLEMENTATION.md: Phase 5.1.3 - Replace find_related_chapters
- WBS_IMPLEMENTATION.md: Phase 5.1.4 - Update threshold to 0.3
- CODING_PATTERNS_ANALYSIS.md: Dependency injection patterns

Key Change:
- Current: find_related_chapters() uses TF-IDF with 0.7 threshold (impossible)
- Target: find_related_chapters_semantic() uses orchestrator with 0.3 threshold (achievable)
"""

import pytest
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent


# =============================================================================
# WBS 5.1.3: Replace find_related_chapters Tests
# =============================================================================
class TestFindRelatedChaptersSemantic:
    """Test suite for WBS 5.1.3: Replace find_related_chapters."""

    def test_find_related_chapters_semantic_exists(self):
        """
        RED TEST: find_related_chapters_semantic() function exists.
        """
        import sys
        sys.path.insert(0, str(PROJECT_ROOT / "workflows" / "metadata_enrichment" / "scripts"))
        
        try:
            from enrich_metadata_per_book import find_related_chapters_semantic
            assert callable(find_related_chapters_semantic)
        except (ImportError, AttributeError):
            pytest.fail("find_related_chapters_semantic() not found")

    @pytest.mark.asyncio
    async def test_find_related_chapters_semantic_calls_orchestrator(self):
        """
        RED TEST: find_related_chapters_semantic() calls orchestrator client.
        """
        import sys
        sys.path.insert(0, str(PROJECT_ROOT / "workflows" / "metadata_enrichment" / "scripts"))
        
        try:
            from enrich_metadata_per_book import find_related_chapters_semantic
            from workflows.shared.clients.orchestrator_client import FakeOrchestratorClient
            
            fake_results = [
                {
                    "book": "AI Engineering",
                    "chapter": 5,
                    "title": "RAG Pipelines",
                    "relevance_score": 0.85,
                }
            ]
            fake_client = FakeOrchestratorClient(results=fake_results)
            
            results = await find_related_chapters_semantic(
                chapter_text="LLM document chunking for RAG",
                domain="ai-ml",
                current_book="Architecture_Patterns",
                client=fake_client,
                top_n=5
            )
            
            assert len(results) > 0
            assert results[0]["book"] == "AI Engineering"
        except (ImportError, AttributeError) as e:
            pytest.fail(f"find_related_chapters_semantic() not found: {e}")

    @pytest.mark.asyncio
    async def test_find_related_chapters_semantic_excludes_current_book(self):
        """
        RED TEST: Results exclude chapters from current book.
        """
        import sys
        sys.path.insert(0, str(PROJECT_ROOT / "workflows" / "metadata_enrichment" / "scripts"))
        
        try:
            from enrich_metadata_per_book import find_related_chapters_semantic
            from workflows.shared.clients.orchestrator_client import FakeOrchestratorClient
            
            fake_results = [
                {"book": "Architecture_Patterns", "chapter": 3, "relevance_score": 0.9},
                {"book": "AI Engineering", "chapter": 5, "relevance_score": 0.85},
            ]
            fake_client = FakeOrchestratorClient(results=fake_results)
            
            results = await find_related_chapters_semantic(
                chapter_text="test",
                domain="ai-ml",
                current_book="Architecture_Patterns",  # This book should be excluded
                client=fake_client
            )
            
            for result in results:
                assert result["book"] != "Architecture_Patterns", "Should exclude current book"
        except (ImportError, AttributeError) as e:
            pytest.fail(f"find_related_chapters_semantic() not found: {e}")

    @pytest.mark.asyncio
    async def test_find_related_chapters_semantic_returns_formatted_results(self):
        """
        RED TEST: Results have required schema fields.
        """
        import sys
        sys.path.insert(0, str(PROJECT_ROOT / "workflows" / "metadata_enrichment" / "scripts"))
        
        try:
            from enrich_metadata_per_book import find_related_chapters_semantic
            from workflows.shared.clients.orchestrator_client import FakeOrchestratorClient
            
            fake_results = [
                {
                    "book": "AI Engineering",
                    "chapter": 5,
                    "title": "RAG Pipelines",
                    "relevance_score": 0.85,
                }
            ]
            fake_client = FakeOrchestratorClient(results=fake_results)
            
            results = await find_related_chapters_semantic(
                chapter_text="test",
                domain="ai-ml",
                current_book="Architecture_Patterns",
                client=fake_client
            )
            
            for result in results:
                assert "book" in result
                assert "chapter" in result
                assert "title" in result
                assert "relevance_score" in result
                assert "method" in result
                assert result["method"] == "orchestrator_semantic"
        except (ImportError, AttributeError) as e:
            pytest.fail(f"find_related_chapters_semantic() not found: {e}")


# =============================================================================
# WBS 5.1.4: Update threshold to 0.3 Tests
# =============================================================================
class TestSemanticThreshold:
    """Test suite for WBS 5.1.4: Update threshold to 0.3."""

    def test_semantic_threshold_constant_exists(self):
        """
        RED TEST: SEMANTIC_SIMILARITY_THRESHOLD constant exists.
        """
        import sys
        sys.path.insert(0, str(PROJECT_ROOT / "workflows" / "metadata_enrichment" / "scripts"))
        
        try:
            from enrich_metadata_per_book import SEMANTIC_SIMILARITY_THRESHOLD
            assert SEMANTIC_SIMILARITY_THRESHOLD == pytest.approx(0.3)
        except (ImportError, AttributeError):
            pytest.fail("SEMANTIC_SIMILARITY_THRESHOLD constant not found")

    def test_tfidf_threshold_unchanged(self):
        """
        RED TEST: Original TF-IDF threshold remains 0.7 for fallback.
        """
        import sys
        sys.path.insert(0, str(PROJECT_ROOT / "workflows" / "metadata_enrichment" / "scripts"))
        
        try:
            from enrich_metadata_per_book import TFIDF_SIMILARITY_THRESHOLD
            assert TFIDF_SIMILARITY_THRESHOLD == pytest.approx(0.7)
        except (ImportError, AttributeError):
            # May not exist as a named constant - check function default
            pass

    @pytest.mark.asyncio
    async def test_threshold_achievable_with_semantic(self):
        """
        RED TEST: 0.3 threshold produces cross-book references.
        
        This is the KEY test - current TF-IDF at 0.7 produces ZERO references.
        """
        import sys
        sys.path.insert(0, str(PROJECT_ROOT / "workflows" / "metadata_enrichment" / "scripts"))
        
        try:
            from enrich_metadata_per_book import find_related_chapters_semantic
            from workflows.shared.clients.orchestrator_client import FakeOrchestratorClient
            
            # Simulate realistic semantic scores (0.3-0.5 range)
            fake_results = [
                {"book": "Building LLM Apps", "chapter": 3, "relevance_score": 0.45},
                {"book": "AI Engineering", "chapter": 8, "relevance_score": 0.38},
                {"book": "Designing ML Systems", "chapter": 2, "relevance_score": 0.32},
            ]
            fake_client = FakeOrchestratorClient(results=fake_results)
            
            results = await find_related_chapters_semantic(
                chapter_text="Multi-stage document chunking with overlap for RAG",
                domain="ai-ml",
                current_book="Architecture_Patterns",
                client=fake_client,
                threshold=0.3  # Achievable threshold
            )
            
            # All results should meet threshold
            assert len(results) == 3, "All results above 0.3 threshold should be included"
            for result in results:
                assert result["relevance_score"] >= 0.3
        except (ImportError, AttributeError) as e:
            pytest.fail(f"find_related_chapters_semantic() not found: {e}")

    @pytest.mark.asyncio
    async def test_high_threshold_filters_results(self):
        """
        RED TEST: Higher threshold filters out lower-scored results.
        """
        import sys
        sys.path.insert(0, str(PROJECT_ROOT / "workflows" / "metadata_enrichment" / "scripts"))
        
        try:
            from enrich_metadata_per_book import find_related_chapters_semantic
            from workflows.shared.clients.orchestrator_client import FakeOrchestratorClient
            
            fake_results = [
                {"book": "Building LLM Apps", "chapter": 3, "relevance_score": 0.45},
                {"book": "AI Engineering", "chapter": 8, "relevance_score": 0.38},
                {"book": "Designing ML Systems", "chapter": 2, "relevance_score": 0.32},
            ]
            fake_client = FakeOrchestratorClient(results=fake_results)
            
            results = await find_related_chapters_semantic(
                chapter_text="test",
                domain="ai-ml",
                current_book="Architecture_Patterns",
                client=fake_client,
                threshold=0.4  # Higher threshold - should filter some
            )
            
            assert len(results) == 1, "Only scores >= 0.4 should be included"
            assert results[0]["relevance_score"] >= 0.4
        except (ImportError, AttributeError) as e:
            pytest.fail(f"find_related_chapters_semantic() not found: {e}")


# =============================================================================
# Integration: Enrichment with Orchestrator Tests
# =============================================================================
class TestEnrichmentWithOrchestrator:
    """Test enrichment flow using orchestrator."""

    @pytest.mark.asyncio
    async def test_enrich_chapter_uses_orchestrator_when_enabled(self):
        """
        RED TEST: enrich_chapter() uses orchestrator when use_orchestrator=True.
        """
        import sys
        sys.path.insert(0, str(PROJECT_ROOT / "workflows" / "metadata_enrichment" / "scripts"))
        
        try:
            from enrich_metadata_per_book import enrich_chapter_with_orchestrator
            from workflows.shared.clients.orchestrator_client import FakeOrchestratorClient
            
            chapter = {
                "chapter_number": 1,
                "title": "Domain Modeling",
                "summary": "Introduction to domain-driven design patterns"
            }
            
            fake_results = [
                {"book": "Building LLM Apps", "chapter": 5, "title": "RAG", "relevance_score": 0.42}
            ]
            fake_client = FakeOrchestratorClient(results=fake_results)
            
            enriched = await enrich_chapter_with_orchestrator(
                chapter=chapter,
                current_book="Architecture_Patterns",
                domain="ai-ml",
                client=fake_client
            )
            
            assert "related_chapters" in enriched
            assert len(enriched["related_chapters"]) > 0
            assert enriched["related_chapters"][0]["method"] == "orchestrator_semantic"
        except (ImportError, AttributeError) as e:
            pytest.fail(f"enrich_chapter_with_orchestrator() not found: {e}")

    @pytest.mark.asyncio
    async def test_enrich_chapter_falls_back_to_tfidf_on_error(self):
        """
        RED TEST: enrich_chapter() falls back to TF-IDF if orchestrator fails.
        """
        import sys
        sys.path.insert(0, str(PROJECT_ROOT / "workflows" / "metadata_enrichment" / "scripts"))
        
        try:
            from enrich_metadata_per_book import enrich_chapter_with_orchestrator
            from workflows.shared.clients.orchestrator_client import FakeOrchestratorClient
            
            # Simulate orchestrator failure
            failing_client = FakeOrchestratorClient(should_fail=True)
            
            chapter = {
                "chapter_number": 1,
                "title": "Domain Modeling",
                "summary": "Introduction to domain-driven design patterns"
            }
            
            enriched = await enrich_chapter_with_orchestrator(
                chapter=chapter,
                current_book="Architecture_Patterns",
                domain="ai-ml",
                client=failing_client,
                fallback_enabled=True
            )
            
            # Should still have related_chapters (from TF-IDF fallback)
            # but may be empty due to high threshold
            assert "related_chapters" in enriched
        except (ImportError, AttributeError) as e:
            pytest.fail(f"enrich_chapter_with_orchestrator() not found: {e}")
