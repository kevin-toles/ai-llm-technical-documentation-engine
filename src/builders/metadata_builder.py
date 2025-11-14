"""
Metadata Builder - Constructs metadata packages for LLM analysis

Sprint 3.4 - TDD GREEN: Extract metadata building from main file

Pattern: Builder Pattern (Architecture Patterns with Python Ch. 9)
Source: interactive_llm_system_v3_hybrid_prompt.py lines 1029-1200
Total Extracted: ~210 lines
"""

import logging
from typing import Dict, List, Any, Tuple

# Import taxonomy components (conditional import handled at module level)
try:
    from book_taxonomy import (
        score_books_for_concepts,
        get_cascading_books,
        BOOK_REGISTRY,
        BookTier
    )
    TAXONOMY_AVAILABLE = True
except ImportError:
    TAXONOMY_AVAILABLE = False
    BOOK_REGISTRY = {}
    BookTier = None

logger = logging.getLogger(__name__)


class MetadataBuilder:
    """
    Builder for metadata packages used in Phase 1 LLM analysis.
    
    Responsibility: Construct metadata structures from book/concept data
    Pattern: Builder Pattern (Architecture Patterns with Python Ch. 9)
    """
    
    def __init__(self, metadata_service):
        """Initialize with metadata service dependency (Dependency Injection)."""
        self._metadata_service = metadata_service
        self._last_metadata_package: Dict[str, Any] = {}  # For mocking fallback
    
    def _get_taxonomy_recommendations(
        self,
        concepts: List[str]
    ) -> Tuple[List[str], Dict[str, List[str]]]:
        """
        Get book recommendations and cascading relationships from taxonomy.
        
        Returns: (recommended_books, cascading_info)
        Source: interactive_llm_system_v3_hybrid_prompt.py lines 1029-1055
        """
        if not TAXONOMY_AVAILABLE:
            return [], {}
        
        concept_set = set(concepts)
        scored_books = score_books_for_concepts(concept_set)
        recommended_books = [book_name for book_name, score in scored_books if score >= 0.2]
        
        # Build cascading relationships
        cascading_info = {}
        for book_name in recommended_books[:8]:
            cascades = get_cascading_books(book_name, depth=1)
            if cascades:
                cascading_info[book_name] = cascades
                for cascaded_book in cascades:
                    if cascaded_book not in recommended_books:
                        recommended_books.append(cascaded_book)
        
        return recommended_books, cascading_info
    
    def _calculate_relevance_boosts(
        self,
        book_file_name: str,
        cascading_info: Dict[str, List[str]]
    ) -> Tuple[float, float]:
        """
        Calculate tier and cascading boosts for a book.
        
        Returns: (tier_boost, cascading_boost)
        Source: interactive_llm_system_v3_hybrid_prompt.py lines 1056-1093
        """
        tier_boost = 0.0
        cascading_boost = 0.0
        
        if not TAXONOMY_AVAILABLE or book_file_name not in BOOK_REGISTRY:
            return tier_boost, cascading_boost
        
        book_role = BOOK_REGISTRY[book_file_name]
        
        # Higher tier = higher priority
        if book_role.tier == BookTier.ARCHITECTURE_SPINE:
            tier_boost = 0.3
        elif book_role.tier == BookTier.IMPLEMENTATION:
            tier_boost = 0.2
        else:  # ENGINEERING_PRACTICES
            tier_boost = 0.1
        
        # Check if this book is recommended via cascading
        for cascades in cascading_info.values():
            if book_file_name in cascades:
                cascading_boost = 0.2
                break
        
        return tier_boost, cascading_boost
    
    def calculate_book_relevance(
        self,
        book,  # BookMetadata type
        concept_map: Dict[str, List]  # Dict[str, List[ConceptMatch]]
    ) -> float:
        """
        Calculate relevance score by summing concept match scores for this book.
        
        Source: interactive_llm_system_v3_hybrid_prompt.py lines 1178-1200
        """
        relevance = 0.0
        
        for concept, matches in concept_map.items():
            for match in matches:
                # Clean book name comparison
                match_book_clean = match.book_name.replace('_', ' ').lower()
                book_title_clean = book.title.replace('_', ' ').lower()
                
                if match_book_clean in book_title_clean or book_title_clean in match_book_clean:
                    relevance += match.relevance_score
        
        return relevance
    
    def build_book_metadata_entry(
        self,
        book,  # BookMetadata type
        concept_map: Dict[str, List],  # Dict[str, List[ConceptMatch]]
        cascading_info: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """
        Build metadata entry for a single book with relevance scoring.
        
        Source: interactive_llm_system_v3_hybrid_prompt.py lines 1095-1128
        """
        base_relevance = self.calculate_book_relevance(book, concept_map)
        tier_boost, cascading_boost = self._calculate_relevance_boosts(book.file_name, cascading_info)
        final_relevance = base_relevance + tier_boost + cascading_boost
        
        book_meta = {
            'file_name': book.file_name,
            'domain': book.domain,
            'total_pages': book.total_pages,
            'chapters_count': len(book.chapters),
            'concepts_covered': sorted(book.concepts_covered),
            'relevance_to_chapter': round(final_relevance, 2),
            'tier': BOOK_REGISTRY[book.file_name].tier.value if TAXONOMY_AVAILABLE and book.file_name in BOOK_REGISTRY else 'Unknown'
        }
        
        if book.file_name in cascading_info:
            book_meta['cascades_to'] = cascading_info[book.file_name]
        
        return book_meta
    
    def build_metadata_package(self, concepts: List[str]) -> Dict[str, Any]:
        """
        Build comprehensive metadata package for Phase 1 LLM analysis.
        
        Returns dict with: books, concept_mapping, totals, cascading_relationships
        Source: interactive_llm_system_v3_hybrid_prompt.py lines 1130-1177
        """
        all_books = self._metadata_service._repo.get_all()
        concept_map = self._metadata_service.create_concept_mapping(concepts)
        
        # Get taxonomy-based recommendations
        _recommended_books, cascading_info = self._get_taxonomy_recommendations(concepts)
        
        # Build structured metadata for each book
        books_metadata = [
            self.build_book_metadata_entry(book, concept_map, cascading_info)
            for book in all_books
        ]
        
        # Sort by relevance
        books_metadata.sort(key=lambda b: b['relevance_to_chapter'], reverse=True)
        
        # Build complete metadata package
        metadata_package = {
            'books': books_metadata,
            'concept_mapping': {
                concept: [
                    {
                        'book': match.book_name,
                        'pages': match.pages[:5],
                        'occurrences': match.total_occurrences,
                        'relevance': round(match.relevance_score, 2)
                    }
                    for match in matches[:3]
                ]
                for concept, matches in concept_map.items()
            },
            'total_books': len(books_metadata),
            'total_pages': sum(b['total_pages'] for b in books_metadata),
            'cascading_relationships': cascading_info if TAXONOMY_AVAILABLE else {}
        }
        
        self._last_metadata_package = metadata_package  # For backward compatibility
        return metadata_package


# Export MetadataBuilder for use in main file
__all__ = ['MetadataBuilder']
