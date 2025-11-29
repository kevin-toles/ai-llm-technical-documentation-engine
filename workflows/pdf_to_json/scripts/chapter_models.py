"""
Chapter data structures for segmentation.

Separated to avoid circular imports between chapter_segmenter and services.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class Chapter:
    """Chapter data structure.
    
    Attributes:
        number: Sequential chapter number (1-indexed)
        title: Chapter title (extracted or synthetic)
        start_page: First page of chapter
        end_page: Last page of chapter
        detection_method: How this chapter was detected (regex_*, topic_boundary, synthetic)
    """
    number: int
    title: str
    start_page: int
    end_page: int
    detection_method: str
    
    def to_dict(self) -> Dict:
        """Convert to dict for JSON serialization."""
        return {
            "number": self.number,
            "title": self.title,
            "start_page": self.start_page,
            "end_page": self.end_page,
            "detection_method": self.detection_method
        }
