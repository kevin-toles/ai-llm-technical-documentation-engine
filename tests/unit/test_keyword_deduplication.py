"""
Test suite for Keyword Deduplication and N-gram Cleanup.

Following TDD RED → GREEN → REFACTOR cycle per ARCHITECTURE_GUIDELINES Ch. 1.
Tests written FIRST to define expected behavior for:
1. Stemming-based deduplication (model/models/modeling → model)
2. N-gram cleanup (remove phrases with repeated words)
3. Increased top_n threshold (10 → 20)

Document References:
- DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md: Phase 2 Enhancement
- ARCHITECTURE_GUIDELINES Ch. 4: Adapter pattern, single responsibility
- PYTHON_GUIDELINES Ch. 7: Function design, dataclass usage
- ANTI_PATTERN_ANALYSIS: Avoid copy-paste, proper Optional typing

TDD Status: RED phase - Expected to FAIL until deduplication implemented
"""

import pytest
from typing import List, Tuple, Dict, Any

# Import will fail initially (RED phase) - this is expected
try:
    from workflows.metadata_extraction.scripts.adapters.statistical_extractor import (
        StatisticalExtractor,
        _deduplicate_by_stem,
        _clean_ngram_duplicates,
        _is_valid_keyword,
        _is_valid_concept,
    )
    IMPORTS_AVAILABLE = True
except ImportError:
    StatisticalExtractor = None
    _deduplicate_by_stem = None
    _clean_ngram_duplicates = None
    _is_valid_keyword = None
    _is_valid_concept = None
    IMPORTS_AVAILABLE = False


class TestStemmingDeduplication:
    """
    Test stemming-based deduplication for keywords and concepts.
    
    Per ARCHITECTURE_GUIDELINES Ch. 4: Single responsibility - dedup function.
    Per PYTHON_GUIDELINES Ch. 7: Function should do one thing well.
    """

    @pytest.fixture
    def extractor(self):
        """Fixture providing StatisticalExtractor instance."""
        if StatisticalExtractor is None:
            pytest.skip("StatisticalExtractor not implemented yet (RED phase)")
        return StatisticalExtractor()

    # RED Phase Test 1: Basic stemming deduplication
    def test_deduplicate_by_stem_basic(self):
        """
        Test that word forms with same root are deduplicated.
        
        Acceptance Criteria:
        - model, models, modeling → keep only first occurrence
        - Different roots are preserved
        - Order is maintained (first occurrence wins)
        """
        if _deduplicate_by_stem is None:
            pytest.skip("_deduplicate_by_stem not implemented yet (RED phase)")
        
        # Arrange - keywords with score tuples
        keywords = [
            ("model", 0.01),
            ("models", 0.02),
            ("modeling", 0.03),
            ("architecture", 0.04),
            ("architectures", 0.05),
            ("pattern", 0.06),
        ]
        
        # Act
        result = _deduplicate_by_stem(keywords)
        
        # Assert
        assert len(result) == 3, f"Should keep 3 unique stems, got {len(result)}"
        result_terms = [kw for kw, _ in result]
        assert "model" in result_terms, "Should keep 'model' (first form)"
        assert "models" not in result_terms, "Should remove 'models' (duplicate stem)"
        assert "modeling" not in result_terms, "Should remove 'modeling' (duplicate stem)"
        assert "architecture" in result_terms, "Should keep 'architecture'"
        assert "pattern" in result_terms, "Should keep 'pattern'"

    # RED Phase Test 2: Stemming preserves scores
    def test_deduplicate_by_stem_preserves_scores(self):
        """
        Test that deduplication preserves original scores.
        
        Per DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN: YAKE scores must be maintained.
        """
        if _deduplicate_by_stem is None:
            pytest.skip("_deduplicate_by_stem not implemented yet (RED phase)")
        
        # Arrange
        keywords = [
            ("learning", 0.001),
            ("learner", 0.002),
            ("learned", 0.003),
        ]
        
        # Act
        result = _deduplicate_by_stem(keywords)
        
        # Assert - first occurrence with its score preserved
        assert len(result) == 1
        assert result[0] == ("learning", 0.001), "Should preserve first occurrence with score"

    # RED Phase Test 3: Multi-word keyword stemming
    def test_deduplicate_by_stem_multiword(self):
        """
        Test stemming handles multi-word keywords correctly.
        
        'machine learning' and 'machine learnings' have same stems.
        """
        if _deduplicate_by_stem is None:
            pytest.skip("_deduplicate_by_stem not implemented yet (RED phase)")
        
        # Arrange
        keywords = [
            ("machine learning", 0.01),
            ("deep learning", 0.02),
            ("machine learner", 0.03),  # Same stem as "machine learning"
        ]
        
        # Act
        result = _deduplicate_by_stem(keywords)
        
        # Assert - "machine learner" has same stem signature as "machine learning"
        result_terms = [kw for kw, _ in result]
        assert len(result) == 2, f"Should keep 2 unique phrases, got {result_terms}"
        assert "machine learning" in result_terms
        assert "deep learning" in result_terms

    # RED Phase Test 4: Empty input handling
    def test_deduplicate_by_stem_empty(self):
        """
        Test graceful handling of empty input.
        
        Per PYTHON_GUIDELINES Ch. 8: Handle edge cases gracefully.
        """
        if _deduplicate_by_stem is None:
            pytest.skip("_deduplicate_by_stem not implemented yet (RED phase)")
        
        # Act
        result = _deduplicate_by_stem([])
        
        # Assert
        assert result == [], "Should return empty list for empty input"

    # RED Phase Test 5: Concepts deduplication (list of strings)
    def test_deduplicate_concepts_by_stem(self):
        """
        Test stemming deduplication for concept lists (strings only).
        
        Concepts are List[str], not List[Tuple[str, float]].
        """
        if _deduplicate_by_stem is None:
            pytest.skip("_deduplicate_by_stem not implemented yet (RED phase)")
        
        # Arrange - concepts as strings
        concepts = ["model", "models", "modeling", "data", "dataset", "training"]
        
        # Act - function should handle both tuples and strings
        result = _deduplicate_by_stem(concepts)
        
        # Assert
        assert len(result) == 4, f"Should keep 4 unique stems: model, data, dataset, training. Got {result}"
        assert "model" in result or ("model", None) in result


class TestNgramCleanup:
    """
    Test n-gram cleanup to remove phrases with repeated words.
    
    Per ARCHITECTURE_GUIDELINES: Remove noise like "Models Models Applications".
    """

    # RED Phase Test 6: Basic n-gram cleanup
    def test_clean_ngram_duplicates_basic(self):
        """
        Test removal of n-grams with repeated words.
        
        "Models Models Applications" → removed (repeated "Models")
        "Machine Learning Models" → kept (no repeats)
        """
        if _clean_ngram_duplicates is None:
            pytest.skip("_clean_ngram_duplicates not implemented yet (RED phase)")
        
        # Arrange
        keywords = [
            ("Models Models Applications", 0.01),
            ("Machine Learning Models", 0.02),
            ("model model language", 0.03),  # Has exact repeat
            ("Large Language Models", 0.04),
        ]
        
        # Act
        result = _clean_ngram_duplicates(keywords)
        
        # Assert
        result_terms = [kw for kw, _ in result]
        assert "Models Models Applications" not in result_terms, "Should remove repeated word n-gram"
        assert "model model language" not in result_terms, "Should remove repeated word n-gram"
        assert "Machine Learning Models" in result_terms, "Should keep valid n-gram"
        assert "Large Language Models" in result_terms, "Should keep valid n-gram"

    # RED Phase Test 7: Case-insensitive duplicate detection
    def test_clean_ngram_duplicates_case_insensitive(self):
        """
        Test that duplicate detection is case-insensitive.
        
        "Model model" has repeated word (case-insensitive).
        """
        if _clean_ngram_duplicates is None:
            pytest.skip("_clean_ngram_duplicates not implemented yet (RED phase)")
        
        # Arrange
        keywords = [
            ("Model model learning", 0.01),
            ("API api Design", 0.02),
            ("Python Programming", 0.03),
        ]
        
        # Act
        result = _clean_ngram_duplicates(keywords)
        
        # Assert
        result_terms = [kw for kw, _ in result]
        assert len(result) == 1, f"Should only keep 'Python Programming', got {result_terms}"
        assert "Python Programming" in result_terms

    # RED Phase Test 8: Single word passes through
    def test_clean_ngram_single_words(self):
        """
        Test that single-word keywords pass through unchanged.
        
        Single words can't have duplicates.
        """
        if _clean_ngram_duplicates is None:
            pytest.skip("_clean_ngram_duplicates not implemented yet (RED phase)")
        
        # Arrange
        keywords = [
            ("Python", 0.01),
            ("architecture", 0.02),
            ("Models Models", 0.03),  # Should be removed
        ]
        
        # Act
        result = _clean_ngram_duplicates(keywords)
        
        # Assert
        result_terms = [kw for kw, _ in result]
        assert "Python" in result_terms
        assert "architecture" in result_terms
        assert "Models Models" not in result_terms


class TestIncreasedTopN:
    """
    Test increased top_n threshold from 10 to 20.
    
    Per discussion: More keywords = more cross-reference opportunities.
    """

    @pytest.fixture
    def extractor(self):
        """Fixture providing StatisticalExtractor instance."""
        if StatisticalExtractor is None:
            pytest.skip("StatisticalExtractor not implemented yet (RED phase)")
        return StatisticalExtractor()

    # RED Phase Test 9: Extract 20 keywords
    def test_extract_keywords_top_20(self, extractor):
        """
        Test extraction of up to 20 keywords (increased from 10).
        
        Acceptance Criteria:
        - Returns at most 20 keywords when top_n=20
        - All keywords are valid (pass noise filter)
        """
        # Arrange
        text = """
        Machine learning and deep learning have revolutionized artificial intelligence.
        Foundation models like GPT and BERT use transformer architectures for NLP.
        Neural networks learn representations through backpropagation and gradient descent.
        Large language models are trained on massive datasets using distributed computing.
        Model deployment requires inference optimization, quantization, and serving infrastructure.
        Fine-tuning pretrained models on domain-specific data improves task performance.
        Prompt engineering techniques help extract better outputs from generative AI systems.
        Vector databases enable semantic search and retrieval augmented generation workflows.
        MLOps practices ensure reproducible training pipelines and model versioning.
        Evaluation metrics like perplexity, BLEU scores, and human evaluation assess quality.
        """ * 3  # Repeat for more content
        
        # Act
        keywords = extractor.extract_keywords(text, top_n=20)
        
        # Assert - returns up to 20 (may be fewer after deduplication)
        assert len(keywords) <= 20, f"Should return at most 20 keywords, got {len(keywords)}"
        assert len(keywords) >= 10, f"Should return at least 10 keywords, got {len(keywords)}"
        
        # Validate all are valid tuples
        for kw, score in keywords:
            assert isinstance(kw, str)
            assert isinstance(score, (int, float))
            assert score >= 0

    # RED Phase Test 10: Verify deduplication in extraction
    def test_extract_keywords_with_deduplication(self, extractor):
        """
        Test that single-word extracted keywords are deduplicated by stem.
        
        After deduplication, shouldn't have BOTH single-word 'model' AND 'models'.
        Multi-word phrases like "models are powerful" are valid distinct keywords.
        """
        # Arrange
        text = """
        Machine learning models are powerful. The model learns patterns.
        Modeling is essential for understanding. These models help predictions.
        Architecture patterns guide design. Architectural decisions matter.
        Pattern recognition is key. Patterns emerge from data.
        """
        
        # Act
        keywords = extractor.extract_keywords(text, top_n=20)
        keyword_terms = [kw.lower() for kw, _ in keywords]
        
        # Assert - single-word variants of same root should be deduplicated
        # Filter to only single-word keywords
        single_word_keywords = [kw for kw in keyword_terms if ' ' not in kw]
        
        # Get forms for each root
        model_single_forms = [kw for kw in single_word_keywords if kw.startswith("model")]
        pattern_single_forms = [kw for kw in single_word_keywords if kw.startswith("pattern")]
        
        # After deduplication, should have at most 1 single-word form per root
        assert len(model_single_forms) <= 1, f"Should deduplicate single-word model forms, got: {model_single_forms}"
        assert len(pattern_single_forms) <= 1, f"Should deduplicate single-word pattern forms, got: {pattern_single_forms}"

    # RED Phase Test 11: Verify n-gram cleanup in extraction
    def test_extract_keywords_clean_ngrams(self, extractor):
        """
        Test that extracted keywords have no repeated-word n-grams.
        """
        # Arrange - text that might produce repeated n-grams
        text = """
        Models models are essential. Foundation models models help.
        API API design matters. Machine machine learning advances.
        Deep learning learning improves performance significantly.
        """
        
        # Act
        keywords = extractor.extract_keywords(text, top_n=20)
        
        # Assert - no keyword should have repeated words
        for kw, _ in keywords:
            words = kw.lower().split()
            unique_words = set(words)
            assert len(words) == len(unique_words), f"Keyword has repeated words: {kw}"


class TestIntegration:
    """
    Integration tests for combined deduplication and cleanup.
    """

    @pytest.fixture
    def extractor(self):
        """Fixture providing StatisticalExtractor instance."""
        if StatisticalExtractor is None:
            pytest.skip("StatisticalExtractor not implemented yet (RED phase)")
        return StatisticalExtractor()

    # RED Phase Test 12: Full pipeline with deduplication
    def test_full_extraction_with_dedup_and_cleanup(self, extractor):
        """
        Test complete extraction pipeline with all enhancements.
        
        Validates:
        - top_n=20 works
        - Stemming deduplication applied
        - N-gram cleanup applied
        - Valid keywords only
        """
        # Arrange
        text = """
        Microservices architecture enables independent service deployment.
        API gateways handle authentication, rate limiting, and request routing.
        Container orchestration with Kubernetes manages distributed systems.
        Service mesh provides observability and traffic management.
        Domain-driven design separates business logic from infrastructure.
        Repository pattern abstracts data persistence mechanisms.
        Event sourcing captures all changes as immutable events.
        CQRS separates read and write models for scalability.
        """ * 3
        
        # Act
        keywords = extractor.extract_keywords(text, top_n=20)
        concepts = extractor.extract_concepts(text, top_n=15)
        
        # Assert - basic counts
        assert len(keywords) <= 20, "Should return at most 20 keywords"
        assert len(concepts) <= 15, "Should return at most 15 concepts"
        
        # Assert - no repeated-word n-grams in keywords
        for kw, _ in keywords:
            words = kw.lower().split()
            assert len(words) == len(set(words)), f"Repeated words in: {kw}"
        
        # Assert - concepts should be unique stems
        concept_stems = []
        for c in concepts:
            stem = c.lower().rstrip('s').rstrip('ing').rstrip('ed')
            assert stem not in concept_stems, f"Duplicate stem in concepts: {c}"
            concept_stems.append(stem)


# TDD Status Marker
def test_tdd_deduplication_status():
    """
    Meta-test to track deduplication TDD implementation phase.
    
    RED phase: This test FAILS (functions not implemented)
    GREEN phase: This test PASSES (functions added)
    """
    assert IMPORTS_AVAILABLE, "Deduplication functions should be importable"
    assert _deduplicate_by_stem is not None, "_deduplicate_by_stem should exist"
    assert _clean_ngram_duplicates is not None, "_clean_ngram_duplicates should exist"
