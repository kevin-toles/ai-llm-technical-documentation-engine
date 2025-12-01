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
from typing import Any, Dict, Final, List, Optional

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
    books_metadata: List[Dict[str, Any]],
    source_book_name: str = "Unknown Book"
) -> str:
    """
    Format comprehensive Phase 1 prompt with actual values.
    
    TDD GREEN: Minimal implementation to pass tests.
    
    Args:
        chapter_num: Chapter number (e.g., 1, 2, 3)
        chapter_title: Chapter title (e.g., "Introduction to Python")
        chapter_full_text: Full chapter text content
        books_metadata: List of book metadata dicts
        source_book_name: Name of the source book being analyzed (dynamic, not hardcoded)
        
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
        source_book_name=source_book_name,
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


def _format_taxonomy_for_prompt(taxonomy_data: Optional[Dict[str, Any]]) -> str:
    """Format taxonomy data into a readable string for the LLM prompt.
    
    Args:
        taxonomy_data: Taxonomy dict with 'tiers' containing book assignments
        
    Returns:
        Formatted string showing tier -> books mapping
    """
    if not taxonomy_data or 'tiers' not in taxonomy_data:
        return "No taxonomy data available."
    
    lines = []
    tiers = taxonomy_data.get('tiers', {})
    
    # Sort by priority (1, 2, 3)
    sorted_tiers = sorted(
        tiers.items(),
        key=lambda x: x[1].get('priority', 99) if isinstance(x[1], dict) else 99
    )
    
    for tier_key, tier_data in sorted_tiers:
        if not isinstance(tier_data, dict):
            continue
            
        priority = tier_data.get('priority', '?')
        name = tier_data.get('name', tier_key.title())
        books = tier_data.get('books', [])
        
        # Clean up book names (remove .json extension)
        clean_books = [b.replace('.json', '') for b in books[:10]]  # Limit to 10
        
        lines.append(f"Priority {priority} - {name}:")
        for book in clean_books:
            lines.append(f"  • {book}")
        if len(books) > 10:
            lines.append(f"  ... and {len(books) - 10} more")
        lines.append("")
    
    return '\n'.join(lines)


def format_comprehensive_phase2_prompt(
    chapter_num: int,
    chapter_title: str,
    metadata_response: Any,  # MetadataExtractionResponse with validation_summary, analysis_strategy
    content_package: Dict[str, Any],
    source_book_name: str = "Unknown Book",
    taxonomy_data: Optional[Dict[str, Any]] = None
) -> str:
    """Format Phase 2 comprehensive prompt for integrated scholarly annotation.
    
    Builds prompt for generating integrated scholarly annotations that synthesize
    content from multiple companion books with Chicago-style citations.
    
    Args:
        chapter_num: Chapter number
        chapter_title: Chapter title
        metadata_response: Object with .validation_summary and .analysis_strategy attributes
        content_package: Dict mapping book_name -> list of excerpt dicts
        source_book_name: Name of the source book being analyzed (dynamic, not hardcoded)
        taxonomy_data: Taxonomy dict with tiers and book assignments
        
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
    
    # Format taxonomy for prompt
    taxonomy_text = _format_taxonomy_for_prompt(taxonomy_data) if taxonomy_data else "No taxonomy data available."
    
    return template.format(
        source_book_name=source_book_name,
        chapter_num=chapter_num,
        chapter_title=chapter_title,
        metadata_response_validation_summary=metadata_response.validation_summary,
        metadata_response_analysis_strategy=metadata_response.analysis_strategy,
        content_package_count=len(content_package),
        content_text=content_text[:15000],  # Limit to first 15000 chars
        taxonomy_text=taxonomy_text
    )


def format_phase1_prompt(
    chapter_num: int,
    chapter_title: str,
    concepts: List[str],
    excerpt: str,
    metadata_package: Dict[str, Any]
) -> str:
    """Format Phase 1 prompt for metadata analysis and gap identification.
    
    Builds prompt for LLM to analyze Python keyword matching results and request
    specific book content needed for comprehensive cross-reference analysis.
    
    Args:
        chapter_num: Chapter number
        chapter_title: Chapter title
        concepts: List of key concepts from chapter
        excerpt: Chapter text excerpt (will be truncated to 800 chars)
        metadata_package: Dict with keys:
            - concept_mapping: Dict mapping concepts to book/page matches
            - total_books: Total number of companion books
            - total_pages: Total page count across all books
            - books: List of book metadata dicts
        
    Returns:
        Formatted prompt string ready for LLM
        
    References:
        - Source: interactive_llm_system_v3_hybrid_prompt.py::_build_phase1_prompt
        - Template: src/prompts/phase1.txt
        - BOOK_TAXONOMY_MATRIX.md: Book tier classifications embedded in template
        - PYTHON_GUIDELINES: json.dumps for structured data formatting
        
    Document Hierarchy Compliance:
        - REFACTORING_PLAN.md: Sprint 2 template extraction
        - ARCHITECTURE_GUIDELINES: Separation of concerns principle
    """
    import json
    
    template = load_template("phase1")
    
    # Format concepts as comma-separated string
    concepts_str = ', '.join(concepts)
    
    # Truncate excerpt to 800 chars (as per original)
    excerpt_truncated = excerpt[:800]
    
    # Format concept_mapping as JSON (with indentation for readability)
    concept_mapping_json = json.dumps(metadata_package['concept_mapping'], indent=2)
    
    # Format books metadata as JSON
    books_metadata_json = json.dumps(metadata_package['books'], indent=2)
    
    # Format total_pages with thousands separator
    total_pages_formatted = f"{metadata_package['total_pages']:,}"
    
    return template.format(
        chapter_num=chapter_num,
        chapter_title=chapter_title,
        concepts=concepts_str,
        excerpt=excerpt_truncated,
        concept_mapping=concept_mapping_json,
        total_books=metadata_package['total_books'],
        total_pages=total_pages_formatted,
        books_metadata=books_metadata_json
    )


def format_phase2_prompt(
    chapter_num: int,
    chapter_title: str,
    concepts: List[str],
    excerpt: str,
    metadata_response: Any,  # LLMMetadataResponse with validation_summary, gap_analysis, analysis_strategy
    content_package: Dict[str, List[Dict]]
) -> str:
    """Format Phase 2 prompt for deep scholarly cross-text analysis.
    
    Builds prompt for LLM to generate scholarly annotations by analyzing relationships
    between primary text and companion book excerpts retrieved in Phase 1.
    
    Args:
        chapter_num: Chapter number
        chapter_title: Chapter title
        concepts: List of key concepts from chapter
        excerpt: Chapter text excerpt (will be truncated to 800 chars)
        metadata_response: Object with attributes:
            - validation_summary: Phase 1 validation of Python keyword matches
            - gap_analysis: Identified gaps in keyword matching
            - analysis_strategy: Planned approach for content retrieval
        content_package: Dict mapping book_name -> list of page excerpt dicts
            Each excerpt dict has: page, content
        
    Returns:
        Formatted prompt string ready for LLM
        
    References:
        - Source: interactive_llm_system_v3_hybrid_prompt.py::_build_phase2_prompt
        - Template: src/prompts/phase2.txt
        - ARCHITECTURE_GUIDELINES: Separation of concerns principle
        - PYTHON_GUIDELINES: Template composition patterns
        
    Document Hierarchy Compliance:
        - REFACTORING_PLAN.md: Sprint 2 template extraction (final prompt)
        - Preserves critical analysis methodology from original
    """
    template = load_template("phase2")
    
    # Format concepts as comma-separated string
    concepts_str = ', '.join(concepts)
    
    # Truncate excerpt to 800 chars (as per original)
    excerpt_truncated = excerpt[:800]
    
    # Truncate metadata response fields to 200 chars (as per original)
    validation_summary_truncated = metadata_response.validation_summary[:200]
    gap_analysis_truncated = metadata_response.gap_analysis[:200]
    analysis_strategy_truncated = metadata_response.analysis_strategy[:200]
    
    # Format content package into text sections
    content_sections = []
    for book_name, excerpts in content_package.items():
        content_sections.append(f"\n## {book_name}")
        for exc in excerpts:
            content_sections.append(
                f"\nPage {exc['page']}: {exc['content'][:500]}..."
            )
    
    content_text = '\n'.join(content_sections)
    
    # Limit content to 8000 chars (as per original)
    content_text_truncated = content_text[:8000]
    
    return template.format(
        chapter_num=chapter_num,
        chapter_title=chapter_title,
        concepts=concepts_str,
        excerpt=excerpt_truncated,
        validation_summary=validation_summary_truncated,
        gap_analysis=gap_analysis_truncated,
        analysis_strategy=analysis_strategy_truncated,
        content_package_count=len(content_package),
        content_text=content_text_truncated
    )
