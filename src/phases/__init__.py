"""
Two-Phase LLM Analysis System - Separated Services

This package contains the refactored two-phase analysis system:
- ContentSelectionService: Phase 1 (metadata analysis, content requests) - STUB
- AnnotationService: Phase 2 (content retrieval, synthesis, scholarly annotation) - STUB
- TwoPhaseOrchestrator: Coordinates Phase 1 → Phase 2 workflow - DELEGATES TO LEGACY

CURRENT STATUS (Sprint 1 Day 1-2):
- Architecture in place, directory structure created
- TwoPhaseOrchestrator provides same interface as AnalysisOrchestrator
- Currently delegates to legacy AnalysisOrchestrator (backward compatible)
- Services are stubs for future full extraction

REFACTORING STRATEGY:
- Phase 1: Create structure (DONE)
- Phase 2: Extract methods incrementally (TODO)
- Phase 3: Replace delegation with real services (TODO)
- Phase 4: Remove legacy orchestrator (TODO)

ARCHITECTURE PATTERNS:
- Single Responsibility Principle (Clean Architecture)
- Dependency Injection (Architecture Patterns with Python Ch. 1)
- Orchestration Pattern (Building Microservices Ch. 4)
- Strangler Fig Pattern (Martin Fowler) - gradually replace legacy
"""

# Import with proper error handling
try:
    from .orchestrator import TwoPhaseOrchestrator
    from .annotation_service import AnnotationService
except ImportError as e:
    # Fallback for import issues
    import sys
    from pathlib import Path
    src_dir = Path(__file__).parent.parent
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))
    
    from phases.orchestrator import TwoPhaseOrchestrator
    from phases.annotation_service import AnnotationService

# ContentSelectionService has two versions - both are stubs for now
__all__ = [
    "TwoPhaseOrchestrator",
    "AnnotationService",
]
