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
    
Test-Driven Development:
    - Tests: tests/integration/test_metadata_enrichment.py
    - This is the GREEN phase - implementing minimal code to pass RED tests
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple
from datetime import datetime

# scikit-learn imports for TF-IDF and cosine similarity
from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore[import-untyped]
from sklearn.metrics.pairwise import cosine_similarity  # type: ignore[import-untyped]

# Project configuration and paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Statistical extractor for YAKE + Summa (existing implementation)
try:
    from workflows.metadata_extraction.scripts.adapters.statistical_extractor import StatisticalExtractor
    STATISTICAL_EXTRACTOR = StatisticalExtractor()
except ImportError as e:
    print(f"Warning: StatisticalExtractor not available: {e}")
    print("Will use fallback keyword extraction")
    STATISTICAL_EXTRACTOR = None  # type: ignore[assignment]


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


def load_cross_book_context(taxonomy_path: Path, metadata_dir: Path) -> Dict[str, Any]:
    """
    Load metadata for all books listed in taxonomy.
    
    Reference: TAB4_IMPLEMENTATION_PLAN.md - Function 1
    Pattern: Repository pattern for data access (Architecture Patterns Ch. 2)
    
    Args:
        taxonomy_path: Path to {book}_taxonomy.json from Tab 3
        metadata_dir: Directory containing *_metadata.json files from Tab 2
        
    Returns:
        Dictionary containing:
        - books: List of book names
        - metadata: Dict mapping book_name -> chapter list
        - corpus_size: Total number of chapters across all books
        
    Raises:
        FileNotFoundError: If taxonomy file doesn't exist
        json.JSONDecodeError: If taxonomy JSON is invalid
    """
    if not taxonomy_path.exists():
        raise FileNotFoundError(f"Taxonomy file not found: {taxonomy_path}")
    
    with open(taxonomy_path, encoding='utf-8') as f:
        taxonomy = json.load(f)
    
    # Extract book list from taxonomy tiers
    book_set = _extract_books_from_taxonomy(taxonomy)
    
    # If no books found in taxonomy, scan metadata directory
    if not book_set:
        print("[INFO] Taxonomy doesn't contain book list. Scanning metadata directory for all available books...")
        book_set = _scan_metadata_directory(metadata_dir)
    
    # Load metadata for each book
    return _load_book_metadata(book_set, metadata_dir)


def build_chapter_corpus(context: Dict[str, Any]) -> Tuple[List[str], List[Dict[str, Any]]]:
    """
    Build corpus of chapter texts and index for TF-IDF.
    
    Reference: TAB4_IMPLEMENTATION_PLAN.md - Function 2
    Pattern: Factory pattern for corpus construction
    
    Args:
        context: Cross-book context from load_cross_book_context()
        
    Returns:
        Tuple of:
        - corpus: List of chapter text strings (one per chapter)
        - index: List of chapter metadata dicts with keys:
            - book: Book filename
            - chapter: Chapter number
            - title: Chapter title
            - start_page: Start page number
            - end_page: End page number
    """
    corpus = []
    index = []
    
    for book_name, chapters in context["metadata"].items():
        for chapter in chapters:
            # Combine all text features for TF-IDF analysis
            # Using title, summary, keywords, and concepts provides rich semantic content
            text_parts = [
                chapter.get("title", ""),
                chapter.get("summary", ""),
                " ".join(chapter.get("keywords", [])),
                " ".join(chapter.get("concepts", []))
            ]
            chapter_text = " ".join(text_parts)
            
            corpus.append(chapter_text)
            index.append({
                "book": book_name,
                "chapter": chapter.get("chapter_number"),
                "title": chapter.get("title", ""),
                "start_page": chapter.get("start_page"),
                "end_page": chapter.get("end_page")
            })
    
    return corpus, index


def compute_similarity_matrix(corpus: List[str]) -> Any:
    """
    Compute TF-IDF matrix and cosine similarity between all chapters.
    
    Reference: TAB4_IMPLEMENTATION_PLAN.md - Function 3
    Pattern: Statistical methods (no LLM) - scikit-learn
    
    Args:
        corpus: List of chapter text strings
        
    Returns:
        similarity_matrix: numpy array of shape (n_chapters, n_chapters)
                          where similarity_matrix[i][j] is cosine similarity between chapter i and j
                          
    Configuration:
        - stop_words: Remove common English words ("the", "a", etc.)
        - max_features: Limit to 1000 most important terms
        - ngram_range: Include unigrams, bigrams, and trigrams
        - min_df: Ignore terms appearing in fewer than 2 documents
        - max_df: Ignore terms appearing in more than 80% of documents
    """
    # TF-IDF vectorization configuration per plan
    vectorizer = TfidfVectorizer(
        stop_words='english',
        max_features=1000,
        ngram_range=(1, 3),  # Unigrams, bigrams, trigrams
        min_df=2,  # Minimum document frequency
        max_df=0.8  # Maximum document frequency (80%)
    )
    
    # Transform corpus to TF-IDF matrix
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    # Compute pairwise cosine similarity
    similarity_matrix = cosine_similarity(tfidf_matrix)
    
    return similarity_matrix


def find_related_chapters(
    chapter_idx: int,
    similarity_matrix: Any,
    index: List[Dict[str, Any]],
    current_book: str,
    threshold: float = 0.7,
    top_n: int = 5
) -> List[Dict[str, Any]]:
    """
    Find top N related chapters for a given chapter using cosine similarity.
    
    Reference: TAB4_IMPLEMENTATION_PLAN.md - Function 4
    Pattern: Filter pattern with threshold and ranking
    
    Args:
        chapter_idx: Index of current chapter in corpus/similarity matrix
        similarity_matrix: Precomputed cosine similarity matrix
        index: Chapter metadata index
        current_book: Book name to exclude self-references
        threshold: Minimum similarity score (0.7 = 70% similarity)
        top_n: Maximum number of related chapters to return (5)
        
    Returns:
        List of related chapter dicts with keys:
        - book: Book filename
        - chapter: Chapter number
        - title: Chapter title
        - relevance_score: Similarity score (0.0-1.0)
        - method: Always "cosine_similarity"
    """
    scores = similarity_matrix[chapter_idx]
    
    # Build list of (index, score) pairs for chapters above threshold
    scored_chapters = []
    for idx, score in enumerate(scores):
        # Skip self-reference and chapters below threshold
        if idx == chapter_idx or score < threshold:
            continue
        
        chapter_info = index[idx]
        # Exclude chapters from same book (cross-book analysis only)
        if chapter_info["book"] == current_book:
            continue
        
        scored_chapters.append({
            "idx": idx,
            "score": float(score),  # Convert numpy float to Python float
            "book": chapter_info["book"],
            "chapter": chapter_info["chapter"],
            "title": chapter_info["title"]
        })
    
    # Sort by similarity score (descending) and take top N
    scored_chapters.sort(key=lambda x: x["score"], reverse=True)
    
    # Format output per schema
    related = []
    for item in scored_chapters[:top_n]:
        related.append({
            "book": item["book"],
            "chapter": item["chapter"],
            "title": item["title"],
            "relevance_score": round(item["score"], 2),
            "method": "cosine_similarity"
        })
    
    return related


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
    
    # Extract keywords using YAKE via StatisticalExtractor
    if STATISTICAL_EXTRACTOR:
        keywords_with_scores = STATISTICAL_EXTRACTOR.extract_keywords(
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
    
    # Extract concepts using Summa via StatisticalExtractor
    if STATISTICAL_EXTRACTOR:
        concepts = STATISTICAL_EXTRACTOR.extract_concepts(combined_text, top_n=top_n)
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


def _enrich_single_chapter(
    chapter: Dict[str, Any],
    book_name: str,
    corpus: List[str],
    index: List[Dict[str, Any]],
    similarity_matrix: Any
) -> Dict[str, Any]:
    """
    Helper function to enrich a single chapter (reduces cognitive complexity).
    
    Pattern: Extract Method refactoring (reduce complexity)
    
    Args:
        chapter: Chapter metadata dict from Tab 2
        book_name: Name of current book
        corpus: Full chapter corpus
        index: Chapter index
        similarity_matrix: Precomputed similarity matrix
        
    Returns:
        Enriched chapter dict with related_chapters, keywords_enriched, concepts_enriched
    """
    chapter_num = chapter.get("chapter_number")
    print(f"  Chapter {chapter_num}: {chapter.get('title', 'Untitled')}")
    
    # Find chapter index in corpus
    chapter_idx = None
    for idx, item in enumerate(index):
        if (item["book"] == f"{book_name}.json" and 
            item["chapter"] == chapter_num):
            chapter_idx = idx
            break
    
    if chapter_idx is None:
        print("    ⚠️  Chapter not found in corpus, skipping enrichment")
        return chapter
    
    # Find related chapters using cosine similarity
    related = find_related_chapters(
        chapter_idx,
        similarity_matrix,
        index,
        f"{book_name}.json",
        threshold=0.7,
        top_n=5
    )
    print(f"    Related chapters found: {len(related)}")
    
    # Get related chapter texts for keyword/concept enrichment
    related_texts = []
    for rel in related:
        for idx, item in enumerate(index):
            if (item["book"] == rel["book"] and 
                item["chapter"] == rel["chapter"]):
                related_texts.append(corpus[idx])
                break
    
    # Build current chapter text
    current_text = " ".join([
        chapter.get("title", ""),
        chapter.get("summary", ""),
        " ".join(chapter.get("keywords", [])),
        " ".join(chapter.get("concepts", []))
    ])
    
    # Re-score keywords with cross-book context
    keywords_enriched = rescore_keywords_cross_book(
        current_text,
        related_texts,
        top_n=10
    )
    
    # Extract cross-book concepts
    concepts_enriched = extract_concepts_cross_book(
        current_text,
        related_texts,
        top_n=10
    )
    
    # Build enriched chapter (preserve all original fields + add enrichments)
    return {
        **chapter,  # Preserve all Tab 2 fields
        "related_chapters": related,
        "keywords_enriched": keywords_enriched,
        "concepts_enriched": concepts_enriched
    }


def enrich_metadata(
    input_path: Path,
    taxonomy_path: Path,
    output_path: Path
) -> None:
    """
    Main enrichment function - orchestrates the complete Tab 4 workflow.
    
    Reference: TAB4_IMPLEMENTATION_PLAN.md - Function 7
    Pattern: Orchestration pattern (Architecture Patterns Ch. 8)
    
    Workflow:
    1. Load current book metadata (Tab 2 output)
    2. Load cross-book context from taxonomy (Tab 3 output)
    3. Build TF-IDF corpus from all books
    4. Compute similarity matrix
    5. For each chapter:
       a. Find related chapters (cosine similarity > 0.7)
       b. Re-score keywords with YAKE using cross-book context
       c. Extract concepts with Summa using cross-book context
    6. Generate enriched metadata JSON (Tab 4 output)
    
    Args:
        input_path: Path to {book}_metadata.json (Tab 2 output)
        taxonomy_path: Path to {book}_taxonomy.json (Tab 3 output)
        output_path: Path for {book}_metadata_enriched.json (Tab 4 output)
        
    Output Schema:
        {
            "book": str,
            "enrichment_metadata": {
                "generated": ISO timestamp,
                "method": "statistical",
                "libraries": {yake, summa, scikit-learn versions},
                "corpus_size": int,
                "total_chapters_analyzed": int
            },
            "chapters": [
                {
                    ... (all original Tab 2 fields preserved),
                    "related_chapters": [...],
                    "keywords_enriched": [...],
                    "concepts_enriched": [...]
                }
            ]
        }
    """
    print("\n📊 Tab 4: Statistical Enrichment")
    print(f"Input: {input_path.name}")
    print(f"Taxonomy: {taxonomy_path.name}")
    
    # 1. Load current book metadata
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    with open(input_path, encoding='utf-8') as f:
        book_metadata = json.load(f)
    
    book_name = input_path.stem.replace("_metadata", "")
    print(f"\nEnriching: {book_name}")
    print(f"Chapters: {len(book_metadata)}")
    
    # 2. Load cross-book context from taxonomy
    print("\nLoading companion books from taxonomy...")
    metadata_dir = input_path.parent
    context = load_cross_book_context(taxonomy_path, metadata_dir)
    
    # Add current book to context (needed for similarity comparisons)
    current_book_key = f"{book_name}.json"
    if current_book_key not in context['metadata']:
        context['metadata'][current_book_key] = book_metadata
        context['books'].append(current_book_key)
        context['corpus_size'] += len(book_metadata)
    
    print(f"  Books found: {len(context['books'])} (including current book)")
    print(f"  Total chapters: {context['corpus_size']}")
    
    # 3. Build TF-IDF corpus
    print("\nBuilding TF-IDF corpus...")
    corpus, index = build_chapter_corpus(context)
    print(f"  Corpus size: {len(corpus)} chapters")
    
    # 4. Compute similarity matrix
    print("\nComputing cosine similarity matrix...")
    similarity_matrix = compute_similarity_matrix(corpus)
    print(f"  Matrix shape: {similarity_matrix.shape}")
    
    # 5. Enrich each chapter using helper function
    print("\nEnriching chapters with cross-book analysis...")
    enriched_chapters = [
        _enrich_single_chapter(chapter, book_name, corpus, index, similarity_matrix)
        for chapter in book_metadata
    ]
    
    # 6. Build enriched metadata output
    enriched_metadata = {
        "book": book_name,
        "enrichment_metadata": {
            "generated": datetime.now().isoformat(),
            "method": "statistical",
            "libraries": {
                "yake": "0.4.8",
                "summa": "1.2.0",
                "scikit-learn": "1.3.2"
            },
            "corpus_size": len(context["books"]),
            "total_chapters_analyzed": context["corpus_size"]
        },
        "chapters": enriched_chapters
    }
    
    # 7. Save enriched metadata
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(enriched_metadata, f, indent=2, ensure_ascii=False)
    
    # Calculate and report file size
    size_kb = output_path.stat().st_size / 1024
    print(f"\n✅ Enriched metadata saved: {output_path.name}")
    print(f"  File size: {size_kb:.1f} KB")
    print(f"  Chapters enriched: {len(enriched_chapters)}")
    print("  Statistical method: TF-IDF + cosine similarity")
    print("  NO LLM calls made ✓")


def main():
    """
    Command-line interface for metadata enrichment.
    
    Example:
        python enrich_metadata_per_book.py \\
            --input workflows/metadata_extraction/output/architecture_patterns_metadata.json \\
            --taxonomy workflows/taxonomy_setup/output/architecture_patterns_taxonomy.json \\
            --output workflows/metadata_enrichment/output/architecture_patterns_metadata_enriched.json
    """
    parser = argparse.ArgumentParser(
        description="Enrich metadata with cross-book statistical analysis (Tab 4)"
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
        required=True,
        help="Taxonomy JSON from Tab 3 (e.g., architecture_patterns_taxonomy.json)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output enriched metadata JSON (e.g., architecture_patterns_metadata_enriched.json)"
    )
    
    args = parser.parse_args()
    
    # Validate inputs exist
    if not args.input.exists():
        print(f"❌ Error: Input file not found: {args.input}")
        sys.exit(1)
    
    if not args.taxonomy.exists():
        print(f"❌ Error: Taxonomy file not found: {args.taxonomy}")
        sys.exit(1)
    
    # Run enrichment
    try:
        enrich_metadata(args.input, args.taxonomy, args.output)
    except Exception as e:
        print(f"\n❌ Enrichment failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
