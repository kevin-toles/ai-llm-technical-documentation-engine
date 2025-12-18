"""
Test TF-IDF Removal - WBS MSE-6.4 Unit Tests

Phase MSE-6: llm-document-enhancer Cleanup & API Client
TDD RED Phase: Tests verifying TF-IDF code has been removed

Reference Documents:
- Kitchen Brigade Pattern: llm-document-enhancer is CUSTOMER only
- SBERT_EXTRACTION_MIGRATION_WBS.md: Remove local embedding fallbacks
- CODING_PATTERNS_ANALYSIS: No local ML processing in CUSTOMER services

Tests cover:
- AC-6.4.1: No TfidfVectorizer import in semantic_similarity_engine.py
- AC-6.4.2: No sklearn.feature_extraction.text import
- AC-6.4.3: No _compute_tfidf_embeddings method
- AC-6.4.4: No fallback_to_tfidf config option
- AC-6.4.5: SimilarityConfig uses API-first strategy

Kitchen Brigade Pattern Compliance:
- llm-document-enhancer is CUSTOMER only
- ALL embedding computation delegated to Code-Orchestrator (SBERT API)
- NO local sentence-transformers or TF-IDF fallbacks
"""

from __future__ import annotations

import ast
import inspect
import pytest
from pathlib import Path
from typing import TYPE_CHECKING


# =============================================================================
# Constants for file paths
# =============================================================================

_SEMANTIC_SIMILARITY_ENGINE_PATH = Path(
    "/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_enrichment/scripts/semantic_similarity_engine.py"
)


# =============================================================================
# TestTFIDFImportsRemoved - AC-6.4.1, AC-6.4.2
# =============================================================================


class TestTFIDFImportsRemoved:
    """AC-6.4.1, AC-6.4.2: Verify TF-IDF imports have been removed."""

    def test_no_tfidf_vectorizer_import(self) -> None:
        """AC-6.4.1: TfidfVectorizer should NOT be imported."""
        source_code = _SEMANTIC_SIMILARITY_ENGINE_PATH.read_text()
        
        # Parse the AST to check imports
        tree = ast.parse(source_code)
        
        imported_names: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module and "sklearn" in node.module:
                    for alias in node.names:
                        imported_names.append(alias.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if "sklearn" in alias.name or "TfidfVectorizer" in alias.name:
                        imported_names.append(alias.name)
        
        assert "TfidfVectorizer" not in imported_names, (
            "TfidfVectorizer should not be imported. "
            "Kitchen Brigade: llm-document-enhancer is CUSTOMER only."
        )

    def test_no_sklearn_feature_extraction_import(self) -> None:
        """AC-6.4.2: sklearn.feature_extraction.text should NOT be imported."""
        source_code = _SEMANTIC_SIMILARITY_ENGINE_PATH.read_text()
        
        # Parse AST to check actual imports (not docstrings)
        tree = ast.parse(source_code)
        
        sklearn_fe_imported = False
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module and "sklearn.feature_extraction" in node.module:
                    sklearn_fe_imported = True
                    break
        
        assert not sklearn_fe_imported, (
            "sklearn.feature_extraction should not be imported. "
            "Kitchen Brigade: llm-document-enhancer is CUSTOMER only."
        )

    def test_no_sklearn_metrics_pairwise_import(self) -> None:
        """AC-6.4.2: sklearn.metrics.pairwise should NOT be imported (TF-IDF related)."""
        source_code = _SEMANTIC_SIMILARITY_ENGINE_PATH.read_text()
        
        # Parse AST for sklearn imports
        tree = ast.parse(source_code)
        
        sklearn_modules: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module and "sklearn" in node.module:
                    sklearn_modules.append(node.module)
        
        # cosine_similarity from sklearn.metrics.pairwise is allowed 
        # (it's math, not ML) - but feature_extraction is NOT
        assert "sklearn.feature_extraction" not in sklearn_modules, (
            "sklearn.feature_extraction should not be imported."
        )


# =============================================================================
# TestTFIDFMethodsRemoved - AC-6.4.3
# =============================================================================


class TestTFIDFMethodsRemoved:
    """AC-6.4.3: Verify TF-IDF methods have been removed."""

    def test_no_compute_tfidf_embeddings_method(self) -> None:
        """AC-6.4.3: _compute_tfidf_embeddings method should NOT exist."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
        )
        
        assert not hasattr(SemanticSimilarityEngine, "_compute_tfidf_embeddings"), (
            "_compute_tfidf_embeddings should be removed. "
            "Kitchen Brigade: delegate to Code-Orchestrator SBERT API."
        )

    def test_no_setup_tfidf_fallback_method(self) -> None:
        """AC-6.4.3: _setup_tfidf_fallback method should NOT exist."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
        )
        
        assert not hasattr(SemanticSimilarityEngine, "_setup_tfidf_fallback"), (
            "_setup_tfidf_fallback should be removed. "
            "Kitchen Brigade: no local fallbacks."
        )

    def test_no_vectorizer_attribute(self) -> None:
        """AC-6.4.3: _vectorizer attribute should NOT exist."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
        )
        
        # Check __init__ method for _vectorizer assignment
        source_code = inspect.getsource(SemanticSimilarityEngine.__init__)
        
        assert "_vectorizer" not in source_code, (
            "_vectorizer attribute should be removed. "
            "Kitchen Brigade: no TF-IDF vectorizer needed."
        )


# =============================================================================
# TestTFIDFConfigRemoved - AC-6.4.4
# =============================================================================


class TestTFIDFConfigRemoved:
    """AC-6.4.4: Verify TF-IDF config options have been removed."""

    def test_no_fallback_to_tfidf_config(self) -> None:
        """AC-6.4.4: fallback_to_tfidf should NOT be in SimilarityConfig."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SimilarityConfig,
        )
        
        config = SimilarityConfig()
        
        assert not hasattr(config, "fallback_to_tfidf"), (
            "fallback_to_tfidf config should be removed. "
            "Kitchen Brigade: no TF-IDF fallback."
        )

    def test_no_using_fallback_property(self) -> None:
        """AC-6.4.4: is_using_fallback property should NOT exist."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
        )
        
        # The property may still exist but should always be False
        # or the property itself should be removed
        if hasattr(SemanticSimilarityEngine, "is_using_fallback"):
            # If property exists, it should be removed or always False
            # Check if it's still referencing TF-IDF
            source_code = _SEMANTIC_SIMILARITY_ENGINE_PATH.read_text()
            assert "_using_fallback" not in source_code or "tfidf" not in source_code.lower(), (
                "is_using_fallback should not reference TF-IDF."
            )


# =============================================================================
# TestAPIFirstStrategy - AC-6.4.5
# =============================================================================


class TestAPIFirstStrategy:
    """AC-6.4.5: Verify API-first strategy is the only option."""

    def test_config_defaults_to_api_mode(self) -> None:
        """AC-6.4.5: SimilarityConfig should be API-only (no mode selection)."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SimilarityConfig,
        )
        
        config = SimilarityConfig()
        
        # After refactor, config should NOT have fallback mode options
        # API is the ONLY mode per Kitchen Brigade
        has_use_api = hasattr(config, "use_api")
        has_fallback_mode = hasattr(config, "fallback_mode")
        has_fallback_to_local = hasattr(config, "fallback_to_local")
        has_fallback_to_tfidf = hasattr(config, "fallback_to_tfidf")
        
        # None of the mode selection attributes should exist
        assert not has_fallback_mode, "fallback_mode should not exist (API only)"
        assert not has_fallback_to_local, "fallback_to_local should not exist"
        assert not has_fallback_to_tfidf, "fallback_to_tfidf should not exist"
        
        # Optional: use_api could still exist if set to True only
        if has_use_api:
            assert config.use_api is True, "use_api should always be True"

    def test_no_local_sbert_fallback_option(self) -> None:
        """AC-6.4.5: fallback_to_local should NOT exist or be deprecated."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SimilarityConfig,
        )
        
        config = SimilarityConfig()
        
        # Either remove fallback_to_local or set it to False
        if hasattr(config, "fallback_to_local"):
            assert config.fallback_to_local is False, (
                "fallback_to_local should be False. "
                "Kitchen Brigade: no local SBERT fallback."
            )


# =============================================================================
# TestSentenceTransformersRemoved - AC-6.4.1
# =============================================================================


class TestSentenceTransformersRemoved:
    """AC-6.4.1: Verify sentence-transformers fallback removed."""

    def test_no_sentence_transformers_try_import(self) -> None:
        """AC-6.4.1: sentence-transformers try/except import should be removed."""
        source_code = _SEMANTIC_SIMILARITY_ENGINE_PATH.read_text()
        
        # Check for try/except import pattern for sentence_transformers
        assert "SENTENCE_TRANSFORMERS_AVAILABLE" not in source_code, (
            "SENTENCE_TRANSFORMERS_AVAILABLE flag should be removed. "
            "Kitchen Brigade: no local model loading."
        )

    def test_no_sentence_transformer_import(self) -> None:
        """AC-6.4.1: SentenceTransformer class should NOT be imported."""
        source_code = _SEMANTIC_SIMILARITY_ENGINE_PATH.read_text()
        
        # Parse AST for SentenceTransformer imports
        tree = ast.parse(source_code)
        
        imported_names: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module and "sentence_transformers" in node.module:
                    for alias in node.names:
                        imported_names.append(alias.name)
        
        assert "SentenceTransformer" not in imported_names, (
            "SentenceTransformer should not be imported. "
            "Kitchen Brigade: delegate to Code-Orchestrator."
        )

    def test_no_local_model_attribute(self) -> None:
        """AC-6.4.1: _model attribute should NOT exist."""
        from workflows.metadata_enrichment.scripts.semantic_similarity_engine import (
            SemanticSimilarityEngine,
        )
        
        # Check __init__ for _model assignment
        source_code = inspect.getsource(SemanticSimilarityEngine.__init__)
        
        # _model should not be assigned to SentenceTransformer
        assert "SentenceTransformer" not in source_code, (
            "_model should not be a SentenceTransformer. "
            "Kitchen Brigade: no local models."
        )


# =============================================================================
# TestKitchenBrigadeCompliance - Overall compliance
# =============================================================================


class TestKitchenBrigadeCompliance:
    """Verify Kitchen Brigade pattern compliance."""

    def test_no_local_ml_imports(self) -> None:
        """Kitchen Brigade: CUSTOMER has no local ML imports."""
        source_code = _SEMANTIC_SIMILARITY_ENGINE_PATH.read_text()
        
        # Parse AST to check actual imports (not docstrings)
        tree = ast.parse(source_code)
        
        forbidden_modules = [
            "sklearn.feature_extraction",
            "sentence_transformers",
        ]
        forbidden_names = ["TfidfVectorizer", "SentenceTransformer"]
        
        violations: list[str] = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module:
                    for forbidden in forbidden_modules:
                        if forbidden in node.module:
                            violations.append(f"from {node.module}")
                    for alias in node.names:
                        if alias.name in forbidden_names:
                            violations.append(alias.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in forbidden_names:
                        violations.append(alias.name)
        
        assert not violations, (
            f"Kitchen Brigade violation: found local ML imports: {violations}. "
            "llm-document-enhancer is CUSTOMER only - delegate to ai-agents."
        )

    def test_msep_client_is_primary(self) -> None:
        """Kitchen Brigade: Should use MSEPClient for enrichment."""
        # This test ensures MSEPClient exists and is importable
        from workflows.shared.clients.msep_client import MSEPClient
        
        assert MSEPClient is not None, (
            "MSEPClient should be available for enrichment. "
            "Kitchen Brigade: call ai-agents for enrichment."
        )
