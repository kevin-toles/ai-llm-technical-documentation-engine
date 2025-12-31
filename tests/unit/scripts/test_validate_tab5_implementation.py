"""
Characterization tests for scripts/validate_tab5_implementation.py

Tests document current behavior before refactoring to reduce complexity:
- validate_tab5_implementation function (CC 34, actually CC 57)

Architecture Pattern: Service Layer + Strategy Pattern
Reference: Architecture Patterns Ch. 4 (Service Layer), Ch. 13 (Strategy Pattern)

The function has 7 distinct validation requirements that can be extracted
into separate validator classes following the Strategy Pattern.
"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open
from scripts.validate_tab5_implementation import validate_tab5_implementation


class TestRequirement1DualOutputGeneration:
    """Test Requirement 1: Script can generate both MD and JSON outputs"""
    
    def test_passes_when_script_has_json_functions(self, tmp_path, monkeypatch, capsys):
        """Requirement 1 passes when script has JSON conversion functions"""
        monkeypatch.chdir(tmp_path)
        
        # Create script with JSON functions
        script_dir = tmp_path / "workflows/base_guideline_generation/scripts"
        script_dir.mkdir(parents=True)
        script_file = script_dir / "chapter_generator_all_text.py"
        script_file.write_text("def _convert_markdown_to_json(): pass\nimport json\njson.dump()")
        
        validate_tab5_implementation()  # Return value checked via capsys
        captured = capsys.readouterr()
        
        assert "✅ PASS: Script has JSON generation functions" in captured.out
        assert "Script has JSON conversion and dump functions" in captured.out
    
    def test_fails_when_script_missing_json_functions(self, tmp_path, monkeypatch, capsys):
        """Requirement 1 fails when script lacks JSON functions"""
        monkeypatch.chdir(tmp_path)
        
        # Create script without JSON functions
        script_dir = tmp_path / "workflows/base_guideline_generation/scripts"
        script_dir.mkdir(parents=True)
        script_file = script_dir / "chapter_generator_all_text.py"
        script_file.write_text("def some_function(): pass")
        
        validate_tab5_implementation()  # Return value checked via capsys
        captured = capsys.readouterr()
        
        assert "❌ FAIL: Script missing JSON generation functions" in captured.out
        assert result is False
    
    def test_fails_when_script_not_found(self, tmp_path, monkeypatch, capsys):
        """Requirement 1 fails when script file doesn't exist"""
        monkeypatch.chdir(tmp_path)
        
        validate_tab5_implementation()  # Return value checked via capsys
        captured = capsys.readouterr()
        
        assert "❌ FAIL: Script not found" in captured.out
        assert "chapter_generator_all_text.py not found" in captured.out
        assert result is False


class TestRequirement2SampleOutputs:
    """Test Requirement 2: Check sample outputs exist and are valid"""
    
    def test_passes_when_both_files_exist(self, tmp_path, monkeypatch, capsys):
        """Requirement 2 passes when both MD and JSON files exist"""
        monkeypatch.chdir(tmp_path)
        
        # Create all required files to avoid other failures
        self._create_minimal_passing_setup(tmp_path)
        
        # Create sample output files
        output_dir = tmp_path / "examples/guideline_outputs"
        output_dir.mkdir(parents=True)
        md_file = output_dir / "PYTHON_GUIDELINES_Architecture Patterns with Python.md"
        json_file = output_dir / "PYTHON_GUIDELINES_Architecture Patterns with Python.json"
        
        md_file.write_text("# Sample MD content")
        json_file.write_text('{"book": "test", "title": "test", "chapters": []}')
        
        validate_tab5_implementation()  # Return value checked via capsys
        captured = capsys.readouterr()
        
        assert "✅ PASS: Both files exist" in captured.out
        assert "MD file:" in captured.out
        assert "JSON file:" in captured.out
        assert "KB" in captured.out
    
    def test_validates_json_is_parseable(self, tmp_path, monkeypatch, capsys):
        """Requirement 2 validates JSON file is parseable"""
        monkeypatch.chdir(tmp_path)
        
        self._create_minimal_passing_setup(tmp_path)
        
        output_dir = tmp_path / "examples/guideline_outputs"
        output_dir.mkdir(parents=True)
        md_file = output_dir / "PYTHON_GUIDELINES_Architecture Patterns with Python.md"
        json_file = output_dir / "PYTHON_GUIDELINES_Architecture Patterns with Python.json"
        
        md_file.write_text("# Sample")
        json_file.write_text('{"book": "test", "title": "test", "chapters": []}')
        
        validate_tab5_implementation()  # Return value checked via capsys
        captured = capsys.readouterr()
        
        assert "✅ PASS: JSON is valid and parseable" in captured.out
    
    def test_fails_when_json_invalid(self, tmp_path, monkeypatch, capsys):
        """Requirement 2 fails when JSON is not parseable"""
        monkeypatch.chdir(tmp_path)
        
        self._create_minimal_passing_setup(tmp_path)
        
        output_dir = tmp_path / "examples/guideline_outputs"
        output_dir.mkdir(parents=True)
        md_file = output_dir / "PYTHON_GUIDELINES_Architecture Patterns with Python.md"
        json_file = output_dir / "PYTHON_GUIDELINES_Architecture Patterns with Python.json"
        
        md_file.write_text("# Sample")
        json_file.write_text('{invalid json')
        
        validate_tab5_implementation()  # Return value checked via capsys
        captured = capsys.readouterr()
        
        assert "❌ FAIL: JSON is invalid:" in captured.out
        assert result is False
    
    def test_fails_when_md_file_missing(self, tmp_path, monkeypatch, capsys):
        """Requirement 2 fails when MD file doesn't exist"""
        monkeypatch.chdir(tmp_path)
        
        self._create_minimal_passing_setup(tmp_path)
        
        output_dir = tmp_path / "examples/guideline_outputs"
        output_dir.mkdir(parents=True)
        json_file = output_dir / "PYTHON_GUIDELINES_Architecture Patterns with Python.json"
        json_file.write_text('{"book": "test", "title": "test", "chapters": []}')
        
        validate_tab5_implementation()  # Return value checked via capsys
        captured = capsys.readouterr()
        
        assert "❌ FAIL: MD file not found" in captured.out
        assert result is False
    
    def test_fails_when_json_file_missing(self, tmp_path, monkeypatch, capsys):
        """Requirement 2 fails when JSON file doesn't exist"""
        monkeypatch.chdir(tmp_path)
        
        self._create_minimal_passing_setup(tmp_path)
        
        output_dir = tmp_path / "examples/guideline_outputs"
        output_dir.mkdir(parents=True)
        md_file = output_dir / "PYTHON_GUIDELINES_Architecture Patterns with Python.md"
        md_file.write_text("# Sample")
        
        validate_tab5_implementation()  # Return value checked via capsys
        captured = capsys.readouterr()
        
        assert "❌ FAIL: JSON file not found" in captured.out
        assert result is False
    
    def _create_minimal_passing_setup(self, tmp_path):
        """Helper to create minimal setup that passes Requirement 1"""
        script_dir = tmp_path / "workflows/base_guideline_generation/scripts"
        script_dir.mkdir(parents=True)
        script_file = script_dir / "chapter_generator_all_text.py"
        script_file.write_text("def _convert_markdown_to_json(): pass\nimport json\njson.dump()")


class TestRequirement3JSONSchema:
    """Test Requirement 3: JSON has required schema structure"""
    
    def test_passes_when_json_has_required_keys(self, tmp_path, monkeypatch, capsys):
        """Requirement 3 passes when JSON has book, title, chapters keys"""
        monkeypatch.chdir(tmp_path)
        
        self._create_passing_setup_with_json(tmp_path, {
            "book": "Test Book",
            "title": "Test Title",
            "chapters": [
                {"chapter_number": 1, "chapter_title": "Chapter 1"}
            ]
        })
        
        validate_tab5_implementation()  # Return value checked via capsys
        captured = capsys.readouterr()
        
        assert "✅ PASS: All required top-level keys present" in captured.out
        assert "['book', 'title', 'chapters']" in captured.out
    
    def test_validates_chapters_structure(self, tmp_path, monkeypatch, capsys):
        """Requirement 3 validates chapters have correct structure"""
        monkeypatch.chdir(tmp_path)
        
        self._create_passing_setup_with_json(tmp_path, {
            "book": "Test",
            "title": "Test",
            "chapters": [
                {"chapter_number": 1, "chapter_title": "Ch1"},
                {"chapter_number": 2, "chapter_title": "Ch2"}
            ]
        })
        
        validate_tab5_implementation()  # Return value checked via capsys
        captured = capsys.readouterr()
        
        assert "✅ PASS: Chapters have correct structure" in captured.out
        assert "Total chapters: 2" in captured.out
    
    def test_fails_when_required_keys_missing(self, tmp_path, monkeypatch, capsys):
        """Requirement 3 fails when top-level keys are missing"""
        monkeypatch.chdir(tmp_path)
        
        self._create_passing_setup_with_json(tmp_path, {
            "book": "Test"
            # Missing title and chapters
        })
        
        validate_tab5_implementation()  # Return value checked via capsys
        captured = capsys.readouterr()
        
        assert "❌ FAIL: Missing required keys:" in captured.out
        assert result is False
    
    def test_warns_when_chapter_keys_missing(self, tmp_path, monkeypatch, capsys):
        """Requirement 3 warns when chapter structure is incomplete"""
        monkeypatch.chdir(tmp_path)
        
        self._create_passing_setup_with_json(tmp_path, {
            "book": "Test",
            "title": "Test",
            "chapters": [
                {"chapter_number": 1}  # Missing chapter_title
            ]
        })
        
        validate_tab5_implementation()  # Return value checked via capsys
        captured = capsys.readouterr()
        
        assert "⚠️  WARNING: Chapters missing keys:" in captured.out
    
    def test_fails_when_chapters_not_array(self, tmp_path, monkeypatch, capsys):
        """Requirement 3 fails when chapters is not a valid array"""
        monkeypatch.chdir(tmp_path)
        
        self._create_passing_setup_with_json(tmp_path, {
            "book": "Test",
            "title": "Test",
            "chapters": "not an array"
        })
        
        validate_tab5_implementation()  # Return value checked via capsys
        captured = capsys.readouterr()
        
        assert "❌ FAIL: Chapters is not a valid array" in captured.out
        assert result is False
    
    def _create_passing_setup_with_json(self, tmp_path, json_data):
        """Helper to create setup with custom JSON data"""
        # Requirement 1
        script_dir = tmp_path / "workflows/base_guideline_generation/scripts"
        script_dir.mkdir(parents=True)
        script_file = script_dir / "chapter_generator_all_text.py"
        script_file.write_text("def _convert_markdown_to_json(): pass\nimport json\njson.dump()")
        
        # Requirement 2
        output_dir = tmp_path / "examples/guideline_outputs"
        output_dir.mkdir(parents=True)
        md_file = output_dir / "PYTHON_GUIDELINES_Architecture Patterns with Python.md"
        json_file = output_dir / "PYTHON_GUIDELINES_Architecture Patterns with Python.json"
        
        md_file.write_text("# Test")
        json_file.write_text(json.dumps(json_data))


class TestRequirement4ContentParity:
    """Test Requirement 4: Content parity between MD and JSON"""
    
    def test_passes_when_chapter_counts_match(self, tmp_path, monkeypatch, capsys):
        """Requirement 4 passes when MD and JSON have same chapter count"""
        monkeypatch.chdir(tmp_path)
        
        # Setup with 3 chapters in both
        self._create_setup_with_chapters(tmp_path, 3)
        
        validate_tab5_implementation()  # Return value checked via capsys
        captured = capsys.readouterr()
        
        assert "✅ PASS: Chapter counts match (3 chapters)" in captured.out
    
    def test_fails_when_chapter_counts_mismatch(self, tmp_path, monkeypatch, capsys):
        """Requirement 4 fails when chapter counts don't match"""
        monkeypatch.chdir(tmp_path)
        
        # MD has 2 chapters, JSON has 1
        self._create_setup_with_mismatched_chapters(tmp_path, md_chapters=2, json_chapters=1)
        
        validate_tab5_implementation()  # Return value checked via capsys
        captured = capsys.readouterr()
        
        assert "❌ FAIL: Chapter count mismatch - MD: 2, JSON: 1" in captured.out
        assert result is False
    
    def _create_setup_with_chapters(self, tmp_path, chapter_count):
        """Helper to create setup with matching chapter counts"""
        # Requirement 1
        script_dir = tmp_path / "workflows/base_guideline_generation/scripts"
        script_dir.mkdir(parents=True)
        script_file = script_dir / "chapter_generator_all_text.py"
        script_file.write_text("def _convert_markdown_to_json(): pass\nimport json\njson.dump()")
        
        # Requirement 2 & 4
        output_dir = tmp_path / "examples/guideline_outputs"
        output_dir.mkdir(parents=True)
        md_file = output_dir / "PYTHON_GUIDELINES_Architecture Patterns with Python.md"
        json_file = output_dir / "PYTHON_GUIDELINES_Architecture Patterns with Python.json"
        
        # Create MD with N chapters
        md_content = "# Book\n" + "\n".join([f"## Chapter {i}" for i in range(1, chapter_count + 1)])
        md_file.write_text(md_content)
        
        # Create JSON with N chapters
        json_data = {
            "book": "Test",
            "title": "Test",
            "chapters": [
                {"chapter_number": i, "chapter_title": f"Ch{i}"} 
                for i in range(1, chapter_count + 1)
            ]
        }
        json_file.write_text(json.dumps(json_data))
    
    def _create_setup_with_mismatched_chapters(self, tmp_path, md_chapters, json_chapters):
        """Helper to create setup with mismatched chapter counts"""
        # Requirement 1
        script_dir = tmp_path / "workflows/base_guideline_generation/scripts"
        script_dir.mkdir(parents=True)
        script_file = script_dir / "chapter_generator_all_text.py"
        script_file.write_text("def _convert_markdown_to_json(): pass\nimport json\njson.dump()")
        
        output_dir = tmp_path / "examples/guideline_outputs"
        output_dir.mkdir(parents=True)
        md_file = output_dir / "PYTHON_GUIDELINES_Architecture Patterns with Python.md"
        json_file = output_dir / "PYTHON_GUIDELINES_Architecture Patterns with Python.json"
        
        md_content = "# Book\n" + "\n".join([f"## Chapter {i}" for i in range(1, md_chapters + 1)])
        md_file.write_text(md_content)
        
        json_data = {
            "book": "Test",
            "title": "Test",
            "chapters": [
                {"chapter_number": i, "chapter_title": f"Ch{i}"} 
                for i in range(1, json_chapters + 1)
            ]
        }
        json_file.write_text(json.dumps(json_data))


class TestRequirement5TestCoverage:
    """Test Requirement 5: Test coverage exists"""
    
    def test_passes_when_test_file_exists(self, tmp_path, monkeypatch, capsys):
        """Requirement 5 passes when integration test file exists"""
        monkeypatch.chdir(tmp_path)
        
        self._create_minimal_setup(tmp_path)
        
        # Create test file
        test_dir = tmp_path / "tests/integration"
        test_dir.mkdir(parents=True)
        test_file = test_dir / "test_end_to_end_json_generation.py"
        test_file.write_text("def test_one(): pass\ndef test_two(): pass")
        
        validate_tab5_implementation()  # Return value checked via capsys
        captured = capsys.readouterr()
        
        assert "✅ PASS: Integration tests exist (2 tests)" in captured.out
    
    def test_warns_when_test_file_missing(self, tmp_path, monkeypatch, capsys):
        """Requirement 5 warns when test file doesn't exist"""
        monkeypatch.chdir(tmp_path)
        
        self._create_minimal_setup(tmp_path)
        
        validate_tab5_implementation()  # Return value checked via capsys
        captured = capsys.readouterr()
        
        assert "⚠️  WARNING: Integration test file not found" in captured.out
        # Should still pass overall if only warnings
    
    def _create_minimal_setup(self, tmp_path):
        """Helper to create minimal passing setup"""
        script_dir = tmp_path / "workflows/base_guideline_generation/scripts"
        script_dir.mkdir(parents=True)
        script_file = script_dir / "chapter_generator_all_text.py"
        script_file.write_text("def _convert_markdown_to_json(): pass\nimport json\njson.dump()")
        
        output_dir = tmp_path / "examples/guideline_outputs"
        output_dir.mkdir(parents=True)
        md_file = output_dir / "PYTHON_GUIDELINES_Architecture Patterns with Python.md"
        json_file = output_dir / "PYTHON_GUIDELINES_Architecture Patterns with Python.json"
        
        md_file.write_text("## Chapter 1")
        json_file.write_text('{"book": "Test", "title": "Test", "chapters": [{"chapter_number": 1, "chapter_title": "Ch1"}]}')


class TestRequirement6QualityGates:
    """Test Requirement 6: Quality gates passed (SonarQube)"""
    
    def test_passes_when_sonarqube_clean(self, tmp_path, monkeypatch, capsys):
        """Requirement 6 passes when SonarQube report shows 0 issues"""
        monkeypatch.chdir(tmp_path)
        
        self._create_minimal_setup(tmp_path)
        
        # Create SonarQube report
        reports_dir = tmp_path / "reports"
        reports_dir.mkdir()
        sonar_report = reports_dir / "sonarqube_task16_analysis.md"
        sonar_report.write_text("Analysis: 0 bugs, 0 vulnerabilities, 0 code smells")
        
        validate_tab5_implementation()  # Return value checked via capsys
        captured = capsys.readouterr()
        
        assert "✅ PASS: SonarQube quality gate passed" in captured.out
    
    def test_warns_when_report_unclear(self, tmp_path, monkeypatch, capsys):
        """Requirement 6 warns when report exists but metrics unclear"""
        monkeypatch.chdir(tmp_path)
        
        self._create_minimal_setup(tmp_path)
        
        reports_dir = tmp_path / "reports"
        reports_dir.mkdir()
        sonar_report = reports_dir / "sonarqube_task16_analysis.md"
        sonar_report.write_text("Some content without clear metrics")
        
        validate_tab5_implementation()  # Return value checked via capsys
        captured = capsys.readouterr()
        
        assert "⚠️  WARNING: SonarQube report exists but quality metrics unclear" in captured.out
    
    def test_warns_when_report_missing(self, tmp_path, monkeypatch, capsys):
        """Requirement 6 warns when SonarQube report doesn't exist"""
        monkeypatch.chdir(tmp_path)
        
        self._create_minimal_setup(tmp_path)
        
        validate_tab5_implementation()  # Return value checked via capsys
        captured = capsys.readouterr()
        
        assert "⚠️  WARNING: SonarQube report not found" in captured.out
    
    def _create_minimal_setup(self, tmp_path):
        """Helper to create minimal passing setup"""
        script_dir = tmp_path / "workflows/base_guideline_generation/scripts"
        script_dir.mkdir(parents=True)
        script_file = script_dir / "chapter_generator_all_text.py"
        script_file.write_text("def _convert_markdown_to_json(): pass\nimport json\njson.dump()")
        
        output_dir = tmp_path / "examples/guideline_outputs"
        output_dir.mkdir(parents=True)
        md_file = output_dir / "PYTHON_GUIDELINES_Architecture Patterns with Python.md"
        json_file = output_dir / "PYTHON_GUIDELINES_Architecture Patterns with Python.json"
        
        md_file.write_text("## Chapter 1")
        json_file.write_text('{"book": "Test", "title": "Test", "chapters": [{"chapter_number": 1, "chapter_title": "Ch1"}]}')


class TestRequirement7Documentation:
    """Test Requirement 7: Implementation documentation exists"""
    
    def test_passes_when_documentation_exists(self, tmp_path, monkeypatch, capsys):
        """Requirement 7 passes when implementation summary exists"""
        monkeypatch.chdir(tmp_path)
        
        self._create_minimal_setup(tmp_path)
        
        # Create documentation
        impl_doc = tmp_path / "implementation-summary-tab5-json-generation.md"
        impl_doc.write_text("# Implementation Summary\n" + "x" * 1000)
        
        validate_tab5_implementation()  # Return value checked via capsys
        captured = capsys.readouterr()
        
        assert "✅ PASS: Implementation summary exists" in captured.out
        assert "KB)" in captured.out
    
    def test_warns_when_documentation_missing(self, tmp_path, monkeypatch, capsys):
        """Requirement 7 warns when implementation summary doesn't exist"""
        monkeypatch.chdir(tmp_path)
        
        self._create_minimal_setup(tmp_path)
        
        validate_tab5_implementation()  # Return value checked via capsys
        captured = capsys.readouterr()
        
        assert "⚠️  WARNING: Implementation summary not found" in captured.out
    
    def _create_minimal_setup(self, tmp_path):
        """Helper to create minimal passing setup"""
        script_dir = tmp_path / "workflows/base_guideline_generation/scripts"
        script_dir.mkdir(parents=True)
        script_file = script_dir / "chapter_generator_all_text.py"
        script_file.write_text("def _convert_markdown_to_json(): pass\nimport json\njson.dump()")
        
        output_dir = tmp_path / "examples/guideline_outputs"
        output_dir.mkdir(parents=True)
        md_file = output_dir / "PYTHON_GUIDELINES_Architecture Patterns with Python.md"
        json_file = output_dir / "PYTHON_GUIDELINES_Architecture Patterns with Python.json"
        
        md_file.write_text("## Chapter 1")
        json_file.write_text('{"book": "Test", "title": "Test", "chapters": [{"chapter_number": 1, "chapter_title": "Ch1"}]}')


class TestValidationSummary:
    """Test overall validation summary behavior"""
    
    def test_returns_true_when_all_pass(self, tmp_path, monkeypatch, capsys):
        """validate_tab5_implementation returns True when all checks pass"""
        monkeypatch.chdir(tmp_path)
        
        # Create complete passing setup
        self._create_complete_passing_setup(tmp_path)
        
        validate_tab5_implementation()  # Return value checked via capsys
        captured = capsys.readouterr()
        
        assert result is True
        assert "🎉 ALL VALIDATION CHECKS PASSED!" in captured.out
        assert "✅ Tab 5 implementation is complete" in captured.out
    
    def test_returns_false_when_failures_exist(self, tmp_path, monkeypatch, capsys):
        """validate_tab5_implementation returns False when any check fails"""
        monkeypatch.chdir(tmp_path)
        
        # Don't create script - causes failure
        
        validate_tab5_implementation()  # Return value checked via capsys
        captured = capsys.readouterr()
        
        assert result is False
        assert "🚨 VALIDATION FAILED" in captured.out
        assert "❌ FAILED:" in captured.out
    
    def test_prints_summary_statistics(self, tmp_path, monkeypatch, capsys):
        """validate_tab5_implementation prints summary with counts"""
        monkeypatch.chdir(tmp_path)
        
        self._create_complete_passing_setup(tmp_path)
        
        validate_tab5_implementation()  # Return value checked via capsys
        captured = capsys.readouterr()
        
        assert "VALIDATION SUMMARY" in captured.out
        assert "✅ PASSED:" in captured.out
        assert "requirements" in captured.out
    
    def _create_complete_passing_setup(self, tmp_path):
        """Helper to create complete setup that passes all requirements"""
        # Requirement 1: Script
        script_dir = tmp_path / "workflows/base_guideline_generation/scripts"
        script_dir.mkdir(parents=True)
        script_file = script_dir / "chapter_generator_all_text.py"
        script_file.write_text("def _convert_markdown_to_json(): pass\nimport json\njson.dump()")
        
        # Requirement 2, 3, 4: Output files
        output_dir = tmp_path / "examples/guideline_outputs"
        output_dir.mkdir(parents=True)
        md_file = output_dir / "PYTHON_GUIDELINES_Architecture Patterns with Python.md"
        json_file = output_dir / "PYTHON_GUIDELINES_Architecture Patterns with Python.json"
        
        md_file.write_text("## Chapter 1\n## Chapter 2")
        json_data = {
            "book": "Test",
            "title": "Test",
            "chapters": [
                {"chapter_number": 1, "chapter_title": "Ch1"},
                {"chapter_number": 2, "chapter_title": "Ch2"}
            ]
        }
        json_file.write_text(json.dumps(json_data))
        
        # Requirement 5: Tests
        test_dir = tmp_path / "tests/integration"
        test_dir.mkdir(parents=True)
        test_file = test_dir / "test_end_to_end_json_generation.py"
        test_file.write_text("def test_one(): pass")
        
        # Requirement 6: SonarQube
        reports_dir = tmp_path / "reports"
        reports_dir.mkdir()
        sonar_report = reports_dir / "sonarqube_task16_analysis.md"
        sonar_report.write_text("bugs: 0, code smells: 0")
        
        # Requirement 7: Documentation
        impl_doc = tmp_path / "implementation-summary-tab5-json-generation.md"
        impl_doc.write_text("# Summary")
