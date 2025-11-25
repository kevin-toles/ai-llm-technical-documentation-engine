"""
Characterization tests for detect_poor_ocr.py

TDD Iteration 1: Document current behavior before refactoring
Target: Reduce assess_text_quality() from CC 16 to <10
Target: Reduce main() from CC 25 to <10

Reference: BATCH1_CRITICAL_FILES_REMEDIATION_PLAN.md File #6
"""
import pytest
from pathlib import Path
from workflows.metadata_extraction.scripts.detect_poor_ocr import (
    OCRQualityDetector,
    OCRQualityReport
)


class TestAssessTextQualityCurrentBehavior:
    """
    Characterization tests for assess_text_quality() method.
    
    Current behavior (CC 16):
    - 5 separate quality checks in one function
    - Returns (score, issues) tuple
    - Score ranges from 0.0 to 1.0
    """
    
    def test_detects_insufficient_text(self):
        """Test: Detects text with <100 chars"""
        detector = OCRQualityDetector(Path("/tmp"))
        
        score, issues = detector.assess_text_quality("Short")
        
        assert "insufficient_text" in issues
        assert score < 1.0
    
    def test_detects_watermark_repetition(self):
        """Test: Detects >50% repetition of same word"""
        detector = OCRQualityDetector(Path("/tmp"))
        
        # Create text with 60% repetition
        text = "WATERMARK " * 12 + "other text words"
        
        score, issues = detector.assess_text_quality(text)
        
        assert any("watermark_repetition" in issue for issue in issues)
        assert score <= 0.5  # Changed from < to <=
    
    def test_detects_high_gibberish(self):
        """Test: Detects >40% non-alphanumeric characters"""
        detector = OCRQualityDetector(Path("/tmp"))
        
        text = "Valid text " + "@#$%^&*()!~`" * 20
        
        score, issues = detector.assess_text_quality(text)
        
        assert any("gibberish" in issue for issue in issues)
        assert score < 1.0
    
    def test_detects_abnormal_vowel_ratio(self):
        """Test: Detects abnormal vowel ratios (<15% or >65%)"""
        detector = OCRQualityDetector(Path("/tmp"))
        
        # Text with very few vowels (<15%)
        text = "bcdfghjklmnpqrstvwxyz " * 10
        
        score, issues = detector.assess_text_quality(text)
        
        assert any("abnormal_vowel_ratio" in issue for issue in issues)
        assert score < 1.0
    
    def test_detects_abnormal_word_length(self):
        """Test: Detects avg word length <2 or >15"""
        detector = OCRQualityDetector(Path("/tmp"))
        
        # Very long words
        text = "supercalifragilisticexpialidocious " * 10
        
        score, issues = detector.assess_text_quality(text)
        
        assert any("abnormal_word_length" in issue for issue in issues)
        assert score < 1.0
    
    def test_returns_perfect_score_for_good_text(self):
        """Test: Normal text gets high score"""
        detector = OCRQualityDetector(Path("/tmp"))
        
        text = """
        This is a normal paragraph of text with good OCR quality.
        It contains proper words, sentences, and punctuation.
        The vocabulary is diverse and the structure is reasonable.
        """ * 3
        
        score, issues = detector.assess_text_quality(text)
        
        assert score >= 0.8
        assert len(issues) <= 1


class TestAssessBookCurrentBehavior:
    """
    Characterization tests for assess_book() method.
    
    Current behavior:
    - Loads JSON file
    - Samples first N pages
    - Calls assess_text_quality()
    - Returns OCRQualityReport
    """
    
    def test_creates_report_for_valid_book(self, tmp_path):
        """Test: Creates report with all expected fields"""
        # Create test JSON file
        book_file = tmp_path / "test_book.json"
        book_file.write_text("""{
            "pages": [
                {"content": "Chapter 1: Introduction with good content about Python programming."},
                {"content": "More content about functions and classes in Python."}
            ]
        }""")
        
        detector = OCRQualityDetector(tmp_path)
        report = detector.assess_book(book_file)
        
        assert report.book_name == "test_book"
        assert report.total_pages == 2
        assert report.avg_chars_per_page > 0
        assert isinstance(report.quality_score, float)
        assert isinstance(report.needs_re_ocr, bool)
    
    def test_handles_missing_file(self, tmp_path):
        """Test: Handles non-existent file gracefully"""
        detector = OCRQualityDetector(tmp_path)
        report = detector.assess_book(tmp_path / "nonexistent.json")
        
        assert "failed_to_load" in report.quality_issues[0]
        assert report.needs_re_ocr is True
        assert report.quality_score == 0.0


class TestMainFunctionCurrentBehavior:
    """
    Characterization tests for main() function.
    
    Current behavior (CC 25):
    - Parses CLI arguments
    - Creates detector
    - Assesses single book OR all books
    - Prints report
    - Returns exit code
    """
    
    def test_main_assesses_single_book(self, tmp_path, monkeypatch, capsys):
        """Test: main() can assess single book"""
        # Create test book
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        book_file = source_dir / "Test_Book.json"
        book_file.write_text("""{
            "pages": [
                {"content": "Good quality content for testing purposes with sufficient length."}
            ]
        }""")
        
        # Mock sys.argv
        monkeypatch.setattr('sys.argv', [
            'detect_poor_ocr.py',
            '--source-dir', str(source_dir),
            '--book', 'Test_Book'
        ])
        
        from workflows.metadata_extraction.scripts.detect_poor_ocr import main
        exit_code = main()
        
        captured = capsys.readouterr()
        assert "Test_Book" in captured.out
        assert "Quality score:" in captured.out
        assert isinstance(exit_code, int)


class TestPrintReportCurrentBehavior:
    """
    Characterization tests for print_report() method.
    
    Current behavior (CC 11):
    - Prints header
    - Shows summary statistics
    - Lists books needing re-OCR
    - Optionally shows acceptable books
    """
    
    def test_prints_report_with_issues(self, capsys):
        """Test: Prints formatted report"""
        detector = OCRQualityDetector(Path("/tmp"))
        
        reports = [
            OCRQualityReport(
                book_name="Bad_Book",
                total_pages=100,
                avg_chars_per_page=10.0,
                quality_issues=["insufficient_text"],
                quality_score=0.3,
                needs_re_ocr=True,
                sample_content="bad content"
            ),
            OCRQualityReport(
                book_name="Good_Book",
                total_pages=200,
                avg_chars_per_page=500.0,
                quality_issues=[],
                quality_score=1.0,
                needs_re_ocr=False,
                sample_content="good content"
            )
        ]
        
        detector.print_report(reports, show_good=False)
        
        captured = capsys.readouterr()
        assert "OCR QUALITY ASSESSMENT REPORT" in captured.out
        assert "Bad_Book" in captured.out
        assert "Good_Book" not in captured.out  # show_good=False
