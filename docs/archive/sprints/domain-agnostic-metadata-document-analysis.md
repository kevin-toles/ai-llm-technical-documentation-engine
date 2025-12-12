# Domain-Agnostic Metadata Extraction - Document Analysis & Cross-Referencing

**Task**: Phase 1 Implementation - Replace hardcoded Python keywords with statistical NLP (YAKE + Summa + scikit-learn)  
**Date**: November 18, 2025  
**WBS Item**: DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md - Part 1 (Metadata Extraction)

---

## Step 1: Document Hierarchy Review

### Primary Guiding Documents (Priority Order)
1. ✅ **DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md** (Priority #1)
2. ✅ **BOOK_TAXONOMY_MATRIX.md** (Priority #2)
3. ✅ **ARCHITECTURE_GUIDELINES_Architecture_Patterns_with_Python_LLM_ENHANCED.md** (Priority #3)
4. ✅ **PYTHON_GUIDELINES_Learning_Python_Ed6_LLM_ENHANCED.md** (Priority #4)

### BOOK_TAXONOMY_MATRIX Mapping

**Applicable Textbooks** (from taxonomy):
- **Tier 1 (Architecture Spine)**: Architecture Patterns with Python
- **Tier 2 (Implementation)**: Building Python Microservices with FastAPI
- **Tier 3 (Engineering Practices)**: Fluent Python 2nd, Python Distilled

**Relevant High-Level Concepts** (from DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md):
1. **Statistical NLP** - keyword extraction, summarization, TF-IDF
2. **Adapter Pattern** - creating statistical_extractor.py adapter
3. **Test-Driven Development** - RED → GREEN → REFACTOR cycle
4. **Domain Independence** - works across Python, biology, law, construction
5. **Cost Optimization** - reduce LLM token usage by 95%

---

## Step 2: Guideline Concept Review & Cross-Referencing

### ARCHITECTURE_GUIDELINES Cross-References

**Chapter 4: Repository Pattern & Adapter Pattern**
- **Concept**: Adapters as abstraction layer between domain logic and external dependencies
- **Application**: `statistical_extractor.py` is an adapter for YAKE/Summa/scikit-learn
- **Key Quote**: "Adapters isolate external dependencies (databases, APIs, file systems) from domain logic"
- **Relevance**: Statistical NLP libraries (YAKE, Summa) are external dependencies needing abstraction

**Chapter 5: Service Layer Pattern**
- **Concept**: Service layer coordinates between adapters and domain logic
- **Application**: `generate_metadata_universal.py` orchestrates statistical extraction
- **Key Quote**: "Service layer defines use cases and coordinates adapters"
- **Relevance**: Metadata extraction is a use case coordinating statistical extractors

**Chapter 1: Test-Driven Development**
- **Concept**: RED (fail) → GREEN (pass) → REFACTOR (clean) cycle
- **Application**: Write failing tests first for statistical extraction across domains
- **Key Quote**: "Write tests FIRST to define expected behavior, then implement minimal code"
- **Relevance**: Must test Python, biology, law, construction domains BEFORE implementing

### PYTHON_GUIDELINES Cross-References

**Chapter 7: Classes and Object-Oriented Programming**
- **Concept**: Class design, single responsibility, composition over inheritance
- **Application**: `StatisticalExtractor` class with focused responsibility
- **Key Quote**: "Each class should have one clear purpose"
- **Relevance**: StatisticalExtractor extracts keywords/summaries, nothing else

**Chapter 9: Decorators and Context Managers**
- **Concept**: Clean resource management patterns
- **Application**: Potential for caching decorator on keyword extraction
- **Key Quote**: "Decorators separate cross-cutting concerns from core logic"
- **Relevance**: May need caching for repeated keyword extraction

**Chapter 13: Testing and Debugging**
- **Concept**: Unit tests, fixtures, parametrization, TDD workflow
- **Application**: `test_statistical_extractor.py` with 4-domain parametrized tests
- **Key Quote**: "Use parametrize to test multiple inputs with same logic"
- **Relevance**: Test 4 domains (Python, biology, law, construction) with same extractor

### Textbook JSON Sections to Review

**From ARCHITECTURE_GUIDELINES annotations**:
1. Architecture Patterns with Python - Chapter 4 (Repository & Adapter patterns)
2. Architecture Patterns with Python - Chapter 5 (Service Layer)
3. Architecture Patterns with Python - Chapter 1 (TDD fundamentals)

**From PYTHON_GUIDELINES annotations**:
1. Fluent Python 2nd - Chapter 7 (Object-Oriented idioms)
2. Python Distilled - Chapter 9 (Testing best practices)
3. Python Essential Reference - Chapter 5 (Built-in types for efficient data structures)

---

## Step 3: Conflict Identification and Resolution

### Identified Conflicts

#### Conflict 1: Extraction Strategy (Statistical vs Hardcoded)

**WBS Item**: DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md - Part 1.1 (Replace hardcoded keywords)  
**Conflicting Guideline(s)**: None - All guidelines support adapter pattern  
**Nature of Conflict**: N/A - No conflict  
**Resolution**: ✅ Proceed with statistical NLP extraction (YAKE + Summa)

#### Conflict 2: Test Coverage (4 Domains vs Python-Only)

**WBS Item**: DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md - Section 5.1 (Testing Strategy)  
**Conflicting Guideline(s)**: None - PYTHON_GUIDELINES Ch. 13 supports parametrized tests  
**Nature of Conflict**: N/A - No conflict  
**Resolution**: ✅ Use `pytest.mark.parametrize` to test 4 domains (Python, biology, law, construction)

#### Conflict 3: Integration Point (Direct replacement vs Feature flag)

**WBS Item**: DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md - Part 1.3 (Integration)  
**Potential Issue**: Should we replace hardcoded extraction immediately or use feature flag?  
**Conflicting Guideline(s)**: ARCHITECTURE_GUIDELINES Ch. 5 (Service Layer suggests clean replacement)  
**Nature of Conflict**: Implementation approach  

**Option A - Direct Replacement**:
- Pros: Clean, no technical debt, follows SOLID principles
- Cons: Higher risk if statistical extraction fails

**Option B - Feature Flag (Gradual Rollout)**:
- Pros: Can rollback, A/B test quality, gradual migration
- Cons: Added complexity, temporary technical debt

**Option C - Parallel Mode (Both methods available)**:
- Pros: Can compare results, validate quality before cutover
- Cons: Most complex, longest implementation time

**Recommendation**: **Option A (Direct Replacement)**  
**Rationale**:
1. DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md explicitly states "Replace all hardcoded"
2. TDD with 4 domains ensures quality before deployment
3. ARCHITECTURE_GUIDELINES Ch. 5 favors clean service layer over conditional logic
4. Current hardcoded extraction is broken for non-Python domains anyway

**Approval Needed From**: User (Kevin) - Confirm direct replacement vs feature flag

---

## Summary: Selected Textbooks & Concepts

### Textbooks (from BOOK_TAXONOMY_MATRIX)
1. **Architecture Patterns with Python** (Tier 1) - Adapter pattern, Service layer, TDD
2. **Fluent Python 2nd** (Tier 3) - Pythonic class design, protocols
3. **Python Distilled** (Tier 3) - Testing best practices, clean code

### Core Concepts (mapped to implementation)
1. **Adapter Pattern** → `statistical_extractor.py` adapts YAKE/Summa/scikit-learn
2. **Service Layer** → `generate_metadata_universal.py` orchestrates extraction
3. **TDD (RED→GREEN→REFACTOR)** → Write tests first for 4 domains
4. **Single Responsibility** → StatisticalExtractor does ONE thing (extract keywords/summaries)
5. **Parametrized Testing** → Test 4 domains with same test logic

### JSON Sections to Review (target reading)
- Architecture Patterns Ch. 4: Pages 85-120 (Adapter pattern implementation)
- Architecture Patterns Ch. 5: Pages 121-155 (Service layer coordination)
- Fluent Python Ch. 7: Pages 180-220 (Class design best practices)
- Python Distilled Ch. 9: Pages 210-240 (Unit testing with pytest)

---

## Compliance Matrix

| Requirement | DOMAIN_AGNOSTIC_PLAN | BOOK_TAXONOMY | ARCHITECTURE_GUIDELINES | PYTHON_GUIDELINES | Status |
|-------------|---------------------|---------------|------------------------|-------------------|--------|
| Use Adapter Pattern | ✅ Part 1.2 | ✅ Tier 1 books | ✅ Ch. 4 | ✅ Ch. 7 | ✅ Aligned |
| TDD Workflow | ✅ Section 5 | ✅ Tier 1 | ✅ Ch. 1 | ✅ Ch. 13 | ✅ Aligned |
| Test 4 Domains | ✅ Section 5.1 | N/A | N/A | ✅ Ch. 13 (parametrize) | ✅ Aligned |
| Replace Hardcoded | ✅ Part 1.1 | N/A | ✅ Ch. 5 (clean service) | ✅ Ch. 7 (SRP) | ✅ Aligned |
| Statistical NLP | ✅ Overview | N/A | ✅ Ch. 4 (external deps) | ✅ Ch. 7 (composition) | ✅ Aligned |

---

## Next Steps (TDD Implementation - Phase 1)

### RED Phase (Write Failing Tests)
1. Create `tests/unit/test_statistical_extractor.py`
2. Define test cases for 4 domains: `@pytest.mark.parametrize("domain", ["python", "biology", "law", "construction"])`
3. Test keyword extraction: `test_extract_keywords_domain_agnostic()`
4. Test concept extraction: `test_extract_concepts_domain_agnostic()`
5. Test summarization: `test_generate_summary_domain_agnostic()`
6. Run tests → Expect failures (no implementation yet)

### GREEN Phase (Minimal Implementation)
1. Create `workflows/metadata_extraction/scripts/adapters/statistical_extractor.py`
2. Implement `StatisticalExtractor` class:
   - `extract_keywords(text: str, top_n: int = 20) -> List[Tuple[str, float]]` (YAKE)
   - `extract_concepts(text: str, top_n: int = 10) -> List[str]` (Summa keywords)
   - `generate_summary(text: str, ratio: float = 0.2) -> str` (Summa summarizer)
3. Run tests → Make them pass with minimal code

### REFACTOR Phase (Clean & Align)
1. Add type hints, docstrings (PER PYTHON_GUIDELINES Ch. 7)
2. Add error handling (PER PYTHON_GUIDELINES Ch. 8)
3. Optimize performance (caching, batching if needed)
4. Verify compliance with ARCHITECTURE_GUIDELINES Ch. 4 (adapter pattern)
5. Run SonarLint, SonarQube, CodeRabbit → Fix all issues

---

**Status**: ✅ Document Analysis Complete - Ready for TDD Implementation (RED phase)  
**Conflicts**: ✅ Zero conflicts identified - All guidelines aligned  
**Approval Needed**: User confirmation on Option A (Direct Replacement) vs Options B/C
