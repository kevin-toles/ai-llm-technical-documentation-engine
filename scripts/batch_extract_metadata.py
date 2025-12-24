#!/usr/bin/env python3
"""
Batch Metadata Extraction Script - Simulates Front-End Workflow

This script simulates the desktop_app.py front-end workflow for metadata extraction
by calling generate_metadata_universal.py for each book in the textbooks_json directory.

This is the programmatic equivalent of:
1. Opening the desktop app
2. Going to Tab 2 (Metadata Extraction)
3. Selecting all 201 books
4. Clicking "Run Workflow"

Usage:
    python3 scripts/batch_extract_metadata.py
    
    # With orchestrator (Code-Orchestrator-Service):
    python3 scripts/batch_extract_metadata.py --use-orchestrator
    
    # Dry run (list files without processing):
    python3 scripts/batch_extract_metadata.py --dry-run
    
    # Resume from specific book:
    python3 scripts/batch_extract_metadata.py --resume-from "Building Microservices.json"

Reference:
- desktop_app.py: WORKFLOWS["tab2"] configuration
- workflow_services.py: _build_metadata_extraction_command()
- generate_metadata_universal.py: --input, --auto-detect flags
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Unbuffered output for logging
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__


def log(message: str):
    """Print and flush immediately for real-time logging."""
    print(message, flush=True)

# Base paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
WORKFLOWS_DIR = PROJECT_ROOT / "workflows"

# Workflow configuration (mirrors desktop_app.py WORKFLOWS["tab2"])
METADATA_EXTRACTION_CONFIG = {
    "name": "Metadata Extraction",
    "input_dir": WORKFLOWS_DIR / "pdf_to_json" / "output" / "textbooks_json",
    "input_ext": ".json",
    "output_dir": WORKFLOWS_DIR / "metadata_extraction" / "output",
    "script": WORKFLOWS_DIR / "metadata_extraction" / "scripts" / "generate_metadata_universal.py"
}


def discover_books(input_dir: Path) -> List[Path]:
    """
    Discover all book JSON files in input directory.
    
    Returns:
        List of Path objects for each book JSON file, sorted alphabetically
    """
    if not input_dir.exists():
        print(f"❌ Input directory does not exist: {input_dir}")
        return []
    
    books = sorted(input_dir.glob("*.json"))
    return books


def run_metadata_extraction(
    book_path: Path, 
    script_path: Path, 
    use_orchestrator: bool = False
) -> Dict[str, Any]:
    """
    Run metadata extraction for a single book.
    
    Mirrors workflow_services.py _build_metadata_extraction_command()
    
    Args:
        book_path: Path to book JSON file
        script_path: Path to generate_metadata_universal.py
        use_orchestrator: If True, use Code-Orchestrator-Service
        
    Returns:
        Dict with status, stdout, stderr
    """
    # Build command (mirrors workflow_services.py)
    cmd = ["python3", str(script_path), "--input", str(book_path), "--auto-detect"]
    
    if use_orchestrator:
        cmd.append("--use-orchestrator")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout per book
        )
        
        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
        
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "returncode": -1,
            "stdout": "",
            "stderr": "Timeout: Extraction took longer than 5 minutes"
        }
    except Exception as e:
        return {
            "success": False,
            "returncode": -1,
            "stdout": "",
            "stderr": str(e)
        }


def main():
    parser = argparse.ArgumentParser(
        description="Batch metadata extraction - simulates front-end workflow"
    )
    parser.add_argument(
        "--use-orchestrator",
        action="store_true",
        help="Use Code-Orchestrator-Service for extraction"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List files without processing"
    )
    parser.add_argument(
        "--resume-from",
        type=str,
        help="Resume from specific book filename (e.g., 'Building Microservices.json')"
    )
    parser.add_argument(
        "--max-books",
        type=int,
        default=None,
        help="Maximum number of books to process (for testing)"
    )
    
    args = parser.parse_args()
    
    # Configuration
    input_dir = METADATA_EXTRACTION_CONFIG["input_dir"]
    output_dir = METADATA_EXTRACTION_CONFIG["output_dir"]
    script_path = METADATA_EXTRACTION_CONFIG["script"]
    
    log("=" * 80)
    log("BATCH METADATA EXTRACTION")
    log("=" * 80)
    log(f"Input directory:  {input_dir}")
    log(f"Output directory: {output_dir}")
    log(f"Script:           {script_path}")
    log(f"Use orchestrator: {args.use_orchestrator}")
    log("=" * 80)
    
    # Validate script exists
    if not script_path.exists():
        print(f"❌ Script not found: {script_path}")
        sys.exit(1)
    
    # Discover books
    books = discover_books(input_dir)
    
    if not books:
        print("❌ No books found to process")
        sys.exit(1)
    
    print(f"\n📚 Found {len(books)} books to process")
    
    # Apply resume-from filter if specified
    if args.resume_from:
        found_start = False
        filtered_books = []
        for book in books:
            if book.name == args.resume_from:
                found_start = True
            if found_start:
                filtered_books.append(book)
        
        if not filtered_books:
            print(f"❌ Resume file not found: {args.resume_from}")
            sys.exit(1)
        
        books = filtered_books
        print(f"📌 Resuming from '{args.resume_from}' ({len(books)} books remaining)")
    
    # Apply max-books limit if specified
    if args.max_books:
        books = books[:args.max_books]
        print(f"📌 Limited to first {args.max_books} books")
    
    # Dry run - just list files
    if args.dry_run:
        print("\n🔍 DRY RUN - Files that would be processed:")
        for i, book in enumerate(books, 1):
            print(f"  {i:3d}. {book.name}")
        print(f"\nTotal: {len(books)} books")
        return
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process books
    start_time = datetime.now()
    successful = []
    failed = []
    
    print(f"\n🚀 Starting extraction at {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    for idx, book in enumerate(books, 1):
        print(f"[{idx:3d}/{len(books)}] Processing: {book.name}")
        
        result = run_metadata_extraction(book, script_path, args.use_orchestrator)
        
        if result["success"]:
            print(f"         ✓ Success")
            successful.append(book.name)
            
            # Show summary from output (last few lines)
            if result["stdout"]:
                lines = result["stdout"].strip().split('\n')
                # Look for chapter count in output
                for line in lines[-10:]:
                    if "chapter" in line.lower() or "metadata" in line.lower():
                        print(f"           {line.strip()}")
        else:
            print(f"         ✗ Failed: {result['stderr'][:200] if result['stderr'] else 'Unknown error'}")
            failed.append({
                "book": book.name,
                "error": result["stderr"][:500] if result["stderr"] else "Unknown error"
            })
    
    # Summary
    end_time = datetime.now()
    duration = end_time - start_time
    
    print("\n" + "=" * 80)
    print("EXTRACTION COMPLETE")
    print("=" * 80)
    print(f"Duration:    {duration}")
    print(f"Successful:  {len(successful)} books")
    print(f"Failed:      {len(failed)} books")
    print(f"Output dir:  {output_dir}")
    
    if failed:
        print("\n❌ FAILED BOOKS:")
        for f in failed:
            print(f"  - {f['book']}: {f['error'][:100]}")
    
    # Save run report
    report_path = output_dir / f"extraction_report_{start_time.strftime('%Y%m%d_%H%M%S')}.json"
    report = {
        "started_at": start_time.isoformat(),
        "completed_at": end_time.isoformat(),
        "duration_seconds": duration.total_seconds(),
        "total_books": len(books),
        "successful_count": len(successful),
        "failed_count": len(failed),
        "successful": successful,
        "failed": failed,
        "use_orchestrator": args.use_orchestrator
    }
    
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Report saved: {report_path}")
    
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
