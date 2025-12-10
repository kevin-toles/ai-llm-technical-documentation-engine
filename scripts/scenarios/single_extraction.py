"""
Single Extraction Scenario
==========================

Scenario for extracting metadata from a single book's JSON text.
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from observability_platform.src.data_classes import Scenario, ScenarioStep


def get_single_extraction_scenario() -> Scenario:
    """
    Define a single book metadata extraction scenario.
    
    Steps:
        1: Load JSON text from prior PDF conversion
        2: Extract metadata (keywords, concepts, summaries)
    
    Returns:
        Scenario for single book extraction
    """
    steps = [
        ScenarioStep(
            step_id="step_load_json_text",
            name="Load JSON Text",
            order=1,
            function="load_source_json",
            module="scripts.run_extraction_tests",
            entity_inputs=[{"entity_id": "entity_json_text", "instance_id": "target_book"}],
            service_id="svc_pdf_converter"
        ),
        ScenarioStep(
            step_id="step_extract_metadata",
            name="Extract Metadata",
            order=2,
            function="run_metadata_extraction",
            module="scripts.run_extraction_tests",
            entity_inputs=[{"entity_id": "entity_json_text", "instance_id": "target_book"}],
            entity_outputs_keys=["metadata_file"],
            service_id="svc_metadata_extractor"
        ),
    ]
    
    return Scenario(
        scenario_id="scenario_single_extraction",
        name="Single Book Metadata Extraction",
        description="Extract metadata from a single book's JSON text",
        steps=steps,
        process_id="proc_metadata_extraction",
    )
