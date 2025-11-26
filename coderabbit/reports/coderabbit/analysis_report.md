# CodeRabbit Local Analysis Report
**Generated**: 2025-11-26 11:25:09
**Total Issues**: 68

## Summary
| Severity | Count |
|----------|-------|
| 🚨 Critical | 0 |
| 🔴 High | 0 |
| 🟡 Medium | 66 |
| 🔵 Low | 2 |
| ℹ️ Info | 0 |

## Recommendations
- 🔧 Consider refactoring to reduce medium-severity issues

## 🟡 Medium Issues (66)

### Issue 1
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/taxonomy_setup/scripts/generate_concept_taxonomy.py`
- **Line**: 26
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: F401
- **Message**: `collections.defaultdict` imported but unused

### Issue 2
- **File**: `shared/phases/orchestrator.py`
- **Line**: 15
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Cannot find implementation or library stub for module named "workflows.shared.interactive_llm_system_v3_hybrid_prompt"  [import-not-found]

### Issue 3
- **File**: `shared/phases/orchestrator.py`
- **Line**: 37
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Cannot find implementation or library stub for module named "interactive_llm_system_v3_hybrid_prompt"  [import-not-found]

### Issue 4
- **File**: `metadata_extraction/scripts/strategies/regex_pattern_strategy.py`
- **Line**: 130
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Need type annotation for "seen_numbers" (hint: "seen_numbers: set[<type>] = ...")  [var-annotated]

### Issue 5
- **File**: `taxonomy_setup/scripts/generate_concept_taxonomy.py`
- **Line**: 296
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Incompatible types in assignment (expression has type "list[str]", variable has type "set[str]")  [assignment]

### Issue 6
- **File**: `pdf_to_json/scripts/ml_chapter_detector.py`
- **Line**: 39
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Need type annotation for "page_keywords" (hint: "page_keywords: list[<type>] = ...")  [var-annotated]

### Issue 7
- **File**: `metadata_enrichment/scripts/enrich_metadata_per_book.py`
- **Line**: 46
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Incompatible types in assignment (expression has type "None", variable has type "StatisticalExtractor")  [assignment]

### Issue 8
- **File**: `metadata_enrichment/scripts/enrich_metadata_per_book.py`
- **Line**: 118
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Unsupported target for indexed assignment ("object")  [index]

### Issue 9
- **File**: `metadata_enrichment/scripts/enrich_metadata_per_book.py`
- **Line**: 119
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Unsupported operand types for + ("object" and "int")  [operator]

### Issue 10
- **File**: `base_guideline_generation/scripts/chapter_generator_all_text.py`
- **Line**: 137
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Incompatible types in assignment (expression has type "dict[str, str] | dict[str, str | None]", variable has type "dict[str, str | None]")  [assignment]

### Issue 11
- **File**: `base_guideline_generation/scripts/chapter_generator_all_text.py`
- **Line**: 1306
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Name "section" already defined on line 1287  [no-redef]

### Issue 12
- **File**: `base_guideline_generation/scripts/chapter_generator_all_text.py`
- **Line**: 1307
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: "str" has no attribute "append"  [attr-defined]

### Issue 13
- **File**: `base_guideline_generation/scripts/chapter_generator_all_text.py`
- **Line**: 1308
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: "str" has no attribute "append"  [attr-defined]

### Issue 14
- **File**: `base_guideline_generation/scripts/chapter_generator_all_text.py`
- **Line**: 1313
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: "str" has no attribute "append"  [attr-defined]

### Issue 15
- **File**: `base_guideline_generation/scripts/chapter_generator_all_text.py`
- **Line**: 1314
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: "str" has no attribute "append"  [attr-defined]

### Issue 16
- **File**: `base_guideline_generation/scripts/chapter_generator_all_text.py`
- **Line**: 1315
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: "str" has no attribute "append"  [attr-defined]

### Issue 17
- **File**: `base_guideline_generation/scripts/chapter_generator_all_text.py`
- **Line**: 1316
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: "str" has no attribute "append"  [attr-defined]

### Issue 18
- **File**: `base_guideline_generation/scripts/chapter_generator_all_text.py`
- **Line**: 1317
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: "str" has no attribute "append"  [attr-defined]

### Issue 19
- **File**: `shared/retry.py`
- **Line**: 173
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Argument 2 to "RetryExhaustedError" has incompatible type "Exception | None"; expected "Exception"  [arg-type]

### Issue 20
- **File**: `shared/retry.py`
- **Line**: 228
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Argument 2 to "RetryExhaustedError" has incompatible type "Exception | None"; expected "Exception"  [arg-type]

... and 46 more issues

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
