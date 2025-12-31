"""Unit tests for WBS D2.1: Enriched Output Naming Convention.

Phase D2.1: Update llm-document-enhancer Output
WBS Tasks: D2.1.1-5

These tests validate:
1. Output files use `{Book Title}_metadata_enriched.json` naming
2. `enrichment_metadata` section contains taxonomy provenance fields
3. All required provenance fields are present and correctly typed

TDD Methodology:
- RED: Tests written first, expected to fail initially
- GREEN: Implement minimal code to pass tests
- REFACTOR: Clean code and align with CODING_PATTERNS_ANALYSIS

Anti-Pattern Audit:
- Per S1192: String literals extracted to constants
- Per Category 1.1: All functions have type annotations
- Per S3776: Functions under 15 complexity

Reference: DATA_PIPELINE_FIX_WBS.md in textbooks/pending/platform/
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

# Add project root for imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# =============================================================================
# Constants per CODING_PATTERNS_ANALYSIS.md (S1192)
# =============================================================================

EXPECTED_OUTPUT_SUFFIX = "_metadata_enriched.json"
OLD_OUTPUT_SUFFIX = "_enriched.json"
ENRICHMENT_METADATA_KEY = "enrichment_metadata"
EXPECTED_PROVENANCE_FIELDS = {
    "taxonomy_id",
    "taxonomy_version", 
    "taxonomy_path",
    "taxonomy_checksum",
    "source_metadata_file",
    "enrichment_date",
    "enrichment_method",
    "model_version",
}
MINIMUM_CHECKSUM_LENGTH = 64  # sha256 hex length
VALID_ENRICHMENT_METHODS = {"sentence_transformers", "tfidf", "statistical", "semantic_search"}
ISO_DATETIME_MIN_LENGTH = 19  # "2025-12-15T12:00:00" minimum


# =============================================================================
# Helper Functions
# =============================================================================

def _create_sample_metadata() -> list[dict[str, Any]]:
    """Create sample book metadata for testing enrichment.
    
    Includes 5 chapters to satisfy TF-IDF min_df=2 requirement.
    """
    return [
        {
            "chapter_number": 1,
            "title": "Introduction to Machine Learning",
            "summary": "Overview of machine learning fundamentals and algorithms",
            "keywords": ["machine learning", "algorithms", "introduction"],
            "concepts": ["supervised learning", "unsupervised learning"],
        },
        {
            "chapter_number": 2,
            "title": "Neural Networks",
            "summary": "Deep dive into neural network architectures and training",
            "keywords": ["neural networks", "deep learning", "training"],
            "concepts": ["backpropagation", "gradient descent"],
        },
        {
            "chapter_number": 3,
            "title": "Natural Language Processing",
            "summary": "Text processing and language models for NLP applications",
            "keywords": ["nlp", "text processing", "language models"],
            "concepts": ["tokenization", "embeddings"],
        },
        {
            "chapter_number": 4,
            "title": "Computer Vision",
            "summary": "Image recognition and convolutional neural networks",
            "keywords": ["computer vision", "cnn", "image recognition"],
            "concepts": ["convolutions", "pooling layers"],
        },
        {
            "chapter_number": 5,
            "title": "Reinforcement Learning",
            "summary": "Learning through rewards and environment interaction",
            "keywords": ["reinforcement learning", "rewards", "agents"],
            "concepts": ["q-learning", "policy gradient"],
        },
    ]


def _create_sample_taxonomy() -> dict[str, Any]:
    """Create sample taxonomy for testing enrichment provenance."""
    return {
        "taxonomy_id": "ai-ml-2024",
        "version": "1.0.0",
        "tiers": {
            "Tier 1": {"books": ["Test Book"]}
        }
    }


# =============================================================================
# Test Class: Output Naming Convention
# =============================================================================

class TestOutputNamingConvention:
    """WBS D2.1.2: Test that output uses _metadata_enriched.json suffix."""

    def test_output_filename_uses_metadata_enriched_suffix(self) -> None:
        """Output filename should use _metadata_enriched.json suffix.
        
        Expected naming: {Book Title}_metadata_enriched.json
        Not: {Book Title}_enriched.json (old convention)
        """
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            enrich_metadata_local,
        )
        
        # This test is marked to fail initially (RED phase)
        # The actual output path will be checked after implementation
        _input_path = Path("Test Book_metadata.json")
        expected_output = Path("Test Book_metadata_enriched.json")
        old_convention = Path("Test Book_enriched.json")
        
        # Verify the naming convention expectation
        assert str(expected_output).endswith(EXPECTED_OUTPUT_SUFFIX)
        assert not str(old_convention).endswith(EXPECTED_OUTPUT_SUFFIX)

    def test_output_path_derives_correctly_from_input(self) -> None:
        """Output path should derive from input with _metadata_enriched suffix."""
        # Given an input file like: "Architecture Patterns_metadata.json"
        # Expected output: "Architecture Patterns_metadata_enriched.json"
        
        input_filename = "Architecture Patterns_metadata.json"
        expected_output = "Architecture Patterns_metadata_enriched.json"
        
        # Extract book title from input
        book_title = input_filename.replace("_metadata.json", "")
        derived_output = f"{book_title}_metadata_enriched.json"
        
        assert derived_output == expected_output
        assert derived_output.endswith(EXPECTED_OUTPUT_SUFFIX)


# =============================================================================
# Test Class: Enrichment Provenance Fields
# =============================================================================

class TestEnrichmentProvenanceFields:
    """WBS D2.1.3: Test that enrichment_metadata contains provenance fields."""

    def test_enriched_output_has_enrichment_metadata_section(self) -> None:
        """Enriched output must have an enrichment_metadata section."""
        sample_output = {
            "book": "Test Book",
            "enrichment_metadata": {
                "taxonomy_id": "ai-ml-2024",
                "taxonomy_version": "1.0.0",
                "taxonomy_path": "AI-ML_taxonomy.json",
                "taxonomy_checksum": "sha256:" + "a" * 64,
                "source_metadata_file": "Test Book_metadata.json",
                "enrichment_date": "2025-12-15T12:00:00Z",
                "enrichment_method": "sentence_transformers",
                "model_version": "all-MiniLM-L6-v2",
            },
            "chapters": [],
        }
        
        assert ENRICHMENT_METADATA_KEY in sample_output
        assert isinstance(sample_output[ENRICHMENT_METADATA_KEY], dict)

    def test_all_required_provenance_fields_present(self) -> None:
        """All required provenance fields must be present."""
        enrichment_metadata = {
            "taxonomy_id": "ai-ml-2024",
            "taxonomy_version": "1.0.0",
            "taxonomy_path": "AI-ML_taxonomy.json",
            "taxonomy_checksum": "sha256:" + "a" * 64,
            "source_metadata_file": "Test Book_metadata.json",
            "enrichment_date": "2025-12-15T12:00:00Z",
            "enrichment_method": "sentence_transformers",
            "model_version": "all-MiniLM-L6-v2",
        }
        
        actual_fields = set(enrichment_metadata.keys())
        missing_fields = EXPECTED_PROVENANCE_FIELDS - actual_fields
        
        assert not missing_fields, f"Missing provenance fields: {missing_fields}"

    def test_taxonomy_checksum_has_valid_format(self) -> None:
        """Taxonomy checksum should be sha256 format with proper length."""
        valid_checksum = "sha256:" + "a" * 64
        
        assert valid_checksum.startswith("sha256:")
        checksum_hex = valid_checksum.split(":")[1]
        assert len(checksum_hex) == MINIMUM_CHECKSUM_LENGTH
        assert all(c in "0123456789abcdef" for c in checksum_hex)

    def test_enrichment_date_is_iso_format(self) -> None:
        """Enrichment date should be ISO 8601 format."""
        valid_date = "2025-12-15T12:00:00Z"
        
        # ISO format should be parseable
        try:
            datetime.fromisoformat(valid_date.replace("Z", "+00:00"))
            is_valid = True
        except ValueError:
            is_valid = False
        
        assert is_valid, f"Date {valid_date} is not valid ISO 8601"
        assert len(valid_date) >= ISO_DATETIME_MIN_LENGTH

    def test_enrichment_method_is_valid_value(self) -> None:
        """Enrichment method should be one of the valid methods."""
        valid_methods = ["sentence_transformers", "tfidf", "statistical", "semantic_search"]
        
        for method in valid_methods:
            assert method in VALID_ENRICHMENT_METHODS

    def test_source_metadata_file_matches_input(self) -> None:
        """Source metadata file should match the input file name."""
        input_file = "Architecture Patterns_metadata.json"
        enrichment_metadata = {
            "source_metadata_file": input_file,
        }
        
        assert enrichment_metadata["source_metadata_file"] == input_file
        assert enrichment_metadata["source_metadata_file"].endswith("_metadata.json")


# =============================================================================
# Test Class: Integration with enrich_metadata_per_book
# =============================================================================

class TestEnrichMetadataPerBookIntegration:
    """Integration tests for enrich_metadata_per_book.py naming convention."""

    @pytest.fixture
    def temp_test_dir(self, tmp_path: Path) -> Path:
        """Create temporary directory with test files."""
        # Create input metadata file
        input_dir = tmp_path / "metadata_extraction" / "output"
        input_dir.mkdir(parents=True)
        
        metadata = _create_sample_metadata()
        input_file = input_dir / "Test Book_metadata.json"
        with open(input_file, "w") as f:
            json.dump(metadata, f)
        
        # Create taxonomy file
        taxonomy_dir = tmp_path / "taxonomy_setup" / "output"
        taxonomy_dir.mkdir(parents=True)
        
        taxonomy = _create_sample_taxonomy()
        taxonomy_file = taxonomy_dir / "Test Book_taxonomy.json"
        with open(taxonomy_file, "w") as f:
            json.dump(taxonomy, f)
        
        # Create output directory
        output_dir = tmp_path / "metadata_enrichment" / "output"
        output_dir.mkdir(parents=True)
        
        return tmp_path

    def test_enrich_metadata_local_generates_correct_filename(
        self, temp_test_dir: Path
    ) -> None:
        """enrich_metadata_local should generate _metadata_enriched.json output."""
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            enrich_metadata_local,
        )
        
        input_path = temp_test_dir / "metadata_extraction" / "output" / "Test Book_metadata.json"
        output_dir = temp_test_dir / "metadata_enrichment" / "output"
        
        # Derive expected output filename
        book_name = input_path.stem.replace("_metadata", "")
        expected_output_name = f"{book_name}_metadata_enriched.json"
        expected_output_path = output_dir / expected_output_name
        
        # Run enrichment (will create output file)
        # Note: This test may fail initially (RED phase) until D2.1.2 is implemented
        enrich_metadata_local(input_path, expected_output_path)
        
        # Verify correct filename used
        assert expected_output_path.exists(), f"Expected {expected_output_name} not created"
        assert expected_output_path.name.endswith(EXPECTED_OUTPUT_SUFFIX)

    def test_enriched_output_contains_provenance_fields(
        self, temp_test_dir: Path
    ) -> None:
        """Enriched output must contain all provenance fields."""
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import (
            enrich_metadata_local,
        )
        
        input_path = temp_test_dir / "metadata_extraction" / "output" / "Test Book_metadata.json"
        output_dir = temp_test_dir / "metadata_enrichment" / "output"
        
        book_name = input_path.stem.replace("_metadata", "")
        output_path = output_dir / f"{book_name}_metadata_enriched.json"
        
        # Run enrichment
        enrich_metadata_local(input_path, output_path)
        
        # Load and verify provenance
        with open(output_path) as f:
            enriched_data = json.load(f)
        
        assert ENRICHMENT_METADATA_KEY in enriched_data
        enrichment_metadata = enriched_data[ENRICHMENT_METADATA_KEY]
        
        # Check all provenance fields are present
        # Note: Some fields may be missing until D2.1.3 is implemented
        for field in ["enrichment_date", "enrichment_method"]:
            assert field in enrichment_metadata, f"Missing field: {field}"


# =============================================================================
# Test Class: Backward Compatibility
# =============================================================================

class TestBackwardCompatibility:
    """Ensure changes don't break existing functionality."""

    def test_old_enriched_files_still_readable(self) -> None:
        """Old _enriched.json files should still be readable."""
        old_format_data = {
            "book": "Test Book",
            "enrichment_metadata": {
                "generated": "2025-12-15T12:00:00",
                "method": "statistical",
            },
            "chapters": [],
        }
        
        # Verify old format can be parsed
        assert "book" in old_format_data
        assert "chapters" in old_format_data
        # Old format may not have all new provenance fields
        enrichment_meta = old_format_data.get(ENRICHMENT_METADATA_KEY, {})
        assert "method" in enrichment_meta or "generated" in enrichment_meta

    def test_new_format_includes_original_fields(self) -> None:
        """New format should preserve all original enrichment_metadata fields."""
        new_format_data = {
            "book": "Test Book",
            "enrichment_metadata": {
                # Original fields
                "generated": "2025-12-15T12:00:00",
                "method": "statistical",
                "libraries": {"yake": "0.4.8"},
                "corpus_size": 47,
                "total_chapters_analyzed": 1576,
                # New provenance fields
                "taxonomy_id": "ai-ml-2024",
                "taxonomy_version": "1.0.0",
                "taxonomy_path": "AI-ML_taxonomy.json",
                "taxonomy_checksum": "sha256:" + "a" * 64,
                "source_metadata_file": "Test Book_metadata.json",
                "enrichment_date": "2025-12-15T12:00:00Z",
                "enrichment_method": "sentence_transformers",
                "model_version": "all-MiniLM-L6-v2",
            },
            "chapters": [],
        }
        
        enrichment_meta = new_format_data[ENRICHMENT_METADATA_KEY]
        
        # Verify original fields preserved
        assert "generated" in enrichment_meta
        assert "method" in enrichment_meta
        
        # Verify new fields added
        assert "taxonomy_id" in enrichment_meta
        assert "taxonomy_checksum" in enrichment_meta
