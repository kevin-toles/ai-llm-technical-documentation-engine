#!/usr/bin/env python3
"""
WBS 3.5.3.7: Compute Cross-Book Similar Chapters (SBERT-enhanced)

Adds `similar_chapters` array to each chapter in enriched book files.
Uses SemanticSimilarityEngine (SBERT) for semantic similarity.
Falls back to TF-IDF when sentence-transformers unavailable.

Architecture Reference: AI_CODING_PLATFORM_WBS.md v1.4.0
- similar_chapters computed against FULL corpus (not taxonomy-limited)
- Filtering by taxonomy happens at query-time
- SBERT provides semantic understanding vs TF-IDF lexical matching

Model Selection (per AI_CODING_PLATFORM_ARCHITECTURE.md):
- SBERT (all-MiniLM-L6-v2): General text/chapter similarity (this module)
- Code-Orchestrator (CodeBERT/GraphCodeBERT): Code-specific understanding

Anti-Pattern Audit:
- CODING_PATTERNS #10.3: Atomic file writes (temp → rename)
- CODING_PATTERNS S1192: No duplicated literals (module constants)
- CODING_PATTERNS S3776: Cognitive complexity < 15

Usage:
    python compute_similar_chapters.py
    
    # Custom paths
    python compute_similar_chapters.py --input-dir /path/to/enriched --output-dir /path/to/output
    
    # Adjust similarity threshold
    python compute_similar_chapters.py --threshold 0.3 --top-n 10
    
    # Use SBERT explicitly (default when available)
    python compute_similar_chapters.py --use-sbert --model-name all-mpnet-base-v2
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Optional

# Project configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import SemanticSimilarityEngine for SBERT-based similarity
from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
    SemanticSimilarityEngine,
    SimilarityConfig,
    SENTENCE_TRANSFORMERS_AVAILABLE,
)

# =============================================================================
# Module Constants (CODING_PATTERNS S1192: No duplicated literals)
# =============================================================================
_SIMILAR_CHAPTERS_KEY = "similar_chapters"
_CHAPTERS_KEY = "chapters"
_DEFAULT_THRESHOLD = 0.3  # Lower threshold for cross-book similarity
_DEFAULT_TOP_N = 5
_DEFAULT_MODEL_NAME = "all-MiniLM-L6-v2"
_METHOD_SBERT = "sentence_transformers"
_METHOD_TFIDF = "tfidf"


def create_similarity_engine(
    model_name: str = _DEFAULT_MODEL_NAME,
    fallback_to_tfidf: bool = True,
) -> SemanticSimilarityEngine:
    """
    Factory function to create a SemanticSimilarityEngine.
    
    Args:
        model_name: SBERT model name (default: all-MiniLM-L6-v2)
        fallback_to_tfidf: Whether to fallback to TF-IDF if SBERT unavailable
        
    Returns:
        Configured SemanticSimilarityEngine instance
    """
    config = SimilarityConfig(
        model_name=model_name,
        fallback_to_tfidf=fallback_to_tfidf,
        similarity_threshold=0.0,  # We apply threshold in find_similar_chapters
        top_k=_DEFAULT_TOP_N,
    )
    return SemanticSimilarityEngine(model_name=model_name, config=config)


def discover_enriched_books(enriched_dir: Path) -> list[Path]:
    """
    Discover all enriched book JSON files.
    
    Args:
        enriched_dir: Path to books/enriched/ directory
        
    Returns:
        List of paths to enriched JSON files
    """
    if not enriched_dir.exists():
        return []
    
    return sorted(enriched_dir.glob("*.json"))


def load_enriched_book(book_path: Path) -> dict[str, Any]:
    """
    Load an enriched book JSON file.
    
    Args:
        book_path: Path to enriched book JSON
        
    Returns:
        Book data dictionary
    """
    with open(book_path, encoding="utf-8") as f:
        return json.load(f)


def build_corpus_from_books(
    book_paths: list[Path],
) -> tuple[list[str], list[dict[str, Any]], dict[str, dict[str, Any]]]:
    """
    Build TF-IDF corpus from all enriched books.
    
    Extracts text features from each chapter: title, summary, keywords, concepts.
    
    Args:
        book_paths: List of paths to enriched book JSONs
        
    Returns:
        Tuple of:
        - corpus: List of chapter text strings
        - index: List of chapter metadata (book, chapter, title)
        - books_data: Dict mapping book name to full book data
    """
    corpus: list[str] = []
    index: list[dict[str, Any]] = []
    books_data: dict[str, dict[str, Any]] = {}
    
    for book_path in book_paths:
        book_name = book_path.stem
        book_data = load_enriched_book(book_path)
        books_data[book_name] = book_data
        
        chapters = book_data.get(_CHAPTERS_KEY, [])
        for chapter in chapters:
            # Combine text features for TF-IDF
            text_parts = _extract_chapter_text_parts(chapter)
            chapter_text = " ".join(text_parts)
            
            corpus.append(chapter_text)
            index.append({
                "book": book_name,
                "chapter": chapter.get("chapter_number", chapter.get("number", 0)),
                "title": chapter.get("title", ""),
            })
    
    return corpus, index, books_data


def _extract_chapter_text_parts(chapter: dict[str, Any]) -> list[str]:
    """
    Extract text features from a chapter for TF-IDF.
    
    Helper function to reduce cognitive complexity of build_corpus_from_books.
    
    Args:
        chapter: Chapter dictionary
        
    Returns:
        List of text strings to combine
    """
    return [
        chapter.get("title", ""),
        chapter.get("summary", ""),
        " ".join(chapter.get("keywords", [])),
        " ".join(chapter.get("concepts", [])),
    ]


def compute_similarity_matrix(
    corpus: list[str],
    engine: Optional[SemanticSimilarityEngine] = None,
) -> Any:
    """
    Compute embeddings and cosine similarity matrix using SemanticSimilarityEngine.
    
    Args:
        corpus: List of chapter text strings
        engine: SemanticSimilarityEngine instance (creates default if None)
        
    Returns:
        Tuple of (cosine similarity matrix, method used)
    """
    if engine is None:
        engine = create_similarity_engine()
    
    # Compute embeddings using engine (SBERT or TF-IDF fallback)
    embeddings = engine.compute_embeddings(corpus)
    
    # Compute similarity matrix
    return engine.compute_similarity_matrix(embeddings)


def find_similar_chapters(
    chapter_idx: int,
    similarity_matrix: Any,
    index: list[dict[str, Any]],
    current_book: str,
    threshold: float = _DEFAULT_THRESHOLD,
    top_n: int = _DEFAULT_TOP_N,
    method: str = _METHOD_SBERT,
) -> list[dict[str, Any]]:
    """
    Find top N similar chapters from OTHER books.
    
    Args:
        chapter_idx: Index of current chapter in corpus
        similarity_matrix: Precomputed cosine similarity matrix
        index: Chapter metadata index
        current_book: Book name to exclude (no self-references)
        threshold: Minimum similarity score
        top_n: Maximum number of results
        method: Similarity method used ('sentence_transformers' or 'tfidf')
        
    Returns:
        List of similar chapter dicts with book, chapter, title, relevance_score, method
    """
    scores = similarity_matrix[chapter_idx]
    
    # Collect chapters above threshold from OTHER books
    scored_chapters = _collect_cross_book_candidates(
        scores, chapter_idx, index, current_book, threshold, method
    )
    
    # Sort by score descending and take top N
    scored_chapters.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    return scored_chapters[:top_n]


def _collect_cross_book_candidates(
    scores: Any,
    chapter_idx: int,
    index: list[dict[str, Any]],
    current_book: str,
    threshold: float,
    method: str = _METHOD_SBERT,
) -> list[dict[str, Any]]:
    """
    Collect candidate chapters from other books above threshold.
    
    Helper function to reduce cognitive complexity.
    
    Args:
        scores: Similarity scores for this chapter
        chapter_idx: Index of current chapter
        index: Chapter metadata index
        current_book: Book to exclude
        threshold: Minimum score
        method: Similarity method used
        
    Returns:
        List of candidate chapter dicts
    """
    candidates: list[dict[str, Any]] = []
    
    for idx, score in enumerate(scores):
        # Skip self and below threshold
        if idx == chapter_idx or score < threshold:
            continue
        
        chapter_info = index[idx]
        
        # Cross-book only
        if chapter_info["book"] == current_book:
            continue
        
        candidates.append({
            "book": chapter_info["book"],
            "chapter": chapter_info["chapter"],
            "title": chapter_info["title"],
            "relevance_score": round(float(score), 2),
            "method": method,
        })
    
    return candidates


def add_similar_chapters_to_book(
    book_data: dict[str, Any],
    book_name: str,
    index: list[dict[str, Any]],
    similarity_matrix: Any,
    threshold: float = _DEFAULT_THRESHOLD,
    top_n: int = _DEFAULT_TOP_N,
    method: str = _METHOD_SBERT,
) -> dict[str, Any]:
    """
    Add similar_chapters to each chapter in a book.
    
    Args:
        book_data: Book data dictionary (modified in place)
        book_name: Name of this book
        index: Full corpus chapter index
        similarity_matrix: Precomputed similarity matrix
        threshold: Minimum similarity score
        top_n: Maximum similar chapters per chapter
        method: Similarity method used
        
    Returns:
        Modified book data with similar_chapters added
    """
    # Build lookup for this book's chapters in the index
    book_chapter_indices = _build_chapter_index_lookup(index, book_name)
    
    chapters = book_data.get(_CHAPTERS_KEY, [])
    for chapter in chapters:
        chapter_num = chapter.get("chapter_number", chapter.get("number", 0))
        
        # Find this chapter's index in the corpus
        idx = book_chapter_indices.get(chapter_num)
        if idx is None:
            # Chapter not in index (shouldn't happen)
            chapter[_SIMILAR_CHAPTERS_KEY] = []
            continue
        
        # Find similar chapters
        similar = find_similar_chapters(
            idx, similarity_matrix, index, book_name, threshold, top_n, method
        )
        chapter[_SIMILAR_CHAPTERS_KEY] = similar
    
    return book_data


def _build_chapter_index_lookup(
    index: list[dict[str, Any]], book_name: str
) -> dict[int, int]:
    """
    Build a lookup from chapter number to corpus index.
    
    Helper function to reduce cognitive complexity.
    
    Args:
        index: Full corpus chapter index
        book_name: Book name to filter by
        
    Returns:
        Dict mapping chapter_number -> corpus_index
    """
    lookup: dict[int, int] = {}
    for corpus_idx, entry in enumerate(index):
        if entry["book"] == book_name:
            lookup[entry["chapter"]] = corpus_idx
    return lookup


def write_book_atomic(book_data: dict[str, Any], output_path: Path) -> None:
    """
    Write book data atomically (temp file → rename).
    
    Per CODING_PATTERNS #10.3: Atomic file writes prevent corruption.
    
    Args:
        book_data: Book data to write
        output_path: Final output path
    """
    temp_path = output_path.with_suffix(".json.tmp")
    
    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(book_data, f, indent=2, ensure_ascii=False)
        
        # Atomic rename
        os.replace(temp_path, output_path)
    finally:
        # Clean up temp file on failure
        if temp_path.exists():
            temp_path.unlink()


def main(
    input_dir: Optional[Path] = None,
    output_dir: Optional[Path] = None,
    threshold: float = _DEFAULT_THRESHOLD,
    top_n: int = _DEFAULT_TOP_N,
    model_name: str = _DEFAULT_MODEL_NAME,
) -> int:
    """
    Main entry point for computing similar chapters.
    
    Args:
        input_dir: Directory containing enriched book JSONs
        output_dir: Directory to write updated JSONs (default: same as input)
        threshold: Minimum similarity score
        top_n: Maximum similar chapters per chapter
        model_name: SBERT model name
        
    Returns:
        Exit code (0 for success)
    """
    # Default paths
    if input_dir is None:
        input_dir = PROJECT_ROOT / "books" / "enriched"
    if output_dir is None:
        output_dir = input_dir
    
    print(f"📚 Computing similar chapters for books in {input_dir}")
    print(f"   Threshold: {threshold}, Top-N: {top_n}")
    
    # Create similarity engine
    engine = create_similarity_engine(model_name=model_name, fallback_to_tfidf=True)
    
    # Determine which method is being used
    if engine.is_using_fallback:
        method = _METHOD_TFIDF
        print("   Method: TF-IDF (sentence-transformers not available)")
    else:
        method = _METHOD_SBERT
        print(f"   Method: SBERT ({model_name})")
    
    # Discover enriched books
    book_paths = discover_enriched_books(input_dir)
    if not book_paths:
        print(f"❌ No enriched books found in {input_dir}")
        return 1
    
    print(f"   Found {len(book_paths)} books")
    
    # Build corpus from all books
    print("📊 Building corpus...")
    corpus, index, books_data = build_corpus_from_books(book_paths)
    print(f"   Corpus: {len(corpus)} chapters from {len(books_data)} books")
    
    # Compute similarity matrix using engine
    print(f"🔢 Computing similarity matrix using {method}...")
    similarity_matrix = compute_similarity_matrix(corpus, engine=engine)
    print(f"   Matrix shape: {similarity_matrix.shape}")
    
    # Add similar_chapters to each book
    print("🔗 Adding similar_chapters to each book...")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for book_name, book_data in books_data.items():
        add_similar_chapters_to_book(
            book_data, book_name, index, similarity_matrix, threshold, top_n, method
        )
        
        output_path = output_dir / f"{book_name}.json"
        write_book_atomic(book_data, output_path)
        
        # Count similar chapters added
        total_similar = sum(
            len(ch.get(_SIMILAR_CHAPTERS_KEY, []))
            for ch in book_data.get(_CHAPTERS_KEY, [])
        )
        print(f"   ✅ {book_name}: {total_similar} similar chapter links")
    
    print(f"\n✅ SUCCESS! Updated {len(books_data)} books with similar_chapters")
    print(f"   Similarity method: {method}")
    return 0


def create_argument_parser() -> argparse.ArgumentParser:
    """Create CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Compute cross-book similar chapters using SBERT semantic similarity"
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=None,
        help="Directory containing enriched book JSONs (default: books/enriched/)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory to write updated JSONs (default: same as input)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=_DEFAULT_THRESHOLD,
        help=f"Minimum similarity score (default: {_DEFAULT_THRESHOLD})",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=_DEFAULT_TOP_N,
        help=f"Maximum similar chapters per chapter (default: {_DEFAULT_TOP_N})",
    )
    parser.add_argument(
        "--use-sbert",
        action="store_true",
        default=True,
        help="Use SBERT for semantic similarity (default: True if available)",
    )
    parser.add_argument(
        "--model-name",
        type=str,
        default=_DEFAULT_MODEL_NAME,
        help=f"SBERT model name (default: {_DEFAULT_MODEL_NAME})",
    )
    return parser


if __name__ == "__main__":
    parser = create_argument_parser()
    args = parser.parse_args()
    
    exit_code = main(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        threshold=args.threshold,
        top_n=args.top_n,
        model_name=args.model_name,
    )
    sys.exit(exit_code)
