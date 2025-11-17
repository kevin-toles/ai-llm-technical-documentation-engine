#!/usr/bin/env python3
"""
Unit tests for merge_metadata_to_cache.py

TDD Phase: RED
- Write failing tests first to define expected behavior
- Tests will fail until features are implemented (GREEN phase)

Guideline Compliance:
- ARCH 5336: Dependency Injection for paths and configuration
- PY 3754: Use pathlib.Path() for all file operations
- PY 32425: Use context managers for file I/O
- PY 21: EAFP exception handling
"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open
import sys

# Add parent directory to path to import module under test
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "workflows" / "metadata_cache_merge" / "scripts"))

# Import will fail initially (RED phase) - MetadataMerger class doesn't exist yet
try:
    from merge_metadata_to_cache import MetadataMerger
except ImportError:
    # Create a placeholder for test collection
    class MetadataMerger:
        pass


class TestAutoDiscovery:
    """Test automatic discovery of metadata files"""
    
    def test_discovers_all_metadata_json_files(self, tmp_path):
        """Should find all *_metadata.json files in input directory"""
        # Create test metadata files
        (tmp_path / "book1_metadata.json").write_text('{"chapters": [{"chapter_num": 1}]}')
        (tmp_path / "book2_metadata.json").write_text('{"chapters": [{"chapter_num": 1}]}')
        (tmp_path / "book3_metadata.json").write_text('{"chapters": [{"chapter_num": 1}]}')
        (tmp_path / "other.json").write_text('{}')  # Should NOT be discovered
        
        merger = MetadataMerger(input_dir=tmp_path)
        discovered = merger.discover_metadata_files()
        
        assert len(discovered) == 3
        assert all(f.name.endswith("_metadata.json") for f in discovered)
    
    def test_returns_empty_list_when_no_metadata_files_found(self, tmp_path):
        """Should return empty list if no metadata files exist"""
        merger = MetadataMerger(input_dir=tmp_path)
        discovered = merger.discover_metadata_files()
        
        assert discovered == []
    
    def test_warns_when_no_metadata_files_found(self, tmp_path, capsys):
        """Should warn user when no metadata files are discovered"""
        merger = MetadataMerger(input_dir=tmp_path)
        merger.discover_metadata_files()
        
        captured = capsys.readouterr()
        assert "No metadata files found" in captured.out or "0 metadata files" in captured.out


class TestCLIArguments:
    """Test command-line argument parsing"""
    
    def test_accepts_input_dir_argument(self):
        """Should accept --input-dir argument"""
        # This test will check argparse setup in main()
        # We'll use subprocess to test CLI directly
        pass  # Will implement after main() is refactored
    
    def test_accepts_output_file_argument(self):
        """Should accept --output-file argument"""
        pass  # Will implement after main() is refactored
    
    def test_accepts_book_list_argument(self):
        """Should accept --book-list argument for filtering"""
        pass  # Will implement after main() is refactored
    
    def test_accepts_dry_run_argument(self):
        """Should accept --dry-run argument"""
        pass  # Will implement after main() is refactored
    
    def test_accepts_validate_only_argument(self):
        """Should accept --validate-only argument"""
        pass  # Will implement after main() is refactored


class TestMetadataValidation:
    """Test validation of metadata files before merging"""
    
    def test_validates_required_fields_in_metadata(self, tmp_path):
        """Should validate metadata has required 'chapters' field"""
        invalid_file = tmp_path / "invalid_metadata.json"
        invalid_file.write_text('{"wrong_field": []}')  # Missing 'chapters'
        
        merger = MetadataMerger(input_dir=tmp_path)
        
        with pytest.raises(ValueError, match="Missing required field"):
            merger.validate_metadata_file(invalid_file)
    
    def test_validates_chapters_is_list(self, tmp_path):
        """Should validate 'chapters' field is a list"""
        invalid_file = tmp_path / "invalid_metadata.json"
        invalid_file.write_text('{"chapters": "not a list"}')
        
        merger = MetadataMerger(input_dir=tmp_path)
        
        with pytest.raises(ValueError, match="must be a list"):
            merger.validate_metadata_file(invalid_file)
    
    def test_accepts_valid_metadata_file(self, tmp_path):
        """Should accept valid metadata file without errors"""
        valid_file = tmp_path / "valid_metadata.json"
        valid_file.write_text('{"chapters": [{"chapter_num": 1, "title": "Test"}]}')
        
        merger = MetadataMerger(input_dir=tmp_path)
        
        # Should not raise exception
        is_valid = merger.validate_metadata_file(valid_file)
        assert is_valid is True


class TestDuplicateDetection:
    """Test detection of duplicate book names"""
    
    def test_detects_duplicate_book_names(self, tmp_path):
        """Should detect when same book name appears multiple times"""
        (tmp_path / "book_a_metadata.json").write_text('{"chapters": []}')
        (tmp_path / "book_a_v2_metadata.json").write_text('{"chapters": []}')  # Same book, different file
        
        merger = MetadataMerger(input_dir=tmp_path)
        files = merger.discover_metadata_files()
        
        duplicates = merger.detect_duplicate_books(files)
        
        # Should detect that "book_a" appears twice
        assert len(duplicates) > 0
    
    def test_no_duplicates_when_all_unique(self, tmp_path):
        """Should return empty list when all books are unique"""
        (tmp_path / "book_a_metadata.json").write_text('{"chapters": []}')
        (tmp_path / "book_b_metadata.json").write_text('{"chapters": []}')
        (tmp_path / "book_c_metadata.json").write_text('{"chapters": []}')
        
        merger = MetadataMerger(input_dir=tmp_path)
        files = merger.discover_metadata_files()
        
        duplicates = merger.detect_duplicate_books(files)
        
        assert duplicates == []


class TestProgressIndicators:
    """Test progress indicators during merge"""
    
    def test_shows_progress_during_merge(self, tmp_path, capsys):
        """Should show progress percentage during merge operation"""
        # Create 5 test files
        for i in range(5):
            (tmp_path / f"book{i}_metadata.json").write_text('{"chapters": [{"chapter_num": 1}]}')
        
        output_file = tmp_path / "cache.json"
        merger = MetadataMerger(input_dir=tmp_path, output_file=output_file)
        merger.merge_all()
        
        captured = capsys.readouterr()
        
        # Should show progress indicators like [20.0%], [40.0%], etc.
        assert "[" in captured.out
        assert "%" in captured.out


class TestDryRunMode:
    """Test dry-run mode (preview without writing)"""
    
    def test_dry_run_does_not_create_file(self, tmp_path):
        """Should NOT create output file when dry_run=True"""
        (tmp_path / "book_metadata.json").write_text('{"chapters": [{"chapter_num": 1}]}')
        
        output_file = tmp_path / "cache.json"
        merger = MetadataMerger(input_dir=tmp_path, output_file=output_file)
        merger.merge_all(dry_run=True)
        
        assert not output_file.exists()
    
    def test_dry_run_shows_preview_output(self, tmp_path, capsys):
        """Should show what WOULD be written in dry-run mode"""
        (tmp_path / "book_metadata.json").write_text('{"chapters": [{"chapter_num": 1}]}')
        
        output_file = tmp_path / "cache.json"
        merger = MetadataMerger(input_dir=tmp_path, output_file=output_file)
        merger.merge_all(dry_run=True)
        
        captured = capsys.readouterr()
        
        assert "DRY RUN" in captured.out or "Would write" in captured.out
        assert "book_metadata.json" in captured.out


class TestValidateOnlyMode:
    """Test validate-only mode (check without merging)"""
    
    def test_validate_only_does_not_create_file(self, tmp_path):
        """Should NOT create output file when validate_only=True"""
        (tmp_path / "book_metadata.json").write_text('{"chapters": [{"chapter_num": 1}]}')
        
        output_file = tmp_path / "cache.json"
        merger = MetadataMerger(input_dir=tmp_path, output_file=output_file)
        merger.validate_all()
        
        assert not output_file.exists()
    
    def test_validate_only_reports_validation_results(self, tmp_path, capsys):
        """Should report validation results for all files"""
        (tmp_path / "valid_metadata.json").write_text('{"chapters": [{"chapter_num": 1}]}')
        (tmp_path / "invalid_metadata.json").write_text('{"wrong": []}')
        
        output_file = tmp_path / "cache.json"
        merger = MetadataMerger(input_dir=tmp_path, output_file=output_file)
        merger.validate_all()
        
        captured = capsys.readouterr()
        
        assert "valid_metadata.json" in captured.out
        assert "invalid_metadata.json" in captured.out or "FAILED" in captured.out


class TestMergeStatistics:
    """Test merge statistics summary"""
    
    def test_displays_merge_statistics(self, tmp_path, capsys):
        """Should display summary statistics after merge"""
        (tmp_path / "book1_metadata.json").write_text('{"chapters": [{"chapter_num": 1}, {"chapter_num": 2}]}')
        (tmp_path / "book2_metadata.json").write_text('{"chapters": [{"chapter_num": 1}]}')
        
        output_file = tmp_path / "cache.json"
        merger = MetadataMerger(input_dir=tmp_path, output_file=output_file)
        merger.merge_all()
        
        captured = capsys.readouterr()
        
        # Should show: X books, Y chapters total
        assert "2 books" in captured.out or "Books: 2" in captured.out
        assert "3 chapters" in captured.out or "Chapters: 3" in captured.out


class TestEmptyChapterWarning:
    """Test warning for books with no chapters"""
    
    def test_warns_when_book_has_no_chapters(self, tmp_path, capsys):
        """Should warn when a book has empty chapters list"""
        (tmp_path / "empty_book_metadata.json").write_text('{"chapters": []}')
        
        output_file = tmp_path / "cache.json"
        merger = MetadataMerger(input_dir=tmp_path, output_file=output_file)
        merger.merge_all()
        
        captured = capsys.readouterr()
        
        assert "no chapters" in captured.out.lower() or "empty" in captured.out.lower()


class TestBookListFiltering:
    """Test filtering by optional book list"""
    
    def test_filters_books_by_provided_list(self, tmp_path):
        """Should only merge books in the provided book_list"""
        (tmp_path / "book_a_metadata.json").write_text('{"chapters": [{"chapter_num": 1}]}')
        (tmp_path / "book_b_metadata.json").write_text('{"chapters": [{"chapter_num": 1}]}')
        (tmp_path / "book_c_metadata.json").write_text('{"chapters": [{"chapter_num": 1}]}')
        
        output_file = tmp_path / "cache.json"
        
        # Only merge book_a and book_c
        merger = MetadataMerger(
            input_dir=tmp_path, 
            output_file=output_file,
            book_list=["book_a", "book_c"]
        )
        result = merger.merge_all()
        
        # Should only have 2 books in cache
        assert len(result) == 2
        assert "book_a_metadata.json" in str(result.keys())
        assert "book_c_metadata.json" in str(result.keys())
        assert "book_b_metadata.json" not in str(result.keys())
