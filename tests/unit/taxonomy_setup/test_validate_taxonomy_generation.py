"""
Test suite for Tab 3 taxonomy validation script.

Tests validate that validate_taxonomy_generation.py exists and correctly validates:
1. Taxonomy JSON structure
2. Tier categorization (architecture, implementation, practices)
3. Concept deduplication
4. Priority ordering

References:
    - MASTER_IMPLEMENTATION_GUIDE Task 2.1
    - ARCHITECTURE_GUIDELINES Ch.4: Service Layer Pattern
    - PYTHON_GUIDELINES: Test-driven development
"""

import json
import pytest
from pathlib import Path
from typing import Dict, Any


class TestValidationScriptExists:
    """RED: Verify validation script file exists."""
    
    def test_validation_script_file_exists(self):
        """
        RED Phase: This test will FAIL until script is created.
        
        Task 2.1: Create validate_taxonomy_generation.py script.
        
        References:
            - MASTER_IMPLEMENTATION_GUIDE Task 2.1
        """
        script_path = Path("scripts/validate_taxonomy_generation.py")
        assert script_path.exists(), (
            f"Validation script not found: {script_path}. "
            "Task 2.1 requires creating scripts/validate_taxonomy_generation.py"
        )
    
    def test_validation_script_is_executable(self):
        """
        RED Phase: Verify script has proper structure.
        
        Script should be executable and importable.
        """
        script_path = Path("scripts/validate_taxonomy_generation.py")
        
        if not script_path.exists():
            pytest.skip("Script doesn't exist yet")
        
        content = script_path.read_text()
        
        # Should have main entry point
        assert "if __name__ ==" in content, "Script should have main entry point"
        
        # Should have shebang for execution
        assert content.startswith("#!/usr/bin/env python3"), (
            "Script should start with #!/usr/bin/env python3 shebang"
        )


class TestTaxonomyStructureValidation:
    """RED: Tests for taxonomy JSON structure validation."""
    
    def test_validates_required_top_level_keys(self):
        """
        RED Phase: Verify validator checks for required 'tiers' key.
        
        Taxonomy JSON must have 'tiers' key at top level.
        """
        # This will fail until validator is implemented
        try:
            from scripts.taxonomy_validation_services import TaxonomyStructureValidator
        except ImportError:
            pytest.skip("Validation services not implemented yet")
        
        # Invalid taxonomy (missing 'tiers')
        invalid_taxonomy = {"concepts": []}
        
        results = TaxonomyStructureValidator.validate_structure(invalid_taxonomy)
        
        # Should detect missing 'tiers' key
        assert any(r.is_failed() for r in results), (
            "Validator should detect missing 'tiers' key"
        )
    
    def test_validates_tier_structure(self):
        """
        RED Phase: Verify validator checks tier structure.
        
        Each tier must have 'priority' and 'concepts' keys.
        """
        try:
            from scripts.taxonomy_validation_services import TaxonomyStructureValidator
        except ImportError:
            pytest.skip("Validation services not implemented yet")
        
        # Invalid tier (missing 'priority')
        invalid_taxonomy = {
            "tiers": {
                "architecture": {
                    "concepts": ["class", "function"]
                    # Missing 'priority'
                }
            }
        }
        
        results = TaxonomyStructureValidator.validate_structure(invalid_taxonomy)
        
        assert any(r.is_failed() for r in results), (
            "Validator should detect missing 'priority' in tier"
        )


class TestTierCategorizationValidation:
    """RED: Tests for tier categorization validation."""
    
    def test_validates_three_tier_structure(self):
        """
        RED Phase: Verify validator checks for 3-tier structure.
        
        Taxonomy must have architecture, implementation, practices tiers.
        """
        try:
            from scripts.taxonomy_validation_services import TierCategorizationValidator
        except ImportError:
            pytest.skip("Validation services not implemented yet")
        
        # Missing 'practices' tier
        incomplete_taxonomy = {
            "tiers": {
                "architecture": {"priority": 1, "concepts": []},
                "implementation": {"priority": 2, "concepts": []}
                # Missing 'practices'
            }
        }
        
        results = TierCategorizationValidator.validate_tiers(incomplete_taxonomy)
        
        assert any(r.is_failed() for r in results), (
            "Validator should detect missing 'practices' tier"
        )
    
    def test_validates_priority_ordering(self):
        """
        RED Phase: Verify validator checks priority ordering.
        
        architecture (1) < implementation (2) < practices (3)
        """
        try:
            from scripts.taxonomy_validation_services import TierCategorizationValidator
        except ImportError:
            pytest.skip("Validation services not implemented yet")
        
        # Invalid priority order
        invalid_taxonomy = {
            "tiers": {
                "architecture": {"priority": 3, "concepts": []},  # Wrong
                "implementation": {"priority": 2, "concepts": []},
                "practices": {"priority": 1, "concepts": []}  # Wrong
            }
        }
        
        results = TierCategorizationValidator.validate_tiers(invalid_taxonomy)
        
        assert any(r.is_failed() for r in results), (
            "Validator should detect incorrect priority ordering"
        )


class TestConceptDeduplicationValidation:
    """RED: Tests for concept deduplication validation."""
    
    def test_validates_no_duplicate_concepts_within_tier(self):
        """
        RED Phase: Verify validator detects duplicate concepts in same tier.
        
        Concepts array within a tier must not have duplicates.
        """
        try:
            from scripts.taxonomy_validation_services import ConceptDeduplicationValidator
        except ImportError:
            pytest.skip("Validation services not implemented yet")
        
        # Duplicate concept in architecture tier
        taxonomy_with_duplicates = {
            "tiers": {
                "architecture": {
                    "priority": 1,
                    "concepts": ["class", "function", "class"]  # Duplicate 'class'
                }
            }
        }
        
        results = ConceptDeduplicationValidator.validate_deduplication(
            taxonomy_with_duplicates
        )
        
        assert any(r.is_failed() for r in results), (
            "Validator should detect duplicate concepts within tier"
        )
    
    def test_allows_same_concept_across_different_tiers(self):
        """
        RED Phase: Verify validator allows same concept in different tiers.
        
        Same concept can appear in multiple tiers (architecture vs implementation).
        This is valid - a concept like 'class' can have both architectural and
        implementation aspects.
        """
        try:
            from scripts.taxonomy_validation_services import ConceptDeduplicationValidator
        except ImportError:
            pytest.skip("Validation services not implemented yet")
        
        # Same concept in different tiers (VALID)
        taxonomy_cross_tier = {
            "tiers": {
                "architecture": {
                    "priority": 1,
                    "concepts": ["class", "function"]
                },
                "implementation": {
                    "priority": 2,
                    "concepts": ["class", "decorator"]  # 'class' also in architecture
                }
            }
        }
        
        results = ConceptDeduplicationValidator.validate_deduplication(
            taxonomy_cross_tier
        )
        
        # Should not fail - cross-tier duplication is allowed
        assert all(r.is_passed() or r.is_warning() for r in results), (
            "Validator should allow same concept in different tiers"
        )


class TestValidationOrchestrator:
    """RED: Tests for validation orchestration."""
    
    def test_orchestrator_runs_all_validators(self):
        """
        RED Phase: Verify orchestrator runs all validation strategies.
        
        Orchestrator should run structure, categorization, and deduplication checks.
        """
        try:
            from scripts.taxonomy_validation_services import TaxonomyValidationOrchestrator
        except ImportError:
            pytest.skip("Orchestrator not implemented yet")
        
        # Create valid taxonomy
        valid_taxonomy = {
            "tiers": {
                "architecture": {"priority": 1, "concepts": ["class", "function"]},
                "implementation": {"priority": 2, "concepts": ["decorator", "generator"]},
                "practices": {"priority": 3, "concepts": ["TDD", "refactoring"]}
            }
        }
        
        orchestrator = TaxonomyValidationOrchestrator(valid_taxonomy)
        success = orchestrator.validate_all()
        
        assert isinstance(success, bool), "Orchestrator should return boolean"
        assert success is True, "Valid taxonomy should pass all validation"


class TestValidationIntegration:
    """Integration tests for complete validation workflow."""
    
    def test_can_validate_real_taxonomy_file(self):
        """
        Integration test: Validate against real taxonomy output.
        
        If Tab 3 has generated taxonomy files, validate them.
        """
        try:
            from scripts.validate_taxonomy_generation import validate_taxonomy
        except ImportError:
            pytest.skip("Validation script not implemented yet")
        
        # Check if any taxonomy files exist
        output_dir = Path("workflows/taxonomy_setup/output")
        if not output_dir.exists() or not list(output_dir.glob("*.json")):
            pytest.skip("No taxonomy files generated yet")
        
        taxonomy_files = list(output_dir.glob("*_taxonomy.json"))
        assert len(taxonomy_files) > 0, "Should find at least one taxonomy file"
        
        # Validate first taxonomy file
        result = validate_taxonomy(taxonomy_files[0])
        assert isinstance(result, bool), "Validation should return boolean"
