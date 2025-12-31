"""
SonarQube Code Quality Tests for Batch 3

TDD Tests for Issues 21-30:
- S7494 (Issue 21): Use set comprehension instead of set()
- S3358 (Issues 22-24): Extract nested ternary expressions
- S3457 (Issues 25-26, 28-30): Remove empty f-strings
- S1481 (Issue 27): Remove unused variable

Reference: CODING_PATTERNS_ANALYSIS.md Categories 14, 16
Reference: Comp_Static_Analysis_Report_20251203.md Issues 47-48, 51-52
"""
import pytest
import re
from pathlib import Path


class TestRunEnrichmentWithValidation:
    """
    Static analysis tests for scripts/run_enrichment_with_validation.py
    Issues 21-27
    """
    
    @pytest.fixture
    def file_content(self) -> str:
        """Load run_enrichment_with_validation.py content for analysis."""
        file_path = Path(__file__).parent.parent.parent.parent / "scripts" / "run_enrichment_with_validation.py"
        return file_path.read_text()
    
    def test_issue_21_set_comprehension(self, file_content: str):
        """
        Issue 21 (S7494 Line 182): Use set comprehension instead of set().
        
        Pre-fix: set(ch.get("topic_id") for ch in chapters_with_topic)
        Post-fix: {ch.get("topic_id") for ch in chapters_with_topic}
        """
        # Should NOT have set() constructor with generator
        assert 'set(ch.get("topic_id") for ch in' not in file_content, (
            "Use set comprehension {expr for x in iterable} instead of set(expr for x in iterable) (S7494)"
        )
        # Should have set comprehension instead
        assert '{ch.get("topic_id") for ch in' in file_content, (
            "Expected set comprehension pattern {ch.get('topic_id') for ch in ...}"
        )
    
    def test_issue_22_nested_ternary_line_330(self, file_content: str):
        """
        Issue 22 (S3358 Line 330): Extract nested ternary expression.
        
        Nested ternaries reduce readability. Extract to helper or if/else.
        """
        # Count nested ternary patterns (x if cond else (y if cond2 else z))
        # Look for pattern with two 'if' and two 'else' on similar context
        lines = file_content.split('\n')
        
        # Find line with topic_id_count comparison
        for i, line in enumerate(lines):
            if 'change=' in line and 'topic' in line.lower():
                # Should NOT have nested ternary (if...else...if...else pattern)
                nested_ternary = re.search(r'if.*else.*if.*else', line)
                assert nested_ternary is None, (
                    f"Line {i+1}: Extract nested ternary to variable or helper function (S3358)"
                )
    
    def test_issue_23_nested_ternary_line_340(self, file_content: str):
        """
        Issue 23 (S3358 Line 340): Extract nested ternary expression.
        """
        lines = file_content.split('\n')
        
        for i, line in enumerate(lines):
            if 'change=' in line and 'related' in line.lower():
                nested_ternary = re.search(r'if.*else.*if.*else', line)
                assert nested_ternary is None, (
                    f"Line {i+1}: Extract nested ternary to variable or helper function (S3358)"
                )
    
    def test_issue_24_nested_ternary_line_350(self, file_content: str):
        """
        Issue 24 (S3358 Line 350): Extract nested ternary expression.
        """
        lines = file_content.split('\n')
        
        for i, line in enumerate(lines):
            if 'change=' in line and 'keyword' in line.lower():
                nested_ternary = re.search(r'if.*else.*if.*else', line)
                assert nested_ternary is None, (
                    f"Line {i+1}: Extract nested ternary to variable or helper function (S3358)"
                )
    
    def test_issue_25_empty_fstring_line_443(self, file_content: str):
        """
        Issue 25 (S3457 Line ~443): Remove empty f-string.
        
        Pattern: print(f"...") without placeholders -> print("...")
        """
        # Search for print(f"  📊 Comparison with Backup") - no placeholders
        assert 'print(f"\\n  📊 Comparison with Backup")' not in file_content, (
            "Remove f-prefix from string without placeholders (S3457)"
        )
    
    def test_issue_26_empty_fstring_line_481(self, file_content: str):
        """
        Issue 26 (S3457 Line ~481): Remove empty f-string.
        """
        # Check for f-strings in the ENRICHMENT WITH VALIDATION header area
        # Should be regular strings, not f-strings
        assert 'print(f"🔬 ENRICHMENT WITH VALIDATION")' not in file_content, (
            "Remove f-prefix from string without placeholders (S3457)"
        )
    
    def test_issue_27_unused_backup_dir(self, file_content: str):
        """
        Issue 27 (S1481 Line 512): Remove unused backup_dir variable.
        
        Variable assigned but never used. Either remove or prefix with _.
        """
        # Should NOT have bare 'backup_dir =' assignment
        # Should either be removed or prefixed with _
        lines = file_content.split('\n')
        for i, line in enumerate(lines):
            if 'backup_dir = backup_current_outputs' in line:
                # Check if prefixed with underscore
                assert line.strip().startswith('_backup_dir') or 'backup_dir' not in line, (
                    f"Line {i+1}: Remove unused variable or prefix with _ (S1481)"
                )


class TestDryRunPipelineComparison:
    """
    Static analysis tests for scripts/dry_run_pipeline_comparison.py
    Issues 28-30
    """
    
    @pytest.fixture
    def file_content(self) -> str:
        """Load dry_run_pipeline_comparison.py content for analysis."""
        file_path = Path(__file__).parent.parent.parent.parent / "scripts" / "dry_run_pipeline_comparison.py"
        return file_path.read_text()
    
    def test_issue_28_empty_fstring_line_392(self, file_content: str):
        """
        Issue 28 (S3457 Line 392): Remove empty f-string.
        
        Pattern: print(f"\\n📄 TAB 1: PDF to JSON Extraction")
        """
        assert 'print(f"\\n📄 TAB 1: PDF to JSON Extraction")' not in file_content, (
            "Remove f-prefix from string without placeholders (S3457)"
        )
    
    def test_issue_29_empty_fstring_line_400(self, file_content: str):
        """
        Issue 29 (S3457 Line 400): Remove empty f-string.
        """
        # Check area around TAB 1 section - should not have empty f-strings
        # Match pattern that has no {} placeholders
        pattern = r'print\(f"[^{}"]*"\)'
        matches = re.findall(pattern, file_content)
        
        # Filter to only the ones in the comparison report area
        empty_fstrings_in_tab1 = [m for m in matches if 'TAB 1' in m or 'not found' in m]
        assert len(empty_fstrings_in_tab1) == 0, (
            f"Found {len(empty_fstrings_in_tab1)} empty f-strings in TAB 1 section (S3457)"
        )
    
    def test_issue_30_empty_fstring_line_404(self, file_content: str):
        """
        Issue 30 (S3457 Line 404): Remove empty f-string.
        """
        # Check for f"   ⚠️  JSON file not found" pattern
        assert 'print(f"   ⚠️  JSON file not found")' not in file_content, (
            "Remove f-prefix from string without placeholders (S3457)"
        )


class TestBatch3NoRegressions:
    """
    Verify fixes don't introduce regressions.
    """
    
    @pytest.fixture
    def enrichment_content(self) -> str:
        file_path = Path(__file__).parent.parent.parent.parent / "scripts" / "run_enrichment_with_validation.py"
        return file_path.read_text()
    
    @pytest.fixture
    def pipeline_content(self) -> str:
        file_path = Path(__file__).parent.parent.parent.parent / "scripts" / "dry_run_pipeline_comparison.py"
        return file_path.read_text()
    
    def test_enrichment_file_is_valid_python(self, enrichment_content: str):
        """Verify the file is still valid Python after fixes."""
        try:
            compile(enrichment_content, "run_enrichment_with_validation.py", "exec")
        except SyntaxError as e:
            pytest.fail(f"Syntax error after fixes: {e}")
    
    def test_pipeline_file_is_valid_python(self, pipeline_content: str):
        """Verify the file is still valid Python after fixes."""
        try:
            compile(pipeline_content, "dry_run_pipeline_comparison.py", "exec")
        except SyntaxError as e:
            pytest.fail(f"Syntax error after fixes: {e}")
    
    def test_enrichment_has_validation_functions(self, enrichment_content: str):
        """Verify key functions still exist."""
        assert 'def validate_enrichment' in enrichment_content
        assert 'def compare_enrichments' in enrichment_content
        assert 'def run_tab4_enrichment' in enrichment_content
    
    def test_pipeline_has_analysis_functions(self, pipeline_content: str):
        """Verify key functions still exist."""
        assert 'def print_comparison_report' in pipeline_content
        assert 'def analyze_' in pipeline_content


class TestS3776CognitiveComplexity:
    """
    TDD RED tests for S3776 Cognitive Complexity issues in Batch 1-3 files.
    
    SonarQube S3776: Refactor functions to reduce Cognitive Complexity.
    Target: Maximum complexity of 15 per function.
    
    Remaining issues:
    - run_enrichment_with_validation.py Line 478: main() complexity exceeds 15
    - dry_run_pipeline_comparison.py Line 313: function complexity exceeds 15
    - dry_run_pipeline_comparison.py Line 384: function complexity exceeds 15
    
    Reference: CODING_PATTERNS_ANALYSIS.md Category 2 (Cognitive Complexity)
    Pattern: Extract Method - break into helper functions with single responsibility
    """
    
    @pytest.fixture
    def enrichment_content(self) -> str:
        file_path = Path(__file__).parent.parent.parent.parent / "scripts" / "run_enrichment_with_validation.py"
        return file_path.read_text()
    
    @pytest.fixture
    def pipeline_content(self) -> str:
        file_path = Path(__file__).parent.parent.parent.parent / "scripts" / "dry_run_pipeline_comparison.py"
        return file_path.read_text()
    
    def _count_complexity_indicators(self, function_body: str) -> int:
        """
        Approximate cognitive complexity by counting complexity indicators.
        
        Complexity increases with:
        - if/elif/else statements (+1 each, +1 for nesting)
        - for/while loops (+1 each, +1 for nesting)
        - try/except blocks (+1)
        - and/or operators (+1)
        - break/continue (+1)
        - recursion (+1)
        - early returns after first (+1 each)
        
        Note: This is a simplified approximation, not exact SonarQube calculation.
        """
        complexity = 0
        nesting_level = 0
        lines = function_body.split('\n')
        
        for line in lines:
            stripped = line.strip()
            
            # Track nesting
            if stripped.startswith(('if ', 'elif ', 'for ', 'while ', 'try:', 'with ')):
                complexity += 1 + nesting_level
                nesting_level += 1
            elif stripped.startswith(('else:', 'except', 'finally:')):
                complexity += 1
            elif stripped.startswith('return ') and complexity > 0:
                complexity += 1  # Early return penalty
            
            # Logical operators
            complexity += stripped.count(' and ')
            complexity += stripped.count(' or ')
            
            # Control flow breaks
            if stripped in ('break', 'continue'):
                complexity += 1
            
            # Decrease nesting on dedent (simplified)
            if nesting_level > 0 and not line.startswith(' ' * (4 * nesting_level)):
                nesting_level = max(0, nesting_level - 1)
        
        return complexity
    
    def test_main_function_complexity_under_threshold(self, enrichment_content: str):
        """
        S3776 Line 478: main() function should have complexity <= 15.
        
        Current issue: Cognitive Complexity exceeds threshold.
        Fix: Extract helper functions for:
          - Argument parsing setup
          - Tab 4 execution and validation
          - Tab 5 execution and validation
          - Summary generation
          - Report saving
        """
        # Extract main function body (simplified - just check function exists and has helpers)
        # A properly refactored main() should delegate to helper functions
        
        # Count how many high-level operations are in main()
        # A well-structured main() should have low complexity with delegation
        main_match = re.search(r'def main\(\):(.*?)(?=\ndef |\nif __name__|\Z)', enrichment_content, re.DOTALL)
        
        assert main_match is not None, "main() function not found"
        main_body = main_match.group(1)
        
        # Check for refactoring pattern: main() should delegate to helpers
        # Look for helper function calls (functions starting with _ or specific names)
        helper_calls = [
            '_run_tab4_workflow',
            '_run_tab5_workflow', 
            '_print_summary',
            '_save_report',
            '_setup_environment'
        ]
        
        # At least some helper delegation should exist after refactoring
        delegation_found = any(helper in main_body for helper in helper_calls)
        
        # Alternative: check if main() has been kept simple
        # Approximate complexity check
        estimated_complexity = self._count_complexity_indicators(main_body)
        
        # The test passes if either:
        # 1. Helper functions are used (delegation pattern)
        # 2. OR complexity is under threshold
        assert delegation_found or estimated_complexity <= 15, (
            f"main() has estimated complexity of {estimated_complexity} (threshold: 15). "
            f"Extract helper functions per CODING_PATTERNS_ANALYSIS.md Category 2."
        )
    
    def test_pipeline_functions_refactored(self, pipeline_content: str):
        """
        S3776 Lines 313, 384: Functions should have complexity <= 15.
        
        Pattern: Look for evidence of refactoring - helper functions that
        reduce main function complexity.
        """
        # Check for helper function definitions (functions starting with _)
        helper_functions = re.findall(r'def (_[a-z_]+)\(', pipeline_content)
        
        # After refactoring, should have helper functions
        # A well-structured file should have private helpers
        has_helper_pattern = len(helper_functions) >= 2
        
        # Alternative: count complexity in specific functions
        # Look for print_comparison_report and check its complexity
        report_match = re.search(
            r'def print_comparison_report\([^)]*\):(.*?)(?=\ndef |\nclass |\Z)', 
            pipeline_content, 
            re.DOTALL
        )
        
        if report_match:
            report_body = report_match.group(1)
            estimated_complexity = self._count_complexity_indicators(report_body)
            
            assert has_helper_pattern or estimated_complexity <= 15, (
                f"print_comparison_report() has estimated complexity of {estimated_complexity}. "
                f"Extract helper functions per CODING_PATTERNS_ANALYSIS.md Category 2."
            )
