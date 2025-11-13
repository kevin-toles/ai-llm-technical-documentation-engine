"""
Test suite for comprehensive_phase1 prompt template extraction.

TDD RED Phase: Write failing tests BEFORE extracting the template.

References:
- REFACTORING_PLAN.md Section II.2.1: Extract prompts from lines 811-1210
- Sprint 2.9: TDD RED - Phase1 Template Tests
"""



def test_comprehensive_phase1_template_file_exists():
    """
    TDD RED: Verify comprehensive_phase1.txt exists.
    
    Expected to FAIL: FileNotFoundError (file doesn't exist yet)
    
    References:
    - REFACTORING_PLAN.md: "Extract prompts to src/prompts/*.txt"
    """
    from src.prompts.templates import load_template
    
    # This will fail - template not extracted yet
    template = load_template("comprehensive_phase1")
    assert isinstance(template, str)
    assert len(template) > 100  # Should be a substantial prompt


def test_comprehensive_phase1_has_required_placeholders():
    """
    TDD RED: Verify template has all required placeholders.
    
    Expected to FAIL: FileNotFoundError
    
    References:
    - Source code line 823-900: Uses chapter_num, chapter_title, 
      chapter_full_text, books_metadata
    """
    from src.prompts.templates import load_template
    
    template = load_template("comprehensive_phase1")
    
    # Required placeholders for str.format()
    required_placeholders = [
        '{chapter_num}',
        '{chapter_title}',
        '{chapter_text_length}',
        '{chapter_text_preview}',
        '{chapter_text_truncation}',
        '{books_count}',
        '{books_text}'
    ]
    
    for placeholder in required_placeholders:
        assert placeholder in template, f"Missing placeholder: {placeholder}"


def test_format_comprehensive_phase1_prompt_function_exists():
    """
    TDD RED: Verify format function exists in templates module.
    
    Expected to FAIL: AttributeError (function doesn't exist)
    
    References:
    - REFACTORING_PLAN.md: "Implement format_phase1_prompt()"
    """
    from src.prompts import templates
    
    assert hasattr(templates, 'format_comprehensive_phase1_prompt')
    assert callable(templates.format_comprehensive_phase1_prompt)


def test_format_comprehensive_phase1_prompt_signature():
    """
    TDD RED: Verify format function has correct signature.
    
    Expected to FAIL: AttributeError
    
    References:
    - Source line 811-818: Parameters are chapter_num, chapter_title,
      chapter_full_text, books_metadata
    """
    import inspect
    from src.prompts.templates import format_comprehensive_phase1_prompt
    
    sig = inspect.signature(format_comprehensive_phase1_prompt)
    params = list(sig.parameters.keys())
    
    expected_params = ['chapter_num', 'chapter_title', 'chapter_full_text', 'books_metadata']
    assert params == expected_params, f"Expected {expected_params}, got {params}"


def test_format_comprehensive_phase1_prompt_returns_string():
    """
    TDD GREEN: Verify format function returns formatted string.
    
    Uses proper book metadata structure matching actual system usage.
    
    References:
    - Source line 823: Returns f-string prompt
    - Book metadata must include: title, author, full_title, domain, concepts_covered
    """
    from src.prompts.templates import format_comprehensive_phase1_prompt
    
    # Sample data matching actual book metadata structure
    result = format_comprehensive_phase1_prompt(
        chapter_num=1,
        chapter_title="Test Chapter",
        chapter_full_text="This is test content for the chapter.",
        books_metadata=[
            {
                'title': 'Test Book',
                'author': 'Test Author',
                'full_title': 'Test Book: Complete Guide',
                'domain': 'testing',
                'concepts_covered': ['testing', 'validation', 'TDD'],
                'has_chapter_metadata': False,
                'chapters': []
            }
        ]
    )
    
    assert isinstance(result, str)
    assert 'CHAPTER 1: Test Chapter' in result
    assert len(result) > 500  # Should be a substantial prompt


def test_comprehensive_phase1_preserves_json_structure():
    """
    TDD RED: Verify template preserves JSON response format.
    
    Expected to FAIL: FileNotFoundError
    
    References:
    - Source line 865-878: Requires JSON output with specific schema
    """
    from src.prompts.templates import load_template
    
    template = load_template("comprehensive_phase1")
    
    # JSON structure must be preserved
    assert '"concepts_extracted"' in template
    assert '"themes_identified"' in template
    assert '"content_requests"' in template
    assert '"analysis_strategy"' in template
    assert '"book_name"' in template
    assert '"chapters_or_sections"' in template
    assert '"pages"' in template
    assert '"rationale"' in template
    assert '"priority"' in template
