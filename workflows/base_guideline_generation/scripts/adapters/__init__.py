"""
Pipeline adapters package - Chapter Generator Adapter

Wraps chapter generation with clean adapter interface.
Pattern: Adapter Pattern (Architecture Patterns with Python Ch. 13)
"""

from .chapter_generator import ChapterGeneratorAdapter, ChapterGenerationError

__all__ = [
    "ChapterGeneratorAdapter",
    "ChapterGenerationError",
]
