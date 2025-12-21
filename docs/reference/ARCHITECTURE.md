# LLM Document Enhancer - Application

## Overview

The LLM Document Enhancer is an **application** (not a microservice) that transforms raw technical documentation into cross-referenced guidelines. It consumes the LLM Gateway, AI Agents, Semantic Search, and Code-Orchestrator microservices to perform its work.

## Architecture Type

**Application** - A batch processing application that runs on-demand or scheduled. It is a **consumer** of the microservices infrastructure, not a service itself.

---

## Kitchen Brigade Role: CUSTOMER

In the Kitchen Brigade architecture, **llm-document-enhancer** is a **Customer** - it places orders and receives the final dish:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                          👤 CUSTOMER - ORDER PLACER                          │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  WHAT IT DOES:                                                               │
│  ─────────────                                                               │
│  ✓ Places orders (calls services via HTTP)                                  │
│  ✓ Receives results (enriched metadata, cross-references)                   │
│  ✓ Writes output files ({book}_enriched.json)                               │
│  ✓ Orchestrates the 6-step workflow pipeline                                │
│                                                                              │
│  SIMILARITY COMPUTATION (IMPLEMENTED 2025-12-14):                           │
│  ─────────────────────────────────────────────────                          │
│  ✓ SemanticSimilarityEngine with SBERT (all-MiniLM-L6-v2)                   │
│  ✓ Auto-fallback to TF-IDF when sentence-transformers unavailable           │
│  ✓ 47 books, 1922 chapters, 9614 similar_chapters links                     │
│  ✓ Method tracked: "sentence_transformers" or "tfidf"                       │
│                                                                              │
│  FUTURE ENHANCEMENT (Code-Orchestrator Integration):                        │
│  ───────────────────────────────────────────────────                        │
│  For CODE-SPECIFIC content, call Code-Orchestrator-Service:                 │
│  • CodeBERT: Code↔NL search                                                 │
│  • GraphCodeBERT: Code structure understanding                              │
│  • CodeT5+: Code generation                                                 │
│                                                                              │
│  Note: Textbook content uses SBERT (text similarity).                       │
│        Code examples/repositories use Code-Orchestrator.                    │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Current vs Target Data Flow

```
CURRENT STATE (Broken - Zero Cross-Book References):
─────────────────────────────────────────────────────
enrich_metadata_per_book.py
    ├─→ TfidfVectorizer (sklearn, local)
    ├─→ cosine_similarity with threshold=0.7
    ├─→ find_related_chapters() returns ZERO cross-book
    └─→ Only within-book references (max TF-IDF ~0.50 cross-book)

TARGET STATE (Semantic Cross-References):
─────────────────────────────────────────
enrich_metadata_per_book.py
    │
    │ --use-orchestrator flag
    ▼
Code-Orchestrator-Service (Port 8083)
    │
    ├─→ CodeT5+ extracts semantic terms from chapter text
    ├─→ GraphCodeBERT validates terms (filters generic)
    ├─→ CodeBERT ranks by embedding similarity
    │
    ▼
Semantic Search Service (Port 8081)
    │
    ├─→ Queries Qdrant with validated terms
    ├─→ Returns ALL matches
    │
    ▼
Code-Orchestrator-Service (Curation)
    │
    ├─→ Filters domain mismatches (C++ chunks vs LLM chunks)
    ├─→ Ranks by relevance to original query
    ├─→ Returns curated cross-book references
    │
    ▼
enrich_metadata_per_book.py
    │
    └─→ Writes {book}_enriched.json with REAL cross-references
```

---

## Folder Structure

```
llm-document-enhancer/
├── src/
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── main.py                  # Typer CLI entry point
│   │   ├── enhance.py               # enhance command
│   │   ├── index.py                 # index command (build indices)
│   │   └── evaluate.py              # evaluate command
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                # Pydantic settings
│   │   └── exceptions.py
│   │
│   ├── clients/
│   │   ├── __init__.py
│   │   ├── gateway_client.py        # HTTP client for llm-gateway
│   │   ├── search_client.py         # HTTP client for semantic-search
│   │   └── agents_client.py         # HTTP client for ai-agents (optional)
│   │
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── pipeline.py              # Main ingestion orchestrator
│   │   ├── parsers/
│   │   │   ├── __init__.py
│   │   │   ├── pdf.py               # PDF text extraction
│   │   │   ├── markdown.py          # Markdown parsing
│   │   │   └── json.py              # JSON/YAML metadata
│   │   ├── structure/
│   │   │   ├── __init__.py
│   │   │   ├── detector.py          # Chapter/section detection
│   │   │   └── chunker.py           # Semantic chunking
│   │   └── metadata/
│   │       ├── __init__.py
│   │       ├── extractor.py         # Metadata extraction
│   │       └── tier_assigner.py     # Tier assignment logic
│   │
│   ├── precompute/
│   │   ├── __init__.py
│   │   ├── pipeline.py              # Pre-compute orchestrator
│   │   ├── keywords/
│   │   │   ├── __init__.py
│   │   │   ├── yake_extractor.py    # YAKE keyword extraction
│   │   │   └── tfidf.py             # TF-IDF vectors
│   │   ├── similarity/
│   │   │   ├── __init__.py
│   │   │   └── matcher.py           # Pre-compute similar chunks
│   │   └── topics/
│   │       ├── __init__.py
│   │       └── assigner.py          # Topic assignment via service
│   │
│   ├── enhancement/
│   │   ├── __init__.py
│   │   ├── pipeline.py              # 3-step enhancement orchestrator
│   │   ├── steps/
│   │   │   ├── __init__.py
│   │   │   ├── step1_hierarchy.py   # Step 1: Document Hierarchy Review
│   │   │   ├── step2_crossref.py    # Step 2: Cross-Referencing
│   │   │   └── step3_conflict.py    # Step 3: Conflict Resolution
│   │   ├── prompts/
│   │   │   ├── __init__.py
│   │   │   ├── hierarchy.py
│   │   │   ├── crossref.py
│   │   │   └── conflict.py
│   │   └── tools/
│   │       ├── __init__.py
│   │       └── definitions.py       # Tool definitions for LLM
│   │
│   ├── output/
│   │   ├── __init__.py
│   │   ├── writer.py                # Write enhanced guidelines
│   │   ├── crossref_index.py        # Generate cross-reference index
│   │   └── evaluation.py            # Generate evaluation report
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── document.py              # Document, Chunk, Section models
│   │   ├── match.py                 # Match, Conflict models
│   │   └── output.py                # Output models
│   │
│   └── main.py                      # Alternative entry point
│
├── tests/
│   ├── unit/
│   │   ├── test_ingestion/
│   │   ├── test_precompute/
│   │   └── test_enhancement/
│   ├── integration/
│   │   └── test_full_pipeline.py
│   └── conftest.py
│
├── config/
│   ├── settings.py                  # Default settings
│   ├── chapter_patterns.json        # Chapter detection patterns
│   ├── extraction_profiles.json     # Per-doc-type extraction rules
│   ├── metadata_keywords.json       # Domain keyword lists
│   ├── tier_taxonomy.json           # Tier assignments
│   └── validation_rules.json        # Output validation
│
├── data/
│   ├── corpus/                      # Input documents (gitignored)
│   ├── guidelines/                  # Baseline guidelines
│   └── cache/                       # Pre-compute cache (gitignored)
│
├── outputs/                         # Generated outputs (gitignored)
│
├── docs/
│   ├── ARCHITECTURE.md              # This file
│   ├── WORKFLOW.md                  # Enhancement workflow details
│   ├── CONFIG.md                    # Configuration guide
│   └── EVALUATION.md                # Evaluation methodology
│
├── scripts/
│   ├── run_enhance.sh
│   └── build_indices.sh
│
├── Dockerfile                       # For containerized runs
├── docker-compose.yml               # Local dev with services
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## System Context

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                      LLM DOCUMENT ENHANCER (Application)                      │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                           CLI Interface                                  │ │
│  │  $ doc-enhancer index --corpus ./data/corpus                            │ │
│  │  $ doc-enhancer enhance --guidelines ./data/guidelines/baseline.md      │ │
│  │  $ doc-enhancer evaluate --output ./outputs/enhanced.md                 │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                      │                                        │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                        PROCESSING PIPELINE                               │ │
│  │                                                                          │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐   │ │
│  │  │  Ingestion   │─▶│  Pre-Compute │─▶│ Enhancement  │─▶│   Output   │   │ │
│  │  │              │  │              │  │  (3-Step)    │  │            │   │ │
│  │  │ • PDF parse  │  │ • YAKE       │  │ 1. Hierarchy │  │ • Markdown │   │ │
│  │  │ • Structure  │  │ • TF-IDF     │  │ 2. Cross-Ref │  │ • JSON idx │   │ │
│  │  │ • Chunking   │  │ • Similarity │  │ 3. Conflict  │  │ • Report   │   │ │
│  │  │ • Metadata   │  │ • Topics     │  │              │  │            │   │ │
│  │  └──────────────┘  └──────┬───────┘  └──────┬───────┘  └────────────┘   │ │
│  │                           │                 │                            │ │
│  └───────────────────────────┼─────────────────┼────────────────────────────┘ │
│                              │                 │                              │
└──────────────────────────────┼─────────────────┼──────────────────────────────┘
                               │                 │
              ┌────────────────┴─────┬───────────┴────────────────┐
              ▼                      ▼                            ▼
   ┌──────────────────┐   ┌──────────────────┐         ┌──────────────────┐
   │ semantic-search  │   │ llm-gateway      │         │ ai-agents        │
   │ microservice     │   │ microservice     │         │ microservice     │
   │ (Port 8081)      │   │ (Port 8080)      │         │ (Port 8082)      │
   │                  │   │                  │         │ (optional)       │
   │ • Embed chunks   │   │ • LLM calls      │         │                  │
   │ • Search similar │   │ • Tool execution │         │                  │
   │ • Topic inference│   │ • Sessions       │         │                  │
   └──────────────────┘   └──────────────────┘         └──────────────────┘
```

---

## CLI Commands

| Command | Description |
|---------|-------------|
| `doc-enhancer index` | Ingest documents and build indices |
| `doc-enhancer precompute` | Run pre-compute pipeline (similarity, topics) |
| `doc-enhancer enhance` | Run 3-step enhancement on guidelines |
| `doc-enhancer evaluate` | Evaluate enhanced output quality |
| `doc-enhancer full` | Run complete pipeline (index → precompute → enhance → evaluate) |

---

## Processing Pipeline

### 1. Ingestion
- Parse PDFs, Markdown, JSON sources
- Detect document structure (chapters, sections)
- Chunk into semantic units
- Extract metadata, assign tiers

### 2. Pre-Compute
- YAKE keyword extraction (local)
- TF-IDF vector generation (local)
- Similarity matching via semantic-search microservice
- Topic assignment via semantic-search microservice

### 3. Enhancement (3-Step Process)
All steps use the **llm-gateway microservice** for LLM inference:

**Step 1: Document Hierarchy Review**
- Validate tier assignments
- Verify chapter/section extraction
- Identify key concepts

**Step 2: Guideline Concept Review & Cross-Referencing**
- For each guideline section, provide pre-computed matches
- LLM validates matches and builds cross-references
- LLM can use tools to retrieve additional context

**Step 3: Conflict Identification & Resolution**
- Present potential conflicts from pre-compute
- LLM applies tier-based priority rules
- LLM synthesizes resolutions with citations

### 4. Output
- Write enhanced guidelines (Markdown)
- Generate cross-reference index (JSON)
- Generate evaluation report (JSON)

---

## CME-1.0: Configurable Metadata Extraction (NEW)

**Feature**: Configurable Metadata Extraction  
**Status**: ✅ COMPLETE (December 2025)  
**Architecture Document**: [CME_ARCHITECTURE.md](../../../textbooks/pending/platform/CME_ARCHITECTURE.md)

### Overview

CME-1.0 adds a configurable toggle to switch between two metadata extraction implementations:

| Mode | Flag Value | Description |
|------|------------|-------------|
| **Local** | `use_orchestrator=False` | StatisticalExtractor (YAKE + Summa). Fast, offline, may include noise. |
| **Orchestrator** | `use_orchestrator=True` | Code-Orchestrator-Service API. TF-IDF + noise filtering, higher quality. |

### Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  llm-document-enhancer                                                      │
│                                                                             │
│  ┌─────────────────────────────┐      ┌─────────────────────────────────┐   │
│  │ MetadataExtractionClient    │─────►│ Code-Orchestrator-Service       │   │
│  │ (httpx async client)        │      │ :8083                           │   │
│  │ ├── extract_metadata()      │ HTTP │                                 │   │
│  │ └── health_check()          │◄─────│ POST /api/v1/metadata/extract   │   │
│  └─────────────────────────────┘      │ ├── TF-IDF keywords             │   │
│                                       │ ├── Concept extraction          │   │
│         OR (fallback)                 │ ├── Noise validation            │   │
│                 │                     │ └── Quality scoring             │   │
│                 ▼                     └─────────────────────────────────┘   │
│  ┌─────────────────────────────┐                                            │
│  │ StatisticalExtractor        │                                            │
│  │ (fallback if service down)  │                                            │
│  └─────────────────────────────┘                                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Toggle Methods

```bash
# Default: Local StatisticalExtractor
python3 generate_metadata_universal.py --input book.json

# Orchestrator via CLI flag (takes precedence)
python3 generate_metadata_universal.py --input book.json --use-orchestrator

# Orchestrator via env var
EXTRACTION_USE_ORCHESTRATOR_EXTRACTION=true python3 generate_metadata_universal.py --input book.json

# With fallback disabled (strict mode)
python3 generate_metadata_universal.py --input book.json --use-orchestrator --no-fallback
```

### Configuration

```python
# config/extraction_settings.py
class ExtractionSettings(BaseSettings):
    use_orchestrator_extraction: bool = False  # Default: local
    orchestrator_url: str = "http://localhost:8083"
    fallback_on_error: bool = True
    
    model_config = SettingsConfigDict(env_prefix="EXTRACTION_")
```

### Files

| File | Description |
|------|-------------|
| `config/extraction_settings.py` | Pydantic Settings with EXTRACTION_* prefix |
| `workflows/shared/clients/metadata_client.py` | MetadataExtractionClient + FakeClient |
| `workflows/metadata_extraction/scripts/generate_metadata_universal.py` | Generator with --use-orchestrator flag |

---

## Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| llm-gateway | Microservice | LLM inference for enhancement steps |
| semantic-search-service | Microservice | Embedding, search, topics |
| ai-agents | Microservice (optional) | Code review for code examples in docs |

---

## Local Development

```yaml
# docker-compose.yml
services:
  # The microservices this application depends on
  semantic-search:
    image: semantic-search-service:latest
    ports:
      - "8081:8081"

  llm-gateway:
    image: llm-gateway:latest
    ports:
      - "8080:8080"
    depends_on:
      - semantic-search

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

```bash
# Run the application (not as a service)
$ doc-enhancer enhance \
    --corpus ./data/corpus \
    --guidelines ./data/guidelines/baseline.md \
    --output ./outputs/enhanced.md \
    --gateway-url http://localhost:8080 \
    --search-url http://localhost:8081
```

---

## Configuration

```python
# src/core/config.py
class Settings(BaseSettings):
    # Microservice URLs
    llm_gateway_url: str = "http://localhost:8080"
    semantic_search_url: str = "http://localhost:8081"
    ai_agents_url: str = "http://localhost:8082"
    
    # Paths
    corpus_path: str = "./data/corpus"
    guidelines_path: str = "./data/guidelines"
    output_path: str = "./outputs"
    cache_path: str = "./data/cache"
    
    # Pre-compute settings
    chunk_size: int = 512
    chunk_overlap: int = 64
    yake_num_keywords: int = 20
    similarity_top_k: int = 10
    similarity_threshold: float = 0.7
    
    # Enhancement settings
    default_model: str = "claude-3-sonnet-20240229"
    max_tool_calls_per_section: int = 5
    
    class Config:
        env_prefix = "DOC_ENHANCER_"
```

---

## Not a Microservice

This application:
- ✅ Runs on-demand or scheduled (batch job)
- ✅ Consumes microservices via HTTP
- ✅ Has no REST API of its own
- ✅ Does not need to be "up" 24/7
- ✅ Can run locally, in CI/CD, or as a K8s Job
