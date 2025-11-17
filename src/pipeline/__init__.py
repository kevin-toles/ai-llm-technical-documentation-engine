"""
Pipeline module for upstream document processing.

This module contains:
1. Legacy pipeline files (convert_pdf_to_json.py, etc.)
2. Adapters (moved to workflow-specific folders in migration)
3. Service Layer (moved to shared/pipeline/pipeline_orchestrator.py)
4. Repositories (repositories/) - Coming soon

Pipeline Flow (Sprint 4):
1. PdfConverterAdapter wraps convert_pdf_to_json.py
2. ChapterGeneratorAdapter wraps chapter_generator_all_text.py
3. MetadataExtractorAdapter wraps generate_chapter_metadata.py
4. PipelineOrchestrator coordinates all stages

Pattern: Adapter Pattern + Service Layer
Reference: 
- Architecture Patterns with Python Ch. 4 (Service Layer)
- Architecture Patterns with Python Ch. 13 (Adapter Pattern)
- docs/analysis/sprint4-pipeline-analysis.md

NOTE: After workflow reorganization migration:
- PipelineOrchestrator moved to shared/pipeline/pipeline_orchestrator.py
- Adapters moved to workflow-specific adapter folders
"""

# For backward compatibility during migration, expose orchestrator from new location
try:
    from shared.pipeline.pipeline_orchestrator import PipelineOrchestrator, PipelineOrchestrationError
    __all__ = ['PipelineOrchestrator', 'PipelineOrchestrationError']
except ImportError:
    __all__ = []
