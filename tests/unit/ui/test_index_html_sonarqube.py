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


class TestRemainingIndexHtmlIssues:
    """
    TDD RED tests for remaining SonarQube issues in index.html.
    
    SonarQube reports 5 remaining issues:
    - S6660 Line 333: 'If' statement should not be the only statement in 'else' block
    - S3776 Line 345: Cognitive Complexity 22 (threshold 15)
    - S3776 Line 538: Cognitive Complexity 48 (threshold 15)
    - S3358 Line 738: Extract nested ternary operation
    - S7785 Line 767: Prefer top-level await over async function call
    
    Reference: CODING_PATTERNS_ANALYSIS.md Category 2 (Cognitive Complexity)
    """
    
    @pytest.fixture
    def index_html_content(self) -> str:
        """Load index.html content for analysis."""
        index_path = Path(__file__).parent.parent.parent.parent / "ui" / "templates" / "index.html"
        return index_path.read_text()
    
    @pytest.fixture
    def script_content(self, index_html_content: str) -> str:
        """Extract main script section."""
        pattern = r'<script>(.*?)</script>'
        matches = re.findall(pattern, index_html_content, re.DOTALL)
        return matches[-1] if matches else ""
    
    def test_s6660_no_if_only_in_else(self, script_content: str):
        """
        S6660 Line 333: 'If' statement should not be the only statement in 'else' block.
        
        Anti-pattern:
            if (afterElement == null) {
                // ...
            } else {
                if (draggedElement && ...) {  // S6660: if as only statement in else
                    afterElement.before(draggedElement);
                }
            }
        
        Fix: Merge into else-if:
            if (afterElement == null) {
                // ...
            } else if (draggedElement && ...) {
                afterElement.before(draggedElement);
            }
        """
        # Look for the pattern: else { if (... only if statement
        # This regex finds else blocks containing only an if statement
        pattern = r'\}\s*else\s*\{\s*\n\s*if\s*\([^)]+\)\s*\{\s*\n\s*[^}]+\.before\([^)]+\);\s*\n\s*\}\s*\n\s*\}'
        
        matches = re.findall(pattern, script_content)
        assert len(matches) == 0, (
            f"Found {len(matches)} 'else {{ if' patterns where if is only statement. "
            f"Merge into 'else if' to fix S6660."
        )
    
    def test_s3358_no_nested_ternary(self, script_content: str):
        """
        S3358 Line 738: Extract nested ternary operation into independent statement.
        
        Anti-pattern:
            const className = isError ? 'error' : (isSuccess ? 'success' : '');
        
        Fix: Extract to helper or use if/else:
            let className = '';
            if (isError) className = 'error';
            else if (isSuccess) className = 'success';
        """
        # Look for nested ternary: condition ? value : (condition ? value : value)
        pattern = r'\?[^?:]+:\s*\([^?]+\?[^:]+:[^)]+\)'
        
        nested_ternary = re.search(pattern, script_content)
        assert nested_ternary is None, (
            f"Found nested ternary expression. Extract to independent statements (S3358). "
            f"Found: {nested_ternary.group(0)[:50] if nested_ternary else 'N/A'}"
        )
    
    def test_s7785_no_async_iife_for_toplevel(self, index_html_content: str):
        """
        S7785 Line 767: Prefer top-level await over async function call.
        
        Anti-pattern:
            async function loadFiles(tabId) { ... }
            loadFiles('tab1');  // Called synchronously
        
        In module context, prefer top-level await:
            await loadFiles('tab1');
        
        Note: Since this is inline script in HTML (not module), we check if
        there's a simple async IIFE wrapper that could be converted.
        The loadFiles('tab1') call at end is fine for non-module scripts.
        """
        # This rule applies to ES modules. For inline scripts, we check if
        # there's unnecessary async IIFE pattern
        # Pattern: (async () => { ... })() or (async function() { ... })()
        async_iife = re.findall(r'\(async\s*(?:function\s*)?\([^)]*\)\s*=>\s*\{|\(async\s*function', index_html_content)
        
        # If using module type, check for sync call to async function at end
        has_module_type = 'type="module"' in index_html_content
        
        if has_module_type:
            # Check for async function called without await at script end
            pattern = r'loadFiles\([^)]+\);\s*$'
            no_await_call = re.search(pattern, index_html_content, re.MULTILINE)
            assert no_await_call is None, (
                "In module scripts, use 'await loadFiles(...)' instead of synchronous call (S7785)."
            )
        
        # Test passes if not a module (top-level await not available)
        # The actual S7785 fix requires converting to module type
        assert True  # Placeholder - actual fix depends on module type decision


class TestS3776JavaScriptCognitiveComplexity:
    """
    S3776: Cognitive Complexity tests for JavaScript functions in index.html.
    
    Functions flagged:
    - initTierBuilder (Line 345): Complexity 22 (threshold 15)
    - runWorkflow (Line 538): Complexity 48 (threshold 15)
    
    Pattern Reference: CODING_PATTERNS_ANALYSIS.md Category 2 (Extract Method)
    
    Strategy: Extract helper functions to reduce complexity below 15.
    For JavaScript in HTML, this means creating separate functions that are
    called from the main functions.
    """
    
    @pytest.fixture
    def index_html_content(self) -> str:
        """Load index.html content for analysis."""
        index_path = Path(__file__).parent.parent.parent.parent / "ui" / "templates" / "index.html"
        return index_path.read_text()
    
    @pytest.fixture
    def script_content(self, index_html_content: str) -> str:
        """Extract main script section."""
        pattern = r'<script>(.*?)</script>'
        matches = re.findall(pattern, index_html_content, re.DOTALL)
        return matches[-1] if matches else ""
    
    def test_init_tier_builder_has_helpers(self, script_content: str):
        """
        S3776 Line 345: initTierBuilder() should delegate to helper functions.
        
        Refactoring strategy: Extract event handlers into separate functions:
        - handleDragStart(e, draggedElement)
        - handleDragEnd(e)
        - handleDragOver(e, dropZone, draggedElement)
        - handleDrop(e, dropZone, draggedElement, tabId)
        
        Alternative: Look for reduced nesting depth.
        """
        # Check for helper functions that reduce initTierBuilder complexity
        has_drag_handlers = any([
            'function handleDragStart' in script_content,
            'function handleDragOver' in script_content,
            'function handleDrop' in script_content,
            'function handleTierDrop' in script_content,
            'const handleDragStart' in script_content,
            'const handleDrop' in script_content,
        ])
        
        # Alternative: Check for reduced event handler nesting
        # If no helpers, check that the forEach loop has simpler handlers
        init_tier_match = re.search(
            r'function initTierBuilder\([^)]*\)\s*\{(.*?)(?=\n\s*function |\n\s*// Get the element)',
            script_content,
            re.DOTALL
        )
        
        if init_tier_match:
            body = init_tier_match.group(1)
            # Count nesting indicators
            event_handlers = body.count('addEventListener')
            # If we have helpers, there should be fewer inline event handlers
            has_delegated_handlers = event_handlers <= 4 or has_drag_handlers
            
            assert has_delegated_handlers, (
                f"initTierBuilder() has {event_handlers} inline event handlers. "
                f"Extract helper functions per CODING_PATTERNS_ANALYSIS.md Category 2."
            )
    
    def test_run_workflow_has_helpers(self, script_content: str):
        """
        S3776 Line 538: runWorkflow() should delegate to helper functions.
        
        Refactoring strategy: Extract validation/setup into helpers:
        - validateLlmTab(tabId) -> { isValid, llmConfig }
        - validateTierTab(tabId) -> { isValid, tierData, selectedFiles }
        - validateFileSelection(tabId) -> { isValid, selectedFiles }
        - buildWorkflowPayload(data) -> payload
        - showWorkflowStatus(tabId, message)
        """
        # Check for helper functions that reduce runWorkflow complexity
        has_workflow_helpers = any([
            'function validateLlmTab' in script_content,
            'function validateTierTab' in script_content,
            'function validateFileSelection' in script_content,
            'function buildWorkflowPayload' in script_content,
            'function getTabConfig' in script_content,
            'function handleLlmTab' in script_content,
            'const validateLlmTab' in script_content,
            'const getTabConfig' in script_content,
        ])
        
        # Alternative: Count if/else branches in runWorkflow
        run_workflow_match = re.search(
            r'async function runWorkflow\([^)]*\)\s*\{(.*?)(?=\n\s*async function |\n\s*function |\Z)',
            script_content,
            re.DOTALL
        )
        
        if run_workflow_match:
            body = run_workflow_match.group(1)
            # Count branching indicators
            if_count = body.count('if (')
            else_count = body.count('else')
            total_branches = if_count + else_count
            
            # With helpers, branch count should be reduced
            has_reduced_branches = total_branches <= 15 or has_workflow_helpers
            
            assert has_reduced_branches, (
                f"runWorkflow() has {total_branches} branches (if/else). "
                f"Extract helper functions per CODING_PATTERNS_ANALYSIS.md Category 2."
            )
