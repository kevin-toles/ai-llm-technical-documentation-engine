# Tab 4: Statistical Enrichment - Implementation Plan

**Date**: November 19, 2025  
**Priority**: HIGH  
**Estimated Time**: 10-12 hours  
**Status**: ⚠️ PARTIALLY IMPLEMENTED (40%)

---

## Current State Analysis

### ✅ What EXISTS (Tab 2 Output)

**Directory**: `workflows/metadata_extraction/output/`

**Files Found**: 17 `*_metadata.json` files from Tab 2
- `architecture_patterns_metadata.json`
- `learning_python_metadata.json`
- `python_distilled_metadata.json`
- `fluent_python_metadata.json`
- `building_microservices_metadata.json`
- ... (12 more books)

**Tab 2 Output Structure** (per book):
```json
[
  {
    "chapter_number": 1,
    "title": "Domain Modeling",
    "start_page": 1,
    "end_page": 24,
    "summary": "Introduces domain modeling and DDD concepts...",
    "keywords": [
      "domain modeling",
      "entities",
      "value objects",
      "aggregates",
      "domain-driven design"
    ],
    "concepts": [
      "domain modeling",
      "entities",
      "value objects",
      "aggregates",
      "business logic"
    ]
  }
]
```

**Statistical Methods Used** (Tab 2):
- ✅ YAKE for keyword extraction
- ✅ Summa TextRank for concepts
- ✅ Template-based summarization

### ❌ What's MISSING (Tab 4 Requirements)

**No Enriched Metadata Files**: Zero `*_metadata_enriched.json` files exist

**Missing Functionality**:
1. Cross-book similarity analysis (scikit-learn)
2. Related chapters computation (cosine similarity)
3. Re-scored keywords with cross-book context
4. Cross-book concept extraction
5. Per-book processing script
6. Taxonomy integration

**Current Script Issues** (`generate_chapter_metadata.py`):
- ❌ Batch-only (processes all 14 hardcoded books)
- ❌ Cannot process single file from UI
- ❌ No command-line arguments
- ❌ Outputs to single `chapter_metadata_manual.json` (wrong format)
- ❌ No scikit-learn imports or usage

---

## CONSOLIDATED_IMPLEMENTATION_PLAN Requirements

### Tab 4 Specification (From Plan)

**Purpose**: Statistical cross-book analysis using scikit-learn (NO LLM)

**Input Files**:
- `{book}_metadata.json` (from Tab 2) ✅ EXISTS
- `{book}_taxonomy.json` (from Tab 3) - need to verify

**Output File**:
- `{book}_metadata_enriched.json` (50-60 KB per book)

**Processing Steps** (From Plan):

1. **Load Cross-Book Context**
   - Read taxonomy for book list
   - Load all companion book metadata files

2. **Build Chapter Corpus**
   - Combine title + summary + keywords + concepts
   - Create text representation for each chapter

3. **TF-IDF Vectorization** (scikit-learn)
   - `TfidfVectorizer` with stop words
   - Max features: 1000
   - N-grams: (1, 3)

4. **Compute Similarity Matrix**
   - `cosine_similarity()` on TF-IDF matrix
   - Find chapters with similarity > 0.7

5. **Extract Related Chapters**
   - Top 5 related chapters per chapter
   - Include relevance scores
   - Cross-book references

6. **Re-score Keywords** (YAKE with cross-book context)
   - Combine current chapter + related chapter texts
   - Re-run YAKE extraction
   - Top 10 keywords with scores

7. **Enhance Concepts** (Summa with cross-book context)
   - Extract concepts from combined text
   - Include book count for each concept

**Output Schema** (From Plan):
```json
{
  "book": "architecture_patterns",
  "enrichment_metadata": {
    "generated": "2025-11-19T...",
    "method": "statistical",
    "libraries": {
      "yake": "0.4.8",
      "summa": "1.2.0",
      "scikit-learn": "1.3.2"
    },
    "corpus_size": 12,
    "total_chapters_analyzed": 342
  },
  "chapters": [
    {
      "chapter_number": 1,
      "title": "Domain Modeling",
      "start_page": 1,
      "end_page": 24,
      
      // Original from Tab 2 (PRESERVED)
      "keywords": ["domain modeling", "entities", "value objects"],
      "concepts": ["domain modeling", "entities", "aggregates"],
      "summary": "Introduces domain modeling and DDD concepts...",
      
      // NEW statistical enrichment (Tab 4)
      "related_chapters": [
        {
          "book": "learning_python",
          "chapter": 2,
          "title": "How Python Runs Programs",
          "relevance_score": 0.85,
          "shared_concepts": ["installation", "setup"],
          "method": "cosine_similarity"
        },
        {
          "book": "python_architecture_patterns",
          "chapter": 1,
          "title": "Clean Architecture",
          "relevance_score": 0.92,
          "shared_concepts": ["domain modeling", "DDD", "patterns"],
          "method": "cosine_similarity"
        }
      ],
      "keywords_enriched": [
        {
          "term": "domain modeling",
          "score": 0.95,
          "source": "cross_book_yake",
          "appears_in_books": 3
        },
        {
          "term": "aggregates",
          "score": 0.88,
          "source": "cross_book_yake",
          "appears_in_books": 2
        }
      ],
      "concepts_enriched": [
        {
          "concept": "domain-driven design",
          "relevance": 0.95,
          "books": 3,
          "related_concepts": ["entities", "value objects", "repositories"]
        }
      ]
    }
  ]
}
```

---

## Implementation Plan

### Phase 1: Create Per-Book Enrichment Script (4 hours)

**File**: `workflows/metadata_enrichment/scripts/enrich_metadata_per_book.py` (NEW)

#### 1.1 Script Structure
```python
#!/usr/bin/env python3
"""
Enrich Metadata Per Book - Statistical Cross-Book Analysis

Enriches single book's metadata with cross-book similarity analysis using
scikit-learn TF-IDF and cosine similarity. NO LLM calls.

Usage:
    python enrich_metadata_per_book.py \\
        --input workflows/metadata_extraction/output/architecture_patterns_metadata.json \\
        --taxonomy workflows/taxonomy_setup/output/architecture_patterns_taxonomy.json \\
        --output workflows/metadata_enrichment/output/architecture_patterns_metadata_enriched.json

Reference:
    - CONSOLIDATED_IMPLEMENTATION_PLAN.md: Tab 4 detailed implementation
    - DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md: Statistical methods only
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# scikit-learn imports
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Existing statistical extractors
from workflows.metadata_extraction.scripts.adapters.statistical_extractor import StatisticalExtractor

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from config.settings import settings

# Global extractor instance
STATISTICAL_EXTRACTOR = StatisticalExtractor()
```

#### 1.2 Core Functions

**Function 1: Load Cross-Book Context**
```python
def load_cross_book_context(taxonomy_path: Path) -> Dict[str, Any]:
    """
    Load metadata for all books listed in taxonomy.
    
    Args:
        taxonomy_path: Path to {book}_taxonomy.json
        
    Returns:
        {
            "books": [list of book names],
            "metadata": {book_name: metadata_list},
            "corpus_size": int
        }
    """
    with open(taxonomy_path) as f:
        taxonomy = json.load(f)
    
    # Extract book list from taxonomy tiers
    book_set = set()
    for tier_name, tier_data in taxonomy.get("tiers", {}).items():
        for book_file in tier_data.get("books", []):
            book_set.add(book_file)
    
    # Load metadata for each book
    metadata_dir = settings.paths.metadata_extraction_output_dir
    context = {
        "books": list(book_set),
        "metadata": {},
        "corpus_size": 0
    }
    
    for book_file in book_set:
        # Convert filename: "Architecture Patterns.json" -> "architecture_patterns_metadata.json"
        metadata_filename = Path(book_file).stem.lower().replace(" ", "_") + "_metadata.json"
        metadata_path = metadata_dir / metadata_filename
        
        if metadata_path.exists():
            with open(metadata_path) as f:
                book_metadata = json.load(f)
                context["metadata"][book_file] = book_metadata
                context["corpus_size"] += len(book_metadata)
        else:
            print(f"  ⚠️  Skipping {book_file} - metadata not found")
    
    return context
```

**Function 2: Build TF-IDF Corpus**
```python
def build_chapter_corpus(context: Dict[str, Any]) -> tuple:
    """
    Build corpus of chapter texts and index for TF-IDF.
    
    Returns:
        (corpus: List[str], index: List[dict])
        
    corpus: ["chapter text 1", "chapter text 2", ...]
    index: [{"book": "...", "chapter": 1, "title": "..."}, ...]
    """
    corpus = []
    index = []
    
    for book_name, chapters in context["metadata"].items():
        for chapter in chapters:
            # Combine all text features
            text_parts = [
                chapter.get("title", ""),
                chapter.get("summary", ""),
                " ".join(chapter.get("keywords", [])),
                " ".join(chapter.get("concepts", []))
            ]
            chapter_text = " ".join(text_parts)
            
            corpus.append(chapter_text)
            index.append({
                "book": book_name,
                "chapter": chapter.get("chapter_number"),
                "title": chapter.get("title", ""),
                "start_page": chapter.get("start_page"),
                "end_page": chapter.get("end_page")
            })
    
    return corpus, index
```

**Function 3: Compute Similarity Matrix**
```python
def compute_similarity_matrix(corpus: List[str]) -> Any:
    """
    Compute TF-IDF matrix and cosine similarity.
    
    Args:
        corpus: List of chapter texts
        
    Returns:
        similarity_matrix: numpy array of cosine similarities
    """
    # TF-IDF vectorization
    vectorizer = TfidfVectorizer(
        stop_words='english',
        max_features=1000,
        ngram_range=(1, 3),
        min_df=2,  # Ignore terms that appear in < 2 documents
        max_df=0.8  # Ignore terms that appear in > 80% of documents
    )
    
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    # Compute cosine similarity
    similarity_matrix = cosine_similarity(tfidf_matrix)
    
    return similarity_matrix
```

**Function 4: Find Related Chapters**
```python
def find_related_chapters(
    chapter_idx: int,
    similarity_matrix: Any,
    index: List[dict],
    current_book: str,
    threshold: float = 0.7,
    top_n: int = 5
) -> List[dict]:
    """
    Find top N related chapters for given chapter.
    
    Args:
        chapter_idx: Index in corpus/similarity matrix
        similarity_matrix: Precomputed cosine similarities
        index: Chapter index (book, chapter, title)
        current_book: Book name to exclude self-references
        threshold: Minimum similarity score (0.7)
        top_n: Maximum results (5)
        
    Returns:
        List of related chapters with scores
    """
    scores = similarity_matrix[chapter_idx]
    
    # Create (index, score) pairs
    scored_chapters = []
    for idx, score in enumerate(scores):
        if idx != chapter_idx and score >= threshold:
            chapter_info = index[idx]
            # Exclude chapters from same book
            if chapter_info["book"] != current_book:
                scored_chapters.append({
                    "idx": idx,
                    "score": score,
                    "book": chapter_info["book"],
                    "chapter": chapter_info["chapter"],
                    "title": chapter_info["title"]
                })
    
    # Sort by score descending
    scored_chapters.sort(key=lambda x: x["score"], reverse=True)
    
    # Return top N
    related = []
    for item in scored_chapters[:top_n]:
        related.append({
            "book": item["book"],
            "chapter": item["chapter"],
            "title": item["title"],
            "relevance_score": round(item["score"], 2),
            "method": "cosine_similarity"
        })
    
    return related
```

**Function 5: Re-score Keywords with Cross-Book Context**
```python
def rescore_keywords_cross_book(
    current_chapter_text: str,
    related_chapters_texts: List[str],
    top_n: int = 10
) -> List[dict]:
    """
    Re-score keywords using combined text from related chapters.
    
    Args:
        current_chapter_text: Text from current chapter
        related_chapters_texts: Texts from related chapters
        top_n: Number of keywords to return
        
    Returns:
        List of keyword dicts with scores
    """
    # Combine texts
    combined_text = current_chapter_text + " " + " ".join(related_chapters_texts)
    
    # Extract keywords with YAKE
    keywords_with_scores = STATISTICAL_EXTRACTOR.extract_keywords(
        combined_text, 
        top_n=top_n
    )
    
    # Format output
    keywords_enriched = []
    for keyword, score in keywords_with_scores:
        keywords_enriched.append({
            "term": keyword,
            "score": round(score, 2),
            "source": "cross_book_yake"
        })
    
    return keywords_enriched
```

**Function 6: Extract Cross-Book Concepts**
```python
def extract_concepts_cross_book(
    current_chapter_text: str,
    related_chapters_texts: List[str],
    top_n: int = 10
) -> List[dict]:
    """
    Extract concepts using combined text from related chapters.
    
    Args:
        current_chapter_text: Text from current chapter
        related_chapters_texts: Texts from related chapters
        top_n: Number of concepts to return
        
    Returns:
        List of concept dicts
    """
    # Combine texts
    combined_text = current_chapter_text + " " + " ".join(related_chapters_texts)
    
    # Extract concepts with Summa
    concepts = STATISTICAL_EXTRACTOR.extract_concepts(combined_text, top_n=top_n)
    
    # Format output
    concepts_enriched = []
    for concept in concepts:
        concepts_enriched.append({
            "concept": concept,
            "source": "cross_book_summa"
        })
    
    return concepts_enriched
```

**Function 7: Main Enrichment Function**
```python
def enrich_metadata(
    input_path: Path,
    taxonomy_path: Path,
    output_path: Path
) -> None:
    """
    Enrich metadata with cross-book statistical analysis.
    
    Args:
        input_path: Path to {book}_metadata.json (Tab 2 output)
        taxonomy_path: Path to {book}_taxonomy.json (Tab 3 output)
        output_path: Path for {book}_metadata_enriched.json (Tab 4 output)
    """
    print(f"\\n📊 Tab 4: Statistical Enrichment")
    print(f"Input: {input_path.name}")
    print(f"Taxonomy: {taxonomy_path.name}")
    
    # 1. Load current book metadata
    with open(input_path) as f:
        book_metadata = json.load(f)
    
    book_name = input_path.stem.replace("_metadata", "")
    print(f"\\nEnriching: {book_name}")
    print(f"Chapters: {len(book_metadata)}")
    
    # 2. Load cross-book context from taxonomy
    print(f"\\nLoading companion books from taxonomy...")
    context = load_cross_book_context(taxonomy_path)
    print(f"  Books found: {len(context['books'])}")
    print(f"  Total chapters: {context['corpus_size']}")
    
    # 3. Build TF-IDF corpus
    print(f"\\nBuilding TF-IDF corpus...")
    corpus, index = build_chapter_corpus(context)
    print(f"  Corpus size: {len(corpus)} chapters")
    
    # 4. Compute similarity matrix
    print(f"\\nComputing cosine similarity matrix...")
    similarity_matrix = compute_similarity_matrix(corpus)
    print(f"  Matrix shape: {similarity_matrix.shape}")
    
    # 5. Enrich each chapter
    print(f"\\nEnriching chapters with cross-book analysis...")
    enriched_chapters = []
    
    for chapter in book_metadata:
        chapter_num = chapter.get("chapter_number")
        print(f"  Chapter {chapter_num}: {chapter.get('title', 'Untitled')}")
        
        # Find chapter index in corpus
        chapter_idx = None
        for idx, item in enumerate(index):
            if (item["book"] == book_name and 
                item["chapter"] == chapter_num):
                chapter_idx = idx
                break
        
        if chapter_idx is None:
            print(f"    ⚠️  Chapter not found in corpus, skipping enrichment")
            enriched_chapters.append(chapter)
            continue
        
        # Find related chapters
        related = find_related_chapters(
            chapter_idx,
            similarity_matrix,
            index,
            book_name,
            threshold=0.7,
            top_n=5
        )
        print(f"    Related chapters found: {len(related)}")
        
        # Get related chapter texts for context
        related_texts = []
        for rel in related:
            # Find chapter text in corpus
            for idx, item in enumerate(index):
                if (item["book"] == rel["book"] and 
                    item["chapter"] == rel["chapter"]):
                    related_texts.append(corpus[idx])
                    break
        
        # Build current chapter text
        current_text = " ".join([
            chapter.get("title", ""),
            chapter.get("summary", ""),
            " ".join(chapter.get("keywords", [])),
            " ".join(chapter.get("concepts", []))
        ])
        
        # Re-score keywords with cross-book context
        keywords_enriched = rescore_keywords_cross_book(
            current_text,
            related_texts,
            top_n=10
        )
        
        # Extract cross-book concepts
        concepts_enriched = extract_concepts_cross_book(
            current_text,
            related_texts,
            top_n=10
        )
        
        # Build enriched chapter
        enriched_chapter = {
            **chapter,  # Preserve all original fields
            "related_chapters": related,
            "keywords_enriched": keywords_enriched,
            "concepts_enriched": concepts_enriched
        }
        
        enriched_chapters.append(enriched_chapter)
    
    # 6. Build enriched metadata output
    enriched_metadata = {
        "book": book_name,
        "enrichment_metadata": {
            "generated": datetime.now().isoformat(),
            "method": "statistical",
            "libraries": {
                "yake": "0.4.8",
                "summa": "1.2.0",
                "scikit-learn": "1.3.2"
            },
            "corpus_size": len(context["books"]),
            "total_chapters_analyzed": context["corpus_size"]
        },
        "chapters": enriched_chapters
    }
    
    # 7. Save enriched metadata
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(enriched_metadata, f, indent=2)
    
    # Calculate file size
    size_kb = output_path.stat().st_size / 1024
    print(f"\\n✓ Enriched metadata saved: {output_path.name}")
    print(f"  File size: {size_kb:.1f} KB")
    print(f"  Chapters enriched: {len(enriched_chapters)}")
    print(f"  Statistical method: TF-IDF + cosine similarity")
    print(f"  NO LLM calls made ✓")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Enrich metadata with cross-book statistical analysis"
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Input metadata JSON from Tab 2"
    )
    parser.add_argument(
        "--taxonomy",
        type=Path,
        required=True,
        help="Taxonomy JSON from Tab 3"
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output enriched metadata JSON"
    )
    
    args = parser.parse_args()
    
    # Validate inputs exist
    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)
    
    if not args.taxonomy.exists():
        print(f"Error: Taxonomy file not found: {args.taxonomy}")
        sys.exit(1)
    
    # Run enrichment
    enrich_metadata(args.input, args.taxonomy, args.output)
```

---

### Phase 2: Update Requirements (30 minutes)

**File**: `config/requirements.txt`

Add scikit-learn if not present:
```
scikit-learn>=1.3.2
```

Install:
```bash
pip install -r config/requirements.txt
```

---

### Phase 3: Create Test Script (1 hour)

**File**: `tests/integration/test_metadata_enrichment.py`

```python
#!/usr/bin/env python3
"""Integration tests for Tab 4 metadata enrichment."""

import json
import pytest
from pathlib import Path

def test_enrich_architecture_patterns():
    """Test enriching Architecture Patterns metadata."""
    # Paths
    input_file = Path("workflows/metadata_extraction/output/architecture_patterns_metadata.json")
    taxonomy_file = Path("workflows/taxonomy_setup/output/architecture_patterns_taxonomy.json")
    output_file = Path("workflows/metadata_enrichment/output/architecture_patterns_metadata_enriched.json")
    
    # Skip if inputs don't exist
    if not input_file.exists() or not taxonomy_file.exists():
        pytest.skip("Input files not found")
    
    # Run enrichment
    from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import enrich_metadata
    enrich_metadata(input_file, taxonomy_file, output_file)
    
    # Validate output
    assert output_file.exists()
    
    with open(output_file) as f:
        enriched = json.load(f)
    
    # Check structure
    assert "book" in enriched
    assert "enrichment_metadata" in enriched
    assert "chapters" in enriched
    
    # Check enrichment metadata
    assert enriched["enrichment_metadata"]["method"] == "statistical"
    assert "yake" in enriched["enrichment_metadata"]["libraries"]
    assert "scikit-learn" in enriched["enrichment_metadata"]["libraries"]
    
    # Check first chapter has enrichments
    chapter = enriched["chapters"][0]
    assert "related_chapters" in chapter
    assert "keywords_enriched" in chapter
    assert "concepts_enriched" in chapter
    
    # Check related chapters structure
    if chapter["related_chapters"]:
        related = chapter["related_chapters"][0]
        assert "book" in related
        assert "chapter" in related
        assert "relevance_score" in related
        assert related["method"] == "cosine_similarity"
    
    print(f"✓ Enrichment test passed")
    print(f"  Chapters enriched: {len(enriched['chapters'])}")
    print(f"  File size: {output_file.stat().st_size / 1024:.1f} KB")
```

---

### Phase 4: Update UI Integration (1 hour)

**File**: `ui/main.py`

Update Tab 4 configuration:
```python
WORKFLOWS = {
    # ... existing tabs ...
    "tab4": {
        "name": "Metadata Enrichment",
        "input_dir": WORKFLOWS_DIR / "metadata_extraction" / "output",
        "input_ext": ".json",
        "input_pattern": "*_metadata.json",  # Only metadata files, not enriched
        "output_dir": WORKFLOWS_DIR / "metadata_enrichment" / "output",
        "script": WORKFLOWS_DIR / "metadata_enrichment" / "scripts" / "enrich_metadata_per_book.py",
        "requires_taxonomy": True,  # NEW: Needs taxonomy file
        "batch_only": False,  # NOW: Supports per-file
        "additional_args": {
            "taxonomy": lambda book_name: WORKFLOWS_DIR / "taxonomy_setup" / "output" / f"{book_name}_taxonomy.json"
        }
    }
}
```

---

### Phase 5: Documentation (30 minutes)

**Update Files**:
1. `workflows/metadata_enrichment/README.md` - Document new script
2. `CONSOLIDATED_IMPLEMENTATION_PLAN.md` - Mark Tab 4 as complete
3. Add code comments and docstrings

---

## Testing Plan

### Manual Testing Steps

1. **Test Single Book Enrichment**:
```bash
python workflows/metadata_enrichment/scripts/enrich_metadata_per_book.py \\
  --input workflows/metadata_extraction/output/architecture_patterns_metadata.json \\
  --taxonomy workflows/taxonomy_setup/output/architecture_patterns_taxonomy.json \\
  --output workflows/metadata_enrichment/output/architecture_patterns_metadata_enriched.json
```

2. **Validate Output**:
```bash
# Check file created
ls -lh workflows/metadata_enrichment/output/architecture_patterns_metadata_enriched.json

# Check structure
python -c "
import json
with open('workflows/metadata_enrichment/output/architecture_patterns_metadata_enriched.json') as f:
    data = json.load(f)
    print(f'Chapters: {len(data[\"chapters\"])}')
    ch = data['chapters'][0]
    print(f'Related chapters: {len(ch.get(\"related_chapters\", []))}')
    print(f'Keywords enriched: {len(ch.get(\"keywords_enriched\", []))}')
    print(f'Concepts enriched: {len(ch.get(\"concepts_enriched\", []))}')
"
```

3. **Integration Test**:
```bash
pytest tests/integration/test_metadata_enrichment.py -v
```

4. **Test from UI**:
- Open UI: `python ui/main.py`
- Navigate to Tab 4
- Select `architecture_patterns_metadata.json`
- Click "Run Enrichment"
- Verify output appears

---

## Success Criteria

### Phase 1 Complete When:
- ✅ `enrich_metadata_per_book.py` script created
- ✅ Accepts `--input`, `--taxonomy`, `--output` arguments
- ✅ Implements TF-IDF + cosine similarity
- ✅ Generates `*_metadata_enriched.json` output
- ✅ File size: 50-60 KB (as per plan)
- ✅ NO LLM calls made

### Phase 2 Complete When:
- ✅ `scikit-learn` in requirements.txt
- ✅ Installed and verified

### Phase 3 Complete When:
- ✅ Integration test created
- ✅ Test passes with sample data

### Phase 4 Complete When:
- ✅ UI updated to use new script
- ✅ Per-file processing works from UI
- ✅ Taxonomy integration working

### Phase 5 Complete When:
- ✅ README documentation updated
- ✅ CONSOLIDATED_IMPLEMENTATION_PLAN marked complete
- ✅ Code comments added

---

## Time Breakdown

| Phase | Task | Estimated Time |
|-------|------|----------------|
| 1 | Create enrichment script | 4 hours |
| 2 | Update requirements | 0.5 hours |
| 3 | Create tests | 1 hour |
| 4 | Update UI | 1 hour |
| 5 | Documentation | 0.5 hours |
| **Testing** | Manual + integration testing | 2 hours |
| **Debugging** | Fix issues, edge cases | 2 hours |
| **TOTAL** | | **11 hours** |

---

## Dependencies

### Required Files (Must Exist):
- ✅ Tab 2 output: `*_metadata.json` files (17 files exist)
- ⚠️ Tab 3 output: `*_taxonomy.json` files (need to verify)
- ✅ StatisticalExtractor: YAKE + Summa (exists)

### Required Libraries:
- ✅ YAKE (installed)
- ✅ Summa (installed)
- ⚠️ scikit-learn (need to add)

---

## Risk Mitigation

### Risk 1: Taxonomy Files Missing
**Impact**: Cannot load companion books
**Mitigation**: Graceful fallback to all books in metadata_extraction/output/

### Risk 2: Memory Issues with Large Corpus
**Impact**: TF-IDF vectorization fails
**Mitigation**: Limit corpus to top N most relevant books

### Risk 3: Poor Similarity Scores
**Impact**: No related chapters found
**Mitigation**: Lower threshold from 0.7 to 0.5

### Risk 4: Slow Processing
**Impact**: Enrichment takes too long
**Mitigation**: Cache TF-IDF matrix for reuse across chapters

---

## Next Steps After Completion

1. **Validate Tab 4 → Tab 5 Integration**
   - Verify `chapter_generator_all_text.py` can read enriched metadata
   - Test guideline generation with enriched data

2. **Verify Tab 4 → Tab 6 Integration**
   - Ensure aggregate package creation can use enriched metadata
   - Test fallback to basic metadata if enriched not found

3. **Update Tab 5 (if needed)**
   - Modify to use `related_chapters` for cross-references
   - Use `keywords_enriched` and `concepts_enriched` in templates

---

## Completion Checklist

- [ ] Phase 1: Create `enrich_metadata_per_book.py`
- [ ] Phase 2: Install scikit-learn
- [ ] Phase 3: Create integration tests
- [ ] Phase 4: Update UI configuration
- [ ] Phase 5: Update documentation
- [ ] Manual testing passed
- [ ] Integration tests passed
- [ ] UI integration verified
- [ ] Update CONSOLIDATED_IMPLEMENTATION_PLAN.md
- [ ] Commit and push changes
- [ ] Create PR for review

---

**Status**: Ready to implement  
**Blocked By**: None  
**Blocks**: Tab 6 (Aggregate Package Creation)
