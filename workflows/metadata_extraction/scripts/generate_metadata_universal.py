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
import re
import argparse
from pathlib import Path
from typing import List, Dict, Set, Any, Tuple, Optional
from collections import Counter
from dataclasses import dataclass, asdict
import sys

# Try to use settings, fallback to defaults
try:
    from config.settings import settings
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
        keywords_file: Optional[Path] = None,
        patterns_file: Optional[Path] = None
    ):
        """
        Initialize generator with JSON file.
        
        Args:
            json_path: Path to textbook JSON file
            domain: Domain of the book ("python", "architecture", "data_science", "auto")
            keywords_file: Optional path to keywords JSON config (default: config/metadata_keywords.json)
            patterns_file: Optional path to patterns JSON config (default: config/chapter_patterns.json)
            
        Raises:
            ValueError: If config files have invalid schema or patterns
            FileNotFoundError: If required files don't exist (EAFP - PY 21)
        """
        self.json_path = Path(json_path)
        self.domain = domain
        
        # Load configuration files (DI pattern - ARCH 5336)
        self.keywords_file = Path(keywords_file) if keywords_file else Path(__file__).parent.parent.parent.parent / "config" / "metadata_keywords.json"
        self.patterns_file = Path(patterns_file) if patterns_file else Path(__file__).parent.parent.parent.parent / "config" / "chapter_patterns.json"
        
        # Load and validate keywords config
        self.keyword_config = self._load_and_validate_keywords()
        
        # Load and validate patterns config
        self.pattern_config = self._load_and_validate_patterns()
        
        # Load JSON (using context manager - PY 32425)
        with open(self.json_path, 'r', encoding='utf-8') as f:
            self.book_data = json.load(f)
        
        self.pages = self.book_data.get('pages', [])
        self.book_name = self.json_path.stem
        
        # Auto-detect domain if not specified
        if self.domain == "auto":
            self.domain = self._detect_domain()
        
        # Combine keyword sets based on domain
        self.keywords = self._get_keyword_set()
        
        # Compile chapter pattern for auto-detection
        self.chapter_pattern = re.compile(self.pattern_config.get("chapter_heading", r'(?:chapter|ch\.?)\s+(\d+)[:\s]+(.+)'), re.IGNORECASE)
        self.section_pattern = re.compile(self.pattern_config.get("section_heading", r'^(?:section|§)\s+(\d+(?:\.\d+)?)'), re.IGNORECASE) if "section_heading" in self.pattern_config else None
    
    def _load_and_validate_keywords(self) -> Dict[str, List[str]]:
        """
        Load and validate keywords config file.
        
        Returns:
            Dictionary with domain keys and keyword lists
            
        Raises:
            ValueError: If file has invalid schema
            FileNotFoundError: If file doesn't exist
        """
        try:
            with open(self.keywords_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Keywords file not found: {self.keywords_file}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in keywords file: {e}")
        
        # Validate schema: must be dict with string keys and list values
        if not isinstance(config, dict):
            raise ValueError(f"Invalid keywords file schema: expected dict, got {type(config).__name__}")
        
        for domain, keywords in config.items():
            if not isinstance(keywords, list):
                raise ValueError(f"Invalid keywords file schema: domain '{domain}' must have list of keywords, got {type(keywords).__name__}")
            if not all(isinstance(kw, str) for kw in keywords):
                raise ValueError(f"Invalid keywords file schema: domain '{domain}' contains non-string keywords")
        
        return config
    
    def _load_and_validate_patterns(self) -> Dict[str, str]:
        """
        Load and validate patterns config file.
        
        Returns:
            Dictionary with pattern names and regex strings
            
        Raises:
            ValueError: If file has invalid schema or regex
            FileNotFoundError: If file doesn't exist
        """
        try:
            with open(self.patterns_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Patterns file not found: {self.patterns_file}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in patterns file: {e}")
        
        # Validate schema and regex patterns
        if not isinstance(config, dict):
            raise ValueError(f"Invalid patterns file schema: expected dict, got {type(config).__name__}")
        
        for pattern_name, pattern_str in config.items():
            if not isinstance(pattern_str, str):
                raise ValueError(f"Invalid patterns file schema: pattern '{pattern_name}' must be string, got {type(pattern_str).__name__}")
            
            # Validate regex by attempting to compile
            try:
                re.compile(pattern_str)
            except re.error as e:
                raise ValueError(f"Invalid regex pattern '{pattern_name}': {e}")
        
        return config
    
    def _detect_domain(self) -> str:
        """Auto-detect book domain from title or content."""
        title_lower = self.book_name.lower()
        
        if any(word in title_lower for word in ['microservice', 'architecture', 'api', 'fastapi', 'flask']):
            return "architecture"
        elif any(word in title_lower for word in ['data', 'analysis', 'pandas', 'numpy']):
            return "data_science"
        else:
            return "python"
    
    def _get_keyword_set(self) -> Set[str]:
        """Get combined keyword set based on domain."""
        # Start with Python keywords (always include basics)
        keywords = set(self.keyword_config.get("python", []))
        
        if self.domain in ["architecture", "microservices"]:
            keywords.update(self.keyword_config.get("architecture", []))
        elif self.domain == "data_science":
            keywords.update(self.keyword_config.get("data_science", []))
        
        return keywords
    
    def auto_detect_chapters(self) -> List[Tuple[int, str, int, int]]:
        """
        Auto-detect chapters from page content.
        
        Looks for:
        1. Pages with "Chapter N" headings
        2. Clear topic changes
        3. Page number breaks
        
        Returns:
            List of (chapter_num, title, start_page, end_page) tuples
        """
        chapters = []
        current_chapter = None
        
        for idx, page in enumerate(self.pages, start=1):
            text = page.get('text', '')
            lines = text.split('\n')[:10]  # Check first 10 lines
            
            for line in lines:
                match = self.chapter_pattern.search(line)
                if match:
                    # Found a new chapter
                    if current_chapter:
                        # Close previous chapter
                        chapters.append((*current_chapter, idx - 1))
                    
                    chapter_num = int(match.group(1))
                    title = match.group(2).strip().rstrip('.')
                    current_chapter = (chapter_num, title, idx)
                    break
        
        # Close last chapter
        if current_chapter:
            chapters.append((*current_chapter, len(self.pages)))
        
        return chapters
    
    def extract_keywords(self, text: str, max_keywords: int = 15) -> List[str]:
        """
        Extract meaningful keywords from chapter text.
        
        Args:
            text: Chapter text content
            max_keywords: Maximum number of keywords to return
            
        Returns:
            List of keywords sorted by frequency
        """
        text_lower = text.lower()
        
        keyword_counts = Counter()
        for keyword in self.keywords:
            count = text_lower.count(keyword)
            if count > 0:
                keyword_counts[keyword] = count
        
        return [kw for kw, _ in keyword_counts.most_common(max_keywords)]
    
    def extract_concepts(self, text: str, max_concepts: int = 10) -> List[str]:
        """
        Extract key concepts and topics from chapter text.
        
        Uses pattern matching to find multi-word concepts and phrases.
        
        Args:
            text: Chapter text content
            max_concepts: Maximum number of concepts to return
            
        Returns:
            List of concepts
        """
        text_lower = text.lower()
        
        concept_patterns = [
            # OOP Concepts
            r'\b(object[- ]oriented programming)\b',
            r'\b(class hierarchi(?:es|y))\b',
            r'\b(multiple inheritance)\b',
            r'\b(method resolution order)\b',
            r'\b(abstract base class(?:es)?)\b',
            
            # Functional Programming
            r'\b(functional programming)\b',
            r'\b(higher[- ]order function(?:s)?)\b',
            r'\b(pure function(?:s)?)\b',
            r'\b(immutabl(?:e|ility))\b',
            
            # Async/Concurrency
            r'\b(asynchronous programming)\b',
            r'\b(concurrent execution)\b',
            r'\b(parallel processing)\b',
            r'\b(event loop)\b',
            r'\b(coroutine(?:s)?)\b',
            
            # Architecture
            r'\b(microservices architecture)\b',
            r'\b(domain[- ]driven design)\b',
            r'\b(event[- ]driven architecture)\b',
            r'\b(service[- ]oriented architecture)\b',
            r'\b(repository pattern)\b',
            r'\b(dependency injection)\b',
            
            # Data Structures
            r'\b(data structure(?:s)?)\b',
            r'\b(hash table(?:s)?)\b',
            r'\b(linked list(?:s)?)\b',
            r'\b(binary tree(?:s)?)\b',
            
            # General Programming
            r'\b(design pattern(?:s)?)\b',
            r'\b(code organization)\b',
            r'\b(best practice(?:s)?)\b',
            r'\b(error handling)\b',
            r'\b(exception handling)\b',
            r'\b(type system)\b',
            r'\b(memory management)\b',
        ]
        
        concepts = []
        for pattern in concept_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                concept = match.group(1)
                if concept not in concepts:
                    concepts.append(concept)
                if len(concepts) >= max_concepts:
                    return concepts
        
        return concepts[:max_concepts]
    
    def generate_summary(self, text: str, title: str, chapter_num: int) -> str:
        """
        Generate a summary for the chapter.
        
        Uses heuristics to extract key sentences and topics.
        For better summaries, integrate with LLM API.
        
        Args:
            text: Chapter text content
            title: Chapter title
            chapter_num: Chapter number
            
        Returns:
            Generated summary string
        """
        # Extract first few paragraphs (likely intro/overview)
        paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 100]
        
        if not paragraphs:
            return f"Chapter {chapter_num}: {title}"
        
        # Take first substantial paragraph as base
        first_para = paragraphs[0]
        
        # Limit to reasonable summary length
        sentences = first_para.split('. ')
        summary_sentences = sentences[:3]  # First 3 sentences
        
        summary = '. '.join(summary_sentences)
        if not summary.endswith('.'):
            summary += '.'
        
        # Ensure reasonable length
        if len(summary) > 500:
            summary = summary[:497] + '...'
        
        return summary
    
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
                    chapter_text += self.pages[page_idx].get('text', '') + "\n"
            
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
    
    chapters = []
    
    while True:
        try:
            chapter_num = input(f"Chapter {len(chapters) + 1} number (or blank to finish): ").strip()
            if not chapter_num:
                break
            
            chapter_num = int(chapter_num)
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
    
    # Get chapter definitions
    chapters = None
    
    if args.chapters:
        # Parse explicit chapter definitions
        try:
            chapters = eval(args.chapters)
            print(f"\n✅ Using {len(chapters)} explicitly defined chapters")
        except Exception as e:
            print(f"❌ Error parsing chapters: {e}")
            sys.exit(1)
    
    elif args.auto_detect:
        # Auto-detect chapters
        print("\n🔍 Auto-detecting chapters...")
        chapters = generator.auto_detect_chapters()
        print(f"✅ Detected {len(chapters)} chapters")
        
        # Show detected chapters for confirmation
        print("\nDetected chapters:")
        for ch_num, title, start, end in chapters:
            print(f"  {ch_num}. {title} (pages {start}-{end})")
    
    elif args.interactive:
        # Interactive mode
        chapters = interactive_chapter_definition(generator.book_name, len(generator.pages))
    
    else:
        print("❌ Error: Must specify --chapters, --auto-detect, or --interactive")
        sys.exit(1)
    
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
