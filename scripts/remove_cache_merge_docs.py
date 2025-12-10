#!/usr/bin/env python3
"""
Remove all Cache Merge references from documentation and update to 6-tab structure
"""
import re
from pathlib import Path

def update_readme():
    """Update README.md to remove Cache Merge stage"""
    readme = Path("README.md")
    content = readme.read_text()
    
    # Remove Stage 4 Cache Merge line, renumber subsequent stages
    old_stages = """Stage 1: Taxonomy Setup          → Configure book categorization system
Stage 2: PDF to JSON              → Convert source PDFs to searchable JSON
Stage 3: Metadata Extraction      → Extract chapter/page metadata from books
Stage 4: Metadata Cache Merge     → Consolidate metadata for fast lookup
Stage 5: Metadata Enrichment      → Add concept tags and keywords
Stage 6: Base Guideline Generation → Generate foundational guideline structure
Stage 7: LLM Enhancement          → Enhance with citations and annotations"""
    
    new_stages = """Stage 1: Taxonomy Setup          → Configure book categorization system
Stage 2: PDF to JSON              → Convert source PDFs to searchable JSON
Stage 3: Metadata Extraction      → Extract chapter/page metadata from books
Stage 4: Metadata Enrichment      → Add concept tags and keywords
Stage 5: Base Guideline Generation → Generate foundational guideline structure
Stage 6: LLM Enhancement          → Enhance with citations and annotations"""
    
    content = content.replace(old_stages, new_stages)
    
    # Update "7-Stage Pipeline" to "6-Stage Pipeline"
    content = content.replace("7-Stage Pipeline", "6-Stage Pipeline")
    
    # Remove cache_merge folder reference
    content = re.sub(
        r'\│\s+├──\s+metadata_cache_merge/\s+#\s+Stage\s+\d+:.*\n',
        '',
        content
    )
    
    # Update Quick Start pipeline diagram
    content = re.sub(
        r'\│\s+\[4\]\s+Cache Merge.*\n',
        '',
        content
    )
    
    readme.write_text(content)
    print("✓ Updated README.md")

def update_workflow_data_flow():
    """Update WORKFLOW_DATA_FLOW.md to remove Tab 3b Cache Merge"""
    doc = Path("WORKFLOW_DATA_FLOW.md")
    if not doc.exists():
        print("⚠️  WORKFLOW_DATA_FLOW.md not found")
        return
    
    content = doc.read_text()
    
    # Remove Tab 3b section completely
    # Find start: "│ Tab 3b: Metadata Cache Merge"
    # Find end: next workflow box or section
    pattern = r'┌──────────────────────────────────────────────────────────────────┐\n│ Tab 3b: Metadata Cache Merge.*?\n└──────────────────────────────────────────────────────────────────┘\n\s+│\n\s+┌───────────────┴───────────────┐\n\s+▼\s+▼\n'
    
    content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Update tab references: Tab 4→3, Tab 5→4, Tab 6→5, Tab 7→6
    content = content.replace("Tab 4: Metadata Enrichment", "Tab 3: Metadata Enrichment")
    content = content.replace("Tab 5: Guideline Generation", "Tab 4: Guideline Generation")
    content = content.replace("Tab 6: Aggregate Package", "Tab 5: Aggregate Package")
    content = content.replace("Tab 7: LLM Enhancement", "Tab 6: LLM Enhancement")
    
    # Remove cache references in dependency descriptions
    content = re.sub(
        r'│\s+└──\s+chapter_metadata_cache\.json\s+│\n',
        '',
        content
    )
    
    doc.write_text(content)
    print("✓ Updated WORKFLOW_DATA_FLOW.md")

def update_workflow_output_analysis():
    """Update WORKFLOW_OUTPUT_ANALYSIS.md to remove Tab 3b"""
    doc = Path("WORKFLOW_OUTPUT_ANALYSIS.md")
    if not doc.exists():
        print("⚠️  WORKFLOW_OUTPUT_ANALYSIS.md not found")
        return
    
    content = doc.read_text()
    
    # Remove Tab 3b section (### Tab 3b: ... to next ###)
    # Fix S5852: Use character class negation instead of reluctant quantifier .*?
    # Per CODING_PATTERNS_ANALYSIS.md Category #6.1
    pattern = r'### Tab 3b: Metadata Cache Merge[^#]*(?=###|\Z)'
    content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Update tab numbering in all references
    content = re.sub(r'Tab 4(?=\s*[:\(])', 'Tab 3', content)
    content = re.sub(r'Tab 5(?=\s*[:\(])', 'Tab 4', content)
    content = re.sub(r'Tab 6(?=\s*[:\(])', 'Tab 5', content)
    content = re.sub(r'Tab 7(?=\s*[:\(])', 'Tab 6', content)
    
    # Remove cache merge from dependency lists
    content = re.sub(r'\s*-\s*Tab 3.*Cache Merge.*\n', '', content)
    
    doc.write_text(content)
    print("✓ Updated WORKFLOW_OUTPUT_ANALYSIS.md")

def update_consolidated_plan():
    """Update CONSOLIDATED_IMPLEMENTATION_PLAN.md"""
    doc = Path("CONSOLIDATED_IMPLEMENTATION_PLAN.md")
    if not doc.exists():
        print("⚠️  CONSOLIDATED_IMPLEMENTATION_PLAN.md not found")
        return
    
    content = doc.read_text()
    
    # Remove Tab 4/5 Cache Merge sections
    patterns = [
        r'Tab 4: Cache Merge\n-+\n.*?(?=\nTab|\Z)',
        r'Tab 5: Cache Merge\n-+\n.*?(?=\nTab|\Z)',
        r'### Tab 4.*Cache Merge.*?\n.*?(?=###|\Z)'
    ]
    
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Mark as deprecated where mentioned
    content = re.sub(
        r'("tab4":\s*\{[^}]*"Cache Merge"[^}]*\})',
        r'\1  # ⚠️ REMOVED - Obsolete (replaced by Tab 5 Aggregate Package)',
        content
    )
    
    # Update references to 7 tabs
    content = content.replace("7 tabs", "6 tabs")
    content = content.replace("tab1-tab7", "tab1-tab6")
    
    doc.write_text(content)
    print("✓ Updated CONSOLIDATED_IMPLEMENTATION_PLAN.md")

def main():
    print("Removing Cache Merge references from documentation...\n")
    
    update_readme()
    update_workflow_data_flow()
    update_workflow_output_analysis()
    update_consolidated_plan()
    
    print("\n✅ All documentation updated to 6-tab structure")
    print("\nRemoved:")
    print("  - Tab 4 'Cache Merge' workflow")
    print("  - chapter_metadata_cache.json references")
    print("  - workflows/metadata_cache_merge/ folder")
    print("\nRenumbered:")
    print("  - Tab 5 (Taxonomy) → Tab 4")
    print("  - Tab 6 (Base Guideline) → Tab 5")
    print("  - Tab 7 (LLM Enhancement) → Tab 6")

if __name__ == "__main__":
    main()
