# CodeRabbit Local Analysis Report
**Generated**: 2025-11-26 12:12:20
**Total Issues**: 39

## Summary
| Severity | Count |
|----------|-------|
| 🚨 Critical | 0 |
| 🔴 High | 0 |
| 🟡 Medium | 37 |
| 🔵 Low | 2 |
| ℹ️ Info | 0 |

## Recommendations
- 🔧 Consider refactoring to reduce medium-severity issues

## 🟡 Medium Issues (37)

### Issue 1
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/llm_enhancement/scripts/models/analysis_models.py`
- **Line**: 290
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: F821
- **Message**: Undefined name `Optional`

### Issue 2
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/taxonomy_setup/scripts/generate_concept_taxonomy.py`
- **Line**: 26
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: F401
- **Message**: `collections.defaultdict` imported but unused

### Issue 3
- **File**: `shared/phases/orchestrator.py`
- **Line**: 15
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Cannot find implementation or library stub for module named "workflows.shared.interactive_llm_system_v3_hybrid_prompt"  [import-not-found]

### Issue 4
- **File**: `shared/phases/orchestrator.py`
- **Line**: 37
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Cannot find implementation or library stub for module named "interactive_llm_system_v3_hybrid_prompt"  [import-not-found]

### Issue 5
- **File**: `metadata_extraction/scripts/strategies/regex_pattern_strategy.py`
- **Line**: 130
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Need type annotation for "seen_numbers" (hint: "seen_numbers: set[<type>] = ...")  [var-annotated]

### Issue 6
- **File**: `taxonomy_setup/scripts/generate_concept_taxonomy.py`
- **Line**: 296
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Incompatible types in assignment (expression has type "list[str]", variable has type "set[str]")  [assignment]

### Issue 7
- **File**: `pdf_to_json/scripts/ml_chapter_detector.py`
- **Line**: 39
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Need type annotation for "page_keywords" (hint: "page_keywords: list[<type>] = ...")  [var-annotated]

### Issue 8
- **File**: `metadata_enrichment/scripts/enrich_metadata_per_book.py`
- **Line**: 46
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Incompatible types in assignment (expression has type "None", variable has type "StatisticalExtractor")  [assignment]

### Issue 9
- **File**: `metadata_enrichment/scripts/enrich_metadata_per_book.py`
- **Line**: 118
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Unsupported target for indexed assignment ("object")  [index]

### Issue 10
- **File**: `metadata_enrichment/scripts/enrich_metadata_per_book.py`
- **Line**: 119
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Unsupported operand types for + ("object" and "int")  [operator]

### Issue 11
- **File**: `shared/retry.py`
- **Line**: 173
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Argument 2 to "RetryExhaustedError" has incompatible type "Exception | None"; expected "Exception"  [arg-type]

### Issue 12
- **File**: `shared/retry.py`
- **Line**: 228
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Argument 2 to "RetryExhaustedError" has incompatible type "Exception | None"; expected "Exception"  [arg-type]

### Issue 13
- **File**: `shared/loaders/content_loaders.py`
- **Line**: 279
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Need type annotation for "excerpts" (hint: "excerpts: list[<type>] = ...")  [var-annotated]

### Issue 14
- **File**: `llm_enhancement/scripts/models/analysis_models.py`
- **Line**: 290
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Name "Optional" is not defined  [name-defined]

### Issue 15
- **File**: `llm_enhancement/scripts/models/analysis_models.py`
- **Line**: 290
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Did you forget to import it from "typing"? (Suggestion: "from typing import Optional")

### Issue 16
- **File**: `llm_enhancement/scripts/builders/metadata_builder.py`
- **Line**: 34
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: By default the bodies of untyped functions are not checked, consider using --check-untyped-defs  [annotation-unchecked]

### Issue 17
- **File**: `metadata_extraction/scripts/generate_metadata_universal.py`
- **Line**: 411
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Need type annotation for "chapters" (hint: "chapters: list[<type>] = ...")  [var-annotated]

### Issue 18
- **File**: `metadata_extraction/scripts/generate_metadata_universal.py`
- **Line**: 419
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Incompatible types in assignment (expression has type "int", variable has type "str")  [assignment]

### Issue 19
- **File**: `metadata_extraction/scripts/generate_metadata_universal.py`
- **Line**: 433
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Incompatible return value type (got "list[tuple[str, str, int, int]]", expected "list[tuple[int, str, int, int]]")  [return-value]

### Issue 20
- **File**: `metadata_enrichment/scripts/generate_chapter_metadata.py`
- **Line**: 103
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Need type annotation for "CONCEPT_PATTERNS" (hint: "CONCEPT_PATTERNS: list[<type>] = ...")  [var-annotated]

... and 17 more issues

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
