"""
Test: Tab 5 (Guideline Generation) has NO LLM calls

Architecture Boundary Enforcement:
- Tab 6 = LLM ONLY
- Tabs 1-5 = Statistical/Template-based ONLY

This test ensures Tab 5 remains LLM-free per MASTER_IMPLEMENTATION_GUIDE.md.

Reference: Architecture Patterns with Python Ch. 3 (Abstraction & Coupling)
TDD Approach: RED → GREEN → REFACTOR
"""
import ast
import pytest
from pathlib import Path


class TestTab5NoLLMCalls:
    """Enforce architectural boundary: Tab 5 must not call LLM services"""
    
    @pytest.fixture
    def tab5_script_path(self):
        """Path to Tab 5 main script"""
        return Path("workflows/base_guideline_generation/scripts/chapter_generator_all_text.py")
    
    @pytest.fixture
    def tab5_source(self, tab5_script_path):
        """Source code of Tab 5 script"""
        return tab5_script_path.read_text()
    
    def test_no_llm_semantic_analysis_flag(self, tab5_source):
        """Test: USE_LLM_SEMANTIC_ANALYSIS flag must NOT exist"""
        assert "USE_LLM_SEMANTIC_ANALYSIS" not in tab5_source, (
            "USE_LLM_SEMANTIC_ANALYSIS flag found - Tab 5 must not have LLM functionality. "
            "LLM calls should only exist in Tab 6 (LLM Enhancement)."
        )
    
    def test_no_legacy_llm_imports(self, tab5_source):
        """Test: Legacy LLM helper functions must NOT be imported"""
        forbidden_imports = [
            "prompt_for_semantic_concepts",
            "prompt_for_cross_reference_validation",
            "prompt_for_cross_reference_summary"
        ]
        
        for forbidden in forbidden_imports:
            assert forbidden not in tab5_source, (
                f"Found forbidden LLM import '{forbidden}'. "
                f"Tab 5 must use statistical methods only (YAKE, Summa, TF-IDF). "
                f"LLM functionality belongs in Tab 6."
            )
    
    def test_no_llm_provider_calls(self, tab5_source):
        """Test: No LLM provider calls (Anthropic, OpenAI) in Tab 5"""
        # Parse AST to find function calls
        tree = ast.parse(tab5_source)
        
        # Look for any LLM-related function calls
        llm_call_patterns = [
            "_llm_provider",
            "call_llm_with_retry",
            "prompt_for_semantic",
            "prompt_for_cross_reference"
        ]
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                call_name = self._get_call_name(node)
                if call_name:
                    for pattern in llm_call_patterns:
                        assert pattern not in call_name, (
                            f"Found LLM call '{call_name}' in Tab 5. "
                            f"Architecture violation: LLM calls must only exist in Tab 6."
                        )
    
    def test_no_anthropic_imports(self, tab5_source):
        """Test: No Anthropic SDK imports in Tab 5"""
        forbidden = ["anthropic", "Anthropic", "AnthropicProvider"]
        
        for forbidden_import in forbidden:
            # Check it's not in actual import statements
            assert f"import {forbidden_import}" not in tab5_source, (
                f"Found Anthropic import in Tab 5 - architectural violation"
            )
            assert f"from anthropic" not in tab5_source, (
                f"Found Anthropic import in Tab 5 - architectural violation"
            )
    
    def test_statistical_methods_present(self, tab5_source):
        """Test: Tab 5 SHOULD use statistical methods (YAKE, Summa)"""
        # Verify legitimate statistical methods are present
        assert "keyword" in tab5_source.lower() or "concept" in tab5_source.lower(), (
            "Tab 5 should use keyword/concept extraction (statistical methods)"
        )
        
        # This is a positive assertion - we WANT these
        # Just confirming Tab 5 still has its core functionality
    
    def test_architecture_documentation_present(self, tab5_source):
        """Test: File documents it's part of statistical pipeline"""
        # Check docstring mentions statistical/template-based approach
        lines = tab5_source.split('\n')[:50]  # First 50 lines should have module docstring
        docstring = '\n'.join(lines)
        
        # Should NOT mention LLM enhancement in primary purpose
        assert "Exhaustive Chapter Generator" in docstring or "guideline" in docstring.lower(), (
            "Tab 5 module docstring should describe its statistical/template purpose"
        )
    
    def _get_call_name(self, node: ast.Call) -> str:
        """Extract function/method call name from AST node"""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        elif isinstance(node.func, ast.Call):
            return self._get_call_name(node.func)
        return ""


class TestArchitecturalBoundaryDocumentation:
    """Verify architecture boundaries are documented"""
    
    def test_master_implementation_guide_defines_boundary(self):
        """Test: MASTER_IMPLEMENTATION_GUIDE.md documents Tab 6 = LLM only"""
        guide_path = Path("MASTER_IMPLEMENTATION_GUIDE.md")
        
        if not guide_path.exists():
            pytest.skip("MASTER_IMPLEMENTATION_GUIDE.md not found")
        
        content = guide_path.read_text()
        
        # Should document that Tab 6 is THE LLM workflow
        assert "Tab 6" in content, "Guide should document 6-tab architecture"
        assert "LLM" in content or "llm" in content, "Guide should mention LLM usage"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
