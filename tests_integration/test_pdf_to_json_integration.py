#!/usr/bin/env python3
"""
Integration test for PDF to JSON converter with ChapterSegmenter.

Tests the full workflow:
1. PDF extraction (mocked)
2. Chapter segmentation using 3-pass algorithm
3. JSON output generation

Reference: Python Testing with pytest Ch. 4 - Fixtures
Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md - Integration testing strategy
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from workflows.pdf_to_json.scripts.convert_pdf_to_json import convert_pdf_to_json


class TestPDFToJSONIntegration:
    """Integration tests for end-to-end PDF to JSON conversion."""
    
    def test_full_conversion_with_chapter_segmentation(self, tmp_path):
        """Test complete PDF to JSON workflow with ChapterSegmenter."""
        
        # Create mock PDF document
        mock_doc = Mock()
        mock_doc.__len__ = Mock(return_value=15)
        mock_doc.metadata = {'author': 'Test Author', 'title': 'Test Book'}
        
        # Create 15 mock pages with realistic content
        mock_pages = []
        for i in range(15):
            page = Mock()
            
            # Pages 1, 6, 11 are chapter starts
            if i == 0:
                content = "Chapter 1: Introduction\n\n" + "This is the introduction chapter with content. " * 50
            elif i == 5:
                content = "Chapter 2: Main Topics\n\n" + "This chapter covers main topics and examples. " * 50
            elif i == 10:
                content = "Chapter 3: Advanced Concepts\n\n" + "Advanced material and techniques discussed here. " * 50
            else:
                content = f"Regular content for page {i+1}. " * 100
            
            page.get_text = Mock(return_value=content)
            mock_pages.append(page)
        
        mock_doc.__iter__ = Mock(return_value=iter(mock_pages))
        mock_doc.__getitem__ = Mock(side_effect=lambda idx: mock_pages[idx])
        mock_doc.close = Mock()
        
        # Create temp output file
        output_path = tmp_path / "test_output.json"
        
        # Mock fitz.open to return our mock document
        with patch('workflows.pdf_to_json.scripts.convert_pdf_to_json.fitz.open', return_value=mock_doc):
            # Run conversion (use a fake PDF path since we're mocking fitz.open)
            with patch('pathlib.Path.exists', return_value=True):
                result = convert_pdf_to_json("fake.pdf", str(output_path))
        
        # Verify conversion succeeded
        assert result is True
        assert output_path.exists()
        
        # Load and verify JSON structure
        with open(output_path) as f:
            data = json.load(f)
        
        # Verify top-level structure
        assert 'metadata' in data
        assert 'chapters' in data
        assert 'pages' in data
        
        # Verify metadata
        assert data['metadata']['author'] == 'Test Author'
        assert data['metadata']['title'] == 'Test Book'
        assert data['metadata']['total_pages'] == 15
        
        # Verify pages
        assert len(data['pages']) == 15
        for i, page in enumerate(data['pages']):
            assert page['page_number'] == i + 1
            assert 'content' in page
            assert page['extraction_method'] == 'Direct'
        
        # Verify chapters were detected
        assert len(data['chapters']) >= 3  # Should detect at least 3 chapters
        
        # Verify chapter structure
        for ch in data['chapters']:
            assert 'number' in ch
            assert 'title' in ch
            assert 'start_page' in ch
            assert 'end_page' in ch
            assert 'detection_method' in ch
            
            # Verify chapter spans valid page range
            assert ch['start_page'] >= 1
            assert ch['end_page'] <= 15
            assert ch['start_page'] <= ch['end_page']
        
        # Verify chapters don't overlap
        for i in range(len(data['chapters']) - 1):
            ch1 = data['chapters'][i]
            ch2 = data['chapters'][i + 1]
            assert ch1['end_page'] < ch2['start_page'], "Chapters should not overlap"
    
    def test_empty_pdf_handled(self, tmp_path):
        """Test that empty PDFs are handled gracefully."""
        
        mock_doc = Mock()
        mock_doc.__len__ = Mock(return_value=0)
        mock_doc.metadata = {}
        mock_doc.__iter__ = Mock(return_value=iter([]))
        mock_doc.close = Mock()
        
        output_path = tmp_path / "empty_output.json"
        
        with patch('workflows.pdf_to_json.scripts.convert_pdf_to_json.fitz.open', return_value=mock_doc):
            with patch('pathlib.Path.exists', return_value=True):
                result = convert_pdf_to_json("fake.pdf", str(output_path))
        
        assert result is True
        
        with open(output_path) as f:
            data = json.load(f)
        
        # Empty PDF (0 pages) should have 0 chapters - nothing to segment
        assert len(data['chapters']) == 0
        assert len(data['pages']) == 0
    
    def test_single_page_pdf(self, tmp_path):
        """Test that single-page PDFs are handled correctly."""
        
        mock_doc = Mock()
        mock_doc.__len__ = Mock(return_value=1)
        mock_doc.metadata = {}
        
        page = Mock()
        page.get_text = Mock(return_value="Single page content with some text. " * 50)
        
        mock_doc.__iter__ = Mock(return_value=iter([page]))
        mock_doc.__getitem__ = Mock(return_value=page)
        mock_doc.close = Mock()
        
        output_path = tmp_path / "single_page.json"
        
        with patch('workflows.pdf_to_json.scripts.convert_pdf_to_json.fitz.open', return_value=mock_doc):
            with patch('pathlib.Path.exists', return_value=True):
                result = convert_pdf_to_json("fake.pdf", str(output_path))
        
        assert result is True
        
        with open(output_path) as f:
            data = json.load(f)
        
        assert len(data['pages']) == 1
        # Single-page book should have exactly 1 chapter
        assert len(data['chapters']) == 1
        assert data['chapters'][0]['start_page'] == 1
        assert data['chapters'][0]['end_page'] == 1
    
    def test_chapter_detection_methods_present(self, tmp_path):
        """Verify that detection_method field is populated correctly."""
        
        mock_doc = Mock()
        mock_doc.__len__ = Mock(return_value=10)
        mock_doc.metadata = {}
        
        # Create pages with clear chapter markers
        mock_pages = []
        for i in range(10):
            page = Mock()
            if i == 0:
                content = "Chapter 1: First Chapter\n\n" + "Introduction content here. " * 50
            elif i == 5:
                content = "Chapter 2: Second Chapter\n\n" + "More content in second chapter. " * 50
            else:
                content = f"Content for page {i+1}. " * 100
            
            page.get_text = Mock(return_value=content)
            mock_pages.append(page)
        
        mock_doc.__iter__ = Mock(return_value=iter(mock_pages))
        mock_doc.__getitem__ = Mock(side_effect=lambda idx: mock_pages[idx])
        mock_doc.close = Mock()
        
        output_path = tmp_path / "method_test.json"
        
        with patch('workflows.pdf_to_json.scripts.convert_pdf_to_json.fitz.open', return_value=mock_doc):
            with patch('pathlib.Path.exists', return_value=True):
                result = convert_pdf_to_json("fake.pdf", str(output_path))
        
        assert result is True
        
        with open(output_path) as f:
            data = json.load(f)
        
        # Verify detection_method is one of the valid methods
        valid_methods = {'regex_chapter', 'regex_item', 'regex_numeric', 'topic_boundary', 'synthetic'}
        
        for ch in data['chapters']:
            assert ch['detection_method'] in valid_methods, \
                f"Invalid detection_method: {ch['detection_method']}"
        
        # With clear "Chapter N:" markers, should use regex_chapter
        assert any(ch['detection_method'] == 'regex_chapter' for ch in data['chapters']), \
            "Should detect at least one chapter using regex_chapter method"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
