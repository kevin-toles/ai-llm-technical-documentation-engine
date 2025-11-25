"""
YAKEValidationStrategy - Validate chapters have real content

PRIORITY: High (filters out TOC entries and noise)
USE CASE: Distinguish real chapters from table-of-contents entries

Reference: DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md
"""

from typing import List, Dict, Tuple


class YAKEValidationStrategy:
    """
    Strategy for validating chapters using YAKE keyword extraction.
    
    Real chapters have rich vocabulary (many keywords).
    TOC pages have sparse vocabulary (few keywords).
    
    Args:
        extractor: StatisticalExtractor instance for YAKE
        min_keywords: Minimum keywords required to pass validation (default: 5)
    
    Reference: DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md (YAKE for domain-agnostic extraction)
    """
    
    def __init__(self, extractor, min_keywords: int = 5, min_content_length: int = 100):
        self.extractor = extractor
        self.min_keywords = min_keywords
        self.min_content_length = min_content_length
    
    def validate(self, candidate_chapters: List[Tuple], pages: List[Dict]) -> List[Tuple]:
        """
        Validate chapters have sufficient keyword density.
        
        Args:
            candidate_chapters: List of (chapter_num, title, start_page, end_page) tuples
            pages: List of page dicts with {page_number, content}
        
        Returns:
            Filtered list containing only chapters with >= min_keywords
        
        Algorithm:
            1. For each candidate chapter, get page content
            2. Extract keywords using YAKE
            3. Keep chapter if keyword count >= threshold
        """
        if not candidate_chapters:
            return []
        
        # Create page lookup for fast access
        page_lookup = {p.get('page_number'): p.get('content', '') for p in pages}
        
        validated = []
        
        for chapter_num, title, start_page, end_page in candidate_chapters:
            # Get content for this chapter's starting page
            content = page_lookup.get(start_page, '')
            
            # Skip if too short (likely header/footer)
            if len(content) < self.min_content_length:
                continue
            
            # Extract keywords using YAKE
            try:
                # Use first 2000 chars for performance
                sample_text = content[:2000]
                keywords = self.extractor.extract_keywords(sample_text, top_n=self.min_keywords + 5)
                
                # Validate keyword count
                if len(keywords) >= self.min_keywords:
                    validated.append((chapter_num, title, start_page, end_page))
            
            except Exception:
                # If keyword extraction fails, skip this candidate
                continue
        
        return validated
