# CodeRabbit Local Analysis Report
**Generated**: 2025-11-26 00:49:07
**Total Issues**: 20

## Summary
| Severity | Count |
|----------|-------|
| 🚨 Critical | 0 |
| 🔴 High | 0 |
| 🟡 Medium | 18 |
| 🔵 Low | 2 |
| ℹ️ Info | 0 |

## 🟡 Medium Issues (18)

### Issue 1
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_enrichment/scripts/generate_chapter_metadata.py`
- **Line**: 27
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: F401
- **Message**: `typing.Tuple` imported but unused

### Issue 2
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_extraction/scripts/detect_poor_ocr.py`
- **Line**: 24
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: F401
- **Message**: `typing.Dict` imported but unused

### Issue 3
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_extraction/scripts/generate_metadata_universal.py`
- **Line**: 32
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: F401
- **Message**: `re` imported but unused

### Issue 4
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_extraction/scripts/generate_metadata_universal.py`
- **Line**: 36
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: F401
- **Message**: `typing.Set` imported but unused

### Issue 5
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_extraction/scripts/strategies/predefined_strategy.py`
- **Line**: 43
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: invalid-syntax
- **Message**: Unexpected indentation

### Issue 6
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_extraction/scripts/strategies/predefined_strategy.py`
- **Line**: 43
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: invalid-syntax
- **Message**: Expected a statement

### Issue 7
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_extraction/scripts/strategies/predefined_strategy.py`
- **Line**: 43
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: invalid-syntax
- **Message**: Expected a statement

### Issue 8
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_extraction/scripts/strategies/predefined_strategy.py`
- **Line**: 44
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: invalid-syntax
- **Message**: missing closing quote in string literal

### Issue 9
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_extraction/scripts/strategies/predefined_strategy.py`
- **Line**: 67
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: invalid-syntax
- **Message**: Expected a statement

### Issue 10
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/pdf_to_json/scripts/chapter_segmentation_services.py`
- **Line**: 19
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: F401
- **Message**: `typing.Dict` imported but unused

### Issue 11
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/pdf_to_json/scripts/chapter_segmentation_services.py`
- **Line**: 20
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: F401
- **Message**: `numpy` imported but unused

### Issue 12
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/pdf_to_json/scripts/chapter_segmenter.py`
- **Line**: 21
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: F401
- **Message**: `re` imported but unused

### Issue 13
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/pdf_to_json/scripts/chapter_segmenter.py`
- **Line**: 27
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: F401
- **Message**: `sklearn.feature_extraction.text.TfidfVectorizer` imported but unused

### Issue 14
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/pdf_to_json/scripts/chapter_segmenter.py`
- **Line**: 28
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: F401
- **Message**: `sklearn.metrics.pairwise.cosine_similarity` imported but unused

### Issue 15
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/pdf_to_json/scripts/chapter_segmenter.py`
- **Line**: 29
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: F401
- **Message**: `numpy` imported but unused

### Issue 16
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/pdf_to_json/scripts/ml_chapter_detector.py`
- **Line**: 15
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: F401
- **Message**: `typing.Dict` imported but unused

### Issue 17
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/taxonomy_setup/scripts/generate_concept_taxonomy.py`
- **Line**: 26
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: F401
- **Message**: `collections.defaultdict` imported but unused

### Issue 18
- **File**: `metadata_extraction/scripts/strategies/predefined_strategy.py`
- **Line**: 43
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Unexpected indent  [syntax]

## 🔵 Low Issues (2)

### Issue 1
- **File**: `./metadata_extraction/scripts/generate_metadata_universal.py`
- **Line**: 253
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
