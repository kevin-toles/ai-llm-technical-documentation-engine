#!/usr/bin/env python3
"""
Metadata Extraction System - Designed using principles from our companion books

ARCHITECTURE (from Architecture books):
- Domain-Driven Design: Clear domain models for Books, Pages, Concepts
- Repository Pattern: Abstract data access from business logic
- Service Layer: Orchestrate complex operations
- Dependency Injection: Decouple components

ENGINEERING PRACTICES (from Engineering books):
- Type hints and protocols (Fluent Python Ch. 8, 13)
- Dataclasses for domain models (Python Distilled Ch. 7)
- ABC for interfaces (Python Essential Reference Ch. 7)
- Context managers for resource handling (Python Cookbook Ch. 8)
- Generators for memory efficiency (Fluent Python Ch. 17)
"""

from dataclasses import dataclass, field
from typing import Protocol, List, Dict, Set, Optional, Any
from pathlib import Path
import json
from collections import defaultdict

# ============================================================================
# DOMAIN MODELS (DDD - Domain-Driven Design)
# From: Architecture Patterns with Python, Building Microservices
# ============================================================================

@dataclass(frozen=True)  # Immutable value object (DDD pattern)
class PageReference:
    """Value object representing a page reference.
    
    Pattern: Value Object (Architecture Patterns with Python, Ch. 1)
    Immutability ensures thread safety and hashability.
    """
    book_name: str
    page_number: int
    
    def __str__(self) -> str:
        return f"{self.book_name}:p{self.page_number}"


@dataclass
class Page:
    """Entity representing a single page of content.
    
    Pattern: Entity (DDD - Architecture Patterns with Python, Ch. 1)
    Has identity (page_number within book context).
    """
    page_number: int
    chapter: str
    content: str
    content_length: int
    extraction_method: str = "unknown"
    
    def contains_concept(self, concept: str) -> bool:
        """Check if page content contains the given concept."""
        return concept.lower() in self.content.lower()
    
    def count_concept(self, concept: str) -> int:
        """Count occurrences of concept in page."""
        return self.content.lower().count(concept.lower())
    
    def extract_context(self, concept: str, context_chars: int = 200) -> List[str]:
        """Extract surrounding context for concept mentions.
        
        Engineering: Generator pattern for memory efficiency
        (Fluent Python Ch. 17 - Iterators, Generators, Classic Coroutines)
        """
        content_lower = self.content.lower()
        concept_lower = concept.lower()
        contexts = []
        
        start = 0
        while True:
            pos = content_lower.find(concept_lower, start)
            if pos == -1:
                break
            
            context_start = max(0, pos - context_chars)
            context_end = min(len(self.content), pos + len(concept) + context_chars)
            contexts.append(self.content[context_start:context_end])
            start = pos + 1
        
        return contexts


@dataclass
class BookMetadata:
    """Aggregate root for book metadata.
    
    Pattern: Aggregate (DDD - Architecture Patterns with Python, Ch. 1)
    Controls access to child entities (pages).
    """
    title: str
    file_name: str
    total_pages: int
    chapters: List[str]
    domain: str  # "Architecture" or "Engineering Practices"
    concepts_covered: Set[str] = field(default_factory=set)
    
    def __post_init__(self):
        """Derive domain from file path."""
        if not self.domain:
            # Auto-detect domain from file name patterns
            if any(keyword in self.file_name.lower() for keyword in 
                   ['architecture', 'microservice', 'patterns']):
                self.domain = "Architecture"
            else:
                self.domain = "Engineering Practices"


@dataclass
class ConceptMatch:
    """Value object representing a concept match in a book.
    
    Pattern: Value Object (immutable, comparable)
    """
    concept: str
    book_name: str
    pages: List[int]
    total_occurrences: int
    relevance_score: float
    
    def __lt__(self, other: 'ConceptMatch') -> bool:
        """Enable sorting by relevance score."""
        return self.relevance_score < other.relevance_score


# ============================================================================
# REPOSITORY PATTERN - Data Access Abstraction
# From: Architecture Patterns with Python Ch. 2 - Repository Pattern
# ============================================================================

class BookRepository(Protocol):
    """Protocol defining the interface for book data access.
    
    Pattern: Repository Pattern + Protocol (structural typing)
    Engineering: Protocols for duck typing (Fluent Python Ch. 13)
    """
    
    def get_by_name(self, book_name: str) -> Optional[BookMetadata]:
        """Retrieve book metadata by name."""
        ...
    
    def get_all(self) -> List[BookMetadata]:
        """Retrieve all books."""
        ...
    
    def find_pages_with_concept(self, book_name: str, concept: str) -> List[Page]:
        """Find all pages containing a concept."""
        ...
    
    def get_page(self, book_name: str, page_num: int) -> Optional[Page]:
        """Get a specific page."""
        ...
    
    def get_page_range(self, book_name: str, start: int, end: int) -> List[Page]:
        """Get a range of pages with context."""
        ...


class JSONBookRepository:
    """Concrete implementation of BookRepository using JSON files.
    
    Pattern: Repository Pattern (Architecture Patterns with Python Ch. 2)
    Engineering: Resource management with context managers (Python Cookbook Ch. 8)
    """
    
    def __init__(self, json_directories: List[Path]):
        """Initialize repository with JSON data sources.
        
        Engineering: Dependency injection via constructor
        (Python Architecture Patterns Ch. 3 - Coupling and Abstractions)
        """
        self._directories = json_directories
        self._books_cache: Dict[str, Dict] = {}
        self._metadata_cache: Dict[str, BookMetadata] = {}
        self._load_books()
    
    def _load_books(self) -> None:
        """Load all JSON books into cache.
        
        Engineering: Lazy loading + caching pattern
        (Python Essential Reference Ch. 7 - Classes and OOP)
        """
        print("Loading companion book metadata...")
        for directory in self._directories:
            if not directory.exists():
                continue
            
            for json_file in directory.glob("*.json"):
                try:
                    print(f"  Loading {json_file.stem}...", end='', flush=True)
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                        # ALWAYS use filename as the canonical name (ignore embedded title metadata)
                        # Filename is the source of truth: "Fluent Python 2nd"
                        book_name = json_file.stem
                        
                        # Store book data using the filename
                        self._books_cache[book_name] = data
                        print(f" ✓ ({len(data.get('pages', []))} pages)")
                        
                        # Create metadata - use filename for both title and file_name
                        metadata = BookMetadata(
                            title=book_name,  # Use filename, not embedded metadata
                            file_name=book_name,  # Same as title
                            total_pages=len(data.get('pages', [])),
                            chapters=data.get('chapters', []),
                            domain="",  # Will be auto-detected
                            concepts_covered=self._extract_concepts_from_book(data)
                        )
                        self._metadata_cache[book_name] = metadata
                        
                except Exception as e:
                    print(f"Error loading {json_file}: {e}")
    
    def _extract_concepts_from_book(self, book_data: Dict) -> Set[str]:
        """Extract Python concepts covered in the book.
        
        Engineering: Set comprehension for efficient unique collection
        (Fluent Python Ch. 3 - Dictionaries and Sets)
        """
        python_concepts = [
            'function', 'class', 'method', 'variable', 'list', 'dict',
            'tuple', 'set', 'decorator', 'generator', 'iterator',
            'exception', 'module', 'package', 'import', 'async',
            'await', 'lambda', 'comprehension', 'metaclass'
        ]
        
        found_concepts = set()
        pages = book_data.get('pages', [])
        
        # Sample pages for concept detection (performance optimization)
        sample_size = min(100, len(pages))
        sample_step = max(1, len(pages) // sample_size)
        
        for i in range(0, len(pages), sample_step):
            content = pages[i].get('content', '').lower()
            for concept in python_concepts:
                if concept in content:
                    found_concepts.add(concept)
        
        return found_concepts
    
    def get_by_name(self, book_name: str) -> Optional[BookMetadata]:
        """Retrieve book metadata by name."""
        return self._metadata_cache.get(book_name)
    
    def get_all(self) -> List[BookMetadata]:
        """Retrieve all books."""
        return list(self._metadata_cache.values())
    
    def find_pages_with_concept(self, book_name: str, concept: str) -> List[Page]:
        """Find all pages containing a concept.
        
        Engineering: Generator for memory efficiency
        (Fluent Python Ch. 17 - Generators)
        """
        if book_name not in self._books_cache:
            return []
        
        pages_data = self._books_cache[book_name].get('pages', [])
        matching_pages = []
        
        for page_data in pages_data:
            page = Page(
                page_number=page_data.get('page_number', 0),
                chapter=page_data.get('chapter', ''),
                content=page_data.get('content', ''),
                content_length=page_data.get('content_length', 0),
                extraction_method=page_data.get('extraction_method', 'unknown')
            )
            
            if page.contains_concept(concept):
                matching_pages.append(page)
        
        return matching_pages
    
    def get_page(self, book_name: str, page_num: int) -> Optional[Page]:
        """Get a specific page."""
        if book_name not in self._books_cache:
            return None
        
        pages_data = self._books_cache[book_name].get('pages', [])
        
        for page_data in pages_data:
            if page_data.get('page_number') == page_num:
                return Page(
                    page_number=page_data.get('page_number', 0),
                    chapter=page_data.get('chapter', ''),
                    content=page_data.get('content', ''),
                    content_length=page_data.get('content_length', 0),
                    extraction_method=page_data.get('extraction_method', 'unknown')
                )
        
        return None
    
    def get_page_range(self, book_name: str, start: int, end: int) -> List[Page]:
        """Get a range of pages with context."""
        if book_name not in self._books_cache:
            return []
        
        pages_data = self._books_cache[book_name].get('pages', [])
        pages_in_range = []
        
        for page_data in pages_data:
            page_num = page_data.get('page_number', 0)
            if start <= page_num <= end:
                page = Page(
                    page_number=page_num,
                    chapter=page_data.get('chapter', ''),
                    content=page_data.get('content', ''),
                    content_length=page_data.get('content_length', 0),
                    extraction_method=page_data.get('extraction_method', 'unknown')
                )
                pages_in_range.append(page)
        
        return sorted(pages_in_range, key=lambda p: p.page_number)


# ============================================================================
# SERVICE LAYER - Business Logic Orchestration
# From: Architecture Patterns with Python Ch. 4 - Service Layer
# ============================================================================

class MetadataExtractionService:
    """Service layer for metadata extraction operations.
    
    Pattern: Service Layer (Architecture Patterns with Python Ch. 4)
    Orchestrates complex operations across domain objects and repository.
    """
    
    def __init__(self, repository: BookRepository):
        """Inject repository dependency.
        
        Pattern: Dependency Injection
        (Python Architecture Patterns Ch. 3)
        """
        self._repo = repository
    
    def extract_book_metadata(self, book_name: str) -> Optional[Dict[str, Any]]:
        """Extract comprehensive metadata for a book.
        
        Returns structured metadata suitable for LLM consumption.
        """
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
    
    def create_concept_mapping(self, concepts: List[str]) -> Dict[str, List[ConceptMatch]]:
        """Map concepts to books and pages.
        
        Engineering: Dictionary comprehension and efficient data structures
        (Fluent Python Ch. 3 - Dictionaries and Sets)
        """
        concept_map = defaultdict(list)
        
        all_books = self._repo.get_all()
        
        for concept in concepts:
            for book in all_books:
                # Use clean book name (without _Content suffix)
                clean_book_name = book.file_name.replace('_Content.json', '').replace('.json', '')
                pages = self._repo.find_pages_with_concept(clean_book_name, concept)
                
                if pages:
                    total_occurrences = sum(p.count_concept(concept) for p in pages)
                    page_numbers = [p.page_number for p in pages]
                    
                    # Calculate relevance score
                    relevance_score = self._calculate_relevance(
                        occurrences=total_occurrences,
                        page_count=len(pages),
                        total_pages=book.total_pages
                    )
                    
                    match = ConceptMatch(
                        concept=concept,
                        book_name=book.title,
                        pages=page_numbers[:10],  # Top 10 pages
                        total_occurrences=total_occurrences,
                        relevance_score=relevance_score
                    )
                    
                    concept_map[concept].append(match)
            
            # Sort matches by relevance
            concept_map[concept].sort(reverse=True)
        
        return dict(concept_map)
    
    def _calculate_relevance(self, occurrences: int, page_count: int, total_pages: int) -> float:
        """Calculate relevance score for a concept match.
        
        Formula combines:
        - Occurrence density (occurrences per page)
        - Coverage (percentage of book covering concept)
        """
        density = occurrences / page_count if page_count > 0 else 0
        coverage = page_count / total_pages if total_pages > 0 else 0
        return (density * 0.6) + (coverage * 0.4)  # Weighted score
    
    def extract_targeted_content(
        self,
        book_name: str,
        concept: str,
        max_excerpts: int = 5,
        context_chars: int = 300
    ) -> List[Dict[str, Any]]:
        """Extract targeted excerpts for a concept with surrounding context.
        
        Engineering: Builder pattern for complex object construction
        (Python Cookbook Ch. 8 - Classes and Objects)
        """
        pages = self._repo.find_pages_with_concept(book_name, concept)
        
        # Sort by concept density
        pages_sorted = sorted(
            pages,
            key=lambda p: p.count_concept(concept),
            reverse=True
        )[:max_excerpts]
        
        excerpts = []
        for page in pages_sorted:
            contexts = page.extract_context(concept, context_chars)
            
            excerpt = {
                'page_number': page.page_number,
                'chapter': page.chapter,
                'occurrences': page.count_concept(concept),
                'contexts': contexts[:3],  # Top 3 contexts per page
                'full_content_available': True
            }
            excerpts.append(excerpt)
        
        return excerpts


# ============================================================================
# FACTORY PATTERN - Object Creation
# From: Python Essential Reference Ch. 7, Fluent Python Ch. 11
# ============================================================================

class MetadataServiceFactory:
    """Factory for creating MetadataExtractionService instances.
    
    Pattern: Factory Pattern
    (Python Essential Reference Ch. 7 - Classes)
    """
    
    @staticmethod
    def create_from_directories(directories: List[Path]) -> MetadataExtractionService:
        """Create service with JSON repository."""
        repository = JSONBookRepository(directories)
        return MetadataExtractionService(repository)
    
    @staticmethod
    def create_default() -> MetadataExtractionService:
        """Create service with default directories."""
        repo_root = Path(__file__).parent.parent
        directories = [
            repo_root / "data" / "textbooks_json"
        ]
        return MetadataServiceFactory.create_from_directories(directories)


if __name__ == "__main__":
    # Demonstration
    print("="*80)
    print("METADATA EXTRACTION SYSTEM")
    print("Built using patterns from our companion books")
    print("="*80)
    
    # Create service using factory
    service = MetadataServiceFactory.create_default()
    
    # Test metadata extraction
    print("\n📚 Testing metadata extraction...")
    metadata = service.extract_book_metadata("Fluent_Python_2nd")
    if metadata:
        print(f"Title: {metadata['title']}")
        print(f"Domain: {metadata['domain']}")
        print(f"Pages: {metadata['total_pages']}")
        print(f"Concepts: {list(metadata['concepts_covered'])[:5]}")
    
    # Test concept mapping
    print("\n🔍 Testing concept mapping...")
    print(f"Loaded books: {[book.file_name for book in service._repo.get_all()[:3]]}")
    concepts = ["decorator", "generator", "async"]
    mapping = service.create_concept_mapping(concepts)
    
    for concept, matches in mapping.items():
        print(f"\n{concept}: {len(matches)} books")
        for match in matches[:3]:
            print(f"  - {match.book_name}: {match.total_occurrences} occurrences, "
                  f"score {match.relevance_score:.2f}")
    
    print("\n✅ System demonstration complete!")