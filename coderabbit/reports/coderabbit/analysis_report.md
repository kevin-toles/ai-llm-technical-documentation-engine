# CodeRabbit Local Analysis Report
**Generated**: 2025-11-26 10:13:48
**Total Issues**: 120

## Summary
| Severity | Count |
|----------|-------|
| 🚨 Critical | 0 |
| 🔴 High | 0 |
| 🟡 Medium | 118 |
| 🔵 Low | 2 |
| ℹ️ Info | 0 |

## Recommendations
- 🔧 Consider refactoring to reduce medium-severity issues

## 🟡 Medium Issues (118)

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
- **Line**: 148
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Need type annotation for "concept_freq"  [var-annotated]

### Issue 6
- **File**: `taxonomy_setup/scripts/generate_concept_taxonomy.py`
- **Line**: 189
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Need type annotation for "categorized"  [var-annotated]

### Issue 7
- **File**: `taxonomy_setup/scripts/generate_concept_taxonomy.py`
- **Line**: 196
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Need type annotation for "all_concepts" (hint: "all_concepts: set[<type>] = ...")  [var-annotated]

### Issue 8
- **File**: `taxonomy_setup/scripts/generate_concept_taxonomy.py`
- **Line**: 252
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Need type annotation for "tier_freq"  [var-annotated]

### Issue 9
- **File**: `taxonomy_setup/scripts/generate_concept_taxonomy.py`
- **Line**: 274
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Need type annotation for "taxonomy"  [var-annotated]

### Issue 10
- **File**: `taxonomy_setup/scripts/generate_concept_taxonomy.py`
- **Line**: 296
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Incompatible types in assignment (expression has type "list[str]", variable has type "set[str]")  [assignment]

### Issue 11
- **File**: `pdf_to_json/scripts/ml_chapter_detector.py`
- **Line**: 39
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Need type annotation for "page_keywords" (hint: "page_keywords: list[<type>] = ...")  [var-annotated]

### Issue 12
- **File**: `metadata_enrichment/scripts/enrich_metadata_per_book.py`
- **Line**: 46
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Incompatible types in assignment (expression has type "None", variable has type "StatisticalExtractor")  [assignment]

### Issue 13
- **File**: `metadata_enrichment/scripts/enrich_metadata_per_book.py`
- **Line**: 118
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Unsupported target for indexed assignment ("object")  [index]

### Issue 14
- **File**: `metadata_enrichment/scripts/enrich_metadata_per_book.py`
- **Line**: 119
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Unsupported operand types for + ("object" and "int")  [operator]

### Issue 15
- **File**: `metadata_enrichment/scripts/chapter_metadata_manager.py`
- **Line**: 29
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Incompatible types in assignment (expression has type "None", variable has type "list[str]")  [assignment]

### Issue 16
- **File**: `metadata_enrichment/scripts/chapter_metadata_manager.py`
- **Line**: 54
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Incompatible types in assignment (expression has type "Path", variable has type "str | None")  [assignment]

### Issue 17
- **File**: `metadata_enrichment/scripts/chapter_metadata_manager.py`
- **Line**: 56
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Incompatible types in assignment (expression has type "Path", variable has type "str | None")  [assignment]

### Issue 18
- **File**: `metadata_enrichment/scripts/chapter_metadata_manager.py`
- **Line**: 58
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Unsupported left operand type for / ("str")  [operator]

### Issue 19
- **File**: `metadata_enrichment/scripts/chapter_metadata_manager.py`
- **Line**: 58
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Unsupported left operand type for / ("None")  [operator]

### Issue 20
- **File**: `metadata_enrichment/scripts/chapter_metadata_manager.py`
- **Line**: 58
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Left operand is of type "str | None"

... and 98 more issues

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
