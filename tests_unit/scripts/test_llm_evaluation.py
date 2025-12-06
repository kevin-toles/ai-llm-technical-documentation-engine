"""
TDD Tests for SonarQube Issue Fixes - llm_evaluation.py

This test file follows the RED → GREEN → REFACTOR cycle as defined in CODING_PATTERNS_ANALYSIS.md.

Issues addressed:
- Unused function parameter "api_key" in _test_deepseek_connection (line 307)
- Unused function parameter "api_key" in _test_gemini_connection (line 331)

References:
- CODING_PATTERNS_ANALYSIS.md: Category - Unused Parameters
- Pattern: Use underscore prefix for intentionally unused parameters
"""

import pytest
import inspect
from pathlib import Path
import sys
import importlib.util

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def load_llm_evaluation_module():
    """Load llm_evaluation module from scripts directory."""
    spec = importlib.util.spec_from_file_location(
        "llm_evaluation",
        PROJECT_ROOT / "scripts" / "llm_evaluation.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestUnusedParameterFixes:
    """Tests for unused parameter fixes in llm_evaluation.py."""

    def test_deepseek_connection_uses_api_key_or_underscore(self) -> None:
        """_test_deepseek_connection should either use api_key or prefix with underscore."""
        llm_evaluation = load_llm_evaluation_module()
        
        # Get function signature
        sig = inspect.signature(llm_evaluation._test_deepseek_connection)
        params = list(sig.parameters.keys())
        
        # Either the parameter is used (check source) or prefixed with underscore
        source = inspect.getsource(llm_evaluation._test_deepseek_connection)
        
        # Check that parameter is either used or prefixed with underscore
        has_underscore_prefix = '_api_key' in params
        
        if 'api_key' in params:
            # If named api_key, it should be used in the function body
            api_key_count = source.count('api_key')
            assert api_key_count > 1, \
                "api_key parameter should be used or prefixed with underscore (SonarQube S1172)"
        else:
            # Underscore prefix is acceptable for intentionally unused params
            assert has_underscore_prefix, \
                "Function should have api_key or _api_key parameter"

    def test_gemini_connection_uses_api_key_or_underscore(self) -> None:
        """_test_gemini_connection should either use api_key or prefix with underscore."""
        llm_evaluation = load_llm_evaluation_module()
        
        # Get function signature
        sig = inspect.signature(llm_evaluation._test_gemini_connection)
        params = list(sig.parameters.keys())
        
        source = inspect.getsource(llm_evaluation._test_gemini_connection)
        
        # Check that parameter is either used or prefixed with underscore
        has_underscore_prefix = '_api_key' in params
        
        if 'api_key' in params:
            api_key_count = source.count('api_key')
            assert api_key_count > 1, \
                "api_key parameter should be used or prefixed with underscore (SonarQube S1172)"
        else:
            # Underscore prefix is acceptable for intentionally unused params
            assert has_underscore_prefix, \
                "Function should have api_key or _api_key parameter"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
