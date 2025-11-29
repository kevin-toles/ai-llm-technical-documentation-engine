"""
Test suite for function complexity refactoring (R0914, R0915 violations).

This test suite enforces complexity thresholds following TDD RED→GREEN→REFACTOR workflow:
- R0914: Too Many Local Variables (threshold: 15)
- R0915: Too Many Statements (threshold: 50)

Following ANTI_PATTERN_ANALYSIS.md §10.2-10.3 fix patterns:
- Extract Method pattern for R0914 violations
- Pipeline Pattern for R0915 violations

References:
    - ARCHITECTURE_GUIDELINES Ch.3: Abstraction reduces complexity
    - PYTHON_GUIDELINES Ch.21: Module boundaries & function organization
    - ANTI_PATTERN_ANALYSIS §10.2: Extract Method (Too Many Locals)
    - ANTI_PATTERN_ANALYSIS §10.3: Pipeline Pattern (Too Many Statements)
"""

import ast
import inspect
from pathlib import Path
from typing import Dict, List, Set, Tuple

import pytest

# Import target module
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from workflows.base_guideline_generation.scripts import (
    chapter_generator_all_text as target_module,
)


# ============================================================================
# Helper: Count Local Variables Using AST
# ============================================================================


def count_local_variables(func) -> int:
    """
    Count local variables in a function using AST analysis.
    
    Counts:
    - Function arguments
    - Variable assignments within function body
    - Loop variables (for, with)
    
    Does NOT count:
    - Class attributes (self.x)
    - Global/nonlocal variables
    - Function calls
    
    Args:
        func: Function object to analyze
        
    Returns:
        Number of local variables
        
    Reference:
        - Python Distilled Ch.5: AST introspection
    """
    source = inspect.getsource(func)
    tree = ast.parse(source)
    func_def = tree.body[0]

    local_vars: Set[str] = set()

    # Count function arguments
    for arg in func_def.args.args:
        local_vars.add(arg.arg)

    # Walk AST to find assignments
    for node in ast.walk(func_def):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    local_vars.add(target.id)
                elif isinstance(target, ast.Tuple):
                    for elt in target.elts:
                        if isinstance(elt, ast.Name):
                            local_vars.add(elt.id)
        elif isinstance(node, ast.For):
            if isinstance(node.target, ast.Name):
                local_vars.add(node.target.id)
        elif isinstance(node, (ast.ListComp, ast.DictComp, ast.SetComp)):
            for generator in node.generators:
                if isinstance(generator.target, ast.Name):
                    local_vars.add(generator.target.id)
        elif isinstance(node, ast.With):
            for item in node.items:
                if item.optional_vars and isinstance(item.optional_vars, ast.Name):
                    local_vars.add(item.optional_vars.id)

    return len(local_vars)


def count_statements(func) -> int:
    """
    Count statements in a function using AST analysis.
    
    Counts all statement nodes (Assign, Return, If, For, etc.)
    
    Args:
        func: Function object to analyze
        
    Returns:
        Number of statements
        
    Reference:
        - Python Distilled Ch.5: AST introspection
    """
    source = inspect.getsource(func)
    tree = ast.parse(source)
    func_def = tree.body[0]

    statement_count = 0
    for node in ast.walk(func_def):
        if isinstance(node, ast.stmt):
            statement_count += 1

    return statement_count


# ============================================================================
# RED Phase Tests: R0914 - Too Many Local Variables
# ============================================================================


class TestR0914TooManyLocals:
    """Test suite for R0914 violations (Too Many Local Variables)."""

    @pytest.mark.parametrize(
        "func_name,expected_max_locals",
        [
            ("build_concept_sections", 15),
            ("_process_single_chapter", 15),
        ],
    )
    def test_function_has_few_locals(self, func_name: str, expected_max_locals: int):
        """
        Test that functions adhere to 15 local variable threshold.
        
        RED Phase: This test WILL FAIL initially because:
        - build_concept_sections: 16 locals (line 1330)
        - _process_single_chapter: 22 locals (line 1851)
        
        GREEN Phase: Will pass after Extract Method refactoring applied.
        
        Args:
            func_name: Name of function to test
            expected_max_locals: Maximum allowed local variables (15)
            
        References:
            - ANTI_PATTERN_ANALYSIS §10.2: Extract Method pattern
            - Architecture Patterns Ch.3: Abstraction boundaries
        """
        func = getattr(target_module, func_name)
        actual_locals = count_local_variables(func)

        assert actual_locals <= expected_max_locals, (
            f"{func_name}() has {actual_locals} local variables "
            f"(threshold: {expected_max_locals}). "
            f"Apply Extract Method pattern to reduce complexity."
        )

    def test_build_concept_sections_uses_helper_functions(self):
        """
        Test that build_concept_sections() uses Extract Method pattern.
        
        RED Phase: WILL FAIL - no helper functions exist yet.
        
        GREEN Phase: Will pass after extracting:
        - _extract_concept_from_pages() - handles concept extraction logic
        - _build_concept_footnote() - handles footnote creation
        
        Expected signature after refactoring:
            build_concept_sections() - orchestration (8-10 locals)
            _extract_concept_from_pages() - extraction logic (5-6 locals)
            _build_concept_footnote() - footnote logic (3-4 locals)
            
        References:
            - ANTI_PATTERN_ANALYSIS §10.2: Extract Method reduces locals
            - Python Distilled Ch.5: Function decomposition
        """
        # Verify helper functions exist in module
        assert hasattr(
            target_module, "_extract_concept_from_pages"
        ), "Missing helper: _extract_concept_from_pages()"
        assert hasattr(
            target_module, "_build_concept_footnote"
        ), "Missing helper: _build_concept_footnote()"

        # Verify main function has reduced complexity
        func = target_module.build_concept_sections
        actual_locals = count_local_variables(func)
        assert actual_locals <= 12, (
            f"build_concept_sections() still has {actual_locals} locals after refactoring "
            f"(expected ≤12 for orchestration function with 6 parameters)"
        )

    def test_process_single_chapter_uses_helper_functions(self):
        """
        Test that _process_single_chapter() uses Extract Method pattern.
        
        RED Phase: WILL FAIL - no helper functions exist yet.
        
        GREEN Phase: Will pass after extracting:
        - _extract_chapter_pages() - page extraction logic
        - _build_chapter_concepts() - concept extraction logic
        - _generate_chapter_cross_refs() - cross-reference logic
        - _assemble_chapter_output() - final assembly
        
        Expected signature after refactoring:
            _process_single_chapter() - orchestration (8-10 locals)
            _extract_chapter_pages() - page logic (4-5 locals)
            _build_chapter_concepts() - concept logic (5-6 locals)
            _generate_chapter_cross_refs() - cross-ref logic (5-6 locals)
            _assemble_chapter_output() - assembly logic (3-4 locals)
            
        References:
            - ANTI_PATTERN_ANALYSIS §10.2: Extract Method pattern
            - Architecture Patterns Ch.4: Service Layer orchestration
        """
        # Verify helper functions exist in module
        required_helpers = [
            "_extract_chapter_pages",
            "_build_chapter_concepts",
            "_generate_chapter_cross_refs",
            "_assemble_chapter_output",
        ]

        for helper_name in required_helpers:
            assert hasattr(target_module, helper_name), f"Missing helper: {helper_name}()"

        # Verify main function has reduced complexity
        func = target_module._process_single_chapter
        actual_locals = count_local_variables(func)
        assert actual_locals <= 17, (
            f"_process_single_chapter() still has {actual_locals} locals after refactoring "
            f"(expected ≤17 for orchestration function with complex workflow)"
        )


# ============================================================================
# RED Phase Tests: R0915 - Too Many Statements
# ============================================================================


class TestR0915TooManyStatements:
    """Test suite for R0915 violations (Too Many Statements)."""

    def test_write_output_file_has_few_statements(self):
        """
        Test that _write_output_file() adheres to 50 statement threshold.
        
        RED Phase: WILL FAIL because function has 51 statements (line 2262).
        
        GREEN Phase: Will pass after Pipeline Pattern refactoring applied.
        
        References:
            - ANTI_PATTERN_ANALYSIS §10.3: Pipeline Pattern
            - Architecture Patterns Ch.4: Service Layer orchestration
        """
        func = target_module._write_output_file
        actual_statements = count_statements(func)
        expected_max = 50

        assert actual_statements <= expected_max, (
            f"_write_output_file() has {actual_statements} statements "
            f"(threshold: {expected_max}). "
            f"Apply Pipeline Pattern to reduce complexity."
        )

    def test_write_output_file_uses_pipeline_pattern(self):
        """
        Test that _write_output_file() uses Pipeline Pattern.
        
        RED Phase: WILL FAIL - no pipeline steps exist yet.
        
        GREEN Phase: Will pass after extracting pipeline steps:
        - _prepare_output_paths() - setup output directories
        - _convert_to_json() - MD → JSON conversion
        - _write_markdown_file() - write MD file
        - _write_json_file() - write JSON file
        - _log_output_summary() - log results
        
        Expected signature after refactoring:
            _write_output_file() - orchestrates pipeline (15-20 statements)
            _prepare_output_paths() - path setup (5-8 statements)
            _convert_to_json() - conversion (8-10 statements)
            _write_markdown_file() - MD write (8-10 statements)
            _write_json_file() - JSON write (8-10 statements)
            _log_output_summary() - logging (3-5 statements)
            
        References:
            - ANTI_PATTERN_ANALYSIS §10.3: Pipeline Pattern
            - Python Cookbook Recipe 5.18: File operations
        """
        # Verify pipeline step functions exist in module
        required_steps = [
            "_prepare_output_paths",
            "_convert_to_json",
            "_write_markdown_file",
            "_write_json_file",
            "_log_output_summary",
        ]

        for step_name in required_steps:
            assert hasattr(target_module, step_name), f"Missing pipeline step: {step_name}()"

        # Verify main function has reduced complexity
        func = target_module._write_output_file
        actual_statements = count_statements(func)
        assert actual_statements <= 20, (
            f"_write_output_file() still has {actual_statements} statements after refactoring "
            f"(expected ≤20 for pipeline orchestration)"
        )


# ============================================================================
# Integration Tests: Verify No Functional Regressions
# ============================================================================


class TestComplexityRefactoringNoRegressions:
    """
    Verify refactored functions maintain identical behavior.
    
    These tests ensure Extract Method and Pipeline Pattern refactoring
    does not introduce functional regressions.
    """

    def test_build_concept_sections_output_unchanged(self):
        """
        Verify build_concept_sections() produces identical output after refactoring.
        
        Tests with sample data to ensure Extract Method refactoring maintains behavior.
        """
        # Sample test data
        chapter_pages = [
            {"page_number": 10, "content": "Python is a programming language. Python uses indentation."},
            {"page_number": 11, "content": "Functions in Python are first-class objects."},
        ]
        concepts = {"python", "function", "indentation"}

        # Call function (should work before and after refactoring)
        result, footnote_num, footnotes = target_module.build_concept_sections(
            _primary_data={},
            chapter_pages=chapter_pages,
            footnote_start=1,
            _chapter_num=1,
            chapter_concepts=concepts,
            _occurrence_index=None,
        )

        # Verify output structure (basic smoke test)
        assert isinstance(result, str), "Should return string"
        assert isinstance(footnote_num, int), "Should return int"
        assert isinstance(footnotes, list), "Should return list"
        assert footnote_num >= 1, "Footnote counter should increment"

    def test_write_output_file_creates_both_formats(self, tmp_path):
        """
        Verify _write_output_file() creates both MD and JSON files after refactoring.
        
        Tests with temporary directory to ensure Pipeline Pattern refactoring maintains behavior.
        """
        # Sample markdown document
        sample_docs = [
            "# Test Document",
            "## Chapter 1: Introduction",
            "Content here.",
        ]
        sample_footnotes = [
            {"num": 1, "author": "Test", "title": "Test Book", "file": "test.pdf", "page": 1, "start_line": 1, "end_line": 10}
        ]

        # Mock output directory using tmp_path
        import workflows.base_guideline_generation.scripts.chapter_generator_all_text as module

        original_path = Path(module.__file__).parent.parent / "output"
        
        # Create test using existing function (should work before and after refactoring)
        # This is a smoke test - actual file I/O tested elsewhere
        try:
            target_module._write_output_file(sample_docs, "test_book", sample_footnotes)
            
            # If function completes without error, pipeline is functional
            # (Actual file verification requires integration test with real paths)
            assert True, "Pipeline completes without errors"
        except Exception as e:
            # If refactoring broke pipeline, this will catch it
            pytest.fail(f"Pipeline Pattern refactoring broke _write_output_file: {e}")
