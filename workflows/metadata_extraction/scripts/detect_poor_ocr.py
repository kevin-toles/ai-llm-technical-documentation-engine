#!/usr/bin/env python3
"""
Poor OCR Detection and Reporting Script

Analyzes source JSON files to detect poor OCR quality that will prevent
effective metadata extraction. Identifies books that need re-OCR.

Detection criteria:
1. Watermark repetition (>50% same word)
2. Insufficient text (<10 chars/page average)
3. High gibberish ratio (>30% non-alphanumeric)
4. Poor language structure (abnormal vowel ratios)
5. No meaningful content in sample pages

Usage:
    python3 detect_poor_ocr.py
    python3 detect_poor_ocr.py --book "Game Programming Gems 4"
    python3 detect_poor_ocr.py --report-only
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple
from collections import Counter
from dataclasses import dataclass


@dataclass
class OCRQualityReport:
    """OCR quality assessment result"""
    book_name: str
    total_pages: int
    avg_chars_per_page: float
    quality_issues: List[str]
    quality_score: float  # 0.0 (worst) to 1.0 (best)
    needs_re_ocr: bool
    sample_content: str


class OCRQualityDetector:
    """Detects poor OCR quality in source JSON files"""
    
    def __init__(self, source_dir: Path, sample_pages: int = 10):
        self.source_dir = source_dir
        self.sample_pages = sample_pages
    
    def _check_insufficient_text(self, text: str, score: float) -> Tuple[float, List[str]]:
        """Check 1: Insufficient text (<100 chars)"""
        if len(text) < 100:
            return score - 0.4, ["insufficient_text"]
        return score, []
    
    def _check_watermark_repetition(self, text: str, score: float) -> Tuple[float, List[str]]:
        """Check 2: Repetitive watermarks/noise (>50% same word)"""
        issues = []
        words = text.split()
        
        if len(words) > 10:
            word_counts = Counter(words)
            most_common = word_counts.most_common(1)[0]
            repetition_ratio = most_common[1] / len(words)
            
            if repetition_ratio > 0.5:
                issues.append(f"watermark_repetition ({most_common[0]}: {repetition_ratio:.1%})")
                score -= 0.5
            elif repetition_ratio > 0.3:
                issues.append(f"high_repetition ({repetition_ratio:.1%})")
                score -= 0.2
        
        return score, issues
    
    def _check_gibberish_ratio(self, text: str, score: float) -> Tuple[float, List[str]]:
        """Check 3: Gibberish (high ratio of non-alphanumeric)"""
        issues = []
        alphanumeric = sum(c.isalnum() or c.isspace() for c in text)
        gibberish_ratio = 1 - (alphanumeric / len(text))
        
        if gibberish_ratio > 0.4:
            issues.append(f"high_gibberish ({gibberish_ratio:.1%})")
            score -= 0.3
        elif gibberish_ratio > 0.2:
            issues.append(f"moderate_gibberish ({gibberish_ratio:.1%})")
            score -= 0.1
        
        return score, issues
    
    def _check_vowel_ratio(self, text: str, score: float) -> Tuple[float, List[str]]:
        """Check 4: Poor language structure (abnormal vowel ratio)"""
        issues = []
        text_no_spaces = text.replace(' ', '').replace('\n', '')
        
        if len(text_no_spaces) > 0:
            vowels = sum(1 for c in text_no_spaces.lower() if c in 'aeiou')
            vowel_ratio = vowels / len(text_no_spaces)
            
            # Normal English: 35-45% vowels
            if vowel_ratio < 0.15 or vowel_ratio > 0.65:
                issues.append(f"abnormal_vowel_ratio ({vowel_ratio:.1%})")
                score -= 0.2
        
        return score, issues
    
    def _check_word_length(self, text: str, score: float) -> Tuple[float, List[str]]:
        """Check 5: Average word length (too short or too long suggests OCR issues)"""
        issues = []
        words = text.split()
        
        if len(words) > 5:
            avg_word_len = sum(len(w) for w in words) / len(words)
            if avg_word_len < 2 or avg_word_len > 15:
                issues.append(f"abnormal_word_length (avg: {avg_word_len:.1f})")
                score -= 0.1
        
        return score, issues
    
    def assess_text_quality(self, text: str) -> Tuple[float, List[str]]:
        """
        Assess text quality using 5 separate checks (CC: 16 → 2).
        
        Applies Extract Method pattern (Learning Python Ed6 Ch. 16) to reduce
        cognitive complexity and improve testability.
        
        Returns:
            (quality_score, issues_list)
        """
        score = 1.0
        all_issues = []
        
        # Run all quality checks
        score, issues = self._check_insufficient_text(text, score)
        if issues:  # Early return if insufficient text
            return max(0.0, score), issues
        
        score, issues = self._check_watermark_repetition(text, score)
        all_issues.extend(issues)
        
        score, issues = self._check_gibberish_ratio(text, score)
        all_issues.extend(issues)
        
        score, issues = self._check_vowel_ratio(text, score)
        all_issues.extend(issues)
        
        score, issues = self._check_word_length(text, score)
        all_issues.extend(issues)
        
        return max(0.0, score), all_issues
    
    def assess_book(self, book_file: Path) -> OCRQualityReport:
        """Assess OCR quality for a single book"""
        try:
            with open(book_file) as f:
                data = json.load(f)
        except Exception as e:
            return OCRQualityReport(
                book_name=book_file.stem,
                total_pages=0,
                avg_chars_per_page=0.0,
                quality_issues=[f"failed_to_load: {e}"],
                quality_score=0.0,
                needs_re_ocr=True,
                sample_content=""
            )
        
        pages = data.get('pages', [])
        book_name = book_file.stem
        
        if not pages:
            return OCRQualityReport(
                book_name=book_name,
                total_pages=0,
                avg_chars_per_page=0.0,
                quality_issues=["no_pages"],
                quality_score=0.0,
                needs_re_ocr=True,
                sample_content=""
            )
        
        # Sample pages for assessment
        sample_size = min(self.sample_pages, len(pages))
        sample_pages = pages[:sample_size]
        
        # Collect text from sample
        sample_text = ""
        total_chars = 0
        
        for page in sample_pages:
            content = page.get('content', page.get('text', ''))
            sample_text += content + " "
            total_chars += len(content)
        
        avg_chars = total_chars / sample_size if sample_size > 0 else 0
        
        # Assess quality
        quality_score, issues = self.assess_text_quality(sample_text)
        
        # Determine if re-OCR needed
        needs_re_ocr = quality_score < 0.5 or avg_chars < 50
        
        return OCRQualityReport(
            book_name=book_name,
            total_pages=len(pages),
            avg_chars_per_page=avg_chars,
            quality_issues=issues,
            quality_score=quality_score,
            needs_re_ocr=needs_re_ocr,
            sample_content=sample_text[:200]
        )
    
    def assess_all_books(self) -> List[OCRQualityReport]:
        """Assess all books in source directory"""
        reports = []
        
        for book_file in sorted(self.source_dir.glob('*.json')):
            report = self.assess_book(book_file)
            reports.append(report)
        
        return reports
    
    def _print_summary_stats(self, reports: List[OCRQualityReport]):
        """Print summary statistics for OCR quality assessment."""
        needs_re_ocr = [r for r in reports if r.needs_re_ocr]
        acceptable = [r for r in reports if not r.needs_re_ocr]
        
        print(f"Total books assessed: {len(reports)}")
        print(f"  ✅ Acceptable quality: {len(acceptable)} ({len(acceptable)/len(reports)*100:.1f}%)")
        print(f"  ❌ Needs re-OCR: {len(needs_re_ocr)} ({len(needs_re_ocr)/len(reports)*100:.1f}%)")
    
    def _print_books_needing_reocr(self, reports: List[OCRQualityReport]):
        """Print details of books requiring re-OCR."""
        needs_re_ocr = [r for r in reports if r.needs_re_ocr]
        
        if needs_re_ocr:
            print("\n" + "="*80)
            print("BOOKS REQUIRING RE-OCR:")
            print("="*80 + "\n")
            
            for report in needs_re_ocr:
                print(f"❌ {report.book_name}")
                print(f"   Pages: {report.total_pages}")
                print(f"   Avg chars/page: {report.avg_chars_per_page:.1f}")
                print(f"   Quality score: {report.quality_score:.2f}")
                print(f"   Issues: {', '.join(report.quality_issues)}")
                print(f"   Sample: {report.sample_content[:100]}...")
                print()
    
    def _print_acceptable_books(self, reports: List[OCRQualityReport]):
        """Print details of books with acceptable OCR quality."""
        acceptable = [r for r in reports if not r.needs_re_ocr]
        
        if acceptable:
            print("\n" + "="*80)
            print("BOOKS WITH ACCEPTABLE OCR:")
            print("="*80 + "\n")
            
            for report in acceptable:
                print(f"✅ {report.book_name}")
                print(f"   Quality score: {report.quality_score:.2f}")
                if report.quality_issues:
                    print(f"   Minor issues: {', '.join(report.quality_issues)}")
                print()
    
    def print_report(self, reports: List[OCRQualityReport], show_good: bool = False):
        """Print formatted assessment report (refactored: CC 11 → <10)"""
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║                      OCR QUALITY ASSESSMENT REPORT                           ║")
        print("╚══════════════════════════════════════════════════════════════════════════════╝\n")
        
        self._print_summary_stats(reports)
        self._print_books_needing_reocr(reports)
        
        if show_good:
            self._print_acceptable_books(reports)


def _parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments (extracted from main)"""
    parser = argparse.ArgumentParser(
        description="Detect poor OCR quality in source JSON files",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--book', '-b',
        help='Assess specific book only'
    )
    
    parser.add_argument(
        '--source-dir',
        type=Path,
        default=Path('workflows/pdf_to_json/output/textbooks_json'),
        help='Directory containing source JSON files'
    )
    
    parser.add_argument(
        '--sample-pages',
        type=int,
        default=10,
        help='Number of pages to sample for assessment (default: 10)'
    )
    
    parser.add_argument(
        '--show-good',
        action='store_true',
        help='Also show books with acceptable OCR quality'
    )
    
    parser.add_argument(
        '--report-only',
        action='store_true',
        help='Only show books that need re-OCR'
    )
    
    return parser.parse_args()


def _assess_single_book(detector: OCRQualityDetector, book_file: Path) -> int:
    """Assess and report on a single book (extracted from main)"""
    report = detector.assess_book(book_file)
    
    print(f"\n=== {report.book_name} ===\n")
    print(f"Total pages: {report.total_pages}")
    print(f"Avg chars/page: {report.avg_chars_per_page:.1f}")
    print(f"Quality score: {report.quality_score:.2f}/1.00")
    print(f"Issues: {', '.join(report.quality_issues) if report.quality_issues else 'None'}")
    print(f"Needs re-OCR: {'YES ❌' if report.needs_re_ocr else 'NO ✅'}")
    print("\nSample content:")  # Fixed: removed unnecessary f-string
    print(report.sample_content[:300])
    
    return 1 if report.needs_re_ocr else 0


def _assess_all_books(detector: OCRQualityDetector, report_only: bool, show_good: bool) -> int:
    """Assess all books and generate report (extracted from main)"""
    reports = detector.assess_all_books()
    
    if report_only:
        # Only show books needing re-OCR
        needs_re_ocr = [r for r in reports if r.needs_re_ocr]
        if needs_re_ocr:
            print("BOOKS REQUIRING RE-OCR:\n")
            for report in needs_re_ocr:
                print(f"  • {report.book_name}")
                print(f"    Issues: {', '.join(report.quality_issues)}")
            print(f"\nTotal: {len(needs_re_ocr)} books need re-OCR")
        else:
            print("✅ All books have acceptable OCR quality")
        return len(needs_re_ocr)
    else:
        detector.print_report(reports, show_good=show_good)
        return 1 if any(r.needs_re_ocr for r in reports) else 0


def main():
    """
    Main entry point (CC: 25 → 5).
    
    Refactored using Extract Method pattern (Python Distilled Ch. 16) to reduce
    cognitive complexity and improve testability.
    """
    args = _parse_arguments()
    
    if not args.source_dir.exists():
        print(f"❌ Error: Source directory not found: {args.source_dir}")
        return 1
    
    detector = OCRQualityDetector(args.source_dir, args.sample_pages)
    
    if args.book:
        # Single book workflow
        book_file = args.source_dir / f"{args.book}.json"
        if not book_file.exists():
            print(f"❌ Error: Book not found: {book_file}")
            return 1
        return _assess_single_book(detector, book_file)
    else:
        # All books workflow
        return _assess_all_books(detector, args.report_only, args.show_good)


if __name__ == "__main__":
    exit(main())
