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
from dataclasses import dataclass
from collections import Counter


@dataclass
class ValidationResult:
    """Result of a validation check"""
    passed: bool
    message: str
    severity: str = "error"  # error, warning, info


class MetadataValidator:
    """Validates extracted metadata files"""
    
    def __init__(self, metadata_dir: Path, source_dir: Path, verbose: bool = False):
        self.metadata_dir = metadata_dir
        self.source_dir = source_dir
        self.verbose = verbose
        self.results: Dict[str, List[ValidationResult]] = {}
    
    def validate_all(self) -> Tuple[int, int, int]:
        """
        Validate all metadata files.
        
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
            
            # Check if any errors
            errors = [r for r in book_results if not r.passed and r.severity == "error"]
            warnings = [r for r in book_results if not r.passed and r.severity == "warning"]
            
            if errors:
                failed += 1
                if not self.verbose:
                    print(f"❌ FAILED ({len(errors)} errors, {len(warnings)} warnings)")
                self._print_results(book_results, verbose=self.verbose)
            else:
                passed += 1
                if not self.verbose:
                    print(f"✅ PASSED ({len(warnings)} warnings)")
                elif warnings:
                    self._print_results(book_results, verbose=self.verbose)
        
        return total, passed, failed
    
    def validate_book(self, metadata_file: Path, book_name: str) -> List[ValidationResult]:
        """Validate a single metadata file"""
        results = []
        
        # 1. File existence and JSON validity
        try:
            with open(metadata_file) as f:
                metadata = json.load(f)
        except FileNotFoundError:
            results.append(ValidationResult(False, "Metadata file not found", "error"))
            return results
        except json.JSONDecodeError as e:
            results.append(ValidationResult(False, f"Invalid JSON: {e}", "error"))
            return results
        
        results.append(ValidationResult(True, "File exists and JSON is valid", "info"))
        
        # 2. Check if metadata is a list
        if not isinstance(metadata, list):
            results.append(ValidationResult(False, f"Metadata must be a list, got {type(metadata).__name__}", "error"))
            return results
        
        if len(metadata) == 0:
            results.append(ValidationResult(False, "Metadata is empty (0 chapters)", "error"))
            return results
        
        results.append(ValidationResult(True, f"Contains {len(metadata)} chapters", "info"))
        
        # 3. Load source JSON for cross-reference
        source_file = self.source_dir / f"{book_name}.json"
        source_chapters = []
        source_pages = 0
        
        if source_file.exists():
            try:
                with open(source_file) as f:
                    source_data = json.load(f)
                    source_chapters = source_data.get('chapters', [])
                    source_pages = len(source_data.get('pages', []))
                results.append(ValidationResult(True, f"Source JSON found: {len(source_chapters)} chapters, {source_pages} pages", "info"))
            except Exception as e:
                results.append(ValidationResult(False, f"Failed to load source JSON: {e}", "warning"))
        else:
            results.append(ValidationResult(False, f"Source JSON not found: {source_file}", "warning"))
        
        # 4. Validate each chapter
        chapter_numbers = []
        page_ranges = []
        
        for idx, chapter in enumerate(metadata):
            chapter_results = self._validate_chapter(chapter, idx + 1, source_pages)
            results.extend(chapter_results)
            
            # Collect for cross-chapter validation
            if 'chapter_number' in chapter:
                chapter_numbers.append(chapter['chapter_number'])
            if 'start_page' in chapter and 'end_page' in chapter:
                page_ranges.append((chapter['start_page'], chapter['end_page']))
        
        # 5. Chapter numbering validation
        results.extend(self._validate_chapter_numbers(chapter_numbers))
        
        # 6. Page range validation (overlaps)
        results.extend(self._validate_page_ranges(page_ranges))
        
        # 7. Cross-reference with source
        if source_chapters:
            results.extend(self._validate_against_source(metadata, source_chapters))
        
        return results
    
    def _validate_chapter(self, chapter: Dict[str, Any], idx: int, total_pages: int) -> List[ValidationResult]:
        """Validate a single chapter"""
        results = []
        
        # Required fields
        required_fields = ['chapter_number', 'title', 'start_page', 'end_page', 'summary', 'keywords', 'concepts']
        missing_fields = [f for f in required_fields if f not in chapter]
        
        if missing_fields:
            results.append(ValidationResult(
                False,
                f"Chapter {idx}: Missing required fields: {', '.join(missing_fields)}",
                "error"
            ))
            return results
        
        # Chapter number type and value
        if not isinstance(chapter['chapter_number'], int):
            results.append(ValidationResult(
                False,
                f"Chapter {idx}: chapter_number must be integer, got {type(chapter['chapter_number']).__name__}",
                "error"
            ))
        elif chapter['chapter_number'] <= 0:
            results.append(ValidationResult(
                False,
                f"Chapter {idx}: chapter_number must be positive, got {chapter['chapter_number']}",
                "error"
            ))
        
        # Title validation
        if not isinstance(chapter['title'], str):
            results.append(ValidationResult(
                False,
                f"Chapter {idx}: title must be string",
                "error"
            ))
        elif len(chapter['title'].strip()) == 0:
            results.append(ValidationResult(
                False,
                f"Chapter {idx}: title is empty",
                "error"
            ))
        elif len(chapter['title']) > 200:
            results.append(ValidationResult(
                False,
                f"Chapter {idx}: title too long ({len(chapter['title'])} chars, max 200)",
                "warning"
            ))
        
        # Page range validation
        if not isinstance(chapter['start_page'], int) or not isinstance(chapter['end_page'], int):
            results.append(ValidationResult(
                False,
                f"Chapter {idx}: start_page and end_page must be integers",
                "error"
            ))
        elif chapter['start_page'] <= 0 or chapter['end_page'] <= 0:
            results.append(ValidationResult(
                False,
                f"Chapter {idx}: page numbers must be positive",
                "error"
            ))
        elif chapter['start_page'] > chapter['end_page']:
            results.append(ValidationResult(
                False,
                f"Chapter {idx}: start_page ({chapter['start_page']}) > end_page ({chapter['end_page']})",
                "error"
            ))
        elif total_pages > 0 and chapter['end_page'] > total_pages:
            results.append(ValidationResult(
                False,
                f"Chapter {idx}: end_page ({chapter['end_page']}) exceeds total pages ({total_pages})",
                "warning"
            ))
        
        # Summary validation
        if not isinstance(chapter['summary'], str):
            results.append(ValidationResult(
                False,
                f"Chapter {idx}: summary must be string",
                "error"
            ))
        elif len(chapter['summary'].strip()) == 0:
            results.append(ValidationResult(
                False,
                f"Chapter {idx}: summary is empty",
                "error"
            ))
        elif len(chapter['summary']) < 20:
            results.append(ValidationResult(
                False,
                f"Chapter {idx}: summary too short ({len(chapter['summary'])} chars, min 20)",
                "warning"
            ))
        
        # Keywords validation
        if not isinstance(chapter['keywords'], list):
            results.append(ValidationResult(
                False,
                f"Chapter {idx}: keywords must be list",
                "error"
            ))
        elif len(chapter['keywords']) == 0:
            results.append(ValidationResult(
                False,
                f"Chapter {idx}: no keywords extracted",
                "warning"
            ))
        else:
            # Check keyword quality
            non_string_keywords = [kw for kw in chapter['keywords'] if not isinstance(kw, str)]
            if non_string_keywords:
                results.append(ValidationResult(
                    False,
                    f"Chapter {idx}: keywords must be strings, found {len(non_string_keywords)} non-strings",
                    "error"
                ))
            
            empty_keywords = [kw for kw in chapter['keywords'] if isinstance(kw, str) and len(kw.strip()) == 0]
            if empty_keywords:
                results.append(ValidationResult(
                    False,
                    f"Chapter {idx}: {len(empty_keywords)} empty keywords",
                    "warning"
                ))
        
        # Concepts validation
        if not isinstance(chapter['concepts'], list):
            results.append(ValidationResult(
                False,
                f"Chapter {idx}: concepts must be list",
                "error"
            ))
        # Note: concepts can be empty for poor OCR, short chapters, or code-heavy content
        elif len(chapter['concepts']) == 0:
            # Check if it's likely due to poor OCR (very short summary)
            if len(chapter.get('summary', '')) < 50:
                results.append(ValidationResult(
                    False,
                    f"Chapter {idx}: no concepts extracted (possible poor OCR or insufficient text)",
                    "warning"
                ))
            else:
                results.append(ValidationResult(
                    False,
                    f"Chapter {idx}: no concepts extracted",
                    "warning"
                ))
        else:
            non_string_concepts = [c for c in chapter['concepts'] if not isinstance(c, str)]
            if non_string_concepts:
                results.append(ValidationResult(
                    False,
                    f"Chapter {idx}: concepts must be strings, found {len(non_string_concepts)} non-strings",
                    "error"
                ))
        
        return results
    
    def _validate_chapter_numbers(self, chapter_numbers: List[int]) -> List[ValidationResult]:
        """Validate chapter numbering is sequential and unique"""
        results = []
        
        if not chapter_numbers:
            return results
        
        # Check for duplicates
        duplicates = [num for num, count in Counter(chapter_numbers).items() if count > 1]
        if duplicates:
            results.append(ValidationResult(
                False,
                f"Duplicate chapter numbers: {duplicates}",
                "error"
            ))
        
        # Check if sequential (allowing gaps)
        sorted_numbers = sorted(chapter_numbers)
        if sorted_numbers != chapter_numbers:
            results.append(ValidationResult(
                False,
                f"Chapter numbers not in order: {chapter_numbers}",
                "warning"
            ))
        
        # Check for large gaps
        for i in range(len(sorted_numbers) - 1):
            gap = sorted_numbers[i + 1] - sorted_numbers[i]
            if gap > 5:
                results.append(ValidationResult(
                    False,
                    f"Large gap in chapter numbering: {sorted_numbers[i]} → {sorted_numbers[i + 1]}",
                    "warning"
                ))
        
        return results
    
    def _validate_page_ranges(self, page_ranges: List[Tuple[int, int]]) -> List[ValidationResult]:
        """Validate page ranges don't overlap"""
        results = []
        
        if len(page_ranges) < 2:
            return results
        
        # Sort by start_page
        sorted_ranges = sorted(page_ranges)
        
        for i in range(len(sorted_ranges) - 1):
            curr_start, curr_end = sorted_ranges[i]
            next_start, next_end = sorted_ranges[i + 1]
            
            # Check for overlap (curr_end >= next_start means overlap)
            if curr_end >= next_start:
                results.append(ValidationResult(
                    False,
                    f"Overlapping page ranges: ({curr_start}-{curr_end}) and ({next_start}-{next_end})",
                    "error"
                ))
        
        return results
    
    def _validate_against_source(self, metadata: List[Dict], source_chapters: List[Dict]) -> List[ValidationResult]:
        """Cross-reference with source JSON chapters"""
        results = []
        
        metadata_count = len(metadata)
        source_count = len(source_chapters)
        
        if source_count == 0:
            # Source has no chapters, metadata used fallback detection
            results.append(ValidationResult(
                True,
                f"Source has 0 chapters, metadata used fallback detection ({metadata_count} chapters found)",
                "info"
            ))
        elif metadata_count == source_count:
            results.append(ValidationResult(
                True,
                f"Chapter count matches source ({metadata_count} chapters)",
                "info"
            ))
        elif metadata_count < source_count:
            results.append(ValidationResult(
                False,
                f"Missing chapters: metadata has {metadata_count}, source has {source_count}",
                "error"
            ))
        else:
            results.append(ValidationResult(
                False,
                f"Extra chapters: metadata has {metadata_count}, source has {source_count}",
                "warning"
            ))
        
        return results
    
    def _print_results(self, results: List[ValidationResult], verbose: bool = False):
        """Print validation results"""
        if verbose:
            for result in results:
                icon = "✅" if result.passed else ("⚠️" if result.severity == "warning" else "❌")
                print(f"  {icon} {result.message}")
        else:
            # Only print errors and warnings in non-verbose mode
            for result in results:
                if not result.passed:
                    icon = "⚠️" if result.severity == "warning" else "❌"
                    print(f"    {icon} {result.message}")
    
    def print_summary(self, total: int, passed: int, failed: int):
        """Print validation summary"""
        print("\n" + "="*80)
        print("VALIDATION SUMMARY")
        print("="*80)
        
        print(f"\n  Total books validated: {total}")
        print(f"  ✅ Passed: {passed} ({passed/total*100:.1f}%)")
        print(f"  ❌ Failed: {failed} ({failed/total*100:.1f}%)")
        
        # Count warnings and errors across all books
        total_errors = 0
        total_warnings = 0
        
        for book_name, results in self.results.items():
            errors = [r for r in results if not r.passed and r.severity == "error"]
            warnings = [r for r in results if not r.passed and r.severity == "warning"]
            total_errors += len(errors)
            total_warnings += len(warnings)
        
        print(f"\n  Total errors: {total_errors}")
        print(f"  Total warnings: {total_warnings}")
        
        if failed > 0:
            print("\n❌ VALIDATION FAILED")
            print("\nBooks with errors:")
            for book_name, results in self.results.items():
                errors = [r for r in results if not r.passed and r.severity == "error"]
                if errors:
                    print(f"  • {book_name}: {len(errors)} errors")
        else:
            print("\n✅ ALL VALIDATIONS PASSED!")
            
            if total_warnings > 0:
                print(f"\n⚠️  {total_warnings} warnings found (non-critical)")


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
            print(f"\n✅ PASSED")
            return 0
    else:
        # Validate all books
        total, passed, failed = validator.validate_all()
        validator.print_summary(total, passed, failed)
        
        return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit(main())
