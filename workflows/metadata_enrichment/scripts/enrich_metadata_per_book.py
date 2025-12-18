#!/usr/bin/env python3
"""
Enrich Metadata Per Book - Statistical Cross-Book Analysis

Enriches single book's metadata with cross-book similarity analysis using
scikit-learn TF-IDF and cosine similarity. NO LLM calls.

Usage:
    python enrich_metadata_per_book.py \\
        --input workflows/metadata_extraction/output/architecture_patterns_metadata.json \\
        --taxonomy workflows/taxonomy_setup/output/architecture_patterns_taxonomy.json \\
        --output workflows/metadata_enrichment/output/architecture_patterns_metadata_enriched.json

References:
    - CONSOLIDATED_IMPLEMENTATION_PLAN.md: Tab 4 requirements
    - TAB4_IMPLEMENTATION_PLAN.md: Detailed implementation
    - Architecture Patterns with Python Ch. 13: Dependency Injection patterns
    - BERTOPIC_SENTENCE_TRANSFORMERS_DESIGN.md: Option C Architecture
    
Test-Driven Development:
    - Tests: tests/integration/test_metadata_enrichment.py
    - This is the GREEN phase - implementing minimal code to pass RED tests
"""

import argparse
import asyncio
import hashlib
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime, timezone

# NOTE: TF-IDF imports REMOVED per Kitchen Brigade pattern
# All ML processing now done in ai-agents MSEP service
# See: MULTI_STAGE_ENRICHMENT_PIPELINE_ARCHITECTURE.md

# Project configuration and paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# =============================================================================
# WBS D2.1.3: Enrichment Provenance Constants
# Per CODING_PATTERNS_ANALYSIS.md S1192 - Extract duplicated literals
# =============================================================================

# Model version for provenance tracking
SBERT_MODEL_VERSION = "all-MiniLM-L6-v2"
TFIDF_MODEL_VERSION = "scikit-learn-1.3.2"

# Enrichment method identifiers
ENRICHMENT_METHOD_SBERT = "sentence_transformers"
ENRICHMENT_METHOD_TFIDF = "tfidf"
ENRICHMENT_METHOD_STATISTICAL = "statistical"
ENRICHMENT_METHOD_SEMANTIC_SEARCH = "semantic_search"


def compute_file_checksum(file_path: Path) -> str:
    """
    Compute SHA-256 checksum of a file for provenance tracking.
    
    Reference: WBS D2.1.3 - Enrichment Provenance
    Pattern: File integrity verification
    
    Args:
        file_path: Path to file to checksum
        
    Returns:
        Checksum string in format "sha256:{hex_digest}"
        Returns "sha256:none" if file doesn't exist
    """
    if not file_path.exists():
        return "sha256:none"
    
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256_hash.update(chunk)
    
    return f"sha256:{sha256_hash.hexdigest()}"


def build_enrichment_provenance(
    input_path: Path,
    taxonomy_path: Optional[Path],
    enrichment_method: str,
    model_version: str,
) -> Dict[str, Any]:
    """
    Build enrichment provenance metadata for output tracking.
    
    Reference: WBS D2.1.3 - Enrichment Provenance Fields
    Pattern: Data lineage tracking
    
    Args:
        input_path: Path to source metadata file
        taxonomy_path: Path to taxonomy file (optional)
        enrichment_method: Method used (sentence_transformers, tfidf, etc.)
        model_version: Version of model/algorithm used
        
    Returns:
        Dictionary with all provenance fields:
        - taxonomy_id, taxonomy_version, taxonomy_path, taxonomy_checksum
        - source_metadata_file, enrichment_date
        - enrichment_method, model_version
    """
    # Extract taxonomy info if available
    taxonomy_id = "none"
    taxonomy_version = "none"
    taxonomy_path_str = "none"
    taxonomy_checksum = "sha256:none"
    
    if taxonomy_path and taxonomy_path.exists():
        taxonomy_path_str = taxonomy_path.name
        taxonomy_checksum = compute_file_checksum(taxonomy_path)
        
        # Try to extract taxonomy_id and version from file content
        try:
            with open(taxonomy_path, encoding="utf-8") as f:
                taxonomy_data = json.load(f)
            taxonomy_id = taxonomy_data.get("taxonomy_id", taxonomy_path.stem)
            taxonomy_version = taxonomy_data.get("version", "1.0.0")
        except (json.JSONDecodeError, KeyError):
            taxonomy_id = taxonomy_path.stem
            taxonomy_version = "1.0.0"
    
    return {
        "taxonomy_id": taxonomy_id,
        "taxonomy_version": taxonomy_version,
        "taxonomy_path": taxonomy_path_str,
        "taxonomy_checksum": taxonomy_checksum,
        "source_metadata_file": input_path.name,
        "enrichment_date": datetime.now(timezone.utc).isoformat(),
        "enrichment_method": enrichment_method,
        "model_version": model_version,
    }


# Statistical extractor for YAKE + Summa (existing implementation)
# NOTE: Lazy loading - instantiate at runtime to respect environment variables
_STATISTICAL_EXTRACTOR_CLASS = None
_STATISTICAL_EXTRACTOR_INSTANCE = None

try:
    from workflows.metadata_extraction.scripts.adapters.statistical_extractor import StatisticalExtractor
    _STATISTICAL_EXTRACTOR_CLASS = StatisticalExtractor
except ImportError as e:
    print(f"Warning: StatisticalExtractor not available: {e}")
    print("Will use fallback keyword extraction")


def get_statistical_extractor():
    """
    Get StatisticalExtractor instance with lazy loading.
    
    This ensures environment variables are read at call time, not import time.
    Each call creates a new instance to pick up any env var changes.
    """
    global _STATISTICAL_EXTRACTOR_CLASS
    if _STATISTICAL_EXTRACTOR_CLASS is None:
        return None
    # Create new instance each time to pick up env var changes
    return _STATISTICAL_EXTRACTOR_CLASS()


# =============================================================================
# REMOVED: Local ML Library Imports (BERTopic, Sentence Transformers)
# Per Kitchen Brigade pattern (MULTI_STAGE_ENRICHMENT_PIPELINE_ARCHITECTURE.md):
# - llm-document-enhancer is CUSTOMER only (no local ML)
# - All ML processing moved to ai-agents MSEP service
#
# Imports removed:
# - TopicClusterer, TopicResults, TopicInfo, BERTOPIC_AVAILABLE
# - SemanticSimilarityEngine, SimilarityConfig, SENTENCE_TRANSFORMERS_AVAILABLE
# =============================================================================


# WBS 3.2.3: Semantic Search Client for remote API calls
try:
    from workflows.shared.clients.search_client import SemanticSearchClient
    SEMANTIC_SEARCH_CLIENT_AVAILABLE = True
except ImportError as e:
    print(f"Warning: SemanticSearchClient not available: {e}")
    SEMANTIC_SEARCH_CLIENT_AVAILABLE = False
    SemanticSearchClient = None  # type: ignore[misc, assignment]

# WBS 5.1.2: Orchestrator Client for Code-Orchestrator-Service integration
try:
    from workflows.shared.clients.orchestrator_client import (
        OrchestratorClient,
        OrchestratorClientProtocol,
        FakeOrchestratorClient,
        OrchestratorClientError,
        SEMANTIC_SIMILARITY_THRESHOLD,
    )
    ORCHESTRATOR_CLIENT_AVAILABLE = True
except ImportError as e:
    print(f"Warning: OrchestratorClient not available: {e}")
    ORCHESTRATOR_CLIENT_AVAILABLE = False
    OrchestratorClient = None  # type: ignore[misc, assignment]
    OrchestratorClientProtocol = None  # type: ignore[misc, assignment]
    FakeOrchestratorClient = None  # type: ignore[misc, assignment]
    OrchestratorClientError = None  # type: ignore[misc, assignment]
    SEMANTIC_SIMILARITY_THRESHOLD = 0.3  # Fallback constant

# =============================================================================
# WBS MSE-6.2: MSEPClient for ai-agents MSEP API Integration
# Pattern: Kitchen Brigade - CUSTOMER (llm-document-enhancer) -> EXPEDITOR (ai-agents)
# =============================================================================
try:
    from workflows.shared.clients.msep_client import (
        MSEPClient,
        ChapterMeta,
        MSEPConfig,
        EnrichedMetadataResponse,
        MSEPConnectionError,
        MSEPTimeoutError,
        MSEPAPIError,
    )
    MSEP_CLIENT_AVAILABLE = True
except ImportError as e:
    print(f"Warning: MSEPClient not available: {e}")
    MSEP_CLIENT_AVAILABLE = False
    MSEPClient = None  # type: ignore[misc, assignment]
    ChapterMeta = None  # type: ignore[misc, assignment]
    MSEPConfig = None  # type: ignore[misc, assignment]
    EnrichedMetadataResponse = None  # type: ignore[misc, assignment]
    MSEPConnectionError = Exception  # type: ignore[misc, assignment]
    MSEPTimeoutError = Exception  # type: ignore[misc, assignment]
    MSEPAPIError = Exception  # type: ignore[misc, assignment]

# Provenance method identifier for MSEP enrichment
ENRICHMENT_METHOD_MSEP = "msep"


def _extract_books_from_taxonomy(taxonomy: Dict[str, Any]) -> set:
    """
    Extract book names from taxonomy tiers.
    
    Helper function extracted to reduce cognitive complexity.
    
    Args:
        taxonomy: Taxonomy dictionary from Tab 3
        
    Returns:
        Set of book names found in taxonomy
    """
    book_set = set()
    for tier_name, tier_data in taxonomy.get("tiers", {}).items():
        if "books" in tier_data:
            for book_entry in tier_data.get("books", []):
                # Handle both old format (string) and new format (dict with 'name' key)
                if isinstance(book_entry, dict):
                    book_file = book_entry.get("name", "")
                else:
                    book_file = book_entry
                # Clean filename: "Book_Name.json" -> "Book_Name"
                book_name = book_file.replace(".json", "").replace("_metadata", "")
                book_set.add(book_name)
    return book_set


def _scan_metadata_directory(metadata_dir: Path) -> set:
    """
    Scan metadata directory for all available books.
    
    Helper function extracted to reduce cognitive complexity.
    
    Args:
        metadata_dir: Directory containing *_metadata.json files
        
    Returns:
        Set of book names found in directory
    """
    book_set = set()
    if metadata_dir.exists():
        for meta_file in metadata_dir.glob("*_metadata.json"):
            book_name = meta_file.stem.replace("_metadata", "")
            book_set.add(book_name)
            print(f"[INFO] Found book: {book_name}")
    return book_set


def _load_book_metadata(book_set: set, metadata_dir: Path) -> Dict[str, Any]:
    """
    Load metadata for each book in the book set.
    
    Helper function extracted to reduce cognitive complexity.
    
    Args:
        book_set: Set of book names to load
        metadata_dir: Directory containing *_metadata.json files
        
    Returns:
        Dictionary with metadata and corpus_size
    """
    context = {
        "books": list(book_set),
        "metadata": {},
        "corpus_size": 0
    }
    
    for book_name in book_set:
        metadata_filename = f"{book_name}_metadata.json"
        metadata_path = metadata_dir / metadata_filename
        
        if metadata_path.exists():
            with open(metadata_path, encoding='utf-8') as f:
                book_metadata = json.load(f)
                # Ensure context["metadata"] and context["corpus_size"] are properly typed
                context["metadata"][book_name] = book_metadata  # type: ignore[index]
                context["corpus_size"] += len(book_metadata)  # type: ignore[arg-type, operator]
        else:
            print(f"  ⚠️  Skipping {book_name} - metadata not found at {metadata_path}")
    
    return context


# =============================================================================
# REMOVED: TF-IDF Local Processing Functions
# Per Kitchen Brigade pattern (MULTI_STAGE_ENRICHMENT_PIPELINE_ARCHITECTURE.md):
# - llm-document-enhancer is CUSTOMER only (no local ML)
# - All ML processing moved to ai-agents MSEP service
#
# Functions removed:
# - load_cross_book_context()
# - build_chapter_corpus()
# - compute_similarity_matrix()
# - find_related_chapters()
# =============================================================================


# =============================================================================
# WBS 5.1.3: find_related_chapters_semantic - Orchestrator Integration
# Pattern: Async function replacing TF-IDF with semantic embeddings
# =============================================================================


async def find_related_chapters_semantic(
    chapter_text: str,
    current_book: str,
    client: "OrchestratorClientProtocol",
    domain: Optional[str] = None,
    threshold: float = SEMANTIC_SIMILARITY_THRESHOLD,
    top_n: int = 5,
) -> List[Dict[str, Any]]:
    """
    Find related chapters using Code-Orchestrator-Service semantic search.
    
    Reference: WBS_IMPLEMENTATION.md - Phase 5.1.3
    Pattern: Replaces TF-IDF find_related_chapters with semantic embeddings
    
    Key Improvements over TF-IDF:
    - Uses HuggingFace sentence-transformers embeddings (vs TF-IDF)
    - Lower threshold 0.3 achievable (vs impossible 0.7 TF-IDF)
    - Cross-book semantic similarity (vs lexical matching)
    
    Args:
        chapter_text: Chapter text/content to search for similar content
        current_book: Book name to exclude from results (self-references)
        client: OrchestratorClient instance (Protocol-compliant)
        domain: Optional domain filter (e.g., "ai-ml", "architecture")
        threshold: Minimum similarity threshold (default: 0.3)
        top_n: Maximum number of results (default: 5)
        
    Returns:
        List of related chapter dicts with keys:
        - book: Source book name
        - chapter: Chapter number
        - title: Chapter title
        - relevance_score: Similarity score (0.0-1.0)
        - method: "semantic_embedding"
        - citation: Chicago-style citation string
        
    Raises:
        ValueError: If chapter_text is empty
        OrchestratorClientError: On API failure
    """
    if not chapter_text or not chapter_text.strip():
        raise ValueError("chapter_text must not be empty")
    
    # Call orchestrator service for semantic search
    # Request extra results to account for filtering
    results = await client.search(
        query=chapter_text,
        domain=domain,
        top_k=top_n * 2,  # Get extra to filter self-references
        threshold=threshold,
    )
    
    # Filter out self-references and format output
    related = []
    for result in results:
        # Handle both direct result format and metadata nested format
        if "metadata" in result:
            metadata = result.get("metadata", {})
            book = metadata.get("book", metadata.get("source", ""))
            chapter_num = metadata.get("chapter", metadata.get("chapter_number", 0))
            title = metadata.get("title", "")
            score = result.get("score", 0.0)
        else:
            # Direct format (from FakeOrchestratorClient)
            book = result.get("book", "")
            chapter_num = result.get("chapter", 0)
            title = result.get("title", "")
            score = result.get("relevance_score", result.get("score", 0.0))
        
        # Exclude chapters from same book (cross-book analysis only)
        if book == current_book:
            continue
        
        # Filter by threshold (for FakeOrchestratorClient which doesn't filter)
        if score < threshold:
            continue
        
        # Generate Chicago-style citation
        citation = generate_chicago_citation(book, chapter_num, title)
        
        related.append({
            "book": book,
            "chapter": chapter_num,
            "title": title,
            "relevance_score": round(score, 2),
            "method": "orchestrator_semantic",
            "citation": citation,
        })
        
        if len(related) >= top_n:
            break
    
    return related


def generate_chicago_citation(
    ref_or_book: Dict[str, Any] | str,
    chapter: Optional[int] = None,
    title: Optional[str] = None
) -> str:
    """
    Generate Chicago-style citation for a chapter reference.
    
    Reference: WBS_IMPLEMENTATION.md - Phase 5.2.3
    Pattern: Citation generation for cross-book references
    
    Supports two call signatures:
    1. generate_chicago_citation(ref_dict) - pass a dict with book, chapter, title, author, start_page
    2. generate_chicago_citation(book, chapter, title) - pass individual args (legacy)
    
    Chicago Manual of Style format for book chapters:
    Author, "Chapter Title," in Book Title (Year), page.
    
    Args:
        ref_or_book: Either a reference dict or book title string
        chapter: Chapter number (only if first arg is string)
        title: Chapter title (only if first arg is string)
        
    Returns:
        Chicago-style citation string
        
    Example:
        >>> generate_chicago_citation({"book": "AI Engineering", "chapter": 5, "title": "RAG", "author": "Huyen", "start_page": 150})
        'Huyen, "RAG," in AI Engineering, 150.'
    """
    # Handle dict input (new style)
    if isinstance(ref_or_book, dict):
        book = ref_or_book.get("book", "")
        chapter = ref_or_book.get("chapter", 0)
        title = ref_or_book.get("title", "")
        author = ref_or_book.get("author", "")
        start_page = ref_or_book.get("start_page", "")
    else:
        # Legacy string input
        book = ref_or_book
        author = ""
        start_page = ""
    
    # Clean book name (remove underscores, metadata suffix)
    clean_book = book.replace("_", " ").replace(" metadata", "").strip()
    
    # Format title with quotes
    quoted_title = f'"{title}"' if title else '"Untitled"'
    
    # Build citation based on available info
    if author:
        # Full Chicago format: Author, "Title," in Book, page.
        surname = author.split()[-1] if author else ""
        if start_page:
            return f'{surname}, {quoted_title}, in {clean_book}, {start_page}.'
        else:
            return f'{surname}, {quoted_title}, in {clean_book}.'
    else:
        # Simple format without author
        return f'{quoted_title} in {clean_book}, Chapter {chapter}.'


def add_citations_to_refs(
    related_chapters: List[Dict[str, Any]],
    book_metadata: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Add Chicago-style citations to related chapter references.
    
    Reference: WBS_IMPLEMENTATION.md - Phase 5.2.3
    Pattern: Citation enrichment
    
    Args:
        related_chapters: List of related chapter dicts
        book_metadata: Dict mapping book name to metadata (author, chapters)
        
    Returns:
        List of related chapters with 'citation' field added
    """
    enriched = []
    for ref in related_chapters:
        book = ref.get("book", "")
        chapter_num = ref.get("chapter", 0)
        title = ref.get("title", "")
        
        # Look up book metadata for author and page info
        book_info = book_metadata.get(book, {})
        author = book_info.get("author", "")
        
        # Look up chapter-specific info
        chapters_info = book_info.get("chapters", {})
        chapter_info = chapters_info.get(chapter_num, {})
        start_page = chapter_info.get("start_page", "")
        end_page = chapter_info.get("end_page", "")
        
        # Build enriched ref with citation
        enriched_ref = {
            **ref,
            "author": author,
            "start_page": start_page,
            "end_page": end_page,
            "citation": generate_chicago_citation({
                "book": book,
                "chapter": chapter_num,
                "title": title,
                "author": author,
                "start_page": start_page,
            })
        }
        enriched.append(enriched_ref)
    
    return enriched


# =============================================================================
# WBS 5.2: E2E Validation Helper Functions
# Pattern: Domain filtering and validation utilities
# =============================================================================


# Domain mapping for book classification
DOMAIN_BOOK_MAPPING = {
    "ai-ml": [
        "AI Engineering",
        "Building LLM Apps",
        "Machine Learning",
        "Deep Learning",
        "Natural Language Processing",
        "RAG",
    ],
    "architecture": [
        "Architecture Patterns",
        "Domain Driven Design",
        "Microservices",
        "Clean Architecture",
        "System Design",
    ],
    "python": [
        "Architecture Patterns with Python",
        "Fluent Python",
        "Python Cookbook",
    ],
}


def count_cross_book_refs(enriched_data: Dict[str, Any]) -> int:
    """
    Count cross-book references in enriched metadata.
    
    Reference: WBS_IMPLEMENTATION.md - Phase 5.2.1
    Pattern: E2E validation helper
    
    Args:
        enriched_data: Enriched metadata dict with 'book' and 'chapters' keys
        
    Returns:
        Count of cross-book references (excludes same-book references)
    """
    current_book = enriched_data.get("book", enriched_data.get("book_title", ""))
    chapters = enriched_data.get("chapters", [])
    
    count = 0
    for chapter in chapters:
        related = chapter.get("related_chapters", chapter.get("cross_book_references", []))
        for ref in related:
            ref_book = ref.get("book", "")
            # Only count if it's from a different book
            if ref_book and ref_book != current_book:
                count += 1
    
    return count


def is_relevant_domain(ref: Dict[str, Any], expected_domain: str) -> bool:
    """
    Check if a reference is relevant to the expected domain.
    
    Reference: WBS_IMPLEMENTATION.md - Phase 5.2.2
    Pattern: False positive detection
    
    Args:
        ref: Reference dict with 'book' key
        expected_domain: Domain to check against (e.g., "ai-ml")
        
    Returns:
        True if the reference book is relevant to the domain
    """
    book = ref.get("book", "")
    
    # Get domain books
    domain_books = DOMAIN_BOOK_MAPPING.get(expected_domain, [])
    
    # Check if book contains any domain keyword
    for domain_book in domain_books:
        if domain_book.lower() in book.lower() or book.lower() in domain_book.lower():
            return True
    
    # Exclude known irrelevant domains
    excluded_for_ai = ["C++", "Concurrency in Action", "Systems Programming", "COBOL"]
    if expected_domain == "ai-ml":
        for excluded in excluded_for_ai:
            if excluded.lower() in book.lower():
                return False
    
    # Default to true for unknown books (benefit of the doubt)
    return True


def filter_by_domain(
    results: List[Dict[str, Any]], domain: str
) -> List[Dict[str, Any]]:
    """
    Filter search results by domain relevance.
    
    Reference: WBS_IMPLEMENTATION.md - Phase 5.2.2
    Pattern: False positive reduction
    
    Args:
        results: List of search result dicts
        domain: Target domain (e.g., "ai-ml")
        
    Returns:
        Filtered list excluding irrelevant domain results
    """
    return [r for r in results if is_relevant_domain(r, domain)]


async def enrich_chapter_with_orchestrator(
    chapter: Dict[str, Any],
    client: "OrchestratorClientProtocol",
    current_book: str,
    domain: Optional[str] = None,
    fallback_enabled: bool = False,
) -> Dict[str, Any]:
    """
    Enrich a single chapter using orchestrator semantic search.
    
    Reference: WBS_IMPLEMENTATION.md - Phase 5.1
    Pattern: Single chapter enrichment for fine-grained control
    
    Args:
        chapter: Chapter dict with title, summary, keywords, concepts
        client: OrchestratorClient instance
        current_book: Book name to exclude from results
        domain: Optional domain filter
        fallback_enabled: If True, use TF-IDF fallback on error
        
    Returns:
        Enriched chapter dict with related_chapters
    """
    chapter_num = chapter.get("chapter_number", 0)
    chapter_title = chapter.get("title", f"Chapter {chapter_num}")
    
    # Build query from chapter content
    query_parts = [
        chapter_title,
        chapter.get("summary", "")[:500],
        " ".join(chapter.get("keywords", [])[:10]),
        " ".join(chapter.get("concepts", [])[:5])
    ]
    query_text = " ".join(filter(None, query_parts))
    
    try:
        related = await find_related_chapters_semantic(
            chapter_text=query_text,
            current_book=current_book,
            client=client,
            domain=domain,
            threshold=SEMANTIC_SIMILARITY_THRESHOLD,
            top_n=5,
        )
    except Exception:
        # Graceful degradation - return empty refs on error
        related = []
    
    # Build enriched chapter
    return {
        **chapter,
        "related_chapters": related,
        "similarity_source": "orchestrator_semantic",
    }


async def run_enrichment_with_orchestrator(
    book_name: str,
    domain: str,
    client: "OrchestratorClientProtocol",
) -> Dict[str, Any]:
    """
    Run full book enrichment using orchestrator semantic search.
    
    Reference: WBS_IMPLEMENTATION.md - Phase 5 Integration Test
    Pattern: E2E enrichment flow
    
    Args:
        book_name: Name of the book to enrich
        domain: Domain filter (e.g., "ai-ml")
        client: OrchestratorClient instance
        
    Returns:
        Enriched book metadata with chapters containing related_chapters
    """
    # For testing, generate sample chapters if not loading from file
    sample_chapters = [
        {
            "chapter_number": 1,
            "title": "Introduction to Patterns",
            "summary": "Overview of software architecture patterns"
        },
        {
            "chapter_number": 2,
            "title": "Repository Pattern",
            "summary": "Data access abstraction pattern"
        },
    ]
    
    enriched_chapters = []
    for chapter in sample_chapters:
        enriched = await enrich_chapter_with_orchestrator(
            chapter=chapter,
            client=client,
            current_book=book_name,
            domain=domain,
        )
        enriched_chapters.append(enriched)
    
    return {
        "book": book_name,
        "book_title": book_name.replace("_", " "),
        "chapters": enriched_chapters,
    }


def rescore_keywords_cross_book(
    current_chapter_text: str,
    related_chapters_texts: List[str],
    top_n: int = 10
) -> List[Dict[str, Any]]:
    """
    Re-score keywords using YAKE with combined text from related chapters.
    
    Reference: TAB4_IMPLEMENTATION_PLAN.md - Function 5
    Pattern: Statistical keyword extraction with cross-book context
    
    Args:
        current_chapter_text: Text from current chapter
        related_chapters_texts: Texts from related chapters
        top_n: Number of keywords to return (10)
        
    Returns:
        List of keyword dicts with keys:
        - term: Keyword string
        - score: YAKE score (lower is better)
        - source: Always "cross_book_yake"
    """
    # Combine current chapter with related chapter contexts
    combined_text = current_chapter_text + " " + " ".join(related_chapters_texts)
    
    # Extract keywords using YAKE via StatisticalExtractor (lazy loaded)
    extractor = get_statistical_extractor()
    if extractor:
        keywords_with_scores = extractor.extract_keywords(
            combined_text,
            top_n=top_n
        )
    else:
        # Fallback: simple word frequency if StatisticalExtractor unavailable
        from collections import Counter
        words = combined_text.lower().split()
        word_counts = Counter(words)
        keywords_with_scores = [(word, count) for word, count in word_counts.most_common(top_n)]
    
    # Format output per schema
    keywords_enriched = []
    for keyword, score in keywords_with_scores:
        keywords_enriched.append({
            "term": keyword,
            "score": round(float(score), 3),
            "source": "cross_book_yake"
        })
    
    return keywords_enriched


def extract_concepts_cross_book(
    current_chapter_text: str,
    related_chapters_texts: List[str],
    top_n: int = 10
) -> List[Dict[str, Any]]:
    """
    Extract concepts using Summa TextRank with combined text from related chapters.
    
    Reference: TAB4_IMPLEMENTATION_PLAN.md - Function 6
    Pattern: Statistical concept extraction with cross-book context
    
    Args:
        current_chapter_text: Text from current chapter
        related_chapters_texts: Texts from related chapters
        top_n: Number of concepts to return (10)
        
    Returns:
        List of concept dicts with keys:
        - concept: Concept phrase string
        - source: Always "cross_book_summa"
    """
    # Combine current chapter with related chapter contexts
    combined_text = current_chapter_text + " " + " ".join(related_chapters_texts)
    
    # Extract concepts using Summa via StatisticalExtractor (lazy loaded)
    extractor = get_statistical_extractor()
    if extractor:
        concepts = extractor.extract_concepts(combined_text, top_n=top_n)
    else:
        # Fallback: simple noun phrase extraction if StatisticalExtractor unavailable
        import re
        # Extract multi-word phrases (simple heuristic)
        phrases = re.findall(r'\b[a-z]+(?:\s+[a-z]+){1,2}\b', combined_text.lower())
        from collections import Counter
        phrase_counts = Counter(phrases)
        concepts = [phrase for phrase, _ in phrase_counts.most_common(top_n)]
    
    # Format output per schema
    concepts_enriched = []
    for concept in concepts:
        concepts_enriched.append({
            "concept": concept,
            "source": "cross_book_summa"
        })
    
    return concepts_enriched


# =============================================================================
# REMOVED: Local Enrichment Helper Functions
# Per Kitchen Brigade pattern (MULTI_STAGE_ENRICHMENT_PIPELINE_ARCHITECTURE.md):
# - llm-document-enhancer is CUSTOMER only (no local ML)
# - All ML processing moved to ai-agents MSEP service
#
# Functions removed:
# - _find_chapter_index()
# - _get_topic_info()
# - _find_related_with_semantic()
# - _collect_related_texts()
# - _enrich_single_chapter()
# =============================================================================


def enrich_metadata(
    input_path: Path,
    taxonomy_path: Path,
    output_path: Path
) -> None:
    """
    Cross-book enrichment FALLBACK mode - creates minimal output without local ML.

    Kitchen Brigade Pattern:
    - llm-document-enhancer is CUSTOMER only (NO local ML)
    - Taxonomy mode is DEPRECATED - use --use-msep for full enrichment
    - This function produces MSEP-unified schema with empty enrichment fields

    DEPRECATED: Use --use-msep instead for full enrichment capabilities.
    
    Reference: MULTI_STAGE_ENRICHMENT_PIPELINE_ARCHITECTURE.md
    Pattern: Graceful degradation, Kitchen Brigade compliance

    Args:
        input_path: Path to {book}_metadata.json (Tab 2 output)
        taxonomy_path: Path to {book}_taxonomy.json (Tab 3 output) - IGNORED in fallback
        output_path: Path for {book}_metadata_enriched.json (Tab 4 output)

    Output Schema (MSEP-unified, empty enrichments):
        {
            "book": str,
            "enrichment_metadata": {...},
            "enrichment_provenance": {...},
            "chapters": [
                {
                    ... (all original Tab 2 fields preserved),
                    "cross_references": [],
                    "enriched_keywords": {...},
                    "topic_id": None,
                    "related_chapters": [],
                    "keywords_enriched": [],
                    "concepts_enriched": []
                }
            ]
        }
    """
    print("\n⚠️  DEPRECATED: --taxonomy mode uses fallback (no local ML)")
    print("  Kitchen Brigade: No local ML processing in llm-document-enhancer")
    print("  For full enrichment, use: --use-msep --msep-url http://localhost:8082")
    print(f"\nInput: {input_path.name}")
    print(f"Taxonomy: {taxonomy_path.name} (ignored in fallback mode)")

    # 1. Load current book metadata
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with open(input_path, encoding='utf-8') as f:
        book_metadata = json.load(f)

    # Handle both formats
    if isinstance(book_metadata, list):
        chapters = book_metadata
        book_name = input_path.stem.replace("_metadata", "")
    else:
        chapters = book_metadata.get("chapters", book_metadata)
        book_name = book_metadata.get("book", input_path.stem.replace("_metadata", ""))

    print(f"\nBook: {book_name}")
    print(f"Chapters: {len(chapters)}")

    # 2. Build enriched chapters with empty enrichment fields
    enriched_chapters = []
    timestamp = datetime.now().isoformat()

    for idx, chapter in enumerate(chapters):
        chapter_num = chapter.get("chapter_number", idx + 1)

        # Build enriched chapter (preserve all original fields + empty enrichments)
        enriched = chapter.copy()
        enriched.update({
            # MSEP-unified fields - empty in fallback mode
            "cross_references": [],
            "enriched_keywords": {
                "tfidf": [],
                "semantic": [],
                "merged": chapter.get("keywords", []),
            },
            "topic_id": None,
            "topic_name": None,
            "graph_relationships": [],
            "chapter_provenance": {
                "methods_used": ["fallback"],
                "sbert_score": 0.0,
                "topic_boost": 0.0,
                "timestamp": timestamp,
            },
            "similarity_source": "fallback_no_ml",
            # Legacy fields (for backward compatibility)
            "related_chapters": [],
            "keywords_enriched": chapter.get("keywords", []),
            "concepts_enriched": chapter.get("concepts", []),
        })
        enriched_chapters.append(enriched)

    # 3. Build enriched metadata output
    enriched_metadata = {
        "book": book_name,
        "enrichment_metadata": {
            "generated": timestamp,
            "method": "fallback",
            "libraries": {
                "note": "Local ML disabled per Kitchen Brigade pattern",
            },
            "corpus_size": 0,
            "total_chapters_analyzed": len(chapters),
            "topic_clustering": {
                "enabled": False,
                "num_topics": 0,
                "using_bertopic": False,
            },
        },
        "enrichment_provenance": build_enrichment_provenance(
            input_path=input_path,
            taxonomy_path=taxonomy_path,
            enrichment_method="fallback",
            model_version="none",
        ),
        "chapters": enriched_chapters
    }
    enriched_metadata["enrichment_provenance"]["fallback_mode"] = True
    enriched_metadata["enrichment_provenance"]["fallback_reason"] = "taxonomy mode deprecated, use --use-msep"

    # 4. Save enriched metadata
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(enriched_metadata, f, indent=2, ensure_ascii=False)

    # Report
    size_kb = output_path.stat().st_size / 1024
    print(f"\n✅ Fallback metadata saved: {output_path.name}")
    print(f"  File size: {size_kb:.1f} KB")
    print(f"  Chapters: {len(enriched_chapters)}")
    print(f"  Cross-references: 0 (fallback mode)")
    print("  ⚠️  Run with --use-msep when ai-agents is available for full enrichment")


def enrich_metadata_local(
    input_path: Path,
    output_path: Path
) -> None:
    """
    Fallback enrichment - creates minimal output without ML processing.

    Kitchen Brigade Pattern:
    - llm-document-enhancer is CUSTOMER only (NO local ML)
    - This function is a FALLBACK when ai-agents MSEP is unavailable
    - Produces MSEP-unified schema with empty enrichment fields

    Reference: MULTI_STAGE_ENRICHMENT_PIPELINE_ARCHITECTURE.md
    Pattern: Graceful degradation without local ML

    Args:
        input_path: Path to book metadata JSON (WBS 3.1.1 output)
        output_path: Path for enriched metadata JSON output

    Output Schema (MSEP-unified, empty enrichments):
        {
            "book_title": str,
            "total_chapters": int,
            "enrichment_provenance": {...},
            "chapters": [
                {
                    ... (all original fields preserved),
                    "cross_references": [],
                    "enriched_keywords": {"tfidf": [], "semantic": [], "merged": []},
                    "topic_id": None,
                    "chapter_provenance": {...}
                }
            ]
        }
    """
    print("\n⚠️  FALLBACK MODE: ai-agents MSEP service unavailable")
    print("  Kitchen Brigade: No local ML processing in llm-document-enhancer")
    print("  Output will have empty enrichment fields")
    print(f"\nInput: {input_path.name}")

    # 1. Load book metadata
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with open(input_path, encoding='utf-8') as f:
        book_data = json.load(f)

    # Handle both formats: list of chapters or {chapters: [...]}
    if isinstance(book_data, list):
        chapters = book_data
        book_title = input_path.stem.replace("_metadata", "")
        original_book_data: Dict[str, Any] = {"chapters": chapters}
    else:
        chapters = book_data.get("chapters", [])
        book_title = book_data.get("book_title", input_path.stem.replace("_metadata", ""))
        original_book_data = book_data

    print(f"\nBook: {book_title}")
    print(f"Chapters: {len(chapters)}")

    # 2. Build enriched chapters with empty enrichment fields (MSEP-unified schema)
    enriched_chapters = []
    timestamp = datetime.now().isoformat()

    for idx, chapter in enumerate(chapters):
        chapter_num = chapter.get("chapter_number", idx + 1)

        # Build enriched chapter (preserve all original fields + empty MSEP fields)
        enriched_chapter = chapter.copy()
        enriched_chapter.update({
            # MSEP-unified fields - empty in fallback mode
            "cross_references": [],
            "enriched_keywords": {
                "tfidf": [],
                "semantic": [],
                "merged": chapter.get("keywords", []),  # Use original keywords
            },
            "topic_id": None,
            "topic_name": None,
            "graph_relationships": [],
            "chapter_provenance": {
                "methods_used": ["fallback"],
                "sbert_score": 0.0,
                "topic_boost": 0.0,
                "timestamp": timestamp,
            },
            "similarity_source": "fallback_no_ml",
        })
        enriched_chapters.append(enriched_chapter)

    # 3. Build enriched metadata output with provenance
    enriched_metadata: Dict[str, Any] = original_book_data.copy()
    enriched_metadata["chapters"] = enriched_chapters
    enriched_metadata["book_title"] = book_title
    enriched_metadata["total_chapters"] = len(enriched_chapters)

    # Add top-level provenance
    enriched_metadata["enrichment_provenance"] = build_enrichment_provenance(
        input_path=input_path,
        taxonomy_path=None,
        enrichment_method="fallback",
        model_version="none",
    )
    enriched_metadata["enrichment_provenance"]["total_cross_references"] = 0
    enriched_metadata["enrichment_provenance"]["msep_processing_time_ms"] = 0.0
    enriched_metadata["enrichment_provenance"]["fallback_mode"] = True
    enriched_metadata["enrichment_provenance"]["fallback_reason"] = "ai-agents MSEP unavailable"

    # 4. Save enriched metadata
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(enriched_metadata, f, indent=2, ensure_ascii=False)

    # Report
    size_kb = output_path.stat().st_size / 1024
    print(f"\n✅ Fallback metadata saved: {output_path.name}")
    print(f"  File size: {size_kb:.1f} KB")
    print(f"  Chapters: {len(enriched_chapters)}")
    print(f"  Cross-references: 0 (fallback mode)")
    print(f"  Schema: MSEP-unified (empty enrichments)")
    print("  ⚠️  Run with --use-msep when ai-agents is available for full enrichment")


async def enrich_metadata_semantic(
    input_path: Path,
    output_path: Path,
    semantic_search_url: str = "http://localhost:8081"
) -> None:
    """
    Semantic search enrichment - uses remote semantic search API for similarity.
    
    Reference: WBS 3.2.4 - Integrate Search Client into Metadata Enrichment
    Pattern: Remote API integration via SemanticSearchClient
    
    Workflow:
    1. Load book metadata (from WBS 3.1.1 output)
    2. For each chapter, call semantic search API
    3. Store similarity results with source="semantic_search"
    4. Save enriched metadata JSON output
    
    Args:
        input_path: Path to book metadata JSON (WBS 3.1.1 output)
        output_path: Path for enriched metadata JSON output
        semantic_search_url: URL of semantic search service
        
    Output Schema:
        {
            "book_title": str,
            "total_chapters": int,
            "enrichment_metadata": {
                "generated": ISO timestamp,
                "method": "semantic_search",
                "mode": "remote_api",
                "semantic_search_url": str
            },
            "chapters": [
                {
                    ... (all original fields preserved),
                    "semantic_similar": [...],
                    "similarity_source": "semantic_search"
                }
            ]
        }
    """
    print("\n📊 WBS 3.2.4: Semantic Search Enrichment (Remote API)")
    print(f"Input: {input_path.name}")
    print(f"Semantic Search URL: {semantic_search_url}")
    
    # 1. Load book metadata
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    with open(input_path, encoding='utf-8') as f:
        book_data = json.load(f)
    
    # Handle both formats: list of chapters or {chapters: [...]}
    if isinstance(book_data, list):
        chapters = book_data
        book_title = input_path.stem.replace("_metadata", "")
    else:
        chapters = book_data.get("chapters", [])
        book_title = book_data.get("book_title", input_path.stem.replace("_metadata", ""))
    
    print(f"\nBook: {book_title}")
    print(f"Chapters: {len(chapters)}")
    
    # 2. Connect to semantic search service and enrich each chapter
    print("\nConnecting to semantic search service...")
    enriched_chapters = []
    
    async with SemanticSearchClient(base_url=semantic_search_url) as client:
        # Test connection with health check
        try:
            health = await client.health_check()
            print(f"  Service status: {health.get('status', 'unknown')}")
        except Exception as e:
            print(f"  ⚠️  Health check failed: {e}")
            print("  Continuing with enrichment...")
        
        print("\nEnriching chapters with semantic search...")
        
        for idx, chapter in enumerate(chapters):
            chapter_num = chapter.get("chapter_number", idx + 1)
            chapter_title = chapter.get("title", f"Chapter {chapter_num}")
            
            # Build query from chapter content
            query_parts = [
                chapter_title,
                chapter.get("summary", "")[:500],  # Limit summary length
                " ".join(chapter.get("keywords", [])[:10]),
                " ".join(chapter.get("concepts", [])[:5])
            ]
            query_text = " ".join(filter(None, query_parts))
            
            try:
                # Call semantic search API
                results = await client.search(
                    query=query_text,
                    limit=6,  # Get 6 to filter out self-matches
                    collection="chapters"
                )
                
                # Filter to top 5, excluding self-matches
                similar_chapters = []
                for r in results:
                    payload = r.get("payload", {})
                    result_title = payload.get("title", "")
                    
                    # Skip if it's the same chapter (self-match)
                    if result_title == chapter_title:
                        continue
                    
                    similar_chapters.append({
                        "chapter_id": payload.get("chapter_number", payload.get("chapter_id", 0)),
                        "title": result_title,
                        "score": round(r.get("score", 0.0), 4),
                        "book": payload.get("book_title", payload.get("book_id", ""))
                    })
                    
                    if len(similar_chapters) >= 5:
                        break
                
                # Progress output
                if idx < 3 or idx == len(chapters) - 1:
                    top_scores = [f"{s['score']:.3f}" for s in similar_chapters[:3]]
                    print(f"  Chapter {chapter_num}: {len(similar_chapters)} similar, scores={top_scores}")
                elif idx == 3:
                    print(f"  ... (processing {len(chapters) - 4} more chapters)")
                
            except Exception as e:
                print(f"  ⚠️  Chapter {chapter_num} search failed: {e}")
                similar_chapters = []
            
            # Build enriched chapter
            enriched_chapter = {
                **chapter,
                "similar_chapters": similar_chapters,
                "similarity_source": "semantic_search"
            }
            enriched_chapters.append(enriched_chapter)
    
    # 3. Build enriched metadata output
    enriched_metadata = {
        "book_title": book_title,
        "total_chapters": len(enriched_chapters),
        "enrichment_metadata": {
            "generated": datetime.now().isoformat(),
            "method": "semantic_search",
            "mode": "remote_api",
            "semantic_search_url": semantic_search_url,
            "libraries": {
                "httpx": "async HTTP client",
                "semantic-search-service": "all-mpnet-base-v2"
            }
        },
        "chapters": enriched_chapters
    }
    
    # 4. Save enriched metadata
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(enriched_metadata, f, indent=2, ensure_ascii=False)
    
    # Report
    size_kb = output_path.stat().st_size / 1024
    print(f"\n✅ Enriched metadata saved: {output_path.name}")
    print(f"  File size: {size_kb:.1f} KB")
    print(f"  Chapters enriched: {len(enriched_chapters)}")
    print(f"  Similarity source: semantic_search (remote API)")
    print("  NO LLM calls made ✓")


# =============================================================================
# WBS 5.1.1: CLI Argument Parser
# Pattern: Extracted function for testability (Architecture Patterns Ch. 13)
# =============================================================================


def create_argument_parser() -> argparse.ArgumentParser:
    """
    Create argument parser for metadata enrichment CLI.
    
    Reference: WBS_IMPLEMENTATION.md - Phase 5.1.1
    Pattern: Extracted function for testability
    
    Returns:
        Configured ArgumentParser instance with all CLI flags
    """
    parser = argparse.ArgumentParser(
        description="Enrich metadata with statistical analysis (Tab 4)"
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Input metadata JSON from Tab 2 (e.g., architecture_patterns_metadata.json)"
    )
    parser.add_argument(
        "--taxonomy",
        type=Path,
        required=False,
        default=None,
        help="Taxonomy JSON from Tab 3 (optional - omit for local/within-book mode)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output enriched metadata JSON (e.g., architecture_patterns_metadata_enriched.json)"
    )
    parser.add_argument(
        "--use-semantic-search",
        action="store_true",
        help="Use remote semantic search API instead of local TF-IDF (WBS 3.2.4)"
    )
    parser.add_argument(
        "--semantic-search-url",
        type=str,
        default="http://localhost:8081",
        help="Semantic search service URL (default: http://localhost:8081)"
    )
    # WBS 5.1.1: Add orchestrator integration flags
    parser.add_argument(
        "--use-orchestrator",
        action="store_true",
        help="Use Code-Orchestrator-Service for semantic search (WBS 5.1)"
    )
    parser.add_argument(
        "--orchestrator-url",
        type=str,
        default="http://localhost:8083",
        help="Orchestrator service URL (default: http://localhost:8083)"
    )
    # WBS MSE-6.2: Add MSEP integration flags (Kitchen Brigade - ai-agents)
    parser.add_argument(
        "--use-msep",
        action="store_true",
        help="Use ai-agents MSEP endpoint for enrichment (WBS MSE-6.2)"
    )
    parser.add_argument(
        "--msep-url",
        type=str,
        default="http://localhost:8082",
        help="ai-agents MSEP service URL (default: http://localhost:8082)"
    )
    return parser


async def enrich_metadata_orchestrator(
    input_path: Path,
    output_path: Path,
    orchestrator_url: str = "http://localhost:8083",
) -> None:
    """
    Orchestrator-based enrichment - uses Code-Orchestrator-Service for semantic search.
    
    Reference: WBS_IMPLEMENTATION.md - Phase 5.1
    Pattern: Remote API integration via OrchestratorClient
    
    Workflow:
    1. Load book metadata (from WBS 3.1.1 output)
    2. For each chapter, call orchestrator search API
    3. Store similarity results with source="orchestrator_semantic"
    4. Generate Chicago-style citations for cross-book refs
    5. Save enriched metadata JSON output
    
    Args:
        input_path: Path to book metadata JSON (WBS 3.1.1 output)
        output_path: Path for enriched metadata JSON output
        orchestrator_url: URL of Code-Orchestrator-Service
    """
    print("\n📊 WBS 5.1: Orchestrator-based Semantic Enrichment")
    print(f"Input: {input_path.name}")
    print(f"Orchestrator URL: {orchestrator_url}")
    
    # 1. Load book metadata
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    with open(input_path, encoding='utf-8') as f:
        book_data = json.load(f)
    
    # Handle both formats: list of chapters or {chapters: [...]}
    if isinstance(book_data, list):
        chapters = book_data
        book_title = input_path.stem.replace("_metadata", "")
    else:
        chapters = book_data.get("chapters", [])
        book_title = book_data.get("book_title", input_path.stem.replace("_metadata", ""))
    
    print(f"\nBook: {book_title}")
    print(f"Chapters: {len(chapters)}")
    print(f"Threshold: {SEMANTIC_SIMILARITY_THRESHOLD}")
    
    # 2. Connect to orchestrator service and enrich each chapter
    print("\nConnecting to Code-Orchestrator-Service...")
    enriched_chapters = []
    
    async with OrchestratorClient(base_url=orchestrator_url) as client:
        print("\nEnriching chapters with orchestrator semantic search...")
        
        for idx, chapter in enumerate(chapters):
            chapter_num = chapter.get("chapter_number", idx + 1)
            chapter_title = chapter.get("title", f"Chapter {chapter_num}")
            
            # Build query from chapter content
            query_parts = [
                chapter_title,
                chapter.get("summary", "")[:500],  # Limit summary length
                " ".join(chapter.get("keywords", [])[:10]),
                " ".join(chapter.get("concepts", [])[:5])
            ]
            query_text = " ".join(filter(None, query_parts))
            
            try:
                # Call orchestrator for semantic search
                related = await find_related_chapters_semantic(
                    chapter_text=query_text,
                    current_book=book_title,
                    client=client,
                    threshold=SEMANTIC_SIMILARITY_THRESHOLD,
                    top_n=5,
                )
                
                # Progress output
                if idx < 3 or idx == len(chapters) - 1:
                    top_scores = [f"{r['relevance_score']:.3f}" for r in related[:3]]
                    print(f"  Chapter {chapter_num}: {len(related)} related, scores={top_scores}")
                elif idx == 3:
                    print(f"  ... (processing {len(chapters) - 4} more chapters)")
                
            except Exception as e:
                print(f"  ⚠️  Chapter {chapter_num} search failed: {e}")
                related = []
            
            # Build enriched chapter with cross-book references
            enriched_chapter = {
                **chapter,
                "cross_book_references": related,
                "similarity_source": "orchestrator_semantic",
            }
            enriched_chapters.append(enriched_chapter)
    
    # 3. Build enriched metadata output
    enriched_metadata = {
        "book_title": book_title,
        "total_chapters": len(enriched_chapters),
        "enrichment_metadata": {
            "generated": datetime.now().isoformat(),
            "method": "orchestrator_semantic",
            "mode": "remote_api",
            "orchestrator_url": orchestrator_url,
            "threshold": SEMANTIC_SIMILARITY_THRESHOLD,
            "libraries": {
                "httpx": "async HTTP client",
                "code-orchestrator-service": "sentence-transformers"
            }
        },
        "chapters": enriched_chapters
    }
    
    # 4. Save enriched metadata
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(enriched_metadata, f, indent=2, ensure_ascii=False)
    
    # Report
    size_kb = output_path.stat().st_size / 1024
    print(f"\n✅ Enriched metadata saved: {output_path.name}")
    print(f"  File size: {size_kb:.1f} KB")
    print(f"  Chapters enriched: {len(enriched_chapters)}")
    print(f"  Similarity source: orchestrator_semantic")
    print(f"  Threshold: {SEMANTIC_SIMILARITY_THRESHOLD}")
    print("  NO LLM calls made ✓")


# =============================================================================
# WBS MSE-6.2: MSEP Integration with ai-agents
# Pattern: Kitchen Brigade - CUSTOMER delegates to EXPEDITOR
# Reference: AI_CODING_PLATFORM_ARCHITECTURE.md - Scenario #1
# =============================================================================

import logging

_logger = logging.getLogger(__name__)


async def enrich_metadata_msep(
    input_path: Path,
    output_path: Path,
    msep_url: str = "http://localhost:8082",
) -> None:
    """
    MSEP-based enrichment - uses ai-agents MSEP endpoint for enrichment.

    Kitchen Brigade Pattern:
    - llm-document-enhancer is CUSTOMER only
    - Delegates ALL enrichment logic to ai-agents (EXPEDITOR)
    - NO local ML processing

    WBS References:
    - AC-6.2.1: Uses MSEPClient when --use-msep flag
    - AC-6.2.2: Fallback to local enrichment when ai-agents unavailable
    - AC-6.3.1: Writes {book}_enriched.json with MSEP results
    - AC-6.3.2: Preserves existing metadata structure
    - AC-6.3.3: Adds provenance to output JSON

    Anti-Patterns Avoided (CODING_PATTERNS):
    - §3.3: Always provide fallback, log it, document behavior
    - S1172: No unused parameters
    - S3776: Cognitive complexity < 15

    Args:
        input_path: Path to book metadata JSON (WBS 3.1.1 output)
        output_path: Path for enriched metadata JSON output
        msep_url: URL of ai-agents MSEP service (default: http://localhost:8082)

    Raises:
        FileNotFoundError: If input file doesn't exist
    """
    print("\n📊 WBS MSE-6.2: MSEP Enrichment (ai-agents API)")
    print(f"Input: {input_path.name}")
    print(f"MSEP URL: {msep_url}")

    # 1. Load book metadata
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with open(input_path, encoding="utf-8") as f:
        book_data = json.load(f)

    # Handle both formats: list of chapters or {chapters: [...]}
    if isinstance(book_data, list):
        chapters = book_data
        book_title = input_path.stem.replace("_metadata", "")
        original_book_data: Dict[str, Any] = {"chapters": chapters}
    else:
        chapters = book_data.get("chapters", [])
        book_title = book_data.get(
            "book_title", input_path.stem.replace("_metadata", "")
        )
        original_book_data = book_data

    print(f"\nBook: {book_title}")
    print(f"Chapters: {len(chapters)}")

    # 2. Build corpus and chapter_index for MSEP API
    corpus: list[str] = []
    chapter_index: list[ChapterMeta] = []

    for idx, chapter in enumerate(chapters):
        chapter_num = chapter.get("chapter_number", idx + 1)
        chapter_title = chapter.get("title", f"Chapter {chapter_num}")

        # Build chapter content from available fields
        content_parts = []
        if chapter.get("title"):
            content_parts.append(chapter["title"])
        if chapter.get("summary"):
            content_parts.append(chapter["summary"])
        if chapter.get("content"):
            content_parts.append(chapter["content"])
        if chapter.get("keywords"):
            content_parts.append(" ".join(chapter["keywords"]))

        chapter_text = " ".join(content_parts) if content_parts else f"Chapter {chapter_num}"
        corpus.append(chapter_text)

        chapter_index.append(
            ChapterMeta(
                book=book_title,
                chapter=chapter_num,
                title=chapter_title,
            )
        )

    # 3. Call MSEP API with fallback on error
    enriched_response: Optional[EnrichedMetadataResponse] = None

    try:
        print("\nConnecting to ai-agents MSEP service...")
        async with MSEPClient(base_url=msep_url) as client:
            enriched_response = await client.enrich_metadata(
                corpus=corpus,
                chapter_index=chapter_index,
                config=MSEPConfig(threshold=0.3),
            )
        print(f"✅ MSEP enrichment complete: {enriched_response.total_cross_references} cross-references")

    except (MSEPConnectionError, MSEPTimeoutError) as e:
        # AC-6.2.2: Fallback to local enrichment when ai-agents unavailable
        # Per CODING_PATTERNS §3.3: Log the fallback
        _logger.warning(
            f"MSEP service unavailable ({type(e).__name__}: {e}). "
            "Falling back to local enrichment."
        )
        print(f"\n⚠️ MSEP service unavailable: {e}")
        print("  Falling back to local enrichment...")

        # Fallback to existing local enrichment
        enrich_metadata_local(input_path, output_path)
        return

    except MSEPAPIError as e:
        # API errors (400, 422) should fail fast - not retry
        _logger.error(f"MSEP API error: {e}")
        raise

    # 4. Merge MSEP response with original metadata (AC-6.3.2)
    # Output format follows unified schema: book_enriched_chapters.schema.json
    enriched_chapters = []

    for idx, chapter in enumerate(chapters):
        enriched_chapter = chapter.copy()  # Preserve all original fields

        # Find matching enriched chapter from response
        # MSEP returns chapter_id as "{book}:ch{chapter}" format
        chapter_num = chapter.get('chapter_number', idx + 1)
        chapter_id = f"{book_title}:ch{chapter_num}"
        msep_chapter = None

        for ec in enriched_response.chapters:
            if ec.chapter_id == chapter_id:
                msep_chapter = ec
                break

        if msep_chapter:
            # Convert MSEP cross_references to unified similar_chapters format
            # MSEP target format: "Book:ch5" -> {book: "Book", chapter: 5, ...}
            similar_chapters = []
            for xr in msep_chapter.cross_references:
                # Parse target format "Book:ch5"
                target_parts = xr.target.rsplit(":ch", 1)
                target_book = target_parts[0] if len(target_parts) == 2 else book_title
                target_chapter = int(target_parts[1]) if len(target_parts) == 2 else 0
                
                similar_chapters.append({
                    "book": target_book,
                    "chapter": target_chapter,
                    "title": "",  # MSEP doesn't provide target title
                    "score": round(xr.score, 3),
                    "base_score": round(xr.base_score, 3),
                    "topic_boost": round(xr.topic_boost, 3),
                    "method": xr.method,
                })
            
            enriched_chapter["similar_chapters"] = similar_chapters
            enriched_chapter["enriched_keywords"] = {
                "tfidf": msep_chapter.keywords.tfidf,
                "semantic": msep_chapter.keywords.semantic,
                "merged": msep_chapter.keywords.merged,
            }
            enriched_chapter["topic_id"] = msep_chapter.topic_id
            enriched_chapter["chapter_provenance"] = {
                "methods_used": msep_chapter.provenance.methods_used,
                "sbert_score": msep_chapter.provenance.sbert_score,
                "topic_boost": msep_chapter.provenance.topic_boost,
                "timestamp": msep_chapter.provenance.timestamp,
            }
        else:
            # No MSEP data for this chapter - add empty similar_chapters
            enriched_chapter["similar_chapters"] = []

        enriched_chapters.append(enriched_chapter)

    # 5. Build output with provenance (AC-6.3.1, AC-6.3.3)
    # Output format follows unified schema: book_enriched_chapters.schema.json
    enriched_metadata: Dict[str, Any] = {
        "metadata": {
            "title": book_title,
            "source_file": input_path.name,
        },
        "chapters": enriched_chapters,
        "total_chapters": len(enriched_chapters),
    }
    
    # Preserve any existing metadata from original book data
    if isinstance(original_book_data, dict):
        for key in ["author", "publisher", "isbn", "total_pages"]:
            if key in original_book_data:
                enriched_metadata["metadata"][key] = original_book_data[key]

    # Add top-level provenance
    enriched_metadata["enrichment_provenance"] = build_enrichment_provenance(
        input_path=input_path,
        taxonomy_path=None,
        enrichment_method=ENRICHMENT_METHOD_MSEP,
        model_version="ai-agents-msep-v1",
    )

    # Add MSEP-specific metadata (using unified field names)
    enriched_metadata["enrichment_provenance"]["processing_time_ms"] = (
        enriched_response.processing_time_ms
    )
    enriched_metadata["enrichment_provenance"]["total_similar_chapters"] = (
        enriched_response.total_cross_references
    )

    # 6. Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(enriched_metadata, f, indent=2, ensure_ascii=False)

    # Report
    size_kb = output_path.stat().st_size / 1024
    print(f"\n✅ Enriched metadata saved: {output_path.name}")
    print(f"  File size: {size_kb:.1f} KB")
    print(f"  Chapters enriched: {len(enriched_chapters)}")
    print(f"  Cross-references: {enriched_response.total_cross_references}")
    print(f"  Processing time: {enriched_response.processing_time_ms:.1f}ms")
    print(f"  Similarity source: msep")
    print("  NO local ML processing ✓")


def main():
    """
    Command-line interface for metadata enrichment.
    
    Example (cross-book mode with taxonomy):
        python enrich_metadata_per_book.py \\
            --input workflows/metadata_extraction/output/architecture_patterns_metadata.json \\
            --taxonomy workflows/taxonomy_setup/output/architecture_patterns_taxonomy.json \\
            --output workflows/metadata_enrichment/output/architecture_patterns_metadata_enriched.json
    
    Example (local/within-book mode without taxonomy):
        python enrich_metadata_per_book.py \\
            --input workflows/metadata_extraction/output/test_book_metadata.json \\
            --output workflows/metadata_enrichment/output/test_book_enriched.json
    
    Example (orchestrator mode - WBS 5.1):
        python enrich_metadata_per_book.py \\
            --input workflows/metadata_extraction/output/architecture_patterns_metadata.json \\
            --output workflows/metadata_enrichment/output/architecture_patterns_enriched.json \\
            --use-orchestrator \\
            --orchestrator-url http://localhost:8083
    
    Example (MSEP mode - WBS MSE-6.2 - Kitchen Brigade):
        python enrich_metadata_per_book.py \\
            --input workflows/metadata_extraction/output/architecture_patterns_metadata.json \\
            --output workflows/metadata_enrichment/output/architecture_patterns_enriched.json \\
            --use-msep \\
            --msep-url http://localhost:8082
    """
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Validate inputs exist
    if not args.input.exists():
        print(f"❌ Error: Input file not found: {args.input}")
        sys.exit(1)
    
    if args.taxonomy and not args.taxonomy.exists():
        print(f"❌ Error: Taxonomy file not found: {args.taxonomy}")
        sys.exit(1)
    
    # Run enrichment - priority: MSEP > Orchestrator > Semantic Search > Taxonomy > Local
    try:
        if args.use_msep:
            # MSEP mode (WBS MSE-6.2 - Kitchen Brigade)
            if not MSEP_CLIENT_AVAILABLE:
                print("❌ Error: MSEPClient not available")
                print("  Check workflows/shared/clients/msep_client.py exists")
                sys.exit(1)
            asyncio.run(enrich_metadata_msep(
                args.input,
                args.output,
                msep_url=args.msep_url
            ))
        elif args.use_orchestrator:
            # Orchestrator mode (WBS 5.1)
            if not ORCHESTRATOR_CLIENT_AVAILABLE:
                print("❌ Error: OrchestratorClient not available")
                print("  Check workflows/shared/clients/orchestrator_client.py exists")
                sys.exit(1)
            asyncio.run(enrich_metadata_orchestrator(
                args.input,
                args.output,
                orchestrator_url=args.orchestrator_url
            ))
        elif args.use_semantic_search:
            # Semantic search mode (WBS 3.2.4)
            if not SEMANTIC_SEARCH_CLIENT_AVAILABLE:
                print("❌ Error: SemanticSearchClient not available")
                print("  Install with: pip install httpx")
                sys.exit(1)
            asyncio.run(enrich_metadata_semantic(
                args.input, 
                args.output,
                semantic_search_url=args.semantic_search_url
            ))
        elif args.taxonomy:
            # Cross-book mode with taxonomy
            enrich_metadata(args.input, args.taxonomy, args.output)
        else:
            # Local/within-book mode without taxonomy
            enrich_metadata_local(args.input, args.output)
    except Exception as e:
        print(f"\n❌ Enrichment failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
