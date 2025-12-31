"""
Unit tests for tier_relationship_engine.py - TDD RED Phase

Tests for tier-aware cross-referencing that supports:
- Parallel relationships (within same tier)
- Perpendicular relationships (adjacent tiers: 1↔2, 2↔3)
- Skip-tier relationships (non-adjacent tiers: 1↔3)
- Meta-cross-references (2nd-hop transitive: A→B→C implies A→C)

Reference Documents:
- BOOK_TAXONOMY_MATRIX.md: 3-tier structure (Architecture, Implementation, Practices)
- DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md: Phase 2 similarity computation
- Architecture Patterns with Python Ch. 2: Repository Pattern
- Architecture Patterns with Python Ch. 8: Event-driven patterns

Architecture Patterns Applied:
- Strategy Pattern: Different relationship classification strategies
- Repository Pattern: Graph-based relationship storage
- Service Layer Pattern: TierRelationshipEngine orchestrates classification

Sprint: Tier-Aware Cross-Referencing Enhancement
"""

import pytest
import sys
from pathlib import Path
from typing import Dict, List, Any
from unittest.mock import Mock, patch

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================================
# TIER MAP FIXTURE - From BOOK_TAXONOMY_MATRIX.md
# ============================================================================

TIER_MAP: Dict[str, int] = {
    # Tier 1: Architecture Spine (4 books)
    "Architecture_Patterns_with_Python.json": 1,
    "Building_Microservices.json": 1,
    "Microservice_Architecture.json": 1,
    "Python_Architecture_Patterns.json": 1,
    # Tier 2: Implementation (4 books)
    "Building_Python_Microservices_with_FastAPI.json": 2,
    "Microservice_APIs_Using_Python_Flask_FastAPI.json": 2,
    "Python_Microservices_Development.json": 2,
    "Microservices_Up_and_Running.json": 2,
    # Tier 3: Engineering Practices (6 books)
    "Fluent_Python_2nd.json": 3,
    "Python_Distilled.json": 3,
    "Python_Cookbook_3rd.json": 3,
    "Python_Essential_Reference_4th.json": 3,
    "Python_Data_Analysis_3rd.json": 3,
    "Learning_Python_Ed6.json": 3,
}


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def tier_map():
    """3-tier taxonomy map from BOOK_TAXONOMY_MATRIX.md."""
    return TIER_MAP.copy()


@pytest.fixture
def sample_similarity_results():
    """Sample output from find_related_chapters (existing flat similarity)."""
    return [
        {"book": "Fluent_Python_2nd.json", "chapter": 7, "similarity": 0.85, "title": "Decorators and Closures"},
        {"book": "Building_Microservices.json", "chapter": 4, "similarity": 0.72, "title": "Integration Patterns"},
        {"book": "Python_Cookbook_3rd.json", "chapter": 9, "similarity": 0.68, "title": "Metaprogramming"},
        {"book": "Building_Python_Microservices_with_FastAPI.json", "chapter": 3, "similarity": 0.65, "title": "Async Patterns"},
    ]


@pytest.fixture
def sample_graph_edges():
    """Sample edges for NetworkX graph from taxonomy cascades."""
    # From BOOK_TAXONOMY_MATRIX.md cascade chains
    return [
        ("Architecture_Patterns_with_Python.json", "Building_Python_Microservices_with_FastAPI.json"),
        ("Architecture_Patterns_with_Python.json", "Python_Architecture_Patterns.json"),
        ("Building_Microservices.json", "Microservices_Up_and_Running.json"),
        ("Building_Microservices.json", "Python_Microservices_Development.json"),
        ("Building_Python_Microservices_with_FastAPI.json", "Microservice_APIs_Using_Python_Flask_FastAPI.json"),
        ("Building_Python_Microservices_with_FastAPI.json", "Python_Distilled.json"),
        ("Fluent_Python_2nd.json", "Python_Distilled.json"),
        ("Fluent_Python_2nd.json", "Python_Essential_Reference_4th.json"),
    ]


# ============================================================================
# RED PHASE: TEST TIER RELATIONSHIP CLASSIFICATION
# ============================================================================

class TestTierRelationshipClassification:
    """
    RED Phase: Tests for classifying relationship types between books.
    
    Relationship Types:
    - parallel: Same tier (e.g., Tier 1 ↔ Tier 1)
    - perpendicular: Adjacent tiers (e.g., Tier 1 ↔ Tier 2)
    - skip_tier: Non-adjacent tiers (e.g., Tier 1 ↔ Tier 3)
    
    Reference: BOOK_TAXONOMY_MATRIX.md - Cascading Logic section
    """

    def test_classify_parallel_relationship_same_tier(self, tier_map):
        """
        RED: Classify relationship between two Tier 1 books as 'parallel'.
        
        Example: Architecture Patterns with Python ↔ Building Microservices
        Both are Tier 1 (Architecture Spine), so relationship is parallel.
        """
        from workflows.metadata_enrichment.scripts.tier_relationship_engine import (
            TierRelationshipEngine
        )
        
        engine = TierRelationshipEngine(tier_map)
        
        relationship = engine.classify_relationship(
            source_book="Architecture_Patterns_with_Python.json",
            target_book="Building_Microservices.json"
        )
        
        assert relationship == "parallel", \
            "Two Tier 1 books should have 'parallel' relationship"

    def test_classify_perpendicular_relationship_adjacent_tiers(self, tier_map):
        """
        RED: Classify relationship between Tier 1 and Tier 2 books as 'perpendicular'.
        
        Example: Architecture Patterns with Python ↔ Building Python Microservices with FastAPI
        Tier 1 → Tier 2 is an adjacent tier transition.
        """
        from workflows.metadata_enrichment.scripts.tier_relationship_engine import (
            TierRelationshipEngine
        )
        
        engine = TierRelationshipEngine(tier_map)
        
        relationship = engine.classify_relationship(
            source_book="Architecture_Patterns_with_Python.json",
            target_book="Building_Python_Microservices_with_FastAPI.json"
        )
        
        assert relationship == "perpendicular", \
            "Tier 1 → Tier 2 should be 'perpendicular' relationship"

    def test_classify_skip_tier_relationship_non_adjacent(self, tier_map):
        """
        RED: Classify relationship between Tier 1 and Tier 3 books as 'skip_tier'.
        
        Example: Architecture Patterns with Python ↔ Fluent Python 2nd
        Tier 1 → Tier 3 skips Tier 2 (non-adjacent).
        """
        from workflows.metadata_enrichment.scripts.tier_relationship_engine import (
            TierRelationshipEngine
        )
        
        engine = TierRelationshipEngine(tier_map)
        
        relationship = engine.classify_relationship(
            source_book="Architecture_Patterns_with_Python.json",
            target_book="Fluent_Python_2nd.json"
        )
        
        assert relationship == "skip_tier", \
            "Tier 1 → Tier 3 should be 'skip_tier' relationship"

    def test_classify_unknown_book_returns_unknown(self, tier_map):
        """
        RED: Handle books not in tier map gracefully.
        
        When a book isn't in the taxonomy, return 'unknown' relationship.
        """
        from workflows.metadata_enrichment.scripts.tier_relationship_engine import (
            TierRelationshipEngine
        )
        
        engine = TierRelationshipEngine(tier_map)
        
        relationship = engine.classify_relationship(
            source_book="Unknown_Book.json",
            target_book="Fluent_Python_2nd.json"
        )
        
        assert relationship == "unknown", \
            "Unknown books should return 'unknown' relationship"


# ============================================================================
# RED PHASE: TEST SIMILARITY ENHANCEMENT WITH TIER CLASSIFICATION
# ============================================================================

class TestSimilarityEnhancement:
    """
    RED Phase: Tests for enhancing find_related_chapters output with tier info.
    
    The engine wraps existing similarity results and adds:
    - relationship_type: parallel/perpendicular/skip_tier
    - tier_distance: 0 (same), 1 (adjacent), 2 (skip)
    - discovery_threshold: Lower threshold for cross-tier discovery
    
    Reference: enrich_metadata_per_book.py find_related_chapters (lines 258-326)
    """

    def test_enhance_with_relationship_types(self, tier_map, sample_similarity_results):
        """
        RED: Enhance similarity results with relationship type classification.
        
        Each result should include 'relationship_type' field.
        """
        from workflows.metadata_enrichment.scripts.tier_relationship_engine import (
            TierRelationshipEngine
        )
        
        engine = TierRelationshipEngine(tier_map)
        source_book = "Architecture_Patterns_with_Python.json"
        
        enhanced = engine.enhance_similarity_results(
            source_book=source_book,
            similarity_results=sample_similarity_results
        )
        
        # All results should have relationship_type
        for result in enhanced:
            assert "relationship_type" in result, \
                f"Missing 'relationship_type' in result: {result}"
        
        # Check specific relationships
        fluent_python = next(r for r in enhanced if "Fluent_Python" in r["book"])
        assert fluent_python["relationship_type"] == "skip_tier", \
            "Tier 1 → Tier 3 should be skip_tier"
        
        building_microservices = next(r for r in enhanced if "Building_Microservices" in r["book"])
        assert building_microservices["relationship_type"] == "parallel", \
            "Tier 1 → Tier 1 should be parallel"

    def test_enhance_with_tier_distance(self, tier_map, sample_similarity_results):
        """
        RED: Add tier_distance to similarity results.
        
        tier_distance: 0 = same tier, 1 = adjacent, 2 = skip
        """
        from workflows.metadata_enrichment.scripts.tier_relationship_engine import (
            TierRelationshipEngine
        )
        
        engine = TierRelationshipEngine(tier_map)
        source_book = "Architecture_Patterns_with_Python.json"
        
        enhanced = engine.enhance_similarity_results(
            source_book=source_book,
            similarity_results=sample_similarity_results
        )
        
        for result in enhanced:
            assert "tier_distance" in result, \
                f"Missing 'tier_distance' in result: {result}"
        
        # Fluent Python is Tier 3, source is Tier 1 → distance = 2
        fluent_python = next(r for r in enhanced if "Fluent_Python" in r["book"])
        assert fluent_python["tier_distance"] == 2

    def test_lower_threshold_for_cross_tier_discovery(self, tier_map):
        """
        RED: Use lower similarity threshold (0.5) for cross-tier relationships.
        
        Current find_related_chapters uses 0.7 threshold.
        For cross-tier discovery, lower to 0.5 to find more connections.
        """
        from workflows.metadata_enrichment.scripts.tier_relationship_engine import (
            TierRelationshipEngine
        )
        
        engine = TierRelationshipEngine(tier_map)
        
        # Get recommended threshold for cross-tier
        threshold = engine.get_discovery_threshold(
            source_tier=1,
            target_tier=3
        )
        
        assert threshold == pytest.approx(0.5), \
            "Cross-tier (Tier 1 → Tier 3) should use 0.5 threshold"
        
        # Same tier should use standard threshold
        same_tier_threshold = engine.get_discovery_threshold(
            source_tier=1,
            target_tier=1
        )
        
        assert same_tier_threshold == pytest.approx(0.7), \
            "Same tier should use standard 0.7 threshold"


# ============================================================================
# RED PHASE: TEST META-CROSS-REFERENCES (2ND-HOP DISCOVERY)
# ============================================================================

class TestMetaCrossReferences:
    """
    RED Phase: Tests for 2nd-hop transitive relationship discovery.
    
    Meta-cross-reference: If A → B and B → C, then A → C (transitive).
    Uses NetworkX for graph traversal.
    
    Reference: BOOK_TAXONOMY_MATRIX.md - Cascade Chains section
    Example: Architecture Patterns → FastAPI → Flask/FastAPI → Cookbook
    """

    def test_discover_second_hop_relationships(self, tier_map, sample_graph_edges):
        """
        RED: Discover 2nd-hop transitive relationships.
        
        Given: Architecture Patterns → FastAPI (direct)
               FastAPI → Flask/FastAPI (direct)
        Expect: Architecture Patterns → Flask/FastAPI (2nd-hop)
        """
        from workflows.metadata_enrichment.scripts.tier_relationship_engine import (
            TierRelationshipEngine
        )
        
        engine = TierRelationshipEngine(tier_map, cascade_edges=sample_graph_edges)
        
        second_hop = engine.discover_second_hop(
            source_book="Architecture_Patterns_with_Python.json"
        )
        
        # Should include 2nd-hop targets
        assert "Microservice_APIs_Using_Python_Flask_FastAPI.json" in second_hop, \
            "Should discover Flask/FastAPI as 2nd-hop via FastAPI"
        
        # Should include Python_Distilled (FastAPI → Python_Distilled)
        assert "Python_Distilled.json" in second_hop, \
            "Should discover Python Distilled as 2nd-hop via FastAPI"

    def test_exclude_direct_relationships_from_second_hop(self, tier_map, sample_graph_edges):
        """
        RED: 2nd-hop results should exclude direct (1st-hop) relationships.
        
        Direct edges are not meta-cross-references.
        """
        from workflows.metadata_enrichment.scripts.tier_relationship_engine import (
            TierRelationshipEngine
        )
        
        engine = TierRelationshipEngine(tier_map, cascade_edges=sample_graph_edges)
        
        second_hop = engine.discover_second_hop(
            source_book="Architecture_Patterns_with_Python.json"
        )
        
        # Direct edges should NOT be in 2nd-hop results
        assert "Building_Python_Microservices_with_FastAPI.json" not in second_hop, \
            "Direct relationship should not appear in 2nd-hop results"
        assert "Python_Architecture_Patterns.json" not in second_hop, \
            "Direct relationship should not appear in 2nd-hop results"

    def test_second_hop_uses_networkx_graph(self, tier_map, sample_graph_edges):
        """
        RED: Verify NetworkX is used for graph traversal.
        
        Engine should build a NetworkX DiGraph from cascade edges.
        """
        from workflows.metadata_enrichment.scripts.tier_relationship_engine import (
            TierRelationshipEngine
        )
        import networkx as nx
        
        engine = TierRelationshipEngine(tier_map, cascade_edges=sample_graph_edges)
        
        # Should have internal graph
        assert hasattr(engine, '_graph'), \
            "Engine should have internal NetworkX graph"
        assert isinstance(engine._graph, nx.DiGraph), \
            "Internal graph should be NetworkX DiGraph"
        
        # Graph should have correct edges
        assert engine._graph.number_of_edges() == len(sample_graph_edges), \
            f"Graph should have {len(sample_graph_edges)} edges"

    def test_second_hop_with_no_transitive_paths(self, tier_map):
        """
        RED: Handle case where no 2nd-hop relationships exist.
        
        Isolated nodes should return empty 2nd-hop results.
        """
        from workflows.metadata_enrichment.scripts.tier_relationship_engine import (
            TierRelationshipEngine
        )
        
        # Create engine with minimal edges
        minimal_edges = [
            ("Architecture_Patterns_with_Python.json", "Python_Architecture_Patterns.json")
        ]
        engine = TierRelationshipEngine(tier_map, cascade_edges=minimal_edges)
        
        second_hop = engine.discover_second_hop(
            source_book="Architecture_Patterns_with_Python.json"
        )
        
        # No 2nd-hop available (Python_Architecture_Patterns has no outgoing edges)
        assert second_hop == [], \
            "Should return empty list when no 2nd-hop paths exist"


# ============================================================================
# RED PHASE: TEST FULL WORKFLOW INTEGRATION
# ============================================================================

class TestFullWorkflowIntegration:
    """
    RED Phase: Tests for full workflow integration.
    
    Tests the complete pipeline:
    1. Receive similarity results from find_related_chapters
    2. Classify each relationship by tier
    3. Enhance with 2nd-hop discovery
    4. Return enriched results
    
    Reference: enrich_metadata_per_book.py _enrich_single_chapter
    """

    def test_full_enhancement_pipeline(self, tier_map, sample_similarity_results, sample_graph_edges):
        """
        RED: Test complete enhancement pipeline.
        
        Input: Raw similarity results from find_related_chapters
        Output: Enhanced results with tier info, relationship types, 2nd-hop
        """
        from workflows.metadata_enrichment.scripts.tier_relationship_engine import (
            TierRelationshipEngine
        )
        
        engine = TierRelationshipEngine(tier_map, cascade_edges=sample_graph_edges)
        source_book = "Architecture_Patterns_with_Python.json"
        
        enhanced = engine.enhance_and_discover(
            source_book=source_book,
            similarity_results=sample_similarity_results,
            include_second_hop=True
        )
        
        # Should have all original results
        assert len(enhanced["direct_relationships"]) == len(sample_similarity_results)
        
        # Should have 2nd-hop discovery
        assert "second_hop_discoveries" in enhanced
        assert len(enhanced["second_hop_discoveries"]) > 0
        
        # Should include relationship metadata
        for result in enhanced["direct_relationships"]:
            assert "relationship_type" in result
            assert "tier_distance" in result

    def test_group_results_by_relationship_type(self, tier_map, sample_similarity_results):
        """
        RED: Group enhanced results by relationship type.
        
        Returns dict with keys: parallel, perpendicular, skip_tier
        """
        from workflows.metadata_enrichment.scripts.tier_relationship_engine import (
            TierRelationshipEngine
        )
        
        engine = TierRelationshipEngine(tier_map)
        source_book = "Architecture_Patterns_with_Python.json"
        
        grouped = engine.group_by_relationship_type(
            source_book=source_book,
            similarity_results=sample_similarity_results
        )
        
        assert "parallel" in grouped
        assert "perpendicular" in grouped
        assert "skip_tier" in grouped
        
        # Building_Microservices should be in parallel (Tier 1 → Tier 1)
        parallel_books = [r["book"] for r in grouped["parallel"]]
        assert "Building_Microservices.json" in parallel_books
        
        # FastAPI should be in perpendicular (Tier 1 → Tier 2)
        perpendicular_books = [r["book"] for r in grouped["perpendicular"]]
        assert "Building_Python_Microservices_with_FastAPI.json" in perpendicular_books
        
        # Fluent Python should be in skip_tier (Tier 1 → Tier 3)
        skip_tier_books = [r["book"] for r in grouped["skip_tier"]]
        assert "Fluent_Python_2nd.json" in skip_tier_books


# ============================================================================
# RED PHASE: TEST EDGE CASES
# ============================================================================

class TestEdgeCases:
    """
    RED Phase: Tests for edge cases and error handling.
    """

    def test_empty_similarity_results(self, tier_map):
        """
        RED: Handle empty similarity results gracefully.
        """
        from workflows.metadata_enrichment.scripts.tier_relationship_engine import (
            TierRelationshipEngine
        )
        
        engine = TierRelationshipEngine(tier_map)
        
        enhanced = engine.enhance_similarity_results(
            source_book="Architecture_Patterns_with_Python.json",
            similarity_results=[]
        )
        
        assert enhanced == [], "Empty input should return empty output"

    def test_empty_tier_map(self, sample_similarity_results):
        """
        RED: Handle empty tier map gracefully.
        """
        from workflows.metadata_enrichment.scripts.tier_relationship_engine import (
            TierRelationshipEngine
        )
        
        engine = TierRelationshipEngine({})
        
        enhanced = engine.enhance_similarity_results(
            source_book="Architecture_Patterns_with_Python.json",
            similarity_results=sample_similarity_results
        )
        
        # All relationships should be 'unknown' with empty tier map
        for result in enhanced:
            assert result["relationship_type"] == "unknown"

    def test_no_cascade_edges_second_hop(self, tier_map):
        """
        RED: Handle 2nd-hop discovery when no cascade edges provided.
        """
        from workflows.metadata_enrichment.scripts.tier_relationship_engine import (
            TierRelationshipEngine
        )
        
        engine = TierRelationshipEngine(tier_map)  # No cascade_edges
        
        second_hop = engine.discover_second_hop(
            source_book="Architecture_Patterns_with_Python.json"
        )
        
        assert second_hop == [], "No cascade edges should return empty 2nd-hop"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
