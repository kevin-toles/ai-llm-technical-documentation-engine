#!/usr/bin/env python3
"""
Batch MSEP Enrichment Script

Processes all metadata files through the MSEP pipeline via Gateway API.

Usage:
    python scripts/batch_msep_enrichment.py
    python scripts/batch_msep_enrichment.py --limit 5  # Test with 5 files
    python scripts/batch_msep_enrichment.py --file "A Philosophy of Software Design_metadata.json"
"""

import argparse
import asyncio
import aiohttp
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any, Optional


# =============================================================================
# Configuration
# =============================================================================

GATEWAY_URL = "http://localhost:8080"
GATEWAY_TIMEOUT = 300  # 5 minutes per book
INPUT_DIR = Path(__file__).parent.parent / "workflows" / "metadata_extraction" / "output"
OUTPUT_DIR = Path(__file__).parent.parent / "workflows" / "metadata_enrichment" / "output"

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class EnrichmentResult:
    """Result from MSEP enrichment."""
    file_name: str
    success: bool
    chapters_count: int = 0
    cross_refs_count: int = 0
    processing_time_ms: float = 0.0
    error: Optional[str] = None


@dataclass
class BatchStats:
    """Batch processing statistics."""
    total_files: int = 0
    successful: int = 0
    failed: int = 0
    skipped: int = 0
    total_chapters: int = 0
    total_cross_refs: int = 0
    total_time_ms: float = 0.0
    errors: list[str] = field(default_factory=list)


# =============================================================================
# MSEP Client
# =============================================================================

async def call_msep(
    session: aiohttp.ClientSession,
    book_title: str,
    chapters: list[dict[str, Any]],
) -> dict[str, Any]:
    """Call MSEP via Gateway API.
    
    Args:
        session: aiohttp session
        book_title: Title of the book
        chapters: List of chapter dicts with text content
        
    Returns:
        Dict with enrichment results or error
    """
    url = f"{GATEWAY_URL}/v1/tools/execute"
    
    # Build corpus and chapter index
    corpus = []
    chapter_index = []
    
    for i, chapter in enumerate(chapters):
        # Get chapter text - try different field names
        # Metadata files use "summary", source files might use "text" or "content"
        text = (
            chapter.get("summary", "") or 
            chapter.get("text", "") or 
            chapter.get("content", "") or
            ""
        )
        
        # Preserve original summary separately
        original_summary = chapter.get("summary", "")
        
        if not text:
            # Try to build text from other fields
            text = f"{chapter.get('title', '')} {chapter.get('description', '')}"
        
        corpus.append(text)
        
        # Get chapter number and title
        ch_num = chapter.get("chapter_number", i + 1)
        ch_title = chapter.get("title", f"Chapter {ch_num}")
        
        chapter_index.append({
            "book": book_title,
            "chapter": ch_num if isinstance(ch_num, int) else i + 1,
            "title": ch_title,
            "summary": original_summary,
        })
    
    payload = {
        "name": "enrich_metadata",
        "arguments": {
            "corpus": corpus,
            "chapter_index": chapter_index,
        },
    }
    
    try:
        async with session.post(url, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                # Handle various response formats
                if isinstance(data, list):
                    # Direct list of enriched chapters
                    return {"success": True, "result": {"chapters": data}}
                elif isinstance(data, dict):
                    result = data.get("result", data)
                    if isinstance(result, list):
                        return {"success": True, "result": {"chapters": result}}
                    return {"success": True, "result": result}
                else:
                    return {"success": False, "error": f"Unexpected response type: {type(data)}"}
            else:
                error_text = await response.text()
                return {"success": False, "error": f"HTTP {response.status}: {error_text[:200]}"}
    except asyncio.TimeoutError:
        return {"success": False, "error": "Request timeout"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# =============================================================================
# File Processing
# =============================================================================

async def process_file(
    session: aiohttp.ClientSession,
    input_path: Path,
    output_dir: Path,
) -> EnrichmentResult:
    """Process a single metadata file through MSEP.
    
    Args:
        session: aiohttp session
        input_path: Path to input metadata JSON
        output_dir: Directory for enriched output
        
    Returns:
        EnrichmentResult with status and metrics
    """
    file_name = input_path.name
    start_time = time.perf_counter()
    
    try:
        # Load metadata
        with open(input_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        # Handle both structures:
        # 1. List of chapters (current format): [{"chapter_number": 1, "title": ..., "summary": ...}, ...]
        # 2. Dict with chapters key: {"book": {...}, "chapters": [...]}
        if isinstance(metadata, list):
            chapters = metadata
            book_title = input_path.stem.replace("_metadata", "")
            book_info = {"title": book_title}
        else:
            book_info = metadata.get("book", metadata.get("metadata", {}))
            book_title = book_info.get("title", input_path.stem.replace("_metadata", ""))
            chapters = metadata.get("chapters", [])
        
        if not chapters:
            return EnrichmentResult(
                file_name=file_name,
                success=False,
                error="No chapters found in metadata",
            )
        
        # Call MSEP
        result = await call_msep(session, book_title, chapters)
        
        if not result["success"]:
            return EnrichmentResult(
                file_name=file_name,
                success=False,
                error=result["error"],
            )
        
        # Build enriched output
        msep_result = result.get("result")
        if msep_result is None:
            return EnrichmentResult(
                file_name=file_name,
                success=False,
                error="MSEP returned null result",
            )
        
        enriched_chapters = msep_result.get("chapters", [])
        
        # Count similar chapters
        similar_count = sum(
            len(ch.get("similar_chapters", []))
            for ch in enriched_chapters
        )
        
        enriched_output = {
            "book": book_info,
            "enrichment_provenance": msep_result.get("enrichment_provenance", {
                "method": "msep",
                "timestamp": datetime.now().isoformat(),
                "gateway_url": GATEWAY_URL,
            }),
            "chapters": enriched_chapters,
            "metadata": metadata.get("metadata", {}) if isinstance(metadata, dict) else {},
            "pages": metadata.get("pages", []) if isinstance(metadata, dict) else [],
        }
        
        # Save output
        output_name = input_path.stem.replace("_metadata", "") + "_enriched.json"
        output_path = output_dir / output_name
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(enriched_output, f, indent=2, ensure_ascii=False)
        
        end_time = time.perf_counter()
        processing_time = (end_time - start_time) * 1000
        
        return EnrichmentResult(
            file_name=file_name,
            success=True,
            chapters_count=len(enriched_chapters),
            cross_refs_count=similar_count,
            processing_time_ms=processing_time,
        )
        
    except json.JSONDecodeError as e:
        return EnrichmentResult(
            file_name=file_name,
            success=False,
            error=f"JSON parse error: {e}",
        )
    except Exception as e:
        return EnrichmentResult(
            file_name=file_name,
            success=False,
            error=str(e),
        )


async def check_gateway_health() -> bool:
    """Check if Gateway is available."""
    try:
        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(f"{GATEWAY_URL}/health") as response:
                return response.status == 200
    except Exception:
        return False


# =============================================================================
# Main Processing Loop
# =============================================================================

async def process_batch(
    input_files: list[Path],
    output_dir: Path,
    concurrency: int = 1,  # Sequential by default to avoid overwhelming services
) -> BatchStats:
    """Process batch of files through MSEP.
    
    Args:
        input_files: List of input file paths
        output_dir: Output directory
        concurrency: Max concurrent requests (default 1 = sequential)
        
    Returns:
        BatchStats with processing metrics
    """
    stats = BatchStats(total_files=len(input_files))
    
    # Check Gateway health
    if not await check_gateway_health():
        print("❌ Gateway not available. Please start services first.")
        print("   Run: cd llm-gateway && docker-compose up -d")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print(f"MSEP Batch Enrichment")
    print(f"{'='*60}")
    print(f"Input directory: {INPUT_DIR}")
    print(f"Output directory: {output_dir}")
    print(f"Files to process: {len(input_files)}")
    print(f"Gateway: {GATEWAY_URL}")
    print(f"{'='*60}\n")
    
    timeout = aiohttp.ClientTimeout(total=GATEWAY_TIMEOUT)
    
    async with aiohttp.ClientSession(timeout=timeout) as session:
        for i, input_path in enumerate(input_files, 1):
            print(f"[{i}/{len(input_files)}] Processing: {input_path.name[:50]}...", end=" ", flush=True)
            
            result = await process_file(session, input_path, output_dir)
            
            if result.success:
                stats.successful += 1
                stats.total_chapters += result.chapters_count
                stats.total_cross_refs += result.cross_refs_count
                stats.total_time_ms += result.processing_time_ms
                print(f"✓ {result.chapters_count} chapters, {result.cross_refs_count} refs ({result.processing_time_ms:.0f}ms)")
            else:
                stats.failed += 1
                stats.errors.append(f"{result.file_name}: {result.error}")
                print(f"✗ {result.error[:50]}")
    
    return stats


def print_summary(stats: BatchStats) -> None:
    """Print batch processing summary."""
    print(f"\n{'='*60}")
    print("BATCH PROCESSING SUMMARY")
    print(f"{'='*60}")
    print(f"Total files:      {stats.total_files}")
    print(f"Successful:       {stats.successful}")
    print(f"Failed:           {stats.failed}")
    print(f"Skipped:          {stats.skipped}")
    print(f"{'='*60}")
    print(f"Total chapters:   {stats.total_chapters}")
    print(f"Total cross-refs: {stats.total_cross_refs}")
    print(f"Total time:       {stats.total_time_ms/1000:.1f}s")
    if stats.successful > 0:
        print(f"Avg time/book:    {stats.total_time_ms/stats.successful:.0f}ms")
        print(f"Avg refs/book:    {stats.total_cross_refs/stats.successful:.1f}")
    print(f"{'='*60}")
    
    if stats.errors:
        print(f"\nFailed files ({len(stats.errors)}):")
        for error in stats.errors[:10]:  # Show first 10 errors
            print(f"  - {error[:80]}")
        if len(stats.errors) > 10:
            print(f"  ... and {len(stats.errors) - 10} more")


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Batch process metadata files through MSEP enrichment"
    )
    parser.add_argument(
        "--limit", type=int, default=None,
        help="Limit number of files to process (for testing)"
    )
    parser.add_argument(
        "--file", type=str, default=None,
        help="Process a single specific file"
    )
    parser.add_argument(
        "--skip-existing", action="store_true",
        help="Skip files that already have enriched output"
    )
    args = parser.parse_args()
    
    # Get input files
    if args.file:
        input_files = [INPUT_DIR / args.file]
        if not input_files[0].exists():
            print(f"❌ File not found: {input_files[0]}")
            sys.exit(1)
    else:
        input_files = sorted(INPUT_DIR.glob("*_metadata.json"))
    
    if not input_files:
        print("❌ No metadata files found")
        sys.exit(1)
    
    # Skip existing if requested
    if args.skip_existing:
        original_count = len(input_files)
        input_files = [
            f for f in input_files
            if not (OUTPUT_DIR / (f.stem.replace("_metadata", "") + "_enriched.json")).exists()
        ]
        skipped = original_count - len(input_files)
        if skipped > 0:
            print(f"ℹ️  Skipping {skipped} files with existing enriched output")
    
    # Apply limit
    if args.limit:
        input_files = input_files[:args.limit]
    
    # Run batch processing
    stats = asyncio.run(process_batch(input_files, OUTPUT_DIR))
    
    # Print summary
    print_summary(stats)
    
    # Exit with error code if any failures
    sys.exit(1 if stats.failed > 0 else 0)


if __name__ == "__main__":
    main()
