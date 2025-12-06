"""
SonarQube Code Quality Tests for ui/templates/index.html

TDD Tests for Batch 1 SonarQube Issues (JavaScript):
- S7764: Prefer `globalThis` over `window`
- S7768: Use `element.before()` instead of `insertBefore()`
- S1481: Remove unused variables
- S1854: Remove useless assignments

Reference: CODING_PATTERNS_ANALYSIS.md Categories 17-18 (NEW)
"""
import pytest
import re
from pathlib import Path


class TestSonarQubeJavaScriptPatterns:
    """
    Static analysis tests for JavaScript anti-patterns in index.html.
    
    These tests verify that SonarQube issues are fixed by checking
    the source code for anti-pattern occurrences.
    """
    
    @pytest.fixture
    def index_html_content(self) -> str:
        """Load index.html content for analysis."""
        index_path = Path(__file__).parent.parent.parent.parent / "ui" / "templates" / "index.html"
        return index_path.read_text()
    
    @pytest.fixture
    def script_sections(self, index_html_content: str) -> list[str]:
        """Extract all <script> sections from HTML."""
        pattern = r'<script[^>]*>(.*?)</script>'
        return re.findall(pattern, index_html_content, re.DOTALL)
    
    # ========== S7764: window -> globalThis ==========
    
    def test_no_window_llmproviders_access(self, index_html_content: str):
        """
        Issue 1-7 (S7764): Replace window.llmProviders with globalThis.llmProviders
        
        SonarQube: Prefer `globalThis` over `window`
        Lines: 148, 250, 274, 275, 276, 283, 255
        """
        # Count window.llmProviders occurrences (should be 0 after fix)
        window_llmproviders = re.findall(r'window\.llmProviders', index_html_content)
        assert len(window_llmproviders) == 0, (
            f"Found {len(window_llmproviders)} instances of 'window.llmProviders'. "
            f"Use 'globalThis.llmProviders' instead (SonarQube S7764)."
        )
    
    def test_no_window_tierstate_access(self, index_html_content: str):
        """
        Issue 1-7 (S7764): Replace window.tierState with globalThis.tierState
        
        SonarQube: Prefer `globalThis` over `window`
        Lines: 274, 362, 363, 370, 371, 374
        """
        window_tierstate = re.findall(r'window\.tierState', index_html_content)
        assert len(window_tierstate) == 0, (
            f"Found {len(window_tierstate)} instances of 'window.tierState'. "
            f"Use 'globalThis.tierState' instead (SonarQube S7764)."
        )
    
    def test_no_window_json_access(self, index_html_content: str):
        """
        Issue (S7764): Replace window.JSON with globalThis equivalent or direct JSON
        
        SonarQube: Prefer `globalThis` over `window`
        Lines: 590, 591
        """
        # Check for window.JSON patterns (but not structuredClone which is the fix for S7784)
        window_json = re.findall(r'window\.JSON', index_html_content)
        assert len(window_json) == 0, (
            f"Found {len(window_json)} instances of 'window.JSON'. "
            f"Use direct 'JSON' reference instead (SonarQube S7764)."
        )
    
    # ========== S1481/S1854: Unused Variables ==========
    
    def test_no_unused_containerid_variable(self, index_html_content: str):
        """
        Issues 2-3 (S1481/S1854): Remove unused containerId variable
        
        SonarQube: Remove the declaration of unused 'containerId' variable
        Line: 271
        """
        # Check for containerId declaration that's never used in meaningful operations
        # Pattern: const containerId = `...` where it's only assigned, never used
        containerid_declarations = re.findall(
            r'const\s+containerId\s*=\s*`[^`]+`',
            index_html_content
        )
        
        # If declared, verify it's actually used (not just assigned)
        for decl in containerid_declarations:
            # Check if containerId is used beyond declaration
            containerid_uses = re.findall(r'\bcontainerId\b', index_html_content)
            # Should only appear in declaration, not elsewhere
            assert len(containerid_uses) <= 1 or len(containerid_uses) == 0, (
                f"Variable 'containerId' is declared but not meaningfully used. "
                f"Remove the unused variable (SonarQube S1481/S1854)."
            )
    
    # ========== S7768: insertBefore -> element.before() ==========
    
    def test_no_insertbefore_pattern(self, index_html_content: str):
        """
        Issue 10 (S7768): Use element.before() instead of insertBefore()
        
        SonarQube: Prefer `emptyMsg.before(draggedElement)` over 
                  `dropZone.insertBefore(draggedElement, emptyMsg)`
        Lines: 328, 335
        """
        # Pattern: something.insertBefore(element, referenceNode)
        insertbefore_calls = re.findall(
            r'\.insertBefore\s*\([^)]+,\s*[^)]+\)',
            index_html_content
        )
        assert len(insertbefore_calls) == 0, (
            f"Found {len(insertbefore_calls)} instances of 'insertBefore()'. "
            f"Use 'referenceNode.before(element)' instead (SonarQube S7768)."
        )


class TestJavaScriptPatternCompliance:
    """
    Positive tests to verify correct patterns are used.
    """
    
    @pytest.fixture
    def index_html_content(self) -> str:
        """Load index.html content for analysis."""
        index_path = Path(__file__).parent.parent.parent.parent / "ui" / "templates" / "index.html"
        return index_path.read_text()
    
    def test_uses_globalthis_for_global_state(self, index_html_content: str):
        """Verify globalThis is used for global state objects."""
        # After fix, should see globalThis.tierState and globalThis.llmProviders
        globalthis_uses = re.findall(r'globalThis\.(tierState|llmProviders)', index_html_content)
        # Should have multiple occurrences after fix
        assert len(globalthis_uses) >= 1, (
            "Expected globalThis to be used for global state (tierState, llmProviders)"
        )
    
    def test_uses_element_before_method(self, index_html_content: str):
        """Verify element.before() method is used for DOM insertion."""
        # After fix, should see .before(draggedElement) pattern
        before_calls = re.findall(r'\.before\s*\(\s*draggedElement\s*\)', index_html_content)
        # Should have occurrences after fix (replacing insertBefore)
        assert len(before_calls) >= 1, (
            "Expected .before() method to be used for DOM insertion"
        )
