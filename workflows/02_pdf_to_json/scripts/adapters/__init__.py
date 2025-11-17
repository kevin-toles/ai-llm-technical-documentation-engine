"""
Pipeline adapters package

Wraps legacy pipeline functions with clean adapter interfaces.
Pattern: Adapter Pattern (Architecture Patterns with Python Ch. 13)
"""

from .pdf_converter import PdfConverterAdapter, PdfConversionError
from .chapter_generator import ChapterGeneratorAdapter, ChapterGenerationError
from .metadata_extractor import MetadataExtractorAdapter, MetadataExtractionError

__all__ = [
    "PdfConverterAdapter",
    "PdfConversionError",
    "ChapterGeneratorAdapter",
    "ChapterGenerationError",
    "MetadataExtractorAdapter",
    "MetadataExtractionError",
]
