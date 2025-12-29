#!/usr/bin/env python3
"""Validate chapter counts between source JSON and metadata files."""

import json
from pathlib import Path

src_dir = Path(__file__).parent.parent / "workflows" / "pdf_to_json" / "output" / "textbooks_json"
meta_dir = Path(__file__).parent.parent / "workflows" / "metadata_extraction" / "output"

results = []
mismatches = []
errors = []

src_files = sorted(src_dir.glob("*.json"))
print(f"Validating {len(src_files)} books...\n")

for src_file in src_files:
    book_name = src_file.stem
    meta_file = meta_dir / f"{book_name}_metadata.json"
    
    try:
        # Load source
        with open(src_file, "r", encoding="utf-8") as f:
            src_data = json.load(f)
        
        # Source structure: {metadata, chapters, pages}
        if isinstance(src_data, dict):
            src_chapters = src_data.get("chapters", [])
        else:
            src_chapters = src_data
        src_count = len(src_chapters)
        
        if not meta_file.exists():
            errors.append(f"{book_name}: No metadata file")
            continue
        
        # Load metadata
        with open(meta_file, "r", encoding="utf-8") as f:
            meta_data = json.load(f)
        
        # Metadata structure: list of chapters OR {chapters: [...]}
        if isinstance(meta_data, list):
            meta_count = len(meta_data)
        elif isinstance(meta_data, dict):
            meta_count = len(meta_data.get("chapters", []))
        else:
            meta_count = 0
        
        if src_count != meta_count:
            mismatches.append({
                "book": book_name[:50],
                "src_chapters": src_count,
                "meta_chapters": meta_count,
                "diff": meta_count - src_count
            })
        
        results.append({
            "book": book_name,
            "src": src_count,
            "meta": meta_count,
            "match": src_count == meta_count
        })
        
    except json.JSONDecodeError as e:
        errors.append(f"{book_name}: JSON error - {str(e)[:50]}")
    except Exception as e:
        errors.append(f"{book_name}: {str(e)[:50]}")

# Summary
matched = sum(1 for r in results if r["match"])
total_src_chapters = sum(r["src"] for r in results)
total_meta_chapters = sum(r["meta"] for r in results)

print("=" * 70)
print("CHAPTER VALIDATION SUMMARY")
print("=" * 70)
print(f"Books validated:     {len(results)}")
if results:
    print(f"Chapters match:      {matched}/{len(results)} books ({100*matched/len(results):.1f}%)")
print(f"Total src chapters:  {total_src_chapters}")
print(f"Total meta chapters: {total_meta_chapters}")
print(f"Difference:          {total_meta_chapters - total_src_chapters:+d}")
print("=" * 70)

if mismatches:
    print(f"\nMISMATCHES ({len(mismatches)}):")
    print("-" * 70)
    print(f"{'Book':<50} {'Src':>6} {'Meta':>6} {'Diff':>6}")
    print("-" * 70)
    for m in sorted(mismatches, key=lambda x: abs(x["diff"]), reverse=True)[:30]:
        print(f"{m['book']:<50} {m['src_chapters']:>6} {m['meta_chapters']:>6} {m['diff']:>+6}")
    if len(mismatches) > 30:
        print(f"... and {len(mismatches) - 30} more")

if errors:
    print(f"\nERRORS ({len(errors)}):")
    for e in errors[:10]:
        print(f"  - {e}")
    if len(errors) > 10:
        print(f"  ... and {len(errors) - 10} more")
