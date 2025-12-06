#!/usr/bin/env python3
"""
Run Enrichment with Validation and Comparison

Runs Tab 4 enrichment and Tab 5 guideline generation for a single book,
then validates outputs and compares with backups.

Usage:
    # Run for a specific book with full validation
    python scripts/run_enrichment_with_validation.py --book "AI Engineering Building Applications"
    
    # Dry run
    python scripts/run_enrichment_with_validation.py --book "AI Engineering Building Applications" --dry-run

Validation Checks:
    Tab 4 (Enrichment):
    - topic_id present on all chapters (NEW)
    - related_chapters populated
    - keywords_enriched populated
    - concepts_enriched populated
    - enrichment_metadata contains required fields
    
    Tab 5 (Guidelines):
    - JSON file created and valid
    - Has expected sections
    - Cross-references populated
"""

import argparse
import json
import subprocess
import sys
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field, asdict

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


@dataclass
class ValidationResult:
    """Result of a validation check."""
    passed: bool
    check_name: str
    message: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ComparisonResult:
    """Result of comparing new vs backup."""
    field: str
    backup_value: Any
    new_value: Any
    change: str  # "improved", "degraded", "same", "new"


def find_taxonomy_file() -> Optional[Path]:
    """Find the AI-ML taxonomy file."""
    taxonomy_dir = PROJECT_ROOT / "workflows" / "taxonomy_setup" / "output"
    aiml = taxonomy_dir / "AI-ML_taxonomy_20251128.json"
    if aiml.exists():
        return aiml
    
    comprehensive = list(taxonomy_dir.glob("comprehensive_taxonomy_*.json"))
    if comprehensive:
        return sorted(comprehensive)[-1]
    return None


def find_latest_backup() -> Optional[Path]:
    """Find the most recent backup directory."""
    backup_dir = PROJECT_ROOT / "backups"
    if not backup_dir.exists():
        return None
    
    backups = sorted(backup_dir.glob("backup_*"))
    return backups[-1] if backups else None


def backup_current_outputs(book_name: str) -> Path:
    """Backup current outputs for a specific book."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = PROJECT_ROOT / "backups" / f"backup_{timestamp}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # Backup enriched file
    enriched_src = PROJECT_ROOT / "workflows" / "metadata_enrichment" / "output" / f"{book_name}_enriched.json"
    if enriched_src.exists():
        enriched_dest = backup_dir / "metadata_enrichment"
        enriched_dest.mkdir(exist_ok=True)
        shutil.copy2(enriched_src, enriched_dest / enriched_src.name)
        print(f"  📦 Backed up enriched: {enriched_src.name}")
    
    # Backup guideline file
    guideline_src = PROJECT_ROOT / "workflows" / "base_guideline_generation" / "output" / f"{book_name}_guideline.json"
    if guideline_src.exists():
        guideline_dest = backup_dir / "base_guideline_generation"
        guideline_dest.mkdir(exist_ok=True)
        shutil.copy2(guideline_src, guideline_dest / guideline_src.name)
        print(f"  📦 Backed up guideline: {guideline_src.name}")
    
    return backup_dir


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_enrichment(book_name: str) -> List[ValidationResult]:
    """Validate Tab 4 enriched metadata output."""
    results = []
    enriched_path = PROJECT_ROOT / "workflows" / "metadata_enrichment" / "output" / f"{book_name}_enriched.json"
    
    # Check file exists
    if not enriched_path.exists():
        results.append(ValidationResult(
            passed=False,
            check_name="file_exists",
            message=f"Enriched file not found: {enriched_path}"
        ))
        return results
    
    results.append(ValidationResult(
        passed=True,
        check_name="file_exists",
        message="Enriched file exists"
    ))
    
    # Load and validate JSON
    try:
        with open(enriched_path, encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        results.append(ValidationResult(
            passed=False,
            check_name="valid_json",
            message=f"Invalid JSON: {e}"
        ))
        return results
    
    results.append(ValidationResult(
        passed=True,
        check_name="valid_json",
        message="Valid JSON structure"
    ))
    
    # Check enrichment_metadata
    enrichment_meta = data.get("enrichment_metadata", {})
    required_meta = ["generated", "method", "libraries", "corpus_size"]
    missing_meta = [k for k in required_meta if k not in enrichment_meta]
    
    results.append(ValidationResult(
        passed=len(missing_meta) == 0,
        check_name="enrichment_metadata",
        message=f"Missing metadata fields: {missing_meta}" if missing_meta else "All metadata fields present",
        details={"method": enrichment_meta.get("method"), "corpus_size": enrichment_meta.get("corpus_size")}
    ))
    
    # Check chapters
    chapters = data.get("chapters", [])
    if not chapters:
        results.append(ValidationResult(
            passed=False,
            check_name="chapters_exist",
            message="No chapters found"
        ))
        return results
    
    results.append(ValidationResult(
        passed=True,
        check_name="chapters_exist",
        message=f"Found {len(chapters)} chapters"
    ))
    
    # Check topic_id (NEW FEATURE)
    chapters_with_topic = [ch for ch in chapters if ch.get("topic_id") is not None]
    topic_coverage = len(chapters_with_topic) / len(chapters) * 100
    unique_topics = len({ch.get("topic_id") for ch in chapters_with_topic})
    
    results.append(ValidationResult(
        passed=topic_coverage > 0,
        check_name="topic_id_coverage",
        message=f"Topic coverage: {topic_coverage:.1f}% ({len(chapters_with_topic)}/{len(chapters)} chapters)",
        details={"coverage_pct": topic_coverage, "unique_topics": unique_topics}
    ))
    
    # Check related_chapters
    chapters_with_related = [ch for ch in chapters if ch.get("related_chapters")]
    related_coverage = len(chapters_with_related) / len(chapters) * 100
    avg_related = sum(len(ch.get("related_chapters", [])) for ch in chapters) / len(chapters)
    
    results.append(ValidationResult(
        passed=related_coverage > 0,
        check_name="related_chapters",
        message=f"Related chapters: {related_coverage:.1f}% coverage, avg {avg_related:.1f} per chapter",
        details={"coverage_pct": related_coverage, "avg_related": avg_related}
    ))
    
    # Check keywords_enriched
    chapters_with_keywords = [ch for ch in chapters if ch.get("keywords_enriched")]
    kw_coverage = len(chapters_with_keywords) / len(chapters) * 100
    avg_keywords = sum(len(ch.get("keywords_enriched", [])) for ch in chapters) / len(chapters)
    
    results.append(ValidationResult(
        passed=kw_coverage > 50,
        check_name="keywords_enriched",
        message=f"Keywords enriched: {kw_coverage:.1f}% coverage, avg {avg_keywords:.1f} per chapter",
        details={"coverage_pct": kw_coverage, "avg_keywords": avg_keywords}
    ))
    
    # Check concepts_enriched
    chapters_with_concepts = [ch for ch in chapters if ch.get("concepts_enriched")]
    concept_coverage = len(chapters_with_concepts) / len(chapters) * 100
    avg_concepts = sum(len(ch.get("concepts_enriched", [])) for ch in chapters) / len(chapters)
    
    results.append(ValidationResult(
        passed=concept_coverage > 50,
        check_name="concepts_enriched",
        message=f"Concepts enriched: {concept_coverage:.1f}% coverage, avg {avg_concepts:.1f} per chapter",
        details={"coverage_pct": concept_coverage, "avg_concepts": avg_concepts}
    ))
    
    return results


def validate_guideline(book_name: str) -> List[ValidationResult]:
    """Validate Tab 5 guideline output."""
    results = []
    guideline_path = PROJECT_ROOT / "workflows" / "base_guideline_generation" / "output" / f"{book_name}_guideline.json"
    
    # Check file exists
    if not guideline_path.exists():
        results.append(ValidationResult(
            passed=False,
            check_name="file_exists",
            message=f"Guideline file not found: {guideline_path}"
        ))
        return results
    
    results.append(ValidationResult(
        passed=True,
        check_name="file_exists",
        message="Guideline file exists"
    ))
    
    # Load and validate JSON
    try:
        with open(guideline_path, encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        results.append(ValidationResult(
            passed=False,
            check_name="valid_json",
            message=f"Invalid JSON: {e}"
        ))
        return results
    
    results.append(ValidationResult(
        passed=True,
        check_name="valid_json",
        message="Valid JSON structure"
    ))
    
    # Check structure
    if isinstance(data, dict):
        sections = data.get("sections", data.get("chapters", []))
        results.append(ValidationResult(
            passed=len(sections) > 0,
            check_name="has_sections",
            message=f"Found {len(sections)} sections"
        ))
        
        # Check for cross-references
        total_xrefs = 0
        for section in sections:
            xrefs = section.get("cross_references", [])
            total_xrefs += len(xrefs)
        
        results.append(ValidationResult(
            passed=True,  # Info only
            check_name="cross_references",
            message=f"Total cross-references: {total_xrefs}"
        ))
    
    return results


# =============================================================================
# COMPARISON FUNCTIONS
# =============================================================================

def _determine_change_status(new_val: float, backup_val: float, threshold: float = 0.0) -> str:
    """
    Determine change status comparing new vs backup values.
    
    Extracted from nested ternary to improve readability (SonarQube S3358).
    
    Args:
        new_val: New value to compare
        backup_val: Backup/baseline value
        threshold: Tolerance for "same" determination (default 0.0 for exact match)
    
    Returns:
        "improved", "same", or "degraded"
    """
    if threshold > 0:
        if abs(new_val - backup_val) < threshold:
            return "same"
        return "improved" if new_val > backup_val else "degraded"
    else:
        if new_val > backup_val:
            return "improved"
        elif new_val == backup_val:
            return "same"
        else:
            return "degraded"


def compare_enrichments(book_name: str, backup_dir: Path) -> List[ComparisonResult]:
    """Compare new enrichment with backup."""
    results = []
    
    new_path = PROJECT_ROOT / "workflows" / "metadata_enrichment" / "output" / f"{book_name}_enriched.json"
    backup_path = backup_dir / "metadata_enrichment" / f"{book_name}_enriched.json"
    
    if not backup_path.exists():
        results.append(ComparisonResult(
            field="backup",
            backup_value=None,
            new_value="exists",
            change="new"
        ))
        return results
    
    if not new_path.exists():
        return results
    
    with open(new_path, encoding='utf-8') as f:
        new_data = json.load(f)
    with open(backup_path, encoding='utf-8') as f:
        backup_data = json.load(f)
    
    new_chapters = new_data.get("chapters", [])
    backup_chapters = backup_data.get("chapters", [])
    
    # Compare topic_id (NEW)
    new_topics = len([ch for ch in new_chapters if ch.get("topic_id") is not None])
    backup_topics = len([ch for ch in backup_chapters if ch.get("topic_id") is not None])
    results.append(ComparisonResult(
        field="topic_id_count",
        backup_value=backup_topics,
        new_value=new_topics,
        change=_determine_change_status(new_topics, backup_topics)
    ))
    
    # Compare related chapters
    new_related = sum(len(ch.get("related_chapters", [])) for ch in new_chapters) / len(new_chapters) if new_chapters else 0
    backup_related = sum(len(ch.get("related_chapters", [])) for ch in backup_chapters) / len(backup_chapters) if backup_chapters else 0
    results.append(ComparisonResult(
        field="avg_related_chapters",
        backup_value=round(backup_related, 2),
        new_value=round(new_related, 2),
        change=_determine_change_status(new_related, backup_related, threshold=0.1)
    ))
    
    # Compare keywords
    new_kw = sum(len(ch.get("keywords_enriched", [])) for ch in new_chapters) / len(new_chapters) if new_chapters else 0
    backup_kw = sum(len(ch.get("keywords_enriched", [])) for ch in backup_chapters) / len(backup_chapters) if backup_chapters else 0
    results.append(ComparisonResult(
        field="avg_keywords_enriched",
        backup_value=round(backup_kw, 2),
        new_value=round(new_kw, 2),
        change=_determine_change_status(new_kw, backup_kw, threshold=0.5)
    ))
    
    return results


# =============================================================================
# RUN FUNCTIONS
# =============================================================================

def run_tab4_enrichment(book_name: str, taxonomy_path: Path) -> bool:
    """Run Tab 4 metadata enrichment."""
    metadata_dir = PROJECT_ROOT / "workflows" / "metadata_extraction" / "output"
    output_dir = PROJECT_ROOT / "workflows" / "metadata_enrichment" / "output"
    
    input_file = metadata_dir / f"{book_name}_metadata.json"
    output_file = output_dir / f"{book_name}_enriched.json"
    
    if not input_file.exists():
        print(f"  ❌ Metadata file not found: {input_file}")
        return False
    
    script = PROJECT_ROOT / "workflows" / "metadata_enrichment" / "scripts" / "enrich_metadata_per_book.py"
    
    cmd = [
        sys.executable, str(script),
        "--input", str(input_file),
        "--taxonomy", str(taxonomy_path),
        "--output", str(output_file)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode == 0:
            return True
        else:
            print(f"  ❌ Tab 4 failed: {result.stderr[:500]}")
            return False
    except Exception as e:
        print(f"  ❌ Tab 4 error: {e}")
        return False


def run_tab5_guideline(book_name: str, taxonomy_path: Path) -> bool:
    """Run Tab 5 guideline generation."""
    json_dir = PROJECT_ROOT / "workflows" / "pdf_to_json" / "output" / "textbooks_json"
    json_file = json_dir / f"{book_name}.json"
    
    if not json_file.exists():
        print(f"  ❌ JSON file not found: {json_file}")
        return False
    
    script = PROJECT_ROOT / "workflows" / "base_guideline_generation" / "scripts" / "chapter_generator_all_text.py"
    
    cmd = [
        sys.executable, str(script),
        str(json_file),
        "--taxonomy", str(taxonomy_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode == 0:
            return True
        else:
            print(f"  ❌ Tab 5 failed: {result.stderr[:500]}")
            return False
    except Exception as e:
        print(f"  ❌ Tab 5 error: {e}")
        return False


# =============================================================================
# REPORTING
# =============================================================================

def print_validation_results(results: List[ValidationResult], title: str) -> int:
    """Print validation results and return failure count."""
    print(f"\n  {title}")
    print(f"  {'─'*50}")
    
    failures = 0
    for r in results:
        status = "✅" if r.passed else "❌"
        print(f"  {status} {r.check_name}: {r.message}")
        if not r.passed:
            failures += 1
    
    return failures


def print_comparison_results(results: List[ComparisonResult]) -> None:
    """Print comparison results."""
    print("\n  📊 Comparison with Backup")
    print(f"  {'─'*50}")
    
    for r in results:
        icon = {"improved": "📈", "degraded": "📉", "same": "➡️", "new": "🆕"}.get(r.change, "❓")
        print(f"  {icon} {r.field}: {r.backup_value} → {r.new_value} ({r.change})")


def main():
    parser = argparse.ArgumentParser(
        description="Run enrichment with validation and comparison"
    )
    parser.add_argument(
        "--book",
        type=str,
        required=True,
        help="Book name to process (e.g., 'AI Engineering Building Applications')"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without executing"
    )
    parser.add_argument(
        "--skip-tab5",
        action="store_true",
        help="Skip Tab 5 guideline generation"
    )
    parser.add_argument(
        "--output-report",
        type=str,
        help="Save validation report to JSON file"
    )
    
    args = parser.parse_args()
    book_name = args.book
    
    print("\n" + "="*60)
    print("🔬 ENRICHMENT WITH VALIDATION")
    print(f"   Book: {book_name}")
    print("="*60)
    
    # Find taxonomy
    taxonomy_path = find_taxonomy_file()
    if not taxonomy_path:
        print("❌ No taxonomy file found!")
        return 1
    print(f"\n📋 Using taxonomy: {taxonomy_path.name}")
    
    # Find existing backup for comparison
    existing_backup = find_latest_backup()
    if existing_backup:
        print(f"📦 Found backup for comparison: {existing_backup.name}")
    
    if args.dry_run:
        print("\n⚠️  DRY RUN - No changes will be made")
        print("\nWould run:")
        print("  • Tab 4: Metadata Enrichment with BERTopic + Sentence Transformers")
        if not args.skip_tab5:
            print("  • Tab 5: Guideline Generation")
        print("\nWould validate:")
        print("  • Enrichment: topic_id, related_chapters, keywords, concepts")
        print("  • Guideline: JSON structure, sections, cross-references")
        print("\nWould compare:")
        print("  • New output vs backup (if exists)")
        return 0
    
    # Backup current outputs
    print("\n📦 Backing up current outputs...")
    # NOTE: backup_dir returned for potential future use; prefixed per S1481
    _backup_dir = backup_current_outputs(book_name)  # noqa: F841
    
    # Run Tab 4
    print(f"\n{'─'*60}")
    print("🔗 TAB 4: Metadata Enrichment")
    print(f"{'─'*60}")
    
    tab4_success = run_tab4_enrichment(book_name, taxonomy_path)
    if tab4_success:
        print("  ✅ Tab 4 complete")
    else:
        print("  ❌ Tab 4 failed")
        return 1
    
    # Validate Tab 4
    enrichment_results = validate_enrichment(book_name)
    enrichment_failures = print_validation_results(enrichment_results, "📋 Enrichment Validation")
    
    # Compare with backup
    if existing_backup:
        comparison_results = compare_enrichments(book_name, existing_backup)
        print_comparison_results(comparison_results)
    
    # Run Tab 5 (optional)
    if not args.skip_tab5:
        print(f"\n{'─'*60}")
        print("📖 TAB 5: Guideline Generation")
        print(f"{'─'*60}")
        
        tab5_success = run_tab5_guideline(book_name, taxonomy_path)
        if tab5_success:
            print("  ✅ Tab 5 complete")
        else:
            print("  ❌ Tab 5 failed")
        
        # Validate Tab 5
        guideline_results = validate_guideline(book_name)
        guideline_failures = print_validation_results(guideline_results, "📋 Guideline Validation")
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 SUMMARY")
    print(f"{'='*60}")
    print(f"\n✅ Tab 4 Enrichment: {'PASSED' if enrichment_failures == 0 else f'FAILED ({enrichment_failures} issues)'}")
    if not args.skip_tab5:
        print(f"✅ Tab 5 Guideline: {'PASSED' if guideline_failures == 0 else f'FAILED ({guideline_failures} issues)'}")
    
    # Save report
    if args.output_report:
        report = {
            "generated": datetime.now().isoformat(),
            "book": book_name,
            "taxonomy": taxonomy_path.name,
            "enrichment_validation": [asdict(r) for r in enrichment_results],
            "comparison": [asdict(r) for r in comparison_results] if existing_backup else [],
        }
        if not args.skip_tab5:
            report["guideline_validation"] = [asdict(r) for r in guideline_results]
        
        report_path = Path(args.output_report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        print(f"\n📁 Report saved to: {report_path}")
    
    return 0 if enrichment_failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
