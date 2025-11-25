"""
PreDefinedStrategy - Extract chapters from JSON metadata

PRIORITY: Highest (try first)
USE CASE: When JSON already contains chapter definitions
"""

from typing import List, Dict, Tuple, Optional


class PreDefinedStrategy:
    """
    Strategy for extracting pre-defined chapters from JSON metadata.
    
    This is the fastest and most accurate method when available.
    
    Args:
        metadata: JSON metadata dict that may contain "chapters" key
    
    Reference: Architecture Patterns with Python Ch. 13 (Dependency Injection)
    """
    
    def __init__(self, metadata: Dict):
        self.metadata = metadata
    
    def detect(self, pages: List[Dict], **kwargs) -> List[Tuple]:
        """
        Extract chapters from metadata.
        
        Args:
            pages: Not used (metadata is self-contained)
            **kwargs: Not used
        
        Returns:
            List of (chapter_num, title, start_page, end_page) tuples
        
        Example:
            >>> metadata = {"chapters": [{"number": 1, "title": "Intro", "start_page": 1, "end_page": 10}]}
            >>> strategy = PreDefinedStrategy(metadata)
            >>> chapters = strategy.detect([])
            >>> assert chapters[0] == (1, 'Intro', 1, 10)
        """
        chapters = self.metadata.get('chapters', [])
        
        if not chapters:
            return []
        
        results = []
        for chapter in chapters:
            try:
                # Validate required fields
                number = chapter.get('number') or chapter.get('chapter_number')
                title = chapter.get('title')
                start_page = chapter.get('start_page')
                end_page = chapter.get('end_page')
                
                if all([number is not None, title, start_page is not None, end_page is not None]):
                    # Return format: (chapter_num, title, start_page, end_page)
                    results.append((number, title, start_page, end_page))
            except (KeyError, TypeError, AttributeError):
                # Skip malformed entries
                continue
        
        return results
