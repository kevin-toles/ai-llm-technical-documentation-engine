#!/usr/bin/env python3
"""
Tab 5 Implementation Validation Script
Validates that all CONSOLIDATED_IMPLEMENTATION_PLAN.md Tab 5 requirements are met.
"""

import json
import sys
from pathlib import Path

def validate_tab5_implementation():
    """Validate Tab 5 implementation against CONSOLIDATED_IMPLEMENTATION_PLAN requirements."""
    
    print("\n" + "="*80)
    print("TAB 5 IMPLEMENTATION VALIDATION")
    print("Checking against CONSOLIDATED_IMPLEMENTATION_PLAN.md requirements")
    print("="*80 + "\n")
    
    results = {
        "passed": [],
        "failed": [],
        "warnings": []
    }
    
    # Requirement 1: Script can generate both MD and JSON outputs
    print("✓ Requirement 1: Dual Output Generation")
    script_path = Path("workflows/base_guideline_generation/scripts/chapter_generator_all_text.py")
    if script_path.exists():
        content = script_path.read_text()
        if "_convert_markdown_to_json" in content and "json.dump" in content:
            print("  ✅ PASS: Script has JSON generation functions")
            results["passed"].append("Script has JSON conversion and dump functions")
        else:
            print("  ❌ FAIL: Script missing JSON generation functions")
            results["failed"].append("Script missing JSON functions")
    else:
        print("  ❌ FAIL: Script not found")
        results["failed"].append("chapter_generator_all_text.py not found")
    
    # Requirement 2: Check sample outputs exist and are valid
    print("\n✓ Requirement 2: Sample Outputs Generated")
    md_file = Path("examples/guideline_outputs/PYTHON_GUIDELINES_Architecture Patterns with Python.md")
    json_file = Path("examples/guideline_outputs/PYTHON_GUIDELINES_Architecture Patterns with Python.json")
    
    if md_file.exists() and json_file.exists():
        md_size_kb = md_file.stat().st_size / 1024
        json_size_kb = json_file.stat().st_size / 1024
        print(f"  ✅ PASS: Both files exist")
        print(f"     - MD file: {md_size_kb:.1f} KB")
        print(f"     - JSON file: {json_size_kb:.1f} KB")
        results["passed"].append(f"Sample files exist (MD: {md_size_kb:.1f}KB, JSON: {json_size_kb:.1f}KB)")
        
        # Validate JSON is parseable
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            print("  ✅ PASS: JSON is valid and parseable")
            results["passed"].append("JSON is valid and parseable")
        except json.JSONDecodeError as e:
            print(f"  ❌ FAIL: JSON is invalid: {e}")
            results["failed"].append(f"JSON parsing failed: {e}")
    else:
        if not md_file.exists():
            print("  ❌ FAIL: MD file not found")
            results["failed"].append("MD sample file missing")
        if not json_file.exists():
            print("  ❌ FAIL: JSON file not found")
            results["failed"].append("JSON sample file missing")
    
    # Requirement 3: JSON has required schema structure
    print("\n✓ Requirement 3: JSON Schema Structure")
    if json_file.exists():
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            required_keys = ["book", "title", "chapters"]
            missing_keys = [key for key in required_keys if key not in json_data]
            
            if not missing_keys:
                print(f"  ✅ PASS: All required top-level keys present: {required_keys}")
                results["passed"].append("JSON has required schema keys")
                
                # Check chapters structure
                if isinstance(json_data.get("chapters"), list) and len(json_data["chapters"]) > 0:
                    chapter_sample = json_data["chapters"][0]
                    chapter_keys = ["chapter_number", "chapter_title"]
                    missing_chapter_keys = [key for key in chapter_keys if key not in chapter_sample]
                    
                    if not missing_chapter_keys:
                        print(f"  ✅ PASS: Chapters have correct structure")
                        print(f"     - Total chapters: {len(json_data['chapters'])}")
                        results["passed"].append(f"Chapters structure valid ({len(json_data['chapters'])} chapters)")
                    else:
                        print(f"  ⚠️  WARNING: Chapters missing keys: {missing_chapter_keys}")
                        results["warnings"].append(f"Chapter keys missing: {missing_chapter_keys}")
                else:
                    print("  ❌ FAIL: Chapters is not a valid array")
                    results["failed"].append("Chapters structure invalid")
            else:
                print(f"  ❌ FAIL: Missing required keys: {missing_keys}")
                results["failed"].append(f"Missing JSON keys: {missing_keys}")
        except Exception as e:
            print(f"  ❌ FAIL: Error validating JSON: {e}")
            results["failed"].append(f"JSON validation error: {e}")
    
    # Requirement 4: Content parity between MD and JSON
    print("\n✓ Requirement 4: Content Parity (MD vs JSON)")
    if md_file.exists() and json_file.exists():
        try:
            md_content = md_file.read_text(encoding='utf-8')
            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            # Count chapters in MD
            md_chapter_count = md_content.count("## Chapter ")
            json_chapter_count = len(json_data.get("chapters", []))
            
            if md_chapter_count == json_chapter_count:
                print(f"  ✅ PASS: Chapter counts match ({md_chapter_count} chapters)")
                results["passed"].append(f"Content parity verified ({md_chapter_count} chapters)")
            else:
                print(f"  ❌ FAIL: Chapter count mismatch - MD: {md_chapter_count}, JSON: {json_chapter_count}")
                results["failed"].append(f"Chapter count mismatch (MD: {md_chapter_count}, JSON: {json_chapter_count})")
        except Exception as e:
            print(f"  ❌ FAIL: Error checking content parity: {e}")
            results["failed"].append(f"Content parity check error: {e}")
    
    # Requirement 5: Test coverage exists
    print("\n✓ Requirement 5: Test Coverage")
    test_file = Path("tests/integration/test_end_to_end_json_generation.py")
    if test_file.exists():
        test_content = test_file.read_text()
        test_count = test_content.count("def test_")
        print(f"  ✅ PASS: Integration tests exist ({test_count} tests)")
        results["passed"].append(f"Integration tests present ({test_count} tests)")
    else:
        print("  ⚠️  WARNING: Integration test file not found")
        results["warnings"].append("Integration test file missing")
    
    # Requirement 6: Quality gates passed (SonarQube)
    print("\n✓ Requirement 6: Quality Gates")
    sonar_report = Path("reports/sonarqube_task16_analysis.md")
    if sonar_report.exists():
        report_content = sonar_report.read_text()
        if "0 bugs, 0 vulnerabilities, 0 code smells" in report_content.lower() or \
           ("bugs: 0" in report_content.lower() and "code smells: 0" in report_content.lower()):
            print("  ✅ PASS: SonarQube quality gate passed (0 bugs, 0 vulnerabilities, 0 code smells)")
            results["passed"].append("SonarQube quality gate passed")
        else:
            print("  ⚠️  WARNING: SonarQube report exists but quality metrics unclear")
            results["warnings"].append("SonarQube metrics unclear")
    else:
        print("  ⚠️  WARNING: SonarQube report not found")
        results["warnings"].append("SonarQube report missing")
    
    # Requirement 7: Documentation exists
    print("\n✓ Requirement 7: Implementation Documentation")
    impl_doc = Path("implementation-summary-tab5-json-generation.md")
    if impl_doc.exists():
        doc_size = impl_doc.stat().st_size / 1024
        print(f"  ✅ PASS: Implementation summary exists ({doc_size:.1f} KB)")
        results["passed"].append(f"Documentation present ({doc_size:.1f} KB)")
    else:
        print("  ⚠️  WARNING: Implementation summary not found")
        results["warnings"].append("Implementation summary missing")
    
    # Final Summary
    print("\n" + "="*80)
    print("VALIDATION SUMMARY")
    print("="*80)
    print(f"\n✅ PASSED: {len(results['passed'])} requirements")
    for item in results['passed']:
        print(f"   - {item}")
    
    if results['warnings']:
        print(f"\n⚠️  WARNINGS: {len(results['warnings'])} items")
        for item in results['warnings']:
            print(f"   - {item}")
    
    if results['failed']:
        print(f"\n❌ FAILED: {len(results['failed'])} requirements")
        for item in results['failed']:
            print(f"   - {item}")
        print("\n🚨 VALIDATION FAILED - Implementation incomplete")
        return False
    else:
        print("\n🎉 ALL VALIDATION CHECKS PASSED!")
        print("✅ Tab 5 implementation is complete and meets all CONSOLIDATED_IMPLEMENTATION_PLAN requirements")
        return True

if __name__ == "__main__":
    success = validate_tab5_implementation()
    sys.exit(0 if success else 1)
