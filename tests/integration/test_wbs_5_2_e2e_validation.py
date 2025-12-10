#!/usr/bin/env python3
"""
WBS 5.2: E2E Validation Tests

Test-Driven Development (TDD) - RED Phase
Tests for cross-book reference validation and domain filtering.

Reference Documents:
- WBS_IMPLEMENTATION.md: Phase 5.2 - E2E Validation
- TIER_RELATIONSHIP_DIAGRAM.md: Taxonomy tier structure

Acceptance Criteria:
- 5.2.1: At least 1 cross-book ref per book
- 5.2.2: No C++/systems refs in AI books (false positive check)
- 5.2.3: Chicago-style citations generated
"""

import pytest
from pathlib import Path
from typing import Dict, List, Any

PROJECT_ROOT = Path(__file__).parent.parent.parent


# =============================================================================
# WBS 5.2.1: Cross-Book Coverage Validation
# =============================================================================
class TestCrossBookCoverage:
    """Test suite for WBS 5.2.1: Validate cross-book refs."""

    def test_cross_book_ref_exists_in_enriched(self):
        """
        RED TEST: Enriched metadata has cross-book references.
        
        Acceptance Criteria: At least 1 cross-book ref per book
        """
        # Simulated enriched chapter
        enriched_chapter = {
            "chapter_number": 1,
            "title": "Domain Modeling",
            "related_chapters": [
                {
                    "book": "AI Engineering",  # Different book = cross-book
                    "chapter": 5,
                    "title": "RAG Pipelines",
                    "relevance_score": 0.42,
                    "method": "orchestrator_semantic"
                }
            ]
        }
        
        # Check for cross-book refs (book != current book)
        current_book = "Architecture_Patterns_with_Python"
        cross_refs = [
            ref for ref in enriched_chapter.get("related_chapters", [])
            if ref.get("book") != current_book
        ]
        
        assert len(cross_refs) > 0, "Should have at least 1 cross-book reference"

    def test_count_cross_book_refs_helper(self):
        """
        RED TEST: count_cross_book_refs() helper function exists.
        """
        import sys
        sys.path.insert(0, str(PROJECT_ROOT / "workflows" / "metadata_enrichment" / "scripts"))
        
        try:
            from enrich_metadata_per_book import count_cross_book_refs
            
            enriched_data = {
                "book": "Architecture_Patterns_with_Python",
                "chapters": [
                    {
                        "chapter_number": 1,
                        "related_chapters": [
                            {"book": "AI Engineering", "chapter": 5},
                            {"book": "Architecture_Patterns_with_Python", "chapter": 3},  # Same book
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
            
            count = count_cross_book_refs(enriched_data)
            assert count == 2, "Should count 2 cross-book refs (excluding same book)"
        except (ImportError, AttributeError):
            pytest.fail("count_cross_book_refs() function not found")


# =============================================================================
# WBS 5.2.2: False Positive Validation
# =============================================================================
class TestFalsePositiveValidation:
    """Test suite for WBS 5.2.2: Validate no false positives."""

    def test_no_cpp_refs_in_ai_book(self):
        """
        RED TEST: AI domain books should not reference C++ Concurrency.
        
        Acceptance Criteria: No C++/systems refs in AI books
        """
        # C++ books that should NOT appear in AI domain results
        excluded_books = [
            "C++ Concurrency in Action",
            "C++_Concurrency",
            "Systems Programming",
        ]
        
        # Simulated enriched chapter from AI domain
        enriched_chapter = {
            "related_chapters": [
                {"book": "AI Engineering", "chapter": 5, "relevance_score": 0.45},
                {"book": "Building LLM Apps", "chapter": 3, "relevance_score": 0.38},
            ]
        }
        
        for ref in enriched_chapter["related_chapters"]:
            for excluded in excluded_books:
                assert excluded not in ref.get("book", ""), \
                    f"False positive: {ref['book']} should not appear in AI domain"

    def test_is_relevant_domain_helper(self):
        """
        RED TEST: is_relevant_domain() helper function exists.
        """
        import sys
        sys.path.insert(0, str(PROJECT_ROOT / "workflows" / "metadata_enrichment" / "scripts"))
        
        try:
            from enrich_metadata_per_book import is_relevant_domain
            
            # AI domain ref
            ai_ref = {"book": "AI Engineering", "chapter": 5}
            assert is_relevant_domain(ai_ref, expected_domain="ai-ml") is True
            
            # C++ ref - should NOT be relevant to ai-ml domain
            cpp_ref = {"book": "C++ Concurrency in Action", "chapter": 3}
            assert is_relevant_domain(cpp_ref, expected_domain="ai-ml") is False
        except (ImportError, AttributeError):
            pytest.fail("is_relevant_domain() function not found")

    def test_domain_filter_applies_during_enrichment(self):
        """
        RED TEST: Domain filtering is applied during enrichment.
        """
        import sys
        sys.path.insert(0, str(PROJECT_ROOT / "workflows" / "metadata_enrichment" / "scripts"))
        
        try:
            from enrich_metadata_per_book import filter_by_domain
            
            results = [
                {"book": "AI Engineering", "chapter": 5, "relevance_score": 0.45},
                {"book": "C++ Concurrency", "chapter": 3, "relevance_score": 0.40},
                {"book": "Building LLM Apps", "chapter": 8, "relevance_score": 0.35},
            ]
            
            filtered = filter_by_domain(results, domain="ai-ml")
            
            # Should exclude C++ book
            assert len(filtered) == 2
            book_names = [r["book"] for r in filtered]
            assert "C++ Concurrency" not in book_names
        except (ImportError, AttributeError):
            pytest.fail("filter_by_domain() function not found")


# =============================================================================
# WBS 5.2.3: Citation Format Validation
# =============================================================================
class TestCitationFormat:
    """Test suite for WBS 5.2.3: Validate citation quality."""

    def test_generate_chicago_citation_exists(self):
        """
        RED TEST: generate_chicago_citation() function exists.
        """
        import sys
        sys.path.insert(0, str(PROJECT_ROOT / "workflows" / "metadata_enrichment" / "scripts"))
        
        try:
            from enrich_metadata_per_book import generate_chicago_citation
            assert callable(generate_chicago_citation)
        except (ImportError, AttributeError):
            pytest.fail("generate_chicago_citation() function not found")

    def test_chicago_citation_format(self):
        """
        RED TEST: Citation follows Chicago author-date style.
        
        Format: Author, "Chapter Title," in Book Title (Year), page.
        """
        import sys
        sys.path.insert(0, str(PROJECT_ROOT / "workflows" / "metadata_enrichment" / "scripts"))
        
        try:
            from enrich_metadata_per_book import generate_chicago_citation
            
            ref = {
                "book": "AI Engineering Building Applications",
                "chapter": 5,
                "title": "RAG Pipelines",
                "author": "Chip Huyen",
                "start_page": 150,
                "end_page": 175
            }
            
            citation = generate_chicago_citation(ref)
            
            # Verify Chicago style components
            assert "Huyen" in citation, "Should include author surname"
            assert "RAG Pipelines" in citation, "Should include chapter title"
            assert "AI Engineering" in citation, "Should include book title"
            assert "150" in citation, "Should include page number"
        except (ImportError, AttributeError):
            pytest.fail("generate_chicago_citation() function not found")

    def test_enriched_chapter_has_citation(self):
        """
        RED TEST: Enriched related_chapters include citation field.
        """
        import sys
        sys.path.insert(0, str(PROJECT_ROOT / "workflows" / "metadata_enrichment" / "scripts"))
        
        try:
            from enrich_metadata_per_book import add_citations_to_refs
            
            related_chapters = [
                {
                    "book": "AI Engineering",
                    "chapter": 5,
                    "title": "RAG Pipelines",
                    "relevance_score": 0.42
                }
            ]
            
            # Book metadata lookup
            book_metadata = {
                "AI Engineering": {
                    "author": "Chip Huyen",
                    "chapters": {
                        5: {"start_page": 150, "end_page": 175}
                    }
                }
            }
            
            enriched = add_citations_to_refs(related_chapters, book_metadata)
            
            assert "citation" in enriched[0], "Related chapter should have citation field"
        except (ImportError, AttributeError):
            pytest.fail("add_citations_to_refs() function not found")


# =============================================================================
# Phase 5 Integration Test (from WBS_IMPLEMENTATION.md)
# =============================================================================
class TestPhase5Integration:
    """Integration test matching WBS_IMPLEMENTATION.md Phase 5 test."""

    @pytest.mark.asyncio
    async def test_phase5_e2e_enrichment(self):
        """
        Phase 5 Integration Test from WBS_IMPLEMENTATION.md.
        
        Full E2E: enrichment produces valid cross-book references.
        """
        import sys
        sys.path.insert(0, str(PROJECT_ROOT / "workflows" / "metadata_enrichment" / "scripts"))
        
        try:
            from enrich_metadata_per_book import (
                run_enrichment_with_orchestrator,
                count_cross_book_refs,
                is_relevant_domain,
            )
            from workflows.shared.clients.orchestrator_client import FakeOrchestratorClient
            
            # Books to test
            books = [
                "Architecture_Patterns_with_Python",
                "Building_LLM_Powered_Applications",
                "AI_Engineering_Building_Applications"
            ]
            
            # Fake client with realistic cross-book results
            fake_results = [
                {"book": "AI Engineering", "chapter": 5, "title": "RAG", "relevance_score": 0.45},
                {"book": "Building LLM Apps", "chapter": 3, "title": "Chunking", "relevance_score": 0.40},
            ]
            fake_client = FakeOrchestratorClient(results=fake_results)
            
            for book in books:
                enriched = await run_enrichment_with_orchestrator(
                    book_name=book,
                    domain="ai-ml",
                    client=fake_client
                )
                
                # Count cross-book references
                cross_refs = count_cross_book_refs(enriched)
                assert cross_refs > 0, f"{book} has no cross-book references"
                
                # Validate domain relevance
                for chapter in enriched.get("chapters", []):
                    for ref in chapter.get("related_chapters", []):
                        assert is_relevant_domain(ref, expected_domain="ai-ml"), \
                            f"Invalid domain in {book}: {ref.get('book')}"
        except (ImportError, AttributeError) as e:
            pytest.fail(f"Phase 5 integration functions not found: {e}")

    @pytest.mark.asyncio
    async def test_orchestrator_results_meet_relevance_threshold(self):
        """
        RED TEST: All orchestrator results meet 0.3 relevance threshold.
        """
        import sys
        sys.path.insert(0, str(PROJECT_ROOT / "workflows" / "metadata_enrichment" / "scripts"))
        
        try:
            from enrich_metadata_per_book import (
                find_related_chapters_semantic,
                SEMANTIC_SIMILARITY_THRESHOLD,
            )
            from workflows.shared.clients.orchestrator_client import FakeOrchestratorClient
            
            fake_results = [
                {"book": "AI Engineering", "chapter": 5, "relevance_score": 0.45},
                {"book": "Building LLM Apps", "chapter": 3, "relevance_score": 0.38},
            ]
            fake_client = FakeOrchestratorClient(results=fake_results)
            
            results = await find_related_chapters_semantic(
                chapter_text="Multi-stage document chunking with overlap for RAG",
                domain="ai-ml",
                current_book="Architecture_Patterns",
                client=fake_client
            )
            
            # All results should meet threshold
            for result in results:
                assert result["relevance_score"] >= SEMANTIC_SIMILARITY_THRESHOLD, \
                    f"Score {result['relevance_score']} below threshold {SEMANTIC_SIMILARITY_THRESHOLD}"
        except (ImportError, AttributeError) as e:
            pytest.fail(f"find_related_chapters_semantic() not found: {e}")
