#!/usr/bin/env python3
"""
Tab 6: Aggregate Package Creation

Creates temporary LLM context bundle for Phase 2 enhancement (NO LLM calls).

Purpose: Combine metadata, taxonomy, and guidelines from multiple books
into a single JSON package that Tab 7 can use for LLM enhancement.

Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1551-1701
Python Guidelines: File I/O, pathlib.Path, json module

Input:
- taxonomy.json (from Tab 3)
- *_metadata.json (from Tab 2)
- *_metadata_enriched.json (from Tab 4) - with fallback
- *_guideline.json (from Tab 5) - optional

Output:
- {book}_llm_package_{timestamp}.json (~720 KB for 12 books)
- Location: workflows/llm_enhancement/tmp/

Processing:
1. Load taxonomy
2. Build book list from taxonomy tiers
3. Load metadata with graceful degradation
4. Combine into single package
5. Generate statistics
6. Save with timestamp

NO LLM CALLS - Pure file loading and combining.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


# Path to the LLM cross-reference workflow schema
WORKFLOW_SCHEMA_PATH = Path(__file__).parent.parent / "llm_cross_reference_workflow.json"


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
        
    Reference: PYTHON_GUIDELINES - File I/O patterns
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, encoding='utf-8') as f:
        return json.load(f)


def load_workflow_schema() -> Optional[Dict[str, Any]]:
    """
    Load the LLM cross-reference workflow schema.
    
    Returns:
        Workflow schema dictionary if found, None otherwise
        
    Reference: LLM-Driven Cross-Reference Process documentation
    """
    if WORKFLOW_SCHEMA_PATH.exists():
        try:
            return load_json(WORKFLOW_SCHEMA_PATH)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"  ⚠️  Error loading workflow schema: {e}")
    return None


def save_json(file_path: Path, data: Dict[str, Any]) -> None:
    """
    Save data to JSON file with formatting.
    
    Args:
        file_path: Path to output file
        data: Dictionary to save as JSON
        
    Reference: PYTHON_GUIDELINES - File I/O patterns
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def build_book_list_from_taxonomy(taxonomy: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract book list from taxonomy with tier information.
    
    Args:
        taxonomy: Loaded taxonomy data
        
    Returns:
        List of book dictionaries with name, tier, and priority
        
    Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1575-1586
    """
    book_list = []
    
    tiers = taxonomy.get("tiers", {})
    for tier_name, tier_data in tiers.items():
        books = tier_data.get("books", [])
        priority = tier_data.get("priority", 1)
        
        for book_name in books:
            book_list.append({
                "name": book_name,
                "tier": tier_name,
                "priority": priority
            })
    
    return book_list


def load_book_metadata(
    book_name: str,
    metadata_dir: Path,
    specific_enriched_file: Optional[Path] = None
) -> tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Load metadata for a book with graceful degradation.
    
    If specific_enriched_file is provided and matches this book, uses it.
    Otherwise falls back to basic metadata.
    
    Args:
        book_name: Name of the book (without extension)
        metadata_dir: Directory containing basic metadata files
        specific_enriched_file: Specific enriched file to use (only for matching book)
        
    Returns:
        Tuple of (metadata_dict, note) where note indicates which file was used
        Returns (None, error_message) if neither file exists
        
    Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1588-1616
    """
    # If specific enriched file provided, check if it matches this book
    if specific_enriched_file and specific_enriched_file.exists():
        # Extract book name from enriched file: "BookName_enr_metadata_*.json" -> "BookName"
        enriched_book_name = specific_enriched_file.stem.split("_enr_metadata_")[0]
        if enriched_book_name == book_name:
            try:
                metadata = load_json(specific_enriched_file)
                return metadata, f"using_enriched_metadata ({specific_enriched_file.name})"
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"  ⚠️  Error loading specific enriched metadata for {book_name}: {e}")
    
    # Fallback to basic metadata
    basic_path = metadata_dir / f"{book_name}_metadata.json"
    if basic_path.exists():
        try:
            metadata = load_json(basic_path)
            return metadata, "using_basic_metadata"
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"  ⚠️  Error loading basic metadata for {book_name}: {e}")
    
    # Neither file exists
    return None, f"metadata_not_found (tried {basic_path.name})"


def load_book_guideline(book_name: str, guideline_dir: Path) -> Optional[Dict[str, Any]]:
    """
    Load guideline JSON for a book if it exists.
    
    Args:
        book_name: Name of the book (without extension)
        guideline_dir: Directory containing guideline JSON files
        
    Returns:
        Guideline dictionary if found, None otherwise
        
    Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1560-1561
    """
    guideline_path = guideline_dir / f"{book_name}_guideline.json"
    if guideline_path.exists():
        try:
            return load_json(guideline_path)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"  ⚠️  Error loading guideline for {book_name}: {e}")
    return None


def load_source_book(
    source_book: str,
    metadata_dir: Path,
    guideline_dir: Path,
    specific_enriched_file: Optional[Path] = None
) -> Dict[str, Any]:
    """
    Load source book metadata and guideline.
    
    Args:
        source_book: Name of the source book
        metadata_dir: Directory with basic metadata files
        guideline_dir: Directory with guideline JSON files
        specific_enriched_file: Specific enriched file to use
        
    Returns:
        Source book data dictionary with metadata and optional guideline
        
    Raises:
        FileNotFoundError: If source book metadata not found
        
    Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1618-1632
    Pattern: Extract complex loading logic (REFACTOR phase)
    """
    print(f"\n📄 Loading source book: {source_book}...")
    source_metadata, source_note = load_book_metadata(
        source_book, metadata_dir, specific_enriched_file
    )
    source_guideline = load_book_guideline(source_book, guideline_dir)
    
    if source_metadata is None:
        raise FileNotFoundError(f"Source book metadata not found for {source_book}")
    
    print(f"  Source metadata: {source_note}")
    print(f"  Source guideline: {'found' if source_guideline else 'not found'}")
    
    # Build source book dict
    source_book_data = {
        "name": source_book,
        "tier": "source",
        "metadata": source_metadata
    }
    
    if source_guideline:
        source_book_data["guideline"] = source_guideline
    
    return source_book_data


def load_companion_books(
    book_list: List[Dict[str, Any]],
    source_book: str,
    metadata_dir: Path,
    guideline_dir: Path,
    specific_enriched_file: Optional[Path] = None
) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Load companion books with graceful degradation.
    
    Args:
        book_list: List of books from taxonomy
        source_book: Name of source book (to skip)
        metadata_dir: Directory with basic metadata files
        guideline_dir: Directory with guideline JSON files
        specific_enriched_file: Specific enriched file (will check if it matches each book)
        
    Returns:
        Tuple of (companion_books, missing_books)
        
    Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1633-1655
    Pattern: Extract complex loading logic (REFACTOR phase)
    """
    print("\n📚 Loading companion books...")
    companion_books = []
    missing_books = []
    
    for book_info in book_list:
        book_name = book_info["name"].replace(".json", "")  # Remove .json extension if present
        
        # Skip source book (already loaded)
        if book_name == source_book or book_name == f"{source_book}.json":
            continue
        
        # Load metadata (will use enriched if specific file matches this book)
        metadata, note = load_book_metadata(
            book_name, metadata_dir, specific_enriched_file
        )
        
        if metadata is not None:
            book_data = {
                "name": book_name,
                "tier": book_info["tier"],
                "priority": book_info["priority"],
                "metadata": metadata,
                "note": note
            }
            
            # Load guideline if available
            guideline = load_book_guideline(book_name, guideline_dir)
            if guideline:
                book_data["guideline"] = guideline
            
            companion_books.append(book_data)
            print(f"  ✓ {book_name} ({note})")
        else:
            missing_books.append({
                "name": book_name,
                "tier": book_info["tier"],
                "reason": note
            })
            print(f"  ⚠️  {book_name} - {note}")
    
    return companion_books, missing_books


def calculate_statistics(
    source_metadata: Dict[str, Any],
    companion_books: List[Dict[str, Any]],
    missing_books: List[Dict[str, Any]]
) -> Dict[str, int]:
    """
    Calculate package statistics.
    
    Args:
        source_metadata: Source book metadata
        companion_books: List of companion book data
        missing_books: List of missing book data
        
    Returns:
        Statistics dictionary with counts
        
    Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1656-1670
    Pattern: Extract calculation logic (REFACTOR phase)
    """
    print("\n📊 Calculating statistics...")
    total_chapters = 0
    
    # Count chapters in source book
    if "chapters" in source_metadata:
        total_chapters += len(source_metadata["chapters"])
    elif isinstance(source_metadata, list):
        total_chapters += len(source_metadata)
    
    # Count chapters in companion books
    for book in companion_books:
        metadata = book.get("metadata", {})
        if "chapters" in metadata:
            total_chapters += len(metadata["chapters"])
        elif isinstance(metadata, list):
            total_chapters += len(metadata)
    
    statistics = {
        "total_books": len(companion_books) + 1,  # +1 for source book
        "companion_books": len(companion_books),
        "total_chapters": total_chapters,
        "missing_count": len(missing_books)
    }
    
    print(f"  Total books: {statistics['total_books']}")
    print(f"  Companion books: {statistics['companion_books']}")
    print(f"  Total chapters: {statistics['total_chapters']}")
    print(f"  Missing books: {statistics['missing_count']}")
    
    return statistics


def create_aggregate_package(
    taxonomy_path: Path,
    metadata_dir: Path,
    guideline_dir: Path,
    output_dir: Path,
    enriched_metadata_file: Optional[Path] = None
) -> Path:
    """
    Create aggregate package combining all sources.
    
    Main orchestration function for Tab 6.
    
    Args:
        taxonomy_path: Path to taxonomy JSON file
        metadata_dir: Directory with basic metadata files
        guideline_dir: Directory with guideline JSON files
        output_dir: Directory for output package
        enriched_metadata_file: Optional specific enriched metadata file.
                               Only used for the book that matches the filename.
        
    Returns:
        Path to created package file
        
    Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1618-1699
    Pattern: Orchestration pattern (Architecture Patterns Ch. 8)
    """
    print("\n📦 Tab 6: Aggregate Package Creation")
    print(f"Taxonomy: {taxonomy_path.name}")
    
    # If enriched metadata provided, it will only be used for the matching book
    if enriched_metadata_file:
        print(f"Enriched metadata file: {enriched_metadata_file.name}")
        print("Will use this enriched metadata for the matching book only")
    
    # 1. Load taxonomy
    print("\n📖 Loading taxonomy...")
    taxonomy = load_json(taxonomy_path)
    source_book = taxonomy_path.stem.replace("_taxonomy", "")
    print(f"  Source book: {source_book}")
    
    # 2. Build book list from taxonomy
    print("\n📚 Building book list from taxonomy...")
    book_list = build_book_list_from_taxonomy(taxonomy)
    print(f"  Found {len(book_list)} books across {len(taxonomy.get('tiers', {}))} tiers")
    
    # 3. Load source book (extracted to helper function)
    source_book_data = load_source_book(
        source_book, metadata_dir, guideline_dir,
        specific_enriched_file=enriched_metadata_file
    )
    
    # 4. Load companion books (extracted to helper function)
    companion_books, missing_books = load_companion_books(
        book_list, source_book, metadata_dir, guideline_dir,
        specific_enriched_file=enriched_metadata_file
    )
    
    # 5. Calculate statistics (extracted to helper function)
    statistics = calculate_statistics(
        source_book_data["metadata"],
        companion_books,
        missing_books
    )
    
    # 6. Load workflow schema for LLM guidance
    print("\n📋 Loading LLM workflow schema...")
    workflow_schema = load_workflow_schema()
    if workflow_schema:
        print(f"  ✓ Workflow schema loaded: {workflow_schema.get('workflow_name', 'unknown')}")
    else:
        print("  ⚠️  Workflow schema not found - package will be created without it")
    
    # 7. Build aggregate package
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    package = {
        "project": {
            "id": source_book,
            "generated": datetime.now().isoformat(),
            "source_taxonomy": taxonomy_path.name,
            "package_version": "1.0"
        },
        "taxonomy": taxonomy,
        "source_book": source_book_data,
        "companion_books": companion_books,
        "missing_books": missing_books,
        "statistics": statistics
    }
    
    # Add workflow schema if available
    if workflow_schema:
        package["llm_workflow"] = workflow_schema
    
    # 8. Save package
    output_path = output_dir / f"{source_book}_llm_package_{timestamp}.json"
    save_json(output_path, package)
    
    file_size_kb = output_path.stat().st_size / 1024
    print(f"\n✅ Package created: {output_path.name}")
    print(f"  File size: {file_size_kb:.1f} KB")
    print(f"  Location: {output_path}")
    print("  NO LLM calls made ✓")
    
    return output_path


def create_aggregate_from_enriched(
    enriched_path: Path,
    output_path: Path,
    taxonomy_path: Optional[Path] = None,
    companion_dir: Optional[Path] = None
) -> Path:
    """
    Create aggregate package directly from enriched metadata (WBS 4.1.1).
    
    Simplified mode for Phase 4 LLM Enhancement workflow.
    
    Args:
        enriched_path: Path to enriched metadata JSON (Phase 3 output)
        output_path: Path to output aggregate package
        taxonomy_path: Optional taxonomy JSON for additional context
        companion_dir: Optional directory with companion book metadata
        
    Returns:
        Path to created aggregate package
        
    Reference: END_TO_END_INTEGRATION_WBS.md WBS 4.1.1
    """
    print("\n📦 WBS 4.1.1: Create Aggregate Package")
    print(f"  Enriched metadata: {enriched_path.name}")
    
    # 1. Load enriched metadata from Phase 3
    print("\n📖 Loading enriched metadata from Phase 3...")
    enriched_data = load_json(enriched_path)
    
    # Extract book info - handle both formats
    if isinstance(enriched_data, list):
        # List of chapters format
        book_title = enriched_path.stem.replace("_enriched", "").replace("_", " ")
        chapters = enriched_data
    else:
        # Dict format with chapters key
        book_title = enriched_data.get("book_title", enriched_path.stem.replace("_enriched", ""))
        chapters = enriched_data.get("chapters", [])
    
    print(f"  Book title: {book_title}")
    print(f"  Chapters: {len(chapters)}")
    
    # 2. Load taxonomy if provided
    taxonomy_data = None
    if taxonomy_path and taxonomy_path.exists():
        print(f"\n📋 Loading taxonomy: {taxonomy_path.name}...")
        try:
            taxonomy_data = load_json(taxonomy_path)
            print("  ✓ Taxonomy loaded")
        except Exception as e:
            print(f"  ⚠️  Error loading taxonomy: {e}")
    
    # 3. Load companion books if directory provided
    companion_books = []
    if companion_dir and companion_dir.exists():
        print(f"\n📚 Loading companion books from: {companion_dir}...")
        for companion_file in companion_dir.glob("*_enriched.json"):
            if companion_file.name == enriched_path.name:
                continue  # Skip source book
            try:
                companion_data = load_json(companion_file)
                companion_books.append({
                    "name": companion_file.stem.replace("_enriched", ""),
                    "metadata": companion_data if isinstance(companion_data, dict) else {"chapters": companion_data}
                })
                print(f"  ✓ Loaded: {companion_file.name}")
            except Exception as e:
                print(f"  ⚠️  Error loading {companion_file.name}: {e}")
    
    # 4. Build aggregate package with WBS 4.1.1 structure
    print("\n📦 Building aggregate package...")
    
    # Build source_book structure matching acceptance criteria
    source_book = {
        "name": book_title,
        "chapters": chapters,
        "total_chapters": len(chapters),
        "tier": "source"
    }
    
    # Add enrichment metadata if present in original
    if isinstance(enriched_data, dict) and "enrichment_metadata" in enriched_data:
        source_book["enrichment_metadata"] = enriched_data["enrichment_metadata"]
    
    package = {
        "package_info": {
            "generated": datetime.now().isoformat(),
            "source_file": enriched_path.name,
            "package_version": "1.0",
            "wbs_task": "4.1.1"
        },
        "source_book": source_book,
        "companion_books": companion_books,
        "statistics": {
            "source_chapters": len(chapters),
            "companion_books": len(companion_books),
            "total_chapters": len(chapters) + sum(
                len(cb.get("metadata", {}).get("chapters", [])) 
                for cb in companion_books
            )
        }
    }
    
    # Add taxonomy if loaded
    if taxonomy_data:
        package["taxonomy"] = taxonomy_data
    
    # 5. Validate package structure
    print("\n✅ Validating package structure...")
    required_keys = ["source_book", "package_info"]
    for key in required_keys:
        if key not in package:
            raise ValueError(f"Missing required key: {key}")
    
    if "chapters" not in package["source_book"]:
        raise ValueError("source_book.chapters is required")
    
    if len(package["source_book"]["chapters"]) < 1:
        raise ValueError("source_book must have at least 1 chapter")
    
    # Check first chapter has enriched metadata
    first_chapter = package["source_book"]["chapters"][0]
    if "keywords" not in first_chapter:
        print("  ⚠️  Warning: First chapter missing 'keywords' - may not be enriched metadata")
    else:
        print("  ✓ Enriched metadata present (keywords found)")
    
    print("  ✓ Package structure valid")
    
    # 6. Save package
    output_path.parent.mkdir(parents=True, exist_ok=True)
    save_json(output_path, package)
    
    file_size_kb = output_path.stat().st_size / 1024
    print(f"\n✅ Aggregate package created: {output_path.name}")
    print(f"  File size: {file_size_kb:.1f} KB")
    print(f"  Location: {output_path}")
    
    return output_path


def main():
    """
    Command-line interface for aggregate package creation.
    
    Supports two modes:
    1. Simple mode (WBS 4.1.1): --enriched + --output
    2. Full mode (Tab 6): --taxonomy + --metadata-dir + --guideline-dir
    
    Reference: 
    - END_TO_END_INTEGRATION_WBS.md WBS 4.1.1
    - CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1551-1565
    """
    parser = argparse.ArgumentParser(
        description="Create aggregate package for LLM enhancement",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Simple mode (WBS 4.1.1) - create from enriched metadata
  python create_aggregate_package.py \\
    --enriched workflows/metadata_enrichment/output/test_book_enriched.json \\
    --output workflows/llm_enhancement/input/aggregate_package.json

  # With companion books
  python create_aggregate_package.py \\
    --enriched workflows/metadata_enrichment/output/test_book_enriched.json \\
    --output workflows/llm_enhancement/input/aggregate_package.json \\
    --companion-dir workflows/metadata_enrichment/output

  # Full mode (Tab 6) - with taxonomy
  python create_aggregate_package.py \\
    --taxonomy workflows/taxonomy_setup/output/architecture_patterns_taxonomy.json \\
    --metadata-dir workflows/metadata_extraction/output \\
    --guideline-dir workflows/base_guideline_generation/output \\
    --output-dir workflows/llm_enhancement/tmp

Reference: END_TO_END_INTEGRATION_WBS.md WBS 4.1.1
        """
    )
    
    # Simple mode arguments (WBS 4.1.1)
    parser.add_argument(
        "--enriched",
        type=Path,
        help="Path to enriched metadata JSON (Phase 3 output) - enables simple mode"
    )
    
    parser.add_argument(
        "--output",
        type=Path,
        help="Output path for aggregate package (used with --enriched)"
    )
    
    parser.add_argument(
        "--companion-dir",
        type=Path,
        help="Optional: Directory with companion book enriched metadata"
    )
    
    # Full mode arguments (Tab 6)
    parser.add_argument(
        "--taxonomy",
        type=Path,
        help="Path to taxonomy JSON file (from Tab 3) - enables full mode"
    )
    
    parser.add_argument(
        "--metadata-dir",
        type=Path,
        help="Directory containing basic metadata files (from Tab 2)"
    )
    
    parser.add_argument(
        "--enriched-dir",
        type=Path,
        help="Directory containing enriched metadata files (from Tab 4)"
    )
    
    parser.add_argument(
        "--guideline-dir",
        type=Path,
        help="Directory containing guideline JSON files (from Tab 5)"
    )
    
    parser.add_argument(
        "--enriched-metadata",
        type=Path,
        help="Optional: Specific enriched metadata file for full mode"
    )
    
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("workflows/llm_enhancement/tmp"),
        help="Directory for output package in full mode (default: workflows/llm_enhancement/tmp)"
    )
    
    args = parser.parse_args()
    
    # Determine mode and validate arguments
    if args.enriched:
        # Simple mode (WBS 4.1.1)
        if not args.enriched.exists():
            print(f"❌ Error: Enriched metadata file not found: {args.enriched}", file=sys.stderr)
            sys.exit(1)
        
        # Default output path if not specified
        output_path = args.output
        if output_path is None:
            output_path = Path("workflows/llm_enhancement/input/aggregate_package.json")
        
        try:
            result_path = create_aggregate_from_enriched(
                enriched_path=args.enriched,
                output_path=output_path,
                taxonomy_path=args.taxonomy,
                companion_dir=args.companion_dir
            )
            print(f"\n✅ Success! Package created at: {result_path}")
            return 0
            
        except Exception as e:
            print(f"\n❌ Error creating aggregate package: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            return 1
    
    elif args.taxonomy:
        # Full mode (Tab 6)
        if not args.taxonomy.exists():
            print(f"❌ Error: Taxonomy file not found: {args.taxonomy}", file=sys.stderr)
            sys.exit(1)
        
        if not args.metadata_dir or not args.metadata_dir.exists():
            print("❌ Error: Metadata directory required for full mode", file=sys.stderr)
            sys.exit(1)
        
        if not args.guideline_dir:
            print("⚠️  Warning: Guideline directory not specified")
            args.guideline_dir = Path("workflows/base_guideline_generation/output")
        
        if not args.guideline_dir.exists():
            print(f"⚠️  Warning: Guideline directory not found: {args.guideline_dir}")
            print("   Package will be created without guideline data")
        
        enriched_metadata_file = None
        if args.enriched_metadata:
            if not args.enriched_metadata.exists():
                print(f"❌ Error: Enriched metadata file not found: {args.enriched_metadata}", file=sys.stderr)
                sys.exit(1)
            enriched_metadata_file = args.enriched_metadata
        
        try:
            output_path = create_aggregate_package(
                args.taxonomy,
                args.metadata_dir,
                args.guideline_dir,
                args.output_dir,
                enriched_metadata_file=enriched_metadata_file
            )
            
            print(f"\n✅ Success! Package created at: {output_path}")
            return 0
            
        except Exception as e:
            print(f"\n❌ Error creating aggregate package: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            return 1
    
    else:
        print("❌ Error: Must specify either --enriched (simple mode) or --taxonomy (full mode)", file=sys.stderr)
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
