#!/usr/bin/env python3
"""
Extract metadata for books that don't have metadata files yet.
Only processes books where the _metadata.json file is missing.
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path
import json

# Unbuffered output
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__

def log(msg):
    print(msg, flush=True)

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
WORKFLOWS_DIR = PROJECT_ROOT / "workflows"
INPUT_DIR = WORKFLOWS_DIR / "pdf_to_json" / "output" / "textbooks_json"
OUTPUT_DIR = WORKFLOWS_DIR / "metadata_extraction" / "output"
SCRIPT_PATH = WORKFLOWS_DIR / "metadata_extraction" / "scripts" / "generate_metadata_universal.py"
REPORTS_DIR = WORKFLOWS_DIR / "metadata_extraction" / "reports"


def find_missing_books():
    """Find books that don't have metadata extracted yet."""
    missing = []
    for f in sorted(INPUT_DIR.glob("*.json")):
        base = f.stem  # filename without .json
        metadata_file = OUTPUT_DIR / f"{base}_metadata.json"
        if not metadata_file.exists():
            missing.append(f)
    return missing


def run_extraction(book_path: Path, use_orchestrator: bool = False):
    """Run metadata extraction for a single book."""
    cmd = ["python3", str(SCRIPT_PATH), "--input", str(book_path), "--auto-detect"]
    
    if use_orchestrator:
        cmd.append("--use-orchestrator")
    
    # Dynamic timeout based on file size
    file_size_mb = book_path.stat().st_size / (1024 * 1024)
    timeout_seconds = max(300, int(300 + (file_size_mb - 1) * 300))
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_seconds
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "stdout": "", "stderr": "Timeout"}
    except Exception as e:
        return {"success": False, "stdout": "", "stderr": str(e)}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Extract metadata for missing books only")
    parser.add_argument("--use-orchestrator", action="store_true", help="Use orchestrator service")
    parser.add_argument("--dry-run", action="store_true", help="List missing books only")
    parser.add_argument("--max-books", type=int, help="Limit number of books to process")
    args = parser.parse_args()
    
    log("=" * 80)
    log("MISSING METADATA EXTRACTION")
    log("=" * 80)
    
    # Find missing books
    missing = find_missing_books()
    log(f"\n📚 Found {len(missing)} books without metadata\n")
    
    if not missing:
        log("✅ All books have metadata extracted!")
        return
    
    if args.dry_run:
        log("🔍 DRY RUN - Missing books:")
        for i, book in enumerate(missing, 1):
            log(f"  {i:3d}. {book.name}")
        return
    
    # Limit if requested
    if args.max_books:
        missing = missing[:args.max_books]
        log(f"📌 Limited to {args.max_books} books")
    
    # Ensure output dir exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Process
    start_time = datetime.now()
    successful = []
    failed = []
    
    log(f"🚀 Starting at {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    for idx, book in enumerate(missing, 1):
        log(f"[{idx:3d}/{len(missing)}] Processing: {book.name}")
        
        result = run_extraction(book, args.use_orchestrator)
        
        if result["success"]:
            log(f"         ✓ Success")
            successful.append(book.name)
        else:
            error_msg = result["stderr"][:200] if result["stderr"] else "Unknown error"
            log(f"         ✗ Failed: {error_msg}")
            failed.append({"book": book.name, "error": result["stderr"][:500]})
    
    # Summary
    end_time = datetime.now()
    duration = end_time - start_time
    
    log("\n" + "=" * 80)
    log("EXTRACTION COMPLETE")
    log("=" * 80)
    log(f"Duration:    {duration}")
    log(f"Successful:  {len(successful)} books")
    log(f"Failed:      {len(failed)} books")
    
    if failed:
        log("\n❌ FAILED BOOKS:")
        for f in failed:
            log(f"  - {f['book']}")
    
    # Save report
    report_path = REPORTS_DIR / f"missing_extraction_{start_time.strftime('%Y%m%d_%H%M%S')}.json"
    report = {
        "started_at": start_time.isoformat(),
        "completed_at": end_time.isoformat(),
        "duration_seconds": duration.total_seconds(),
        "total_missing": len(missing),
        "successful": successful,
        "failed": failed,
        "use_orchestrator": args.use_orchestrator
    }
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    
    log(f"\n📄 Report saved: {report_path}")


if __name__ == "__main__":
    main()
