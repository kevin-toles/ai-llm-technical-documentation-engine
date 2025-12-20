"""Extraction Settings - WBS-2.1.

Pydantic Settings for metadata extraction configuration.

AC Reference:
- AC-1.3: Default behavior uses StatisticalExtractor (use_orchestrator_extraction=False)
- AC-1.4: EXTRACTION_* env vars override defaults

Anti-Patterns Avoided:
- S1192: Constants extracted to module level
- Anti-Pattern #12: Singleton pattern for settings
"""

from __future__ import annotations

from typing import Final

from pydantic_settings import BaseSettings, SettingsConfigDict


# =============================================================================
# Module Constants (S1192 compliance)
# =============================================================================

DEFAULT_ORCHESTRATOR_URL: Final[str] = "http://localhost:8083"
DEFAULT_ORCHESTRATOR_TIMEOUT: Final[float] = 30.0
DEFAULT_ORCHESTRATOR_MAX_RETRIES: Final[int] = 3
DEFAULT_MIN_KEYWORD_CONFIDENCE: Final[float] = 0.3
DEFAULT_MIN_CONCEPT_CONFIDENCE: Final[float] = 0.3
DEFAULT_TOP_K_KEYWORDS: Final[int] = 15
DEFAULT_TOP_K_CONCEPTS: Final[int] = 10


# =============================================================================
# ExtractionSettings Pydantic Model
# =============================================================================


class ExtractionSettings(BaseSettings):
    """Settings for metadata extraction.

    Environment variables with EXTRACTION_ prefix override defaults.

    Attributes:
        use_orchestrator_extraction: Use orchestrator (True) or local (False).
        orchestrator_url: URL of Code-Orchestrator-Service.
        orchestrator_timeout: Request timeout in seconds.
        orchestrator_max_retries: Max retries for failed requests.
        fallback_on_error: Fallback to local if orchestrator fails.
        min_keyword_confidence: Min confidence for keywords.
        min_concept_confidence: Min confidence for concepts.
        top_k_keywords: Number of keywords to extract.
        top_k_concepts: Number of concepts to extract.

    AC Reference:
        - AC-1.3: Default use_orchestrator_extraction=False
        - AC-1.4: EXTRACTION_* env vars override defaults
    """

    # Extraction mode (AC-1.3: default False)
    use_orchestrator_extraction: bool = False

    # Orchestrator connection
    orchestrator_url: str = DEFAULT_ORCHESTRATOR_URL
    orchestrator_timeout: float = DEFAULT_ORCHESTRATOR_TIMEOUT
    orchestrator_max_retries: int = DEFAULT_ORCHESTRATOR_MAX_RETRIES

    # Fallback behavior
    fallback_on_error: bool = True

    # Quality thresholds
    min_keyword_confidence: float = DEFAULT_MIN_KEYWORD_CONFIDENCE
    min_concept_confidence: float = DEFAULT_MIN_CONCEPT_CONFIDENCE
    top_k_keywords: int = DEFAULT_TOP_K_KEYWORDS
    top_k_concepts: int = DEFAULT_TOP_K_CONCEPTS

    model_config = SettingsConfigDict(
        env_prefix="EXTRACTION_",
        env_file=".env",
        extra="ignore",
    )


# =============================================================================
# Singleton Instance (Anti-Pattern #12)
# =============================================================================

_extraction_settings: ExtractionSettings | None = None


def get_extraction_settings() -> ExtractionSettings:
    """Get or create cached ExtractionSettings instance.

    Implements singleton pattern per Anti-Pattern #12:
    settings should be cached, not created per request.

    Returns:
        Cached ExtractionSettings instance.
    """
    global _extraction_settings
    if _extraction_settings is None:
        _extraction_settings = ExtractionSettings()
    return _extraction_settings
