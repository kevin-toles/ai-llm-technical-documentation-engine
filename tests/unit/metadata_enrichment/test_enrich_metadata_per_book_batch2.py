"""
Unit tests for enrich_metadata_per_book functions (CC 9)

Tests focus on functions with CC 8-9:
- load_cross_book_context (CC 9) - Multiple conditional paths for taxonomy/metadata loading
- build_chapter_corpus (CC 4) - Corpus construction for TF-IDF

Architecture Patterns Applied:
- Repository Pattern: Data access for cross-book metadata (Architecture Patterns Ch. 2)
- Factory Pattern: Corpus construction (Architecture Patterns Ch. 9)
- Service Layer: Orchestration of metadata loading (Architecture Patterns Ch. 4)

Sprint: Batch #2 File #9 (HIGH priority, CC 9, tests only)
"""

import pytest
import json
import sys
from pathlib import Path
from typing import Dict, Any
from unittest.mock import Mock, MagicMock, patch, mock_open

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
    load_cross_book_context,
    build_chapter_corpus
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def sample_taxonomy_with_books():
    """Sample taxonomy with books field."""
    return {
        "tiers": {
            "Architecture": {
                "priority": 1,
                "concepts": ["pattern", "design"],
                "books": ["Architecture_Patterns.json", "Microservices.json"]
            }
        }
    }


@pytest.fixture
def sample_taxonomy_without_books():
    """Sample taxonomy without books field (Tab 3 format)."""
    return {
        "tiers": {
            "Python": {
                "priority": 1,
                "concepts": ["decorator", "generator"]
            }
        }
    }


@pytest.fixture
def sample_metadata():
    """Sample chapter metadata."""
    return [
        {
            "chapter_number": 1,
            "title": "Introduction",
            "start_page": 1,
            "end_page": 20,
            "summary": "Introduction to patterns",
            "keywords": ["pattern", "design"],
            "concepts": ["architecture", "principles"]
        },
        {
            "chapter_number": 2,
            "title": "Repository Pattern",
            "start_page": 21,
            "end_page": 50,
            "summary": "Data access abstraction",
            "keywords": ["repository", "database"],
            "concepts": ["data access", "abstraction"]
        }
    ]


# ============================================================================
# TEST CLASS: load_cross_book_context (CC 9)
# ============================================================================

class TestLoadCrossBookContext:
    """
    Test load_cross_book_context function.
    
    This function loads metadata for all books with complex logic:
    - Extracts books from taxonomy (if present)
    - Falls back to scanning metadata directory
    - Loads metadata files for each book
    - Calculates corpus size
    
    Complexity: CC 9 (multiple conditional branches, loops, error handling)
    Pattern: Repository Pattern for data access
    """
    
    def test_load_with_taxonomy_containing_books(self, tmp_path, sample_taxonomy_with_books, sample_metadata):
        """Test loading when taxonomy contains books field."""
        # Arrange
        tax_path = tmp_path / "taxonomy.json"
        meta_dir = tmp_path / "metadata"
        meta_dir.mkdir()
        
        with open(tax_path, 'w') as f:
            json.dump(sample_taxonomy_with_books, f)
        
        with open(meta_dir / "Architecture_Patterns_metadata.json", 'w') as f:
            json.dump(sample_metadata, f)
        
        # Act
        result = load_cross_book_context(tax_path, meta_dir)
        
        # Assert
        assert "books" in result
        assert "metadata" in result
        assert "corpus_size" in result
        assert "Architecture_Patterns" in result["books"]
        assert result["corpus_size"] == 2
    
    def test_load_with_taxonomy_without_books_scans_directory(self, tmp_path, sample_taxonomy_without_books, sample_metadata):
        """Test fallback to scanning metadata directory when taxonomy has no books."""
        # Arrange
        tax_path = tmp_path / "taxonomy.json"
        meta_dir = tmp_path / "metadata"
        meta_dir.mkdir()
        
        with open(tax_path, 'w') as f:
            json.dump(sample_taxonomy_without_books, f)
        
        # Create metadata files
        with open(meta_dir / "Python_Distilled_metadata.json", 'w') as f:
            json.dump(sample_metadata, f)
        
        with open(meta_dir / "Fluent_Python_metadata.json", 'w') as f:
            json.dump(sample_metadata[:1], f)
        
        # Act
        result = load_cross_book_context(tax_path, meta_dir)
        
        # Assert - should find books by scanning
        assert len(result["books"]) == 2
        assert "Python_Distilled" in result["books"]
        assert "Fluent_Python" in result["books"]
        assert result["corpus_size"] == 3  # 2 + 1 chapters
    
    def test_load_raises_error_for_missing_taxonomy(self, tmp_path):
        """Test FileNotFoundError when taxonomy doesn't exist."""
        # Arrange
        tax_path = tmp_path / "nonexistent.json"
        meta_dir = tmp_path / "metadata"
        
        # Act & Assert
        with pytest.raises(FileNotFoundError, match="Taxonomy file not found"):
            load_cross_book_context(tax_path, meta_dir)
    
    def test_load_handles_missing_metadata_files_gracefully(self, tmp_path, sample_taxonomy_with_books, capsys):
        """Test graceful handling when metadata files don't exist."""
        # Arrange
        tax_path = tmp_path / "taxonomy.json"
        meta_dir = tmp_path / "metadata"
        meta_dir.mkdir()
        
        with open(tax_path, 'w') as f:
            json.dump(sample_taxonomy_with_books, f)
        
        # Don't create metadata files - they're missing
        
        # Act
        result = load_cross_book_context(tax_path, meta_dir)
        
        # Assert - should handle missing files
        assert len(result["metadata"]) == 0
        assert result["corpus_size"] == 0
        
        # Check warning printed
        captured = capsys.readouterr()
        assert "Skipping" in captured.out or "metadata not found" in captured.out or result["corpus_size"] == 0
    
    def test_load_cleans_book_names_correctly(self, tmp_path, sample_metadata):
        """Test book name cleaning from various formats."""
        # Arrange
        taxonomy = {
            "tiers": {
                "Test": {
                    "books": [
                        "Book_Name.json",
                        "Another_Book_metadata.json",
                        "Third_Book_metadata"
                    ]
                }
            }
        }
        
        tax_path = tmp_path / "taxonomy.json"
        meta_dir = tmp_path / "metadata"
        meta_dir.mkdir()
        
        with open(tax_path, 'w') as f:
            json.dump(taxonomy, f)
        
        # Create metadata with cleaned names
        for name in ["Book_Name", "Another_Book", "Third_Book"]:
            with open(meta_dir / f"{name}_metadata.json", 'w') as f:
                json.dump(sample_metadata, f)
        
        # Act
        result = load_cross_book_context(tax_path, meta_dir)
        
        # Assert - names should be cleaned
        assert "Book_Name" in result["books"]
        assert "Another_Book" in result["books"]
        assert "Third_Book" in result["books"]
    
    def test_load_empty_taxonomy_scans_directory(self, tmp_path, sample_metadata):
        """Test handling of empty taxonomy."""
        # Arrange
        taxonomy = {"tiers": {}}
        tax_path = tmp_path / "taxonomy.json"
        meta_dir = tmp_path / "metadata"
        meta_dir.mkdir()
        
        with open(tax_path, 'w') as f:
            json.dump(taxonomy, f)
        
        with open(meta_dir / "Some_Book_metadata.json", 'w') as f:
            json.dump(sample_metadata, f)
        
        # Act
        result = load_cross_book_context(tax_path, meta_dir)
        
        # Assert - should scan and find book
        assert "Some_Book" in result["books"]


# ============================================================================
# TEST CLASS: build_chapter_corpus (CC 4)
# ============================================================================

class TestBuildChapterCorpus:
    """Test build_chapter_corpus function (corpus construction for TF-IDF)."""
    
    def test_build_corpus_from_context(self, sample_metadata):
        """Test corpus building from cross-book context."""
        # Arrange
        context = {
            "books": ["Test_Book"],
            "metadata": {
                "Test_Book": sample_metadata
            },
            "corpus_size": 2
        }
        
        # Act
        corpus, index = build_chapter_corpus(context)
        
        # Assert
        assert len(corpus) == 2
        assert len(index) == 2
        assert isinstance(corpus[0], str)
        assert index[0]["book"] == "Test_Book"
        assert index[0]["chapter"] == 1
    
    def test_corpus_combines_all_text_features(self, sample_metadata):
        """Test corpus combines title, summary, keywords, concepts."""
        # Arrange
        context = {
            "books": ["Book"],
            "metadata": {"Book": [sample_metadata[0]]},
            "corpus_size": 1
        }
        
        # Act
        corpus, _ = build_chapter_corpus(context)
        
        # Assert - should contain all text features
        text = corpus[0]
        assert "Introduction" in text  # title
        assert "patterns" in text  # summary
        assert "pattern" in text  # keywords
        assert "architecture" in text  # concepts
    
    def test_corpus_handles_missing_fields(self):
        """Test corpus building with missing optional fields."""
        # Arrange
        minimal_chapter = {
            "chapter_number": 1,
            "start_page": 1,
            "end_page": 10
            # Missing: title, summary, keywords, concepts
        }
        context = {
            "books": ["Minimal"],
            "metadata": {"Minimal": [minimal_chapter]},
            "corpus_size": 1
        }
        
        # Act
        corpus, index = build_chapter_corpus(context)
        
        # Assert - should handle missing fields
        assert len(corpus) == 1
        assert len(index) == 1
        assert index[0]["title"] == ""
    
    def test_corpus_with_multiple_books(self, sample_metadata):
        """Test corpus building across multiple books."""
        # Arrange
        context = {
            "books": ["Book1", "Book2"],
            "metadata": {
                "Book1": [sample_metadata[0]],
                "Book2": [sample_metadata[1]]
            },
            "corpus_size": 2
        }
        
        # Act
        corpus, index = build_chapter_corpus(context)
        
        # Assert
        assert len(corpus) == 2
        assert len(index) == 2
        assert index[0]["book"] == "Book1"
        assert index[1]["book"] == "Book2"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
