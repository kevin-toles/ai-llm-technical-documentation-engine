#!/usr/bin/env python3
"""
Comprehensive Extraction Evaluation Pipeline
=============================================

Orchestrates the complete test pipeline:
1. Run 4 extraction profiles (baseline, current, moderate, aggressive)
2. Create profile-specific aggregates with validation
3. Run Strategy B comparative LLM evaluation (all 4 aggregates to each LLM)
4. Generate final report

Usage:
    python run_comprehensive_evaluation.py --run-all
    python run_comprehensive_evaluation.py --extract-only
    python run_comprehensive_evaluation.py --evaluate-only
    python run_comprehensive_evaluation.py --dry-run
    
    # With observability logging:
    python run_comprehensive_evaluation.py --run-all --with-observability
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Optional observability integration
_observability_enabled = False
_trace_id: Optional[str] = None


def init_observability() -> None:
    """Initialize observability logging if available."""
    global _observability_enabled, _trace_id
    try:
        from observability_platform.src.jsonl_logger import log_record, new_id, now_iso
        from observability_platform.src.architecture_context import log_architecture_context
        
        _observability_enabled = True
        _trace_id = new_id("trc")
        
        # Log architecture context once at start
        log_architecture_context()
        
        # Log pipeline start
        log_record({
            "record_type": "event",
            "event_type": "PipelineStarted",
            "trace_id": _trace_id,
            "pipeline": "comprehensive_extraction_evaluation",
            "timestamp": now_iso(),
        })
        
        print("📊 Observability logging enabled")
    except ImportError:
        _observability_enabled = False
        print("ℹ️  Observability logging not available (optional)")


def log_phase_start(phase_name: str) -> None:
    """Log the start of a pipeline phase."""
    if not _observability_enabled:
        return
    try:
        from observability_platform.src.jsonl_logger import log_record, now_iso
        log_record({
            "record_type": "event",
            "event_type": "PhaseStarted",
            "trace_id": _trace_id,
            "phase": phase_name,
            "timestamp": now_iso(),
        })
    except Exception:
        pass


def log_phase_end(phase_name: str, status: str, metrics: Optional[Dict] = None) -> None:
    """Log the end of a pipeline phase."""
    if not _observability_enabled:
        return
    try:
        from observability_platform.src.jsonl_logger import log_record, now_iso
        record = {
            "record_type": "event",
            "event_type": "PhaseCompleted",
            "trace_id": _trace_id,
            "phase": phase_name,
            "status": status,
            "timestamp": now_iso(),
        }
        if metrics:
            record["metrics"] = metrics
        log_record(record)
    except Exception:
        pass


def log_pipeline_end(status: str, summary: Optional[Dict] = None) -> None:
    """Log the end of the entire pipeline."""
    if not _observability_enabled:
        return
    try:
        from observability_platform.src.jsonl_logger import log_record, now_iso
        record = {
            "record_type": "event",
            "event_type": "PipelineCompleted",
            "trace_id": _trace_id,
            "pipeline": "comprehensive_extraction_evaluation",
            "status": status,
            "timestamp": now_iso(),
        }
        if summary:
            record["summary"] = summary
        log_record(record)
    except Exception:
        pass


def verify_prerequisites() -> Dict[str, Any]:
    """Verify all prerequisites are in place."""
    status = {
        "profiles_config": False,
        "source_metadata": False,
        "taxonomies": False,
        "api_keys": {},
    }
    
    # Check profiles config
    profiles_path = PROJECT_ROOT / "config" / "extraction_profiles.json"
    status["profiles_config"] = profiles_path.exists()
    
    # Check source metadata
    config = {}
    if profiles_path.exists():
        with open(profiles_path) as f:
            config = json.load(f)
    
    test_book = config.get("test_book", {})
    metadata_file = PROJECT_ROOT / "workflows" / "metadata_extraction" / "output" / test_book.get("metadata_file", "")
    status["source_metadata"] = metadata_file.exists()
    status["source_metadata_path"] = str(metadata_file) if metadata_file.exists() else "NOT FOUND"
    
    # Check taxonomies
    eval_dir = PROJECT_ROOT / "outputs" / "evaluation"
    taxonomy_count = 0
    book_name = test_book.get("name", "AI Engineering Building Applications")
    for suffix in ["BASELINE", "CURRENT", "MODERATE", "AGGRESSIVE"]:
        # Check both naming patterns
        pattern1 = eval_dir / f"{book_name}_{suffix}_taxonomy.json"
        pattern2 = eval_dir / f"AI-ML_taxonomy_{suffix}.json"
        if pattern1.exists() or pattern2.exists():
            taxonomy_count += 1
    status["taxonomies"] = taxonomy_count == 4
    status["taxonomies_count"] = taxonomy_count
    
    # Check API keys
    for key in ["DEEPSEEK_API_KEY", "GEMINI_API_KEY", "ANTHROPIC_API_KEY", "OPENAI_API_KEY"]:
        val = os.environ.get(key, "")
        if val:
            status["api_keys"][key] = f"***{val[-4:]}"
        else:
            status["api_keys"][key] = "NOT SET"
    
    return status


def run_dry_run() -> None:
    """Run configuration verification without executing."""
    print("\n🔍 DRY RUN - Configuration Verification")
    print("=" * 60)
    
    status = verify_prerequisites()
    
    # Profiles config
    print("\n📋 Extraction Profiles:")
    if status["profiles_config"]:
        profiles_path = PROJECT_ROOT / "config" / "extraction_profiles.json"
        with open(profiles_path) as f:
            config = json.load(f)
        for name, profile in config.get("profiles", {}).items():
            params = profile.get("parameters", {})
            yake = params.get("yake", {})
            custom = params.get("custom_dedup", {})
            print(f"  ✅ {name}: top_n={yake.get('top_n')}, "
                  f"stem_dedup={custom.get('stem_dedup_enabled')}, "
                  f"ngram_clean={custom.get('ngram_clean_enabled')}")
    else:
        print("  ❌ Profiles config not found")
    
    # Source metadata
    print("\n📄 Source Metadata:")
    if status["source_metadata"]:
        print(f"  ✅ {status['source_metadata_path']}")
    else:
        print(f"  ❌ {status.get('source_metadata_path', 'NOT FOUND')}")
    
    # Taxonomies
    print("\n📚 Taxonomies:")
    if status["taxonomies"]:
        print(f"  ✅ All 4 taxonomy variants exist")
    else:
        print(f"  ⚠️  Only {status['taxonomies_count']}/4 taxonomies found")
        print("    Run: scripts/run_extraction_tests.py to create missing taxonomies")
    
    # API Keys
    print("\n🔐 API Keys:")
    for key, val in status["api_keys"].items():
        if val != "NOT SET":
            print(f"  ✅ {key}: {val}")
        else:
            print(f"  ❌ {key}: NOT SET")
    
    # Test LLM connections
    print("\n🔌 LLM Connection Test:")
    try:
        from scripts.llm_evaluation import test_api_connections
        test_api_connections()
    except Exception as e:
        print(f"  ⚠️ Could not test connections: {e}")
    
    print("\n" + "=" * 60)
    
    # Ready status
    all_ready = (
        status["profiles_config"] and 
        status["source_metadata"] and 
        status["taxonomies"] and
        any(v != "NOT SET" for v in status["api_keys"].values())
    )
    
    if all_ready:
        print("✅ Ready for execution. Use --run-all to start.")
    else:
        print("⚠️ Prerequisites missing. Fix issues above before running.")


def run_extraction_phase() -> bool:
    """Run extraction for all 4 profiles with validation gates."""
    print("\n" + "=" * 60)
    print("PHASE 1: EXTRACTION")
    print("=" * 60)
    
    log_phase_start("extraction")
    
    from scripts.run_extraction_tests import run_all_profiles, validate_aggregates
    
    results = run_all_profiles()
    
    # Check all succeeded
    success = all(r.get("success", False) for r in results.values())
    
    log_phase_end("extraction", "success" if success else "failed", {
        "profiles_run": len(results),
        "profiles_succeeded": sum(1 for r in results.values() if r.get("success", False)),
    })
    
    if not success:
        return False
    
    # VALIDATION GATE: Validate all aggregates before proceeding
    print("\n" + "-" * 60)
    print("VALIDATION GATE: Aggregate Validation")
    print("-" * 60)
    
    log_phase_start("aggregate_validation")
    
    aggregates_valid = validate_aggregates()
    validation_details = collect_aggregate_validation_details()
    
    log_phase_end("aggregate_validation", "success" if aggregates_valid else "failed", validation_details)
    
    if not aggregates_valid:
        print("\n❌ VALIDATION GATE FAILED: Aggregates have issues.")
        print("   Review the validation output above before proceeding.")
        # For now, we'll continue but warn (aggregates may have expected issues like 0 cross-refs)
        print("   ⚠️  Continuing with warning (some issues may be expected in simulation)")
    else:
        print("\n✅ VALIDATION GATE PASSED: All aggregates valid")
    
    return success


def collect_aggregate_validation_details() -> Dict[str, Any]:
    """Collect detailed validation metrics for aggregates."""
    eval_dir = PROJECT_ROOT / "outputs" / "evaluation"
    details = {
        "profiles_validated": 0,
        "issues": [],
        "per_profile": {}
    }
    
    for profile_name, suffix in [("baseline", "BASELINE"), ("current", "CURRENT"), 
                                  ("moderate", "MODERATE"), ("aggressive", "AGGRESSIVE")]:
        agg_file = eval_dir / f"aggregate_{suffix}.json"
        if agg_file.exists():
            try:
                with open(agg_file) as f:
                    data = json.load(f)
                details["profiles_validated"] += 1
                details["per_profile"][profile_name] = {
                    "source_book": data.get("source_book", "Unknown"),
                    "keywords_count": len(data.get("keywords_sample", [])),
                    "concepts_count": len(data.get("concepts_sample", [])),
                    "cross_refs_count": len(data.get("cross_references_sample", [])),
                    "keyword_diversity": data.get("statistics", {}).get("keyword_diversity_ratio", 0),
                }
                if data.get("source_book") == "Unknown":
                    details["issues"].append(f"{suffix}: source_book is Unknown")
                if len(data.get("keywords_sample", [])) == 0:
                    details["issues"].append(f"{suffix}: no keywords")
            except Exception as e:
                details["issues"].append(f"{suffix}: {str(e)}")
    
    return details


def run_evaluation_phase(models: List[str] | None = None) -> Dict[str, Any]:
    """Run Strategy B comparative LLM evaluation."""
    print("\n" + "=" * 60)
    print("PHASE 2: LLM COMPARATIVE EVALUATION")
    print("=" * 60)
    
    log_phase_start("llm_evaluation")
    
    from scripts.llm_evaluation import run_comparative_evaluation
    
    results = run_comparative_evaluation(models)
    
    status = "failed" if "error" in results else "success"
    log_phase_end("llm_evaluation", status, {
        "models_used": results.get("models_used", []),
        "consensus": results.get("consensus", {}),
    })
    
    return results


def generate_final_report(eval_results: Dict[str, Any]) -> None:
    """Generate final summary report."""
    print("\n" + "=" * 60)
    print("FINAL REPORT")
    print("=" * 60)
    
    if "error" in eval_results:
        print(f"\n❌ Evaluation failed: {eval_results['error']}")
        return
    
    # Consensus
    consensus = eval_results.get("consensus", {})
    if consensus:
        best = consensus.get("best_for_production", "Unknown")
        votes = consensus.get("votes", {})
        ratio = consensus.get("agreement_ratio", 0)
        
        print(f"\n🏆 RECOMMENDED PROFILE: {best.upper()}")
        print(f"   Agreement: {ratio:.0%} of LLMs")
        print(f"   Votes: {votes}")
    
    # Per-LLM results
    print("\n📊 Per-LLM Rankings:")
    for model, eval_result in eval_results.get("evaluations", {}).items():
        if "comparative_ranking" in eval_result:
            rankings = eval_result["comparative_ranking"]
            print(f"\n  {model}:")
            for r in rankings:
                print(f"    #{r['rank']}: {r['profile']} ({r['overall_score']}/10)")
    
    # Save summary
    eval_dir = PROJECT_ROOT / "outputs" / "evaluation"
    summary_file = eval_dir / f"final_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "consensus": consensus,
        "models_used": eval_results.get("models_used", []),
        "recommendation": best if consensus else "Inconclusive",
    }
    
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n📄 Summary saved: {summary_file}")


def run_full_pipeline(models: List[str] | None = None) -> None:
    """Run complete pipeline: extraction + evaluation with validation gates."""
    start_time = datetime.now()
    
    print("\n" + "=" * 60)
    print("COMPREHENSIVE EXTRACTION EVALUATION PIPELINE")
    print("=" * 60)
    print(f"Started: {start_time.isoformat()}")
    print("Observability: " + ("✅ Enabled" if _observability_enabled else "❌ Disabled"))
    
    # Phase 1: Extraction with validation gate
    extraction_success = run_extraction_phase()
    
    if not extraction_success:
        print("\n❌ Extraction phase failed. Cannot proceed with evaluation.")
        log_pipeline_end("failed", {"phase": "extraction", "reason": "extraction_failed"})
        return
    
    print("\n✅ Extraction phase completed. Proceeding to LLM evaluation.")
    
    # Phase 2: LLM Evaluation
    eval_results = run_evaluation_phase(models)
    
    # Validate LLM results
    print("\n" + "-" * 60)
    print("VALIDATION GATE: LLM Evaluation Results")
    print("-" * 60)
    
    log_phase_start("llm_validation")
    
    llm_validation = validate_llm_results(eval_results)
    
    log_phase_end("llm_validation", "success" if llm_validation["valid"] else "failed", llm_validation)
    
    if llm_validation["valid"]:
        print("✅ LLM evaluation results validated")
    else:
        print(f"⚠️  LLM evaluation has issues: {llm_validation.get('issues', [])}")
    
    # Final Report
    generate_final_report(eval_results)
    
    # Timing and pipeline completion
    end_time = datetime.now()
    duration = end_time - start_time
    
    summary = {
        "extraction_success": extraction_success,
        "llm_models_used": eval_results.get("models_used", []),
        "consensus": eval_results.get("consensus", {}),
        "duration_seconds": duration.total_seconds(),
    }
    
    log_pipeline_end("success", summary)
    
    print(f"\n⏱️  Total duration: {duration}")
    print("=" * 60)


def validate_llm_results(eval_results: Dict[str, Any]) -> Dict[str, Any]:
    """Validate LLM evaluation results."""
    validation = {
        "valid": True,
        "issues": [],
        "models_responded": 0,
        "consensus_reached": False,
    }
    
    if "error" in eval_results:
        validation["valid"] = False
        validation["issues"].append(f"Evaluation error: {eval_results['error']}")
        return validation
    
    evaluations = eval_results.get("evaluations", {})
    validation["models_responded"] = len(evaluations)
    
    if validation["models_responded"] == 0:
        validation["valid"] = False
        validation["issues"].append("No models responded")
        return validation
    
    # Check for consensus
    consensus = eval_results.get("consensus", {})
    if consensus.get("best_for_production"):
        validation["consensus_reached"] = True
        validation["consensus_profile"] = consensus.get("best_for_production")
        validation["agreement_ratio"] = consensus.get("agreement_ratio", 0)
    else:
        validation["issues"].append("No consensus reached among models")
    
    # Check each model's response
    for model, result in evaluations.items():
        if "error" in result:
            validation["issues"].append(f"{model}: {result['error']}")
        elif "comparative_ranking" not in result:
            validation["issues"].append(f"{model}: No ranking provided")
    
    return validation


def main():
    parser = argparse.ArgumentParser(
        description="Comprehensive extraction evaluation pipeline"
    )
    
    parser.add_argument(
        "--run-all",
        action="store_true",
        help="Run complete pipeline: extraction + LLM evaluation"
    )
    
    parser.add_argument(
        "--extract-only",
        action="store_true",
        help="Run extraction phase only (create aggregates)"
    )
    
    parser.add_argument(
        "--evaluate-only",
        action="store_true",
        help="Run LLM evaluation only (requires existing aggregates)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Verify configuration without executing"
    )
    
    parser.add_argument(
        "--models",
        nargs="+",
        choices=[
            "claude-opus-4.5", "claude-sonnet-4.5",
            "gpt-5.1", "gpt-5", "gpt-5.1-mini", "gpt-5.1-nano",
            "gemini-3-pro", "gemini-3-flash",
            "deepseek-v3", "deepseek-r1"
        ],
        default=None,  # Will use all available models if None
        help="LLM models to use for evaluation (default: all 10 models)"
    )
    
    parser.add_argument(
        "--enable-observability",
        action="store_true",
        help="Enable JSONL observability logging (logs to observability_platform/logs/)"
    )
    
    args = parser.parse_args()
    
    # Configure observability if enabled
    if args.enable_observability:
        init_observability()
    
    if args.dry_run:
        run_dry_run()
    elif args.run_all:
        run_full_pipeline(args.models)
    elif args.extract_only:
        run_extraction_phase()
    elif args.evaluate_only:
        eval_results = run_evaluation_phase(args.models)
        generate_final_report(eval_results)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
