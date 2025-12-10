"""
Unit tests for LLMCacheRepository (LLM Response Cache).

Tests cover Repository Pattern implementation for caching expensive Claude API responses.

Pattern References:
- Architecture Patterns with Python Ch. 2 (Repository Pattern)
- Python Architecture Patterns Ch. 3, pg. 99 (Cache systems)
- Learning Python Ed6 Ch. 28-31 (Dataclass patterns)

Design Principles:
1. Repository Pattern: Abstract storage behind interface
2. Cache-Aside Pattern: Check cache first, call LLM on miss
3. TTL Management: 30-day expiration (expensive to regenerate - $0.60/chapter)
4. Prompt Hash Keys: Cache based on exact prompt sent to LLM
5. Cost Tracking: Save $0.30 per phase per cache hit

Cost Analysis:
- Phase 1 LLM call: $0.30 (content selection)
- Phase 2 LLM call: $0.30 (citation extraction)
- Total per chapter: $0.60
- Cache hit saves: 100% API cost ($0.30 per phase)
- 30-day TTL balances storage vs API cost

TDD Phase: RED (failing tests)
"""

import hashlib
import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Optional, Any

import pytest


# ============================================================
# DATACLASS DEFINITIONS (from DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md)
# ============================================================

@dataclass
class LLMResponse:
    """DTO for LLM API responses (phase1 or phase2)."""
    phase: str                     # "phase1" or "phase2"
    chapter_num: int
    prompt_hash: str               # Hash of prompt sent to LLM
    response_text: str             # Raw LLM response
    parsed_data: Dict[str, Any]    # Parsed/structured data
    model: str                     # e.g., "claude-sonnet-4"
    tokens_used: int               # For cost tracking


@dataclass
class CacheEntry:
    """Value Object for cache metadata (Repository Pattern)."""
    key: str
    created_at: float              # Unix timestamp
    ttl_seconds: int               # Time to live
    content_hash: str              # For cache invalidation (reused as prompt_hash here)
    
    def is_expired(self) -> bool:
        """Check if cache entry has expired based on TTL."""
        return time.time() > (self.created_at + self.ttl_seconds)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dict for JSON storage."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CacheEntry':
        """Deserialize from dict."""
        return cls(**data)


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def cache_dir(tmp_path: Path) -> Path:
    """Temporary cache directory for testing."""
    cache_path = tmp_path / "test_llm_cache"
    cache_path.mkdir(parents=True, exist_ok=True)
    return cache_path


@pytest.fixture
def sample_phase1_response() -> LLMResponse:
    """Sample phase1 LLM response (content selection)."""
    return LLMResponse(
        phase="phase1",
        chapter_num=3,
        prompt_hash="abc12345",
        response_text='{"selected_guidelines": [1, 5, 12], "relevance": {...}}',
        parsed_data={
            "selected_guidelines": [1, 5, 12],
            "relevance": {
                "1": {"score": 0.95, "reason": "Repository pattern discussion"},
                "5": {"score": 0.89, "reason": "ORM abstraction"},
                "12": {"score": 0.82, "reason": "Database persistence"}
            }
        },
        model="claude-sonnet-4",
        tokens_used=1200
    )


@pytest.fixture
def sample_phase2_response() -> LLMResponse:
    """Sample phase2 LLM response (citation extraction)."""
    return LLMResponse(
        phase="phase2",
        chapter_num=3,
        prompt_hash="def67890",
        response_text='{"citations": [...], "page_numbers": [...]}',
        parsed_data={
            "citations": [
                {"guideline_id": 1, "text": "Use Repository Pattern for data access"},
                {"guideline_id": 5, "text": "Abstract ORM details"}
            ],
            "page_numbers": [45, 67]
        },
        model="claude-sonnet-4",
        tokens_used=800
    )


@pytest.fixture
def prompt_hash_v1() -> str:
    """Prompt hash version 1."""
    return "abc12345"


@pytest.fixture
def prompt_hash_v2() -> str:
    """Prompt hash version 2 (different prompt)."""
    return "xyz98765"


# ============================================================
# TEST 1: Phase 1 cache hit returns cached response
# ============================================================

def test_phase1_cache_hit_returns_cached_response(
    cache_dir: Path,
    sample_phase1_response: LLMResponse
):
    """
    Test Repository Pattern cache hit for phase1 (content selection).
    
    Given:
      - Cache directory with stored phase1 response
      - Valid prompt hash matching cached entry
      - Non-expired cache entry (within 30-day TTL)
    
    When:
      - get_phase1() is called with chapter_num and prompt_hash
    
    Then:
      - Returns cached LLMResponse
      - Data matches original stored response
      - Saves $0.30 API cost (phase1 LLM call avoided)
    
    Pattern: Repository Pattern + Cache-Aside Pattern
    Cost Savings: $0.30 per cache hit
    """
    from workflows.llm_enhancement.scripts.cache.llm_cache import LLMCacheRepository
    
    # Arrange: Create cache with stored phase1 response
    cache_repo = LLMCacheRepository(cache_dir=cache_dir, ttl_days=30)
    cache_repo.set_phase1(sample_phase1_response)
    
    # Act: Retrieve cached phase1 response
    result = cache_repo.get_phase1(
        chapter_num=sample_phase1_response.chapter_num,
        prompt_hash=sample_phase1_response.prompt_hash
    )
    
    # Assert: Cache hit returns exact data
    assert result is not None, "Phase1 cache hit should return data, not None"
    assert result.phase == "phase1"
    assert result.chapter_num == sample_phase1_response.chapter_num
    assert result.prompt_hash == sample_phase1_response.prompt_hash
    assert result.response_text == sample_phase1_response.response_text
    assert result.parsed_data == sample_phase1_response.parsed_data
    assert result.model == sample_phase1_response.model
    assert result.tokens_used == sample_phase1_response.tokens_used


# ============================================================
# TEST 2: Phase 2 cache hit returns cached response
# ============================================================

def test_phase2_cache_hit_returns_cached_response(
    cache_dir: Path,
    sample_phase2_response: LLMResponse
):
    """
    Test Repository Pattern cache hit for phase2 (citation extraction).
    
    Given:
      - Cache directory with stored phase2 response
      - Valid prompt hash matching cached entry
      - Non-expired cache entry (within 30-day TTL)
    
    When:
      - get_phase2() is called with chapter_num and prompt_hash
    
    Then:
      - Returns cached LLMResponse
      - Data matches original stored response
      - Saves $0.30 API cost (phase2 LLM call avoided)
    
    Pattern: Repository Pattern + Cache-Aside Pattern
    Cost Savings: $0.30 per cache hit
    """
    from workflows.llm_enhancement.scripts.cache.llm_cache import LLMCacheRepository
    
    # Arrange: Create cache with stored phase2 response
    cache_repo = LLMCacheRepository(cache_dir=cache_dir, ttl_days=30)
    cache_repo.set_phase2(sample_phase2_response)
    
    # Act: Retrieve cached phase2 response
    result = cache_repo.get_phase2(
        chapter_num=sample_phase2_response.chapter_num,
        prompt_hash=sample_phase2_response.prompt_hash
    )
    
    # Assert: Cache hit returns exact data
    assert result is not None, "Phase2 cache hit should return data, not None"
    assert result.phase == "phase2"
    assert result.chapter_num == sample_phase2_response.chapter_num
    assert result.prompt_hash == sample_phase2_response.prompt_hash
    assert result.response_text == sample_phase2_response.response_text
    assert result.parsed_data == sample_phase2_response.parsed_data
    assert result.model == sample_phase2_response.model
    assert result.tokens_used == sample_phase2_response.tokens_used


# ============================================================
# TEST 3: Expired LLM cache entry deleted (30-day TTL)
# ============================================================

def test_expired_llm_cache_entry_deleted(
    cache_dir: Path,
    sample_phase1_response: LLMResponse
):
    """
    Test TTL management (30-day expiration for expensive LLM responses).
    
    Given:
      - Cache entry created 31 days ago (expired)
      - TTL set to 30 days
    
    When:
      - get_phase1() is called on expired entry
    
    Then:
      - Returns None (entry expired)
      - Cache file deleted from disk (cleanup)
      - Workflow should call LLM API to regenerate ($0.30 cost)
    
    Pattern: TTL-based cache invalidation
    Cost Impact: $0.30 to regenerate after expiration
    """
    from workflows.llm_enhancement.scripts.cache.llm_cache import LLMCacheRepository
    
    # Arrange: Create cache entry with fake old timestamp
    cache_repo = LLMCacheRepository(cache_dir=cache_dir, ttl_days=30)
    cache_repo.set_phase1(sample_phase1_response)
    
    # Manually edit cache file to set old timestamp (31 days ago)
    cache_key = cache_repo._get_cache_key(sample_phase1_response.chapter_num, sample_phase1_response.prompt_hash)
    cache_file = cache_repo._get_cache_path("phase1", cache_key)
    
    with open(cache_file, 'r') as f:
        cache_data = json.load(f)
    
    thirty_one_days_ago = time.time() - (31 * 24 * 60 * 60)
    cache_data['metadata']['created_at'] = thirty_one_days_ago
    
    with open(cache_file, 'w') as f:
        json.dump(cache_data, f)
    
    # Act: Try to retrieve expired data
    result = cache_repo.get_phase1(sample_phase1_response.chapter_num, sample_phase1_response.prompt_hash)
    
    # Assert: Expired entry returns None and is deleted
    assert result is None, "Expired LLM cache entry should return None"
    assert not cache_file.exists(), "Expired LLM cache file should be deleted"


# ============================================================
# TEST 4: Prompt hash changes invalidate cache
# ============================================================

def test_prompt_hash_changes_invalidate_cache(
    cache_dir: Path,
    sample_phase1_response: LLMResponse,
    prompt_hash_v1: str,
    prompt_hash_v2: str
):
    """
    Test cache invalidation when prompt changes.
    
    Given:
      - Cached phase1 response with prompt_hash_v1
      - Prompt modified (new prompt_hash_v2)
    
    When:
      - get_phase1() is called with new prompt_hash_v2
    
    Then:
      - Returns None (cache invalidated)
      - Old cache file remains (different key)
      - Workflow should call LLM API with new prompt ($0.30 cost)
    
    Pattern: Prompt hash invalidation (detect prompt changes)
    Use Case: Prompt engineering iteration, guideline updates
    """
    from workflows.llm_enhancement.scripts.cache.llm_cache import LLMCacheRepository
    
    # Arrange: Cache entry with old prompt hash
    cache_repo = LLMCacheRepository(cache_dir=cache_dir, ttl_days=30)
    
    response_v1 = LLMResponse(
        phase="phase1",
        chapter_num=3,
        prompt_hash=prompt_hash_v1,
        response_text='{"selected": [1, 2, 3]}',
        parsed_data={"selected": [1, 2, 3]},
        model="claude-sonnet-4",
        tokens_used=1000
    )
    cache_repo.set_phase1(response_v1)
    
    # Act: Try to retrieve with different prompt hash
    result = cache_repo.get_phase1(chapter_num=3, prompt_hash=prompt_hash_v2)
    
    # Assert: Prompt hash mismatch returns None (cache miss)
    assert result is None, "Prompt hash mismatch should return None (cache invalidated)"
    
    # Old cache entry still exists (different key)
    old_result = cache_repo.get_phase1(chapter_num=3, prompt_hash=prompt_hash_v1)
    assert old_result is not None, "Old cache entry should still exist"


# ============================================================
# TEST 5: Cost tracking saves $0.30 per cache hit
# ============================================================

def test_cost_tracking_saves_money(
    cache_dir: Path,
    sample_phase1_response: LLMResponse,
    sample_phase2_response: LLMResponse
):
    """
    Test cost tracking for cache ROI analysis.
    
    Given:
      - Phase1 cache hit (saves $0.30)
      - Phase2 cache hit (saves $0.30)
      - Both responses cached with tokens_used field
    
    When:
      - Multiple cache hits occur
    
    Then:
      - tokens_used field preserved in cached response
      - Total savings = $0.60 per chapter (both phases cached)
      - Cache ROI: Storage cost << API cost
    
    Pattern: Cost tracking for cache effectiveness
    Analysis: 30-day TTL justified by $0.60 regeneration cost
    """
    from workflows.llm_enhancement.scripts.cache.llm_cache import LLMCacheRepository
    
    # Arrange: Cache both phase1 and phase2 responses
    cache_repo = LLMCacheRepository(cache_dir=cache_dir, ttl_days=30)
    cache_repo.set_phase1(sample_phase1_response)
    cache_repo.set_phase2(sample_phase2_response)
    
    # Act: Retrieve cached responses (simulate cache hits)
    phase1_result = cache_repo.get_phase1(
        sample_phase1_response.chapter_num,
        sample_phase1_response.prompt_hash
    )
    phase2_result = cache_repo.get_phase2(
        sample_phase2_response.chapter_num,
        sample_phase2_response.prompt_hash
    )
    
    # Assert: Cost tracking data preserved
    assert phase1_result is not None, "Phase1 cache hit should return data"
    assert phase1_result.tokens_used == 1200, "Phase1 tokens_used should be preserved"
    
    assert phase2_result is not None, "Phase2 cache hit should return data"
    assert phase2_result.tokens_used == 800, "Phase2 tokens_used should be preserved"
    
    # Calculate total tokens saved (for ROI analysis)
    total_tokens_saved = phase1_result.tokens_used + phase2_result.tokens_used
    assert total_tokens_saved == 2000, f"Expected 2000 tokens saved, got {total_tokens_saved}"
    
    # Cost savings: $0.30 per phase = $0.60 total per chapter


# ============================================================
# TEST 6: Separate phase1/phase2 directories
# ============================================================

def test_separate_phase_directories(
    cache_dir: Path,
    sample_phase1_response: LLMResponse,
    sample_phase2_response: LLMResponse
):
    """
    Test phase separation in directory structure.
    
    Given:
      - Phase1 response for chapter 3
      - Phase2 response for chapter 3
    
    When:
      - set_phase1() and set_phase2() are called
    
    Then:
      - Phase1 file stored in cache/llm_responses/phase1/
      - Phase2 file stored in cache/llm_responses/phase2/
      - Same chapter can have separate phase1/phase2 entries
      - Avoids key collisions between phases
    
    Pattern: Directory-based phase separation
    Benefit: Clear organization, independent phase caching
    """
    from workflows.llm_enhancement.scripts.cache.llm_cache import LLMCacheRepository
    
    # Arrange & Act: Store phase1 and phase2 responses
    cache_repo = LLMCacheRepository(cache_dir=cache_dir, ttl_days=30)
    cache_repo.set_phase1(sample_phase1_response)
    cache_repo.set_phase2(sample_phase2_response)
    
    # Assert: Phase1 file in phase1/ directory
    phase1_key = cache_repo._get_cache_key(sample_phase1_response.chapter_num, sample_phase1_response.prompt_hash)
    phase1_file = cache_repo._get_cache_path("phase1", phase1_key)
    assert phase1_file.exists(), "Phase1 cache file should exist in phase1/ directory"
    assert "phase1" in str(phase1_file), f"Phase1 file path should contain 'phase1': {phase1_file}"
    
    # Assert: Phase2 file in phase2/ directory
    phase2_key = cache_repo._get_cache_key(sample_phase2_response.chapter_num, sample_phase2_response.prompt_hash)
    phase2_file = cache_repo._get_cache_path("phase2", phase2_key)
    assert phase2_file.exists(), "Phase2 cache file should exist in phase2/ directory"
    assert "phase2" in str(phase2_file), f"Phase2 file path should contain 'phase2': {phase2_file}"
    
    # Assert: Different directories for same chapter
    assert phase1_file.parent != phase2_file.parent, "Phase1 and phase2 should use different directories"


# ============================================================
# TEST 7: Convenience methods (get_phase1, set_phase2)
# ============================================================

def test_convenience_methods(
    cache_dir: Path,
    sample_phase1_response: LLMResponse,
    sample_phase2_response: LLMResponse
):
    """
    Test convenience methods vs generic get/set.
    
    Given:
      - LLMCacheRepository with convenience methods
    
    When:
      - get_phase1() is used instead of get("phase1", ...)
      - set_phase2() is used instead of set(LLMResponse(phase="phase2", ...))
    
    Then:
      - Convenience methods work identically to generic methods
      - Cleaner API: get_phase1(ch, hash) vs get("phase1", ch, hash)
      - Type safety: set_phase1() validates phase="phase1"
    
    Pattern: Facade Pattern (convenient interface over generic)
    """
    from workflows.llm_enhancement.scripts.cache.llm_cache import LLMCacheRepository
    
    # Arrange
    cache_repo = LLMCacheRepository(cache_dir=cache_dir, ttl_days=30)
    
    # Act: Use convenience methods
    cache_repo.set_phase1(sample_phase1_response)
    cache_repo.set_phase2(sample_phase2_response)
    
    # Assert: Convenience methods retrieve data correctly
    phase1_result = cache_repo.get_phase1(
        sample_phase1_response.chapter_num,
        sample_phase1_response.prompt_hash
    )
    assert phase1_result is not None, "get_phase1() should return data"
    assert phase1_result.phase == "phase1"
    
    phase2_result = cache_repo.get_phase2(
        sample_phase2_response.chapter_num,
        sample_phase2_response.prompt_hash
    )
    assert phase2_result is not None, "get_phase2() should return data"
    assert phase2_result.phase == "phase2"
    
    # Assert: Generic methods work identically
    generic_phase1 = cache_repo.get(
        "phase1",
        sample_phase1_response.chapter_num,
        sample_phase1_response.prompt_hash
    )
    assert generic_phase1 is not None, "Generic get() should work for phase1"
    assert generic_phase1.parsed_data == phase1_result.parsed_data


# ============================================================
# TEST 8: LLM cache graceful error handling
# ============================================================

def test_llm_cache_graceful_error_handling(
    cache_dir: Path,
    sample_phase1_response: LLMResponse
):
    """
    Test fail-safe behavior for LLM cache errors.
    
    Given:
      - Cache file with corrupted JSON
      - Cache file with missing fields
      - Non-existent cache directory
    
    When:
      - get_phase1() is called on corrupted entry
    
    Then:
      - Returns None (graceful degradation)
      - No exception raised
      - Workflow continues by calling LLM API ($0.30 cost)
    
    Pattern: Fail-safe design (ANTI_PATTERN_ANALYSIS best practices)
    Cost Impact: Cache errors trigger LLM call (acceptable fallback)
    """
    from workflows.llm_enhancement.scripts.cache.llm_cache import LLMCacheRepository
    
    # Arrange: Create cache with valid entry, then corrupt it
    cache_repo = LLMCacheRepository(cache_dir=cache_dir, ttl_days=30)
    cache_repo.set_phase1(sample_phase1_response)
    
    cache_key = cache_repo._get_cache_key(sample_phase1_response.chapter_num, sample_phase1_response.prompt_hash)
    cache_file = cache_repo._get_cache_path("phase1", cache_key)
    
    # Corrupt the JSON file
    with open(cache_file, 'w') as f:
        f.write("{ INVALID JSON }")
    
    # Act: Try to retrieve corrupted data
    result = cache_repo.get_phase1(sample_phase1_response.chapter_num, sample_phase1_response.prompt_hash)
    
    # Assert: Gracefully returns None (no exception)
    assert result is None, "Corrupted LLM cache entry should return None (fail-safe)"


# ============================================================
# TEST 9: Prompt hash generation
# ============================================================

def test_prompt_hash_generation():
    """
    Test _compute_prompt_hash() for cache key generation.
    
    Given:
      - Prompt string: "Select relevant guidelines for chapter 3"
    
    When:
      - _compute_prompt_hash(prompt) is called
    
    Then:
      - Returns SHA256 hash of prompt
      - Hash is deterministic (same prompt → same hash)
      - Different prompts produce different hashes
    
    Pattern: Content-addressable caching (hash-based keys)
    Benefit: Cache invalidation when prompt changes
    """
    from workflows.llm_enhancement.scripts.cache.llm_cache import LLMCacheRepository
    
    # Arrange
    cache_repo = LLMCacheRepository(ttl_days=30)
    prompt_v1 = "Select relevant guidelines for chapter 3"
    prompt_v2 = "Select relevant guidelines for chapter 4"
    
    # Act
    hash_v1 = cache_repo._compute_prompt_hash(prompt_v1)
    hash_v2 = cache_repo._compute_prompt_hash(prompt_v2)
    
    # Assert: Hashes are SHA256 (64 hex characters)
    assert len(hash_v1) == 64, f"SHA256 hash should be 64 characters, got {len(hash_v1)}"
    assert all(c in '0123456789abcdef' for c in hash_v1), "Hash should be hex string"
    
    # Assert: Deterministic (same input → same output)
    hash_v1_repeat = cache_repo._compute_prompt_hash(prompt_v1)
    assert hash_v1 == hash_v1_repeat, "Prompt hash should be deterministic"
    
    # Assert: Different prompts produce different hashes
    assert hash_v1 != hash_v2, "Different prompts should produce different hashes"
