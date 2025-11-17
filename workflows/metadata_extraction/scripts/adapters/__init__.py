"""
Pipeline adapters package - Metadata Extractor Adapter

Wraps metadata extraction with clean adapter interface.
Pattern: Adapter Pattern (Architecture Patterns with Python Ch. 13)
"""

from .metadata_extractor import MetadataExtractorAdapter, MetadataExtractionError

__all__ = [
    "MetadataExtractorAdapter",
    "MetadataExtractionError",
]
