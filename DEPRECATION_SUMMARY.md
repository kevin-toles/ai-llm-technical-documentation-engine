# Deprecation & Update Summary

**Date:** November 18, 2025
**Context:** Transition from Book Taxonomy System to Concept Taxonomy System

## TL;DR

**DO NOT DEPRECATE** the LLM enhancement scripts - they're actively used and already have graceful fallbacks for the old book_taxonomy system.

**ONLY DEPRECATE** the unused book_taxonomy.py file and old manual taxonomy JSONs.

---

## What's Being DEPRECATED ❌

### 1. Book Taxonomy Module (Not Used by UI)
- **File:** `workflows/taxonomy_setup/scripts/book_taxonomy.py` (506 lines)
- **Why:** Hardcoded Python book relationships, not data-driven
- **Impact:** Low - not imported by UI workflows
- **Status:** Can be moved to `Deprecated/` folder

### 2. Manual Taxonomy Files (Old Format)
- **Files:** 
  - `workflows/taxonomy_setup/output/pygame_taxonomy.json`
  - `workflows/taxonomy_setup/output/python_taxonomy.json`
- **Why:** Old "book organization" format with `"books": []` arrays
- **New Format:** Concept taxonomies with `"concepts": []` arrays
- **Status:** Keep for reference, mark as deprecated

---

## What's Being UPDATED (NOT Deprecated) ✅

### Active LLM Enhancement Scripts

These files are **ACTIVELY USED** and import book_taxonomy, but they already have graceful fallbacks:

#### 1. `workflows/07_llm_enhancement/scripts/interactive_llm_system_v3_hybrid_prompt.py`
```python
# Lines 45-52 - ALREADY HAS FALLBACK
try:
    from workflows.w01_taxonomy_setup.scripts import book_taxonomy
    TAXONOMY_AVAILABLE = True
except ImportError:
    TAXONOMY_AVAILABLE = False
    print("Warning: book_taxonomy.py not available - cascading logic disabled")
```

**Status:** ✅ Already gracefully degrades when book_taxonomy is unavailable
**Action:** None required - works with or without book_taxonomy.py

#### 2. `workflows/07_llm_enhancement/scripts/phases/content_selection.py`
```python
# Lines 39-44 - ALREADY HAS FALLBACK
try:
    from workflows.w01_taxonomy_setup.scripts import book_taxonomy
    TAXONOMY_AVAILABLE = True
except ImportError:
    TAXONOMY_AVAILABLE = False
    print("Warning: book_taxonomy.py not available - cascading logic disabled")
```

**Status:** ✅ Already gracefully degrades
**Action:** None required

#### 3. `workflows/07_llm_enhancement/scripts/phases/content_selection_impl.py`
```python
# Lines 33-42 - ALREADY HAS FALLBACK
try:
    from workflows.w01_taxonomy_setup.scripts.book_taxonomy import (...)
    TAXONOMY_AVAILABLE = True
except ImportError:
    TAXONOMY_AVAILABLE = False
```

**Status:** ✅ Already gracefully degrades
**Action:** None required

---

## Current System Architecture

### Old System (Optional Fallback)
```
book_taxonomy.py (hardcoded) 
  ↓
LLM scripts import for book scoring
  ↓
Graceful fallback if not available
```

### New System (Primary)
```
Tab 5 UI → generate_concept_taxonomy.py
  ↓
Outputs concept taxonomy JSON
  ↓
Tab 6/7 load JSON → Use concepts for cross-referencing
```

**Key Insight:** The old and new systems are **independent**. The LLM scripts can use book_taxonomy for advanced scoring, but they don't require it.

---

## What Tests Need Updating

### Tests That Reference book_taxonomy
These need to be updated to work with concept taxonomies instead:

1. **`tests/test_chapter1_comparison.py`**
   - Uses `_prefilter_books_by_taxonomy()` from interactive_llm_system
   - **Action:** Update to use concept taxonomy JSON or mock TAXONOMY_AVAILABLE=False

2. **`tests/test_sprint1_integration.py`**
   - Tests book_taxonomy scoring
   - **Action:** Update to test concept taxonomy loading instead

3. **`tests/unit/test_config.py`**
   - Tests `TaxonomyConfig` class (for book scoring)
   - **Action:** Decide if TaxonomyConfig is needed or should be removed

### Tests for Deprecated Code
1. **`tests/unit/test_generate_taxonomy_config.py`**
   - Tests the old taxonomy config generator
   - **Action:** Mark as deprecated or remove

---

## Configuration Review

### `config/settings.py` - `TaxonomyConfig` Class

```python
class TaxonomyConfig:
    """Book taxonomy settings."""
    min_relevance: float = 0.3  # Book relevance scoring
    max_books: int = 10         # Max books to send to LLM
    cascade_depth: int = 1      # Book cascading depth
```

**Question:** Is this still needed?
- Used by old book_taxonomy scoring system
- NOT used by new concept taxonomy system
- NOT used by UI workflows

**Options:**
1. Keep for backward compatibility (if someone uses book_taxonomy.py directly)
2. Repurpose for concept taxonomy settings
3. Deprecate and remove in future release

**Recommendation:** Keep for now with deprecation notice

---

## Migration Path

### For Users of book_taxonomy.py (if any exist)

**Old Code:**
```python
from workflows.taxonomy_setup.scripts.book_taxonomy import score_books_for_concepts

scores = score_books_for_concepts(concepts=['decorator', 'async'])
# Returns: [('fluent_python', 0.85), ('python_distilled', 0.72), ...]
```

**New Code:**
```python
import json
from pathlib import Path

# Load concept taxonomy generated by Tab 5 UI
tax_path = Path('workflows/taxonomy_setup/output/my_taxonomy.json')
with open(tax_path) as f:
    taxonomy = json.load(f)

# Get all concepts from all tiers
all_concepts = []
for tier in taxonomy['tiers'].values():
    all_concepts.extend(tier['concepts'])

# Use concepts for cross-referencing
relevant_concepts = [c for c in all_concepts if c in chapter_text.lower()]
```

---

## Summary

### ❌ DEPRECATE (Move to Deprecated/)
- `workflows/taxonomy_setup/scripts/book_taxonomy.py`
- Old manual taxonomy JSONs (keep for reference)

### ✅ UPDATE (Already Done!)
- LLM enhancement scripts already have fallback logic
- No changes needed - they work with or without book_taxonomy.py

### 🔄 TEST UPDATES NEEDED
- Update tests to use concept taxonomies
- Mock TAXONOMY_AVAILABLE=False in tests
- Remove or mark deprecated: test_generate_taxonomy_config.py

### ⚠️ DECISION NEEDED
- Keep or remove `TaxonomyConfig` class in settings.py?
- Recommendation: Keep with deprecation notice for backward compatibility

---

## Timeline

- ✅ **Completed:** Concept taxonomy system (Tab 5 → generate_concept_taxonomy.py)
- ✅ **Completed:** LLM scripts already have fallback logic
- 🔲 **Next:** Update tests to use new system
- 🔲 **Next:** Move book_taxonomy.py to Deprecated/ folder
- 🔲 **Future:** Remove deprecated code in next major version

---

## Key Takeaway

**The LLM enhancement scripts are NOT tightly coupled to book_taxonomy.** They import it for optional advanced features (book scoring, cascading relationships), but they already gracefully degrade when it's not available.

The confusion arose from:
1. Seeing the imports and assuming tight coupling
2. Not recognizing the `TAXONOMY_AVAILABLE` fallback pattern
3. Conflating "imports X" with "requires X"

**Action Required:** Minimal
- Move book_taxonomy.py to Deprecated/ (optional)
- Update tests to use concept taxonomies
- Document that book_taxonomy is deprecated but still available for backward compatibility
