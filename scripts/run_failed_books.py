#!/usr/bin/env python3
"""
Run metadata extraction on the 9 books that previously timed out.

These books are larger than average (2.5-4.4MB) and need the dynamic timeout fix.
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

# The 9 books that timed out with the original 5-minute timeout
FAILED_BOOKS = [
    "AI Engineering Building Applications.json",
    "Building Secure and Reliable Systems - Heather Adkins.json",
    "C++ Templates_ The Complete Guide.json",
    "Code Complete - Steve McConnell.json",
    "Computer Systems A Programmer\u2019s Perspective.json",  # Unicode apostrophe U+2019
    "Continuous Delivery - Jez Humble David Farley (Copy).json",
    "Continuous Delivery - Jez Humble David Farley.json",
    "Designing Data-Intensive Applications.json",
    "Distributed Systems - Maarten van Steen (Copy).json",
]

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
INPUT_DIR = PROJECT_ROOT / "workflows" / "pdf_to_json" / "output" / "textbooks_json"
SCRIPT_PATH = PROJECT_ROOT / "workflows" / "metadata_extraction" / "scripts" / "generate_metadata_universal.py"


def run_extraction(book_name: str, use_orchestrator: bool = True) -> dict:
    """Run metadata extraction for a single book with dynamic timeout."""
    book_path = INPUT_DIR / book_name
    
    if not book_path.exists():
        return {"success": False, "error": f"File not found: {book_path}"}
    
    # Calculate dynamic timeout based on file size
    file_size_mb = book_path.stat().st_size / (1024 * 1024)
    timeout_seconds = max(300, int(300 + (file_size_mb - 1) * 300))  # 5-20 min range
    
    print(f"\n{'='*60}")
    print(f"📚 Processing: {book_name}")
    print(f"   Size: {file_size_mb:.1f} MB")
    print(f"   Timeout: {timeout_seconds // 60} minutes")
    print(f"{'='*60}")
    
    cmd = ["python3", str(SCRIPT_PATH), "--input", str(book_path), "--auto-detect"]
    if use_orchestrator:
        cmd.append("--use-orchestrator")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_seconds
        )
        
        if result.returncode == 0:
            print(f"✅ SUCCESS: {book_name}")
            return {"success": True, "stdout": result.stdout}
        else:
            print(f"❌ FAILED: {book_name}")
            print(f"   Error: {result.stderr[-500:] if result.stderr else 'Unknown'}")
            return {"success": False, "error": result.stderr}
            
    except subprocess.TimeoutExpired:
        print(f"⏰ TIMEOUT: {book_name} (exceeded {timeout_seconds}s)")
        return {"success": False, "error": f"Timeout after {timeout_seconds}s"}
    except Exception as e:
        print(f"💥 EXCEPTION: {book_name}: {e}")
        return {"success": False, "error": str(e)}


def main():
    print("=" * 70)
    print("RE-RUNNING 9 FAILED BOOKS WITH DYNAMIC TIMEOUT")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    use_orchestrator = "--use-orchestrator" in sys.argv or "-o" in sys.argv
    dry_run = "--dry-run" in sys.argv
    
    print(f"Use orchestrator: {use_orchestrator}")
    print(f"Dry run: {dry_run}")
    print(f"\nBooks to process: {len(FAILED_BOOKS)}")
    
    for book in FAILED_BOOKS:
        book_path = INPUT_DIR / book
        if book_path.exists():
            size_mb = book_path.stat().st_size / (1024 * 1024)
            print(f"  - {book} ({size_mb:.1f} MB)")
        else:
            print(f"  - {book} (NOT FOUND)")
    
    if dry_run:
        print("\n[DRY RUN] No processing performed.")
        return
    
    results = {"success": [], "failed": []}
    
    for book in FAILED_BOOKS:
        result = run_extraction(book, use_orchestrator=use_orchestrator)
        if result["success"]:
            results["success"].append(book)
        else:
            results["failed"].append((book, result.get("error", "Unknown")))
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"✅ Successful: {len(results['success'])}/{len(FAILED_BOOKS)}")
    print(f"❌ Failed: {len(results['failed'])}/{len(FAILED_BOOKS)}")
    
    if results["failed"]:
        print("\nFailed books:")
        for book, error in results["failed"]:
            print(f"  - {book}: {error[:100]}")
    
    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
