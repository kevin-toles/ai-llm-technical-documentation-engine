# Keyword Extraction Test Plan - Implementation Addendum

**Date:** November 29, 2025  
**Status:** FINALIZED - Ready for Execution  
**Related:** KEYWORD_EXTRACTION_TEST_PLAN.md  

---

## 1. Final Configuration Status

### Test Profiles (4 Total)

| Profile | YAKE top_n | N-gram | dedupLim | Stem Dedup | Threshold | Status |
|---------|-----------|--------|----------|------------|-----------|--------|
| **baseline** | 10 | 3 | 0.9 | OFF | 0.7 | ✅ Configured |
| **current** | 20 | 3 | 0.9 | ON | 0.7 | ✅ Configured |
| **moderate** | 25 | 4 | 0.85 | ON | 0.6 | ✅ Configured |
| **aggressive** | 35 | 5 | 0.8 | ON | 0.5 | ✅ Configured |

**Configuration File:** `config/extraction_profiles.json`

### LLM Evaluators (5 Available, 3 Usable)

| Provider | Model | API Key | Status | Notes |
|----------|-------|---------|--------|-------|
| **Gemini** | gemini-2.5-flash | ✅ Set | ✅ READY | 50 models available |
| **Claude** | claude-sonnet-4-20250514 | ✅ Set | ✅ READY | Connected |
| **OpenAI** | gpt-4o | ✅ Set | ✅ READY | 99 models available |
| DeepSeek | deepseek-chat | ✅ Set | ⚠️ Needs Credits | Models list works |
| DeepSeek | deepseek-reasoner | ✅ Set | ⚠️ Needs Credits | Models list works |

**API Keys Location:** `~/.zshrc` (loaded via environment variables)

### Test Matrix

```
4 profiles × 3 LLMs = 12 evaluations
12 evaluations × 5 criteria = 60 individual scores
```

---

## 2. Actual LLM Evaluation Prompts

### System Prompt
```
You are an expert at evaluating NLP extraction quality. Always respond with valid JSON.
```

### Evaluation Prompt Template

```
You are evaluating the quality of automated keyword extraction for a technical book chapter.

## Context
{context}

## Extracted Data

### Keywords (first 30):
{json.dumps(keywords, indent=2)}

### Key Concepts (first 20):
{json.dumps(concepts, indent=2)}

### Related Chapters (first 10):
{json.dumps(related_chapters, indent=2)}

## Evaluation Criteria

Please evaluate on a scale of 1-10 for each criterion:

1. **Keyword Quality** (1-10): Are keywords relevant, specific, and diverse? 
   Do they avoid redundant variants (e.g., "model" vs "models")?

2. **Concept Coverage** (1-10): Do the concepts capture the main themes of 
   the chapter? Are they appropriately abstract?

3. **Navigation Utility** (1-10): Would these keywords and related chapters 
   help a reader navigate the book effectively?

4. **Deduplication Quality** (1-10): Are there redundant or near-duplicate 
   terms? Rate higher if terms are unique and diverse.

5. **Cross-Reference Value** (1-10): Do the related chapters make sense? 
   Would a reader find value in following these connections?

## Response Format

Respond with JSON only:
```json
{
  "scores": {
    "keyword_quality": <1-10>,
    "concept_coverage": <1-10>,
    "navigation_utility": <1-10>,
    "deduplication_quality": <1-10>,
    "cross_reference_value": <1-10>
  },
  "overall_score": <1-10>,
  "strengths": ["<strength 1>", "<strength 2>"],
  "weaknesses": ["<weakness 1>", "<weakness 2>"],
  "specific_issues": ["<issue 1>", "<issue 2>"],
  "recommendations": ["<recommendation 1>", "<recommendation 2>"]
}
```
```

**Implementation:** `scripts/llm_evaluation.py` → `create_evaluation_prompt()`

---

## 3. Objective Verification Metrics

### Statistical Measures (Calculated Automatically)

The evaluation includes **objective statistical metrics** alongside LLM scores:

#### Diversity Metrics
- **Unique Keywords Count:** Total unique keywords extracted
- **Diversity Ratio:** `unique_keywords / total_keyword_instances`
- **Average Frequency:** How often each keyword appears

#### Deduplication Metrics
- **Potential Duplicate Groups:** Stem-based duplicate detection
- **Duplicate Examples:** Sample of found duplicates
- **N-gram Distribution:** 1-word, 2-word, 3-word, 4+ word counts

#### Coverage Metrics
- **Chapters Processed:** Number of chapters analyzed
- **Keywords per Chapter:** Distribution statistics
- **Concept Density:** Concepts per page

**Implementation:** `scripts/run_comprehensive_evaluation.py` → `calculate_objective_metrics()`

### Verification Against Ground Truth

#### Baseline Comparison
```python
# Compare against known baseline (before enhancement)
BASELINE_METRICS = {
    "unique_keywords": 383,
    "diversity_ratio": 0.XX,  # To be measured
    "duplicate_groups": ~20-30  # Estimated
}

# Current enhancement
CURRENT_METRICS = {
    "unique_keywords": 404,
    "improvement": "+5.48%",
    "duplicate_groups": 0  # Target
}
```

#### Inter-Rater Reliability
```python
# Cross-validate LLM scores
- Calculate variance across 3 LLM evaluators
- Flag high-variance scores for human review
- Compute Cohen's Kappa if possible
```

---

## 4. Updated Test Execution Plan

### Phase 1: Pre-Validation ✅ COMPLETE
- [x] TDD test suite (13/13 tests passing)
- [x] Static analysis (mypy, SonarQube)
- [x] Git commits pushed
- [x] Initial validation (5.48% improvement quantified)

### Phase 2: Infrastructure Setup ✅ COMPLETE
- [x] API keys configured (Gemini, Claude, OpenAI)
- [x] Test profiles defined (baseline, current, moderate, aggressive)
- [x] Evaluation scripts created
- [x] Comprehensive evaluation pipeline ready

### Phase 3: Extraction Runs 🔄 PENDING
```bash
# Run all 4 profiles with full extraction
python scripts/run_comprehensive_evaluation.py --run-all
```

**Estimated Time:** 2-4 hours (depends on book size)

**Outputs:**
- 4 extraction output directories
- 4 objective metrics reports
- Profile configuration records

### Phase 4: LLM Evaluation 🔄 PENDING
```bash
# Evaluate each profile with 3 LLMs
# (Automatically triggered by --run-all)
```

**Estimated Time:** 1-2 hours (API calls)

**Outputs:**
- 12 LLM evaluation results (4 profiles × 3 LLMs)
- 60 individual criterion scores
- Aggregate comparison report

### Phase 5: Analysis 🔄 PENDING
```bash
# Analyze results
python scripts/run_comprehensive_evaluation.py --analyze-results
```

**Outputs:**
- Rankings by LLM score
- Objective metrics comparison
- Diversity improvement quantification
- Duplicate reduction analysis

### Phase 6: Documentation 🔄 PENDING
```bash
# Generate comprehensive writeup
python scripts/generate_implementation_writeup.py \\
  --output docs/KEYWORD_DEDUPLICATION_WRITEUP.md
```

**Outputs:**
- Full architecture mapping
- Problem/solution/results documentation
- Codebase state at each point
- Git history
- Lessons learned

---

## 5. Answers to Specific Questions

### Q1: Script Configuration for Aggregates and Models

**Answer:** ✅ YES

**Aggregates (4 profiles):**
- Defined in `config/extraction_profiles.json`
- Loaded by `scripts/run_extraction_tests.py`
- Applied via environment variables
- `statistical_extractor.py` reads env vars ✅ (just updated)

**Models (3 usable):**
- Configured in `scripts/llm_evaluation.py`
- API keys set in `~/.zshrc` ✅
- Connection tested: Gemini, Claude, OpenAI ✅
- DeepSeek available but needs credits ⚠️

**Integration:**
- `scripts/run_comprehensive_evaluation.py` orchestrates everything
- Single command: `--run-all` executes full pipeline

---

### Q2: Test Plan Updated

**Answer:** ✅ YES - This document

**Updates:**
- Reduced from 12 to 5 LLM models (3 usable)
- Added actual prompt text (see Section 2)
- Included objective metrics (see Section 3)
- Finalized test matrix: 4 profiles × 3 LLMs = 12 evaluations
- Added execution timeline and commands

---

### Q3: LLM Prompts Included

**Answer:** ✅ YES - See Section 2

**Prompt Components:**
1. System prompt (instructs JSON response)
2. Context (book title, chapter title)
3. Extracted data (keywords, concepts, related chapters)
4. Evaluation criteria (5 dimensions, 1-10 scale)
5. Response format (structured JSON schema)

**Reviewable at:** Section 2 above, or in code:
- `scripts/llm_evaluation.py` lines ~170-240

---

### Q4: Objective Verification

**Answer:** ✅ YES - Multi-level verification

**Level 1: Statistical Metrics** (Objective)
- Unique keyword count
- Diversity ratio
- Duplicate detection
- N-gram distribution

**Level 2: LLM Evaluation** (Subjective but Cross-Validated)
- 3 independent LLM assessments
- 5 criteria per assessment
- Aggregate scoring
- Variance analysis

**Level 3: Baseline Comparison** (Ground Truth)
- Compare vs. pre-enhancement state (383 keywords)
- Measure improvement (+5.48% already validated)
- Track duplicate reduction

**Level 4: Human Validation** (Optional)
- Manual review of high-variance scores
- Spot-check duplicate groups
- Verify edge cases

**What We're Testing Against:**
1. **Pre-enhancement baseline:** 383 unique keywords, ~20-30 duplicate groups
2. **Expected improvement:** +5-10% unique keywords, 0 duplicate groups
3. **Quality maintenance:** LLM scores should not decrease
4. **Diversity increase:** More unique terms in same slot count

---

### Q5: Final Writeup Automation

**Answer:** ✅ YES - Automated script created

**Tool:** `scripts/generate_implementation_writeup.py`

**Generates:**
- Architecture state mapping (before/after)
- Component diagrams
- Data flow diagrams
- File structure with line counts
- Git commit history
- Problem identification
- Solution design
- Implementation details
- Results and validation
- Lessons learned
- Future improvements

**Codebase Mapping:**
- Scans all relevant files
- Counts lines, calculates sizes
- Maps dependencies
- Traces data flows
- Documents each decision point

**Output:** `docs/KEYWORD_DEDUPLICATION_WRITEUP.md` (20+ pages)

---

## 6. Execution Checklist

### Ready to Execute

- [x] All scripts created and tested
- [x] API keys configured
- [x] Test profiles defined
- [x] Environment variables working
- [x] Statistical extractor updated
- [x] Objective metrics implemented
- [x] LLM evaluation prompts finalized
- [x] Documentation generator ready

### Execute Now

```bash
# 1. Run full evaluation (2-6 hours total)
cd /Users/kevintoles/POC/llm-document-enhancer
python scripts/run_comprehensive_evaluation.py --run-all \\
  --models gemini claude openai

# 2. Analyze results
python scripts/run_comprehensive_evaluation.py --analyze-results

# 3. Generate writeup
python scripts/generate_implementation_writeup.py \\
  --output docs/KEYWORD_DEDUPLICATION_WRITEUP.md
```

---

## 7. Expected Outputs Summary

### Quantitative Outputs

| Metric | Baseline | Current | Moderate | Aggressive |
|--------|----------|---------|----------|------------|
| Unique Keywords | ~380 | ~404 | TBD | TBD |
| Diversity Ratio | TBD | TBD | TBD | TBD |
| Duplicate Groups | ~25 | 0 | 0 | 0 |
| LLM Avg Score | TBD | TBD | TBD | TBD |
| Keyword Quality | TBD | TBD | TBD | TBD |
| Dedup Quality | TBD | TBD | TBD | TBD |

### Qualitative Outputs

- **Strengths:** Identified by 3 LLMs per profile
- **Weaknesses:** Identified by 3 LLMs per profile
- **Recommendations:** Actionable improvements
- **Rankings:** Best to worst profile

### Documentation Outputs

- Comprehensive 20+ page writeup
- Architecture diagrams
- Decision documentation
- Results validation
- Lessons learned

---

**Status:** READY FOR EXECUTION  
**Next Action:** Run `python scripts/run_comprehensive_evaluation.py --run-all`  
**Estimated Completion:** 4-6 hours  

