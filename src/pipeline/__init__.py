"""
Pipeline module for upstream document processing.

This module contains:
1. Legacy pipeline files (convert_pdf_to_json.py, etc.)
2. Adapters (src/pipeline/adapters/) - Sprint 4 implementation
3. Service Layer (orchestrator.py) - Coming soon
4. Repositories (repositories/) - Coming soon

Pipeline Flow (Sprint 4):
1. PdfConverterAdapter wraps convert_pdf_to_json.py
2. ChapterGeneratorAdapter wraps chapter_generator_all_text.py
3. MetadataExtractorAdapter wraps generate_chapter_metadata.py
4. PipelineOrchestrator coordinates all stages

Pattern: Adapter Pattern (Architecture Patterns with Python Ch. 13)
Reference: docs/analysis/sprint4-pipeline-analysis.md
"""

# Sprint 4: Expose adapters
from . import adapters

__all__ = [
    'convert_pdf_to_json',
    'chapter_generator_all_text',
    'generate_chapter_metadata',
    'adapters'
]
