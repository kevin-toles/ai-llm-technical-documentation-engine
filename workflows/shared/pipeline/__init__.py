"""
Pipeline module - Service Layer for Pipeline Integration

Exports:
- PipelineOrchestrator: Coordinates PDF → Chapters → Metadata pipeline
- PipelineOrchestrationError: Exception for pipeline orchestration failures

Reference:
- Architecture Patterns with Python Ch. 4 - Service Layer
"""

from .pipeline_orchestrator import PipelineOrchestrator, PipelineOrchestrationError

__all__ = ['PipelineOrchestrator', 'PipelineOrchestrationError']
