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
    
    # 6. Build aggregate package
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
    
    # 7. Save package
    output_path = output_dir / f"{source_book}_llm_package_{timestamp}.json"
    save_json(output_path, package)
    
    file_size_kb = output_path.stat().st_size / 1024
    print(f"\n✅ Package created: {output_path.name}")
    print(f"  File size: {file_size_kb:.1f} KB")
    print(f"  Location: {output_path}")
    print("  NO LLM calls made ✓")
    
    return output_path


def main():
    """
    Command-line interface for aggregate package creation.
    
    Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1551-1565
    """
    parser = argparse.ArgumentParser(
        description="Tab 6: Create aggregate package for LLM enhancement",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create package with basic metadata
  python create_aggregate_package.py \\
    --taxonomy workflows/taxonomy_setup/output/architecture_patterns_taxonomy.json \\
    --metadata-dir workflows/metadata_extraction/output \\
    --enriched-dir workflows/metadata_enrichment/output \\
    --guideline-dir workflows/base_guideline_generation/output \\
    --output-dir workflows/llm_enhancement/tmp

  # Create package with enriched metadata (uses enriched for matching book only)
  python create_aggregate_package.py \\
    --taxonomy workflows/taxonomy_setup/output/architecture_patterns_taxonomy.json \\
    --metadata-dir workflows/metadata_extraction/output \\
    --enriched-dir workflows/metadata_enrichment/output \\
    --guideline-dir workflows/base_guideline_generation/output \\
    --enriched-metadata workflows/metadata_enrichment/output/Architecture_Patterns_enr_metadata_2024_01_15_14_30.json \\
    --output-dir workflows/llm_enhancement/tmp

Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md Tab 6
        """
    )
    
    parser.add_argument(
        "--taxonomy",
        type=Path,
        required=True,
        help="Path to taxonomy JSON file (from Tab 3)"
    )
    
    parser.add_argument(
        "--metadata-dir",
        type=Path,
        required=True,
        help="Directory containing basic metadata files (from Tab 2)"
    )
    
    parser.add_argument(
        "--enriched-dir",
        type=Path,
        required=False,
        help="Directory containing enriched metadata files (from Tab 4) - not used if --enriched-metadata is specified"
    )
    
    parser.add_argument(
        "--guideline-dir",
        type=Path,
        required=True,
        help="Directory containing guideline JSON files (from Tab 5)"
    )
    
    parser.add_argument(
        "--enriched-metadata",
        type=Path,
        required=False,
        help="Optional: Specific enriched metadata file. Only used for the book that matches the filename."
    )
    
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("workflows/llm_enhancement/tmp"),
        help="Directory for output package (default: workflows/llm_enhancement/tmp)"
    )
    
    args = parser.parse_args()
    
    # Validate input files
    if not args.taxonomy.exists():
        print(f"❌ Error: Taxonomy file not found: {args.taxonomy}", file=sys.stderr)
        sys.exit(1)
    
    if not args.metadata_dir.exists():
        print(f"❌ Error: Metadata directory not found: {args.metadata_dir}", file=sys.stderr)
        sys.exit(1)
    
    if not args.guideline_dir.exists():
        print(f"⚠️  Warning: Guideline directory not found: {args.guideline_dir}")
        print("   Package will be created without guideline data")
    
    # Validate optional enriched metadata file
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


if __name__ == "__main__":
    sys.exit(main())
