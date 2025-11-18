#!/usr/bin/env python3
"""
generate_concept_taxonomy.py

Generates a concept taxonomy by analyzing books organized into tiers.
Extracts concepts from book content and metadata to create a holistic taxonomy.

Flow:
1. Load books from each tier (Architecture, Implementation, Practices)
2. Extract concepts using same logic as guideline generator
3. Enrich with metadata keywords/concepts if available
4. Perform frequency analysis to determine tier-appropriate concepts
5. Output structured taxonomy JSON for use by guideline generator

Reference: workflows/base_guideline_generation/scripts/chapter_generator_all_text.py
"""

import json
import re
import argparse
from pathlib import Path
from typing import Dict, List, Set, Any, Tuple
from collections import Counter, defaultdict

# -------------------------------
# Configuration
# -------------------------------

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent.parent.parent
WORKFLOWS_DIR = REPO_ROOT / "workflows"
JSON_DIR = WORKFLOWS_DIR / "pdf_to_json" / "output" / "textbooks_json"
METADATA_DIR = WORKFLOWS_DIR / "metadata_extraction" / "output"
OUTPUT_DIR = WORKFLOWS_DIR / "taxonomy_setup" / "output"

# Comprehensive Python concepts (same as guideline generator)
# This serves as our master list for pattern matching
COMPREHENSIVE_CONCEPTS = [
    # Core Language
    "variable", "function", "class", "method", "object", "module",
    "package", "namespace", "scope", "closure", "decorator", "generator",
    "iterator", "comprehension", "lambda", "async", "await", "coroutine",
    
    # Data Types
    "string", "integer", "float", "boolean", "list", "tuple", "dict",
    "set", "bytes", "bytearray", "frozenset", "None",
    
    # Control Flow
    "if", "else", "elif", "for", "while", "break", "continue", "pass",
    "try", "except", "finally", "raise", "with", "match", "case",
    
    # OOP
    "inheritance", "polymorphism", "encapsulation", "abstraction",
    "composition", "interface", "mixin", "metaclass", "property",
    "classmethod", "staticmethod", "dataclass",
    
    # Functional Programming
    "map", "filter", "reduce", "pure function", "immutable",
    "higher-order function", "partial application", "recursion",
    
    # Advanced
    "context manager", "descriptor", "protocol", "type hint", "annotation",
    "generic", "overload", "async context manager", "async generator",
    
    # Standard Library
    "collections", "itertools", "functools", "operator", "pathlib",
    "datetime", "re", "json", "csv", "sqlite3", "argparse",
    
    # Data Structures
    "stack", "queue", "deque", "heap", "tree", "graph", "hash table",
    "linked list", "array", "matrix", "data structure",
    
    # Patterns & Practices
    "design pattern", "singleton", "factory", "observer", "strategy",
    "dependency injection", "SOLID", "DRY", "KISS", "YAGNI",
    "test-driven development", "refactoring", "code smell",
    
    # Testing & Quality
    "unittest", "pytest", "mock", "fixture", "assertion", "coverage",
    "integration test", "unit test", "end-to-end test",
    
    # Performance
    "optimization", "profiling", "benchmark", "memory management",
    "garbage collection", "reference counting", "caching",
    
    # Concurrency
    "threading", "multiprocessing", "asyncio", "concurrent",
    "parallel", "race condition", "deadlock", "semaphore", "lock",
    
    # Architecture
    "microservices", "API", "REST", "GraphQL", "event-driven",
    "message queue", "pub/sub", "CQRS", "event sourcing",
    "domain-driven design", "hexagonal architecture", "clean architecture",
    
    # Web & Network
    "HTTP", "HTTPS", "WebSocket", "TCP", "UDP", "socket",
    "request", "response", "middleware", "routing", "endpoint",
    
    # Database
    "SQL", "ORM", "migration", "transaction", "ACID", "index",
    "query optimization", "connection pool", "repository pattern",
    
    # DevOps & Tools
    "Docker", "Kubernetes", "CI/CD", "pipeline", "deployment",
    "monitoring", "logging", "tracing", "metrics", "observability"
]


def extract_concepts_from_text(text: str, concept_list: List[str]) -> Set[str]:
    """
    Extract concepts found in text using pattern matching.
    Same logic as guideline generator.
    """
    text_lower = text.lower()
    found = set()
    for concept in concept_list:
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(concept.lower()) + r'\b'
        if re.search(pattern, text_lower):
            found.add(concept)
    return found


def load_book_json(filepath: Path) -> Dict[str, Any]:
    """Load book JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_book_metadata(book_name: str) -> Dict[str, Any]:
    """
    Load metadata file for a book if it exists.
    Metadata contains pre-extracted keywords and concepts.
    """
    # Convert book.json to book_metadata.json
    metadata_name = book_name.replace('.json', '_metadata.json')
    metadata_path = METADATA_DIR / metadata_name
    
    if metadata_path.exists():
        with open(metadata_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def extract_concepts_from_book(book_path: Path) -> Tuple[Set[str], Dict[str, int]]:
    """
    Extract concepts from a book using:
    1. Content analysis (like guideline generator)
    2. Metadata keywords/concepts (if available)
    
    Returns:
        - Set of unique concepts
        - Frequency count of each concept
    """
    book_data = load_book_json(book_path)
    book_name = book_path.name
    metadata = load_book_metadata(book_name)
    
    concept_freq = Counter()
    all_concepts = set()
    
    # Extract from book content (pages)
    pages = book_data.get('pages', [])
    for page in pages:
        content = page.get('content', '')
        if content:
            concepts = extract_concepts_from_text(content, COMPREHENSIVE_CONCEPTS)
            all_concepts.update(concepts)
            concept_freq.update(concepts)
    
    # Enrich with metadata if available
    if metadata:
        for chapter in metadata:
            # Add keywords from metadata
            keywords = chapter.get('keywords', [])
            for keyword in keywords:
                # Check if keyword matches any concept
                matching = extract_concepts_from_text(keyword, COMPREHENSIVE_CONCEPTS)
                if matching:
                    all_concepts.update(matching)
                    concept_freq.update(matching)
                else:
                    # Add the keyword itself if it doesn't match known concepts
                    all_concepts.add(keyword)
                    concept_freq[keyword] += 1
            
            # Add concepts from metadata
            concepts = chapter.get('concepts', [])
            for concept in concepts:
                all_concepts.add(concept)
                concept_freq[concept] += 1
    
    return all_concepts, dict(concept_freq)


def categorize_concepts_by_tier(
    tier_concepts: Dict[str, Dict[str, int]],
    tier_book_counts: Dict[str, int]
) -> Dict[str, List[str]]:
    """
    Categorize concepts based on which tier(s) they appear in and their frequency.
    
    Strategy:
    - Architecture tier: Concepts that appear most frequently in architecture books
    - Implementation tier: Concepts specific to implementation books
    - Practices tier: Concepts specific to practices books (optional)
    
    Uses frequency analysis to determine tier membership.
    """
    categorized = {
        "architecture": [],
        "implementation": [],
        "practices": []
    }
    
    # Collect all unique concepts across all tiers
    all_concepts = set()
    for tier_freq in tier_concepts.values():
        all_concepts.update(tier_freq.keys())
    
    # Categorize each concept based on where it appears most
    for concept in sorted(all_concepts):
        arch_freq = tier_concepts.get('architecture', {}).get(concept, 0)
        impl_freq = tier_concepts.get('implementation', {}).get(concept, 0)
        prac_freq = tier_concepts.get('practices', {}).get(concept, 0)
        
        # Normalize by number of books in each tier to avoid bias
        arch_books = tier_book_counts.get('architecture', 1)
        impl_books = tier_book_counts.get('implementation', 1)
        prac_books = tier_book_counts.get('practices', 1)
        
        arch_norm = arch_freq / max(arch_books, 1)
        impl_norm = impl_freq / max(impl_books, 1)
        prac_norm = prac_freq / max(prac_books, 1)
        
        # Assign to tier with highest normalized frequency
        if arch_norm >= impl_norm and arch_norm >= prac_norm and arch_freq > 0:
            categorized["architecture"].append(concept)
        elif impl_norm >= prac_norm and impl_freq > 0:
            categorized["implementation"].append(concept)
        elif prac_freq > 0:
            categorized["practices"].append(concept)
        else:
            # If no clear winner, assign to implementation as middle ground
            categorized["implementation"].append(concept)
    
    return categorized


def generate_taxonomy(tier_books: Dict[str, List[str]], output_name: str) -> None:
    """
    Generate taxonomy from books organized into tiers.
    
    Args:
        tier_books: Dict mapping tier name to list of book filenames
        output_name: Name for output taxonomy file
    """
    print(f"\n🔍 Analyzing books for taxonomy generation...")
    print(f"Output: {output_name}")
    
    # Track concepts and frequencies per tier
    tier_concepts = {}
    tier_book_counts = {}
    
    # Process each tier
    for tier_name, book_files in tier_books.items():
        if not book_files:
            continue
            
        print(f"\n📚 Processing {tier_name} tier ({len(book_files)} books)...")
        tier_book_counts[tier_name] = len(book_files)
        
        tier_freq = Counter()
        tier_concepts_set = set()
        
        for book_file in book_files:
            book_path = JSON_DIR / book_file
            if not book_path.exists():
                print(f"  ⚠️  Book not found: {book_file}")
                continue
            
            print(f"  📖 Analyzing: {book_file}")
            concepts, freq = extract_concepts_from_book(book_path)
            tier_concepts_set.update(concepts)
            tier_freq.update(freq)
        
        tier_concepts[tier_name] = dict(tier_freq)
        print(f"  ✓ Found {len(tier_concepts_set)} unique concepts")
    
    # Categorize concepts by tier
    print(f"\n🎯 Categorizing concepts by tier...")
    categorized = categorize_concepts_by_tier(tier_concepts, tier_book_counts)
    
    # Build taxonomy structure
    taxonomy = {
        "tiers": {}
    }
    
    tier_info = {
        "architecture": {
            "priority": 1,
            "name": "Architecture Spine",
            "description": "Foundational concepts that form the structural backbone"
        },
        "implementation": {
            "priority": 2,
            "name": "Implementation",
            "description": "Practical techniques and concrete implementations"
        },
        "practices": {
            "priority": 3,
            "name": "Engineering Practices",
            "description": "Professional methodologies and best practices"
        }
    }
    
    for tier_name, concepts in categorized.items():
        if concepts:  # Only include tiers with concepts
            info = tier_info[tier_name]
            taxonomy["tiers"][tier_name] = {
                "priority": info["priority"],
                "concepts": sorted(list(set(concepts)))  # Deduplicate and sort
            }
            print(f"  {info['name']}: {len(concepts)} concepts")
    
    # Save taxonomy
    output_path = OUTPUT_DIR / output_name
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(taxonomy, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Taxonomy generated: {output_path}")
    print(f"📊 Total tiers: {len(taxonomy['tiers'])}")
    total_concepts = sum(len(t['concepts']) for t in taxonomy['tiers'].values())
    print(f"📊 Total concepts: {total_concepts}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate concept taxonomy from books organized into tiers"
    )
    parser.add_argument(
        "--tiers",
        type=str,
        required=True,
        help="JSON string with tier organization: {\"architecture\": [\"book1.json\"], ...}"
    )
    parser.add_argument(
        "--output",
        type=str,
        required=False,
        help="Output filename (optional - auto-generated from source book if not provided)"
    )
    
    args = parser.parse_args()
    
    # Parse tier data
    try:
        tier_books = json.loads(args.tiers)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing --tiers JSON: {e}")
        return 1
    
    # Auto-generate output filename if not provided
    if not args.output:
        # Get first book from tiers to derive taxonomy name
        all_books = []
        for books in tier_books.values():
            all_books.extend(books)
        
        if not all_books:
            print("❌ Error: No books specified in tiers")
            return 1
        
        # Use first book's name for taxonomy filename
        # makinggames.json → makinggames_taxonomy.json
        first_book = all_books[0]
        base_name = first_book.replace('.json', '')
        args.output = f"{base_name}_taxonomy.json"
        print(f"📝 Auto-generated output filename: {args.output}")
    
    # Validate output filename
    if not args.output.endswith('.json'):
        args.output += '.json'
    
    # Generate taxonomy
    try:
        generate_taxonomy(tier_books, args.output)
        return 0
    except Exception as e:
        print(f"\n❌ Error generating taxonomy: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
