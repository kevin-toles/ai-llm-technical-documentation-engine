"""
Characterization tests for scripts/validate_metadata_extraction.py

Tests document current behavior before refactoring to reduce complexity:
- MetadataValidator._validate_chapter (CC 34)
- MetadataValidator.validate_all (CC 13)
- MetadataValidator.print_summary (CC 15)
- MetadataValidator.validate_book (CC 12)

Architecture Pattern: Service Layer + Strategy Pattern
Reference: Architecture Patterns Ch. 4 (Service Layer), Ch. 13 (Strategy Pattern)
"""

import json
import pytest
from pathlib import Path
from scripts.validate_metadata_extraction import MetadataValidator, ValidationResult


class TestValidationResultBehavior:
    """Test ValidationResult dataclass"""
    
    def test_creates_validation_result_with_defaults(self):
        """ValidationResult has default severity 'error'"""
        result = ValidationResult(True, "Test message")
        assert result.passed is True
        assert result.message == "Test message"
        assert result.severity == "error"
    
    def test_creates_validation_result_with_custom_severity(self):
        """ValidationResult accepts custom severity"""
        result = ValidationResult(False, "Warning message", "warning")
        assert result.passed is False
        assert result.severity == "warning"


class TestMetadataValidatorInitialization:
    """Test MetadataValidator initialization"""
    
    def test_initializes_with_directories(self, tmp_path):
        """MetadataValidator stores directory paths"""
        metadata_dir = tmp_path / "metadata"
        source_dir = tmp_path / "source"
        validator = MetadataValidator(metadata_dir, source_dir, verbose=False)
        
        assert validator.metadata_dir == metadata_dir
        assert validator.source_dir == source_dir
        assert validator.verbose is False
        assert validator.results == {}
    
    def test_initializes_with_verbose_flag(self, tmp_path):
        """MetadataValidator respects verbose flag"""
        validator = MetadataValidator(tmp_path, tmp_path, verbose=True)
        assert validator.verbose is True


class TestValidateChapterBehavior:
    """Test _validate_chapter method (CC 34 - highest complexity)"""
    
    def test_returns_error_for_missing_required_fields(self, tmp_path):
        """_validate_chapter detects missing required fields"""
        validator = MetadataValidator(tmp_path, tmp_path)
        chapter = {"title": "Test"}  # Missing most required fields
        
        results = validator._validate_chapter(chapter, 1, 100)
        
        errors = [r for r in results if not r.passed and r.severity == "error"]
        assert len(errors) > 0
        assert any("Missing required fields" in r.message for r in errors)
    
    def test_validates_complete_chapter_successfully(self, tmp_path):
        """_validate_chapter passes for valid chapter"""
        validator = MetadataValidator(tmp_path, tmp_path)
        chapter = {
            "chapter_number": 1,
            "title": "Introduction to Python",
            "start_page": 1,
            "end_page": 20,
            "summary": "This chapter introduces Python programming basics and syntax",
            "keywords": ["python", "programming", "syntax"],
            "concepts": ["variables", "data types", "functions"]
        }
        
        results = validator._validate_chapter(chapter, 1, 100)
        
        errors = [r for r in results if not r.passed and r.severity == "error"]
        assert len(errors) == 0
    
    def test_validates_chapter_number_is_integer(self, tmp_path):
        """_validate_chapter checks chapter_number is integer"""
        validator = MetadataValidator(tmp_path, tmp_path)
        chapter = {
            "chapter_number": "1",  # String instead of int
            "title": "Test",
            "start_page": 1,
            "end_page": 10,
            "summary": "Test summary for validation",
            "keywords": ["test"],
            "concepts": ["concept"]
        }
        
        results = validator._validate_chapter(chapter, 1, 100)
        
        errors = [r for r in results if not r.passed and "chapter_number must be integer" in r.message]
        assert len(errors) == 1
    
    def test_validates_chapter_number_is_positive(self, tmp_path):
        """_validate_chapter checks chapter_number is positive"""
        validator = MetadataValidator(tmp_path, tmp_path)
        chapter = {
            "chapter_number": -1,
            "title": "Test",
            "start_page": 1,
            "end_page": 10,
            "summary": "Test summary for validation",
            "keywords": ["test"],
            "concepts": ["concept"]
        }
        
        results = validator._validate_chapter(chapter, 1, 100)
        
        errors = [r for r in results if not r.passed and "must be positive" in r.message]
        assert len(errors) == 1
    
    def test_validates_title_is_string(self, tmp_path):
        """_validate_chapter checks title is string"""
        validator = MetadataValidator(tmp_path, tmp_path)
        chapter = {
            "chapter_number": 1,
            "title": 123,  # Integer instead of string
            "start_page": 1,
            "end_page": 10,
            "summary": "Test summary for validation",
            "keywords": ["test"],
            "concepts": ["concept"]
        }
        
        results = validator._validate_chapter(chapter, 1, 100)
        
        errors = [r for r in results if not r.passed and "title must be string" in r.message]
        assert len(errors) == 1
    
    def test_validates_title_not_empty(self, tmp_path):
        """_validate_chapter checks title is not empty"""
        validator = MetadataValidator(tmp_path, tmp_path)
        chapter = {
            "chapter_number": 1,
            "title": "   ",  # Empty after strip
            "start_page": 1,
            "end_page": 10,
            "summary": "Test summary for validation",
            "keywords": ["test"],
            "concepts": ["concept"]
        }
        
        results = validator._validate_chapter(chapter, 1, 100)
        
        errors = [r for r in results if not r.passed and "title is empty" in r.message]
        assert len(errors) == 1
    
    def test_warns_about_long_title(self, tmp_path):
        """_validate_chapter warns if title exceeds 200 chars"""
        validator = MetadataValidator(tmp_path, tmp_path)
        chapter = {
            "chapter_number": 1,
            "title": "A" * 250,  # 250 chars
            "start_page": 1,
            "end_page": 10,
            "summary": "Test summary for validation",
            "keywords": ["test"],
            "concepts": ["concept"]
        }
        
        results = validator._validate_chapter(chapter, 1, 100)
        
        warnings = [r for r in results if not r.passed and r.severity == "warning" and "title too long" in r.message]
        assert len(warnings) == 1
    
    def test_validates_page_numbers_are_integers(self, tmp_path):
        """_validate_chapter checks page numbers are integers"""
        validator = MetadataValidator(tmp_path, tmp_path)
        chapter = {
            "chapter_number": 1,
            "title": "Test",
            "start_page": "1",  # String
            "end_page": 10,
            "summary": "Test summary for validation",
            "keywords": ["test"],
            "concepts": ["concept"]
        }
        
        results = validator._validate_chapter(chapter, 1, 100)
        
        errors = [r for r in results if not r.passed and "must be integers" in r.message]
        assert len(errors) == 1
    
    def test_validates_page_numbers_are_positive(self, tmp_path):
        """_validate_chapter checks page numbers are positive"""
        validator = MetadataValidator(tmp_path, tmp_path)
        chapter = {
            "chapter_number": 1,
            "title": "Test",
            "start_page": 0,  # Not positive
            "end_page": 10,
            "summary": "Test summary for validation",
            "keywords": ["test"],
            "concepts": ["concept"]
        }
        
        results = validator._validate_chapter(chapter, 1, 100)
        
        errors = [r for r in results if not r.passed and "page numbers must be positive" in r.message]
        assert len(errors) == 1
    
    def test_validates_start_page_before_end_page(self, tmp_path):
        """_validate_chapter checks start_page <= end_page"""
        validator = MetadataValidator(tmp_path, tmp_path)
        chapter = {
            "chapter_number": 1,
            "title": "Test",
            "start_page": 20,
            "end_page": 10,  # End before start
            "summary": "Test summary for validation",
            "keywords": ["test"],
            "concepts": ["concept"]
        }
        
        results = validator._validate_chapter(chapter, 1, 100)
        
        errors = [r for r in results if not r.passed and "start_page" in r.message and "end_page" in r.message]
        assert len(errors) == 1
    
    def test_warns_if_end_page_exceeds_total_pages(self, tmp_path):
        """_validate_chapter warns if end_page > total_pages"""
        validator = MetadataValidator(tmp_path, tmp_path)
        chapter = {
            "chapter_number": 1,
            "title": "Test",
            "start_page": 1,
            "end_page": 150,  # Exceeds 100 total pages
            "summary": "Test summary for validation",
            "keywords": ["test"],
            "concepts": ["concept"]
        }
        
        results = validator._validate_chapter(chapter, 1, 100)
        
        warnings = [r for r in results if not r.passed and "exceeds total pages" in r.message]
        assert len(warnings) == 1
    
    def test_validates_summary_is_string(self, tmp_path):
        """_validate_chapter checks summary is string"""
        validator = MetadataValidator(tmp_path, tmp_path)
        chapter = {
            "chapter_number": 1,
            "title": "Test",
            "start_page": 1,
            "end_page": 10,
            "summary": 123,  # Not string
            "keywords": ["test"],
            "concepts": ["concept"]
        }
        
        results = validator._validate_chapter(chapter, 1, 100)
        
        errors = [r for r in results if not r.passed and "summary must be string" in r.message]
        assert len(errors) == 1
    
    def test_validates_summary_not_empty(self, tmp_path):
        """_validate_chapter checks summary is not empty"""
        validator = MetadataValidator(tmp_path, tmp_path)
        chapter = {
            "chapter_number": 1,
            "title": "Test",
            "start_page": 1,
            "end_page": 10,
            "summary": "   ",  # Empty after strip
            "keywords": ["test"],
            "concepts": ["concept"]
        }
        
        results = validator._validate_chapter(chapter, 1, 100)
        
        errors = [r for r in results if not r.passed and "summary is empty" in r.message]
        assert len(errors) == 1
    
    def test_warns_if_summary_too_short(self, tmp_path):
        """_validate_chapter warns if summary < 20 chars"""
        validator = MetadataValidator(tmp_path, tmp_path)
        chapter = {
            "chapter_number": 1,
            "title": "Test",
            "start_page": 1,
            "end_page": 10,
            "summary": "Short",  # Less than 20 chars
            "keywords": ["test"],
            "concepts": ["concept"]
        }
        
        results = validator._validate_chapter(chapter, 1, 100)
        
        warnings = [r for r in results if not r.passed and "summary too short" in r.message]
        assert len(warnings) == 1
    
    def test_validates_keywords_is_list(self, tmp_path):
        """_validate_chapter checks keywords is list"""
        validator = MetadataValidator(tmp_path, tmp_path)
        chapter = {
            "chapter_number": 1,
            "title": "Test",
            "start_page": 1,
            "end_page": 10,
            "summary": "Test summary for validation",
            "keywords": "not a list",  # String instead of list
            "concepts": ["concept"]
        }
        
        results = validator._validate_chapter(chapter, 1, 100)
        
        errors = [r for r in results if not r.passed and "keywords must be list" in r.message]
        assert len(errors) == 1
    
    def test_warns_if_keywords_empty(self, tmp_path):
        """_validate_chapter warns if keywords list is empty"""
        validator = MetadataValidator(tmp_path, tmp_path)
        chapter = {
            "chapter_number": 1,
            "title": "Test",
            "start_page": 1,
            "end_page": 10,
            "summary": "Test summary for validation",
            "keywords": [],  # Empty list
            "concepts": ["concept"]
        }
        
        results = validator._validate_chapter(chapter, 1, 100)
        
        warnings = [r for r in results if not r.passed and "no keywords extracted" in r.message]
        assert len(warnings) == 1
    
    def test_validates_keywords_are_strings(self, tmp_path):
        """_validate_chapter checks all keywords are strings"""
        validator = MetadataValidator(tmp_path, tmp_path)
        chapter = {
            "chapter_number": 1,
            "title": "Test",
            "start_page": 1,
            "end_page": 10,
            "summary": "Test summary for validation",
            "keywords": ["valid", 123, "another"],  # Contains non-string
            "concepts": ["concept"]
        }
        
        results = validator._validate_chapter(chapter, 1, 100)
        
        errors = [r for r in results if not r.passed and "keywords must be strings" in r.message]
        assert len(errors) == 1
    
    def test_warns_about_empty_keywords(self, tmp_path):
        """_validate_chapter warns about empty string keywords"""
        validator = MetadataValidator(tmp_path, tmp_path)
        chapter = {
            "chapter_number": 1,
            "title": "Test",
            "start_page": 1,
            "end_page": 10,
            "summary": "Test summary for validation",
            "keywords": ["valid", "   ", "another"],  # Contains empty string
            "concepts": ["concept"]
        }
        
        results = validator._validate_chapter(chapter, 1, 100)
        
        warnings = [r for r in results if not r.passed and "empty keywords" in r.message]
        assert len(warnings) == 1
    
    def test_validates_concepts_is_list(self, tmp_path):
        """_validate_chapter checks concepts is list"""
        validator = MetadataValidator(tmp_path, tmp_path)
        chapter = {
            "chapter_number": 1,
            "title": "Test",
            "start_page": 1,
            "end_page": 10,
            "summary": "Test summary for validation",
            "keywords": ["test"],
            "concepts": "not a list"  # String instead of list
        }
        
        results = validator._validate_chapter(chapter, 1, 100)
        
        errors = [r for r in results if not r.passed and "concepts must be list" in r.message]
        assert len(errors) == 1
    
    def test_warns_if_concepts_empty_with_short_summary(self, tmp_path):
        """_validate_chapter warns about empty concepts with possible OCR issues"""
        validator = MetadataValidator(tmp_path, tmp_path)
        chapter = {
            "chapter_number": 1,
            "title": "Test",
            "start_page": 1,
            "end_page": 10,
            "summary": "Short",  # Less than 50 chars
            "keywords": ["test"],
            "concepts": []  # Empty
        }
        
        results = validator._validate_chapter(chapter, 1, 100)
        
        warnings = [r for r in results if not r.passed and "poor OCR" in r.message]
        assert len(warnings) == 1
    
    def test_warns_if_concepts_empty_with_normal_summary(self, tmp_path):
        """_validate_chapter warns about empty concepts with sufficient text"""
        validator = MetadataValidator(tmp_path, tmp_path)
        chapter = {
            "chapter_number": 1,
            "title": "Test",
            "start_page": 1,
            "end_page": 10,
            "summary": "This is a longer summary with more than fifty characters for testing",
            "keywords": ["test"],
            "concepts": []  # Empty
        }
        
        results = validator._validate_chapter(chapter, 1, 100)
        
        warnings = [r for r in results if not r.passed and "no concepts extracted" in r.message]
        assert len(warnings) == 1
    
    def test_validates_concepts_are_strings(self, tmp_path):
        """_validate_chapter checks all concepts are strings"""
        validator = MetadataValidator(tmp_path, tmp_path)
        chapter = {
            "chapter_number": 1,
            "title": "Test",
            "start_page": 1,
            "end_page": 10,
            "summary": "Test summary for validation",
            "keywords": ["test"],
            "concepts": ["valid", 456, "another"]  # Contains non-string
        }
        
        results = validator._validate_chapter(chapter, 1, 100)
        
        errors = [r for r in results if not r.passed and "concepts must be strings" in r.message]
        assert len(errors) == 1


class TestValidateChapterNumbersBehavior:
    """Test _validate_chapter_numbers method"""
    
    def test_detects_duplicate_chapter_numbers(self, tmp_path):
        """_validate_chapter_numbers detects duplicates"""
        validator = MetadataValidator(tmp_path, tmp_path)
        chapter_numbers = [1, 2, 3, 2, 4]  # Duplicate 2
        
        results = validator._validate_chapter_numbers(chapter_numbers)
        
        errors = [r for r in results if not r.passed and "Duplicate" in r.message]
        assert len(errors) == 1
        assert "2" in errors[0].message
    
    def test_warns_if_chapter_numbers_not_sequential(self, tmp_path):
        """_validate_chapter_numbers warns if not in order"""
        validator = MetadataValidator(tmp_path, tmp_path)
        chapter_numbers = [1, 3, 2, 4]  # Out of order
        
        results = validator._validate_chapter_numbers(chapter_numbers)
        
        warnings = [r for r in results if not r.passed and "not in order" in r.message]
        assert len(warnings) == 1
    
    def test_warns_about_large_gaps_in_numbering(self, tmp_path):
        """_validate_chapter_numbers warns about gaps > 5"""
        validator = MetadataValidator(tmp_path, tmp_path)
        chapter_numbers = [1, 2, 10]  # Gap of 8
        
        results = validator._validate_chapter_numbers(chapter_numbers)
        
        warnings = [r for r in results if not r.passed and "Large gap" in r.message]
        assert len(warnings) == 1
    
    def test_returns_empty_for_empty_list(self, tmp_path):
        """_validate_chapter_numbers handles empty list"""
        validator = MetadataValidator(tmp_path, tmp_path)
        results = validator._validate_chapter_numbers([])
        assert results == []


class TestValidatePageRangesBehavior:
    """Test _validate_page_ranges method"""
    
    def test_detects_overlapping_page_ranges(self, tmp_path):
        """_validate_page_ranges detects overlaps"""
        validator = MetadataValidator(tmp_path, tmp_path)
        page_ranges = [(1, 20), (15, 30)]  # Overlap at 15-20
        
        results = validator._validate_page_ranges(page_ranges)
        
        errors = [r for r in results if not r.passed and "Overlapping" in r.message]
        assert len(errors) == 1
    
    def test_passes_for_adjacent_page_ranges(self, tmp_path):
        """_validate_page_ranges allows adjacent ranges"""
        validator = MetadataValidator(tmp_path, tmp_path)
        page_ranges = [(1, 20), (21, 40)]  # No overlap
        
        results = validator._validate_page_ranges(page_ranges)
        
        errors = [r for r in results if not r.passed]
        assert len(errors) == 0
    
    def test_handles_single_range(self, tmp_path):
        """_validate_page_ranges handles single range"""
        validator = MetadataValidator(tmp_path, tmp_path)
        results = validator._validate_page_ranges([(1, 20)])
        assert results == []


class TestValidateAgainstSourceBehavior:
    """Test _validate_against_source method"""
    
    def test_passes_when_chapter_counts_match(self, tmp_path):
        """_validate_against_source passes when counts match"""
        validator = MetadataValidator(tmp_path, tmp_path)
        metadata = [{"chapter": 1}, {"chapter": 2}]
        source_chapters = [{"title": "Ch1"}, {"title": "Ch2"}]
        
        results = validator._validate_against_source(metadata, source_chapters)
        
        info_results = [r for r in results if r.passed and "matches source" in r.message]
        assert len(info_results) == 1
    
    def test_errors_when_metadata_has_fewer_chapters(self, tmp_path):
        """_validate_against_source errors when metadata missing chapters"""
        validator = MetadataValidator(tmp_path, tmp_path)
        metadata = [{"chapter": 1}]
        source_chapters = [{"title": "Ch1"}, {"title": "Ch2"}]
        
        results = validator._validate_against_source(metadata, source_chapters)
        
        errors = [r for r in results if not r.passed and "Missing chapters" in r.message]
        assert len(errors) == 1
    
    def test_warns_when_metadata_has_extra_chapters(self, tmp_path):
        """_validate_against_source warns when metadata has extra chapters"""
        validator = MetadataValidator(tmp_path, tmp_path)
        metadata = [{"chapter": 1}, {"chapter": 2}, {"chapter": 3}]
        source_chapters = [{"title": "Ch1"}, {"title": "Ch2"}]
        
        results = validator._validate_against_source(metadata, source_chapters)
        
        warnings = [r for r in results if not r.passed and "Extra chapters" in r.message]
        assert len(warnings) == 1
    
    def test_handles_source_with_no_chapters(self, tmp_path):
        """_validate_against_source handles fallback detection case"""
        validator = MetadataValidator(tmp_path, tmp_path)
        metadata = [{"chapter": 1}, {"chapter": 2}]
        source_chapters = []  # No chapters in source
        
        results = validator._validate_against_source(metadata, source_chapters)
        
        info_results = [r for r in results if r.passed and "fallback detection" in r.message]
        assert len(info_results) == 1


class TestValidateBookBehavior:
    """Test validate_book method (CC 12)"""
    
    def test_returns_error_for_missing_file(self, tmp_path):
        """validate_book handles missing metadata file"""
        validator = MetadataValidator(tmp_path, tmp_path)
        nonexistent_file = tmp_path / "nonexistent.json"
        
        results = validator.validate_book(nonexistent_file, "Test Book")
        
        errors = [r for r in results if not r.passed and "not found" in r.message]
        assert len(errors) == 1
    
    def test_returns_error_for_invalid_json(self, tmp_path):
        """validate_book handles invalid JSON"""
        validator = MetadataValidator(tmp_path, tmp_path)
        invalid_file = tmp_path / "invalid.json"
        invalid_file.write_text("{invalid json")
        
        results = validator.validate_book(invalid_file, "Test Book")
        
        errors = [r for r in results if not r.passed and "Invalid JSON" in r.message]
        assert len(errors) == 1
    
    def test_returns_error_for_non_list_metadata(self, tmp_path):
        """validate_book checks metadata is list"""
        validator = MetadataValidator(tmp_path, tmp_path)
        metadata_file = tmp_path / "test.json"
        metadata_file.write_text('{"chapters": []}')  # Dict, not list
        
        results = validator.validate_book(metadata_file, "Test Book")
        
        errors = [r for r in results if not r.passed and "must be a list" in r.message]
        assert len(errors) == 1
    
    def test_returns_error_for_empty_metadata(self, tmp_path):
        """validate_book checks metadata is not empty"""
        validator = MetadataValidator(tmp_path, tmp_path)
        metadata_file = tmp_path / "test.json"
        metadata_file.write_text('[]')  # Empty list
        
        results = validator.validate_book(metadata_file, "Test Book")
        
        errors = [r for r in results if not r.passed and "empty" in r.message]
        assert len(errors) == 1
    
    def test_validates_complete_book_successfully(self, tmp_path):
        """validate_book passes for valid metadata"""
        validator = MetadataValidator(tmp_path, tmp_path)
        metadata_file = tmp_path / "test_metadata.json"
        metadata = [
            {
                "chapter_number": 1,
                "title": "Introduction",
                "start_page": 1,
                "end_page": 20,
                "summary": "Introduction to Python programming concepts and syntax",
                "keywords": ["python", "introduction"],
                "concepts": ["programming", "syntax"]
            }
        ]
        metadata_file.write_text(json.dumps(metadata))
        
        results = validator.validate_book(metadata_file, "Test Book")
        
        errors = [r for r in results if not r.passed and r.severity == "error"]
        assert len(errors) == 0
    
    def test_loads_source_json_when_available(self, tmp_path):
        """validate_book loads source JSON for cross-reference"""
        metadata_dir = tmp_path / "metadata"
        source_dir = tmp_path / "source"
        metadata_dir.mkdir()
        source_dir.mkdir()
        
        validator = MetadataValidator(metadata_dir, source_dir)
        
        metadata_file = metadata_dir / "test_metadata.json"
        metadata = [
            {
                "chapter_number": 1,
                "title": "Test",
                "start_page": 1,
                "end_page": 10,
                "summary": "Test summary for validation purposes",
                "keywords": ["test"],
                "concepts": ["concept"]
            }
        ]
        metadata_file.write_text(json.dumps(metadata))
        
        source_file = source_dir / "test.json"
        source_data = {
            "chapters": [{"title": "Test Chapter"}],
            "pages": [{"number": i} for i in range(1, 21)]
        }
        source_file.write_text(json.dumps(source_data))
        
        results = validator.validate_book(metadata_file, "test")
        
        info_results = [r for r in results if r.passed and "Source JSON found" in r.message]
        assert len(info_results) == 1
        assert "1 chapters" in info_results[0].message
        assert "20 pages" in info_results[0].message


class TestValidateAllBehavior:
    """Test validate_all method (CC 13)"""
    
    def test_returns_counts_for_empty_directory(self, tmp_path):
        """validate_all handles empty metadata directory"""
        validator = MetadataValidator(tmp_path, tmp_path)
        
        total, passed, failed = validator.validate_all()
        
        assert total == 0
        assert passed == 0
        assert failed == 0
    
    def test_validates_multiple_books(self, tmp_path):
        """validate_all processes multiple metadata files"""
        metadata_dir = tmp_path / "metadata"
        metadata_dir.mkdir()
        
        validator = MetadataValidator(metadata_dir, tmp_path)
        
        # Create two valid metadata files
        for i in range(1, 3):
            metadata_file = metadata_dir / f"book{i}_metadata.json"
            metadata = [
                {
                    "chapter_number": 1,
                    "title": f"Book {i}",
                    "start_page": 1,
                    "end_page": 10,
                    "summary": "Test summary with enough characters for validation",
                    "keywords": ["test"],
                    "concepts": ["concept"]
                }
            ]
            metadata_file.write_text(json.dumps(metadata))
        
        total, passed, failed = validator.validate_all()
        
        assert total == 2
        assert passed == 2
        assert failed == 0
    
    def test_counts_failed_books_correctly(self, tmp_path):
        """validate_all counts books with errors as failed"""
        metadata_dir = tmp_path / "metadata"
        metadata_dir.mkdir()
        
        validator = MetadataValidator(metadata_dir, tmp_path)
        
        # Valid book
        valid_file = metadata_dir / "valid_metadata.json"
        valid_file.write_text(json.dumps([
            {
                "chapter_number": 1,
                "title": "Valid",
                "start_page": 1,
                "end_page": 10,
                "summary": "Test summary with enough characters",
                "keywords": ["test"],
                "concepts": ["concept"]
            }
        ]))
        
        # Invalid book (empty)
        invalid_file = metadata_dir / "invalid_metadata.json"
        invalid_file.write_text('[]')
        
        total, passed, failed = validator.validate_all()
        
        assert total == 2
        assert passed == 1
        assert failed == 1
    
    def test_stores_results_for_all_books(self, tmp_path):
        """validate_all stores results in validator.results"""
        metadata_dir = tmp_path / "metadata"
        metadata_dir.mkdir()
        
        validator = MetadataValidator(metadata_dir, tmp_path)
        
        metadata_file = metadata_dir / "test_metadata.json"
        metadata_file.write_text(json.dumps([
            {
                "chapter_number": 1,
                "title": "Test",
                "start_page": 1,
                "end_page": 10,
                "summary": "Test summary with enough characters",
                "keywords": ["test"],
                "concepts": ["concept"]
            }
        ]))
        
        validator.validate_all()
        
        assert "test" in validator.results
        assert len(validator.results["test"]) > 0


class TestPrintSummaryBehavior:
    """Test print_summary method (CC 15)"""
    
    def test_prints_basic_statistics(self, tmp_path, capsys):
        """print_summary displays total, passed, failed counts"""
        validator = MetadataValidator(tmp_path, tmp_path)
        validator.results = {
            "book1": [ValidationResult(True, "OK", "info")],
            "book2": [ValidationResult(False, "Error", "error")]
        }
        
        validator.print_summary(2, 1, 1)
        
        captured = capsys.readouterr()
        assert "Total books validated: 2" in captured.out
        assert "Passed: 1" in captured.out
        assert "Failed: 1" in captured.out
    
    def test_counts_total_errors_and_warnings(self, tmp_path, capsys):
        """print_summary counts all errors and warnings"""
        validator = MetadataValidator(tmp_path, tmp_path)
        validator.results = {
            "book1": [
                ValidationResult(False, "Error 1", "error"),
                ValidationResult(False, "Warning 1", "warning")
            ],
            "book2": [
                ValidationResult(False, "Error 2", "error"),
                ValidationResult(False, "Warning 2", "warning")
            ]
        }
        
        validator.print_summary(2, 0, 2)
        
        captured = capsys.readouterr()
        assert "Total errors: 2" in captured.out
        assert "Total warnings: 2" in captured.out
    
    def test_lists_books_with_errors(self, tmp_path, capsys):
        """print_summary lists books that have errors"""
        validator = MetadataValidator(tmp_path, tmp_path)
        validator.results = {
            "book1": [ValidationResult(False, "Error", "error")],
            "book2": [ValidationResult(True, "OK", "info")]
        }
        
        validator.print_summary(2, 1, 1)
        
        captured = capsys.readouterr()
        assert "Books with errors:" in captured.out
        assert "book1" in captured.out
    
    def test_shows_success_message_when_all_passed(self, tmp_path, capsys):
        """print_summary shows success when no failures"""
        validator = MetadataValidator(tmp_path, tmp_path)
        validator.results = {
            "book1": [ValidationResult(True, "OK", "info")]
        }
        
        validator.print_summary(1, 1, 0)
        
        captured = capsys.readouterr()
        assert "ALL VALIDATIONS PASSED!" in captured.out
