"""
Builders Module - Data Construction and Packaging

Sprint 3.4 - TDD GREEN: Extract builder classes from interactive_llm_system_v3_hybrid_prompt.py

Following Document Hierarchy:
- REFACTORING_PLAN.md: Sprint 3.4 - Extract builders (~200-300 lines)
- BOOK_TAXONOMY_MATRIX.md: Architecture Patterns with Python (Tier 1, relevance 1.2)
  * Builder Pattern: Incremental construction of complex objects
  * Repository Pattern: Data access abstraction
  * Single Responsibility Principle
- ARCHITECTURE_GUIDELINES: Builder Pattern, DDD, Separation of Concerns
- PYTHON_GUIDELINES: Class design, type hints, functional programming

Module Purpose:
    Extract metadata and content building logic from main orchestrator.
    Apply Builder pattern for complex object construction.
    
TDD Cycle:
    RED: tests/test_sprint3_metadata_builders.py created with 10 failing tests
    GREEN: This module implements MetadataBuilder to pass tests
    REFACTOR: Main file updated to use MetadataBuilder

Anti-Patterns Avoided (per Quality Assessment):
    - NO duplicate code
    - File size <300 lines (builder modules should be focused)
    - 100% type hints
    - Single Responsibility: ONLY builds metadata/content, no LLM calls or loading
"""

__all__ = ["MetadataBuilder"]
