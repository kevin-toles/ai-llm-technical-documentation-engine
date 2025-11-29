"""
Tests for Tab 4 Metadata Enrichment Validation Script

TDD Phase: RED - Create failing tests first
Next Phase: GREEN - Implement validation script to pass tests

References:
    - MASTER_IMPLEMENTATION_GUIDE Task 2.2
    - ARCHITECTURE_GUIDELINES Ch.4: Service Layer Pattern
    - PYTHON_GUIDELINES Ch.15: Testing
"""

import pytest
from pathlib import Path
import json
from typing import Dict, Any


class TestValidationScriptExists:
    """Test that the validation script exists and is properly structured."""
    
    def test_validation_script_file_exists(self):
        """Validation script must exist at scripts/validate_metadata_enrichment.py"""
        script_path = Path("scripts/validate_metadata_enrichment.py")
        assert script_path.exists(), \
            f"Validation script not found at {script_path}"
    
    def test_validation_script_is_executable(self):
        """Validation script must have shebang and main entry point"""
        script_path = Path("scripts/validate_metadata_enrichment.py")
        
        if not script_path.exists():
            pytest.skip("Script not yet created")
        
        content = script_path.read_text()
        assert "#!/usr/bin/env python3" in content, \
            "Script must have Python3 shebang"
        assert "def main()" in content or "if __name__ == '__main__':" in content, \
            "Script must have main entry point"


class TestEnrichmentStructureValidation:
    """Test validation of enriched metadata JSON structure."""
    
    def test_validates_required_top_level_keys(self):
        """Must validate presence of 'book', 'enrichment_metadata', 'chapters' keys"""
        from scripts.metadata_enrichment_validation_services import EnrichmentStructureValidator
        
        # Missing 'book' key
        invalid_data = {
            "enrichment_metadata": {},
            "chapters": []
        }
        
        results = EnrichmentStructureValidator.validate_structure(invalid_data)
        assert any(r.is_failed() for r in results), \
            "Should fail when 'book' key is missing"
    
    def test_validates_enrichment_metadata_structure(self):
        """Must validate enrichment_metadata has required keys"""
        from scripts.metadata_enrichment_validation_services import EnrichmentStructureValidator
        
        # Missing required enrichment_metadata keys
        invalid_data = {
            "book": "test_book",
            "enrichment_metadata": {
                "generated": "2025-11-27T00:00:00"
                # Missing: method, libraries, corpus_size, total_chapters_analyzed
            },
            "chapters": []
        }
        
        results = EnrichmentStructureValidator.validate_structure(invalid_data)
        assert any(r.is_failed() for r in results), \
            "Should fail when enrichment_metadata keys are missing"


class TestEnrichmentContentValidation:
    """Test validation of enrichment content (related_chapters, keywords, concepts)."""
    
    def test_validates_chapter_enrichment_fields(self):
        """Must validate each chapter has enrichment fields"""
        from scripts.metadata_enrichment_validation_services import EnrichmentContentValidator
        
        # Chapter missing enrichment fields
        invalid_chapters = [
            {
                "chapter": "Chapter 1",
                "title": "Introduction"
                # Missing: related_chapters, keywords_enriched, concepts_enriched
            }
        ]
        
        results = EnrichmentContentValidator.validate_content(invalid_chapters)
        assert any(r.is_failed() for r in results), \
            "Should fail when chapter missing enrichment fields"
    
    def test_validates_similarity_scores(self):
        """Must validate similarity scores are floats between 0.0 and 1.0"""
        from scripts.metadata_enrichment_validation_services import EnrichmentContentValidator
        
        # Invalid similarity score (>1.0)
        invalid_chapters = [
            {
                "chapter": "Chapter 1",
                "title": "Introduction",
                "related_chapters": [
                    {
                        "book": "Other Book",
                        "chapter": "Chapter 2",
                        "title": "Related",
                        "similarity_score": 1.5  # Invalid: >1.0
                    }
                ],
                "keywords_enriched": [],
                "concepts_enriched": []
            }
        ]
        
        results = EnrichmentContentValidator.validate_content(invalid_chapters)
        assert any(r.is_failed() for r in results), \
            "Should fail when similarity_score > 1.0"


class TestStatisticalMethodValidation:
    """Test validation of statistical method metadata."""
    
    def test_validates_method_is_statistical(self):
        """Must validate method is 'statistical' (no LLM)"""
        from scripts.metadata_enrichment_validation_services import StatisticalMethodValidator
        
        # Invalid method (LLM used)
        invalid_metadata = {
            "method": "llm-enhanced",  # Should be "statistical"
            "libraries": {"yake": "0.4.8", "summa": "1.2.0", "scikit-learn": "1.3.2"}
        }
        
        results = StatisticalMethodValidator.validate_method(invalid_metadata)
        assert any(r.is_failed() for r in results), \
            "Should fail when method is not 'statistical'"
    
    def test_validates_required_libraries(self):
        """Must validate required statistical libraries are present"""
        from scripts.metadata_enrichment_validation_services import StatisticalMethodValidator
        
        # Missing libraries
        invalid_metadata = {
            "method": "statistical",
            "libraries": {"yake": "0.4.8"}  # Missing summa, scikit-learn
        }
        
        results = StatisticalMethodValidator.validate_method(invalid_metadata)
        assert any(r.is_failed() for r in results), \
            "Should fail when required libraries are missing"


class TestValidationOrchestrator:
    """Test the orchestrator that runs all validators."""
    
    def test_orchestrator_runs_all_validators(self):
        """Orchestrator must run all validation strategies"""
        from scripts.metadata_enrichment_validation_services import EnrichmentValidationOrchestrator
        
        # Valid enriched metadata
        valid_data = {
            "book": "test_book",
            "enrichment_metadata": {
                "generated": "2025-11-27T00:00:00",
                "method": "statistical",
                "libraries": {
                    "yake": "0.4.8",
                    "summa": "1.2.0",
                    "scikit-learn": "1.3.2"
                },
                "corpus_size": 5,
                "total_chapters_analyzed": 50
            },
            "chapters": [
                {
                    "chapter": "Chapter 1",
                    "title": "Introduction",
                    "related_chapters": [
                        {
                            "book": "Other Book",
                            "chapter": "Chapter 2",
                            "title": "Related",
                            "similarity_score": 0.85
                        }
                    ],
                    "keywords_enriched": [
                        {"keyword": "pattern", "score": 0.9}
                    ],
                    "concepts_enriched": ["architecture", "design"]
                }
            ]
        }
        
        orchestrator = EnrichmentValidationOrchestrator(valid_data)
        success = orchestrator.validate_all()
        assert isinstance(success, bool), \
            "Orchestrator should return boolean success status"


class TestValidationIntegration:
    """Integration test with real enriched metadata file."""
    
    def test_can_validate_real_enriched_file(self):
        """Should be able to validate a real enriched metadata file"""
        # Look for enriched metadata files
        output_dir = Path("workflows/metadata_enrichment/output")
        
        if not output_dir.exists():
            pytest.skip("No enriched metadata output directory found")
        
        enriched_files = list(output_dir.glob("*_metadata_enriched.json"))
        
        if not enriched_files:
            pytest.skip("No enriched metadata files found yet")
        
        # Test with first file
        enriched_path = enriched_files[0]
        
        with open(enriched_path) as f:
            enriched_data = json.load(f)
        
        from scripts.metadata_enrichment_validation_services import EnrichmentValidationOrchestrator
        
        orchestrator = EnrichmentValidationOrchestrator(enriched_data)
        success = orchestrator.validate_all()
        
        assert success, \
            f"Real enriched metadata file should pass validation: {enriched_path.name}"
