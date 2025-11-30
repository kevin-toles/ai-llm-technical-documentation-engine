# Keyword Extraction Test Plan - Implementation Addendum

**Date:** November 30, 2025  
**Status:** FINALIZED - Ready for Execution  
**Version:** 3.0 - Rigorous Navigation-Based Validation  
**Related:** KEYWORD_EXTRACTION_TEST_PLAN.md  

---

## 1. Evaluation Philosophy: LLM as Knowledge Graph Navigator

### 1.1 The Critical Distinction

The LLM is **NOT** an expert evaluator giving subjective scores.  
The LLM is a **NAVIGATOR** testing whether concepts are discoverable through the aggregate.

```
❌ WRONG APPROACH (Subjective Scoring):
   "I rate this extraction 8/10 for quality"
   
❌ WRONG APPROACH (Using Own Knowledge):
   "To answer Q7 about multi-agent frameworks, you need role choreography..."
   
✅ CORRECT APPROACH (Navigation Testing):
   "Searching BASELINE aggregate for Q7 focus areas:
    - 'agent' → FOUND in sample_keywords
    - 'multi-agent' → NOT FOUND
    - 'choreography' → NOT FOUND
    - Following cross-ref Ch14→Ch22: found 'tool use', relevant
    - Navigation score: 4/10 (1/5 focus areas discoverable)"
```

### 1.2 Why This Approach?

1. **Simulates Production Usage**: Users navigate the knowledge graph to find content
2. **Verifiable Results**: Every claim cites specific data from the aggregate
3. **No Hallucination**: LLM cannot invent quality scores without evidence
4. **Objective Comparison**: Which aggregate enables finding more relevant content?

### 1.3 The 18 System Design Questions

These are **NOT** questions for the LLM to answer.  
These are **NAVIGATION EXERCISES** to test discoverability.

For each question:
1. Extract the focus areas (the concepts needed to answer it)
2. Search each aggregate's sample_keywords for those concepts
3. Follow cross-references to find related content
4. Report: What percentage of focus areas are discoverable?
5. Compare: Which aggregate enables better navigation?

---

## 2. Configuration Status

### Test Profiles (4 Total)

| Profile | YAKE top_n | Stem Dedup | Threshold | Status |
|---------|-----------|------------|-----------|--------|
| **baseline** | 10 | OFF | 0.7 | ✅ Ready |
| **current** | 20 | ON | 0.7 | ✅ Ready |
| **moderate** | 25 | ON | 0.6 | ✅ Ready |
| **aggressive** | 35 | ON | 0.5 | ✅ Ready |

### LLM Evaluators (10 Models)

| # | Provider | Model | API Model ID |
|---|----------|-------|--------------|
| 1 | Anthropic | Claude Opus 4.5 | `claude-opus-4-5-20251101` |
| 2 | Anthropic | Claude Sonnet 4.5 | `claude-sonnet-4-5-20250929` |
| 3 | OpenAI | GPT-5.1 | `gpt-5.1` |
| 4 | OpenAI | GPT-5 | `gpt-5` |
| 5 | OpenAI | GPT-5 Mini | `gpt-5-mini` |
| 6 | OpenAI | GPT-5 Nano | `gpt-5-nano` |
| 7 | Google | Gemini 3 Pro | `gemini-3-pro-preview` |
| 8 | Google | Gemini 2.5 Flash | `gemini-2.5-flash` |
| 9 | DeepSeek | DeepSeek V3 | `deepseek-chat` |
| 10 | DeepSeek | DeepSeek R1 | `deepseek-reasoner` |

---

## 3. The Five Required Analyses

Each LLM must complete these **navigation-based analyses**:

### Analysis 1: Keyword Relevance (Data Search Only)

**Task:** Search sample_keywords against chapter_analysis titles.

**Method:**
```
For each chapter in chapter_analysis:
  1. Read chapter title (e.g., "Transformer Architectures")
  2. Search sample_keywords for terms related to that title
  3. Count: How many of that chapter's keywords appear in sample_keywords?
  4. Report: relevant_count / total_count with examples
```

**Output:**
```json
{
  "baseline": {
    "relevant_count": 42,
    "irrelevant_count": 8,
    "examples": [
      {"keyword": "transformer", "chapter": "Ch5: Transformer Architectures", "relevant": true},
      {"keyword": "example code", "chapter": "Ch5", "relevant": false, "reason": "generic section marker"}
    ]
  }
}
```

---

### Analysis 2: Duplicate Detection (Scan Sample Keywords)

**Task:** Find morphological variants in sample_keywords.

**Method:**
```
For each keyword in sample_keywords:
  1. Compute stem (e.g., "modeling" → "model")
  2. Group keywords by stem
  3. Any group with >1 member = duplicate group
  4. Count total duplicate groups
```

**Expected:**
- BASELINE should have 15-30 duplicate groups (stem_dedup OFF)
- CURRENT/MODERATE/AGGRESSIVE should have 0-5 (stem_dedup ON)

**Output:**
```json
{
  "baseline": {
    "duplicate_groups": 23,
    "examples": [
      ["model", "models", "modeling"],
      ["embed", "embedding", "embeddings"],
      ["train", "training", "trained"]
    ]
  },
  "current": {
    "duplicate_groups": 2,
    "examples": [["neural network", "neural"]]
  }
}
```

---

### Analysis 3: Cross-Reference Tracing

**Task:** Follow cross-references and validate connections.

**Method:**
```
For each chapter in chapter_analysis:
  For each entry in sample_related:
    1. Read source chapter topic
    2. Read target book/chapter info
    3. Determine: Is this a logical navigation path?
    4. Record: valid or invalid with reason
```

**Output:**
```json
{
  "baseline": {
    "total_traced": 35,
    "valid": 28,
    "invalid": 7,
    "examples_valid": [
      {"from": "Ch5: Transformers", "to": "Ch12: BERT", "reason": "BERT is transformer-based"}
    ],
    "examples_invalid": [
      {"from": "Ch3: Python Basics", "to": "Ch45: Deployment", "reason": "No topical connection"}
    ]
  }
}
```

---

### Analysis 4: Noise Term Identification

**Task:** Count non-informative terms in sample_keywords.

**Noise Categories:**
- Section markers: "introduction", "conclusion", "summary", "chapter", "section"
- Generic terms: "approach", "method", "technique", "example", "system", "process"
- Meta terms: "figure", "table", "code listing", "output"

**Method:**
```
For each keyword in sample_keywords:
  If keyword matches noise category:
    Add to noise_terms list
Calculate: noise_ratio = len(noise_terms) / len(sample_keywords)
```

**Output:**
```json
{
  "baseline": {
    "noise_terms": ["introduction", "example", "approach", "method"],
    "noise_count": 12,
    "total_keywords": 100,
    "noise_ratio": 0.12
  }
}
```

---

### Analysis 5: Navigation Test (18 Questions)

**Task:** For each system design question, test if the aggregate enables finding relevant content.

**The LLM does NOT answer the question. It only searches the aggregate.**

#### Navigation Protocol Per Question:

```
Question: "How would you design a multi-agent framework with planner/coder/critic/tester roles?"

Focus areas to search for:
- role choreography
- reasoning handoffs
- arbitration layer
- self-termination rules
- confidence scoring

BASELINE aggregate search:
  sample_keywords scan:
    - "agent" → FOUND
    - "multi-agent" → NOT FOUND
    - "choreography" → NOT FOUND
    - "handoff" → NOT FOUND
    - "arbitration" → NOT FOUND
    - "termination" → NOT FOUND
  
  cross-reference trace:
    - Ch14 (if exists) → followed to Ch22, found "tool use" (partially relevant)
  
  Focus areas discoverable: 1/5 (20%)
  Navigation score: 3/10
  
CURRENT aggregate search:
  sample_keywords scan:
    - "agent" → FOUND
    - "multi-agent" → FOUND
    - "agent coordination" → FOUND
    - "orchestration" → FOUND
    - "choreography" → NOT FOUND
    - "arbitration" → NOT FOUND
  
  Focus areas discoverable: 3/5 (60%)
  Navigation score: 6/10

Best aggregate for Q7: CURRENT (found coordination concepts)
```

---

## 4. The 18 System Design Questions (Focus Areas)

| Q# | Question | Focus Areas to Search |
|----|----------|----------------------|
| Q1 | Scalable LLM code understanding | chunking, embeddings, retrieval, indexing, grounding, hallucination |
| Q2 | Agentic coding assistant | sandboxing, static analysis, verification, diff, rollback, guardrails |
| Q3 | LLM batch processing >GB | map-reduce, chunk orchestration, persistent state, quality gates |
| Q4 | Multi-model orchestrator | routing, retry, backoff, cost-aware, degradation, parallelism |
| Q5 | Local fallback system | local inference, Qwen, Llama, GGUF, quantization, offline |
| Q6 | LLM for infrastructure | tool schemas, IAM, guardrails, traceability, intent classification |
| Q7 | Multi-agent collaboration | choreography, handoffs, arbitration, self-termination, confidence |
| Q8 | Hallucination prevention | grounding, schema validation, safety rails, log-probability, self-tests |
| Q9 | 100GB document indexing | distributed embeddings, HNSW, IVF, vector pruning, hot/cold storage |
| Q10 | Secure multi-tenant fine-tuning | data boundary, encryption, isolation, gradients, audit |
| Q11 | 70B model latency | KV cache, speculative decoding, MoE, distillation, flash-attention |
| Q12 | Diagnosing incorrect outputs | retrieval eval, likelihood, consistency, CoT validation, benchmarks |
| Q13 | Code-writing agent safety | static analysis, sandboxing, unit tests, rollback, anomaly detection |
| Q14 | Jailbreak detection | classifiers, intent detection, safety models, perplexity |
| Q15 | Resume-job matching | skill embeddings, requirement extraction, scoring, rewriting |
| Q16 | LLM refactoring engine | AST, snippet embedding, per-file isolation, diff-only, self-review |
| Q17 | Code-to-diagram service | static parsing, call graph, LLM summarization, Mermaid, PlantUML |
| Q18 | Knowledge graph from textbooks | metadata extraction, taxonomy, semantic alignment, cross-book dedup |

---

## 5. Expected Output Per LLM

Each of the 10 LLMs produces:

```json
{
  "evaluator_model": "claude-opus-4.5",
  "timestamp": "2025-11-30T...",
  
  "analysis_1_relevance": {
    "baseline": {"relevant": 42, "irrelevant": 8, "ratio": 0.84, "examples": [...]},
    "current": {"relevant": 45, "irrelevant": 5, "ratio": 0.90, "examples": [...]},
    ...
  },
  
  "analysis_2_duplicates": {
    "baseline": {"groups": 23, "examples": [["model", "models"], ...]},
    "current": {"groups": 2, "examples": [...]},
    ...
  },
  
  "analysis_3_cross_refs": {
    "baseline": {"valid": 28, "invalid": 7, "ratio": 0.80, "examples": [...]},
    ...
  },
  
  "analysis_4_noise": {
    "baseline": {"count": 12, "ratio": 0.12, "terms": [...]},
    ...
  },
  
  "analysis_5_navigation": {
    "Q1": {
      "focus_areas": ["chunking", "embeddings", ...],
      "baseline": {"found": 2, "missing": 4, "score": 4},
      "current": {"found": 4, "missing": 2, "score": 7},
      "moderate": {"found": 5, "missing": 1, "score": 8},
      "aggressive": {"found": 6, "missing": 0, "score": 9},
      "best": "aggressive"
    },
    "Q2": {...},
    ... (all 18)
  },
  
  "summary": {
    "navigation_totals": {
      "baseline": 72,
      "current": 98,
      "moderate": 112,
      "aggressive": 124
    },
    "duplicate_reduction": {
      "baseline": 23,
      "current": 2,
      "improvement": "91%"
    },
    "recommendation": "moderate",
    "reasoning": "Best balance of navigation coverage (112/180) with low noise (8%)"
  }
}
```

---

## 6. Aggregation Across 10 LLMs

Final report combines all 10 evaluations:

```json
{
  "consensus": {
    "best_for_navigation": {
      "winner": "moderate",
      "votes": 7,
      "avg_score": 115
    },
    "best_for_deduplication": {
      "winner": "current",
      "baseline_duplicates": 23,
      "current_duplicates": 2
    },
    "question_by_question": {
      "Q1": {"winner": "aggressive", "consensus": 8},
      "Q2": {"winner": "moderate", "consensus": 6},
      ...
    }
  }
}
```

---

## 7. Execution

### Command

```bash
cd /Users/kevintoles/POC/llm-document-enhancer
source ~/.zshrc
python3 scripts/llm_evaluation.py --comparative --rigorous
```

### Expected Time

- 10 LLM calls × ~3 minutes each = ~30-45 minutes
- Plus 3-second delays between calls
- Total: ~1 hour

### Output Location

```
outputs/evaluation/
├── rigorous_evaluation_claude-opus-4.5_<timestamp>.json
├── rigorous_evaluation_claude-sonnet-4.5_<timestamp>.json
├── rigorous_evaluation_gpt-5.1_<timestamp>.json
├── ... (10 files total)
└── rigorous_evaluation_aggregate_<timestamp>.json
```

---

## 8. Success Criteria

| Metric | Baseline | Target (Current/Moderate) |
|--------|----------|---------------------------|
| Duplicate Groups | >15 | <5 |
| Navigation Score (avg/180) | <80 | >100 |
| Questions Won | <5 | >10 |
| Cross-Ref Validity | TBD | >75% |
| Noise Ratio | TBD | <15% |

---

**Status:** READY FOR EXECUTION  
**Next Action:** Update `scripts/llm_evaluation.py` with rigorous prompt  
**Estimated Completion:** 2-3 hours total

