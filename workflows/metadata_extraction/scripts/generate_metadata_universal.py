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

Output:
    - Saves to: data/metadata/{book_name}_metadata.json
    - Format: List of chapter objects with keywords, concepts, summary

Reference:
- Python Distilled Ch. 9 - pathlib.Path operations
- Python Distilled Ch. 7 - Dataclass configuration patterns
- Microservices Up and Running Ch. 7 - 12-Factor App configuration
"""

import json
import argparse
from ast import literal_eval
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
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
from workflows.metadata_extraction.scripts.strategies.regex_pattern_strategy import RegexPatternStrategy  # noqa: E402
from workflows.metadata_extraction.scripts.strategies.yake_validation_strategy import YAKEValidationStrategy  # noqa: E402
from workflows.metadata_extraction.scripts.strategies.toc_filter_strategy import TOCFilterStrategy  # noqa: E402
from workflows.metadata_extraction.scripts.strategies.duplicate_filter_strategy import DuplicateFilterStrategy  # noqa: E402

# Try to use settings, fallback to defaults
try:
    from config.settings import settings  # noqa: E402
    DEFAULT_JSON_DIR = settings.paths.textbooks_json_dir
    DEFAULT_METADATA_DIR = settings.paths.metadata_dir
except ImportError:
    DEFAULT_JSON_DIR = Path("data/textbooks_json")
    DEFAULT_METADATA_DIR = Path("data/metadata")


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
    """
    
    def __init__(
        self, 
        json_path: Path, 
        domain: str = "auto",
        keywords_file: Optional[Path] = None,  # Deprecated - kept for backward compatibility
        patterns_file: Optional[Path] = None   # Deprecated - kept for backward compatibility
    ):
        """
        Initialize generator with JSON file.
        
        Args:
            json_path: Path to textbook JSON file
            domain: Domain of the book (ignored - now domain-agnostic via StatisticalExtractor)
            keywords_file: DEPRECATED - No longer used (statistical extraction is domain-agnostic)
            patterns_file: DEPRECATED - No longer used (statistical extraction is domain-agnostic)
            
        Raises:
            FileNotFoundError: If JSON file doesn't exist (EAFP - PY 21)
            
        Document References:
            - DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN: Part 1.3 (Integration)
            - ARCHITECTURE_GUIDELINES Ch. 4: Adapter pattern for external libraries
        """
        self.json_path = Path(json_path)
        self.domain = domain
        
        # Initialize StatisticalExtractor for domain-agnostic extraction
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
        
        # Compile chapter pattern for auto-detection (default pattern)
        # Initialize StatisticalExtractor for domain-agnostic keyword extraction
        # Per DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN Part 1.3
        self.extractor = StatisticalExtractor()
    
    def auto_detect_chapters(self) -> List[Tuple[int, str, int, int]]:
        """
        Auto-detect chapters using Strategy Pattern (CC: 18 → <10).
        
        Strategy Pipeline:
        1. PreDefinedStrategy - Extract from JSON metadata (highest priority)
        2. RegexPatternStrategy - Find "Chapter N:" markers (fallback)
        3. YAKEValidationStrategy - Validate content quality via keywords
        4. TOCFilterStrategy - Remove table-of-contents pages
        5. DuplicateFilterStrategy - Remove duplicate chapter numbers
        
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
        
        # Priority 2: Scan pages for chapter markers using regex patterns
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
    
    def extract_keywords(self, text: str, max_keywords: int = 15) -> List[str]:
        """
        Extract meaningful keywords from chapter text using statistical methods.
        
        Replaced hardcoded keyword matching with YAKE unsupervised extraction.
        Now works across ANY domain (Python, biology, law, construction, etc.).
        
        Args:
            text: Chapter text content
            max_keywords: Maximum number of keywords to return
            
        Returns:
            List of keywords sorted by relevance (YAKE score)
            
        Document References:
            - DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN Part 1.3: Integration with StatisticalExtractor
            - ARCHITECTURE_GUIDELINES Ch. 4: Adapter pattern for NLP libraries
        """
        keywords_with_scores = self.extractor.extract_keywords(text, top_n=max_keywords)
        return [keyword for keyword, score in keywords_with_scores]
    
    def extract_concepts(self, text: str, max_concepts: int = 10) -> List[str]:
        """
        Extract key concepts and topics from chapter text using TextRank.
        
        Replaced 35+ hardcoded regex patterns with Summa statistical extraction.
        Now works across ANY domain without hardcoded domain knowledge.
        
        Args:
            text: Chapter text content
            max_concepts: Maximum number of concepts to return
            
        Returns:
            List of concepts (single-word terms)
            
        Document References:
            - DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN Part 1.3: Remove hardcoded patterns
            - ARCHITECTURE_GUIDELINES Ch. 5: Service layer orchestration
        """
        return self.extractor.extract_concepts(text, top_n=max_concepts)
    
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
        except Exception:
            # Fallback for very short text or empty content that can't be summarized
            pass
        
        # Fallback: return chapter title
        return f"Chapter {chapter_num}: {title}"
    
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
    
    def generate_metadata(
        self,
        chapters: List[Tuple[int, str, int, int]]
    ) -> List[ChapterMetadata]:
        """
        Generate metadata for all chapters.
        
        Args:
            chapters: List of (chapter_num, title, start_page, end_page) tuples
            
        Returns:
            List of ChapterMetadata objects
            
        Raises:
            ValueError: If chapters have overlapping page ranges
        """
        # Validate chapters for overlaps (exception hierarchy - PY 32425)
        self._validate_chapter_ranges(chapters)
        
        metadata_list = []
        total_chapters = len(chapters)
        
        for idx, (ch_num, title, start_page, end_page) in enumerate(chapters, start=1):
            # Progress indicator (for large books)
            progress_pct = (idx / total_chapters) * 100
            print(f"\n[{progress_pct:.1f}%] Processing Chapter {ch_num}: {title}")
            
            # Collect text from chapter pages
            chapter_text = ""
            for page_idx in range(start_page - 1, min(end_page, len(self.pages))):
                if page_idx < len(self.pages):
                    chapter_text += self.pages[page_idx].get('content', self.pages[page_idx].get('text', '')) + "\n"
            
            # Optimize for large chapters: limit text size to avoid timeouts
            # StatisticalExtractor (YAKE + Summa) is expensive for >100K chars
            MAX_CHAPTER_TEXT = 100000  # 100K chars (~50-60 pages of text)
            if len(chapter_text) > MAX_CHAPTER_TEXT:
                print(f"  Warning: Chapter text too large ({len(chapter_text):,} chars), truncating to {MAX_CHAPTER_TEXT:,} chars")
                chapter_text = chapter_text[:MAX_CHAPTER_TEXT]
            
            page_count = end_page - start_page + 1
            print(f"  Collected {len(chapter_text):,} characters from {page_count} pages")
            
            # Extract metadata
            keywords = self.extract_keywords(chapter_text)
            concepts = self.extract_concepts(chapter_text)
            summary = self.generate_summary(chapter_text, title, ch_num)
            
            print(f"  Keywords: {', '.join(keywords[:5])}...")
            print(f"  Concepts: {', '.join(concepts[:5]) if concepts else 'none detected'}...")
            
            chapter_meta = ChapterMetadata(
                chapter_number=ch_num,
                title=title,
                start_page=start_page,
                end_page=end_page,
                summary=summary,
                keywords=keywords,
                concepts=concepts
            )
            
            metadata_list.append(chapter_meta)
        
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
    
    args = parser.parse_args()
    
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
