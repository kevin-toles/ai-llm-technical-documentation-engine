"""
Pipeline adapters package

Wraps legacy pipeline functions with clean adapter interfaces.
Pattern: Adapter Pattern (Architecture Patterns with Python Ch. 13)
"""

from .pdf_converter import PdfConverterAdapter, PdfConversionError

__all__ = ["PdfConverterAdapter", "PdfConversionError"]
