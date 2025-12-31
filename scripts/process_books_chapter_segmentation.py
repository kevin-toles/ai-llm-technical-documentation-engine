#!/usr/bin/env python3
"""
Process books with empty chapters through ChapterSegmenter.

WBS 3.5.1.2-3.5.1.3 - GREEN Phase: Chapter Segmentation Processing
Reference: AI_CODING_PLATFORM_WBS.md Phase 3.5

Purpose:
    Read book JSONs from ai-platform-data/books/raw/
    Process through ChapterSegmenter to populate empty chapters
    Write to test_fixtures/books/ for testing
    
Usage:
    # Process single test book:
    python3 scripts/process_books_chapter_segmentation.py --single
    
    # Process all 12 books with empty chapters:
    python3 scripts/process_books_chapter_segmentation.py --all
    
    # Dry run (show what would be processed):
    python3 scripts/process_books_chapter_segmentation.py --dry-run

Document References:
    - GUIDELINES_AI_Engineering: Batch processing patterns
    - CODING_PATTERNS_ANALYSIS: Error handling, type hints
    - AI_CODING_PLATFORM_ARCHITECTURE: Workflow separation

Output:
    - test_fixtures/books/{book_name}.json: Processed book with chapters
    - Console: Processing statistics and validation results
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from workflows.pdf_to_json.scripts.chapter_segmenter import ChapterSegmenter
from config.settings import ChapterSegmentationConfig


# ============================================================================
# Constants
# ============================================================================

# Path to ai-platform-data books (sibling repo)
_AI_PLATFORM_DATA_BOOKS = Path(__file__).parent.parent.parent / "ai-platform-data" / "books" / "raw"

# Output path for test fixtures
_TEST_FIXTURES_DIR = PROJECT_ROOT / "test_fixtures" / "books"

# 12 books with empty chapters (identified in WBS)
BOOKS_WITH_EMPTY_CHAPTERS = [
    "Architecture Patterns with Python.json",
    "Building Microservices.json",
    "Building Python Microservices with FastAPI.json",
    "Fluent Python 2nd.json",
    "Microservice APIs Using Python Flask FastAPI.json",
    "Microservice Architecture.json",
    "Microservices Up and Running.json",
    "Python Architecture Patterns.json",
    "Python Data Analysis 3rd.json",
    "Python Distilled.json",
    "Python Essential Reference 4th.json",
    "Python Microservices Development.json",
]


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class ProcessingResult:
    """Result of processing a single book.
    
    Attributes:
        book_name: Name of the book file
        success: Whether processing succeeded
        chapters_count: Number of chapters detected
        detection_methods: Set of detection methods used
        error: Error message if processing failed
    """
    book_name: str
    success: bool
    chapters_count: int = 0
    detection_methods: Optional[set] = None
    error: Optional[str] = None
    
    def __str__(self) -> str:
        if self.success:
            methods = ", ".join(sorted(self.detection_methods or set()))
            return f"✅ {self.book_name}: {self.chapters_count} chapters ({methods})"
        return f"❌ {self.book_name}: {self.error}"


# ============================================================================
# Processing Functions
# ============================================================================

def load_book(book_path: Path) -> Optional[Dict[str, Any]]:
    """Load book JSON from file.
    
    Args:
        book_path: Path to book JSON file
        
    Returns:
        Book data dict or None if loading failed
    """
    try:
        with open(book_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading {book_path.name}: {e}")
        return None


def process_book(
    book_data: Dict[str, Any],
    segmenter: ChapterSegmenter
) -> List[Dict[str, Any]]:
    """Process book pages through ChapterSegmenter.
    
    Args:
        book_data: Book JSON with pages array
        segmenter: Configured ChapterSegmenter instance
        
    Returns:
        List of chapter dicts
    """
    pages = book_data.get("pages", [])
    if not pages:
        return []
    
    return segmenter.segment_book(pages)


def save_processed_book(
    book_data: Dict[str, Any],
    chapters: List[Dict[str, Any]],
    output_path: Path
) -> bool:
    """Save processed book with chapters to output file.
    
    Args:
        book_data: Original book data
        chapters: Processed chapters
        output_path: Path to write output
        
    Returns:
        True if save succeeded
    """
    # Update book data with chapters
    processed_book = book_data.copy()
    processed_book["chapters"] = chapters
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(processed_book, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Error saving {output_path.name}: {e}")
        return False


def process_single_book(
    book_name: str,
    segmenter: ChapterSegmenter,
    source_dir: Path,
    output_dir: Path,
    dry_run: bool = False
) -> ProcessingResult:
    """Process a single book through chapter segmentation.
    
    Args:
        book_name: Name of book JSON file
        segmenter: ChapterSegmenter instance
        source_dir: Directory containing source books
        output_dir: Directory to write processed books
        dry_run: If True, don't write output files
        
    Returns:
        ProcessingResult with success/failure details
    """
    source_path = source_dir / book_name
    output_path = output_dir / book_name
    
    # Check source exists
    if not source_path.exists():
        return ProcessingResult(
            book_name=book_name,
            success=False,
            error=f"Source file not found: {source_path}"
        )
    
    # Load book
    book_data = load_book(source_path)
    if book_data is None:
        return ProcessingResult(
            book_name=book_name,
            success=False,
            error="Failed to load book JSON"
        )
    
    # Check if already has chapters
    existing_chapters = book_data.get("chapters", [])
    if existing_chapters:
        return ProcessingResult(
            book_name=book_name,
            success=True,
            chapters_count=len(existing_chapters),
            detection_methods={ch.get("detection_method", "unknown") for ch in existing_chapters},
            error="Already has chapters (skipped)"
        )
    
    # Process through ChapterSegmenter
    try:
        chapters = process_book(book_data, segmenter)
    except Exception as e:
        return ProcessingResult(
            book_name=book_name,
            success=False,
            error=f"Processing error: {e}"
        )
    
    if not chapters:
        return ProcessingResult(
            book_name=book_name,
            success=False,
            error="No chapters produced"
        )
    
    # Save output (unless dry run)
    if not dry_run and not save_processed_book(book_data, chapters, output_path):
        return ProcessingResult(
            book_name=book_name,
            success=False,
            error="Failed to save output"
        )
    
    # Collect detection methods
    detection_methods = {ch.get("detection_method", "unknown") for ch in chapters}
    
    return ProcessingResult(
        book_name=book_name,
        success=True,
        chapters_count=len(chapters),
        detection_methods=detection_methods
    )


# ============================================================================
# Main Processing Logic
# ============================================================================

def main() -> int:
    """Main entry point for book processing.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    parser = argparse.ArgumentParser(
        description="Process books with empty chapters through ChapterSegmenter"
    )
    parser.add_argument(
        "--single",
        action="store_true",
        help="Process only the first test book (Architecture Patterns with Python)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all 12 books with empty chapters"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be processed without writing files"
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=_AI_PLATFORM_DATA_BOOKS,
        help="Directory containing source book JSONs"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=_TEST_FIXTURES_DIR,
        help="Directory to write processed books"
    )
    
    args = parser.parse_args()
    
    # Validate source directory
    if not args.source_dir.exists():
        print(f"Error: Source directory not found: {args.source_dir}")
        print("Expected ai-platform-data/books/raw/ as sibling repo")
        return 1
    
    # Determine books to process
    if args.single:
        books_to_process = BOOKS_WITH_EMPTY_CHAPTERS[:1]
    elif args.all:
        books_to_process = BOOKS_WITH_EMPTY_CHAPTERS
    else:
        parser.print_help()
        return 1
    
    print(f"{'[DRY RUN] ' if args.dry_run else ''}Processing {len(books_to_process)} books...")
    print(f"Source: {args.source_dir}")
    print(f"Output: {args.output_dir}")
    print()
    
    # Initialize ChapterSegmenter
    config = ChapterSegmentationConfig()
    segmenter = ChapterSegmenter(config)
    
    # Process books
    results: List[ProcessingResult] = []
    for book_name in books_to_process:
        print(f"Processing: {book_name}...")
        result = process_single_book(
            book_name=book_name,
            segmenter=segmenter,
            source_dir=args.source_dir,
            output_dir=args.output_dir,
            dry_run=args.dry_run
        )
        results.append(result)
        print(f"  {result}")
    
    # Print summary
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    success_count = sum(1 for r in results if r.success)
    total_chapters = sum(r.chapters_count for r in results if r.success)
    
    print(f"Books processed: {success_count}/{len(results)}")
    print(f"Total chapters detected: {total_chapters}")
    
    # Detection method breakdown
    all_methods: Dict[str, int] = {}
    for r in results:
        if r.success and r.detection_methods:
            for method in r.detection_methods:
                all_methods[method] = all_methods.get(method, 0) + 1
    
    if all_methods:
        print("\nDetection methods used:")
        for method, count in sorted(all_methods.items()):
            print(f"  - {method}: {count} books")
    
    # Check for failures
    failures = [r for r in results if not r.success]
    if failures:
        print("\nFailures:")
        for r in failures:
            print(f"  ❌ {r.book_name}: {r.error}")
        return 1
    
    print("\n✅ All books processed successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
