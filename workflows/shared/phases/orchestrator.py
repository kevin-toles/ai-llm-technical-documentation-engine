"""
Two-Phase Orchestrator - Coordinates Phase 1 and Phase 2

This is a lightweight coordinator that will eventually replace AnalysisOrchestrator.
For now, it delegates to the original implementation while demonstrating the
separation of concerns pattern.

Sprint 1 Day 1-2: Phase separation architecture
"""

from typing import List, Any, TYPE_CHECKING

if TYPE_CHECKING:
    # Type hints only - not imported at runtime
    from workflows.shared.interactive_llm_system_v3_hybrid_prompt import (  # type: ignore[import-not-found]
        ScholarlyAnnotation
    )

# Lazy import at runtime to avoid import issues
def _get_legacy_classes():
    """Lazy import to handle both module and package execution."""
    try:
        # Try relative import first (when run as package)
        from ..interactive_llm_system_v3_hybrid_prompt import (
            AnalysisOrchestrator,
            ScholarlyAnnotation
        )
        return AnalysisOrchestrator, ScholarlyAnnotation
    except (ImportError, ValueError):
        # Fall back to absolute import (when run as module)
        import sys
        from pathlib import Path
        src_dir = Path(__file__).parent.parent
        if str(src_dir) not in sys.path:
            sys.path.insert(0, str(src_dir))
        
        import interactive_llm_system_v3_hybrid_prompt
        return (
            interactive_llm_system_v3_hybrid_prompt.AnalysisOrchestrator,
            interactive_llm_system_v3_hybrid_prompt.ScholarlyAnnotation
        )



class TwoPhaseOrchestrator:
    """
    Coordinates Phase 1 (content selection) and Phase 2 (annotation generation).
    
    ARCHITECTURE:
    - Dependency Injection: Services injected via constructor
    - Orchestration Pattern: Coordinates workflow between phases
    - Configuration: Uses config.settings for all runtime parameters
    
    CURRENT IMPLEMENTATION:
    - Delegates to original AnalysisOrchestrator (legacy code)
    - Provides same interface for backward compatibility
    - Prepares for future extraction of Phase 1/2 services
    
    FUTURE:
    - Phase 1 will use ContentSelectionService
    - Phase 2 will use AnnotationService
    - This orchestrator will coordinate between them
    """
    
    def __init__(self, metadata_service: Any, llm_available: bool = True):
        """
        Initialize orchestrator with dependencies.
        
        Args:
            metadata_service: Metadata extraction service
            llm_available: Whether LLM is available
        """
        # Lazy load the legacy orchestrator class
        legacy_orchestrator_class, _ = _get_legacy_classes()
        
        # For now, delegate to legacy orchestrator
        self._legacy_orchestrator = legacy_orchestrator_class(
            metadata_service=metadata_service,
            llm_available=llm_available
        )
        
        # Future: Replace with:
        # self._content_selector = ContentSelectionService(metadata_service, llm_available)
        # self._annotator = AnnotationService(metadata_service, llm_available)
    
    def analyze_chapter(
        self,
        chapter_num: int,
        chapter_title: str,
        chapter_concepts: List[str],
        chapter_excerpt: str
    ) -> 'ScholarlyAnnotation':
        """
        Analyze chapter using Python-guided approach (Scenario 1).
        
        Flow:
        1. Python extracts concepts
        2. Phase 1: LLM validates and requests content
        3. Phase 2: LLM generates annotation
        
        Args:
            chapter_num: Chapter number
            chapter_title: Chapter title
            chapter_concepts: Pre-extracted concepts
            chapter_excerpt: Short excerpt
            
        Returns:
            ScholarlyAnnotation with cross-references
        """
        # Delegate to legacy implementation
        return self._legacy_orchestrator.analyze_chapter(
            chapter_num=chapter_num,
            chapter_title=chapter_title,
            chapter_concepts=chapter_concepts,
            chapter_excerpt=chapter_excerpt
        )
        
        # Future implementation:
        # # Phase 1: Content Selection
        # metadata_response = self._content_selector.select_content_python_guided(
        #     chapter_num, chapter_title, chapter_concepts, chapter_excerpt
        # )
        #
        # # Phase 2: Annotation Generation  
        # annotation = self._annotator.generate_annotation(
        #     chapter_num, chapter_title, chapter_concepts, chapter_excerpt, metadata_response
        # )
        #
        # return annotation
    
    def analyze_chapter_comprehensive(
        self,
        chapter_num: int,
        chapter_title: str,
        chapter_full_text: str
    ) -> 'ScholarlyAnnotation':
        """
        Analyze chapter using comprehensive LLM-driven approach (Scenario 2).
        
        Flow:
        1. Phase 1: LLM reads full chapter, extracts concepts, requests content
        2. Phase 2: LLM generates annotation
        
        Args:
            chapter_num: Chapter number
            chapter_title: Chapter title
            chapter_full_text: Full chapter text
            
        Returns:
            ScholarlyAnnotation with cross-references
        """
        # Delegate to legacy implementation
        return self._legacy_orchestrator.analyze_chapter_comprehensive(
            chapter_num=chapter_num,
            chapter_title=chapter_title,
            chapter_full_text=chapter_full_text
        )
        
        # Future implementation:
        # # Phase 1: Content Selection
        # metadata_response = self._content_selector.select_content_comprehensive(
        #     chapter_num, chapter_title, chapter_full_text
        # )
        #
        # # Phase 2: Annotation Generation
        # annotation = self._annotator.generate_annotation_comprehensive(
        #     chapter_num, chapter_title, chapter_full_text, metadata_response
        # )
        #
        # return annotation


# Already imported at top
