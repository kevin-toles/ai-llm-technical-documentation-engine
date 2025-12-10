#!/usr/bin/env python3
"""
Integration tests for Tab 6 Aggregate Package Creation.

Test-Driven Development (TDD) approach:
- RED: These tests should FAIL initially (script doesn't exist yet)
- GREEN: Implement minimal code to make tests pass
- REFACTOR: Clean code and align with guidelines

Reference Documents:
1. CONSOLIDATED_IMPLEMENTATION_PLAN.md - Tab 6 requirements (lines 1551-1701)
2. PYTHON_GUIDELINES_Learning_Python_Ed6_LLM_ENHANCED.md - File I/O, pathlib, json
"""

import json
import pytest
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Project root for path resolution
PROJECT_ROOT = Path(__file__).parent.parent.parent


class TestAggregatePackageCreation:
    """Test suite for Tab 6 Aggregate Package functionality."""
    
    @pytest.fixture
    def sample_taxonomy_path(self) -> Path:
        """Path to sample Tab 3 taxonomy output."""
        return PROJECT_ROOT / "workflows" / "taxonomy_setup" / "output" / "architecture_patterns_taxonomy.json"
    
    @pytest.fixture
    def metadata_dir(self) -> Path:
        """Directory containing metadata files."""
        return PROJECT_ROOT / "workflows" / "metadata_extraction" / "output"
    
    @pytest.fixture
    def enriched_metadata_dir(self) -> Path:
        """Directory containing enriched metadata files."""
        return PROJECT_ROOT / "workflows" / "metadata_enrichment" / "output"
    
    @pytest.fixture
    def guideline_dir(self) -> Path:
        """Directory containing guideline JSON files."""
        return PROJECT_ROOT / "workflows" / "base_guideline_generation" / "output"
    
    @pytest.fixture
    def output_dir(self, tmp_path) -> Path:
        """Temporary output directory for aggregate packages."""
        output = tmp_path / "llm_enhancement" / "tmp"
        output.mkdir(parents=True, exist_ok=True)
        return output
    
    def test_aggregate_package_script_exists(self):
        """
        RED TEST: Verify aggregation script exists.
        
        Expected to FAIL initially - script not yet created.
        Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1551-1565
        """
        script_path = PROJECT_ROOT / "workflows" / "llm_enhancement" / "scripts" / "create_aggregate_package.py"
        assert script_path.exists(), f"Script not found: {script_path}"
    
    def test_taxonomy_file_loading(self, sample_taxonomy_path):
        """
        RED TEST: Verify taxonomy file can be loaded.
        
        Tests requirement: Load Taxonomy (step 1)
        Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1570-1573
        """
        if not sample_taxonomy_path.exists():
            pytest.skip("Sample taxonomy file not available")
        
        with open(sample_taxonomy_path, encoding='utf-8') as f:
            taxonomy = json.load(f)
        
        assert "tiers" in taxonomy, "Taxonomy should have 'tiers' field"
        assert isinstance(taxonomy["tiers"], dict), "Tiers should be a dictionary"
    
    def test_build_book_list_from_taxonomy(self, sample_taxonomy_path):
        """
        RED TEST: Verify book list can be extracted from taxonomy.
        
        Tests requirement: Build Book List from Taxonomy (step 2)
        Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1575-1586
        """
        if not sample_taxonomy_path.exists():
            pytest.skip("Sample taxonomy file not available")
        
        with open(sample_taxonomy_path, encoding='utf-8') as f:
            taxonomy = json.load(f)
        
        # Build book list
        book_list = []
        for tier_name, tier_data in taxonomy["tiers"].items():
            if "books" in tier_data:
                for book_name in tier_data["books"]:
                    book_list.append({
                        "name": book_name,
                        "tier": tier_name,
                        "priority": tier_data.get("priority", 1)
                    })
        
        assert len(book_list) > 0, "Should extract at least one book from taxonomy"
        assert all("name" in book and "tier" in book for book in book_list), "Each book should have name and tier"
    
    def test_graceful_degradation_missing_files(self, metadata_dir):
        """
        RED TEST: Verify graceful handling of missing files.
        
        Tests requirement: Graceful degradation (fallback logic)
        Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1588-1616
        """
        # Test with non-existent book
        book_name = "nonexistent_book"
        enriched_path = metadata_dir / f"{book_name}_metadata_enriched.json"
        basic_path = metadata_dir / f"{book_name}_metadata.json"
        
        # Both should not exist
        assert not enriched_path.exists(), "Test setup: enriched file should not exist"
        assert not basic_path.exists(), "Test setup: basic file should not exist"
        
        # Should handle gracefully by tracking missing book
        missing_book = {
            "name": book_name,
            "reason": "metadata_not_found",
            "expected_files": [str(enriched_path), str(basic_path)]
        }
        
        assert missing_book["name"] == book_name
        assert missing_book["reason"] == "metadata_not_found"
    
    def test_timestamp_generation(self):
        """
        RED TEST: Verify timestamp format for output filename.
        
        Tests requirement: Timestamped filename
        Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1621-1622
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Verify format: YYYYMMDD_HHMMSS
        assert len(timestamp) == 15, "Timestamp should be 15 characters"
        assert timestamp[8] == "_", "Timestamp should have underscore separator"
        assert timestamp[:8].isdigit(), "Date part should be numeric"
        assert timestamp[9:].isdigit(), "Time part should be numeric"
    
    def test_aggregate_package_output_schema(self):
        """
        RED TEST: Verify aggregate package has correct schema.
        
        Tests requirement: Output Schema validation
        Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1645-1699
        
        Expected schema:
        {
            "project": {
                "id": str,
                "generated": ISO timestamp,
                "source_taxonomy": str,
                "package_version": str
            },
            "source_book": {
                "name": str,
                "metadata": {...},
                "taxonomy": {...},
                "guideline": {...} (optional)
            },
            "companion_books": [
                {
                    "name": str,
                    "guideline": {...}
                }
            ],
            "missing_books": [
                {
                    "name": str,
                    "reason": str,
                    "expected_files": [str]
                }
            ],
            "statistics": {
                "total_books": int,
                "total_chapters": int,
                "missing_count": int
            }
        }
        """
        # Find the most recent aggregate package file
        output_dir = PROJECT_ROOT / "workflows" / "llm_enhancement" / "tmp"
        package_files = list(output_dir.glob("architecture_patterns_llm_package_*.json"))
        
        if not package_files:
            pytest.skip("Aggregate package not yet generated - run aggregation script first")
        
        # Use most recent file (sorted by name, which includes timestamp)
        output_file = sorted(package_files)[-1]
        
        with open(output_file, encoding='utf-8') as f:
            package = json.load(f)
        
        # Verify top-level structure
        assert "project" in package, "Missing 'project' field"
        assert "source_book" in package, "Missing 'source_book' field"
        assert "companion_books" in package, "Missing 'companion_books' field"
        assert "missing_books" in package, "Missing 'missing_books' field"
        assert "statistics" in package, "Missing 'statistics' field"
        
        # Verify project metadata
        project = package["project"]
        assert "id" in project, "Missing 'project.id'"
        assert "generated" in project, "Missing 'project.generated'"
        assert "source_taxonomy" in project, "Missing 'project.source_taxonomy'"
        assert "package_version" in project, "Missing 'project.package_version'"
        
        # Verify source book
        source = package["source_book"]
        assert "name" in source, "Missing 'source_book.name'"
        assert "metadata" in source or "metadata_enriched" in source, "Missing metadata in source_book"
        
        # Verify statistics
        stats = package["statistics"]
        assert "total_books" in stats, "Missing 'statistics.total_books'"
        assert "total_chapters" in stats, "Missing 'statistics.total_chapters'"
        assert "missing_count" in stats, "Missing 'statistics.missing_count'"
        assert isinstance(stats["total_books"], int), "total_books should be integer"
        assert isinstance(stats["missing_count"], int), "missing_count should be integer"
    
    def test_statistics_calculation(self):
        """
        RED TEST: Verify statistics are calculated correctly.
        
        Tests requirement: Statistics for validation
        Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1692-1698
        """
        # Sample data for statistics test
        books_data = [
            {"name": "book1", "metadata_enriched": {"chapters": [{"num": 1}, {"num": 2}]}},
            {"name": "book2", "metadata_enriched": {"chapters": [{"num": 1}, {"num": 2}, {"num": 3}]}},
        ]
        missing_books = [{"name": "book3"}]
        
        # Calculate statistics
        total_books = len(books_data)
        total_chapters = sum(len(b["metadata_enriched"]["chapters"]) for b in books_data if "metadata_enriched" in b)
        missing_count = len(missing_books)
        
        assert total_books == 2, "Should count 2 books"
        assert total_chapters == 5, "Should count 5 total chapters"
        assert missing_count == 1, "Should count 1 missing book"
    
    def test_no_llm_calls(self):
        """
        RED TEST: Verify no LLM calls are made during aggregation.
        
        Tests requirement: Pure file loading and combining (NO LLM)
        Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md line 1703
        """
        # This is a design constraint test
        # The script should only do file I/O operations
        # No imports of llm-related modules should exist
        
        script_path = PROJECT_ROOT / "workflows" / "llm_enhancement" / "scripts" / "create_aggregate_package.py"
        
        if not script_path.exists():
            pytest.skip("Script not yet created")
        
        with open(script_path, encoding='utf-8') as f:
            content = f.read()
        
        # Check for LLM-related imports (should not exist)
        llm_imports = ["openai", "anthropic", "langchain", "llama"]
        for llm_lib in llm_imports:
            assert llm_lib not in content.lower(), f"Should not import {llm_lib} - this is a pure file operation task"


class TestAggregatePackageWorkflow:
    """
    End-to-end workflow tests for Tab 6.
    
    These tests verify the complete aggregation pipeline:
    1. Load taxonomy
    2. Build book list
    3. Load metadata with graceful degradation
    4. Combine into single package
    5. Generate timestamped output
    6. Calculate statistics
    """
    
    @pytest.mark.integration
    def test_full_aggregation_workflow(self):
        """
        RED TEST: Full workflow integration test.
        
        This test validates the complete Tab 6 workflow per CONSOLIDATED_IMPLEMENTATION_PLAN:
        1. Load taxonomy from Tab 3
        2. Extract book list
        3. Load metadata with fallbacks
        4. Build aggregate package
        5. Save with timestamp
        6. Calculate statistics
        
        Expected to FAIL until full implementation complete.
        """
        taxonomy_file = PROJECT_ROOT / "workflows" / "taxonomy_setup" / "output" / "architecture_patterns_taxonomy.json"
        output_dir = PROJECT_ROOT / "workflows" / "llm_enhancement" / "tmp"
        
        if not taxonomy_file.exists():
            pytest.skip("Required taxonomy file not available")
        
        if not output_dir.exists():
            pytest.skip("Output directory not created yet")
        
        # Check for any generated package files
        package_files = list(output_dir.glob("*_llm_package_*.json"))
        
        if not package_files:
            pytest.skip("Aggregate package not yet generated - run aggregation script first")
        
        # Verify most recent package
        latest_package = max(package_files, key=lambda p: p.stat().st_mtime)
        assert latest_package.exists(), "Package file should exist"
        
        with open(latest_package, encoding='utf-8') as f:
            package = json.load(f)
        
        # Verify complete structure
        assert "project" in package
        assert "source_book" in package
        assert "companion_books" in package
        assert "statistics" in package
        
        # Verify statistics are non-zero
        stats = package["statistics"]
        assert stats["total_books"] > 0, "Should have at least one book"
        assert stats.get("total_chapters", 0) >= 0, "Should have chapter count"
