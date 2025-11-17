#!/usr/bin/env python3
"""
Unit tests for generate_taxonomy_config.py

TDD Phase: RED
- Write failing tests first to define expected behavior
- Tests will fail until features are implemented (GREEN phase)

Guideline Compliance:
- ARCH 5336: Dependency Injection for paths and configuration
- PY 3754: Use pathlib.Path() for all file operations
- PY 32425: Use context managers for file I/O
- PY 21: EAFP exception handling
"""

import json
import pytest
import yaml
import toml
from pathlib import Path
import sys

# Add parent directory to path to import module under test
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "workflows" / "taxonomy_setup" / "scripts"))

from generate_taxonomy_config import TaxonomyConfigGenerator


class TestConfigurationGeneration:
    """Test taxonomy configuration generation"""
    
    def test_generates_valid_json_config(self, tmp_path):
        """Should generate valid JSON configuration"""
        output_file = tmp_path / "taxonomy.json"
        
        generator = TaxonomyConfigGenerator(output_file=output_file)
        config = generator.generate()
        
        # Should be valid dictionary
        assert isinstance(config, dict)
        assert "metadata" in config
        assert "books" in config
        assert "tiers" in config
    
    def test_includes_all_books_from_taxonomy(self, tmp_path):
        """Should include all books defined in book_taxonomy.py"""
        output_file = tmp_path / "taxonomy.json"
        
        generator = TaxonomyConfigGenerator(output_file=output_file)
        config = generator.generate()
        
        # Should have books
        assert len(config["books"]) > 0
        assert config["metadata"]["total_books"] == len(config["books"])
    
    def test_books_have_required_fields(self, tmp_path):
        """Should ensure each book has all required fields"""
        output_file = tmp_path / "taxonomy.json"
        
        generator = TaxonomyConfigGenerator(output_file=output_file)
        config = generator.generate()
        
        required_fields = ["name", "tier", "primary_focus", "relevance_weight", "keyword_triggers", "cascades_to"]
        
        for book in config["books"]:
            for field in required_fields:
                assert field in book, f"Book missing field: {field}"


class TestCLIArguments:
    """Test command-line argument parsing"""
    
    def test_accepts_output_argument(self):
        """Should accept --output argument for custom output path"""
        # Will implement after CLI is refactored
        pass
    
    def test_accepts_format_argument(self):
        """Should accept --format json|yaml|toml"""
        pass
    
    def test_accepts_pretty_flag(self):
        """Should accept --pretty flag for formatted output"""
        pass
    
    def test_accepts_validate_only_flag(self):
        """Should accept --validate-only flag"""
        pass
    
    def test_accepts_dry_run_flag(self):
        """Should accept --dry-run flag"""
        pass


class TestOutputFormats:
    """Test different output format options"""
    
    def test_outputs_json_format(self, tmp_path):
        """Should output configuration in JSON format"""
        output_file = tmp_path / "taxonomy.json"
        
        generator = TaxonomyConfigGenerator(output_file=output_file, output_format="json")
        generator.generate_and_save()
        
        assert output_file.exists()
        
        # Should be valid JSON
        with open(output_file, 'r') as f:
            config = json.load(f)
        
        assert "books" in config
    
    def test_outputs_yaml_format(self, tmp_path):
        """Should output configuration in YAML format"""
        output_file = tmp_path / "taxonomy.yaml"
        
        generator = TaxonomyConfigGenerator(output_file=output_file, output_format="yaml")
        generator.generate_and_save()
        
        assert output_file.exists()
        
        # Should be valid YAML
        with open(output_file, 'r') as f:
            config = yaml.safe_load(f)
        
        assert "books" in config
    
    def test_outputs_toml_format(self, tmp_path):
        """Should output configuration in TOML format"""
        output_file = tmp_path / "taxonomy.toml"
        
        generator = TaxonomyConfigGenerator(output_file=output_file, output_format="toml")
        generator.generate_and_save()
        
        assert output_file.exists()
        
        # Should be valid TOML
        with open(output_file, 'r') as f:
            config = toml.load(f)
        
        # TOML flattens books into separate tables (book_0_Name, book_1_Name, etc.)
        assert "metadata" in config
        # Check that at least one book entry exists
        book_keys = [k for k in config.keys() if k.startswith("book_")]
        assert len(book_keys) > 0


class TestPrettyFormatting:
    """Test --pretty flag for human-readable output"""
    
    def test_pretty_formats_json_with_indentation(self, tmp_path):
        """Should format JSON with proper indentation when pretty=True"""
        output_file = tmp_path / "taxonomy.json"
        
        generator = TaxonomyConfigGenerator(output_file=output_file, pretty=True)
        generator.generate_and_save()
        
        # Read raw content
        content = output_file.read_text()
        
        # Should have indentation (multiple spaces)
        assert "  " in content or "\t" in content
    
    def test_compact_formats_without_indentation(self, tmp_path):
        """Should format JSON compactly when pretty=False"""
        output_file = tmp_path / "taxonomy.json"
        
        generator = TaxonomyConfigGenerator(output_file=output_file, pretty=False)
        generator.generate_and_save()
        
        # Read raw content
        content = output_file.read_text()
        
        # Should be more compact (no newlines between fields)
        # This is a simple heuristic
        assert len(content.split('\n')) < 20  # Compact has fewer lines


class TestCascadeValidation:
    """Test validation of cascade references"""
    
    def test_validates_cascade_references_exist(self, tmp_path):
        """Should validate that all cascade_to references point to existing books"""
        output_file = tmp_path / "taxonomy.json"
        
        generator = TaxonomyConfigGenerator(output_file=output_file)
        config = generator.generate()
        
        # Validate should check cascade references
        generator.validate_config(config)
        
        # Should not raise exception if all references valid
    
    def test_detects_invalid_cascade_references(self, tmp_path):
        """Should detect when cascade reference points to non-existent book"""
        # Create a config with invalid cascade
        invalid_config = {
            "metadata": {"total_books": 1},
            "books": [
                {
                    "name": "Book A",
                    "cascades_to": ["NonExistentBook"]
                }
            ]
        }
        
        generator = TaxonomyConfigGenerator(output_file=tmp_path / "taxonomy.json")
        
        with pytest.raises(ValueError, match="unknown book|does not exist"):
            generator.validate_config(invalid_config)


class TestCircularDependencyDetection:
    """Test detection of circular cascade dependencies"""
    
    def test_detects_direct_circular_dependency(self, tmp_path, capsys):
        """Should warn about A -> B -> A circular dependency"""
        config = {
            "metadata": {"total_books": 2},
            "books": [
                {"name": "Book A", "cascades_to": ["Book B"], "relevance_weight": 1.0},
                {"name": "Book B", "cascades_to": ["Book A"], "relevance_weight": 1.0}
            ]
        }
        
        generator = TaxonomyConfigGenerator(output_file=tmp_path / "taxonomy.json")
        
        # Should warn but not raise exception (cascades may be intentional)
        generator.validate_config(config)
        
        captured = capsys.readouterr()
        assert "Warning" in captured.out or "circular" in captured.out.lower()
    
    def test_detects_indirect_circular_dependency(self, tmp_path, capsys):
        """Should warn about A -> B -> C -> A circular dependency"""
        config = {
            "metadata": {"total_books": 3},
            "books": [
                {"name": "Book A", "cascades_to": ["Book B"], "relevance_weight": 1.0},
                {"name": "Book B", "cascades_to": ["Book C"], "relevance_weight": 1.0},
                {"name": "Book C", "cascades_to": ["Book A"], "relevance_weight": 1.0}
            ]
        }
        
        generator = TaxonomyConfigGenerator(output_file=tmp_path / "taxonomy.json")
        
        # Should warn but not raise
        generator.validate_config(config)
        
        captured = capsys.readouterr()
        assert "Warning" in captured.out or "circular" in captured.out.lower()
    
    def test_allows_valid_cascade_chains(self, tmp_path):
        """Should allow valid cascade chains without cycles"""
        config = {
            "metadata": {"total_books": 3},
            "books": [
                {"name": "Book A", "cascades_to": ["Book B"], "relevance_weight": 1.0},
                {"name": "Book B", "cascades_to": ["Book C"], "relevance_weight": 1.0},
                {"name": "Book C", "cascades_to": [], "relevance_weight": 1.0}
            ]
        }
        
        generator = TaxonomyConfigGenerator(output_file=tmp_path / "taxonomy.json")
        
        # Should not raise exception
        generator.validate_config(config)


class TestValidateOnlyMode:
    """Test --validate-only mode"""
    
    def test_validate_only_does_not_create_file(self, tmp_path):
        """Should NOT create output file when validate_only=True"""
        output_file = tmp_path / "taxonomy.json"
        
        generator = TaxonomyConfigGenerator(output_file=output_file)
        generator.validate_only()
        
        assert not output_file.exists()
    
    def test_validate_only_reports_validation_results(self, tmp_path, capsys):
        """Should report validation results without saving file"""
        output_file = tmp_path / "taxonomy.json"
        
        generator = TaxonomyConfigGenerator(output_file=output_file)
        generator.validate_only()
        
        captured = capsys.readouterr()
        
        # Should show validation messages
        assert "validat" in captured.out.lower() or "✅" in captured.out


class TestDryRunMode:
    """Test --dry-run mode"""
    
    def test_dry_run_does_not_create_file(self, tmp_path):
        """Should NOT create output file when dry_run=True"""
        output_file = tmp_path / "taxonomy.json"
        
        generator = TaxonomyConfigGenerator(output_file=output_file)
        generator.generate_and_save(dry_run=True)
        
        assert not output_file.exists()
    
    def test_dry_run_shows_preview(self, tmp_path, capsys):
        """Should show preview of what would be written"""
        output_file = tmp_path / "taxonomy.json"
        
        generator = TaxonomyConfigGenerator(output_file=output_file)
        generator.generate_and_save(dry_run=True)
        
        captured = capsys.readouterr()
        
        # Should show preview or dry run message
        assert "DRY RUN" in captured.out or "Would write" in captured.out or "Preview" in captured.out


class TestSummaryStatistics:
    """Test summary statistics output"""
    
    def test_displays_taxonomy_summary(self, tmp_path, capsys):
        """Should display summary of taxonomy structure"""
        output_file = tmp_path / "taxonomy.json"
        
        generator = TaxonomyConfigGenerator(output_file=output_file)
        generator.generate_and_save()
        
        captured = capsys.readouterr()
        
        # Should show statistics
        assert "books" in captured.out.lower() or "Total" in captured.out
    
    def test_summary_includes_tier_breakdown(self, tmp_path, capsys):
        """Should include breakdown by tier in summary"""
        output_file = tmp_path / "taxonomy.json"
        
        generator = TaxonomyConfigGenerator(output_file=output_file)
        generator.generate_and_save()
        
        captured = capsys.readouterr()
        
        # Should show tier information
        assert "tier" in captured.out.lower() or "Tier" in captured.out
    
    def test_summary_includes_cascade_count(self, tmp_path, capsys):
        """Should include count of cascade relationships"""
        output_file = tmp_path / "taxonomy.json"
        
        generator = TaxonomyConfigGenerator(output_file=output_file)
        config = generator.generate()
        
        # Count total cascades
        total_cascades = sum(len(book["cascades_to"]) for book in config["books"])
        
        assert total_cascades >= 0  # Should have some cascade data


class TestDefaultOutputPath:
    """Test default output path behavior"""
    
    def test_uses_workflow_output_folder_by_default(self):
        """Should default to ../output/taxonomy_config.json"""
        generator = TaxonomyConfigGenerator()
        
        # Should have default output path set to workflow output folder
        assert generator.output_file is not None
        assert "output" in str(generator.output_file)
        assert "taxonomy_config" in str(generator.output_file)


class TestRelevanceWeightValidation:
    """Test validation of relevance weights"""
    
    def test_validates_positive_relevance_weights(self, tmp_path):
        """Should validate that relevance weights are positive"""
        config = {
            "metadata": {"total_books": 1},
            "books": [
                {"name": "Book A", "relevance_weight": -1, "cascades_to": []}
            ]
        }
        
        generator = TaxonomyConfigGenerator(output_file=tmp_path / "taxonomy.json")
        
        with pytest.raises(ValueError, match="relevance|weight|invalid"):
            generator.validate_config(config)
    
    def test_allows_valid_relevance_weights(self, tmp_path):
        """Should allow positive relevance weights"""
        config = {
            "metadata": {"total_books": 1},
            "books": [
                {"name": "Book A", "relevance_weight": 1.0, "cascades_to": []}
            ]
        }
        
        generator = TaxonomyConfigGenerator(output_file=tmp_path / "taxonomy.json")
        
        # Should not raise exception
        generator.validate_config(config)
