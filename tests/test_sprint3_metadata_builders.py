"""
Sprint 3.4 Tests: Metadata Builder Extraction

Test-Driven Development (TDD) approach: RED → GREEN → REFACTOR

Purpose:
    Extract metadata building logic from main file to separate builder module.
    Apply Builder pattern and Single Responsibility Principle.

Document References:
    - REFACTORING_PLAN.md: Sprint 3.4 - Extract builders
    - BOOK_TAXONOMY_MATRIX.md: Architecture Patterns with Python (Tier 1, relevance 1.2)
      * Builder pattern, Factory pattern, Repository pattern
      * Separation of concerns, Single Responsibility
    - ARCHITECTURE_GUIDELINES: Builder Pattern, DDD principles
    - PYTHON_GUIDELINES: Class design, type hints, module organization

TDD Cycle:
    RED: This test will FAIL until src/builders/metadata_builder.py is created
    GREEN: Implement MetadataBuilder class with extracted methods
    REFACTOR: Update main file to use MetadataBuilder

Anti-Patterns to Avoid (per Quality Assessment):
    - NO duplicate code
    - NO files >500 lines
    - 100% type hints
    - Single Responsibility Principle
    - NO missing imports
"""

import pytest
from pathlib import Path


class TestMetadataBuilderModule:
    """Test that metadata builder module exists and is properly structured."""
    
    def test_builders_directory_exists(self):
        """
        RED: Test that src/builders/ directory exists.
        
        Expected to FAIL initially - directory doesn't exist yet.
        GREEN: Create src/builders/ directory structure.
        
        Reference: PYTHON_GUIDELINES - Module organization
        """
        builders_dir = Path(__file__).parent.parent / "src" / "builders"
        assert builders_dir.exists(), "src/builders/ directory must exist"
        assert builders_dir.is_dir(), "src/builders/ must be a directory"
    
    def test_metadata_builder_module_exists(self):
        """
        RED: Test that src/builders/metadata_builder.py exists.
        
        Expected to FAIL initially.
        GREEN: Create metadata_builder.py file.
        """
        metadata_builder_file = Path(__file__).parent.parent / "src" / "builders" / "metadata_builder.py"
        assert metadata_builder_file.exists(), "src/builders/metadata_builder.py must exist"
    
    def test_metadata_builder_class_importable(self):
        """
        RED: Test that MetadataBuilder class can be imported.
        
        Expected to FAIL initially.
        GREEN: Implement MetadataBuilder class.
        
        Reference: ARCHITECTURE_GUIDELINES - Builder Pattern
        """
        from src.builders.metadata_builder import MetadataBuilder
        
        assert MetadataBuilder is not None
        assert hasattr(MetadataBuilder, '__name__')


class TestMetadataBuilderMethods:
    """Test MetadataBuilder class methods (core functionality)."""
    
    def test_build_metadata_package_method_exists(self):
        """
        RED: Test that build_metadata_package method exists.
        
        Expected to FAIL initially.
        GREEN: Implement build_metadata_package() method.
        
        This method builds complete metadata package for Phase 1 LLM analysis.
        Extracted from: interactive_llm_system_v3_hybrid_prompt.py lines 1130-1177
        """
        from src.builders.metadata_builder import MetadataBuilder
        
        # Verify method exists
        assert hasattr(MetadataBuilder, 'build_metadata_package')
        
        # Verify it's callable
        assert callable(getattr(MetadataBuilder, 'build_metadata_package'))
    
    def test_build_book_metadata_entry_method_exists(self):
        """
        RED: Test that build_book_metadata_entry method exists.
        
        Expected to FAIL initially.
        GREEN: Implement build_book_metadata_entry() method.
        
        This method builds metadata entry for a single book.
        Extracted from: interactive_llm_system_v3_hybrid_prompt.py lines 1095-1128
        
        Reference: ARCHITECTURE_GUIDELINES - Builder Pattern (incremental construction)
        """
        from src.builders.metadata_builder import MetadataBuilder
        
        assert hasattr(MetadataBuilder, 'build_book_metadata_entry')
        assert callable(getattr(MetadataBuilder, 'build_book_metadata_entry'))
    
    def test_calculate_book_relevance_method_exists(self):
        """
        RED: Test that calculate_book_relevance method exists.
        
        Expected to FAIL initially.
        GREEN: Implement calculate_book_relevance() method.
        
        This method calculates book relevance score based on concept matches.
        Extracted from: interactive_llm_system_v3_hybrid_prompt.py lines 1178-1200
        
        Reference: PYTHON_GUIDELINES - Scoring algorithms, functional programming
        """
        from src.builders.metadata_builder import MetadataBuilder
        
        assert hasattr(MetadataBuilder, 'calculate_book_relevance')
        assert callable(getattr(MetadataBuilder, 'calculate_book_relevance'))


class TestMetadataBuilderTypeHints:
    """Test that MetadataBuilder has 100% type hint coverage."""
    
    def test_build_metadata_package_has_type_hints(self):
        """
        RED: Test that build_metadata_package has proper type hints.
        
        Expected to FAIL initially.
        GREEN: Add complete type hints to method signature.
        
        Quality gate: 100% type hint coverage (per Sprint 3 standards)
        """
        from src.builders.metadata_builder import MetadataBuilder
        import inspect
        
        method = getattr(MetadataBuilder, 'build_metadata_package')
        sig = inspect.signature(method)
        
        # Verify return type annotation exists
        assert sig.return_annotation != inspect.Signature.empty, \
            "build_metadata_package must have return type hint"
    
    def test_builder_follows_single_responsibility(self):
        """
        RED: Test that MetadataBuilder ONLY builds metadata (not loading, not LLM calls).
        
        Expected to FAIL if builder has unrelated responsibilities.
        GREEN: Ensure builder only has metadata construction methods.
        
        Quality gate: Single Responsibility Principle
        Reference: ARCHITECTURE_GUIDELINES - SRP, separation of concerns
        """
        from src.builders.metadata_builder import MetadataBuilder
        
        # Get all public methods (excluding __init__, __dunder__)
        public_methods = [
            name for name in dir(MetadataBuilder)
            if not name.startswith('_') or name in ['build_metadata_package', 'build_book_metadata_entry', 'calculate_book_relevance']
        ]
        
        # All public methods should be about "building" or "calculating" metadata
        for method_name in public_methods:
            if method_name.startswith('__'):
                continue  # Skip dunder methods
            
            assert any(keyword in method_name for keyword in ['build', 'calculate', 'create', 'construct']), \
                f"Method {method_name} doesn't follow builder naming pattern (build/calculate/create/construct)"


class TestMetadataBuilderIntegration:
    """Test MetadataBuilder integration with existing components."""
    
    def test_metadata_builder_accepts_metadata_service(self):
        """
        RED: Test that MetadataBuilder can be initialized with metadata_service.
        
        Expected to FAIL initially.
        GREEN: Add __init__ accepting metadata_service parameter.
        
        Reference: ARCHITECTURE_GUIDELINES - Dependency Injection
        """
        from src.builders.metadata_builder import MetadataBuilder
        import inspect
        
        # Check constructor signature
        sig = inspect.signature(MetadataBuilder.__init__)
        params = list(sig.parameters.keys())
        
        # Should accept metadata_service (or similar dependency)
        assert len(params) >= 2, "MetadataBuilder.__init__ should accept dependencies (self + params)"
    
    def test_metadata_builder_file_size_under_limit(self):
        """
        RED: Test that metadata_builder.py is under 300 lines.
        
        Expected to FAIL if file is too large.
        GREEN: Keep implementation focused and concise.
        
        Quality gate: Files <500 lines (aiming for <300 for builders)
        """
        metadata_builder_file = Path(__file__).parent.parent / "src" / "builders" / "metadata_builder.py"
        
        if metadata_builder_file.exists():
            with open(metadata_builder_file, 'r') as f:
                line_count = len(f.readlines())
            
            assert line_count < 300, \
                f"metadata_builder.py is {line_count} lines (should be <300 for focused builder module)"
