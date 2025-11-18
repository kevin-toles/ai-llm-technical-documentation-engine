# Deprecated Files - Hardcoded Taxonomy System

**Date Deprecated:** November 18, 2025  
**Reason:** Replaced by data-driven concept taxonomy system

---

## What Was Deprecated

### book_taxonomy.py.deprecated (506 lines)
**Original Purpose:** Hardcoded Python book taxonomy with manual tier classifications

**Why Deprecated:**
- Manual maintenance burden (required code changes for new books)
- Not used by UI workflows (Tab 5 uses generate_concept_taxonomy.py instead)
- Replaced by data-driven concept extraction from book content + metadata

**What Replaced It:**
- `workflows/taxonomy_setup/scripts/generate_concept_taxonomy.py` - Extracts concepts from JSON textbooks
- `workflows/taxonomy_setup/output/python_taxonomy.json` - Generated taxonomy with concepts arrays
- UI Tab 5: Dynamic concept taxonomy generation from book metadata

---

## Migration Path

### Old System (Hardcoded)
```python
from workflows.taxonomy_setup.scripts.book_taxonomy import (
    score_books_for_concepts,
    get_recommended_books,
    BOOK_REGISTRY,
    ALL_BOOKS
)

# Hardcoded scoring
scored_books = score_books_for_concepts(["async", "coroutine"])
```

### New System (Data-Driven)
```python
import json
from pathlib import Path

# Load generated taxonomy
taxonomy_path = Path("workflows/taxonomy_setup/output/python_taxonomy.json")
with open(taxonomy_path) as f:
    taxonomy = json.load(f)

# Extract concepts from all tiers
concepts = []
for tier_name, tier_data in taxonomy["tiers"].items():
    if "concepts" in tier_data:
        concepts.extend(tier_data["concepts"])

# Use concepts for analysis (no hardcoded scoring needed)
```

---

## Removal Checklist

✅ **Phase 1:** Move book_taxonomy.py to Deprecated/ (COMPLETE)  
⏳ **Phase 2:** Remove dead code from active files  
⏳ **Phase 3:** Delete supporting files (generate_taxonomy_config.py)  
⏳ **Phase 4:** Update tests  
⏳ **Phase 5:** Remove TaxonomyConfig from settings.py  
⏳ **Phase 6:** Documentation cleanup  
⏳ **Phase 7:** Validation testing  
⏳ **Phase 8:** Git commit  

---

## Rollback (If Needed)

```bash
# Restore book_taxonomy.py
cp /Users/kevintoles/POC/llm-document-enhancer/workflows/taxonomy_setup/Deprecated/book_taxonomy.py.deprecated \
   /Users/kevintoles/POC/llm-document-enhancer/workflows/taxonomy_setup/scripts/book_taxonomy.py
```

---

## References

- **HARDCODED_TAXONOMY_REMOVAL_PLAN.md** - 8-phase removal strategy
- **BOOK_TAXONOMY_MATRIX.md** - Documents old system structure
- **REFACTORING_PLAN.md** - Sprint 1-3 improvements (TDD approach)
- **ARCHITECTURE_GUIDELINES** - Repository pattern, Service Layer preserved
