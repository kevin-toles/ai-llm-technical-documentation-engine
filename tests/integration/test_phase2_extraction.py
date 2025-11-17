"""
TDD RED PHASE: Sprint 2.14 - Extract phase2 prompt template (FINAL extraction).

Document Hierarchy Compliance:
- REFACTORING_PLAN.md: Sprint 2 Day 1-2 (Extract prompt templates)
- ARCHITECTURE_GUIDELINES: Separation of concerns, template patterns
- PYTHON_GUIDELINES: str.format() for template composition

These tests MUST FAIL initially (TDD RED), then pass after extraction (TDD GREEN).
"""
from pathlib import Path



def test_phase2_template_file_exists():
    """
    TDD RED: Verify phase2.txt template file exists.
    
    Expected to FAIL until GREEN phase creates the template file.
    
    References:
    - REFACTORING_PLAN.md: Sprint 2 template extraction (final prompt)
    - Source: interactive_llm_system_v3_hybrid_prompt.py lines 1389-1469
    """
    template_path = Path("src/prompts/phase2.txt")
    assert template_path.exists(), \
        f"Template not found: {template_path}. Extract from interactive_llm_system_v3_hybrid_prompt.py lines 1389-1469"


def test_phase2_has_required_placeholders():
    """
    TDD RED: Verify template contains all required placeholders.
    
    Expected placeholders from source (line 1411):
    - {chapter_num}
    - {chapter_title}
    - {concepts}
    - {excerpt}
    - {validation_summary}
    - {gap_analysis}
    - {analysis_strategy}
    - {content_package_count}
    - {content_text}
    
    References:
    - PYTHON_GUIDELINES: String formatting with {placeholder} syntax
    """
    template_path = Path("src/prompts/phase2.txt")
    template_content = template_path.read_text()
    
    required_placeholders = {
        '{chapter_num}',
        '{chapter_title}',
        '{concepts}',
        '{excerpt}',
        '{validation_summary}',
        '{gap_analysis}',
        '{analysis_strategy}',
        '{content_package_count}',
        '{content_text}'
    }
    
    for placeholder in required_placeholders:
        assert placeholder in template_content, \
            f"Missing required placeholder: {placeholder}"


def test_format_phase2_prompt_function_exists():
    """
    TDD RED: Verify format_phase2_prompt() function exists.
    
    Expected to FAIL until GREEN phase implements formatter in templates.py.
    
    References:
    - ARCHITECTURE_GUIDELINES: Separation of concerns
    """
    from shared.prompts.templates import format_phase2_prompt
    assert callable(format_phase2_prompt)


def test_format_phase2_prompt_signature():
    """
    TDD RED: Verify function signature matches requirements.
    
    Expected parameters (from _build_phase2_prompt line 1390):
    - chapter_num: int
    - chapter_title: str
    - concepts: List[str]
    - excerpt: str
    - metadata_response: LLMMetadataResponse (has validation_summary, gap_analysis, analysis_strategy)
    - content_package: Dict[str, List[Dict]]
    
    References:
    - PYTHON_GUIDELINES: Type hints for function signatures
    """
    from shared.prompts.templates import format_phase2_prompt
    import inspect
    
    sig = inspect.signature(format_phase2_prompt)
    params = list(sig.parameters.keys())
    
    expected_params = ['chapter_num', 'chapter_title', 'concepts', 'excerpt', 'metadata_response', 'content_package']
    assert params == expected_params, \
        f"Expected params {expected_params}, got {params}"


def test_format_phase2_prompt_returns_string():
    """
    TDD RED: Verify function returns formatted prompt string.
    
    Uses mock metadata response and content package.
    
    References:
    - ARCHITECTURE_GUIDELINES: Test-driven development
    """
    from shared.prompts.templates import format_phase2_prompt
    from typing import NamedTuple
    
    # Mock metadata response (has validation_summary, gap_analysis, analysis_strategy)
    class MockMetadataResponse(NamedTuple):
        validation_summary: str
        gap_analysis: str
        analysis_strategy: str
    
    mock_metadata = MockMetadataResponse(
        validation_summary="High relevance matches found for decorators in Fluent Python and Architecture Patterns",
        gap_analysis="Need coverage of closure mechanics and scope chain resolution",
        analysis_strategy="Request detailed decorator implementation pages plus architectural pattern descriptions"
    )
    
    # Mock content package
    mock_content = {
        "Fluent Python 2nd": [
            {
                'page': 145,
                'content': 'Decorators are callables that take another callable as argument and return a modified callable...'
            }
        ],
        "Architecture Patterns with Python": [
            {
                'page': 89,
                'content': 'The Decorator pattern allows behavior to be added to individual objects dynamically...'
            }
        ]
    }
    
    result = format_phase2_prompt(
        chapter_num=7,
        chapter_title="Function Decorators",
        concepts=['decorators', 'closures', 'scope'],
        excerpt="This chapter explores Python decorators and their applications...",
        metadata_response=mock_metadata,
        content_package=mock_content
    )
    
    assert isinstance(result, str)
    assert len(result) > 800  # Should be substantial prompt
    assert "CHAPTER 7: Function Decorators" in result
    assert "decorators, closures, scope" in result


def test_phase2_preserves_analysis_instructions():
    """
    TDD RED: Verify template preserves detailed analysis instructions.
    
    The prompt contains specific analytical framework (lines 1426-1461):
    1. VALIDATE EACH EXCERPT
    2. FOR GENUINE TECHNICAL CONTENT
    3. FOR NON-SUBSTANTIVE CONTENT
    4. ORGANIZE BY TIER
    
    This is critical methodology that must be preserved.
    
    References:
    - Source: lines 1426-1461 define analysis approach
    """
    template_path = Path("src/prompts/phase2.txt")
    template_content = template_path.read_text()
    
    # Verify analysis sections exist
    assert "ANALYSIS APPROACH" in template_content, \
        "Template must preserve analysis approach section"
    assert "VALIDATE EACH EXCERPT" in template_content, \
        "Template must include validation step"
    assert "FOR GENUINE TECHNICAL CONTENT" in template_content, \
        "Template must include genuine content handling"
    assert "FOR NON-SUBSTANTIVE CONTENT" in template_content, \
        "Template must include non-substantive content handling"
    assert "ORGANIZE BY TIER" in template_content, \
        "Template must include tier organization"


def test_phase2_preserves_strict_rules():
    """
    TDD RED: Verify template preserves strict output rules.
    
    The prompt contains critical constraints (lines 1463-1469):
    - BE SPECIFIC
    - DO NOT invent connections
    - DO NOT use generic filler
    - DO NOT exceed 10 sentences
    - OUTPUT ONLY the annotation text
    
    References:
    - Source: lines 1463-1469 define strict rules
    """
    template_path = Path("src/prompts/phase2.txt")
    template_content = template_path.read_text()
    
    # Verify strict rules section exists
    assert "STRICT RULES" in template_content, \
        "Template must preserve strict rules section"
    assert "BE SPECIFIC" in template_content, \
        "Template must include specificity requirement"
    assert "DO NOT invent connections" in template_content, \
        "Template must warn against invented connections"
    assert "DO NOT use generic filler" in template_content, \
        "Template must prohibit generic filler"
    assert "DO NOT exceed 10 sentences" in template_content or "10 sentences" in template_content, \
        "Template must include sentence limit"
