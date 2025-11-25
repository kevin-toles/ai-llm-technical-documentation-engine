"""
RegexPatternStrategy - Find chapter markers using regex patterns

PRIORITY: Medium (fallback when no pre-defined chapters)
USE CASE: Books with clear chapter markers ("Chapter N: Title")
"""

import re
from typing import List, Dict, Tuple


class RegexPatternStrategy:
    """
    Strategy for detecting chapters via regex pattern matching.
    
    Supports multiple chapter marker formats:
    - "Chapter 1: Title" (most common)
    - "CHAPTER 1: TITLE" (uppercase variant)
    - "Item 1: Title" (Effective Python style)
    - "1 Title" (numeric prefix)
    
    Args:
        None (uses fixed patterns)
    
    Reference: Python Distilled Ch. 5 (Regular Expressions)
    """
    
    def __init__(self):
        # Compile regex patterns for performance
        self.patterns = [
            (re.compile(r'(?:Chapter|CHAPTER)\s+(\d+)[\s\.:]+([^\n]+)', re.MULTILINE), "chapter"),
            (re.compile(r'^\s*Item\s+(\d+)\s*[:.-]\s+(.+)$', re.MULTILINE), "item"),
            (re.compile(r'^(\d+)\s+([A-Z][A-Z\s]{10,})', re.MULTILINE), "numeric"),
        ]
    
    def detect(self, pages: List[Dict], **kwargs) -> List[Tuple]:
        """
        Detect chapters using regex pattern matching.
        
        Args:
            pages: List of page dicts with {page_number, content}
            **kwargs: Optional parameters
                - max_lines_to_scan: Number of lines to check per page (default: 25)
        
        Returns:
            List of (start_page, title, start, end) tuples
        
        Algorithm:
            1. Scan first 25 lines of each page for chapter markers
            2. Extract chapter number and title
            3. Return candidates (validation happens in later strategies)
        """
        max_lines = kwargs.get('max_lines_to_scan', 25)
        candidates = []
        seen_numbers = set()
        
        for page in pages:
            page_num = page.get('page_number', 0)
            content = page.get('content', '')
            
            # Skip empty or very short pages (but allow test data)
            if len(content.strip()) < 50:
                continue
            
            # Check first N lines for chapter markers
            lines = content.split('\n')[:max_lines]
            first_text = '\n'.join(lines)
            
            # Try each pattern
            for pattern, pattern_type in self.patterns:
                match = pattern.search(first_text)
                if match:
                    try:
                        chapter_num = int(match.group(1))
                        title = match.group(2).strip().rstrip('.')
                        
                        # Skip duplicates (will be handled by DuplicateFilterStrategy)
                        if chapter_num in seen_numbers:
                            continue
                        
                        seen_numbers.add(chapter_num)
                        
                        # Add candidate: (chapter_num, title, start_page, temp_end_page)
                        # End page will be calculated later
                        candidates.append((chapter_num, title, page_num, page_num))
                        break  # Found match, no need to try other patterns
                    
                    except (ValueError, IndexError, AttributeError):
                        # Malformed match, skip
                        continue
        
        # Sort by start_page
        candidates.sort(key=lambda x: x[2])
        
        # Calculate end pages (start of next chapter - 1)
        if len(candidates) > 0:
            results = []
            for i, (chapter_num, title, start_page, _) in enumerate(candidates):
                if i + 1 < len(candidates):
                    end_page = candidates[i + 1][2] - 1  # Next chapter's start_page - 1
                else:
                    # Last chapter: use last page from pages list
                    end_page = pages[-1].get('page_number', start_page) if pages else start_page
                
                results.append((chapter_num, title, start_page, end_page))
            
            return results
        
        return []
