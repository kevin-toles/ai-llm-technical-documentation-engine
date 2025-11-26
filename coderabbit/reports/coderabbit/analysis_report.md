# CodeRabbit Local Analysis Report
**Generated**: 2025-11-26 00:42:47
**Total Issues**: 48

## Summary
| Severity | Count |
|----------|-------|
| 🚨 Critical | 0 |
| 🔴 High | 0 |
| 🟡 Medium | 46 |
| 🔵 Low | 2 |
| ℹ️ Info | 0 |

## Recommendations
- 🔧 Consider refactoring to reduce medium-severity issues

## 🟡 Medium Issues (46)

### Issue 1
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/llm_enhancement/scripts/phases/content_selection_impl.py`
- **Line**: 414
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: invalid-syntax
- **Message**: Expected a newline after line continuation character

### Issue 2
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/llm_enhancement/scripts/phases/content_selection_impl.py`
- **Line**: 414
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: invalid-syntax
- **Message**: missing closing quote in string literal

### Issue 3
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/llm_enhancement/scripts/phases/content_selection_impl.py`
- **Line**: 415
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: invalid-syntax
- **Message**: Unexpected indentation

### Issue 4
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/llm_enhancement/scripts/phases/content_selection_impl.py`
- **Line**: 424
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: invalid-syntax
- **Message**: unindent does not match any outer indentation level

### Issue 5
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/llm_enhancement/scripts/phases/content_selection_impl.py`
- **Line**: 459
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: invalid-syntax
- **Message**: unindent does not match any outer indentation level

### Issue 6
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/llm_enhancement/scripts/phases/content_selection_impl.py`
- **Line**: 492
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: invalid-syntax
- **Message**: unindent does not match any outer indentation level

### Issue 7
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/llm_enhancement/scripts/phases/content_selection_impl.py`
- **Line**: 497
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: invalid-syntax
- **Message**: unindent does not match any outer indentation level

### Issue 8
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/llm_enhancement/scripts/phases/content_selection_impl.py`
- **Line**: 500
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: invalid-syntax
- **Message**: Expected dedent, found end of file

### Issue 9
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_enrichment/scripts/enrich_metadata_per_book.py`
- **Line**: 28
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: F401
- **Message**: `typing.Optional` imported but unused

### Issue 10
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_enrichment/scripts/enrich_metadata_per_book.py`
- **Line**: 30
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: F401
- **Message**: `collections.defaultdict` imported but unused

### Issue 11
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_enrichment/scripts/generate_chapter_metadata.py`
- **Line**: 27
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: F401
- **Message**: `typing.Tuple` imported but unused

### Issue 12
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_enrichment/scripts/generate_chapter_metadata.py`
- **Line**: 34
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: E402
- **Message**: Module level import not at top of file

### Issue 13
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_enrichment/scripts/generate_chapter_metadata.py`
- **Line**: 38
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: E402
- **Message**: Module level import not at top of file

### Issue 14
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_extraction/scripts/detect_poor_ocr.py`
- **Line**: 24
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: F401
- **Message**: `typing.Dict` imported but unused

### Issue 15
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_extraction/scripts/generate_metadata_universal.py`
- **Line**: 32
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: F401
- **Message**: `re` imported but unused

### Issue 16
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_extraction/scripts/generate_metadata_universal.py`
- **Line**: 36
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: F401
- **Message**: `typing.Set` imported but unused

### Issue 17
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_extraction/scripts/generate_metadata_universal.py`
- **Line**: 46
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: E402
- **Message**: Module level import not at top of file

### Issue 18
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_extraction/scripts/generate_metadata_universal.py`
- **Line**: 50
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: E402
- **Message**: Module level import not at top of file

### Issue 19
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_extraction/scripts/generate_metadata_universal.py`
- **Line**: 51
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: E402
- **Message**: Module level import not at top of file

### Issue 20
- **File**: `/Users/kevintoles/POC/llm-document-enhancer/workflows/metadata_extraction/scripts/generate_metadata_universal.py`
- **Line**: 52
- **Tool**: ruff
- **Type**: code_quality
- **Rule**: E402
- **Message**: Module level import not at top of file

... and 26 more issues

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
