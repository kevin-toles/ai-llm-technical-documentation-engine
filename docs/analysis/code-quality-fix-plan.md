# Code Quality Fix Plan - Ruff Issues Resolution

**Date**: November 14, 2025  
**Sprint**: Post-Sprint 4 Quality Gate  
**Workflow**: Full TDD (RED → GREEN → REFACTOR)

---

## Step 1: BOOK_TAXONOMY_MATRIX Analysis

### Task Context
Resolve 19 Ruff static analysis issues across codebase:
- **F401** (9 issues): Unused imports
- **F821** (8 issues): Undefined names
- **F811** (1 issue): Redefined function
- **F841** (1 issue): Unused variable

### Relevant Books Identified

**Tier 3: Engineering Practices** (Primary)
1. **Fluent Python 2nd** (Weight: 1.2) - Pythonic patterns, imports, type hints
   - Keywords: pythonic, idiomatic, type hint, annotation, import, module
2. **Python Distilled** (Weight: 1.1) - Best practices, core concepts
   - Keywords: import, module, package, exception, type, reference
3. **Python Cookbook 3rd** (Weight: 1.0) - Practical solutions, idioms
   - Keywords: module, metaprogramming, best practice, idiom, technique

**Not Applicable**:
- Tier 1/2 books (microservices, architecture) - not relevant to import/naming fixes
- Data analysis books - not relevant to code quality

---

## Step 2: Guideline Cross-Referencing

### PYTHON_GUIDELINES Sections

**Imports** (from Fluent Python 2nd, Python Distilled):
- Use explicit imports, avoid wildcard imports
- Remove unused imports
- Type hints for function signatures (PEP 484, 526)
- Import organization: stdlib → third-party → local

**Naming** (from PEP 8, Python Distilled):
- Variables must be defined before use
- Avoid shadowing built-in names
- Functions should have single responsibility (no redefinition)

**Code Quality** (from Python Cookbook 3rd):
- Every import should be used
- Every variable should be used
- No dead code
- Type annotations for clarity

### ARCHITECTURE_GUIDELINES Sections

Not directly applicable - these are implementation-level fixes, not architectural patterns.

---

## Step 3: Conflict Identification

### Analysis
No conflicts detected. All issues are clear violations of Python best practices:
1. **Unused imports** → Remove them (Fluent Python Ch. 10, Python Distilled Ch. 8)
2. **Undefined names** → Define variables or fix typos (Python Distilled Ch. 2)
3. **Redefined function** → Remove duplicate or rename (Python Cookbook Recipe 9.5)
4. **Unused variable** → Remove assignment or use it (PEP 8)

### Resolution Priority
Follow **PYTHON_GUIDELINES** (priority #4 in document hierarchy) for all fixes.

---

## Issue Categorization

### Category 1: Unused Imports (F401) - 9 issues
**Files**:
1. `src/interactive_llm_system_v3_hybrid_prompt.py:42` - `.book_taxonomy.score_books_for_concepts`
2. `tests/test_sprint3_constants.py:28` - `pytest`
3. `tests/test_sprint3_metadata_builders.py:31` - `pytest`
4. `tests_unit/test_pipeline_adapters.py:16` - `Mock`
5. `tests_unit/test_pipeline_adapters.py:16` - `MagicMock`
6. `tests_unit/test_pipeline_orchestrator.py:11` - `json`
7. `tests_unit/test_pipeline_orchestrator.py:13` - `Path`
8. `tests_unit/test_pipeline_orchestrator.py:14` - `patch`
9. `tests_unit/test_pipeline_orchestrator.py:14` - `MagicMock`

**TDD Approach**:
- RED: Verify import is unused (tests still pass without it)
- GREEN: Remove the import
- REFACTOR: Run tests, verify no regression

### Category 2: Undefined Names (F821) - 8 issues
**Files**:
1. `coderabbit/scripts/local_coderabbit.py:134` - `Optional`
2. `src/integrate_llm_enhancements.py:697` - `header`
3. `src/integrate_llm_enhancements.py:774` - `header`
4. `src/interactive_llm_system_v3_hybrid_prompt.py:1347` - `PYTHON_DISTILLED`
5. `src/interactive_llm_system_v3_hybrid_prompt.py:1373` - `PYTHON_ESSENTIAL_REF`
6. `src/interactive_llm_system_v3_hybrid_prompt.py:1373` - `FLUENT_PYTHON`
7. `src/interactive_llm_system_v3_hybrid_prompt.py:1373` - `PYTHON_DATA_ANALYSIS`
8. `src/interactive_llm_system_v3_hybrid_prompt.py:1373` - `PYTHON_DISTILLED` (duplicate line)

**TDD Approach**:
- RED: Write test that triggers the undefined name error
- GREEN: Define the variable/import the type
- REFACTOR: Verify proper scoping and usage

### Category 3: Redefined Function (F811) - 1 issue
**File**:
1. `src/integrate_llm_enhancements.py:288` - `find_relevant_sections` redefined from line 164

**TDD Approach**:
- RED: Verify both definitions exist
- GREEN: Remove duplicate or rename to distinct function
- REFACTOR: Update all callers if needed

### Category 4: Unused Variable (F841) - 1 issue
**File**:
1. `src/pipeline/convert_pdf_to_json.py:23` - `pix` assigned but never used

**TDD Approach**:
- RED: Verify variable is assigned but not used
- GREEN: Either use the variable or remove assignment
- REFACTOR: Ensure OCR logic is still correct

---

## TDD Implementation Order

### Phase 1: Quick Wins - Unused Imports (F401) - 30 minutes
1. Test files (safe to remove)
2. Source files (verify usage first)

### Phase 2: Undefined Names (F821) - 45 minutes
1. Type hint imports (Optional)
2. Undefined variables (header, constants)

### Phase 3: Code Structure (F811, F841) - 30 minutes
1. Function redefinition
2. Unused variable

### Phase 4: Continuous Quality Gate
After each fix:
1. ✅ Run Ruff
2. ✅ Run tests (52/52 passing)
3. ✅ Verify ZERO REGRESSIONS

---

## Success Criteria

✅ All 19 Ruff issues resolved  
✅ 52/52 tests still passing  
✅ No new issues introduced  
✅ Code follows PYTHON_GUIDELINES  
✅ All changes documented with textbook references

---

## Textbook References Applied

- **Fluent Python 2nd**: Ch. 10 (Imports and Packages)
- **Python Distilled**: Ch. 2 (Types and Objects), Ch. 8 (Modules and Packages)
- **Python Cookbook 3rd**: Recipe 9.5 (Defining decorators with optional arguments)
- **PEP 8**: Style Guide for Python Code (imports, naming)
