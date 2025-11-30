# Keyword Extraction Enhancement Test Plan

**Version:** 3.0  
**Date:** 2025-11-30  
**Branch:** `feature/observability-platform-refactoring`

## 1. Objective

Evaluate whether stem-based keyword deduplication and expanded extraction parameters improve cross-referencing quality in the document enhancement pipeline through **rigorous, verifiable LLM evaluation** using technical system design questions as targeted cross-referencing exercises.

### 1.1 Why This Approach?

Traditional LLM evaluation asks for subjective scores without verification. This approach demands:

1. **Ground Truth Verification**: LLMs must verify extracted keywords against actual chapter content
2. **Concrete Evidence**: Every claim must cite specific examples from the extraction data
3. **Cross-Reference Validation**: Using real technical interview questions to test if the knowledge graph enables meaningful navigation
4. **Quantitative Proof**: Duplicate detection, noise counting, and diversity metrics with actual numbers

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

### 6.1 Evaluation Philosophy: Real Analytical Cross-Referencing

**Problem with Traditional LLM Evaluation:**
- Asks for subjective 1-10 scores without ground truth
- LLMs can "hallucinate" quality assessments
- No verification that cross-references actually make sense
- Surface-level metrics without concrete evidence

**Our Solution: LLM as Knowledge Graph Navigator**

The LLM acts as a **simulated user** navigating the knowledge graph. For each system design question:

1. **The LLM does NOT answer the question** - it has no domain expertise role
2. **The LLM navigates the aggregate** - searching keywords, following cross-references
3. **The LLM reports what it found** - which concepts are discoverable vs missing
4. **The LLM compares aggregates** - which one enabled better navigation

This mimics **production usage**: a user searching the knowledge graph to find relevant content.

### 6.2 Critical Distinction: Navigator, Not Expert

```
❌ WRONG: "To design a multi-agent framework, you need role choreography..."
   (LLM using its own knowledge)

✅ CORRECT: "Searching BASELINE aggregate for 'multi-agent framework':
   - Found keywords: ['agent', 'multi-agent']
   - Missing keywords: ['choreography', 'handoff', 'arbitration']
   - Cross-references led to: Ch14 (Agent Architectures)
   - Could NOT navigate to: coordination patterns, failure handling
   - Navigation success: 4/10"
```

The LLM evaluates **discoverability through the aggregate**, not correctness of answers.

### 6.2 Strategy B: Comparative Evaluation (10 LLM Calls)

All 4 aggregates are sent to each LLM in a single prompt for comparative analysis.

**LLMs Used:**
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

### 6.3 Rigorous Evaluation Framework

The LLM evaluation requires **five concrete analytical tasks**:

#### Task 1: Keyword Relevance Verification
```
For each profile, examine the sample keywords against chapter titles.
- Count how many keywords appear in or relate to their chapter title
- Identify orphan keywords (extracted but contextually irrelevant)
- Calculate: relevance_ratio = relevant_keywords / total_keywords
```

#### Task 2: Duplicate Pattern Detection
```
Scan all keywords for morphological variants:
- Stem duplicates: "model" / "models" / "modeling"
- Phrase overlaps: "neural network" / "neural" / "network"
- Acronym conflicts: "NLP" / "natural language processing"
Report: exact duplicate pairs found, grouped by stem
```

#### Task 3: Cross-Reference Validation
```
For each related_chapter connection:
- Does the source chapter's topic logically connect to target?
- Would a reader find value in this navigation path?
- Are there obvious missing connections?
Report: valid_connections / total_connections, with examples
```

#### Task 4: Noise Term Identification
```
Count generic/non-informative terms:
- Section markers: "introduction", "conclusion", "summary", "example"
- Filler words: "approach", "method", "technique", "system"
- Overly broad: "data", "model", "learning" (without context)
Report: noise_count, noise_ratio, specific examples
```

#### Task 5: System Design Question Navigation Test
```
For each of 18 technical questions, trace the knowledge graph:
- Which keywords would lead to relevant chapters?
- Do cross-references connect the needed concepts?
- What's missing that would help answer the question?
```

### 6.4 Technical System Design Questions (18 Exercises)

These questions test whether the knowledge graph enables real-world technical navigation.
LLMs must trace paths through the extracted keywords and cross-references.

---

#### **Q1: Scalable LLM Code Understanding System**
> "How would you design a system where an LLM reads and understands a 20M-line monorepo and answers queries like 'where is the rate-limiter implemented?'?"

**Focus Areas to Find:**
- Multi-stage chunking
- Embeddings + hierarchical retrieval
- Indexing strategies
- Incremental refresh pipeline
- Grounding LLM outputs
- Safety and hallucination-hardening

---

#### **Q2: Agentic Coding Assistant**
> "How would you design an autonomous agent that can propose code changes and guarantee correctness before merging?"

**Focus Areas to Find:**
- Sandboxed execution
- Static analysis (Ruff, MyPy, Bandit, Semgrep)
- Multi-step plans and self-verification
- Diff-based workflows
- Rollback and guardrails
- Preventing malicious loops or mass deletions

---

#### **Q3: LLM Batch Processing for Multi-GB Datasets**
> "How would you let an LLM process a 5GB JSON dataset without exceeding token limits?"

**Focus Areas to Find:**
- Map/reduce architecture for LLM calls
- Chunk orchestration
- Persistent state
- Embedding-first workflows
- Quality gates / consistency checks
- Metadata propagation

---

#### **Q4: Multi-Model Orchestrator**
> "How would you build a unified interface that can route tasks across GPT-5.1, Claude 4.5, DeepSeek V3, and Gemini 3?"

**Focus Areas to Find:**
- Normalization of responses
- Retry/backoff policies
- Cost/context-aware routing
- Vendor capability detection
- Graceful degradation
- Safe parallelism

---

#### **Q5: Fully Local Fallback System**
> "If all API access to the cloud LLMs went down, how would your system maintain degraded functionality?"

**Focus Areas to Find:**
- Local lightweight inference (Qwen-2.5, Llama-3.3)
- Quantization (GGUF)
- Retrieval-only fallback
- On-device embeddings
- Offline execution constraints

---

#### **Q6: LLM Agent for Infrastructure Automation**
> "How would you design an LLM agent that safely runs DevOps tasks (K8s scaling, monitoring, CD pipeline tasks)?"

**Focus Areas to Find:**
- Tool schemas
- Multi-step verification
- Least-privilege IAM access
- Real-time guardrails
- Journaling and traceability
- Intent classification before taking actions

---

#### **Q7: Multi-Agent Collaboration Framework**
> "Design a multi-agent framework where different agents have roles (planner, coder, critic, tester). How do you avoid collapse or infinite loops?"

**Focus Areas to Find:**
- Role choreography
- Reasoning handoffs
- Arbitration layer
- Self-termination rules
- Confidence scoring feedback loops

---

#### **Q8: Hallucination Prevention in Agentic Systems**
> "How do you prevent an agent from hallucinating when executing actions?"

**Focus Areas to Find:**
- Grounding with tools
- Schema validation
- Runtime safety rails
- Log-probability thresholds
- Runtime synthetic self-tests

---

#### **Q9: 100GB+ Document Indexing System**
> "How do you build a cross-domain semantic index for 100GB of PDFs (books, manuals, code, docs)?"

**Focus Areas to Find:**
- Distributed embedding generation
- Hierarchical indexes (HNSW, IVF)
- Vector pruning
- Metadata joins
- Partial updates
- Cold vs hot storage

---

#### **Q10: Secure Multi-Tenant Fine-Tuning**
> "How would you design a fine-tuning setup that guarantees customer data never leaks between tenants?"

**Focus Areas to Find:**
- Data boundarying
- Per-tenant encryption
- Model snapshot isolation
- No cross-tenant gradients
- Secure data pipelines
- Auditability

---

#### **Q11: 70B Model Inference Latency Reduction**
> "What are the bottlenecks in LLM inference and how would you reduce latency for real-time use?"

**Focus Areas to Find:**
- KV caching
- Speculative decoding
- MoE routing
- Model distillation
- Batching
- Flash-attention
- Quantization

---

#### **Q12: Diagnosing Confident But Incorrect LLM Outputs**
> "Your LLM is making confident but incorrect statements. How do you diagnose?"

**Focus Areas to Find:**
- Retrieval evaluation
- Token-level likelihood inspection
- Multi-pass consistency checks
- Synthetic difficulty datasets
- Chain-of-thought validation
- Hallucination benchmarks

---

#### **Q13: Safety Guardrails for Code-Writing Agents**
> "Design safety guardrails for an agent that can write Python."

**Focus Areas to Find:**
- Static analysis filters
- Unit-test scaffolding
- Exception trapping
- Execution sandboxing
- Rollback and approval workflows
- Anomaly detection

---

#### **Q14: Jailbreak Detection System**
> "How would you detect if a user is trying to jailbreak the system?"

**Focus Areas to Find:**
- Classifier prompts
- Intent detection
- Safety-layer models
- Pattern matching
- Perplexity spikes

---

#### **Q15: Resume-Job Description Matching System**
> "Design a system that automatically reads résumés + job descriptions and outputs a tailored version."

**Focus Areas to Find:**
- Embeddings for skills
- Extraction of job requirements
- Scoring matrices
- Rewriting passes
- Multi-model ensemble

---

#### **Q16: LLM-Powered Refactoring Engine**
> "How would you build Copilot-style 'repo refactor' functionality without hallucinating code removal?"

**Focus Areas to Find:**
- AST awareness
- Snippet-level embedding navigation
- Per-file isolation
- Diff-only policy
- Iterative self-review passes

---

#### **Q17: Code-to-Architecture Diagram Microservice**
> "Build a Python microservice that produces architectural diagrams from code."

**Focus Areas to Find:**
- Static parsing
- Call graph extraction
- LLM summarization
- JSON schema
- Diagram export (Mermaid / PlantUML)

---

#### **Q18: Knowledge Graph from Technical Textbooks**
> "Build a knowledge graph from 12+ technical textbooks."

**Focus Areas to Find:**
- Metadata extraction
- Taxonomy resolution
- Semantic alignment
- Cross-book deduplication
- Enriched guideline generation

---

### 6.5 Navigation Test Protocol (18 Questions)

For each system design question, the LLM performs this **navigation simulation**:

#### Step 1: Extract Search Terms from Question
```
Question: "Design a multi-agent framework with planner/coder/critic/tester roles"
Search terms derived: ["multi-agent", "agent", "planner", "coder", "critic", 
                       "tester", "role", "framework", "coordination"]
```

#### Step 2: Search Each Aggregate's Keywords
```
BASELINE aggregate search results:
  - "agent" → Found in Ch14, Ch22
  - "multi-agent" → NOT FOUND
  - "planner" → NOT FOUND
  - "coordination" → NOT FOUND
  Keywords found: 1/9 (11%)

CURRENT aggregate search results:
  - "agent" → Found in Ch14, Ch22, Ch31
  - "multi-agent" → Found in Ch14
  - "agent coordination" → Found in Ch14
  - "planner" → NOT FOUND
  Keywords found: 3/9 (33%)
```

#### Step 3: Follow Cross-References
```
From Ch14 (Agent Architectures), cross-references lead to:
  - Ch22: Tool Use → Relevant (agents use tools)
  - Ch31: Safety → Relevant (agent guardrails)
  - Ch8: Prompting → Partially relevant

Cross-reference utility: Good - enables discovery of related concepts
```

#### Step 4: Identify Navigation Gaps
```
Focus areas from question that CANNOT be found:
  - "role choreography" → No keywords match
  - "reasoning handoffs" → No keywords match  
  - "arbitration layer" → No keywords match
  - "self-termination" → No keywords match
  
Gap severity: HIGH - core concepts not discoverable
```

#### Step 5: Score Navigation Success
```
BASELINE: 3/10 - Only found generic "agent" keyword
CURRENT: 5/10 - Found "multi-agent" and "coordination" 
MODERATE: 6/10 - Additional concepts captured
AGGRESSIVE: 7/10 - Best coverage but more noise
```

### 6.6 Evaluation Scoring Per Question

For each of the 18 questions, the LLM must report:

```json
{
  "question_id": "Q1",
  "question_title": "Scalable LLM Code Understanding System",
  "navigation_analysis": {
    "keywords_found": ["embeddings", "retrieval", "chunking", "indexing"],
    "keywords_missing": ["hierarchical retrieval", "incremental refresh"],
    "chapters_relevant": [
      {"chapter": 5, "title": "...", "keywords_matching": 3},
      {"chapter": 12, "title": "...", "keywords_matching": 2}
    ],
    "cross_references_useful": true,
    "cross_references_examples": [
      {"from": "Ch5: Embeddings", "to": "Ch12: Vector DBs", "valid": true}
    ],
    "navigation_score": 7,
    "gaps_identified": ["No content on incremental indexing found"]
  }
}
```

### 6.7 Comparative Evaluation Prompt (Revised)

```
You are a KNOWLEDGE GRAPH NAVIGATOR testing the discoverability of technical concepts.

## YOUR ROLE

You are NOT a domain expert. You are simulating a user who needs to find information 
using ONLY the keyword extraction data provided. You cannot use your own knowledge 
to answer questions - you can only report what is DISCOVERABLE through the aggregates.

## CRITICAL RULES

1. DO NOT answer the system design questions yourself
2. DO NOT use your training knowledge to evaluate quality
3. ONLY report what you can find by searching the provided keywords and cross-references
4. Your job is to TEST NAVIGATION, not demonstrate expertise

## NAVIGATION SIMULATION PROTOCOL

For each of 18 system design questions:

1. EXTRACT search terms from the question's focus areas
2. SEARCH each aggregate's sample_keywords for matches
3. FOLLOW cross-references in chapter_analysis.sample_related
4. REPORT what was found vs what was missing
5. SCORE each aggregate on navigation success (1-10)

## EXAMPLE (Follow This Exact Pattern)

Question: "How would you design a multi-agent framework?"
Focus areas: role choreography, reasoning handoffs, arbitration, self-termination

For BASELINE aggregate:
```
Search terms: ["multi-agent", "agent", "choreography", "handoff", "arbitration", "termination"]

Keywords found in sample_keywords:
  - "agent" → YES (appears in list)
  - "multi-agent" → NO
  - "choreography" → NO
  - "handoff" → NO
  - "arbitration" → NO
  - "termination" → NO

Cross-references from relevant chapters:
  - Ch14 → Ch22 (Tool Use): FOLLOWED, found related content
  - Ch14 → Ch31 (Safety): FOLLOWED, found guardrails topic

Focus areas discoverable: 1/5 (only basic "agent")
Focus areas NOT discoverable: choreography, handoffs, arbitration, termination

Navigation score: 3/10
Reasoning: Could only find generic "agent" term, cannot navigate to coordination patterns
```

## REQUIRED ANALYSES

### ANALYSIS 1: Keyword Relevance (search aggregate data only)
For each profile, search sample_keywords and report:
- How many keywords relate to their chapter titles in chapter_analysis?
- List specific relevant/irrelevant examples WITH EVIDENCE from the data

### ANALYSIS 2: Duplicate Detection (examine aggregate data only)
For each profile, scan sample_keywords for:
- Morphological variants (model/models/modeling)
- Report EXACT duplicate pairs found in the data
- Baseline should have MORE duplicates (stem_dedup was OFF)

### ANALYSIS 3: Cross-Reference Tracing (follow the links)
For each profile's chapter_analysis.sample_related:
- Trace each cross-reference
- Report: Does source topic logically connect to target?
- Count valid vs invalid connections WITH EXAMPLES

### ANALYSIS 4: Noise Identification (count in sample_keywords)
For each profile, count these terms in sample_keywords:
- Section markers: "introduction", "conclusion", "summary"
- Generic terms: "approach", "method", "technique", "example"
- Report exact counts and list the noise terms found

### ANALYSIS 5: Navigation Test (18 Questions)

For EACH question, simulate navigation through each aggregate:

Q1: "Design a system where an LLM reads a 20M-line monorepo"
    Focus: chunking, embeddings, retrieval, indexing, grounding, hallucination-hardening
    → Search sample_keywords for these terms
    → Follow cross-references to find related content
    → Report per-aggregate: found, missing, navigation score

Q2: "Design an autonomous agent that proposes code changes safely"
    Focus: sandboxing, static analysis, verification, diff-based, rollback, guardrails
    → Search and report per-aggregate

[... Q3-Q18 follow same pattern - search, trace, report ...]

For each question, your output must show:
- The search terms you extracted
- Per-aggregate: exact keywords found in sample_keywords
- Per-aggregate: which cross-references you followed
- Per-aggregate: what focus areas are NOT discoverable
- Navigation score (1-10) per aggregate
- Which aggregate enabled best navigation

## OUTPUT FORMAT

{
  "analysis_1_relevance": {
    "baseline": {"relevant": N, "irrelevant": N, "evidence": [{"keyword": "X", "in_chapter": "Y", "relevant": true}]},
    ...
  },
  "analysis_2_duplicates": {
    "baseline": {"groups_found": N, "examples_from_data": [["model", "models"], ...]},
    ...
  },
  "analysis_3_cross_refs": {
    "baseline": {"traced": N, "valid": N, "invalid": N, "examples": [{"from": "Ch5", "to": "Ch12", "valid": true, "reason": "..."}]},
    ...
  },
  "analysis_4_noise": {
    "baseline": {"noise_terms_found": ["introduction", "example", ...], "count": N},
    ...
  },
  "analysis_5_navigation": {
    "Q1": {
      "question": "Design a system where an LLM reads a 20M-line monorepo",
      "focus_areas": ["chunking", "embeddings", "retrieval", ...],
      "baseline": {
        "keywords_found": ["embedding"],
        "keywords_missing": ["chunking", "retrieval", "indexing"],
        "cross_refs_followed": [{"from": "Ch3", "to": "Ch7", "helpful": true}],
        "score": 4
      },
      "current": {...},
      "moderate": {...},
      "aggressive": {...},
      "best_aggregate": "aggressive",
      "reasoning": "Aggressive found 'chunking' and 'hierarchical retrieval' that others missed"
    },
    ... (all 18 questions)
  },
  "final_ranking": {
    "by_navigation_total": [{"profile": "moderate", "total_score": 112}, ...],
    "by_duplicate_reduction": [{"profile": "current", "duplicates": 2}, {"profile": "baseline", "duplicates": 23}],
    "by_noise_ratio": [...],
    "overall_recommendation": "moderate",
    "evidence": "Moderate won 11/18 navigation tests, had 0 duplicates, 8% noise ratio"
  }
}
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
