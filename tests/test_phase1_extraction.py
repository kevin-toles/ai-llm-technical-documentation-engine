"""
TDD RED PHASE: Sprint 2.13 - Extract phase1 prompt template.

Document Hierarchy Compliance:
- REFACTORING_PLAN.md: Sprint 2 Day 1-2 (Extract prompt templates)
- ARCHITECTURE_GUIDELINES: Separation of concerns, template patterns
- PYTHON_GUIDELINES: str.format() for template composition

These tests MUST FAIL initially (TDD RED), then pass after extraction (TDD GREEN).
"""
from pathlib import Path
from typing import Any, Dict, List

import pytest


def test_phase1_template_file_exists():
    """
    TDD RED: Verify phase1.txt template file exists.
    
    Expected to FAIL until GREEN phase creates the template file.
    
    References:
    - REFACTORING_PLAN.md: Sprint 2 template extraction
    - Source: interactive_llm_system_v3_hybrid_prompt.py lines 1349-1456
    """
    template_path = Path("src/prompts/phase1.txt")
    assert template_path.exists(), \
        f"Template not found: {template_path}. Extract from interactive_llm_system_v3_hybrid_prompt.py lines 1349-1456"


def test_phase1_has_required_placeholders():
    """
    TDD RED: Verify template contains all required placeholders.
    
    Expected placeholders from source (line 1362):
    - {chapter_num}
    - {chapter_title}
    - {concepts}
    - {excerpt}
    - {concept_mapping}
    - {total_books}
    - {total_pages}
    - {books_metadata}
    
    References:
    - PYTHON_GUIDELINES: String formatting with {placeholder} syntax
    """
    template_path = Path("src/prompts/phase1.txt")
    template_content = template_path.read_text()
    
    required_placeholders = {
        '{chapter_num}',
        '{chapter_title}',
        '{concepts}',
        '{excerpt}',
        '{concept_mapping}',
        '{total_books}',
        '{total_pages}',
        '{books_metadata}'
    }
    
    for placeholder in required_placeholders:
        assert placeholder in template_content, \
            f"Missing required placeholder: {placeholder}"


def test_format_phase1_prompt_function_exists():
    """
    TDD RED: Verify format_phase1_prompt() function exists.
    
    Expected to FAIL until GREEN phase implements formatter in templates.py.
    
    References:
    - ARCHITECTURE_GUIDELINES: Separation of concerns
    """
    from src.prompts.templates import format_phase1_prompt
    assert callable(format_phase1_prompt)


def test_format_phase1_prompt_signature():
    """
    TDD RED: Verify function signature matches requirements.
    
    Expected parameters (from _build_phase1_prompt line 1350):
    - chapter_num: int
    - chapter_title: str
    - concepts: List[str]
    - excerpt: str
    - metadata_package: Dict[str, Any]
    
    References:
    - PYTHON_GUIDELINES: Type hints for function signatures
    """
    from src.prompts.templates import format_phase1_prompt
    import inspect
    
    sig = inspect.signature(format_phase1_prompt)
    params = list(sig.parameters.keys())
    
    expected_params = ['chapter_num', 'chapter_title', 'concepts', 'excerpt', 'metadata_package']
    assert params == expected_params, \
        f"Expected params {expected_params}, got {params}"


def test_format_phase1_prompt_returns_string():
    """
    TDD RED: Verify function returns formatted prompt string.
    
    Uses mock metadata package structure.
    
    References:
    - ARCHITECTURE_GUIDELINES: Test-driven development
    """
    from src.prompts.templates import format_phase1_prompt
    
    # Mock metadata package (matches structure from line 1372)
    mock_metadata = {
        'concept_mapping': {
            'decorators': [
                {'book': 'Fluent Python 2nd', 'page': 145, 'relevance': 0.85}
            ]
        },
        'total_books': 15,
        'total_pages': 12500,
        'books': [
            {
                'file_name': 'Fluent Python 2nd',
                'title': 'Fluent Python, 2nd Edition',
                'author': 'Luciano Ramalho',
                'pages': 1050
            }
        ]
    }
    
    result = format_phase1_prompt(
        chapter_num=7,
        chapter_title="Function Decorators",
        concepts=['decorators', 'closures', 'scope'],
        excerpt="This chapter explores Python decorators...",
        metadata_package=mock_metadata
    )
    
    assert isinstance(result, str)
    assert len(result) > 1000  # Should be substantial prompt
    assert "CHAPTER 7: Function Decorators" in result
    assert "decorators, closures, scope" in result


def test_phase1_preserves_json_schema():
    """
    TDD RED: Verify template preserves JSON response schema.
    
    The prompt requires specific JSON response format with:
    - validation_summary
    - gap_analysis
    - content_requests (array of objects)
    - analysis_strategy
    
    References:
    - Source: lines 1377-1389 define JSON schema
    """
    template_path = Path("src/prompts/phase1.txt")
    template_content = template_path.read_text()
    
    # Verify JSON schema is present
    assert "RESPOND IN JSON FORMAT" in template_content, \
        "Template must preserve JSON response requirement"
    assert '"validation_summary"' in template_content, \
        "Template must include validation_summary field"
    assert '"gap_analysis"' in template_content, \
        "Template must include gap_analysis field"
    assert '"content_requests"' in template_content, \
        "Template must include content_requests array"
    assert '"analysis_strategy"' in template_content, \
        "Template must include analysis_strategy field"


def test_phase1_preserves_book_taxonomy():
    """
    TDD RED: Verify template preserves complete book taxonomy structure.
    
    The prompt contains extensive taxonomy guidance (lines 1408-1442):
    - Architecture Spine Books (4 books)
    - Implementation Layer Books (4 books)
    - Engineering Practices Books (6 books)
    
    This is critical domain knowledge that must be preserved.
    
    References:
    - BOOK_TAXONOMY_MATRIX.md: Microservice Architecture taxonomy
    - Source: lines 1408-1430 define taxonomy tiers
    """
    template_path = Path("src/prompts/phase1.txt")
    template_content = template_path.read_text()
    
    # Verify taxonomy sections exist
    assert "APPLY BOOK TAXONOMY" in template_content, \
        "Template must preserve book taxonomy guidance"
    assert "ARCHITECTURE SPINE BOOKS" in template_content, \
        "Template must include Architecture tier"
    assert "IMPLEMENTATION LAYER BOOKS" in template_content, \
        "Template must include Implementation tier"
    assert "ENGINEERING PRACTICES BOOKS" in template_content, \
        "Template must include Engineering tier"
    
    # Verify specific books are referenced
    assert "Architecture Patterns with Python" in template_content
    assert "Fluent Python 2nd" in template_content
    assert "Python Distilled" in template_content
