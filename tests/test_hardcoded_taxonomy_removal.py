#!/usr/bin/env python3
"""
TDD RED Phase - Tests for Hardcoded Taxonomy Removal

These tests will FAIL initially and pass after refactoring is complete.
Following strict TDD discipline: RED → GREEN → REFACTOR

Test Strategy:
1. Verify imports removed from interactive_llm_system_v3_hybrid_prompt.py
2. Verify dead functions deleted (_prefilter_books_by_taxonomy, analyze_chapter_with_all_books)
3. Verify no book_taxonomy references remain in active code
4. Verify TaxonomyConfig removed from settings

Document Hierarchy (Priority):
1. REFACTORING_PLAN.md - Sprint 3 complete, confirms removal approach
2. BOOK_TAXONOMY_MATRIX.md - Documents OLD system being removed
3. ARCHITECTURE_GUIDELINES - Repository pattern, Service Layer (preserved)
4. HARDCODED_TAXONOMY_REMOVAL_PLAN.md - 8-phase removal guide

Architecture Alignment:
- Following Service Layer pattern (Architecture Patterns with Python Ch. 4)
- Maintaining Repository pattern for metadata access (Ch. 2)
- Preserving DDD principles (Ch. 1) - only removing hardcoded taxonomy
"""

import pytest
import ast
import inspect
from pathlib import Path


class TestHardcodedTaxonomyRemoval:
    """Test suite for hardcoded taxonomy removal (TDD RED phase)."""

    @pytest.fixture
    def interactive_llm_file(self):
        """Return path to interactive_llm_system_v3_hybrid_prompt.py."""
        return Path(__file__).parent.parent / "workflows" / "llm_enhancement" / "scripts" / "interactive_llm_system_v3_hybrid_prompt.py"

    @pytest.fixture
    def content_selection_impl_file(self):
        """Return path to content_selection_impl.py."""
        return Path(__file__).parent.parent / "workflows" / "llm_enhancement" / "scripts" / "phases" / "content_selection_impl.py"

    @pytest.fixture
    def settings_file(self):
        """Return path to config/settings.py."""
        return Path(__file__).parent.parent / "config" / "settings.py"

    def test_book_taxonomy_import_removed_from_interactive_llm(self, interactive_llm_file):
        """
        RED Phase Test 1: Verify book_taxonomy import removed.
        
        Should fail initially because import still exists at lines 45-52.
        Will pass after GREEN phase removes import block.
        """
        content = interactive_llm_file.read_text()
        
        # Should NOT contain any book_taxonomy imports
        assert "from workflows.w01_taxonomy_setup.scripts import book_taxonomy" not in content, \
            "book_taxonomy import still present (lines 45-52) - should be removed"
        
        assert "import book_taxonomy" not in content, \
            "Direct book_taxonomy import found - should be removed"
        
        assert "TAXONOMY_AVAILABLE" not in content, \
            "TAXONOMY_AVAILABLE flag still present - no longer needed"

    def test_prefilter_books_function_removed(self, interactive_llm_file):
        """
        RED Phase Test 2: Verify _prefilter_books_by_taxonomy deleted.
        
        Should fail initially because function exists at lines 159-220.
        Will pass after GREEN phase deletes dead code.
        """
        content = interactive_llm_file.read_text()
        
        # Function should not exist
        assert "_prefilter_books_by_taxonomy" not in content, \
            "_prefilter_books_by_taxonomy function still exists (lines 159-220) - should be deleted"
        
        # Should not reference hardcoded taxonomy functions
        assert "score_books_for_concepts" not in content, \
            "score_books_for_concepts call still present - should be removed"
        
        assert "ALL_BOOKS" not in content, \
            "ALL_BOOKS reference still present - should be removed"

    def test_analyze_chapter_with_all_books_removed(self, interactive_llm_file):
        """
        RED Phase Test 3: Verify analyze_chapter_with_all_books deleted.
        
        Should fail initially because function exists at lines 365-600.
        Will pass after GREEN phase deletes dead code.
        
        Per HARDCODED_TAXONOMY_REMOVAL_PLAN.md: This function is dead code
        (grep shows NO callers) and calls _prefilter_books_by_taxonomy.
        """
        content = interactive_llm_file.read_text()
        
        # Dead function should not exist
        assert "def analyze_chapter_with_all_books" not in content, \
            "analyze_chapter_with_all_books function still exists - should be deleted (dead code)"
        
        assert "analyze_chapter_with_all_books" not in content, \
            "References to analyze_chapter_with_all_books found - should be completely removed"

    def test_book_registry_references_removed(self, interactive_llm_file):
        """
        RED Phase Test 4: Verify BOOK_REGISTRY references removed.
        
        Should fail initially if any BOOK_REGISTRY references exist.
        Will pass after GREEN phase removes hardcoded taxonomy references.
        """
        content = interactive_llm_file.read_text()
        
        # Should not use hardcoded BOOK_REGISTRY
        assert "BOOK_REGISTRY" not in content, \
            "BOOK_REGISTRY reference still present - should be removed"

    def test_content_selection_impl_book_taxonomy_removed(self, content_selection_impl_file):
        """
        RED Phase Test 5: Verify book_taxonomy removed from content_selection_impl.py.
        
        Should fail initially if book_taxonomy imports exist.
        Will pass after GREEN phase analysis determines if methods are called.
        
        Per HARDCODED_TAXONOMY_REMOVAL_PLAN.md Phase 2:
        - Check if methods are called by UI
        - If yes: update to use concept taxonomy JSON
        - If no: delete the methods
        """
        if not content_selection_impl_file.exists():
            pytest.skip("content_selection_impl.py not found")
        
        content = content_selection_impl_file.read_text()
        
        # Should not import from book_taxonomy
        assert "from workflows.taxonomy_setup.scripts.book_taxonomy import" not in content, \
            "book_taxonomy import still present in content_selection_impl.py"
        
        # Should not use hardcoded scoring
        assert "score_books_for_concepts" not in content, \
            "score_books_for_concepts still used in content_selection_impl.py"

    def test_taxonomy_config_removed_from_settings(self, settings_file):
        """
        RED Phase Test 6: Verify TaxonomyConfig class removed from settings.py.
        
        Should fail initially because TaxonomyConfig exists at lines 68-98.
        Will pass after GREEN phase removes obsolete config.
        
        Per HARDCODED_TAXONOMY_REMOVAL_PLAN.md Phase 5:
        TaxonomyConfig is NOT used by new concept taxonomy system.
        """
        if not settings_file.exists():
            pytest.skip("config/settings.py not found")
        
        content = settings_file.read_text()
        
        # TaxonomyConfig should be removed
        assert "class TaxonomyConfig" not in content, \
            "TaxonomyConfig class still exists (lines 68-98) - should be deleted"
        
        # Related settings should be removed
        assert "min_relevance" not in content or "TaxonomyConfig" not in content, \
            "TaxonomyConfig settings still present"
        
        assert "enable_prefilter" not in content or "TaxonomyConfig" not in content, \
            "enable_prefilter setting still present"

    def test_no_get_recommended_books_calls(self, interactive_llm_file):
        """
        RED Phase Test 7: Verify get_recommended_books removed.
        
        Should fail if _get_recommended_books_from_taxonomy method exists.
        Will pass after analyzing if method is called and updating/deleting.
        """
        content = interactive_llm_file.read_text()
        
        # Should not call hardcoded book taxonomy functions
        assert "get_recommended_books" not in content or "from book_taxonomy" not in content, \
            "get_recommended_books from book_taxonomy still referenced"

    def test_prompts_preserved_only_taxonomy_language_removed(self, interactive_llm_file):
        """
        RED Phase Test 8: Verify prompts preserved (only taxonomy references removed).
        
        CRITICAL: Per user requirement - "only remove or revise the specific language
        regarding the hardcoded taxonomy approach, everything else in the prompt is
        to stay the same"
        
        This test ensures we don't accidentally remove valid prompt content.
        """
        content = interactive_llm_file.read_text()
        
        # Key prompt markers should still exist (proves we didn't delete prompts)
        assert "Phase 1" in content or "phase1" in content, \
            "Phase 1 prompt content removed - should be preserved"
        
        assert "Phase 2" in content or "phase2" in content, \
            "Phase 2 prompt content removed - should be preserved"
        
        # Should not reference hardcoded taxonomy CODE (imports/functions)
        # Documentation references like "BOOK_TAXONOMY_MATRIX.md" are OK
        code_lines_with_taxonomy = [
            line for line in content.split('\n')
            if ('from' in line or 'import' in line) and 'book_taxonomy' in line
        ]
        
        assert len(code_lines_with_taxonomy) == 0, \
            f"Found {len(code_lines_with_taxonomy)} import lines with book_taxonomy - should be 0"


class TestArchitecturePreservation:
    """
    Verify architectural patterns are PRESERVED during refactoring.
    
    Per ARCHITECTURE_GUIDELINES:
    - Repository Pattern (Ch. 2) - metadata access preserved
    - Service Layer (Ch. 4) - orchestration preserved
    - DDD principles (Ch. 1) - domain models preserved
    """

    @pytest.fixture
    def interactive_llm_file(self):
        """Return path to interactive_llm_system_v3_hybrid_prompt.py."""
        return Path(__file__).parent.parent / "workflows" / "llm_enhancement" / "scripts" / "interactive_llm_system_v3_hybrid_prompt.py"

    def test_metadata_extraction_service_preserved(self, interactive_llm_file):
        """Verify MetadataExtractionService import preserved (Repository pattern)."""
        content = interactive_llm_file.read_text()
        assert "MetadataExtractionService" in content, \
            "MetadataExtractionService removed - should be preserved (Repository pattern)"

    def test_orchestrator_class_preserved(self, interactive_llm_file):
        """Verify AnalysisOrchestrator class preserved (Service Layer pattern)."""
        content = interactive_llm_file.read_text()
        assert "class AnalysisOrchestrator" in content or "AnalysisOrchestrator" in content, \
            "AnalysisOrchestrator removed - should be preserved (Service Layer)"

    def test_llm_integration_preserved(self, interactive_llm_file):
        """Verify call_llm integration preserved (external service adapter)."""
        content = interactive_llm_file.read_text()
        assert "call_llm" in content, \
            "call_llm removed - should be preserved (LLM service integration)"

    def test_two_phase_workflow_preserved(self, interactive_llm_file):
        """
        Verify two-phase analysis workflow preserved.
        
        Per REFACTORING_PLAN.md:
        "Two-Phase Request/Response Pattern (Microservice APIs Ch. 6)"
        """
        content = interactive_llm_file.read_text()
        
        # Phase 1 and Phase 2 should exist
        phase_indicators = [
            "phase_1" in content.lower(),
            "phase_2" in content.lower(),
            "phase1" in content.lower(),
            "phase2" in content.lower()
        ]
        
        assert any(phase_indicators), \
            "Two-phase workflow indicators missing - should be preserved"


class TestConceptTaxonomyUsage:
    """
    Verify NEW concept taxonomy system is used (not hardcoded taxonomy).
    
    Per HARDCODED_TAXONOMY_REMOVAL_PLAN.md:
    "The NEW system uses generate_concept_taxonomy.py (data-driven from JSON)"
    """

    def test_generate_concept_taxonomy_exists(self):
        """Verify generate_concept_taxonomy.py exists (new system)."""
        taxonomy_script = Path(__file__).parent.parent / "workflows" / "taxonomy_setup" / "scripts" / "generate_concept_taxonomy.py"
        
        # Check both possible locations
        alt_location = Path(__file__).parent.parent / "workflows" / "01_taxonomy_setup" / "scripts" / "generate_concept_taxonomy.py"
        
        assert taxonomy_script.exists() or alt_location.exists(), \
            "generate_concept_taxonomy.py not found - new system missing"

    def test_concept_taxonomy_json_loadable(self):
        """
        Verify concept taxonomy JSON can be loaded.
        
        This is the NEW data-driven approach that replaces hardcoded book_taxonomy.py
        """
        taxonomy_paths = [
            Path(__file__).parent.parent / "workflows" / "taxonomy_setup" / "output" / "python_taxonomy.json",
            Path(__file__).parent.parent / "inputs" / "taxonomy" / "python_taxonomy.json"
        ]
        
        taxonomy_exists = any(p.exists() for p in taxonomy_paths)
        
        if not taxonomy_exists:
            pytest.skip("Concept taxonomy JSON not yet generated (run Tab 5 in UI)")
        
        # Load and verify structure
        import json
        for path in taxonomy_paths:
            if path.exists():
                with open(path) as f:
                    taxonomy_data = json.load(f)
                
                # Verify it's the new format (tiers with concepts)
                assert "tiers" in taxonomy_data, \
                    "Taxonomy JSON missing 'tiers' - not new concept taxonomy format"
                
                break


if __name__ == "__main__":
    # Run with: pytest tests/test_hardcoded_taxonomy_removal.py -v
    pytest.main([__file__, "-v", "--tb=short"])
