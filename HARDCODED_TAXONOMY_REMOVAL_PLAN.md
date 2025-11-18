# Hardcoded Taxonomy Removal - Consolidated Refactoring Plan

**Date:** November 18, 2025  
**Objective:** Remove ALL hardcoded book_taxonomy references and dead code

---

## Executive Summary

**Problem:** System has TWO taxonomy systems:
1. ✅ **NEW**: Concept taxonomy (Tab 5 UI → `generate_concept_taxonomy.py`)
2. ❌ **OLD**: Hardcoded book taxonomy (`book_taxonomy.py` with `ALL_BOOKS`, `BOOK_REGISTRY`)

**Solution:** Remove old system entirely - it's either dead code or can be deleted without breaking UI workflows.

---

## Phase 1: Deprecate Core File (SAFE)

### File to Move to Deprecated/

**`workflows/taxonomy_setup/scripts/book_taxonomy.py`** (506 lines)
- **Status:** NOT used by UI workflows
- **Contains:** Hardcoded book relationships, scoring functions
- **Action:** Move to `workflows/taxonomy_setup/Deprecated/book_taxonomy.py.deprecated`

```bash
mkdir -p workflows/taxonomy_setup/Deprecated
mv workflows/taxonomy_setup/scripts/book_taxonomy.py \
   workflows/taxonomy_setup/Deprecated/book_taxonomy.py.deprecated
```

---

## Phase 2: Remove Dead Code from Active Files

### File 1: `workflows/07_llm_enhancement/scripts/interactive_llm_system_v3_hybrid_prompt.py`

**Dead Code to DELETE:**

#### Section 1: Import block (Lines 45-52)
```python
# REMOVE THIS:
try:
    from workflows.w01_taxonomy_setup.scripts import book_taxonomy
    TAXONOMY_AVAILABLE = True
except ImportError:
    TAXONOMY_AVAILABLE = False
    print("Warning: book_taxonomy.py not available - cascading logic disabled")
```

#### Section 2: Function `_prefilter_books_by_taxonomy()` (Lines 159-220)
```python
# DELETE ENTIRE FUNCTION - NEVER CALLED
def _prefilter_books_by_taxonomy(
    orchestrator,
    chapter_full_text: str,
    max_books: int = 10
) -> List[str]:
    # ... 60+ lines ...
```
**Reason:** Function uses hardcoded `ALL_BOOKS` and `score_books_for_concepts()`

#### Section 3: Function `analyze_chapter_with_all_books()` (Lines ~365-~600)
```python
# DELETE ENTIRE FUNCTION - NEVER CALLED
def analyze_chapter_with_all_books(
    self,
    chapter_num: int,
    chapter_title: str,
    chapter_full_text: str
) -> LLMMetadataResponse:
    # ... calls _prefilter_books_by_taxonomy() at line 378 ...
```
**Reason:** This function is dead code - grep shows NO callers

#### Section 4: Method `_get_recommended_books_from_taxonomy()` (Lines ~1260-~1320)
```python
# DELETE OR UPDATE THIS METHOD
def _get_recommended_books_from_taxonomy(
    self,
    concepts: List[str],
    concept_mapping: Dict[str, List[str]]
) -> List[str]:
    try:
        from workflows.w01_taxonomy_setup.scripts.book_taxonomy import get_recommended_books
        # ... uses hardcoded book_taxonomy ...
    except ImportError:
        return list(concept_mapping.keys())[:settings.taxonomy.max_books]
```
**Decision needed:** Is this method called? If yes, update to use concept taxonomy JSON. If no, delete.

---

### File 2: `workflows/07_llm_enhancement/scripts/phases/content_selection.py`

**Lines 39-44 - Import block:**
```python
# REMOVE THIS:
try:
    from workflows.w01_taxonomy_setup.scripts import book_taxonomy  # noqa: F401
    TAXONOMY_AVAILABLE = True
except ImportError:
    TAXONOMY_AVAILABLE = False
    print("Warning: book_taxonomy.py not available - cascading logic disabled")
```

**Check:** Does this file have any functions that USE `book_taxonomy`? If not, just remove the import.

---

### File 3: `workflows/07_llm_enhancement/scripts/phases/content_selection_impl.py`

**Lines 33-42 - Import block:**
```python
# REMOVE THIS:
try:
    from workflows.taxonomy_setup.scripts.book_taxonomy import (
        get_recommended_books,
        score_books_for_concepts,
        BOOK_REGISTRY,
        get_cascading_books
    )
    TAXONOMY_AVAILABLE = True
except ImportError:
    TAXONOMY_AVAILABLE = False
```

**Functions that use book_taxonomy:**
- Line 155: `scored_books = score_books_for_concepts(concept_set)`
- Line 178: `if not TAXONOMY_AVAILABLE or book_file_name not in BOOK_REGISTRY:`
- Line 181: `book_role = BOOK_REGISTRY[book_file_name]`
- Line 214: `'tier': BOOK_REGISTRY[book.file_name].tier.value`
- Line 415: `from book_taxonomy import get_recommended_books`
- Line 437: `from book_taxonomy import BOOK_REGISTRY`

**Action:** Need to check if these methods are called by UI workflows. If yes, update to use concept taxonomy JSON. If no, delete.

---

### File 4: `workflows/base_guideline_generation/scripts/chapter_generator_all_text.py`

**Lines 237-248 - Hardcoded book list:**
```python
# THIS IS DIFFERENT - NOT book_taxonomy.py
# This is a simple list for companion book loading
ALL_BOOKS = [
    "Learning Python Ed6",
    "Architecture Patterns with Python",
    # ...
]
```

**Status:** This is OK - it's just a list of book names for loading companions
**Action:** KEEP THIS - it's not the hardcoded taxonomy system

---

## Phase 3: Delete Supporting Files

### File 1: `workflows/01_taxonomy_setup/scripts/generate_taxonomy_config.py`
- **Purpose:** Generates config FROM book_taxonomy.py
- **Status:** Obsolete - depends on book_taxonomy.py
- **Action:** Move to Deprecated/

### File 2: `workflows/taxonomy_setup/scripts/generate_taxonomy_config.py`
- **Same as above** (duplicate file in different location)
- **Action:** Move to Deprecated/

---

## Phase 4: Update Tests

### Tests to Update or Delete:

**1. `tests/test_chapter1_comparison.py`**
- Line 54: `from src.interactive_llm_system_v3_hybrid_prompt import _prefilter_books_by_taxonomy`
- **Action:** Delete or update to test concept taxonomy loading

**2. `tests/test_sprint1_integration.py`**
- Line 24: `_prefilter_books_by_taxonomy`
- Lines 93, 118: Uses book_taxonomy scoring
- **Action:** Update to test concept taxonomy or mark as deprecated

**3. `tests/unit/test_generate_taxonomy_config.py`**
- **Purpose:** Tests old taxonomy config generator
- **Action:** DELETE entire file (tests obsolete code)

**4. `tests/unit/test_config.py`**
- Tests `TaxonomyConfig` class (for book scoring)
- **Action:** Keep but mark `TaxonomyConfig` tests as deprecated

---

## Phase 5: Configuration Review

### `config/settings.py` - `TaxonomyConfig` Class

```python
class TaxonomyConfig:
    """Book taxonomy settings."""
    min_relevance: float = 0.3
    max_books: int = 10
    cascade_depth: int = 1
    enable_prefilter: bool = True
```

**Decision Options:**
1. **Delete** - Not used by new system (RECOMMENDED)
2. **Deprecate** - Keep with warning comment
3. **Repurpose** - Use for concept taxonomy settings

**Recommendation:** DELETE - UI workflows don't use these settings

---

## Phase 6: Documentation Cleanup

### Files Referencing book_taxonomy (documentation only):

- `BOOK_TAXONOMY_MATRIX.md` - Keep as reference
- `REFACTORING_PLAN.md` - Add deprecation notice
- `MIGRATION_PLAN.md` - Add deprecation notice
- `TECHNICAL_ASSESSMENT.md` - Add deprecation notice
- `README.md` - Remove book_taxonomy instructions

---

## Implementation Checklist

### Phase 1: Safe Moves ✅
- [ ] Create `workflows/taxonomy_setup/Deprecated/` folder
- [ ] Move `book_taxonomy.py` to Deprecated/
- [ ] Move `generate_taxonomy_config.py` files to Deprecated/
- [ ] Add DEPRECATION_NOTICE.md in Deprecated folder

### Phase 2: Code Analysis 🔍
- [ ] Check if `_get_recommended_books_from_taxonomy()` is called
- [ ] Check if content_selection_impl.py methods are called by UI
- [ ] Identify ALL dead code functions

### Phase 3: Delete Dead Code 🗑️
- [ ] Delete `_prefilter_books_by_taxonomy()` from interactive_llm_system_v3_hybrid_prompt.py
- [ ] Delete `analyze_chapter_with_all_books()` from same file
- [ ] Delete unused imports (book_taxonomy lines)
- [ ] Delete or update content_selection_impl.py functions

### Phase 4: Update Tests 🧪
- [ ] Delete `test_generate_taxonomy_config.py`
- [ ] Update or delete `test_chapter1_comparison.py`
- [ ] Update or delete `test_sprint1_integration.py`
- [ ] Mark TaxonomyConfig tests as deprecated

### Phase 5: Configuration ⚙️
- [ ] Delete `TaxonomyConfig` class from settings.py
- [ ] Remove TaxonomyConfig tests
- [ ] Update __init__.py exports

### Phase 6: Documentation 📝
- [ ] Add deprecation notices to docs
- [ ] Update README.md
- [ ] Create migration guide for any external users

### Phase 7: Testing ✅
- [ ] Run UI - verify Tab 5 works
- [ ] Run UI - verify Tab 6 works
- [ ] Run UI - verify Tab 7 works
- [ ] Run all remaining tests
- [ ] Check for any import errors

### Phase 8: Commit 🚀
- [ ] Git add all changes
- [ ] Commit with message: "refactor: Remove hardcoded book_taxonomy system"
- [ ] Push to branch

---

## Validation Commands

```bash
# Check for remaining book_taxonomy references
grep -r "book_taxonomy" workflows/ ui/ --exclude-dir=Deprecated

# Check for ALL_BOOKS (from book_taxonomy, not chapter_generator)
grep -r "from.*book_taxonomy import.*ALL_BOOKS" workflows/

# Check for BOOK_REGISTRY
grep -r "BOOK_REGISTRY" workflows/ --exclude-dir=Deprecated

# Check for score_books_for_concepts
grep -r "score_books_for_concepts" workflows/ --exclude-dir=Deprecated

# Run tests
pytest tests/ -v

# Test UI
cd ui && python3 main.py
```

---

## Risk Assessment

### LOW RISK ✅
- Moving book_taxonomy.py to Deprecated/ (has try/except fallbacks)
- Deleting `_prefilter_books_by_taxonomy()` (never called)
- Deleting `analyze_chapter_with_all_books()` (never called)
- Deleting test_generate_taxonomy_config.py (tests obsolete code)

### MEDIUM RISK ⚠️
- Deleting TaxonomyConfig (need to verify no external dependencies)
- Updating content_selection_impl.py (need to check callers first)

### HIGH RISK 🚨
- **NONE** - UI workflows don't use book_taxonomy.py

---

## Rollback Plan

If something breaks:

```bash
# Restore book_taxonomy.py
cp workflows/taxonomy_setup/Deprecated/book_taxonomy.py.deprecated \
   workflows/taxonomy_setup/scripts/book_taxonomy.py

# Restore from git
git checkout workflows/07_llm_enhancement/scripts/interactive_llm_system_v3_hybrid_prompt.py
git checkout config/settings.py
```

---

## Success Criteria

✅ **All hardcoded book_taxonomy references removed**
✅ **UI workflows (Tabs 5, 6, 7) still work**
✅ **All tests pass**
✅ **No import errors**
✅ **Concept taxonomy system is the single source of truth**

---

## Notes

- The `ALL_BOOKS` list in `chapter_generator_all_text.py` is DIFFERENT - it's just a simple list for loading companions, not the hardcoded taxonomy system. KEEP IT.
- Some "all_books" variables are from `_metadata_service._repo.get_all()` - these are FINE, they're getting books from the metadata service, not hardcoded taxonomy.
- Focus on removing imports from `book_taxonomy.py` and functions like `score_books_for_concepts()`, `BOOK_REGISTRY`, etc.
