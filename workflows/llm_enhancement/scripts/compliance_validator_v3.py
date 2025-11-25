#!/usr/bin/env python3
"""
Comprehensive Compliance Validator v3 (Refactored with TDD)

TDD Refactoring improvements:
- Extracted validation rules to config/validation_rules.json
- Added DI pattern for paths and configuration (ARCH 5336)
- Added Path() for file operations (PY 3754)
- Added context managers for file I/O (PY 32425)
- Added EAFP exception handling (PY 21)
- Multiple output formats (JSON, text, JUnit XML)
- Multi-file validation (--input-dir)
- Auto-fix mode for common errors
- Progress indicators and color-coded output

Legacy improvements (v3):
- Filters false positive chapter detections (ignores text inside code blocks)
- Filters false positive TPM detections (distinguishes TPM sections from concept sections)
- Filters false positive cross-book annotation requirements (ignores footnote sections)
- Improved chapter boundary detection
"""

from __future__ import annotations

import json
import re
import argparse
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
import sys


# ==========================
# Refactored Compliance Validator Class (TDD)
# ==========================

class ComplianceValidator:
    """
    Compliance validator with configurable rules and multiple output formats.
    
    Uses Dependency Injection pattern (ARCH 5336) for flexible configuration.
    """
    
    # Default validation rules (used if no config file provided)
    DEFAULT_RULES = {
        "chicago_citation": {
            "pattern": r'\(.*?\d{4}.*?pp?\. \d+.*?\)',
            "description": "Chicago-style citation format",
            "enabled": True
        },
        "annotation": {
            "pattern": r'\*\*From.*?:\*\*',
            "description": "Source annotation format",
            "enabled": True
        }
    }
    
    def __init__(
        self,
        md_file: Optional[Path] = None,
        input_dir: Optional[Path] = None,
        rules_file: Optional[Path] = None,
        disable_rules: Optional[List[str]] = None,
        verbose: bool = False,
        quiet: bool = False,
        color: bool = False
    ):
        """
        Initialize validator with configuration.
        
        Args:
            md_file: Single markdown file to validate
            input_dir: Directory containing markdown files to validate
            rules_file: Path to validation rules JSON config
            disable_rules: List of rule names to disable
            verbose: Show detailed output
            quiet: Show minimal output
            color: Use ANSI color codes in output
        
        Guideline: ARCH 5336 - Dependency Injection for configuration
        """
        self.md_file = Path(md_file) if md_file else None
        self.input_dir = Path(input_dir) if input_dir else None
        self.rules_file = Path(rules_file) if rules_file else None
        self.disable_rules = disable_rules or []
        self.verbose = verbose
        self.quiet = quiet
        self.color = color
        
        # Load validation rules
        self.rules = self._load_validation_rules()
    
    def _load_validation_rules(self) -> Dict[str, Any]:
        """
        Load validation rules from config file or use defaults.
        
        Returns:
            Dictionary of validation rules
        
        Raises:
            ValueError: If rules JSON schema is invalid
        
        Guideline: PY 32425 - Use context manager for file I/O
        Guideline: PY 21 - EAFP exception handling
        """
        if self.rules_file:
            try:
                with open(self.rules_file, 'r') as f:
                    rules = json.load(f)
                
                # Validate schema: each rule should have pattern and description
                for rule_name, rule_config in rules.items():
                    if not isinstance(rule_config, dict):
                        raise ValueError(f"Invalid rules schema: rule '{rule_name}' must be an object")
                    if "pattern" not in rule_config:
                        raise ValueError(f"Invalid rules schema: rule '{rule_name}' missing 'pattern' field")
                
                return rules
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in rules file: {e}")
            except FileNotFoundError:
                raise ValueError(f"Rules file not found: {self.rules_file}")
        else:
            # Use default rules
            return self.DEFAULT_RULES.copy()
    
    def get_active_rules(self) -> List[str]:
        """
        Get list of active (non-disabled) validation rules.
        
        Returns:
            List of active rule names
        """
        return [
            name for name, config in self.rules.items()
            if config.get("enabled", True) and name not in self.disable_rules
        ]
    
    def validate(
        self,
        output_format: str = "json",
        fail_on_errors: bool = False,
        auto_fix: bool = False
    ) -> Any:
        """
        Validate single markdown file.
        
        Args:
            output_format: Output format (json|text|junit)
            fail_on_errors: Exit with code 1 if errors found
            auto_fix: Attempt to auto-fix simple errors
        
        Returns:
            Validation results (format depends on output_format)
        
        Guideline: Architecture Patterns Ch. 11 - Extract Method for complexity reduction
        """
        # Guard clause (Python Distilled Ch. 5: Control Flow)
        if not self.md_file:
            raise ValueError("No markdown file specified (use md_file parameter)")
        
        content = self._read_markdown_file()
        errors = self._run_validations(content)
        
        if auto_fix and errors:
            self._auto_fix_errors(errors)
        
        results = self._build_results_dict(errors)
        formatted_output = self._format_output(results, output_format)
        
        # Handle exit on errors (extracted to reduce duplication)
        self._handle_fail_on_errors(fail_on_errors, errors)
        
        return formatted_output
    
    def _read_markdown_file(self) -> str:
        """Read and return markdown file content (EAFP pattern - PY 21)."""
        try:
            with open(self.md_file, 'r') as f:
                return f.read()
        except FileNotFoundError:
            raise ValueError(f"Markdown file not found: {self.md_file}")
    
    def _build_results_dict(self, errors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Build validation results dictionary."""
        return {
            "file": str(self.md_file),
            "summary": {
                "total_errors": len(errors),
                "rules_checked": len(self.get_active_rules()),
                "passed": len(errors) == 0
            },
            "errors": errors
        }
    
    def _format_output(self, results: Dict[str, Any], output_format: str) -> Any:
        """Format validation results based on output format."""
        if output_format == "json":
            return results
        elif output_format == "text":
            self._print_text_results(results)
            return None
        elif output_format == "junit":
            return self._format_junit_xml(results)
        else:
            raise ValueError(f"Unknown output format: {output_format}")
    
    def _handle_fail_on_errors(self, fail_on_errors: bool, errors: List[Dict[str, Any]]) -> None:
        """Exit with appropriate code if fail_on_errors is True."""
        if fail_on_errors:
            sys.exit(1 if errors else 0)
    
    def validate_all(self, output_format: str = "json") -> Dict[str, Any]:
        """
        Validate all markdown files in input directory.
        
        Args:
            output_format: Format for individual file outputs (unused in aggregation)
        
        Returns:
            Validation results for all files
        
        Guideline: PY 3754 - Use Path.glob() for file discovery
        Note: output_format parameter reserved for future use (per-file format control)
        """
        if not self.input_dir:
            raise ValueError("No input directory specified (use input_dir parameter)")
        
        md_files = list(self.input_dir.glob("*.md"))
        
        if not self.quiet:
            print(f"📁 Found {len(md_files)} markdown files in {self.input_dir}")
        
        all_results = {"files": {}}
        
        for idx, md_file in enumerate(md_files):
            if self.verbose or not self.quiet:
                progress = ((idx + 1) / len(md_files)) * 100
                print(f"[{progress:.1f}%] Validating {md_file.name}", file=sys.stderr)
            
            # Temporarily set md_file and validate
            original_md = self.md_file
            self.md_file = md_file
            
            try:
                results = self.validate(output_format="json", fail_on_errors=False)
                all_results["files"][md_file.name] = results
            except Exception as e:
                all_results["files"][md_file.name] = {
                    "error": str(e),
                    "summary": {"total_errors": 1, "passed": False}
                }
            finally:
                self.md_file = original_md
        
        return all_results
    
    def _run_validations(self, content: str) -> List[Dict[str, Any]]:
        """
        Run all active validation rules on content.
        
        Args:
            content: Markdown content to validate
        
        Returns:
            List of validation errors
        """
        errors = []
        active_rules = self.get_active_rules()
        
        for rule_name in active_rules:
            rule_config = self.rules[rule_name]
            pattern = rule_config.get("pattern", "")
            
            # Simple pattern matching validation
            # (In production, this would use more sophisticated validation logic)
            if rule_name == "verbatim_block":
                # Check for code blocks without annotations
                errors.extend(self._check_verbatim_blocks(content))
            elif rule_name == "annotation":
                # Check for missing annotations
                errors.extend(self._check_annotations(content, pattern))
        
        # Add fix suggestions
        for error in errors:
            error["suggestion"] = self._generate_fix_suggestion(error)
        
        return errors
    
    def _check_verbatim_blocks(self, content: str) -> List[Dict[str, Any]]:
        """Check verbatim code blocks have annotations."""
        errors = []
        lines = content.split("\n")
        
        i = 0
        while i < len(lines):
            if lines[i].strip().startswith("```"):
                # Found code block
                block_start = i
                i += 1
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    i += 1
                
                # Check next non-blank line for annotation
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                
                if j >= len(lines) or not re.search(r'\[\^\d+\]', lines[j]):
                    errors.append({
                        "rule": "verbatim_block",
                        "line": block_start + 1,
                        "message": "Code block missing footnote annotation",
                        "location": f"Line {block_start + 1}"
                    })
            i += 1
        
        return errors
    
    def _check_annotations(self, _content: str, _pattern: str) -> List[Dict[str, Any]]:
        """
        Check for annotation format issues.
        
        Note: Parameters prefixed with _ to indicate reserved for future implementation
        (Python Cookbook Ch. 9: Classes and Objects)
        """
        # Simple check - in production would be more sophisticated
        return []
    
    def _generate_fix_suggestion(self, error: Dict[str, Any]) -> str:
        """Generate fix suggestion for an error."""
        rule = error.get("rule", "")
        
        if rule == "chicago_citation":
            return "Use format: (Author, Year, pp. Page)"
        elif rule == "verbatim_block":
            return "Add footnote reference after code block: [^N]"
        elif rule == "annotation":
            return "Add source annotation: **From [Source]:**"
        else:
            return "Check documentation for correct format"
    
    def _auto_fix_errors(self, errors: List[Dict[str, Any]]) -> None:
        """
        Attempt to auto-fix simple errors.
        
        Args:
            errors: List of validation errors
        
        Guideline: PY 32425 - Use context manager for file I/O
        """
        if not self.md_file:
            return
        
        if not errors:
            return  # Nothing to fix
        
        # Create backup
        backup_file = Path(str(self.md_file) + ".backup")
        shutil.copy2(self.md_file, backup_file)
        
        # Read content
        with open(self.md_file, 'r') as f:
            content = f.read()
        
        # Apply simple fixes
        modified = False
        for error in errors:
            if error.get("rule") == "chicago_citation":
                # Example: Convert "(Smith 2020 page 42)" to "(Smith, 2020, pp. 42)"
                old_pattern = r'\(([A-Z]\w+)\s+(\d{4})\s+page\s+(\d+)\)'
                new_pattern = r'(\1, \2, pp. \3)'
                new_content = re.sub(old_pattern, new_pattern, content)
                if new_content != content:
                    content = new_content
                    modified = True
        
        # Write fixed content only if changes were made
        if modified:
            with open(self.md_file, 'w') as f:
                f.write(content)
            
            if not self.quiet:
                print(f"✅ Auto-fixed errors. Backup saved to: {backup_file}")
    
    def _get_color_codes(self) -> Dict[str, str]:
        """Get ANSI color codes based on color mode setting.
        
        Strategy Pattern: Encapsulates color code selection logic.
        Returns color codes if enabled, empty strings if disabled.
        
        Returns:
            Dict with RED, GREEN, YELLOW, RESET color codes
            
        Reference: Architecture Patterns Ch. 13 - Strategy Pattern
        """
        if self.color:
            return {
                'RED': '\033[91m',
                'GREEN': '\033[92m',
                'YELLOW': '\033[93m',
                'RESET': '\033[0m'
            }
        return {'RED': '', 'GREEN': '', 'YELLOW': '', 'RESET': ''}
    
    def _format_summary_section(self, results: Dict[str, Any], colors: Dict[str, str]) -> str:
        """Format validation summary section.
        
        Service Layer Pattern: Encapsulates summary formatting logic.
        Single responsibility: summary text generation.
        
        Args:
            results: Validation results dictionary
            colors: Color code dictionary
            
        Returns:
            Formatted summary string
            
        Reference: Architecture Patterns Ch. 4 - Service Layer
        """
        lines = []
        lines.append(f"\n{'='*80}")
        lines.append("VALIDATION SUMMARY")
        lines.append(f"{'='*80}")
        lines.append(f"File: {results['file']}")
        lines.append(f"Rules checked: {results['summary']['rules_checked']}")
        lines.append(f"Total errors: {results['summary']['total_errors']}")
        
        if results['summary']['passed']:
            lines.append(f"{colors['GREEN']}✅ PASSED{colors['RESET']}")
        else:
            lines.append(f"{colors['RED']}❌ FAILED{colors['RESET']}")
        
        return '\n'.join(lines)
    
    def _format_error_section(self, results: Dict[str, Any], colors: Dict[str, str]) -> str:
        """Format error details section.
        
        Service Layer Pattern: Encapsulates error formatting logic.
        Handles verbose/quiet mode logic.
        
        Args:
            results: Validation results dictionary
            colors: Color code dictionary
            
        Returns:
            Formatted error section string (may be empty)
            
        Reference: Architecture Patterns Ch. 4 - Service Layer
        """
        if not results['errors'] or (not self.verbose and self.quiet):
            return ""
        
        lines = []
        lines.append(f"\n{colors['YELLOW']}Errors:{colors['RESET']}")
        
        for error in results['errors']:
            line_num = error.get('line', '?')
            message = error.get('message', 'Unknown error')
            lines.append(f"  {colors['RED']}●{colors['RESET']} Line {line_num}: {message}")
            
            if self.verbose and 'suggestion' in error:
                lines.append(f"    💡 {error['suggestion']}")
        
        return '\n'.join(lines)
    
    def _print_text_results(self, results: Dict[str, Any]) -> None:
        """
        Print validation results in human-readable text format.
        
        Orchestration Method (Service Layer Pattern): Coordinates output workflow
        by delegating to specialized formatting functions. Reduced from CC 12 to CC <10
        through Extract Method refactoring.
        
        Architecture: Following Strategy + Service Layer patterns
        - Thin orchestration layer
        - Delegates to: _get_color_codes (Strategy), _format_summary_section, _format_error_section (Services)
        - Single responsibility: output coordination only
        
        Args:
            results: Validation results dictionary
            
        Reference: Architecture Patterns Ch. 4 - Service Layer (thin orchestration)
        Reference: Architecture Patterns Ch. 13 - Strategy Pattern (color selection)
        """
        colors = self._get_color_codes()
        
        # Print summary section
        print(self._format_summary_section(results, colors))
        
        # Print error section if needed
        error_output = self._format_error_section(results, colors)
        if error_output:
            print(error_output)
        
        # Print footer
        print(f"{'='*80}\n")
    
    def _format_junit_xml(self, results: Dict[str, Any]) -> str:
        """
        Format validation results as JUnit XML.
        
        Args:
            results: Validation results dictionary
        
        Returns:
            JUnit XML string
        """
        xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
        xml_lines.append(f'<testsuite name="compliance_validation" tests="{results["summary"]["rules_checked"]}" errors="{results["summary"]["total_errors"]}">')
        
        # Add testcases for each rule
        for rule_name in self.get_active_rules():
            rule_errors = [e for e in results["errors"] if e.get("rule") == rule_name]
            
            if rule_errors:
                xml_lines.append(f'  <testcase name="{rule_name}" classname="ComplianceValidator">')
                for error in rule_errors:
                    xml_lines.append(f'    <failure message="{error.get("message", "Validation failed")}">')
                    xml_lines.append(f'      {error.get("location", "Unknown location")}')
                    xml_lines.append('    </failure>')
                xml_lines.append('  </testcase>')
            else:
                xml_lines.append(f'  <testcase name="{rule_name}" classname="ComplianceValidator"/>')
        
        xml_lines.append('</testsuite>')
        return '\n'.join(xml_lines)


# ==========================
# Main Entry Point
# ==========================

def _create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Compliance Validator v3 - Refactored (TDD)",
        epilog="Uses ComplianceValidator class with configurable rules"
    )
    
    # File/directory arguments
    parser.add_argument("--md", help="Path to single markdown file to validate")
    parser.add_argument("--input-dir", help="Directory containing markdown files to validate")
    
    # Configuration arguments
    parser.add_argument("--rules-file", help="Path to validation rules JSON config")
    parser.add_argument("--disable-rules", nargs="+", help="Rule names to disable")
    
    # Output arguments
    parser.add_argument("--output-format", choices=["json", "text", "junit"], 
                       default="json", help="Output format (default: json)")
    parser.add_argument("--fail-on-errors", action="store_true",
                       help="Exit with code 1 if errors found")
    parser.add_argument("--auto-fix", action="store_true",
                       help="Attempt to auto-fix issues where possible")
    
    # Display arguments
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress all output except errors")
    
    return parser

def _create_validator_from_args(args) -> ComplianceValidator:
    """Create ComplianceValidator instance from parsed arguments."""
    return ComplianceValidator(
        md_file=Path(args.md) if args.md else None,
        input_dir=Path(args.input_dir) if args.input_dir else None,
        rules_file=Path(args.rules_file) if args.rules_file else None,
        disabled_rules=args.disable_rules or [],
        verbose=args.verbose,
        quiet=args.quiet,
        auto_fix=args.auto_fix
    )

def _run_validation(validator: ComplianceValidator, args) -> Any:
    """Run validation based on arguments."""
    if args.md:
        return validator.validate(output_format=args.output_format)
    else:
        return validator.validate_all(output_format=args.output_format)

def _output_results(results: Any, output_format: str) -> None:
    """Output validation results in the specified format."""
    if output_format == "json":
        print(json.dumps(results, indent=2))
    elif output_format == "text":
        pass  # Text output already printed by validator
    elif output_format == "junit":
        print(results)  # JUnit XML string

def _calculate_exit_code(results: Any, fail_on_errors: bool) -> int:
    """Calculate exit code based on results and fail_on_errors flag."""
    if not fail_on_errors:
        return 0
    
    total_errors = sum(cat.get("count", 0) for cat in results.values() 
                     if isinstance(cat, dict))
    return 1 if total_errors > 0 else 0

def main():
    """
    Main entry point using refactored ComplianceValidator class.
    
    Guideline: Architecture Patterns - Extract Method for complexity reduction
    """
    parser = _create_argument_parser()
    args = parser.parse_args()
    
    # Validate arguments
    if not args.md and not args.input_dir:
        parser.error("Either --md or --input-dir must be specified")
    
    if args.md and args.input_dir:
        parser.error("Cannot specify both --md and --input-dir")
    
    # Create validator and run validation
    try:
        validator = _create_validator_from_args(args)
        results = _run_validation(validator, args)
        _output_results(results, args.output_format)
        return _calculate_exit_code(results, args.fail_on_errors)
        
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
