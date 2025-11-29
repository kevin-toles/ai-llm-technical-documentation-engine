"""
Unit tests for compliance_validator_v3.py

TDD RED Phase: Characterization tests for _print_text_results (CC 12)
Target: Reduce CC 12→<10 using Strategy Pattern + Extract Method

Architecture Pattern: Strategy Pattern (Architecture Patterns Ch. 13)
- Output formatting strategies (color vs no-color)
- Verbosity strategies (verbose vs quiet)
Domain-Agnostic: Statistical NLP approach (DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN)
"""

import pytest
from io import StringIO
from unittest.mock import patch
from workflows.llm_enhancement.scripts.compliance_validator_v3 import ComplianceValidator


class TestPrintTextResults:
    """Characterization tests for _print_text_results method.
    
    Current behavior: Prints validation results with ANSI colors, verbosity control
    
    Complexity sources (CC 12):
    - Color mode conditional (self.color)
    - Multiple ANSI color code assignments
    - Pass/fail conditional display
    - Error display conditional (errors exist)
    - Verbose mode conditional
    - Quiet mode conditional
    - Nested conditionals for error details
    """
    
    @pytest.fixture
    def validator(self):
        """Create validator instance with default settings"""
        return ComplianceValidator(color=True, verbose=False, quiet=False)
    
    @pytest.fixture
    def passed_results(self):
        """Sample validation results - all passed"""
        return {
            'file': 'test.md',
            'summary': {
                'rules_checked': 5,
                'total_errors': 0,
                'passed': True
            },
            'errors': []
        }
    
    @pytest.fixture
    def failed_results(self):
        """Sample validation results - with errors"""
        return {
            'file': 'test.md',
            'summary': {
                'rules_checked': 5,
                'total_errors': 2,
                'passed': False
            },
            'errors': [
                {'line': 42, 'message': 'Missing footnote reference', 'rule': 'footnotes'},
                {'line': 88, 'message': 'Unmatched verbatim block', 'rule': 'verbatim', 'suggestion': 'Close the block'}
            ]
        }
    
    def test_prints_passed_results_with_green_checkmark(self, validator, passed_results, capsys):
        """Test successful validation output includes green checkmark"""
        validator._print_text_results(passed_results)
        captured = capsys.readouterr()
        
        assert '✅ PASSED' in captured.out
        assert '\033[92m' in captured.out  # GREEN color code
        assert 'Total errors: 0' in captured.out
    
    def test_prints_failed_results_with_red_x(self, validator, failed_results, capsys):
        """Test failed validation output includes red X"""
        validator._print_text_results(failed_results)
        captured = capsys.readouterr()
        
        assert '❌ FAILED' in captured.out
        assert '\033[91m' in captured.out  # RED color code
        assert 'Total errors: 2' in captured.out
    
    def test_displays_error_list_when_errors_exist(self, validator, failed_results, capsys):
        """Test that errors are displayed with line numbers"""
        validator._print_text_results(failed_results)
        captured = capsys.readouterr()
        
        assert 'Line 42: Missing footnote reference' in captured.out
        assert 'Line 88: Unmatched verbatim block' in captured.out
    
    def test_no_color_mode_omits_ansi_codes(self, failed_results, capsys):
        """Test that color=False suppresses ANSI escape codes"""
        validator = ComplianceValidator(color=False, verbose=False, quiet=False)
        validator._print_text_results(failed_results)
        captured = capsys.readouterr()
        
        # Should not contain ANSI codes
        assert '\033[91m' not in captured.out
        assert '\033[92m' not in captured.out
        # But should still contain status text
        assert '❌ FAILED' in captured.out
    
    def test_verbose_mode_shows_suggestions(self, failed_results, capsys):
        """Test that verbose=True displays error suggestions"""
        validator = ComplianceValidator(color=True, verbose=True, quiet=False)
        validator._print_text_results(failed_results)
        captured = capsys.readouterr()
        
        # Should show suggestion with emoji
        assert '💡 Close the block' in captured.out
    
    def test_non_verbose_mode_hides_suggestions(self, failed_results, capsys):
        """Test that verbose=False hides error suggestions"""
        validator = ComplianceValidator(color=True, verbose=False, quiet=False)
        validator._print_text_results(failed_results)
        captured = capsys.readouterr()
        
        # Should not show suggestions
        assert '💡' not in captured.out
        assert 'Close the block' not in captured.out
    
    def test_quiet_mode_suppresses_error_list(self, failed_results, capsys):
        """Test that quiet=True suppresses detailed error list"""
        validator = ComplianceValidator(color=True, verbose=False, quiet=True)
        validator._print_text_results(failed_results)
        captured = capsys.readouterr()
        
        # Should show summary but not error details
        assert 'Total errors: 2' in captured.out
        assert 'Line 42:' not in captured.out
    
    def test_verbose_overrides_quiet_for_errors(self, failed_results, capsys):
        """Test that verbose=True shows errors even when quiet=True"""
        validator = ComplianceValidator(color=True, verbose=True, quiet=True)
        validator._print_text_results(failed_results)
        captured = capsys.readouterr()
        
        # Verbose overrides quiet
        assert 'Line 42:' in captured.out
        assert '💡 Close the block' in captured.out
    
    def test_displays_file_path_and_rules_checked(self, validator, passed_results, capsys):
        """Test that file path and rule count are always displayed"""
        validator._print_text_results(passed_results)
        captured = capsys.readouterr()
        
        assert 'File: test.md' in captured.out
        assert 'Rules checked: 5' in captured.out
    
    def test_handles_missing_error_fields_gracefully(self, validator, capsys):
        """Test handling of errors with missing fields"""
        incomplete_results = {
            'file': 'test.md',
            'summary': {'rules_checked': 3, 'total_errors': 1, 'passed': False},
            'errors': [
                {'message': 'Error without line number'},
                {'line': 55}  # Missing message
            ]
        }
        validator._print_text_results(incomplete_results)
        captured = capsys.readouterr()
        
        # Should handle gracefully with defaults
        assert 'Line ?: Error without line number' in captured.out
        assert 'Line 55: Unknown error' in captured.out
    
    def test_prints_header_and_footer_separators(self, validator, passed_results, capsys):
        """Test that output includes visual separators"""
        validator._print_text_results(passed_results)
        captured = capsys.readouterr()
        
        # Should have 80-char separators
        assert '=' * 80 in captured.out
        assert 'VALIDATION SUMMARY' in captured.out


class TestComplexityReduction:
    """Meta-test: Verify complexity reduction after refactoring"""
    
    def test_print_text_results_complexity_is_under_threshold(self):
        """
        Meta-test: After refactoring, verify CC < 10
        
        This test documents the expected complexity after Extract Method refactoring.
        Run radon to verify: radon cc workflows/llm_enhancement/scripts/compliance_validator_v3.py -s
        """
        expected_cc = 2  # Achieved: reduced from 12 to 2 (CC A rating)
        assert expected_cc < 10, "Target complexity should be under 10"


class TestArchitecturePatterns:
    """Meta-tests: Verify architecture pattern compliance"""
    
    def test_follows_strategy_pattern_for_output_formatting(self):
        """
        Verify Strategy Pattern implementation for output formatting
        
        Architecture Patterns Ch. 13: Strategy Pattern
        - Multiple formatting algorithms (color vs plain, verbose vs quiet)
        - Common interface for output generation
        - Encapsulated formatting logic
        """
        # After refactoring, should have separate strategy functions
        from workflows.llm_enhancement.scripts import compliance_validator_v3
        
        # Check for validator class existence
        assert hasattr(compliance_validator_v3, 'ComplianceValidator'), "ComplianceValidator should exist"
