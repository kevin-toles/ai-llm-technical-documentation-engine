"""
TDD RED PHASE: Sprint 2.12 - Extract comprehensive_phase2 prompt template.

References:
- REFACTORING_PLAN.md: Sprint 2 Day 1-2 (Large method extractions)
- ARCHITECTURE_GUIDELINES: Separation of concerns, template patterns

These tests MUST FAIL initially (TDD RED), then pass after extraction (TDD GREEN).
"""
from pathlib import Path



def test_comprehensive_phase2_template_file_exists():
    """
    TDD RED: Verify comprehensive_phase2.txt template file exists.
    
    Expected to FAIL until GREEN phase creates the template file.
    """
    template_path = Path("src/prompts/comprehensive_phase2.txt")
    assert template_path.exists(), \
        f"Template not found: {template_path}. Extract from interactive_llm_system_v3_hybrid_prompt.py lines ~1150-1228"


def test_comprehensive_phase2_has_required_placeholders():
    """
    TDD RED: Verify template contains all required placeholders.
    
    Expected placeholders from source (line 1211):
    - {chapter_num}
    - {chapter_title}
    - {metadata_response_validation_summary}
    - {metadata_response_analysis_strategy}
    - {content_package_count}
    - {content_text}
    """
    template_path = Path("src/prompts/comprehensive_phase2.txt")
    template_content = template_path.read_text()
    
    required_placeholders = {
        '{chapter_num}',
        '{chapter_title}',
        '{metadata_response_validation_summary}',
        '{metadata_response_analysis_strategy}',
        '{content_package_count}',
        '{content_text}'
    }
    
    for placeholder in required_placeholders:
        assert placeholder in template_content, \
            f"Missing required placeholder: {placeholder}"


def test_format_comprehensive_phase2_prompt_function_exists():
    """
    TDD RED: Verify format_comprehensive_phase2_prompt() function exists.
    
    Expected to FAIL until GREEN phase implements formatter in templates.py.
    """
    from workflows.shared.prompts.templates import format_comprehensive_phase2_prompt
    assert callable(format_comprehensive_phase2_prompt)


def test_format_comprehensive_phase2_prompt_signature():
    """
    TDD RED: Verify function signature matches requirements.
    
    Expected parameters (from _build_comprehensive_phase2_prompt):
    - chapter_num: int
    - chapter_title: str
    - metadata_response: MetadataExtractionResponse (has validation_summary, analysis_strategy)
    - content_package: Dict[str, Any]
    """
    from workflows.shared.prompts.templates import format_comprehensive_phase2_prompt
    import inspect
    
    sig = inspect.signature(format_comprehensive_phase2_prompt)
    params = list(sig.parameters.keys())
    
    expected_params = ['chapter_num', 'chapter_title', 'metadata_response', 'content_package']
    assert params == expected_params, \
        f"Expected params {expected_params}, got {params}"


def test_format_comprehensive_phase2_prompt_returns_string():
    """
    TDD RED: Verify function returns formatted prompt string.
    
    Uses mock metadata response and content package.
    """
    from workflows.shared.prompts.templates import format_comprehensive_phase2_prompt
    from typing import NamedTuple
    
    # Mock metadata response (has validation_summary, analysis_strategy)
    class MockMetadataResponse(NamedTuple):
        validation_summary: str
        analysis_strategy: str
    
    mock_metadata = MockMetadataResponse(
        validation_summary="Concepts: decorators, context managers",
        analysis_strategy="Compare architectural patterns with practical implementations"
    )
    
    # Mock content package
    mock_content = {
        "Fluent Python": [
            {
                'is_full_chapter': True,
                'chapter': 5,
                'title': 'Decorators and Closures',
                'author': 'Luciano Ramalho',
                'book_title': 'Fluent Python, 2nd Edition',
                'pages': '145-167',
                'content': 'Decorators are callables that take another callable as argument...'
            }
        ]
    }
    
    result = format_comprehensive_phase2_prompt(
        chapter_num=7,
        chapter_title="Function Decorators",
        metadata_response=mock_metadata,
        content_package=mock_content
    )
    
    assert isinstance(result, str)
    assert len(result) > 500  # Should be substantial prompt
    assert "CHAPTER 7: Function Decorators" in result
    assert "Concepts: decorators, context managers" in result


def test_comprehensive_phase2_preserves_citation_format():
    """
    TDD RED: Verify template preserves Chicago-style citation format.
    
    The prompt requires specific citation format:
    - **CHICAGO FOOTNOTE FORMAT**: Author(s), *Book Title*, Chapter/Section, page numbers.
    - Example: "Ramalho, Luciano, *Fluent Python, 2nd Edition*, Chapter 5, 145-167."
    """
    template_path = Path("src/prompts/comprehensive_phase2.txt")
    template_content = template_path.read_text()
    
    # Verify citation requirements are present
    assert "CHICAGO FOOTNOTE FORMAT" in template_content or "Chicago-style footnotes" in template_content, \
        "Template must preserve Chicago citation format requirements"
    assert "Author(s), *Book Title*" in template_content, \
        "Template must include citation format example"
