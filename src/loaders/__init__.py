"""
Content loaders module for two-phase LLM workflow.

Sprint 3.2 - TDD GREEN: Module interface for content loading utilities

Following Document Hierarchy:
- REFACTORING_PLAN.md: Sprint 3.2 - Extract content loaders
- ARCHITECTURE_GUIDELINES: Clean module interfaces (Ch. 2)
- PYTHON_GUIDELINES Ch. 8: Package design and exports

Exports:
- BookContentRepository: Repository pattern for loading book JSON files
- ChapterContentLoader: Strategy pattern for loading chapter content

References:
    - Source: Extracted from interactive_llm_system_v3_hybrid_prompt.py
    - Pattern: Repository Pattern (Architecture Patterns Ch. 4)
    - Pattern: Strategy Pattern (Architecture Patterns Ch. 5)
"""

from .content_loaders import (
    BookContentRepository,
    ChapterContentLoader,
)

__all__ = [
    'BookContentRepository',
    'ChapterContentLoader',
]
