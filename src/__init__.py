"""
LLM Document Enhancer - Intelligent document enhancement using Claude.

This package provides a two-phase LLM workflow for enhancing technical documentation
with citations from a curated library of Python programming books.
"""

__version__ = "1.0.0"
__author__ = "Kevin Toles"

# Lazy imports to avoid circular dependencies
__all__ = [
    "main",
    "EnhancedLLMSystemV3",
    "MetadataServiceFactory",
    "MetadataExtractionService",
    "ChapterMetadataManager",
    "call_llm",
    "get_recommended_books",
    "get_cascading_books",
    "score_books_for_concepts",
    "BOOK_REGISTRY",
    "BookTier",
]
