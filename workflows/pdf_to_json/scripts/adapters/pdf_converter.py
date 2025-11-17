"""
PDF Converter Adapter

Wraps legacy convert_pdf_to_json function with clean interface.
Integrates with llm-document-enhancer infrastructure (config, logging, error handling).

Pattern: Adapter Pattern (Architecture Patterns with Python Ch. 13)
Reference: docs/analysis/sprint4-pipeline-analysis.md
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any

from config.settings import settings


class PdfConversionError(Exception):
    """Raised when PDF conversion fails"""
    pass


class PdfConverterAdapter:
    """
    Adapter for PDF to JSON conversion.
    
    Wraps legacy convert_pdf_to_json function, providing:
    - Config-based path management (not hardcoded)
    - Structured logging (not print statements)
    - Path objects (not strings)
    - Domain exceptions (not silent failures)
    
    Usage:
        adapter = PdfConverterAdapter()
        json_data = adapter.convert(Path("book.pdf"))
    """
    
    def __init__(self, logger=None):
        """
        Initialize adapter.
        
        Args:
            logger: Optional logger instance (for testing)
        """
        self.logger = logger or logging.getLogger(__name__)
    
    def convert(self, pdf_path: Path) -> Dict[str, Any]:
        """
        Convert PDF to JSON structure.
        
        Args:
            pdf_path: Path to input PDF file
        
        Returns:
            JSON data dictionary with metadata and pages
        
        Raises:
            PdfConversionError: If conversion fails
            FileNotFoundError: If PDF file doesn't exist
        """
        # Import legacy function (lazy import to avoid circular dependencies)
        from workflows.pdf_to_json.scripts.convert_pdf_to_json import convert_pdf_to_json
        
        # Validate input
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        # Determine output path using config (not hardcoded)
        output_path = settings.paths.textbooks_json_dir / f"{pdf_path.stem}.json"
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Log conversion start
        self.logger.info(f"Converting PDF: {pdf_path}")
        
        # Call legacy function (expects strings, not Path objects)
        success = convert_pdf_to_json(str(pdf_path), str(output_path))
        
        if not success:
            raise PdfConversionError(f"Failed to convert: {pdf_path}")
        
        # Log completion
        self.logger.info(f"Conversion complete: {output_path}")
        
        # Load and return JSON data
        return json.loads(output_path.read_text())
