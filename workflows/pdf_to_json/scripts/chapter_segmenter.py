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

from typing import List, Dict, Optional, Tuple
import sys
from pathlib import Path

# Add project root for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Config and statistical extractor
from config.settings import ChapterSegmentationConfig  # noqa: E402
from workflows.metadata_extraction.scripts.adapters.statistical_extractor import StatisticalExtractor  # noqa: E402

# Data models
from workflows.pdf_to_json.scripts.chapter_models import Chapter  # noqa: E402

# Service layer imports (refactored for reduced complexity)
from workflows.pdf_to_json.scripts.chapter_segmentation_services import (  # noqa: E402
    SegmentationValidator,
    BoundaryScorer,
    TFIDFAnalyzer,
    RegexMatcher,
    PageFilter,
    YAKEValidator,
    ChapterBuilder,
    SyntheticSegmentationCalculator,
)


# Constants - Per PYTHON_GUIDELINES: Class constants for validation messages
_ERROR_EMPTY_PAGES = "Pages list cannot be empty"
_ERROR_INVALID_CONFIG = "Invalid chapter segmentation configuration"


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
        
        # Initialize service layer components (refactored for reduced complexity)
        self.validator = SegmentationValidator(config)
        self.regex_matcher = RegexMatcher()
        self.yake_validator = YAKEValidator(self.extractor, config.min_keywords)
        self.tfidf_analyzer = TFIDFAnalyzer(config.tfidf_max_features)
    
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
            return []
        
        # Preprocess pages
        page_texts = [p.get("content", "") for p in pages]
        page_numbers = [p.get("page_number", i+1) for i, p in enumerate(pages)]
        
        # Execute 3-pass algorithm
        chapters = self._execute_segmentation_passes(pages, page_texts, page_numbers)
        return [ch.to_dict() for ch in chapters]
    
    def _execute_segmentation_passes(self, pages: List[Dict], page_texts: List[str], 
                                     page_numbers: List[int]) -> List[Chapter]:
        """
        Execute 3-pass segmentation algorithm with validation.
        
        Returns:
            List of Chapter objects (guaranteed non-empty via Pass C fallback)
        """
        num_pages = len(pages)
        
        # Pass A: Regex detection
        chapters = self._pass_a_regex(pages, page_texts, page_numbers)
        if chapters and self._validate_segmentation(chapters, num_pages):
            return chapters
        
        # Pass B: Topic-shift detection
        chapters = self._pass_b_topic_shift(page_texts, page_numbers)
        if chapters and self._validate_segmentation(chapters, num_pages):
            return chapters
        
        # Pass C: Synthetic fallback (always succeeds)
        return self._pass_c_synthetic(pages, page_texts, page_numbers)
    
    def _pass_a_regex(self, pages: List[Dict], page_texts: List[str], page_numbers: List[int]) -> Optional[List[Chapter]]:
        """
        Pass A: Regex-based chapter detection with YAKE validation.
        
        Refactored: CC 12 → <10 using service layer.
        
        Enhanced: Two-phase detection:
        1. First collect all dedicated chapter title pages (authoritative)
        2. Then collect regex chapters that don't conflict with title pages
        
        This ensures title pages take precedence over chapter references.
        
        Returns:
            List of chapters or None if detection failed
        """
        title_page_candidates = []
        regex_candidates = []
        title_page_numbers = set()  # Chapter numbers found on title pages
        
        # Phase 1: Collect all title page chapters (these are authoritative)
        for i, (page, text, page_num) in enumerate(zip(pages, page_texts, page_numbers)):
            if PageFilter.is_too_short(text, min_length=100):
                continue
            
            first_text = '\n'.join(text.split('\n')[:25])
            if PageFilter.is_toc_page(first_text):
                continue
            
            title_page_match = self.regex_matcher.is_chapter_title_page(text)
            if title_page_match:
                chapter_num, title = title_page_match
                if chapter_num not in title_page_numbers:
                    title_page_numbers.add(chapter_num)
                    title_page_candidates.append((page_num, chapter_num, title, "chapter_title"))
        
        # If we found title page chapters, use only those (they're the real chapters)
        if title_page_candidates:
            return ChapterBuilder.build_from_regex(title_page_candidates, page_numbers)
        
        # Phase 2: No title pages found - fall back to general regex detection
        seen_numbers = set()
        for i, (page, text, page_num) in enumerate(zip(pages, page_texts, page_numbers)):
            if PageFilter.is_too_short(text, min_length=100):
                continue
            
            first_text = '\n'.join(text.split('\n')[:25])
            if PageFilter.is_toc_page(first_text):
                continue
            
            marker = self.regex_matcher.find_chapter_marker(first_text)
            if not marker:
                continue
            
            chapter_num, title, pattern_type = marker
            
            # Require substantial content and YAKE validation for regex chapters
            if not PageFilter.has_substantial_content(text):
                continue
            
            if not self.yake_validator.validate(text):
                continue
            
            if chapter_num in seen_numbers:
                continue
            
            seen_numbers.add(chapter_num)
            regex_candidates.append((page_num, chapter_num, title, pattern_type))
        
        if not regex_candidates:
            return None
        
        return ChapterBuilder.build_from_regex(regex_candidates, page_numbers)
    
    def _pass_b_topic_shift(self, page_texts: List[str], page_numbers: List[int]) -> Optional[List[Chapter]]:
        """
        Pass B: TF-IDF-based topic boundary detection.
        
        Refactored: Using TFIDFAnalyzer service.
        
        Returns:
            List of chapters or None if detection failed
        """
        # Compute similarities using service
        similarities = self.tfidf_analyzer.compute_similarities(page_texts)
        if similarities is None:
            return None
        
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
        
        if not boundaries or len(boundaries) < 2:
            return None
        
        # Build chapters from boundaries
        return ChapterBuilder.build_from_boundaries(boundaries, page_numbers, "topic_boundary")
    
    def _pass_c_synthetic(self, pages: List[Dict], page_texts: List[str], page_numbers: List[int]) -> List[Chapter]:
        """
        Pass C: Synthetic segmentation with size + heading signals.
        
        GUARANTEED to return non-empty chapters.
        Refactored: Using service layer for calculations.
        
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
        
        # Compute similarities for boundary scoring (best effort)
        similarities = self.tfidf_analyzer.compute_similarities(page_texts)
        if similarities is None:
            # Fallback: use dummy similarities
            similarities = [0.5] * (num_pages - 1)
        
        # Calculate segmentation parameters
        target_chapters = SyntheticSegmentationCalculator.calculate_target_chapters(num_pages, self.config)
        actual_target_pages = SyntheticSegmentationCalculator.calculate_target_pages_per_chapter(
            num_pages, target_chapters, self.config.min_pages
        )
        
        # Greedy segmentation with boundary scoring
        segments = self._greedy_segmentation(
            num_pages, actual_target_pages, page_texts, similarities
        )
        
        # Convert to Chapter objects
        return self._segments_to_chapters(segments, page_numbers)
    
    def _greedy_segmentation(
        self, num_pages: int, target_pages: int, page_texts: List[str], similarities: List[float]
    ) -> List[Tuple[int, int]]:
        """Helper: Greedy segmentation with boundary scoring"""
        segments = []
        current_start_idx = 0
        
        while current_start_idx < num_pages:
            # Target end for this chapter
            rough_end_idx = min(current_start_idx + target_pages, num_pages)
            
            # Search window for best boundary
            window_start = max(current_start_idx + self.config.min_pages - 1, rough_end_idx - 3)
            window_end = min(num_pages, rough_end_idx + 3)
            
            best_end_idx = rough_end_idx
            best_score = -1.0
            
            for candidate_idx in range(window_start, window_end):
                score = BoundaryScorer.score(candidate_idx, page_texts, similarities)
                if score > best_score:
                    best_score = score
                    best_end_idx = candidate_idx
            
            # Add segment
            segments.append((current_start_idx, best_end_idx))
            current_start_idx = best_end_idx + 1
        
        return segments
    
    def _segments_to_chapters(self, segments: List[Tuple[int, int]], page_numbers: List[int]) -> List[Chapter]:
        """Helper: Convert segments to Chapter objects"""
        chapters = []
        num_pages = len(page_numbers)
        
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
        
        Refactored: Delegates to BoundaryScorer service (CC 8 → 1).
        
        Higher score = better boundary candidate.
        """
        return BoundaryScorer.score(page_idx, page_texts, similarities)
    
    def _validate_segmentation(self, chapters: List[Chapter], num_pages: int) -> bool:
        """
        Validate that segmentation is reasonable.
        
        Refactored: Delegates to SegmentationValidator service (CC 14 → 1).
        
        Returns:
            True if valid, False otherwise
        """
        return self.validator.validate(chapters, num_pages)
