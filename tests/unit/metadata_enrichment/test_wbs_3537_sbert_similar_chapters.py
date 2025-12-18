#!/usr/bin/env python3
"""
TDD Tests for WBS 3.5.3.7 - SBERT-based Similar Chapters Computation - DEPRECATED

=============================================================================
DEPRECATED: Tests for local SBERT/TF-IDF mode removed per Kitchen Brigade pattern
=============================================================================

These tests were for the LOCAL ML functionality that has been REMOVED:
- Local SBERT integration in compute_similar_chapters.py
- Local TF-IDF fallback mode
- SemanticSimilarityEngine local modes

Per the Kitchen Brigade Architecture (MULTI_STAGE_ENRICHMENT_PIPELINE_ARCHITECTURE.md):
- llm-document-enhancer is a CUSTOMER only (no local ML)
- All ML processing is now delegated to ai-agents MSEP service

For MSEP-related tests, see:
- tests/e2e/test_msep_customer.py
- tests/integration/test_msep_fallbacks.py
- tests/unit/metadata_enrichment/test_msep_client.py

These tests are kept for historical reference only.
All tests are SKIPPED via module-level pytest.skip().

Original documentation:
WBS Reference: AI_CODING_PLATFORM_WBS.md Phase 3.5.3.7
Architecture: TIER_RELATIONSHIP_DIAGRAM.md Step 4 (semantic similarity)
TDD Phase: RED - Tests for SemanticSimilarityEngine integration
"""

import pytest

# Skip entire module - local SBERT/TF-IDF mode has been removed per Kitchen Brigade pattern
pytest.skip(
    "DEPRECATED: Local SBERT integration removed per Kitchen Brigade architecture. "
    "See MULTI_STAGE_ENRICHMENT_PIPELINE_ARCHITECTURE.md. "
    "Use --use-msep flag for enrichment, or see tests/e2e/test_msep_customer.py.",
    allow_module_level=True
)


# =============================================================================
# HISTORICAL REFERENCE: Original test code below (not executed due to skip)
# =============================================================================
# The remaining code is preserved for historical reference only.
# All tests are skipped at module level.
