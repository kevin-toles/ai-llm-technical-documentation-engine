"""
PipelineOrchestrator - Service Layer for Pipeline Integration

Pattern: Service Layer (Architecture Patterns with Python Ch. 4)
Purpose: Orchestrate PDF → Chapters → Metadata pipeline

The Service Layer acts as an orchestration boundary between the external
interface and the domain logic (adapters). It coordinates the sequence of
operations needed to complete a use case.

Reference:
- Architecture Patterns with Python, Ch. 4, pp. 59-86
- "Flask API and Service Layer"
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import adapters from their workflow-specific locations
from workflows.pdf_to_json.scripts.adapters import (
    PdfConverterAdapter,
    PdfConversionError,
)
from workflows.metadata_extraction.scripts.adapters import (
    MetadataExtractorAdapter,
    MetadataExtractionError,
)
from workflows.base_guideline_generation.scripts.adapters import (
    ChapterGeneratorAdapter,
    ChapterGenerationError,
)


class PipelineOrchestrationError(Exception):
    """Raised when pipeline orchestration fails"""
    pass


class PipelineOrchestrator:
    """
    Service Layer: Orchestrates the document enhancement pipeline
    
    Coordinates three adapters in sequence:
    1. PdfConverterAdapter: PDF → JSON
    2. ChapterGeneratorAdapter: JSON → Enhanced Markdown
    3. MetadataExtractorAdapter: JSON → Metadata Cache
    
    Pattern: Service Layer (acts as orchestration boundary)
    """
    
    def __init__(
        self,
        pdf_converter: Optional[PdfConverterAdapter] = None,
        chapter_generator: Optional[ChapterGeneratorAdapter] = None,
        metadata_extractor: Optional[MetadataExtractorAdapter] = None,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize orchestrator with adapters (dependency injection)
        
        Args:
            pdf_converter: PDF conversion adapter (created if None)
            chapter_generator: Chapter generation adapter (created if None)
            metadata_extractor: Metadata extraction adapter (created if None)
            logger: Optional logger instance. If None, creates default logger.
        """
        self.logger = logger or logging.getLogger(__name__)
        
        # Initialize adapters (dependency injection pattern)
        self.pdf_converter = pdf_converter or PdfConverterAdapter(logger=self.logger)
        self.chapter_generator = chapter_generator or ChapterGeneratorAdapter(logger=self.logger)
        self.metadata_extractor = metadata_extractor or MetadataExtractorAdapter(logger=self.logger)
    
    def run_full_pipeline(self, pdf_path: Path) -> Dict[str, Any]:
        """
        Run complete pipeline: PDF → Chapters → Metadata
        
        Orchestrates all three stages in sequence, handling errors
        and logging progress at each step.
        
        Args:
            pdf_path: Path to input PDF file
        
        Returns:
            Dict containing results from each stage:
            {
                "pdf_conversion": {...},
                "chapters": Path(...),
                "metadata": Path(...)
            }
        
        Raises:
            PipelineOrchestrationError: If any stage fails
        """
        self.logger.info(f"Starting pipeline for: {pdf_path}")
        
        results = {}
        
        try:
            # Stage 1: PDF Conversion
            self.logger.info("Stage 1/3: Converting PDF to JSON...")
            pdf_result = self.pdf_converter.convert(pdf_path)
            results["pdf_conversion"] = pdf_result
            self.logger.info("✓ PDF conversion complete")
            
            # Stage 2: Chapter Generation
            self.logger.info("Stage 2/3: Generating enhanced chapters...")
            chapters_result = self.chapter_generator.generate()
            results["chapters"] = chapters_result
            self.logger.info(f"✓ Chapter generation complete: {chapters_result}")
            
            # Stage 3: Metadata Extraction
            self.logger.info("Stage 3/3: Extracting chapter metadata...")
            metadata_result = self.metadata_extractor.extract()
            results["metadata"] = metadata_result
            self.logger.info(f"✓ Metadata extraction complete: {metadata_result}")
            
            self.logger.info("Pipeline complete!")
            return results
            
        except (PdfConversionError, ChapterGenerationError, MetadataExtractionError) as e:
            error_msg = f"Pipeline failed during {self._get_current_stage(results)}: {str(e)}"
            self.logger.error(error_msg)
            raise PipelineOrchestrationError(error_msg) from e
        except Exception as e:
            error_msg = f"Pipeline failed with unexpected error: {str(e)}"
            self.logger.error(error_msg)
            raise PipelineOrchestrationError(error_msg) from e
    
    def run_pdf_conversion(self, pdf_path: Path) -> Dict[str, Any]:
        """
        Run only PDF conversion stage
        
        Useful for testing or when only JSON output is needed.
        
        Args:
            pdf_path: Path to input PDF file
        
        Returns:
            Dict: Parsed JSON data from PDF
        
        Raises:
            PipelineOrchestrationError: If conversion fails
        """
        self.logger.info(f"Running PDF conversion only for: {pdf_path}")
        
        try:
            result = self.pdf_converter.convert(pdf_path)
            self.logger.info("PDF conversion complete")
            return result
        except PdfConversionError as e:
            error_msg = f"PDF conversion failed: {str(e)}"
            self.logger.error(error_msg)
            raise PipelineOrchestrationError(error_msg) from e
    
    def run_chapter_generation(self) -> Path:
        """
        Run only chapter generation stage
        
        Assumes JSON files already exist (from previous PDF conversion).
        
        Returns:
            Path: Path to generated markdown file
        
        Raises:
            PipelineOrchestrationError: If generation fails
        """
        self.logger.info("Running chapter generation only")
        
        try:
            result = self.chapter_generator.generate()
            self.logger.info(f"Chapter generation complete: {result}")
            return result
        except ChapterGenerationError as e:
            error_msg = f"Chapter generation failed: {str(e)}"
            self.logger.error(error_msg)
            raise PipelineOrchestrationError(error_msg) from e
    
    def run_metadata_extraction(self) -> Path:
        """
        Run only metadata extraction stage
        
        Assumes JSON files already exist (from previous PDF conversion).
        
        Returns:
            Path: Path to updated metadata cache file
        
        Raises:
            PipelineOrchestrationError: If extraction fails
        """
        self.logger.info("Running metadata extraction only")
        
        try:
            result = self.metadata_extractor.extract()
            self.logger.info(f"Metadata extraction complete: {result}")
            return result
        except MetadataExtractionError as e:
            error_msg = f"Metadata extraction failed: {str(e)}"
            self.logger.error(error_msg)
            raise PipelineOrchestrationError(error_msg) from e
    
    def _get_current_stage(self, results: Dict[str, Any]) -> str:
        """Helper to determine which stage failed based on results"""
        if "pdf_conversion" not in results:
            return "PDF conversion (stage 1/3)"
        elif "chapters" not in results:
            return "chapter generation (stage 2/3)"
        elif "metadata" not in results:
            return "metadata extraction (stage 3/3)"
        else:
            return "unknown stage"
