"""
Tool Handlers for LLM Enhancement - WBS 3.1.2.2 Tool-Use Integration

Implements handlers for each tool defined in definitions.py.
These handlers interact with the document corpus services.

Reference Documents:
- llm-gateway/src/tools/executor.py: Handler pattern
- workflows/metadata_enrichment/scripts/chapter_metadata_manager.py
- workflows/metadata_enrichment/scripts/semantic_similarity_engine.py
"""

from pathlib import Path
from typing import Any, Optional

# Lazy imports to avoid circular dependencies
_chapter_manager: Optional[Any] = None
_similarity_engine: Optional[Any] = None


def _get_chapter_manager() -> Any:
    """Lazy load ChapterMetadataManager."""
    global _chapter_manager
    if _chapter_manager is None:
        from workflows.metadata_enrichment.scripts.chapter_metadata_manager import (
            ChapterMetadataManager,
        )
        _chapter_manager = ChapterMetadataManager()
    return _chapter_manager


def _get_similarity_engine() -> Any:
    """Lazy load SemanticSimilarityEngine."""
    global _similarity_engine
    if _similarity_engine is None:
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
        )
        _similarity_engine = SemanticSimilarityEngine()
    return _similarity_engine


def _get_corpus_dir() -> Path:
    """Get the corpus directory path."""
    # Default to outputs directory
    project_root = Path(__file__).parent.parent.parent.parent
    return project_root / "outputs"


def search_corpus(
    query: str,
    top_k: int = 5,
    min_similarity: float = 0.3,
) -> dict[str, Any]:
    """
    Search the document corpus for chapters related to a query.

    Args:
        query: The search query
        top_k: Maximum number of results
        min_similarity: Minimum similarity threshold

    Returns:
        Dict with 'results' list containing matching chapters
    """
    try:
        manager = _get_chapter_manager()
        engine = _get_similarity_engine()

        # Get all available books
        corpus_dir = _get_corpus_dir()
        json_files = list(corpus_dir.glob("*_Content.json"))

        if not json_files:
            return {"results": [], "message": "No corpus files found"}

        # Build corpus and index
        corpus_texts: list[str] = []
        chapter_index: list[dict[str, Any]] = []

        for json_file in json_files:
            filename = json_file.name
            chapters = manager.get_chapters(filename)

            for chapter in chapters:
                # Use title + keywords as search text
                search_text = f"{chapter.title} {' '.join(chapter.keywords)}"
                if chapter.summary:
                    search_text += f" {chapter.summary}"

                corpus_texts.append(search_text)
                chapter_index.append({
                    "book": filename,
                    "chapter": chapter.chapter_number,
                    "title": chapter.title,
                    "pages": f"{chapter.start_page}-{chapter.end_page}",
                })

        if not corpus_texts:
            return {"results": [], "message": "No chapters found in corpus"}

        # Compute embeddings and find similar
        embeddings = engine.compute_embeddings(corpus_texts + [query])

        # Query is the last embedding
        query_embedding = embeddings[-1:]
        corpus_embeddings = embeddings[:-1]

        # Compute similarities
        from sklearn.metrics.pairwise import cosine_similarity
        similarities = cosine_similarity(query_embedding, corpus_embeddings)[0]

        # Get top-k results above threshold
        results = []
        sorted_indices = similarities.argsort()[::-1]

        for idx in sorted_indices[:top_k]:
            score = float(similarities[idx])
            if score >= min_similarity:
                result = chapter_index[idx].copy()
                result["score"] = round(score, 3)
                results.append(result)

        return {"results": results, "query": query}

    except Exception as e:
        return {"error": str(e), "results": []}


def get_chapter(
    book: str,
    chapter_number: int,
) -> dict[str, Any]:
    """
    Get detailed metadata for a specific chapter.

    Args:
        book: The book filename
        chapter_number: The chapter number

    Returns:
        Dict with chapter metadata
    """
    try:
        manager = _get_chapter_manager()
        chapter = manager.get_chapter_by_number(book, chapter_number)

        if chapter is None:
            return {"error": f"Chapter {chapter_number} not found in {book}"}

        return {
            "book": book,
            "chapter_number": chapter.chapter_number,
            "title": chapter.title,
            "pages": f"{chapter.start_page}-{chapter.end_page}",
            "page_count": chapter.page_count,
            "keywords": chapter.keywords,
            "summary": chapter.summary,
            "concepts": chapter.concepts or [],
        }

    except Exception as e:
        return {"error": str(e)}


def get_related_chapters(
    book: str,
    chapter_number: int,
    top_k: int = 5,
    exclude_same_book: bool = False,
) -> dict[str, Any]:
    """
    Find chapters semantically related to a given chapter.

    Args:
        book: The book filename of the source chapter
        chapter_number: The source chapter number
        top_k: Maximum number of related chapters
        exclude_same_book: Whether to exclude chapters from same book

    Returns:
        Dict with 'related' list of similar chapters
    """
    try:
        manager = _get_chapter_manager()
        source_chapter = manager.get_chapter_by_number(book, chapter_number)

        if source_chapter is None:
            return {"error": f"Chapter {chapter_number} not found in {book}"}

        # Build search query from source chapter
        query = f"{source_chapter.title} {' '.join(source_chapter.keywords)}"
        if source_chapter.summary:
            query += f" {source_chapter.summary}"

        # Search corpus
        results = search_corpus(query, top_k=top_k + 5, min_similarity=0.1)

        if "error" in results:
            return results

        # Filter results
        related = []
        for result in results.get("results", []):
            # Skip the source chapter itself
            if result["book"] == book and result["chapter"] == chapter_number:
                continue

            # Skip same book if requested
            if exclude_same_book and result["book"] == book:
                continue

            related.append(result)

            if len(related) >= top_k:
                break

        return {
            "source": {
                "book": book,
                "chapter": chapter_number,
                "title": source_chapter.title,
            },
            "related": related,
        }

    except Exception as e:
        return {"error": str(e)}


def list_books() -> dict[str, Any]:
    """
    List all books available in the corpus.

    Returns:
        Dict with 'books' list containing book info
    """
    try:
        manager = _get_chapter_manager()
        corpus_dir = _get_corpus_dir()

        json_files = list(corpus_dir.glob("*_Content.json"))

        books = []
        for json_file in json_files:
            filename = json_file.name
            chapters = manager.get_chapters(filename)

            # Extract book title from filename
            title = filename.replace("_Content.json", "").replace("_", " ")

            books.append({
                "filename": filename,
                "title": title,
                "chapter_count": len(chapters),
            })

        return {"books": books, "total": len(books)}

    except Exception as e:
        return {"error": str(e)}


# =============================================================================
# Handler Registry
# =============================================================================

TOOL_HANDLERS: dict[str, Any] = {
    "search_corpus": search_corpus,
    "get_chapter": get_chapter,
    "get_related_chapters": get_related_chapters,
    "list_books": list_books,
}


def execute_tool(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """
    Execute a tool by name with given arguments.

    Args:
        tool_name: Name of the tool to execute
        arguments: Arguments to pass to the tool

    Returns:
        Tool execution result as dict

    Raises:
        ValueError: If tool not found
    """
    handler = TOOL_HANDLERS.get(tool_name)
    if handler is None:
        raise ValueError(f"Unknown tool: {tool_name}")

    return handler(**arguments)
