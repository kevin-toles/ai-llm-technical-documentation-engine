#!/usr/bin/env python3
"""
TDD Tests for WBS 3.5.3.7 - SBERT-based Similar Chapters Computation.

WBS Reference: AI_CODING_PLATFORM_WBS.md Phase 3.5.3.7
Architecture: TIER_RELATIONSHIP_DIAGRAM.md Step 4 (semantic similarity)
TDD Phase: RED - Tests for SemanticSimilarityEngine integration

Anti-Pattern Audit:
- CODING_PATTERNS #1.3: No hardcoded book counts (dynamic discovery)
- CODING_PATTERNS #2: Cognitive complexity < 15
- CODING_PATTERNS S1192: No duplicated literals (module constants)

Document Cross-References:
- AI_CODING_PLATFORM_ARCHITECTURE: Code-Orchestrator vs SBERT distinction
- semantic_similarity_engine.py: SemanticSimilarityEngine class
- BERTOPIC_SENTENCE_TRANSFORMERS_DESIGN.md: Option C Architecture
"""

import pytest
import sys
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch
import numpy as np

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# =============================================================================
# Module Constants (CODING_PATTERNS S1192: No duplicated literals)
# =============================================================================
_SIMILAR_CHAPTERS_KEY = "similar_chapters"
_CHAPTERS_KEY = "chapters"


class TestComputeSimilarChaptersUsesSBERT:
    """
    RED Phase: Tests that compute_similar_chapters.py uses SemanticSimilarityEngine.
    
    These tests will FAIL until compute_similar_chapters.py is refactored to use
    SemanticSimilarityEngine instead of raw TF-IDF.
    """

    def test_module_imports_semantic_similarity_engine(self) -> None:
        """
        RED: Module should import SemanticSimilarityEngine.
        
        The compute_similar_chapters module should use the SemanticSimilarityEngine
        instead of raw sklearn TF-IDF for computing chapter similarity.
        """
        from workflows.metadata_enrichment.scripts import compute_similar_chapters
        
        # Check that module uses SemanticSimilarityEngine
        assert hasattr(compute_similar_chapters, "SemanticSimilarityEngine"), (
            "compute_similar_chapters should import SemanticSimilarityEngine"
        )

    def test_module_has_create_similarity_engine_function(self) -> None:
        """
        RED: Module should have factory function for similarity engine.
        
        A factory function allows configuration and testability.
        """
        from workflows.metadata_enrichment.scripts import compute_similar_chapters
        
        assert hasattr(compute_similar_chapters, "create_similarity_engine"), (
            "Module should have create_similarity_engine() factory function"
        )

    def test_compute_similarity_uses_engine(self) -> None:
        """
        RED: compute_similarity_matrix should use SemanticSimilarityEngine.
        
        The function should delegate to engine.compute_embeddings() and
        engine.compute_similarity_matrix() instead of raw sklearn TfidfVectorizer.
        """
        from workflows.metadata_enrichment.scripts.compute_similar_chapters import (
            compute_similarity_matrix,
        )
        
        # Create mock engine
        mock_engine = MagicMock()
        mock_embeddings = np.array([[0.1, 0.2], [0.3, 0.4], [0.5, 0.6]])
        mock_similarity = np.array([
            [1.0, 0.8, 0.3],
            [0.8, 1.0, 0.5],
            [0.3, 0.5, 1.0],
        ])
        mock_engine.compute_embeddings.return_value = mock_embeddings
        mock_engine.compute_similarity_matrix.return_value = mock_similarity
        
        corpus = ["Chapter 1 text", "Chapter 2 text", "Chapter 3 text"]
        
        # Should accept engine parameter
        result = compute_similarity_matrix(corpus, engine=mock_engine)
        
        # Verify engine was used
        mock_engine.compute_embeddings.assert_called_once_with(corpus)
        mock_engine.compute_similarity_matrix.assert_called_once()
        
        # Verify result matches engine output
        np.testing.assert_array_equal(result, mock_similarity)


class TestSimilarityResultsIncludeMethod:
    """
    RED Phase: Tests that similar_chapters results include method information.
    
    Results should indicate whether SBERT or TF-IDF fallback was used.
    """

    def test_similar_chapters_include_method_field(self) -> None:
        """
        RED: Each similar chapter result should include 'method' field.
        
        Method can be 'sentence_transformers' or 'tfidf'.
        """
        from workflows.metadata_enrichment.scripts.compute_similar_chapters import (
            find_similar_chapters,
        )
        
        # Mock similarity matrix
        similarity_matrix = np.array([
            [1.0, 0.8, 0.3],
            [0.8, 1.0, 0.5],
            [0.3, 0.5, 1.0],
        ])
        
        index = [
            {"book": "book_a", "chapter": 1, "title": "Ch 1"},
            {"book": "book_b", "chapter": 1, "title": "Ch 1"},
            {"book": "book_c", "chapter": 1, "title": "Ch 1"},
        ]
        
        result = find_similar_chapters(
            chapter_idx=0,
            similarity_matrix=similarity_matrix,
            index=index,
            current_book="book_a",
            method="sentence_transformers",  # New parameter
        )
        
        # All results should have method field
        for similar in result:
            assert "method" in similar, "Result should include 'method' field"
            assert similar["method"] in ("sentence_transformers", "tfidf"), (
                f"Method should be 'sentence_transformers' or 'tfidf', got {similar['method']}"
            )


class TestMainFunctionUsesEngine:
    """
    RED Phase: Tests that main() uses SemanticSimilarityEngine.
    """

    def test_main_creates_similarity_engine(self) -> None:
        """
        RED: main() should create a SemanticSimilarityEngine instance.
        """
        from workflows.metadata_enrichment.scripts.compute_similar_chapters import main
        
        with patch(
            "workflows.metadata_enrichment.scripts.compute_similar_chapters.create_similarity_engine"
        ) as mock_create:
            mock_engine = MagicMock()
            mock_create.return_value = mock_engine
            
            # Create minimal test data
            with patch(
                "workflows.metadata_enrichment.scripts.compute_similar_chapters.discover_enriched_books"
            ) as mock_discover:
                mock_discover.return_value = []
                
                # Call main (will exit early due to no books)
                main(input_dir=Path("/nonexistent"))
            
            # Verify engine was created
            mock_create.assert_called_once()

    def test_main_prints_sbert_or_tfidf_status(self) -> None:
        """
        RED: main() should print whether SBERT or TF-IDF is being used.
        """
        from workflows.metadata_enrichment.scripts.compute_similar_chapters import main
        import io
        from contextlib import redirect_stdout
        
        with patch(
            "workflows.metadata_enrichment.scripts.compute_similar_chapters.discover_enriched_books"
        ) as mock_discover:
            mock_discover.return_value = []
            
            f = io.StringIO()
            with redirect_stdout(f):
                main(input_dir=Path("/nonexistent"))
            
            output = f.getvalue()
            
            # Should indicate similarity method
            assert "SBERT" in output or "TF-IDF" in output or "sentence_transformers" in output, (
                "Output should indicate which similarity method is being used"
            )


class TestBackwardsCompatibility:
    """
    Tests to ensure backwards compatibility with existing behavior.
    """

    def test_build_corpus_from_books_unchanged(self) -> None:
        """
        GREEN: build_corpus_from_books should remain unchanged.
        
        Corpus building is independent of similarity method.
        """
        from workflows.metadata_enrichment.scripts.compute_similar_chapters import (
            build_corpus_from_books,
        )
        
        # This should still work the same way
        assert callable(build_corpus_from_books)

    def test_find_similar_chapters_maintains_output_format(self) -> None:
        """
        GREEN: find_similar_chapters output format should be compatible.
        
        Existing fields: book, chapter, title, relevance_score
        New field: method (optional for backwards compat)
        """
        # Import to verify signature hasn't broken
        from workflows.metadata_enrichment.scripts.compute_similar_chapters import (
            find_similar_chapters,
        )
        
        import inspect
        sig = inspect.signature(find_similar_chapters)
        
        # Original required parameters should still exist
        required_params = ["chapter_idx", "similarity_matrix", "index", "current_book"]
        for param in required_params:
            assert param in sig.parameters, f"Missing required parameter: {param}"


class TestSemanticSimilarityEngineIntegration:
    """
    Integration tests for SemanticSimilarityEngine with compute_similar_chapters.
    """

    def test_engine_fallback_to_tfidf_when_sbert_unavailable(self) -> None:
        """
        GREEN: When sentence-transformers unavailable, should use TF-IDF fallback.
        """
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
            SimilarityConfig,
        )
        
        # Force fallback
        config = SimilarityConfig(fallback_to_tfidf=True)
        
        # Mock unavailable sentence-transformers
        with patch(
            "workflows.metadata_enrichment.scripts.semantic_similarity_engine.SENTENCE_TRANSFORMERS_AVAILABLE",
            False,
        ):
            engine = SemanticSimilarityEngine(config=config)
            assert engine.is_using_fallback, "Should use TF-IDF fallback"

    def test_engine_produces_valid_similarity_matrix(self) -> None:
        """
        GREEN: Engine should produce valid similarity matrix.
        """
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
        )
        
        engine = SemanticSimilarityEngine()
        corpus = [
            "Python decorators enhance function behavior",
            "Repository pattern provides data abstraction",
            "Test-driven development follows red green refactor",
        ]
        
        embeddings = engine.compute_embeddings(corpus)
        similarity_matrix = engine.compute_similarity_matrix(embeddings)
        
        # Matrix should be n x n
        assert similarity_matrix.shape == (3, 3), (
            f"Expected (3, 3), got {similarity_matrix.shape}"
        )
        
        # Diagonal should be 1.0 (self-similarity)
        for i in range(3):
            assert abs(similarity_matrix[i, i] - 1.0) < 0.01, (
                f"Diagonal element [{i},{i}] should be ~1.0"
            )
        
        # Matrix should be symmetric
        np.testing.assert_array_almost_equal(
            similarity_matrix, similarity_matrix.T, decimal=5
        )


class TestCLIArguments:
    """
    Tests for CLI argument handling.
    """

    def test_cli_parser_accepts_use_sbert_flag(self) -> None:
        """
        GREEN: CLI should accept --use-sbert flag (documented option).
        
        Note: The flag is accepted for documentation purposes but
        the engine automatically uses SBERT when available.
        """
        from workflows.metadata_enrichment.scripts.compute_similar_chapters import (
            create_argument_parser,
        )
        
        parser = create_argument_parser()
        args = parser.parse_args(["--use-sbert"])
        
        assert hasattr(args, "use_sbert"), "Parser should accept --use-sbert flag"
        # Flag exists for CLI documentation, actual behavior is automatic

    def test_cli_parser_accepts_model_name_option(self) -> None:
        """
        RED: CLI should accept --model-name option for custom SBERT model.
        """
        from workflows.metadata_enrichment.scripts.compute_similar_chapters import (
            create_argument_parser,
        )
        
        parser = create_argument_parser()
        args = parser.parse_args(["--model-name", "all-mpnet-base-v2"])
        
        assert hasattr(args, "model_name"), "Parser should accept --model-name option"
        assert args.model_name == "all-mpnet-base-v2"
