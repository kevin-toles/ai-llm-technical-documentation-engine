# Keyword Extraction Enhancement Test Plan

**Document Version:** 1.0  
**Created:** 2025-11-29  
**Author:** GitHub Copilot  
**Branch:** `feature/keyword-deduplication-enhancement`

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Current State Assessment](#current-state-assessment)
3. [Problem Statement](#problem-statement)
4. [Proposed Solution](#proposed-solution)
5. [Implementation Progress](#implementation-progress)
6. [Complete Parameter Matrix](#complete-parameter-matrix)
7. [Test Configurations](#test-configurations)
8. [LLM Evaluation Framework](#llm-evaluation-framework)
9. [Execution Plan](#execution-plan)
10. [Success Criteria](#success-criteria)

---

## 1. Executive Summary

This test plan documents a systematic evaluation of keyword extraction and cross-referencing quality improvements in the LLM Document Enhancer application. We are testing 4 parameter configurations across 11 tunable parameters, with quality assessment performed by multiple LLM providers.

### Key Metrics
- **+5.48%** increase in unique keywords (383 → 404)
- **1.95x** replacement ratio (43 new terms / 22 removed)
- **10.64%** of new keyword set consists of brand new diverse terms

---

## 2. Current State Assessment

### 2.1 Application Architecture

```
llm-document-enhancer/
├── workflows/
│   ├── pdf_to_json/                    # Tab 1: PDF → JSON conversion
│   │   └── scripts/
│   │       ├── convert_pdf_to_json.py
│   │       ├── chapter_segmenter.py
│   │       └── adapters/
│   │           ├── pdf_converter.py
│   │           └── unstructured_extractor.py
│   │
│   ├── metadata_extraction/            # Tab 2: Keyword/Concept extraction
│   │   └── scripts/
│   │       ├── generate_metadata_universal.py
│   │       ├── adapters/
│   │       │   └── statistical_extractor.py  ← PRIMARY MODIFICATION TARGET
│   │       └── strategies/
│   │           ├── predefined_strategy.py
│   │           ├── toc_parser_strategy.py
│   │           ├── regex_pattern_strategy.py
│   │           └── duplicate_filter_strategy.py
│   │
│   ├── taxonomy_setup/                 # Tab 3: Taxonomy generation
│   │   └── output/
│   │       └── AI-ML_taxonomy_20251128.json
│   │
│   ├── metadata_enrichment/            # Tab 4: Cross-referencing & enrichment
│   │   └── scripts/
│   │       ├── enrich_metadata_per_book.py
│   │       ├── semantic_similarity_engine.py
│   │       ├── topic_clusterer.py
│   │       └── tier_relationship_engine.py
│   │
│   ├── base_guideline_generation/      # Tab 5: Guideline generation
│   │   └── scripts/
│   │       └── chapter_generator_all_text.py
│   │
│   └── llm_enhancement/                # Tab 6: LLM enhancement
│       └── scripts/
│           └── (LLM API integration)
│
├── config/
│   ├── settings.py
│   ├── extraction_profiles.json        ← NEW: Parameter configurations
│   └── validation_rules.json
│
├── scripts/
│   ├── validate_deduplication_changes.py
│   ├── run_enrichment_with_validation.py
│   └── llm_cross_reference_evaluation.py  ← NEW: Multi-LLM evaluation
│
└── outputs/
    └── archive/
        ├── baseline_from_git/          # Original pre-enhancement
        ├── test_current/               # Current (top_n=20, dedup ON)
        ├── test_moderate/              # Moderate (top_n=25)
        └── test_aggressive/            # Aggressive (top_n=35)
```

### 2.2 Key Components Modified

| Component | File | Changes Made |
|-----------|------|--------------|
| StatisticalExtractor | `statistical_extractor.py` | Added stem-based deduplication, n-gram cleanup |
| Keyword Extraction | `statistical_extractor.py` | Changed `top_n` default from 10 → 20 |
| Helper Functions | `statistical_extractor.py` | Added `_get_word_stem()`, `_deduplicate_by_stem()`, `_clean_ngram_duplicates()`, `_get_phrase_stem_signature()` |

### 2.3 Data Flow

```
PDF → JSON → Metadata Extraction → Enrichment → Guideline → LLM Enhancement
         ↓                ↓              ↓
    Raw Text      Keywords/Concepts  Cross-References
                  (YAKE + Summa)     (TF-IDF + Cosine)
```

---

## 3. Problem Statement

### 3.1 Original Issues
1. **Duplicate keywords**: "model" and "models" both appearing, wasting extraction slots
2. **Low diversity**: Same word forms repeated across chapters
3. **Noisy n-grams**: Phrases like "Models Models Applications" appearing
4. **Limited extraction**: Only 10 keywords per chapter (insufficient for cross-referencing)

### 3.2 Impact
- Poor cross-reference discovery
- Redundant navigation paths
- Missed conceptual connections between chapters

---

## 4. Proposed Solution

### 4.1 Implemented Changes
1. **Stem-based deduplication**: Uses suffix stripping to normalize word forms
2. **N-gram cleanup**: Filters phrases with repeated words
3. **Increased extraction**: `top_n` increased from 10 to 20
4. **Phrase stem signatures**: Multi-word deduplication support

### 4.2 New Helper Functions

```python
def _get_word_stem(word: str) -> str:
    """Simple suffix-based stemming without NLTK dependency."""
    
def _deduplicate_by_stem(items: List) -> List:
    """Remove items with same stem, keeping first occurrence."""
    
def _clean_ngram_duplicates(keywords: List[Tuple[str, float]]) -> List:
    """Remove n-grams with repeated words."""
    
def _get_phrase_stem_signature(phrase: str) -> str:
    """Create sorted stem signature for multi-word deduplication."""
```

---

## 5. Implementation Progress

### 5.1 Completed ✅
- [x] TDD RED: 13 test cases written
- [x] TDD GREEN: All deduplication functions implemented
- [x] TDD REFACTOR: SonarQube issues resolved
- [x] Validation: Fresh extraction confirms deduplication working
- [x] Metrics: +5.48% unique keywords, 1.95x replacement ratio
- [x] Project reorganization: Docs → `docs/`, scripts → `scripts/`
- [x] Git commits pushed to `feature/keyword-deduplication-enhancement`

### 5.2 In Progress 🔄
- [ ] Create extraction_profiles.json configuration
- [ ] Run baseline test (restore original settings)
- [ ] Run moderate test (top_n=25)
- [ ] Run aggressive test (top_n=35)
- [ ] Create LLM evaluation script
- [ ] Execute multi-LLM evaluations
- [ ] Generate final analysis report

---

## 6. Complete Parameter Matrix

### 6.1 All Tunable Parameters

| # | Component | Parameter | Description | Range | Impact |
|---|-----------|-----------|-------------|-------|--------|
| 1 | YAKE | `top_n` | Keywords per chapter | 5-50 | HIGH |
| 2 | YAKE | `n` | Max n-gram size | 1-5 | MEDIUM |
| 3 | YAKE | `dedupLim` | Internal dedup threshold | 0.5-1.0 | MEDIUM |
| 4 | Summa | `concepts_top_n` | Concepts per chapter | 5-20 | MEDIUM |
| 5 | Summa | `summary_ratio` | Summary extraction ratio | 0.1-0.5 | LOW |
| 6 | Custom | `stem_dedup` | Stem-based deduplication | ON/OFF | HIGH |
| 7 | Custom | `ngram_clean` | N-gram cleanup | ON/OFF | MEDIUM |
| 8 | TF-IDF | `max_features` | Vocabulary size | 500-5000 | MEDIUM |
| 9 | TF-IDF | `min_df` | Min document frequency | 1-5 | LOW |
| 10 | Related | `threshold` | Min similarity for relation | 0.3-0.9 | HIGH |
| 11 | Related | `related_top_n` | Max related chapters | 3-10 | MEDIUM |

### 6.2 Test Configuration Matrix

| Parameter | Baseline | Current | Moderate | Aggressive |
|-----------|----------|---------|----------|------------|
| `top_n` | 10 | 20 | 25 | 35 |
| `n` (n-gram) | 3 | 3 | 4 | 5 |
| `dedupLim` | 0.9 | 0.9 | 0.85 | 0.8 |
| `concepts_top_n` | 10 | 10 | 12 | 15 |
| `stem_dedup` | OFF | ON | ON | ON |
| `ngram_clean` | OFF | ON | ON | ON |
| `max_features` | 1000 | 1000 | 1500 | 2000 |
| `min_df` | 2 | 2 | 1 | 1 |
| `threshold` | 0.7 | 0.7 | 0.6 | 0.5 |
| `related_top_n` | 5 | 5 | 7 | 10 |

---

## 7. Test Configurations

### 7.1 Test Book
- **Name:** AI Engineering Building Applications
- **Chapters:** 49
- **Pages:** 991
- **Taxonomy:** AI-ML_taxonomy_20251128.json

### 7.2 Test Outputs
Each test run produces:
1. `{test_name}_metadata.json` - Raw extraction output
2. `{test_name}_enriched.json` - Enriched with cross-references
3. `{test_name}_aggregate.json` - Summary statistics for LLM evaluation

---

## 8. LLM Evaluation Framework

### 8.1 LLM Providers & Models

| Provider | Model | Use Case | API Endpoint |
|----------|-------|----------|--------------|
| **OpenAI** | GPT-5.1 | Main evaluation | api.openai.com |
| **OpenAI** | GPT-5.1 Pro | Deep analysis | api.openai.com |
| **OpenAI** | GPT-5.1 Codex | Code-heavy evaluation | api.openai.com |
| **OpenAI** | GPT-5 Mini | Budget evaluation | api.openai.com |
| **OpenAI** | GPT-5 Nano | Cheap evaluation runs | api.openai.com |
| **Anthropic** | Claude 4.5 Sonnet | Balanced evaluation | api.anthropic.com |
| **Anthropic** | Claude 4.6 Opus | Deep reasoning | api.anthropic.com |
| **Anthropic** | Claude 4.5 Haiku | Fast/cheap evaluation | api.anthropic.com |
| **DeepSeek** | Coder V3 | Code analysis | api.deepseek.com |
| **DeepSeek** | R1 | Reasoning evaluation | api.deepseek.com |
| **DeepSeek** | Coder R1 Hybrid | Code + reasoning | api.deepseek.com |
| **Google** | Gemini 3 | Multimodal evaluation | generativelanguage.googleapis.com |

### 8.2 API Keys (Stored in Environment)
```bash
export OPENAI_API_KEY="..."          # User's existing key
export ANTHROPIC_API_KEY="..."       # User's existing key
export DEEPSEEK_API_KEY="sk-104b1216a8244bc6ab3182016d704d20"
export GEMINI_API_KEY="AIzaSyBuFw1-29vjvJc6sFqaRLXwpbp-YPHUbhM"
```

### 8.3 Evaluation Prompt

```markdown
# Cross-Reference Quality Evaluation

You are an expert technical documentation analyst. Evaluate the cross-referencing 
quality of the following keyword extraction configurations for a technical book.

## Task
Compare these 4 extraction configurations and score each on the criteria below.

## Configurations
1. **BASELINE**: {baseline_aggregate}
2. **CURRENT**: {current_aggregate}  
3. **MODERATE**: {moderate_aggregate}
4. **AGGRESSIVE**: {aggressive_aggregate}

## Evaluation Criteria (Score 1-10 for each)

### Navigation Quality
1. **Concept Discoverability**: Can a reader find related topics easily from keywords?
2. **Cross-Reference Density**: Are chapters well-connected through shared keywords?
3. **Semantic Coherence**: Do keywords accurately represent chapter content?

### Keyword Quality
4. **Specificity**: Are keywords precise (e.g., "training data pipeline") vs generic ("data")?
5. **Redundancy Score**: How much overlap/duplication exists? (Lower = better)
6. **Coverage Breadth**: Does the keyword set capture the chapter's full scope?

### Practical Utility
7. **Search Effectiveness**: Would these keywords help a user find this chapter?
8. **Learning Path Clarity**: Can a reader understand prerequisite relationships?
9. **Topic Clustering**: Do related chapters share appropriate keywords?

### Overall
10. **Best Configuration**: Which configuration provides the best balance?

## Response Format
Provide your evaluation as JSON:
```json
{
  "baseline": {
    "scores": {"discoverability": X, "density": X, ...},
    "total": X,
    "strengths": ["..."],
    "weaknesses": ["..."]
  },
  "current": {...},
  "moderate": {...},
  "aggressive": {...},
  "recommendation": "...",
  "reasoning": "..."
}
```

## Data for Evaluation
{aggregates_json}
```

### 8.4 Aggregate JSON Structure

```json
{
  "configuration": "current",
  "parameters": {
    "top_n": 20,
    "n_gram": 3,
    "dedup_enabled": true,
    ...
  },
  "statistics": {
    "total_keywords": 733,
    "unique_keywords": 404,
    "total_concepts": 490,
    "avg_keywords_per_chapter": 14.96,
    "avg_related_chapters": 3.7,
    "keyword_diversity_ratio": 0.55
  },
  "sample_chapters": [
    {
      "chapter": 1,
      "title": "Segment 1 (pages 1-18)",
      "keywords": ["book", "Engineering", "Foundation Models", ...],
      "concepts": ["models", "engineering", "engineer", ...],
      "related_chapters": [2, 5, 10]
    },
    ...
  ],
  "cross_reference_matrix": {
    "1": [2, 5, 10],
    "2": [1, 3, 7],
    ...
  }
}
```

---

## 9. Execution Plan

### Phase 1: Configuration Setup
1. Create `config/extraction_profiles.json`
2. Create parameterized extraction runner
3. Archive current outputs

### Phase 2: Test Execution
| Step | Test | Duration | Output |
|------|------|----------|--------|
| 1 | Baseline (restore original) | ~5 min | `baseline_aggregate.json` |
| 2 | Current (already done) | - | `current_aggregate.json` |
| 3 | Moderate | ~5 min | `moderate_aggregate.json` |
| 4 | Aggressive | ~5 min | `aggressive_aggregate.json` |

### Phase 3: LLM Evaluation
| Step | LLM | Duration | Cost Est. |
|------|-----|----------|-----------|
| 1 | Claude 4.5 Sonnet | ~2 min | $0.10 |
| 2 | GPT-5.1 | ~2 min | $0.15 |
| 3 | DeepSeek R1 | ~2 min | $0.02 |
| 4 | Gemini 3 | ~2 min | $0.05 |

### Phase 4: Analysis & Documentation
1. Compile LLM evaluations
2. Generate comparison report
3. Create architecture writeup
4. Update CHANGELOG

---

## 10. Success Criteria

### 10.1 Quantitative
- [ ] All 4 test configurations complete successfully
- [ ] At least 3 LLM evaluations completed
- [ ] Aggregate JSON files generated for all tests
- [ ] Comparison metrics calculated

### 10.2 Qualitative
- [ ] LLM consensus on best configuration
- [ ] Clear improvement over baseline documented
- [ ] Trade-offs between configurations understood
- [ ] Recommendation for production configuration

### 10.3 Documentation
- [ ] Architecture writeup complete
- [ ] Test results documented
- [ ] CHANGELOG updated
- [ ] All changes committed to feature branch

---

## Appendix A: Git Commits on Feature Branch

| Commit | Description |
|--------|-------------|
| `7bf7bc9f` | feat: add keyword deduplication with stemming and n-gram cleanup |
| `9b3a6c8e` | refactor: fix SonarQube redundant exception warnings |
| `149541e5` | feat: add validation script for deduplication changes |
| `00eff0ce` | refactor: reorganize project structure |
| `8d544a84` | fix: correct argument format for enrichment script |
| `ccde4f45` | test: validate deduplication with fresh extraction |

---

## Appendix B: Validated Metrics (Current Configuration)

| Metric | Baseline | Current | Change |
|--------|----------|---------|--------|
| Total keywords | 735 | 733 | -0.27% |
| Unique keywords | 383 | 404 | **+5.48%** |
| Keywords removed | - | 22 | - |
| New keywords added | - | 43 | - |
| Replacement ratio | - | 1.95x | - |
| % new in set | - | 10.64% | - |

---

*Document generated as part of TDD workflow on feature/keyword-deduplication-enhancement*
