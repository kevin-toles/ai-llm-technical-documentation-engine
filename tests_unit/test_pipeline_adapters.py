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
    """Tests for ChapterGeneratorAdapter (wraps chapter_generator_all_text main function)"""
    
    @pytest.fixture
    def adapter(self):
        """Create adapter instance for testing"""
        try:
            from src.pipeline.adapters.chapter_generator import ChapterGeneratorAdapter
            return ChapterGeneratorAdapter()
        except ImportError:
            pytest.skip("ChapterGeneratorAdapter not implemented yet (RED phase)")
    
    def test_generate_success(self, adapter, tmp_path):
        """
        RED: Test successful chapter generation
        
        Validates:
        - Adapter calls legacy main() function from chapter_generator_all_text
        - Returns output file path
        - Verifies output file was created
        """
        # Arrange - create output file when main() is called
        def mock_main_side_effect():
            """Simulate legacy main() writing output file"""
            output_file = Path.cwd() / "PYTHON_GUIDELINES_Learning Python Ed6.md"
            output_file.write_text("# Generated Guidelines\n\nChapter content...")
        
        with patch('src.pipeline.chapter_generator_all_text.main', side_effect=mock_main_side_effect):
            # Act
            result = adapter.generate()
        
        # Assert
        assert isinstance(result, Path)
        assert result.exists()
        assert "PYTHON_GUIDELINES" in result.name
        assert result.read_text().startswith("# Generated Guidelines")
    
    def test_generate_failure_raises_exception(self, adapter, tmp_path):
        """
        RED: Test generation failure raises ChapterGenerationError
        
        Validates:
        - Exception raised when legacy function fails
        - Exception message is descriptive
        """
        # Arrange
        with patch('src.pipeline.chapter_generator_all_text.main') as mock_main:
            mock_main.side_effect = Exception("JSON file not found")
            
            # Act & Assert
            try:
                from src.pipeline.adapters.chapter_generator import ChapterGenerationError
            except ImportError:
                pytest.skip("ChapterGenerationError not implemented yet")
            
            with pytest.raises(ChapterGenerationError) as exc_info:
                adapter.generate()
            
            assert "Failed to generate" in str(exc_info.value)
    
    def test_generate_logs_progress(self, adapter, tmp_path, caplog):
        """
        RED: Test adapter logs generation progress
        
        Validates:
        - Logs "Generating chapters" at start
        - Logs "Generation complete" at end
        """
        # Arrange
        import logging
        
        def mock_main_side_effect():
            """Simulate legacy main() writing output file"""
            output_file = Path.cwd() / "PYTHON_GUIDELINES_Learning Python Ed6.md"
            output_file.write_text("# Generated Guidelines\n\nChapter content...")
        
        with caplog.at_level(logging.INFO):
            with patch('src.pipeline.chapter_generator_all_text.main', side_effect=mock_main_side_effect):
                # Act
                adapter.generate()
        
        # Assert
        assert "Generating chapters" in caplog.text
        assert "Generation complete" in caplog.text
    
    def test_generate_returns_path_not_string(self, adapter, tmp_path):
        """
        RED: Test adapter returns Path object (not string)
        
        Validates:
        - Return type is pathlib.Path
        - Type hints are properly enforced
        """
        # Arrange
        def mock_main_side_effect():
            """Simulate legacy main() writing output file"""
            output_file = Path.cwd() / "PYTHON_GUIDELINES_Learning Python Ed6.md"
            output_file.write_text("# Generated Guidelines")
        
        with patch('src.pipeline.chapter_generator_all_text.main', side_effect=mock_main_side_effect):
            # Act
            result = adapter.generate()
        
        # Assert
        assert isinstance(result, Path)
        assert not isinstance(result, str)


class TestMetadataExtractorAdapter:
    """Tests for MetadataExtractorAdapter (wraps generate_chapter_metadata)"""
    
    @pytest.fixture
    def adapter(self):
        """Create adapter instance for testing"""
        try:
            from src.pipeline.adapters.metadata_extractor import MetadataExtractorAdapter
            return MetadataExtractorAdapter()
        except ImportError:
            pytest.skip("MetadataExtractorAdapter not implemented yet (RED phase)")
    
    def test_extract_success(self, adapter, tmp_path):
        """
        RED: Test successful metadata extraction
        
        Validates:
        - Adapter calls legacy main() function from generate_chapter_metadata
        - Returns cache file path
        - Verifies cache was updated
        """
        # Arrange - mock main() to simulate cache update
        def mock_main_side_effect():
            """Simulate legacy main() updating cache file"""
            # Legacy function expects cache in script directory
            cache_file = Path(__file__).parent.parent / "src" / "pipeline" / "chapter_metadata_cache.json"
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            cache_file.write_text(json.dumps({
                "Test Book": [
                    {"title": "Chapter 1", "summary": "Updated summary", "keywords": ["test"], "concepts": ["testing"]}
                ]
            }))
        
        with patch('src.pipeline.generate_chapter_metadata.main', side_effect=mock_main_side_effect):
            # Act
            result = adapter.extract()
        
        # Assert
        assert isinstance(result, Path)
        assert result.exists()
        assert "chapter_metadata_cache.json" in result.name
    
    def test_extract_failure_raises_exception(self, adapter):
        """
        RED: Test extraction failure raises MetadataExtractionError
        
        Validates:
        - Exception raised when legacy function fails
        - Exception message is descriptive
        """
        # Arrange
        with patch('src.pipeline.generate_chapter_metadata.main', side_effect=Exception("Cache file not found")):
            # Act & Assert
            try:
                from src.pipeline.adapters.metadata_extractor import MetadataExtractionError
            except ImportError:
                pytest.skip("MetadataExtractionError not implemented yet")
            
            with pytest.raises(MetadataExtractionError) as exc_info:
                adapter.extract()
            
            assert "Failed to extract" in str(exc_info.value)
    
    def test_extract_logs_progress(self, adapter, tmp_path, caplog):
        """
        RED: Test adapter logs extraction progress
        
        Validates:
        - Logs "Extracting chapter metadata" at start
        - Logs "Extraction complete" at end
        """
        # Arrange
        import logging
        
        def mock_main_side_effect():
            cache_file = Path(__file__).parent.parent / "src" / "pipeline" / "chapter_metadata_cache.json"
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            cache_file.write_text('{"test": []}')
        
        with caplog.at_level(logging.INFO):
            with patch('src.pipeline.generate_chapter_metadata.main', side_effect=mock_main_side_effect):
                # Act
                adapter.extract()
        
        # Assert
        assert "Extracting chapter metadata" in caplog.text
        assert "Extraction complete" in caplog.text
    
    def test_extract_returns_path_not_string(self, adapter):
        """
        RED: Test adapter returns Path object (not string)
        
        Validates:
        - Return type is pathlib.Path
        - Type hints are properly enforced
        """
        # Arrange
        def mock_main_side_effect():
            cache_file = Path(__file__).parent.parent / "src" / "pipeline" / "chapter_metadata_cache.json"
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            cache_file.write_text('{}')
        
        with patch('src.pipeline.generate_chapter_metadata.main', side_effect=mock_main_side_effect):
            # Act
            result = adapter.extract()
        
        # Assert
        assert isinstance(result, Path)
        assert not isinstance(result, str)
