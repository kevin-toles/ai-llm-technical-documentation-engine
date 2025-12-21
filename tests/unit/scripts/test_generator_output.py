"""Tests for save_metadata() and output paths in generate_metadata_universal.py.

WBS-AC7.4c: Add tests for save_metadata() and output paths.

Coverage targets:
- Lines 727-755: save_metadata() method
- Dry run mode
- Default output path
- Custom output path
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List
from unittest.mock import MagicMock, patch

import pytest

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def sample_book_data() -> Dict[str, Any]:
    """Minimal book data for testing."""
    return {
        "title": "Test Output Book",
        "metadata": {},
        "pages": [
            {"page_number": 1, "content": "Chapter 1: Test\n\nTest content about machine learning."},
            {"page_number": 2, "content": "More test content about neural networks and deep learning."},
        ]
    }


@pytest.fixture
def sample_metadata_list() -> List[Any]:
    """Sample ChapterMetadata objects for testing."""
    from workflows.metadata_extraction.scripts.generate_metadata_universal import ChapterMetadata
    
    return [
        ChapterMetadata(
            chapter_number=1,
            title="Introduction",
            start_page=1,
            end_page=5,
            keywords=["machine learning", "neural networks"],
            concepts=["AI", "Deep Learning"],
            summary="Introduction to ML concepts."
        ),
        ChapterMetadata(
            chapter_number=2,
            title="Advanced Topics",
            start_page=6,
            end_page=10,
            keywords=["transformers", "attention"],
            concepts=["NLP", "Architectures"],
            summary="Advanced ML architectures."
        )
    ]


# =============================================================================
# Test save_metadata() - Dry Run Mode
# =============================================================================


class TestSaveMetadataDryRun:
    """AC7.4c: Test dry run mode doesn't write files."""

    def test_dry_run_does_not_create_file(
        self, sample_book_data: Dict[str, Any], sample_metadata_list: List[Any], tmp_path: Path
    ) -> None:
        """AC7.4c: Dry run mode shows preview but doesn't write."""
        from workflows.metadata_extraction.scripts.generate_metadata_universal import (
            UniversalMetadataGenerator,
        )

        json_file = tmp_path / "test_book.json"
        json_file.write_text(json.dumps(sample_book_data))

        output_path = tmp_path / "output" / "metadata.json"

        generator = UniversalMetadataGenerator(json_file)
        result = generator.save_metadata(sample_metadata_list, output_path, dry_run=True)

        # File should NOT be created
        assert not output_path.exists(), "Dry run should not create file"
        # But should return the path that WOULD be used
        assert result == output_path

    def test_dry_run_returns_output_path(
        self, sample_book_data: Dict[str, Any], sample_metadata_list: List[Any], tmp_path: Path
    ) -> None:
        """AC7.4c: Dry run returns the path that would be used."""
        from workflows.metadata_extraction.scripts.generate_metadata_universal import (
            UniversalMetadataGenerator,
        )

        json_file = tmp_path / "test_book.json"
        json_file.write_text(json.dumps(sample_book_data))

        output_path = tmp_path / "custom_output.json"

        generator = UniversalMetadataGenerator(json_file)
        result = generator.save_metadata(sample_metadata_list, output_path, dry_run=True)

        assert result == output_path


# =============================================================================
# Test save_metadata() - Actual Write
# =============================================================================


class TestSaveMetadataWrite:
    """AC7.4c: Test actual file writing."""

    def test_save_creates_file(
        self, sample_book_data: Dict[str, Any], sample_metadata_list: List[Any], tmp_path: Path
    ) -> None:
        """AC7.4c: save_metadata creates the output file."""
        from workflows.metadata_extraction.scripts.generate_metadata_universal import (
            UniversalMetadataGenerator,
        )

        json_file = tmp_path / "test_book.json"
        json_file.write_text(json.dumps(sample_book_data))

        output_path = tmp_path / "output" / "metadata.json"

        generator = UniversalMetadataGenerator(json_file)
        result = generator.save_metadata(sample_metadata_list, output_path)

        # File should be created
        assert output_path.exists(), "File should be created"
        assert result == output_path

    def test_save_creates_parent_directories(
        self, sample_book_data: Dict[str, Any], sample_metadata_list: List[Any], tmp_path: Path
    ) -> None:
        """AC7.4c: save_metadata creates parent directories if needed."""
        from workflows.metadata_extraction.scripts.generate_metadata_universal import (
            UniversalMetadataGenerator,
        )

        json_file = tmp_path / "test_book.json"
        json_file.write_text(json.dumps(sample_book_data))

        # Nested path
        output_path = tmp_path / "deep" / "nested" / "path" / "metadata.json"

        generator = UniversalMetadataGenerator(json_file)
        result = generator.save_metadata(sample_metadata_list, output_path)

        assert output_path.exists()
        assert output_path.parent.exists()

    def test_save_writes_valid_json(
        self, sample_book_data: Dict[str, Any], sample_metadata_list: List[Any], tmp_path: Path
    ) -> None:
        """AC7.4c: Saved file contains valid JSON."""
        from workflows.metadata_extraction.scripts.generate_metadata_universal import (
            UniversalMetadataGenerator,
        )

        json_file = tmp_path / "test_book.json"
        json_file.write_text(json.dumps(sample_book_data))

        output_path = tmp_path / "metadata.json"

        generator = UniversalMetadataGenerator(json_file)
        generator.save_metadata(sample_metadata_list, output_path)

        # Should be valid JSON
        with open(output_path) as f:
            loaded = json.load(f)
        
        assert isinstance(loaded, list)
        assert len(loaded) == 2
        assert loaded[0]["chapter_number"] == 1

    def test_save_includes_all_metadata_fields(
        self, sample_book_data: Dict[str, Any], sample_metadata_list: List[Any], tmp_path: Path
    ) -> None:
        """AC7.4c: Saved JSON includes all ChapterMetadata fields."""
        from workflows.metadata_extraction.scripts.generate_metadata_universal import (
            UniversalMetadataGenerator,
        )

        json_file = tmp_path / "test_book.json"
        json_file.write_text(json.dumps(sample_book_data))

        output_path = tmp_path / "metadata.json"

        generator = UniversalMetadataGenerator(json_file)
        generator.save_metadata(sample_metadata_list, output_path)

        with open(output_path) as f:
            loaded = json.load(f)
        
        # Check all expected fields
        expected_fields = {"chapter_number", "title", "start_page", "end_page", 
                          "keywords", "concepts", "summary"}
        assert expected_fields.issubset(set(loaded[0].keys()))


# =============================================================================
# Test Default Output Path
# =============================================================================


class TestDefaultOutputPath:
    """AC7.4c: Test default output path generation."""

    def test_default_path_uses_book_name(
        self, sample_book_data: Dict[str, Any], sample_metadata_list: List[Any], tmp_path: Path
    ) -> None:
        """AC7.4c: Default path is data/metadata/{book_name}_metadata.json."""
        from workflows.metadata_extraction.scripts.generate_metadata_universal import (
            UniversalMetadataGenerator,
        )

        json_file = tmp_path / "MyTestBook.json"
        json_file.write_text(json.dumps(sample_book_data))

        generator = UniversalMetadataGenerator(json_file)
        
        # Call save_metadata with dry_run to see what path would be used
        # without output_path, it should use default
        with patch('workflows.metadata_extraction.scripts.generate_metadata_universal.DEFAULT_METADATA_DIR', tmp_path):
            result = generator.save_metadata(sample_metadata_list, output_path=None, dry_run=True)
        
        # Path should include book name
        assert "MyTestBook" in str(result)
        assert result.suffix == ".json"


# =============================================================================
# Test ChapterMetadata.to_dict()
# =============================================================================


class TestChapterMetadataToDict:
    """Test ChapterMetadata dataclass serialization."""

    def test_to_dict_includes_all_fields(self) -> None:
        """AC7.4c: to_dict() includes all dataclass fields."""
        from workflows.metadata_extraction.scripts.generate_metadata_universal import ChapterMetadata

        metadata = ChapterMetadata(
            chapter_number=1,
            title="Test",
            start_page=1,
            end_page=10,
            keywords=["k1", "k2"],
            concepts=["c1"],
            summary="Test summary"
        )

        result = metadata.to_dict()

        assert result["chapter_number"] == 1
        assert result["title"] == "Test"
        assert result["start_page"] == 1
        assert result["end_page"] == 10
        assert result["keywords"] == ["k1", "k2"]
        assert result["concepts"] == ["c1"]
        assert result["summary"] == "Test summary"

    def test_to_dict_returns_dict(self) -> None:
        """AC7.4c: to_dict() returns a dictionary."""
        from workflows.metadata_extraction.scripts.generate_metadata_universal import ChapterMetadata

        metadata = ChapterMetadata(
            chapter_number=1,
            title="Test",
            start_page=1,
            end_page=10,
            keywords=[],
            concepts=[],
            summary=""
        )

        result = metadata.to_dict()
        assert isinstance(result, dict)
