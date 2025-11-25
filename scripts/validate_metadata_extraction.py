#!/usr/bin/env python3
"""
Metadata Extraction Validation Script

Validates that extracted metadata files are complete, structurally correct,
and contain valid data for all chapters.

Validation checks:
1. File existence and JSON validity
2. Required fields present in each chapter
3. Chapter numbering sequential and unique
4. Page ranges valid and non-overlapping
5. Keywords and concepts extracted (non-empty)
6. Cross-reference with source JSON chapters
7. Data quality (string lengths, list sizes)

Usage:
    python3 scripts/validate_metadata_extraction.py
    python3 scripts/validate_metadata_extraction.py --book "Learning Python Ed6"
    python3 scripts/validate_metadata_extraction.py --verbose
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Service Layer imports
from scripts.validation_services import (
    ValidationResult,
    ChapterValidator,
    ChapterNumberValidator,
    PageRangeValidator,
    SourceValidator,
    BookValidator,
    ValidationResultFormatter
)


class MetadataValidator:
    """Validates extracted metadata files"""
    
    def __init__(self, metadata_dir: Path, source_dir: Path, verbose: bool = False):
        self.metadata_dir = metadata_dir
        self.source_dir = source_dir
        self.verbose = verbose
        self.results: Dict[str, List[ValidationResult]] = {}
    
    def validate_all(self) -> Tuple[int, int, int]:
        """
        Validate all metadata files (refactored: CC 13 → 5).
        
        Returns:
            (total_books, passed_books, failed_books)
        """
        metadata_files = sorted(self.metadata_dir.glob("*_metadata.json"))
        
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║                    METADATA EXTRACTION VALIDATION                            ║")
        print("╚══════════════════════════════════════════════════════════════════════════════╝\n")
        
        total = len(metadata_files)
        passed = 0
        failed = 0
        
        for metadata_file in metadata_files:
            book_name = metadata_file.stem.replace("_metadata", "")
            
            if self.verbose:
                print(f"\n{'='*80}")
                print(f"Validating: {book_name}")
                print('='*80)
            else:
                print(f"Validating: {book_name:<50}", end=" ")
            
            book_results = self.validate_book(metadata_file, book_name)
            self.results[book_name] = book_results
            
            # Count errors and warnings
            errors, warnings = ValidationResultFormatter.count_errors_and_warnings(book_results)
            
            if errors > 0:
                failed += 1
                ValidationResultFormatter.print_book_status(book_name, errors, warnings, self.verbose)
                self._print_results(book_results, verbose=self.verbose)
            else:
                passed += 1
                ValidationResultFormatter.print_book_status(book_name, errors, warnings, self.verbose)
                if warnings and self.verbose:
                    self._print_results(book_results, verbose=self.verbose)
        
        return total, passed, failed
    
    def validate_book(self, metadata_file: Path, book_name: str) -> List[ValidationResult]:
        """Validate a single book (refactored: CC 12 → 1)"""
        book_validator = BookValidator(self.source_dir)
        return book_validator.validate(metadata_file, book_name)
    
    def _validate_chapter(self, chapter: Dict[str, Any], idx: int, total_pages: int) -> List[ValidationResult]:
        """Validate a single chapter (refactored: CC 34 → 1)"""
        chapter_validator = ChapterValidator()
        return chapter_validator.validate(chapter, idx, total_pages)
    
    def _validate_chapter_numbers(self, chapter_numbers: List[int]) -> List[ValidationResult]:
        """Validate chapter numbering (refactored: CC 8 → 1)"""
        return ChapterNumberValidator.validate(chapter_numbers)
    
    def _validate_page_ranges(self, page_ranges: List[Tuple[int, int]]) -> List[ValidationResult]:
        """Validate page ranges (refactored: CC 4 → 1)"""
        return PageRangeValidator.validate(page_ranges)
    
    def _validate_against_source(self, metadata: List[Dict], source_chapters: List[Dict]) -> List[ValidationResult]:
        """Cross-reference with source (refactored: CC 4 → 1)"""
        return SourceValidator.validate(metadata, source_chapters)
    
    def _print_results(self, results: List[ValidationResult], verbose: bool = False):
        """Print validation results (refactored: CC 8 → 1)"""
        ValidationResultFormatter.print_results(results, verbose)
    
    def print_summary(self, total: int, passed: int, failed: int):
        """Print validation summary (refactored: CC 15 → 3)"""
        ValidationResultFormatter.print_summary_header()
        
        # Calculate total errors and warnings
        total_errors = 0
        total_warnings = 0
        
        for results in self.results.values():
            errors, warnings = ValidationResultFormatter.count_errors_and_warnings(results)
            total_errors += errors
            total_warnings += warnings
        
        ValidationResultFormatter.print_summary_statistics(
            total, passed, failed, total_errors, total_warnings
        )
        
        if failed > 0:
            ValidationResultFormatter.print_failed_books(self.results)
        else:
            ValidationResultFormatter.print_success_message(total_warnings)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Validate metadata extraction completeness and quality",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--book', '-b',
        help='Validate specific book only (e.g., "Learning Python Ed6")'
    )
    
    parser.add_argument(
        '--metadata-dir',
        type=Path,
        default=Path('workflows/metadata_extraction/output'),
        help='Directory containing metadata JSON files'
    )
    
    parser.add_argument(
        '--source-dir',
        type=Path,
        default=Path('workflows/pdf_to_json/output/textbooks_json'),
        help='Directory containing source JSON files'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed validation results for each book'
    )
    
    args = parser.parse_args()
    
    # Validate directories exist
    if not args.metadata_dir.exists():
        print(f"❌ Error: Metadata directory not found: {args.metadata_dir}")
        return 1
    
    if not args.source_dir.exists():
        print(f"❌ Error: Source directory not found: {args.source_dir}")
        return 1
    
    # Create validator
    validator = MetadataValidator(args.metadata_dir, args.source_dir, args.verbose)
    
    # Run validation
    if args.book:
        # Validate single book
        metadata_file = args.metadata_dir / f"{args.book}_metadata.json"
        if not metadata_file.exists():
            print(f"❌ Error: Metadata file not found: {metadata_file}")
            return 1
        
        print(f"Validating: {args.book}\n")
        results = validator.validate_book(metadata_file, args.book)
        validator.results[args.book] = results
        validator._print_results(results, verbose=True)
        
        errors = [r for r in results if not r.passed and r.severity == "error"]
        if errors:
            print(f"\n❌ FAILED: {len(errors)} errors")
            return 1
        else:
            print("\n✅ PASSED")
            return 0
    else:
        # Validate all books
        total, passed, failed = validator.validate_all()
        validator.print_summary(total, passed, failed)
        
        return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit(main())
