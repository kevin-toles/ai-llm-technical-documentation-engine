"""
TDD Tests for SonarQube Issue Fixes - run_comprehensive_evaluation.py

This test file follows the RED → GREEN → REFACTOR cycle as defined in CODING_PATTERNS_ANALYSIS.md.

Issues addressed:
- S1192: Duplicated literal "NOT SET" (3 times)
- S3457: f-string without replacement fields

References:
- CODING_PATTERNS_ANALYSIS.md: Category S1192 - Extract to module-level constants
- CODING_PATTERNS_ANALYSIS.md: Category S3457 - Remove f-string prefix
"""

import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path
import importlib.util

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def load_module():
    """Load run_comprehensive_evaluation module from scripts directory."""
    spec = importlib.util.spec_from_file_location(
        "run_comprehensive_evaluation",
        PROJECT_ROOT / "scripts" / "run_comprehensive_evaluation.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestNotSetConstant:
    """Tests for S1192 fix - duplicated literal 'NOT SET' should be a constant."""

    def test_not_set_constant_exists(self) -> None:
        """NOT_SET constant should be defined at module level."""
        module = load_module()
        
        assert hasattr(module, 'NOT_SET'), \
            "Module should define NOT_SET constant for S1192 compliance"

    def test_not_set_constant_value(self) -> None:
        """NOT_SET constant should have correct value."""
        module = load_module()
        
        assert module.NOT_SET == "NOT SET", \
            "NOT_SET constant should equal 'NOT SET'"

    def test_verify_prerequisites_uses_constant(self) -> None:
        """verify_prerequisites should use NOT_SET constant instead of literal."""
        module = load_module()
        
        # Mock os.environ to return empty strings for API keys
        with patch.dict('os.environ', {}, clear=True):
            with patch.object(Path, 'exists', return_value=False):
                status = module.verify_prerequisites()
        
        # All API key values should be the NOT_SET constant
        for key in ["DEEPSEEK_API_KEY", "GEMINI_API_KEY", "ANTHROPIC_API_KEY", "OPENAI_API_KEY"]:
            assert status["api_keys"][key] == module.NOT_SET, \
                f"API key {key} should use NOT_SET constant"


class TestFStringWithoutPlaceholder:
    """Tests for S3457 fix - f-string without replacement fields."""

    def test_no_empty_fstring_in_dry_run(self) -> None:
        """run_dry_run should not use f-strings without placeholders."""
        module = load_module()
        import inspect
        
        source = inspect.getsource(module.run_dry_run)
        
        # Parse the source to check for f-strings
        # The problematic line was: print(f"  ✅ All 4 taxonomy variants exist")
        # This should be changed to: print("  ✅ All 4 taxonomy variants exist")
        
        # Check that the specific problematic pattern is not present
        assert 'f"  ✅ All 4 taxonomy variants exist"' not in source, \
            "Should not use f-string without replacement fields (S3457)"


class TestRunDryRunComplexity:
    """Tests for cognitive complexity reduction in run_dry_run."""

    def test_helper_functions_exist(self) -> None:
        """Helper functions should be extracted to reduce complexity."""
        module = load_module()
        
        # These helpers should exist after refactoring
        expected_helpers = [
            '_print_profiles_status',
            '_print_source_metadata_status', 
            '_print_taxonomies_status',
            '_print_api_keys_status',
        ]
        
        for helper in expected_helpers:
            assert hasattr(module, helper), \
                f"Helper function {helper} should exist to reduce run_dry_run complexity"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
