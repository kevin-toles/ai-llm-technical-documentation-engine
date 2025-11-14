"""
Pipeline module for upstream document processing.

This module contains:
1. Legacy pipeline files (convert_pdf_to_json.py, etc.)
2. Adapters (src/pipeline/adapters/) - Sprint 4 Phase 1
3. Service Layer (orchestrator.py) - Sprint 4 Phase 2
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
"""

# Sprint 4: Expose adapters and orchestrator
from . import adapters
from .orchestrator import PipelineOrchestrator, PipelineOrchestrationError

__all__ = [
    'convert_pdf_to_json',
    'chapter_generator_all_text',
    'generate_chapter_metadata',
    'adapters',
    'PipelineOrchestrator',
    'PipelineOrchestrationError',
]
