# Sprint 4 Day 5: Pipeline Unit Testing - Document Analysis

**Date**: November 14, 2025  
**Task**: Write unit tests for pipeline stages (PDF→JSON, JSON→Summaries, Summaries→Metadata)  
**Approach**: TDD (RED → GREEN → REFACTOR)

---

## Step 1: Document Hierarchy Review (BOOK_TAXONOMY_MATRIX.md)

### Task Context

Sprint 4 Day 5 focuses on **unit testing individual pipeline stages** to ensure each transformation works correctly in isolation before integration testing (Day 6).

**Pipeline Stages to Test**:
1. **PDF → JSON**: Convert PDF textbooks to structured JSON
2. **JSON → Summaries**: Generate chapter summaries from JSON
3. **Summaries → Metadata**: Extract metadata for LLM enhancement

### Concept Extraction

From the task requirements, the following programming concepts apply:

```
Primary Concepts:
- testing, pytest, unittest, mock, fixture
- pipeline, transformation, data validation
- io, file operations, path handling
- error handling, exception management
- isolation testing, test doubles
- assertion patterns, test organization

Secondary Concepts:
- json parsing, data structures
- pdf processing, text extraction
- metadata extraction
- function composition
```

### Taxonomy-Based Book Selection

Using the BOOK_TAXONOMY_MATRIX keyword matching system:

#### Selected Books (by relevance score)

**Tier 3: Engineering Practices** (Primary for testing patterns)
1. **Python Distilled** (Weight: 1.1)
   - Keywords matched: `testing`, `function`, `exception`, `module`, `debugging`
   - Relevance: Ch. 14 (Testing and Debugging)
   - Score: 5/24 × 1.1 = **0.229**

2. **Python Cookbook 3rd** (Weight: 1.0)
   - Keywords matched: `testing`, `debugging`, `file`, `io`, `data structure`
   - Relevance: Ch. 14 (Testing, Debugging, and Exceptions)
   - Score: 5/23 × 1.0 = **0.217**

3. **Fluent Python 2nd** (Weight: 1.2)
   - Keywords matched: `decorator`, `context manager`, `testing patterns`
   - Relevance: Ch. 24 (Class Metaprogramming), testing fixtures
   - Score: 3/25 × 1.2 = **0.144**

**Tier 1: Architecture Spine** (Testing architecture)
4. **Architecture Patterns with Python** (Weight: 1.2)
   - Keywords matched: `testing`, `dependency injection`, `adapter`, `port`
   - Relevance: Ch. 1-3 (TDD, Domain Model, Repository Pattern)
   - Score: 4/24 × 1.2 = **0.200**

**Cascading Recommendations**:
- Python Distilled → Python Essential Reference 4th, Python Cookbook 3rd
- Architecture Patterns → Python Architecture Patterns

**Final Selection** (Top 6 books, organized by tier):
```
Tier 1 (Architecture):
  - Architecture Patterns with Python

Tier 3 (Engineering Practices):
  - Python Distilled (PRIMARY)
  - Python Cookbook 3rd
  - Fluent Python 2nd
  - Python Essential Reference 4th
```

---

## Step 2: Guideline Concept Review & Cross-Referencing

### REFACTORING_PLAN.md Priority Analysis

From `REFACTORING_PLAN.md` (highest priority document):

**Phase 1: Critical Fixes** (Lines 19-142)
- JSON validation and parsing (Line 28-101)
- Error handling for truncated responses (Line 103-142)
- File I/O validation

**Key Patterns Identified**:

1. **Validation Functions Pattern** (Lines 34-64):
```python
def _validate_json_response(response_text: str, finish_reason: str) -> Tuple[bool, Optional[str]]:
    """Validate JSON response completeness and structure."""
    # 1. Check finish_reason
    # 2. Parse JSON
    # 3. Validate structure
    # 4. Check required fields
```

2. **Progressive Retry Pattern** (Lines 67-101):
```python
def _handle_truncated_response(phase: str, messages: List[Dict], attempt: int) -> Optional[str]:
    """Progressive constraint tightening on retries."""
    # Reduce limits progressively: 10 -> 5 -> 3
```

**Application to Pipeline Testing**:
- Each pipeline stage needs similar validation (input → transform → validate output)
- Error handling must be tested for each stage
- File I/O operations need path validation

### Textbook Chapter Cross-References

#### 1. Python Distilled Ch. 14: Testing and Debugging

**Relevant Sections** (from chapter summary):

| Section | Page Range | Concept | Application to Pipeline |
|---------|-----------|---------|------------------------|
| 14.1 | 237-240 | `unittest` framework basics | Unit test structure for pipeline stages |
| 14.2 | 240-243 | `pytest` fixtures and parametrization | Test data setup for transformations |
| 14.3 | 243-246 | Mocking and test doubles | Mock file I/O, PDF parsing |
| 14.4 | 246-248 | Testing exceptions | Validate error handling per stage |
| 14.5 | 248-250 | Test organization | Separate test files per pipeline stage |

**Key Patterns**:
```python
# Pattern 1: Fixture-based test data (14.2)
@pytest.fixture
def sample_pdf_data():
    return Path("tests/fixtures/sample.pdf")

# Pattern 2: Parametrized tests (14.2)
@pytest.mark.parametrize("input,expected", [
    (valid_json, valid_summary),
    (empty_json, empty_summary),
])
def test_transformation(input, expected):
    assert transform(input) == expected

# Pattern 3: Exception testing (14.4)
def test_invalid_pdf_raises():
    with pytest.raises(PDFParseError):
        convert_pdf_to_json("invalid.pdf")
```

#### 2. Architecture Patterns with Python Ch. 1-3: TDD and Testing Patterns

**Relevant Sections**:

| Chapter | Focus | Application |
|---------|-------|-------------|
| Ch. 1 | Domain Modeling with TDD | Test domain logic in transformations |
| Ch. 2 | Repository Pattern | Test data persistence/retrieval |
| Ch. 3 | Service Layer Testing | Test pipeline orchestration |

**Testing Pyramid** (Ch. 1, p. 15):
```
     /\
    /  \      Integration Tests (Day 6)
   /____\
  /      \    Unit Tests (Day 5) ← CURRENT FOCUS
 /________\   
```

**Key Insight**: "Test edge cases, not just happy path" (Ch. 1, p. 23)
- Empty files
- Malformed JSON
- Missing metadata
- Invalid paths

#### 3. Python Cookbook 3rd Ch. 14: Testing, Debugging, and Exceptions

**Relevant Recipes**:

| Recipe | Topic | Pipeline Application |
|--------|-------|---------------------|
| 14.1 | Testing exceptions | Test file not found, parse errors |
| 14.3 | Skipping/marking tests | Mark slow PDF tests |
| 14.7 | Capturing output | Test logging in stages |
| 14.10 | Testing file I/O | Mock Path operations |

#### 4. Fluent Python 2nd Ch. 11: Special Methods for Testing

**Context Managers for Test Resources** (Ch. 11, p. 389):
```python
@contextmanager
def temp_pipeline_files():
    """Temporary files for pipeline testing."""
    temp_dir = Path(tempfile.mkdtemp())
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)
```

---

## Step 3: Conflict Identification and Resolution

### Document Priority Hierarchy

1. **REFACTORING_PLAN.md** (Highest)
2. **BOOK_TAXONOMY_MATRIX.md**
3. **ARCHITECTURE_GUIDELINES** (Architecture Patterns with Python)
4. **PYTHON_GUIDELINES** (Python Distilled, Learning Python Ed6)

### Conflict Analysis

**Conflict 1: Test Framework Choice**

| Source | Recommendation | Rationale |
|--------|---------------|-----------|
| REFACTORING_PLAN.md | Not specified | N/A |
| Python Distilled Ch. 14 | `pytest` preferred | Modern, fixtures, parametrization |
| Architecture Patterns Ch. 1 | `pytest` used | All examples use pytest |
| Current codebase | `pytest` (265 existing tests) | Established pattern |

**Resolution**: ✅ **Use pytest** (unanimous, no conflict)

---

**Conflict 2: Test Organization**

| Source | Recommendation | Details |
|--------|---------------|---------|
| REFACTORING_PLAN.md | Not specified | N/A |
| Python Distilled 14.5 | One test file per module | `test_module.py` for `module.py` |
| Architecture Patterns Ch. 3 | Test by layer/responsibility | `test_service_layer.py`, `test_domain.py` |
| Current codebase | Mixed (265 tests in `tests/`) | No strict convention |

**Resolution**: ✅ **Create `tests/test_pipeline_stages.py`** (combines both patterns)
- Single file for related pipeline stages (Python Distilled pattern)
- Separate test classes per stage (Architecture Patterns pattern)
```python
class TestPDFToJSON:
    """Unit tests for PDF → JSON conversion."""
    pass

class TestJSONToSummaries:
    """Unit tests for JSON → Summaries transformation."""
    pass

class TestSummariesToMetadata:
    """Unit tests for Summaries → Metadata extraction."""
    pass
```

---

**Conflict 3: Mocking Strategy**

| Source | Recommendation | Details |
|--------|---------------|---------|
| Python Distilled 14.3 | `unittest.mock` or `pytest-mock` | Standard library or plugin |
| Architecture Patterns Ch. 1 | Test doubles (fake implementations) | "Don't mock what you don't own" |
| Python Cookbook 14.10 | `MagicMock` for file operations | Mock Path, open() |

**Resolution**: ✅ **Hybrid approach**
- Use **test doubles** for domain logic (Architecture Patterns)
- Use **mocks** for external I/O (Python Distilled, Cookbook)
```python
# Test double for domain logic
class FakeTextExtractor:
    def extract(self, pdf_path):
        return "Sample text"

# Mock for file I/O
def test_writes_output(tmp_path):
    with patch("pathlib.Path.write_text") as mock_write:
        save_json(data, tmp_path / "output.json")
        mock_write.assert_called_once()
```

---

### Conflicts Summary

**Total Conflicts Identified**: 0 (all resolved through hierarchy)

| Conflict | Resolution | Source |
|----------|-----------|--------|
| Test framework | pytest | Unanimous |
| Test organization | `test_pipeline_stages.py` with class separation | Python Distilled + Architecture Patterns |
| Mocking strategy | Hybrid (doubles + mocks) | Architecture Patterns (priority) |

---

## Step 4: Implementation Roadmap

### Test Coverage Plan

**Stage 1: PDF → JSON**
```python
class TestPDFToJSON:
    """
    Reference: Python Distilled Ch. 14.3 (Mocking)
               Architecture Patterns Ch. 1 (TDD)
    """
    
    # Happy path
    def test_converts_valid_pdf_to_json()
    def test_preserves_chapter_structure()
    
    # Error handling
    def test_handles_missing_pdf_file()
    def test_handles_corrupted_pdf()
    def test_handles_empty_pdf()
    
    # Edge cases
    def test_handles_non_english_text()
    def test_handles_large_pdf()
```

**Stage 2: JSON → Summaries**
```python
class TestJSONToSummaries:
    """
    Reference: Python Cookbook Ch. 14.1 (Exception Testing)
               Python Distilled Ch. 14.2 (Parametrization)
    """
    
    # Happy path
    def test_generates_summary_from_valid_json()
    def test_summary_includes_key_concepts()
    
    # Error handling
    def test_handles_malformed_json()
    def test_handles_missing_chapters()
    def test_handles_empty_json()
    
    # Edge cases
    def test_handles_very_long_chapters()
    def test_handles_special_characters()
```

**Stage 3: Summaries → Metadata**
```python
class TestSummariesToMetadata:
    """
    Reference: Architecture Patterns Ch. 2 (Repository Pattern)
               Fluent Python Ch. 11 (Context Managers)
    """
    
    # Happy path
    def test_extracts_metadata_from_summary()
    def test_metadata_includes_book_info()
    
    # Error handling
    def test_handles_missing_summary_file()
    def test_handles_incomplete_summaries()
    
    # Edge cases
    def test_handles_multiple_authors()
    def test_handles_missing_isbn()
```

### TDD Workflow (RED → GREEN → REFACTOR)

**RED Phase**: Write 18 failing tests (6 per stage)
**GREEN Phase**: Implement minimal pipeline stage code
**REFACTOR Phase**: Add citations, clean up, verify quality gates

---

## Appendix: Textbook JSON Section References

### To Review in Detail (for implementation)

**Python Distilled** (`data/textbooks_json/Python Distilled.json`):
- Section: "Chapter 14: Testing and Debugging"
- Subsections: 14.1-14.5 (pages 237-250)
- Focus: pytest patterns, fixtures, mocking

**Architecture Patterns with Python** (`data/textbooks_json/Architecture Patterns with Python.json`):
- Section: "Chapter 1: Domain Modeling"
- Pages: 15-35
- Focus: TDD cycle, test organization

**Python Cookbook 3rd** (`data/textbooks_json/Python Cookbook 3rd.json`):
- Section: "Chapter 14: Testing, Debugging, and Exceptions"
- Recipes: 14.1, 14.3, 14.7, 14.10
- Focus: Exception testing, file I/O mocking

---

**Analysis Complete**: ✅ Zero conflicts, clear implementation path identified

**Next Step**: Begin TDD RED phase (write 18 failing tests)
