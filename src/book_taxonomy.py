#!/usr/bin/env python3
"""
book_taxonomy.py

Defines the hierarchical taxonomy of all 15 companion books with:
- Role classification (Architecture Spine / Implementation / Engineering Practices)
- Cascading relationships (Architecture → Implementation → Practices)
- Keyword triggers for intelligent book selection
- Relevance scoring based on chapter concepts

Architecture:
- Pattern: Strategy + Template Method (Design Patterns - GoF)
- Allows flexible book selection based on content analysis
"""

from dataclasses import dataclass
from typing import List, Set, Dict, Optional
from enum import Enum


class BookTier(Enum):
    """Book tier in the cascading hierarchy."""
    ARCHITECTURE_SPINE = "Architecture Spine"  # Foundational patterns
    IMPLEMENTATION = "Implementation"  # Practical application
    ENGINEERING_PRACTICES = "Engineering Practices"  # Language fundamentals


@dataclass
class BookRole:
    """Defines a book's role in the taxonomy with cascading relationships."""
    
    book_name: str
    tier: BookTier
    primary_focus: str
    keyword_triggers: Set[str]  # Concepts that make this book relevant
    cascades_to: List[str]  # Books to include when this book is selected
    relevance_weight: float = 1.0  # Multiplier for relevance scoring
    
    def matches_concepts(self, concepts: Set[str]) -> float:
        """Calculate relevance score based on concept overlap.
        
        Returns:
            Float between 0.0 and 1.0 representing relevance
        """
        if not concepts:
            return 0.0
        
        matches = self.keyword_triggers.intersection(concepts)
        return (len(matches) / len(self.keyword_triggers)) * self.relevance_weight


# ============================================================================
# ARCHITECTURE SPINE BOOKS
# ============================================================================

ARCHITECTURE_PATTERNS_WITH_PYTHON = BookRole(
    book_name="Architecture Patterns with Python",
    tier=BookTier.ARCHITECTURE_SPINE,
    primary_focus="DDD, Event-Driven Architecture, Repository Pattern",
    keyword_triggers={
        "domain", "aggregate", "repository", "unit of work", "service layer",
        "event", "message bus", "dependency injection", "adapter", "port",
        "bounded context", "entity", "value object", "architecture",
        "persistence", "orm", "database", "transaction", "testing",
        "hexagonal", "clean architecture", "domain-driven design"
    },
    cascades_to=[
        "Building Python Microservices with FastAPI",
        "Python Architecture Patterns"
    ],
    relevance_weight=1.2  # High weight for architectural concepts
)

BUILDING_MICROSERVICES = BookRole(
    book_name="Building Microservices",
    tier=BookTier.ARCHITECTURE_SPINE,
    primary_focus="Microservices architecture, organizational patterns",
    keyword_triggers={
        "microservice", "service", "distributed", "resilience", "scalability",
        "deployment", "monitoring", "observability", "circuit breaker",
        "api gateway", "service mesh", "containerization", "docker",
        "orchestration", "communication", "rest", "grpc", "messaging",
        "kafka", "rabbitmq", "fault tolerance", "load balancing"
    },
    cascades_to=[
        "Microservices Up and Running",
        "Python Microservices Development"
    ],
    relevance_weight=1.1
)

MICROSERVICE_ARCHITECTURE = BookRole(
    book_name="Microservice Architecture",
    tier=BookTier.ARCHITECTURE_SPINE,
    primary_focus="Academic theory, formal design patterns",
    keyword_triggers={
        "architecture", "pattern", "design", "structure", "component",
        "module", "interface", "abstraction", "coupling", "cohesion",
        "separation of concerns", "single responsibility", "dependency",
        "layered", "modular", "composition", "decomposition"
    },
    cascades_to=[
        "Architecture Patterns with Python",
        "Python Architecture Patterns"
    ],
    relevance_weight=1.0
)

PYTHON_ARCHITECTURE_PATTERNS = BookRole(
    book_name="Python Architecture Patterns",
    tier=BookTier.ARCHITECTURE_SPINE,
    primary_focus="Python-specific architectural patterns",
    keyword_triggers={
        "pattern", "architecture", "design", "mvc", "mvvm", "clean code",
        "solid", "refactoring", "testability", "maintainability",
        "extensibility", "plugin", "framework", "library", "package",
        "structure", "organization", "best practices"
    },
    cascades_to=[
        "Fluent Python 2nd",
        "Python Essential Reference 4th"
    ],
    relevance_weight=1.1
)

# ============================================================================
# IMPLEMENTATION LAYER BOOKS
# ============================================================================

BUILDING_PYTHON_MICROSERVICES_WITH_FASTAPI = BookRole(
    book_name="Building Python Microservices with FastAPI",
    tier=BookTier.IMPLEMENTATION,
    primary_focus="FastAPI framework, async Python, API development",
    keyword_triggers={
        "fastapi", "async", "await", "asyncio", "api", "rest", "endpoint",
        "router", "dependency", "validation", "pydantic", "schema",
        "openapi", "swagger", "authentication", "authorization", "jwt",
        "middleware", "cors", "websocket", "background tasks", "testing"
    },
    cascades_to=[
        "Microservice APIs Using Python Flask FastAPI",
        "Python Distilled"
    ],
    relevance_weight=1.0
)

MICROSERVICE_APIS_USING_PYTHON_FLASK_FASTAPI = BookRole(
    book_name="Microservice APIs Using Python Flask FastAPI",
    tier=BookTier.IMPLEMENTATION,
    primary_focus="Comparative API frameworks (Flask, FastAPI)",
    keyword_triggers={
        "flask", "fastapi", "api", "blueprint", "route", "decorator",
        "request", "response", "middleware", "extension", "plugin",
        "template", "jinja", "sqlalchemy", "migration", "testing",
        "deployment", "wsgi", "asgi", "gunicorn", "uvicorn"
    },
    cascades_to=[
        "Python Cookbook 3rd",
        "Fluent Python 2nd"
    ],
    relevance_weight=1.0
)

PYTHON_MICROSERVICES_DEVELOPMENT = BookRole(
    book_name="Python Microservices Development",
    tier=BookTier.IMPLEMENTATION,
    primary_focus="Building microservices with Python",
    keyword_triggers={
        "microservice", "service", "distributed", "communication", "rpc",
        "messaging", "queue", "celery", "redis", "docker", "kubernetes",
        "deployment", "scaling", "monitoring", "logging", "tracing",
        "debugging", "performance", "optimization", "caching"
    },
    cascades_to=[
        "Building Microservices",
        "Python Essential Reference 4th"
    ],
    relevance_weight=1.0
)

MICROSERVICES_UP_AND_RUNNING = BookRole(
    book_name="Microservices Up and Running",
    tier=BookTier.IMPLEMENTATION,
    primary_focus="Operational microservices patterns",
    keyword_triggers={
        "operations", "deployment", "devops", "ci/cd", "pipeline",
        "container", "orchestration", "monitoring", "alerting", "logging",
        "metrics", "observability", "reliability", "availability",
        "incident", "postmortem", "sre", "kubernetes", "helm"
    },
    cascades_to=[
        "Building Microservices",
        "Python Microservices Development"
    ],
    relevance_weight=0.9
)

# ============================================================================
# ENGINEERING PRACTICES BOOKS (Python Language Fundamentals)
# ============================================================================

FLUENT_PYTHON_2ND = BookRole(
    book_name="Fluent Python 2nd",
    tier=BookTier.ENGINEERING_PRACTICES,
    primary_focus="Advanced Pythonic patterns, protocols, metaprogramming",
    keyword_triggers={
        "pythonic", "idiomatic", "protocol", "abc", "metaclass", "descriptor",
        "decorator", "context manager", "generator", "iterator", "coroutine",
        "async", "await", "type hint", "annotation", "special method",
        "__init__", "__call__", "__enter__", "__exit__", "property",
        "classmethod", "staticmethod", "dataclass", "comprehension"
    },
    cascades_to=[
        "Python Distilled",
        "Python Essential Reference 4th"
    ],
    relevance_weight=1.2  # High weight for advanced Python concepts
)

PYTHON_DISTILLED = BookRole(
    book_name="Python Distilled",
    tier=BookTier.ENGINEERING_PRACTICES,
    primary_focus="Concise best practices, core concepts",
    keyword_triggers={
        "function", "class", "method", "module", "package", "import",
        "exception", "iterator", "generator", "decorator", "property",
        "closure", "lambda", "comprehension", "context manager", "type",
        "object", "reference", "memory", "garbage collection", "threading",
        "multiprocessing", "async", "testing", "debugging"
    },
    cascades_to=[
        "Python Essential Reference 4th",
        "Python Cookbook 3rd"
    ],
    relevance_weight=1.1
)

PYTHON_COOKBOOK_3RD = BookRole(
    book_name="Python Cookbook 3rd",
    tier=BookTier.ENGINEERING_PRACTICES,
    primary_focus="Recipe-based practical solutions",
    keyword_triggers={
        "data structure", "algorithm", "string", "text", "number", "file",
        "io", "iteration", "function", "class", "metaprogramming", "module",
        "network", "web", "concurrency", "testing", "debugging", "c extension",
        "recipe", "pattern", "idiom", "technique", "best practice"
    },
    cascades_to=[
        "Fluent Python 2nd",
        "Python Distilled"
    ],
    relevance_weight=1.0
)

PYTHON_ESSENTIAL_REFERENCE_4TH = BookRole(
    book_name="Python Essential Reference 4th",
    tier=BookTier.ENGINEERING_PRACTICES,
    primary_focus="Authoritative language reference",
    keyword_triggers={
        "reference", "specification", "syntax", "semantics", "built-in",
        "standard library", "function", "class", "module", "type", "object",
        "operator", "expression", "statement", "exception", "iterator",
        "generator", "decorator", "descriptor", "metaclass", "gc",
        "threading", "multiprocessing", "io", "network", "sys"
    },
    cascades_to=[
        "Python Distilled",
        "Fluent Python 2nd"
    ],
    relevance_weight=1.0
)

PYTHON_DATA_ANALYSIS_3RD = BookRole(
    book_name="Python Data Analysis 3rd",
    tier=BookTier.ENGINEERING_PRACTICES,
    primary_focus="Data analysis with pandas, NumPy",
    keyword_triggers={
        "pandas", "numpy", "dataframe", "series", "array", "matrix",
        "data", "analysis", "statistics", "visualization", "matplotlib",
        "plotting", "cleaning", "wrangling", "transformation", "aggregation",
        "groupby", "merge", "join", "pivot", "reshape", "time series",
        "missing data", "io", "csv", "excel", "sql", "hdf5"
    },
    cascades_to=[
        "Python Cookbook 3rd"
    ],
    relevance_weight=0.8  # Lower unless data-specific concepts
)

LEARNING_PYTHON_ED6 = BookRole(
    book_name="Learning Python Ed6",
    tier=BookTier.ENGINEERING_PRACTICES,
    primary_focus="Comprehensive Python tutorial (primary text)",
    keyword_triggers={
        "tutorial", "learning", "beginner", "introduction", "fundamental",
        "basic", "core", "concept", "syntax", "type", "function", "class",
        "module", "exception", "iterator", "generator", "decorator",
        "comprehension", "object", "variable", "operator", "statement"
    },
    cascades_to=[
        "Python Distilled",
        "Fluent Python 2nd"
    ],
    relevance_weight=0.5  # Lower weight (it's the primary text being annotated)
)


# ============================================================================
# TAXONOMY REGISTRY
# ============================================================================

ALL_BOOKS = [
    # Architecture Spine
    ARCHITECTURE_PATTERNS_WITH_PYTHON,
    BUILDING_MICROSERVICES,
    MICROSERVICE_ARCHITECTURE,
    PYTHON_ARCHITECTURE_PATTERNS,
    
    # Implementation
    BUILDING_PYTHON_MICROSERVICES_WITH_FASTAPI,
    MICROSERVICE_APIS_USING_PYTHON_FLASK_FASTAPI,
    PYTHON_MICROSERVICES_DEVELOPMENT,
    MICROSERVICES_UP_AND_RUNNING,
    
    # Engineering Practices
    FLUENT_PYTHON_2ND,
    PYTHON_DISTILLED,
    PYTHON_COOKBOOK_3RD,
    PYTHON_ESSENTIAL_REFERENCE_4TH,
    PYTHON_DATA_ANALYSIS_3RD,
    LEARNING_PYTHON_ED6,
]

BOOK_REGISTRY: Dict[str, BookRole] = {
    book.book_name: book for book in ALL_BOOKS
}


# ============================================================================
# CASCADING LOGIC
# ============================================================================

def get_cascading_books(book_name: str, depth: int = 1) -> List[str]:
    """Get cascading book recommendations.
    
    Args:
        book_name: Starting book name
        depth: How many levels deep to cascade (default 1)
        
    Returns:
        List of book names in cascading order
        
    Example:
        get_cascading_books("Architecture Patterns with Python", depth=1)
        -> ["Building Python Microservices with FastAPI", "Python Architecture Patterns"]
    """
    if book_name not in BOOK_REGISTRY:
        return []
    
    book_role = BOOK_REGISTRY[book_name]
    cascaded = list(book_role.cascades_to)
    
    if depth > 1:
        for cascaded_book in book_role.cascades_to:
            cascaded.extend(get_cascading_books(cascaded_book, depth - 1))
    
    # Remove duplicates while preserving order
    seen = set()
    return [b for b in cascaded if not (b in seen or seen.add(b))]


def get_books_by_tier(tier: BookTier) -> List[BookRole]:
    """Get all books in a specific tier.
    
    Args:
        tier: BookTier enum value
        
    Returns:
        List of BookRole objects in that tier
    """
    return [book for book in ALL_BOOKS if book.tier == tier]


def score_books_for_concepts(concepts: Set[str]) -> List[tuple[str, float]]:
    """Score all books based on concept relevance.
    
    Args:
        concepts: Set of concept strings from a chapter
        
    Returns:
        List of (book_name, relevance_score) tuples, sorted by score descending
        
    Example:
        concepts = {"decorator", "async", "fastapi", "api"}
        -> [("Building Python Microservices with FastAPI", 0.85), ...]
    """
    scores = []
    
    # Normalize concepts to lowercase for matching
    normalized_concepts = {c.lower() for c in concepts}
    
    for book in ALL_BOOKS:
        score = book.matches_concepts(normalized_concepts)
        if score > 0.0:
            scores.append((book.book_name, score))
    
    return sorted(scores, key=lambda x: x[1], reverse=True)


def get_recommended_books(
    concepts: Set[str],
    min_relevance: float = 0.3,
    include_cascades: bool = True,
    max_books: int = 15
) -> List[str]:
    """Get intelligent book recommendations with cascading.
    
    This is the main entry point for book selection.
    
    Args:
        concepts: Set of concepts from the chapter
        min_relevance: Minimum relevance score (0.0 to 1.0)
        include_cascades: Whether to include cascading recommendations
        max_books: Maximum number of books to return
        
    Returns:
        List of recommended book names in priority order
        
    Architecture:
        1. Score all books by concept match
        2. Filter by minimum relevance threshold
        3. If cascading enabled, add cascaded books
        4. Limit to max_books
        5. Organize by tier (Architecture → Implementation → Practices)
    """
    # Get initial scores
    scored_books = score_books_for_concepts(concepts)
    
    # Filter by minimum relevance
    relevant_books = [
        book_name for book_name, score in scored_books
        if score >= min_relevance
    ]
    
    # Add cascading recommendations
    if include_cascades:
        cascaded = set()
        for book_name in relevant_books[:5]:  # Cascade from top 5
            cascaded.update(get_cascading_books(book_name, depth=1))
        relevant_books.extend(list(cascaded))
    
    # Remove duplicates while preserving order
    seen = set()
    unique_books = [b for b in relevant_books if not (b in seen or seen.add(b))]
    
    # Organize by tier (Architecture → Implementation → Practices)
    def tier_priority(book_name: str) -> int:
        if book_name not in BOOK_REGISTRY:
            return 999
        tier = BOOK_REGISTRY[book_name].tier
        return {
            BookTier.ARCHITECTURE_SPINE: 0,
            BookTier.IMPLEMENTATION: 1,
            BookTier.ENGINEERING_PRACTICES: 2
        }.get(tier, 999)
    
    organized = sorted(unique_books, key=tier_priority)
    
    return organized[:max_books]


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def print_taxonomy():
    """Print the complete book taxonomy for debugging."""
    for tier in BookTier:
        print(f"\n{tier.value}")
        print("=" * 70)
        for book in get_books_by_tier(tier):
            print(f"\n{book.book_name}")
            print(f"  Focus: {book.primary_focus}")
            print(f"  Weight: {book.relevance_weight}")
            print(f"  Triggers: {len(book.keyword_triggers)} keywords")
            print(f"  Cascades: {', '.join(book.cascades_to) if book.cascades_to else 'None'}")


if __name__ == "__main__":
    # Example usage
    print("Book Taxonomy System")
    print("=" * 70)
    
    # Test with decorator concepts
    test_concepts = {"decorator", "async", "fastapi", "api", "dependency injection"}
    print(f"\nTest concepts: {test_concepts}")
    print("\nRecommended books:")
    
    recommendations = get_recommended_books(test_concepts, min_relevance=0.2)
    for i, book_name in enumerate(recommendations, 1):
        tier = BOOK_REGISTRY[book_name].tier.value
        print(f"  {i}. {book_name} ({tier})")
    
    print("\n" + "=" * 70)
    print_taxonomy()
