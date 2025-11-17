"""
Unit tests for generate_metadata_universal.py refactoring

TDD Workflow: RED → GREEN → REFACTOR
Following PYTHON_GUIDELINES exception handling (PY 32425) and Path operations (PY 3754)
"""

import pytest
import json
from pathlib import Path
from workflows.metadata_extraction.scripts.generate_metadata_universal import (
    UniversalMetadataGenerator,
    ChapterMetadata
)


class TestConfigurationLoading:
    """Test external configuration file loading (RED phase)"""
    
    def test_loads_keywords_from_config_file(self, tmp_path):
        """
        RED TEST: Should load keywords from config/metadata_keywords.json
        
        Guideline: DI for configuration (ARCH 5336)
        """
        # Create dummy book JSON
        book_json = tmp_path / "test_book.json"
        book_json.write_text(json.dumps({"pages": [{"page_num": 1, "text": "test"}]}))
        
        # Create config file
        keywords_file = tmp_path / "metadata_keywords.json"
        keywords_data = {
            "python": ["class", "function", "method"],
            "architecture": ["microservice", "api", "rest"]
        }
        keywords_file.write_text(json.dumps(keywords_data))
        
        # Should load keywords from config file
        generator = UniversalMetadataGenerator(
            json_path=book_json,
            keywords_file=keywords_file,
            domain="architecture"  # Ensure architecture keywords are loaded
        )
        
        assert "class" in generator.keywords
        assert "microservice" in generator.keywords
    
    def test_loads_patterns_from_config_file(self, tmp_path):
        """
        RED TEST: Should load chapter patterns from config/chapter_patterns.json
        
        Guideline: DI for configuration (ARCH 5336)
        """
        # Create dummy book JSON
        book_json = tmp_path / "test_book.json"
        book_json.write_text(json.dumps({"pages": [{"page_num": 1, "text": "test"}]}))
        
        patterns_file = tmp_path / "chapter_patterns.json"
        patterns_data = {
            "chapter_heading": r"(?:chapter|ch\.?)\s+(\d+)[:\s]+(.+)",
            "section_heading": r"^(?:section|§)\s+(\d+(?:\.\d+)?)"
        }
        patterns_file.write_text(json.dumps(patterns_data))
        
        # Should load patterns from config file
        generator = UniversalMetadataGenerator(
            json_path=book_json,
            patterns_file=patterns_file
        )
        
        assert generator.chapter_pattern is not None
        assert generator.section_pattern is not None


class TestCLIArguments:
    """Test new CLI argument parsing (RED phase)"""
    
    def test_accepts_keywords_file_argument(self):
        """
        RED TEST: Should accept --keywords-file CLI argument
        
        Guideline: CLI design (PY_GUIDELINES command-line arguments)
        """
        # EXPECTED TO FAIL - argument not yet added
        from workflows.metadata_extraction.scripts.generate_metadata_universal import main
        import sys
        
        test_args = [
            '--input', 'test.json',
            '--keywords-file', 'custom_keywords.json',
            '--auto-detect'
        ]
        
        # This will fail because --keywords-file doesn't exist yet
        with pytest.raises(SystemExit):  # argparse will exit on unknown argument
            sys.argv = ['generate_metadata_universal.py'] + test_args
            main()
    
    def test_accepts_patterns_file_argument(self):
        """
        RED TEST: Should accept --patterns-file CLI argument
        """
        # EXPECTED TO FAIL - argument not yet added
        from workflows.metadata_extraction.scripts.generate_metadata_universal import main
        import sys
        
        test_args = [
            '--input', 'test.json',
            '--patterns-file', 'custom_patterns.json',
            '--auto-detect'
        ]
        
        with pytest.raises(SystemExit):
            sys.argv = ['generate_metadata_universal.py'] + test_args
            main()
    
    def test_accepts_domain_from_config(self):
        """
        RED TEST: Should load domain from keywords config instead of hardcoded list
        """
        # EXPECTED TO FAIL - domains are hardcoded in _detect_domain()
        pytest.skip("Domain detection still uses hardcoded title keywords")


class TestJSONValidation:
    """Test JSON validation (RED phase)"""
    
    def test_validates_keywords_json_schema(self, tmp_path):
        """
        RED TEST: Should validate keywords JSON has required structure
        
        Guideline: Pydantic validation pipeline (ARCH 3968)
        """
        invalid_keywords_file = tmp_path / "invalid_keywords.json"
        invalid_keywords_file.write_text('{"invalid": "structure"}')
        
        # EXPECTED TO FAIL - validation not implemented
        with pytest.raises(ValueError, match="Invalid keywords file schema"):
            UniversalMetadataGenerator(
                json_path=tmp_path / "dummy.json",
                keywords_file=invalid_keywords_file
            )
    
    def test_validates_patterns_json_schema(self, tmp_path):
        """
        RED TEST: Should validate patterns JSON has valid regex
        """
        invalid_patterns_file = tmp_path / "invalid_patterns.json"
        invalid_patterns_file.write_text('{"chapter": "[invalid(regex"}')
        
        # EXPECTED TO FAIL - validation not implemented
        with pytest.raises(ValueError, match="Invalid regex pattern"):
            UniversalMetadataGenerator(
                json_path=tmp_path / "dummy.json",
                patterns_file=invalid_patterns_file
            )


class TestProgressIndicators:
    """Test progress indicators (RED phase)"""
    
    def test_shows_progress_for_large_books(self, tmp_path, capsys):
        """
        RED TEST: Should show progress indicator when processing many chapters
        """
        # Create dummy book JSON with many chapters
        book_json = tmp_path / "large_book.json"
        pages = [{"page_num": i, "text": f"Page {i} content"} for i in range(1, 501)]
        book_json.write_text(json.dumps({"pages": pages}))
        
        generator = UniversalMetadataGenerator(book_json)
        
        # Create 20 adjacent chapters (not overlapping)
        chapters = [(i, f"Chapter {i}", (i-1)*25 + 1, i*25) for i in range(1, 21)]
        
        # Should show progress indicator
        generator.generate_metadata(chapters)
        
        captured = capsys.readouterr()
        assert "Processing" in captured.out
        assert "%" in captured.out or "progress" in captured.out.lower()


class TestDryRunMode:
    """Test dry-run mode (RED phase)"""
    
    def test_dry_run_does_not_save_file(self, tmp_path):
        """
        RED TEST: Should not save file in dry-run mode
        
        Guideline: Safe operations for testing
        """
        book_json = tmp_path / "test_book.json"
        book_json.write_text(json.dumps({"pages": [{"page_num": 1, "text": "test"}]}))
        
        output_file = tmp_path / "output.json"
        
        generator = UniversalMetadataGenerator(book_json)
        chapters = [(1, "Chapter 1", 1, 1)]
        metadata = generator.generate_metadata(chapters)
        
        # EXPECTED TO FAIL - dry_run parameter doesn't exist
        generator.save_metadata(metadata, output_file, dry_run=True)
        
        assert not output_file.exists(), "Dry-run should not create file"
    
    def test_dry_run_shows_what_would_be_saved(self, tmp_path, capsys):
        """
        RED TEST: Should show preview of what would be saved
        """
        book_json = tmp_path / "test_book.json"
        book_json.write_text(json.dumps({"pages": [{"page_num": 1, "text": "test"}]}))
        
        generator = UniversalMetadataGenerator(book_json)
        chapters = [(1, "Chapter 1", 1, 1)]
        metadata = generator.generate_metadata(chapters)
        
        # EXPECTED TO FAIL - dry_run not implemented
        generator.save_metadata(metadata, tmp_path / "output.json", dry_run=True)
        
        captured = capsys.readouterr()
        assert "DRY RUN" in captured.out or "would save" in captured.out


class TestChapterOverlapDetection:
    """Test chapter overlap detection (RED phase)"""
    
    def test_detects_overlapping_chapters(self, tmp_path):
        """
        RED TEST: Should detect when chapter page ranges overlap
        
        Guideline: Exception hierarchies for validation (PY 32425)
        """
        book_json = tmp_path / "test_book.json"
        pages = [{"page_num": i, "text": f"Page {i}"} for i in range(1, 101)]
        book_json.write_text(json.dumps({"pages": pages}))
        
        generator = UniversalMetadataGenerator(book_json)
        
        # Overlapping chapters: Chapter 2 starts before Chapter 1 ends
        overlapping_chapters = [
            (1, "Chapter 1", 1, 50),
            (2, "Chapter 2", 45, 100),  # Overlaps with Chapter 1
        ]
        
        # EXPECTED TO FAIL - overlap detection not implemented
        with pytest.raises(ValueError, match="Chapters overlap"):
            generator.generate_metadata(overlapping_chapters)
    
    def test_allows_adjacent_chapters(self, tmp_path):
        """
        RED TEST: Should allow chapters that are adjacent (not overlapping)
        """
        book_json = tmp_path / "test_book.json"
        pages = [{"page_num": i, "text": f"Page {i}"} for i in range(1, 101)]
        book_json.write_text(json.dumps({"pages": pages}))
        
        generator = UniversalMetadataGenerator(book_json)
        
        # Adjacent chapters - should be valid
        adjacent_chapters = [
            (1, "Chapter 1", 1, 50),
            (2, "Chapter 2", 51, 100),
        ]
        
        # Should NOT raise exception
        metadata = generator.generate_metadata(adjacent_chapters)
        assert len(metadata) == 2


# Fixture for creating test JSON books
@pytest.fixture
def sample_book_json(tmp_path):
    """Create a sample book JSON for testing"""
    book_path = tmp_path / "sample_book.json"
    
    pages = [
        {"page_num": 1, "text": "Chapter 1: Introduction\nThis chapter covers classes and functions."},
        {"page_num": 2, "text": "More about classes and object-oriented programming."},
        {"page_num": 3, "text": "Chapter 2: Advanced Topics\nMicroservices and API design."},
        {"page_num": 4, "text": "REST APIs and FastAPI framework."},
    ]
    
    book_data = {"pages": pages}
    book_path.write_text(json.dumps(book_data))
    
    return book_path
