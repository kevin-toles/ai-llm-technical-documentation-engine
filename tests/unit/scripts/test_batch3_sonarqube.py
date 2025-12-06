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
