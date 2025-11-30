"""
Extraction Evaluation Scenario
==============================

9-step scenario for running 4 extraction profiles and LLM comparative evaluation.

Reference: docs/testing/KEYWORD_EXTRACTION_TEST_PLAN.md
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from observability_platform.src.data_classes import Scenario, ScenarioStep

# Profile suffix mapping (also in run_extraction_tests.py)
PROFILE_SUFFIXES = {
    "baseline": "BASELINE",
    "current": "CURRENT",
    "moderate": "MODERATE",
    "aggressive": "AGGRESSIVE",
}


def get_extraction_evaluation_scenario() -> Scenario:
    """
    Define the 9-step extraction evaluation scenario.
    
    Steps:
        1-2: Apply Baseline config, Run Baseline extraction
        3-4: Apply Current config, Run Current extraction
        5-6: Apply Moderate config, Run Moderate extraction
        7-8: Apply Aggressive config, Run Aggressive extraction
        9: Run LLM Comparative Evaluation
    
    Returns:
        Scenario with all 9 steps for extraction evaluation
    """
    steps = []
    order = 1
    
    profiles = ["baseline", "current", "moderate", "aggressive"]
    
    # Steps 1-8: Apply config + run extraction for each profile
    for profile in profiles:
        # Apply configuration step
        steps.append(ScenarioStep(
            step_id=f"step_apply_{profile}_config",
            name=f"Apply {profile.title()} Configuration",
            order=order,
            function="apply_profile_env_vars",
            module="scripts.run_extraction_tests",
            entity_inputs=[{"entity_id": "entity_extraction_profile", "instance_id": profile}],
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
            entity_inputs=[{"entity_id": "entity_json_text", "instance_id": "ai_engineering"}],
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
        entity_inputs=[
            {"entity_id": "entity_aggregate", "instance_id": "baseline"},
            {"entity_id": "entity_aggregate", "instance_id": "current"},
            {"entity_id": "entity_aggregate", "instance_id": "moderate"},
            {"entity_id": "entity_aggregate", "instance_id": "aggressive"},
        ],
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
