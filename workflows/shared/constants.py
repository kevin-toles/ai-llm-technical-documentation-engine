"""
Centralized Constants Module

Sprint 3.3 - TDD GREEN: Extract constants to eliminate duplication

Document References:
    - REFACTORING_PLAN.md: Sprint 3.3 - Configuration management
    - BOOK_TAXONOMY_MATRIX.md: Canonical book titles (Priority 2)
    - PYTHON_GUIDELINES Ch. 6: Module organization and constants
    - PYTHON_GUIDELINES Ch. 7: Type hints for all public APIs
    - Quality Assessment Report: Fix 4 duplicate constants issue

Purpose:
    Centralize book title constants to eliminate duplication across:
    - src/interactive_llm_system_v3_hybrid_prompt.py
    - src/loaders/content_loaders.py
    
    Implements DRY (Don't Repeat Yourself) principle per Quality Assessment.

Anti-Patterns Avoided:
    - ✓ NO duplicate constants across files
    - ✓ 100% type hints (all constants explicitly typed)
    - ✓ Single Responsibility: This module ONLY defines constants
    - ✓ File size <100 lines (currently ~80 lines with docs)

TDD Cycle:
    RED: tests/test_sprint3_constants.py fails (9/9 tests)
    GREEN: This file created - make tests pass
    REFACTOR: Update loaders and main file to import from here

Quality Gates:
    - All 9 Sprint 3.3 tests must pass
    - All 48 existing tests must continue passing (zero regressions)
    - SonarLint clean (no new issues)
    - 100% type hint coverage
"""

from typing import Final


class BookTitles:
    """
    Canonical book title constants for citation and content loading.
    
    Source of Truth: BOOK_TAXONOMY_MATRIX.md (Document Priority 2)
    
    These constants are used across the codebase for:
    - Citation map keys (Chicago-style author/title formatting)
    - JSON filename matching
    - Book selection and filtering
    
    Pattern: Constants Class (PYTHON_GUIDELINES Ch. 6)
    Benefits:
    - Centralized source of truth (DRY principle)
    - Namespace isolation (BookTitles.* prevents naming conflicts)
    - Type-safe (Final prevents reassignment)
    - Easy to import and maintain
    
    References:
        - BOOK_TAXONOMY_MATRIX.md: Engineering Practices tier (Tier 3)
        - Quality Assessment: Fix for 4 duplicated constants
        - Previous locations:
          * src/interactive_llm_system_v3_hybrid_prompt.py lines 70-73
          * src/loaders/content_loaders.py lines 38-41
    
    Note on PYTHON_DATA_ANALYSIS:
        Canonical name is "Python Data Analysis 3rd" (without "for")
        as per BOOK_TAXONOMY_MATRIX.md. Previous code had inconsistency:
        - Main file: "Python Data Analysis 3rd" ✓ CORRECT
        - Loaders:   "Python for Data Analysis 3rd" ✗ INCORRECT
        Now resolved to taxonomy canonical name.
    """
    
    # Engineering Practices Tier - Python Language Books
    # Tier 3 per BOOK_TAXONOMY_MATRIX.md
    
    PYTHON_ESSENTIAL_REF: Final[str] = "Python Essential Reference 4th"
    """
    David Beazley's authoritative Python language reference.
    
    Taxonomy: Tier 3 - Engineering Practices
    Relevance Weight: 1.0 (standard)
    Focus: Language specification, built-ins, standard library
    """
    
    FLUENT_PYTHON: Final[str] = "Fluent Python 2nd"
    """
    Luciano Ramalho's advanced Pythonic patterns and protocols.
    
    Taxonomy: Tier 3 - Engineering Practices
    Relevance Weight: 1.2 (highest in tier)
    Focus: Idiomatic Python, protocols, metaprogramming
    """
    
    PYTHON_DISTILLED: Final[str] = "Python Distilled"
    """
    David Beazley's concise best practices and core concepts.
    
    Taxonomy: Tier 3 - Engineering Practices
    Relevance Weight: 1.1
    Focus: Best practices, core language features
    """
    
    PYTHON_DATA_ANALYSIS: Final[str] = "Python Data Analysis 3rd"
    """
    Wes McKinney's data analysis with pandas and NumPy.
    
    Taxonomy: Tier 3 - Engineering Practices
    Relevance Weight: 0.8 (lower - specialized)
    Focus: pandas, NumPy, data wrangling, visualization
    
    NOTE: Canonical name per BOOK_TAXONOMY_MATRIX.md
    (NOT "Python for Data Analysis 3rd" - previous inconsistency fixed)
    """
    
    # Architecture & Microservices Tier
    # Added for S1192 compliance - eliminating duplicated literals
    
    ARCH_PATTERNS_PYTHON: Final[str] = "Architecture Patterns with Python"
    """
    Percival & Gregory's domain-driven design with Python.
    
    Taxonomy: Architecture patterns and clean architecture
    Focus: DDD, Repository pattern, Event-driven architecture
    """
    
    BUILDING_MICROSERVICES: Final[str] = "Building Microservices"
    """
    Sam Newman's microservices architecture guide.
    
    Taxonomy: Architecture patterns
    Focus: Service decomposition, integration patterns, deployment
    """
    
    PYTHON_COOKBOOK: Final[str] = "Python Cookbook 3rd"
    """
    Beazley & Jones Python recipes and best practices.
    
    Taxonomy: Tier 3 - Engineering Practices
    Focus: Practical recipes, advanced techniques
    """


# Module-level validation (executed at import time)
# Ensures all constants are non-empty strings
if __name__ != "__main__":
    # Only validate when imported (not when running as script)
    _required_attrs = [
        "PYTHON_ESSENTIAL_REF",
        "FLUENT_PYTHON", 
        "PYTHON_DISTILLED",
        "PYTHON_DATA_ANALYSIS",
        "ARCH_PATTERNS_PYTHON",
        "BUILDING_MICROSERVICES",
        "PYTHON_COOKBOOK",
    ]
    
    for attr_name in _required_attrs:
        if not hasattr(BookTitles, attr_name):
            raise AttributeError(f"BookTitles missing required constant: {attr_name}")
        
        value = getattr(BookTitles, attr_name)
        if not isinstance(value, str) or not value:
            raise ValueError(
                f"BookTitles.{attr_name} must be non-empty string, got: {value!r}"
            )


# Export only the BookTitles class
__all__ = ["BookTitles"]
