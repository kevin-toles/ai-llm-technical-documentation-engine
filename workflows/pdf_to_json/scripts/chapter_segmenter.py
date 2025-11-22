"""
Statistical chapter segmentation using 3-pass detection algorithm.

Uses ONLY statistical NLP methods (no LLM calls):
- Pass A: Regex pattern matching with YAKE validation
- Pass B: TF-IDF topic-shift detection (cosine similarity)
- Pass C: Synthetic segmentation (guaranteed fallback)

Reference Documents:
    - CONSOLIDATED_IMPLEMENTATION_PLAN.md: Tab 1 statistical methods only
    - BOOK_TAXONOMY_MATRIX.md: Architecture Patterns (Adapter), Python Cookbook (algorithms)
    - docs/analysis/chapter_segmenter_conflict_assessment.md: Performance analysis

Document Cross-References:
    - Architecture Patterns with Python Ch. 4: Adapter pattern
    - Python Distilled Ch. 7: Class design, dataclasses
    - Fluent Python 2nd Ch. 6: Strategy pattern for pass selection
    - Python Cookbook 3rd Ch. 1: Data structures, algorithms
"""

import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import sys
from pathlib import Path

# Sklearn for TF-IDF and cosine similarity (Tab 4 already uses this)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Add project root for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Config and statistical extractor
from config.settings import ChapterSegmentationConfig
from workflows.metadata_extraction.scripts.adapters.statistical_extractor import StatisticalExtractor


# Constants - Per PYTHON_GUIDELINES: Class constants for validation messages
_ERROR_EMPTY_PAGES = "Pages list cannot be empty"
_ERROR_INVALID_CONFIG = "Invalid chapter segmentation configuration"


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


class ChapterSegmenter:
    """
    Statistical 3-pass chapter detection for PDF → JSON conversion.
    
    Implements fallback strategy:
    - Pass A (regex): Fast pattern matching with YAKE validation
    - Pass B (topic-shift): TF-IDF cosine similarity boundaries
    - Pass C (synthetic): Guaranteed size-based segmentation
    
    Per ARCHITECTURE_GUIDELINES Ch. 4: Adapter pattern for sklearn integration.
    Per PYTHON_GUIDELINES Ch. 7: Single responsibility - segmentation only.
    
    Example:
        >>> config = ChapterSegmentationConfig()
        >>> segmenter = ChapterSegmenter(config)
        >>> chapters = segmenter.segment_book(pages)
        >>> # chapters is NEVER empty (Pass C guarantees this)
    """
    
    def __init__(self, config: ChapterSegmentationConfig):
        """
        Initialize chapter segmenter with configuration.
        
        Args:
            config: Chapter segmentation configuration
        
        Raises:
            ValueError: If config is invalid
        """
        if config is None:
            raise ValueError(_ERROR_INVALID_CONFIG)
        
        self.config = config
        self.extractor = StatisticalExtractor()
        
        # Regex patterns for Pass A (conservative - only clear chapter markers)
        self.patterns = [
            (re.compile(r'(?:Chapter|CHAPTER)\s+(\d+)[\s\.:]+([^\n]+)', re.MULTILINE), "chapter"),
            (re.compile(r'^\s*Item\s+(\d+)\s*[:.-]\s+(.+)$', re.MULTILINE), "item"),
            (re.compile(r'^(\d+)\s+([A-Z][A-Z\s]{10,})', re.MULTILINE), "numeric"),
        ]
    
    def segment_book(self, pages: List[Dict]) -> List[Dict]:
        """
        Segment book into chapters using 3-pass algorithm.
        
        Args:
            pages: List of page dicts with {page_number, content}
        
        Returns:
            List of chapter dicts with {number, title, start_page, end_page, detection_method}
            GUARANTEED non-empty (Pass C fallback ensures this)
        
        Algorithm:
            1. Try Pass A (regex) → if valid, return
            2. Try Pass B (topic-shift) → if valid, return
            3. Use Pass C (synthetic) → always succeeds
        """
        if not pages:
            # Edge case: empty input returns empty list
            return []
        
        # Preprocessing: extract text and page numbers
        page_texts = [p.get("content", "") for p in pages]
        page_numbers = [p.get("page_number", i+1) for i, p in enumerate(pages)]
        num_pages = len(pages)
        
        # Try Pass A: Regex pattern matching
        chapters = self._pass_a_regex(pages, page_texts, page_numbers)
        if chapters and self._validate_segmentation(chapters, num_pages):
            return [ch.to_dict() for ch in chapters]
        
        # Try Pass B: Topic-shift detection
        chapters = self._pass_b_topic_shift(pages, page_texts, page_numbers)
        if chapters and self._validate_segmentation(chapters, num_pages):
            return [ch.to_dict() for ch in chapters]
        
        # Pass C: Synthetic segmentation (guaranteed fallback)
        chapters = self._pass_c_synthetic(pages, page_texts, page_numbers)
        return [ch.to_dict() for ch in chapters]
    
    def _pass_a_regex(self, pages: List[Dict], page_texts: List[str], page_numbers: List[int]) -> Optional[List[Chapter]]:
        """
        Pass A: Regex-based chapter detection with YAKE validation.
        
        Returns:
            List of chapters or None if detection failed
        """
        candidates = []
        seen_numbers = set()
        
        for i, (page, text, page_num) in enumerate(zip(pages, page_texts, page_numbers)):
            # Skip empty or very short pages
            if len(text.strip()) < 300:
                continue
            
            # Check first 25 lines for chapter markers
            lines = text.split('\n')[:25]
            first_text = '\n'.join(lines)
            
            # Skip TOC pages (many isolated numbers)
            isolated_nums = len(re.findall(r'(?:^|\s)(\d{1,3})(?:\s|$)', first_text))
            if isolated_nums > 8:
                continue
            
            # Try each pattern
            for pattern, pattern_type in self.patterns:
                match = pattern.search(first_text)
                if match:
                    chapter_num = int(match.group(1))
                    title = match.group(2).strip().rstrip('.')
                    
                    # Validate chapter has substantial content first (before checking duplicates)
                    if len(text) < 800:
                        continue
                    
                    # YAKE validation: real content, not TOC
                    keywords = self.extractor.extract_keywords(text[:2000], top_n=5)
                    if len(keywords) < self.config.min_keywords:
                        continue
                    
                    # Skip duplicates (keep first VALID occurrence)
                    if chapter_num in seen_numbers:
                        continue
                    
                    seen_numbers.add(chapter_num)
                    candidates.append((page_num, chapter_num, title, pattern_type))
                    break
        
        if not candidates:
            return None
        
        # Sort by page number and convert to Chapter objects
        candidates.sort(key=lambda x: x[0])
        
        chapters = []
        for i, (start_page, ch_num, title, pattern_type) in enumerate(candidates):
            end_page = candidates[i+1][0] - 1 if i+1 < len(candidates) else page_numbers[-1]
            
            chapters.append(Chapter(
                number=i+1,  # Sequential numbering
                title=title,
                start_page=start_page,
                end_page=end_page,
                detection_method=f"regex_{pattern_type}"
            ))
        
        return chapters
    
    def _pass_b_topic_shift(self, pages: List[Dict], page_texts: List[str], page_numbers: List[int]) -> Optional[List[Chapter]]:
        """
        Pass B: TF-IDF-based topic boundary detection.
        
        Returns:
            List of chapters or None if detection failed
        """
        num_pages = len(pages)
        
        # Compute TF-IDF matrix for all pages
        try:
            vectorizer = TfidfVectorizer(
                max_features=self.config.tfidf_max_features,
                stop_words='english'
            )
            tfidf_matrix = vectorizer.fit_transform(page_texts)
        except Exception:
            # TF-IDF failed (empty text, etc.)
            return None
        
        # Compute cosine similarity between adjacent pages
        similarities = []
        for i in range(num_pages - 1):
            sim = cosine_similarity(tfidf_matrix[i:i+1], tfidf_matrix[i+1:i+2])[0,0]
            similarities.append(sim)
        
        # Detect boundaries: low similarity = topic shift
        boundaries = [page_numbers[0]]  # Start with first page
        last_boundary_idx = 0
        
        for i, sim in enumerate(similarities):
            pages_since_last = i - last_boundary_idx + 1
            
            # Enforce minimum chapter length
            if pages_since_last < self.config.min_pages:
                continue
            
            # Topic shift detected
            if sim < self.config.similarity_threshold:
                boundaries.append(page_numbers[i+1])
                last_boundary_idx = i+1
        
        # Build chapters from boundaries
        chapters = []
        for i in range(len(boundaries)):
            start_page = boundaries[i]
            end_page = boundaries[i+1] - 1 if i+1 < len(boundaries) else page_numbers[-1]
            
            chapters.append(Chapter(
                number=i+1,
                title=f"Segment {i+1} (pages {start_page}-{end_page})",
                start_page=start_page,
                end_page=end_page,
                detection_method="topic_boundary"
            ))
        
        return chapters if chapters else None
    
    def _pass_c_synthetic(self, pages: List[Dict], page_texts: List[str], page_numbers: List[int]) -> List[Chapter]:
        """
        Pass C: Synthetic segmentation with size + heading signals.
        
        GUARANTEED to return non-empty chapters.
        
        Returns:
            List of chapters (never None, never empty)
        """
        num_pages = len(pages)
        
        # Special case: single page book
        if num_pages == 1:
            return [Chapter(
                number=1,
                title="Full Document",
                start_page=page_numbers[0],
                end_page=page_numbers[0],
                detection_method="synthetic"
            )]
        
        # Compute TF-IDF for heading detection (best effort)
        try:
            vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
            tfidf_matrix = vectorizer.fit_transform(page_texts)
            similarities = []
            for i in range(num_pages - 1):
                sim = cosine_similarity(tfidf_matrix[i:i+1], tfidf_matrix[i+1:i+2])[0,0]
                similarities.append(sim)
        except Exception:
            # TF-IDF failed, use dummy similarities
            similarities = [0.5] * (num_pages - 1)
        
        # Target number of chapters (ensure at least min_chapters)
        raw_target = num_pages // self.config.target_pages
        target_chapters = max(self.config.min_chapters, raw_target if raw_target > 0 else 1)
        target_chapters = min(target_chapters, self.config.max_chapters)
        
        # Greedy segmentation with boundary scoring
        segments = []
        current_start_idx = 0
        
        # Calculate actual target based on desired chapter count
        actual_target_pages = max(self.config.min_pages, num_pages // target_chapters)
        
        while current_start_idx < num_pages:
            # Target end for this chapter
            rough_end_idx = min(current_start_idx + actual_target_pages, num_pages)
            
            # Search window for best boundary
            window_start = max(current_start_idx + self.config.min_pages - 1, rough_end_idx - 3)
            window_end = min(num_pages, rough_end_idx + 3)
            
            best_end_idx = rough_end_idx
            best_score = -1.0
            
            for candidate_idx in range(window_start, window_end):
                score = self._boundary_score(candidate_idx, page_texts, similarities)
                if score > best_score:
                    best_score = score
                    best_end_idx = candidate_idx
            
            # Add segment
            segments.append((current_start_idx, best_end_idx))
            current_start_idx = best_end_idx + 1
        
        # Convert to Chapter objects
        chapters = []
        for i, (start_idx, end_idx) in enumerate(segments):
            start_page = page_numbers[start_idx]
            end_page = page_numbers[min(end_idx, num_pages - 1)]
            
            chapters.append(Chapter(
                number=i+1,
                title=f"Segment {i+1} (pages {start_page}-{end_page})",
                start_page=start_page,
                end_page=end_page,
                detection_method="synthetic"
            ))
        
        return chapters
    
    def _boundary_score(self, page_idx: int, page_texts: List[str], similarities: List[float]) -> float:
        """
        Score a page as potential chapter boundary.
        
        Higher score = better boundary candidate.
        """
        score = 0.0
        
        # Factor 1: Low similarity right before this page (topic shift)
        if 0 < page_idx < len(similarities):
            score += 1.0 - similarities[page_idx - 1]
        
        # Factor 2: Heading-like text on this page
        if page_idx < len(page_texts):
            text = page_texts[page_idx]
            
            # All-caps lines (heading signal)
            for line in text.split('\n')[:10]:
                line = line.strip()
                if line.isupper() and len(line) > 10:
                    score += 0.3
                    break
            
            # Starts with "Chapter", "Item", "Section", "Part"
            if any(text.startswith(word) for word in ["Chapter ", "Item ", "Section ", "Part "]):
                score += 0.4
        
        return score
    
    def _validate_segmentation(self, chapters: List[Chapter], num_pages: int) -> bool:
        """
        Validate that segmentation is reasonable.
        
        Returns:
            True if valid, False otherwise
        """
        if not chapters:
            return False
        
        # Check chapter count in range (allow fewer chapters for small books)
        min_chapters = min(self.config.min_chapters, max(1, num_pages // 20))
        if len(chapters) < min_chapters:
            return False
        
        if len(chapters) > self.config.max_chapters:
            return False
        
        # Additional check: reasonable chapters-to-pages ratio
        # Reject if creating micro-chapters (avg < 6 pages per chapter)
        # But allow for small books
        if num_pages >= 50:  # Only enforce for larger books
            avg_pages_per_chapter = num_pages / len(chapters)
            if avg_pages_per_chapter < 6:
                return False
        
        # Check chapters are sorted and reasonable
        chapters_sorted = sorted(chapters, key=lambda ch: ch.start_page)
        
        # Allow first chapter to start after page 1 (preface/TOC pages)
        if chapters_sorted[0].start_page < 1 or chapters_sorted[0].start_page > 10:
            return False
        
        # Check no major gaps between chapters (small gaps OK for skipped TOC)
        for i in range(len(chapters_sorted) - 1):
            gap = chapters_sorted[i+1].start_page - chapters_sorted[i].end_page - 1
            if gap < 0:
                # Overlap
                return False
            if gap > 5:
                # Large gap - suspicious
                return False
        
        # Check minimum chapter size (relaxed for small books and last chapter)
        min_size = max(2, self.config.min_pages // 2)
        for i, chapter in enumerate(chapters_sorted):
            chapter_length = chapter.end_page - chapter.start_page + 1
            
            # Last chapter can be just 1 page (conclusion, epilogue, etc.)
            is_last = (i == len(chapters_sorted) - 1)
            effective_min = 1 if is_last else min_size
            
            if chapter_length < effective_min:
                return False
        
        return True
