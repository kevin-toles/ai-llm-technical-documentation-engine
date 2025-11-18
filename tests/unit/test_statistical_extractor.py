"""
Test suite for StatisticalExtractor - Domain-agnostic metadata extraction.

Following TDD RED → GREEN → REFACTOR cycle per ARCHITECTURE_GUIDELINES Ch. 1.
Tests written FIRST to define expected behavior across 4 domains.

Document References:
- DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md: Part 1.2 (Statistical extraction)
- ARCHITECTURE_GUIDELINES Ch. 4: Adapter pattern for external dependencies
- PYTHON_GUIDELINES Ch. 13: Parametrized testing, fixtures, assertions
- BOOK_TAXONOMY_MATRIX: Architecture Patterns (Tier 1), Python Distilled (Tier 3)

Test Coverage:
1. Keyword extraction (YAKE) - works across Python, biology, law, construction
2. Concept extraction (Summa) - domain-agnostic keyword identification
3. Summarization (Summa TextRank) - extractive summarization
4. Error handling - empty text, invalid parameters
5. Performance - reasonable extraction time (<1 second per chapter)

TDD Status: RED phase - Expected to FAIL until StatisticalExtractor implemented
"""

import pytest
from pathlib import Path
from typing import List, Tuple

# Import will fail initially (RED phase) - this is expected
try:
    from workflows.metadata_extraction.scripts.adapters.statistical_extractor import (
        StatisticalExtractor
    )
except ImportError:
    StatisticalExtractor = None  # Will cause tests to fail as expected


# Test data for 4 domains (per DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN Section 5.1)
DOMAIN_TEXTS = {
    "python": """
        Python is a high-level programming language that emphasizes code readability and simplicity.
        Object-oriented programming allows developers to create reusable code through classes and objects.
        Functions are first-class citizens in Python, supporting functional programming paradigms.
        Decorators provide a way to modify function behavior without changing the function itself.
        List comprehensions offer a concise syntax for creating lists based on existing sequences.
        The Python standard library includes modules for file I/O, networking, and data structures.
        Type hints improve code documentation and enable static type checking with tools like mypy.
        Context managers using 'with' statements ensure proper resource cleanup.
        Generators provide memory-efficient iteration over large datasets.
        The Global Interpreter Lock (GIL) affects multi-threading performance in CPython.
    """,
    "biology": """
        Photosynthesis is the process by which plants convert light energy into chemical energy.
        Cellular respiration breaks down glucose to produce ATP, the cell's energy currency.
        DNA replication ensures genetic information is accurately copied during cell division.
        Mitosis produces two identical daughter cells from a single parent cell.
        Meiosis generates four genetically diverse gametes for sexual reproduction.
        The endoplasmic reticulum synthesizes proteins and lipids within the cell.
        Ribosomes are the cellular machinery responsible for protein synthesis.
        The Krebs cycle is a central metabolic pathway in aerobic respiration.
        Homeostasis maintains stable internal conditions despite external environmental changes.
        Enzymes are biological catalysts that speed up chemical reactions in living organisms.
    """,
    "law": """
        Contract law governs legally binding agreements between parties with mutual obligations.
        Tort law addresses civil wrongs that cause harm or loss to individuals.
        The burden of proof in criminal cases requires evidence beyond a reasonable doubt.
        Stare decisis is the legal principle of following precedent in judicial decisions.
        Habeas corpus protects individuals from unlawful detention without due process.
        The Miranda warning informs suspects of their constitutional rights during arrest.
        Intellectual property law protects creations of the mind including patents and copyrights.
        Class action lawsuits allow groups of plaintiffs to collectively sue defendants.
        Mediation and arbitration provide alternative dispute resolution mechanisms.
        The statute of limitations sets time limits for filing legal claims.
    """,
    "construction": """
        Structural engineering analyzes forces and stresses in building frameworks and supports.
        Concrete curing requires proper moisture and temperature control for optimal strength.
        Steel reinforcement bars (rebar) provide tensile strength in concrete structures.
        Load-bearing walls transfer building weight to the foundation system.
        HVAC systems regulate heating, ventilation, and air conditioning in buildings.
        Building codes establish minimum safety and construction standards.
        Foundation types include slab-on-grade, crawl space, and basement configurations.
        Framing techniques using wood or steel create the building's skeletal structure.
        Drywall installation involves hanging, taping, and finishing gypsum panels.
        Electrical wiring must comply with National Electrical Code requirements.
    """
}


# Expected keywords for validation (per domain)
EXPECTED_KEYWORDS = {
    "python": ["python", "programming", "code", "function", "class", "object"],
    "biology": ["cell", "photosynthesis", "dna", "protein", "synthesis", "energy"],
    "law": ["law", "legal", "court", "rights", "tort", "contract"],
    "construction": ["building", "construction", "structural", "concrete", "foundation"]
}


class TestStatisticalExtractor:
    """
    Test suite for domain-agnostic statistical metadata extraction.
    
    Per ARCHITECTURE_GUIDELINES Ch. 1: Write tests FIRST (RED phase).
    Per PYTHON_GUIDELINES Ch. 13: Use parametrize for multiple test cases.
    """

    @pytest.fixture
    def extractor(self):
        """
        Fixture providing StatisticalExtractor instance.
        
        Per PYTHON_GUIDELINES Ch. 13: Use fixtures for test dependencies.
        Per ARCHITECTURE_GUIDELINES Ch. 4: Adapter pattern for external libraries.
        """
        if StatisticalExtractor is None:
            pytest.skip("StatisticalExtractor not implemented yet (RED phase)")
        return StatisticalExtractor()

    # RED Phase Test 1: Keyword Extraction (YAKE)
    @pytest.mark.parametrize("domain", ["python", "biology", "law", "construction"])
    def test_extract_keywords_domain_agnostic(self, extractor, domain: str):
        """
        Test keyword extraction works across all 4 domains using YAKE.
        
        Acceptance Criteria (DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN Part 1.2):
        - Extracts meaningful keywords from any domain
        - Returns List[Tuple[str, float]] with (keyword, score)
        - Scores are sorted descending (lower YAKE score = more important)
        - Top 10 keywords should include domain-specific terms
        
        Document References:
        - DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN: Section 5.1 (4-domain testing)
        - PYTHON_GUIDELINES Ch. 13: Parametrized test pattern
        """
        # Arrange
        text = DOMAIN_TEXTS[domain]
        expected_keywords = EXPECTED_KEYWORDS[domain]
        
        # Act
        keywords = extractor.extract_keywords(text, top_n=10)
        
        # Assert - Per PYTHON_GUIDELINES Ch. 13: Clear assertions
        assert isinstance(keywords, list), "Should return list of tuples"
        assert len(keywords) == 10, "Should return exactly 10 keywords"
        
        # Validate tuple structure: (keyword: str, score: float)
        for kw, score in keywords:
            assert isinstance(kw, str), f"Keyword should be string, got {type(kw)}"
            assert isinstance(score, (int, float)), f"Score should be numeric, got {type(score)}"
            assert score >= 0, f"YAKE score should be non-negative, got {score}"
        
        # Validate keywords are sorted by score (ascending - YAKE lower is better)
        scores = [score for _, score in keywords]
        assert scores == sorted(scores), "Keywords should be sorted by score (ascending)"
        
        # Validate at least 2 expected domain keywords present
        extracted_kw_text = " ".join([kw.lower() for kw, _ in keywords])
        matches = [ek for ek in expected_keywords if ek in extracted_kw_text]
        assert len(matches) >= 2, (
            f"Should extract at least 2 domain-specific keywords for {domain}. "
            f"Expected any of {expected_keywords}, got keywords: {[kw for kw, _ in keywords]}"
        )

    # RED Phase Test 2: Concept Extraction (Summa)
    @pytest.mark.parametrize("domain", ["python", "biology", "law", "construction"])
    def test_extract_concepts_domain_agnostic(self, extractor, domain: str):
        """
        Test concept extraction using Summa TextRank keywords.
        
        Acceptance Criteria:
        - Extracts single-word concepts from any domain
        - Returns List[str] of concept terms
        - Concepts are relevant to domain content
        
        Document References:
        - DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN: Part 1.2 (Summa integration)
        - PYTHON_GUIDELINES Ch. 13: Test assertions and validation
        """
        # Arrange
        text = DOMAIN_TEXTS[domain]
        expected_keywords = EXPECTED_KEYWORDS[domain]
        
        # Act
        concepts = extractor.extract_concepts(text, top_n=5)
        
        # Assert
        assert isinstance(concepts, list), "Should return list of strings"
        assert len(concepts) == 5, "Should return exactly 5 concepts"
        
        # Validate all concepts are strings
        for concept in concepts:
            assert isinstance(concept, str), f"Concept should be string, got {type(concept)}"
            assert len(concept) > 0, "Concept should not be empty string"
        
        # Validate at least 1 expected domain keyword present
        concepts_text = " ".join([c.lower() for c in concepts])
        matches = [ek for ek in expected_keywords if ek in concepts_text]
        assert len(matches) >= 1, (
            f"Should extract at least 1 domain-specific concept for {domain}. "
            f"Expected any of {expected_keywords}, got concepts: {concepts}"
        )

    # RED Phase Test 3: Summarization (Summa TextRank)
    @pytest.mark.parametrize("domain", ["python", "biology", "law", "construction"])
    def test_generate_summary_domain_agnostic(self, extractor, domain: str):
        """
        Test extractive summarization using Summa TextRank.
        
        Acceptance Criteria:
        - Generates summary from any domain text
        - Summary is shorter than original text
        - Summary contains complete sentences
        - Summary preserves domain-specific terminology
        
        Document References:
        - DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN: Part 1.2 (Summa summarization)
        - PYTHON_GUIDELINES Ch. 13: String validation patterns
        """
        # Arrange
        text = DOMAIN_TEXTS[domain]
        ratio = 0.3  # 30% of original text
        
        # Act
        summary = extractor.generate_summary(text, ratio=ratio)
        
        # Assert
        assert isinstance(summary, str), "Summary should be string"
        assert len(summary) > 0, "Summary should not be empty"
        assert len(summary) < len(text), "Summary should be shorter than original"
        
        # Validate summary contains complete sentences (ends with period)
        assert summary.strip().endswith('.'), "Summary should end with period"
        
        # Validate summary contains at least 1 domain-specific term
        expected_keywords = EXPECTED_KEYWORDS[domain]
        summary_lower = summary.lower()
        matches = [ek for ek in expected_keywords if ek in summary_lower]
        assert len(matches) >= 1, (
            f"Summary should contain domain-specific terms for {domain}. "
            f"Expected any of {expected_keywords}, got summary: {summary[:100]}..."
        )

    # RED Phase Test 4: Error Handling - Empty Text
    def test_extract_keywords_empty_text(self, extractor):
        """
        Test graceful handling of empty input text.
        
        Per PYTHON_GUIDELINES Ch. 8: EAFP error handling.
        Per ARCHITECTURE_GUIDELINES Ch. 4: Adapter validates input.
        """
        # Act & Assert
        with pytest.raises(ValueError, match="(?i)empty|text"):
            extractor.extract_keywords("", top_n=10)

    # RED Phase Test 5: Error Handling - Invalid Parameters
    def test_extract_keywords_invalid_top_n(self, extractor):
        """
        Test validation of top_n parameter.
        
        Per PYTHON_GUIDELINES Ch. 8: Validate inputs early.
        """
        text = "Sample text for testing parameter validation."
        
        # Act & Assert - negative top_n
        with pytest.raises(ValueError, match="(?i)top_n|positive"):
            extractor.extract_keywords(text, top_n=-1)
        
        # Act & Assert - zero top_n
        with pytest.raises(ValueError, match="(?i)top_n|positive"):
            extractor.extract_keywords(text, top_n=0)

    # RED Phase Test 6: Performance - Extraction Speed
    @pytest.mark.parametrize("domain", ["python", "biology", "law", "construction"])
    def test_extraction_performance(self, extractor, domain: str):
        """
        Test extraction completes in reasonable time (<1 second).
        
        Acceptance Criteria (DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN Section 6):
        - Processing time <1 second per chapter
        - Enables real-time metadata extraction
        
        Per PYTHON_GUIDELINES Ch. 13: Performance testing with benchmarks.
        """
        import time
        
        # Arrange
        text = DOMAIN_TEXTS[domain]
        
        # Act
        start = time.time()
        keywords = extractor.extract_keywords(text, top_n=20)
        concepts = extractor.extract_concepts(text, top_n=10)
        summary = extractor.generate_summary(text, ratio=0.2)
        elapsed = time.time() - start
        
        # Assert - Per DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN: <1 second
        assert elapsed < 1.0, (
            f"Extraction should complete in <1 second for {domain}. "
            f"Took {elapsed:.3f} seconds"
        )
        
        # Validate all operations succeeded
        assert len(keywords) == 20
        assert len(concepts) == 10
        assert len(summary) > 0

    # RED Phase Test 7: Integration - Combined Extraction
    def test_combined_extraction_all_domains(self, extractor):
        """
        Test extracting keywords, concepts, and summary together.
        
        Validates adapter can handle multiple operations on same text.
        Per ARCHITECTURE_GUIDELINES Ch. 4: Adapter provides unified interface.
        """
        for domain, text in DOMAIN_TEXTS.items():
            # Act
            keywords = extractor.extract_keywords(text, top_n=10)
            concepts = extractor.extract_concepts(text, top_n=5)
            summary = extractor.generate_summary(text, ratio=0.3)
            
            # Assert all operations succeeded
            assert len(keywords) == 10, f"Failed for domain: {domain}"
            assert len(concepts) == 5, f"Failed for domain: {domain}"
            assert len(summary) > 0, f"Failed for domain: {domain}"
            
            # Validate coherence - extract individual words from multi-word keywords
            # YAKE returns phrases like "object-oriented programming"
            # Summa returns single words like "programming"
            keyword_words = set()
            for kw, _ in keywords:
                # Split multi-word keywords and add individual words
                keyword_words.update(word.lower() for word in kw.split())
            
            concept_terms = set([c.lower() for c in concepts])
            overlap = keyword_words.intersection(concept_terms)
            
            # At least 1 word should appear in both (validates consistency)
            assert len(overlap) >= 1, (
                f"Keywords and concepts should overlap for {domain}. "
                f"Keyword words: {keyword_words}, Concepts: {concept_terms}"
            )


# TDD Status Marker
def test_tdd_status():
    """
    Meta-test to track TDD implementation phase.
    
    RED phase: This test FAILS (StatisticalExtractor not implemented)
    GREEN phase: This test PASSES (minimal implementation added)
    REFACTOR phase: This test PASSES (code cleaned and optimized)
    """
    if StatisticalExtractor is None:
        pytest.fail(
            "RED PHASE: StatisticalExtractor not implemented yet. "
            "Next: Create workflows/metadata_extraction/scripts/adapters/statistical_extractor.py"
        )
    else:
        # GREEN/REFACTOR phase - extractor exists
        assert StatisticalExtractor is not None, "StatisticalExtractor should be implemented"
        
        # Validate class has required methods
        extractor = StatisticalExtractor()
        assert hasattr(extractor, 'extract_keywords'), "Missing extract_keywords method"
        assert hasattr(extractor, 'extract_concepts'), "Missing extract_concepts method"
        assert hasattr(extractor, 'generate_summary'), "Missing generate_summary method"
