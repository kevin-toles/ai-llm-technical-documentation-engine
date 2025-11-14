"""
TDD RED: Tests for data models extraction (Sprint 3.1)

Following TDD Workflow:
1. RED: Write failing tests first
2. GREEN: Extract models to src/models/analysis_models.py
3. REFACTOR: Clean and verify zero regressions

Document References:
- REFACTORING_PLAN.md: Sprint 3 - Break down large file
- ARCHITECTURE_GUIDELINES: Single Responsibility Principle
- PYTHON_GUIDELINES: Dataclasses, type hints, immutability
- BOOK_TAXONOMY_MATRIX: Engineering Practices tier

Sprint 3.1 Objectives:
- Extract 4 data classes from interactive_llm_system_v3_hybrid_prompt.py
- Create src/models/analysis_models.py (<200 lines)
- Maintain backward compatibility
- Zero regressions in existing 50 tests
"""

from pathlib import Path


def test_models_module_exists():
    """
    TDD RED: Verify src/models/analysis_models.py exists.
    
    This test will FAIL until we create the module.
    """
    models_path = Path("src/models/analysis_models.py")
    assert models_path.exists(), f"Expected {models_path} to exist"


def test_analysis_phase_enum_extracted():
    """
    TDD GREEN: Verify AnalysisPhase enum is importable from models.
    
    Updated to match actual enum values from extracted code.
    """
    from src.models.analysis_models import AnalysisPhase
    
    # Verify enum values exist (from actual implementation)
    assert hasattr(AnalysisPhase, 'INITIAL')
    assert hasattr(AnalysisPhase, 'METADATA_SENT')
    assert hasattr(AnalysisPhase, 'CONTENT_REQUESTED')
    assert hasattr(AnalysisPhase, 'ANALYSIS_COMPLETE')
    assert hasattr(AnalysisPhase, 'FAILED')


def test_content_request_extracted():
    """
    TDD GREEN: Verify ContentRequest dataclass is importable.
    
    Updated to match actual ContentRequest signature.
    """
    from src.models.analysis_models import ContentRequest
    
    # Verify can create instance (using actual field names)
    request = ContentRequest(
        book_name="Test Book",
        pages=[1, 2],
        rationale="test reason",
        priority=1
    )
    assert request.book_name == "Test Book"
    assert request.pages == [1, 2]
    assert request.rationale == "test reason"
    

def test_llm_metadata_response_extracted():
    """
    TDD RED: Verify LLMMetadataResponse dataclass is importable.
    
    This test will FAIL until we extract the class.
    """
    from src.models.analysis_models import LLMMetadataResponse
    
    # Verify can create instance
    response = LLMMetadataResponse(
        validation_summary="test validation",
        gap_analysis="test gaps",
        analysis_strategy="test strategy",
        content_requests=[]
    )
    assert response.validation_summary == "test validation"


def test_scholarly_annotation_extracted():
    """
    TDD GREEN: Verify ScholarlyAnnotation dataclass is importable.
    
    Updated to match actual ScholarlyAnnotation signature.
    """
    from src.models.analysis_models import ScholarlyAnnotation
    
    # Verify can create instance (using actual field names)
    annotation = ScholarlyAnnotation(
        chapter_number=1,
        chapter_title="Test Chapter",
        annotation_text="test content",
        sources_cited=["source1"],
        concepts_validated=["concept1"],
        gaps_identified=[]
    )
    assert annotation.annotation_text == "test content"
    assert len(annotation.sources_cited) == 1


def test_backward_compatibility():
    """
    TDD RED: Verify models can still be imported from original location.
    
    This ensures zero regressions in existing code.
    This test will FAIL until we update imports.
    """
    # Should be able to import from new location
    from src.models.analysis_models import (
        AnalysisPhase,
        ContentRequest,
        LLMMetadataResponse,
        ScholarlyAnnotation
    )
    
    # Should also work from original file (for backward compatibility)
    from src.interactive_llm_system_v3_hybrid_prompt import (
        AnalysisPhase as OldAnalysisPhase,
        ContentRequest as OldContentRequest,
        LLMMetadataResponse as OldLLMMetadataResponse,
        ScholarlyAnnotation as OldScholarlyAnnotation
    )
    
    # Should be same classes
    assert AnalysisPhase is OldAnalysisPhase
    assert ContentRequest is OldContentRequest
    assert LLMMetadataResponse is OldLLMMetadataResponse
    assert ScholarlyAnnotation is OldScholarlyAnnotation
