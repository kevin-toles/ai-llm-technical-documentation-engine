#!/usr/bin/env python3
"""
WBS M5: Compute Similar Chapters via SBERT API.

This script re-computes similar_chapters for all books using the
Code-Orchestrator SBERT API (async mode).

Purpose: Validate SBERT migration by re-enriching all 47 books via API.

Usage:
    # Ensure Code-Orchestrator is running on port 8083
    SBERT_API_URL=http://localhost:8083 python -m workflows.metadata_enrichment.scripts.compute_similar_chapters_api

References:
    - SBERT_EXTRACTION_MIGRATION_WBS.md: M5 Documentation & Rollout
    - compute_similar_chapters.py: Original synchronous implementation
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import numpy as np

# Project root
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
    SemanticSimilarityEngine,
    SimilarityConfig,
)
from workflows.shared.clients.sbert_client import SBERTClient

# =============================================================================
# Constants
# =============================================================================

_DEFAULT_THRESHOLD = 0.3
_DEFAULT_TOP_N = 5
_SIMILAR_CHAPTERS_KEY = "similar_chapters"
_CHAPTERS_KEY = "chapters"
_DEFAULT_SBERT_API_URL = "http://localhost:8083"


@dataclass
class EnrichmentStats:
    """Statistics from enrichment run."""
    
    total_books: int = 0
    total_chapters: int = 0
    total_links: int = 0
    elapsed_seconds: float = 0.0
    method: str = "api"


def discover_enriched_books(enriched_dir: Path) -> list[Path]:
    """Discover all enriched book JSON files."""
    if not enriched_dir.exists():
        return []
    return sorted(enriched_dir.glob("*.json"))


def load_book(book_path: Path) -> dict[str, Any]:
    """Load a book JSON file."""
    with open(book_path, encoding="utf-8") as f:
        return json.load(f)


def save_book(book_path: Path, book_data: dict[str, Any]) -> None:
    """Save a book JSON file with atomic write."""
    temp_path = book_path.with_suffix(".tmp")
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(book_data, f, indent=2, ensure_ascii=False)
    temp_path.rename(book_path)


def build_corpus(book_paths: list[Path]) -> tuple[list[str], list[dict[str, Any]], dict[str, dict[str, Any]]]:
    """
    Build corpus from all enriched books.
    
    Returns:
        - corpus: List of chapter text strings
        - index: List of chapter metadata
        - books_data: Dict of book name -> book data
    """
    corpus: list[str] = []
    index: list[dict[str, Any]] = []
    books_data: dict[str, dict[str, Any]] = {}
    
    for book_path in book_paths:
        book_name = book_path.stem
        book_data = load_book(book_path)
        books_data[book_name] = book_data
        
        chapters = book_data.get(_CHAPTERS_KEY, [])
        for chapter in chapters:
            # Combine text features
            text_parts = [
                chapter.get("title", ""),
                chapter.get("summary", ""),
                " ".join(chapter.get("keywords", [])),
                " ".join(chapter.get("concepts", [])),
            ]
            chapter_text = " ".join(text_parts)
            
            corpus.append(chapter_text)
            index.append({
                "book": book_name,
                "chapter": chapter.get("chapter_number", chapter.get("number", 0)),
                "title": chapter.get("title", ""),
            })
    
    return corpus, index, books_data


def find_similar_chapters(
    chapter_idx: int,
    similarity_matrix: np.ndarray,
    index: list[dict[str, Any]],
    current_book: str,
    threshold: float,
    top_n: int,
    method: str,
) -> list[dict[str, Any]]:
    """Find top N similar chapters from OTHER books."""
    scores = similarity_matrix[chapter_idx]
    
    candidates: list[dict[str, Any]] = []
    for idx, score in enumerate(scores):
        if idx == chapter_idx or score < threshold:
            continue
        
        chapter_info = index[idx]
        if chapter_info["book"] == current_book:
            continue
        
        candidates.append({
            "book": chapter_info["book"],
            "chapter": chapter_info["chapter"],
            "title": chapter_info["title"],
            "relevance_score": round(float(score), 2),
            "method": method,
        })
    
    candidates.sort(key=lambda x: x["relevance_score"], reverse=True)
    return candidates[:top_n]


async def compute_embeddings_via_api(
    corpus: list[str],
    api_url: str,
) -> tuple[np.ndarray, str]:
    """
    Compute embeddings using Code-Orchestrator SBERT API.
    
    Returns:
        - embeddings: numpy array of shape (n_chapters, 384)
        - method: "api" or fallback method used
    """
    config = SimilarityConfig(
        fallback_mode="api",
        use_api=True,
        sbert_api_url=api_url,
        fallback_to_local=True,
        fallback_to_tfidf=True,
    )
    
    async with SBERTClient(base_url=api_url) as client:
        engine = SemanticSimilarityEngine(config=config, sbert_client=client)
        embeddings = await engine.compute_embeddings_async(corpus)
        method = engine._last_method or "api"
    
    return embeddings, method


def compute_similarity_matrix(embeddings: np.ndarray) -> np.ndarray:
    """Compute cosine similarity matrix."""
    from sklearn.metrics.pairwise import cosine_similarity
    return cosine_similarity(embeddings)


async def run_enrichment(
    input_dir: Path,
    output_dir: Optional[Path] = None,
    threshold: float = _DEFAULT_THRESHOLD,
    top_n: int = _DEFAULT_TOP_N,
    api_url: str = _DEFAULT_SBERT_API_URL,
) -> EnrichmentStats:
    """
    Run full enrichment on all books via SBERT API.
    
    Args:
        input_dir: Directory with enriched book JSONs
        output_dir: Output directory (defaults to input_dir)
        threshold: Minimum similarity score
        top_n: Max similar chapters per chapter
        api_url: Code-Orchestrator SBERT API URL
    
    Returns:
        EnrichmentStats with run statistics
    """
    stats = EnrichmentStats()
    start_time = time.perf_counter()
    
    if output_dir is None:
        output_dir = input_dir
    
    # Discover books
    book_paths = discover_enriched_books(input_dir)
    stats.total_books = len(book_paths)
    
    if not book_paths:
        print(f"❌ No books found in {input_dir}")
        return stats
    
    print(f"📚 Computing similar chapters for {stats.total_books} books")
    print(f"   API URL: {api_url}")
    print(f"   Threshold: {threshold}, Top-N: {top_n}")
    
    # Build corpus
    print("📊 Building corpus...")
    corpus, index, books_data = build_corpus(book_paths)
    stats.total_chapters = len(corpus)
    print(f"   Corpus: {stats.total_chapters} chapters from {stats.total_books} books")
    
    # Compute embeddings via API
    print("🔢 Computing embeddings via SBERT API...")
    embeddings, method = await compute_embeddings_via_api(corpus, api_url)
    stats.method = method
    print(f"   Method: {method}")
    print(f"   Embeddings shape: {embeddings.shape}")
    
    # Compute similarity matrix
    print("🔗 Computing similarity matrix...")
    similarity_matrix = compute_similarity_matrix(embeddings)
    print(f"   Matrix shape: {similarity_matrix.shape}")
    
    # Add similar_chapters to each book
    print("📝 Adding similar_chapters to each book...")
    corpus_idx = 0
    
    for book_path in book_paths:
        book_name = book_path.stem
        book_data = books_data[book_name]
        chapters = book_data.get(_CHAPTERS_KEY, [])
        
        book_links = 0
        for chapter in chapters:
            similar = find_similar_chapters(
                chapter_idx=corpus_idx,
                similarity_matrix=similarity_matrix,
                index=index,
                current_book=book_name,
                threshold=threshold,
                top_n=top_n,
                method=method,
            )
            chapter[_SIMILAR_CHAPTERS_KEY] = similar
            book_links += len(similar)
            corpus_idx += 1
        
        # Save updated book
        output_path = output_dir / f"{book_name}.json"
        save_book(output_path, book_data)
        
        stats.total_links += book_links
        print(f"   ✅ {book_name}: {book_links} similar chapter links")
    
    stats.elapsed_seconds = time.perf_counter() - start_time
    
    print()
    print(f"✅ SUCCESS! Enriched {stats.total_books} books with similar_chapters")
    print(f"   Total links: {stats.total_links}")
    print(f"   Method: {stats.method}")
    print(f"   Elapsed: {stats.elapsed_seconds:.1f}s")
    
    return stats


async def main() -> int:
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Compute similar chapters via SBERT API"
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=PROJECT_ROOT / "books" / "enriched",
        help="Input directory with enriched books",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory (defaults to input-dir)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=_DEFAULT_THRESHOLD,
        help=f"Similarity threshold (default: {_DEFAULT_THRESHOLD})",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=_DEFAULT_TOP_N,
        help=f"Max similar chapters per chapter (default: {_DEFAULT_TOP_N})",
    )
    parser.add_argument(
        "--api-url",
        type=str,
        default=os.getenv("SBERT_API_URL", _DEFAULT_SBERT_API_URL),
        help="Code-Orchestrator SBERT API URL",
    )
    
    args = parser.parse_args()
    
    try:
        stats = await run_enrichment(
            input_dir=args.input_dir,
            output_dir=args.output_dir,
            threshold=args.threshold,
            top_n=args.top_n,
            api_url=args.api_url,
        )
        return 0 if stats.total_books > 0 else 1
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
