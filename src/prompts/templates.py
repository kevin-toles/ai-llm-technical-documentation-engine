"""
Template loader for LLM prompts.

TDD REFACTOR Phase: Enhanced implementation with type safety and documentation.

Architectural Patterns:
- Separation of Concerns: Templates stored as .txt files, not embedded in code
- EAFP: "Easier to Ask Forgiveness than Permission" - let exceptions propagate
- Context Managers: Use 'with' statements for safe file handling

References:
- ARCHITECTURE_GUIDELINES Ch 13: Dependency Injection, separation of concerns
- PYTHON_GUIDELINES: pathlib.Path, context managers, EAFP error handling
- REFACTORING_PLAN.md Section II.2.1: Extract prompts to src/prompts/
"""

from pathlib import Path
from typing import Any, Dict, Final, List

# Template directory is fixed relative to this module
TEMPLATE_DIR: Final[Path] = Path(__file__).parent


def load_template(name: str) -> str:
    """
    Load a prompt template from file.
    
    Implements EAFP pattern from PYTHON_GUIDELINES:
    "If read_data() is given a bad filename, there is no sensible way to recover...
    It's better to let the operation fail and report an exception back to the caller."
    
    Args:
        name: Template name (without .txt extension). Must be a valid filename.
              Examples: "comprehensive_phase1", "phase2"
        
    Returns:
        Template content as UTF-8 encoded string, ready for str.format() replacement.
        
    Raises:
        FileNotFoundError: If template file doesn't exist at {TEMPLATE_DIR}/{name}.txt
        IOError: If file cannot be read (permissions, encoding errors)
        ValueError: If name contains path separators (security check)
        
    Example:
        >>> template = load_template("test_template")
        >>> formatted = template.format(placeholder1="value1", placeholder2="value2")
        
    References:
        - PYTHON_GUIDELINES: "pathlib.Path for cross-platform file operations"
        - PYTHON_GUIDELINES: "with open() for context management"
        - PYTHON_GUIDELINES: "Explicit UTF-8 encoding for cross-platform compatibility"
    """
    # Security: Prevent path traversal attacks
    if '/' in name or '\\' in name:
        raise ValueError(f"Template name cannot contain path separators: {name}")
    
    template_path = TEMPLATE_DIR / f"{name}.txt"
    with template_path.open('r', encoding='utf-8') as f:
        return f.read()


def _format_book_description(book: Dict[str, Any], index: int) -> str:
    """
    Format a single book's metadata description with chapter details.
    
    Extracted from interactive_llm_system_v3_hybrid_prompt.py line 788
    to support template formatting.
    
    Args:
        book: Book metadata dict with keys: title, author, full_title, domain,
              concepts_covered, has_chapter_metadata, chapters
        index: Book number in list (1-based)
        
    Returns:
        Formatted book description string
        
    References:
        - Source: interactive_llm_system_v3_hybrid_prompt.py::_format_book_description
    """
    book_desc = (
        f"{index}. {book['title']}\n"
        f"   Author(s): {book.get('author', 'Unknown')}\n"
        f"   Full Title: {book.get('full_title', book['title'])}\n"
        f"   Domain: {book['domain']}\n"
        f"   Concepts: {', '.join(book['concepts_covered'][:8])}"
    )
    
    # Add detailed chapter information if available
    if book.get('has_chapter_metadata') and book.get('chapters'):
        chapters_summary = "\n   Chapters:"
        for ch in book['chapters'][:10]:  # Show first 10 chapters with full metadata
            chapters_summary += (
                f"\n     • Ch.{ch['number']}: {ch['title']} (pp.{ch['pages']})"
            )
            if ch.get('summary'):
                chapters_summary += f"\n       Summary: {ch['summary']}"
            if ch.get('concepts'):
                chapters_summary += f"\n       Concepts: {', '.join(ch['concepts'][:5])}"
        
        if len(book['chapters']) > 10:
            chapters_summary += f"\n     ... [{len(book['chapters'])} chapters total]"
        book_desc += chapters_summary
    
    return book_desc


def format_comprehensive_phase1_prompt(
    chapter_num: int,
    chapter_title: str,
    chapter_full_text: str,
    books_metadata: List[Dict[str, Any]]
) -> str:
    """
    Format comprehensive Phase 1 prompt with actual values.
    
    TDD GREEN: Minimal implementation to pass tests.
    
    Args:
        chapter_num: Chapter number (e.g., 1, 2, 3)
        chapter_title: Chapter title (e.g., "Introduction to Python")
        chapter_full_text: Full chapter text content
        books_metadata: List of book metadata dicts
        
    Returns:
        Formatted prompt string ready for LLM
        
    References:
        - Source: interactive_llm_system_v3_hybrid_prompt.py::_build_comprehensive_phase1_prompt
        - Template: src/prompts/comprehensive_phase1.txt
    """
    template = load_template("comprehensive_phase1")
    
    # Format book metadata list
    books_list = [
        _format_book_description(book, i) 
        for i, book in enumerate(books_metadata, 1)
    ]
    books_text = "\n\n".join(books_list)
    
    # Prepare text preview and truncation indicator
    chapter_text_preview = chapter_full_text[:8000]
    chapter_text_truncation = (
        "... [truncated for prompt length]" 
        if len(chapter_full_text) > 8000 
        else ""
    )
    
    return template.format(
        chapter_num=chapter_num,
        chapter_title=chapter_title,
        chapter_text_length=len(chapter_full_text),
        chapter_text_preview=chapter_text_preview,
        chapter_text_truncation=chapter_text_truncation,
        books_count=len(books_metadata),
        books_text=books_text
    )


def _format_excerpt_content(book_name: str, excerpts: List[Dict[str, Any]]) -> str:
    """Format book excerpts (full chapters or page excerpts) with citation info.
    
    Extracted from interactive_llm_system_v3_hybrid_prompt.py::_build_comprehensive_phase2_prompt
    
    Args:
        book_name: Name of the book
        excerpts: List of excerpt dictionaries (each has either is_full_chapter or page)
        
    Returns:
        Formatted excerpt sections with citations
        
    References:
        - Source: interactive_llm_system_v3_hybrid_prompt.py lines 1153-1174
    """
    sections = [f"\n## {book_name}"]
    
    for exc in excerpts:
        if exc.get('is_full_chapter'):
            # Full chapter content with citation info
            sections.append(
                f"\n**Chapter {exc['chapter']}: {exc['title']}**\n"
                f"Citation: {exc.get('author', 'Unknown')}, *{exc.get('book_title', book_name)}*, "
                f"Chapter {exc['chapter']}, pages {exc['pages']}.\n"
                f"Content:\n{exc['content'][:4000]}..."  # First 4000 chars of chapter
            )
        else:
            # Page excerpt with citation info
            sections.append(
                f"\n**Page {exc['page']}**\n"
                f"Citation: {exc.get('author', 'Unknown')}, *{exc.get('book_title', book_name)}*, {exc['page']}.\n"
                f"Content: {exc['content'][:600]}..."
            )
    
    return '\n'.join(sections)


def format_comprehensive_phase2_prompt(
    chapter_num: int,
    chapter_title: str,
    metadata_response: Any,  # MetadataExtractionResponse with validation_summary, analysis_strategy
    content_package: Dict[str, Any]
) -> str:
    """Format Phase 2 comprehensive prompt for integrated scholarly annotation.
    
    Builds prompt for generating integrated scholarly annotations that synthesize
    content from multiple companion books with Chicago-style citations.
    
    Args:
        chapter_num: Chapter number
        chapter_title: Chapter title
        metadata_response: Object with .validation_summary and .analysis_strategy attributes
        content_package: Dict mapping book_name -> list of excerpt dicts
        
    Returns:
        Formatted prompt string ready for LLM
        
    References:
        - Source: interactive_llm_system_v3_hybrid_prompt.py::_build_comprehensive_phase2_prompt
        - Template: src/prompts/comprehensive_phase2.txt
    """
    template = load_template("comprehensive_phase2")
    
    # Build content sections from all books
    content_sections = []
    for book_name, excerpts in content_package.items():
        content_sections.append(_format_excerpt_content(book_name, excerpts))
    
    content_text = '\n'.join(content_sections)
    
    return template.format(
        chapter_num=chapter_num,
        chapter_title=chapter_title,
        metadata_response_validation_summary=metadata_response.validation_summary,
        metadata_response_analysis_strategy=metadata_response.analysis_strategy,
        content_package_count=len(content_package),
        content_text=content_text[:15000]  # Limit to first 15000 chars
    )
