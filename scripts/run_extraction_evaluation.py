#!/usr/bin/env python3
"""
Extraction Evaluation Runner
=============================

Orchestrates the 9-step extraction evaluation workflow:
1. Apply Baseline Configuration
2. Run Baseline Extraction
3. Apply Current Configuration
4. Run Current Extraction
5. Apply Moderate Configuration
6. Run Moderate Extraction
7. Apply Aggressive Configuration
8. Run Aggressive Extraction
9. LLM Comparative Evaluation

This script imports logging utilities from observability_platform
while keeping execution logic in scripts/.

Reference: ARCHITECTURE_GUIDELINES - separation of concerns
Reference: docs/testing/KEYWORD_EXTRACTION_TEST_PLAN.md

Usage:
    python scripts/run_extraction_evaluation.py --run-all
    python scripts/run_extraction_evaluation.py --profile baseline
    python scripts/run_extraction_evaluation.py --validate
"""

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import logging utilities from observability_platform
from observability_platform.src.jsonl_logger import (
    log_record,
    log_records,
    new_id,
    now_iso,
    validate_log,
)
from observability_platform.src.data_classes import (
    Scenario,
    ScenarioStep,
    StepExecutionResult,
)

# Import existing extraction test runner
from scripts.run_extraction_tests import (
    apply_profile_env_vars,
    get_profile,
    load_profiles,
    PROFILE_SUFFIXES,
)


# =============================================================================
# Configuration
# =============================================================================

PROFILES = ["baseline", "current", "moderate", "aggressive"]


# =============================================================================
# Scenario Definition
# =============================================================================

def get_extraction_evaluation_scenario() -> Scenario:
    """
    Define the 9-step extraction evaluation scenario.
    
    Returns:
        Scenario with all 9 steps for extraction evaluation
    """
    steps = []
    order = 1
    
    # Steps 1-8: Apply config + run extraction for each profile
    for profile in PROFILES:
        # Apply configuration step
        steps.append(ScenarioStep(
            step_id=f"step_apply_{profile}_config",
            name=f"Apply {profile.title()} Configuration",
            order=order,
            function="apply_profile_env_vars",
            module="scripts.run_extraction_tests",
            service_id="svc_statistical_extractor",
        ))
        order += 1
        
        # Run extraction step
        steps.append(ScenarioStep(
            step_id=f"step_run_{profile}_extraction",
            name=f"Run {profile.title()} Extraction",
            order=order,
            function="run_profile_pipeline",
            module="scripts.run_extraction_tests",
            entity_outputs_keys=[f"aggregate_{PROFILE_SUFFIXES[profile]}.json"],
            service_id="svc_metadata_extractor",
        ))
        order += 1
    
    # Step 9: LLM Comparative Evaluation
    steps.append(ScenarioStep(
        step_id="step_run_llm_comparative",
        name="Run LLM Comparative Evaluation",
        order=9,
        function="run_comparative_evaluation",
        module="scripts.llm_evaluation",
        entity_outputs_keys=["llm_comparative_evaluation"],
        service_id="svc_llm_enhancer",
    ))
    
    return Scenario(
        scenario_id="scenario_extraction_evaluation",
        name="Extraction Profile Evaluation",
        description="Run 4 extraction profiles and evaluate with LLMs (Strategy B)",
        steps=steps,
        process_id="proc_extraction_evaluation",
    )


# =============================================================================
# Step Execution
# =============================================================================

def execute_step(step: ScenarioStep, context: Dict[str, Any]) -> StepExecutionResult:
    """
    Execute a single scenario step.
    
    Args:
        step: The step to execute
        context: Shared context between steps
        
    Returns:
        StepExecutionResult with status, result, and timing
    """
    start_time = time.time()
    trace_id = context.get("trace_id", new_id("trc"))
    
    # Log step start
    log_record({
        "record_type": "step_start",
        "trace_id": trace_id,
        "step_id": step.step_id,
        "step_name": step.name,
        "order": step.order,
        "timestamp": now_iso(),
    })
    
    try:
        result: Any = None
        
        # Handle different step types
        if "apply" in step.step_id and "config" in step.step_id:
            # Configuration step
            profile_name = step.step_id.replace("step_apply_", "").replace("_config", "")
            profile = get_profile(profile_name)
            apply_profile_env_vars(profile)
            result = {"profile": profile_name, "applied": True}
            
        elif "extraction" in step.step_id:
            # Extraction step - placeholder for actual execution
            # In real implementation, this would call run_profile_pipeline
            profile_name = step.step_id.replace("step_run_", "").replace("_extraction", "")
            result = {
                "profile": profile_name,
                "output": f"aggregate_{PROFILE_SUFFIXES.get(profile_name, 'UNKNOWN')}.json",
                "status": "simulated",  # Would be "completed" in real run
            }
            
        elif "llm_comparative" in step.step_id:
            # LLM evaluation step - placeholder
            result = {
                "profiles_compared": PROFILES,
                "status": "simulated",
            }
        
        latency_ms = (time.time() - start_time) * 1000
        
        # Log step success
        log_record({
            "record_type": "step_end",
            "trace_id": trace_id,
            "step_id": step.step_id,
            "status": "success",
            "latency_ms": latency_ms,
            "timestamp": now_iso(),
        })
        
        return StepExecutionResult(
            status="success",
            result=result,
            latency_ms=latency_ms,
        )
        
    except Exception as e:
        latency_ms = (time.time() - start_time) * 1000
        
        # Log step failure
        log_record({
            "record_type": "step_end",
            "trace_id": trace_id,
            "step_id": step.step_id,
            "status": "failed",
            "error": str(e),
            "latency_ms": latency_ms,
            "timestamp": now_iso(),
        })
        
        return StepExecutionResult(
            status="failed",
            error=str(e),
            latency_ms=latency_ms,
        )


def run_scenario(scenario: Scenario) -> Dict[str, Any]:
    """
    Execute a complete scenario with all steps.
    
    Args:
        scenario: The scenario to run
        
    Returns:
        Dictionary with execution results for all steps
    """
    trace_id = new_id("trc")
    context = {"trace_id": trace_id}
    results: Dict[str, StepExecutionResult] = {}
    
    # Log scenario start
    log_record({
        "record_type": "scenario_start",
        "trace_id": trace_id,
        "scenario_id": scenario.scenario_id,
        "scenario_name": scenario.name,
        "total_steps": len(scenario.steps),
        "timestamp": now_iso(),
    })
    
    print(f"\n{'='*60}")
    print(f"Running Scenario: {scenario.name}")
    print(f"{'='*60}")
    
    start_time = time.time()
    failed = False
    
    # Execute each step in order
    for step in sorted(scenario.steps, key=lambda s: s.order):
        print(f"\n[{step.order}/{len(scenario.steps)}] {step.name}...")
        
        result = execute_step(step, context)
        results[step.step_id] = result
        
        if result.status == "success":
            print(f"    ✓ Completed in {result.latency_ms:.1f}ms")
        else:
            print(f"    ✗ Failed: {result.error}")
            failed = True
            break  # Stop on first failure
    
    total_latency = (time.time() - start_time) * 1000
    
    # Log scenario end
    log_record({
        "record_type": "scenario_end",
        "trace_id": trace_id,
        "scenario_id": scenario.scenario_id,
        "status": "failed" if failed else "success",
        "total_latency_ms": total_latency,
        "steps_completed": len(results),
        "timestamp": now_iso(),
    })
    
    print(f"\n{'='*60}")
    print(f"Scenario {'FAILED' if failed else 'COMPLETED'} in {total_latency:.1f}ms")
    print(f"Steps completed: {len(results)}/{len(scenario.steps)}")
    print(f"{'='*60}\n")
    
    return {
        "trace_id": trace_id,
        "scenario_id": scenario.scenario_id,
        "status": "failed" if failed else "success",
        "total_latency_ms": total_latency,
        "results": {k: {"status": v.status, "latency_ms": v.latency_ms} for k, v in results.items()},
    }


# =============================================================================
# CLI
# =============================================================================

def main() -> None:
    """Main entry point for extraction evaluation."""
    parser = argparse.ArgumentParser(
        description="Run extraction profile evaluation workflow"
    )
    parser.add_argument(
        "--run-all",
        action="store_true",
        help="Run the complete 9-step extraction evaluation",
    )
    parser.add_argument(
        "--profile",
        choices=PROFILES,
        help="Run extraction for a single profile",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate the JSONL log file",
    )
    parser.add_argument(
        "--list-steps",
        action="store_true",
        help="List all steps in the evaluation scenario",
    )
    
    args = parser.parse_args()
    
    if args.validate:
        result = validate_log()
        print("\n📊 Log Validation Results:")
        print(f"   Total records: {result['total_records']}")
        print(f"   Error count: {result['error_count']}")
        if result['record_types']:
            print("   Record types:")
            for rtype, count in sorted(result['record_types'].items()):
                print(f"      {rtype}: {count}")
        return
    
    if args.list_steps:
        scenario = get_extraction_evaluation_scenario()
        print(f"\n📋 {scenario.name}")
        print(f"   {scenario.description}")
        print(f"\nSteps ({len(scenario.steps)}):")
        for step in sorted(scenario.steps, key=lambda s: s.order):
            print(f"   {step.order}. {step.name}")
        return
    
    if args.run_all:
        scenario = get_extraction_evaluation_scenario()
        run_scenario(scenario)
        return
    
    if args.profile:
        print(f"\n🔧 Running single profile: {args.profile}")
        # Create a mini-scenario with just this profile
        profile = get_profile(args.profile)
        apply_profile_env_vars(profile)
        print(f"   ✓ Applied {args.profile} configuration")
        # Would run extraction here
        return
    
    parser.print_help()


if __name__ == "__main__":
    main()
