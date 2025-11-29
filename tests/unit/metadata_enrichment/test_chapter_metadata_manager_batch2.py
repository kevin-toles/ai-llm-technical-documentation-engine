"""
Unit tests for ChapterMetadataManager.get_chapters (CC 8)

Tests focus on get_chapters method with CC 8:
- Priority logic: Manual override > Auto-detected > Manual fallback
- Chapter data parsing and validation
- Error handling for malformed data
- Chapter sorting by number

Architecture Patterns Applied:
- Repository Pattern: Data access abstraction (Architecture Patterns Ch. 2)
- Strategy Pattern: Multiple data source strategies (Architecture Patterns Ch. 13)
- Value Object Pattern: ChapterInfo immutability (DDD)

Sprint: Batch #2 File #8 (HIGH priority, CC 8, tests only)
"""

import pytest
import sys
from pathlib import Path
from typing import List, Dict, Any
from unittest.mock import Mock, MagicMock, patch, mock_open

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
def sample_auto_detected():
    """Sample auto-detected chapter data."""
    return {
        'Python_Distilled.json': [
            {
                'chapter_number': 1,
                'title': 'Python Basics',
                'start_page': 1,
                'end_page': 50,
                'keywords': ['syntax', 'variables'],
                'summary': 'Introduction to Python',
                'concepts': ['basics', 'syntax']
            },
            {
                'chapter_number': 2,
                'title': 'Data Structures',
                'start_page': 51,
                'end_page': 100,
                'keywords': ['list', 'dict'],
                'summary': 'Core data structures',
                'concepts': ['collections', 'iteration']
            }
        ]
    }


@pytest.fixture
def sample_manual_metadata():
    """Sample manual metadata."""
    return {
        'Fluent_Python_2nd.json': {
            'chapters': [
                {
                    'chapter_number': 1,
                    'title': 'The Python Data Model',
                    'start_page': 1,
                    'end_page': 30,
                    'keywords': ['special methods', 'protocols'],
                    'summary': 'Python data model',
                    'concepts': ['dunder methods', 'protocols']
                }
            ]
        }
    }


@pytest.fixture
def manager_with_data(sample_auto_detected, sample_manual_metadata):
    """Create manager with test data."""
    manager = ChapterMetadataManager()
    manager.auto_detected = sample_auto_detected
    manager.manual_metadata = sample_manual_metadata
    manager.override_files = []
    return manager


# ============================================================================
# TEST CLASS: get_chapters (CC 8)
# ============================================================================

class TestGetChapters:
    """
    Test ChapterMetadataManager.get_chapters method.
    
    This method retrieves chapter metadata with priority logic:
    1. Manual (if in override list)
    2. Auto-detected
    3. Manual fallback
    
    Complexity: CC 8 (multiple conditional paths, error handling)
    Pattern: Strategy Pattern for data source selection
    """
    
    def test_get_chapters_from_auto_detected(self, manager_with_data):
        """Test retrieval from auto-detected source."""
        # Arrange
        filename = 'Python_Distilled.json'
        
        # Act
        chapters = manager_with_data.get_chapters(filename)
        
        # Assert
        assert len(chapters) == 2
        assert all(isinstance(ch, ChapterInfo) for ch in chapters)
        assert chapters[0].chapter_number == 1
        assert chapters[0].title == 'Python Basics'
        assert chapters[1].chapter_number == 2
    
    def test_get_chapters_from_manual_metadata(self, manager_with_data):
        """Test retrieval from manual metadata."""
        # Arrange
        filename = 'Fluent_Python_2nd.json'
        
        # Act
        chapters = manager_with_data.get_chapters(filename)
        
        # Assert
        assert len(chapters) == 1
        assert isinstance(chapters[0], ChapterInfo)
        assert chapters[0].title == 'The Python Data Model'
        assert chapters[0].start_page == 1
    
    def test_get_chapters_priority_manual_override(self, manager_with_data, sample_manual_metadata):
        """Test manual override takes priority over auto-detected."""
        # Arrange
        filename = 'Python_Distilled.json'
        manager_with_data.override_files = ['Python_Distilled.json']
        manager_with_data.manual_metadata['Python_Distilled.json'] = {
            'chapters': [
                {
                    'chapter_number': 99,
                    'title': 'Override Chapter',
                    'start_page': 1,
                    'end_page': 10
                }
            ]
        }
        
        # Act
        chapters = manager_with_data.get_chapters(filename)
        
        # Assert - should use manual override
        assert len(chapters) == 1
        assert chapters[0].chapter_number == 99
        assert chapters[0].title == 'Override Chapter'
    
    def test_get_chapters_missing_file_returns_empty(self, manager_with_data):
        """Test missing file returns empty list."""
        # Arrange
        filename = 'NonexistentBook.json'
        
        # Act
        chapters = manager_with_data.get_chapters(filename)
        
        # Assert
        assert chapters == []
    
    def test_get_chapters_sorts_by_chapter_number(self, manager_with_data):
        """Test chapters are sorted by chapter_number."""
        # Arrange
        filename = 'Unsorted.json'
        manager_with_data.auto_detected['Unsorted.json'] = [
            {'chapter_number': 3, 'title': 'Third', 'start_page': 50, 'end_page': 75},
            {'chapter_number': 1, 'title': 'First', 'start_page': 1, 'end_page': 25},
            {'chapter_number': 2, 'title': 'Second', 'start_page': 26, 'end_page': 49}
        ]
        
        # Act
        chapters = manager_with_data.get_chapters(filename)
        
        # Assert - should be sorted
        assert len(chapters) == 3
        assert chapters[0].chapter_number == 1
        assert chapters[1].chapter_number == 2
        assert chapters[2].chapter_number == 3
    
    def test_get_chapters_handles_missing_optional_fields(self, manager_with_data):
        """Test graceful handling of missing optional fields."""
        # Arrange
        filename = 'MinimalData.json'
        manager_with_data.auto_detected['MinimalData.json'] = [
            {
                'chapter_number': 1,
                'title': 'Basic Chapter',
                'start_page': 1,
                'end_page': 10
                # Missing: keywords, summary, concepts
            }
        ]
        
        # Act
        chapters = manager_with_data.get_chapters(filename)
        
        # Assert - should handle missing fields with defaults
        assert len(chapters) == 1
        assert chapters[0].keywords == []
        assert chapters[0].summary == ''
        assert chapters[0].concepts == []
    
    def test_get_chapters_calculates_page_count(self, manager_with_data):
        """Test page_count calculation when not provided."""
        # Arrange
        filename = 'PageCount.json'
        manager_with_data.auto_detected['PageCount.json'] = [
            {
                'chapter_number': 1,
                'title': 'Test',
                'start_page': 10,
                'end_page': 20
                # Missing: page_count (should calculate: 20 - 10 + 1 = 11)
            }
        ]
        
        # Act
        chapters = manager_with_data.get_chapters(filename)
        
        # Assert
        assert len(chapters) == 1
        assert chapters[0].page_count == 11
    
    def test_get_chapters_skips_malformed_entries(self, manager_with_data, capsys):
        """Test continues processing when encountering malformed data."""
        # Arrange
        filename = 'Malformed.json'
        manager_with_data.auto_detected['Malformed.json'] = [
            {
                'chapter_number': 1,
                'title': 'Valid Chapter',
                'start_page': 1,
                'end_page': 10
            },
            {
                # Malformed: missing title - should use defaults
                'chapter_number': 2
            },
            {
                'chapter_number': 3,
                'title': 'Another Valid',
                'start_page': 11,
                'end_page': 20
            }
        ]
        
        # Act
        chapters = manager_with_data.get_chapters(filename)
        
        # Assert - implementation uses defaults for missing fields
        assert len(chapters) == 3
        assert chapters[0].chapter_number == 1
        assert chapters[1].chapter_number == 2
        assert chapters[1].title == 'Unknown'  # Default title
        assert chapters[2].chapter_number == 3
    
    def test_get_chapters_preserves_all_fields(self, manager_with_data):
        """Test all ChapterInfo fields are properly populated."""
        # Arrange
        filename = 'Complete.json'
        manager_with_data.auto_detected['Complete.json'] = [
            {
                'chapter_number': 5,
                'title': 'Complete Chapter',
                'start_page': 100,
                'end_page': 150,
                'page_count': 51,
                'keywords': ['keyword1', 'keyword2', 'keyword3'],
                'summary': 'This is a complete chapter summary',
                'concepts': ['concept1', 'concept2']
            }
        ]
        
        # Act
        chapters = manager_with_data.get_chapters(filename)
        
        # Assert - all fields preserved
        assert len(chapters) == 1
        ch = chapters[0]
        assert ch.chapter_number == 5
        assert ch.title == 'Complete Chapter'
        assert ch.start_page == 100
        assert ch.end_page == 150
        assert ch.page_count == 51
        assert ch.keywords == ['keyword1', 'keyword2', 'keyword3']
        assert ch.summary == 'This is a complete chapter summary'
        assert ch.concepts == ['concept1', 'concept2']


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestChapterMetadataManagerIntegration:
    """Integration tests for ChapterMetadataManager data source priority."""
    
    def test_three_tier_priority_system(self):
        """Test complete priority system: override > auto > manual."""
        # Arrange
        manager = ChapterMetadataManager()
        filename = 'test_book.json'
        
        # Set up all three sources
        manager.auto_detected[filename] = [
            {'chapter_number': 1, 'title': 'Auto', 'start_page': 1, 'end_page': 10}
        ]
        manager.manual_metadata[filename] = {
            'chapters': [
                {'chapter_number': 2, 'title': 'Manual', 'start_page': 1, 'end_page': 10}
            ]
        }
        manager.override_files = [filename]
        
        # Act
        chapters = manager.get_chapters(filename)
        
        # Assert - should use manual (override priority)
        assert len(chapters) == 1
        assert chapters[0].title == 'Manual'
    
    def test_fallback_chain_auto_to_manual(self):
        """Test fallback from auto-detected to manual."""
        # Arrange
        manager = ChapterMetadataManager()
        filename = 'fallback_test.json'
        
        # Only manual metadata available
        manager.manual_metadata[filename] = {
            'chapters': [
                {'chapter_number': 1, 'title': 'Manual Fallback', 'start_page': 1, 'end_page': 10}
            ]
        }
        
        # Act
        chapters = manager.get_chapters(filename)
        
        # Assert - should use manual as fallback
        assert len(chapters) == 1
        assert chapters[0].title == 'Manual Fallback'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
