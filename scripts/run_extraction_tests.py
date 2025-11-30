#!/usr/bin/env python3
"""
Extraction Profile Test Runner
==============================

Runs extraction tests with different parameter profiles and collects
results for LLM evaluation.

Usage:
    python run_extraction_tests.py --profile baseline
    python run_extraction_tests.py --profile current
    python run_extraction_tests.py --profile all
    python run_extraction_tests.py --compare baseline current
"""

import argparse
import json
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def load_profiles() -> dict[str, Any]:
    """Load extraction profiles from JSON config."""
    config_path = PROJECT_ROOT / "config" / "extraction_profiles.json"
    
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path) as f:
        return json.load(f)


def get_profile(name: str) -> dict[str, Any]:
    """Get a specific profile by name."""
    config = load_profiles()
    profiles = config.get("profiles", {})
    
    if name not in profiles:
        available = list(profiles.keys())
        raise ValueError(f"Profile '{name}' not found. Available: {available}")
    
    return profiles[name]


def apply_profile_to_extractor(profile: dict[str, Any]) -> None:
    """
    Apply profile parameters to the statistical extractor.
    
    This modifies the extractor's behavior for the current run.
    """
    params = profile.get("parameters", {})
    
    # For now, we'll set environment variables that the extractor can read
    # This is a non-invasive way to configure without code changes
    
    yake_params = params.get("yake", {})
    os.environ["EXTRACTION_YAKE_TOP_N"] = str(yake_params.get("top_n", 20))
    os.environ["EXTRACTION_YAKE_N"] = str(yake_params.get("n", 3))
    os.environ["EXTRACTION_YAKE_DEDUPLIM"] = str(yake_params.get("dedupLim", 0.9))
    
    summa_params = params.get("summa", {})
    os.environ["EXTRACTION_SUMMA_CONCEPTS_TOP_N"] = str(summa_params.get("concepts_top_n", 10))
    
    dedup_params = params.get("custom_dedup", {})
    os.environ["EXTRACTION_STEM_DEDUP_ENABLED"] = str(dedup_params.get("stem_dedup_enabled", True)).lower()
    os.environ["EXTRACTION_NGRAM_CLEAN_ENABLED"] = str(dedup_params.get("ngram_clean_enabled", True)).lower()
    
    tfidf_params = params.get("tfidf", {})
    os.environ["EXTRACTION_TFIDF_MAX_FEATURES"] = str(tfidf_params.get("max_features", 1000))
    
    chapters_params = params.get("related_chapters", {})
    os.environ["EXTRACTION_CHAPTERS_THRESHOLD"] = str(chapters_params.get("threshold", 0.7))
    os.environ["EXTRACTION_CHAPTERS_TOP_N"] = str(chapters_params.get("top_n", 5))
    
    print(f"\n✅ Applied profile: {profile.get('name', 'Unknown')}")
    print(f"   Description: {profile.get('description', 'N/A')}")


def run_extraction_for_profile(profile_name: str) -> Path:
    """
    Run the full extraction pipeline for a given profile.
    
    Returns the path to the output directory.
    """
    profile = get_profile(profile_name)
    apply_profile_to_extractor(profile)
    
    # Create timestamped output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = PROJECT_ROOT / "outputs" / f"extraction_test_{profile_name}_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save profile used
    profile_record = {
        "profile_name": profile_name,
        "profile_data": profile,
        "timestamp": timestamp,
        "test_run": True
    }
    with open(output_dir / "profile_used.json", "w") as f:
        json.dump(profile_record, f, indent=2)
    
    print(f"\n🔄 Running extraction with profile: {profile_name}")
    print(f"   Output directory: {output_dir}")
    
    # Import and run the enrichment workflow
    try:
        from workflows.metadata_enrichment.scripts.run_metadata_enrichment import MetadataEnricher
        
        # Find the test book metadata
        metadata_dir = PROJECT_ROOT / "data" / "metadata"
        json_files = list(metadata_dir.glob("*.json"))
        
        if not json_files:
            print("⚠️  No JSON metadata files found in data/metadata/")
            return output_dir
        
        # Use the first (most recent) JSON file
        metadata_file = max(json_files, key=lambda p: p.stat().st_mtime)
        print(f"   Using metadata: {metadata_file.name}")
        
        # Run enrichment
        enricher = MetadataEnricher()
        enricher.enrich_metadata(str(metadata_file), str(output_dir))
        
        print(f"✅ Extraction complete: {output_dir}")
        
    except ImportError as e:
        print(f"⚠️  Could not import enrichment workflow: {e}")
        print("   Creating mock output for demonstration...")
        
        # Create mock output
        mock_data = {
            "profile": profile_name,
            "keywords_extracted": [],
            "note": "Mock output - actual enricher not available"
        }
        with open(output_dir / "mock_output.json", "w") as f:
            json.dump(mock_data, f, indent=2)
    
    return output_dir


def compare_outputs(profile1: str, profile2: str) -> dict[str, Any]:
    """
    Compare extraction outputs between two profiles.
    
    Returns comparison statistics.
    """
    # Find most recent outputs for each profile
    outputs_dir = PROJECT_ROOT / "outputs"
    
    def find_latest_output(profile: str) -> Path | None:
        pattern = f"extraction_test_{profile}_*"
        matches = list(outputs_dir.glob(pattern))
        if matches:
            return max(matches, key=lambda p: p.stat().st_mtime)
        return None
    
    out1 = find_latest_output(profile1)
    out2 = find_latest_output(profile2)
    
    if not out1 or not out2:
        missing = []
        if not out1:
            missing.append(profile1)
        if not out2:
            missing.append(profile2)
        print(f"⚠️  Missing outputs for: {missing}")
        print("   Run extractions first with --profile")
        return {}
    
    print(f"\n📊 Comparing outputs:")
    print(f"   Profile 1: {profile1} -> {out1.name}")
    print(f"   Profile 2: {profile2} -> {out2.name}")
    
    # Load and compare (simplified for now)
    comparison = {
        "profile1": profile1,
        "profile2": profile2,
        "output1_dir": str(out1),
        "output2_dir": str(out2),
        "comparison_date": datetime.now().isoformat()
    }
    
    # Save comparison
    comparison_file = outputs_dir / f"comparison_{profile1}_vs_{profile2}.json"
    with open(comparison_file, "w") as f:
        json.dump(comparison, f, indent=2)
    
    print(f"✅ Comparison saved: {comparison_file}")
    
    return comparison


def list_profiles() -> None:
    """List all available profiles."""
    config = load_profiles()
    profiles = config.get("profiles", {})
    
    print("\n📋 Available Extraction Profiles:")
    print("=" * 60)
    
    for name, data in profiles.items():
        enabled = "✅" if data.get("enabled", True) else "❌"
        print(f"\n  {enabled} {name}")
        print(f"     Name: {data.get('name', 'N/A')}")
        print(f"     Description: {data.get('description', 'N/A')}")
        
        params = data.get("parameters", {})
        yake = params.get("yake", {})
        dedup = params.get("custom_dedup", {})
        
        print(f"     YAKE top_n: {yake.get('top_n', 'N/A')}")
        print(f"     Stem Dedup: {'ON' if dedup.get('stem_dedup_enabled') else 'OFF'}")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run extraction tests with different parameter profiles"
    )
    
    parser.add_argument(
        "--profile",
        choices=["baseline", "current", "moderate", "aggressive", "all"],
        help="Profile to run extraction with"
    )
    
    parser.add_argument(
        "--compare",
        nargs=2,
        metavar=("PROFILE1", "PROFILE2"),
        help="Compare outputs between two profiles"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available profiles"
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_profiles()
        return
    
    if args.compare:
        compare_outputs(args.compare[0], args.compare[1])
        return
    
    if args.profile:
        if args.profile == "all":
            profiles = ["baseline", "current", "moderate", "aggressive"]
            for p in profiles:
                run_extraction_for_profile(p)
        else:
            run_extraction_for_profile(args.profile)
        return
    
    # Default: show help
    parser.print_help()


if __name__ == "__main__":
    main()
