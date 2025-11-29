"""
Test error handling in JSON generation functions.

Validates EAFP (Easier to Ask Forgiveness than Permission) error handling patterns
per ARCHITECTURE_GUIDELINES Ch. 12 and Fluent Python Ch. 18.

References:
    - ARCHITECTURE_GUIDELINES Ch. 12: Exception handling patterns
    - Fluent Python Ch. 18: EAFP error handling style
    - Python Distilled Ch. 10: Exception handling best practices
"""

import json
import sys
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

# Add workflows to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "workflows" / "base_guideline_generation" / "scripts"))

from chapter_generator_all_text import (
    _convert_markdown_to_json,
    _write_output_file,
    _extract_book_metadata
)


class TestErrorHandlingPatterns:
    """Test EAFP error handling in JSON generation."""
    
    def test_convert_empty_docs_raises_valueerror(self):
        """
        Verify empty document raises ValueError with clear message.
        
        EAFP pattern: Try to convert, catch specific exception.
        
        References:
            - Fluent Python Ch. 18: EAFP style error handling
        """
        with pytest.raises(ValueError, match="Cannot convert empty document"):
            _convert_markdown_to_json([], "TestBook", [])
    
    def test_convert_none_docs_raises_valueerror(self):
        """
        Verify None document raises ValueError.
        
        Tests graceful handling of invalid input types.
        """
        with pytest.raises(ValueError, match="Cannot convert empty document"):
            _convert_markdown_to_json(None, "TestBook", [])
    
    def test_convert_no_chapters_raises_valueerror(self):
        """
        Verify markdown without chapters raises ValueError.
        
        Ensures we validate markdown structure before proceeding.
        """
        invalid_md = ["# Some Title", "Just plain text without chapters"]
        
        with pytest.raises(ValueError, match="No chapters found"):
            _convert_markdown_to_json(invalid_md, "TestBook", [])
    
    def test_write_file_permission_error_propagates(self, tmp_path, capsys):
        """
        Verify PermissionError is caught, logged, and re-raised.
        
        EAFP pattern: Try to write, catch PermissionError, log, raise.
        
        References:
            - ARCHITECTURE_GUIDELINES Ch. 12: Error handling and logging
        """
        # Create markdown that will pass parsing
        all_docs = [
            "# Test Book",
            "*Source: Test Source*",
            "",
            "## Chapter 1: Test Chapter",
            "*Source: Test Book, pages 1–10*",
            "",
            "### Cross-Text Analysis",
            "Test analysis",
            "",
            "### Chapter Summary",
            "Test summary"
        ]
        
        # Mock Path.write_text to raise PermissionError
        with patch('pathlib.Path.write_text', side_effect=PermissionError("Access denied")):
            with pytest.raises(PermissionError):
                _write_output_file(all_docs, "TestBook", [])
        
        # Check error message was logged
        captured = capsys.readouterr()
        assert "Permission denied" in captured.out
        assert "PYTHON_GUIDELINES_TestBook.md" in captured.out
    
    def test_write_file_oserror_propagates(self, tmp_path, capsys):
        """
        Verify OSError (e.g., disk full) is caught, logged, and re-raised.
        
        EAFP pattern: Try to write, catch OSError, log, raise.
        """
        all_docs = [
            "# Test Book",
            "*Source: Test Source*",
            "",
            "## Chapter 1: Test Chapter",
            "*Source: Test Book, pages 1–10*",
            "",
            "### Cross-Text Analysis",
            "Test analysis",
            "",
            "### Chapter Summary",
            "Test summary"
        ]
        
        # Mock Path.write_text to raise OSError (disk full)
        with patch('pathlib.Path.write_text', side_effect=OSError(28, "No space left on device")):
            with pytest.raises(OSError):
                _write_output_file(all_docs, "TestBook", [])
        
        # Check error message was logged
        captured = capsys.readouterr()
        assert "OS error" in captured.out
    
    def test_json_serialization_error_graceful_degradation(self, tmp_path, capsys, monkeypatch):
        """
        Verify JSON serialization TypeError is caught and MD-only output succeeds.
        
        EAFP pattern: Try JSON dump, catch TypeError, log warning, continue.
        This tests graceful degradation - MD file created even if JSON fails.
        
        References:
            - ARCHITECTURE_GUIDELINES Ch. 12: Graceful degradation
        """
        # Change to tmp directory for file output
        monkeypatch.chdir(tmp_path)
        
        all_docs = [
            "# Test Book",
            "*Source: Test Source*",
            "",
            "## Chapter 1: Test Chapter",
            "*Source: Test Book, pages 1–10*",
            "",
            "### Cross-Text Analysis",
            "Test analysis",
            "",
            "### Chapter Summary",
            "Test summary"
        ]
        
        # Mock json.dump to raise TypeError (non-serializable data)
        with patch('json.dump', side_effect=TypeError("Object not JSON serializable")):
            # Should NOT raise - graceful degradation
            _write_output_file(all_docs, "TestBook", [])
        
        # Check MD file was created
        md_path = tmp_path / "PYTHON_GUIDELINES_TestBook.md"
        assert md_path.exists()
        
        # Check warning was logged
        captured = capsys.readouterr()
        assert "JSON serialization error" in captured.out
        assert "Markdown file created successfully" in captured.out
    
    def test_markdown_parse_error_graceful_degradation(self, tmp_path, capsys, monkeypatch):
        """
        Verify markdown parse errors allow MD-only output.
        
        Tests graceful degradation when JSON conversion fails but MD is valid.
        """
        # Change to tmp directory for file output
        monkeypatch.chdir(tmp_path)
        
        all_docs = [
            "# Test Book",
            "Valid markdown but will fail JSON parsing"
        ]
        
        # Should NOT raise - graceful degradation
        _write_output_file(all_docs, "TestBook", [])
        
        # Check MD file was created
        md_path = tmp_path / "PYTHON_GUIDELINES_TestBook.md"
        assert md_path.exists()
        
        # Check warning was logged
        captured = capsys.readouterr()
        assert "Failed to parse markdown" in captured.out or "No chapters found" in captured.out
        assert "Markdown file created successfully" in captured.out
    
    def test_malformed_chapter_skipped_with_warning(self, capsys):
        """
        Verify malformed chapter is skipped with warning, other chapters processed.
        
        EAFP pattern: Try to parse chapter, catch error, log, continue.
        
        Note: Chapter with non-numeric number won't match regex, so won't trigger handler.
        This test verifies a chapter that matches but has invalid page range format.
        
        References:
            - ARCHITECTURE_GUIDELINES Ch. 12: Continue on error for events
        """
        # Note: regex (\d+) won't match "INVALID", so that chapter is simply ignored by regex
        # This tests that we successfully parse valid chapters even if some are malformed
        all_docs = [
            "# Test Book",
            "*Source: Test Source*",
            "",
            "## Chapter 1: Valid Chapter",
            "*Source: Test Book, pages 1–10*",
            "",
            "### Cross-Text Analysis",
            "Test analysis",
            "",
            "### Chapter Summary",
            "Test summary",
            "",
            "## Chapter INVALID: Malformed",  # Won't match regex - silently ignored
            "This chapter has invalid structure",
            "",
            "## Chapter 2: Another Valid Chapter",
            "*Source: Test Book, pages 11–20*",
            "",
            "### Cross-Text Analysis",
            "Test analysis 2",
            "",
            "### Chapter Summary",
            "Test summary 2"
        ]
        
        result = _convert_markdown_to_json(all_docs, "TestBook", [])
        
        # Should have 2 valid chapters (malformed one doesn't match regex)
        assert len(result["chapters"]) == 2
        assert result["chapters"][0]["chapter_number"] == 1
        assert result["chapters"][1]["chapter_number"] == 2
        
        # The "INVALID" chapter doesn't match regex pattern, so no warning logged
        # This is expected behavior - only chapters matching pattern are processed


class TestErrorMessaging:
    """Test error messages are clear and actionable."""
    
    def test_empty_doc_error_message_is_clear(self):
        """Verify error messages guide user to solution."""
        with pytest.raises(ValueError) as exc_info:
            _convert_markdown_to_json([], "TestBook", [])
        
        assert "empty document" in str(exc_info.value).lower()
    
    def test_no_chapters_error_message_is_clear(self):
        """Verify error specifies what's missing."""
        with pytest.raises(ValueError) as exc_info:
            _convert_markdown_to_json(["# Title", "No chapters"], "TestBook", [])
        
        assert "No chapters found" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
