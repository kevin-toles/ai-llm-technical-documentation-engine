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

# Constants (Python Distilled Ch. 2: Best Practices)
CACHE_FILENAME = "chapter_metadata_cache.json"


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
            from workflows.metadata_enrichment.scripts.generate_chapter_metadata import main
            
            # Call legacy function (returns None, updates cache file in-place)
            main()
            
            # Find cache file (hardcoded location in legacy code)
            # The legacy function creates the cache in a fixed location
            # For tests, we need to find it relative to the project root
            from pathlib import Path
            
            # Get project root (go up from workflows/metadata_extraction/scripts/adapters/)
            # __file__ -> adapters/ -> scripts/ -> metadata_extraction/ -> workflows/ -> PROJECT_ROOT
            project_root = Path(__file__).parent.parent.parent.parent.parent
            
            # Try multiple possible locations for cache file
            possible_cache_paths = [
                project_root / "tests" / "src" / "pipeline" / CACHE_FILENAME,  # Test location
                project_root / "workflows" / "metadata_cache_merge" / "output" / CACHE_FILENAME,  # Output location
                Path(__file__).parent.parent / CACHE_FILENAME,  # Adjacent to scripts/
            ]
            
            cache_path = None
            for path in possible_cache_paths:
                if path.exists():
                    cache_path = path
                    break
            
            if cache_path is None:
                raise MetadataExtractionError(
                    f"Extraction completed but cache file not found in any expected location: {[str(p) for p in possible_cache_paths]}"
                )
            
            self.logger.info(f"Extraction complete: {cache_path}")
            return cache_path
            
        except Exception as e:
            error_msg = f"Failed to extract metadata: {str(e)}"
            self.logger.error(error_msg)
            raise MetadataExtractionError(error_msg) from e
