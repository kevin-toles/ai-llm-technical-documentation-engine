"""
tier_relationship_engine.py - Tier-Aware Cross-Referencing Engine

Enhances cross-book similarity results with tier classification:
- Parallel: Same tier (e.g., Tier 1 ↔ Tier 1)
- Perpendicular: Adjacent tiers (e.g., Tier 1 ↔ Tier 2)
- Skip-tier: Non-adjacent tiers (e.g., Tier 1 ↔ Tier 3)
- Meta-cross-references: 2nd-hop transitive discovery (A→B→C implies A→C)

This module wraps the output of find_related_chapters (enrich_metadata_per_book.py)
and adds tier-awareness using NetworkX for graph operations.

Reference Documents:
- BOOK_TAXONOMY_MATRIX.md: 3-tier taxonomy structure
- DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md: Phase 2 similarity computation
- Architecture Patterns with Python Ch. 2: Repository Pattern
- Architecture Patterns with Python Ch. 8: Event-driven patterns

Architecture Patterns Applied:
- Strategy Pattern: Relationship classification based on tier distance
- Repository Pattern: Graph-based relationship storage
- Service Layer Pattern: Orchestrates classification and discovery

Dependencies:
- networkx: Graph operations for 2nd-hop traversal
- scikit-learn: NOT used here (similarity computation stays in enrich_metadata_per_book.py)

Author: TDD Implementation following MASTER_IMPLEMENTATION_GUIDE.md
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field

# NetworkX is optional - gracefully handle if not installed
try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    nx = None  # type: ignore
    NETWORKX_AVAILABLE = False


# ============================================================================
# TYPE DEFINITIONS
# ============================================================================

@dataclass
class RelationshipInfo:
    """Information about a tier-based relationship.
    
    Attributes:
        relationship_type: One of parallel, perpendicular, skip_tier, unknown
        tier_distance: 0 for same tier, 1 for adjacent, 2 for skip-tier
    """
    relationship_type: str
    tier_distance: int
    source_tier: Optional[int] = None
    target_tier: Optional[int] = None


# ============================================================================
# CONSTANTS
# ============================================================================

# Relationship type constants
PARALLEL = "parallel"
PERPENDICULAR = "perpendicular"
SKIP_TIER = "skip_tier"
UNKNOWN = "unknown"

# Threshold constants (from analysis of enrich_metadata_per_book.py)
DEFAULT_THRESHOLD = 0.7  # Current threshold in find_related_chapters
CROSS_TIER_THRESHOLD = 0.5  # Lower threshold for cross-tier discovery


# ============================================================================
# TIER RELATIONSHIP ENGINE
# ============================================================================

class TierRelationshipEngine:
    """
    Engine for tier-aware cross-referencing.
    
    Wraps existing find_related_chapters output and enhances with:
    - Relationship type classification (parallel/perpendicular/skip_tier)
    - Tier distance calculation
    - 2nd-hop discovery using NetworkX graph traversal
    
    Usage:
        >>> tier_map = {"Book_A.json": 1, "Book_B.json": 2}
        >>> engine = TierRelationshipEngine(tier_map)
        >>> enhanced = engine.enhance_similarity_results("Book_A.json", results)
    
    Reference: BOOK_TAXONOMY_MATRIX.md for tier definitions
    """
    
    def __init__(
        self,
        tier_map: Dict[str, int],
        cascade_edges: Optional[List[Tuple[str, str]]] = None
    ) -> None:
        """
        Initialize TierRelationshipEngine.
        
        Args:
            tier_map: Mapping of book filename to tier number (1, 2, or 3)
            cascade_edges: Optional list of (source, target) tuples for cascade graph
        
        Example:
            >>> tier_map = {
            ...     "Architecture_Patterns_with_Python.json": 1,
            ...     "FastAPI.json": 2,
            ...     "Fluent_Python.json": 3
            ... }
            >>> engine = TierRelationshipEngine(tier_map)
        """
        self._tier_map = tier_map or {}
        self._graph: Optional[Any] = None
        
        # Build NetworkX graph if edges provided and library available
        if cascade_edges and NETWORKX_AVAILABLE:
            self._graph = nx.DiGraph()
            self._graph.add_edges_from(cascade_edges)
        elif cascade_edges and not NETWORKX_AVAILABLE:
            # Fallback: store edges as adjacency list
            self._graph = self._build_adjacency_list(cascade_edges)
    
    def _build_adjacency_list(
        self,
        edges: List[Tuple[str, str]]
    ) -> Dict[str, List[str]]:
        """Build simple adjacency list when NetworkX not available."""
        adj: Dict[str, List[str]] = {}
        for source, target in edges:
            if source not in adj:
                adj[source] = []
            adj[source].append(target)
        return adj
    
    # ========================================================================
    # RELATIONSHIP CLASSIFICATION
    # ========================================================================
    
    def classify_relationship(
        self,
        source_book: str,
        target_book: str
    ) -> str:
        """
        Classify the relationship type between two books based on tier distance.
        
        Args:
            source_book: Source book filename
            target_book: Target book filename
        
        Returns:
            Relationship type: 'parallel', 'perpendicular', 'skip_tier', or 'unknown'
        
        Example:
            >>> engine.classify_relationship(
            ...     "Architecture_Patterns_with_Python.json",
            ...     "Building_Microservices.json"
            ... )
            'parallel'  # Both Tier 1
        """
        source_tier = self._tier_map.get(source_book)
        target_tier = self._tier_map.get(target_book)
        
        if source_tier is None or target_tier is None:
            return UNKNOWN
        
        tier_distance = abs(source_tier - target_tier)
        
        if tier_distance == 0:
            return PARALLEL
        elif tier_distance == 1:
            return PERPENDICULAR
        else:
            return SKIP_TIER
    
    def _get_relationship_info(
        self,
        source_book: str,
        target_book: str
    ) -> RelationshipInfo:
        """Get detailed relationship information."""
        source_tier = self._tier_map.get(source_book)
        target_tier = self._tier_map.get(target_book)
        
        if source_tier is None or target_tier is None:
            return RelationshipInfo(
                relationship_type=UNKNOWN,
                tier_distance=-1,
                source_tier=source_tier,
                target_tier=target_tier
            )
        
        tier_distance = abs(source_tier - target_tier)
        
        if tier_distance == 0:
            rel_type = PARALLEL
        elif tier_distance == 1:
            rel_type = PERPENDICULAR
        else:
            rel_type = SKIP_TIER
        
        return RelationshipInfo(
            relationship_type=rel_type,
            tier_distance=tier_distance,
            source_tier=source_tier,
            target_tier=target_tier
        )
    
    # ========================================================================
    # SIMILARITY ENHANCEMENT
    # ========================================================================
    
    def enhance_similarity_results(
        self,
        source_book: str,
        similarity_results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Enhance similarity results with tier relationship information.
        
        Takes output from find_related_chapters and adds:
        - relationship_type: parallel/perpendicular/skip_tier/unknown
        - tier_distance: 0, 1, 2, or -1 for unknown
        
        Args:
            source_book: Source book filename
            similarity_results: List of dicts from find_related_chapters
        
        Returns:
            Enhanced list with relationship info added to each result
        
        Example:
            >>> results = [{"book": "Fluent_Python.json", "similarity": 0.8}]
            >>> enhanced = engine.enhance_similarity_results("Architecture.json", results)
            >>> enhanced[0]["relationship_type"]
            'skip_tier'
        """
        if not similarity_results:
            return []
        
        enhanced = []
        for result in similarity_results:
            # Create a copy to avoid mutating original
            enhanced_result = result.copy()
            
            target_book = result.get("book", "")
            info = self._get_relationship_info(source_book, target_book)
            
            enhanced_result["relationship_type"] = info.relationship_type
            enhanced_result["tier_distance"] = info.tier_distance
            
            enhanced.append(enhanced_result)
        
        return enhanced
    
    def get_discovery_threshold(
        self,
        source_tier: int,
        target_tier: int
    ) -> float:
        """
        Get recommended similarity threshold for tier combination.
        
        Same tier uses standard 0.7 threshold.
        Cross-tier uses lower 0.5 threshold for broader discovery.
        
        Args:
            source_tier: Source book tier (1, 2, or 3)
            target_tier: Target book tier (1, 2, or 3)
        
        Returns:
            Recommended threshold (0.5 for cross-tier, 0.7 for same tier)
        """
        if source_tier == target_tier:
            return DEFAULT_THRESHOLD
        return CROSS_TIER_THRESHOLD
    
    # ========================================================================
    # 2ND-HOP DISCOVERY (META-CROSS-REFERENCES)
    # ========================================================================
    
    def _traverse_networkx_graph(
        self,
        source_book: str
    ) -> List[str]:
        """Traverse NetworkX graph for 2nd-hop discovery."""
        direct_neighbors = set(self._graph.successors(source_book))
        second_hop = self._collect_second_hop_neighbors(
            direct_neighbors,
            lambda n: self._graph.successors(n),
            source_book
        )
        return list(second_hop - direct_neighbors)
    
    def _traverse_adjacency_list(
        self,
        source_book: str
    ) -> List[str]:
        """Traverse adjacency list for 2nd-hop discovery (fallback)."""
        direct_neighbors = set(self._graph.get(source_book, []))
        second_hop = self._collect_second_hop_neighbors(
            direct_neighbors,
            lambda n: self._graph.get(n, []),
            source_book
        )
        return list(second_hop - direct_neighbors)
    
    def _collect_second_hop_neighbors(
        self,
        direct_neighbors: set,
        get_neighbors_fn,
        source_book: str
    ) -> set:
        """Collect 2nd-hop neighbors using provided neighbor function."""
        second_hop = set()
        for neighbor in direct_neighbors:
            for second_neighbor in get_neighbors_fn(neighbor):
                if second_neighbor != source_book:
                    second_hop.add(second_neighbor)
        return second_hop
    
    def discover_second_hop(
        self,
        source_book: str
    ) -> List[str]:
        """
        Discover 2nd-hop transitive relationships.
        
        If A → B and B → C, then A → C is a 2nd-hop relationship.
        Uses NetworkX BFS for graph traversal.
        
        Args:
            source_book: Source book filename
        
        Returns:
            List of 2nd-hop target book filenames (excludes direct relationships)
        
        Example:
            >>> # Given: Architecture → FastAPI → Flask/FastAPI
            >>> engine.discover_second_hop("Architecture_Patterns_with_Python.json")
            ['Microservice_APIs_Using_Python_Flask_FastAPI.json']
        """
        if not self._graph:
            return []
        
        if NETWORKX_AVAILABLE and isinstance(self._graph, nx.DiGraph):
            return self._traverse_networkx_graph(source_book)
        
        if isinstance(self._graph, dict):
            return self._traverse_adjacency_list(source_book)
        
        return []
    
    # ========================================================================
    # GROUPING AND AGGREGATION
    # ========================================================================
    
    def group_by_relationship_type(
        self,
        source_book: str,
        similarity_results: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Group similarity results by relationship type.
        
        Args:
            source_book: Source book filename
            similarity_results: List of dicts from find_related_chapters
        
        Returns:
            Dict with keys 'parallel', 'perpendicular', 'skip_tier', 'unknown'
        
        Example:
            >>> grouped = engine.group_by_relationship_type("Arch.json", results)
            >>> grouped["parallel"]  # Same-tier books
            >>> grouped["skip_tier"]  # Tier 1 → Tier 3 books
        """
        grouped: Dict[str, List[Dict[str, Any]]] = {
            PARALLEL: [],
            PERPENDICULAR: [],
            SKIP_TIER: [],
            UNKNOWN: []
        }
        
        enhanced = self.enhance_similarity_results(source_book, similarity_results)
        
        for result in enhanced:
            rel_type = result.get("relationship_type", UNKNOWN)
            grouped[rel_type].append(result)
        
        return grouped
    
    # ========================================================================
    # FULL WORKFLOW
    # ========================================================================
    
    def enhance_and_discover(
        self,
        source_book: str,
        similarity_results: List[Dict[str, Any]],
        include_second_hop: bool = True
    ) -> Dict[str, Any]:
        """
        Full enhancement pipeline with optional 2nd-hop discovery.
        
        Args:
            source_book: Source book filename
            similarity_results: List of dicts from find_related_chapters
            include_second_hop: Whether to include 2nd-hop discovery
        
        Returns:
            Dict with 'direct_relationships' and 'second_hop_discoveries'
        
        Example:
            >>> result = engine.enhance_and_discover("Arch.json", results)
            >>> result["direct_relationships"]  # Enhanced results
            >>> result["second_hop_discoveries"]  # 2nd-hop books
        """
        enhanced = self.enhance_similarity_results(source_book, similarity_results)
        
        result: Dict[str, Any] = {
            "direct_relationships": enhanced,
            "second_hop_discoveries": []
        }
        
        if include_second_hop:
            result["second_hop_discoveries"] = self.discover_second_hop(source_book)
        
        return result
