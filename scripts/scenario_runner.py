#!/usr/bin/env python3
"""
Scenario Runner
===============

Execution engine for running business scenarios with full observability logging.

This module provides:
- Step execution (local Python functions and HTTP requests)
- Scenario orchestration with traceability
- Event logging for each step
- State transition tracking

The scenario definitions themselves are in /scripts/scenarios/.
This module only handles execution logic.

Usage:
    python scripts/scenario_runner.py --run extraction_evaluation
    python scripts/scenario_runner.py --list
    python scripts/scenario_runner.py --log-architecture

Reference: observability_platform/DESIGN_DOCUMENT.md
"""

import argparse
import importlib
import json
import sys
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import from observability_platform (JSONL logging only)
from observability_platform.src.jsonl_logger import (
    log_record,
    log_records,
    new_id,
    now_iso,
    validate_log,
    LOG_FILE,
)
from observability_platform.src.data_classes import (
    Scenario,
    ScenarioStep,
    StepExecutionResult,
)
from observability_platform.src.architecture_context import (
    log_architecture_context,
)

# Import scenario definitions from scripts/scenarios/
from scripts.scenarios import (
    get_extraction_evaluation_scenario,
    get_enrichment_pipeline_scenario,
    get_single_extraction_scenario,
)

# Optional HTTP client
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


# =============================================================================
# Scenario Registry
# =============================================================================

def get_scenario_definitions() -> Dict[str, Scenario]:
    """
    Return all defined business scenarios.
    
    Scenarios are defined in scripts/scenarios/ and imported here.
    """
    return {
        "extraction_evaluation": get_extraction_evaluation_scenario(),
        "single_extraction": get_single_extraction_scenario(),
        "enrichment_pipeline": get_enrichment_pipeline_scenario(),
    }


# =============================================================================
# Step Execution Helpers
# =============================================================================

def execute_local_function(
    module_path: str,
    function_name: str,
    args: Optional[List[Any]] = None,
    kwargs: Optional[Dict[str, Any]] = None
) -> Tuple[bool, Any, float]:
    """
    Execute a local Python function and measure latency.
    
    Returns:
        Tuple of (success, result_or_error, latency_ms)
    """
    args = args or []
    kwargs = kwargs or {}
    
    t0 = time.time()
    
    try:
        module = importlib.import_module(module_path)
        func = getattr(module, function_name)
        result = func(*args, **kwargs)
        elapsed_ms = (time.time() - t0) * 1000
        return True, result, elapsed_ms
        
    except (ModuleNotFoundError, AttributeError, TypeError) as e:
        elapsed_ms = (time.time() - t0) * 1000
        return False, str(e), elapsed_ms
    except Exception as e:
        elapsed_ms = (time.time() - t0) * 1000
        return False, str(e), elapsed_ms


def _execute_local_step(
    step: ScenarioStep,
    step_args: Dict[str, Dict[str, Any]]
) -> StepExecutionResult:
    """Execute a local function step."""
    args_kwargs = step_args.get(step.step_id, {"args": [], "kwargs": {}})
    success, result, latency_ms = execute_local_function(
        step.module or "",
        step.function or "",
        args_kwargs.get("args", []),
        args_kwargs.get("kwargs", {})
    )
    
    if success:
        return StepExecutionResult(
            status="success",
            result=result,
            latency_ms=latency_ms
        )
    else:
        return StepExecutionResult(
            status="failed",
            error=str(result),
            latency_ms=latency_ms
        )


def _execute_http_step(step: ScenarioStep) -> StepExecutionResult:
    """Execute an HTTP request step."""
    if not REQUESTS_AVAILABLE:
        return StepExecutionResult(
            status="skipped",
            error="requests library not available"
        )
    
    t0 = time.time()
    try:
        resp = requests.request(
            step.method or "GET",
            step.url or "",
            json=step.payload,
            timeout=30,
        )
        latency_ms = (time.time() - t0) * 1000
        
        if resp.status_code == step.expected_status:
            try:
                result = resp.json()
            except json.JSONDecodeError:
                result = resp.text
            return StepExecutionResult(
                status="success",
                result=result,
                latency_ms=latency_ms
            )
        else:
            return StepExecutionResult(
                status="failed",
                error=f"HTTP {resp.status_code}",
                latency_ms=latency_ms
            )
    except Exception as e:
        latency_ms = (time.time() - t0) * 1000
        return StepExecutionResult(
            status="failed",
            error=str(e),
            latency_ms=latency_ms
        )


def _execute_step(
    step: ScenarioStep,
    step_args: Dict[str, Dict[str, Any]]
) -> StepExecutionResult:
    """
    Execute a single scenario step.
    
    Dispatches to appropriate executor based on step type.
    """
    if step.function and step.module:
        return _execute_local_step(step, step_args)
    elif step.url and step.method:
        return _execute_http_step(step)
    else:
        return StepExecutionResult(
            status="skipped",
            error="No function or URL defined"
        )


def _update_step_context(
    step: ScenarioStep,
    result: Any,
    step_context: Dict[str, Any]
) -> None:
    """Extract entity outputs from step result into context."""
    if step.entity_outputs_keys and isinstance(result, dict):
        for key in step.entity_outputs_keys:
            if key in result:
                step_context[key] = result[key]


def _log_step_events(
    step: ScenarioStep,
    exec_result: StepExecutionResult,
    trace_id: str,
    scenario_run_id: str,
    step_start_ts: str
) -> None:
    """Log step started and completed events."""
    # Log step started
    log_record({
        "record_type": "event",
        "event_type": "StepStarted",
        "timestamp": step_start_ts,
        "trace_id": trace_id,
        "scenario_run_id": scenario_run_id,
        "step_id": step.step_id,
        "order": step.order,
        "step_name": step.name,
        "service_id": step.service_id,
    })
    
    # Log step completed
    log_record({
        "record_type": "event",
        "event_type": "StepCompleted",
        "timestamp": now_iso(),
        "trace_id": trace_id,
        "scenario_run_id": scenario_run_id,
        "step_id": step.step_id,
        "status": exec_result.status,
        "metrics": {"latency_ms": round(exec_result.latency_ms, 2)},
        "error": exec_result.error,
    })


def _print_step_status(step: ScenarioStep, exec_result: StepExecutionResult) -> None:
    """Print step execution status to console."""
    print(f"\n  [{step.order}] {step.name}")
    
    if exec_result.status == "success":
        status_icon = "✅"
    elif exec_result.status == "skipped":
        status_icon = "⚠️"
    else:
        status_icon = "❌"
    
    print(f"      {status_icon} {exec_result.status} ({exec_result.latency_ms:.0f}ms)")
    
    if exec_result.error:
        print(f"         Error: {exec_result.error[:80]}")


# =============================================================================
# Scenario Execution
# =============================================================================

def log_scenario_definition(scenario: Scenario) -> None:
    """Log a scenario definition record."""
    log_record({
        "record_type": "scenario_definition",
        "scenario_id": scenario.scenario_id,
        "name": scenario.name,
        "description": scenario.description,
        "process_id": scenario.process_id,
        "trigger_type": scenario.trigger_type,
        "trigger_source": scenario.trigger_source,
        "steps": [
            {
                "step_id": s.step_id,
                "order": s.order,
                "name": s.name,
            }
            for s in scenario.steps
        ],
    })


def run_scenario(
    scenario: Scenario,
    step_args: Optional[Dict[str, Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Run a scenario end-to-end with full observability logging.
    
    Args:
        scenario: Scenario to execute
        step_args: Optional dict mapping step_id -> {args, kwargs} for function calls
        
    Returns:
        Scenario run result with all step outcomes
    """
    step_args = step_args or {}
    
    # Generate IDs
    trace_id = new_id("trc")
    scenario_run_id = new_id("sr")
    started_at = now_iso()
    
    print(f"\n🚀 Running scenario: {scenario.name}")
    print(f"   Trace ID: {trace_id}")
    print(f"   Scenario Run ID: {scenario_run_id}")
    
    # Log scenario definition (idempotent)
    log_scenario_definition(scenario)
    
    # Log scenario_run start
    log_record({
        "record_type": "scenario_run",
        "scenario_run_id": scenario_run_id,
        "scenario_id": scenario.scenario_id,
        "trace_id": trace_id,
        "started_at": started_at,
        "status": "running",
    })
    
    # Execute all steps
    step_context: Dict[str, Any] = {}
    overall_status = "success"
    step_results: List[Dict[str, Any]] = []
    
    for step in scenario.steps:
        step_start_ts = now_iso()
        
        # Execute step
        exec_result = _execute_step(step, step_args)
        
        # Update context with entity outputs
        if exec_result.status == "success":
            _update_step_context(step, exec_result.result, step_context)
        else:
            overall_status = "failed"
        
        # Log events
        _log_step_events(step, exec_result, trace_id, scenario_run_id, step_start_ts)
        
        # Print status
        _print_step_status(step, exec_result)
        
        # Collect result
        step_results.append({
            "step_id": step.step_id,
            "status": exec_result.status,
            "latency_ms": exec_result.latency_ms,
            "error": exec_result.error,
        })
    
    # Log scenario_run completion
    ended_at = now_iso()
    log_record({
        "record_type": "scenario_run",
        "scenario_run_id": scenario_run_id,
        "scenario_id": scenario.scenario_id,
        "trace_id": trace_id,
        "started_at": started_at,
        "ended_at": ended_at,
        "status": overall_status,
    })
    
    # Summary
    status_icon = "✅" if overall_status == "success" else "❌"
    print(f"\n  {status_icon} Scenario {overall_status}")
    print(f"  Duration: {started_at} → {ended_at}")
    
    return {
        "scenario_run_id": scenario_run_id,
        "trace_id": trace_id,
        "scenario_id": scenario.scenario_id,
        "status": overall_status,
        "started_at": started_at,
        "ended_at": ended_at,
        "step_results": step_results,
        "step_context": step_context,
    }


# =============================================================================
# State Transition Logging
# =============================================================================

def log_state_transition(
    entity_id: str,
    instance_id: str,
    previous_state: str,
    new_state: str,
    trace_id: str,
    service_id: str,
    reason: str = ""
) -> None:
    """Log an entity state transition."""
    log_record({
        "record_type": "state_transition",
        "entity_id": entity_id,
        "entity_instance_id": instance_id,
        "previous_state": previous_state,
        "new_state": new_state,
        "timestamp": now_iso(),
        "trace_id": trace_id,
        "service_id": service_id,
        "reason": reason,
    })


# =============================================================================
# Log Validation (delegates to jsonl_logger)
# =============================================================================

def print_log_summary() -> None:
    """Print summary of the log file."""
    stats = validate_log()
    
    if "error" in stats:
        print(f"\n❌ {stats['error']}")
        return
    
    print(f"\n📊 Log File Summary: {LOG_FILE}")
    print("=" * 60)
    print(f"  Total records: {stats['total_records']}")
    print(f"  Error count: {stats['error_count']}")
    
    if stats.get("record_types"):
        print("\n  Record types:")
        for rtype, count in sorted(stats["record_types"].items()):
            print(f"    {rtype}: {count}")


# =============================================================================
# CLI
# =============================================================================

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scenario Runner - Execute business scenarios with observability"
    )
    
    parser.add_argument(
        "--run",
        choices=["extraction_evaluation", "single_extraction", "enrichment_pipeline"],
        help="Run a specific scenario"
    )
    
    parser.add_argument(
        "--run-all",
        action="store_true",
        help="Run all defined scenarios"
    )
    
    parser.add_argument(
        "--log-architecture",
        action="store_true",
        help="Log architecture context only (services, entities, etc.)"
    )
    
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate and summarize the log file"
    )
    
    parser.add_argument(
        "--clear-log",
        action="store_true",
        help="Clear the existing log file"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all defined scenarios"
    )
    
    args = parser.parse_args()
    
    if args.clear_log:
        if LOG_FILE.exists():
            LOG_FILE.unlink()
            print(f"✅ Cleared log file: {LOG_FILE}")
        else:
            print(f"ℹ️  Log file does not exist: {LOG_FILE}")
        return
    
    if args.validate:
        print_log_summary()
        return
    
    if args.list:
        scenarios = get_scenario_definitions()
        print("\n📋 Available Scenarios:")
        print("=" * 60)
        for name, scenario in scenarios.items():
            print(f"\n  {name}:")
            print(f"    Name: {scenario.name}")
            print(f"    Description: {scenario.description}")
            print(f"    Steps: {len(scenario.steps)}")
        return
    
    if args.log_architecture:
        log_architecture_context()
        print(f"\n✅ Architecture context logged to: {LOG_FILE}")
        return
    
    if args.run:
        # First log architecture context
        log_architecture_context()
        
        # Get and run scenario
        scenarios = get_scenario_definitions()
        scenario = scenarios.get(args.run)
        
        if not scenario:
            print(f"❌ Unknown scenario: {args.run}")
            return
        
        run_scenario(scenario)
        print(f"\n✅ Scenario logged to: {LOG_FILE}")
        return
    
    if args.run_all:
        # First log architecture context
        log_architecture_context()
        
        # Run all scenarios
        scenarios = get_scenario_definitions()
        
        for name, scenario in scenarios.items():
            print(f"\n{'='*60}")
            run_scenario(scenario)
        
        print(f"\n✅ All scenarios logged to: {LOG_FILE}")
        print_log_summary()
        return
    
    # Default: show help
    parser.print_help()


if __name__ == "__main__":
    main()
