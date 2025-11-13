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
from typing import Final

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
