# UI Specification - LLM Document Enhancer

## Audit Results: Actual Data Flow

### Tab 1: PDF to JSON
**Input:** PDFs (individual files)  
**Output:** JSON files (one per PDF)  
**Script:** `workflows/pdf_to_json/scripts/convert_pdf_to_json.py`

**Corrected UI:**
```
Input Folder (PDFs): [/Users/.../inputs/pdfs/]
Found: 14 PDFs

Select PDFs to convert:
☑ Learning_Python_6th.pdf
☑ Architecture_Patterns.pdf
☐ Building_Microservices.pdf

Output Folder: [/Users/.../workflows/pdf_to_json/output/]

[Clear] [Convert PDFs ▶]
```

**Data Created:** `{pdf_name}.json` in output folder

---

### Tab 2: Metadata Extraction  
**Input:** JSON files (from Tab 1 output)  
**Output:** Metadata JSON files  
**Script:** `workflows/metadata_extraction/scripts/generate_metadata_universal.py --input book.json`

**Corrected UI:**
```
Input Folder (JSONs): [/Users/.../workflows/pdf_to_json/output/]
Found: 14 JSONs

Select JSONs to process:
☑ Learning_Python_6th.json
☑ Architecture_Patterns.json

Output Folder: [/Users/.../workflows/metadata_extraction/output/]

[Clear] [Extract Metadata ▶]
```

**Data Created:** `{book_name}_metadata.json` per JSON

---

### Tab 3: Metadata Enrichment
**Input:** Metadata JSON files (from Tab 2)  
**Output:** Enriched metadata  
**Script:** `workflows/metadata_enrichment/scripts/generate_chapter_metadata.py`

**NEEDS INVESTIGATION** - Script exists but unclear what it does differently from Tab 2

**Corrected UI:**
```
Input Folder: [/Users/.../workflows/metadata_extraction/output/]
Found: 14 metadata files

Select files to enrich:
☑ Learning_Python_6th_metadata.json
☑ Architecture_Patterns_metadata.json

Output Folder: [/Users/.../workflows/metadata_enrichment/output/]

[Clear] [Enrich Metadata ▶]
```

---

### Tab 4: Metadata Cache Merge
**Input:** Metadata files (from Tab 2 or 3)  
**Output:** Single cache file  
**Script:** `workflows/metadata_cache_merge/scripts/merge_metadata_to_cache.py --input-dir DIR`

**Corrected UI:**
```
Input Folder: [/Users/.../workflows/metadata_extraction/output/]
Found: 14 metadata files

Select files to merge:
☑ Select All (14 files)
OR individually select

Output File: [/Users/.../workflows/metadata_cache_merge/output/chapter_metadata_cache.json]

[Clear] [Merge Cache ▶]
```

**Data Created:** Single `chapter_metadata_cache.json`

---

### Tab 5: Base Guideline Generation
**Input:**  
1. JSON files (from Tab 1)  
2. Metadata cache (from Tab 4)  
3. **TAXONOMY** (from Tab 6!)

**Output:** Base guideline markdown  
**Script:** `workflows/base_guideline_generation/scripts/chapter_generator_all_text.py`

**Corrected UI:**
```
Input Folder (JSONs): [/Users/.../workflows/pdf_to_json/output/]
Found: 14 JSONs

Metadata Cache: [/Users/.../workflows/metadata_cache_merge/output/chapter_metadata_cache.json]
☑ Found: chapter_metadata_cache.json

Taxonomy File: [/Users/.../inputs/taxonomy/taxonomy.json]  ⚠️ REQUIRED!
☑ Found: python_microservices.json

Select JSONs to include:
☑ Learning_Python_6th.json (primary)
☑ Architecture_Patterns.json
☑ Fluent_Python_2nd.json

Output File: [/Users/.../workflows/base_guideline_generation/output/PYTHON_GUIDELINES_BASE.md]

[Clear] [Generate Guideline ▶]
```

**Data Created:** Base guideline `.md` file (NO LLM yet)

---

### Tab 6: Taxonomy Setup
**Input:** JSON files (from Tab 1) - **to extract keywords from**  
**Output:** Taxonomy JSON  
**Script:** NEW - needs to be created (currently hardcoded in `book_taxonomy.py`)

**Corrected UI:**
```
Input Folder (JSONs): [/Users/.../workflows/pdf_to_json/output/]
Found: 14 JSONs

🏛️ Architecture Spine:
Available JSONs:                Selected (Priority):
☐ Learning_Python_6th.json      1. Architecture_Patterns.json  [↑][↓][✕]
☑ Architecture_Patterns.json    2. Building_Microservices.json [↑][↓][✕]
☑ Building_Microservices.json
[← Add Selected]

🔧 Implementation:
Available JSONs:                Selected (Priority):
☑ FastAPI_Microservices.json   1. FastAPI_Microservices.json  [↑][↓][✕]
[← Add Selected]

📚 Engineering Practices:
Available JSONs:                Selected (Priority):
☑ Fluent_Python_2nd.json       1. Fluent_Python_2nd.json      [↑][↓][✕]
☑ Python_Distilled.json        2. Python_Distilled.json       [↑][↓][✕]
☑ Learning_Python_Ed6.json     3. Learning_Python_Ed6.json    [↑][↓][✕]
[← Add Selected]

Options:
☑ Auto-extract keywords from chapter titles
☑ Auto-generate cascade relationships
Relevance Weights: [Auto ▼]

Output File: [/Users/.../inputs/taxonomy/taxonomy.json]

[Clear] [Generate Taxonomy ▶]
```

**Data Created:** `taxonomy.json` with extracted keywords

**⚠️ CRITICAL:** This must be done BEFORE Tab 5!

---

### Tab 7: LLM Enhancement
**Input:**  
1. Base guideline (from Tab 5)  
2. **Taxonomy file** (from Tab 6) - MISSING IN MY ORIGINAL DESIGN!  
3. LLM provider + model

**Output:** Enhanced guideline with LLM citations  
**Script:** `workflows/llm_enhancement/scripts/integrate_llm_enhancements.py`

**Corrected UI:**
```
Input File (Base Guideline): 
[/Users/.../workflows/base_guideline_generation/output/PYTHON_GUIDELINES_BASE.md]
☑ Found: PYTHON_GUIDELINES_BASE.md

Taxonomy File: [Browse...]  ⚠️ REQUIRED!
[/Users/.../inputs/taxonomy/python_microservices.json]
☑ Found: python_microservices.json

(Dropdown shows all .json files in inputs/taxonomy/)

LLM Provider:
(•) OpenAI  ( ) Anthropic

Model (OpenAI):
[gpt-4o                    ▼]
- gpt-4o
- gpt-4o-mini
- gpt-4-turbo
- gpt-3.5-turbo

Model (Anthropic): (hidden unless Anthropic selected)
[claude-3-5-sonnet-20241022 ▼]
- claude-3-5-sonnet-20241022
- claude-3-opus-20240229
- claude-3-sonnet-20240229

API Key: [••••••••••••••••••••••]

Output File: [/Users/.../workflows/llm_enhancement/output/PYTHON_GUIDELINES_LLM_ENHANCED.md]

[Clear] [Enhance with LLM ▶]
```

**Data Created:** Final enhanced guideline with LLM citations

---

## CORRECTED Workflow Order:

```
1. PDF → JSON (Tab 1)
2. Extract Metadata (Tab 2)  
3. Enrich Metadata (Tab 3) - OPTIONAL?
4. Merge Cache (Tab 4)
5. **CREATE TAXONOMY** (Tab 6) ← Must happen before Tab 5!
6. Generate Base Guideline (Tab 5) - needs taxonomy from Tab 6
7. LLM Enhancement (Tab 7) - needs taxonomy from Tab 6 + base from Tab 5
```

---

## Key Missing Elements in Original Design:

### 1. **Taxonomy File Selection Missing in Tab 7**
LLM enhancement NEEDS the taxonomy to know which books to cite!

### 2. **Dynamic Model Selection**
When user selects OpenAI → show OpenAI models  
When user selects Anthropic → show Anthropic models

### 3. **Tab 6 Must Run Before Tab 5**
Base guideline generation needs the taxonomy!

### 4. **Multiple Taxonomy Support**
Users could have:
- `python_microservices.json`
- `cpp_game_dev.json`  
- `ml_data_science.json`

UI should let them SELECT which taxonomy to use for Tab 5 and Tab 7.

### 5. **File Validation**
Each tab should show:
- ✅ Found: filename  
- ⚠️ Not found  
- ℹ️ Optional

---

## Recommended UI Improvements:

### Add File Browser Buttons
Instead of just text inputs, add `[Browse...]` buttons to open file picker.

### Add Dependency Warnings
If user tries to run Tab 5 without taxonomy:
```
⚠️ Warning: No taxonomy file selected
Base guideline generation requires a taxonomy.
→ Go to Tab 6 to create one
```

### Show Data Flow Diagram
At the top of UI, show which tabs feed into others:
```
[1] → [2] → [3] → [4] ↘
                         [5] → [7]
             [6] ────────↗     ↗
```

---

## Next Steps:

1. **Create new taxonomy generation script** (Tab 6 backend)
2. **Update Tab 5 UI** to require taxonomy file selection
3. **Update Tab 7 UI** to require taxonomy file selection + dynamic model dropdown
4. **Add file validation** across all tabs
5. **Test complete workflow** with new domain (not Python)

