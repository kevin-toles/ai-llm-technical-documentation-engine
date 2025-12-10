# Keyword Extraction Test Plan - Implementation Addendum

**Date:** November 30, 2025  
**Status:** FINALIZED - Ready for Execution  
**Version:** 4.0 - Chunked Evaluation Architecture  
**Related:** KEYWORD_EXTRACTION_TEST_PLAN.md  

---

## 1. Evaluation Architecture: Chunked + Final Assessment

### 1.1 Why Chunked Evaluation?

The original single-prompt approach had limitations:

| Issue | Single Prompt | Chunked Approach |
|-------|---------------|------------------|
| Prompt Size | ~73KB | ~25KB per chunk |
| Timeout Risk | High | Low |
| Context Pressure | High (18 questions + 4 aggregates) | Low (6 questions per call) |
| Model Focus | Diluted | Concentrated |
| Recovery from Errors | Must restart all | Only retry failed chunk |

### 1.2 Chunked Evaluation Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    STAGE 1: CHUNKED ANALYSIS                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Chunk 1: [Instructions + Q1-Q6 + 4 Aggregates]                 │
│           → Scores for 6 questions per profile                  │
│           ~25KB prompt                                          │
│                                                                 │
│  Chunk 2: [Instructions + Q7-Q12 + 4 Aggregates]                │
│           → Scores for 6 questions per profile                  │
│           ~25KB prompt                                          │
│                                                                 │
│  Chunk 3: [Instructions + Q13-Q18 + 4 Aggregates]               │
│           → Scores for 6 questions per profile                  │
│           ~25KB prompt                                          │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                    LOCAL MERGE                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Python merges all 18 question scores per profile:              │
│  {                                                              │
│    "baseline": { "Q1": 4, "Q2": 5, ..., "total": 72 },          │
│    "current": { "Q1": 6, "Q2": 7, ..., "total": 98 },           │
│    "moderate": { "Q1": 7, "Q2": 8, ..., "total": 112 },         │
│    "aggressive": { "Q1": 8, "Q2": 7, ..., "total": 108 }        │
│  }                                                              │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                    STAGE 2: FINAL DECISION                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Final Call: [Merged scores summary + "Pick the winner"]        │
│              → Final recommendation with reasoning              │
│              ~5KB prompt (just scores, no aggregates)           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 Benefits

1. **Smaller Prompts**: Each chunk is ~25KB vs 73KB single prompt
2. **Better Focus**: LLM concentrates on 6 questions at a time
3. **Error Recovery**: If one chunk fails, only retry that chunk
4. **Final Synthesis**: Dedicated call for holistic recommendation
5. **Cost Similar**: 4 calls × ~7K tokens ≈ 1 call × 28K tokens

---

## 2. Configuration Status

### Test Profiles (4 Total)

| Profile | YAKE top_n | Stem Dedup | Threshold | Status |
|---------|-----------|------------|-----------|--------|
| **BASELINE** | 10 | OFF | 0.7 | ✅ Ready |
| **CURRENT** | 20 | ON | 0.7 | ✅ Ready |
| **MODERATE** | 25 | ON | 0.6 | ✅ Ready |
| **AGGRESSIVE** | 35 | ON | 0.5 | ✅ Ready |

### LLM Evaluators (10 Models)

| # | Provider | Model | API Model ID | Status |
|---|----------|-------|--------------|--------|
| 1 | Anthropic | Claude Opus 4.5 | `claude-opus-4-5-20251101` | ✅ Working |
| 2 | Anthropic | Claude Sonnet 4.5 | `claude-sonnet-4-5-20250929` | ⚠️ 529 Temp |
| 3 | OpenAI | GPT-5.1 | `gpt-5.1` | ✅ Working |
| 4 | OpenAI | GPT-5 | `gpt-5` | ✅ Working |
| 5 | OpenAI | GPT-5 Mini | `gpt-5-mini` | ✅ Working |
| 6 | OpenAI | GPT-5 Nano | `gpt-5-nano` | ✅ Working |
| 7 | Google | Gemini 3 Pro | `gemini-3-pro-preview` | ⚠️ 429 Quota |
| 8 | Google | Gemini 2.5 Flash | `gemini-2.5-flash` | ✅ Working |
| 9 | DeepSeek | DeepSeek V3 | `deepseek-chat` | ✅ Working |
| 10 | DeepSeek | DeepSeek R1 | `deepseek-reasoner` | ✅ Working |

**Note:** 8/10 models confirmed working. 2 have temporary rate limit issues.

---

## 3. Chunk Structure

### Chunk 1: Questions Q1-Q6 (Infrastructure & Orchestration)

| Q# | Question | Focus Areas |
|----|----------|-------------|
| Q1 | Scalable LLM code understanding | chunking, embeddings, retrieval, indexing |
| Q2 | Agentic coding assistant | sandboxing, static analysis, verification, rollback |
| Q3 | LLM batch processing >GB | map-reduce, orchestration, persistent state |
| Q4 | Multi-model orchestrator | routing, retry, backoff, cost-aware |
| Q5 | Local fallback system | local inference, Qwen, Llama, quantization |
| Q6 | LLM for infrastructure | tool schemas, IAM, guardrails, traceability |

### Chunk 2: Questions Q7-Q12 (Agents & Performance)

| Q# | Question | Focus Areas |
|----|----------|-------------|
| Q7 | Multi-agent collaboration | choreography, handoffs, arbitration, confidence |
| Q8 | Hallucination prevention | grounding, schema validation, safety rails |
| Q9 | 100GB document indexing | distributed, HNSW, IVF, vector pruning |
| Q10 | Secure multi-tenant fine-tuning | data boundary, encryption, isolation |
| Q11 | 70B model latency | KV cache, speculative decoding, MoE |
| Q12 | Diagnosing incorrect outputs | retrieval eval, consistency, benchmarks |

### Chunk 3: Questions Q13-Q18 (Safety & Applications)

| Q# | Question | Focus Areas |
|----|----------|-------------|
| Q13 | Code-writing agent safety | static analysis, sandboxing, unit tests |
| Q14 | Jailbreak detection | classifiers, intent detection, perplexity |
| Q15 | Resume-job matching | skill embeddings, requirement extraction |
| Q16 | LLM refactoring engine | AST, snippet embedding, diff-only |
| Q17 | Code-to-diagram service | static parsing, call graph, Mermaid |
| Q18 | Knowledge graph from textbooks | metadata extraction, taxonomy, deduplication |

---

## 4. Chunk Prompt Template

Each chunk receives this prompt structure:

```
You are a KNOWLEDGE GRAPH NAVIGATOR testing discoverability.

## CHUNK {N} OF 3 - Questions Q{X} to Q{Y}

You are analyzing 4 extraction profiles to determine which produces
better keyword navigation. Score questions Q{X}-Q{Y} only.

## CRITICAL RULES

1. DO NOT answer the system design questions yourself
2. ONLY report what you can find by searching sample_keywords
3. Score based on how many focus areas are DISCOVERABLE

## QUESTIONS FOR THIS CHUNK

Q{X}: "{Title}"
    Focus areas to search: [term1, term2, ...]

Q{X+1}: "{Title}"
    Focus areas to search: [term1, term2, ...]

... (6 questions total)

## SCORING INSTRUCTIONS

For each question:
1. Search sample_keywords for each focus area term
2. Count: found vs missing terms
3. Score: (found / total) * 10, rounded

## OUTPUT FORMAT (JSON only)

{
  "chunk": {N},
  "scores": {
    "Q{X}": {
      "baseline": {"found": [...], "missing": [...], "score": N},
      "current": {"found": [...], "missing": [...], "score": N},
      "moderate": {"found": [...], "missing": [...], "score": N},
      "aggressive": {"found": [...], "missing": [...], "score": N}
    },
    ... (all 6 questions)
  }
}

## AGGREGATE DATA

### BASELINE PROFILE
{summarized aggregate JSON}

### CURRENT PROFILE
{summarized aggregate JSON}

### MODERATE PROFILE
{summarized aggregate JSON}

### AGGRESSIVE PROFILE
{summarized aggregate JSON}
```

---

## 5. Final Assessment Prompt

After merging chunk results, the final call receives:

```
You are making a FINAL ASSESSMENT of 4 extraction profiles.

## YOUR TASK

Based on the merged scores from 18 system design questions,
determine which profile is BEST for production use.

## MERGED SCORES FROM ALL 18 QUESTIONS

{
  "all_scores": {
    "Q1": {"baseline": {"score": 4}, "current": {"score": 6}, ...},
    "Q2": {...},
    ... (all 18 questions)
  },
  "profile_totals": {
    "baseline": 72,
    "current": 98,
    "moderate": 112,
    "aggressive": 108
  }
}

## ANALYSIS REQUIRED

1. Review total scores for each profile
2. Count how many questions each profile "won"
3. Identify patterns in which profiles excel at which question types
4. Make a final recommendation with reasoning

## OUTPUT FORMAT (JSON only)

{
  "totals": {
    "baseline": 72,
    "current": 98,
    "moderate": 112,
    "aggressive": 108
  },
  "questions_won": {
    "baseline": 2,
    "current": 5,
    "moderate": 7,
    "aggressive": 4
  },
  "analysis": {
    "baseline_strengths": "...",
    "current_strengths": "...",
    "moderate_strengths": "...",
    "aggressive_strengths": "..."
  },
  "recommendation": {
    "best_for_production": "moderate",
    "confidence": "high",
    "reasoning": "Moderate achieved highest total score (112/180) and won most questions (7/18)..."
  }
}
```

---

## 6. API Call Flow Per Model

For each of the 10 LLM models:

```
Model: claude-opus-4.5
├── Chunk 1 (Q1-Q6)     → ~25KB prompt → Response with 6 scores
│   ⏳ 3s delay
├── Chunk 2 (Q7-Q12)    → ~25KB prompt → Response with 6 scores
│   ⏳ 3s delay
├── Chunk 3 (Q13-Q18)   → ~25KB prompt → Response with 6 scores
│   ⏳ 3s delay
├── [LOCAL] Merge 18 scores
└── Final Assessment    → ~5KB prompt → Final recommendation
    ⏳ 3s delay before next model
```

**Total API calls:** 4 per model × 10 models = 40 calls
**Total time estimate:** ~30-45 minutes (including delays)

---

## 7. Expected Output Structure

### Per-Model Evaluation Result

```json
{
  "model": "claude-opus-4.5",
  "approach": "chunked_evaluation",
  "stage1_chunks": [
    {
      "chunk": 1,
      "scores": {
        "Q1": {"baseline": {"found": [...], "score": 4}, ...},
        "Q2": {...},
        ...
      }
    },
    {
      "chunk": 2,
      "scores": {...}
    },
    {
      "chunk": 3,
      "scores": {...}
    }
  ],
  "merged_scores": {
    "all_scores": {...},
    "profile_totals": {
      "baseline": 72,
      "current": 98,
      "moderate": 112,
      "aggressive": 108
    }
  },
  "final_assessment": {
    "totals": {...},
    "questions_won": {...},
    "recommendation": {
      "best_for_production": "moderate",
      "confidence": "high",
      "reasoning": "..."
    }
  }
}
```

### Aggregate Results Across All Models

```json
{
  "evaluation_type": "chunked_comparative",
  "timestamp": "2025-11-30T...",
  "approach": {
    "stage1": "3 chunks of 6 questions each (~25KB per call)",
    "stage2": "Final assessment from merged scores (~5KB)",
    "total_calls_per_model": 4
  },
  "models_used": ["claude-opus-4.5", "gpt-5.1", ...],
  "evaluations": {
    "claude-opus-4.5": {...},
    "gpt-5.1": {...},
    ...
  },
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

## 8. Execution

### Command

```bash
cd /Users/kevintoles/POC/llm-document-enhancer
python3 scripts/llm_evaluation.py --chunked
```

### Alternative: Single-Prompt Mode (Not Recommended)

```bash
python3 scripts/llm_evaluation.py --comparative
```

### Expected Time

| Phase | Duration |
|-------|----------|
| Loading aggregates | ~5 seconds |
| Per model (4 calls) | ~3-5 minutes |
| 10 models total | ~30-50 minutes |
| Saving results | ~2 seconds |

### Output Location

```
outputs/evaluation/
├── llm_chunked_evaluation_<timestamp>.json
└── (optional debug files if parsing fails)
```

---

## 9. Success Criteria

| Metric | Baseline Target | Current/Moderate Target |
|--------|-----------------|-------------------------|
| Navigation Score (sum/180) | <80 | >100 |
| Questions Won | <5 | >10 |
| LLM Consensus | N/A | >50% agreement |
| Chunk Success Rate | N/A | >80% (at least 2/3 chunks) |

---

## 10. Error Handling

### Chunk Failure Recovery

If a chunk fails:
1. The error is logged in `stage1_chunks`
2. Merge proceeds with available chunks
3. Final assessment uses partial data (if ≥2 chunks succeeded)
4. Model result marked with `chunk_errors: true`

### Graceful Degradation

| Scenario | Behavior |
|----------|----------|
| 1 chunk fails | Continue with 12/18 questions |
| 2 chunks fail | Continue with 6/18 questions |
| All 3 chunks fail | Skip model, log error |
| Final assessment fails | Use merged totals as result |

---

## 11. API Fixes Applied

The following issues were resolved to enable all 10 models:

| Issue | Fix Applied |
|-------|-------------|
| OpenAI GPT-5 `max_tokens` error | Changed to `max_completion_tokens` |
| OpenAI GPT-5 `temperature` error | Removed temperature parameter |
| Model routing mismatch | Changed to `startswith()` matching |
| Gemini SDK missing | Installed `google-generativeai` package |

---

**Status:** READY FOR EXECUTION  
**Command:** `python3 scripts/llm_evaluation.py --chunked`  
**Estimated Completion:** 30-50 minutes

