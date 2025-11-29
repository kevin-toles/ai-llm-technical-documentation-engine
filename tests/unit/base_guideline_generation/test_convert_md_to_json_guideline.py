"""
Unit tests for convert_md_to_json_guideline.py

Tests focus on functions with CC 8-9:
- parse_markdown_chapter (CC 8) - Markdown parsing strategy
- convert_markdown_to_json (CC 8) - Service layer for conversion
- main (CC 9) - Orchestration and file I/O

Architecture Patterns Applied:
- Service Layer Pattern: Test conversion business logic (Architecture Patterns Ch. 4)
- Strategy Pattern: Test markdown parsing strategy
- Domain-Agnostic Implementation: Regex-based text processing

Sprint: Batch #2 Files 6-11 (HIGH priority, CC 8-9, tests only)
"""

import pytest
import json
import sys
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, mock_open
from typing import Dict, List, Any

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from workflows.base_guideline_generation.scripts.convert_md_to_json_guideline import (
    parse_markdown_chapter,
    convert_markdown_to_json
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def sample_markdown_chapter():
    """Sample markdown chapter text."""
    return """
## Chapter 5: Decorators and Closures
*Source: Fluent Python 2nd, pages 100-125*

### Chapter Summary
This chapter explores decorators and closures in Python, demonstrating how decorators
modify function behavior and how closures capture variables from enclosing scopes.

### Concept-by-Concept Breakdown

#### **Function Decorators** *(p.102)*
Decorators wrap functions to modify behavior without changing the function itself.

#### **Closure Scope** *(p.115)*
Closures allow functions to access variables from enclosing scopes even after those scopes have exited.

#### **@property Decorator** *(p.120)*
The @property decorator transforms methods into read-only attributes.
"""


@pytest.fixture
def sample_full_markdown():
    """Sample complete markdown file."""
    return """# Comprehensive Guidelines — Fluent Python 2nd
*Source: Fluent Python 2nd Edition*

## Chapter 1: The Python Data Model
*Source: Fluent Python 2nd, pages 1-25*

### Chapter Summary
Introduction to Python's data model and special methods.

### Concept-by-Concept Breakdown

#### **Special Methods** *(p.5)*
Special methods like __repr__ and __str__ customize object behavior.

## Chapter 2: An Array of Sequences
*Source: Fluent Python 2nd, pages 26-60*

### Chapter Summary
Explores Python's sequence types including lists, tuples, and arrays.

### Concept-by-Concept Breakdown

#### **List Comprehensions** *(p.30)*
List comprehensions provide concise syntax for creating lists.
"""


@pytest.fixture
def temp_output_dir(tmp_path):
    """Create temporary output directory."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir


# ============================================================================
# TEST parse_markdown_chapter (CC 8)
# ============================================================================

class TestParseMarkdownChapter:
    """
    Test suite for parse_markdown_chapter function.
    
    This function implements Strategy pattern for markdown parsing:
    - Extracts chapter number and title using regex
    - Parses page ranges
    - Extracts chapter summary
    - Extracts concepts with page numbers
    - Handles missing optional sections
    
    Complexity: CC 8 (multiple regex matches, conditional extraction)
    Pattern: Strategy Pattern (parsing strategy)
    """
    
    def test_parse_valid_chapter(self, sample_markdown_chapter):
        """Test parsing complete chapter with all sections."""
        result = parse_markdown_chapter(sample_markdown_chapter)
        
        assert result is not None
        assert result["chapter_number"] == 5
        assert result["title"] == "Decorators and Closures"
        assert result["page_range"]["start"] == 100
        assert result["page_range"]["end"] == 125
        assert len(result["chapter_summary"]) > 0
        assert len(result["concepts"]) == 3
    
    def test_parse_extracts_chapter_number_and_title(self, sample_markdown_chapter):
        """Test extraction of chapter number and title."""
        result = parse_markdown_chapter(sample_markdown_chapter)
        
        assert result["chapter_number"] == 5
        assert result["title"] == "Decorators and Closures"
    
    def test_parse_extracts_page_range(self, sample_markdown_chapter):
        """Test extraction of page range."""
        result = parse_markdown_chapter(sample_markdown_chapter)
        
        assert result["page_range"] is not None
        assert result["page_range"]["start"] == 100
        assert result["page_range"]["end"] == 125
    
    def test_parse_extracts_chapter_summary(self, sample_markdown_chapter):
        """Test extraction of chapter summary section."""
        result = parse_markdown_chapter(sample_markdown_chapter)
        
        assert "chapter_summary" in result
        assert "decorators and closures" in result["chapter_summary"].lower()
    
    def test_parse_extracts_concepts_with_page_numbers(self, sample_markdown_chapter):
        """Test extraction of concepts from breakdown section."""
        result = parse_markdown_chapter(sample_markdown_chapter)
        
        assert len(result["concepts"]) == 3
        
        concept_names = [c["name"] for c in result["concepts"]]
        assert "Function Decorators" in concept_names
        assert "Closure Scope" in concept_names
        assert "@property Decorator" in concept_names
        
        # Check page numbers
        for concept in result["concepts"]:
            assert "page" in concept
            assert concept["page"] in [102, 115, 120]
    
    def test_parse_chapter_without_header(self):
        """Test parsing text without chapter header."""
        text = "Random text without chapter header"
        
        result = parse_markdown_chapter(text)
        
        assert result is None
    
    def test_parse_chapter_without_page_range(self):
        """Test parsing chapter without page range."""
        text = """
## Chapter 3: Test Chapter
*Source: Test Book*

### Chapter Summary
Summary without page range.
"""
        result = parse_markdown_chapter(text)
        
        assert result is not None
        assert result["chapter_number"] == 3
        assert result["page_range"] is None
    
    def test_parse_chapter_without_summary(self):
        """Test parsing chapter without summary section."""
        text = """
## Chapter 7: Test Chapter
*Source: Test Book, pages 50-75*

### Concept-by-Concept Breakdown

#### **Test Concept** *(p.55)*
Concept description.
"""
        result = parse_markdown_chapter(text)
        
        assert result is not None
        assert result["chapter_summary"] == ""
    
    def test_parse_chapter_without_concepts(self):
        """Test parsing chapter without concept breakdown."""
        text = """
## Chapter 9: Test Chapter
*Source: Test Book, pages 100-125*

### Chapter Summary
Chapter summary here.
"""
        result = parse_markdown_chapter(text)
        
        assert result is not None
        assert len(result["concepts"]) == 0
    
    def test_parse_filters_invalid_concept_names(self):
        """Test that invalid concept names are filtered out."""
        text = """
## Chapter 4: Test Chapter
*Source: Test Book, pages 20-40*

### Concept-by-Concept Breakdown

#### **none** *(p.25)*
Invalid concept name.

#### **Valid Concept** *(p.30)*
Valid concept.

#### **as** *(p.35)*
Another invalid concept.
"""
        result = parse_markdown_chapter(text)
        
        assert result is not None
        # Should filter out 'none' and 'as'
        concept_names = [c["name"] for c in result["concepts"]]
        assert "none" not in concept_names
        assert "as" not in concept_names
        assert "Valid Concept" in concept_names
    
    def test_parse_handles_multiline_summary(self):
        """Test parsing summary that spans multiple lines."""
        text = """
## Chapter 2: Test Chapter
*Source: Test Book, pages 10-30*

### Chapter Summary
This is a multiline summary that
spans several lines and includes
various details about the chapter.

### Concept-by-Concept Breakdown
"""
        result = parse_markdown_chapter(text)
        
        assert result is not None
        assert len(result["chapter_summary"]) > 0
        assert "multiline" in result["chapter_summary"].lower()


# ============================================================================
# TEST convert_markdown_to_json (CC 8)
# ============================================================================

class TestConvertMarkdownToJson:
    """
    Test suite for convert_markdown_to_json function.
    
    This function implements Service Layer pattern for conversion:
    - Reads markdown file
    - Extracts book metadata
    - Splits into chapter sections
    - Parses each chapter
    - Builds JSON structure
    - Writes output file
    
    Complexity: CC 8 (file I/O, metadata extraction, chapter iteration)
    Pattern: Service Layer Pattern
    """
    
    def test_convert_creates_json_file(
        self, sample_full_markdown, temp_output_dir, tmp_path
    ):
        """Test that conversion creates output JSON file."""
        md_file = tmp_path / "Chapter_Summaries_Fluent Python Ed6.md"
        md_file.write_text(sample_full_markdown)
        
        result_path = convert_markdown_to_json(md_file, temp_output_dir)
        
        assert result_path.exists()
        assert result_path.suffix == ".json"
    
    def test_convert_extracts_book_name_from_filename(
        self, sample_full_markdown, temp_output_dir, tmp_path
    ):
        """Test extraction of book name from filename."""
        md_file = tmp_path / "Chapter_Summaries_Learning Python Ed6.md"
        md_file.write_text(sample_full_markdown)
        
        result_path = convert_markdown_to_json(md_file, temp_output_dir)
        
        with open(result_path, 'r') as f:
            data = json.load(f)
        
        assert "book_metadata" in data
        assert "Learning Python Ed6" in data["book_metadata"]["book_name"]
    
    def test_convert_includes_source_info(
        self, sample_full_markdown, temp_output_dir, tmp_path
    ):
        """Test that output includes source_info metadata."""
        md_file = tmp_path / "test_file.md"
        md_file.write_text(sample_full_markdown)
        
        result_path = convert_markdown_to_json(md_file, temp_output_dir)
        
        with open(result_path, 'r') as f:
            data = json.load(f)
        
        assert "source_info" in data
        assert data["source_info"]["generated_by"] == "convert_md_to_json_guideline.py"
        assert data["source_info"]["llm_enabled"] is False
        assert "generation_date" in data["source_info"]
    
    def test_convert_parses_multiple_chapters(
        self, sample_full_markdown, temp_output_dir, tmp_path
    ):
        """Test parsing file with multiple chapters."""
        md_file = tmp_path / "test.md"
        md_file.write_text(sample_full_markdown)
        
        result_path = convert_markdown_to_json(md_file, temp_output_dir)
        
        with open(result_path, 'r') as f:
            data = json.load(f)
        
        assert "chapters" in data
        assert len(data["chapters"]) == 2  # Two chapters in sample
        assert data["chapters"][0]["chapter_number"] == 1
        assert data["chapters"][1]["chapter_number"] == 2
    
    def test_convert_preserves_chapter_structure(
        self, sample_full_markdown, temp_output_dir, tmp_path
    ):
        """Test that chapter structure is preserved in JSON."""
        md_file = tmp_path / "test.md"
        md_file.write_text(sample_full_markdown)
        
        result_path = convert_markdown_to_json(md_file, temp_output_dir)
        
        with open(result_path, 'r') as f:
            data = json.load(f)
        
        chapter = data["chapters"][0]
        assert "chapter_number" in chapter
        assert "title" in chapter
        assert "page_range" in chapter
        assert "chapter_summary" in chapter
        assert "concepts" in chapter
    
    def test_convert_extracts_title_from_first_line(
        self, temp_output_dir, tmp_path
    ):
        """Test extraction of title from first # heading."""
        markdown = """# Custom Title — Test Book
## Chapter 1: Test
*Source: Test Book, pages 1-10*

### Chapter Summary
Summary text.
"""
        md_file = tmp_path / "test.md"
        md_file.write_text(markdown)
        
        result_path = convert_markdown_to_json(md_file, temp_output_dir)
        
        with open(result_path, 'r') as f:
            data = json.load(f)
        
        assert "Custom Title" in data["book_metadata"]["title"]
    
    def test_convert_uses_default_title_if_missing(
        self, temp_output_dir, tmp_path
    ):
        """Test default title when first line has no # heading."""
        markdown = """## Chapter 1: Test
*Source: Test Book, pages 1-10*

### Chapter Summary
Summary text.
"""
        md_file = tmp_path / "Test_Book.md"
        md_file.write_text(markdown)
        
        result_path = convert_markdown_to_json(md_file, temp_output_dir)
        
        with open(result_path, 'r') as f:
            data = json.load(f)
        
        # Should use filename-based default
        assert "Comprehensive Guidelines" in data["book_metadata"]["title"]
    
    def test_convert_includes_empty_footnotes(
        self, sample_full_markdown, temp_output_dir, tmp_path
    ):
        """Test that output includes empty footnotes array."""
        md_file = tmp_path / "test.md"
        md_file.write_text(sample_full_markdown)
        
        result_path = convert_markdown_to_json(md_file, temp_output_dir)
        
        with open(result_path, 'r') as f:
            data = json.load(f)
        
        assert "footnotes" in data
        assert isinstance(data["footnotes"], list)
    
    def test_convert_handles_filename_without_prefix(
        self, sample_full_markdown, temp_output_dir, tmp_path
    ):
        """Test filename handling when 'Chapter_Summaries_' prefix missing."""
        md_file = tmp_path / "Simple_Filename.md"
        md_file.write_text(sample_full_markdown)
        
        result_path = convert_markdown_to_json(md_file, temp_output_dir)
        
        with open(result_path, 'r') as f:
            data = json.load(f)
        
        # Should use filename as book name
        assert data["book_metadata"]["book_name"] == "Simple_Filename"


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestConversionIntegration:
    """Integration tests for markdown to JSON conversion."""
    
    def test_full_conversion_pipeline(
        self, sample_full_markdown, temp_output_dir, tmp_path
    ):
        """Test complete conversion pipeline."""
        md_file = tmp_path / "Chapter_Summaries_Test_Book.md"
        md_file.write_text(sample_full_markdown)
        
        result_path = convert_markdown_to_json(md_file, temp_output_dir)
        
        # Verify file created
        assert result_path.exists()
        
        # Verify JSON is valid
        with open(result_path, 'r') as f:
            data = json.load(f)
        
        # Verify structure
        assert "book_metadata" in data
        assert "source_info" in data
        assert "chapters" in data
        assert "footnotes" in data
        
        # Verify chapters parsed
        assert len(data["chapters"]) > 0
        
        # Verify concepts extracted
        if data["chapters"][0]["concepts"]:
            concept = data["chapters"][0]["concepts"][0]
            assert "name" in concept
            assert "page" in concept
    
    def test_conversion_with_real_chapter_structure(
        self, temp_output_dir, tmp_path
    ):
        """Test conversion with realistic chapter structure."""
        markdown = """# Comprehensive Guidelines — Fluent Python 2nd
*Source: Fluent Python 2nd Edition*

## Chapter 5: Decorators and Closures
*Source: Fluent Python 2nd, pages 100-125*

### Chapter Summary
This chapter explores decorators and closures in Python.

### Concept-by-Concept Breakdown

#### **Function Decorators** *(p.102)*
Decorators modify function behavior.

#### **Closure Variables** *(p.115)*
Closures capture variables from enclosing scopes.

## Chapter 6: Design Patterns
*Source: Fluent Python 2nd, pages 126-150*

### Chapter Summary
Introduction to design patterns in Python.

### Concept-by-Concept Breakdown

#### **Strategy Pattern** *(p.130)*
Strategy pattern encapsulates algorithms.
"""
        md_file = tmp_path / "Chapter_Summaries_Fluent_Python_2nd.md"
        md_file.write_text(markdown)
        
        result_path = convert_markdown_to_json(md_file, temp_output_dir)
        
        with open(result_path, 'r') as f:
            data = json.load(f)
        
        # Verify 2 chapters parsed
        assert len(data["chapters"]) == 2
        
        # Verify first chapter
        assert data["chapters"][0]["chapter_number"] == 5
        assert data["chapters"][0]["title"] == "Decorators and Closures"
        assert len(data["chapters"][0]["concepts"]) == 2
        
        # Verify second chapter
        assert data["chapters"][1]["chapter_number"] == 6
        assert data["chapters"][1]["title"] == "Design Patterns"
        assert len(data["chapters"][1]["concepts"]) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
