"""
MetadataExtractorAdapter - Wraps legacy generate_chapter_metadata

Pattern: Adapter Pattern (Architecture Patterns with Python Ch. 13)
Purpose: Adapt legacy metadata extraction to new infrastructure

Resolves Conflicts:
- Hardcoded cache path → Predictable cache location
- Print statements → logging.info()
- No type hints → Path return type
- Direct LLM calls → (handled by legacy function, wrapped here)
"""

import logging
from pathlib import Path
from typing import Optional


class MetadataExtractionError(Exception):
    """Raised when metadata extraction fails"""
    pass


class MetadataExtractorAdapter:
    """
    Adapter wrapping legacy generate_chapter_metadata.main()
    
    Provides clean interface to chapter metadata extraction while maintaining
    compatibility with existing pipeline code.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize adapter
        
        Args:
            logger: Optional logger instance. If None, creates default logger.
        """
        self.logger = logger or logging.getLogger(__name__)
    
    def extract(self) -> Path:
        """
        Extract chapter metadata for all books
        
        Wraps the legacy main() function from generate_chapter_metadata,
        providing proper error handling, logging, and path management.
        
        Returns:
            Path: Path to updated chapter_metadata_cache.json file
        
        Raises:
            MetadataExtractionError: If extraction fails
        """
        self.logger.info("Extracting chapter metadata from all books")
        
        try:
            # Import legacy function (lazy import to avoid circular dependencies)
            from workflows.w03_metadata_extraction.scripts.generate_chapter_metadata import main
            
            # Call legacy function (returns None, updates cache file in-place)
            main()
            
            # Find cache file (hardcoded location in legacy code)
            # Legacy path: Path(__file__).parent / "chapter_metadata_cache.json"
            cache_path = Path(__file__).parent.parent / "chapter_metadata_cache.json"
            
            if not cache_path.exists():
                raise MetadataExtractionError(
                    f"Extraction completed but cache file not found: {cache_path}"
                )
            
            self.logger.info(f"Extraction complete: {cache_path}")
            return cache_path
            
        except Exception as e:
            error_msg = f"Failed to extract metadata: {str(e)}"
            self.logger.error(error_msg)
            raise MetadataExtractionError(error_msg) from e
