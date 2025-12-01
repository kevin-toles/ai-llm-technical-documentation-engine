"""
TDD RED PHASE: Sprint 2.12 - Extract comprehensive_phase2 prompt template.

References:
- REFACTORING_PLAN.md: Sprint 2 Day 1-2 (Large method extractions)
- ARCHITECTURE_GUIDELINES: Separation of concerns, template patterns

These tests MUST FAIL initially (TDD RED), then pass after extraction (TDD GREEN).
"""
from pathlib import Path


# Correct path to templates in workflows/shared/prompts/
PROMPTS_DIR = Path(__file__).parent.parent.parent / "workflows" / "shared" / "prompts"


def test_comprehensive_phase2_template_file_exists():
    """
    TDD GREEN: Verify comprehensive_phase2.txt template file exists.
    """
    template_path = PROMPTS_DIR / "comprehensive_phase2.txt"
    assert template_path.exists(), \
        f"Template not found: {template_path}"


def test_comprehensive_phase2_system_prompt_exists():
    """
    TDD GREEN: Verify comprehensive_phase2_system.txt exists (system/user split).
    """
    system_path = PROMPTS_DIR / "comprehensive_phase2_system.txt"
    assert system_path.exists(), \
        f"System prompt not found: {system_path}"


def test_comprehensive_phase2_has_required_placeholders():
    """
    TDD GREEN: Verify template contains all required placeholders.
    
    Expected placeholders:
    - {source_book_name}
    - {chapter_num}
    - {chapter_title}
    - {metadata_response_validation_summary}
    - {metadata_response_analysis_strategy}
    - {content_package_count}
    - {content_text}
    - {taxonomy_text}
    """
    template_path = PROMPTS_DIR / "comprehensive_phase2.txt"
    template_content = template_path.read_text()
    
    required_placeholders = {
        '{source_book_name}',
        '{chapter_num}',
        '{chapter_title}',
        '{metadata_response_validation_summary}',
        '{metadata_response_analysis_strategy}',
        '{content_package_count}',
        '{content_text}',
        '{taxonomy_text}'
    }
    
    for placeholder in required_placeholders:
        assert placeholder in template_content, \
            f"Missing required placeholder: {placeholder}"


def test_format_comprehensive_phase2_prompt_function_exists():
    """
    TDD GREEN: Verify format_comprehensive_phase2_prompt() function exists.
    """
    from workflows.shared.prompts.templates import format_comprehensive_phase2_prompt
    assert callable(format_comprehensive_phase2_prompt)


def test_format_comprehensive_phase2_prompt_signature():
    """
    TDD GREEN: Verify function signature matches requirements.
    
    Expected parameters:
    - chapter_num: int
    - chapter_title: str
    - metadata_response: object with validation_summary, analysis_strategy
    - content_package: Dict[str, Any]
    - source_book_name: str (optional, default "Unknown Book")
    - taxonomy_data: Optional[Dict] (optional)
    """
    from workflows.shared.prompts.templates import format_comprehensive_phase2_prompt
    import inspect
    
    sig = inspect.signature(format_comprehensive_phase2_prompt)
    params = list(sig.parameters.keys())
    
    # Required params first, then optional
    expected_params = ['chapter_num', 'chapter_title', 'metadata_response', 
                       'content_package', 'source_book_name', 'taxonomy_data']
    assert params == expected_params, \
        f"Expected params {expected_params}, got {params}"


def test_format_comprehensive_phase2_prompt_returns_tuple():
    """
    TDD GREEN: Verify function returns (system_prompt, user_prompt) tuple.
    
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
    
    # Should return tuple of (system_prompt, user_prompt)
    assert isinstance(result, tuple)
    assert len(result) == 2
    system_prompt, user_prompt = result
    
    assert isinstance(system_prompt, str)
    assert isinstance(user_prompt, str)
    assert len(user_prompt) > 500  # Should be substantial prompt
    assert "CHAPTER 7: Function Decorators" in user_prompt
    assert "Concepts: decorators, context managers" in user_prompt
    # System prompt should have the role identity
    assert "scholarly documentation analyst" in system_prompt


def test_comprehensive_phase2_preserves_citation_format():
    """
    TDD GREEN: Verify template preserves Chicago-style citation requirements.
    """
    template_path = PROMPTS_DIR / "comprehensive_phase2.txt"
    template_content = template_path.read_text()
    
    # Verify citation requirements are present (uses 17th edition)
    assert "Chicago Manual of Style" in template_content or "Chicago-style" in template_content, \
        "Template must reference Chicago citation format"


def test_system_prompt_contains_role_identity():
    """
    TDD GREEN: Verify system prompt contains role/identity context.
    """
    system_path = PROMPTS_DIR / "comprehensive_phase2_system.txt"
    content = system_path.read_text()
    
    # Should have role definition
    assert "scholarly documentation analyst" in content.lower(), \
        "System prompt should define analyst role"
    
    # Should have output constraint
    assert "annotation" in content.lower(), \
        "System prompt should mention annotation output"


def test_user_prompt_starts_with_task():
    """
    TDD GREEN: Verify user prompt starts with task, not role definition.
    """
    template_path = PROMPTS_DIR / "comprehensive_phase2.txt"
    content = template_path.read_text()
    
    # Should NOT start with "You are..."
    first_line = content.strip().split('\n')[0]
    assert not first_line.startswith("You are"), \
        "User prompt should start with task, not role (role is in system prompt)"
    
    # Should start with task instruction
    assert "Generate" in first_line or "annotation" in first_line.lower(), \
        "User prompt should start with task instruction"
