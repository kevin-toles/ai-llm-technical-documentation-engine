#!/usr/bin/env python3
"""
Full Pipeline Re-Run Script

Re-runs the complete pipeline for all books to generate fresh outputs
with the updated code (BERTopic, Sentence Transformers, etc.)

Usage:
    # Dry run (shows what would be done)
    python scripts/rerun_full_pipeline.py --dry-run
    
    # Re-run Tab 4 enrichment only (most common)
    python scripts/rerun_full_pipeline.py --tab4-only
    
    # Re-run only books in a specific taxonomy
    python scripts/rerun_full_pipeline.py --taxonomy AI-ML_taxonomy_20251128.json --dry-run
    
    # Re-run everything from Tab 2 onwards
    python scripts/rerun_full_pipeline.py --from-tab2
    
    # Re-run specific books
    python scripts/rerun_full_pipeline.py --books "Fluent Python 2nd" "Architecture Patterns with Python"
    
    # Full re-run with backup
    python scripts/rerun_full_pipeline.py --full --backup

Reference:
    - Tab 2: Metadata Extraction (generate_metadata_universal.py)
    - Tab 3: Taxonomy Setup (taxonomy scripts)
    - Tab 4: Metadata Enrichment (enrich_metadata_per_book.py) - BERTopic + Sentence Transformers
    - Tab 5: Guideline Generation (chapter_generator_all_text.py)
"""

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


@dataclass
class PipelineStats:
    """Statistics for pipeline execution."""
    total_books: int = 0
    tab2_success: int = 0
    tab2_failed: int = 0
    tab4_success: int = 0
    tab4_failed: int = 0
    tab5_success: int = 0
    tab5_failed: int = 0
    total_time_seconds: float = 0.0
    errors: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_books": self.total_books,
            "tab2": {"success": self.tab2_success, "failed": self.tab2_failed},
            "tab4": {"success": self.tab4_success, "failed": self.tab4_failed},
            "tab5": {"success": self.tab5_success, "failed": self.tab5_failed},
            "total_time_seconds": round(self.total_time_seconds, 2),
            "errors": self.errors
        }


def get_all_books() -> List[str]:
    """Get list of all books with metadata."""
    metadata_dir = PROJECT_ROOT / "workflows" / "metadata_extraction" / "output"
    books = []
    
    for f in metadata_dir.glob("*_metadata.json"):
        name = f.stem.replace("_metadata", "")
        if name and not name.startswith(".") and name != "chapter_metadata_cache":
            books.append(name)
    
    return sorted(books)


def get_books_from_taxonomy(taxonomy_path: Path) -> List[str]:
    """Extract unique book names from a taxonomy file."""
    if not taxonomy_path.exists():
        print(f"⚠️  Taxonomy file not found: {taxonomy_path}")
        return []
    
    try:
        with open(taxonomy_path, encoding='utf-8') as f:
            data = json.load(f)
        
        books = set()
        for tier_name, tier_data in data.get('tiers', {}).items():
            for book in tier_data.get('books', []):
                name = book.get('name', '').replace('.json', '')
                if name:
                    books.add(name)
        
        return sorted(books)
    except Exception as e:
        print(f"⚠️  Error reading taxonomy: {e}")
        return []


def backup_outputs(backup_dir: Path) -> None:
    """Backup current outputs before re-running."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_dir / f"backup_{timestamp}"
    backup_path.mkdir(parents=True, exist_ok=True)
    
    # Directories to backup
    dirs_to_backup = [
        ("metadata_enrichment", PROJECT_ROOT / "workflows" / "metadata_enrichment" / "output"),
        ("base_guideline_generation", PROJECT_ROOT / "workflows" / "base_guideline_generation" / "output"),
    ]
    
    for name, source in dirs_to_backup:
        if source.exists():
            dest = backup_path / name
            shutil.copytree(source, dest)
            print(f"  ✅ Backed up {name} to {dest}")
    
    print(f"\n📁 Backup saved to: {backup_path}")


def find_taxonomy_file() -> Optional[Path]:
    """Find the most recent comprehensive taxonomy file."""
    taxonomy_dir = PROJECT_ROOT / "workflows" / "taxonomy_setup" / "output"
    
    # Try comprehensive taxonomy first
    comprehensive = list(taxonomy_dir.glob("comprehensive_taxonomy_*.json"))
    if comprehensive:
        return sorted(comprehensive)[-1]  # Most recent
    
    # Try any taxonomy file
    any_taxonomy = list(taxonomy_dir.glob("*_taxonomy_*.json"))
    if any_taxonomy:
        return sorted(any_taxonomy)[-1]
    
    return None


def run_tab2_metadata_extraction(book_name: str, dry_run: bool = False) -> bool:
    """Run Tab 2 metadata extraction for a book."""
    json_dir = PROJECT_ROOT / "workflows" / "pdf_to_json" / "output" / "textbooks_json"
    json_file = json_dir / f"{book_name}.json"
    output_dir = PROJECT_ROOT / "workflows" / "metadata_extraction" / "output"
    output_file = output_dir / f"{book_name}_metadata.json"
    
    if not json_file.exists():
        print(f"  ⚠️  No JSON file for Tab 2: {json_file}")
        return False
    
    script = PROJECT_ROOT / "workflows" / "metadata_extraction" / "scripts" / "generate_metadata_universal.py"
    
    cmd = [
        sys.executable, str(script),
        "--input", str(json_file),
        "--output", str(output_file),
        "--auto-detect"
    ]
    
    if dry_run:
        print(f"  [DRY RUN] Would run: {' '.join(cmd)}")
        return True
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            return True
        else:
            print(f"  ❌ Tab 2 failed: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"  ❌ Tab 2 error: {e}")
        return False


def run_tab4_metadata_enrichment(book_name: str, taxonomy_path: Path, dry_run: bool = False) -> bool:
    """Run Tab 4 metadata enrichment for a book."""
    metadata_dir = PROJECT_ROOT / "workflows" / "metadata_extraction" / "output"
    output_dir = PROJECT_ROOT / "workflows" / "metadata_enrichment" / "output"
    
    input_file = metadata_dir / f"{book_name}_metadata.json"
    output_file = output_dir / f"{book_name}_enriched.json"
    
    if not input_file.exists():
        print(f"  ⚠️  No metadata file for Tab 4: {input_file}")
        return False
    
    script = PROJECT_ROOT / "workflows" / "metadata_enrichment" / "scripts" / "enrich_metadata_per_book.py"
    
    cmd = [
        sys.executable, str(script),
        "--input", str(input_file),
        "--taxonomy", str(taxonomy_path),
        "--output", str(output_file)
    ]
    
    if dry_run:
        print("  [DRY RUN] Would run Tab 4 enrichment")
        return True
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode == 0:
            return True
        else:
            print(f"  ❌ Tab 4 failed: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"  ❌ Tab 4 error: {e}")
        return False


def run_tab5_guideline_generation(book_name: str, taxonomy_path: Optional[Path] = None, dry_run: bool = False) -> bool:
    """Run Tab 5 guideline generation for a book."""
    enriched_dir = PROJECT_ROOT / "workflows" / "metadata_enrichment" / "output"
    json_dir = PROJECT_ROOT / "workflows" / "pdf_to_json" / "output" / "textbooks_json"
    
    enriched_file = enriched_dir / f"{book_name}_enriched.json"
    json_file = json_dir / f"{book_name}.json"
    
    # Use the original JSON file as input (script reads enriched metadata separately)
    if not json_file.exists():
        print(f"  ⚠️  No JSON file for Tab 5: {json_file}")
        return False
    
    if not enriched_file.exists():
        print(f"  ⚠️  No enriched file for Tab 5: {enriched_file}")
        return False
    
    script = PROJECT_ROOT / "workflows" / "base_guideline_generation" / "scripts" / "chapter_generator_all_text.py"
    
    cmd = [
        sys.executable, str(script),
        str(json_file)  # positional argument
    ]
    
    # Add taxonomy if available
    if taxonomy_path and taxonomy_path.exists():
        cmd.extend(["--taxonomy", str(taxonomy_path)])
    
    if dry_run:
        print("  [DRY RUN] Would run Tab 5 guideline generation")
        return True
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode == 0:
            return True
        else:
            print(f"  ❌ Tab 5 failed: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"  ❌ Tab 5 error: {e}")
        return False


def run_pipeline(
    books: List[str],
    run_tab2: bool = False,
    run_tab4: bool = True,
    run_tab5: bool = True,
    dry_run: bool = False,
    backup: bool = False
) -> PipelineStats:
    """Run the pipeline for specified books."""
    stats = PipelineStats()
    stats.total_books = len(books)
    
    start_time = time.time()
    
    # Find taxonomy file
    taxonomy_path = find_taxonomy_file()
    if not taxonomy_path and run_tab4:
        print("❌ No taxonomy file found! Cannot run Tab 4.")
        stats.errors.append("No taxonomy file found")
        return stats
    
    print(f"\n📋 Using taxonomy: {taxonomy_path.name if taxonomy_path else 'N/A'}")
    
    # Backup if requested
    if backup and not dry_run:
        print("\n📦 Creating backup of current outputs...")
        backup_dir = PROJECT_ROOT / "backups"
        backup_outputs(backup_dir)
    
    # Process each book
    for i, book_name in enumerate(books, 1):
        print(f"\n{'─'*60}")
        print(f"[{i}/{len(books)}] 📖 {book_name}")
        print(f"{'─'*60}")
        
        # Tab 2: Metadata Extraction
        if run_tab2:
            print("  📋 Tab 2: Metadata Extraction...")
            if run_tab2_metadata_extraction(book_name, dry_run):
                stats.tab2_success += 1
                print("  ✅ Tab 2 complete")
            else:
                stats.tab2_failed += 1
        
        # Tab 4: Metadata Enrichment
        if run_tab4 and taxonomy_path:
            print("  🔗 Tab 4: Metadata Enrichment (BERTopic + Sentence Transformers)...")
            if run_tab4_metadata_enrichment(book_name, taxonomy_path, dry_run):
                stats.tab4_success += 1
                print("  ✅ Tab 4 complete")
            else:
                stats.tab4_failed += 1
        
        # Tab 5: Guideline Generation
        if run_tab5:
            print("  📖 Tab 5: Guideline Generation...")
            if run_tab5_guideline_generation(book_name, taxonomy_path, dry_run):
                stats.tab5_success += 1
                print("  ✅ Tab 5 complete")
            else:
                stats.tab5_failed += 1
    
    stats.total_time_seconds = time.time() - start_time
    return stats


def print_stats(stats: PipelineStats, dry_run: bool) -> None:
    """Print execution statistics."""
    print(f"\n{'='*60}")
    print("📊 PIPELINE EXECUTION SUMMARY")
    print(f"{'='*60}")
    
    if dry_run:
        print("\n⚠️  DRY RUN - No changes were made")
    
    print(f"\n📚 Total books: {stats.total_books}")
    
    if stats.tab2_success + stats.tab2_failed > 0:
        print("\n📋 Tab 2 (Metadata Extraction):")
        print(f"   ✅ Success: {stats.tab2_success}")
        print(f"   ❌ Failed: {stats.tab2_failed}")
    
    if stats.tab4_success + stats.tab4_failed > 0:
        print("\n🔗 Tab 4 (Metadata Enrichment):")
        print(f"   ✅ Success: {stats.tab4_success}")
        print(f"   ❌ Failed: {stats.tab4_failed}")
    
    if stats.tab5_success + stats.tab5_failed > 0:
        print("\n📖 Tab 5 (Guideline Generation):")
        print(f"   ✅ Success: {stats.tab5_success}")
        print(f"   ❌ Failed: {stats.tab5_failed}")
    
    print(f"\n⏱️  Total time: {stats.total_time_seconds:.1f}s ({stats.total_time_seconds/60:.1f} min)")
    
    if stats.errors:
        print("\n⚠️  Errors:")
        for err in stats.errors:
            print(f"   • {err}")


def _parse_arguments() -> argparse.Namespace:
    """Set up and parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Re-run pipeline to generate fresh outputs with updated code"
    )
    
    # Scope options
    parser.add_argument(
        "--books", nargs="+", help="Specific books to process (default: all)"
    )
    parser.add_argument(
        "--limit", type=int, help="Maximum number of books to process"
    )
    
    # Tab selection
    parser.add_argument(
        "--tab4-only", action="store_true",
        help="Only run Tab 4 enrichment (most common)"
    )
    parser.add_argument(
        "--from-tab2", action="store_true",
        help="Run from Tab 2 onwards (metadata → enrichment → guidelines)"
    )
    parser.add_argument(
        "--full", action="store_true",
        help="Run complete pipeline (Tab 2, 4, 5)"
    )
    
    # Options
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would be done without executing"
    )
    parser.add_argument(
        "--backup", action="store_true",
        help="Backup current outputs before re-running"
    )
    parser.add_argument(
        "--output-report", type=str,
        help="Save execution report to JSON file"
    )
    parser.add_argument(
        "--list-books", action="store_true",
        help="List available books and exit"
    )
    parser.add_argument(
        "--taxonomy", type=str,
        help="Only process books in this taxonomy file"
    )
    
    return parser.parse_args()


def _list_available_books() -> None:
    """Print list of available books and exit."""
    books = get_all_books()
    print(f"\n📚 Available books ({len(books)}):")
    for book in books:
        print(f"  • {book}")


def _get_books_to_process(args: argparse.Namespace) -> Optional[List[str]]:
    """Determine which books to process based on arguments."""
    if args.books:
        books = args.books
    elif args.taxonomy:
        taxonomy_dir = PROJECT_ROOT / "workflows" / "taxonomy_setup" / "output"
        taxonomy_file = taxonomy_dir / args.taxonomy
        if not taxonomy_file.exists():
            taxonomy_file = Path(args.taxonomy)
        books = get_books_from_taxonomy(taxonomy_file)
        if not books:
            print(f"❌ No books found in taxonomy: {args.taxonomy}")
            return None
        print(f"\n📋 Using taxonomy: {args.taxonomy}")
    else:
        books = get_all_books()
    
    if args.limit:
        books = books[:args.limit]
    return books


def _print_run_config(
    books: List[str], run_tab2: bool, run_tab5: bool, args: argparse.Namespace
) -> None:
    """Print pipeline configuration."""
    print("\n" + "="*60)
    print("🚀 FULL PIPELINE RE-RUN")
    print("="*60)
    print(f"\n📚 Books to process: {len(books)}")
    print(f"📋 Tab 2 (Metadata): {'Yes' if run_tab2 else 'No'}")
    print("🔗 Tab 4 (Enrichment): Yes - BERTopic + Sentence Transformers")
    print(f"📖 Tab 5 (Guidelines): {'Yes' if run_tab5 else 'No'}")
    print(f"💾 Backup: {'Yes' if args.backup else 'No'}")
    print(f"🔍 Dry run: {'Yes' if args.dry_run else 'No'}")


def _confirm_execution(args: argparse.Namespace) -> bool:
    """Confirm execution with user if not dry run."""
    if not args.dry_run:
        print("\n⚠️  This will overwrite existing output files!")
        response = input("Continue? [y/N]: ").strip().lower()
        return response == 'y'
    return True


def _save_report(
    args: argparse.Namespace,
    stats: PipelineStats,
    books: List[str],
    run_tab2: bool,
    run_tab4: bool,
    run_tab5: bool
) -> None:
    """Save execution report to JSON file."""
    if not args.output_report:
        return
    
    report_path = Path(args.output_report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    report = {
        "generated": datetime.now().isoformat(),
        "dry_run": args.dry_run,
        "books_processed": books,
        "tabs_run": {"tab2": run_tab2, "tab4": run_tab4, "tab5": run_tab5},
        "stats": stats.to_dict()
    }
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    print(f"\n📁 Report saved to: {report_path}")


def main():
    """Main entry point - orchestrates pipeline execution using helpers."""
    args = _parse_arguments()
    
    # Handle list-books command
    if args.list_books:
        _list_available_books()
        return
    
    # Get books to process
    books = _get_books_to_process(args)
    if books is None:
        return
    
    # Determine which tabs to run
    run_tab2 = args.from_tab2 or args.full
    run_tab4 = True  # Always run Tab 4 (the main focus)
    run_tab5 = not args.tab4_only
    
    # Print configuration
    _print_run_config(books, run_tab2, run_tab5, args)
    
    # Confirm execution
    if not _confirm_execution(args):
        print("Aborted.")
        return
    
    # Run pipeline
    stats = run_pipeline(
        books=books,
        run_tab2=run_tab2,
        run_tab4=run_tab4,
        run_tab5=run_tab5,
        dry_run=args.dry_run,
        backup=args.backup
    )
    
    # Print summary and save report
    print_stats(stats, args.dry_run)
    _save_report(args, stats, books, run_tab2, run_tab4, run_tab5)


if __name__ == "__main__":
    main()
