# CodeRabbit Local Analysis Report
**Generated**: 2025-11-26 12:52:34
**Total Issues**: 6

## Summary
| Severity | Count |
|----------|-------|
| 🚨 Critical | 0 |
| 🔴 High | 0 |
| 🟡 Medium | 4 |
| 🔵 Low | 2 |
| ℹ️ Info | 0 |

## 🟡 Medium Issues (4)

### Issue 1
- **File**: `shared/phases/orchestrator.py`
- **Line**: 37
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Cannot find implementation or library stub for module named "interactive_llm_system_v3_hybrid_prompt"  [import-not-found]

### Issue 2
- **File**: `taxonomy_setup/scripts/generate_concept_taxonomy.py`
- **Line**: 296
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Incompatible types in assignment (expression has type "list[str]", variable has type "set[str]")  [assignment]

### Issue 3
- **File**: `llm_enhancement/scripts/phases/annotation_service.py`
- **Line**: 34
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Cannot find implementation or library stub for module named "interactive_llm_system_v3_hybrid_prompt"  [import-not-found]

### Issue 4
- **File**: `llm_enhancement/scripts/phases/annotation_service.py`
- **Line**: 34
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports

## 🔵 Low Issues (2)

### Issue 1
- **File**: `./metadata_extraction/scripts/generate_metadata_universal.py`
- **Line**: 252
- **Tool**: bandit
- **Type**: security
- **Rule**: B110
- **Message**: Try, Except, Pass detected.

### Issue 2
- **File**: `./metadata_extraction/scripts/strategies/yake_validation_strategy.py`
- **Line**: 74
- **Tool**: bandit
- **Type**: security
- **Rule**: B112
- **Message**: Try, Except, Continue detected.
