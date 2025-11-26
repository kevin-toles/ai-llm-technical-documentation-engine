"""
Unit tests for chapter_metadata_manager.py

Tests focus on ChapterMetadataManager methods with CC 8:
- get_chapters (CC 8) - Repository pattern for chapter metadata retrieval

Architecture Patterns Applied:
- Repository Pattern: Test data access abstraction (Architecture Patterns Ch. 2)
- Strategy Pattern: Test priority logic (manual > auto-detected)
- Factory Pattern: Test ChapterInfo object creation

Sprint: Batch #2 Files 6-11 (HIGH priority, CC 8-9, tests only)
"""

import pytest
import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
from typing import List, Dict

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from workflows.metadata_enrichment.scripts.chapter_metadata_manager import (
    ChapterMetadataManager,
    ChapterInfo
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def temp_cache_dir(tmp_path):
    """Create temporary directory for cache files."""
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    return cache_dir


@pytest.fixture
def mock_auto_detected_data():
    """Sample auto-detected chapter metadata."""
    return {
        "Fluent_Python_2nd_Content.json": {
            "chapters": [
                {
                    "chapter_number": 1,
                    "title": "The Python Data Model",
                    "start_page": 1,
                    "end_page": 25,
                    "keywords": ["data model", "dunder methods", "__repr__"]
                },
                {
                    "chapter_number": 2,
                    "title": "An Array of Sequences",
                    "start_page": 26,
                    "end_page": 60,
                    "keywords": ["list", "tuple", "array"]
                }
            ]
        }
    }


@pytest.fixture
def mock_manual_data():
    """Sample manual chapter metadata with override."""
    return {
        "_override_auto_detection": {
            "files": ["Fluent_Python_2nd_Content.json"]
        },
        "Fluent_Python_2nd_Content.json": {
            "chapters": [
                {
                    "chapter_number": 1,
                    "title": "The Python Data Model (Manual)",
                    "start_page": 1,
                    "end_page": 25,
                    "keywords": ["data model", "dunder", "__repr__", "__str__"],
                    "summary": "Manual summary"
                }
            ]
        }
    }


@pytest.fixture
def chapter_manager(temp_cache_dir, mock_auto_detected_data):
    """Create ChapterMetadataManager with mock data."""
    cache_file = temp_cache_dir / "chapter_metadata_cache.json"
    manual_file = temp_cache_dir / "chapter_metadata_manual.json"
    
    # Write mock cache file
    with open(cache_file, 'w') as f:
        json.dump(mock_auto_detected_data, f)
    
    return ChapterMetadataManager(scripts_dir=str(temp_cache_dir))


# ============================================================================
# TEST get_chapters (CC 8)
# ============================================================================

class TestGetChapters:
    """
    Test suite for ChapterMetadataManager.get_chapters method.
    
    This method implements Repository pattern for chapter metadata:
    - Provides unified access to chapter data from multiple sources
    - Priority: Manual corrections > Auto-detected metadata
    - Handles missing files gracefully
    - Converts raw metadata to ChapterInfo objects
    
    Complexity: CC 8 (multiple conditional branches, source prioritization)
    Pattern: Repository Pattern (Architecture Patterns Ch. 2)
    """
    
    def test_get_chapters_from_auto_detected(self, chapter_manager):
        """Test retrieving chapters from auto-detected metadata."""
        chapters = chapter_manager.get_chapters("Fluent_Python_2nd_Content.json")
        
        assert isinstance(chapters, list)
        assert len(chapters) == 2
        assert all(isinstance(ch, ChapterInfo) for ch in chapters)
        assert chapters[0].title == "The Python Data Model"
        assert chapters[0].start_page == 1
        assert chapters[0].end_page == 25
    
    def test_get_chapters_manual_overrides_auto_detected(
        self, temp_cache_dir, mock_auto_detected_data, mock_manual_data
    ):
        """Test that manual metadata overrides auto-detected when in override list."""
        # Write both cache and manual files
        cache_file = temp_cache_dir / "chapter_metadata_cache.json"
        manual_file = temp_cache_dir / "chapter_metadata_manual.json"
        
        with open(cache_file, 'w') as f:
            json.dump(mock_auto_detected_data, f)
        with open(manual_file, 'w') as f:
            json.dump(mock_manual_data, f)
        
        manager = ChapterMetadataManager(scripts_dir=str(temp_cache_dir))
        chapters = manager.get_chapters("Fluent_Python_2nd_Content.json")
        
        # Should use manual data (has "Manual" suffix in title)
        assert len(chapters) >= 1
        assert "Manual" in chapters[0].title or chapters[0].summary == "Manual summary"
    
    def test_get_chapters_with_missing_file(self, chapter_manager):
        """Test behavior when requesting chapters for non-existent file."""
        chapters = chapter_manager.get_chapters("NonExistent_Book.json")
        
        # Should return empty list for missing files
        assert isinstance(chapters, list)
        assert len(chapters) == 0
    
    def test_get_chapters_creates_chapter_info_objects(self, chapter_manager):
        """Test that returned chapters are ChapterInfo objects."""
        chapters = chapter_manager.get_chapters("Fluent_Python_2nd_Content.json")
        
        for chapter in chapters:
            assert isinstance(chapter, ChapterInfo)
            assert hasattr(chapter, 'chapter_number')
            assert hasattr(chapter, 'title')
            assert hasattr(chapter, 'start_page')
            assert hasattr(chapter, 'end_page')
            assert hasattr(chapter, 'keywords')
    
    def test_get_chapters_calculates_page_count(self, chapter_manager):
        """Test that ChapterInfo includes calculated page_count."""
        chapters = chapter_manager.get_chapters("Fluent_Python_2nd_Content.json")
        
        assert chapters[0].page_count == 25  # end_page - start_page + 1
        assert chapters[1].page_count == 35
    
    def test_get_chapters_includes_keywords(self, chapter_manager):
        """Test that chapters include keyword lists."""
        chapters = chapter_manager.get_chapters("Fluent_Python_2nd_Content.json")
        
        assert isinstance(chapters[0].keywords, list)
        assert len(chapters[0].keywords) > 0
        assert "data model" in chapters[0].keywords
    
    def test_get_chapters_handles_missing_optional_fields(self, temp_cache_dir):
        """Test handling of chapters with missing summary/concepts."""
        data = {
            "Test_Book.json": {
                "chapters": [
                    {
                        "chapter_number": 1,
                        "title": "Minimal Chapter",
                        "start_page": 1,
                        "end_page": 10,
                        "keywords": []
                        # No summary or concepts
                    }
                ]
            }
        }
        
        cache_file = temp_cache_dir / "chapter_metadata_cache.json"
        with open(cache_file, 'w') as f:
            json.dump(data, f)
        
        manager = ChapterMetadataManager(scripts_dir=str(temp_cache_dir))
        chapters = manager.get_chapters("Test_Book.json")
        
        assert len(chapters) == 1
        assert chapters[0].summary == ""  # Default empty string
        assert chapters[0].concepts == []  # Default empty list
    
    def test_get_chapters_preserves_chapter_order(self, chapter_manager):
        """Test that chapters are returned in correct order."""
        chapters = chapter_manager.get_chapters("Fluent_Python_2nd_Content.json")
        
        # Should be ordered by chapter_number
        assert chapters[0].chapter_number < chapters[1].chapter_number
    
    def test_get_chapters_with_empty_cache(self, temp_cache_dir):
        """Test behavior with empty cache file."""
        cache_file = temp_cache_dir / "chapter_metadata_cache.json"
        with open(cache_file, 'w') as f:
            json.dump({}, f)
        
        manager = ChapterMetadataManager(scripts_dir=str(temp_cache_dir))
        chapters = manager.get_chapters("Any_Book.json")
        
        assert isinstance(chapters, list)
        assert len(chapters) == 0


# ============================================================================
# TEST ChapterInfo
# ============================================================================

class TestChapterInfo:
    """Test ChapterInfo dataclass functionality."""
    
    def test_chapter_info_creation(self):
        """Test creating ChapterInfo with required fields."""
        chapter = ChapterInfo(
            chapter_number=5,
            title="Test Chapter",
            start_page=100,
            end_page=125,
            page_count=26,
            keywords=["test", "example"]
        )
        
        assert chapter.chapter_number == 5
        assert chapter.title == "Test Chapter"
        assert chapter.start_page == 100
        assert chapter.end_page == 125
    
    def test_chapter_info_string_representation(self):
        """Test ChapterInfo __str__ method."""
        chapter = ChapterInfo(
            chapter_number=3,
            title="Functions",
            start_page=50,
            end_page=75,
            page_count=26,
            keywords=[]
        )
        
        str_repr = str(chapter)
        assert "3" in str_repr
        assert "Functions" in str_repr
        assert "50" in str_repr
        assert "75" in str_repr
    
    def test_chapter_info_compact_string(self):
        """Test ChapterInfo to_compact_string method."""
        chapter = ChapterInfo(
            chapter_number=10,
            title="Advanced Topics",
            start_page=200,
            end_page=250,
            page_count=51,
            keywords=[]
        )
        
        compact = chapter.to_compact_string()
        assert "10" in compact
        assert "Advanced Topics" in compact
        assert "200" in compact
        assert "250" in compact
    
    def test_chapter_info_post_init_concepts(self):
        """Test that concepts field is initialized to empty list."""
        chapter = ChapterInfo(
            chapter_number=1,
            title="Intro",
            start_page=1,
            end_page=10,
            page_count=10,
            keywords=[]
        )
        
        assert chapter.concepts == []


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestChapterMetadataManagerIntegration:
    """Integration tests for ChapterMetadataManager."""
    
    def test_manager_loads_multiple_books(
        self, temp_cache_dir, mock_auto_detected_data
    ):
        """Test manager can handle multiple books."""
        # Add second book to cache
        mock_auto_detected_data["Python_Distilled_Content.json"] = {
            "chapters": [
                {
                    "chapter_number": 1,
                    "title": "Python Basics",
                    "start_page": 1,
                    "end_page": 30,
                    "keywords": ["basics"]
                }
            ]
        }
        
        cache_file = temp_cache_dir / "chapter_metadata_cache.json"
        with open(cache_file, 'w') as f:
            json.dump(mock_auto_detected_data, f)
        
        manager = ChapterMetadataManager(scripts_dir=str(temp_cache_dir))
        
        chapters1 = manager.get_chapters("Fluent_Python_2nd_Content.json")
        chapters2 = manager.get_chapters("Python_Distilled_Content.json")
        
        assert len(chapters1) == 2
        assert len(chapters2) == 1
    
    def test_manager_priority_system(
        self, temp_cache_dir, mock_auto_detected_data, mock_manual_data
    ):
        """Test priority: manual (if in override) > auto-detected."""
        cache_file = temp_cache_dir / "chapter_metadata_cache.json"
        manual_file = temp_cache_dir / "chapter_metadata_manual.json"
        
        with open(cache_file, 'w') as f:
            json.dump(mock_auto_detected_data, f)
        with open(manual_file, 'w') as f:
            json.dump(mock_manual_data, f)
        
        manager = ChapterMetadataManager(scripts_dir=str(temp_cache_dir))
        
        # File in override list should use manual
        chapters = manager.get_chapters("Fluent_Python_2nd_Content.json")
        assert len(chapters) >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
