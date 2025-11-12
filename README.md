# LLM Document Enhancer

Intelligent technical documentation enhancement using Claude AI. This tool analyzes programming guidelines and enriches them with precise citations from a curated library of 14 authoritative Python books.

## Features

- **Two-Phase LLM Workflow**: Separates content selection from enhancement for optimal quality
- **Smart Book Taxonomy**: Three-tier categorization system (Architecture Spine, Implementation, Engineering Practices)
- **Intelligent Batching**: Automatic protection against token limits with proactive and reactive constraints
- **Comprehensive Logging**: Full API call tracking with token usage analytics
- **8,598 Pages**: Pre-indexed content from 14 Python programming books

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

### Usage

```bash
# Run from repository root
python3 -m src.integrate_llm_enhancements
```

The tool will:
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

## Architecture

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

### Smart Batching Protection

- **Proactive**: Phase 1 prompt constrains LLM to top 10 books
- **Reactive**: Auto-retry with tighter limits if response truncated
- **Token Monitoring**: 8,192 max output tokens with usage tracking

### Directory Structure

```
llm-document-enhancer/
├── src/                          # Source code
│   ├── integrate_llm_enhancements.py           # Main orchestrator
│   ├── interactive_llm_system_v3_hybrid_prompt.py  # V3 analysis engine
│   ├── llm_integration.py                      # Anthropic API wrapper
│   ├── metadata_extraction_system.py           # Book metadata service
│   ├── book_taxonomy.py                        # Book categorization
│   └── chapter_metadata_manager.py             # Chapter cache loader
│
├── data/                         # Data files
│   ├── textbooks_json/           # 14 book JSONs (~2GB)
│   ├── metadata/                 # 14 metadata JSONs
│   ├── chapter_metadata_cache.json
│   └── chapter_metadata_manual.json
│
├── guidelines/                   # Input documents
│   └── PYTHON_GUIDELINES_*.md    # Base + enhanced versions
│
├── outputs/                      # Generated ENHANCED guidelines
├── logs/                         # API call logs
└── docs/                         # Documentation
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

### Adding New Books

1. Add PDF to conversion queue (requires separate PDF→JSON tool)
2. Generate metadata (requires separate metadata extractor)
3. Update `book_taxonomy.py` with book classification
4. Update `chapter_metadata_cache.json`

### Running Tests

```bash
# Install dev dependencies
pip install pytest

# Run tests
pytest tests/
```

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
python3 -m src.integrate_llm_enhancements

# Not: python3 src/integrate_llm_enhancements.py
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
