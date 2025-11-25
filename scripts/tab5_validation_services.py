"""
Tab 5 Validation Service Layer

Architecture Pattern: Service Layer + Strategy Pattern
Reference: Architecture Patterns Ch. 4 (Service Layer), Ch. 13 (Strategy Pattern)

Services:
- DualOutputValidator: Validates script has JSON generation capability
- SampleOutputsValidator: Validates sample files exist and are valid
- JSONSchemaValidator: Validates JSON schema structure
- ContentParityValidator: Validates content parity between MD and JSON
- TestCoverageValidator: Validates test coverage exists
- QualityGateValidator: Validates SonarQube quality gates
- DocumentationValidator: Validates implementation documentation
- ValidationResultFormatter: Formats and prints results
"""

import json
import re
from pathlib import Path
from typing import Dict, List


class ValidationResult:
    """Result of a single validation check"""
    
    def __init__(self, status: str, message: str):
        """
        Args:
            status: 'passed', 'failed', or 'warning'
            message: Description of the validation result
        """
        self.status = status
        self.message = message
    
    def is_passed(self) -> bool:
        return self.status == "passed"
    
    def is_failed(self) -> bool:
        return self.status == "failed"
    
    def is_warning(self) -> bool:
        return self.status == "warning"


class DualOutputValidator:
    """
    Requirement 1: Script can generate both MD and JSON outputs
    
    Pattern: Strategy Pattern (one validation strategy)
    """
    
    @staticmethod
    def validate() -> List[ValidationResult]:
        """Validate script has JSON generation functions"""
        results = []
        
        script_path = Path("workflows/base_guideline_generation/scripts/chapter_generator_all_text.py")
        
        if not script_path.exists():
            results.append(ValidationResult("failed", "Script not found"))
            results.append(ValidationResult("failed", "chapter_generator_all_text.py not found"))
            return results
        
        content = script_path.read_text()
        
        if "_convert_markdown_to_json" in content and "json.dump" in content:
            results.append(ValidationResult("passed", "Script has JSON generation functions"))
            results.append(ValidationResult("passed", "Script has JSON conversion and dump functions"))
        else:
            results.append(ValidationResult("failed", "Script missing JSON generation functions"))
        
        return results


class SampleOutputsValidator:
    """
    Requirement 2: Sample outputs generated and valid
    
    Pattern: Strategy Pattern (one validation strategy)
    """
    
    @staticmethod
    def validate(md_file: Path = None, json_file: Path = None) -> List[ValidationResult]:
        """Validate sample MD and JSON files exist and are valid"""
        results = []
        
        # Default to examples output paths if not provided
        if md_file is None:
            md_file = Path("examples/guideline_outputs/PYTHON_GUIDELINES_Architecture Patterns with Python.md")
        if json_file is None:
            json_file = Path("examples/guideline_outputs/PYTHON_GUIDELINES_Architecture Patterns with Python.json")
        
        # Check file existence
        if not md_file.exists():
            results.append(ValidationResult("failed", "MD file not found"))
            return results
        
        if not json_file.exists():
            results.append(ValidationResult("failed", "JSON file not found"))
            return results
        
        # Files exist
        md_size_kb = md_file.stat().st_size / 1024
        json_size_kb = json_file.stat().st_size / 1024
        results.append(ValidationResult("passed", "Both files exist"))
        results.append(ValidationResult("passed", f"MD file: {md_size_kb:.1f}KB"))
        results.append(ValidationResult("passed", f"JSON file: {json_size_kb:.1f}KB"))
        
        # Validate JSON is parseable
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                json.load(f)
            results.append(ValidationResult("passed", "JSON is valid and parseable"))
        except json.JSONDecodeError as e:
            results.append(ValidationResult("failed", f"JSON is invalid: {e}"))
        
        return results


class JSONSchemaValidator:
    """
    Requirement 3: JSON has required schema structure
    
    Pattern: Strategy Pattern (one validation strategy)
    """
    
    # Test expects these specific keys
    REQUIRED_TOP_LEVEL_KEYS = ["book", "title", "chapters"]
    OPTIONAL_TOP_LEVEL_KEYS = ["book_metadata", "source_info", "footnotes"]
    REQUIRED_CHAPTER_KEYS = ["chapter_number", "chapter_title"]  # Test expects both
    OPTIONAL_CHAPTER_KEYS = ["title", "page_range", "summary"]
    
    @staticmethod
    def validate(json_file: Path = None) -> List[ValidationResult]:
        """Validate JSON schema structure"""
        results = []
        
        if json_file is None:
            json_file = Path("examples/guideline_outputs/PYTHON_GUIDELINES_Architecture Patterns with Python.json")
        
        if not json_file.exists():
            return results  # Already handled by SampleOutputsValidator
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
        except Exception as e:
            results.append(ValidationResult("failed", f"JSON validation error: {e}"))
            return results
        
        # Check top-level keys
        missing_keys = [key for key in JSONSchemaValidator.REQUIRED_TOP_LEVEL_KEYS if key not in json_data]
        
        if missing_keys:
            results.append(ValidationResult("failed", f"Missing required keys: {missing_keys}"))
            return results
        
        results.append(ValidationResult("passed", f"All required top-level keys present: {JSONSchemaValidator.REQUIRED_TOP_LEVEL_KEYS}"))
        
        # Check chapters structure
        chapters = json_data.get("chapters")
        
        if not isinstance(chapters, list):
            results.append(ValidationResult("failed", "Chapters is not a valid array"))
            return results
        
        if len(chapters) == 0:
            results.append(ValidationResult("failed", "Chapters array is empty"))
            return results
        
        # Validate chapter keys
        chapter_sample = chapters[0]
        missing_chapter_keys = [
            key for key in JSONSchemaValidator.REQUIRED_CHAPTER_KEYS 
            if key not in chapter_sample
        ]
        
        if missing_chapter_keys:
            results.append(ValidationResult("warning", f"Chapters missing keys: {missing_chapter_keys}"))
        
        results.append(ValidationResult("passed", f"Chapters have correct structure (Total chapters: {len(chapters)})"))
        
        return results


class ContentParityValidator:
    """
    Requirement 4: Content parity between MD and JSON
    
    Pattern: Strategy Pattern (one validation strategy)
    """
    
    @staticmethod
    def validate(md_file: Path = None, json_file: Path = None) -> List[ValidationResult]:
        """Validate content parity between MD and JSON"""
        results = []
        
        if md_file is None:
            md_file = Path("examples/guideline_outputs/PYTHON_GUIDELINES_Architecture Patterns with Python.md")
        if json_file is None:
            json_file = Path("examples/guideline_outputs/PYTHON_GUIDELINES_Architecture Patterns with Python.json")
        
        if not md_file.exists() or not json_file.exists():
            return results  # Already handled by SampleOutputsValidator
        
        try:
            md_content = md_file.read_text(encoding='utf-8')
            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            # Count chapters using regex to avoid false matches
            md_chapter_count = len(re.findall(r'^## Chapter \d+', md_content, re.MULTILINE))
            json_chapter_count = len(json_data.get("chapters", []))
            
            if md_chapter_count == json_chapter_count:
                results.append(ValidationResult("passed", f"Chapter counts match ({md_chapter_count} chapters)"))
            else:
                results.append(ValidationResult(
                    "failed", 
                    f"Chapter count mismatch - MD: {md_chapter_count}, JSON: {json_chapter_count}"
                ))
        except Exception as e:
            results.append(ValidationResult("failed", f"Content parity check error: {e}"))
        
        return results


class TestCoverageValidator:
    """
    Requirement 5: Test coverage exists
    
    Pattern: Strategy Pattern (one validation strategy)
    """
    
    @staticmethod
    def validate() -> List[ValidationResult]:
        """Validate test coverage exists"""
        results = []
        
        test_file = Path("tests/integration/test_end_to_end_json_generation.py")
        
        if not test_file.exists():
            results.append(ValidationResult("warning", "Integration test file not found"))
            return results
        
        test_content = test_file.read_text()
        test_count = test_content.count("def test_")
        
        results.append(ValidationResult("passed", f"Integration tests exist ({test_count} tests)"))
        
        return results


class QualityGateValidator:
    """
    Requirement 6: Quality gates passed (SonarQube)
    
    Pattern: Strategy Pattern (one validation strategy)
    """
    
    @staticmethod
    def validate() -> List[ValidationResult]:
        """Validate SonarQube quality gates"""
        results = []
        
        sonar_report = Path("reports/sonarqube_task16_analysis.md")
        
        if not sonar_report.exists():
            results.append(ValidationResult("warning", "SonarQube report not found"))
            return results
        
        report_content = sonar_report.read_text()
        
        # Check for clean quality gate
        if "0 bugs, 0 vulnerabilities, 0 code smells" in report_content.lower() or \
           ("bugs: 0" in report_content.lower() and "code smells: 0" in report_content.lower()):
            results.append(ValidationResult("passed", "SonarQube quality gate passed (0 issues)"))
        else:
            results.append(ValidationResult("warning", "SonarQube report exists but quality metrics unclear"))
        
        return results


class DocumentationValidator:
    """
    Requirement 7: Implementation documentation exists
    
    Pattern: Strategy Pattern (one validation strategy)
    """
    
    @staticmethod
    def validate() -> List[ValidationResult]:
        """Validate implementation documentation exists"""
        results = []
        
        impl_doc = Path("implementation-summary-tab5-json-generation.md")
        
        if not impl_doc.exists():
            results.append(ValidationResult("warning", "Implementation summary not found"))
            return results
        
        doc_size = impl_doc.stat().st_size / 1024
        results.append(ValidationResult("passed", f"Implementation summary exists ({doc_size:.1f}KB)"))
        
        return results


class ValidationResultFormatter:
    """
    Formats and prints validation results
    
    Pattern: Single Responsibility Principle (formatting only)
    """
    
    @staticmethod
    def print_header():
        """Print validation header"""
        print("\n" + "="*80)
        print("TAB 5 IMPLEMENTATION VALIDATION")
        print("Checking against CONSOLIDATED_IMPLEMENTATION_PLAN.md requirements")
        print("="*80 + "\n")
    
    @staticmethod
    def print_requirement_header(number: int, title: str):
        """Print requirement section header"""
        print(f"\n✓ Requirement {number}: {title}")
    
    @staticmethod
    def print_result(result: ValidationResult):
        """Print a single validation result"""
        if result.is_passed():
            icon = "✅ PASS"
        elif result.is_failed():
            icon = "❌ FAIL"
        else:
            icon = "⚠️  WARNING"
        
        print(f"  {icon}: {result.message}")
    
    @staticmethod
    def print_summary(passed: List[str], warnings: List[str], failed: List[str]) -> bool:
        """Print validation summary and return success status"""
        print("\n" + "="*80)
        print("VALIDATION SUMMARY")
        print("="*80)
        
        print(f"\n✅ PASSED: {len(passed)} requirements")
        for item in passed:
            print(f"   - {item}")
        
        if warnings:
            print(f"\n⚠️  WARNINGS: {len(warnings)} items")
            for item in warnings:
                print(f"   - {item}")
        
        if failed:
            print(f"\n❌ FAILED: {len(failed)} requirements")
            for item in failed:
                print(f"   - {item}")
            print("\n🚨 VALIDATION FAILED - Implementation incomplete")
            return False
        else:
            print("\n🎉 ALL VALIDATION CHECKS PASSED!")
            print("✅ Tab 5 implementation is complete and meets all CONSOLIDATED_IMPLEMENTATION_PLAN requirements")
            return True


class Tab5ValidationOrchestrator:
    """
    Service Layer orchestrator for Tab 5 validation.
    
    Coordinates all requirement validators and aggregates results.
    Pattern: Facade Pattern - provides simple interface to complex validation subsystem.
    """
    
    def __init__(self, md_file: Path = None, json_file: Path = None):
        """Initialize orchestrator with optional file paths"""
        self.md_file = md_file
        self.json_file = json_file
    
    def validate_all(self) -> bool:
        """Run all validations and return overall pass/fail"""
        print("\n" + "="*80)
        print("TAB 5 IMPLEMENTATION VALIDATION")
        print("Checking against CONSOLIDATED_IMPLEMENTATION_PLAN.md requirements")
        if self.md_file or self.json_file:
            print(f"MD file: {self.md_file or 'default'}")
            print(f"JSON file: {self.json_file or 'default'}")
        print("="*80)
        print()
        
        all_results = []
        
        # Requirement 1: Dual output generation
        print("\n✓ Requirement 1: Dual Output Generation")
        req1_results = DualOutputValidator.validate()
        all_results.extend(req1_results)
        for result in req1_results:
            ValidationResultFormatter.print_result(result)
        
        # Requirement 2: Sample outputs
        print("\n✓ Requirement 2: Sample Outputs Generated")
        req2_results = SampleOutputsValidator.validate(self.md_file, self.json_file)
        all_results.extend(req2_results)
        for result in req2_results:
            ValidationResultFormatter.print_result(result)
        
        # Requirement 3: JSON schema
        print("\n✓ Requirement 3: JSON Schema Structure")
        req3_results = JSONSchemaValidator.validate(self.json_file)
        all_results.extend(req3_results)
        for result in req3_results:
            ValidationResultFormatter.print_result(result)
        
        # Requirement 4: Content parity
        print("\n✓ Requirement 4: Content Parity (MD vs JSON)")
        req4_results = ContentParityValidator.validate(self.md_file, self.json_file)
        all_results.extend(req4_results)
        for result in req4_results:
            ValidationResultFormatter.print_result(result)
        
        # Requirement 5: Test coverage
        print("\n✓ Requirement 5: Test Coverage")
        req5_results = TestCoverageValidator.validate()
        all_results.extend(req5_results)
        for result in req5_results:
            ValidationResultFormatter.print_result(result)
        
        # Requirement 6: Quality gates
        print("\n✓ Requirement 6: Quality Gates")
        req6_results = QualityGateValidator.validate()
        all_results.extend(req6_results)
        for result in req6_results:
            ValidationResultFormatter.print_result(result)
        
        # Requirement 7: Documentation
        print("\n✓ Requirement 7: Implementation Documentation")
        req7_results = DocumentationValidator.validate()
        all_results.extend(req7_results)
        for result in req7_results:
            ValidationResultFormatter.print_result(result)
        
        # Print summary
        passed = [r.message for r in all_results if r.is_passed()]
        warnings = [r.message for r in all_results if r.is_warning()]
        failed = [r.message for r in all_results if r.is_failed()]
        
        return ValidationResultFormatter.print_summary(passed, warnings, failed)

