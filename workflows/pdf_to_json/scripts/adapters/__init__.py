"""
Pipeline adapters package - PDF Converter Adapter

Wraps PDF to JSON conversion with clean adapter interface.
Pattern: Adapter Pattern (Architecture Patterns with Python Ch. 13)
"""

from .pdf_converter import PdfConverterAdapter, PdfConversionError

__all__ = [
    "PdfConverterAdapter",
    "PdfConversionError",
]
