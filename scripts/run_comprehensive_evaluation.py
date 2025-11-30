#!/usr/bin/env python3
"""
Comprehensive Extraction Evaluation Pipeline
=============================================

Orchestrates the complete test pipeline:
1. Run 4 extraction profiles (baseline, current, moderate, aggressive)
2. Collect objective metrics (diversity, uniqueness, coverage)
3. Evaluate with 3 LLMs (Gemini, Claude, OpenAI)
4. Aggregate results and generate comparison report

Usage:
    python run_comprehensive_evaluation.py --run-all
    python run_comprehensive_evaluation.py --profile baseline --evaluate
    python run_comprehensive_evaluation.py --analyze-results
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.run_extraction_tests import run_extraction_for_profile, get_profile
from scripts.llm_evaluation import run_evaluation, get_llm_configs


def calculate_objective_metrics(output_dir: Path) -> Dict[str, Any]:
    """
    Calculate objective statistical metrics for extraction output.
    
    Returns metrics for verifying extraction quality:
    - Keyword diversity (unique vs total)
    - Average keyword length
    - N-gram distribution
    - Duplicate detection
    - Coverage metrics
    """
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "output_dir": str(output_dir),
    }
    
    # Load extraction output
    json_files = list(output_dir.glob("*_enriched.json"))
    if not json_files:
        json_files = list(output_dir.glob("*.json"))
    
    if not json_files:
        return {"error": "No JSON files found"}
    
    latest_file = max(json_files, key=lambda p: p.stat().st_mtime)
    
    try:
        with open(latest_file) as f:
            data = json.load(f)
        
        # Extract keywords from all chapters
        all_keywords = set()
        keyword_counts = {}
        ngram_distribution = {1: 0, 2: 0, 3: 0, "4+": 0}
        
        chapters = data.get("chapters", [])
        for chapter in chapters:
            keywords = chapter.get("keywords", [])
            for kw in keywords:
                keyword_text = kw if isinstance(kw, str) else kw.get("keyword", "")
                if keyword_text:
                    all_keywords.add(keyword_text.lower())
                    keyword_counts[keyword_text.lower()] = keyword_counts.get(keyword_text.lower(), 0) + 1
                    
                    # Count n-grams
                    word_count = len(keyword_text.split())
                    if word_count <= 3:
                        ngram_distribution[word_count] += 1
                    else:
                        ngram_distribution["4+"] += 1
        
        # Calculate metrics
        total_keywords = sum(keyword_counts.values())
        unique_keywords = len(all_keywords)
        
        metrics.update({
            "total_keyword_instances": total_keywords,
            "unique_keywords": unique_keywords,
            "diversity_ratio": unique_keywords / total_keywords if total_keywords > 0 else 0,
            "average_frequency": total_keywords / unique_keywords if unique_keywords > 0 else 0,
            "ngram_distribution": ngram_distribution,
            "chapters_processed": len(chapters),
        })
        
        # Find potential duplicates (stem-based)
        from workflows.metadata_extraction.scripts.adapters.statistical_extractor import _get_word_stem
        
        stem_groups = {}
        for kw in all_keywords:
            stem = _get_word_stem(kw)
            if stem not in stem_groups:
                stem_groups[stem] = []
            stem_groups[stem].append(kw)
        
        potential_duplicates = {stem: words for stem, words in stem_groups.items() if len(words) > 1}
        
        metrics.update({
            "potential_duplicate_groups": len(potential_duplicates),
            "duplicate_examples": dict(list(potential_duplicates.items())[:5]),
        })
        
    except Exception as e:
        metrics["error"] = str(e)
    
    return metrics


def run_profile_with_evaluation(profile_name: str, llm_models: List[str]) -> Dict[str, Any]:
    """
    Run extraction for a profile and evaluate with LLMs.
    
    Returns combined results with objective and subjective metrics.
    """
    print(f"\n{'='*60}")
    print(f"Processing Profile: {profile_name}")
    print(f"{'='*60}")
    
    # Step 1: Run extraction
    print("\n[1/3] Running extraction...")
    output_dir = run_extraction_for_profile(profile_name)
    
    # Step 2: Calculate objective metrics
    print("\n[2/3] Calculating objective metrics...")
    objective_metrics = calculate_objective_metrics(output_dir)
    
    # Step 3: Run LLM evaluation
    print("\n[3/3] Running LLM evaluation...")
    llm_results = run_evaluation(str(output_dir), llm_models)
    
    # Combine results
    combined_results = {
        "profile": profile_name,
        "output_dir": str(output_dir),
        "timestamp": datetime.now().isoformat(),
        "objective_metrics": objective_metrics,
        "llm_evaluation": llm_results,
    }
    
    # Save combined results
    results_file = PROJECT_ROOT / "outputs" / f"evaluation_results_{profile_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, "w") as f:
        json.dump(combined_results, f, indent=2)
    
    print(f"\n✅ Results saved: {results_file}")
    
    return combined_results


def run_all_profiles(llm_models: List[str]) -> Dict[str, Any]:
    """
    Run all 4 profiles and aggregate results.
    """
    profiles = ["baseline", "current", "moderate", "aggressive"]
    all_results = {}
    
    for profile in profiles:
        try:
            results = run_profile_with_evaluation(profile, llm_models)
            all_results[profile] = results
        except Exception as e:
            print(f"\n⚠️  Error processing profile '{profile}': {e}")
            all_results[profile] = {"error": str(e)}
    
    # Generate comparison report
    comparison_report = generate_comparison_report(all_results)
    
    # Save aggregate results
    aggregate_file = PROJECT_ROOT / "outputs" / f"aggregate_evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(aggregate_file, "w") as f:
        json.dump({
            "profiles": all_results,
            "comparison": comparison_report,
            "timestamp": datetime.now().isoformat(),
        }, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"✅ Aggregate results saved: {aggregate_file}")
    print(f"{'='*60}")
    
    return all_results


def generate_comparison_report(all_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate comparison report across all profiles.
    """
    report = {
        "objective_comparison": {},
        "llm_scores_comparison": {},
        "rankings": {},
    }
    
    # Compare objective metrics
    for profile, results in all_results.items():
        if "error" in results:
            continue
        
        metrics = results.get("objective_metrics", {})
        report["objective_comparison"][profile] = {
            "unique_keywords": metrics.get("unique_keywords", 0),
            "diversity_ratio": metrics.get("diversity_ratio", 0),
            "potential_duplicates": metrics.get("potential_duplicate_groups", 0),
        }
    
    # Compare LLM scores
    for profile, results in all_results.items():
        if "error" in results:
            continue
        
        llm_eval = results.get("llm_evaluation", {})
        aggregate = llm_eval.get("aggregate", {})
        report["llm_scores_comparison"][profile] = {
            "average_score": aggregate.get("average_score", 0),
            "models_responded": aggregate.get("models_responded", 0),
        }
    
    # Rank profiles
    scores = [(profile, data.get("average_score", 0)) 
              for profile, data in report["llm_scores_comparison"].items()]
    scores.sort(key=lambda x: x[1], reverse=True)
    
    report["rankings"] = {
        "by_llm_score": [{"profile": p, "score": s} for p, s in scores],
    }
    
    return report


def main():
    parser = argparse.ArgumentParser(
        description="Comprehensive extraction evaluation pipeline"
    )
    
    parser.add_argument(
        "--run-all",
        action="store_true",
        help="Run all 4 profiles with full evaluation"
    )
    
    parser.add_argument(
        "--profile",
        choices=["baseline", "current", "moderate", "aggressive"],
        help="Run specific profile"
    )
    
    parser.add_argument(
        "--evaluate",
        action="store_true",
        help="Evaluate with LLMs (requires --profile)"
    )
    
    parser.add_argument(
        "--models",
        nargs="+",
        choices=["gemini", "claude", "openai", "deepseek", "deepseek-reasoner"],
        default=["gemini", "claude", "openai"],
        help="LLM models to use for evaluation (default: gemini claude openai)"
    )
    
    parser.add_argument(
        "--analyze-results",
        action="store_true",
        help="Analyze existing results"
    )
    
    args = parser.parse_args()
    
    if args.run_all:
        run_all_profiles(args.models)
    elif args.profile:
        if args.evaluate:
            run_profile_with_evaluation(args.profile, args.models)
        else:
            run_extraction_for_profile(args.profile)
    elif args.analyze_results:
        # Load and analyze recent results
        outputs_dir = PROJECT_ROOT / "outputs"
        result_files = list(outputs_dir.glob("aggregate_evaluation_*.json"))
        if result_files:
            latest = max(result_files, key=lambda p: p.stat().st_mtime)
            with open(latest) as f:
                data = json.load(f)
            
            print(f"\n📊 Analysis of: {latest.name}")
            print("="*60)
            
            comparison = data.get("comparison", {})
            rankings = comparison.get("rankings", {})
            
            print("\n🏆 Rankings by LLM Score:")
            for rank in rankings.get("by_llm_score", []):
                print(f"  {rank['profile']}: {rank['score']:.2f}/10")
            
            print("\n📈 Objective Metrics Comparison:")
            obj_comp = comparison.get("objective_comparison", {})
            for profile, metrics in obj_comp.items():
                print(f"\n  {profile}:")
                print(f"    Unique keywords: {metrics.get('unique_keywords', 0)}")
                print(f"    Diversity ratio: {metrics.get('diversity_ratio', 0):.2%}")
                print(f"    Potential duplicates: {metrics.get('potential_duplicates', 0)}")
        else:
            print("No aggregate results found")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
