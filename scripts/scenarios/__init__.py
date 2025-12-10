"""
Scenario Definitions
====================

Business scenario definitions for the LLM Document Enhancer pipeline.
These define the steps and flow of various workflows.

Scenarios are data structures that describe what to execute.
Execution logic is in the individual runner scripts.
"""

from .extraction_evaluation import get_extraction_evaluation_scenario
from .enrichment_pipeline import get_enrichment_pipeline_scenario
from .single_extraction import get_single_extraction_scenario

__all__ = [
    "get_extraction_evaluation_scenario",
    "get_enrichment_pipeline_scenario",
    "get_single_extraction_scenario",
]
