# TODO: File #1 - generate_metadata_universal.py Remediation
**TDD-Driven Refactoring: RED → GREEN → REFACTOR**

**File**: `workflows/metadata_extraction/scripts/generate_metadata_universal.py`  
**Priority**: 🔴 CRITICAL  
**Complexity Issues**: 3 (CC 18, 12, + eval() security)  
**Estimated Effort**: 28 hours  
**Started**: November 24, 2025  
**Status**: 🔄 IN PROGRESS

---

## Phase 1: Document Analysis & Cross-Referencing (MANDATORY FIRST)

### ✅ Step 1 – Document Hierarchy Review

#### 1.1 Review MASTER_IMPLEMENTATION_GUIDE.md ✅ COMPLETE
- [x] Read Part 1, §2: Critical Priority Files - `generate_metadata_universal.py` section
- [x] Extract documented issues:
  * [x] `auto_detect_chapters()` - CC 18 (CONFIRMED via Radon: M 140:4 - C (18))
  * [x] `main()` - CC 12 (CONFIRMED via Radon: F 472:0 - C (12))
  * [x] `eval()` usage - SECURITY (needs verification in code)
  * [x] 100+ hardcoded Python-specific patterns (per DOMAIN_AGNOSTIC_PLAN)
- [x] Extract remediation strategies already documented
- [x] Note architecture violations (SRP, OCP, DIP)
- [x] Extract effort estimate: 28 hours
- [x] Document acceptance criteria from guide

**Findings from MASTER_IMPLEMENTATION_GUIDE.md**:
- File: `workflows/metadata_extraction/scripts/generate_metadata_universal.py`
- Priority: 🔴 CRITICAL
- Lines: 612 | Functions: 13 | Maintainability: A
- Complexity Issues: `auto_detect_chapters` (CC 18), `main` (CC 12)
- Security: eval() usage detected
- Testing: No unit tests found
- Estimated Effort: 28 hours

#### 1.2 Review DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md ✅ COMPLETE
- [x] Confirm applicability: ✅ YES (metadata extraction domain)
- [x] Read Part 1: Domain-Agnostic Metadata Extraction
- [x] Extract key requirements:
  * [x] §2.1: Replace hardcoded keywords with YAKE extraction
  * [x] §2.2: Use TF-IDF for concept similarity
  * [x] §2.3: Statistical summarization with Summa
  * [x] Configuration-driven extraction (no hardcoded patterns)
- [x] Note dependencies: yake, summa, scikit-learn
- [x] Extract acceptance criteria specific to domain-agnostic approach

**Findings from DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md**:
- **Problem**: 100+ hardcoded software-specific regex patterns for concepts
- **Impact**: Cannot extract keywords from biology, law, construction, design textbooks
- **Solution**: Statistical NLP (YAKE, Summa, TF-IDF)
- **Dependencies**: yake==0.4.8, summa==1.2.0, scikit-learn>=1.3.0
- **Implementation**: StatisticalExtractor class already exists in codebase!
  * File: `workflows/metadata_extraction/scripts/adapters/statistical_extractor.py` (222 lines)
  * Methods: extract_keywords(), extract_concepts(), generate_summary()
- **Current Status**: File already imports StatisticalExtractor (line 28)
- **Configuration**: ExtractionConfig dataclass with YAKE/Summa parameters

#### 1.3 Review BOOK_TAXONOMY_MATRIX.md ✅ COMPLETE
- [x] Identify applicable domains:
  * [x] NLP/Text Processing domain → **Python Cookbook 3rd** (string, text, data structure)
  * [x] Architecture domain → **Architecture Patterns with Python**
  * [x] Python Programming domain → **Learning Python Ed6**, **Python Distilled**, **Fluent Python 2nd**
- [x] Map concepts to textbooks:
  * [x] Statistical NLP → **Python Cookbook 3rd** (data structure, algorithm, string)
  * [x] Repository Pattern → **Architecture Patterns with Python** Ch. 2
  * [x] Strategy Pattern → **Architecture Patterns with Python** Ch. 9
  * [x] Safe Evaluation (ast.literal_eval) → **Python Distilled**, **Python Essential Reference 4th**
  * [x] Function Design → **Python Distilled** (function, method, module)
  * [x] Type Hints → **Fluent Python 2nd** (type hint, annotation, protocol)
- [x] Create cross-reference table for this file

**Cross-Reference Table for generate_metadata_universal.py**:

| Issue/Concept | Applicable Book(s) | Tier | Chapters/Keywords | Priority |
|---------------|-------------------|------|-------------------|----------|
| `auto_detect_chapters()` CC 18 | Python Distilled | 3 | function, method, refactoring | PRIMARY |
| `main()` CC 12 | Python Distilled | 3 | function, exception, structure | PRIMARY |
| eval() security | Python Distilled | 3 | eval, ast.literal_eval, security | CRITICAL |
| Repository Pattern | Architecture Patterns with Python | 1 | Ch. 2 - Repository Pattern | HIGH |
| Strategy Pattern | Architecture Patterns with Python | 1 | Ch. 9 - Dependency Injection | HIGH |
| Type Hints | Fluent Python 2nd | 3 | type hint, annotation, protocol | MEDIUM |
| Statistical NLP | Python Cookbook 3rd | 3 | string, text, data structure | MEDIUM |
| Testing | Python Distilled | 3 | testing, debugging, pytest | HIGH |

**Cascading Books** (per taxonomy):
1. **Primary**: Python Distilled → Python Essential Reference 4th → Python Cookbook 3rd
2. **Architecture**: Architecture Patterns with Python → Building Python Microservices with FastAPI
3. **Advanced**: Fluent Python 2nd → Python Distilled

#### 1.4 List Relevant High-Level Concepts ✅ COMPLETE
- [x] Document all applicable concepts:
  * [x] YAKE keyword extraction (NLP) - **Already implemented via StatisticalExtractor**
  * [x] TF-IDF scoring (NLP) - **Already implemented via StatisticalExtractor**
  * [x] Summa summarization (NLP) - **Already implemented via StatisticalExtractor**
  * [x] Repository Pattern (Architecture) - **Needed for file I/O abstraction**
  * [x] Strategy Pattern (Architecture) - **Needed for chapter detection methods**
  * [x] ast.literal_eval (Security/Python) - **CRITICAL: Line 567 uses eval(args.chapters)**
  * [x] Extract Method refactoring (Python) - **CC 18 in auto_detect_chapters(), CC 12 in main()**
  * [x] Type hints and protocols (Python) - **Partially implemented, needs completion**

**Security Vulnerability Confirmed**:
```python
# Line 567 in generate_metadata_universal.py
chapters = eval(args.chapters)  # ❌ DANGEROUS - executes arbitrary code
```

**Current State Assessment**:
- File already imports `StatisticalExtractor` (line 28)
- Methods `extract_keywords()`, `extract_concepts()`, `generate_summary()` delegate to StatisticalExtractor
- **GOOD**: Domain-agnostic extraction already integrated
- **BAD**: eval() security hole at line 567
- **BAD**: auto_detect_chapters() has CC 18 with nested conditionals
- **BAD**: main() has CC 12 mixing validation, execution, error handling

---

### ✅ Step 2 – Guideline Concept Review & Cross-Referencing

#### 2.1 Open and Review ARCHITECTURE_GUIDELINES ✅ COMPLETE
- [x] Opened: `workflows/base_guideline_generation/output/Architecture Patterns with Python_guideline.json`
- [x] Read Chapter 2: Repository Pattern (pages 25-46)
  * [x] **Summary**: "Explores the Repository pattern for abstracting data persistence and database access. Covers implementing repositories with SQLAlchemy, the ports and adapters (hexagonal) architecture, and separating domain logic from infrastructure concerns."
  * [x] **Key Insight**: Repository abstracts file I/O, enables mocking for tests
  * [x] **Application**: generate_metadata_universal.py currently has direct file operations - needs JsonMetadataRepository abstraction
  * [x] **Benefit**: Testability - can mock repository instead of actual file system
- [x] Read Chapter 13: Dependency Injection (and Bootstrapping) (pages 289-497)
  * [x] **Summary**: "Covers dependency injection and application bootstrapping. Discusses composition root pattern, IoC containers, factory patterns, managing dependencies for testability, and properly wiring up application components during initialization."
  * [x] **Key Insight**: Constructor injection for required dependencies, enables testing with mocks
  * [x] **Application**: auto_detect_chapters() has 5 detection strategies hardcoded - needs Strategy Pattern with ChapterDetectionStrategy protocol
  * [x] **Pattern**: Use Protocol for duck typing, inject strategy via constructor
- [x] Read Chapter 1: Domain Modeling (pages 1-24)
  * [x] **Summary**: "Introduces domain modeling and Domain-Driven Design (DDD) concepts including entities, value objects, and aggregates. Focuses on modeling business logic and domain concepts in Python with proper encapsulation and invariants."
  * [x] **Key Insight**: Value Objects for chapter metadata (ChapterMetadata dataclass already exists - GOOD)
  * [x] **Application**: ChapterMetadata is immutable value object, properly encapsulates chapter data
  * [x] **Note**: Current implementation already follows this pattern
- [x] Chapter 4: Service Layer - confirms service layer separates orchestration from domain logic
- [x] Chapter 5: TDD practices - "High gear" (end-to-end) vs "Low gear" (unit) testing approach needed

**Architectural Patterns to Apply**:
1. **Repository Pattern** (Ch. 2) → Abstract file I/O into JsonMetadataRepository
2. **Strategy Pattern** (Ch. 13 DI context) → Extract 5 chapter detection strategies
3. **Service Layer** (Ch. 4) → Separate orchestration from extraction logic
4. **Ports & Adapters** (Ch. 2) → StatisticalExtractor is already an adapter - GOOD!

#### 2.2 Open and Review PYTHON_GUIDELINES ✅ COMPLETE
- [x] Opened: `workflows/base_guideline_generation/output/Python Distilled_guideline.json`
- [x] Read Chapter 5: Functions (pages 125-162)
  * [x] **Summary**: "Comprehensive coverage of Python functions including parameter passing, return values, lambda functions, closures, decorators, and scope rules. Discusses namespaces, global/nonlocal keywords, and various parameter types."
  * [x] **Key Insight**: Functions should have single purpose, clear parameters, proper return types
  * [x] **Violation in Code**: `auto_detect_chapters()` does 3 things: (1) check JSON for pre-defined chapters (2) scan pages for chapter markers (3) validate chapter numbers
  * [x] **Violation in Code**: `main()` does 5 things: (1) parse args (2) instantiate generator (3) get chapters (4) generate metadata (5) save results
  * [x] **Refactoring Needed**: Extract Method pattern - break into focused functions
- [x] Searched for Exception Handling chapter in Python Distilled
  * [x] **Note**: Python Distilled JSON only covers Chapters 1-9 (doesn't include exception handling chapter)
  * [x] **Security Principle Known**: Never use eval() on untrusted input
  * [x] **Solution**: Python's `ast.literal_eval()` safely evaluates only Python literals (dict, list, tuple, str, int, float, bool, None)
  * [x] **Critical Fix Needed**: Line 567 `chapters = eval(args.chapters)` must become `chapters = ast.literal_eval(args.chapters)`
  * [x] **Risk**: Current code allows arbitrary code execution via command line: `--chapters "__import__('os').system('rm -rf /')"`
- [ ] Search for "Type Hints" annotations
  * [ ] Read annotations for Chapter 19
  * [ ] Extract cross-references: typing.Protocol, TypedDict
  * [ ] Note: Type hints for all public APIs
- [ ] Search for "Testing" annotations
  * [ ] Read annotations for Chapter 35
  * [ ] Extract cross-references: pytest, fixtures
  * [ ] Note: Characterization testing approach
- [ ] Review chapter summaries for identified chapters
- [ ] List specific JSON sections to read in full

#### 2.3 Review Guideline JSON Sections (Targeted Reading)
- [ ] Open: `workflows/base_guideline_generation/output/Architecture_Patterns_with_Python_guideline.json`
  * [ ] Read Chapter 2 section: Repository Pattern
    - [ ] Read `chapter_summary`
    - [ ] Read `concepts` array
    - [ ] Read `text` for implementation details
  * [ ] Read Chapter 9 section: Dependency Injection / Strategy Pattern
    - [ ] Read `chapter_summary`
    - [ ] Read `concepts` array
    - [ ] Read `text` for strategy pattern examples
- [ ] Open: `workflows/base_guideline_generation/output/Learning_Python_Ed6_guideline.json`
  * [ ] Read Chapter 16 section: Function Basics
    - [ ] Read `chapter_summary`
    - [ ] Read `concepts` array (focus on Extract Method)
    - [ ] Read `text` for function design principles
  * [ ] Read Chapter 34 section: Exception Coding Details
    - [ ] Read `chapter_summary`
    - [ ] Read `concepts` array (focus on ast.literal_eval)
    - [ ] Read `text` for safe evaluation patterns
  * [ ] Read Chapter 19 section: Advanced Function Topics
    - [ ] Read `chapter_summary`
    - [ ] Read `concepts` array (focus on type hints)
    - [ ] Read `text` for typing.Protocol examples

---

### ✅ Step 3 – Conflict Identification and Resolution

#### 3.1 Cross-Document Comparison
- [ ] Compare MASTER_IMPLEMENTATION_GUIDE strategy vs DOMAIN_AGNOSTIC_PLAN
  * [ ] MASTER says: "Refactor complexity first"
  * [ ] DOMAIN_AGNOSTIC says: "Replace hardcoded patterns with YAKE"
  * [ ] **Analysis**: Both can be done simultaneously (already documented in plan)
  * [ ] **Resolution**: Follow DOMAIN_AGNOSTIC_PLAN as primary (document priority #2)
  
- [ ] Compare MASTER_IMPLEMENTATION_GUIDE strategy vs ARCHITECTURE_GUIDELINES
  * [ ] MASTER suggests: Repository Pattern for file I/O
  * [ ] ARCHITECTURE confirms: Chapter 2 Repository Pattern
  * [ ] **Analysis**: No conflict, aligned
  * [ ] **Resolution**: Implement Repository Pattern as recommended
  
- [ ] Compare MASTER_IMPLEMENTATION_GUIDE strategy vs PYTHON_GUIDELINES
  * [ ] MASTER suggests: Replace eval() with ast.literal_eval
  * [ ] PYTHON confirms: Chapter 34 safe evaluation
  * [ ] **Analysis**: No conflict, aligned
  * [ ] **Resolution**: Use ast.literal_eval as recommended

#### 3.2 Document Conflicts (if any)
- [ ] **Conflict Assessment**: TDD vs Refactor-First
  * **WBS Item**: All complexity issues require refactoring
  * **Conflicting Guideline**: MASTER suggests refactor, but TDD requires tests first
  * **Nature**: Implementation methodology
  * **Option A**: TDD (tests first) - Pros: safety net • Cons: slower
  * **Option B**: Refactor first - Pros: faster • Cons: no safety net
  * **Option C**: Characterization tests → TDD - Pros: best of both • Cons: two-phase
  * **Recommendation**: Option C (Characterization Testing)
  * **Approval**: ✅ User approved via TDD mandate
  * **Resolution**: Write characterization tests to lock current behavior, then refactor

#### 3.3 Final Conflict Resolution Summary
- [ ] Document all resolved conflicts
- [ ] Confirm no blocking conflicts remain
- [ ] Proceed to TDD implementation

---

## Phase 2: TDD Implementation (RED → GREEN → REFACTOR)

### 🔴 Iteration 1: Characterization Tests (Lock Current Behavior)

**Goal**: Document existing behavior before refactoring  
**Time**: 2 hours  
**Traceability**: PYTHON_GUIDELINES Ch. 35 (Testing), User TDD mandate

#### RED Phase
- [ ] Create test file: `tests/unit/workflows/metadata_extraction/test_generate_metadata_universal_characterization.py`
- [ ] Write failing test: `test_auto_detect_chapters_current_behavior`
  * [ ] Test with sample text containing chapter markers
  * [ ] Verify current detection logic (even if imperfect)
  * [ ] Document expected output format
- [ ] Write failing test: `test_main_happy_path`
  * [ ] Test successful execution with valid inputs
  * [ ] Mock file I/O operations
  * [ ] Verify JSON output structure
- [ ] Write failing test: `test_eval_usage_security_risk` (XFAIL)
  * [ ] Demonstrate eval() vulnerability
  * [ ] Mark as expected failure
  * [ ] Document security risk
- [ ] Run tests: `pytest tests/unit/workflows/metadata_extraction/test_generate_metadata_universal_characterization.py -v`
  * [ ] Verify tests fail (RED)

#### GREEN Phase
- [ ] Implement minimal test fixtures
- [ ] Add necessary imports and mocks
- [ ] Run tests: Verify they pass (documenting current behavior)
  * [ ] `test_auto_detect_chapters_current_behavior` → PASS
  * [ ] `test_main_happy_path` → PASS
  * [ ] `test_eval_usage_security_risk` → XFAIL (expected)

#### REFACTOR Phase
- [ ] Clean up test code
- [ ] Add docstrings explaining characterization approach
- [ ] Organize test fixtures

#### Quality Gate
- [ ] SonarLint: 0 issues in test file
- [ ] Run tests: All pass or XFAIL as expected
- [ ] Code review: Tests accurately document current behavior

---

### 🔴 Iteration 2: Security Fix - Replace eval() with ast.literal_eval

**Goal**: Fix CRITICAL security vulnerability  
**Time**: 1 hour  
**Traceability**: MASTER_IMPLEMENTATION_GUIDE §Security, PYTHON_GUIDELINES Ch. 34, DOMAIN_AGNOSTIC_PLAN §2.1

#### RED Phase
- [ ] Write failing test: `test_safe_eval_with_literal_expression`
  * [ ] Test safe evaluation of dict, list, string, number
  * [ ] Example: `safe_eval("{'key': 'value'}") == {'key': 'value'}`
- [ ] Write failing test: `test_safe_eval_rejects_dangerous_code`
  * [ ] Test rejection of code execution attempts
  * [ ] Example: `safe_eval("__import__('os').system('ls')")` raises ValueError
- [ ] Write failing test: `test_safe_eval_rejects_function_calls`
  * [ ] Test rejection of function call syntax
  * [ ] Example: `safe_eval("print('hello')")` raises ValueError
- [ ] Run tests: Verify failures (function doesn't exist yet)

#### GREEN Phase
- [ ] Read JSON section: Learning_Python_Ed6_guideline.json Ch. 34 (safe evaluation)
- [ ] Implement `safe_eval()` function using `ast.literal_eval()`
  ```python
  import ast
  from typing import Any
  
  def safe_eval(expr: str) -> Any:
      """Safely evaluate Python literal expressions.
      
      Args:
          expr: String containing a Python literal (dict, list, str, num, bool, None)
      
      Returns:
          Evaluated Python object
      
      Raises:
          ValueError: If expression is not a safe literal
      
      Traceability: PYTHON_GUIDELINES Ch. 34 (Exception Coding Details)
      """
      try:
          return ast.literal_eval(expr)
      except (ValueError, SyntaxError) as e:
          raise ValueError(f"Invalid literal expression: {expr}") from e
  ```
- [ ] Add type hints (per PYTHON_GUIDELINES Ch. 19)
- [ ] Run tests: Verify all pass

#### REFACTOR Phase
- [ ] Find all `eval()` calls in generate_metadata_universal.py (line 567 documented)
- [ ] Replace with `safe_eval()` calls
- [ ] Add security comment explaining change
- [ ] Update characterization tests to use safe_eval
- [ ] Run full test suite: Verify no regressions

#### Quality Gate
- [ ] SonarLint: 0 issues
- [ ] SonarQube: Verify security vulnerability removed
- [ ] CodeRabbit: 0 new comments
- [ ] All tests pass (including characterization)
- [ ] Security issue CLOSED ✅

---

### 🔴 Iteration 3: Extract Chapter Detection Strategies (Strategy Pattern)

**Goal**: Reduce `auto_detect_chapters()` CC from 18 to <10  
**Time**: 6 hours  
**Traceability**: MASTER_IMPLEMENTATION_GUIDE §Complexity, ARCHITECTURE_GUIDELINES Ch. 9, DOMAIN_AGNOSTIC_PLAN §2.1

#### RED Phase - Define Strategy Protocol
- [ ] Read JSON section: Architecture_Patterns_with_Python_guideline.json Ch. 9 (Dependency Injection / Strategy)
- [ ] Write failing test: `test_regex_detection_strategy`
  * [ ] Test RegexDetectionStrategy with known pattern
  * [ ] Verify ChapterBoundary objects returned
- [ ] Write failing test: `test_ml_detection_strategy`
  * [ ] Test MLDetectionStrategy (if implemented)
- [ ] Write failing test: `test_toc_detection_strategy`
  * [ ] Test TOC-based detection
- [ ] Write failing test: `test_heuristic_detection_strategy`
  * [ ] Test heuristic approach
- [ ] Write failing test: `test_manual_detection_strategy`
  * [ ] Test manual boundary specification
- [ ] Run tests: Verify failures (strategies don't exist yet)

#### GREEN Phase - Implement Strategy Pattern
- [ ] Create `ChapterDetectionStrategy` protocol
  ```python
  from typing import Protocol, List
  from dataclasses import dataclass
  
  @dataclass
  class ChapterBoundary:
      """Represents a detected chapter boundary."""
      chapter_number: int
      start_page: int
      end_page: int
      title: str
      confidence: float
  
  class ChapterDetectionStrategy(Protocol):
      """Protocol for chapter detection strategies.
      
      Traceability: ARCHITECTURE_GUIDELINES Ch. 9 (Strategy Pattern)
      """
      def detect(self, text: str, **kwargs) -> List[ChapterBoundary]:
          """Detect chapter boundaries in text."""
          ...
  ```
- [ ] Implement `RegexDetectionStrategy`
  ```python
  class RegexDetectionStrategy:
      """Regex-based chapter detection.
      
      Traceability: DOMAIN_AGNOSTIC_PLAN §2.1 (configurable patterns)
      """
      def __init__(self, patterns: List[str]):
          self.patterns = patterns
      
      def detect(self, text: str, **kwargs) -> List[ChapterBoundary]:
          # Implementation using regex patterns
          pass
  ```
- [ ] Implement `TOCDetectionStrategy` (extract TOC and use as guide)
- [ ] Implement `HeuristicDetectionStrategy` (font size, page breaks, etc.)
- [ ] Implement `ManualDetectionStrategy` (user-provided boundaries)
- [ ] Run tests: Verify all pass

#### REFACTOR Phase - Simplify auto_detect_chapters
- [ ] Refactor `auto_detect_chapters()` to use strategies
  ```python
  def auto_detect_chapters(
      text: str,
      strategy: ChapterDetectionStrategy,
      **kwargs
  ) -> List[ChapterBoundary]:
      """Detect chapters using provided strategy.
      
      Args:
          text: Full book text
          strategy: Detection strategy implementation
          **kwargs: Strategy-specific arguments
      
      Returns:
          List of detected chapter boundaries
      
      Traceability:
          - MASTER_IMPLEMENTATION_GUIDE (reduce CC 18 → <10)
          - ARCHITECTURE_GUIDELINES Ch. 9 (Strategy Pattern)
      """
      return strategy.detect(text, **kwargs)
  ```
- [ ] Add factory function for strategy selection
  ```python
  def create_detection_strategy(
      method: str,
      config: Dict[str, Any]
  ) -> ChapterDetectionStrategy:
      """Factory for creating detection strategies.
      
      Traceability: ARCHITECTURE_GUIDELINES Ch. 9 (Dependency Injection)
      """
      strategies = {
          'regex': RegexDetectionStrategy,
          'toc': TOCDetectionStrategy,
          'heuristic': HeuristicDetectionStrategy,
          'manual': ManualDetectionStrategy,
      }
      return strategies[method](**config)
  ```
- [ ] Update all callers of `auto_detect_chapters()`
- [ ] Run full test suite: Verify no regressions

#### Quality Gate
- [ ] Radon CC: `auto_detect_chapters()` now < 10 ✅
- [ ] SonarLint: 0 issues
- [ ] SonarQube: CC reduced, no new issues
- [ ] CodeRabbit: 0 new comments
- [ ] All tests pass
- [ ] Complexity issue #1 RESOLVED ✅

---

### 🔴 Iteration 4: Domain-Agnostic Keyword Extraction (YAKE)

**Goal**: Replace 100+ hardcoded Python patterns with statistical extraction  
**Time**: 12 hours  
**Traceability**: DOMAIN_AGNOSTIC_PLAN §2.1-2.3, MASTER_IMPLEMENTATION_GUIDE §Architecture

#### RED Phase - YAKE Integration
- [ ] Install dependencies: `pip install yake-keyword`
- [ ] Write failing test: `test_yake_keyword_extraction_python_text`
  * [ ] Sample: "Python uses classes and functions for object-oriented programming"
  * [ ] Expected keywords: ["Python", "classes", "functions", "object-oriented", "programming"]
- [ ] Write failing test: `test_yake_keyword_extraction_biology_text`
  * [ ] Sample: "DNA replication involves polymerase enzymes and nucleotides"
  * [ ] Expected keywords: ["DNA", "replication", "polymerase", "enzymes", "nucleotides"]
- [ ] Write failing test: `test_yake_keyword_extraction_architecture_text`
  * [ ] Sample: "Microservices architecture uses distributed systems patterns"
  * [ ] Expected keywords: ["Microservices", "architecture", "distributed", "systems", "patterns"]
- [ ] Run tests: Verify failures

#### GREEN Phase - Implement YAKE Extraction
- [ ] Implement `extract_keywords_yake()`
  ```python
  import yake
  from typing import List, Dict
  
  def extract_keywords_yake(
      text: str,
      language: str = "en",
      top_n: int = 20,
      max_ngram_size: int = 3
  ) -> List[str]:
      """Extract keywords using YAKE algorithm.
      
      Args:
          text: Input text for keyword extraction
          language: Language code (default: en)
          top_n: Number of top keywords to extract
          max_ngram_size: Maximum n-gram size (1-3)
      
      Returns:
          List of extracted keywords (domain-agnostic)
      
      Traceability: DOMAIN_AGNOSTIC_PLAN §2.1 (YAKE extraction)
      """
      kw_extractor = yake.KeywordExtractor(
          lan=language,
          n=max_ngram_size,
          dedupLim=0.9,
          top=top_n,
          features=None
      )
      keywords = kw_extractor.extract_keywords(text)
      return [kw[0] for kw in keywords]  # Extract keyword strings only
  ```
- [ ] Run tests: Verify all pass

#### RED Phase - TF-IDF Integration
- [ ] Install dependencies: `pip install scikit-learn`
- [ ] Write failing test: `test_tfidf_concept_similarity`
  * [ ] Test similarity scoring between chapter and keywords
  * [ ] Verify concepts ranked by relevance
- [ ] Write failing test: `test_tfidf_filters_common_words`
  * [ ] Verify stopwords are filtered out
- [ ] Run tests: Verify failures

#### GREEN Phase - Implement TF-IDF Scoring
- [ ] Implement `score_concepts_tfidf()`
  ```python
  from sklearn.feature_extraction.text import TfidfVectorizer
  from sklearn.metrics.pairwise import cosine_similarity
  import numpy as np
  
  def score_concepts_tfidf(
      chapter_text: str,
      candidate_keywords: List[str],
      top_n: int = 10
  ) -> List[tuple[str, float]]:
      """Score and rank concepts using TF-IDF.
      
      Args:
          chapter_text: Full chapter text
          candidate_keywords: Keywords to score
          top_n: Number of top concepts to return
      
      Returns:
          List of (concept, score) tuples, sorted by relevance
      
      Traceability: DOMAIN_AGNOSTIC_PLAN §2.2 (TF-IDF scoring)
      """
      # Create TF-IDF vectors
      vectorizer = TfidfVectorizer(stop_words='english')
      tfidf_matrix = vectorizer.fit_transform([chapter_text] + candidate_keywords)
      
      # Compute similarity scores
      chapter_vector = tfidf_matrix[0:1]
      keyword_vectors = tfidf_matrix[1:]
      scores = cosine_similarity(chapter_vector, keyword_vectors).flatten()
      
      # Sort and return top N
      scored = list(zip(candidate_keywords, scores))
      scored.sort(key=lambda x: x[1], reverse=True)
      return scored[:top_n]
  ```
- [ ] Run tests: Verify all pass

#### RED Phase - Summa Integration
- [ ] Install dependencies: `pip install summa`
- [ ] Write failing test: `test_summa_summarization_preserves_key_points`
  * [ ] Input: Long chapter text
  * [ ] Output: 200-word summary containing main concepts
- [ ] Write failing test: `test_summa_summarization_configurable_ratio`
  * [ ] Test different summary lengths (10%, 20%, 30%)
- [ ] Run tests: Verify failures

#### GREEN Phase - Implement Summa Summarization
- [ ] Implement `summarize_chapter_summa()`
  ```python
  from summa import summarizer
  
  def summarize_chapter_summa(
      chapter_text: str,
      ratio: float = 0.2,
      word_count: int = None
  ) -> str:
      """Generate extractive summary using Summa.
      
      Args:
          chapter_text: Full chapter text
          ratio: Proportion of text to extract (0.0-1.0)
          word_count: Target word count (overrides ratio)
      
      Returns:
          Extractive summary
      
      Traceability: DOMAIN_AGNOSTIC_PLAN §2.3 (Summa summarization)
      """
      if word_count:
          return summarizer.summarize(chapter_text, words=word_count)
      else:
          return summarizer.summarize(chapter_text, ratio=ratio)
  ```
- [ ] Run tests: Verify all pass

#### REFACTOR Phase - Replace Hardcoded Patterns
- [ ] Create configuration file: `config/keyword_extraction.json`
  ```json
  {
    "yake": {
      "language": "en",
      "top_n": 20,
      "max_ngram_size": 3
    },
    "tfidf": {
      "top_n": 10,
      "stop_words": "english"
    },
    "summa": {
      "ratio": 0.2,
      "word_count": 200
    }
  }
  ```
- [ ] Remove all 100+ hardcoded Python-specific regex patterns
- [ ] Replace with statistical extraction pipeline:
  ```python
  def extract_metadata_domain_agnostic(
      chapter_text: str,
      config: Dict[str, Any]
  ) -> Dict[str, Any]:
      """Extract metadata using domain-agnostic methods.
      
      Traceability: DOMAIN_AGNOSTIC_PLAN (complete implementation)
      """
      # Step 1: Extract keywords with YAKE
      keywords = extract_keywords_yake(
          chapter_text,
          **config['yake']
      )
      
      # Step 2: Score concepts with TF-IDF
      concepts = score_concepts_tfidf(
          chapter_text,
          keywords,
          top_n=config['tfidf']['top_n']
      )
      
      # Step 3: Generate summary with Summa
      summary = summarize_chapter_summa(
          chapter_text,
          **config['summa']
      )
      
      return {
          'keywords': keywords,
          'concepts': [c[0] for c in concepts],
          'concept_scores': dict(concepts),
          'summary': summary
      }
  ```
- [ ] Update `main()` to use new pipeline
- [ ] Run full test suite: Verify no regressions
- [ ] Test with non-Python books (biology, architecture, etc.)

#### Quality Gate
- [ ] All hardcoded patterns removed ✅
- [ ] Domain-agnostic extraction working for multiple domains ✅
- [ ] SonarLint: 0 issues
- [ ] SonarQube: 0 new issues
- [ ] CodeRabbit: 0 new comments
- [ ] All tests pass (including domain-agnostic tests)
- [ ] Architecture issue RESOLVED ✅

---

### 🔴 Iteration 5: Repository Pattern for File I/O

**Goal**: Abstract file access for testability  
**Time**: 4 hours  
**Traceability**: MASTER_IMPLEMENTATION_GUIDE §Architecture, ARCHITECTURE_GUIDELINES Ch. 2

#### RED Phase - Define Repository Protocol
- [ ] Read JSON section: Architecture_Patterns_with_Python_guideline.json Ch. 2 (Repository Pattern)
- [ ] Write failing test: `test_json_metadata_repository_save`
  * [ ] Test saving metadata to JSON file
  * [ ] Verify file created with correct content
- [ ] Write failing test: `test_json_metadata_repository_load`
  * [ ] Test loading metadata from JSON file
  * [ ] Verify correct deserialization
- [ ] Write failing test: `test_json_metadata_repository_exists`
  * [ ] Test checking if metadata exists
- [ ] Write failing test: `test_metadata_repository_protocol`
  * [ ] Verify protocol compliance (duck typing)
- [ ] Run tests: Verify failures

#### GREEN Phase - Implement Repository
- [ ] Create `MetadataRepository` protocol
  ```python
  from typing import Protocol, Dict, Any
  from pathlib import Path
  
  class MetadataRepository(Protocol):
      """Protocol for metadata persistence.
      
      Traceability: ARCHITECTURE_GUIDELINES Ch. 2 (Repository Pattern)
      """
      def save(self, book_name: str, metadata: Dict[str, Any]) -> None:
          """Save metadata for a book."""
          ...
      
      def load(self, book_name: str) -> Dict[str, Any]:
          """Load metadata for a book."""
          ...
      
      def exists(self, book_name: str) -> bool:
          """Check if metadata exists for a book."""
          ...
  ```
- [ ] Implement `JsonMetadataRepository`
  ```python
  import json
  from pathlib import Path
  from typing import Dict, Any
  
  class JsonMetadataRepository:
      """JSON-based metadata repository.
      
      Traceability: ARCHITECTURE_GUIDELINES Ch. 2 (Repository Pattern)
      """
      def __init__(self, base_path: Path):
          self.base_path = base_path
          self.base_path.mkdir(parents=True, exist_ok=True)
      
      def save(self, book_name: str, metadata: Dict[str, Any]) -> None:
          """Save metadata to JSON file."""
          path = self._get_path(book_name)
          with open(path, 'w', encoding='utf-8') as f:
              json.dump(metadata, f, indent=2, ensure_ascii=False)
      
      def load(self, book_name: str) -> Dict[str, Any]:
          """Load metadata from JSON file."""
          path = self._get_path(book_name)
          with open(path, 'r', encoding='utf-8') as f:
              return json.load(f)
      
      def exists(self, book_name: str) -> bool:
          """Check if metadata file exists."""
          return self._get_path(book_name).exists()
      
      def _get_path(self, book_name: str) -> Path:
          """Get file path for book metadata."""
          safe_name = book_name.replace('/', '_').replace('\\', '_')
          return self.base_path / f"{safe_name}_metadata.json"
  ```
- [ ] Run tests: Verify all pass

#### REFACTOR Phase - Inject Repository
- [ ] Refactor `main()` to accept repository as dependency
  ```python
  def main(
      input_file: Path,
      repository: MetadataRepository,
      detection_strategy: ChapterDetectionStrategy,
      config: Dict[str, Any]
  ) -> None:
      """Main metadata extraction workflow.
      
      Args:
          input_file: Path to input PDF/text file
          repository: Metadata persistence layer
          detection_strategy: Chapter detection strategy
          config: Extraction configuration
      
      Traceability:
          - ARCHITECTURE_GUIDELINES Ch. 2 (Repository Pattern)
          - ARCHITECTURE_GUIDELINES Ch. 9 (Dependency Injection)
      """
      # Extract metadata
      metadata = extract_metadata_domain_agnostic(...)
      
      # Save via repository
      book_name = input_file.stem
      repository.save(book_name, metadata)
  ```
- [ ] Update CLI to instantiate repository
- [ ] Run full test suite: Verify no regressions
- [ ] Mock repository in unit tests for speed

#### Quality Gate
- [ ] Repository pattern implemented ✅
- [ ] All file I/O abstracted ✅
- [ ] Tests use mocked repository ✅
- [ ] SonarLint: 0 issues
- [ ] SonarQube: 0 new issues
- [ ] CodeRabbit: 0 new comments
- [ ] All tests pass

---

### 🔴 Iteration 6: Reduce main() Complexity

**Goal**: Reduce `main()` CC from 12 to <10  
**Time**: 3 hours  
**Traceability**: MASTER_IMPLEMENTATION_GUIDE §Complexity, PYTHON_GUIDELINES Ch. 16

#### RED Phase - Extract Validation Logic
- [ ] Read JSON section: Learning_Python_Ed6_guideline.json Ch. 16 (Function Design)
- [ ] Write failing test: `test_validate_input_file_valid`
  * [ ] Test validation passes for valid PDF
- [ ] Write failing test: `test_validate_input_file_invalid_extension`
  * [ ] Test validation fails for non-PDF
- [ ] Write failing test: `test_validate_input_file_not_found`
  * [ ] Test validation fails for missing file
- [ ] Run tests: Verify failures

#### GREEN Phase - Extract Functions
- [ ] Extract validation logic:
  ```python
  def validate_input_file(file_path: Path) -> None:
      """Validate input file exists and has correct format.
      
      Args:
          file_path: Path to input file
      
      Raises:
          FileNotFoundError: If file doesn't exist
          ValueError: If file format is invalid
      
      Traceability: PYTHON_GUIDELINES Ch. 16 (Extract Method)
      """
      if not file_path.exists():
          raise FileNotFoundError(f"Input file not found: {file_path}")
      
      if file_path.suffix.lower() not in ['.pdf', '.txt']:
          raise ValueError(f"Invalid file format: {file_path.suffix}")
  ```
- [ ] Extract error handling logic:
  ```python
  def handle_extraction_error(error: Exception, book_name: str) -> None:
      """Handle and log extraction errors.
      
      Traceability: PYTHON_GUIDELINES Ch. 34 (Exception Handling)
      """
      logger.error(f"Failed to extract metadata for {book_name}: {error}")
      # Add telemetry, notifications, etc.
  ```
- [ ] Extract reporting logic:
  ```python
  def report_extraction_success(book_name: str, metadata: Dict) -> None:
      """Report successful extraction with statistics.
      
      Traceability: PYTHON_GUIDELINES Ch. 16 (Single Responsibility)
      """
      logger.info(f"Extracted metadata for {book_name}")
      logger.info(f"  Chapters: {len(metadata.get('chapters', []))}")
      logger.info(f"  Keywords: {len(metadata.get('keywords', []))}")
      logger.info(f"  Concepts: {len(metadata.get('concepts', []))}")
  ```
- [ ] Run tests: Verify all pass

#### REFACTOR Phase - Simplify main()
- [ ] Refactor `main()` to use extracted functions:
  ```python
  def main(
      input_file: Path,
      repository: MetadataRepository,
      detection_strategy: ChapterDetectionStrategy,
      config: Dict[str, Any]
  ) -> None:
      """Main metadata extraction workflow (simplified).
      
      Traceability: MASTER_IMPLEMENTATION_GUIDE (reduce CC 12 → <10)
      """
      # Validate input
      validate_input_file(input_file)
      
      try:
          # Extract metadata
          book_name = input_file.stem
          metadata = extract_metadata_domain_agnostic(
              input_file,
              detection_strategy,
              config
          )
          
          # Persist metadata
          repository.save(book_name, metadata)
          
          # Report success
          report_extraction_success(book_name, metadata)
          
      except Exception as e:
          handle_extraction_error(e, book_name)
          raise
  ```
- [ ] Run full test suite: Verify no regressions

#### Quality Gate
- [ ] Radon CC: `main()` now < 10 ✅
- [ ] SonarLint: 0 issues
- [ ] SonarQube: CC reduced, no new issues
- [ ] CodeRabbit: 0 new comments
- [ ] All tests pass
- [ ] Complexity issue #2 RESOLVED ✅

---

### 🔴 Iteration 7: Type Hints and Documentation

**Goal**: Add complete type hints and docstrings  
**Time**: 2 hours  
**Traceability**: PYTHON_GUIDELINES Ch. 19 (Type Hints), MASTER_IMPLEMENTATION_GUIDE §Documentation

#### RED Phase - Type Hints
- [ ] Install: `pip install mypy`
- [ ] Run mypy: `mypy workflows/metadata_extraction/scripts/generate_metadata_universal.py`
- [ ] Document all type errors found

#### GREEN Phase - Add Type Hints
- [ ] Add type hints to all public functions
- [ ] Add type hints to all private functions
- [ ] Use `typing.Protocol` for strategy interfaces
- [ ] Use `typing.TypedDict` for metadata structures
- [ ] Run mypy: Verify 0 errors

#### REFACTOR Phase - Complete Documentation
- [ ] Add module docstring with overview
- [ ] Add docstrings to all functions (including Args, Returns, Raises, Traceability)
- [ ] Add inline comments for complex logic
- [ ] Generate API documentation: `pydoc generate_metadata_universal`

#### Quality Gate
- [ ] Mypy: 0 type errors ✅
- [ ] All functions have type hints ✅
- [ ] All functions have docstrings ✅
- [ ] SonarLint: 0 issues
- [ ] Documentation complete ✅

---

## Phase 3: Integration Testing

**Goal**: Verify end-to-end functionality  
**Time**: 3 hours  
**Traceability**: User TDD mandate, PYTHON_GUIDELINES Ch. 35

### Integration Tests

- [ ] Create: `tests/integration/test_generate_metadata_universal_integration.py`

#### Test 1: End-to-End Python Book
- [ ] Test complete extraction for Python book
- [ ] Verify all metadata fields populated
- [ ] Verify keywords are Python-related
- [ ] Verify concepts are relevant
- [ ] Verify summary is coherent

#### Test 2: End-to-End Non-Python Book
- [ ] Test complete extraction for biology book
- [ ] Verify domain-agnostic extraction works
- [ ] Verify no Python-specific keywords appear
- [ ] Verify biology concepts detected

#### Test 3: End-to-End Architecture Book
- [ ] Test complete extraction for architecture book
- [ ] Verify architectural patterns detected
- [ ] Verify concepts are architecture-related

#### Test 4: Repository Persistence
- [ ] Test metadata is saved correctly
- [ ] Test metadata can be loaded back
- [ ] Test file format is valid JSON

#### Test 5: Strategy Selection
- [ ] Test different detection strategies
- [ ] Verify strategy factory works
- [ ] Verify each strategy produces valid output

### Quality Gate
- [ ] All integration tests pass ✅
- [ ] End-to-end workflows functional ✅
- [ ] Test coverage > 80% (run: `pytest --cov`)

---

## Phase 4: Final Quality Gates

**Goal**: Ensure all quality standards met  
**Time**: 2 hours  
**Traceability**: User quality gate requirements

### 4.1 SonarLint (Real-time)
- [ ] Run SonarLint during all coding
- [ ] Fix all issues immediately
- [ ] Final check: 0 issues remaining

### 4.2 SonarQube (Project Scan)
- [ ] Run: `sonar-scanner -Dsonar.projectKey=llm-document-enhancer`
- [ ] Verify: 0 new bugs
- [ ] Verify: 0 new vulnerabilities
- [ ] Verify: 0 new code smells
- [ ] Verify: Security hotspot closed (eval() removal)
- [ ] Target: A rating maintained

### 4.3 CodeRabbit (PR Review)
- [ ] Create PR: "refactor: generate_metadata_universal.py - domain-agnostic extraction"
- [ ] Run CodeRabbit analysis
- [ ] Address all comments
- [ ] Get approval

### 4.4 Radon Complexity Verification
- [ ] Run: `radon cc workflows/metadata_extraction/scripts/generate_metadata_universal.py -s -a`
- [ ] Verify: `auto_detect_chapters()` CC < 10 ✅
- [ ] Verify: `main()` CC < 10 ✅
- [ ] Verify: All functions CC < 10 ✅
- [ ] Verify: Average complexity < 5 ✅

### 4.5 Test Coverage
- [ ] Run: `pytest tests/unit/workflows/metadata_extraction/ --cov --cov-report=html`
- [ ] Verify: Coverage > 80% for generate_metadata_universal.py ✅
- [ ] Review uncovered lines
- [ ] Add tests for missing coverage

### 4.6 Manual Testing
- [ ] Run with Python book: `Learning_Python_Ed6.json`
- [ ] Run with architecture book: `Architecture_Patterns_with_Python.json`
- [ ] Run with biology book (if available)
- [ ] Verify outputs are correct
- [ ] Verify no regressions in functionality

---

## Phase 5: Documentation and Handoff

**Goal**: Update all documentation  
**Time**: 1 hour  
**Traceability**: Project documentation standards

### Documentation Updates

- [ ] Update MASTER_IMPLEMENTATION_GUIDE.md
  * [ ] Mark `generate_metadata_universal.py` as ✅ COMPLETE
  * [ ] Update complexity metrics (CC 18→<10, CC 12→<10)
  * [ ] Update security status (eval() removed)
  * [ ] Update architecture compliance
  * [ ] Update test coverage (0%→>80%)

- [ ] Update DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md
  * [ ] Mark §2.1 (YAKE) as ✅ IMPLEMENTED
  * [ ] Mark §2.2 (TF-IDF) as ✅ IMPLEMENTED
  * [ ] Mark §2.3 (Summa) as ✅ IMPLEMENTED
  * [ ] Mark configuration-driven approach as ✅ IMPLEMENTED

- [ ] Update TODO_FILE1_generate_metadata_universal.md
  * [ ] Mark all items as complete
  * [ ] Add completion timestamp
  * [ ] Add final metrics summary

- [ ] Create summary document: `FILE1_COMPLETION_REPORT.md`
  * [ ] List all issues resolved
  * [ ] List all tests added
  * [ ] List all quality gate results
  * [ ] List all traceability references
  * [ ] Add before/after metrics

---

## Acceptance Criteria (Final Verification)

### From MASTER_IMPLEMENTATION_GUIDE
- [ ] ✅ All eval() calls replaced with ast.literal_eval (SECURITY)
- [ ] ✅ `auto_detect_chapters()` CC reduced from 18 to < 10 (COMPLEXITY)
- [ ] ✅ `main()` CC reduced from 12 to < 10 (COMPLEXITY)
- [ ] ✅ 5 detection strategies extracted into separate classes (SRP)
- [ ] ✅ Repository pattern for file I/O (ARCHITECTURE)
- [ ] ✅ Type hints on all functions (PYTHON)
- [ ] ✅ Docstrings on all public functions (DOCUMENTATION)
- [ ] ✅ Unit test coverage > 80% (TESTING)
- [ ] ✅ Integration tests for full workflow (TESTING)
- [ ] ✅ SonarQube: 0 new issues (QUALITY)
- [ ] ✅ CodeRabbit: 0 new issues (QUALITY)

### From DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN
- [ ] ✅ YAKE keyword extraction implemented (DOMAIN-AGNOSTIC)
- [ ] ✅ TF-IDF concept scoring implemented (DOMAIN-AGNOSTIC)
- [ ] ✅ Summa summarization implemented (DOMAIN-AGNOSTIC)
- [ ] ✅ Configuration-driven extraction (no hardcoded patterns)
- [ ] ✅ Works with non-Python books (biology, architecture, etc.)

### From User TDD Mandate
- [ ] ✅ All work done using RED → GREEN → REFACTOR
- [ ] ✅ Tests written before implementation
- [ ] ✅ Characterization tests for existing behavior
- [ ] ✅ No code written without test coverage

---

## Summary: File #1 Completion

**Start Date**: November 24, 2025  
**Estimated End Date**: November 27, 2025 (3.5 days @ 8 hrs/day)  
**Actual End Date**: _TBD_

**Issues Resolved**:
- 3 Complexity issues (CC 18, 12, + mixed abstractions)
- 1 Security issue (eval() vulnerability)
- 1 Architecture issue (100+ hardcoded patterns)
- 1 Testing issue (0% coverage → >80%)

**Lines Changed**: _TBD_  
**Tests Added**: _TBD_  
**Test Coverage**: 0% → >80%

**Quality Metrics**:
- Cyclomatic Complexity: Avg 18 → <5
- Security Vulnerabilities: 1 → 0
- Code Smells: _TBD_ → 0
- Test Coverage: 0% → >80%
- Architecture Compliance: 74% → 85%+

**Next File**: `detect_poor_ocr.py` (File #2)

---

## Notes and Lessons Learned

- [ ] Document any challenges encountered
- [ ] Document any deviations from plan
- [ ] Document any improvements to TDD process
- [ ] Document any reusable patterns for next files

---

**STATUS**: 🔄 READY TO BEGIN  
**Current Phase**: Phase 1 - Document Analysis  
**Current Step**: Step 1.1 - Review MASTER_IMPLEMENTATION_GUIDE.md
