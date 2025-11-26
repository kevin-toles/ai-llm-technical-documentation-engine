#!/usr/bin/env python3
"""
Tab 7: LLM Enhancement - Phase 2 Enhancement Workflow

THE ONLY WORKFLOW THAT MAKES LLM API CALLS.

Creates LLM-enhanced guidelines with cross-book synthesis, scholarly citations,
best practices, and common pitfalls.

Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1736-1886
Architecture: Repository Pattern for LLM provider abstraction (ARCHITECTURE_GUIDELINES Ch.2)
Error Handling: EAFP philosophy, try/except (PYTHON_GUIDELINES Ch.1)

Document Analysis Phase Complete (Steps 1-3):
- Step 1: BOOK_TAXONOMY_MATRIX - No LLM concepts (infrastructure task)
- Step 2: Guidelines - Repository Pattern, exception handling, EAFP
- Step 3: NO CONFLICTS - Tab 7 spec is authoritative, reuse Anthropic client

Input:
- Aggregate package JSON (from Tab 6)
- Guideline JSON (from Tab 5)

Output:
- Enhanced guideline Markdown (400-1000 KB with LLM enhancements)

Processing:
1. Load aggregate package
2. Load guideline
3. Build cross-book context index
4. For each chapter:
   a. Get related content from context
   b. Construct LLM prompt
   c. Call LLM API
   d. Parse response
   e. Integrate enhancements
5. Generate enhanced markdown
6. Save output

NO LLM CALLS in Tabs 1-6 - ONLY Tab 7
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import LLM provider (Tab 7 ONLY)
try:
    from workflows.shared.providers import AnthropicProvider, LLMError
    from config.settings import LLMConfig
    LLM_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Warning: LLM provider not available: {e}")
    LLM_AVAILABLE = False


def load_json(file_path: Path) -> Dict[str, Any]:
    """
    Load JSON file with error handling.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Parsed JSON data as dictionary
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
        
    Reference: PYTHON_GUIDELINES - EAFP philosophy
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, encoding='utf-8') as f:
        return json.load(f)


def get_latest_file(pattern: str) -> Optional[Path]:
    """
    Get the most recent file matching a glob pattern.
    
    Args:
        pattern: Glob pattern (e.g., "tmp/*_llm_package_*.json")
        
    Returns:
        Path to most recent file, or None if no matches
        
    Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1755-1758
    """
    files = list(Path(pattern).parent.glob(Path(pattern).name))
    if not files:
        return None
    
    # Sort by modification time, return most recent
    return max(files, key=lambda p: p.stat().st_mtime)


def build_context_index(aggregate: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Build searchable context index from aggregate package.
    
    Creates a dictionary mapping "book_ch{number}" keys to chapter data,
    enabling quick lookup of related content during enhancement.
    
    Args:
        aggregate: Aggregate package from Tab 6
        
    Returns:
        Context index dict with keys like "architecture_patterns_ch1"
        
    Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1765-1780
    """
    print("\n📚 Building cross-book context index...")
    context_index = {}
    
    # Index source book
    source_book = aggregate.get("source_book", {})
    book_name = source_book.get("name", "unknown")
    metadata = source_book.get("metadata", {})
    
    for chapter in metadata.get("chapters", []):
        key = f"{book_name}_ch{chapter.get('number', 0)}"
        context_index[key] = {
            "book": book_name,
            "chapter": chapter.get("number"),
            "title": chapter.get("title", ""),
            "keywords": chapter.get("keywords_enriched", chapter.get("keywords", [])),
            "concepts": chapter.get("concepts_enriched", chapter.get("concepts", [])),
            "summary": chapter.get("summary", "")
        }
    
    # Index companion books
    for book in aggregate.get("companion_books", []):
        book_name = book.get("name", "unknown")
        metadata = book.get("metadata", {})
        
        for chapter in metadata.get("chapters", []):
            key = f"{book_name}_ch{chapter.get('number', 0)}"
            context_index[key] = {
                "book": book_name,
                "chapter": chapter.get("number"),
                "title": chapter.get("title", ""),
                "keywords": chapter.get("keywords_enriched", chapter.get("keywords", [])),
                "concepts": chapter.get("concepts_enriched", chapter.get("concepts", [])),
                "summary": chapter.get("summary", "")
            }
    
    print(f"  Indexed {len(context_index)} chapters across {len(aggregate.get('companion_books', [])) + 1} books")
    return context_index


def construct_enhancement_prompt(
    chapter: Dict[str, Any],
    related_content: List[Dict[str, Any]],
    source_book_name: str
) -> str:
    """
    Construct LLM prompt for chapter enhancement.
    
    Builds a detailed prompt including current chapter data, cross-book context,
    and specific enhancement tasks.
    
    Args:
        chapter: Current chapter data
        related_content: List of related chapter data from context index
        source_book_name: Name of the source book
        
    Returns:
        Formatted LLM prompt string
        
    Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1782-1824
    """
    # Extract chapter details
    title = chapter.get("title", "Unknown Chapter")
    keywords = chapter.get("keywords", [])
    summary = chapter.get("summary", "No summary available")
    
    # Build prompt
    prompt = f"""You are enhancing a technical guideline chapter with scholarly depth.

CURRENT CHAPTER: {source_book_name}
Title: {title}
Keywords: {", ".join(keywords) if keywords else "None"}
Summary: {summary}

CROSS-BOOK CONTEXT:
"""
    
    # Add related content
    if related_content:
        for item in related_content:
            prompt += f"\n- {item['book']}, Ch.{item['chapter']}: {item['title']}"
            if item.get('keywords'):
                prompt += f"\n  Keywords: {', '.join(item['keywords'][:5])}"
            if item.get('summary'):
                prompt += f"\n  Summary: {item['summary'][:200]}..."
            prompt += "\n"
    else:
        prompt += "\nNo cross-references available for this chapter.\n"
    
    prompt += """
TASK: Enhance this chapter by adding the following sections in Markdown format:

1. **Enhanced Summary** (2-3 paragraphs):
   - Integrate insights from related chapters listed above
   - Add cross-book synthesis connecting concepts
   - Maintain technical accuracy and depth
   - If no related chapters, provide deeper analysis of the chapter itself

2. **Key Takeaways** (3-5 bullet points):
   - Actionable insights from this chapter
   - Practical applications developers can use
   - Core concepts that must be understood

3. **Best Practices** (2-4 bullet points with citations when possible):
   - Industry-standard approaches related to this chapter
   - Cite specific books/chapters from context when relevant
   - Practical recommendations for implementation

4. **Common Pitfalls** (2-3 bullet points with solutions):
   - Known challenges developers face with these concepts
   - Practical solutions and workarounds
   - Format: "**Problem**: Description\\n  - Solution: How to fix"

OUTPUT FORMAT (Markdown only, no JSON):
"""
    
    return prompt


def _match_section_header(line: str, section_markers: Dict[str, str]) -> Optional[str]:
    """Match line against known section markers.
    
    Strategy Pattern: Encapsulates section header detection logic.
    Supports both ### and ** markdown header styles.
    
    Args:
        line: Line of text to check
        section_markers: Dict mapping display names to section keys
        
    Returns:
        Section key if matched, None otherwise
        
    Reference: Architecture Patterns Ch. 13 - Strategy Pattern
    """
    for marker, section_key in section_markers.items():
        if marker in line and ('###' in line or '**' in line):
            return section_key
    return None


def _save_section_content(sections: Dict[str, str], section_name: str, content_lines: list) -> None:
    """Save accumulated section content to sections dict.
    
    Service Layer Pattern: Encapsulates content persistence logic.
    Single responsibility: content formatting and storage.
    
    Args:
        sections: Dictionary to store section content
        section_name: Key for this section
        content_lines: Lines of content to save
        
    Reference: Architecture Patterns Ch. 4 - Service Layer
    """
    if section_name:
        sections[section_name] = '\n'.join(content_lines).strip()


def parse_llm_response(response: str) -> Dict[str, str]:
    """
    Parse LLM markdown response into structured sections.
    
    Orchestration Function (Service Layer Pattern): Coordinates parsing workflow
    by delegating to specialized strategy functions. Reduced from CC 10 to CC <10
    through Extract Method refactoring.
    
    Architecture: Following Strategy + Service Layer patterns
    - Thin orchestration layer
    - Delegates to: _match_section_header (Strategy), _save_section_content (Service)
    - Single responsibility: parsing workflow coordination only
    
    Extracts Enhanced Summary, Key Takeaways, Best Practices, and Common Pitfalls
    sections from the LLM's markdown output.
    
    Args:
        response: Raw LLM response text (markdown)
        
    Returns:
        Dictionary with keys: enhanced_summary, key_takeaways, best_practices, common_pitfalls
        
    Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1832-1836
    Reference: PYTHON_GUIDELINES - String processing, file iteration
    Reference: Architecture Patterns Ch. 4 - Service Layer (thin orchestration)
    Reference: Architecture Patterns Ch. 13 - Strategy Pattern (header matching)
    """
    sections = {}
    lines = response.strip().split('\n')
    current_section = None
    current_content = []
    
    # Section headers to look for
    section_markers = {
        'Enhanced Summary': 'enhanced_summary',
        'Key Takeaways': 'key_takeaways',
        'Best Practices': 'best_practices',
        'Common Pitfalls': 'common_pitfalls'
    }
    
    for line in lines:
        # Use strategy function to detect section headers
        matched_section = _match_section_header(line, section_markers)
        
        if matched_section:
            # Save previous section using service function
            _save_section_content(sections, current_section, current_content)
            # Start new section
            current_section = matched_section
            current_content = []
        elif current_section:
            # Add line to current section
            current_content.append(line)
    
    # Save last section
    _save_section_content(sections, current_section, current_content)
    
    return sections


def enhance_chapter(
    chapter: Dict[str, Any],
    context_index: Dict[str, Dict[str, Any]],
    llm_provider: Any,
    source_book_name: str,
    config: LLMConfig
) -> Dict[str, Any]:
    """
    Enhance a single chapter using LLM.
    
    THE ONLY FUNCTION THAT MAKES LLM API CALLS.
    
    Args:
        chapter: Chapter data to enhance
        context_index: Full cross-book context index
        llm_provider: LLM provider instance (Anthropic)
        source_book_name: Name of the source book
        config: LLM configuration
        
    Returns:
        Enhanced chapter data with new fields
        
    Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1782-1836
    Reference: ARCHITECTURE_GUIDELINES Ch.2 - Repository Pattern
    Reference: PYTHON_GUIDELINES Ch.1 - Exception handling, EAFP
    """
    # Get related content if available
    related_chapters = chapter.get("related_chapters", [])
    related_content = []
    
    for rel in related_chapters:
        if isinstance(rel, dict):
            book = rel.get("book", "")
            ch_num = rel.get("chapter", 0)
        else:
            # Handle simple format
            continue
        
        key = f"{book}_ch{ch_num}"
        if key in context_index:
            related_content.append(context_index[key])
    
    # Construct prompt
    prompt = construct_enhancement_prompt(chapter, related_content, source_book_name)
    
    try:
        # Call LLM (THE ONLY LLM CALL IN ENTIRE PROJECT OUTSIDE TESTING)
        print(f"  🤖 Enhancing: {chapter.get('title', 'Unknown')}")
        
        response = llm_provider.call(
            prompt=prompt,
            max_tokens=config.max_tokens,
            temperature=config.temperature
        )
        
        # Parse response
        enhancements = parse_llm_response(response.content)
        
        # Add enhancements to chapter
        enhanced_chapter = chapter.copy()
        enhanced_chapter.update({
            "enhanced_summary": enhancements.get("enhanced_summary", ""),
            "key_takeaways": enhancements.get("key_takeaways", ""),
            "best_practices": enhancements.get("best_practices", ""),
            "common_pitfalls": enhancements.get("common_pitfalls", ""),
            "llm_enhanced": True,
            "llm_model": response.model,
            "llm_tokens": response.input_tokens + response.output_tokens
        })
        
        return enhanced_chapter
        
    except LLMError as e:
        print(f"  ⚠️  LLM Error: {e}")
        # Graceful degradation - return original chapter
        return chapter
    except Exception as e:
        print(f"  ⚠️  Unexpected error: {e}")
        # Graceful degradation - return original chapter
        return chapter


def _format_chapter_markdown(chapter: Dict[str, Any]) -> List[str]:
    """
    Format a single chapter as markdown lines.
    
    Helper function to reduce complexity in generate_enhanced_markdown.
    
    Args:
        chapter: Chapter data dict
        
    Returns:
        List of markdown lines for this chapter
        
    Reference: REFACTOR phase - complexity reduction
    """
    lines = []
    ch_num = chapter.get("number", 0)
    title = chapter.get("title", "Unknown")
    
    lines.append(f"## Chapter {ch_num}: {title}")
    lines.append("")
    
    # Original summary
    if chapter.get("summary"):
        lines.append("### Original Summary")
        lines.append("")
        lines.append(chapter["summary"])
        lines.append("")
    
    # Enhanced summary (LLM-generated)
    if chapter.get("enhanced_summary"):
        lines.append("### Enhanced Summary")
        lines.append("")
        lines.append(chapter["enhanced_summary"])
        lines.append("")
    
    # Key takeaways (LLM-generated)
    if chapter.get("key_takeaways"):
        lines.append("### Key Takeaways")
        lines.append("")
        lines.append(chapter["key_takeaways"])
        lines.append("")
    
    # Best practices (LLM-generated)
    if chapter.get("best_practices"):
        lines.append("### Best Practices")
        lines.append("")
        lines.append(chapter["best_practices"])
        lines.append("")
    
    # Common pitfalls (LLM-generated)
    if chapter.get("common_pitfalls"):
        lines.append("### Common Pitfalls")
        lines.append("")
        lines.append(chapter["common_pitfalls"])
        lines.append("")
    
    # Original keywords
    if chapter.get("keywords"):
        lines.append("### Keywords")
        lines.append("")
        lines.append(", ".join(chapter["keywords"]))
        lines.append("")
    
    # Metadata
    if chapter.get("llm_enhanced"):
        lines.append("### Enhancement Metadata")
        lines.append("")
        lines.append(f"- **LLM Model**: {chapter.get('llm_model', 'Unknown')}")
        lines.append(f"- **Tokens Used**: {chapter.get('llm_tokens', 0)}")
        lines.append("")
    
    lines.append("---")
    lines.append("")
    
    return lines


def generate_enhanced_markdown(
    guideline: Dict[str, Any],
    enhanced_chapters: List[Dict[str, Any]],
    source_book_name: str
) -> str:
    """
    Generate final enhanced markdown output.
    
    Creates a complete markdown document with all enhanced chapters,
    including LLM-generated content and metadata.
    
    Args:
        guideline: Original guideline data
        enhanced_chapters: List of enhanced chapter dicts
        source_book_name: Name of the source book
        
    Returns:
        Complete markdown string
        
    Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1838-1885
    Pattern: Extract helper function to reduce complexity (REFACTOR phase)
    """
    # Build markdown document
    lines = []
    
    # Header
    book_title = guideline.get("metadata", {}).get("book_title", source_book_name.replace("_", " ").title())
    lines.append(f"# {book_title} (LLM-Enhanced Guideline)")
    lines.append("")
    lines.append(f"**Generated**: {datetime.now().strftime('%B %d, %Y')}")
    lines.append("**Enhancement**: Tab 7 Phase 2 LLM Enhancement")
    lines.append("**Source**: CONSOLIDATED_IMPLEMENTATION_PLAN.md Tab 7")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Table of contents
    lines.append("## Table of Contents")
    lines.append("")
    for chapter in enhanced_chapters:
        ch_num = chapter.get("number", 0)
        title = chapter.get("title", "Unknown")
        lines.append(f"{ch_num}. [{title}](#{title.lower().replace(' ', '-')})")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Chapters (using helper function)
    for chapter in enhanced_chapters:
        lines.extend(_format_chapter_markdown(chapter))
    
    return '\n'.join(lines)


def enhance_guideline(
    aggregate_path: Path,
    guideline_path: Path,
    output_dir: Path,
    config: LLMConfig
) -> Path:
    """
    Main orchestration function for Tab 7 enhancement.
    
    Coordinates the complete enhancement workflow from loading inputs
    to generating enhanced output.
    
    Args:
        aggregate_path: Path to aggregate package JSON
        guideline_path: Path to guideline JSON
        output_dir: Directory for output files
        config: LLM configuration
        
    Returns:
        Path to generated enhanced guideline
        
    Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1751-1885
    Pattern: Orchestration pattern (ARCHITECTURE_GUIDELINES Ch.8)
    """
    print("\n🚀 Tab 7: LLM Enhancement - Phase 2")
    print(f"Aggregate package: {aggregate_path.name}")
    print(f"Guideline: {guideline_path.name}")
    
    # 1. Load aggregate package
    print("\n📦 Loading aggregate package...")
    aggregate = load_json(aggregate_path)
    source_book_name = aggregate.get("project", {}).get("id", "unknown")
    print(f"  Source book: {source_book_name}")
    print(f"  Statistics: {aggregate.get('statistics', {})}")
    
    # 2. Load guideline
    print("\n📖 Loading guideline...")
    guideline = load_json(guideline_path)
    
    # Extract chapters (handle different formats)
    if "chapters" in guideline:
        chapters = guideline["chapters"]
    elif isinstance(guideline, list):
        chapters = guideline
    else:
        chapters = []
    
    print(f"  Found {len(chapters)} chapters to enhance")
    
    # 3. Build context index
    context_index = build_context_index(aggregate)
    
    # 4. Initialize LLM provider
    if not LLM_AVAILABLE:
        raise RuntimeError("LLM provider not available - cannot perform enhancement")
    
    print(f"\n🤖 Initializing LLM provider: {config.provider}")
    print(f"  Model: {config.model}")
    print(f"  Max tokens: {config.max_tokens}")
    print(f"  Temperature: {config.temperature}")
    
    llm_provider = AnthropicProvider(api_key=config.api_key, model=config.model)
    
    # 5. Enhance each chapter
    print(f"\n📝 Enhancing {len(chapters)} chapters...")
    enhanced_chapters = []
    total_tokens = 0
    
    for idx, chapter in enumerate(chapters, 1):
        print(f"\nChapter {idx}/{len(chapters)}")
        enhanced = enhance_chapter(chapter, context_index, llm_provider, source_book_name, config)
        enhanced_chapters.append(enhanced)
        
        if enhanced.get("llm_tokens"):
            total_tokens += enhanced["llm_tokens"]
    
    print("\n✅ Enhancement complete")
    print(f"  Total chapters enhanced: {len(enhanced_chapters)}")
    print(f"  Total tokens used: {total_tokens:,}")
    
    # 6. Generate markdown
    print("\n📄 Generating enhanced markdown...")
    markdown = generate_enhanced_markdown(guideline, enhanced_chapters, source_book_name)
    
    # 7. Save output
    output_path = output_dir / f"{source_book_name}_guideline_enhanced.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    output_path.write_text(markdown, encoding='utf-8')
    
    file_size_kb = output_path.stat().st_size / 1024
    print(f"\n✅ Enhanced guideline created: {output_path.name}")
    print(f"  File size: {file_size_kb:.1f} KB")
    print(f"  Location: {output_path}")
    
    return output_path


def main():
    """
    Command-line interface for Tab 7 LLM enhancement.
    
    Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1736-1750
    """
    parser = argparse.ArgumentParser(
        description="Tab 7: Enhance guideline with LLM-powered insights",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Enhance architecture_patterns guideline
  python llm_enhance_guideline.py \\
    --aggregate workflows/llm_enhancement/tmp/architecture_patterns_llm_package_*.json \\
    --guideline workflows/base_guideline_generation/output/architecture_patterns_guideline.json \\
    --output-dir workflows/llm_enhancement/output

  # Use specific files
  python llm_enhance_guideline.py \\
    --aggregate workflows/llm_enhancement/tmp/architecture_patterns_llm_package_20251120_143000.json \\
    --guideline workflows/base_guideline_generation/output/architecture_patterns_guideline.json \\
    --output-dir workflows/llm_enhancement/output

Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md Tab 7
THE ONLY WORKFLOW THAT MAKES LLM API CALLS (Tabs 1-6 use statistical methods only)
        """
    )
    
    parser.add_argument(
        "--aggregate",
        type=str,
        required=True,
        help="Path or pattern to aggregate package JSON (from Tab 6)"
    )
    
    parser.add_argument(
        "--guideline",
        type=Path,
        required=True,
        help="Path to guideline JSON (from Tab 5)"
    )
    
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("workflows/llm_enhancement/output"),
        help="Directory for enhanced guideline output (default: workflows/llm_enhancement/output)"
    )
    
    args = parser.parse_args()
    
    # Resolve aggregate path (handle glob patterns)
    if '*' in args.aggregate:
        aggregate_path = get_latest_file(args.aggregate)
        if not aggregate_path:
            print(f"❌ Error: No files match pattern: {args.aggregate}", file=sys.stderr)
            sys.exit(1)
    else:
        aggregate_path = Path(args.aggregate)
    
    # Validate inputs
    if not aggregate_path.exists():
        print(f"❌ Error: Aggregate package not found: {aggregate_path}", file=sys.stderr)
        sys.exit(1)
    
    if not args.guideline.exists():
        print(f"❌ Error: Guideline not found: {args.guideline}", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Load configuration
        config = LLMConfig()
        
        # Run enhancement
        output_path = enhance_guideline(
            aggregate_path,
            args.guideline,
            args.output_dir,
            config
        )
        
        print(f"\n✅ Success! Enhanced guideline created at: {output_path}")
        return 0
        
    except Exception as e:
        print(f"\n❌ Error during enhancement: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
