# LLM Document Enhancer

**A Pipeline-Based Document Processing Engine** for transforming technical books into enhanced, cross-referenced programming guidelines using LLM-powered analysis.

This system processes 14 authoritative Python programming books through a 7-stage workflow pipeline, generating comprehensive guidelines enriched with intelligent cross-references, scholarly annotations, and concept validations.

## Architecture: Workflow-Based Pipeline

This application implements a **7-stage document processing pipeline** with Domain-Driven Design principles:

```
Stage 1: Taxonomy Setup          → Configure book categorization system
Stage 2: PDF to JSON              → Convert source PDFs to searchable JSON
Stage 3: Metadata Extraction      → Extract chapter/page metadata from books
Stage 4: Metadata Cache Merge     → Consolidate metadata for fast lookup
Stage 5: Metadata Enrichment      → Add concept tags and keywords
Stage 6: Base Guideline Generation → Generate foundational guideline structure
Stage 7: LLM Enhancement          → Enhance with citations and annotations
```

**Architecture Type:** Modular Monolith with Pipeline Pattern
- Each workflow stage is a **bounded context** (DDD concept)
- Shared infrastructure layer for cross-cutting concerns
- Sequential data transformation with clear input/output contracts
- Not a microservices architecture (single deployable unit)
- Not a traditional monolith (clear separation via workflows)

## Key Features

- **7-Stage Pipeline Architecture**: Progressive enhancement from raw PDFs to enriched guidelines
- **Smart Book Taxonomy**: Three-tier categorization (Architecture Spine, Implementation, Engineering Practices)
- **Two-Phase LLM Workflow**: Separates content selection from enhancement for optimal quality
- **Provider Abstraction**: Protocol-based LLM interface (Anthropic, OpenAI-ready)
- **Caching System**: File-based cache with TTL reduces costs by 99%+
- **Retry Logic**: Exponential backoff with automatic constraint tightening
- **Type-Safe Configuration**: Python dataclasses + .env for secure, validated settings
- **Comprehensive Testing**: 137 unit tests, full pipeline validation
- **8,598 Pages Indexed**: Pre-processed content from 14 Python books

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Anthropic API key ([get one here](https://console.anthropic.com/))

### Installation

```bash
# Clone the repository
git clone https://github.com/kevin-toles/llm-document-enhancer.git
cd llm-document-enhancer

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Configuration

The system uses a hybrid **`.env` + Python dataclasses** configuration approach:

```bash
# .env file (edit this)
ANTHROPIC_API_KEY=your-api-key-here
ANTHROPIC_MODEL=claude-sonnet-4-5-20250929
LLM_MAX_TOKENS=8192
TAXONOMY_MAX_BOOKS=10
CACHE_ENABLED=true
```

All settings are documented in `.env.example`. Configuration is:
- **Type-safe**: Python dataclasses provide validation and IDE autocomplete
- **Secure**: API keys in `.env` (gitignored, never committed)
- **Flexible**: Override any setting via environment variables

#### Viewing Current Configuration

```bash
# Display all settings
python3 -c "from config.settings import settings; settings.display()"
```

#### Configuration in Code

```python
from config.settings import settings

# Type-safe access with autocomplete
max_tokens = settings.llm.max_tokens
cache_enabled = settings.cache.enabled
min_relevance = settings.taxonomy.min_relevance
```

See `examples/config_usage.py` for more examples.

### Running Workflows

Each workflow stage can be run independently or as part of the full pipeline:

```bash
# Run full LLM enhancement workflow (Stages 6-7)
python3 -m workflows.llm_enhancement.scripts.integrate_llm_enhancements

# Run base guideline generation (Stage 6)
python3 -m workflows.base_guideline_generation.scripts.chapter_generator_all_text

# Run metadata extraction (Stage 3)
python3 -m workflows.metadata_extraction.scripts.adapters.metadata_extractor
```

**LLM Enhancement Workflow** (Stages 6-7):
1. Load 14 books (8,598 pages) and 277 chapter metadata entries
2. Read the base guideline document
3. Execute Phase 1: Analyze guideline and select relevant book content
4. Execute Phase 2: Enhance guideline with citations and validations
5. Generate enhanced output in `outputs/` directory

## Book Library

### Architecture Spine (Tier 1)
- Architecture Patterns with Python
- Microservice Architecture
- Building Microservices

### Implementation (Tier 2)
- Building Python Microservices with FastAPI
- Microservice APIs Using Python Flask FastAPI
- Python Microservices Development
- Microservices Up and Running
- Python Architecture Patterns

### Engineering Practices (Tier 3)
- Learning Python Ed6
- Fluent Python 2nd
- Python Cookbook 3rd
- Python Distilled
- Python Essential Reference 4th
- Python Data Analysis 3rd

## Design Patterns & Principles

This system implements several architectural patterns from **Architecture Patterns with Python** and **Domain-Driven Design**:

### Patterns Used

1. **Pipeline Pattern** (7 workflow stages)
   - Sequential data transformation
   - Clear stage boundaries
   - Independent execution

2. **Repository Pattern** (`workflows/metadata_extraction/`)
   - Abstracts book data access
   - Encapsulates data retrieval logic
   - Enables testing with mock data

3. **Provider Pattern** (`workflows/shared/providers/`)
   - Protocol-based abstraction for LLM APIs
   - Pluggable implementations (Anthropic, OpenAI-ready)
   - Dependency injection via protocols

4. **Adapter Pattern** (Each workflow stage)
   - Adapts different input/output formats
   - Wraps external dependencies
   - Clean integration boundaries

5. **Template Pattern** (`workflows/shared/prompts/`)
   - Reusable prompt templates
   - Parameterized text generation
   - Separation of logic and content

### DDD Concepts

- **Bounded Contexts**: Each workflow stage is a bounded context
- **Shared Kernel**: `workflows/shared/` provides common infrastructure
- **Domain Events**: Pipeline stages communicate via well-defined contracts
- **Value Objects**: Immutable data structures (PageReference, BookMetadata)

### Two-Phase Workflow

**Phase 1: Content Selection**
- Analyzes guideline document sections
- Identifies concepts needing citations
- Selects top 10 most relevant books using taxonomy scoring
- Requests specific chapters/sections from books
- **Output**: JSON array of content requests

**Phase 2: Enhancement**
- Receives selected book content
- Adds `SOURCE_REFERENCE` citations
- Inserts `CONCEPT_VALIDATION` blocks
- Preserves original structure and numbering
- **Output**: Enhanced markdown with citations

### Smart Batching & Resilience

- **Proactive**: Phase 1 prompt constrains LLM to top 10 books
- **Reactive**: Auto-retry with tighter limits if response truncated
- **Caching**: Automatic cache hits reduce API calls by 99%+
- **Retry Logic**: Exponential backoff on transient failures
- **Token Monitoring**: 8,192 max output tokens with usage tracking

## System Architecture

### Overview: Pipeline-Based Document Processing

```
┌─────────────────────────────────────────────────────────────────┐
│                   7-Stage Workflow Pipeline                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [1] Taxonomy Setup    →  Configure book categorization         │
│  [2] PDF to JSON       →  Convert source materials              │
│  [3] Metadata Extract  →  Extract chapter/page metadata         │
│  [4] Cache Merge       →  Consolidate for fast lookup           │
│  [5] Enrichment        →  Add concepts and tags                 │
│  [6] Base Generation   →  Generate guideline structure          │
│  [7] LLM Enhancement   →  Add citations and annotations         │
│                                                                  │
└────────┬──────────────────┬─────────────────┬──────────────────┘
         │                  │                 │
         ▼                  ▼                 ▼
┌─────────────────┐  ┌──────────────┐  ┌────────────────┐
│ Shared Layer    │  │  Providers   │  │  Configuration │
├─────────────────┤  ├──────────────┤  ├────────────────┤
│ • Loaders       │  │ • LLM API    │  │ • Settings     │
│ • Prompts       │  │ • Retry      │  │ • Paths        │
│ • Pipeline      │  │ • Cache      │  │ • .env         │
│ • Phases        │  │ • Protocols  │  │ • Type-safe    │
└─────────────────┘  └──────────────┘  └────────────────┘
```

**Architecture Pattern:** Workflow-Based Pipeline with DDD

Each stage is a **bounded context** that:
- Has clear input/output contracts
- Can be run independently
- Shares infrastructure via `workflows/shared/`
- Follows single responsibility principle

### Directory Structure

```
llm-document-enhancer/
├── workflows/                    # 7-stage pipeline
│   ├── taxonomy_setup/          # Stage 1: Book categorization
│   ├── pdf_to_json/             # Stage 2: PDF conversion
│   ├── metadata_extraction/     # Stage 3: Metadata extraction
│   ├── metadata_cache_merge/    # Stage 4: Cache consolidation
│   ├── metadata_enrichment/     # Stage 5: Concept tagging
│   ├── base_guideline_generation/  # Stage 6: Base generation
│   ├── llm_enhancement/         # Stage 7: LLM enhancement
│   │   ├── scripts/             # Main workflow scripts
│   │   └── phases/              # Phase 1/2 logic
│   │
│   └── shared/                  # Shared infrastructure
│       ├── providers/           # LLM provider abstraction
│       │   ├── base.py         # Protocol & response types
│       │   ├── anthropic.py    # Anthropic implementation
│       │   └── retry.py        # Retry decorator
│       ├── loaders/            # Data loading utilities
│       ├── prompts/            # LLM prompt templates
│       │   ├── templates.py    # Template loader
│       │   ├── phase1.txt      # Phase 1 prompt
│       │   └── phase2.txt      # Phase 2 prompt
│       ├── pipeline/           # Pipeline orchestration
│       ├── phases/             # Phase management
│       ├── cache.py            # Caching system
│       ├── retry.py            # Retry logic
│       └── llm_integration.py  # LLM integration
│
├── config/                      # Configuration
│   ├── settings.py             # Central settings (dataclasses)
│   ├── requirements.txt        # Production dependencies
│   └── requirements-dev.txt    # Development dependencies
│
├── tests/                       # Test suite (137 tests)
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   ├── e2e/                    # End-to-end tests
│   └── fixtures/               # Test fixtures
│
├── data/                        # Data files (gitignored)
│   ├── textbooks_json/         # 14 book JSONs (~2GB)
│   └── metadata/               # Chapter metadata
│
├── docs/                        # Documentation
│   ├── architecture/           # Architecture docs
│   ├── workflows/              # Workflow guides
│   └── WORKFLOW_DECISION_FRAMEWORK.md
│
├── tools/                       # Repository validation tools
├── examples/                    # Usage examples
├── outputs/                     # Generated guidelines
├── logs/                        # API call logs
└── coderabbit/                 # Code quality tools
```

## Configuration

Edit `.env` file:

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-api03-...

# Optional (defaults shown)
LLM_PROVIDER=anthropic
ANTHROPIC_MODEL=claude-sonnet-4-5-20250929
LLM_TEMPERATURE=0.2
LLM_MAX_TOKENS=8192
```

## Development

### Recent Migration (November 2025)

**Workflow Reorganization** - See [MIGRATION_PLAN.md](MIGRATION_PLAN.md) and [REFACTORING_PLAN.md](REFACTORING_PLAN.md)

- ✅ **7-Stage Pipeline Architecture**: Moved from `src/` to `workflows/` structure
- ✅ **Shared Infrastructure Layer**: `workflows/shared/` for cross-cutting concerns
- ✅ **Provider Abstraction**: Protocol-based LLM interface (Anthropic, OpenAI-ready)
- ✅ **Caching System**: File-based cache with TTL (99%+ cost reduction)
- ✅ **Type-Safe Configuration**: Python dataclasses + .env
- ✅ **Comprehensive Testing**: 137 unit tests (100% passing)
- ✅ **Clean Separation**: Each workflow stage is independent bounded context

**Benefits**:
- **Modularity**: Each stage can be developed/tested independently
- **Cost Savings**: 99%+ reduction on repeated runs via caching
- **Reliability**: Automatic retry with exponential backoff
- **Maintainability**: Clear boundaries, single responsibility
- **Testability**: Protocol-based design with dependency injection
- **Extensibility**: Easy to add new stages or LLM providers

### Adding New Books

1. Add PDF to conversion queue (requires separate PDF→JSON tool)
2. Generate metadata (requires separate metadata extractor)
3. Update `book_taxonomy.py` with book classification
4. Update `chapter_metadata_cache.json`

### Running Tests

```bash
# Install dev dependencies
pip install -r config/requirements-dev.txt

# Run all tests (137 tests)
ANTHROPIC_API_KEY=test_key python3 -m pytest tests/unit/

# Run specific test suite
pytest tests/unit/test_providers.py -v

# Run with coverage
pytest tests/unit/ --cov=workflows --cov-report=html
```

**Test Coverage:**
- 137 unit tests (100% passing)
- Provider abstraction tests
- Configuration validation tests
- Pipeline adapter tests
- Cache functionality tests

## API Usage & Costs

- **Model**: Claude Sonnet 4 (claude-sonnet-4-5-20250929)
- **Context**: 200K tokens input
- **Output**: 8,192 tokens max per request
- **Typical Usage**: ~20K input + ~3K output tokens per chapter

Example costs (as of Nov 2025):
- Input: $3 per million tokens
- Output: $15 per million tokens
- **Single Chapter**: ~$0.10-$0.15

## Logging

All API calls are logged to `logs/llm_api/` as JSON:

```json
{
  "timestamp": "2025-11-11T19:30:45.123456",
  "provider": "anthropic",
  "model": "claude-sonnet-4-5-20250929",
  "input_tokens": 15224,
  "output_tokens": 2464,
  "request": "...",
  "response": "...",
  "finish_reason": "end_turn"
}
```

## Troubleshooting

### Import Errors

```bash
# Ensure running as module from repo root
python3 -m workflows.llm_enhancement.scripts.integrate_llm_enhancements

# Not: python3 workflows/llm_enhancement/scripts/integrate_llm_enhancements.py
```

### Missing Data Files

```bash
# Verify all data files present
ls data/textbooks_json/*.json | wc -l   # Should be 14
ls data/metadata/*.json | wc -l         # Should be 14
```

### API Key Issues

```bash
# Check .env file exists and has key
test -f .env && echo "Found" || echo "Missing .env"
grep ANTHROPIC_API_KEY .env
```

## License

MIT License - See LICENSE file

## Author

Kevin Toles - [GitHub](https://github.com/kevin-toles)

## Acknowledgments

- Built with [Anthropic Claude](https://www.anthropic.com/)
- Book content from O'Reilly, Addison-Wesley, and other publishers
- Inspired by the need for precision in technical documentation
