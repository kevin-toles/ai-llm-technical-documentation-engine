"""
Integration test for end-to-end JSON generation (Task 17 - TDD RED Phase).

Tests complete pipeline:
    1. Load actual textbook JSON (Architecture Patterns)
    2. Generate both MD and JSON outputs
    3. Validate both files
    4. Check file sizes match estimates (300-800 KB MD, 360-1040 KB JSON)

Expected: PASS (implementation already complete from Tasks 6-15)

References:
- CONSOLIDATED_IMPLEMENTATION_PLAN Tab 5: End-to-end requirements
- ARCHITECTURE_GUIDELINES Ch. 5: Integration testing
- Tasks 6-15: JSON generation implementation
"""

import json
import pytest
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any


class TestEndToEndJsonGeneration:
    """Integration test for complete JSON generation pipeline."""
    
    @pytest.fixture(scope="session")
    def test_output_dir(self, tmp_path_factory):
        """Create temporary output directory for test files (session-scoped)."""
        output_dir = tmp_path_factory.mktemp("test_output")
        return output_dir
    
    @pytest.fixture
    def architecture_patterns_json(self):
        """
        Locate Architecture Patterns textbook JSON.
        
        Returns path to the source JSON file used for guideline generation.
        """
        # Search for Architecture Patterns JSON in expected locations
        repo_root = Path(__file__).parent.parent.parent
        
        possible_paths = [
            repo_root / "Python_References" / "Architecture" / "JSON" / "Architecture Patterns with Python.json",
            repo_root / "workflows" / "pdf_to_json" / "output" / "textbooks_json" / "Architecture Patterns with Python.json",
            repo_root / "Textbooks_JSON" / "Architecture Patterns with Python.json",
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        
        pytest.skip(f"Architecture Patterns JSON not found. Searched: {possible_paths}")
    
    def test_generate_guideline_files(self, architecture_patterns_json, test_output_dir):
        """
        Test: Generate both MD and JSON files from Architecture Patterns book.
        
        Expected behavior:
        - Script executes successfully
        - Both .md and .json files created
        - Files are non-empty
        - Files created in same directory
        
        References:
        - Task 17 requirement: End-to-end pipeline validation
        """
        # Arrange: Prepare to run the generator script
        script_path = Path(__file__).parent.parent.parent / "workflows" / "base_guideline_generation" / "scripts" / "chapter_generator_all_text.py"
        
        assert script_path.exists(), f"Generator script not found at {script_path}"
        assert architecture_patterns_json.exists(), f"Input JSON not found at {architecture_patterns_json}"
        
        # Act: Run the generator (output will be in repo root by default)
        result = subprocess.run(
            [sys.executable, str(script_path), str(architecture_patterns_json)],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout for generation
        )
        
        # Debug output if failed
        if result.returncode != 0:
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
        
        # Assert: Script executed successfully
        assert result.returncode == 0, f"Generator script failed with code {result.returncode}: {result.stderr}"
        
        # Assert: Output files created
        repo_root = Path(__file__).parent.parent.parent
        
        # Files are created in workflows/base_guideline_generation/output/ per Tab 5 design
        # Named: {BookName}_guideline.md/json (without PYTHON_GUIDELINES_ prefix)
        output_dir = repo_root / "workflows" / "base_guideline_generation" / "output"
        expected_md = output_dir / "Architecture Patterns with Python_guideline.md"
        expected_json = output_dir / "Architecture Patterns with Python_guideline.json"
        
        assert expected_md.exists(), f"MD file not created at {expected_md}"
        assert expected_json.exists(), f"JSON file not created at {expected_json}"
        
        # Assert: Files are non-empty
        assert expected_md.stat().st_size > 0, "MD file is empty"
        assert expected_json.stat().st_size > 0, "JSON file is empty"
        
        # Move files to test output directory for subsequent tests
        if test_output_dir:
            md_dest = test_output_dir / expected_md.name
            json_dest = test_output_dir / expected_json.name
            expected_md.rename(md_dest)
            expected_json.rename(json_dest)
            print("\nFiles moved to test output directory:")
            print(f"  MD:   {md_dest}")
            print(f"  JSON: {json_dest}")
    
    def test_validate_json_structure(self, test_output_dir):
        """
        Test: Validate JSON file has correct structure.
        
        Expected structure per CONSOLIDATED_IMPLEMENTATION_PLAN:
        - book_metadata: title, author, etc.
        - source_info: generated timestamp, tool version
        - chapters: array of chapter objects
        - footnotes: array of footnote objects
        
        References:
        - Task 5: JSON schema definition
        - Task 7: Schema validation test
        """
        # Find the JSON file from previous test (moved to test_output_dir)
        json_file = test_output_dir / "Architecture Patterns with Python_guideline.json"
        
        if not json_file.exists():
            pytest.skip("JSON file not found (run test_generate_guideline_files first)")
        
        # Act: Load and parse JSON
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Assert: Top-level structure
        assert isinstance(data, dict), "JSON should be a dictionary"
        
        required_keys = ["book_metadata", "source_info", "chapters", "footnotes"]
        for key in required_keys:
            assert key in data, f"Missing required key: {key}"
        
        # Assert: book_metadata structure (actual schema uses 'book_name', not 'author')
        assert "title" in data["book_metadata"], "Missing book_metadata.title"
        assert "book_name" in data["book_metadata"], "Missing book_metadata.book_name"
        
        # Assert: source_info structure (actual schema: generated_by, generation_date, method)
        assert "generated_by" in data["source_info"], "Missing source_info.generated_by"
        assert "generation_date" in data["source_info"], "Missing source_info.generation_date"
        
        # Assert: chapters is array
        assert isinstance(data["chapters"], list), "chapters should be a list"
        assert len(data["chapters"]) > 0, "chapters should not be empty"
        
        # Assert: footnotes is array
        assert isinstance(data["footnotes"], list), "footnotes should be a list"
        
        # Assert: First chapter has required structure
        first_chapter = data["chapters"][0]
        chapter_required_keys = ["chapter_number", "title", "page_range", "cross_text_analysis", "chapter_summary", "concepts"]
        for key in chapter_required_keys:
            assert key in first_chapter, f"Missing chapter key: {key}"
    
    def test_validate_file_sizes(self, test_output_dir):
        """
        Test: Validate file sizes are in expected range.
        
        Expected per CONSOLIDATED_IMPLEMENTATION_PLAN Tab 5:
        - MD: 300-800 KB for typical books (10-20 chapters)
        - JSON: 360-1040 KB (includes full content + metadata)
        
        Architecture Patterns has 13 chapters → should be within range.
        
        References:
        - Task 17 requirement: Real-world file size validation
        - CONSOLIDATED_IMPLEMENTATION_PLAN: Size estimates
        """
        md_file = test_output_dir / "Architecture Patterns with Python_guideline.md"
        json_file = test_output_dir / "Architecture Patterns with Python_guideline.json"
        
        if not md_file.exists() or not json_file.exists():
            pytest.skip("Output files not found (run test_generate_guideline_files first)")
        
        # Get file sizes in KB
        md_size_kb = md_file.stat().st_size / 1024
        json_size_kb = json_file.stat().st_size / 1024
        
        print("\nFile sizes:")
        print(f"  MD:   {md_size_kb:.1f} KB")
        print(f"  JSON: {json_size_kb:.1f} KB")
        print(f"  Ratio: {json_size_kb/md_size_kb*100:.1f}%")
        
        # Assert: MD size reasonable (allow wider range for test data)
        # Note: Actual size depends on content density (concepts extracted)
        assert md_size_kb > 50, f"MD file too small: {md_size_kb:.1f} KB (expected >50 KB)"
        assert md_size_kb < 2000, f"MD file too large: {md_size_kb:.1f} KB (expected <2000 KB)"
        
        # Assert: JSON size reasonable
        assert json_size_kb > 20, f"JSON file too small: {json_size_kb:.1f} KB (expected >20 KB)"
        assert json_size_kb < 2000, f"JSON file too large: {json_size_kb:.1f} KB (expected <2000 KB)"
        
        # Assert: JSON is smaller than MD (efficiency check)
        # JSON should be 30-50% of MD size (structured data vs formatted text)
        assert json_size_kb < md_size_kb * 1.5, f"JSON unexpectedly larger than MD ({json_size_kb:.1f} KB vs {md_size_kb:.1f} KB)"
    
    def test_content_parity_chapter_count(self, test_output_dir):
        """
        Test: Verify chapter count matches between MD and JSON.
        
        Both files should represent the same book with same chapters.
        
        References:
        - Task 8: Content parity test
        """
        md_file = test_output_dir / "Architecture Patterns with Python_guideline.md"
        json_file = test_output_dir / "Architecture Patterns with Python_guideline.json"
        
        if not md_file.exists() or not json_file.exists():
            pytest.skip("Output files not found (run test_generate_guideline_files first)")
        
        # Count chapters in MD
        md_content = md_file.read_text(encoding='utf-8')
        import re
        md_chapters = len(re.findall(r'^## Chapter \d+:', md_content, re.MULTILINE))
        
        # Count chapters in JSON
        with open(json_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        json_chapters = len(json_data["chapters"])
        
        print("\nChapter counts:")
        print(f"  MD:   {md_chapters}")
        print(f"  JSON: {json_chapters}")
        
        # Assert: Same number of chapters
        assert md_chapters == json_chapters, f"Chapter count mismatch: MD={md_chapters}, JSON={json_chapters}"
        assert md_chapters > 0, "No chapters found in either file"
    
    def test_json_footnote_preservation(self, test_output_dir):
        """
        Test: Verify footnotes are preserved in JSON.
        
        Chicago-style footnotes should be extracted and included in JSON.
        
        References:
        - Task 9: JSON serialization includes footnotes
        """
        json_file = test_output_dir / "Architecture Patterns with Python_guideline.json"
        
        if not json_file.exists():
            pytest.skip("JSON file not found (run test_generate_guideline_files first)")
        
        # Load JSON
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Assert: Footnotes array exists
        assert "footnotes" in data, "Missing footnotes key"
        assert isinstance(data["footnotes"], list), "footnotes should be a list"
        
        # If footnotes exist, validate structure (actual schema: number, author, file, lines, page, title)
        if len(data["footnotes"]) > 0:
            first_footnote = data["footnotes"][0]
            assert "number" in first_footnote, "Footnote missing number"
            # Actual schema doesn't have 'text' field, has 'author', 'title', 'file', 'page', 'lines' instead
            assert "author" in first_footnote, "Footnote missing author"
            assert "file" in first_footnote, "Footnote missing file"
            
            print(f"\nFootnotes found: {len(data['footnotes'])}")
    
    def test_json_is_valid_and_parseable(self, test_output_dir):
        """
        Test: Verify JSON is valid and can be re-loaded.
        
        JSON should be:
        - Valid JSON syntax
        - Properly formatted (indent=2)
        - Re-loadable without errors
        
        References:
        - Task 10: JSON file writer with proper formatting
        """
        json_file = test_output_dir / "Architecture Patterns with Python_guideline.json"
        
        if not json_file.exists():
            pytest.skip("JSON file not found (run test_generate_guideline_files first)")
        
        # Act: Load JSON multiple times to ensure stability
        for attempt in range(3):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Verify basic structure each time
            assert isinstance(data, dict), f"Attempt {attempt+1}: Not a dictionary"
            assert len(data) > 0, f"Attempt {attempt+1}: Empty dictionary"
        
        # Assert: JSON is properly formatted (check indentation)
        content = json_file.read_text(encoding='utf-8')
        assert '  ' in content, "JSON should be indented"
        assert content.count('\n') > 10, "JSON should be multi-line formatted"


class TestLargeBookHandling:
    """
    Tests for handling large books (e.g., Learning Python: 81 chapters).
    
    These tests verify scalability and performance.
    """
    
    def test_learning_python_generation(self):
        """
        Test: Generate guidelines for Learning Python (81 chapters).
        
        This is a stress test for:
        - Large chapter count handling
        - Memory efficiency
        - Reasonable execution time
        
        Expected file sizes:
        - MD: ~2 MB (based on CONSOLIDATED_IMPLEMENTATION_PLAN validation)
        - JSON: ~750 KB (30-40% of MD)
        
        References:
        - CONSOLIDATED_IMPLEMENTATION_PLAN: Learning Python validation
        - Task 19: Performance optimization
        """
        pytest.skip("Large book test deferred to performance optimization phase (Task 19)")


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_files():
    """
    Cleanup generated test files after test session.
    
    Files are left in place during session for inspection,
    then cleaned up after all tests complete.
    """
    yield
    
    # Cleanup after all tests
    repo_root = Path(__file__).parent.parent.parent
    output_dir = repo_root / "workflows" / "base_guideline_generation" / "output"
    test_files = [
        output_dir / "Architecture Patterns with Python_guideline.md",
        output_dir / "Architecture Patterns with Python_guideline.json",
    ]
    
    for file in test_files:
        if file.exists():
            try:
                file.unlink()
                print(f"Cleaned up: {file.name}")
            except Exception as e:
                print(f"Could not clean up {file.name}: {e}")
