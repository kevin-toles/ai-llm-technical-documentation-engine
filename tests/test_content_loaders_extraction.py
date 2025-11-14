"""
Sprint 3.2 - TDD RED: Content loaders extraction tests.

Following Document Hierarchy:
1. REFACTORING_PLAN.md: Sprint 3.2 - Extract content loading methods
2. BOOK_TAXONOMY_MATRIX.md (docs/): Engineering Practices tier - Python fundamentals
3. ARCHITECTURE_GUIDELINES: Repository Pattern (Ch. 4), Single Responsibility
4. PYTHON_GUIDELINES: File I/O (Ch. 9), Path handling (Ch. 10)

TDD RED Phase:
- Create failing tests for content loader extraction
- Test module exists
- Test each loader function signature
- Test backward compatibility (imports from both old and new locations)

Architectural Patterns:
- Repository Pattern: BookContentRepository for data access abstraction
- Strategy Pattern: Different loading strategies (full chapter vs. page excerpts)
- Lazy Loading: Load content only when requested

Expected extraction targets from interactive_llm_system_v3_hybrid_prompt.py:
- _load_book_json_by_name (lines 844-895)
- _load_full_chapter_content (lines 682-721)
- _load_chapters_for_request (lines 724-756)
- _load_page_excerpts_for_request (lines 759-787)
- _get_citation_info (lines 897-936)
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from typing import Dict, List, Optional, Any


def test_loaders_module_exists():
    """
    TDD RED: Verify src/loaders/content_loaders.py exists.
    
    Per REFACTORING_PLAN.md Sprint 3.2: Extract content loading methods
    Per ARCHITECTURE_GUIDELINES: Repository Pattern for data access
    """
    loaders_file = Path(__file__).parent.parent / "src" / "loaders" / "content_loaders.py"
    assert loaders_file.exists(), "src/loaders/content_loaders.py should exist"


def test_book_content_repository_class_extracted():
    """
    TDD RED: Verify BookContentRepository class exists with repository pattern.
    
    Per ARCHITECTURE_GUIDELINES Ch. 4: Repository Pattern
    - Abstracts data access from business logic
    - Provides clean interface for loading book content
    - Encapsulates file system interactions
    
    Expected methods:
    - load_book_json(book_name: str) -> Optional[Dict]
    - get_citation_info(book_name: str) -> tuple[str, str]
    """
    from loaders.content_loaders import BookContentRepository
    
    # Verify class exists
    assert BookContentRepository is not None
    
    # Verify it's instantiable
    repo = BookContentRepository()
    assert repo is not None
    
    # Verify key methods exist
    assert hasattr(repo, 'load_book_json')
    assert hasattr(repo, 'get_citation_info')


def test_chapter_content_loader_class_extracted():
    """
    TDD RED: Verify ChapterContentLoader class exists with strategy pattern.
    
    Per ARCHITECTURE_GUIDELINES Ch. 5: Strategy Pattern
    - Different loading strategies (full chapter vs. page excerpts)
    - Encapsulates chapter loading logic
    
    Expected methods:
    - load_full_chapter(chapter_num, chapter_info, book_content, book_name)
    - load_chapters_for_request(request, book_content, chapter_manager)
    - load_page_excerpts(request, book_content)
    """
    from loaders.content_loaders import ChapterContentLoader
    
    # Verify class exists
    assert ChapterContentLoader is not None
    
    # Verify it's instantiable
    loader = ChapterContentLoader()
    assert loader is not None
    
    # Verify key methods exist
    assert hasattr(loader, 'load_full_chapter')
    assert hasattr(loader, 'load_chapters_for_request')
    assert hasattr(loader, 'load_page_excerpts')


def test_load_book_json_signature():
    """
    TDD RED: Verify load_book_json method has correct signature.
    
    Per PYTHON_GUIDELINES Ch. 9: File I/O operations
    Per PYTHON_GUIDELINES Ch. 7: Type hints for clarity
    
    Expected signature:
        def load_book_json(self, book_name: str) -> Optional[Dict]
    """
    from loaders.content_loaders import BookContentRepository
    import inspect
    
    repo = BookContentRepository()
    sig = inspect.signature(repo.load_book_json)
    
    # Verify parameters
    assert 'book_name' in sig.parameters
    assert sig.parameters['book_name'].annotation == str
    
    # Verify return type
    assert 'Optional[Dict]' in str(sig.return_annotation) or 'Dict | None' in str(sig.return_annotation)


def test_load_full_chapter_signature():
    """
    TDD RED: Verify load_full_chapter method has correct signature.
    
    Per PYTHON_GUIDELINES Ch. 7: Type hints
    Per ARCHITECTURE_GUIDELINES: Single Responsibility - load one chapter
    
    Expected signature:
        def load_full_chapter(
            self,
            chapter_num: int,
            chapter_info,
            book_content: Dict,
            book_name: str
        ) -> Optional[Dict[str, Any]]
    """
    from loaders.content_loaders import ChapterContentLoader
    import inspect
    
    loader = ChapterContentLoader()
    sig = inspect.signature(loader.load_full_chapter)
    
    # Verify key parameters exist
    assert 'chapter_num' in sig.parameters
    assert 'chapter_info' in sig.parameters
    assert 'book_content' in sig.parameters
    assert 'book_name' in sig.parameters
    
    # Verify parameter types
    assert sig.parameters['chapter_num'].annotation == int
    assert sig.parameters['book_content'].annotation == Dict
    assert sig.parameters['book_name'].annotation == str


def test_get_citation_info_signature():
    """
    TDD RED: Verify get_citation_info method has correct signature.
    
    Per PYTHON_GUIDELINES Ch. 7: Type hints with tuple returns
    
    Expected signature:
        def get_citation_info(self, book_name: str) -> tuple[str, str]
    
    Returns (author, full_title) for Chicago-style citations.
    """
    from loaders.content_loaders import BookContentRepository
    import inspect
    
    repo = BookContentRepository()
    sig = inspect.signature(repo.get_citation_info)
    
    # Verify parameter
    assert 'book_name' in sig.parameters
    assert sig.parameters['book_name'].annotation == str
    
    # Verify return type is tuple
    return_annotation = str(sig.return_annotation)
    assert 'tuple' in return_annotation.lower()


def test_backward_compatibility_imports():
    """
    TDD RED: Verify backward compatibility - old imports still work.
    
    Per REFACTORING_PLAN.md: Maintain backward compatibility during refactoring
    Per PYTHON_GUIDELINES Ch. 8: Module design for gradual migration
    
    After extraction, old code should still be able to import from
    interactive_llm_system_v3_hybrid_prompt.py, which will delegate
    to the new loaders module.
    """
    # This will fail initially - should pass after GREEN phase
    from interactive_llm_system_v3_hybrid_prompt import AnalysisOrchestrator
    
    # Verify orchestrator still has the methods (as wrappers)
    orchestrator = AnalysisOrchestrator(
        chapter_file_path="dummy.json",
        taxonomy_scores={"test": 1.0}
    )
    
    # These should exist but delegate to loaders
    assert hasattr(orchestrator, '_load_book_json_by_name')
    assert hasattr(orchestrator, '_load_full_chapter_content')
    assert hasattr(orchestrator, '_get_citation_info')


def test_loaders_module_imports():
    """
    TDD RED: Verify src/loaders/__init__.py exports key classes.
    
    Per PYTHON_GUIDELINES Ch. 8: Clean module interfaces
    Per ARCHITECTURE_GUIDELINES: Public API design
    
    Expected exports:
    - BookContentRepository
    - ChapterContentLoader
    """
    from loaders import BookContentRepository, ChapterContentLoader
    
    # Verify imports work from package level
    assert BookContentRepository is not None
    assert ChapterContentLoader is not None


def test_repository_pattern_compliance():
    """
    TDD RED: Verify Repository pattern implementation.
    
    Per ARCHITECTURE_GUIDELINES Ch. 4: Repository Pattern
    - Repository abstracts data access
    - Returns domain objects (dicts with structured data)
    - Handles file system errors gracefully
    
    This test verifies the pattern is correctly implemented.
    """
    from loaders.content_loaders import BookContentRepository
    
    repo = BookContentRepository()
    
    # Repository should handle invalid book names gracefully
    result = repo.load_book_json("NonExistentBook")
    assert result is None or isinstance(result, dict)
    
    # Citation info should always return a tuple
    author, title = repo.get_citation_info("Unknown Book")
    assert isinstance(author, str)
    assert isinstance(title, str)
