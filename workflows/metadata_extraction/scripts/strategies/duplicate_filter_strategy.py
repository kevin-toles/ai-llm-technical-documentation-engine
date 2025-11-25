"""
DuplicateFilterStrategy - Remove duplicate chapter numbers

PRIORITY: Medium (cleanup false positives)
USE CASE: Headers/footers cause same chapter to be detected on multiple pages

Strategy: Keep FIRST valid occurrence of each chapter number
"""

from typing import List, Tuple


class DuplicateFilterStrategy:
    """
    Strategy for removing duplicate chapter numbers.
    
    Duplicates occur when:
    - Chapter title appears in header/footer on multiple pages
    - Regex matches both actual chapter start and page headers
    
    Solution: Keep only the first occurrence of each chapter number.
    
    Args:
        None
    
    Reference: Python Distilled Ch. 5 (Data Structures)
    """
    
    def __init__(self):
        pass
    
    def filter(self, candidate_chapters: List[Tuple]) -> List[Tuple]:
        """
        Remove duplicate chapter numbers, keeping first occurrence.
        
        Args:
            candidate_chapters: List of (chapter_num, title, start_page, end_page) tuples
        
        Returns:
            List with duplicates removed, sorted by start_page
        
        Algorithm:
            1. Sort chapters by start_page (ascending)
            2. Use chapter_num as uniqueness key
            3. Keep first occurrence of each unique chapter_num
        """
        if not candidate_chapters:
            return []
        
        # Sort by start page to ensure we keep earliest occurrence
        sorted_chapters = sorted(candidate_chapters, key=lambda x: x[2])  # sort by start_page (index 2)
        
        seen = set()
        unique = []
        
        for chapter_num, title, start_page, end_page in sorted_chapters:
            # Use chapter_num to detect duplicates
            # (same chapter_num on different pages = duplicate from header/footer)
            key = chapter_num
            
            if key not in seen:
                seen.add(key)
                unique.append((chapter_num, title, start_page, end_page))
        
        return unique
