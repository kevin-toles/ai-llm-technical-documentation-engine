#!/usr/bin/env python3
"""
Convert markdown chapter summaries to JSON guideline format.

Converts existing markdown files from chapter_summaries/ directory
into the structured JSON format expected by Tab 6 aggregate package.

Input: workflows/base_guideline_generation/output/chapter_summaries/*.md
Output: workflows/base_guideline_generation/output/*_guideline.json
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


def parse_markdown_chapter(chapter_text: str) -> Optional[Dict[str, Any]]:
    """
    Parse a single chapter section from markdown.
    
    Expected format:
    ## Chapter N: Title
    *Source: Book, pages X-Y*
    
    ### Chapter Summary
    Summary text here...
    
    ### Concept-by-Concept Breakdown
    ...
    """
    # Extract chapter number and title
    # Security: Use atomic grouping and limit quantifiers to prevent ReDoS
    chapter_match = re.search(r'^## Chapter (\d{1,3}):\s*([^\n]{1,200})$', chapter_text, re.MULTILINE)
    if not chapter_match:
        return None
    
    chapter_number = int(chapter_match.group(1))
    title = chapter_match.group(2).strip()
    
    # Extract page range
    page_match = re.search(r'pages?\s+(\d+)[-–](\d+)', chapter_text)
    page_range = None
    if page_match:
        page_range = {
            "start": int(page_match.group(1)),
            "end": int(page_match.group(2))
        }
    
    # Extract chapter summary
    summary_match = re.search(
        r'### Chapter Summary\s*\n(.+)(?=\n###|\n##|$)',
        chapter_text,
        re.DOTALL
    )
    chapter_summary = ""
    if summary_match:
        chapter_summary = summary_match.group(1).strip()
    
    # Extract concepts from Concept-by-Concept Breakdown
    concepts = []
    concept_section = re.search(
        r'### Concept-by-Concept Breakdown\s*\n(.+)(?=\n##|$)',
        chapter_text,
        re.DOTALL
    )
    
    if concept_section:
        # Find all concept headers (#### **Concept Name**)
        concept_matches = re.finditer(
            r'####\s+\*\*(.+?)\*\*\s+\*\(p\.(\d+)\)\*',
            concept_section.group(1)
        )
        for match in concept_matches:
            concept_name = match.group(1).strip()
            page_number = int(match.group(2))
            if concept_name and concept_name.lower() not in ['none', 'as']:
                concepts.append({
                    "name": concept_name,
                    "page": page_number
                })
    
    return {
        "chapter_number": chapter_number,
        "title": title,
        "page_range": page_range,
        "cross_text_analysis": "",
        "chapter_summary": chapter_summary,
        "concepts": concepts
    }


def convert_markdown_to_json(md_path: Path, output_dir: Path) -> Path:
    """
    Convert a markdown chapter summary file to JSON guideline format.
    
    Args:
        md_path: Path to markdown file
        output_dir: Directory for output JSON file
        
    Returns:
        Path to created JSON file
    """
    print(f"\n📄 Converting: {md_path.name}")
    
    # Read markdown file
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract book name from filename
    # "Chapter_Summaries_Learning Python Ed6.md" -> "Learning Python Ed6"
    filename = md_path.stem
    if filename.startswith("Chapter_Summaries_"):
        book_name = filename.replace("Chapter_Summaries_", "")
    else:
        book_name = filename
    
    # Extract title from first line
    # Security: Limit quantifier to prevent ReDoS
    title_match = re.search(r'^#\s+([^\n]{1,200})$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else f"Comprehensive Guidelines — {book_name}"
    
    # Extract source info
    # Security: Limit quantifier to prevent ReDoS
    source_match = re.search(r'\*Source:\s*([^*\n]{1,200})\*', content)
    source = source_match.group(1) if source_match else book_name
    
    # Split into chapters
    chapter_sections = re.split(r'\n(?=## Chapter \d+:)', content)
    
    chapters = []
    for section in chapter_sections:
        if section.strip() and '## Chapter' in section:
            chapter_data = parse_markdown_chapter(section)
            if chapter_data:
                chapters.append(chapter_data)
    
    # Build JSON structure
    guideline = {
        "book_metadata": {
            "title": title,
            "source": source,
            "book_name": book_name
        },
        "source_info": {
            "generated_by": "convert_md_to_json_guideline.py",
            "generation_date": datetime.now().strftime("%Y-%m-%d"),
            "llm_enabled": False,
            "conversion_source": "markdown_chapter_summaries"
        },
        "chapters": chapters,
        "footnotes": []
    }
    
    # Save JSON file
    output_path = output_dir / f"{book_name}_guideline.json"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(guideline, f, indent=2, ensure_ascii=False)
    
    file_size_kb = output_path.stat().st_size / 1024
    print(f"  ✅ Created: {output_path.name}")
    print(f"     Chapters: {len(chapters)}")
    print(f"     Size: {file_size_kb:.1f} KB")
    
    return output_path


def main():
    """Convert all markdown chapter summaries to JSON guideline format."""
    
    # Paths
    base_dir = Path(__file__).parent.parent
    md_dir = base_dir / "output" / "chapter_summaries"
    output_dir = base_dir / "output"
    
    print("=" * 60)
    print("📚 Converting Markdown Chapter Summaries to JSON Guidelines")
    print("=" * 60)
    print(f"Input:  {md_dir}")
    print(f"Output: {output_dir}")
    
    # Find all markdown files
    md_files = sorted(md_dir.glob("Chapter_Summaries_*.md"))
    
    if not md_files:
        print("\n❌ No markdown chapter summary files found")
        return 1
    
    print(f"\nFound {len(md_files)} markdown files to convert")
    
    # Convert each file
    converted = []
    failed = []
    
    for md_path in md_files:
        try:
            output_path = convert_markdown_to_json(md_path, output_dir)
            converted.append(output_path.name)
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            failed.append(md_path.name)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 CONVERSION SUMMARY")
    print("=" * 60)
    print(f"✅ Converted: {len(converted)}")
    print(f"❌ Failed: {len(failed)}")
    
    if converted:
        print("\n✅ Successfully converted:")
        for name in converted:
            print(f"   - {name}")
    
    if failed:
        print("\n❌ Failed to convert:")
        for name in failed:
            print(f"   - {name}")
    
    print(f"\n📁 Output directory: {output_dir}")
    print("\nThese JSON files can now be used in Tab 6 aggregate packages!")
    
    return 0 if not failed else 1


if __name__ == "__main__":
    exit(main())
