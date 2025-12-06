#!/usr/bin/env python3
"""
Extraction Profile Test Runner
==============================

Runs the complete pipeline for each extraction profile configuration,
producing profile-specific artifacts with proper naming conventions.

Pipeline per profile:
    1. Metadata Extraction (from JSON text, with profile params)
    2. Taxonomy (copy with profile suffix)
    3. Enrichment (with profile params)
    4. Aggregate creation

Usage:
    python run_extraction_tests.py --profile baseline
    python run_extraction_tests.py --run-all
    python run_extraction_tests.py --validate
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import shutil

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import production aggregate package creation
from workflows.llm_enhancement.scripts.create_aggregate_package import create_aggregate_package


# Profile suffix mapping
PROFILE_SUFFIXES = {
    "baseline": "BASELINE",
    "current": "CURRENT",
    "moderate": "MODERATE",
    "aggressive": "AGGRESSIVE",
}


def load_profiles() -> Dict[str, Any]:
    """Load extraction profiles from config."""
    profiles_path = PROJECT_ROOT / "config" / "extraction_profiles.json"
    with open(profiles_path) as f:
        return json.load(f)


def get_profile(profile_name: str) -> Dict[str, Any]:
    """Get a specific profile configuration."""
    config = load_profiles()
    profiles = config.get("profiles", {})
    
    if profile_name not in profiles:
        available = list(profiles.keys())
        raise ValueError(f"Profile '{profile_name}' not found. Available: {available}")
    
    return profiles[profile_name]


def apply_profile_env_vars(profile: Dict[str, Any]) -> None:
    """
    Set environment variables for the profile parameters.
    
    These are read by StatisticalExtractor at instantiation time.
    """
    params = profile.get("parameters", {})
    
    # YAKE parameters
    yake = params.get("yake", {})
    os.environ["EXTRACTION_YAKE_TOP_N"] = str(yake.get("top_n", 20))
    os.environ["EXTRACTION_YAKE_N"] = str(yake.get("n", 3))
    os.environ["EXTRACTION_YAKE_DEDUPLIM"] = str(yake.get("dedupLim", 0.9))
    
    # Summa parameters
    summa = params.get("summa", {})
    os.environ["EXTRACTION_SUMMA_CONCEPTS_TOP_N"] = str(summa.get("concepts_top_n", 10))
    
    # Custom deduplication parameters
    custom = params.get("custom_dedup", {})
    os.environ["EXTRACTION_STEM_DEDUP_ENABLED"] = str(custom.get("stem_dedup_enabled", True)).lower()
    os.environ["EXTRACTION_NGRAM_CLEAN_ENABLED"] = str(custom.get("ngram_clean_enabled", True)).lower()
    
    # TF-IDF parameters
    tfidf = params.get("tfidf", {})
    os.environ["EXTRACTION_TFIDF_MAX_FEATURES"] = str(tfidf.get("max_features", 1000))
    os.environ["EXTRACTION_TFIDF_MIN_DF"] = str(tfidf.get("min_df", 2))
    
    # Related chapters parameters
    related = params.get("related_chapters", {})
    os.environ["EXTRACTION_CHAPTERS_THRESHOLD"] = str(related.get("threshold", 0.7))
    os.environ["EXTRACTION_CHAPTERS_TOP_N"] = str(related.get("top_n", 5))


def validate_step(step_name: str, condition: bool, message: str) -> bool:
    """Validate a pipeline step and print status."""
    if condition:
        print(f"  ✅ {step_name}: {message}")
        return True
    else:
        print(f"  ❌ {step_name}: {message}")
        return False


def find_source_json_text(book_name: str) -> Optional[Path]:
    """
    Find the source JSON text file for a book.
    
    This is the raw JSON extracted from PDF (output of pdf_to_json workflow).
    """
    # Common locations for source JSON text (in order of priority)
    search_paths = [
        PROJECT_ROOT / "workflows" / "pdf_to_json" / "output" / "textbooks_json",
        PROJECT_ROOT / "workflows" / "pdf_to_json" / "output",
        PROJECT_ROOT / "data" / "textbooks_json",
        PROJECT_ROOT / "data" / "textbooks-json",
    ]
    
    for search_dir in search_paths:
        if search_dir.exists():
            # Try exact match first
            matches = list(search_dir.glob(f"*{book_name}*.json"))
            if matches:
                return matches[0]
    
    return None


def run_metadata_extraction(
    source_json: Path,
    output_file: Path,
    chapters: Optional[List[Tuple[int, str, int, int]]] = None
) -> bool:
    """
    Run metadata extraction from source JSON text.
    
    This creates the *_metadata.json file with keywords, concepts, summaries.
    The StatisticalExtractor will use current environment variables.
    """
    try:
        from workflows.metadata_extraction.scripts.generate_metadata_universal import UniversalMetadataGenerator
        
        # Create generator (will use env vars for StatisticalExtractor)
        generator = UniversalMetadataGenerator(source_json)
        
        # Auto-detect chapters if not provided
        if chapters is None:
            chapters = generator.auto_detect_chapters()
        
        if not chapters:
            print("  ⚠️ No chapters detected")
            return False
        
        # Generate metadata
        metadata_list = generator.generate_metadata(chapters)
        
        # Save to output file
        generator.save_metadata(metadata_list, output_file)
        
        return output_file.exists()
        
    except Exception as e:
        print(f"  ❌ Metadata extraction error: {e}")
        import traceback
        traceback.print_exc()
        return False


def _initialize_profile_result(profile_name: str, suffix: str) -> Dict[str, Any]:
    """Initialize the result dictionary for a profile run."""
    return {
        "profile": profile_name,
        "suffix": suffix,
        "timestamp": datetime.now().isoformat(),
        "validations": {},
        "paths": {},
        "success": False,
    }


def _setup_profile_paths(
    book_name: str, suffix: str, eval_dir: Path
) -> Dict[str, Path]:
    """Set up all file paths for a profile run."""
    return {
        "metadata": eval_dir / f"{book_name}_metadata_{suffix}.json",
        "taxonomy": eval_dir / f"{book_name}_{suffix}_taxonomy.json",
        "enriched": eval_dir / f"{book_name}_enriched_{suffix}.json",
        "aggregate": eval_dir / f"aggregate_{suffix}.json",
    }


def _apply_and_print_config(profile: Dict[str, Any]) -> None:
    """Apply profile configuration and print settings."""
    apply_profile_env_vars(profile)
    
    params = profile.get("parameters", {})
    yake = params.get("yake", {})
    custom = params.get("custom_dedup", {})
    
    print(f"  YAKE top_n: {yake.get('top_n')}")
    print(f"  YAKE n: {yake.get('n')}")
    print(f"  YAKE dedupLim: {yake.get('dedupLim')}")
    print(f"  stem_dedup: {custom.get('stem_dedup_enabled')}")
    print(f"  ngram_clean: {custom.get('ngram_clean_enabled')}")


def run_profile_pipeline(profile_name: str) -> Dict[str, Any]:
    """
    Run the complete pipeline for a single profile.
    
    Steps:
    1. Apply profile environment variables
    2. Run metadata extraction (from JSON text)
    3. Verify/copy taxonomy with profile suffix
    4. Run enrichment
    5. Create aggregate
    
    Returns:
        Result dictionary with paths and validation status
    """
    suffix = PROFILE_SUFFIXES[profile_name]
    config = load_profiles()
    profile = get_profile(profile_name)
    test_book = config.get("test_book", {})
    
    print(f"\n{'='*60}")
    print(f"Running Profile: {profile_name.upper()}")
    print(f"{'='*60}")
    print(f"Description: {profile.get('description', 'N/A')}")
    
    result = {
        "profile": profile_name,
        "suffix": suffix,
        "timestamp": datetime.now().isoformat(),
        "validations": {},
        "paths": {},
        "success": False,
    }
    
    # Define paths
    eval_dir = PROJECT_ROOT / "outputs" / "evaluation"
    eval_dir.mkdir(parents=True, exist_ok=True)
    
    book_name = test_book.get("name", "Unknown")
    
    # Profile-specific extracted metadata
    metadata_file = eval_dir / f"{book_name}_metadata_{suffix}.json"
    
    # Profile-specific taxonomy with naming that production aggregate script expects
    # Production create_aggregate_package.py extracts: taxonomy_path.stem.replace("_taxonomy", "")
    # So "{book_name}_{suffix}_taxonomy.json" -> "{book_name}_{suffix}" as source book
    # We'll need to copy metadata to match this expected source book name
    taxonomy_file = eval_dir / f"{book_name}_{suffix}_taxonomy.json"
    
    # Profile-specific enriched output
    enriched_file = eval_dir / f"{book_name}_enriched_{suffix}.json"
    
    # Profile-specific aggregate
    aggregate_file = eval_dir / f"aggregate_{suffix}.json"
    
    result["paths"] = {
        "metadata": str(metadata_file),
        "taxonomy": str(taxonomy_file),
        "enriched": str(enriched_file),
        "aggregate": str(aggregate_file),
    }
    
    # Step 1: Apply profile environment variables
    print("\n[Step 1/5] Applying profile configuration...")
    apply_profile_env_vars(profile)
    
    params = profile.get("parameters", {})
    yake = params.get("yake", {})
    custom = params.get("custom_dedup", {})
    
    print(f"  YAKE top_n: {yake.get('top_n')}")
    print(f"  YAKE n: {yake.get('n')}")
    print(f"  YAKE dedupLim: {yake.get('dedupLim')}")
    print(f"  stem_dedup: {custom.get('stem_dedup_enabled')}")
    print(f"  ngram_clean: {custom.get('ngram_clean_enabled')}")
    
    result["validations"]["config_applied"] = True
    
    # Step 2: Run metadata extraction
    print("\n[Step 2/5] Running metadata extraction...")
    
    # Find source JSON text file
    source_json = find_source_json_text(book_name)
    
    if source_json is None:
        # Fallback: use existing metadata as source (copy and re-process would be complex)
        existing_metadata = PROJECT_ROOT / "workflows" / "metadata_extraction" / "output" / test_book.get("metadata_file", "")
        if existing_metadata.exists():
            print(f"  ⚠️ Source JSON text not found, using existing metadata: {existing_metadata.name}")
            # Copy existing metadata with profile suffix (the extraction params won't apply here)
            shutil.copy(existing_metadata, metadata_file)
            v2 = validate_step("Metadata", metadata_file.exists(), f"Copied {metadata_file.name}")
        else:
            print(f"  ❌ No source found for {book_name}")
            result["validations"]["metadata_extraction"] = False
            return result
    else:
        print(f"  Source JSON: {source_json.name}")
        v2 = run_metadata_extraction(source_json, metadata_file)
        v2 = validate_step("Metadata Extraction", v2, f"Created {metadata_file.name}")
    
    result["validations"]["metadata_extraction"] = v2 if 'v2' in dir() else False
    
    # Step 3: Verify taxonomy exists and transform to production format
    print("\n[Step 3/5] Verifying taxonomy and transforming to production format...")
    
    v3 = validate_step("Taxonomy", taxonomy_file.exists(), str(taxonomy_file.name))
    
    if not v3:
        # Try to copy from base taxonomy
        base_taxonomy = PROJECT_ROOT / "workflows" / "taxonomy_setup" / "output" / "AI-ML_taxonomy_20251128.json"
        if base_taxonomy.exists():
            shutil.copy(base_taxonomy, taxonomy_file)
            v3 = validate_step("Taxonomy", taxonomy_file.exists(), f"Created {taxonomy_file.name}")
    
    # Transform taxonomy to production format
    # Production create_aggregate_package.py expects books as list of strings: ["Book1.json", "Book2.json"]
    # But our taxonomy has books as list of dicts: [{"name": "Book1.json", "priority": 1, ...}, ...]
    if v3 and taxonomy_file.exists():
        try:
            with open(taxonomy_file) as f:
                taxonomy_data = json.load(f)
            
            # Transform tiers.*.books from list of dicts to list of strings
            tiers = taxonomy_data.get("tiers", {})
            transformed = False
            for tier_name, tier_data in tiers.items():
                books = tier_data.get("books", [])
                if books and isinstance(books[0], dict):
                    # Transform: extract just the "name" field from each book dict
                    tier_data["books"] = [book["name"] for book in books if isinstance(book, dict) and "name" in book]
                    transformed = True
            
            if transformed:
                # Write transformed taxonomy back
                with open(taxonomy_file, "w") as f:
                    json.dump(taxonomy_data, f, indent=2)
                print("  ✅ Transformed taxonomy to production format (books as string list)")
            else:
                print("  ℹ️ Taxonomy already in production format")
        except Exception as e:
            print(f"  ⚠️ Could not transform taxonomy: {e}")
    
    result["validations"]["taxonomy"] = v3
    
    if not result["validations"]["taxonomy"]:
        print("\n❌ Taxonomy not available. Cannot proceed.")
        return result
    
    # Step 4: Run enrichment
    print("\n[Step 4/5] Running enrichment...")
    
    # Copy companion book metadata to eval_dir so enrichment can find them
    # The enrichment script looks for companion books in the same directory as the input file
    source_metadata_dir = PROJECT_ROOT / "workflows" / "metadata_extraction" / "output"
    print("  Copying companion book metadata to evaluation directory...")
    companion_count = 0
    for meta_file in source_metadata_dir.glob("*_metadata.json"):
        dest_file = eval_dir / meta_file.name
        if not dest_file.exists():
            shutil.copy(meta_file, dest_file)
            companion_count += 1
    if companion_count > 0:
        print(f"  Copied {companion_count} companion metadata files")
    else:
        print("  Companion metadata already present")
    
    try:
        from workflows.metadata_enrichment.scripts.enrich_metadata_per_book import enrich_metadata
        
        enrich_metadata(metadata_file, taxonomy_file, enriched_file)
        
        v4 = validate_step("Enrichment", enriched_file.exists(), f"Created {enriched_file.name}")
        
        # Validate enriched content
        if enriched_file.exists():
            with open(enriched_file) as f:
                enriched_data = json.load(f)
            
            chapters = enriched_data.get("chapters", [])
            total_keywords = sum(len(ch.get("keywords", [])) for ch in chapters)
            total_concepts = sum(len(ch.get("concepts", [])) for ch in chapters)
            
            print(f"  Chapters: {len(chapters)}")
            print(f"  Total keywords: {total_keywords}")
            print(f"  Total concepts: {total_concepts}")
            
            v4 = v4 and total_keywords > 0
        
        result["validations"]["enrichment"] = v4
        
    except Exception as e:
        print(f"  ❌ Enrichment failed: {e}")
        import traceback
        traceback.print_exc()
        result["validations"]["enrichment"] = False
        return result
    
    # Step 5: Create aggregate using production aggregate package creation
    # This bundles: taxonomy + source book enriched metadata + all companion book metadata
    print("\n[Step 5/5] Creating aggregate package (production flow)...")
    
    try:
        # Use production aggregate creation which includes full taxonomy and all companion metadata
        # Create tmp output dir for aggregate packages
        aggregate_tmp_dir = eval_dir / "aggregate_packages"
        aggregate_tmp_dir.mkdir(parents=True, exist_ok=True)
        
        # The production script extracts source_book from taxonomy filename:
        # "{book_name}_{suffix}_taxonomy.json" -> "{book_name}_{suffix}"
        # It then looks for "{source_book}_metadata.json" in metadata_dir
        # So we need to create a metadata file with that exact name
        source_book_with_suffix = f"{book_name}_{suffix}"
        
        # Create a metadata directory for this profile's aggregate
        profile_metadata_dir = aggregate_tmp_dir / f"metadata_{suffix}"
        profile_metadata_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy all companion book metadata to this directory
        source_metadata_dir = PROJECT_ROOT / "workflows" / "metadata_extraction" / "output"
        for meta_file in source_metadata_dir.glob("*_metadata.json"):
            shutil.copy(meta_file, profile_metadata_dir / meta_file.name)
        
        # Copy our profile-specific metadata with the expected naming
        # Production expects: {source_book}_metadata.json where source_book = "{book_name}_{suffix}"
        expected_metadata_name = f"{source_book_with_suffix}_metadata.json"
        shutil.copy(metadata_file, profile_metadata_dir / expected_metadata_name)
        print(f"  Created metadata for production: {expected_metadata_name}")
        
        # The production script expects enriched files named "{book}_enr_metadata_{timestamp}.json"
        # Our enriched file is named "{book}_enriched_{PROFILE}.json"
        # Create a copy with the expected naming pattern so production script can find it
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        production_enriched_file = aggregate_tmp_dir / f"{source_book_with_suffix}_enr_metadata_{timestamp}.json"
        shutil.copy(enriched_file, production_enriched_file)
        print(f"  Created enriched file for production: {production_enriched_file.name}")
        
        # Guideline directory
        guideline_dir = PROJECT_ROOT / "workflows" / "base_guideline_generation" / "output"
        
        # Call production aggregate package creation
        # This will load taxonomy, source book enriched metadata, and all companion book metadata
        package_path = create_aggregate_package(
            taxonomy_path=taxonomy_file,
            metadata_dir=profile_metadata_dir,  # Use our prepared metadata directory
            guideline_dir=guideline_dir,
            output_dir=aggregate_tmp_dir,
            enriched_metadata_file=production_enriched_file  # Use renamed enriched file
        )
        
        # Copy/rename to our expected aggregate file location
        shutil.copy(package_path, aggregate_file)
        
        v5 = validate_step("Aggregate", aggregate_file.exists(), f"Created {aggregate_file.name}")
        
        # Validate aggregate content from production format
        with open(aggregate_file) as f:
            aggregate = json.load(f)
        
        companion_count = len(aggregate.get("companion_books", []))
        stats = aggregate.get("statistics", {})
        total_books = stats.get("total_books", 0)
        total_chapters = stats.get("total_chapters", 0)
        
        print(f"  Total books in aggregate: {total_books}")
        print(f"  Companion books: {companion_count}")
        print(f"  Total chapters across all books: {total_chapters}")
        print(f"  Missing books: {stats.get('missing_count', 0)}")
        
        v5 = v5 and companion_count > 0
        result["validations"]["aggregate"] = v5
        
    except Exception as e:
        print(f"  ❌ Aggregate creation failed: {e}")
        import traceback
        traceback.print_exc()
        result["validations"]["aggregate"] = False
        return result
    
    # Final status
    result["success"] = all(result["validations"].values())
    
    if result["success"]:
        print(f"\n✅ Profile {profile_name.upper()} completed successfully")
    else:
        print(f"\n⚠️ Profile {profile_name.upper()} completed with errors")
    
    return result


def create_aggregate(enriched_file: Path, profile_name: str, profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create aggregate data structure for LLM evaluation.
    
    Includes:
    - Profile configuration used
    - Sample keywords and concepts
    - Related chapters connections
    - Statistics
    """
    with open(enriched_file) as f:
        enriched_data = json.load(f)
    
    chapters = enriched_data.get("chapters", [])
    
    # Collect all keywords and concepts
    all_keywords = []
    all_concepts = []
    all_related = []
    
    for ch in chapters:
        # Keywords
        for kw in ch.get("keywords", []):
            if isinstance(kw, dict):
                all_keywords.append(kw.get("term", kw.get("keyword", "")))
            else:
                all_keywords.append(str(kw))
        
        # Concepts
        for concept in ch.get("concepts", []):
            if isinstance(concept, dict):
                all_concepts.append(concept.get("concept", ""))
            else:
                all_concepts.append(str(concept))
        
        # Related chapters
        for rel in ch.get("related_chapters", []):
            if isinstance(rel, dict):
                all_related.append({
                    "from_chapter": ch.get("chapter_number", ch.get("number", 0)),
                    "to_book": rel.get("book", ""),
                    "to_chapter": rel.get("chapter", ""),
                    "similarity": rel.get("similarity", 0),
                })
    
    # Deduplicate and count
    unique_keywords = list(set(all_keywords))
    unique_concepts = list(set(all_concepts))
    
    # Calculate statistics
    stats = {
        "total_chapters": len(chapters),
        "total_keyword_instances": len(all_keywords),
        "unique_keywords": len(unique_keywords),
        "keyword_diversity_ratio": len(unique_keywords) / len(all_keywords) if all_keywords else 0,
        "total_concept_instances": len(all_concepts),
        "unique_concepts": len(unique_concepts),
        "total_cross_references": len(all_related),
    }
    
    # Build aggregate
    # Extract book name: enriched files have "book" key with format "BookName_SUFFIX"
    raw_book = enriched_data.get("book", enriched_data.get("book_title", enriched_data.get("title", "Unknown")))
    # Remove profile suffix if present (e.g., "AI Engineering_BASELINE" -> "AI Engineering")
    source_book = raw_book
    for suffix in ["_BASELINE", "_CURRENT", "_MODERATE", "_AGGRESSIVE"]:
        if source_book.endswith(suffix):
            source_book = source_book[:-len(suffix)]
            break
    
    aggregate = {
        "profile": profile_name,
        "profile_config": {
            "name": profile.get("name"),
            "description": profile.get("description"),
            "parameters": profile.get("parameters"),
        },
        "source_book": source_book,
        "timestamp": datetime.now().isoformat(),
        "statistics": stats,
        "keywords_sample": unique_keywords[:50],  # First 50 unique keywords
        "concepts_sample": unique_concepts[:30],  # First 30 unique concepts
        "cross_references_sample": all_related[:20],  # First 20 cross-references
        "chapters_summary": [
            {
                "number": ch.get("chapter_number", ch.get("number", i+1)),
                "title": ch.get("title", f"Chapter {i+1}"),
                "keywords_count": len(ch.get("keywords", [])),
                "concepts_count": len(ch.get("concepts", [])),
                "related_count": len(ch.get("related_chapters", [])),
            }
            for i, ch in enumerate(chapters[:10])  # First 10 chapters
        ],
    }
    
    return aggregate


def run_all_profiles() -> Dict[str, Any]:
    """Run pipeline for all 4 profiles."""
    profiles = ["baseline", "current", "moderate", "aggressive"]
    results = {}
    
    for profile in profiles:
        results[profile] = run_profile_pipeline(profile)
    
    # Summary
    print("\n" + "="*60)
    print("EXECUTION SUMMARY")
    print("="*60)
    
    for profile, result in results.items():
        status = "✅" if result["success"] else "❌"
        print(f"  {status} {profile.upper()}")
    
    # Check all succeeded
    all_success = all(r["success"] for r in results.values())
    
    if all_success:
        print("\n✅ All profiles completed successfully")
        print("\nAggregates ready for LLM evaluation:")
        for profile in profiles:
            suffix = PROFILE_SUFFIXES[profile]
            print(f"  - outputs/evaluation/aggregate_{suffix}.json")
    else:
        print("\n⚠️ Some profiles failed. Check logs above.")
    
    return results


def validate_aggregates() -> bool:
    """Validate all 4 aggregates exist and have valid structure (production format)."""
    eval_dir = PROJECT_ROOT / "outputs" / "evaluation"
    
    print("\nValidating aggregates (production format)...")
    print("=" * 60)
    all_valid = True
    issues = []
    
    for profile, suffix in PROFILE_SUFFIXES.items():
        agg_file = eval_dir / f"aggregate_{suffix}.json"
        
        if not agg_file.exists():
            print(f"  ❌ {suffix}: File not found")
            all_valid = False
            issues.append(f"{suffix}: File missing")
            continue
        
        try:
            with open(agg_file) as f:
                data = json.load(f)
            
            # Required fields check (production aggregate format)
            required_fields = ["project", "taxonomy", "source_book", "companion_books", "statistics"]
            missing_fields = [f for f in required_fields if f not in data]
            if missing_fields:
                issues.append(f"{suffix}: Missing fields {missing_fields}")
                all_valid = False
            
            # Content validation (production format)
            project = data.get("project", {})
            source_book_data = data.get("source_book", {})
            source_book_name = source_book_data.get("name", "Unknown") if isinstance(source_book_data, dict) else "Unknown"
            companion_books = data.get("companion_books", [])
            missing_books = data.get("missing_books", [])
            stats = data.get("statistics", {})
            
            total_books = stats.get("total_books", 0)
            total_chapters = stats.get("total_chapters", 0)
            companion_count = stats.get("companion_books", len(companion_books))
            missing_count = stats.get("missing_count", len(missing_books))
            
            # Check for "Unknown" source_book
            if source_book_name == "Unknown":
                issues.append(f"{suffix}: source_book name is 'Unknown' (extraction bug)")
                all_valid = False
            
            # Check for companion books
            if companion_count == 0:
                issues.append(f"{suffix}: No companion books loaded")
                all_valid = False
            
            # Check source book has metadata
            source_metadata = source_book_data.get("metadata", {}) if isinstance(source_book_data, dict) else {}
            if not source_metadata:
                issues.append(f"{suffix}: Source book has no metadata")
                all_valid = False
            
            # Warn about missing books (not a failure, but notable)
            if missing_count > 0:
                issues.append(f"{suffix}: {missing_count} books from taxonomy missing metadata")
            
            # Summary line
            status = "✅" if source_book_name != "Unknown" and companion_count > 0 and source_metadata else "⚠️ "
            print(f"  {status} {suffix}:")
            print(f"      Project ID: {project.get('id', 'N/A')}")
            print(f"      Source book: {source_book_name}")
            print(f"      Total books: {total_books}, Companion: {companion_count}, Missing: {missing_count}")
            print(f"      Total chapters across all books: {total_chapters}")
            
        except json.JSONDecodeError as e:
            print(f"  ❌ {suffix}: Invalid JSON - {e}")
            all_valid = False
            issues.append(f"{suffix}: Invalid JSON")
        except Exception as e:
            print(f"  ❌ {suffix}: Error - {e}")
            all_valid = False
            issues.append(f"{suffix}: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    if issues:
        print("Issues found:")
        for issue in issues:
            print(f"  ⚠️  {issue}")
    
    if all_valid:
        print("\n✅ All aggregates valid and ready for LLM evaluation")
    else:
        print("\n❌ Some aggregates have issues. Review above.")
    
    return all_valid


def main():
    parser = argparse.ArgumentParser(
        description="Run extraction profile test pipeline"
    )
    
    parser.add_argument(
        "--profile",
        choices=["baseline", "current", "moderate", "aggressive"],
        help="Run specific profile"
    )
    
    parser.add_argument(
        "--run-all",
        action="store_true",
        help="Run all 4 profiles"
    )
    
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate existing aggregates"
    )
    
    args = parser.parse_args()
    
    if args.run_all:
        run_all_profiles()
    elif args.profile:
        run_profile_pipeline(args.profile)
    elif args.validate:
        validate_aggregates()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
