"""
Test suite for prompt template loading functionality.

TDD RED Phase: These tests are written BEFORE implementation exists.
All tests should FAIL initially (ModuleNotFoundError or FileNotFoundError).

References:
- REFACTORING_PLAN.md: Sprint 2 Day 1-2 (Template Extraction)
- PYTHON_GUIDELINES: EAFP error handling, context managers
- ARCHITECTURE_GUIDELINES: Dependency injection, separation of concerns
"""

import pytest


def test_load_template_module_importable():
    """
    TDD RED: Test that we can import the templates module.
    
    Expected to FAIL: ModuleNotFoundError (module doesn't exist yet)
    
    References:
    - REFACTORING_PLAN.md Section II.2.1: "Create src/prompts/templates.py"
    """
    from workflows.shared.prompts import templates
    assert hasattr(templates, 'load_template')


def test_load_template_success():
    """
    TDD RED: Test successful template loading.
    
    Expected to FAIL: Either ModuleNotFoundError or FileNotFoundError
    
    References:
    - PYTHON_GUIDELINES: "with open() for context management"
    - PYTHON_GUIDELINES: "pathlib.Path for cross-platform paths"
    """
    from workflows.shared.prompts.templates import load_template
    
    # This will fail - template doesn't exist yet
    template_content = load_template("test_template")
    assert isinstance(template_content, str)
    assert len(template_content) > 0


def test_load_template_file_not_found():
    """
    TDD RED: Test that missing template raises FileNotFoundError.
    
    Expected to FAIL: ModuleNotFoundError (module doesn't exist)
    
    References:
    - PYTHON_GUIDELINES: "EAFP - let exceptions propagate"
    - Quote: "If read_data() is given a bad filename, there is no sensible 
      way to recover... It's better to let the operation fail and report 
      an exception back to the caller."
    """
    from workflows.shared.prompts.templates import load_template
    
    with pytest.raises(FileNotFoundError):
        load_template("nonexistent_template")


def test_load_template_utf8_encoding():
    """
    TDD RED: Test that templates are loaded with UTF-8 encoding.
    
    Expected to FAIL: ModuleNotFoundError
    
    References:
    - PYTHON_GUIDELINES: "Explicit encoding for cross-platform compatibility"
    """
    from workflows.shared.prompts.templates import load_template
    
    # Will test with actual template later
    # For now, just verify function exists and accepts name parameter
    assert callable(load_template)


def test_load_template_returns_string():
    """
    TDD RED: Test that load_template returns a string.
    
    Expected to FAIL: ModuleNotFoundError
    
    References:
    - REFACTORING_PLAN.md: "Extract prompts to .txt files"
    """
    from workflows.shared.prompts.templates import load_template
    
    result = load_template("test_template")
    assert isinstance(result, str)


def test_template_path_resolution():
    """
    TDD RED: Test that template path is resolved correctly.
    
    Expected to FAIL: ModuleNotFoundError
    
    References:
    - PYTHON_GUIDELINES: "pathlib.Path for cross-platform file operations"
    - Pattern: Path(__file__).parent / "template.txt"
    """
    from workflows.shared.prompts.templates import load_template
    
    # Template should be in src/prompts/ directory
    # This test verifies path resolution works correctly
    template = load_template("test_template")
    assert "test template" in template.lower()


def test_load_template_path_traversal_security():
    """
    TDD REFACTOR: Test that path traversal attacks are prevented.
    
    Security check added during REFACTOR phase.
    
    References:
    - ARCHITECTURE_GUIDELINES: Security best practices
    """
    from workflows.shared.prompts.templates import load_template
    
    with pytest.raises(ValueError, match="path separators"):
        load_template("../../../etc/passwd")
    
    with pytest.raises(ValueError, match="path separators"):
        load_template("subdir/template")
