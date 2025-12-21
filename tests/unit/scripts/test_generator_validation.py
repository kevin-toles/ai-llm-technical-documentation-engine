"""Tests for _validate_chapter_ranges() and summary extraction in generate_metadata_universal.py.

WBS-AC7.4d: Add tests for _validate_chapter_ranges() edge cases.

Coverage targets:
- Lines 350-357: Summary extraction exception fallback
- Lines 548-554: _validate_chapter_ranges() method
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
# Test Summary Extraction Fallback
# =============================================================================


class TestSummaryExtractionFallback:
    """AC7.4d: Test summary extraction exception fallback."""

    def test_summary_fallback_returns_chapter_title(self, tmp_path: Path) -> None:
        """AC7.4d: When summary extraction fails, returns chapter title fallback."""
        from workflows.metadata_extraction.scripts.generate_metadata_universal import (
            UniversalMetadataGenerator,
        )

        book_data = {
            "title": "Summary Test Book",
            "pages": [{"page_number": 1, "content": "Test content"}]
        }
        json_file = tmp_path / "summary_book.json"
        json_file.write_text(json.dumps(book_data))

        generator = UniversalMetadataGenerator(json_file)
        
        # Mock extractor to return empty string (triggering fallback)
        with patch.object(generator.extractor, 'generate_summary', return_value=""):
            summary = generator.generate_summary("Some content", "Short Chapter", 1)
        
        # Should return fallback (chapter title)
        assert "Chapter 1" in summary or "Short Chapter" in summary

    def test_summary_fallback_on_exception(self, tmp_path: Path) -> None:
        """AC7.4d: Summary falls back gracefully on extractor exception."""
        from workflows.metadata_extraction.scripts.generate_metadata_universal import (
            UniversalMetadataGenerator,
        )

        book_data = {
            "title": "Exception Test Book",
            "pages": [{"page_number": 1, "content": "Test content"}]
        }
        json_file = tmp_path / "exc_book.json"
        json_file.write_text(json.dumps(book_data))

        generator = UniversalMetadataGenerator(json_file)
        
        # Mock extractor to raise exception
        with patch.object(generator.extractor, 'generate_summary', side_effect=Exception("Test error")):
            summary = generator.generate_summary("Some text content", "Test Title", 1)
        
        # Should return fallback without raising
        assert "Chapter 1" in summary or "Test Title" in summary


# =============================================================================
# Test Chapter Range Validation
# =============================================================================


class TestChapterRangeValidation:
    """AC7.4d: Test _validate_chapter_ranges() edge cases."""

    def test_validate_empty_chapters_no_error(self, tmp_path: Path) -> None:
        """AC7.4d: Empty chapters list doesn't raise error."""
        from workflows.metadata_extraction.scripts.generate_metadata_universal import (
            UniversalMetadataGenerator,
        )

        book_data = {
            "title": "Empty Chapters Book",
            "pages": [{"page_number": 1, "content": "Content"}]
        }
        json_file = tmp_path / "empty_chapters.json"
        json_file.write_text(json.dumps(book_data))

        generator = UniversalMetadataGenerator(json_file)
        
        # Validate empty chapters should not raise
        generator._validate_chapter_ranges([])

    def test_validate_overlapping_chapters_raises_error(self, tmp_path: Path) -> None:
        """AC7.4d: Overlapping page ranges raise ValueError."""
        from workflows.metadata_extraction.scripts.generate_metadata_universal import (
            UniversalMetadataGenerator,
        )

        book_data = {
            "title": "Overlap Test Book",
            "pages": [
                {"page_number": i, "content": f"Content {i}"} for i in range(1, 11)
            ]
        }
        json_file = tmp_path / "overlap_book.json"
        json_file.write_text(json.dumps(book_data))

        generator = UniversalMetadataGenerator(json_file)
        
        # Chapters with overlapping page ranges
        chapters = [
            (1, "Intro", 1, 5),
            (2, "Advanced", 3, 8)  # Starts at 3, but chapter 1 ends at 5 - overlap!
        ]
        
        with pytest.raises(ValueError, match="overlap"):
            generator._validate_chapter_ranges(chapters)

    def test_validate_adjacent_chapters_ok(self, tmp_path: Path) -> None:
        """AC7.4d: Adjacent (non-overlapping) chapters pass validation."""
        from workflows.metadata_extraction.scripts.generate_metadata_universal import (
            UniversalMetadataGenerator,
        )

        book_data = {
            "title": "Adjacent Test Book",
            "pages": [
                {"page_number": i, "content": f"Content {i}"} for i in range(1, 11)
            ]
        }
        json_file = tmp_path / "adjacent_book.json"
        json_file.write_text(json.dumps(book_data))

        generator = UniversalMetadataGenerator(json_file)
        
        # Adjacent chapters (no overlap)
        chapters = [
            (1, "Intro", 1, 4),
            (2, "Advanced", 5, 10)  # Starts at 5, chapter 1 ends at 4 - no overlap
        ]
        
        # Should not raise
        generator._validate_chapter_ranges(chapters)


# =============================================================================
# Test Generate Metadata Full Pipeline
# =============================================================================


class TestGenerateMetadataFullPipeline:
    """Test the full generate_metadata() pipeline."""

    def test_generate_metadata_produces_chapter_metadata(self, tmp_path: Path) -> None:
        """Test that generate_metadata returns ChapterMetadata objects."""
        from workflows.metadata_extraction.scripts.generate_metadata_universal import (
            UniversalMetadataGenerator,
            ChapterMetadata,
        )

        book_data = {
            "title": "Pipeline Test Book",
            "pages": [
                {"page_number": 1, "content": "Introduction to machine learning algorithms and neural network architectures. This chapter covers the fundamentals."},
                {"page_number": 2, "content": "More details about deep learning and convolutional neural networks."},
            ]
        }
        json_file = tmp_path / "pipeline_book.json"
        json_file.write_text(json.dumps(book_data))

        generator = UniversalMetadataGenerator(json_file)
        
        chapters = [(1, "Introduction", 1, 2)]
        metadata_list = generator.generate_metadata(chapters)
        
        assert len(metadata_list) == 1
        assert isinstance(metadata_list[0], ChapterMetadata)
        assert metadata_list[0].chapter_number == 1
        assert metadata_list[0].title == "Introduction"

    def test_generate_metadata_extracts_keywords(self, tmp_path: Path) -> None:
        """Test that generate_metadata extracts keywords."""
        from workflows.metadata_extraction.scripts.generate_metadata_universal import (
            UniversalMetadataGenerator,
        )

        book_data = {
            "title": "Keywords Test Book",
            "pages": [
                {"page_number": 1, "content": "Machine learning algorithms for neural networks. Deep learning and transformers. Kubernetes container orchestration."},
            ]
        }
        json_file = tmp_path / "keywords_book.json"
        json_file.write_text(json.dumps(book_data))

        generator = UniversalMetadataGenerator(json_file)
        
        chapters = [(1, "ML Chapter", 1, 1)]
        metadata_list = generator.generate_metadata(chapters)
        
        # Should have extracted some keywords
        assert len(metadata_list[0].keywords) > 0

    def test_generate_metadata_empty_chapters_returns_empty(self, tmp_path: Path) -> None:
        """Test that generate_metadata with empty chapters returns empty list."""
        from workflows.metadata_extraction.scripts.generate_metadata_universal import (
            UniversalMetadataGenerator,
        )

        book_data = {
            "title": "Empty Test Book",
            "pages": [{"page_number": 1, "content": "Content"}]
        }
        json_file = tmp_path / "empty_test.json"
        json_file.write_text(json.dumps(book_data))

        generator = UniversalMetadataGenerator(json_file)
        
        metadata_list = generator.generate_metadata([])
        
        assert metadata_list == []
