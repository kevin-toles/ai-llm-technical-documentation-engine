"""
SonarQube Code Quality Tests for Batch 4 - High Priority Scripts

TDD Tests for Issues in:
- dry_run_enrichment_comparison.py: S7494 (2), S3457 (5), S3776 (1)
- llm_evaluation.py: S1172 (2), S3776 (5)
- rerun_full_pipeline.py: S3457 (7), S3776 (2)
- workflow_validation_services.py: S3776 (4)
- run_extraction_tests.py: S3776 (3)

Reference: CODING_PATTERNS_ANALYSIS.md Categories 2, 4, 14, 15, 16
Reference: Comp_Static_Analysis_Report_20251203.md Pattern References
"""
import pytest
import re
import ast
from pathlib import Path


# =============================================================================
# Batch 4.1: dry_run_enrichment_comparison.py
# Issues: S7494 L121-122 (2), S3457 L260-280 (5), S3776 L317 (1)
# =============================================================================


class TestDryRunEnrichmentComparisonS7494:
    """
    S7494: Replace set constructor call with a set comprehension.
    
    Anti-pattern: set(normalize(x) for x in list1)
    Fix pattern: {normalize(x) for x in list1}
    
    Reference: CODING_PATTERNS_ANALYSIS.md - Python best practices
    """
    
    @pytest.fixture
    def file_content(self) -> str:
        """Load dry_run_enrichment_comparison.py content."""
        file_path = Path(__file__).parent.parent.parent.parent / "scripts" / "dry_run_enrichment_comparison.py"
        return file_path.read_text()
    
    def test_line_121_set_comprehension(self, file_content: str):
        """
        S7494 Line 121: Replace set(normalize(x) for x in list1) with comprehension.
        """
        # Should NOT have set() constructor with generator
        pattern = r'set\s*\(\s*normalize\s*\(\s*x\s*\)\s+for\s+x\s+in\s+list1\s*\)'
        matches = re.findall(pattern, file_content)
        assert len(matches) == 0, (
            f"Found {len(matches)} set() constructor calls for list1. "
            f"Use set comprehension {{normalize(x) for x in list1}} instead (S7494)."
        )
    
    def test_line_122_set_comprehension(self, file_content: str):
        """
        S7494 Line 122: Replace set(normalize(x) for x in list2) with comprehension.
        """
        pattern = r'set\s*\(\s*normalize\s*\(\s*x\s*\)\s+for\s+x\s+in\s+list2\s*\)'
        matches = re.findall(pattern, file_content)
        assert len(matches) == 0, (
            f"Found {len(matches)} set() constructor calls for list2. "
            f"Use set comprehension {{normalize(x) for x in list2}} instead (S7494)."
        )


class TestDryRunEnrichmentComparisonS3457:
    """
    S3457: Add replacement fields or use a normal string instead of f-string.
    
    Anti-pattern: print(f"some text without placeholders")
    Fix pattern: print("some text without placeholders")
    
    Reference: CODING_PATTERNS_ANALYSIS.md Category 14 (Empty F-Strings)
    """
    
    @pytest.fixture
    def file_content(self) -> str:
        file_path = Path(__file__).parent.parent.parent.parent / "scripts" / "dry_run_enrichment_comparison.py"
        return file_path.read_text()
    
    def test_no_empty_fstrings_in_print_comparison_report(self, file_content: str):
        """
        S3457 Lines 260-280: print_comparison_report() should not have empty f-strings.
        
        Checks for f"..." patterns without {} placeholders.
        """
        # Extract print_comparison_report function using split approach
        # to avoid reluctant quantifier (S5852)
        func_start = file_content.find('def print_comparison_report(')
        if func_start != -1:
            # Find function body by locating next function/class definition
            rest = file_content[func_start:]
            next_def = rest.find('\ndef ', 1)  # Start from 1 to skip current def
            next_class = rest.find('\nclass ', 1)
            end_pos = min(
                pos for pos in [next_def, next_class, len(rest)] if pos > 0
            )
            func_body = rest[:end_pos]
            # Find f-strings without placeholders in print statements
            # Pattern: print(f"..." where ... has no { }
            empty_fstring_prints = re.findall(r'print\(f"[^{}"\n]+"\)', func_body)
            
            assert len(empty_fstring_prints) == 0, (
                f"Found {len(empty_fstring_prints)} print statements with empty f-strings. "
                f"Remove f-prefix when no {{}} placeholders are used (S3457). "
                f"Found: {empty_fstring_prints[:3]}"
            )


class TestDryRunEnrichmentComparisonS3776:
    """
    S3776: Refactor function to reduce Cognitive Complexity.
    
    Reference: CODING_PATTERNS_ANALYSIS.md Category 2 (Extract Method)
    Target: Complexity <= 15
    """
    
    @pytest.fixture
    def file_content(self) -> str:
        file_path = Path(__file__).parent.parent.parent.parent / "scripts" / "dry_run_enrichment_comparison.py"
        return file_path.read_text()
    
    def test_main_function_uses_helpers(self, file_content: str):
        """
        S3776 Line 317: main() should delegate to helper functions.
        
        Pattern: Extract Method - break into _helper functions
        """
        # Check for helper function definitions
        helper_patterns = [
            '_parse_arguments',
            '_list_available_books',
            '_process_book',
            '_print_summary',
            '_save_report',
            '_analyze_books',
        ]
        
        helpers_found = [h for h in helper_patterns if f'def {h}(' in file_content]
        
        # Extract main() function using split approach
        # to avoid reluctant quantifier (S5852)
        main_start = file_content.find('def main():')
        if main_start != -1:
            rest = file_content[main_start:]
            # Find end by looking for if __name__ or end of file
            name_check = rest.find('\nif __name__')
            end_pos = name_check if name_check > 0 else len(rest)
            main_body = rest[:end_pos]
            # Count complexity indicators
            for_count = main_body.count('for ')
            if_count = main_body.count('if ')
            try_count = main_body.count('try:')
            
            total_complexity_indicators = for_count + if_count + try_count
            
            # Pass if either: has helpers OR low complexity
            assert len(helpers_found) >= 2 or total_complexity_indicators <= 8, (
                f"main() has {total_complexity_indicators} complexity indicators. "
                f"Extract helper functions per CODING_PATTERNS_ANALYSIS.md Category 2. "
                f"Suggested helpers: {helper_patterns}"
            )


# =============================================================================
# Batch 4.2: llm_evaluation.py (additional S1172 and S3776 issues)
# =============================================================================


class TestLlmEvaluationS1172:
    """
    S1172: Remove unused function parameters.
    
    Reference: CODING_PATTERNS_ANALYSIS.md Category 4 (Unused Parameters)
    """
    
    @pytest.fixture
    def file_content(self) -> str:
        file_path = Path(__file__).parent.parent.parent.parent / "scripts" / "llm_evaluation.py"
        return file_path.read_text()
    
    def test_line_307_unused_api_key_param(self, file_content: str):
        """
        S1172 Line 307: Remove unused 'api_key' parameter.
        
        If parameter is required by interface but not used, prefix with _.
        """
        # Check if api_key is used in function body or prefixed with _
        # Look for functions with api_key parameter that haven't been fixed
        # Pattern: api_key without leading underscore
        pattern = r'def \w+\([^)]*(?<!_)\bapi_key\b[^)]*\):'
        unfixed_matches = re.findall(pattern, file_content)
        
        # Filter out matches that have _api_key (already fixed)
        unfixed_matches = [m for m in unfixed_matches if '_api_key' not in m]
        
        # Test passes if all api_key params are either used or prefixed with _
        # This is a placeholder until AST analysis is implemented
        pytest.skip("Placeholder - requires function body analysis to verify api_key usage")
    
    def test_line_331_unused_api_key_param(self, file_content: str):
        """
        S1172 Line 331: Remove unused 'api_key' parameter.
        """
        # Similar to above - check for api_key usage or _ prefix
        # This is a structural test - validates the parameter is handled
        pytest.skip("Placeholder - requires function body analysis")


class TestLlmEvaluationS3776Batch4:
    """
    S3776: Additional cognitive complexity issues in llm_evaluation.py.
    
    Lines: 701, 1033, 1647, 1838, 2152
    """
    
    @pytest.fixture
    def file_content(self) -> str:
        file_path = Path(__file__).parent.parent.parent.parent / "scripts" / "llm_evaluation.py"
        return file_path.read_text()
    
    def test_complex_functions_have_helpers(self, file_content: str):
        """
        Verify complex functions delegate to helper functions.
        """
        # Count helper functions (functions starting with _)
        helper_count = len(re.findall(r'\ndef _[a-z_]+\(', file_content))
        
        # After proper refactoring, should have multiple helpers
        assert helper_count >= 10, (
            f"Found only {helper_count} helper functions. "
            f"Complex functions should delegate to _ prefixed helpers (S3776)."
        )


# =============================================================================
# Batch 4.3: rerun_full_pipeline.py
# Issues: S3457 (7), S3776 (2)
# =============================================================================


class TestRerunFullPipelineS3457:
    """
    S3457: Remove empty f-strings.
    
    Lines: 206, 250, 343, 348, 353, 360, 365, 467
    """
    
    @pytest.fixture
    def file_content(self) -> str:
        file_path = Path(__file__).parent.parent.parent.parent / "scripts" / "rerun_full_pipeline.py"
        return file_path.read_text()
    
    def test_no_empty_fstrings(self, file_content: str):
        """
        S3457: No f-strings without placeholders.
        """
        # Find all f-strings without placeholders
        # Pattern matches f"..." or f'...' without any {}
        fstring_pattern = r'f["\'][^{}"\']*["\']'
        
        # Filter to only print statements for clearer results
        print_fstrings = re.findall(r'print\(' + fstring_pattern + r'\)', file_content)
        
        assert len(print_fstrings) == 0, (
            f"Found {len(print_fstrings)} print statements with empty f-strings. "
            f"Remove f-prefix when no {{}} placeholders (S3457)."
        )


class TestRerunFullPipelineS3776:
    """
    S3776: Cognitive Complexity issues.
    
    Lines: 265, 365
    """
    
    @pytest.fixture
    def file_content(self) -> str:
        file_path = Path(__file__).parent.parent.parent.parent / "scripts" / "rerun_full_pipeline.py"
        return file_path.read_text()
    
    def test_has_helper_functions(self, file_content: str):
        """
        Complex functions should delegate to helpers.
        """
        helper_count = len(re.findall(r'\ndef _[a-z_]+\(', file_content))
        
        # Should have helpers for run_pipeline and main
        assert helper_count >= 3, (
            f"Found only {helper_count} helper functions. "
            f"Extract helpers per CODING_PATTERNS_ANALYSIS.md Category 2."
        )


# =============================================================================
# Batch 4.4: workflow_validation_services.py
# Issues: S3776 (4)
# =============================================================================


class TestWorkflowValidationServicesS3776:
    """
    S3776: Cognitive Complexity issues.
    
    Lines: 87, 187, 375, 490
    """
    
    @pytest.fixture
    def file_content(self) -> str:
        file_path = Path(__file__).parent.parent.parent.parent / "scripts" / "workflow_validation_services.py"
        return file_path.read_text()
    
    def test_validation_functions_have_helpers(self, file_content: str):
        """
        Validation functions should delegate to helpers.
        """
        # Count module-level helpers (def _name) and class method helpers (def _name in class)
        module_helpers = len(re.findall(r'\ndef _[a-z_]+\(', file_content))
        class_method_helpers = len(re.findall(r'def _[a-z_]+\(', file_content))
        helper_count = max(module_helpers, class_method_helpers)
        
        assert helper_count >= 4, (
            f"Found only {helper_count} helper functions. "
            f"4 complex functions need helper extraction (S3776)."
        )


# =============================================================================
# Batch 4.5: run_extraction_tests.py
# Issues: S3776 (3)
# =============================================================================


class TestRunExtractionTestsS3776:
    """
    S3776: Cognitive Complexity issues.
    
    Lines: 174, 463, 593
    """
    
    @pytest.fixture
    def file_content(self) -> str:
        file_path = Path(__file__).parent.parent.parent.parent / "scripts" / "run_extraction_tests.py"
        return file_path.read_text()
    
    def test_extraction_functions_have_helpers(self, file_content: str):
        """
        Extraction test functions should delegate to helpers.
        """
        # Count module-level helpers (def _name) and class method helpers (def _name in class)
        module_helpers = len(re.findall(r'\ndef _[a-z_]+\(', file_content))
        class_method_helpers = len(re.findall(r'def _[a-z_]+\(', file_content))
        helper_count = max(module_helpers, class_method_helpers)
        
        assert helper_count >= 3, (
            f"Found only {helper_count} helper functions. "
            f"3 complex functions need helper extraction (S3776)."
        )


# =============================================================================
# Regression Tests - Ensure fixes don't break functionality
# =============================================================================


class TestBatch4NoRegressions:
    """
    Verify files remain valid Python after fixes.
    """
    
    def test_dry_run_enrichment_is_valid_python(self):
        """Verify syntax is valid."""
        file_path = Path(__file__).parent.parent.parent.parent / "scripts" / "dry_run_enrichment_comparison.py"
        content = file_path.read_text()
        try:
            compile(content, str(file_path), "exec")
        except SyntaxError as e:
            pytest.fail(f"Syntax error: {e}")
    
    def test_llm_evaluation_is_valid_python(self):
        """Verify syntax is valid."""
        file_path = Path(__file__).parent.parent.parent.parent / "scripts" / "llm_evaluation.py"
        content = file_path.read_text()
        try:
            compile(content, str(file_path), "exec")
        except SyntaxError as e:
            pytest.fail(f"Syntax error: {e}")
    
    def test_rerun_full_pipeline_is_valid_python(self):
        """Verify syntax is valid."""
        file_path = Path(__file__).parent.parent.parent.parent / "scripts" / "rerun_full_pipeline.py"
        content = file_path.read_text()
        try:
            compile(content, str(file_path), "exec")
        except SyntaxError as e:
            pytest.fail(f"Syntax error: {e}")
