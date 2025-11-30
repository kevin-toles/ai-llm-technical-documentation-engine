# Keyword Extraction Enhancement Test Plan

**Version:** 2.0  
**Date:** 2025-11-29  
**Branch:** `feature/keyword-deduplication-enhancement`

## 1. Objective

Evaluate whether stem-based keyword deduplication and expanded extraction parameters improve cross-referencing quality in the document enhancement pipeline.

## 2. Pipeline Under Test

The test exercises the following pipeline stages:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          TEST PIPELINE FLOW                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  EXISTING JSON TEXT          TAXONOMY              ENRICHMENT    AGGREGATE  │
│  (unchanged input)           (profile suffix)      (profile params)         │
│                                                                             │
│  ┌──────────────────┐    ┌─────────────────┐    ┌───────────────┐    ┌────┐│
│  │ AI Engineering   │───▶│ AI-ML_taxonomy_ │───▶│ *_enriched_   │───▶│ AGG││
│  │ Building Apps    │    │ BASELINE.json   │    │ BASELINE.json │    │    ││
│  │ _metadata.json   │    └─────────────────┘    └───────────────┘    └────┘│
│  │                  │                                                       │
│  │  (source stays   │    Repeated for: CURRENT, MODERATE, AGGRESSIVE       │
│  │   the same)      │                                                       │
│  └──────────────────┘                                                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Important:** The source JSON text file is pre-existing. We do NOT convert PDFs to JSON during this test. The PDF→JSON conversion is a separate, prior workflow step.

## 3. Test Configurations (4 Profiles)

### 3.1 Complete Parameter Matrix

| Component | Parameter | Baseline | Current | Moderate | Aggressive |
|-----------|-----------|----------|---------|----------|------------|
| **YAKE** | top_n | 10 | 20 | 25 | 35 |
| **YAKE** | n (n-gram) | 3 | 3 | 4 | 5 |
| **YAKE** | dedupLim | 0.9 | 0.9 | 0.85 | 0.8 |
| **Summa** | concepts_top_n | 10 | 10 | 12 | 15 |
| **Custom** | stem_dedup | OFF | ON | ON | ON |
| **Custom** | ngram_clean | OFF | ON | ON | ON |
| **TF-IDF** | max_features | 1000 | 1000 | 1500 | 2000 |
| **TF-IDF** | min_df | 2 | 2 | 1 | 1 |
| **Related** | threshold | 0.7 | 0.7 | 0.6 | 0.5 |
| **Related** | top_n | 5 | 5 | 7 | 10 |
| **BERTopic** | min_topic_size | 2 | 2 | 2 | 2 |

**Total: 11 parameters across 4 configurations**

### 3.2 Profile Descriptions

- **Baseline:** Original settings before deduplication enhancement (stem_dedup OFF)
- **Current:** Implementation with stem-based deduplication enabled (top_n=20)
- **Moderate:** Expanded extraction with relaxed thresholds
- **Aggressive:** Maximum extraction with lowest thresholds

## 4. Test Artifacts

### 4.1 Naming Convention

All artifacts follow the pattern: `{original_name}_{PROFILE}.json`

| Artifact Type | Example Filename |
|--------------|------------------|
| Taxonomy | `AI-ML_taxonomy_BASELINE.json` |
| Enriched Metadata | `AI Engineering Building Applications_enriched_BASELINE.json` |
| Aggregate | `aggregate_BASELINE.json` |

### 4.2 Source Data (Unchanged)

- **Metadata File:** `AI Engineering Building Applications_metadata.json`
- **Location:** `workflows/metadata_extraction/output/`
- **Base Taxonomy:** `AI-ML_taxonomy_20251128.json`
- **Chapters:** 49
- **Pages:** 991

### 4.3 Generated Per Profile

1. **Taxonomy:** Copy of base taxonomy with profile suffix (for traceability)
2. **Enriched Metadata:** Output of enrichment with profile parameters applied
3. **Aggregate:** Combined metrics and extracted data for LLM evaluation

## 5. Validation Checkpoints

Each profile run includes validation at every step:

| Step | Validation | Pass Criteria |
|------|------------|---------------|
| Taxonomy | File exists, valid JSON, tier structure intact | ✓ |
| Enrichment | Keywords extracted, concepts identified, related chapters found | Count > 0 |
| Aggregate | All required fields present, JSON serializable | Schema valid |

## 6. LLM Evaluation Strategy

### 6.1 Strategy B: Comparative Evaluation (4 LLM Calls)

All 4 aggregates are sent to each LLM in a single prompt for comparative analysis.

**LLMs Used:**
1. Gemini 2.5 Flash
2. Claude Sonnet 4
3. GPT-4o
4. DeepSeek Chat

### 6.2 Evaluation Process

1. Load all 4 aggregates (BASELINE, CURRENT, MODERATE, AGGRESSIVE)
2. For each LLM:
   - Send comparative prompt with all 4 aggregates
   - LLM performs sequential cross-reference analysis
   - LLM returns objective evaluation with metrics and rankings
3. Aggregate LLM responses into final report

### 6.3 Comparative Evaluation Prompt

```
You are an expert NLP evaluator assessing keyword extraction quality for technical documentation cross-referencing.

## Task
You have been given extraction outputs from 4 different parameter configurations applied to the same source document. Evaluate each configuration SEQUENTIALLY (not in parallel) and provide an objective comparison.

## Configurations Provided
1. BASELINE: Original settings (stem deduplication OFF, top_n=10)
2. CURRENT: Enhanced settings (stem deduplication ON, top_n=20)
3. MODERATE: Expanded extraction (top_n=25, relaxed thresholds)
4. AGGRESSIVE: Maximum extraction (top_n=35, lowest thresholds)

## Evaluation Criteria (Score 1-10 for each configuration)

1. **Keyword Quality**: Relevance, specificity, technical accuracy
2. **Deduplication Effectiveness**: Absence of redundant variants (model/models/modeling)
3. **Concept Coverage**: Breadth and depth of main themes captured
4. **Cross-Reference Utility**: Value of related chapter connections for navigation
5. **Signal-to-Noise Ratio**: Meaningful terms vs. generic/noise terms

## Required Output Format

```json
{
  "evaluation_timestamp": "<ISO timestamp>",
  "sequential_analysis": {
    "baseline": { "scores": {...}, "observations": [...] },
    "current": { "scores": {...}, "observations": [...] },
    "moderate": { "scores": {...}, "observations": [...] },
    "aggressive": { "scores": {...}, "observations": [...] }
  },
  "comparative_ranking": [
    {"rank": 1, "profile": "<best>", "overall_score": <1-10>, "rationale": "..."},
    {"rank": 2, "profile": "...", "overall_score": <1-10>, "rationale": "..."},
    {"rank": 3, "profile": "...", "overall_score": <1-10>, "rationale": "..."},
    {"rank": 4, "profile": "<worst>", "overall_score": <1-10>, "rationale": "..."}
  ],
  "recommendation": {
    "best_for_production": "<profile>",
    "reasoning": "...",
    "tradeoffs": [...]
  }
}
```

## Aggregate Data

[BASELINE AGGREGATE]
{baseline_data}

[CURRENT AGGREGATE]
{current_data}

[MODERATE AGGREGATE]
{moderate_data}

[AGGRESSIVE AGGREGATE]
{aggressive_data}
```

## 7. Expected Outcomes

### 7.1 Hypothesis

The **Current** configuration (stem_dedup=ON, top_n=20) will outperform Baseline by:
- Reducing redundant keyword variants by 30-50%
- Maintaining or improving cross-reference quality
- Achieving higher deduplication effectiveness scores

### 7.2 Success Metrics

| Metric | Baseline Target | Current Target |
|--------|-----------------|----------------|
| Unique Keywords | N (measured) | ≥ N |
| Duplicate Variants | High | Low (30-50% reduction) |
| Cross-Reference Score | Measured | ≥ Baseline |
| Overall LLM Ranking | 3rd or 4th | 1st or 2nd |

## 8. Execution

### 8.1 Prerequisites

- API keys configured in environment:
  - `GEMINI_API_KEY`
  - `ANTHROPIC_API_KEY`
  - `OPENAI_API_KEY`
  - `DEEPSEEK_API_KEY`

### 8.2 Run Command

```bash
cd /Users/kevintoles/POC/llm-document-enhancer
source ~/.zshrc
python3 scripts/run_comprehensive_evaluation.py --run-all
```

### 8.3 Output Location

```
outputs/
├── evaluation/
│   ├── AI-ML_taxonomy_BASELINE.json
│   ├── AI-ML_taxonomy_CURRENT.json
│   ├── AI-ML_taxonomy_MODERATE.json
│   ├── AI-ML_taxonomy_AGGRESSIVE.json
│   ├── AI Engineering Building Applications_enriched_BASELINE.json
│   ├── AI Engineering Building Applications_enriched_CURRENT.json
│   ├── AI Engineering Building Applications_enriched_MODERATE.json
│   ├── AI Engineering Building Applications_enriched_AGGRESSIVE.json
│   ├── aggregate_BASELINE.json
│   ├── aggregate_CURRENT.json
│   ├── aggregate_MODERATE.json
│   ├── aggregate_AGGRESSIVE.json
│   └── llm_comparative_evaluation_<timestamp>.json
```

## 9. Configuration Reference

Profile configurations are defined in:
- `config/extraction_profiles.json`

Environment variables read by StatisticalExtractor:
- `EXTRACTION_YAKE_TOP_N`
- `EXTRACTION_YAKE_N`
- `EXTRACTION_YAKE_DEDUPLIM`
- `EXTRACTION_SUMMA_CONCEPTS_TOP_N`
- `EXTRACTION_STEM_DEDUP_ENABLED`
- `EXTRACTION_NGRAM_CLEAN_ENABLED`
- `EXTRACTION_TFIDF_MAX_FEATURES`
- `EXTRACTION_TFIDF_MIN_DF`
- `EXTRACTION_CHAPTERS_THRESHOLD`
- `EXTRACTION_CHAPTERS_TOP_N`

## 10. Test Script Architecture

```
scripts/
├── run_comprehensive_evaluation.py    # Main orchestrator
│   ├── Loads 4 profiles from config
│   ├── For each profile:
│   │   ├── Creates taxonomy copy with suffix
│   │   ├── Sets environment variables for profile
│   │   ├── Runs enrichment (StatisticalExtractor uses env vars)
│   │   ├── Creates aggregate
│   │   └── Validates outputs
│   └── Sends all 4 aggregates to each LLM (Strategy B)
│
├── run_extraction_tests.py            # Profile application utilities
│   ├── get_profile(name) → profile config
│   ├── apply_profile_to_extractor(profile) → sets env vars
│   └── run_extraction_for_profile(name) → executes enrichment
│
└── llm_evaluation.py                  # LLM API integration
    ├── create_comparative_prompt(aggregates) → prompt string
    ├── call_gemini(prompt) → evaluation JSON
    ├── call_claude(prompt) → evaluation JSON
    ├── call_openai(prompt) → evaluation JSON
    └── call_deepseek(prompt) → evaluation JSON
```
