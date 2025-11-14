"""
Sprint 3.3 Tests: Centralized Constants Extraction

Test-Driven Development (TDD) approach: RED → GREEN → REFACTOR

Purpose:
    Verify that book title constants are centralized in src/constants.py
    and eliminate duplication across multiple files.

Document References:
    - REFACTORING_PLAN.md: Sprint 3.3 objectives
    - BOOK_TAXONOMY_MATRIX.md: Canonical book titles
    - PYTHON_GUIDELINES Ch. 6: Module organization and constants
    - Quality Assessment: Fix 4 duplicate constants issue

TDD Cycle:
    RED: This test will FAIL until src/constants.py is created
    GREEN: Implement src/constants.py with BookTitles class
    REFACTOR: Update loaders and main file to import from constants

Anti-Patterns to Avoid (from Quality Assessment):
    - NO duplicate constants across files
    - NO missing type hints
    - NO missing imports
    - Apply DRY (Don't Repeat Yourself) principle
"""

from pathlib import Path


class TestBookTitlesConstants:
    """Test centralized book title constants (RED → GREEN → REFACTOR)."""
    
    def test_constants_module_exists(self):
        """
        RED: Test that src/constants.py exists.
        
        Expected to FAIL initially - src/constants.py doesn't exist yet.
        GREEN: Create src/constants.py module.
        """
        constants_file = Path(__file__).parent.parent / "src" / "constants.py"
        assert constants_file.exists(), "src/constants.py must exist"
    
    def test_book_titles_class_exists(self):
        """
        RED: Test that BookTitles class exists in constants module.
        
        Expected to FAIL initially.
        GREEN: Add BookTitles class to src/constants.py.
        """
        from src.constants import BookTitles
        
        # Verify it's a class with the expected name
        assert hasattr(BookTitles, '__name__')
    
    def test_book_titles_has_all_required_constants(self):
        """
        RED: Test that BookTitles has all 4 required book title constants.
        
        Constants identified from duplication analysis:
        - PYTHON_ESSENTIAL_REF
        - FLUENT_PYTHON
        - PYTHON_DISTILLED
        - PYTHON_DATA_ANALYSIS
        
        Expected to FAIL initially.
        GREEN: Add all 4 constants to BookTitles class.
        
        Reference: Quality Assessment Report - 4 duplicated constants
        """
        from src.constants import BookTitles
        
        # All 4 constants must exist
        assert hasattr(BookTitles, 'PYTHON_ESSENTIAL_REF')
        assert hasattr(BookTitles, 'FLUENT_PYTHON')
        assert hasattr(BookTitles, 'PYTHON_DISTILLED')
        assert hasattr(BookTitles, 'PYTHON_DATA_ANALYSIS')
    
    def test_book_titles_correct_values(self):
        """
        RED: Test that book title constants have correct canonical values.
        
        Canonical values from BOOK_TAXONOMY_MATRIX.md:
        - Python Essential Reference 4th
        - Fluent Python 2nd
        - Python Distilled
        - Python Data Analysis 3rd (NOTE: NOT "Python for Data Analysis 3rd")
        
        Expected to FAIL initially.
        GREEN: Set correct string values for all constants.
        
        Note: Found discrepancy in existing code:
        - main file: "Python Data Analysis 3rd" ✓ CORRECT
        - loaders:   "Python for Data Analysis 3rd" ✗ INCORRECT
        
        Resolution: Use canonical name from BOOK_TAXONOMY_MATRIX.md (Priority 2)
        """
        from src.constants import BookTitles
        
        # Canonical values from Book Taxonomy Matrix
        assert BookTitles.PYTHON_ESSENTIAL_REF == "Python Essential Reference 4th"
        assert BookTitles.FLUENT_PYTHON == "Fluent Python 2nd"
        assert BookTitles.PYTHON_DISTILLED == "Python Distilled"
        assert BookTitles.PYTHON_DATA_ANALYSIS == "Python Data Analysis 3rd"
    
    def test_book_titles_are_strings(self):
        """
        RED: Test that all book title constants are strings.
        
        Expected to FAIL initially.
        GREEN: Ensure all constants are str type.
        
        Type safety per PYTHON_GUIDELINES: All constants should have type hints.
        """
        from src.constants import BookTitles
        
        assert isinstance(BookTitles.PYTHON_ESSENTIAL_REF, str)
        assert isinstance(BookTitles.FLUENT_PYTHON, str)
        assert isinstance(BookTitles.PYTHON_DISTILLED, str)
        assert isinstance(BookTitles.PYTHON_DATA_ANALYSIS, str)


class TestNoDuplication:
    """Test that constants are NOT duplicated across files (REFACTOR phase)."""
    
    def test_loaders_imports_from_constants(self):
        """
        RED: Test that loaders/content_loaders.py imports BookTitles.
        
        Expected to FAIL until we refactor loaders to import constants.
        GREEN: Update loaders to use 'from src.constants import BookTitles'.
        
        Anti-pattern from Quality Assessment: Duplicate constants across files
        """
        # Read loaders file source code
        loaders_file = Path(__file__).parent.parent / "src" / "loaders" / "content_loaders.py"
        source = loaders_file.read_text()
        
        # Must import from constants
        assert "from src.constants import BookTitles" in source, \
            "loaders/content_loaders.py must import BookTitles from src.constants"
    
    def test_loaders_does_not_define_duplicate_constants(self):
        """
        RED: Test that loaders does NOT define duplicate constants.
        
        Expected to FAIL while duplicates still exist in loaders file.
        GREEN: Remove duplicate FLUENT_PYTHON, etc. from loaders file.
        
        Quality gate: DRY principle - constants defined once in src/constants.py
        """
        loaders_file = Path(__file__).parent.parent / "src" / "loaders" / "content_loaders.py"
        source = loaders_file.read_text()
        
        # These constants should NOT be defined in loaders anymore
        assert 'PYTHON_ESSENTIAL_REF = "Python Essential Reference 4th"' not in source, \
            "Duplicate PYTHON_ESSENTIAL_REF must be removed from loaders"
        assert 'FLUENT_PYTHON = "Fluent Python 2nd"' not in source, \
            "Duplicate FLUENT_PYTHON must be removed from loaders"
        assert 'PYTHON_DISTILLED = "Python Distilled"' not in source, \
            "Duplicate PYTHON_DISTILLED must be removed from loaders"
        # Check both versions (incorrect and correct)
        assert 'PYTHON_DATA_ANALYSIS = "Python for Data Analysis 3rd"' not in source, \
            "Incorrect PYTHON_DATA_ANALYSIS must be removed from loaders"
        assert 'PYTHON_DATA_ANALYSIS = "Python Data Analysis 3rd"' not in source, \
            "Duplicate PYTHON_DATA_ANALYSIS must be removed from loaders"
    
    def test_main_file_imports_from_constants(self):
        """
        RED: Test that main file imports BookTitles from constants.
        
        Expected to FAIL until we refactor main file.
        GREEN: Update main file to use 'from .constants import BookTitles'.
        
        Note: Accepts both absolute (src.constants) and relative (.constants) imports.
        """
        main_file = Path(__file__).parent.parent / "src" / "interactive_llm_system_v3_hybrid_prompt.py"
        source = main_file.read_text()
        
        # Must import from constants (accept both absolute and relative forms)
        has_absolute_import = "from src.constants import BookTitles" in source
        has_relative_import = "from .constants import BookTitles" in source
        
        assert has_absolute_import or has_relative_import, \
            "Main file must import BookTitles from constants (either 'from src.constants' or 'from .constants')"
    
    def test_main_file_does_not_define_duplicate_constants(self):
        """
        RED: Test that main file does NOT define duplicate constants.
        
        Expected to FAIL while duplicates still exist.
        GREEN: Remove duplicate constants from main file.
        
        Quality gate: Zero duplication allowed in refactored code.
        """
        main_file = Path(__file__).parent.parent / "src" / "interactive_llm_system_v3_hybrid_prompt.py"
        source = main_file.read_text()
        
        # These constants should NOT be defined in main file anymore
        assert 'PYTHON_ESSENTIAL_REF = "Python Essential Reference 4th"' not in source, \
            "Duplicate PYTHON_ESSENTIAL_REF must be removed from main file"
        assert 'FLUENT_PYTHON = "Fluent Python 2nd"' not in source, \
            "Duplicate FLUENT_PYTHON must be removed from main file"
        assert 'PYTHON_DISTILLED = "Python Distilled"' not in source, \
            "Duplicate PYTHON_DISTILLED must be removed from main file"
        assert 'PYTHON_DATA_ANALYSIS = "Python Data Analysis 3rd"' not in source, \
            "Duplicate PYTHON_DATA_ANALYSIS must be removed from main file"
