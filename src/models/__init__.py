"""
Data models for LLM document enhancer.

Sprint 3.1 - Architecture Refactoring: Extract Data Models

Following Document Hierarchy:
- REFACTORING_PLAN.md: Sprint 3 - Break down large file
- ARCHITECTURE_GUIDELINES: Single Responsibility Principle, Separation of Concerns
- PYTHON_GUIDELINES: Dataclasses, type hints, immutability patterns
- BOOK_TAXONOMY_MATRIX: Engineering Practices tier (language fundamentals)

References:
- Architecture Patterns with Python Ch. 8: State Machines
- Architecture Patterns with Python Ch. 9: Commands and Events
- Microservices Ch. 6: Data Transfer Objects
- Python Distilled Ch. 7: Dataclasses with validation
- Python Essential Reference Ch. 7: Factory method pattern
"""

from .analysis_models import (
    AnalysisPhase,
    ContentRequest,
    LLMMetadataResponse,
    ScholarlyAnnotation
)

__all__ = [
    'AnalysisPhase',
    'ContentRequest',
    'LLMMetadataResponse',
    'ScholarlyAnnotation'
]
