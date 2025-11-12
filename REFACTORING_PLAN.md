# REFACTORING PLAN - LLM Document Enhancer
## Standalone Repo Improvements

**Repository**: `/Users/kevintoles/POC/llm-document-enhancer`  
**Date**: November 11, 2025  
**Based On**: Engineering feedback from tpm-job-finder-poc testing

---

## I. ENGINEERING FEEDBACK ADDRESSED

From your comprehensive technical review, we identified:

1. **JSON Parsing Issues**: Truncation detection needed improvement
2. **Token Management**: Better validation of finish_reason
3. **Error Handling**: Missing edge cases in response parsing
4. **Book Taxonomy**: Underutilized - could pre-filter before LLM
5. **Code Quality**: Some areas need refactoring for maintainability

---

## II. PRIORITY IMPROVEMENTS

### Phase 1: Critical Fixes (Immediate)

#### 1.1 Enhanced JSON Validation (`src/llm_integration.py`)

**Current Issues**:
- Basic truncation detection (line 317-367)
- No validation of JSON structure
- Missing finish_reason checks

**Improvements**:

```python
# File: src/llm_integration.py
# Location: After line 140 (in call_llm function)

def _validate_json_response(response_text: str, finish_reason: str) -> Tuple[bool, Optional[str]]:
    """
    Validate JSON response completeness and structure.
    
    Returns:
        (is_valid, error_message)
    """
    # Check finish_reason first
    if finish_reason != "end_turn":
        return False, f"Incomplete response: {finish_reason}"
    
    # Attempt to parse JSON
    try:
        parsed = json.loads(response_text)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    
    # Validate structure (for Phase 1 responses)
    if isinstance(parsed, list):
        # Phase 1: Array of content requests
        for idx, item in enumerate(parsed):
            if not isinstance(item, dict):
                return False, f"Item {idx} is not a dict"
            
            required_fields = ["book_title", "chapter", "reason"]
            missing = [f for f in required_fields if f not in item]
            if missing:
                return False, f"Item {idx} missing fields: {missing}"
    
    return True, None


def _handle_truncated_response(
    phase: str,
    messages: List[Dict],
    attempt: int,
    max_retries: int = 2
) -> Optional[str]:
    """
    Handle truncated responses with progressive constraint tightening.
    
    Phase 1: Reduce book limit (15 -> 10 -> 5)
    Phase 2: Cannot retry (contains actual content)
    """
    if phase == "phase_2":
        logger.error("Phase 2 truncated - cannot retry (would lose content)")
        return None
    
    if attempt >= max_retries:
        logger.error(f"Max retries ({max_retries}) exceeded")
        return None
    
    # Progressive limits
    limits = [10, 5, 3]
    new_limit = limits[min(attempt, len(limits) - 1)]
    
    logger.warning(f"Retry {attempt + 1}: Constraining to top {new_limit} books")
    
    # Modify system message to add constraint
    constraint_msg = f"\n\nIMPORTANT: Limit requests to TOP {new_limit} most relevant books only."
    messages[0]["content"] += constraint_msg
    
    return call_llm(messages, phase=phase, _retry_attempt=attempt + 1)
```

**Integration** (update existing `call_llm` function):

```python
# Line ~175 in src/llm_integration.py
# Replace existing validation with:

# Validate response
is_valid, error_msg = _validate_json_response(response_text, finish_reason)

if not is_valid:
    logger.error(f"Invalid response: {error_msg}")
    
    # Attempt retry if truncated
    if "length" in finish_reason.lower() or "max_tokens" in finish_reason.lower():
        retry_response = _handle_truncated_response(
            phase=phase,
            messages=messages,
            attempt=getattr(call_llm, '_retry_attempt', 0)
        )
        if retry_response:
            return retry_response
    
    raise ValueError(f"LLM response validation failed: {error_msg}")
```

---

#### 1.2 Book Taxonomy Pre-Filtering (`src/interactive_llm_system_v3_hybrid_prompt.py`)

**Current State**: Book taxonomy imported but only used for display

**Improvement**: Pre-filter books before sending to LLM (save ~40% tokens)

```python
# File: src/interactive_llm_system_v3_hybrid_prompt.py
# Add new method to AnalysisOrchestrator class (around line 800)

def _prefilter_books_by_taxonomy(
    self,
    guideline_text: str,
    max_books: int = 10
) -> List[str]:
    """
    Use book taxonomy to pre-filter most relevant books before LLM analysis.
    
    Extracts concepts from guideline, scores books, returns top N.
    Reduces token usage by ~40% while maintaining quality.
    """
    # Extract key concepts from guideline (simple keyword extraction)
    concepts = self._extract_concepts_from_text(guideline_text)
    
    # Score books using taxonomy
    scored_books = score_books_for_concepts(concepts)
    
    # Get top N books
    top_books = [book.title for book, score in scored_books[:max_books]]
    
    logger.info(f"Taxonomy pre-filtered to {len(top_books)} books: {top_books}")
    
    return top_books


def _extract_concepts_from_text(self, text: str) -> List[str]:
    """Extract programming concepts from text for taxonomy scoring."""
    # Keywords that indicate concepts
    concept_keywords = [
        "class", "function", "method", "module", "package",
        "decorator", "generator", "iterator", "context manager",
        "async", "await", "coroutine", "thread", "process",
        "pytest", "unittest", "mock", "fixture",
        "microservice", "api", "rest", "fastapi", "flask",
        "architecture", "pattern", "solid", "dry",
        "type hint", "annotation", "protocol", "generic"
    ]
    
    text_lower = text.lower()
    found_concepts = [kw for kw in concept_keywords if kw in text_lower]
    
    # Also extract capitalized terms (likely proper nouns/concepts)
    import re
    capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
    
    return found_concepts + capitalized[:10]  # Limit to avoid noise
```

**Integration** (update `analyze_with_llm` method):

```python
# Line ~900 in src/interactive_llm_system_v3_hybrid_prompt.py
# At start of analyze_with_llm, before Phase 1:

# Pre-filter books using taxonomy
if TAXONOMY_AVAILABLE:
    recommended_books = self._prefilter_books_by_taxonomy(
        guideline_text=content,
        max_books=10
    )
    
    # Update prompt to only include these books
    book_filter_note = f"""
IMPORTANT: Focus ONLY on these pre-selected relevant books:
{', '.join(recommended_books)}

Do not request content from other books in the library.
"""
    # Add to Phase 1 system message
    phase_1_messages[0]["content"] += book_filter_note
```

---

#### 1.3 Finish Reason Validation (`src/llm_integration.py`)

**Current**: finish_reason logged but not fully validated

**Improvement**: Comprehensive finish_reason handling

```python
# File: src/llm_integration.py
# Add enum and validation (around line 30)

from enum import Enum

class FinishReason(Enum):
    """Anthropic API finish reasons."""
    END_TURN = "end_turn"          # Normal completion
    MAX_TOKENS = "max_tokens"       # Hit output limit (truncated)
    STOP_SEQUENCE = "stop_sequence" # Hit stop sequence
    ERROR = "error"                 # API error
    
    @classmethod
    def is_complete(cls, reason: str) -> bool:
        """Check if response is complete (not truncated)."""
        return reason == cls.END_TURN.value or reason == cls.STOP_SEQUENCE.value
    
    @classmethod
    def is_truncated(cls, reason: str) -> bool:
        """Check if response was truncated."""
        return reason == cls.MAX_TOKENS.value


# Update call_llm to use enum (around line 180)

finish_reason = response.stop_reason

# Log finish reason with severity
if FinishReason.is_complete(finish_reason):
    logger.info(f"Response complete: {finish_reason}")
elif FinishReason.is_truncated(finish_reason):
    logger.warning(f"Response TRUNCATED: {finish_reason}")
else:
    logger.error(f"Unexpected finish reason: {finish_reason}")

# Validate based on finish reason
if not FinishReason.is_complete(finish_reason):
    logger.warning(f"Incomplete response (finish_reason={finish_reason})")
    
    # Attempt retry for truncation
    if FinishReason.is_truncated(finish_reason):
        return _handle_truncated_response(phase, messages, attempt=0)
```

---

### Phase 2: Code Quality Improvements (Next Sprint)

#### 2.1 Extract Prompt Templates (`src/prompts/`)

**Problem**: Long prompt strings embedded in code (lines 710-1400)

**Solution**: Extract to template files

```
src/
  prompts/
    __init__.py
    phase1_system.txt
    phase1_user.txt
    phase2_system.txt
    phase2_user.txt
    templates.py  # Template loader and formatter
```

**Implementation**:

```python
# File: src/prompts/templates.py

from pathlib import Path
from typing import Dict, Any

PROMPTS_DIR = Path(__file__).parent

def load_template(name: str) -> str:
    """Load prompt template from file."""
    template_file = PROMPTS_DIR / f"{name}.txt"
    return template_file.read_text()

def format_phase1_prompt(
    guideline_section: str,
    available_books: str,
    recommended_books: str = ""
) -> Dict[str, str]:
    """Format Phase 1 prompts with dynamic content."""
    system = load_template("phase1_system")
    user = load_template("phase1_user")
    
    return {
        "system": system.format(
            available_books=available_books,
            recommended_books=recommended_books
        ),
        "user": user.format(guideline_section=guideline_section)
    }
```

---

#### 2.2 Add Unit Tests (`tests/`)

**Coverage Targets**:
- `test_llm_integration.py` - API wrapper, JSON validation, retry logic
- `test_metadata_extraction.py` - Book metadata service
- `test_book_taxonomy.py` - Scoring and filtering
- `test_prompt_templates.py` - Template loading and formatting

**Example Test**:

```python
# File: tests/test_llm_integration.py

import pytest
from src.llm_integration import _validate_json_response, FinishReason

def test_validate_json_response_valid():
    """Test valid JSON response passes validation."""
    response = '[{"book_title": "Test", "chapter": 1, "reason": "test"}]'
    is_valid, error = _validate_json_response(response, "end_turn")
    assert is_valid
    assert error is None

def test_validate_json_response_truncated():
    """Test truncated response detected."""
    response = '[{"book_title": "Test", "chapter":'  # Incomplete
    is_valid, error = _validate_json_response(response, "max_tokens")
    assert not is_valid
    assert "Incomplete response" in error

def test_finish_reason_classification():
    """Test finish reason enum classification."""
    assert FinishReason.is_complete("end_turn")
    assert FinishReason.is_truncated("max_tokens")
    assert not FinishReason.is_complete("max_tokens")

@pytest.mark.parametrize("finish_reason,expected", [
    ("end_turn", True),
    ("stop_sequence", True),
    ("max_tokens", False),
    ("error", False),
])
def test_finish_reason_is_complete(finish_reason, expected):
    """Test finish reason completion detection."""
    assert FinishReason.is_complete(finish_reason) == expected
```

---

#### 2.3 Configuration Management (`src/config.py`)

**Problem**: Magic numbers and hardcoded values scattered across files

**Solution**: Centralized configuration

```python
# File: src/config.py

import os
from dataclasses import dataclass
from pathlib import Path

@dataclass
class LLMConfig:
    """LLM API configuration."""
    provider: str = "anthropic"
    model: str = "claude-sonnet-4-5-20250929"
    temperature: float = 0.2
    max_tokens: int = 8192
    max_retries: int = 2
    
    @classmethod
    def from_env(cls):
        """Load configuration from environment variables."""
        return cls(
            provider=os.getenv("LLM_PROVIDER", "anthropic"),
            model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929"),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.2")),
            max_tokens=int(os.getenv("LLM_MAX_TOKENS", "8192")),
        )

@dataclass
class TaxonomyConfig:
    """Book taxonomy configuration."""
    enable_prefiltering: bool = True
    max_books: int = 10
    min_score: float = 0.3
    
@dataclass
class PathConfig:
    """File path configuration."""
    repo_root: Path
    data_dir: Path
    guidelines_dir: Path
    outputs_dir: Path
    logs_dir: Path
    
    @classmethod
    def from_repo_root(cls, repo_root: Path):
        """Initialize paths from repository root."""
        return cls(
            repo_root=repo_root,
            data_dir=repo_root / "data",
            guidelines_dir=repo_root / "guidelines",
            outputs_dir=repo_root / "outputs",
            logs_dir=repo_root / "logs",
        )

# Global config instances
llm_config = LLMConfig.from_env()
taxonomy_config = TaxonomyConfig()
```

---

### Phase 3: Architecture Improvements (Future)

#### 3.1 Separate Phase 1 and Phase 2 Classes

**Current**: Single `AnalysisOrchestrator` handles both phases (1,628 lines)

**Proposed**:

```
src/
  phases/
    __init__.py
    base.py           # Base phase class
    phase1.py         # ContentSelectionPhase
    phase2.py         # EnhancementPhase
    orchestrator.py   # Coordinator
```

#### 3.2 Add Caching Layer

**Problem**: Re-analyzing same content wastes API calls

**Solution**: Cache Phase 1 results

```python
# File: src/cache/phase1_cache.py

import hashlib
import json
from pathlib import Path
from typing import Optional, List, Dict

class Phase1Cache:
    """Cache Phase 1 content requests to avoid redundant API calls."""
    
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(exist_ok=True)
    
    def _hash_content(self, content: str) -> str:
        """Generate cache key from content."""
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def get(self, content: str) -> Optional[List[Dict]]:
        """Retrieve cached content requests."""
        cache_key = self._hash_content(content)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if cache_file.exists():
            return json.loads(cache_file.read_text())
        return None
    
    def set(self, content: str, requests: List[Dict]):
        """Cache content requests."""
        cache_key = self._hash_content(content)
        cache_file = self.cache_dir / f"{cache_key}.json"
        cache_file.write_text(json.dumps(requests, indent=2))
```

---

## III. IMPLEMENTATION TIMELINE

### Sprint 1 (Week 1): Critical Fixes
- [ ] Day 1-2: Enhanced JSON validation (`_validate_json_response`)
- [ ] Day 3: Finish reason enum and validation
- [ ] Day 4-5: Book taxonomy pre-filtering
- [ ] Day 6: Integration testing
- [ ] Day 7: Test on Chapter 1, compare output

**Deliverable**: Working system with 40% token savings, robust error handling

### Sprint 2 (Week 2): Code Quality
- [ ] Day 1-2: Extract prompt templates
- [ ] Day 3-4: Add unit tests (>80% coverage)
- [ ] Day 5: Configuration management
- [ ] Day 6-7: Documentation updates

**Deliverable**: Maintainable codebase, test suite

### Sprint 3 (Week 3): Architecture
- [ ] Day 1-3: Separate phase classes
- [ ] Day 4-5: Add caching layer
- [ ] Day 6-7: Performance testing

**Deliverable**: Scalable architecture, optimized performance

---

## IV. SUCCESS METRICS

### Functional
- ✅ Zero JSON parsing errors (currently: occasional truncation)
- ✅ 100% finish_reason validation coverage
- ✅ 40% token reduction via taxonomy pre-filtering
- ✅ Same output quality as current system

### Code Quality
- ✅ >80% test coverage
- ✅ <500 lines per file (currently: 1,628 in main file)
- ✅ All magic numbers in config
- ✅ Prompts in separate templates

### Performance
- ✅ <10 seconds per chapter (currently: ~15s)
- ✅ 50% reduction in failed API calls
- ✅ Cache hit rate >30% for re-runs

---

## V. RISK MITIGATION

### Regression Prevention
1. **Before ANY changes**: Run full Chapter 1 test, save output
2. **After EACH change**: Re-run Chapter 1, diff output
3. **Acceptance criteria**: Output must match exactly (character-for-character)

### Rollback Plan
- Git branch for each sprint: `refactor/sprint-1`, `refactor/sprint-2`, etc.
- Tag working states: `v1.0.0` (current), `v1.1.0` (sprint 1), etc.
- Keep original `integrate_llm_enhancements.py` as `integrate_llm_enhancements_v1.py` backup

### Testing Strategy
```bash
# Baseline (before changes)
python3 -m src.integrate_llm_enhancements > baseline_output.txt

# After refactoring
python3 -m src.integrate_llm_enhancements > refactored_output.txt

# Compare
diff baseline_output.txt refactored_output.txt
# Must be identical (or explicitly documented differences)
```

---

## VI. NEXT ACTIONS

**Immediate** (Start Sprint 1):

1. Create feature branch:
   ```bash
   cd /Users/kevintoles/POC/llm-document-enhancer
   git checkout -b refactor/sprint-1-critical-fixes
   ```

2. Run baseline test:
   ```bash
   python3 -m src.integrate_llm_enhancements > tests/baseline_chapter1.txt
   git add tests/baseline_chapter1.txt
   git commit -m "Add baseline output for regression testing"
   ```

3. Start with JSON validation:
   - Add `_validate_json_response()` to `src/llm_integration.py`
   - Add unit tests in `tests/test_llm_integration.py`
   - Run Chapter 1 test, verify identical output

4. Progress through Sprint 1 checklist

**Want me to start implementing Sprint 1?**
