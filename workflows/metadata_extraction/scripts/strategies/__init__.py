"""
Chapter Detection Strategies

Strategy Pattern implementation for extracting chapters from documents.
Reduces cyclomatic complexity by separating detection methods.

Reference Documents:
- Architecture Patterns with Python Ch. 13 (Dependency Injection)
- Architecture Patterns with Python Ch. 4 (Adapter Pattern)
- Python Distilled Ch. 7 (Classes and OOP)
"""

from typing import Protocol, List, Dict, Tuple


class ChapterDetectionStrategy(Protocol):
    """
    Protocol for chapter detection strategies.
    
    Per Python Distilled Ch. 7: Use protocols for structural subtyping.
    All strategies must implement the detection interface.
    """
    
    def detect(self, pages: List[Dict], **kwargs) -> List[Tuple]:
        """
        Detect chapters from pages.
        
        Args:
            pages: List of page dicts with {page_number, content}
            **kwargs: Strategy-specific parameters
        
        Returns:
            List of (chapter_num, title, start_page, end_page) tuples
        """
        ...
