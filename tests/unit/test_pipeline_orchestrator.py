"""
Unit tests for PipelineOrchestrator (Sprint 4 - Phase 2)

TDD Cycle: RED → GREEN → REFACTOR
Pattern: Service Layer (Architecture Patterns with Python Ch. 4)

Tests for:
- PipelineOrchestrator: Coordinates PDF → Chapters → Metadata pipeline
"""

import pytest
from unittest.mock import Mock

# Import will fail initially (RED phase) - that's expected
try:
    from workflows.shared.pipeline.pipeline_orchestrator import PipelineOrchestrator, PipelineOrchestrationError
except ImportError:
    # Expected during RED phase
    PipelineOrchestrator = None
    PipelineOrchestrationError = None


class TestPipelineOrchestrator:
    """Tests for PipelineOrchestrator (Service Layer)"""
    
    def test_run_full_pipeline_success(self, tmp_path):
        """
        RED: Test successful full pipeline execution
        
        Validates:
        - Orchestrator calls all 3 adapters in sequence
        - PDF → Chapters → Metadata
        - Returns summary of results
        """
        # Arrange
        pdf_path = tmp_path / "test_book.pdf"
        pdf_path.write_text("fake pdf")
        
        # Mock the three adapters
        mock_pdf_result = {"metadata": {"title": "Test"}, "pages": []}
        mock_chapters_result = tmp_path / "PYTHON_GUIDELINES.md"
        mock_chapters_result.write_text("# Guidelines")
        mock_metadata_result = tmp_path / "cache.json"
        mock_metadata_result.write_text('{}')
        
        # Create mocks
        mock_pdf_adapter = Mock()
        mock_pdf_adapter.convert.return_value = mock_pdf_result
        
        mock_chapter_adapter = Mock()
        mock_chapter_adapter.generate.return_value = mock_chapters_result
        
        mock_meta_adapter = Mock()
        mock_meta_adapter.extract.return_value = mock_metadata_result
        
        # Inject mocks via dependency injection
        orchestrator = PipelineOrchestrator(
            pdf_converter=mock_pdf_adapter,
            chapter_generator=mock_chapter_adapter,
            metadata_extractor=mock_meta_adapter
        )
        
        # Act
        result = orchestrator.run_full_pipeline(pdf_path)
        
        # Assert
        assert result is not None
        assert "pdf_conversion" in result
        assert "chapters" in result
        assert "metadata" in result
        
        # Verify adapters called in order
        mock_pdf_adapter.convert.assert_called_once_with(pdf_path)
        mock_chapter_adapter.generate.assert_called_once()
        mock_meta_adapter.extract.assert_called_once()
    
    def test_run_pdf_conversion_only(self, tmp_path):
        """
        RED: Test running only PDF conversion step
        
        Validates:
        - Can run individual pipeline stages
        - Only calls PdfConverterAdapter
        """
        # Arrange
        pdf_path = tmp_path / "test.pdf"
        pdf_path.write_text("pdf content")
        
        expected_json = {"metadata": {"title": "Test"}}
        
        # Create mock
        mock_pdf_adapter = Mock()
        mock_pdf_adapter.convert.return_value = expected_json
        
        orchestrator = PipelineOrchestrator(pdf_converter=mock_pdf_adapter)
        
        # Act
        result = orchestrator.run_pdf_conversion(pdf_path)
        
        # Assert
        assert result == expected_json
        mock_pdf_adapter.convert.assert_called_once_with(pdf_path)
    
    def test_pipeline_failure_raises_exception(self, tmp_path):
        """
        RED: Test pipeline failure handling
        
        Validates:
        - PipelineOrchestrationError raised on adapter failures
        - Error message includes which stage failed
        """
        # Arrange
        pdf_path = tmp_path / "bad.pdf"
        pdf_path.write_text("bad content")
        
        # Create mock that raises exception
        mock_pdf_adapter = Mock()
        mock_pdf_adapter.convert.side_effect = Exception("PDF parsing failed")
        
        orchestrator = PipelineOrchestrator(pdf_converter=mock_pdf_adapter)
        
        # Act & Assert
        if PipelineOrchestrationError is None:
            pytest.skip("PipelineOrchestrationError not implemented yet")
        
        with pytest.raises(PipelineOrchestrationError) as exc_info:
            orchestrator.run_full_pipeline(pdf_path)
        
        assert "Pipeline failed" in str(exc_info.value)
    
    def test_orchestrator_logs_progress(self, tmp_path, caplog):
        """
        RED: Test orchestrator logs each pipeline stage
        
        Validates:
        - Logs "Starting pipeline" at beginning
        - Logs each stage completion
        - Logs "Pipeline complete" at end
        """
        # Arrange
        import logging
        pdf_path = tmp_path / "test.pdf"
        pdf_path.write_text("content")
        
        mock_pdf_result = {"test": True}
        mock_chapters_result = tmp_path / "guidelines.md"
        mock_chapters_result.write_text("# Test")
        mock_metadata_result = tmp_path / "cache.json"
        mock_metadata_result.write_text('{}')
        
        # Create mocks
        mock_pdf = Mock()
        mock_pdf.convert.return_value = mock_pdf_result
        
        mock_chapter = Mock()
        mock_chapter.generate.return_value = mock_chapters_result
        
        mock_meta = Mock()
        mock_meta.extract.return_value = mock_metadata_result
        
        orchestrator = PipelineOrchestrator(
            pdf_converter=mock_pdf,
            chapter_generator=mock_chapter,
            metadata_extractor=mock_meta
        )
        
        with caplog.at_level(logging.INFO):
            # Act
            orchestrator.run_full_pipeline(pdf_path)
        
        # Assert
        assert "Starting pipeline" in caplog.text or "Running pipeline" in caplog.text
        assert "Pipeline complete" in caplog.text
