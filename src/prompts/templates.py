"""
Template loader for LLM prompts.

TDD GREEN Phase: Minimal implementation to pass tests.

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


def load_template(name: str) -> str:
    """
    Load a prompt template from file.
    
    Implements EAFP pattern from PYTHON_GUIDELINES:
    "If read_data() is given a bad filename, there is no sensible way to recover...
    It's better to let the operation fail and report an exception back to the caller."
    
    Args:
        name: Template name (without .txt extension)
        
    Returns:
        Template content as string
        
    Raises:
        FileNotFoundError: If template file doesn't exist
        IOError: If file cannot be read
        
    References:
        - PYTHON_GUIDELINES: "pathlib.Path for cross-platform file operations"
        - PYTHON_GUIDELINES: "with open() for context management"
        - PYTHON_GUIDELINES: "Explicit UTF-8 encoding for cross-platform compatibility"
    """
    template_path = Path(__file__).parent / f"{name}.txt"
    with template_path.open('r', encoding='utf-8') as f:
        return f.read()
