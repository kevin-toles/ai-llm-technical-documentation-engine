#!/usr/bin/env python3
"""
Batch convert PDFs to JSON format.

Usage:
    python scripts/batch_convert_pdfs.py --input-dir <pdf_dir> --output-dir <json_dir>
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from workflows.pdf_to_json.scripts.convert_pdf_to_json import convert_pdf_to_json


def batch_convert(input_dir: Path, output_dir: Path, dry_run: bool = False) -> dict:
    """
    Convert all PDFs in input_dir to JSON format.
    
    Args:
        input_dir: Directory containing PDF files
        output_dir: Directory for output JSON files
        dry_run: If True, only list files without converting
        
    Returns:
        Dictionary with success/failure counts and details
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    
    if not input_dir.exists():
        print(f"❌ Input directory not found: {input_dir}")
        return {"error": "Input directory not found"}
    
    # Get all PDF files
    pdf_files = sorted(input_dir.glob("*.pdf"))
    total = len(pdf_files)
    
    print("\n" + "="*80)
    print("📚 BATCH PDF TO JSON CONVERSION")
    print("="*80)
    print(f"Input:  {input_dir}")
    print(f"Output: {output_dir}")
    print(f"Total PDFs: {total}")
    print(f"{'='*80}\n")
    
    if dry_run:
        print("🔍 DRY RUN - Listing files only:\n")
        for i, pdf in enumerate(pdf_files, 1):
            output_file = output_dir / f"{pdf.stem}.json"
            exists = "✅ EXISTS" if output_file.exists() else "📄 NEW"
            print(f"  {i:3}. {pdf.name}")
            print(f"       → {output_file.name} [{exists}]")
        print(f"\n📊 Would convert {total} PDFs")
        return {"dry_run": True, "total": total}
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Track results
    results = {
        "success": [],
        "failed": [],
        "skipped": [],
        "start_time": datetime.now().isoformat()
    }
    
    for i, pdf_path in enumerate(pdf_files, 1):
        output_file = output_dir / f"{pdf_path.stem}.json"
        
        # Skip if already exists
        if output_file.exists():
            print(f"\n⏭️  [{i}/{total}] Skipping (exists): {pdf_path.name}")
            results["skipped"].append(pdf_path.name)
            continue
        
        print(f"\n{'='*80}")
        print(f"📖 [{i}/{total}] Converting: {pdf_path.name}")
        print(f"{'='*80}")
        
        try:
            success = convert_pdf_to_json(
                pdf_path=str(pdf_path),
                output_path=str(output_file),
                use_unstructured=True
            )
            
            if success:
                print(f"✅ Success: {output_file.name}")
                results["success"].append(pdf_path.name)
            else:
                print(f"❌ Failed: {pdf_path.name}")
                results["failed"].append(pdf_path.name)
                
        except Exception as e:
            print(f"❌ Error converting {pdf_path.name}: {e}")
            results["failed"].append(f"{pdf_path.name}: {str(e)}")
    
    # Print summary
    results["end_time"] = datetime.now().isoformat()
    
    print("\n" + "="*80)
    print("📊 CONVERSION SUMMARY")
    print("="*80)
    print(f"✅ Successful: {len(results['success'])}")
    print(f"⏭️  Skipped:    {len(results['skipped'])}")
    print(f"❌ Failed:     {len(results['failed'])}")
    print(f"📚 Total:      {total}")
    
    if results["failed"]:
        print("\n❌ Failed files:")
        for f in results["failed"]:
            print(f"   - {f}")
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Batch convert PDFs to JSON")
    parser.add_argument("--input-dir", "-i", required=True,
                        help="Directory containing PDF files")
    parser.add_argument("--output-dir", "-o", required=True,
                        help="Directory for output JSON files")
    parser.add_argument("--dry-run", "-n", action="store_true",
                        help="List files without converting")
    
    args = parser.parse_args()
    
    results = batch_convert(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        dry_run=args.dry_run
    )
    
    # Exit with error if any failures
    if results.get("failed"):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
