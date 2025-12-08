#!/usr/bin/env python3
"""
Validation Script for Keyword Deduplication Enhancement

This script orchestrates the validation workflow for the deduplication changes:
1. Archive current outputs (pre-change)
2. Run full pipeline with new code
3. Run validation scripts
4. Compare pre vs post outputs
5. Generate diff reports

Usage:
    python scripts/validate_deduplication_changes.py

Document References:
- DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN: Validation workflow
- ARCHITECTURE_GUIDELINES Ch. 4: Script organization
"""

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
ARCHIVE_DIR = OUTPUTS_DIR / "archive"
ENRICHMENT_OUTPUT = PROJECT_ROOT / "workflows" / "metadata_enrichment" / "output"
GUIDELINE_OUTPUT = PROJECT_ROOT / "workflows" / "base_guideline_generation" / "output"
BASELINES_DIR = PROJECT_ROOT / "tests" / "baselines"

# Test book for validation
TEST_BOOK = "AI Engineering Building Applications"


def log(message: str, level: str = "INFO") -> None:
    """Log message with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")


def run_command(cmd: List[str], cwd: Optional[Path] = None) -> subprocess.CompletedProcess:
    """Run a command and return result."""
    log(f"Running: {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        cwd=cwd or PROJECT_ROOT,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        log(f"Command failed: {result.stderr}", "ERROR")
    return result


def create_archive_dir(suffix: str) -> Path:
    """Create timestamped archive directory."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    archive_path = ARCHIVE_DIR / f"{timestamp}_{suffix}"
    archive_path.mkdir(parents=True, exist_ok=True)
    log(f"Created archive directory: {archive_path}")
    return archive_path


def archive_current_outputs(archive_path: Path) -> Dict[str, bool]:
    """Archive current output files."""
    log("Archiving current outputs...")
    results = {}
    
    # Archive enrichment outputs
    if ENRICHMENT_OUTPUT.exists():
        for file in ENRICHMENT_OUTPUT.glob("*.json"):
            dest = archive_path / "enrichment" / file.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, dest)
            results[f"enrichment/{file.name}"] = True
            log(f"  Archived: {file.name}")
    
    # Archive guideline outputs
    if GUIDELINE_OUTPUT.exists():
        for file in GUIDELINE_OUTPUT.glob("*"):
            if file.is_file():
                dest = archive_path / "guideline" / file.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file, dest)
                results[f"guideline/{file.name}"] = True
                log(f"  Archived: {file.name}")
    
    return results


def run_enrichment_pipeline() -> bool:
    """Run the enrichment pipeline with validation."""
    log("Running enrichment pipeline...")
    
    script_path = PROJECT_ROOT / "scripts" / "run_enrichment_with_validation.py"
    if not script_path.exists():
        log(f"Script not found: {script_path}", "ERROR")
        return False
    
    result = run_command([
        sys.executable,
        str(script_path),
        "--book",
        TEST_BOOK
    ])
    
    if result.returncode == 0:
        log("Enrichment pipeline completed successfully")
        return True
    else:
        log(f"Enrichment pipeline failed: {result.stderr}", "ERROR")
        return False


def load_json_file(path: Path) -> Optional[Dict[str, Any]]:
    """Load JSON file safely."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        log(f"Failed to load {path}: {e}", "ERROR")
        return None


def compare_keyword_counts(pre_data: Dict, post_data: Dict) -> Dict[str, Any]:
    """Compare keyword counts between pre and post."""
    results = {
        "pre_total_keywords": 0,
        "post_total_keywords": 0,
        "pre_unique_stems": set(),
        "post_unique_stems": set(),
        "chapters_compared": 0
    }
    
    pre_chapters = pre_data.get("chapters", [])
    post_chapters = post_data.get("chapters", [])
    
    for chapter in pre_chapters:
        keywords = chapter.get("keywords", [])
        results["pre_total_keywords"] += len(keywords)
        for kw in keywords:
            # Simple stem: lowercase, remove trailing s
            stem = kw.lower().rstrip('s')
            results["pre_unique_stems"].add(stem)
    
    for chapter in post_chapters:
        keywords = chapter.get("keywords", [])
        results["post_total_keywords"] += len(keywords)
        for kw in keywords:
            stem = kw.lower().rstrip('s')
            results["post_unique_stems"].add(stem)
    
    results["chapters_compared"] = min(len(pre_chapters), len(post_chapters))
    results["pre_unique_stems"] = len(results["pre_unique_stems"])
    results["post_unique_stems"] = len(results["post_unique_stems"])
    
    return results


def compare_outputs(pre_path: Path, post_path: Path) -> Dict[str, Any]:
    """Compare pre and post enrichment outputs."""
    log("Comparing pre vs post outputs...")
    
    comparison = {
        "files_compared": [],
        "keyword_analysis": {},
        "structural_changes": []
    }
    
    # Find matching files
    pre_files = list(pre_path.glob("enrichment/*.json"))
    
    for pre_file in pre_files:
        post_file = post_path / "enrichment" / pre_file.name
        
        if not post_file.exists():
            comparison["structural_changes"].append(f"Missing post file: {pre_file.name}")
            continue
        
        pre_data = load_json_file(pre_file)
        post_data = load_json_file(post_file)
        
        if pre_data and post_data:
            comparison["files_compared"].append(pre_file.name)
            comparison["keyword_analysis"][pre_file.name] = compare_keyword_counts(
                pre_data, post_data
            )
    
    return comparison


def check_for_duplicates(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Check for duplicate keywords/concepts in enriched data."""
    duplicates = []
    
    for chapter in data.get("chapters", []):
        chapter_title = chapter.get("title", "Unknown")
        
        # Check keywords
        keywords = [kw.lower() for kw in chapter.get("keywords", [])]
        keyword_stems = {}
        for kw in keywords:
            stem = kw.rstrip('s').rstrip('ing').rstrip('ed')
            if stem in keyword_stems:
                duplicates.append({
                    "chapter": chapter_title,
                    "type": "keyword",
                    "original": keyword_stems[stem],
                    "duplicate": kw
                })
            else:
                keyword_stems[stem] = kw
        
        # Check concepts
        concepts = [c.lower() for c in chapter.get("concepts", [])]
        concept_stems = {}
        for c in concepts:
            stem = c.rstrip('s').rstrip('ing').rstrip('ed')
            if stem in concept_stems:
                duplicates.append({
                    "chapter": chapter_title,
                    "type": "concept",
                    "original": concept_stems[stem],
                    "duplicate": c
                })
            else:
                concept_stems[stem] = c
    
    return duplicates


def generate_report(
    pre_archive: Path,
    post_archive: Path,
    comparison: Dict[str, Any],
    duplicates: List[Dict[str, Any]]
) -> str:
    """Generate validation report."""
    
    report_lines = [
        "=" * 60,
        "KEYWORD DEDUPLICATION VALIDATION REPORT",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 60,
        "",
        "## Archive Locations",
        f"Pre-change:  {pre_archive}",
        f"Post-change: {post_archive}",
        "",
        "## Files Compared",
    ]
    
    for filename in comparison.get("files_compared", []):
        report_lines.append(f"  - {filename}")
    
    report_lines.extend(["", "## Keyword Analysis"])
    
    for filename, analysis in comparison.get("keyword_analysis", {}).items():
        report_lines.extend([
            "",
            f"### {filename}",
            f"  Pre-change total keywords:  {analysis.get('pre_total_keywords', 0)}",
            f"  Post-change total keywords: {analysis.get('post_total_keywords', 0)}",
            f"  Pre-change unique stems:    {analysis.get('pre_unique_stems', 0)}",
            f"  Post-change unique stems:   {analysis.get('post_unique_stems', 0)}",
            f"  Chapters compared:          {analysis.get('chapters_compared', 0)}",
        ])
    
    report_lines.extend(["", "## Duplicate Check (Post-Change)"])
    
    if duplicates:
        report_lines.append(f"  Found {len(duplicates)} potential duplicates:")
        for dup in duplicates[:10]:  # Show first 10
            report_lines.append(
                f"    - [{dup['type']}] {dup['chapter']}: "
                f"'{dup['original']}' vs '{dup['duplicate']}'"
            )
        if len(duplicates) > 10:
            report_lines.append(f"    ... and {len(duplicates) - 10} more")
    else:
        report_lines.append("  ✅ No duplicates found!")
    
    report_lines.extend([
        "",
        "## Structural Changes",
    ])
    
    changes = comparison.get("structural_changes", [])
    if changes:
        for change in changes:
            report_lines.append(f"  - {change}")
    else:
        report_lines.append("  No structural changes detected.")
    
    report_lines.extend(["", "=" * 60])
    
    return "\n".join(report_lines)


def main() -> int:
    """Main validation workflow."""
    log("Starting validation workflow for keyword deduplication")
    log(f"Project root: {PROJECT_ROOT}")
    
    # Step 1: Archive pre-change outputs
    log("=" * 50)
    log("STEP 1: Archive pre-change outputs")
    pre_archive = create_archive_dir("pre-change")
    archive_current_outputs(pre_archive)
    
    # Step 2: Run enrichment pipeline
    log("=" * 50)
    log("STEP 2: Run enrichment pipeline with new code")
    pipeline_success = run_enrichment_pipeline()
    
    if not pipeline_success:
        log("Pipeline failed, continuing with available outputs", "WARN")
    
    # Step 3: Archive post-change outputs
    log("=" * 50)
    log("STEP 3: Archive post-change outputs")
    post_archive = create_archive_dir("post-change")
    archive_current_outputs(post_archive)
    
    # Step 4: Compare outputs
    log("=" * 50)
    log("STEP 4: Compare pre vs post outputs")
    comparison = compare_outputs(pre_archive, post_archive)
    
    # Step 5: Check for duplicates in post-change
    log("=" * 50)
    log("STEP 5: Check for duplicates in post-change output")
    
    post_enrichment = post_archive / "enrichment"
    all_duplicates = []
    
    for json_file in post_enrichment.glob("*.json"):
        data = load_json_file(json_file)
        if data:
            duplicates = check_for_duplicates(data)
            all_duplicates.extend(duplicates)
    
    if all_duplicates:
        log(f"Found {len(all_duplicates)} potential duplicates", "WARN")
    else:
        log("No duplicates found - deduplication working!")
    
    # Step 6: Generate report
    log("=" * 50)
    log("STEP 6: Generate validation report")
    report = generate_report(pre_archive, post_archive, comparison, all_duplicates)
    
    # Save report
    report_path = post_archive / "validation_report.txt"
    with open(report_path, 'w') as f:
        f.write(report)
    log(f"Report saved to: {report_path}")
    
    # Print report
    print("\n" + report)
    
    # Summary
    log("=" * 50)
    log("VALIDATION COMPLETE")
    log(f"Pre-change archive:  {pre_archive}")
    log(f"Post-change archive: {post_archive}")
    log(f"Report: {report_path}")
    
    return 0 if not all_duplicates else 1


if __name__ == "__main__":
    sys.exit(main())
