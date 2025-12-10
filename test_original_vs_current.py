#!/usr/bin/env python3
"""
Test script to compare original metadata extraction/enrichment logic vs current workflow.

Input: /Users/kevintoles/POC/textbooks/JSON Texts/AI Engineering Building Applications.json
Taxonomy: /Users/kevintoles/POC/textbooks/Taxonomies/AI-ML_taxonomy_20251128.json

This traces the internal logic of:
1. Original metadata_extraction_system.py (from commit 7067c90b)
2. Original chapter_metadata_manager.py (from commit 7067c90b)
3. Original book_taxonomy.py (from commit 7067c90b)
"""

import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Any
from collections import defaultdict
from enum import Enum

# ============================================================================
# PATHS
# ============================================================================

INPUT_JSON = Path("/Users/kevintoles/POC/textbooks/JSON Texts/AI Engineering Building Applications.json")
TAXONOMY_JSON = Path("/Users/kevintoles/POC/textbooks/Taxonomies/AI-ML_taxonomy_20251128.json")
COMPANION_BOOKS_DIR = Path("/Users/kevintoles/POC/textbooks/JSON Texts")

# ============================================================================
# ORIGINAL DOMAIN MODELS (from metadata_extraction_system.py @ 7067c90b)
# ============================================================================

@dataclass(frozen=True)
class PageReference:
    """Value object representing a page reference."""
    book_name: str
    page_number: int
    
    def __str__(self) -> str:
        return f"{self.book_name}:p{self.page_number}"


@dataclass
class Page:
    """Entity representing a single page of content."""
    page_number: int
    chapter: str
    content: str
    content_length: int
    extraction_method: str = "unknown"
    
    def contains_concept(self, concept: str) -> bool:
        return concept.lower() in self.content.lower()
    
    def count_concept(self, concept: str) -> int:
        return self.content.lower().count(concept.lower())


@dataclass
class BookMetadata:
    """Aggregate root for book metadata."""
    title: str
    file_name: str
    total_pages: int
    chapters: List[str]
    domain: str
    concepts_covered: Set[str] = field(default_factory=set)


@dataclass
class ConceptMatch:
    """Value object representing a concept match in a book."""
    concept: str
    book_name: str
    pages: List[int]
    total_occurrences: int
    relevance_score: float


# ============================================================================
# ORIGINAL BOOK TAXONOMY (from book_taxonomy.py @ 7067c90b)
# Adapted to use the AI-ML taxonomy JSON
# ============================================================================

class BookTier(Enum):
    ARCHITECTURE_SPINE = "Architecture Spine"
    IMPLEMENTATION = "Implementation"
    ENGINEERING_PRACTICES = "Engineering Practices"


@dataclass
class BookRole:
    """Defines a book's role in the taxonomy."""
    book_name: str
    tier: BookTier
    primary_focus: str
    keyword_triggers: Set[str]
    cascades_to: List[str]
    relevance_weight: float = 1.0
    priority: int = 1
    
    def matches_concepts(self, concepts: Set[str]) -> float:
        if not concepts or not self.keyword_triggers:
            return 0.0
        matches = self.keyword_triggers.intersection(concepts)
        return (len(matches) / len(self.keyword_triggers)) * self.relevance_weight


def load_taxonomy_from_json(taxonomy_path: Path) -> Dict[str, BookRole]:
    """Load taxonomy from the AI-ML taxonomy JSON file."""
    with open(taxonomy_path, 'r') as f:
        data = json.load(f)
    
    book_roles = {}
    tier_mapping = {
        "architecture": BookTier.ARCHITECTURE_SPINE,
        "implementation": BookTier.IMPLEMENTATION,
        "practices": BookTier.ENGINEERING_PRACTICES
    }
    
    for tier_key, tier_data in data.get("tiers", {}).items():
        tier_enum = tier_mapping.get(tier_key, BookTier.ENGINEERING_PRACTICES)
        concepts = set(tier_data.get("concepts", []))
        
        for book in tier_data.get("books", []):
            book_name = book["name"].replace(".json", "")
            
            # Get cascading books (books in the same tier with lower priority)
            cascades_to = [
                b["name"].replace(".json", "") 
                for b in tier_data.get("books", [])
                if b["priority"] > book["priority"]
            ][:3]  # Limit to 3 cascading books
            
            book_roles[book_name] = BookRole(
                book_name=book_name,
                tier=tier_enum,
                primary_focus=tier_data.get("description", ""),
                keyword_triggers=concepts,
                cascades_to=cascades_to,
                relevance_weight=1.0 + (0.1 * (10 - book["priority"])),  # Higher priority = higher weight
                priority=book["priority"]
            )
    
    return book_roles


# ============================================================================
# ORIGINAL REPOSITORY (from metadata_extraction_system.py @ 7067c90b)
# ============================================================================

class JSONBookRepository:
    """Concrete implementation of BookRepository using JSON files."""
    
    def __init__(self, json_directory: Path):
        self._directory = json_directory
        self._books_cache: Dict[str, Dict] = {}
        self._metadata_cache: Dict[str, BookMetadata] = {}
        self._load_books()
    
    def _load_books(self) -> None:
        """Load all JSON books into cache."""
        print(f"\n📚 Loading companion books from: {self._directory}")
        
        if not self._directory.exists():
            print(f"  ❌ Directory not found!")
            return
        
        for json_file in self._directory.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                book_name = json_file.stem
                self._books_cache[book_name] = data
                
                # Handle different JSON structures
                pages = data.get('pages', [])
                if not pages:
                    # Try segments structure
                    segments = data.get('segments', [])
                    if segments:
                        pages = segments
                
                # Extract chapters
                chapters = []
                if 'chapters' in data:
                    chapters = data['chapters']
                elif pages:
                    # Extract from page data
                    seen_chapters = set()
                    for page in pages:
                        ch = page.get('chapter', page.get('title', ''))
                        if ch and ch not in seen_chapters:
                            chapters.append(ch)
                            seen_chapters.add(ch)
                
                metadata = BookMetadata(
                    title=book_name,
                    file_name=book_name,
                    total_pages=len(pages),
                    chapters=chapters,
                    domain="",
                    concepts_covered=self._extract_concepts_from_book(data)
                )
                self._metadata_cache[book_name] = metadata
                print(f"  ✓ {book_name}: {len(pages)} pages, {len(chapters)} chapters")
                
            except Exception as e:
                print(f"  ❌ Error loading {json_file.name}: {e}")
    
    def _extract_concepts_from_book(self, book_data: Dict) -> Set[str]:
        """Extract concepts covered in the book."""
        # Common AI/ML concepts
        concepts = [
            'model', 'training', 'inference', 'embedding', 'vector',
            'transformer', 'attention', 'token', 'prompt', 'fine-tuning',
            'rag', 'retrieval', 'generation', 'llm', 'agent', 'tool',
            'api', 'endpoint', 'service', 'microservice', 'architecture',
            'pattern', 'repository', 'domain', 'event', 'message'
        ]
        
        found = set()
        pages = book_data.get('pages', book_data.get('segments', []))
        
        sample_size = min(50, len(pages))
        sample_step = max(1, len(pages) // sample_size)
        
        for i in range(0, len(pages), sample_step):
            content = pages[i].get('content', '').lower()
            for concept in concepts:
                if concept in content:
                    found.add(concept)
        
        return found
    
    def get_by_name(self, book_name: str) -> Optional[BookMetadata]:
        return self._metadata_cache.get(book_name)
    
    def get_all(self) -> List[BookMetadata]:
        return list(self._metadata_cache.values())
    
    def find_pages_with_concept(self, book_name: str, concept: str) -> List[Page]:
        if book_name not in self._books_cache:
            return []
        
        book_data = self._books_cache[book_name]
        pages_data = book_data.get('pages', book_data.get('segments', []))
        matching = []
        
        for page_data in pages_data:
            content = page_data.get('content', '')
            if concept.lower() in content.lower():
                page = Page(
                    page_number=page_data.get('page_number', page_data.get('number', 0)),
                    chapter=page_data.get('chapter', page_data.get('title', '')),
                    content=content,
                    content_length=len(content),
                    extraction_method=page_data.get('detection_method', 'unknown')
                )
                matching.append(page)
        
        return matching
    
    def get_page_content(self, book_name: str, page_num: int) -> Optional[str]:
        if book_name not in self._books_cache:
            return None
        
        book_data = self._books_cache[book_name]
        pages_data = book_data.get('pages', book_data.get('segments', []))
        
        for page_data in pages_data:
            if page_data.get('page_number', page_data.get('number', 0)) == page_num:
                return page_data.get('content', '')
        
        return None


# ============================================================================
# ORIGINAL SERVICE LAYER (from metadata_extraction_system.py @ 7067c90b)
# ============================================================================

class MetadataExtractionService:
    """Service layer for metadata extraction operations."""
    
    def __init__(self, repository: JSONBookRepository, taxonomy: Dict[str, BookRole]):
        self._repo = repository
        self._taxonomy = taxonomy
    
    def extract_book_metadata(self, book_name: str) -> Optional[Dict[str, Any]]:
        """Extract comprehensive metadata for a book."""
        metadata = self._repo.get_by_name(book_name)
        if not metadata:
            return None
        
        return {
            'title': metadata.title,
            'domain': metadata.domain,
            'total_pages': metadata.total_pages,
            'chapters': metadata.chapters,
            'concepts_covered': sorted(metadata.concepts_covered)
        }
    
    def create_concept_mapping(self, concepts: List[str], source_book: str) -> Dict[str, List[ConceptMatch]]:
        """Map concepts to books and pages - THE CORE CROSS-REFERENCING LOGIC."""
        concept_map = defaultdict(list)
        
        all_books = self._repo.get_all()
        
        print(f"\n🔍 Creating concept mapping for {len(concepts)} concepts across {len(all_books)} books...")
        
        for concept in concepts:
            for book in all_books:
                # Skip the source book itself
                if book.file_name == source_book:
                    continue
                
                pages = self._repo.find_pages_with_concept(book.file_name, concept)
                
                if pages:
                    total_occurrences = sum(p.count_concept(concept) for p in pages)
                    page_numbers = [p.page_number for p in pages]
                    
                    # Calculate relevance using taxonomy
                    book_role = self._taxonomy.get(book.file_name)
                    base_score = self._calculate_relevance(
                        occurrences=total_occurrences,
                        page_count=len(pages),
                        total_pages=book.total_pages
                    )
                    
                    # Apply taxonomy weight
                    if book_role:
                        base_score *= book_role.relevance_weight
                    
                    match = ConceptMatch(
                        concept=concept,
                        book_name=book.title,
                        pages=page_numbers[:10],
                        total_occurrences=total_occurrences,
                        relevance_score=base_score
                    )
                    
                    concept_map[concept].append(match)
            
            # Sort matches by relevance
            concept_map[concept].sort(key=lambda x: x.relevance_score, reverse=True)
        
        return dict(concept_map)
    
    def _calculate_relevance(self, occurrences: int, page_count: int, total_pages: int) -> float:
        """Calculate relevance score for a concept match."""
        density = occurrences / page_count if page_count > 0 else 0
        coverage = page_count / total_pages if total_pages > 0 else 0
        return (density * 0.6) + (coverage * 0.4)
    
    def get_cascading_books(self, book_name: str) -> List[str]:
        """Get books that should be included via cascading logic."""
        book_role = self._taxonomy.get(book_name)
        if not book_role:
            return []
        return book_role.cascades_to
    
    def get_books_by_tier(self, tier: BookTier) -> List[BookRole]:
        """Get all books in a specific tier."""
        return [role for role in self._taxonomy.values() if role.tier == tier]


# ============================================================================
# MAIN TEST EXECUTION
# ============================================================================

def main():
    print("=" * 80)
    print("ORIGINAL METADATA EXTRACTION/ENRICHMENT TEST")
    print("=" * 80)
    
    # Load taxonomy
    print(f"\n📖 Loading taxonomy from: {TAXONOMY_JSON}")
    taxonomy = load_taxonomy_from_json(TAXONOMY_JSON)
    print(f"  ✓ Loaded {len(taxonomy)} book roles")
    
    # Show taxonomy tiers
    for tier in BookTier:
        books_in_tier = [r for r in taxonomy.values() if r.tier == tier]
        print(f"  {tier.value}: {len(books_in_tier)} books")
        for book in sorted(books_in_tier, key=lambda x: x.priority)[:3]:
            print(f"    - {book.book_name} (priority {book.priority}, weight {book.relevance_weight:.2f})")
    
    # Load repository with all companion books
    repo = JSONBookRepository(COMPANION_BOOKS_DIR)
    
    # Create service
    service = MetadataExtractionService(repo, taxonomy)
    
    # Load input book
    print(f"\n📄 Loading input book: {INPUT_JSON.name}")
    with open(INPUT_JSON, 'r') as f:
        input_data = json.load(f)
    
    input_book_name = INPUT_JSON.stem
    print(f"  Book name: {input_book_name}")
    
    # Extract metadata for input book
    metadata = service.extract_book_metadata(input_book_name)
    if metadata:
        print(f"  Total pages: {metadata['total_pages']}")
        print(f"  Chapters: {len(metadata['chapters'])}")
        print(f"  Concepts found: {len(metadata['concepts_covered'])}")
    
    # Get key concepts from taxonomy for this book
    book_role = taxonomy.get(input_book_name)
    if book_role:
        print(f"\n📊 Book role in taxonomy:")
        print(f"  Tier: {book_role.tier.value}")
        print(f"  Priority: {book_role.priority}")
        print(f"  Cascades to: {book_role.cascades_to}")
    
    # Extract sample concepts from first few chapters
    print(f"\n🔬 Extracting concepts from input book...")
    sample_concepts = ['model', 'training', 'inference', 'agent', 'transformer', 
                       'attention', 'embedding', 'api', 'prompt', 'fine-tuning']
    
    # Create concept mapping (THE CORE CROSS-REFERENCE LOGIC)
    concept_mapping = service.create_concept_mapping(sample_concepts, input_book_name)
    
    # Display results
    print("\n" + "=" * 80)
    print("CROSS-REFERENCE RESULTS (Original Logic)")
    print("=" * 80)
    
    for concept, matches in concept_mapping.items():
        if matches:
            print(f"\n📌 '{concept}' found in {len(matches)} companion books:")
            for match in matches[:5]:  # Top 5
                tier_info = ""
                if match.book_name in taxonomy:
                    tier_info = f" [{taxonomy[match.book_name].tier.value}]"
                print(f"   - {match.book_name}{tier_info}")
                print(f"     {match.total_occurrences} occurrences, {len(match.pages)} pages")
                print(f"     Relevance: {match.relevance_score:.3f}")
                print(f"     Sample pages: {match.pages[:5]}")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    total_cross_refs = sum(len(matches) for matches in concept_mapping.values())
    print(f"Total cross-references found: {total_cross_refs}")
    print(f"Concepts with matches: {sum(1 for m in concept_mapping.values() if m)}/{len(sample_concepts)}")
    
    # Show what's missing in current workflow
    print("\n⚠️  WHAT THE CURRENT WORKFLOW IS MISSING:")
    print("   1. No book taxonomy loading (hardcoded was removed)")
    print("   2. No cross-book concept mapping")
    print("   3. No tier-based relevance weighting")
    print("   4. No cascading book relationships")
    print("   5. Missing integration with semantic-search-service")
    print("   6. Missing integration with Graph RAG")


if __name__ == "__main__":
    main()
