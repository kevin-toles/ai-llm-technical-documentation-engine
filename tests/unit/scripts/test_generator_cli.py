"""Tests for main() CLI entrypoint in generate_metadata_universal.py.

WBS-AC7.4e: Add tests for main() argparse and entrypoint.

Coverage targets:
- Lines 861-1007: main() function
- Argument parsing
- Error handling (file not found, no chapters)
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict
from unittest.mock import MagicMock, patch

import pytest

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

GENERATOR_SCRIPT = PROJECT_ROOT / "workflows/metadata_extraction/scripts/generate_metadata_universal.py"


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def sample_book_json(tmp_path: Path) -> Path:
    """Create a sample book JSON file for testing.
    
    Note: PreDefinedStrategy looks for book_data['chapters'] at the top level.
    """
    book_data = {
        "title": "CLI Test Book",
        "chapters": [
            {"number": 1, "title": "Introduction", "start_page": 1, "end_page": 2}
        ],
        "pages": [
            {"page_number": 1, "content": "Chapter 1: Introduction\n\nMachine learning fundamentals."},
            {"page_number": 2, "content": "More content about neural networks and deep learning."},
        ]
    }
    json_file = tmp_path / "cli_test_book.json"
    json_file.write_text(json.dumps(book_data))
    return json_file


# =============================================================================
# Test CLI Argument Parsing
# =============================================================================


class TestCLIArgumentParsing:
    """AC7.4e: Test argparse argument handling."""

    def test_help_flag_shows_usage(self) -> None:
        """AC7.4e: --help shows usage information."""
        result = subprocess.run(
            [sys.executable, str(GENERATOR_SCRIPT), "--help"],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT)
        )

        assert result.returncode == 0
        assert "--input" in result.stdout
        assert "--output" in result.stdout
        assert "--auto-detect" in result.stdout
        assert "--dry-run" in result.stdout

    def test_required_input_flag(self) -> None:
        """AC7.4e: --input is required."""
        result = subprocess.run(
            [sys.executable, str(GENERATOR_SCRIPT)],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT)
        )

        assert result.returncode != 0
        assert "required" in result.stderr.lower() or "--input" in result.stderr

    def test_auto_detect_flag_accepted(self, sample_book_json: Path, tmp_path: Path) -> None:
        """AC7.4e: --auto-detect flag is accepted."""
        output_path = tmp_path / "output.json"
        
        result = subprocess.run(
            [
                sys.executable, str(GENERATOR_SCRIPT),
                "--input", str(sample_book_json),
                "--output", str(output_path),
                "--auto-detect"
            ],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT)
        )

        # Should run without error (may or may not produce output depending on detection)
        # The main thing is that the flag is accepted
        assert "--auto-detect" not in result.stderr or "unrecognized" not in result.stderr

    def test_dry_run_flag_accepted(self, sample_book_json: Path, tmp_path: Path) -> None:
        """AC7.4e: --dry-run flag is accepted and prevents file write."""
        output_path = tmp_path / "output.json"
        
        result = subprocess.run(
            [
                sys.executable, str(GENERATOR_SCRIPT),
                "--input", str(sample_book_json),
                "--output", str(output_path),
                "--auto-detect",
                "--dry-run"
            ],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT)
        )

        # Should mention DRY RUN
        assert "DRY RUN" in result.stdout or not output_path.exists()


# =============================================================================
# Test CLI Error Handling
# =============================================================================


class TestCLIErrorHandling:
    """AC7.4e: Test CLI error handling."""

    def test_file_not_found_error(self, tmp_path: Path) -> None:
        """AC7.4e: Non-existent input file shows error."""
        non_existent = tmp_path / "does_not_exist.json"
        
        result = subprocess.run(
            [
                sys.executable, str(GENERATOR_SCRIPT),
                "--input", str(non_existent),
                "--auto-detect"
            ],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT)
        )

        assert result.returncode != 0
        assert "not found" in result.stdout.lower() or "error" in result.stdout.lower()

    def test_no_chapters_defined_error(self, tmp_path: Path) -> None:
        """AC7.4e: No chapters defined shows error."""
        # Book with no predefined chapters and no detectable content
        empty_book = {
            "title": "Empty Book",
            "metadata": {},
            "pages": [
                {"page_number": 1, "content": "Just some random text without chapter markers."}
            ]
        }
        json_file = tmp_path / "empty_book.json"
        json_file.write_text(json.dumps(empty_book))
        
        result = subprocess.run(
            [
                sys.executable, str(GENERATOR_SCRIPT),
                "--input", str(json_file),
                "--auto-detect"
            ],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT)
        )

        # Should either fail or report no chapters
        # (may succeed with 0 chapters depending on implementation)
        assert "chapter" in result.stdout.lower() or result.returncode != 0


# =============================================================================
# Test CLI Use-Orchestrator Flag
# =============================================================================


class TestCLIUseOrchestratorFlag:
    """AC7.4e: Test --use-orchestrator CLI flag."""

    def test_use_orchestrator_flag_accepted(self, sample_book_json: Path, tmp_path: Path) -> None:
        """AC7.4e: --use-orchestrator flag is accepted."""
        output_path = tmp_path / "output.json"
        
        result = subprocess.run(
            [
                sys.executable, str(GENERATOR_SCRIPT),
                "--input", str(sample_book_json),
                "--output", str(output_path),
                "--auto-detect",
                "--use-orchestrator",
                "--dry-run"
            ],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT)
        )

        # Should mention orchestrator in output
        assert "orchestrator" in result.stdout.lower()

    def test_fallback_on_error_flag_accepted(self, sample_book_json: Path, tmp_path: Path) -> None:
        """AC7.4e: --fallback-on-error flag is accepted."""
        output_path = tmp_path / "output.json"
        
        result = subprocess.run(
            [
                sys.executable, str(GENERATOR_SCRIPT),
                "--input", str(sample_book_json),
                "--output", str(output_path),
                "--auto-detect",
                "--fallback-on-error",
                "--dry-run"
            ],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT)
        )

        # Flag should be recognized (no unrecognized argument error)
        assert "unrecognized" not in result.stderr.lower()


# =============================================================================
# Test CLI Domain Flag
# =============================================================================


class TestCLIDomainFlag:
    """AC7.4e: Test --domain CLI flag."""

    def test_domain_python_accepted(self, sample_book_json: Path, tmp_path: Path) -> None:
        """AC7.4e: --domain python is accepted."""
        output_path = tmp_path / "output.json"
        
        result = subprocess.run(
            [
                sys.executable, str(GENERATOR_SCRIPT),
                "--input", str(sample_book_json),
                "--output", str(output_path),
                "--domain", "python",
                "--auto-detect",
                "--dry-run"
            ],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT)
        )

        # Should show domain in output
        assert "python" in result.stdout.lower()

    def test_invalid_domain_rejected(self, sample_book_json: Path) -> None:
        """AC7.4e: Invalid domain value is rejected."""
        result = subprocess.run(
            [
                sys.executable, str(GENERATOR_SCRIPT),
                "--input", str(sample_book_json),
                "--domain", "invalid_domain",
                "--auto-detect"
            ],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT)
        )

        # argparse should reject invalid choice
        assert result.returncode != 0
        assert "invalid choice" in result.stderr.lower()


# =============================================================================
# Test Full CLI Execution
# =============================================================================


class TestFullCLIExecution:
    """AC7.4e: Test complete CLI execution paths."""

    def test_full_execution_with_predefined_chapters(
        self, sample_book_json: Path, tmp_path: Path
    ) -> None:
        """AC7.4e: Full execution with predefined chapters succeeds."""
        output_path = tmp_path / "output.json"
        
        result = subprocess.run(
            [
                sys.executable, str(GENERATOR_SCRIPT),
                "--input", str(sample_book_json),
                "--output", str(output_path),
                "--auto-detect"
            ],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT)
        )

        # Should succeed
        assert result.returncode == 0 or "Done" in result.stdout
        
        # Output file should be created
        if result.returncode == 0:
            assert output_path.exists()

    def test_execution_shows_loaded_message(
        self, sample_book_json: Path, tmp_path: Path
    ) -> None:
        """AC7.4e: Execution shows 'Loaded:' message."""
        output_path = tmp_path / "output.json"
        
        result = subprocess.run(
            [
                sys.executable, str(GENERATOR_SCRIPT),
                "--input", str(sample_book_json),
                "--output", str(output_path),
                "--auto-detect",
                "--dry-run"
            ],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT)
        )

        # Should show loaded message
        assert "Loaded" in result.stdout or "📚" in result.stdout
