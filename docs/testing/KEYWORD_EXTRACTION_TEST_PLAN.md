# Keyword Extraction Enhancement Test Plan

**Version:** 4.0  
**Date:** 2025-11-30  
**Branch:** `feature/observability-platform-refactoring`

---

## 1. Objective

Evaluate whether stem-based keyword deduplication and expanded extraction parameters improve cross-referencing quality in the document enhancement pipeline through **chunked LLM evaluation** using technical system design questions as targeted navigation exercises.

### 1.1 Why Chunked Evaluation?

| Problem with Single-Prompt | Solution with Chunked Approach |
|---------------------------|-------------------------------|
| 73KB prompts cause timeouts | 25KB per chunk, reliable |
| 18 questions dilute model focus | 6 questions per chunk, concentrated |
| Single failure loses everything | Only retry failed chunks |
| Final decision is rushed | Dedicated final assessment call |

### 1.2 Evaluation Philosophy

The LLM acts as a **NAVIGATOR** testing whether concepts are discoverable through the knowledge graph:

```
❌ WRONG: "I rate this extraction 8/10 for quality"
   (Subjective, unverifiable)

✅ CORRECT: "Searching BASELINE for 'multi-agent framework':
   - Found: ['agent']
   - Missing: ['choreography', 'handoff', 'arbitration']
   - Navigation score: 3/10"
   (Objective, evidence-based)
```

---

## 2. Pipeline Under Test

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          TEST PIPELINE FLOW                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  SOURCE JSON              ENRICHMENT              AGGREGATE      LLM EVAL   │
│  (unchanged)              (4 profiles)            (4 files)      (chunked)  │
│                                                                             │
│  ┌──────────────┐    ┌─────────────────┐    ┌────────────┐    ┌──────────┐ │
│  │ AI Eng Book  │───▶│ StatisticalExtr │───▶│ aggregate_ │───▶│ Chunk 1  │ │
│  │ _metadata    │    │ BASELINE params │    │ BASELINE   │    │ Q1-Q6    │ │
│  │ .json        │    └─────────────────┘    └────────────┘    ├──────────┤ │
│  │              │                                             │ Chunk 2  │ │
│  │              │    Repeated for: CURRENT, MODERATE,         │ Q7-Q12   │ │
│  │              │                  AGGRESSIVE                 ├──────────┤ │
│  └──────────────┘                                             │ Chunk 3  │ │
│                                                               │ Q13-Q18  │ │
│                                                               ├──────────┤ │
│                                                               │ Final    │ │
│                                                               │ Assess   │ │
│                                                               └──────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Test Configurations (4 Profiles)

### 3.1 Parameter Matrix

| Component | Parameter | Baseline | Current | Moderate | Aggressive |
|-----------|-----------|----------|---------|----------|------------|
| **YAKE** | top_n | 10 | 20 | 25 | 35 |
| **YAKE** | n (n-gram) | 3 | 3 | 4 | 5 |
| **Custom** | stem_dedup | OFF | ON | ON | ON |
| **Custom** | ngram_clean | OFF | ON | ON | ON |
| **Related** | threshold | 0.7 | 0.7 | 0.6 | 0.5 |
| **Related** | top_n | 5 | 5 | 7 | 10 |

### 3.2 Profile Descriptions

- **BASELINE:** Original settings before deduplication (stem_dedup OFF)
- **CURRENT:** Implementation with stem deduplication enabled (top_n=20)
- **MODERATE:** Expanded extraction with relaxed thresholds
- **AGGRESSIVE:** Maximum extraction with lowest thresholds

---

## 4. LLM Evaluators (10 Models)

| # | Provider | Model | API Model ID | Status |
|---|----------|-------|--------------|--------|
| 1 | Anthropic | Claude Opus 4.5 | `claude-opus-4-5-20251101` | ✅ Working |
| 2 | Anthropic | Claude Sonnet 4.5 | `claude-sonnet-4-5-20250929` | ⚠️ 529 |
| 3 | OpenAI | GPT-5.1 | `gpt-5.1` | ✅ Working |
| 4 | OpenAI | GPT-5 | `gpt-5` | ✅ Working |
| 5 | OpenAI | GPT-5 Mini | `gpt-5-mini` | ✅ Working |
| 6 | OpenAI | GPT-5 Nano | `gpt-5-nano` | ✅ Working |
| 7 | Google | Gemini 3 Pro | `gemini-3-pro-preview` | ⚠️ 429 |
| 8 | Google | Gemini 2.5 Flash | `gemini-2.5-flash` | ✅ Working |
| 9 | DeepSeek | DeepSeek V3 | `deepseek-chat` | ✅ Working |
| 10 | DeepSeek | DeepSeek R1 | `deepseek-reasoner` | ✅ Working |

---

## 5. Chunked Evaluation Architecture

### 5.1 Evaluation Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    STAGE 1: CHUNKED ANALYSIS                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Chunk 1: [Instructions + Q1-Q6 + 4 Aggregates] → ~25KB         │
│           Returns: Scores for Q1-Q6 per profile                 │
│                                                                 │
│  Chunk 2: [Instructions + Q7-Q12 + 4 Aggregates] → ~25KB        │
│           Returns: Scores for Q7-Q12 per profile                │
│                                                                 │
│  Chunk 3: [Instructions + Q13-Q18 + 4 Aggregates] → ~25KB       │
│           Returns: Scores for Q13-Q18 per profile               │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                    LOCAL MERGE (Python)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Combine 18 question scores → profile_totals                    │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                    STAGE 2: FINAL ASSESSMENT                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Final: [Merged scores + "Pick winner"] → ~5KB                  │
│         Returns: Recommendation with reasoning                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 API Call Summary

| Per Model | Calls | Prompt Size | Total Tokens |
|-----------|-------|-------------|--------------|
| Chunk 1 | 1 | ~25KB | ~6K |
| Chunk 2 | 1 | ~25KB | ~6K |
| Chunk 3 | 1 | ~25KB | ~6K |
| Final | 1 | ~5KB | ~1K |
| **Total** | **4** | ~80KB | ~19K |

**All Models:** 4 calls × 10 models = 40 API calls total

---

## 6. The 18 System Design Questions

### Chunk 1: Q1-Q6 (Infrastructure & Orchestration)

| Q# | Question | Focus Areas |
|----|----------|-------------|
| Q1 | Scalable LLM code understanding system | chunking, embeddings, retrieval, indexing, grounding, hallucination |
| Q2 | Agentic coding assistant with safe code changes | sandboxing, static analysis, verification, diff, rollback, guardrails |
| Q3 | LLM batch processing for multi-GB datasets | map-reduce, chunk, orchestration, persistent state, quality gates, metadata |
| Q4 | Multi-model orchestrator across providers | routing, retry, backoff, cost, degradation, parallelism, normalization |
| Q5 | Fully local fallback system | local inference, Qwen, Llama, GGUF, quantization, offline, on-device |
| Q6 | LLM agent for infrastructure automation | tool schema, IAM, guardrails, traceability, intent classification, verification |

### Chunk 2: Q7-Q12 (Agents & Performance)

| Q# | Question | Focus Areas |
|----|----------|-------------|
| Q7 | Multi-agent collaboration framework | choreography, handoff, arbitration, termination, confidence, roles |
| Q8 | Hallucination prevention in agentic systems | grounding, schema validation, safety rails, log-probability, self-test |
| Q9 | 100GB+ document indexing system | distributed, HNSW, IVF, vector pruning, hot storage, cold storage, partial update |
| Q10 | Secure multi-tenant fine-tuning | data boundary, encryption, isolation, gradients, audit, tenant |
| Q11 | 70B model inference latency reduction | KV cache, speculative decoding, MoE, distillation, flash-attention, quantization |
| Q12 | Diagnosing confident but incorrect LLM outputs | retrieval eval, likelihood, consistency, chain-of-thought, benchmark |

### Chunk 3: Q13-Q18 (Safety & Applications)

| Q# | Question | Focus Areas |
|----|----------|-------------|
| Q13 | Safety guardrails for code-writing agents | static analysis, sandboxing, unit test, rollback, anomaly detection, approval |
| Q14 | Jailbreak detection system | classifier, intent detection, safety model, perplexity, pattern |
| Q15 | Resume-job description matching system | skill embedding, requirement extraction, scoring, rewriting, ensemble |
| Q16 | LLM-powered refactoring engine | AST, snippet embedding, per-file isolation, diff-only, self-review |
| Q17 | Code-to-architecture diagram microservice | static parsing, call graph, summarization, Mermaid, PlantUML, JSON schema |
| Q18 | Knowledge graph from technical textbooks | metadata extraction, taxonomy, semantic alignment, cross-book, deduplication, guideline |

---

## 7. Navigation Test Protocol

For each question, the LLM performs this navigation simulation:

### Step 1: Extract Search Terms
```
Question: "Design a multi-agent framework with planner/coder/critic/tester roles"
Focus areas: ["choreography", "handoff", "arbitration", "termination", "confidence", "roles"]
```

### Step 2: Search Each Aggregate's Keywords
```
BASELINE aggregate search:
  - "choreography" → NOT FOUND
  - "handoff" → NOT FOUND
  - "agent" → FOUND
  Focus areas found: 1/6 (17%)

CURRENT aggregate search:
  - "multi-agent" → FOUND
  - "coordination" → FOUND
  - "agent" → FOUND
  Focus areas found: 3/6 (50%)
```

### Step 3: Calculate Score
```
Score = (focus_areas_found / total_focus_areas) × 10

BASELINE: 1/6 × 10 = 2
CURRENT: 3/6 × 10 = 5
```

---

## 8. Expected Output Structure

### Per-Model Result

```json
{
  "model": "claude-opus-4.5",
  "approach": "chunked_evaluation",
  "stage1_chunks": [
    {"chunk": 1, "scores": {"Q1": {...}, "Q2": {...}, ...}},
    {"chunk": 2, "scores": {"Q7": {...}, "Q8": {...}, ...}},
    {"chunk": 3, "scores": {"Q13": {...}, "Q14": {...}, ...}}
  ],
  "merged_scores": {
    "profile_totals": {
      "baseline": 72,
      "current": 98,
      "moderate": 112,
      "aggressive": 108
    }
  },
  "final_assessment": {
    "recommendation": {
      "best_for_production": "moderate",
      "confidence": "high",
      "reasoning": "Highest total score (112/180), won 7/18 questions"
    }
  }
}
```

### Consensus Across Models

```json
{
  "consensus": {
    "best_for_production": "moderate",
    "votes": {
      "baseline": 0,
      "current": 2,
      "moderate": 6,
      "aggressive": 2
    },
    "agreement_ratio": 0.6
  }
}
```

---

## 9. Execution

### Prerequisites

- API keys configured in `.env`:
  - `ANTHROPIC_API_KEY`
  - `OPENAI_API_KEY`
  - `GEMINI_API_KEY`
  - `DEEPSEEK_API_KEY`

### Run Command

```bash
cd /Users/kevintoles/POC/llm-document-enhancer

# Chunked evaluation (RECOMMENDED)
python3 scripts/llm_evaluation.py --chunked

# Single-prompt evaluation (not recommended - larger prompts)
python3 scripts/llm_evaluation.py --comparative
```

### Expected Time

| Phase | Duration |
|-------|----------|
| Load aggregates | ~5 seconds |
| Per model (4 calls) | ~3-5 minutes |
| 10 models | ~30-50 minutes |
| Save results | ~2 seconds |

### Output Location

```
outputs/evaluation/
├── llm_chunked_evaluation_<timestamp>.json
├── aggregate_BASELINE.json
├── aggregate_CURRENT.json
├── aggregate_MODERATE.json
└── aggregate_AGGRESSIVE.json
```

---

## 10. Success Criteria

| Metric | Baseline | Target (Current/Moderate) |
|--------|----------|---------------------------|
| Navigation Score (sum/180) | <80 | >100 |
| Questions Won (out of 18) | <5 | >10 |
| LLM Consensus | N/A | >50% agreement |
| Duplicate Groups | >15 | <5 |

---

## 11. Error Handling

### Graceful Degradation

| Scenario | Behavior |
|----------|----------|
| 1 chunk fails | Continue with 12/18 questions |
| 2 chunks fail | Continue with 6/18 questions |
| All 3 chunks fail | Skip model, log error |
| Final assessment fails | Use merged totals as result |

### API Fixes Applied

| Issue | Fix |
|-------|-----|
| OpenAI `max_tokens` error | Use `max_completion_tokens` |
| OpenAI `temperature` error | Remove temperature parameter |
| Model routing mismatch | Use `startswith()` matching |
| Gemini SDK missing | Install `google-generativeai` |

---

## 12. Test Script Architecture

```
scripts/
├── llm_evaluation.py              # Main evaluation script
│   ├── EVALUATION_QUESTIONS       # 18 questions with focus areas
│   ├── create_chunked_prompt()    # Stage 1 prompt generator
│   ├── create_final_assessment_prompt()  # Stage 2 prompt
│   ├── run_chunked_evaluation()   # Per-model orchestration
│   ├── run_chunked_comparative_evaluation()  # All models
│   └── call_llm()                 # API routing
│
├── run_extraction_tests.py        # Profile application
│   ├── get_profile(name)          # Load profile config
│   ├── apply_profile_to_extractor()  # Set env vars
│   └── run_extraction_for_profile()  # Execute enrichment
│
└── run_comprehensive_evaluation.py  # Full pipeline orchestrator
```

---

## 13. Hypothesis

The **MODERATE** or **CURRENT** configuration will outperform BASELINE by:

1. **Reducing duplicate variants** by 30-50% (stem_dedup ON)
2. **Improving navigation scores** by capturing more focus area terms
3. **Achieving LLM consensus** across multiple model evaluations

### Expected Results

| Profile | Nav Score | Questions Won | Duplicates |
|---------|-----------|---------------|------------|
| BASELINE | ~70 | ~4 | ~20 |
| CURRENT | ~95 | ~6 | ~3 |
| MODERATE | ~110 | ~8 | ~2 |
| AGGRESSIVE | ~105 | ~6 | ~1 |

---

**Status:** READY FOR EXECUTION  
**Command:** `python3 scripts/llm_evaluation.py --chunked`  
**Estimated Time:** 30-50 minutes  
**Related Document:** KEYWORD_EXTRACTION_TEST_PLAN_ADDENDUM.md
