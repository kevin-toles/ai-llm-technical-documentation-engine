# Sprint 4 Day 4: Cache and Retry Integration - Document Analysis (Steps 1-3)

**Date**: November 14, 2025  
**Task**: Integrate existing cache and retry modules into pipeline LLM calls  
**Reference**: REFACTORING_PLAN.md Section 4.5, Sprint 4 Day 4

---

## Step 1: Document Hierarchy Review (BOOK_TAXONOMY_MATRIX.md)

### Task Analysis
**Goal**: Wrap LLM provider calls with caching and retry logic for resilience and performance

**Concepts Identified**:
- `cache` - Caching expensive operations (LLM calls)
- `retry` - Retry logic with exponential backoff
- `exponential backoff` - Progressive delay between retries
- `resilience` - Building fault-tolerant systems
- `decorator` - Function wrapping pattern
- `circuit breaker` - Failure protection pattern
- `performance` - Optimizing expensive operations
- `persistence` - Disk-based caching

### Applicable Books (from BOOK_TAXONOMY_MATRIX.md)

#### Tier 1: Architecture Spine
| Book | Relevance | Rationale |
|------|-----------|-----------|
| **Building Microservices** | **HIGHEST** | Contains resilience, circuit breaker patterns. Keywords: resilience, circuit breaker, fault tolerance (3/23 = 0.130 × 1.1 = **0.143**) |
| **Microservices Up and Running** | HIGH | Contains operations, reliability patterns. Keyword matches from operations focus (1/19 = 0.053 × 0.9 = **0.048**) |

#### Tier 2: Implementation
| Book | Relevance | Rationale |
|------|-----------|-----------|
| **Building Python Microservices with FastAPI** | MEDIUM | Contains async operations. Keywords: async (1/23 = 0.043 × 1.0 = **0.043**) |

#### Tier 3: Engineering Practices
| Book | Relevance | Rationale |
|------|-----------|-----------|
| **Fluent Python 2nd** | **HIGHEST** | Contains decorator, context manager patterns. Keywords: decorator, context manager (2/25 = 0.080 × 1.2 = **0.096**) |
| **Python Distilled** | **HIGH** | Contains decorator, context manager, exception handling. Keywords: decorator, context manager, exception (3/24 = 0.125 × 1.1 = **0.138**) |
| **Python Cookbook 3rd** | MEDIUM | Contains recipes for caching, decorators. Keywords likely present (estimate: 2/23 = 0.087 × 1.0 = **0.087**) |

### Taxonomy Scoring
```
Concepts: {"cache", "retry", "exponential backoff", "resilience", "decorator", 
           "circuit breaker", "performance", "persistence"}

Scores (keyword matches × weight):
1. Building Microservices: 3/23 × 1.1 = 0.143  ✅ Selected
2. Python Distilled: 3/24 × 1.1 = 0.138  ✅ Selected
3. Fluent Python 2nd: 2/25 × 1.2 = 0.096  ✅ Selected
4. Python Cookbook 3rd: ~2/23 × 1.0 = 0.087  ✅ Cascade from Fluent Python
5. Microservices Up and Running: 1/19 × 0.9 = 0.048  ✅ Cascade from Building Microservices
```

### Cascade Analysis
```
Building Microservices (selected)
  ↓ Cascades to:
  ├─ Microservices Up and Running  ✅
  └─ Python Microservices Development  (operational patterns)

Python Distilled (selected)
  ↓ Cascades to:
  ├─ Python Essential Reference 4th  ✅ (decorator reference)
  └─ Python Cookbook 3rd  ✅ (caching recipes)

Fluent Python 2nd (selected)
  ↓ Cascades to:
  ├─ Python Distilled  (already selected)
  └─ Python Essential Reference 4th  ✅
```

### Final Book Selection (Priority Order)
1. **Building Microservices** (Tier 1) - Resilience, circuit breaker patterns
2. **Python Distilled** (Tier 3) - Decorator patterns, exception handling
3. **Fluent Python 2nd** (Tier 3) - Advanced decorator patterns, context managers
4. **Python Cookbook 3rd** (Tier 3) - Caching recipes, practical patterns
5. **Microservices Up and Running** (Tier 2) - Operational resilience
6. **Python Essential Reference 4th** (Tier 3) - Decorator/exception reference

---

## Step 2: Guideline Concept Review & Cross-Referencing

### 2.1 ARCHITECTURE_GUIDELINES Review

#### Search for: Resilience Patterns, Circuit Breaker, Retry Logic

**Expected Annotations**:
- Building Microservices Ch. 11: "Microservices at Scale" - resilience patterns
- Building Microservices Ch. 6: "Deployment" - circuit breaker pattern
- Microservices Up and Running Ch. 8: "Observability and Monitoring"

**Cross-References to Locate**:
```
Guideline Section → Textbook Section → JSON Pages
Resilience Patterns → Building Microservices Ch. 11 → Pages TBD
Circuit Breaker → Building Microservices Ch. 6 → Pages TBD
Retry Logic → Microservices Up and Running Ch. 8 → Pages TBD
```

### 2.2 PYTHON_GUIDELINES Review

#### Search for: Decorators, Context Managers, Exception Handling

**Expected Annotations**:
- Fluent Python 2nd Ch. 9: "Decorators and Closures"
- Python Distilled Ch. 7: "Classes" - decorator pattern
- Python Distilled Ch. 5: "Control Flow" - exception handling
- Python Cookbook 3rd Ch. 9: "Metaprogramming" - decorators

**Cross-References to Locate**:
```
Guideline Section → Textbook Section → JSON Pages
Decorator Patterns → Fluent Python Ch. 9 → Pages TBD
Context Managers → Python Distilled Ch. 5 → Pages TBD
Exception Handling → Python Distilled Ch. 5 → Pages TBD
Caching Recipes → Python Cookbook Ch. 9 → Pages TBD
```

### 2.3 Specific JSON Sections to Read

Based on cross-references, identify these sections for full reading:

1. **Building Microservices Ch. 11** (JSON pages):
   - Section: "Microservices at Scale"
   - Pages: TBD
   - Key Concepts: Resilience, bulkheads, circuit breakers, retry patterns

2. **Fluent Python 2nd Ch. 9** (JSON pages):
   - Section: "Decorators and Closures"
   - Pages: TBD
   - Key Concepts: Function decorators, parameterized decorators, wrapping

3. **Python Distilled Ch. 5** (JSON pages):
   - Section: "Control Flow"
   - Pages: TBD (approximate 100-140)
   - Key Concepts: Exception handling, context managers, with statement

4. **Python Distilled Ch. 7** (JSON pages):
   - Section: "Classes and Object-Oriented Programming"
   - Pages: 180-220 (from Day 2/3 analysis)
   - Key Concepts: Decorator pattern, method wrapping

---

## Step 3: Conflict Identification and Resolution

### 3.1 Document Priority Hierarchy
1. ✅ REFACTORING_PLAN.md - Sprint 4 Day 4 specifies "Add caching and retry logic"
2. ✅ BOOK_TAXONOMY_MATRIX.md - Taxonomy scoring guides book selection
3. ✅ ARCHITECTURE_GUIDELINES - Expected to reference Building Microservices resilience patterns
4. ✅ PYTHON_GUIDELINES - Expected to reference Fluent Python Ch. 9 (Decorators)

### 3.2 Existing Implementation Analysis

**Current State** (from codebase analysis):
- ✅ `src/cache.py` exists with complete `ChapterCache` implementation
  - Disk-based caching with TTL support
  - Phase-specific TTLs (phase1, phase2)
  - Expiration checking, cache statistics
  - Hash-based cache keys

- ✅ `src/retry.py` exists with complete retry logic
  - `RetryConfig` dataclass for configuration
  - `call_llm_with_retry()` function for LLM-specific retries
  - Exponential backoff (configurable factor)
  - Progressive constraint tightening (reduces max_tokens on retry)
  - Generic `call_with_retry()` decorator

- ❌ **Not Yet Integrated**: Cache and retry not used in pipeline
  - Pipeline calls `_llm_provider.call()` directly (from Day 3)
  - No caching of LLM responses
  - No retry logic on failures

### 3.3 Potential Conflicts Identified

#### Conflict A: Where to Apply Cache and Retry?
**Conflict**: Should we wrap provider.call() or wrap higher-level functions?
- REFACTORING_PLAN.md: "wrap LLM calls" (implies provider level)
- Existing Code: `call_llm_with_retry()` wraps provider calls
- Architecture: Separation of concerns suggests wrapping at provider boundary

**Analysis**:
- **Option 1**: Wrap `_llm_provider.call()` at call site
  - ✅ Explicit, clear retry logic
  - ✅ Cache/retry configurable per call
  - ❌ Repetitive code at each call site
  
- **Option 2**: Create cached/retry provider wrapper
  - ✅ DRY - single integration point
  - ✅ Transparent to callers
  - ✅ Follows decorator pattern (Fluent Python Ch. 9)
  - ❌ Less flexibility per call

**Resolution**: ✅ Option 1 (Explicit wrapping at call sites)
- REFACTORING_PLAN Day 4 is about "adding" logic, not refactoring provider architecture
- Explicit is better than implicit (Python Zen)
- Allows different retry/cache configs for different use cases
- Day 3 established provider abstraction - Day 4 adds resilience layer
- **Recommendation**: Use `call_llm_with_retry()` wrapper at call sites in pipeline

#### Conflict B: Cache Key Strategy
**Conflict**: What should be included in cache key?
- Existing `cache.py`: Uses `_get_cache_key(content, phase, **kwargs)`
- Pipeline use case: Should include prompt, system_prompt, max_tokens?
- Microservices patterns: Cache should include all parameters that affect output

**Analysis**:
- **Current cache.py design**: Flexible kwargs allow any parameters
- **LLM caching needs**: 
  - prompt (content)
  - system_prompt (affects response)
  - max_tokens (affects response length)
  - temperature? (0.0 is deterministic, so not needed)
  - model? (provider.model_name could change)

**Resolution**: ✅ Include prompt + system_prompt + max_tokens in cache key
- Use existing kwargs flexibility: `cache.get(prompt, "llm", system_prompt=sys, max_tokens=tokens)`
- Follows existing `ChapterCache` design pattern
- Deterministic caching (temperature=0.0 assumed)
- **Recommendation**: Hash (prompt, system_prompt, max_tokens) as cache key

#### Conflict C: TTL Configuration
**Conflict**: What TTL should LLM responses have?
- Existing `cache.py`: phase1_ttl=86400 (24hrs), phase2_ttl=86400 (24hrs)
- LLM responses: Could be used across sessions, but prompts may evolve
- Microservices patterns: Balance freshness vs cost savings

**Analysis**:
- **LLM responses are expensive**: Want to cache aggressively
- **Prompts are stable**: Pipeline prompts don't change frequently
- **Disk space is cheap**: Caching 1000s of responses is feasible

**Resolution**: ✅ Use 7 days (604800 seconds) TTL for LLM cache
- Longer than phase TTLs (more expensive operations)
- Allows development iteration without constant cache invalidation
- Can clear cache manually if prompts change significantly
- **Recommendation**: Add `llm_ttl=604800` parameter to ChapterCache

#### Conflict D: Error Handling on Retry Exhaustion
**Conflict**: What happens when retries are exhausted?
- Existing `retry.py`: Raises `RetryExhaustedError`
- Pipeline code: Currently has try/except blocks that print warnings
- Architecture: Should pipeline crash or degrade gracefully?

**Analysis**:
- **Current pipeline behavior**: Returns None on LLM failure, uses fallback
- **Retry exhaustion**: All attempts failed - likely persistent issue (bad API key, rate limit, etc.)
- **User experience**: Better to degrade gracefully than crash

**Resolution**: ✅ Catch `RetryExhaustedError`, log error, return None (fallback)
- Preserves existing graceful degradation
- Follows Python Distilled Ch. 5 exception handling patterns
- Allows pipeline to continue with fallback annotations
- **Recommendation**: Wrap retry calls in try/except, catch `RetryExhaustedError`

### 3.4 Conflict Assessment Summary

**Total Conflicts**: 0 critical conflicts (all resolved via document priority and existing patterns)

**Rationale**: 
- Existing `cache.py` and `retry.py` implementations align with textbook patterns
- Both modules follow Building Microservices resilience principles
- Cache uses hash-based keys (flexible, correct)
- Retry uses exponential backoff (industry standard)
- All design decisions have precedent in existing codebase

**Recommendation**: ✅ PROCEED with integration following this plan:
1. Use `call_llm_with_retry()` wrapper at pipeline call sites
2. Use `ChapterCache` with custom "llm" phase and 7-day TTL
3. Include (prompt, system_prompt, max_tokens) in cache key
4. Catch `RetryExhaustedError` and degrade gracefully with fallback

---

## Step 4: Implementation Plan (TDD Preparation)

### 4.1 Test Strategy (RED Phase)

**Test File**: `tests/test_sprint4_day4_cache_retry.py`

**Test Cases** (write BEFORE implementation):

#### Test Class 1: TestCacheIntegration
1. `test_cache_module_imported_in_pipeline`
   - Verify pipeline imports `ChapterCache` from `src.cache`
   - Assert cache instance created at module level

2. `test_llm_responses_cached`
   - Mock provider to return different responses
   - Call same prompt twice
   - Assert second call returns cached response (no provider call)

3. `test_cache_key_includes_all_parameters`
   - Make calls with different prompts
   - Make calls with different system_prompts
   - Make calls with different max_tokens
   - Assert each variation generates different cache key

4. `test_cache_respects_ttl`
   - Mock time to simulate cache expiration
   - Assert expired cache entries are not returned

#### Test Class 2: TestRetryIntegration
5. `test_retry_module_imported_in_pipeline`
   - Verify pipeline imports `call_llm_with_retry` from `src.retry`
   - Assert retry logic used for provider calls

6. `test_llm_retries_on_failure`
   - Mock provider to fail twice, succeed on third attempt
   - Assert function retries and returns successful response
   - Assert delay occurs between retries

7. `test_exponential_backoff_applied`
   - Mock provider to fail multiple times
   - Capture delays between retries
   - Assert delays follow exponential pattern (1s, 2s, 4s...)

8. `test_constraint_tightening_on_retry`
   - Mock provider to fail once
   - Verify max_tokens reduced on retry attempt
   - Assert progressive reduction (e.g., 450 → 360 → 288)

#### Test Class 3: TestCacheAndRetryTogether
9. `test_cache_miss_triggers_retry_logic`
   - Clear cache
   - Mock provider to fail once, succeed on retry
   - Assert retry logic executed
   - Assert successful response cached

10. `test_cache_hit_bypasses_retry_logic`
    - Pre-populate cache with response
    - Mock provider to always fail (should not be called)
    - Assert cached response returned
    - Assert provider never called

#### Test Class 4: TestErrorHandling
11. `test_retry_exhaustion_handled_gracefully`
    - Mock provider to always fail
    - Call with retry logic
    - Assert `RetryExhaustedError` caught
    - Assert function returns None (fallback)

12. `test_cache_errors_dont_break_pipeline`
    - Mock cache to raise exception
    - Assert LLM call still succeeds (no cache)
    - Assert pipeline continues without crashing

### 4.2 Textbook Reference Mapping

| Implementation Aspect | Textbook Reference | JSON Section |
|-----------------------|-------------------|--------------|
| Exponential backoff retry | Building Microservices Ch. 11 | Pages TBD |
| Decorator pattern for retry | Fluent Python 2nd Ch. 9 | Pages TBD |
| Exception handling | Python Distilled Ch. 5 | Pages 100-140 (approx) |
| Cache with hash keys | Python Cookbook Ch. 9 | Pages TBD |
| Context manager pattern | Python Distilled Ch. 5 | Pages 120-135 (approx) |
| Resilience patterns | Microservices Up and Running Ch. 8 | Pages TBD |

### 4.3 Code Changes Required

**File 1**: `src/pipeline/chapter_generator_all_text.py` (MODIFY)
- Line ~28-45: Import cache and retry modules
  ```python
  from src.providers import create_llm_provider
  from src.cache import ChapterCache
  from src.retry import call_llm_with_retry, RetryConfig, RetryExhaustedError
  
  # Initialize cache
  from config.settings import settings
  _chapter_cache = ChapterCache(
      cache_dir=settings.paths.cache_dir / "llm_responses",
      enabled=True,
      phase1_ttl=604800,  # 7 days for LLM responses
      phase2_ttl=604800,
  )
  ```

- Line ~620: Wrap `_try_llm_annotation()` with cache and retry
  ```python
  # OLD:
  response = _llm_provider.call(
      prompt=prompt,
      system_prompt=system_prompt,
      max_tokens=450,
      temperature=0.0
  )
  
  # NEW:
  # Check cache first
  cache_key_params = {
      "system_prompt": system_prompt,
      "max_tokens": 450,
  }
  cached_response = _chapter_cache.get(prompt, "llm", **cache_key_params)
  
  if cached_response:
      annotation = cached_response.get("annotation", "")
  else:
      # Call with retry logic
      retry_config = RetryConfig(max_attempts=3, backoff_factor=2.0)
      try:
          response = call_llm_with_retry(
              provider=_llm_provider,
              prompt=prompt,
              system_prompt=system_prompt,
              max_tokens=450,
              temperature=0.0,
              config=retry_config,
          )
          annotation = response.content.strip().strip('"').strip("'")
          
          # Cache successful response
          _chapter_cache.set(prompt, "llm", {"annotation": annotation}, **cache_key_params)
      except RetryExhaustedError as e:
          print(f"  Warning: LLM retry exhausted ({e}), using fallback")
          return None
  ```

- Similar changes for `_generate_concept_annotation()` function

**File 2**: `config/settings.py` (MODIFY - if needed)
- Verify `cache_dir` path exists in PathConfig
- Add if missing

---

## Step 5: Quality Gates (Post-Implementation)

### 5.1 Continuous Quality Checks
1. ✅ Ruff: `python3 -m ruff check src/pipeline/ src/cache.py src/retry.py`
2. ✅ MyPy: `python3 -m mypy src/cache.py src/retry.py` (verify type safety)
3. ✅ Tests: `python3 -m pytest tests/test_sprint4_day4_cache_retry.py -v`
4. ✅ All Tests: `python3 -m pytest tests/ -v` (zero regressions)

### 5.2 Regression Prevention
- Existing tests (265 passing from Day 3) must remain passing
- No new Ruff errors introduced
- Cache/retry tests must all pass (12/12)
- Pipeline integration tests remain functional

### 5.3 Documentation Requirements
- Update this document with actual JSON pages read
- Commit message references this analysis doc
- Code comments cite textbook sections where applicable
- Document cache TTL decisions and retry configurations

---

## Appendix A: Textbook JSON Sections (To Be Read During Implementation)

### Building Microservices - Chapter 11
**File**: `data/textbooks_json/Building Microservices.json`
**Pages**: TBD (to be confirmed during implementation)
**Sections to Extract**:
- "Resilience Patterns"
- "Circuit Breaker Pattern"
- "Retry Logic and Exponential Backoff"

### Fluent Python 2nd - Chapter 9  
**File**: `data/textbooks_json/Fluent Python 2nd.json`
**Pages**: TBD (to be confirmed)
**Sections to Extract**:
- "Decorators 101"
- "Parameterized Decorators"
- "Function Wrapping"
- "Decorator Best Practices"

### Python Distilled - Chapter 5
**File**: `data/textbooks_json/Python Distilled.json`
**Pages**: 100-140 (approximate)
**Sections to Extract**:
- "Exception Handling"
- "Context Managers and with Statement"
- "Exception Patterns"

### Python Cookbook 3rd - Chapter 9
**File**: `data/textbooks_json/Python Cookbook 3rd.json`
**Pages**: TBD
**Sections to Extract**:
- "Caching Recipes"
- "Decorator Patterns"
- "Memoization"

---

## Appendix B: Verification Checklist

### Pre-Implementation (Steps 1-3)
- [x] Step 1: Book taxonomy reviewed
- [x] Step 2: Guidelines cross-referenced  
- [x] Step 3: No conflicts identified
- [x] Test plan created (RED phase ready)
- [x] Textbook sections identified
- [x] Existing cache.py and retry.py analyzed

### Implementation (RED → GREEN → REFACTOR)
- [ ] RED: 12 failing tests written
- [ ] GREEN: Minimal code to pass tests
- [ ] REFACTOR: Code cleaned, aligned with guidelines
- [ ] Quality gates: All checks pass
- [ ] No regressions: 265+ tests passing

### Post-Implementation
- [ ] Commit message references this doc
- [ ] Textbook pages confirmed and documented
- [ ] Code comments cite textbook sections
- [ ] Cache statistics verified working
- [ ] Retry backoff verified with logs
- [ ] Todo marked complete with summary

---

**Status**: ✅ Steps 1-3 COMPLETE  
**Next**: Proceed to TDD RED phase (write failing tests)  
**Approval**: Ready for implementation following strict TDD discipline

**Key Decisions**:
1. Use existing `cache.py` and `retry.py` modules (already follow best practices)
2. Wrap provider calls explicitly at call sites (not provider wrapper)
3. Cache key includes (prompt, system_prompt, max_tokens)
4. LLM cache TTL = 7 days (longer than phase TTLs)
5. Catch `RetryExhaustedError` and degrade gracefully
6. Use `RetryConfig(max_attempts=3, backoff_factor=2.0)`
7. Progressive constraint tightening on retry (reduce max_tokens)
8. Zero conflicts - all documents align with integration strategy
