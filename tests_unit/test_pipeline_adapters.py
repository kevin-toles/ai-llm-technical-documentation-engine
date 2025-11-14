"""
Unit tests for pipeline adapters (Sprint 4 - Phase 1)

TDD Cycle: RED → GREEN → REFACTOR
Pattern: Adapter Pattern (Architecture Patterns with Python Ch. 13)

Tests for:
- PdfConverterAdapter: Wraps legacy convert_pdf_to_json function
- ChapterGeneratorAdapter: Wraps legacy chapter_generator_all_text
- MetadataExtractorAdapter: Wraps legacy generate_chapter_metadata
"""

import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Import will fail initially (RED phase) - that's expected
try:
    from src.pipeline.adapters.pdf_converter import PdfConverterAdapter, PdfConversionError
except ImportError:
    # Expected during RED phase
    PdfConverterAdapter = None
    PdfConversionError = None


class TestPdfConverterAdapter:
    """Tests for PdfConverterAdapter (wraps convert_pdf_to_json)"""
    
    @pytest.fixture
    def adapter(self):
        """Create adapter instance for testing"""
        if PdfConverterAdapter is None:
            pytest.skip("PdfConverterAdapter not implemented yet (RED phase)")
        return PdfConverterAdapter()
    
    def test_convert_success(self, adapter, tmp_path):
        """
        RED: Test successful PDF conversion
        
        Validates:
        - Adapter calls legacy convert_pdf_to_json function
        - Uses config-based output path (not hardcoded)
        - Returns parsed JSON data
        """
        # Arrange
        pdf_path = tmp_path / "test_book.pdf"
        pdf_path.write_text("fake pdf content")
        
        expected_json = {
            "metadata": {"title": "Test Book"},
            "pages": [{"page_number": 1, "content": "Test content"}]
        }
        
        # Mock settings paths
        with patch('src.pipeline.adapters.pdf_converter.settings') as mock_settings:
            mock_settings.paths.textbooks_json_dir = tmp_path / "json_output"
            mock_settings.paths.textbooks_json_dir.mkdir(parents=True, exist_ok=True)
            
            # Mock the legacy function where it's imported and used (inside convert method)
            with patch('src.pipeline.convert_pdf_to_json.convert_pdf_to_json') as mock_convert:
                mock_convert.return_value = True
                
                # Create the expected JSON file that the adapter will read
                json_file = mock_settings.paths.textbooks_json_dir / "test_book.json"
                json_file.write_text(json.dumps(expected_json))
                
                # Act
                result = adapter.convert(pdf_path)
        
        # Assert
        assert result == expected_json
        mock_convert.assert_called_once()
        
        # Verify it used config path (not hardcoded)
        call_args = mock_convert.call_args
        output_path = Path(call_args[0][1])
        assert "json_output" in str(output_path)
    
    def test_convert_failure_raises_exception(self, adapter, tmp_path):
        """
        RED: Test conversion failure raises PdfConversionError
        
        Validates:
        - Legacy function returning False triggers exception
        - Exception message includes PDF path
        """
        # Arrange
        pdf_path = tmp_path / "bad_book.pdf"
        pdf_path.write_text("corrupted pdf")
        
        with patch('src.pipeline.convert_pdf_to_json.convert_pdf_to_json') as mock_convert:
            mock_convert.return_value = False
            
            # Act & Assert
            if PdfConversionError is None:
                pytest.skip("PdfConversionError not implemented yet")
            
            with pytest.raises(PdfConversionError) as exc_info:
                adapter.convert(pdf_path)
            
            assert "bad_book.pdf" in str(exc_info.value)
    
    def test_convert_logs_progress(self, tmp_path, caplog):
        """
        RED: Test adapter logs conversion progress
        
        Validates:
        - Logs "Converting PDF: <path>" at start
        - Logs "Conversion complete: <output>" at end
        """
        # Arrange - create adapter with explicit logging level
        import logging
        adapter = PdfConverterAdapter()
        
        # Set logging level to capture INFO messages
        with caplog.at_level(logging.INFO):
            pdf_path = tmp_path / "logged_book.pdf"
            pdf_path.write_text("pdf content")
            
            expected_json = {"metadata": {"title": "Logged"}}
            
            with patch('src.pipeline.convert_pdf_to_json.convert_pdf_to_json', return_value=True):
                with patch.object(Path, 'read_text', return_value=json.dumps(expected_json)):
                    with patch('src.pipeline.adapters.pdf_converter.settings') as mock_settings:
                        mock_settings.paths.textbooks_json_dir = tmp_path / "json_output"
                        mock_settings.paths.textbooks_json_dir.mkdir(parents=True, exist_ok=True)
                        
                        # Act
                        adapter.convert(pdf_path)
        
        # Assert
        assert "Converting PDF" in caplog.text
        assert "logged_book.pdf" in caplog.text
        assert "Conversion complete" in caplog.text
    
    def test_convert_uses_pathlib_not_strings(self, adapter, tmp_path):
        """
        RED: Test adapter accepts Path objects (not strings)
        
        Validates:
        - Method signature uses Path type
        - Legacy function receives string conversion
        """
        # Arrange
        pdf_path = tmp_path / "path_book.pdf"
        pdf_path.write_text("content")
        
        with patch('src.pipeline.convert_pdf_to_json.convert_pdf_to_json', return_value=True) as mock_convert:
            with patch.object(Path, 'read_text', return_value='{"test": true}'):
                with patch('src.pipeline.adapters.pdf_converter.settings') as mock_settings:
                    mock_settings.paths.textbooks_json_dir = tmp_path / "json_output"
                    mock_settings.paths.textbooks_json_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Act
                    adapter.convert(pdf_path)
        
        # Assert - legacy function should receive string, not Path
        call_args = mock_convert.call_args[0]
        assert isinstance(call_args[0], str)  # Legacy expects string
        assert isinstance(call_args[1], str)


class TestChapterGeneratorAdapter:
    """Tests for ChapterGeneratorAdapter (wraps chapter_generator_all_text)"""
    
    def test_adapter_not_implemented_yet(self):
        """Placeholder for Chapter Generator adapter tests"""
        pytest.skip("ChapterGeneratorAdapter implementation comes after PdfConverterAdapter")


class TestMetadataExtractorAdapter:
    """Tests for MetadataExtractorAdapter (wraps generate_chapter_metadata)"""
    
    def test_adapter_not_implemented_yet(self):
        """Placeholder for Metadata Extractor adapter tests"""
        pytest.skip("MetadataExtractorAdapter implementation comes after ChapterGeneratorAdapter")
