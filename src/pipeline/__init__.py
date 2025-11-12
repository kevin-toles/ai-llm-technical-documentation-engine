"""
Pipeline module for upstream document processing.

This module contains the pipeline stages that process documents from
PDF through to chapter summaries and metadata extraction, before the
LLM enhancement workflow.

Pipeline Flow:
1. convert_pdf_to_json.py - PDF → JSON conversion
2. chapter_generator_all_text.py - JSON → Chapter summaries
3. generate_chapter_metadata.py - Summaries → Metadata extraction

These files were migrated from tpm-job-finder-poc as part of Phase 4
(Pipeline Integration) per REFACTORING_PLAN.md.

Future work: Adapt these files to use:
- config/settings.py for paths and configuration
- src/providers/ for LLM calls
- src/retry.py for robust API calls
- src/cache.py for caching expensive operations
- src/json_parser.py for JSON validation
"""

__all__ = [
    'convert_pdf_to_json',
    'chapter_generator_all_text',
    'generate_chapter_metadata'
]
