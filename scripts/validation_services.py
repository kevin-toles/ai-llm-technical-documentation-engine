"""
Validation Service Layer for Metadata Extraction

Architecture Pattern: Service Layer + Strategy Pattern
Reference: Architecture Patterns Ch. 4 (Service Layer), Ch. 13 (Strategy Pattern)

Services:
- ChapterFieldValidator: Validates individual chapter fields
- ChapterDataQualityValidator: Validates data quality (lengths, sizes)
- ChapterNumberValidator: Validates chapter numbering sequences
- PageRangeValidator: Validates page range logic
- SourceValidator: Cross-references with source JSON
- BookMetadataLoader: Loads metadata and source files
- BookValidator: Orchestrates complete book validation
- ValidationResultFormatter: Formats and prints validation results
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of a validation check"""
    passed: bool
    message: str
    severity: str = "error"  # error, warning, info


class ChapterFieldValidator:
    """
    Validates required fields and types for a chapter.
    
    Pattern: Extract Method (Python Distilled Ch. 16)
    Reduces complexity by separating field validation logic.
    """
    
    REQUIRED_FIELDS = ['chapter_number', 'title', 'start_page', 'end_page', 'summary', 'keywords', 'concepts']
    MIN_SUMMARY_LENGTH = 20
    MAX_TITLE_LENGTH = 200
    
    @staticmethod
    def validate_required_fields(chapter: Dict[str, Any], idx: int) -> List[ValidationResult]:
        """Check all required fields are present"""
        missing_fields = [f for f in ChapterFieldValidator.REQUIRED_FIELDS if f not in chapter]
        
        if missing_fields:
            return [ValidationResult(
                False,
                f"Chapter {idx}: Missing required fields: {', '.join(missing_fields)}",
                "error"
            )]
        return []
    
    @staticmethod
    def validate_chapter_number(chapter: Dict[str, Any], idx: int) -> List[ValidationResult]:
        """Validate chapter_number field"""
        results = []
        
        if 'chapter_number' not in chapter:
            return results
        
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
        
        return results
    
    @staticmethod
    def validate_title(chapter: Dict[str, Any], idx: int) -> List[ValidationResult]:
        """Validate title field"""
        results = []
        
        if 'title' not in chapter:
            return results
        
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
        elif len(chapter['title']) > ChapterFieldValidator.MAX_TITLE_LENGTH:
            results.append(ValidationResult(
                False,
                f"Chapter {idx}: title too long ({len(chapter['title'])} chars, max {ChapterFieldValidator.MAX_TITLE_LENGTH})",
                "warning"
            ))
        
        return results
    
    @staticmethod
    def validate_page_numbers(chapter: Dict[str, Any], idx: int, total_pages: int) -> List[ValidationResult]:
        """Validate start_page and end_page fields"""
        results = []
        
        if 'start_page' not in chapter or 'end_page' not in chapter:
            return results
        
        # Type validation
        if not isinstance(chapter['start_page'], int) or not isinstance(chapter['end_page'], int):
            results.append(ValidationResult(
                False,
                f"Chapter {idx}: start_page and end_page must be integers",
                "error"
            ))
            return results
        
        # Positive validation
        if chapter['start_page'] <= 0 or chapter['end_page'] <= 0:
            results.append(ValidationResult(
                False,
                f"Chapter {idx}: page numbers must be positive",
                "error"
            ))
            return results
        
        # Range validation
        if chapter['start_page'] > chapter['end_page']:
            results.append(ValidationResult(
                False,
                f"Chapter {idx}: start_page ({chapter['start_page']}) > end_page ({chapter['end_page']})",
                "error"
            ))
        
        # Total pages validation
        if total_pages > 0 and chapter['end_page'] > total_pages:
            results.append(ValidationResult(
                False,
                f"Chapter {idx}: end_page ({chapter['end_page']}) exceeds total pages ({total_pages})",
                "warning"
            ))
        
        return results
    
    @staticmethod
    def validate_summary(chapter: Dict[str, Any], idx: int) -> List[ValidationResult]:
        """Validate summary field"""
        results = []
        
        if 'summary' not in chapter:
            return results
        
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
        elif len(chapter['summary']) < ChapterFieldValidator.MIN_SUMMARY_LENGTH:
            results.append(ValidationResult(
                False,
                f"Chapter {idx}: summary too short ({len(chapter['summary'])} chars, min {ChapterFieldValidator.MIN_SUMMARY_LENGTH})",
                "warning"
            ))
        
        return results
    
    @staticmethod
    def validate_keywords(chapter: Dict[str, Any], idx: int) -> List[ValidationResult]:
        """Validate keywords field"""
        results = []
        
        if 'keywords' not in chapter:
            return results
        
        if not isinstance(chapter['keywords'], list):
            results.append(ValidationResult(
                False,
                f"Chapter {idx}: keywords must be list",
                "error"
            ))
            return results
        
        if len(chapter['keywords']) == 0:
            results.append(ValidationResult(
                False,
                f"Chapter {idx}: no keywords extracted",
                "warning"
            ))
            return results
        
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
        
        return results
    
    @staticmethod
    def validate_concepts(chapter: Dict[str, Any], idx: int) -> List[ValidationResult]:
        """Validate concepts field"""
        results = []
        
        if 'concepts' not in chapter:
            return results
        
        if not isinstance(chapter['concepts'], list):
            results.append(ValidationResult(
                False,
                f"Chapter {idx}: concepts must be list",
                "error"
            ))
            return results
        
        # Empty concepts handling
        if len(chapter['concepts']) == 0:
            summary_length = len(chapter.get('summary', ''))
            if summary_length < 50:
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
            return results
        
        # Type validation
        non_string_concepts = [c for c in chapter['concepts'] if not isinstance(c, str)]
        if non_string_concepts:
            results.append(ValidationResult(
                False,
                f"Chapter {idx}: concepts must be strings, found {len(non_string_concepts)} non-strings",
                "error"
            ))
        
        return results


class ChapterValidator:
    """
    Main service for validating a single chapter.
    
    Pattern: Service Layer + Facade (delegates to specific validators)
    Reference: Architecture Patterns Ch. 4
    """
    
    def __init__(self):
        self.field_validator = ChapterFieldValidator()
    
    def validate(self, chapter: Dict[str, Any], idx: int, total_pages: int) -> List[ValidationResult]:
        """
        Validate a single chapter (refactored from CC 34).
        
        Delegates to specialized validators for each field type.
        """
        results = []
        
        # Required fields check (early return if missing)
        missing_fields_results = self.field_validator.validate_required_fields(chapter, idx)
        if missing_fields_results:
            return missing_fields_results
        
        # Delegate to field validators
        results.extend(self.field_validator.validate_chapter_number(chapter, idx))
        results.extend(self.field_validator.validate_title(chapter, idx))
        results.extend(self.field_validator.validate_page_numbers(chapter, idx, total_pages))
        results.extend(self.field_validator.validate_summary(chapter, idx))
        results.extend(self.field_validator.validate_keywords(chapter, idx))
        results.extend(self.field_validator.validate_concepts(chapter, idx))
        
        return results


class ChapterNumberValidator:
    """
    Validates chapter numbering sequences.
    
    Pattern: Strategy Pattern (one validation strategy)
    """
    
    @staticmethod
    def validate(chapter_numbers: List[int]) -> List[ValidationResult]:
        """Validate chapter numbering is sequential and unique"""
        results = []
        
        if not chapter_numbers:
            return results
        
        # Check for duplicates
        from collections import Counter
        duplicates = [num for num, count in Counter(chapter_numbers).items() if count > 1]
        if duplicates:
            results.append(ValidationResult(
                False,
                f"Duplicate chapter numbers: {duplicates}",
                "error"
            ))
        
        # Check if sequential
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


class PageRangeValidator:
    """
    Validates page ranges don't overlap.
    
    Pattern: Strategy Pattern (one validation strategy)
    """
    
    @staticmethod
    def validate(page_ranges: List[Tuple[int, int]]) -> List[ValidationResult]:
        """Validate page ranges don't overlap"""
        results = []
        
        if len(page_ranges) < 2:
            return results
        
        # Sort by start_page
        sorted_ranges = sorted(page_ranges)
        
        for i in range(len(sorted_ranges) - 1):
            curr_start, curr_end = sorted_ranges[i]
            next_start, next_end = sorted_ranges[i + 1]
            
            # Check for overlap
            if curr_end >= next_start:
                results.append(ValidationResult(
                    False,
                    f"Overlapping page ranges: ({curr_start}-{curr_end}) and ({next_start}-{next_end})",
                    "error"
                ))
        
        return results


class SourceValidator:
    """
    Cross-references metadata with source JSON.
    
    Pattern: Strategy Pattern (one validation strategy)
    """
    
    @staticmethod
    def validate(metadata: List[Dict], source_chapters: List[Dict]) -> List[ValidationResult]:
        """Cross-reference with source JSON chapters"""
        results = []
        
        metadata_count = len(metadata)
        source_count = len(source_chapters)
        
        if source_count == 0:
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


class BookMetadataLoader:
    """
    Loads and validates book metadata files.
    
    Pattern: Single Responsibility (file I/O separation)
    """
    
    @staticmethod
    def load_metadata(metadata_file: Path) -> Tuple[List[ValidationResult], List[Dict]]:
        """
        Load metadata from file.
        
        Returns:
            (results, metadata_list)
        """
        results = []
        
        # File existence and JSON validity
        try:
            with open(metadata_file) as f:
                metadata = json.load(f)
        except FileNotFoundError:
            results.append(ValidationResult(False, "Metadata file not found", "error"))
            return results, []
        except json.JSONDecodeError as e:
            results.append(ValidationResult(False, f"Invalid JSON: {e}", "error"))
            return results, []
        
        results.append(ValidationResult(True, "File exists and JSON is valid", "info"))
        
        # Type validation
        if not isinstance(metadata, list):
            results.append(ValidationResult(
                False, 
                f"Metadata must be a list, got {type(metadata).__name__}", 
                "error"
            ))
            return results, []
        
        if len(metadata) == 0:
            results.append(ValidationResult(False, "Metadata is empty (0 chapters)", "error"))
            return results, []
        
        results.append(ValidationResult(True, f"Contains {len(metadata)} chapters", "info"))
        
        return results, metadata
    
    @staticmethod
    def load_source_json(source_dir: Path, book_name: str) -> Tuple[List[ValidationResult], List[Dict], int]:
        """
        Load source JSON for cross-reference.
        
        Returns:
            (results, source_chapters, source_pages)
        """
        results = []
        source_file = source_dir / f"{book_name}.json"
        source_chapters = []
        source_pages = 0
        
        if source_file.exists():
            try:
                with open(source_file) as f:
                    source_data = json.load(f)
                    source_chapters = source_data.get('chapters', [])
                    source_pages = len(source_data.get('pages', []))
                results.append(ValidationResult(
                    True, 
                    f"Source JSON found: {len(source_chapters)} chapters, {source_pages} pages", 
                    "info"
                ))
            except Exception as e:
                results.append(ValidationResult(False, f"Failed to load source JSON: {e}", "warning"))
        else:
            results.append(ValidationResult(False, f"Source JSON not found: {source_file}", "warning"))
        
        return results, source_chapters, source_pages


class BookValidator:
    """
    Orchestrates validation of a complete book.
    
    Pattern: Service Layer + Facade (coordinates multiple validators)
    """
    
    def __init__(self, source_dir: Path):
        self.source_dir = source_dir
        self.chapter_validator = ChapterValidator()
    
    def validate(self, metadata_file: Path, book_name: str) -> List[ValidationResult]:
        """
        Validate a single book (refactored from CC 12).
        
        Delegates to specialized services for loading and validation.
        """
        results = []
        
        # Load metadata
        load_results, metadata = BookMetadataLoader.load_metadata(metadata_file)
        results.extend(load_results)
        
        if not metadata:
            return results
        
        # Load source JSON
        source_results, source_chapters, source_pages = BookMetadataLoader.load_source_json(
            self.source_dir, book_name
        )
        results.extend(source_results)
        
        # Validate each chapter and collect data
        chapter_numbers = []
        page_ranges = []
        
        for idx, chapter in enumerate(metadata):
            chapter_results = self.chapter_validator.validate(chapter, idx + 1, source_pages)
            results.extend(chapter_results)
            
            # Collect for cross-chapter validation
            if 'chapter_number' in chapter:
                chapter_numbers.append(chapter['chapter_number'])
            if 'start_page' in chapter and 'end_page' in chapter:
                page_ranges.append((chapter['start_page'], chapter['end_page']))
        
        # Cross-chapter validations
        results.extend(ChapterNumberValidator.validate(chapter_numbers))
        results.extend(PageRangeValidator.validate(page_ranges))
        
        # Cross-reference with source
        if source_chapters:
            results.extend(SourceValidator.validate(metadata, source_chapters))
        
        return results


class ValidationResultFormatter:
    """
    Formats and prints validation results.
    
    Pattern: Single Responsibility Principle (formatting only)
    """
    
    @staticmethod
    def get_icon(result: ValidationResult) -> str:
        """Get icon for validation result"""
        if result.passed:
            return "✅"
        return "⚠️" if result.severity == "warning" else "❌"
    
    @staticmethod
    def print_results(results: List[ValidationResult], verbose: bool = False):
        """Print validation results"""
        if verbose:
            for result in results:
                icon = ValidationResultFormatter.get_icon(result)
                print(f"  {icon} {result.message}")
        else:
            # Only print errors and warnings in non-verbose mode
            for result in results:
                if not result.passed:
                    icon = ValidationResultFormatter.get_icon(result)
                    print(f"    {icon} {result.message}")
    
    @staticmethod
    def count_errors_and_warnings(results: List[ValidationResult]) -> Tuple[int, int]:
        """Count errors and warnings in results"""
        errors = sum(1 for r in results if not r.passed and r.severity == "error")
        warnings = sum(1 for r in results if not r.passed and r.severity == "warning")
        return errors, warnings
    
    @staticmethod
    def print_book_status(book_name: str, errors: int, warnings: int, verbose: bool):
        """Print status for a single book"""
        if errors > 0:
            if not verbose:
                print(f"❌ FAILED ({errors} errors, {warnings} warnings)")
        else:
            if not verbose:
                print(f"✅ PASSED ({warnings} warnings)")
    
    @staticmethod
    def print_summary_header():
        """Print summary header"""
        print("\n" + "="*80)
        print("VALIDATION SUMMARY")
        print("="*80)
    
    @staticmethod
    def print_summary_statistics(total: int, passed: int, failed: int, total_errors: int, total_warnings: int):
        """Print summary statistics"""
        print(f"\n  Total books validated: {total}")
        print(f"  ✅ Passed: {passed} ({passed/total*100:.1f}%)")
        print(f"  ❌ Failed: {failed} ({failed/total*100:.1f}%)")
        print(f"\n  Total errors: {total_errors}")
        print(f"  Total warnings: {total_warnings}")
    
    @staticmethod
    def print_failed_books(results_dict: Dict[str, List[ValidationResult]]):
        """Print list of books with errors"""
        print("\n❌ VALIDATION FAILED")
        print("\nBooks with errors:")
        for book_name, results in results_dict.items():
            errors = sum(1 for r in results if not r.passed and r.severity == "error")
            if errors > 0:
                print(f"  • {book_name}: {errors} errors")
    
    @staticmethod
    def print_success_message(total_warnings: int):
        """Print success message"""
        print("\n✅ ALL VALIDATIONS PASSED!")
        
        if total_warnings > 0:
            print(f"\n⚠️  {total_warnings} warnings found (non-critical)")
