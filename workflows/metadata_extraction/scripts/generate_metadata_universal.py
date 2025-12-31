#!/usr/bin/env python3
"""
Universal Metadata Generator for Any Textbook JSON

This script generates chapter metadata (keywords, concepts, summaries) from any
textbook JSON file. It works for both:
1. Books with known chapter structure (via chapter definitions)
2. New/unknown books (auto-detects chapters from page numbers or TOC)

Usage:
    # With explicit chapter definitions:
    python3 generate_metadata_universal.py --input "path/to/book.json" \
        --chapters "[(1, 'Chapter Title', 1, 50), (2, 'Next Chapter', 51, 100)]"
    
    # Auto-detect chapters (analyzes TOC or page breaks):
    python3 generate_metadata_universal.py --input "path/to/book.json" --auto-detect
    
    # Interactive mode:
    python3 generate_metadata_universal.py --input "path/to/book.json" --interactive
    
    # Use orchestrator service for extraction (AC-1.2):
    python3 generate_metadata_universal.py --input "path/to/book.json" --use-orchestrator

Output:
    - Saves to: data/metadata/{book_name}_metadata.json
    - Format: List of chapter objects with keywords, concepts, summary

Reference:
- Python Distilled Ch. 9 - pathlib.Path operations
- Python Distilled Ch. 7 - Dataclass configuration patterns
- Microservices Up and Running Ch. 7 - 12-Factor App configuration

AC Reference:
- AC-1.1: USE_ORCHESTRATOR_EXTRACTION env var → MetadataExtractionClient
- AC-1.2: --use-orchestrator CLI flag → MetadataExtractionClient (precedence)
- AC-5.1: Orchestrator mode uses MetadataExtractionClient
- AC-5.2: Local mode uses StatisticalExtractor
- AC-5.3: Fallback on error uses StatisticalExtractor
- AC-5.4: Strict mode (fallback=False) propagates exception
"""

from __future__ import annotations

import asyncio
import json
import argparse
import logging
from ast import literal_eval
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional, TYPE_CHECKING
from dataclasses import dataclass, asdict
import sys

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import StatisticalExtractor for domain-agnostic metadata extraction
# Per DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN Part 1.3
from workflows.metadata_extraction.scripts.adapters.statistical_extractor import StatisticalExtractor  # noqa: E402

# Import chapter detection strategies for Strategy Pattern (TDD Iteration 3)
# Reduces auto_detect_chapters() complexity from CC 18 to <10
from workflows.metadata_extraction.scripts.strategies.predefined_strategy import PreDefinedStrategy  # noqa: E402
from workflows.metadata_extraction.scripts.strategies.toc_parser_strategy import TOCParserStrategy  # noqa: E402
from workflows.metadata_extraction.scripts.strategies.regex_pattern_strategy import RegexPatternStrategy  # noqa: E402
from workflows.metadata_extraction.scripts.strategies.yake_validation_strategy import YAKEValidationStrategy  # noqa: E402
from workflows.metadata_extraction.scripts.strategies.toc_filter_strategy import TOCFilterStrategy  # noqa: E402
from workflows.metadata_extraction.scripts.strategies.duplicate_filter_strategy import DuplicateFilterStrategy  # noqa: E402

# Import orchestrator client and settings (AC-1.1, AC-1.2)
from workflows.shared.clients.metadata_client import (  # noqa: E402
    MetadataExtractionClient,
    MetadataExtractionOptions,
    MetadataExtractionResult,
    MetadataClientError,
    MetadataClientConnectionError,
    MetadataClientTimeoutError,
    BatchTextItem,
    BatchExtractionResult,
)
from config.extraction_settings import get_extraction_settings  # noqa: E402

# Try to use settings, fallback to defaults
try:
    from config.settings import settings  # noqa: E402
    DEFAULT_JSON_DIR = settings.paths.textbooks_json_dir
    DEFAULT_METADATA_DIR = settings.paths.metadata_dir
except ImportError:
    DEFAULT_JSON_DIR = Path("data/textbooks_json")
    DEFAULT_METADATA_DIR = Path("data/metadata")

# Configure logging by default
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Logger for this module
logger = logging.getLogger(__name__)


@dataclass
class ChapterMetadata:
    """Structured metadata for a single chapter."""
    chapter_number: int
    title: str
    start_page: int
    end_page: int
    summary: str
    keywords: List[str]
    concepts: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


class UniversalMetadataGenerator:
    """
    Universal metadata generator that works with any textbook JSON.
    
    Extracts keywords, concepts, and generates summaries from chapter content.
    Can auto-detect chapters or accept explicit chapter definitions.
    
    Configuration via dependency injection (ARCH 5336):
    - Keywords loaded from external config file
    - Patterns loaded from external config file
    
    Orchestrator Mode (AC-5.1 to AC-5.5):
    - use_orchestrator=True: Uses MetadataExtractionClient for extraction
    - use_orchestrator=False: Uses local StatisticalExtractor (default)
    - fallback_on_error=True: Falls back to local on orchestrator failure
    """
    
    def __init__(
        self, 
        json_path: Path, 
        domain: str = "auto",
        keywords_file: Optional[Path] = None,  # Deprecated - kept for backward compatibility
        patterns_file: Optional[Path] = None,  # Deprecated - kept for backward compatibility
        use_orchestrator: Optional[bool] = None,  # AC-5.1, AC-5.2: None = use env var
        fallback_on_error: bool = True,  # AC-5.3, AC-5.4: fallback behavior
        orchestrator_url: Optional[str] = None,  # Custom orchestrator URL
    ):
        """
        Initialize generator with JSON file.
        
        Args:
            json_path: Path to textbook JSON file
            domain: Domain of the book (ignored - now domain-agnostic via StatisticalExtractor)
            keywords_file: DEPRECATED - No longer used (statistical extraction is domain-agnostic)
            patterns_file: DEPRECATED - No longer used (statistical extraction is domain-agnostic)
            use_orchestrator: If True, use MetadataExtractionClient; if False, use local;
                             if None, read from ExtractionSettings (AC-1.1)
            fallback_on_error: If True, fall back to local on orchestrator error (AC-5.3);
                              if False, propagate exception (AC-5.4)
            orchestrator_url: Custom orchestrator service URL (default from settings)
            
        Raises:
            FileNotFoundError: If JSON file doesn't exist (EAFP - PY 21)
            
        Document References:
            - DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN: Part 1.3 (Integration)
            - ARCHITECTURE_GUIDELINES Ch. 4: Adapter pattern for external libraries
            - CME_ARCHITECTURE.md: AC-5.1 to AC-5.5 (Orchestrator integration)
        """
        self.json_path = Path(json_path)
        self.domain = domain
        
        # AC-5.1/AC-5.2: Determine extraction mode
        # If use_orchestrator is None, read from ExtractionSettings (AC-1.1)
        settings = get_extraction_settings()
        if use_orchestrator is None:
            self._use_orchestrator = settings.use_orchestrator_extraction
        else:
            self._use_orchestrator = use_orchestrator
        
        self._fallback_on_error = fallback_on_error
        self._orchestrator_url = orchestrator_url
        
        # No limits on keywords/concepts - extract ALL, filter downstream, dedupe
        # Limits removed per user requirement: "pull all available, filter through confirmed, dedupe"
        
        # Initialize StatisticalExtractor for domain-agnostic extraction
        # Used as primary (AC-5.2) or fallback (AC-5.3)
        # Per DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN Part 1.2
        self.extractor = StatisticalExtractor()
        
        # Deprecated configuration paths (kept for backward compatibility)
        if keywords_file or patterns_file:
            print("Warning: keywords_file and patterns_file are deprecated. Using StatisticalExtractor instead.")
        
        # Load JSON (using context manager - PY 32425)
        with open(self.json_path, 'r', encoding='utf-8') as f:
            self.book_data = json.load(f)
        
        self.pages = self.book_data.get('pages', [])
        self.book_name = self.json_path.stem
        
        # Log extraction mode
        mode = "orchestrator" if self._use_orchestrator else "local"
        logger.info(f"Initialized generator with {mode} extraction mode")
        
        # Initialize StatisticalExtractor for domain-agnostic keyword extraction
        # Per DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN Part 1.3
        self.extractor = StatisticalExtractor()

    # =========================================================================
    # Public Properties (AC-1.1, AC-1.2, AC-5.1-AC-5.4)
    # =========================================================================

    @property
    def use_orchestrator(self) -> bool:
        """
        Read-only access to orchestrator mode flag.
        
        AC Reference:
            - AC-1.1: Reflects env var value when not overridden
            - AC-1.2: Reflects CLI flag when specified
            - AC-5.1/AC-5.2: Used for extraction routing
        """
        return self._use_orchestrator

    @property
    def fallback_on_error(self) -> bool:
        """
        Read-only access to fallback mode flag.
        
        AC Reference:
            - AC-5.3: True enables fallback to StatisticalExtractor
            - AC-5.4: False propagates exceptions
        """
        return self._fallback_on_error
    
    def auto_detect_chapters(self) -> List[Tuple[int, str, int, int]]:
        """
        Auto-detect chapters using Strategy Pattern (CC: 18 → <10).
        
        Strategy Pipeline:
        1. PreDefinedStrategy - Extract from JSON metadata (highest priority)
        2. TOCParserStrategy - Parse Table of Contents (handles page offset issues)
        3. RegexPatternStrategy - Find "Chapter N:" markers (fallback)
        4. YAKEValidationStrategy - Validate content quality via keywords
        5. TOCFilterStrategy - Remove table-of-contents pages
        6. DuplicateFilterStrategy - Remove duplicate chapter numbers
        
        Returns:
            List of (chapter_num, title, start_page, end_page) tuples
            
        Reference:
            - Architecture Patterns Ch. 13 (Dependency Injection)
            - TDD Iteration 3: Strategy Pattern implementation
        """
        # Priority 1: Check for pre-defined chapters in JSON metadata
        predefined = PreDefinedStrategy(self.book_data)
        chapters = predefined.detect(self.pages)
        
        if chapters:
            print(f"   Using {len(chapters)} pre-defined chapters from JSON")
            return chapters
        
        # Priority 2: Parse Table of Contents (handles books with page offset issues)
        # This strategy is especially effective for books like "Python Microservices Development"
        # where TOC page numbers don't match physical page numbers
        print("   Attempting TOC parsing strategy...")
        toc_parser = TOCParserStrategy(yake_extractor=self.extractor, min_keywords=3)
        chapters = toc_parser.detect(self.pages)
        
        if chapters:
            print(f"   Found {len(chapters)} chapters via TOC parsing")
            return chapters
        
        # Priority 3: Scan pages for chapter markers using regex patterns
        print("   Scanning pages for chapter markers...")
        regex = RegexPatternStrategy()
        candidates = regex.detect(self.pages)
        
        if not candidates:
            return []
        
        # Apply filtering strategies to clean up candidates
        # Filter 1: Validate chapters have real content (not TOC entries)
        yake = YAKEValidationStrategy(self.extractor, min_keywords=3, min_content_length=100)
        validated = yake.validate(candidates, self.pages)
        
        # Filter 2: Remove table-of-contents pages (many isolated numbers)
        toc_filter = TOCFilterStrategy(threshold=8)
        filtered = toc_filter.filter(validated, self.pages)
        
        # Filter 3: Remove duplicate chapter numbers (headers/footers)
        dedup = DuplicateFilterStrategy()
        final_chapters = dedup.filter(filtered)
        
        return final_chapters
    
    def extract_keywords(self, text: str, chapter_title: str = "", chapter_num: int = 0) -> List[str]:
        """
        Extract ALL meaningful keywords from chapter text using statistical methods.
        
        Replaced hardcoded keyword matching with YAKE unsupervised extraction.
        Now works across ANY domain (Python, biology, law, construction, etc.).
        
        No limits applied - extracts all valid keywords for downstream filtering.
        
        Args:
            text: Chapter text content
            chapter_title: Optional chapter title for verbose logging
            chapter_num: Optional chapter number for verbose logging
            
        Returns:
            List of ALL keywords sorted by relevance (YAKE score)
            
        Document References:
            - DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN Part 1.3: Integration with StatisticalExtractor
            - ARCHITECTURE_GUIDELINES Ch. 4: Adapter pattern for NLP libraries
        """
        # Build source name for verbose logging
        source_name = ""
        if hasattr(self, 'book_name'):
            if chapter_title or chapter_num:
                source_name = f"{self.book_name} - Ch{chapter_num}: {chapter_title}"
            else:
                source_name = self.book_name
        
        keywords_with_scores = self.extractor.extract_keywords(text, source_name=source_name)
        return [keyword for keyword, score in keywords_with_scores]
    
    def extract_concepts(self, text: str, chapter_title: str = "", chapter_num: int = 0) -> List[str]:
        """
        Extract ALL key concepts and topics from chapter text using TextRank.
        
        Replaced 35+ hardcoded regex patterns with Summa statistical extraction.
        Now works across ANY domain without hardcoded domain knowledge.
        
        No limits applied - extracts all valid concepts for downstream filtering.
        
        Args:
            text: Chapter text content
            chapter_title: Optional chapter title for verbose logging
            chapter_num: Optional chapter number for verbose logging
            
        Returns:
            List of ALL concepts (single-word terms)
            
        Document References:
            - DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN Part 1.3: Remove hardcoded patterns
            - ARCHITECTURE_GUIDELINES Ch. 5: Service layer orchestration
        """
        # Build source name for verbose logging
        source_name = ""
        if hasattr(self, 'book_name'):
            if chapter_title or chapter_num:
                source_name = f"{self.book_name} - Ch{chapter_num}: {chapter_title}"
            else:
                source_name = self.book_name
        
        return self.extractor.extract_concepts(text, source_name=source_name)
    
    def generate_summary(self, text: str, title: str, chapter_num: int) -> str:
        """
        Generate an extractive summary for the chapter using Summa TextRank.
        
        Replaced basic heuristics (first 3 sentences) with Summa statistical summarization.
        Preserves context and works across ANY domain.
        
        Args:
            text: Chapter text content
            title: Chapter title
            chapter_num: Chapter number
            
        Returns:
            Generated summary string (20% of original text)
            
        Document References:
            - DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN Part 1.3: Replace summarization heuristics
            - PYTHON_GUIDELINES Ch. 8: Error handling with EAFP
        """
        try:
            summary = self.extractor.generate_summary(text, ratio=0.2)
            if summary:
                return summary
        except Exception as e:
            # Fallback for very short text or empty content that can't be summarized
            # Log the exception for debugging but continue with fallback
            import logging
            logging.debug(f"Summary extraction failed for chapter {chapter_num}: {e}")
        
        # Fallback: return chapter title
        return f"Chapter {chapter_num}: {title}"

    # =========================================================================
    # Orchestrator Integration (WBS-AC5)
    # =========================================================================

    def _create_metadata_client(self) -> MetadataExtractionClient:
        """
        Factory method to create MetadataExtractionClient.
        
        AC Reference:
            - AC-5.1: Client instantiation when use_orchestrator=True
        
        Returns:
            Configured MetadataExtractionClient instance
        """
        # Use configured URL or default from client
        if self._orchestrator_url:
            return MetadataExtractionClient(base_url=self._orchestrator_url)
        return MetadataExtractionClient()

    async def _extract_via_orchestrator_async(
        self,
        text: str,
        title: str,
        chapter_num: int,
    ) -> Tuple[List[str], List[str], str]:
        """
        Extract metadata via orchestrator service asynchronously.
        
        No limits on keywords/concepts - orchestrator extracts all, filters, and dedupes.
        
        AC Reference:
            - AC-5.1: Orchestrator mode extraction
            - AC-5.3: Fallback on error (when enabled)
            - AC-5.4: Exception propagation (when fallback disabled)
        
        Args:
            text: Chapter text content
            title: Chapter title
            chapter_num: Chapter number for logging
            
        Returns:
            Tuple of (keywords, concepts, summary)
            
        Raises:
            MetadataClientError: If extraction fails and fallback disabled
        """
        try:
            async with self._create_metadata_client() as client:
                options = MetadataExtractionOptions(
                    enable_summary=True,
                    summary_ratio=0.2,
                )
                result = await client.extract_metadata(text, title=title, options=options)
                
                # Map orchestrator response to standard format (AC-5.5)
                keywords = [kw.term for kw in result.keywords]
                concepts = [c.name for c in result.concepts]
                summary = result.summary or self.generate_summary(text, title, chapter_num)
                
                logger.info(
                    f"Orchestrator extraction for chapter {chapter_num}: "
                    f"{len(keywords)} keywords, {len(concepts)} concepts"
                )
                return keywords, concepts, summary
                
        except MetadataClientError as e:
            if self._fallback_on_error:
                # AC-5.3: Fallback to local extraction
                logger.warning(
                    f"Orchestrator failed for chapter {chapter_num}, "
                    f"falling back to local extraction: {e}"
                )
                return self._extract_local(text, title, chapter_num)
            else:
                # AC-5.4: Propagate exception
                raise

    def _extract_via_orchestrator(
        self,
        text: str,
        title: str,
        chapter_num: int,
    ) -> Tuple[List[str], List[str], str]:
        """
        Synchronous wrapper for orchestrator extraction.
        
        Handles asyncio event loop management for sync callers.
        No limits on keywords/concepts - extracts all.
        
        Args:
            text: Chapter text content
            title: Chapter title
            chapter_num: Chapter number
            
        Returns:
            Tuple of (keywords, concepts, summary)
        """
        return asyncio.run(
            self._extract_via_orchestrator_async(
                text, title, chapter_num
            )
        )

    async def _extract_batch_via_orchestrator_async(
        self,
        chapters_data: List[Dict[str, Any]],
    ) -> Dict[str, Tuple[List[str], List[str], str]]:
        """
        Extract metadata for all chapters in a single batch request.
        
        Optimized for large books - reduces HTTP overhead by sending all chapters
        in one request instead of one request per chapter.
        
        No limits on keywords/concepts - extracts all, filters, and dedupes.
        
        Args:
            chapters_data: List of dicts with 'id', 'text', 'title' for each chapter
            
        Returns:
            Dict mapping chapter_id to (keywords, concepts, summary) tuple
        """
        try:
            async with self._create_metadata_client() as client:
                # Build batch items
                items = [
                    BatchTextItem(
                        id=ch['id'],
                        text=ch['text'],
                        title=ch.get('title'),
                    )
                    for ch in chapters_data
                ]
                
                options = MetadataExtractionOptions(
                    enable_summary=True,
                    summary_ratio=0.2,
                )
                
                result = await client.extract_metadata_batch(
                    items=items,
                    book_title=self.book_name,
                    options=options,
                )
                
                logger.info(
                    f"Batch extraction: {result.successful}/{result.total_items} succeeded "
                    f"in {result.total_processing_time_ms:.1f}ms"
                )
                
                # Map results back to chapter IDs
                results_map = {}
                for item_result in result.results:
                    if item_result.success and item_result.result:
                        r = item_result.result
                        keywords = [kw.term for kw in r.keywords]
                        concepts = [c.name for c in r.concepts]
                        summary = r.summary or ""
                        results_map[item_result.id] = (keywords, concepts, summary)
                    else:
                        # Failed item - return empty results
                        logger.warning(f"Batch item {item_result.id} failed: {item_result.error}")
                        results_map[item_result.id] = ([], [], "")
                
                return results_map
                
        except MetadataClientError as e:
            if self._fallback_on_error:
                logger.warning(f"Batch extraction failed, falling back to per-chapter: {e}")
                raise  # Let caller handle fallback
            else:
                raise

    def _extract_batch_via_orchestrator(
        self,
        chapters_data: List[Dict[str, Any]],
    ) -> Dict[str, Tuple[List[str], List[str], str]]:
        """
        Synchronous wrapper for batch orchestrator extraction.
        """
        return asyncio.run(
            self._extract_batch_via_orchestrator_async(
                chapters_data
            )
        )

    def _extract_local(
        self,
        text: str,
        title: str,
        chapter_num: int,
    ) -> Tuple[List[str], List[str], str]:
        """
        Extract metadata using local StatisticalExtractor.
        
        No limits on keywords/concepts - extracts all valid terms.
        
        AC Reference:
            - AC-5.2: Local extraction when use_orchestrator=False
            - AC-5.3: Fallback target when orchestrator fails
        
        Args:
            text: Chapter text content
            title: Chapter title
            chapter_num: Chapter number
            
        Returns:
            Tuple of (keywords, concepts, summary)
        """
        keywords = self.extract_keywords(text, chapter_title=title, chapter_num=chapter_num)
        concepts = self.extract_concepts(text, chapter_title=title, chapter_num=chapter_num)
        summary = self.generate_summary(text, title, chapter_num)
        return keywords, concepts, summary

    def extract_chapter_metadata(
        self,
        text: str,
        title: str,
        chapter_num: int,
    ) -> Tuple[List[str], List[str], str]:
        """
        Extract metadata for a chapter using configured extraction mode.
        
        Routes to orchestrator or local extraction based on self._use_orchestrator.
        No limits on keywords/concepts - extracts all valid terms.
        
        AC Reference:
            - AC-5.1: Routes to orchestrator when use_orchestrator=True
            - AC-5.2: Routes to local when use_orchestrator=False
        
        Args:
            text: Chapter text content
            title: Chapter title
            chapter_num: Chapter number
            
        Returns:
            Tuple of (keywords, concepts, summary)
        """
        if self._use_orchestrator:
            return self._extract_via_orchestrator(
                text, title, chapter_num
            )
        else:
            return self._extract_local(
                text, title, chapter_num
            )
    
    def _validate_chapter_ranges(self, chapters: List[Tuple[int, str, int, int]]) -> None:
        """
        Validate that chapter page ranges don't overlap.
        
        Args:
            chapters: List of (chapter_num, title, start_page, end_page) tuples
            
        Raises:
            ValueError: If any chapters have overlapping page ranges
        """
        sorted_chapters = sorted(chapters, key=lambda c: c[2])  # Sort by start_page
        
        for i in range(len(sorted_chapters) - 1):
            curr_num, _, _, curr_end = sorted_chapters[i]
            next_num, _, next_start, _ = sorted_chapters[i + 1]
            
            # Check if current chapter's end overlaps with next chapter's start
            # Adjacent chapters are OK (curr_end = next_start - 1), overlapping is not
            if curr_end >= next_start:
                raise ValueError(
                    f"Chapters overlap: Chapter {curr_num} ends at page {curr_end}, "
                    f"but Chapter {next_num} starts at page {next_start}"
                )
    
    def _collect_chapter_text(self, start_page: int, end_page: int) -> Tuple[str, int]:
        """
        Collect text content from pages within a chapter range.
        
        Extracted to reduce cognitive complexity in generate_metadata().
        
        Args:
            start_page: Starting page number (inclusive)
            end_page: Ending page number (inclusive)
            
        Returns:
            Tuple of (chapter_text, pages_found_count)
        """
        chapter_text = ""
        pages_found = 0
        for page in self.pages:
            page_num = page.get('page_number', 0)
            if start_page <= page_num <= end_page:
                chapter_text += page.get('content', page.get('text', '')) + "\n"
                pages_found += 1
        return chapter_text, pages_found
    
    def _create_fallback_metadata(
        self,
        ch_num: int,
        title: str,
        start_page: int,
        end_page: int,
        error_suffix: str = ""
    ) -> ChapterMetadata:
        """
        Create minimal metadata for chapters with no text or extraction failures.
        
        Extracted to reduce cognitive complexity in generate_metadata().
        
        Args:
            ch_num: Chapter number
            title: Chapter title
            start_page: Starting page number
            end_page: Ending page number
            error_suffix: Optional suffix for summary (e.g., "(metadata extraction failed)")
            
        Returns:
            ChapterMetadata with fallback values
        """
        summary = f"Chapter {ch_num}: {title}"
        if error_suffix:
            summary = f"{summary} {error_suffix}"
        return ChapterMetadata(
            chapter_number=ch_num,
            title=title,
            start_page=start_page,
            end_page=end_page,
            summary=summary,
            keywords=[],
            concepts=[]
        )
    
    def generate_metadata(
        self,
        chapters: List[Tuple[int, str, int, int]]
    ) -> List[ChapterMetadata]:
        """
        Generate metadata for all chapters.
        
        When orchestrator mode is enabled, uses batch extraction to process
        all chapters in a single HTTP request for improved performance.
        
        Args:
            chapters: List of (chapter_num, title, start_page, end_page) tuples
            
        Returns:
            List of ChapterMetadata objects
            
        Raises:
            ValueError: If chapters have overlapping page ranges
        """
        # Validate chapters for overlaps (exception hierarchy - PY 32425)
        self._validate_chapter_ranges(chapters)
        
        total_chapters = len(chapters)
        
        # Phase 1: Collect all chapter texts
        print(f"\n📖 Collecting text from {total_chapters} chapters...")
        chapters_data = []
        chapter_info = {}  # Maps chapter_id to (ch_num, title, start_page, end_page)
        
        MAX_CHAPTER_TEXT = 100000  # 100K chars (~50-60 pages of text)
        
        for idx, (ch_num, title, start_page, end_page) in enumerate(chapters, start=1):
            chapter_id = f"ch_{ch_num}"
            chapter_info[chapter_id] = (ch_num, title, start_page, end_page)
            
            # Collect text from chapter pages
            chapter_text, pages_found = self._collect_chapter_text(start_page, end_page)
            
            # Truncate large chapters
            if len(chapter_text) > MAX_CHAPTER_TEXT:
                chapter_text = chapter_text[:MAX_CHAPTER_TEXT]
            
            _page_count = pages_found if pages_found > 0 else (end_page - start_page + 1)
            
            if chapter_text and chapter_text.strip():
                chapters_data.append({
                    'id': chapter_id,
                    'text': chapter_text,
                    'title': title,
                    'ch_num': ch_num,
                    'start_page': start_page,
                    'end_page': end_page,
                })
                print(f"  [{idx}/{total_chapters}] Chapter {ch_num}: {len(chapter_text):,} chars")
            else:
                print(f"  [{idx}/{total_chapters}] Chapter {ch_num}: (no text content)")
        
        print(f"\n✅ Collected {len(chapters_data)} chapters with text content")
        
        # Phase 2: Extract metadata (batch or per-chapter)
        metadata_list = []
        
        if self._use_orchestrator and chapters_data:
            # Try batch extraction first
            print(f"\n🚀 Using BATCH orchestrator extraction for {len(chapters_data)} chapters...")
            try:
                batch_results = self._extract_batch_via_orchestrator(
                    chapters_data
                )
                
                # Build metadata from batch results
                for ch_data in chapters_data:
                    chapter_id = ch_data['id']
                    ch_num, title, start_page, end_page = chapter_info[chapter_id]
                    
                    if chapter_id in batch_results:
                        keywords, concepts, summary = batch_results[chapter_id]
                        print(f"  ✓ Chapter {ch_num}: {len(keywords)} keywords, {len(concepts)} concepts")
                    else:
                        keywords, concepts, summary = [], [], ""
                        print(f"  ⚠ Chapter {ch_num}: no results")
                    
                    # Generate summary if not provided
                    if not summary:
                        summary = self.generate_summary(ch_data['text'], title, ch_num)
                    
                    metadata_list.append(ChapterMetadata(
                        chapter_number=ch_num,
                        title=title,
                        start_page=start_page,
                        end_page=end_page,
                        summary=summary,
                        keywords=keywords,
                        concepts=concepts,
                    ))
                
                # Calculate unique totals across all chapters
                all_keywords = set()
                all_concepts = set()
                for m in metadata_list:
                    all_keywords.update(m.keywords)
                    all_concepts.update(m.concepts)
                
                print(f"\n✅ Batch extraction complete: {len(metadata_list)} chapters processed")
                print(f"📊 Book totals (unique): {len(all_keywords):,} keywords | {len(all_concepts):,} concepts")
                
                # Log book-level summary for analysis
                logger.info(
                    f"Book extraction complete: book='{self.book_name}' "
                    f"chapters={len(metadata_list)} "
                    f"unique_keywords={len(all_keywords)} "
                    f"unique_concepts={len(all_concepts)} "
                    f"mode=batch"
                )
                
            except Exception as e:
                print(f"\n⚠️ Batch extraction failed: {e}")
                print("   Falling back to per-chapter extraction...")
                metadata_list = self._generate_metadata_per_chapter(chapters_data, chapter_info)
        else:
            # Per-chapter extraction (local or orchestrator per-chapter)
            mode = "orchestrator" if self._use_orchestrator else "local"
            print(f"\n🔄 Using per-chapter {mode} extraction...")
            metadata_list = self._generate_metadata_per_chapter(chapters_data, chapter_info)
        
        # Add fallback entries for chapters without text
        for ch_num, title, start_page, end_page in chapters:
            chapter_id = f"ch_{ch_num}"
            if chapter_id not in [f"ch_{m.chapter_number}" for m in metadata_list]:
                metadata_list.append(self._create_fallback_metadata(
                    ch_num, title, start_page, end_page
                ))
        
        # Sort by chapter number
        metadata_list.sort(key=lambda m: m.chapter_number)
        
        return metadata_list
    
    def _generate_metadata_per_chapter(
        self,
        chapters_data: List[Dict[str, Any]],
        chapter_info: Dict[str, Tuple[int, str, int, int]],
    ) -> List[ChapterMetadata]:
        """
        Generate metadata chapter-by-chapter (fallback when batch fails).
        
        Args:
            chapters_data: List of chapter data dicts
            chapter_info: Map of chapter_id to (ch_num, title, start_page, end_page)
            
        Returns:
            List of ChapterMetadata objects
        """
        metadata_list = []
        total = len(chapters_data)
        
        for idx, ch_data in enumerate(chapters_data, start=1):
            chapter_id = ch_data['id']
            ch_num, title, start_page, end_page = chapter_info[chapter_id]
            chapter_text = ch_data['text']
            
            progress_pct = (idx / total) * 100
            print(f"\n[{progress_pct:.1f}%] Processing Chapter {ch_num}: {title}")
            
            try:
                keywords, concepts, summary = self.extract_chapter_metadata(
                    chapter_text, title, ch_num
                )
                
                print(f"  Keywords: {', '.join(keywords[:5])}..." if keywords else "  Keywords: (none)")
                print(f"  Concepts: {', '.join(concepts[:5])}..." if concepts else "  Concepts: (none)")
                
                metadata_list.append(ChapterMetadata(
                    chapter_number=ch_num,
                    title=title,
                    start_page=start_page,
                    end_page=end_page,
                    summary=summary,
                    keywords=keywords,
                    concepts=concepts,
                ))
                
            except Exception as e:
                print(f"  ❌ Error: {e}")
                metadata_list.append(self._create_fallback_metadata(
                    ch_num, title, start_page, end_page,
                    error_suffix="(metadata extraction failed)"
                ))
        
        # Calculate unique totals across all chapters
        all_keywords = set()
        all_concepts = set()
        for m in metadata_list:
            all_keywords.update(m.keywords)
            all_concepts.update(m.concepts)
        
        print(f"\n✅ Per-chapter extraction complete: {len(metadata_list)} chapters processed")
        print(f"📊 Book totals (unique): {len(all_keywords):,} keywords | {len(all_concepts):,} concepts")
        
        # Log book-level summary for analysis
        logger.info(
            f"Book extraction complete: book='{self.book_name}' "
            f"chapters={len(metadata_list)} "
            f"unique_keywords={len(all_keywords)} "
            f"unique_concepts={len(all_concepts)} "
            f"mode=per-chapter"
        )
        
        return metadata_list
    
    def save_metadata(
        self,
        metadata_list: List[ChapterMetadata],
        output_path: Optional[Path] = None,
        dry_run: bool = False
    ) -> Path:
        """
        Save metadata to JSON file.
        
        Args:
            metadata_list: List of ChapterMetadata objects
            output_path: Optional custom output path
            dry_run: If True, show what would be saved without writing file
            
        Returns:
            Path where metadata was (or would be) saved
        """
        if output_path is None:
            output_path = DEFAULT_METADATA_DIR / f"{self.book_name}_metadata.json"
        
        # Convert to dictionaries for JSON
        metadata_dicts = [m.to_dict() for m in metadata_list]
        
        if dry_run:
            print("\n" + "="*60)
            print("DRY RUN MODE - No files will be written")
            print("="*60)
            print(f"\nWould save to: {output_path}")
            print(f"Chapters: {len(metadata_list)}")
            print("\nPreview (first 500 chars):")
            preview = json.dumps(metadata_dicts, indent=2, ensure_ascii=False)[:500]
            print(preview)
            if len(json.dumps(metadata_dicts)) > 500:
                print("...")
            print("\n" + "="*60)
            return output_path
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write with context manager (PY 32425)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metadata_dicts, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Saved metadata for {len(metadata_list)} chapters to {output_path}")
        return output_path


def interactive_chapter_definition(book_name: str, total_pages: int) -> List[Tuple[int, str, int, int]]:
    """
    Interactive mode for defining chapters.
    
    Args:
        book_name: Name of the book
        total_pages: Total number of pages
        
    Returns:
        List of (chapter_num, title, start_page, end_page) tuples
    """
    print(f"\n📖 Interactive Chapter Definition for: {book_name}")
    print(f"Total pages: {total_pages}")
    print("\nEnter chapters one at a time. Press Ctrl+C or enter blank to finish.\n")
    
    chapters: List[Tuple[int, str, int, int]] = []
    
    while True:
        try:
            chapter_num_str = input(f"Chapter {len(chapters) + 1} number (or blank to finish): ").strip()
            if not chapter_num_str:
                break
            
            chapter_num = int(chapter_num_str)
            title = input("  Title: ").strip()
            start_page = int(input("  Start page: ").strip())
            end_page = int(input("  End page: ").strip())
            
            chapters.append((chapter_num, title, start_page, end_page))
            print(f"  ✅ Added: Chapter {chapter_num}: {title} (pages {start_page}-{end_page})\n")
            
        except (KeyboardInterrupt, EOFError):
            print("\n\nFinished defining chapters.")
            break
        except ValueError as e:
            print(f"  ❌ Invalid input: {e}. Please try again.\n")
    
    return chapters


def _parse_explicit_chapters(chapters_arg: str):
    """Parse explicit chapter definitions from command-line argument.
    
    Args:
        chapters_arg: String representation of chapter list
        
    Returns:
        List of chapter tuples or None on error
    """
    try:
        chapters = literal_eval(chapters_arg)
        print(f"\n✅ Using {len(chapters)} explicitly defined chapters")
        return chapters
    except (ValueError, SyntaxError) as e:
        print(f"❌ Error parsing chapters: {e}")
        print("   Expected format: \"[(1, 'Title', 1, 10), (2, 'Title2', 11, 20)]\"")
        sys.exit(1)


def _auto_detect_chapters(generator):
    """Auto-detect chapters and display results.
    
    Args:
        generator: UniversalMetadataGenerator instance
        
    Returns:
        List of detected chapter tuples
    """
    print("\n🔍 Auto-detecting chapters...")
    chapters = generator.auto_detect_chapters()
    print(f"✅ Detected {len(chapters)} chapters")
    
    # Show detected chapters for confirmation
    print("\nDetected chapters:")
    for ch_num, title, start, end in chapters:
        print(f"  {ch_num}. {title} (pages {start}-{end})")
    
    return chapters


def _get_chapter_definitions(args, generator):
    """Get chapter definitions based on command-line arguments.
    
    Args:
        args: Parsed command-line arguments
        generator: UniversalMetadataGenerator instance
        
    Returns:
        List of chapter tuples
    """
    if args.chapters:
        return _parse_explicit_chapters(args.chapters)
    elif args.auto_detect:
        return _auto_detect_chapters(generator)
    elif args.interactive:
        return interactive_chapter_definition(generator.book_name, len(generator.pages))
    else:
        print("❌ Error: Must specify --chapters, --auto-detect, or --interactive")
        sys.exit(1)


def main():
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(
        description="Universal metadata generator for textbook JSON files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Auto-detect chapters:
  python3 generate_metadata_universal.py --input data/textbooks_json/MyBook.json --auto-detect
  
  # Interactive mode:
  python3 generate_metadata_universal.py --input data/textbooks_json/MyBook.json --interactive
  
  # With explicit chapters (Python list format):
  python3 generate_metadata_universal.py --input MyBook.json --chapters "[(1,'Intro',1,20),(2,'Advanced',21,50)]"
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Path to textbook JSON file'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Optional output path for metadata JSON (default: data/metadata/{book_name}_metadata.json)'
    )
    
    parser.add_argument(
        '--chapters', '-c',
        help='Chapter definitions as Python list: [(num, title, start, end), ...]'
    )
    
    parser.add_argument(
        '--auto-detect',
        action='store_true',
        help='Auto-detect chapters from page content'
    )
    
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Interactive mode for defining chapters'
    )
    
    parser.add_argument(
        '--domain',
        choices=['python', 'architecture', 'data_science', 'auto'],
        default='auto',
        help='Book domain for keyword extraction (default: auto-detect)'
    )
    
    parser.add_argument(
        '--keywords-file',
        help='Path to custom keywords JSON config file (default: config/metadata_keywords.json)'
    )
    
    parser.add_argument(
        '--patterns-file',
        help='Path to custom chapter patterns JSON config file (default: config/chapter_patterns.json)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be saved without writing files'
    )
    
    # AC-1.2: --use-orchestrator CLI flag for orchestrator-based extraction
    parser.add_argument(
        '--use-orchestrator',
        action='store_true',
        default=False,
        help='Use Code-Orchestrator-Service for metadata extraction instead of local StatisticalExtractor'
    )
    
    # AC-1.2: --fallback-on-error flag for graceful degradation
    parser.add_argument(
        '--fallback-on-error',
        action='store_true',
        default=True,
        help='Fall back to local StatisticalExtractor if orchestrator fails (default: True)'
    )
    
    args = parser.parse_args()
    
    # ===========================================================================
    # AC-1.2: Determine if orchestrator should be used
    # Precedence: CLI flag > env var > default (False)
    # ===========================================================================
    settings = get_extraction_settings()
    
    # CLI flag takes precedence if explicitly provided
    # argparse sets args.use_orchestrator to True if flag is present, False otherwise
    # We check if CLI was explicitly used by seeing if --use-orchestrator appears in sys.argv
    cli_explicitly_set = "--use-orchestrator" in sys.argv
    
    if cli_explicitly_set:
        # CLI takes precedence
        use_orchestrator = args.use_orchestrator
    else:
        # Fall back to env var via ExtractionSettings
        use_orchestrator = settings.use_orchestrator_extraction
    
    # Log the decision for debugging
    if use_orchestrator:
        source = "CLI" if cli_explicitly_set else "env var (EXTRACTION_USE_ORCHESTRATOR_EXTRACTION)"
        print(f"🔗 Using orchestrator service (source: {source})")
    else:
        print("📊 Using local StatisticalExtractor")
    
    # Initialize generator
    json_path = Path(args.input)
    if not json_path.exists():
        print(f"❌ Error: File not found: {json_path}")
        sys.exit(1)
    
    # Prepare optional arguments
    kwargs = {'domain': args.domain}
    if args.keywords_file:
        kwargs['keywords_file'] = Path(args.keywords_file)
    if args.patterns_file:
        kwargs['patterns_file'] = Path(args.patterns_file)
    
    generator = UniversalMetadataGenerator(json_path, **kwargs)
    print(f"📚 Loaded: {generator.book_name}")
    print(f"   Pages: {len(generator.pages)}")
    print(f"   Domain: {generator.domain}")
    
    # Get chapter definitions using extracted helper
    chapters = _get_chapter_definitions(args, generator)
    
    if not chapters:
        print("❌ Error: No chapters defined")
        sys.exit(1)
    
    # Generate metadata
    print(f"\n🔬 Generating metadata for {len(chapters)} chapters...")
    metadata_list = generator.generate_metadata(chapters)
    
    # Save metadata
    output_path = Path(args.output) if args.output else None
    saved_path = generator.save_metadata(metadata_list, output_path, dry_run=args.dry_run)
    
    if not args.dry_run:
        print(f"\n✨ Done! Metadata saved to: {saved_path}")
    else:
        print("\n✨ Done! (DRY RUN - no files written)")


if __name__ == "__main__":
    main()
