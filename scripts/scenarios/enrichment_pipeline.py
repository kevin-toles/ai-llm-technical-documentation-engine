"""
Enrichment Pipeline Scenario
============================

Full enrichment pipeline from metadata to aggregate.
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from observability_platform.src.data_classes import Scenario, ScenarioStep


def get_enrichment_pipeline_scenario() -> Scenario:
    """
    Define the full enrichment pipeline scenario.
    
    Steps:
        1: Load book metadata
        2: Load taxonomy
        3: Build chapter corpus
        4: Compute similarity matrix
        5: Enrich chapters with cross-references
        6: Create aggregate for evaluation
    
    Returns:
        Scenario for full enrichment pipeline
    """
    steps = [
        ScenarioStep(
            step_id="step_load_metadata",
            name="Load Book Metadata",
            order=1,
            function="load_metadata",
            module="workflows.metadata_enrichment.scripts.enrich_metadata_per_book",
            entity_inputs=[{"entity_id": "entity_book_metadata", "instance_id": "target_book"}],
            service_id="svc_metadata_enricher"
        ),
        ScenarioStep(
            step_id="step_load_taxonomy",
            name="Load Taxonomy",
            order=2,
            function="load_taxonomy",
            module="workflows.metadata_enrichment.scripts.enrich_metadata_per_book",
            entity_inputs=[{"entity_id": "entity_taxonomy", "instance_id": "target_taxonomy"}],
            service_id="svc_taxonomy_builder"
        ),
        ScenarioStep(
            step_id="step_build_corpus",
            name="Build Chapter Corpus",
            order=3,
            function="build_chapter_corpus",
            module="workflows.metadata_enrichment.scripts.enrich_metadata_per_book",
            service_id="svc_metadata_enricher"
        ),
        ScenarioStep(
            step_id="step_compute_similarity",
            name="Compute Similarity Matrix",
            order=4,
            function="compute_similarity_matrix",
            module="workflows.metadata_enrichment.scripts.enrich_metadata_per_book",
            service_id="svc_metadata_enricher"
        ),
        ScenarioStep(
            step_id="step_enrich_chapters",
            name="Enrich Chapters",
            order=5,
            function="enrich_metadata",
            module="workflows.metadata_enrichment.scripts.enrich_metadata_per_book",
            entity_outputs_keys=["enriched_metadata_file"],
            service_id="svc_metadata_enricher"
        ),
        ScenarioStep(
            step_id="step_create_aggregate",
            name="Create Aggregate",
            order=6,
            function="create_aggregate",
            module="scripts.run_extraction_tests",
            entity_outputs_keys=["aggregate_file"],
            service_id="svc_metadata_enricher"
        ),
    ]
    
    return Scenario(
        scenario_id="scenario_enrichment_pipeline",
        name="Full Enrichment Pipeline",
        description="Run complete enrichment from metadata to aggregate",
        steps=steps,
        process_id="proc_enrichment",
    )
