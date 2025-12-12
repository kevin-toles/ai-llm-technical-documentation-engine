# Documentation Index

## 📁 Directory Structure

```
docs/
├── reference/          # Evergreen architecture & design docs
├── operations/         # Runbooks & troubleshooting guides
├── testing/            # Test plans & methodologies
├── archive/            # Completed implementation docs
│   ├── *.md            # Completed implementation plans
│   └── sprints/        # Sprint-specific analysis docs
├── TECHNICAL_CHANGE_LOG.md
└── README.md           # This file
```

> **Note**: Pending work items are centralized in `textbooks/pending/` by service.

---

## 📚 Reference Documentation

Evergreen architecture and design documents.

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](reference/ARCHITECTURE.md) | System architecture overview |
| [BOOK_TAXONOMY_MATRIX.md](reference/BOOK_TAXONOMY_MATRIX.md) | Textbook tier relationships & cross-referencing |
| [CODING_PATTERNS_ANALYSIS.md](reference/CODING_PATTERNS_ANALYSIS.md) | Code patterns used across the codebase |
| [METADATA_FLOW_EXPLAINED.md](reference/METADATA_FLOW_EXPLAINED.md) | How metadata flows through the pipeline |
| [TIER_RELATIONSHIP_DIAGRAM.md](reference/TIER_RELATIONSHIP_DIAGRAM.md) | Visual tier relationships |
| [UI_SPECIFICATION.md](reference/UI_SPECIFICATION.md) | Desktop UI specifications |
| [WORKFLOW_DATA_FLOW.md](reference/WORKFLOW_DATA_FLOW.md) | Data flow through workflow tabs |
| [WORKFLOW_DECISION_FRAMEWORK.md](reference/WORKFLOW_DECISION_FRAMEWORK.md) | Decision logic for workflow processing |
| [WORKFLOW_OUTPUT_ANALYSIS.md](reference/WORKFLOW_OUTPUT_ANALYSIS.md) | Analysis of workflow outputs |

---

## 🔧 Operations

How to run, debug, and troubleshoot.

| Document | Description |
|----------|-------------|
| [RUNBOOK.md](operations/RUNBOOK.md) | Operational procedures |
| [TROUBLESHOOTING.md](operations/TROUBLESHOOTING.md) | Common issues & solutions |

---

## 🧪 Testing

Test plans and methodologies.

| Document | Description |
|----------|-------------|
| [KEYWORD_EXTRACTION_TEST_PLAN.md](testing/KEYWORD_EXTRACTION_TEST_PLAN.md) | Keyword extraction evaluation methodology |
| [KEYWORD_EXTRACTION_TEST_PLAN_ADDENDUM.md](testing/KEYWORD_EXTRACTION_TEST_PLAN_ADDENDUM.md) | Addendum to keyword test plan |
| [WORKFLOW_TEST_PLAN.md](testing/WORKFLOW_TEST_PLAN.md) | Workflow integration test plan |

---

## 🚧 Pending Work

> **Note**: All pending work documents have been centralized in the `textbooks/pending/` folder, organized by service.
> 
> See: [textbooks/pending/llm-document-enhancer/](../../textbooks/pending/llm-document-enhancer/)

---

## 📦 Archive

Completed implementation documentation retained for historical reference.

### Implementation Plans (Complete)
| Document | Completion Date |
|----------|-----------------|
| [MASTER_IMPLEMENTATION_GUIDE.md](archive/MASTER_IMPLEMENTATION_GUIDE.md) | December 2025 |
| [CONFIG_IMPLEMENTATION.md](archive/CONFIG_IMPLEMENTATION.md) | November 2025 |
| [DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md](archive/DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md) | December 2025 |

### Sprint Analysis (Historical)
Located in `archive/sprints/` - sprint-specific analysis documents from development:
- ANTI_PATTERN_ANALYSIS.md
- BERTOPIC_SENTENCE_TRANSFORMERS_DESIGN.md
- chapter_segmenter_conflict_assessment.md
- coderabbit_fixes_sprint_summary.md
- coderabbit_pr1_analysis_summary.md
- domain-agnostic-metadata-document-analysis.md
- sonarqube_issues_tdd_analysis.md

---

## 📝 Changelog

| Document | Description |
|----------|-------------|
| [TECHNICAL_CHANGE_LOG.md](TECHNICAL_CHANGE_LOG.md) | Technical changes & decisions |

---

*Last Updated: December 2025*
