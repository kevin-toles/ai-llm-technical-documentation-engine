# CodeRabbit Local Analysis Report
**Generated**: 2025-11-14 12:31:18
**Total Issues**: 713

## Summary
| Severity | Count |
|----------|-------|
| 🚨 Critical | 0 |
| 🔴 High | 0 |
| 🟡 Medium | 116 |
| 🔵 Low | 597 |
| ℹ️ Info | 0 |

## Recommendations
- 🔧 Consider refactoring to reduce medium-severity issues

## 🟡 Medium Issues (116)

### Issue 1
- **File**: `src/book_taxonomy.py`
- **Line**: 369
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: "add" of "set" does not return a value (it only ever returns None)  [func-returns-value]

### Issue 2
- **File**: `src/book_taxonomy.py`
- **Line**: 454
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: "add" of "set" does not return a value (it only ever returns None)  [func-returns-value]

### Issue 3
- **File**: `src/chapter_metadata_manager.py`
- **Line**: 29
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Incompatible types in assignment (expression has type "None", variable has type "list[str]")  [assignment]

### Issue 4
- **File**: `src/chapter_metadata_manager.py`
- **Line**: 54
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Incompatible types in assignment (expression has type "Path", variable has type "str | None")  [assignment]

### Issue 5
- **File**: `src/chapter_metadata_manager.py`
- **Line**: 56
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Incompatible types in assignment (expression has type "Path", variable has type "str | None")  [assignment]

### Issue 6
- **File**: `src/chapter_metadata_manager.py`
- **Line**: 58
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Unsupported left operand type for / ("str")  [operator]

### Issue 7
- **File**: `src/chapter_metadata_manager.py`
- **Line**: 58
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Unsupported left operand type for / ("None")  [operator]

### Issue 8
- **File**: `src/chapter_metadata_manager.py`
- **Line**: 58
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Left operand is of type "str | None"

### Issue 9
- **File**: `src/chapter_metadata_manager.py`
- **Line**: 59
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Unsupported left operand type for / ("str")  [operator]

### Issue 10
- **File**: `src/chapter_metadata_manager.py`
- **Line**: 59
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Unsupported left operand type for / ("None")  [operator]

### Issue 11
- **File**: `src/chapter_metadata_manager.py`
- **Line**: 59
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Left operand is of type "str | None"

### Issue 12
- **File**: `src/chapter_metadata_manager.py`
- **Line**: 195
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Need type annotation for "all_books" (hint: "all_books: set[<type>] = ...")  [var-annotated]

### Issue 13
- **File**: `src/pipeline/convert_pdf_to_json.py`
- **Line**: 11
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Skipping analyzing "fitz": module is installed, but missing library stubs or py.typed marker  [import-untyped]

### Issue 14
- **File**: `src/pipeline/chapter_generator_all_text.py`
- **Line**: 27
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Cannot find implementation or library stub for module named "llm_integration"  [import-not-found]

### Issue 15
- **File**: `src/pipeline/chapter_generator_all_text.py`
- **Line**: 395
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Need type annotation for "matches" (hint: "matches: list[<type>] = ...")  [var-annotated]

### Issue 16
- **File**: `src/pipeline/chapter_generator_all_text.py`
- **Line**: 1376
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: Incompatible types in assignment (expression has type "list[Never]", variable has type "str")  [assignment]

### Issue 17
- **File**: `src/pipeline/chapter_generator_all_text.py`
- **Line**: 1377
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: "str" has no attribute "append"  [attr-defined]

### Issue 18
- **File**: `src/pipeline/chapter_generator_all_text.py`
- **Line**: 1378
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: "str" has no attribute "append"  [attr-defined]

### Issue 19
- **File**: `src/pipeline/chapter_generator_all_text.py`
- **Line**: 1383
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: "str" has no attribute "append"  [attr-defined]

### Issue 20
- **File**: `src/pipeline/chapter_generator_all_text.py`
- **Line**: 1384
- **Tool**: mypy
- **Type**: type_safety
- **Rule**: type-check
- **Message**: "str" has no attribute "append"  [attr-defined]

... and 96 more issues

## 🔵 Low Issues (597)

### Issue 1
- **File**: `./coderabbit/scripts/local_coderabbit.py`
- **Line**: 9
- **Tool**: bandit
- **Type**: security
- **Rule**: B404
- **Message**: Consider possible security implications associated with the subprocess module.

### Issue 2
- **File**: `./coderabbit/scripts/local_coderabbit.py`
- **Line**: 48
- **Tool**: bandit
- **Type**: security
- **Rule**: B607
- **Message**: Starting a process with a partial executable path

### Issue 3
- **File**: `./coderabbit/scripts/local_coderabbit.py`
- **Line**: 48
- **Tool**: bandit
- **Type**: security
- **Rule**: B603
- **Message**: subprocess call - check for execution of untrusted input.

### Issue 4
- **File**: `./coderabbit/scripts/local_coderabbit.py`
- **Line**: 92
- **Tool**: bandit
- **Type**: security
- **Rule**: B607
- **Message**: Starting a process with a partial executable path

### Issue 5
- **File**: `./coderabbit/scripts/local_coderabbit.py`
- **Line**: 92
- **Tool**: bandit
- **Type**: security
- **Rule**: B603
- **Message**: subprocess call - check for execution of untrusted input.

### Issue 6
- **File**: `./coderabbit/scripts/local_coderabbit.py`
- **Line**: 113
- **Tool**: bandit
- **Type**: security
- **Rule**: B607
- **Message**: Starting a process with a partial executable path

### Issue 7
- **File**: `./coderabbit/scripts/local_coderabbit.py`
- **Line**: 113
- **Tool**: bandit
- **Type**: security
- **Rule**: B603
- **Message**: subprocess call - check for execution of untrusted input.

### Issue 8
- **File**: `./coderabbit/scripts/local_coderabbit.py`
- **Line**: 175
- **Tool**: bandit
- **Type**: security
- **Rule**: B607
- **Message**: Starting a process with a partial executable path

### Issue 9
- **File**: `./coderabbit/scripts/local_coderabbit.py`
- **Line**: 175
- **Tool**: bandit
- **Type**: security
- **Rule**: B603
- **Message**: subprocess call - check for execution of untrusted input.

### Issue 10
- **File**: `./coderabbit/scripts/local_coderabbit.py`
- **Line**: 198
- **Tool**: bandit
- **Type**: security
- **Rule**: B607
- **Message**: Starting a process with a partial executable path

### Issue 11
- **File**: `./coderabbit/scripts/local_coderabbit.py`
- **Line**: 198
- **Tool**: bandit
- **Type**: security
- **Rule**: B603
- **Message**: subprocess call - check for execution of untrusted input.

### Issue 12
- **File**: `./coderabbit/scripts/local_coderabbit.py`
- **Line**: 249
- **Tool**: bandit
- **Type**: security
- **Rule**: B112
- **Message**: Try, Except, Continue detected.

### Issue 13
- **File**: `./src/interactive_llm_system_v3_hybrid_prompt.py`
- **Line**: 1307
- **Tool**: bandit
- **Type**: security
- **Rule**: B110
- **Message**: Try, Except, Pass detected.

### Issue 14
- **File**: `./src/phases/content_selection_impl.py`
- **Line**: 439
- **Tool**: bandit
- **Type**: security
- **Rule**: B110
- **Message**: Try, Except, Pass detected.

### Issue 15
- **File**: `./tests/test_cache.py`
- **Line**: 23
- **Tool**: bandit
- **Type**: security
- **Rule**: B101
- **Message**: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Issue 16
- **File**: `./tests/test_cache.py`
- **Line**: 24
- **Tool**: bandit
- **Type**: security
- **Rule**: B101
- **Message**: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Issue 17
- **File**: `./tests/test_cache.py`
- **Line**: 25
- **Tool**: bandit
- **Type**: security
- **Rule**: B101
- **Message**: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Issue 18
- **File**: `./tests/test_cache.py`
- **Line**: 36
- **Tool**: bandit
- **Type**: security
- **Rule**: B101
- **Message**: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Issue 19
- **File**: `./tests/test_cache.py`
- **Line**: 48
- **Tool**: bandit
- **Type**: security
- **Rule**: B101
- **Message**: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Issue 20
- **File**: `./tests/test_cache.py`
- **Line**: 60
- **Tool**: bandit
- **Type**: security
- **Rule**: B101
- **Message**: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

... and 577 more issues
