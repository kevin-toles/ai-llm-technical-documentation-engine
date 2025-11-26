# CodeRabbit Local Analysis Report
**Generated**: 2025-11-26 00:27:46
**Total Issues**: 42

## Summary
| Severity | Count |
|----------|-------|
| 🚨 Critical | 0 |
| 🔴 High | 1 |
| 🟡 Medium | 38 |
| 🔵 Low | 3 |
| ℹ️ Info | 0 |

## Recommendations
- ⚡ Fix high-severity issues before deployment
- 🔧 Consider refactoring to reduce medium-severity issues

## 🔴 High Issues (1)

### Issue 1
- **File**: `pdf_to_json/scripts/ml_chapter_detector.py`
- **Line**: 199
- **Tool**: radon
- **Type**: complexity
- **Rule**: complexity
- **Message**: High complexity: 17 (threshold: 10)

## 🟡 Medium Issues (38)

### Issue 1
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_enrichment/scripts/enrich_metadata_per_book.py`
- **Line**: 28
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: F401
- **Message**: `typing.Optional` imported but unused

### Issue 2
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_enrichment/scripts/enrich_metadata_per_book.py`
- **Line**: 30
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: F401
- **Message**: `collections.defaultdict` imported but unused

### Issue 3
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_enrichment/scripts/generate_chapter_metadata.py`
- **Line**: 27
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: F401
- **Message**: `typing.Tuple` imported but unused

### Issue 4
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_enrichment/scripts/generate_chapter_metadata.py`
- **Line**: 34
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: E402
- **Message**: Module level import not at top of file

### Issue 5
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_enrichment/scripts/generate_chapter_metadata.py`
- **Line**: 38
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: E402
- **Message**: Module level import not at top of file

### Issue 6
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_extraction/scripts/detect_poor_ocr.py`
- **Line**: 24
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: F401
- **Message**: `typing.Dict` imported but unused

### Issue 7
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_extraction/scripts/generate_metadata_universal.py`
- **Line**: 32
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: F401
- **Message**: `re` imported but unused

### Issue 8
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_extraction/scripts/generate_metadata_universal.py`
- **Line**: 36
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: F401
- **Message**: `typing.Set` imported but unused

### Issue 9
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_extraction/scripts/generate_metadata_universal.py`
- **Line**: 46
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: E402
- **Message**: Module level import not at top of file

### Issue 10
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_extraction/scripts/generate_metadata_universal.py`
- **Line**: 50
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: E402
- **Message**: Module level import not at top of file

### Issue 11
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_extraction/scripts/generate_metadata_universal.py`
- **Line**: 51
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: E402
- **Message**: Module level import not at top of file

### Issue 12
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_extraction/scripts/generate_metadata_universal.py`
- **Line**: 52
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: E402
- **Message**: Module level import not at top of file

### Issue 13
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_extraction/scripts/generate_metadata_universal.py`
- **Line**: 53
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: E402
- **Message**: Module level import not at top of file

### Issue 14
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_extraction/scripts/generate_metadata_universal.py`
- **Line**: 54
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: E402
- **Message**: Module level import not at top of file

### Issue 15
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_extraction/scripts/strategies/predefined_strategy.py`
- **Line**: 43
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: invalid-syntax
- **Message**: Unexpected indentation

### Issue 16
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_extraction/scripts/strategies/predefined_strategy.py`
- **Line**: 43
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: invalid-syntax
- **Message**: Expected a statement

### Issue 17
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_extraction/scripts/strategies/predefined_strategy.py`
- **Line**: 43
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: invalid-syntax
- **Message**: Expected a statement

### Issue 18
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_extraction/scripts/strategies/predefined_strategy.py`
- **Line**: 44
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: invalid-syntax
- **Message**: missing closing quote in string literal

### Issue 19
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_extraction/scripts/strategies/predefined_strategy.py`
- **Line**: 67
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: invalid-syntax
- **Message**: Expected a statement

### Issue 20
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/pdf_to_json/scripts/chapter_segmentation_services.py`
- **Line**: 19
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: F401
- **Message**: `typing.Dict` imported but unused

... and 18 more issues

## 🔵 Low Issues (3)

### Issue 1
- **File**: `./llm_enhancement/scripts/phases/content_selection_impl.py`
- **Line**: 428
- **Tool**: bandit
- **Type**: security
- **Rule**: B110
- **Message**: Try, Except, Pass detected.

### Issue 2
- **File**: `./metadata_extraction/scripts/generate_metadata_universal.py`
- **Line**: 253
- **Tool**: bandit
- **Type**: security
- **Rule**: B110
- **Message**: Try, Except, Pass detected.

### Issue 3
- **File**: `./metadata_extraction/scripts/strategies/yake_validation_strategy.py`
- **Line**: 74
- **Tool**: bandit
- **Type**: security
- **Rule**: B112
- **Message**: Try, Except, Continue detected.
