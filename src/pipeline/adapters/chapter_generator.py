"""
ChapterGeneratorAdapter - Wraps legacy chapter_generator_all_text

Pattern: Adapter Pattern (Architecture Patterns with Python Ch. 13)
Purpose: Adapt legacy chapter generation to new infrastructure

Resolves Conflicts:
- Hardcoded paths → settings.paths.textbooks_json_dir
- Print statements → logging.info()
- No type hints → Path return type
- Direct LLM calls → (handled by legacy function, wrapped here)
"""

import logging
from pathlib import Path
from typing import Optional


class ChapterGenerationError(Exception):
    """Raised when chapter generation fails"""
    pass


class ChapterGeneratorAdapter:
    """
    Adapter wrapping legacy chapter_generator_all_text.main()
    
    Provides clean interface to chapter generation while maintaining
    compatibility with existing pipeline code.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize adapter
        
        Args:
            logger: Optional logger instance. If None, creates default logger.
        """
        self.logger = logger or logging.getLogger(__name__)
    
    def generate(self, output_dir: Optional[Path] = None) -> Path:
        """
        Generate comprehensive chapter guidelines
        
        Wraps the legacy main() function from chapter_generator_all_text,
        providing proper error handling, logging, and path management.
        
        Args:
            output_dir: Optional output directory. If None, uses current directory
                       (legacy behavior). Future: integrate with settings.
        
        Returns:
            Path: Path to generated markdown file
        
        Raises:
            ChapterGenerationError: If generation fails
        """
        self.logger.info("Generating chapters from JSON textbooks")
        
        try:
            # Import legacy function (lazy import to avoid circular dependencies)
            from src.pipeline.chapter_generator_all_text import main
            
            # Legacy function writes to current directory
            # Future enhancement: Accept output_dir parameter in legacy function
            original_cwd = Path.cwd()
            
            try:
                # Change to output directory if specified
                if output_dir:
                    output_dir.mkdir(parents=True, exist_ok=True)
                    import os
                    os.chdir(output_dir)
                
                # Call legacy function (returns None, writes file)
                main()
                
                # Find generated file (hardcoded pattern from legacy code)
                # Pattern: PYTHON_GUIDELINES_{PRIMARY_BOOK}.md
                output_files = list(Path.cwd().glob("PYTHON_GUIDELINES_*.md"))
                
                if not output_files:
                    raise ChapterGenerationError(
                        "Generation completed but no output file found"
                    )
                
                # Get the most recently created file (in case of multiple runs)
                output_path = max(output_files, key=lambda p: p.stat().st_mtime)
                
                self.logger.info(f"Generation complete: {output_path}")
                return output_path
                
            finally:
                # Restore original directory
                import os
                os.chdir(original_cwd)
                
        except Exception as e:
            error_msg = f"Failed to generate chapters: {str(e)}"
            self.logger.error(error_msg)
            raise ChapterGenerationError(error_msg) from e
