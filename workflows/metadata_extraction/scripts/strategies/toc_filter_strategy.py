"""
TOCFilterStrategy - Remove Table of Contents pages

PRIORITY: Medium (removes false positives)
USE CASE: Filter out TOC pages that have chapter markers but aren't real chapters

Heuristic: TOC pages have many isolated numbers (page references)
"""

import re
from typing import List, Dict, Tuple


class TOCFilterStrategy:
    """
    Strategy for filtering out Table of Contents pages.
    
    TOC pages are characterized by:
    - Many isolated numbers (page references like "1 2 3 4 5...")
    - Short text between numbers
    - Repetitive structure
    
    Args:
        threshold: Maximum isolated numbers before page is considered TOC (default: 8)
    
    Reference: Python Distilled Ch. 5 (Regular Expressions)
    """
    
    def __init__(self, threshold: int = 8):
        self.threshold = threshold
        # Regex to find isolated numbers (digits with word boundaries)
        self.isolated_number_pattern = re.compile(r'\b(\d{1,3})\b')
    
    def filter(self, candidate_chapters: List[Tuple], pages: List[Dict]) -> List[Tuple]:
        """
        Filter out TOC pages from candidate chapters.
        
        Args:
            candidate_chapters: List of (chapter_num, title, start_page, end_page) tuples
            pages: List of page dicts with {page_number, content}
        
        Returns:
            Filtered list with TOC pages removed
        
        Algorithm:
            1. For each candidate chapter, check starting page
            2. Count isolated numbers in first 1000 chars
            3. If count > threshold, mark as TOC and exclude
        """
        if not candidate_chapters:
            return []
        
        # Create page lookup
        page_lookup = {p.get('page_number'): p.get('content', '') for p in pages}
        
        filtered = []
        
        for chapter_num, title, start_page, end_page in candidate_chapters:
            content = page_lookup.get(start_page, '')
            
            # Check first 1000 characters for TOC pattern
            sample = content[:1000]
            
            # Count isolated numbers
            matches = self.isolated_number_pattern.findall(sample)
            isolated_count = len(matches)
            
            # Keep if below threshold (not a TOC)
            if isolated_count <= self.threshold:
                filtered.append((chapter_num, title, start_page, end_page))
        
        return filtered
