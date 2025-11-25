"""
Chapter Segmentation Service Layer

Extracts segmentation logic from ChapterSegmenter into service classes.
Reduces complexity by applying Strategy Pattern and Single Responsibility Principle.

Architecture Patterns:
- Service Layer (Architecture Patterns Ch. 4): Orchestration logic
- Strategy Pattern (Architecture Patterns Ch. 13): Pass A/B/C strategies
- Extract Method (Python Distilled Ch. 16): Decompose complex functions

References:
- CONSOLIDATED_IMPLEMENTATION_PLAN.md: Tab 1 statistical methods
- ARCHITECTURE_GUIDELINES Ch. 4: Service Layer pattern
- PYTHON_GUIDELINES Ch. 7: Class design, single responsibility
"""

import re
from typing import List, Dict, Optional, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from workflows.pdf_to_json.scripts.chapter_models import Chapter
from workflows.metadata_extraction.scripts.adapters.statistical_extractor import StatisticalExtractor


# ============================================================================
# Validation Services
# ============================================================================

class SegmentationValidator:
    """
    Validates chapter segmentation quality.
    
    Pattern: Strategy Pattern - validation rules as separate methods
    Reference: Architecture Patterns Ch. 13
    """
    
    def __init__(self, config):
        """
        Initialize validator with configuration.
        
        Args:
            config: ChapterSegmentationConfig instance
        """
        self.config = config
    
    def validate(self, chapters: List[Chapter], num_pages: int) -> bool:
        """
        Validate segmentation meets quality criteria.
        
        Refactored from CC 14 → <10 by extracting validation checks.
        
        Args:
            chapters: List of detected chapters
            num_pages: Total number of pages in book
        
        Returns:
            True if valid, False otherwise
        """
        if not chapters:
            return False
        
        # Check 1: Chapter count in range
        if not self._validate_chapter_count(chapters, num_pages):
            return False
        
        # Check 2: Chapters-to-pages ratio
        if not self._validate_chapters_to_pages_ratio(chapters, num_pages):
            return False
        
        # Check 3: Chapter ordering and boundaries
        if not self._validate_chapter_ordering(chapters):
            return False
        
        # Check 4: No overlaps or large gaps
        if not self._validate_chapter_spacing(chapters):
            return False
        
        # Check 5: Minimum chapter sizes
        if not self._validate_chapter_sizes(chapters):
            return False
        
        return True
    
    def _validate_chapter_count(self, chapters: List[Chapter], num_pages: int) -> bool:
        """Check chapter count is in acceptable range"""
        min_chapters = min(self.config.min_chapters, max(1, num_pages // 20))
        if len(chapters) < min_chapters:
            return False
        
        if len(chapters) > self.config.max_chapters:
            return False
        
        return True
    
    def _validate_chapters_to_pages_ratio(self, chapters: List[Chapter], num_pages: int) -> bool:
        """Check reasonable chapters-to-pages ratio (avoid micro-chapters)"""
        if num_pages >= 50:  # Only enforce for larger books
            avg_pages_per_chapter = num_pages / len(chapters)
            if avg_pages_per_chapter < 6:
                return False
        return True
    
    def _validate_chapter_ordering(self, chapters: List[Chapter]) -> bool:
        """Check chapters are sorted and start reasonably"""
        chapters_sorted = sorted(chapters, key=lambda ch: ch.start_page)
        
        # First chapter should start within first 10 pages
        if chapters_sorted[0].start_page < 1 or chapters_sorted[0].start_page > 10:
            return False
        
        return True
    
    def _validate_chapter_spacing(self, chapters: List[Chapter]) -> bool:
        """Check no overlaps or large gaps between chapters"""
        chapters_sorted = sorted(chapters, key=lambda ch: ch.start_page)
        
        for i in range(len(chapters_sorted) - 1):
            gap = chapters_sorted[i+1].start_page - chapters_sorted[i].end_page - 1
            
            if gap < 0:
                # Overlap
                return False
            
            if gap > 5:
                # Large gap - suspicious
                return False
        
        return True
    
    def _validate_chapter_sizes(self, chapters: List[Chapter]) -> bool:
        """Check minimum chapter sizes (relaxed for last chapter)"""
        chapters_sorted = sorted(chapters, key=lambda ch: ch.start_page)
        min_size = max(2, self.config.min_pages // 2)
        
        for i, chapter in enumerate(chapters_sorted):
            chapter_length = chapter.end_page - chapter.start_page + 1
            
            # Last chapter can be just 1 page (conclusion, epilogue)
            is_last = (i == len(chapters_sorted) - 1)
            effective_min = 1 if is_last else min_size
            
            if chapter_length < effective_min:
                return False
        
        return True


# ============================================================================
# Boundary Scoring Service
# ============================================================================

class BoundaryScorer:
    """
    Scores potential chapter boundaries.
    
    Pattern: Single Responsibility - scoring only
    Reference: PYTHON_GUIDELINES Ch. 7
    """
    
    @staticmethod
    def score(page_idx: int, page_texts: List[str], similarities: List[float]) -> float:
        """
        Score a page as potential chapter boundary.
        
        Higher score = better boundary candidate.
        
        Args:
            page_idx: Index of page to score
            page_texts: List of all page texts
            similarities: List of cosine similarities between adjacent pages
        
        Returns:
            Boundary score (higher = better split point)
        """
        score = 0.0
        
        # Factor 1: Topic shift signal
        score += BoundaryScorer._topic_shift_score(page_idx, similarities)
        
        # Factor 2: Heading detection
        score += BoundaryScorer._heading_score(page_idx, page_texts)
        
        return score
    
    @staticmethod
    def _topic_shift_score(page_idx: int, similarities: List[float]) -> float:
        """Score based on topic shift (low similarity)"""
        if 0 < page_idx < len(similarities):
            return 1.0 - similarities[page_idx - 1]
        return 0.0
    
    @staticmethod
    def _heading_score(page_idx: int, page_texts: List[str]) -> float:
        """Score based on heading-like text"""
        if page_idx >= len(page_texts):
            return 0.0
        
        text = page_texts[page_idx]
        score = 0.0
        
        # All-caps lines (heading signal)
        for line in text.split('\n')[:10]:
            line = line.strip()
            if line.isupper() and len(line) > 10:
                score += 0.3
                break
        
        # Starts with chapter/section keywords
        if any(text.startswith(word) for word in ["Chapter ", "Item ", "Section ", "Part "]):
            score += 0.4
        
        return score


# ============================================================================
# TF-IDF Analysis Service
# ============================================================================

class TFIDFAnalyzer:
    """
    TF-IDF-based text analysis for topic detection.
    
    Pattern: Adapter Pattern (Architecture Patterns Ch. 4) - wraps sklearn
    """
    
    def __init__(self, max_features: int = 1000):
        """
        Initialize TF-IDF analyzer.
        
        Args:
            max_features: Maximum number of TF-IDF features
        """
        self.max_features = max_features
    
    def compute_similarities(self, page_texts: List[str]) -> Optional[List[float]]:
        """
        Compute cosine similarities between adjacent pages.
        
        Args:
            page_texts: List of page text content
        
        Returns:
            List of similarities or None if TF-IDF fails
        """
        try:
            vectorizer = TfidfVectorizer(
                max_features=self.max_features,
                stop_words='english'
            )
            tfidf_matrix = vectorizer.fit_transform(page_texts)
        except Exception:
            return None
        
        # Compute pairwise similarities
        similarities = []
        for i in range(len(page_texts) - 1):
            sim = cosine_similarity(tfidf_matrix[i:i+1], tfidf_matrix[i+1:i+2])[0,0]
            similarities.append(sim)
        
        return similarities


# ============================================================================
# Regex Pattern Matching Service
# ============================================================================

class RegexMatcher:
    """
    Regex-based chapter marker detection.
    
    Pattern: Strategy Pattern - multiple regex patterns
    """
    
    def __init__(self):
        """Initialize regex patterns"""
        self.patterns = [
            (re.compile(r'(?:Chapter|CHAPTER)\s+(\d+)[\s\.:]+([^\n]+)', re.MULTILINE), "chapter"),
            (re.compile(r'^\s*Item\s+(\d+)\s*[:.-]\s+(.+)$', re.MULTILINE), "item"),
            (re.compile(r'^(\d+)\s+([A-Z][A-Z\s]{10,})', re.MULTILINE), "numeric"),
        ]
    
    def find_chapter_marker(self, text: str) -> Optional[Tuple[int, str, str]]:
        """
        Find chapter marker in text using regex patterns.
        
        Args:
            text: Page text to search
        
        Returns:
            Tuple of (chapter_num, title, pattern_type) or None if not found
        """
        for pattern, pattern_type in self.patterns:
            match = pattern.search(text)
            if match:
                try:
                    chapter_num = int(match.group(1))
                    title = match.group(2).strip().rstrip('.')
                    return (chapter_num, title, pattern_type)
                except (ValueError, IndexError):
                    continue
        
        return None


# ============================================================================
# Page Filtering Service
# ============================================================================

class PageFilter:
    """
    Filters pages based on content characteristics.
    
    Pattern: Single Responsibility - filtering logic only
    """
    
    @staticmethod
    def is_too_short(text: str, min_length: int = 300) -> bool:
        """Check if page text is too short"""
        return len(text.strip()) < min_length
    
    @staticmethod
    def is_toc_page(text: str, max_isolated_numbers: int = 8) -> bool:
        """Check if page looks like table of contents"""
        first_text = '\n'.join(text.split('\n')[:25])
        isolated_nums = len(re.findall(r'(?:^|\s)(\d{1,3})(?:\s|$)', first_text))
        return isolated_nums > max_isolated_numbers
    
    @staticmethod
    def has_substantial_content(text: str, min_length: int = 800) -> bool:
        """Check if page has substantial content"""
        return len(text) >= min_length


# ============================================================================
# YAKE Keyword Validator
# ============================================================================

class YAKEValidator:
    """
    Validates pages have real content using YAKE keyword extraction.
    
    Pattern: Adapter Pattern - wraps StatisticalExtractor
    """
    
    def __init__(self, extractor: StatisticalExtractor, min_keywords: int = 3):
        """
        Initialize YAKE validator.
        
        Args:
            extractor: StatisticalExtractor instance
            min_keywords: Minimum number of keywords required
        """
        self.extractor = extractor
        self.min_keywords = min_keywords
    
    def validate(self, text: str) -> bool:
        """
        Validate page has sufficient keyword diversity.
        
        Args:
            text: Page text to validate
        
        Returns:
            True if valid (has enough keywords), False otherwise
        """
        keywords = self.extractor.extract_keywords(text[:2000], top_n=5)
        return len(keywords) >= self.min_keywords


# ============================================================================
# Chapter Builder Service
# ============================================================================

class ChapterBuilder:
    """
    Builds Chapter objects from detection data.
    
    Pattern: Builder Pattern - constructs complex objects
    Reference: ARCHITECTURE_GUIDELINES Ch. 3
    """
    
    @staticmethod
    def build_from_regex(candidates: List[Tuple], page_numbers: List[int]) -> List[Chapter]:
        """
        Build chapters from regex detection candidates.
        
        Args:
            candidates: List of (start_page, ch_num, title, pattern_type) tuples
            page_numbers: List of all page numbers
        
        Returns:
            List of Chapter objects
        """
        # Sort by page number
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
    
    @staticmethod
    def build_from_boundaries(boundaries: List[int], page_numbers: List[int], method: str) -> List[Chapter]:
        """
        Build chapters from boundary detection.
        
        Args:
            boundaries: List of chapter start pages
            page_numbers: List of all page numbers
            method: Detection method name
        
        Returns:
            List of Chapter objects
        """
        chapters = []
        for i in range(len(boundaries)):
            start_page = boundaries[i]
            end_page = boundaries[i+1] - 1 if i+1 < len(boundaries) else page_numbers[-1]
            
            chapters.append(Chapter(
                number=i+1,
                title=f"Segment {i+1} (pages {start_page}-{end_page})",
                start_page=start_page,
                end_page=end_page,
                detection_method=method
            ))
        
        return chapters


# ============================================================================
# Synthetic Segmentation Calculator
# ============================================================================

class SyntheticSegmentationCalculator:
    """
    Calculates synthetic segmentation parameters.
    
    Pattern: Single Responsibility - calculation logic only
    """
    
    @staticmethod
    def calculate_target_chapters(num_pages: int, config) -> int:
        """
        Calculate target number of chapters for synthetic segmentation.
        
        Args:
            num_pages: Total number of pages
            config: ChapterSegmentationConfig instance
        
        Returns:
            Target number of chapters
        """
        raw_target = num_pages // config.target_pages
        target_chapters = max(config.min_chapters, raw_target if raw_target > 0 else 1)
        return min(target_chapters, config.max_chapters)
    
    @staticmethod
    def calculate_target_pages_per_chapter(num_pages: int, target_chapters: int, min_pages: int) -> int:
        """
        Calculate target pages per chapter.
        
        Args:
            num_pages: Total number of pages
            target_chapters: Target number of chapters
            min_pages: Minimum pages per chapter
        
        Returns:
            Target pages per chapter
        """
        return max(min_pages, num_pages // target_chapters)
