"""
TOCParserStrategy - Parse Table of Contents for Chapter Detection

PRIORITY: High (before RegexPatternStrategy)
USE CASE: Books where TOC provides accurate chapter→page mappings

This strategy:
1. Locates the Table of Contents page
2. Extracts chapter title → page number mappings
3. Calculates page offset (logical vs physical pages)
4. Validates chapters have real content via YAKE (optional fallback)

Algorithm:
1. Find TOC page by looking for "Table of Contents" or "Contents" header
2. Parse chapter entries using multiple regex patterns:
   - "Chapter N: Title" followed by page number on next line
   - "Chapter N: Title ......... page" inline format
   - "N Title page" numeric prefix format
3. Calculate offset by finding where chapter content actually starts
4. Apply offset to get actual page numbers
5. Optionally validate with YAKE to ensure chapters have real content

References:
- Architecture Patterns with Python Ch. 13 (Strategy Pattern)
- Python Distilled Ch. 5 (Regular Expressions)
- DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md (YAKE integration)
"""

import re
from typing import List, Dict, Tuple, Optional, Any


class TOCParserStrategy:
    """
    Strategy for detecting chapters by parsing the Table of Contents.
    
    Solves the problem where books have:
    - Non-standard chapter markers (e.g., "1\\nUnderstanding Microservices" instead of "Chapter 1:")
    - Page offset issues (TOC lists page 8, but actual content is on page 22)
    
    Args:
        yake_extractor: Optional StatisticalExtractor for content validation
        min_keywords: Minimum keywords to consider a page has real content (default: 3)
        
    Reference: Architecture Patterns with Python Ch. 13 (Strategy Pattern)
    """
    
    def __init__(self, yake_extractor=None, min_keywords: int = 3):
        self.yake_extractor = yake_extractor
        self.min_keywords = min_keywords
        
        # Compile regex patterns for TOC header detection
        self.toc_header_patterns = [
            re.compile(r'^Table\s+of\s+Contents', re.IGNORECASE | re.MULTILINE),
            re.compile(r'^Contents\s*$', re.IGNORECASE | re.MULTILINE),
        ]
        
        # Patterns for extracting chapter entries from TOC
        # Pattern 1: "Chapter N: Title" on one line, page number on next line
        self.chapter_separate_line_pattern = re.compile(
            r'Chapter\s+(\d{1,3})\s*[:.]?\s*([^\n]{1,200})\n\s*(\d{1,4})\s*\n',
            re.IGNORECASE
        )
        
        # Pattern 2: "Chapter N: Title ......... page" inline
        self.chapter_inline_pattern = re.compile(
            r'Chapter\s+(\d{1,3})\s*[:.]?\s*([^\n\.]{1,200})\s*\.{2,}\s*(\d{1,4})',
            re.IGNORECASE
        )
        
        # Pattern 3: "N Title page" numeric prefix (space-separated on one line)
        self.numeric_prefix_pattern = re.compile(
            r'^(\d{1,3})\s+([A-Z][^\n]{5,100}?)\s{2,}(\d{1,4})\s*$',
            re.MULTILINE
        )
        
        # Pattern 4: "N\nTitle\npage" format (number, title, page on separate lines)
        # This handles "1\nUnderstanding Microservices\n8" format but we need title first
        # Re-parse after finding chapter entries
    
    def find_toc_page(self, pages: List[Dict]) -> Optional[Dict]:
        """
        Find the Table of Contents page.
        
        Args:
            pages: List of page dicts with {page_number, content}
            
        Returns:
            Page dict containing TOC, or None if not found
            
        Algorithm:
            1. Scan first 30 pages (TOC is usually early in book)
            2. Look for "Table of Contents" or "Contents" header
            3. Return first matching page
        """
        # Only scan first 30 pages to avoid false matches
        scan_limit = min(30, len(pages))
        
        for page in pages[:scan_limit]:
            content = page.get('content', '')
            
            for pattern in self.toc_header_patterns:
                if pattern.search(content):
                    return page
        
        return None
    
    def find_toc_pages(self, pages: List[Dict]) -> List[Dict]:
        """
        Find all pages that are part of the Table of Contents.
        
        TOC often spans multiple pages (e.g., pages 10-14 in a large book).
        
        Args:
            pages: List of page dicts with {page_number, content}
            
        Returns:
            List of page dicts that are part of the TOC
            
        Algorithm:
            1. Find first TOC page (with header)
            2. Continue scanning subsequent pages that have Chapter entries
            3. Stop when we hit actual content (long paragraphs without Chapter entries)
        """
        toc_start = self.find_toc_page(pages)
        if not toc_start:
            return []
        
        toc_pages = [toc_start]
        start_page_num = toc_start.get('page_number', 0)
        
        # Sort pages by page number
        sorted_pages = sorted(pages, key=lambda p: p.get('page_number', 0))
        
        # Find subsequent TOC pages (usually next 5-6 pages max)
        for page in sorted_pages:
            page_num = page.get('page_number', 0)
            
            # Skip until after our start page
            if page_num <= start_page_num:
                continue
            
            # Stop if we've gone too far (TOC rarely exceeds 10 pages)
            if page_num > start_page_num + 10:
                break
            
            content = page.get('content', '')
            
            # Check if this page still has Chapter entries (part of TOC)
            has_chapter_entries = bool(self.chapter_separate_line_pattern.search(content))
            
            # Also check for page number patterns common in TOC (like "123\n")
            has_toc_numbers = len(re.findall(r'\b\d{1,3}\b', content)) > 10
            
            if has_chapter_entries or has_toc_numbers:
                toc_pages.append(page)
            else:
                # No more TOC content, stop scanning
                break
        
        return toc_pages
    
    def parse_toc_entries(self, toc_content: str) -> List[Dict[str, Any]]:
        """
        Parse chapter entries from TOC content.
        
        Args:
            toc_content: Text content of the TOC page(s)
            
        Returns:
            List of dicts with {chapter_number, title, toc_page_number}
            
        Supports multiple formats:
        1. Separate line: "Chapter 1: Title\\n8\\n"
        2. Inline dots: "Chapter 1: Title ......... 8"
        3. Numeric prefix: "1 Title                    8"
        """
        entries = []
        seen_chapters = set()
        
        # Try Pattern 1: Separate line format
        for match in self.chapter_separate_line_pattern.finditer(toc_content):
            chapter_num = int(match.group(1))
            title = match.group(2).strip().rstrip('.')
            page_num = int(match.group(3))
            
            if chapter_num not in seen_chapters:
                entries.append({
                    'chapter_number': chapter_num,
                    'title': title,
                    'toc_page_number': page_num
                })
                seen_chapters.add(chapter_num)
        
        # If no matches, try Pattern 2: Inline dots format
        if not entries:
            for match in self.chapter_inline_pattern.finditer(toc_content):
                chapter_num = int(match.group(1))
                title = match.group(2).strip().rstrip('.')
                page_num = int(match.group(3))
                
                if chapter_num not in seen_chapters:
                    entries.append({
                        'chapter_number': chapter_num,
                        'title': title,
                        'toc_page_number': page_num
                    })
                    seen_chapters.add(chapter_num)
        
        # If still no matches, try Pattern 3: Numeric prefix
        if not entries:
            for match in self.numeric_prefix_pattern.finditer(toc_content):
                chapter_num = int(match.group(1))
                title = match.group(2).strip().rstrip('.')
                page_num = int(match.group(3))
                
                if chapter_num not in seen_chapters:
                    entries.append({
                        'chapter_number': chapter_num,
                        'title': title,
                        'toc_page_number': page_num
                    })
                    seen_chapters.add(chapter_num)
        
        # Sort by chapter number
        entries.sort(key=lambda x: x['chapter_number'])
        
        return entries
    
    def _is_chapter_content_page(
        self, 
        content: str, 
        chapter_title: str, 
        chapter_num: int
    ) -> bool:
        """
        Check if page content represents actual chapter start.
        
        A valid chapter page must have:
        - Chapter title in first 500 characters
        - Substantial content (> 500 chars with > 5 sentences)
        - Chapter number prefix OR "Chapter N" marker
        """
        if len(content) <= 500 or content.count('.') <= 5:
            return False
            
        title_prefix = chapter_title[:25].lower()
        has_title = title_prefix in content[:500].lower()
        if not has_title:
            return False
            
        content_start = content[:200].lower()
        has_chapter_num = content[:100].strip().startswith(str(chapter_num))
        has_chapter_marker = f'chapter {chapter_num}' in content_start
        
        return has_chapter_num or has_chapter_marker
    
    def _find_chapter_page(
        self, 
        pages: List[Dict], 
        chapter_title: str, 
        chapter_num: int, 
        min_page: int
    ) -> Optional[int]:
        """Find the actual page number where chapter content starts."""
        sorted_pages = sorted(pages, key=lambda p: p.get('page_number', 0))
        
        for page in sorted_pages:
            page_num = page.get('page_number', 0)
            if page_num < min_page:
                continue
                
            content = page.get('content', '')
            if self._is_chapter_content_page(content, chapter_title, chapter_num):
                return page_num
                
        return None
    
    def calculate_page_offset(
        self, 
        toc_entries: List[Dict[str, Any]], 
        pages: List[Dict]
    ) -> int:
        """
        Calculate page offset between TOC page numbers and actual content.
        
        Some books have front matter that creates a mismatch:
        - TOC says "Chapter 1 on page 8"
        - But actual Chapter 1 content is on physical page 22
        - Offset = 22 - 8 = 14
        
        Args:
            toc_entries: List of parsed TOC entries
            pages: List of all page dicts
            
        Returns:
            Integer offset to add to TOC page numbers
            
        Algorithm:
            1. Get first chapter's TOC page number
            2. Search for chapter title or "Chapter 1" content in pages
            3. Calculate difference between actual and TOC page numbers
        """
        if not toc_entries or not pages:
            return 0
        
        first_chapter = toc_entries[0]
        toc_page_num = first_chapter['toc_page_number']
        chapter_title = first_chapter['title']
        chapter_num = first_chapter['chapter_number']
        
        # Build page lookup for quick access
        page_lookup = {p.get('page_number'): p for p in pages}
        
        # First check if TOC page number is correct (offset = 0)
        if toc_page_num in page_lookup:
            page_content = page_lookup[toc_page_num].get('content', '')
            if self._is_chapter_content_page(page_content, chapter_title, chapter_num):
                return 0
        
        # Search for actual chapter content location
        actual_page = self._find_chapter_page(pages, chapter_title, chapter_num, toc_page_num)
        
        if actual_page is not None:
            return max(0, actual_page - toc_page_num)
        
        return 0
    
    def apply_offset(
        self, 
        toc_entries: List[Dict[str, Any]], 
        offset: int
    ) -> List[Dict[str, Any]]:
        """
        Apply calculated offset to TOC page numbers.
        
        Args:
            toc_entries: List of parsed TOC entries
            offset: Integer offset to add
            
        Returns:
            List of entries with 'actual_page_number' field added
        """
        result = []
        for entry in toc_entries:
            updated = entry.copy()
            updated['actual_page_number'] = entry['toc_page_number'] + offset
            result.append(updated)
        return result
    
    def _validate_with_yake(
        self, 
        chapters: List[Tuple], 
        pages: List[Dict]
    ) -> List[Tuple]:
        """
        Validate chapters have real content using YAKE keyword extraction.
        
        Args:
            chapters: List of (chapter_num, title, start_page, end_page) tuples
            pages: List of page dicts
            
        Returns:
            Filtered list of chapters with valid content
        """
        if not self.yake_extractor:
            return chapters
        
        page_lookup = {p.get('page_number'): p.get('content', '') for p in pages}
        validated = []
        
        for chapter_num, title, start_page, end_page in chapters:
            content = page_lookup.get(start_page, '')
            
            # Skip very short content
            if len(content) < 100:
                continue
            
            try:
                keywords = self.yake_extractor.extract_keywords(content[:2000], top_n=self.min_keywords + 3)
                if len(keywords) >= self.min_keywords:
                    validated.append((chapter_num, title, start_page, end_page))
            except Exception:
                # If extraction fails, skip this chapter
                continue
        
        return validated
    
    def detect(self, pages: List[Dict], **kwargs) -> List[Tuple]:
        """
        Detect chapters by parsing the Table of Contents.
        
        Args:
            pages: List of page dicts with {page_number, content}
            **kwargs: Optional parameters
            
        Returns:
            List of (chapter_num, title, start_page, end_page) tuples
            
        Algorithm:
            1. Find all TOC pages (may span multiple pages)
            2. Combine TOC content and parse chapter entries
            3. Calculate page offset
            4. Apply offset and calculate end pages
            5. Optionally validate with YAKE
        """
        if not pages:
            return []
        
        # Step 1: Find all TOC pages (TOC may span multiple pages)
        toc_pages = self.find_toc_pages(pages)
        if not toc_pages:
            return []
        
        # Step 2: Combine all TOC content and parse chapter entries
        toc_content = '\n'.join(p.get('content', '') for p in toc_pages)
        entries = self.parse_toc_entries(toc_content)
        
        if not entries:
            return []
        
        # Step 3: Calculate offset
        offset = self.calculate_page_offset(entries, pages)
        
        # Step 4: Apply offset
        entries_with_offset = self.apply_offset(entries, offset)
        
        # Step 5: Convert to chapter tuples with end pages
        chapters = []
        max_page = max(p.get('page_number', 0) for p in pages) if pages else 0
        
        for i, entry in enumerate(entries_with_offset):
            chapter_num = entry['chapter_number']
            title = entry['title']
            start_page = entry['actual_page_number']
            
            # Calculate end page (next chapter's start - 1, or last page)
            if i + 1 < len(entries_with_offset):
                end_page = entries_with_offset[i + 1]['actual_page_number'] - 1
            else:
                end_page = max_page
            
            chapters.append((chapter_num, title, start_page, end_page))
        
        # Step 6: Optionally validate with YAKE
        if self.yake_extractor:
            chapters = self._validate_with_yake(chapters, pages)
        
        return chapters
