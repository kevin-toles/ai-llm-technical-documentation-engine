# Workflow-Based Repository Reorganization

## Status: Planning Phase

**Last Updated:** November 15, 2025

---

## ⚠️ Notes to Revisit

### Taxonomy Configuration Generation
- **Script Location:** `workflows/1-taxonomy/scripts/generate_taxonomy_config.py`
- **Output Location:** `workflows/1-taxonomy/output/taxonomy_config.json`
- **Purpose:** Generate taxonomy_config.json from Python taxonomy definitions
- **Status:** Stubbed placeholder - needs implementation details
- **TODO:** Determine when/how this script runs
  - Part of initial setup?
  - Run on taxonomy updates?
  - Manual vs automated execution?

---

## Workflow Overview

Starting from: **Person has PDF textbooks and wants to create enhanced guideline documentation**

### Workflow Stages

Based on the TPM (tpm-job-finder-poc) workflow, the complete end-to-end process is:

1. **Taxonomy & Project Setup** - Define book taxonomy and project configuration
2. **PDF → JSON Conversion** - Convert PDF textbooks to structured JSON with page numbers
3. **Per-Book Metadata Extraction** - For each book, extract chapter structure (titles, page ranges, summaries, keywords, concepts) from JSON files
4. **Metadata Cache Merging** - Merge all per-book metadata JSON files into central `chapter_metadata_cache.json`
5. **Metadata Cache Enrichment** - Update/enrich the central cache with additional metadata from textbook JSON content
6. **Base Guideline Generation** - Generate base comprehensive guidelines from metadata cache + JSON (without LLM enhancement)
7. **LLM Enhancement** - Enhance base guidelines with interactive two-phase LLM analysis (metadata analysis → targeted content extraction → scholarly annotation)
8. **Pipeline Orchestration** - Coordinate entire process with retry logic, caching, and error handling

**Note:** In this repository, workflows 3-4 have already been completed (14 metadata JSON files exist in `data/metadata/` and the central cache exists at `data/chapter_metadata_cache.json`). The per-book metadata generators and merge script are not present because they were already run in the TPM project.

---

## Proposed Directory Structure

**Note:** This shows the TARGET structure after migration. Only workflows 1, 2, 3, 4, and 7 contain actual existing files. The structure below shows where current files will be relocated.

```
llm-document-enhancer/
│
├── (root files stay unchanged - see file mapping below)
├── config/ (stays)
├── docs/ (stays)
├── scripts/ (stays with validate_standalone.py)
├── coderabbit/ (stays)
├── examples/ (stays)
├── reports/ (stays)
├── tests/ (reorganized into subdirectories)
│
└── workflows/
    ├── 1-taxonomy/
    │   ├── README.md (to be created)
    │   ├── output/
    │   │   └── taxonomy_config.json (future output)
    │   ├── src/
    │   │   └── book_taxonomy.py (from src/)
    │   └── scripts/
    │       └── generate_taxonomy_config.py (from scripts/)
    │
    ├── 2-pdf-conversion/
    │   ├── README.md (to be created)
    │   ├── input/
    │   │   └── textbooks_pdf/ (empty - PDFs to be added)
    │   ├── output/
    │   │   └── textbooks_json/ (from data/textbooks_json/ - 14 JSON files)
    │   └── scripts/
    │       └── convert_pdf_to_json.py (from src/pipeline/)
    │
    ├── 3-per-book-metadata/
    │   ├── README.md (to be created - documents that this was done in TPM)
    │   ├── output/
    │   │   └── metadata/ (from data/metadata/ - 14 JSON files)
    │   └── scripts/
    │       └── (EMPTY - per-book generators not in this repo, were in TPM)
    │
    ├── 4-metadata-merge/
    │   ├── README.md (to be created - documents that this was done in TPM)
    │   ├── output/
    │   │   └── chapter_metadata_cache.json (from data/chapter_metadata_cache.json)
    │   └── scripts/
    │       └── (EMPTY - merge script not in this repo, was in TPM)
    │
    ├── 5-metadata-enrichment/
    │   ├── README.md (to be created)
    │   ├── input/
    │   │   └── (reads from workflow 4 output: chapter_metadata_cache.json)
    │   ├── output/
    │   │   ├── chapter_metadata_cache.json (updated version)
    │   │   └── chapter_metadata_manual.json (from data/)
    │   ├── scripts/
    │   │   └── generate_chapter_metadata.py (from src/pipeline/)
    │   └── src/
    │       └── chapter_metadata_manager.py (from src/)
    │
    ├── 6-base-guidelines/
    │   ├── README.md (to be created)
    │   ├── input/
    │   │   └── (reads from workflow 4/5 output: chapter_metadata_cache.json)
    │   ├── output/
    │   │   ├── chapter_summaries/ (from data/chapter_summaries/ - 14 MD files)
    │   │   └── metadata/ (from data/metadata/ - 14 JSON files - IF different from workflow 3)
    │   ├── scripts/
    │   │   └── chapter_generator_all_text.py (from src/pipeline/)
    │   └── src/
    │       └── metadata_builder.py (from src/builders/)
    │
    ├── 7-llm-enhancement/
    │   ├── README.md (to be created)
    │   ├── input/
    │   │   └── (reads from workflow 6 output: base guideline MD files)
    │   ├── output/
    │   │   └── enhanced_guidelines/ (for LLM-enhanced MD files)
    │   ├── scripts/
    │   │   ├── integrate_llm_enhancements.py (from src/)
    │   │   └── compliance_validator_v3.py (from src/pipeline/)
    │   └── src/
    │       ├── interactive_llm_system_v3_hybrid_prompt.py (from src/)
    │       ├── metadata_extraction_system.py (from src/)
    │       ├── models/ (from src/models/ - 2 files)
    │       └── phases/ (from src/phases/ - 5 files, content_selection_impl.py etc.)
    │
    └── 8-pipeline/
        ├── README.md (to be created)
        ├── output/ (empty - for future logs/reports/caches)
        ├── src/
        │   ├── cache.py (from src/)
        │   ├── retry.py (from src/)
        │   ├── constants.py (from src/)
        │   ├── json_parser.py (from src/)
        │   ├── llm_integration.py (from src/)
        │   ├── pipeline_orchestrator.py (from src/pipeline/orchestrator.py)
        │   ├── loaders/ (from src/loaders/ - 2 files)
        │   ├── adapters/ (from src/pipeline/adapters/ - 4 files)
        │   └── providers/ (from src/providers/ - 4 files)
        └── prompts/ (from src/prompts/ - 7 files)
```

---

## Data Flow Visualization

```
PDFs (workflows/2-pdf-conversion/input/textbooks_pdf/)
  ↓ [convert_pdf_to_json.py]
JSON Textbooks (workflows/2-pdf-conversion/output/textbooks_json/)
  ↓ [PER-BOOK METADATA EXTRACTION - Done in TPM, not in this repo]
  ↓ [generate_fluent_python_metadata.py, generate_learning_python_metadata.py, etc. - 19 scripts]
Individual Book Metadata (workflows/3-per-book-metadata/output/metadata/*.json - 14 files)
  ↓ [MERGE METADATA - Done in TPM, not in this repo]
  ↓ [merge_metadata_to_cache.py]
Central Metadata Cache (workflows/4-metadata-merge/output/chapter_metadata_cache.json)
  ↓ [OPTIONAL: generate_chapter_metadata.py - enriches/updates cache from JSON]
Enriched Metadata Cache (workflows/5-metadata-enrichment/output/chapter_metadata_cache.json)
  ↓ [chapter_generator_all_text.py - reads cache + JSON, generates base guidelines]
Base Guidelines (workflows/6-base-guidelines/output/chapter_summaries/*.md - 14 files)
  ↓ [integrate_llm_enhancements.py + interactive_llm_system_v3_hybrid_prompt.py]
  ↓ [Two-phase LLM: metadata analysis → targeted content → scholarly annotation]
Enhanced Guidelines (workflows/7-llm-enhancement/output/enhanced_guidelines/*.md)
  ↑
Pipeline Infrastructure (workflows/8-pipeline/) orchestrates all stages
  - Retry logic, caching, provider abstraction
  - Error handling, logging
  - Adapters for legacy code integration
```

**Data Dependencies:**
- Workflow 2 → Workflow 3 (JSON files → per-book metadata extraction)
- Workflow 3 → Workflow 4 (individual metadata JSONs → merge)
- Workflow 4 → Workflow 5 (cache → enrichment)
- Workflow 5 + Workflow 2 → Workflow 6 (cache + JSON → base guidelines)
- Workflow 6 → Workflow 7 (base guidelines → LLM enhancement)
- Workflow 8 provides infrastructure to workflows 5, 6, 7

**Already Completed in This Repo:**
✅ Workflow 2: 14 JSON files in `data/textbooks_json/`
✅ Workflow 3: 14 metadata files in `data/metadata/`
✅ Workflow 4: `data/chapter_metadata_cache.json` (215 KB)
✅ Workflow 6: 14 chapter summary files in `data/chapter_summaries/`

**Active Workflows in This Repo:**
- Workflow 5: Metadata enrichment via `generate_chapter_metadata.py`
- Workflow 6: Base guideline generation via `chapter_generator_all_text.py`
- Workflow 7: LLM enhancement via `integrate_llm_enhancements.py`
- Workflow 8: Infrastructure support

---

## Migration Strategy

### Phase 1: Create Structure
- Create all workflow directories
- Add README.md for each workflow
- Create input/output subdirectories

### Phase 2: Move Files
- Move source code to appropriate workflow src/ directories
- Move tests to workflow-specific test directories
- Update import statements

### Phase 3: Update Configuration
- Update scripts to reference correct input/output paths
- Scripts read from other workflow output directories directly
- No symlinks - use path configuration instead

### Phase 4: Validation
- Run all tests to ensure nothing broke
- Verify imports work correctly
- Update documentation

---

## File Migration Mapping

### ✅ Root Level (Universal Documents Only)

**These files stay at root:**
- `README.md` - Project overview
- `LICENSE` - License information  
- `.gitignore` - Git ignore rules
- `pytest.ini` - Universal test configuration
- `Makefile` - Build automation

**Root directories that stay:**
- `config/` - Cross-workflow configuration (settings.py, requirements.txt, pyproject.toml)
- `docs/` - Project-level documentation (NOT generated outputs)
- `coderabbit/` - Code quality tools
- `examples/` - Example code and demos
- `reports/` - Tool-generated quality reports (NOT workflow outputs)
- `scripts/` - Cross-workflow validation utilities (validate_standalone.py)
- `tests/` - Centralized test suite (organized by workflow in subdirectories)

**Root directories that will be EMPTY after migration:**
- ❌ `src/` - ALL code moves to workflow-specific src/ directories
- ❌ `data/` - All data moves to workflow input/output directories
- ❌ `guidelines/` - Generated guidelines move to workflow 6 output (if exists)

---

### 📦 Current src/ Files → Destination Mapping

#### From `src/` (root) to Workflows:

**Workflow 1 (Taxonomy):**
- `src/book_taxonomy.py` → `workflows/1-taxonomy/src/book_taxonomy.py`

**Workflow 2 (PDF Conversion):**
- `src/pipeline/convert_pdf_to_json.py` → `workflows/2-pdf-conversion/scripts/convert_pdf_to_json.py`

**Workflow 3 (Chapter Extraction):**
- (No existing file - may need to extract from chapter_metadata_manager.py or create new script)
- Output: `workflows/3-chapter-extraction/output/chapter_structure_cache.json`

**Workflow 4 (Metadata Cache Creation):**
- `src/pipeline/generate_chapter_metadata.py` → `workflows/4-metadata-cache/scripts/generate_chapter_metadata.py`
- `data/chapter_metadata_cache.json` → `workflows/4-metadata-cache/output/chapter_metadata_cache.json`
- `data/chapter_metadata_manual.json` → `workflows/4-metadata-cache/output/chapter_metadata_manual.json`

**Workflow 5 (Guideline Generation):**
- `src/pipeline/chapter_generator_all_text.py` → `workflows/5-guideline-generation/scripts/chapter_generator_all_text.py`
- `src/builders/metadata_builder.py` → `workflows/5-guideline-generation/src/metadata_builder.py`
- `data/chapter_summaries/*.md` (14 files) → `workflows/5-guideline-generation/output/chapter_summaries/`
- `data/metadata/*.json` (14 files) → `workflows/5-guideline-generation/output/metadata/`

**Workflow 6 (Pipeline Orchestration):**
- `src/cache.py` → `workflows/7-pipeline/src/cache.py`
- `src/retry.py` → `workflows/7-pipeline/src/retry.py`
- `src/constants.py` → `workflows/7-pipeline/src/constants.py`
- `src/json_parser.py` → `workflows/7-pipeline/src/json_parser.py`
- `src/llm_integration.py` → `workflows/7-pipeline/src/llm_integration.py`
- `src/interactive_llm_system_v3_hybrid_prompt.py` → `workflows/7-pipeline/src/interactive_llm_system_v3_hybrid_prompt.py`
- `src/integrate_llm_enhancements.py` → `workflows/7-pipeline/src/integrate_llm_enhancements.py`
- `src/chapter_metadata_manager.py` → `workflows/7-pipeline/src/chapter_metadata_manager.py`
- `src/metadata_extraction_system.py` → `workflows/7-pipeline/src/metadata_extraction_system.py`
- `src/loaders/__init__.py` → `workflows/7-pipeline/src/loaders/__init__.py`
- `src/loaders/content_loaders.py` → `workflows/7-pipeline/src/loaders/content_loaders.py`
- `src/models/__init__.py` → `workflows/7-pipeline/src/models/__init__.py`
- `src/models/analysis_models.py` → `workflows/7-pipeline/src/models/analysis_models.py`
- `src/phases/__init__.py` → `workflows/7-pipeline/src/phases/__init__.py`
- `src/phases/annotation_service.py` → `workflows/7-pipeline/src/phases/annotation_service.py`
- `src/phases/content_selection.py` → `workflows/7-pipeline/src/phases/content_selection.py`
- `src/phases/content_selection_impl.py` → `workflows/7-pipeline/src/phases/content_selection_impl.py`
- `src/phases/orchestrator.py` → `workflows/7-pipeline/src/phases/orchestrator.py`
- `src/pipeline/orchestrator.py` → `workflows/7-pipeline/src/pipeline_orchestrator.py`
- `src/pipeline/adapters/__init__.py` → `workflows/7-pipeline/src/adapters/__init__.py`
- `src/pipeline/adapters/chapter_generator.py` → `workflows/7-pipeline/src/adapters/chapter_generator.py`
- `src/pipeline/adapters/metadata_extractor.py` → `workflows/7-pipeline/src/adapters/metadata_extractor.py`
- `src/pipeline/adapters/pdf_converter.py` → `workflows/7-pipeline/src/adapters/pdf_converter.py`
- `src/providers/__init__.py` → `workflows/7-pipeline/src/providers/__init__.py`
- `src/providers/anthropic_provider.py` → `workflows/7-pipeline/src/providers/anthropic_provider.py`
- `src/providers/base.py` → `workflows/7-pipeline/src/providers/base.py`
- `src/providers/factory.py` → `workflows/7-pipeline/src/providers/factory.py`
- `src/prompts/__init__.py` → `workflows/7-pipeline/prompts/__init__.py`
- `src/prompts/comprehensive_phase1.txt` → `workflows/7-pipeline/prompts/comprehensive_phase1.txt`
- `src/prompts/comprehensive_phase2.txt` → `workflows/7-pipeline/prompts/comprehensive_phase2.txt`
- `src/prompts/phase1.txt` → `workflows/7-pipeline/prompts/phase1.txt`
- `src/prompts/phase2.txt` → `workflows/7-pipeline/prompts/phase2.txt`
- `src/prompts/templates.py` → `workflows/7-pipeline/prompts/templates.py`
- `src/prompts/test_template.txt` → `workflows/7-pipeline/prompts/test_template.txt`

**Files to DELETE (module initializers for empty directories):**
- `src/__init__.py`
- `src/builders/__init__.py`
- `src/pipeline/__init__.py`

---

### 📋 Current scripts/ Files → Destination Mapping

**Workflow 1 (Taxonomy):**
- `scripts/generate_taxonomy_config.py` → `workflows/1-taxonomy/scripts/generate_taxonomy_config.py`

**STAYS AT ROOT (cross-workflow utility):**
- `scripts/validate_standalone.py` → STAYS at `scripts/validate_standalone.py`

**Files to DELETE (duplicates or no longer needed):**
- `scripts/__init__.py` - DELETE (scripts/ doesn't need to be a module)
- `scripts/coderabbit_audit_generator.py` - DELETE (duplicate of coderabbit/scripts/coderabbit_audit_generator.py)

---

### 📁 Current data/ Files → Destination Mapping

**Workflow 2 (PDF Conversion) - Output:**
- `data/textbooks_json/*.json` (14 files) → `workflows/2-pdf-conversion/output/textbooks_json/`

**Workflow 3 (Chapter Extraction) - Output:**
- (Chapter structure cache - may need to be created or extracted from existing data)

**Workflow 4 (Metadata Cache Creation) - Output:**
- `data/chapter_metadata_cache.json` → `workflows/4-metadata-cache/output/chapter_metadata_cache.json`
- `data/chapter_metadata_manual.json` → `workflows/4-metadata-cache/output/chapter_metadata_manual.json`

**Workflow 5 (Guideline Generation) - Output:**
- `data/chapter_summaries/*.md` (14 files) → `workflows/5-guideline-generation/output/chapter_summaries/`
- `data/metadata/*.json` (14 files) → `workflows/5-guideline-generation/output/metadata/`

**Note:** Total 44 files in data/ directory all accounted for above.

---

### 📋 Current tests/ Files → Destination Mapping

**ALL tests STAY in centralized `tests/` directory, organized by type and workflow:**

**Unit Tests (by workflow):**

*Workflow 1 (Taxonomy):*
- `tests/test_book_taxonomy.py` → `tests/unit/1-taxonomy/test_book_taxonomy.py`
- `tests/test_taxonomy_prefiltering.py` → `tests/unit/1-taxonomy/test_taxonomy_prefiltering.py`

*Workflow 3 (Chapter Extraction):*
- (No tests yet - workflow may need implementation)

*Workflow 4 (Metadata Cache Creation):*
- (No specific tests yet - covered by integration tests)

*Workflow 5 (Guideline Generation):*
- `tests/test_chapter_generator.py` → `tests/unit/5-guideline-generation/test_chapter_generator.py`
- `tests/test_chapter_generator_refactoring.py` → `tests/unit/5-guideline-generation/test_chapter_generator_refactoring.py`
- `tests/test_chapter1_comparison.py` → `tests/unit/5-guideline-generation/test_chapter1_comparison.py`
- `tests/test_sprint3_metadata_builders.py` → `tests/unit/5-guideline-generation/test_sprint3_metadata_builders.py`

*Workflow 6 (Pipeline):*
- `tests/test_cache.py` → `tests/unit/7-pipeline/test_cache.py`
- `tests/test_retry.py` → `tests/unit/7-pipeline/test_retry.py`
- `tests/test_providers.py` → `tests/unit/7-pipeline/test_providers.py`
- `tests/test_llm_integration.py` → `tests/unit/7-pipeline/test_llm_integration.py`
- `tests/test_json_parser.py` → `tests/unit/7-pipeline/test_json_parser.py`
- `tests/test_config.py` → `tests/unit/7-pipeline/test_config.py`
- `tests/test_template_loader.py` → `tests/unit/7-pipeline/test_template_loader.py`
- `tests/test_sprint3_constants.py` → `tests/unit/7-pipeline/test_sprint3_constants.py`
- `tests/test_sprint4_day2_pathconfig.py` → `tests/unit/7-pipeline/test_sprint4_day2_pathconfig.py`
- `tests/test_sprint4_day3_provider.py` → `tests/unit/7-pipeline/test_sprint4_day3_provider.py`
- `tests/test_sprint4_day4_cache_retry.py` → `tests/unit/7-pipeline/test_sprint4_day4_cache_retry.py`
- `tests/test_phase1_extraction.py` → `tests/unit/7-pipeline/test_phase1_extraction.py`
- `tests/test_phase2_extraction.py` → `tests/unit/7-pipeline/test_phase2_extraction.py`
- `tests/test_comprehensive_phase1_extraction.py` → `tests/unit/7-pipeline/test_comprehensive_phase1_extraction.py`
- `tests/test_comprehensive_phase2_extraction.py` → `tests/unit/7-pipeline/test_comprehensive_phase2_extraction.py`
- `tests/test_content_loaders_extraction.py` → `tests/unit/7-pipeline/test_content_loaders_extraction.py`
- `tests/test_models_extraction.py` → `tests/unit/7-pipeline/test_models_extraction.py`
- `tests/test_pipeline_stages.py` → `tests/unit/7-pipeline/test_pipeline_stages.py`
- `tests_unit/test_pipeline_adapters.py` → `tests/unit/7-pipeline/test_pipeline_adapters.py`
- `tests_unit/test_pipeline_orchestrator.py` → `tests/unit/7-pipeline/test_pipeline_orchestrator.py`

**Integration Tests:**
- `tests/test_pipeline_integration.py` → `tests/integration/test_pipeline_integration.py`
- `tests/test_sprint1_integration.py` → `tests/integration/test_sprint1_integration.py`
- `tests/test_sprint1_validation.py` → `tests/integration/test_sprint1_validation.py`

**Test Fixtures (shared data):**
- `tests/.gitkeep` → `tests/fixtures/.gitkeep`
- `tests/baseline_chapter1_new.txt` → `tests/fixtures/baseline_chapter1_new.txt`
- `tests/baseline_chapter1.txt` → `tests/fixtures/baseline_chapter1.txt`
- `tests/baseline_sprint1.txt` → `tests/fixtures/baseline_sprint1.txt`
- `tests/conftest.py` → `tests/fixtures/conftest.py`

**Note:** Total 29 test files (27 in tests/ + 2 in tests_unit/) all mapped above.

---

### 📄 Other Files

**STAYS AT ROOT:**
- `.coderabbit.yaml` - CodeRabbit configuration
- `.env.example` - Environment variable template
- `.gitignore` - Git ignore rules
- `Makefile.coderabbit` - CodeRabbit build automation
- `QUALITY_ASSESSMENT_REPORT.md` - Project quality assessment
- `README.md` - Project overview
- `REFACTORING_PLAN.md` - Refactoring documentation
- `requirements.txt` - Move to `config/requirements.txt`
- `sonar-project.properties` - SonarQube configuration
- `TECHNICAL_ASSESSMENT.md` - Technical assessment
- `WORKFLOW_REORGANIZATION.md` - This document (temporary, can move to docs/ or delete after migration)

**STAYS in config/:**
- `config/__init__.py` - Config module initializer
- `config/settings.py` - Application settings

**STAYS in docs/:**
- All 14 docs files (analysis/, *.md files) - Project documentation

**STAYS in examples/:**
- `examples/config_usage.py` - Configuration usage example

**STAYS in reports/:**
- `reports/coderabbit/analysis_report.md` - CodeRabbit analysis report
- `reports/coderabbit/analysis_results.json` - CodeRabbit results
- `reports/ruff_report.json` - Ruff linting report

**STAYS in coderabbit/:**
- All 11 coderabbit files - Code quality tool files

---

### 📊 Migration Summary

**Total Files Reviewed:** 165

**Distribution:**
- **Stays at Root:** 42 files (config/, docs/, examples/, reports/, coderabbit/, root-level configs)
- **Moves to Workflow 1:** 2 files (src + script)
- **Moves to Workflow 2:** 15 files (1 script + 14 JSON outputs)
- **Moves to Workflow 3:** TBD (needs identification of chapter extraction code)
- **Moves to Workflow 4:** 3 files (1 script + 2 data cache files)
- **Moves to Workflow 5:** 31 files (1 script + 1 src + 14 chapter summaries + 14 metadata + 1 builder)
- **Moves to Workflow 6:** 37 files (src/, phases/, pipeline/, providers/, prompts/, loaders/, models/, adapters/)
- **Tests (reorganized):** 29 files (stay in tests/, organized by workflow)
- **Files to DELETE:** 5 files (__init__.py files, duplicate script)

---

### 📁 Data Files → Destination Mapping

**Current `data/` directory:**
- `data/textbooks_json/` → `workflows/2-pdf-conversion/output/textbooks_json/`
- `data/metadata/` → `workflows/4-metadata-extraction/output/metadata/`
- `data/chapter_summaries/` → `workflows/3-chapter-definition/output/chapter_summaries/`
- `data/chapter_metadata_cache.json` → `workflows/3-chapter-definition/data/chapter_metadata_cache.json`
- `data/chapter_metadata_manual.json` → `workflows/3-chapter-definition/data/chapter_metadata_manual.json`

**Input data (PDFs) - TO BE ADDED:**
- PDF files (currently not in repo) → `workflows/2-pdf-conversion/input/textbooks_pdf/`

---

### 🔗 Import Statement Updates Required

After migration, ALL imports must be updated:

**Before:**
```python
from src.providers import create_llm_provider
from src.cache import ChapterCache
from src.retry import call_llm_with_retry
```

**After (from within workflow 3):**
```python
from workflows.7-pipeline.src.providers import create_llm_provider
from workflows.7-pipeline.src.cache import ChapterCache
from workflows.7-pipeline.src.retry import call_llm_with_retry
```

**OR** use relative imports within workflows:
```python
from ...7-pipeline.src.providers import create_llm_provider
```

**OR** add workflows/ to PYTHONPATH and use:
```python
from 7-pipeline.src.providers import create_llm_provider
```

---

## Business Process Mapping

### Scripts That Read/Write JSON/MD Files (16 total)

**WORKFLOW 1: Taxonomy & Project Setup**
- `scripts/generate_taxonomy_config.py` - Generates taxonomy configuration
- `src/book_taxonomy.py` - Taxonomy definitions and 3-tier cascading book selection

**WORKFLOW 2: PDF → JSON Conversion**
- `src/pipeline/convert_pdf_to_json.py` - Main conversion script (PDF → JSON)
- `src/pipeline/adapters/pdf_converter.py` - Adapter wrapper for pipeline integration

**WORKFLOW 3: Per-Book Metadata Extraction**
- ⚠️ **NOT IN THIS REPO** - Per-book metadata generators (e.g., `generate_fluent_python_metadata.py`) were in TPM project
- Output files ARE present: `data/metadata/*.json` (14 files)
- These scripts extract chapter structure, keywords, concepts, summaries from each book's JSON

**WORKFLOW 4: Metadata Cache Merging**
- ⚠️ **NOT IN THIS REPO** - `merge_metadata_to_cache.py` was in TPM project
- Output file IS present: `data/chapter_metadata_cache.json` (215 KB, merged from 14 metadata files)

**WORKFLOW 5: Metadata Cache Enrichment**
- `src/pipeline/generate_chapter_metadata.py` - Reads cache + JSON, extracts/updates keywords, concepts, summaries
- `src/chapter_metadata_manager.py` - Manages chapter metadata, provides API to read cache

**WORKFLOW 6: Base Guideline Generation**
- `src/pipeline/chapter_generator_all_text.py` - Main guideline generator (reads cache + JSON, writes base MD)
- `src/builders/metadata_builder.py` - Builds metadata packages for guideline generation

**WORKFLOW 7: LLM Enhancement**
- `src/integrate_llm_enhancements.py` - Main orchestration script (reads base guidelines, writes enhanced MD)
- `src/interactive_llm_system_v3_hybrid_prompt.py` - Interactive two-phase LLM analysis system
- `src/metadata_extraction_system.py` - Extracts page content from JSON for LLM analysis
- `src/models/analysis_models.py` - Data models for LLM analysis workflow
- `src/phases/content_selection_impl.py` - Content selection logic for targeted LLM analysis
- `src/pipeline/compliance_validator_v3.py` - Validates generated guidelines (Chicago citations, annotations, cross-references)

**WORKFLOW 8: Pipeline Orchestration & Infrastructure**
- `src/cache.py` - Caching infrastructure for LLM responses
- `src/llm_integration.py` - LLM API integration and logging
- `src/json_parser.py` - JSON parsing utilities
- `src/loaders/content_loaders.py` - Loads book content from JSON files
- `src/prompts/templates.py` - Prompt template management
- `src/pipeline/adapters/*.py` - Pipeline adapters (4 files)
- `src/providers/*.py` - LLM provider abstraction (4 files)
- `src/phases/*.py` - Phase orchestration (5 files)

### Summary

**All 8 Workflows:** 16+ scripts clearly mapped (plus infrastructure)
1. Taxonomy: 2 files
2. PDF→JSON: 2 scripts  
3. Per-Book Metadata: 0 scripts (already run in TPM, 14 output files present)
4. Metadata Merging: 0 scripts (already run in TPM, 1 output file present)
5. Cache Enrichment: 2 scripts
6. Base Guidelines: 2 scripts
7. LLM Enhancement: 5 scripts
8. Infrastructure: 20+ files (adapters, providers, phases, utilities)

**Data Flow:**
```
PDF → JSON → [Per-Book Metadata Extraction] → Individual Metadata JSONs → 
[Merge] → chapter_metadata_cache.json → [Enrichment] → Updated Cache →
Base Guidelines → LLM-Enhanced Guidelines
```

**Critical Files Present:**
✅ `data/metadata/*.json` (14 files) - Individual book metadata
✅ `data/chapter_metadata_cache.json` - Central merged cache
✅ `src/pipeline/generate_chapter_metadata.py` - Cache enrichment
✅ `src/pipeline/chapter_generator_all_text.py` - Base guideline generator
✅ `src/integrate_llm_enhancements.py` - LLM enhancement orchestrator
✅ `src/interactive_llm_system_v3_hybrid_prompt.py` - Two-phase LLM system

**Scripts NOT in This Repo (Were in TPM):**
❌ Per-book metadata generators (19 scripts like `generate_fluent_python_metadata.py`)
❌ `merge_metadata_to_cache.py` - Metadata merger

---

## Validation Report

All required files for active workflows are present:

**✅ Workflow 2 (PDF → JSON):**
- 14 JSON files in `data/textbooks_json/`
- `src/pipeline/convert_pdf_to_json.py`

**✅ Workflow 3 (Per-Book Metadata) - Already Complete:**
- 14 metadata JSON files in `data/metadata/`

**✅ Workflow 4 (Metadata Merge) - Already Complete:**
- `data/chapter_metadata_cache.json` (210 KB)

**✅ Workflow 5 (Metadata Enrichment):**
- `src/pipeline/generate_chapter_metadata.py`
- `src/chapter_metadata_manager.py`
- `data/chapter_metadata_manual.json`

**✅ Workflow 6 (Base Guidelines):**
- `src/pipeline/chapter_generator_all_text.py`
- `src/builders/metadata_builder.py`
- 14 chapter summary MD files in `data/chapter_summaries/`

**✅ Workflow 7 (LLM Enhancement):**
- `src/integrate_llm_enhancements.py`
- `src/interactive_llm_system_v3_hybrid_prompt.py`
- `src/metadata_extraction_system.py`
- `src/models/analysis_models.py`
- `src/phases/content_selection_impl.py`
- `src/pipeline/compliance_validator_v3.py`

**✅ Workflow 8 (Infrastructure):**
- `src/cache.py`, `src/retry.py`, `src/llm_integration.py`, `src/json_parser.py`
- `src/loaders/content_loaders.py`, `src/prompts/templates.py`
- 4 pipeline adapters in `src/pipeline/adapters/`
- 4 providers in `src/providers/`

**✅ Taxonomy:**
- `src/book_taxonomy.py`
- `scripts/generate_taxonomy_config.py`

**Summary:** All active workflow files present. Workflows 3-4 (per-book metadata generation and merging) were completed in the TPM project, and their outputs are included in this repo.

---

## Open Questions

1. **Taxonomy Script Execution**
   - When does `generate_taxonomy_config.py` run?
   - Manual vs automated?
   - Part of CI/CD?

2. **Import Path Strategy**
   - Use absolute imports with `workflows.X-name.src.module`?
   - Use relative imports `...X-name.src.module`?
   - Add `workflows/` to PYTHONPATH?

3. **Shared Code Across Workflows**
   - cache.py, retry.py, providers/ are used by workflows 3, 4, 7
   - Should these stay in workflow 7 and be imported by others?
   - Or create a shared utilities workflow?

4. **Testing Strategy**
   - How to run all tests at once after distributing to workflows?
   - pytest.ini at root with paths to all workflow test directories?
   - Makefile targets for running all tests?

---

## Next Steps

1. ✅ Document workflow stages
2. ✅ Create directory structure proposal
3. ⏳ Review and refine structure with user
4. ⏳ Create implementation plan
5. ⏳ Execute migration
6. ⏳ Validate and test
