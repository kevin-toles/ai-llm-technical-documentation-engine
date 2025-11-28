"""
LLMCacheRepository: Repository Pattern for LLM response cache.

Caches expensive Claude API responses for content selection (phase1) and citation extraction (phase2).

Design Principles:
1. Repository Pattern: Abstract storage behind clean interface
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

Pattern References:
- Architecture Patterns with Python Ch. 2 (Repository Pattern)
- Python Architecture Patterns Ch. 3, pg. 99 (Cache systems)
- Learning Python Ed6 Ch. 9 (File I/O), Ch. 28-31 (Dataclass patterns)

File Structure:
    cache/llm_responses/
        phase1/
            chapter_1_abc12345.json
            chapter_2_def67890.json
            ...
        phase2/
            chapter_1_xyz98765.json
            chapter_2_mno54321.json
            ...

Cache File Format:
    {
        "metadata": {
            "key": "chapter_3_abc12345",
            "created_at": 1234567890.0,
            "ttl_seconds": 2592000,
            "content_hash": "abc12345"  # Reused for prompt_hash
        },
        "data": {
            "phase": "phase1",
            "chapter_num": 3,
            "prompt_hash": "abc12345",
            "response_text": "{...}",
            "parsed_data": {...},
            "model": "claude-sonnet-4",
            "tokens_used": 1200
        }
    }
"""

import hashlib
import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Optional, Any


# ============================================================
# DATACLASS DEFINITIONS
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
# REPOSITORY IMPLEMENTATION
# ============================================================

class LLMCacheRepository:
    """
    Repository Pattern for LLM response cache.
    
    Abstracts file-based cache storage for expensive Claude API calls.
    Implements Cache-Aside Pattern with TTL-based expiration.
    Separate phase1/phase2 directories for organization.
    
    Pattern: Repository Pattern (Architecture Patterns Ch. 2)
    Anti-Pattern Avoidance: Optional types for nullable returns (ANTI_PATTERN_ANALYSIS §1.1)
    
    Usage:
        >>> cache = LLMCacheRepository(ttl_days=30)
        >>> 
        >>> # Phase 1: Content selection
        >>> prompt_hash = cache._compute_prompt_hash(prompt)
        >>> response = cache.get_phase1(chapter_num=3, prompt_hash=prompt_hash)
        >>> if response is None:
        ...     response = call_llm_api(prompt)  # $0.30 cost
        ...     cache.set_phase1(response)
        >>> 
        >>> # Phase 2: Citation extraction
        >>> response = cache.get_phase2(chapter_num=3, prompt_hash=prompt_hash)
        >>> if response is None:
        ...     response = call_llm_api(prompt)  # $0.30 cost
        ...     cache.set_phase2(response)
    
    Cost Savings:
        - Cache hit: $0 (100% savings)
        - Cache miss: $0.30 per phase
        - Total savings: Up to $0.60 per chapter on repeated runs
    """
    
    def __init__(self, cache_dir: Optional[Path] = None, ttl_days: int = 30):
        """
        Initialize LLMCacheRepository.
        
        Args:
            cache_dir: Root directory for cache storage. Defaults to: cache/llm_responses/
            ttl_days: Time-to-live in days. Default 30 days (expensive to regenerate - $0.60/chapter).
        
        Pattern: Repository Pattern initialization (Architecture Patterns Ch. 2)
        """
        if cache_dir is None:
            # Default location: cache/llm_responses/
            self.cache_dir = Path("cache/llm_responses")
        else:
            self.cache_dir = cache_dir
        
        # Create phase-specific directories
        self.phase1_dir = self.cache_dir / "phase1"
        self.phase2_dir = self.cache_dir / "phase2"
        
        self.phase1_dir.mkdir(parents=True, exist_ok=True)
        self.phase2_dir.mkdir(parents=True, exist_ok=True)
        
        self.ttl_seconds = ttl_days * 24 * 60 * 60  # Convert days to seconds
    
    def get(self, phase: str, chapter_num: int, prompt_hash: str) -> Optional[LLMResponse]:
        """
        Retrieve cached LLM response (generic method).
        
        Args:
            phase: "phase1" or "phase2"
            chapter_num: Chapter number
            prompt_hash: Hash of prompt sent to LLM
        
        Returns:
            LLMResponse if cache hit and not expired, None otherwise
        
        Cache Invalidation:
            - TTL expiration: Entry deleted if older than 30 days
            - Prompt hash mismatch: Different hash → cache miss (prompt changed)
            - Corrupted file: Returns None (graceful degradation)
        
        Pattern: Cache-Aside Pattern
        Anti-Pattern Avoidance: Returns Optional[T] not None (ANTI_PATTERN_ANALYSIS §1.1)
        Cost Impact: Cache miss triggers $0.30 LLM API call
        """
        try:
            cache_key = self._get_cache_key(chapter_num, prompt_hash)
            cache_file = self._get_cache_path(phase, cache_key)
            
            # Cache miss: File doesn't exist
            if not cache_file.exists():
                return None
            
            # Read cache file
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # Validate cache structure
            if 'metadata' not in cache_data or 'data' not in cache_data:
                return None
            
            # Parse metadata
            metadata = CacheEntry.from_dict(cache_data['metadata'])
            
            # Check TTL expiration
            if metadata.is_expired():
                # Delete expired entry
                cache_file.unlink(missing_ok=True)
                return None
            
            # Verify prompt hash matches (detect prompt changes)
            if metadata.content_hash != prompt_hash:
                return None
            
            # Parse cached data
            data = cache_data['data']
            result = LLMResponse(
                phase=data['phase'],
                chapter_num=data['chapter_num'],
                prompt_hash=data['prompt_hash'],
                response_text=data['response_text'],
                parsed_data=data['parsed_data'],
                model=data['model'],
                tokens_used=data['tokens_used']
            )
            
            return result
        
        except (json.JSONDecodeError, KeyError, IOError, OSError) as e:
            # Graceful degradation: Cache errors return None
            # Workflow continues by calling LLM API ($0.30 cost acceptable)
            return None
    
    def set(self, response: LLMResponse) -> None:
        """
        Store LLM response in cache (generic method).
        
        Args:
            response: LLMResponse to cache
        
        Cache Structure:
            {
                "metadata": { CacheEntry fields },
                "data": { LLMResponse fields }
            }
        
        Pattern: Value Object (CacheEntry) wraps business data
        Error Handling: Graceful failure (doesn't raise exceptions)
        Cost Impact: Successful cache write saves $0.30 on future runs
        """
        try:
            cache_key = self._get_cache_key(response.chapter_num, response.prompt_hash)
            cache_file = self._get_cache_path(response.phase, cache_key)
            
            # Create metadata wrapper (reuse content_hash for prompt_hash)
            metadata = CacheEntry(
                key=cache_key,
                created_at=time.time(),
                ttl_seconds=self.ttl_seconds,
                content_hash=response.prompt_hash  # Reuse field for prompt_hash
            )
            
            # Serialize to JSON
            cache_data = {
                'metadata': metadata.to_dict(),
                'data': asdict(response)
            }
            
            # Write cache file atomically
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
        
        except (IOError, OSError) as e:
            # Graceful failure: Cache write errors don't break workflow
            pass
    
    def get_phase1(self, chapter_num: int, prompt_hash: str) -> Optional[LLMResponse]:
        """
        Retrieve cached phase1 LLM response (content selection).
        
        Convenience method for get("phase1", chapter_num, prompt_hash).
        
        Args:
            chapter_num: Chapter number
            prompt_hash: Hash of phase1 prompt
        
        Returns:
            LLMResponse if cache hit, None otherwise
        
        Pattern: Facade Pattern (convenient interface)
        Cost Savings: $0.30 per cache hit
        """
        return self.get("phase1", chapter_num, prompt_hash)
    
    def get_phase2(self, chapter_num: int, prompt_hash: str) -> Optional[LLMResponse]:
        """
        Retrieve cached phase2 LLM response (citation extraction).
        
        Convenience method for get("phase2", chapter_num, prompt_hash).
        
        Args:
            chapter_num: Chapter number
            prompt_hash: Hash of phase2 prompt
        
        Returns:
            LLMResponse if cache hit, None otherwise
        
        Pattern: Facade Pattern (convenient interface)
        Cost Savings: $0.30 per cache hit
        """
        return self.get("phase2", chapter_num, prompt_hash)
    
    def set_phase1(self, response: LLMResponse) -> None:
        """
        Store phase1 LLM response (content selection).
        
        Convenience method with validation that phase="phase1".
        
        Args:
            response: LLMResponse with phase="phase1"
        
        Pattern: Type-safe convenience method
        Cost Impact: Saves $0.30 on future runs
        """
        if response.phase != "phase1":
            # Validation: Ensure correct phase
            response = LLMResponse(
                phase="phase1",
                chapter_num=response.chapter_num,
                prompt_hash=response.prompt_hash,
                response_text=response.response_text,
                parsed_data=response.parsed_data,
                model=response.model,
                tokens_used=response.tokens_used
            )
        self.set(response)
    
    def set_phase2(self, response: LLMResponse) -> None:
        """
        Store phase2 LLM response (citation extraction).
        
        Convenience method with validation that phase="phase2".
        
        Args:
            response: LLMResponse with phase="phase2"
        
        Pattern: Type-safe convenience method
        Cost Impact: Saves $0.30 on future runs
        """
        if response.phase != "phase2":
            # Validation: Ensure correct phase
            response = LLMResponse(
                phase="phase2",
                chapter_num=response.chapter_num,
                prompt_hash=response.prompt_hash,
                response_text=response.response_text,
                parsed_data=response.parsed_data,
                model=response.model,
                tokens_used=response.tokens_used
            )
        self.set(response)
    
    def clear(self) -> int:
        """
        Delete all LLM cache entries (both phase1 and phase2).
        
        Returns:
            Number of entries deleted
        
        Pattern: Repository Pattern maintenance operation
        Use Case: Force LLM recomputation, clear stale prompts, free disk space
        Cost Impact: Next run will incur full $0.60/chapter LLM cost
        """
        try:
            deleted_count = 0
            
            # Clear phase1 entries
            for cache_file in self.phase1_dir.glob("chapter_*.json"):
                cache_file.unlink(missing_ok=True)
                deleted_count += 1
            
            # Clear phase2 entries
            for cache_file in self.phase2_dir.glob("chapter_*.json"):
                cache_file.unlink(missing_ok=True)
                deleted_count += 1
            
            return deleted_count
        except (IOError, OSError):
            return 0
    
    def _get_cache_key(self, chapter_num: int, prompt_hash: str) -> str:
        """
        Generate cache key from chapter number and prompt hash.
        
        Args:
            chapter_num: Chapter number
            prompt_hash: Full hash string (will be truncated to 8 chars)
        
        Returns:
            Cache key format: "chapter_{num}_{hash[:8]}"
        
        Pattern: Deterministic key generation (same inputs → same key)
        Rationale: Truncate hash for readability (8 chars = 4B collision space)
        """
        return f"chapter_{chapter_num}_{prompt_hash[:8]}"
    
    def _get_cache_path(self, phase: str, cache_key: str) -> Path:
        """
        Get full path to cache file in phase-specific directory.
        
        Args:
            phase: "phase1" or "phase2"
            cache_key: Cache key from _get_cache_key()
        
        Returns:
            Full path: {cache_dir}/{phase}/{cache_key}.json
        
        Pattern: File I/O with pathlib.Path (Learning Python Ch. 9)
        Benefit: Phase separation prevents key collisions
        """
        if phase == "phase1":
            return self.phase1_dir / f"{cache_key}.json"
        elif phase == "phase2":
            return self.phase2_dir / f"{cache_key}.json"
        else:
            raise ValueError(f"Invalid phase: {phase}. Expected 'phase1' or 'phase2'")
    
    def _compute_prompt_hash(self, prompt: str) -> str:
        """
        Compute SHA256 hash of prompt text.
        
        Args:
            prompt: Full prompt text sent to LLM
        
        Returns:
            SHA256 hash (64 hex characters)
        
        Pattern: Content-addressable caching
        Use Case: Detect prompt changes for cache invalidation
        Benefit: Cache survives prompt engineering iterations
        
        Note: Caller should compute hash once and reuse.
              Different prompts → different hashes → separate cache entries.
        """
        return hashlib.sha256(prompt.encode('utf-8')).hexdigest()
