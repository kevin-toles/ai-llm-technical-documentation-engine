#!/usr/bin/env python3
"""
System Observability Runner
===========================

A synthetic user runner + logger that:
1. Defines and executes business scenarios (front-end driver)
2. Records all events, metrics, and state transitions to JSONL
3. Captures architecture context (services, interfaces, entities, integrations)
4. Provides replayable and analyzable observability data

Output File: system_observability_log.jsonl
- One JSON object per line
- Multiple record types in single file
- Append-only for replay capability

Usage:
    python system_observability_runner.py --run-scenario guideline_generation
    python system_observability_runner.py --run-all
    python system_observability_runner.py --log-architecture
    python system_observability_runner.py --validate-log

Reference: User-provided observability specification
"""

import argparse
import json
import os
import platform
import socket
import subprocess
import sys
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

# Optional HTTP client
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# =============================================================================
# Configuration
# =============================================================================

LOG_FILE = PROJECT_ROOT / "logs" / "observability" / "system_observability_log.jsonl"
SCHEMA_VERSION = "1.0.0"
GENERATOR_ID = "frontend_driver_v1"


# =============================================================================
# ID Generation Utilities
# =============================================================================

def new_id(prefix: str) -> str:
    """Generate a unique ID with prefix (e.g., 'trc_01HF...')."""
    return f"{prefix}_{uuid.uuid4().hex[:16]}"


def now_iso() -> str:
    """Return current timestamp in ISO format."""
    return datetime.now(tz=None).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


# =============================================================================
# JSONL Logging
# =============================================================================

def ensure_log_directory() -> None:
    """Create log directory if it doesn't exist."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


def log_record(record: Dict[str, Any]) -> None:
    """
    Append a single JSON record to the JSONL log file.
    
    Each record is one line with no pretty-printing.
    """
    ensure_log_directory()
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, separators=(",", ":"), default=str) + "\n")


def log_records(records: List[Dict[str, Any]]) -> None:
    """Append multiple records to the JSONL log file."""
    ensure_log_directory()
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, separators=(",", ":"), default=str) + "\n")


# =============================================================================
# Data Classes for Scenarios
# =============================================================================

@dataclass
class ScenarioStep:
    """Definition of a single step within a scenario."""
    step_id: str
    name: str
    order: int
    # For HTTP-based steps
    method: Optional[str] = None
    url: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None
    expected_status: int = 200
    # For local execution steps
    function: Optional[str] = None
    module: Optional[str] = None
    # Entity mappings
    entity_inputs: Optional[List[Dict[str, str]]] = None
    entity_outputs_keys: Optional[List[str]] = None
    # Service mappings
    service_id: Optional[str] = None
    interface_id: Optional[str] = None


@dataclass
class Scenario:
    """Definition of a complete business scenario."""
    scenario_id: str
    name: str
    description: str
    steps: List[ScenarioStep] = field(default_factory=list)
    process_id: Optional[str] = None
    trigger_type: str = "user_action"
    trigger_source: str = "observability_runner"


@dataclass
class Component:
    """Definition of a system component (service, endpoint, database, etc.)."""
    component_id: str
    component_kind: str  # Service, Endpoint, Database, ExternalSystem, InfraNode, Container
    name: str
    description: str = ""
    # For services
    owner_team: Optional[str] = None
    inputs: Optional[List[str]] = None
    outputs: Optional[List[str]] = None
    # For endpoints
    service_id: Optional[str] = None
    protocol: Optional[str] = None
    method: Optional[str] = None
    path: Optional[str] = None
    consumes: Optional[List[str]] = None
    produces: Optional[List[str]] = None
    # For databases
    engine: Optional[str] = None
    # For external systems
    contact_type: Optional[str] = None
    base_url: Optional[str] = None
    # For containers
    node_id: Optional[str] = None
    image: Optional[str] = None
    environment: Optional[str] = None
    # For infra nodes
    provider: Optional[str] = None
    region: Optional[str] = None
    zone: Optional[str] = None


@dataclass
class Relationship:
    """Definition of a relationship between components."""
    from_id: str
    to_id: str
    relationship_type: str  # EXPOSES, WRITES_TO, READS_FROM, INTEGRATES_WITH, RUNS_ON


@dataclass
class EntityDefinition:
    """Definition of a domain entity."""
    entity_id: str
    name: str
    description: str = ""
    states: Optional[List[str]] = None
    primary_key: Optional[str] = None
    schema_ref: Optional[str] = None


@dataclass
class ProcessDefinition:
    """Definition of a business process."""
    process_id: str
    name: str
    description: str = ""
    trigger_type: str = "user_action"
    trigger_source: str = "frontend_app"
    success_criteria: str = ""
    failure_criteria: str = ""


# =============================================================================
# Architecture Context: Define all components, services, entities
# =============================================================================

def get_architecture_context() -> Dict[str, List[Any]]:
    """
    Return complete architecture context for the LLM Document Enhancer.
    
    This is static configuration that describes the system architecture.
    """
    
    # ==========
    # SERVICES
    # ==========
    services = [
        Component(
            component_id="svc_pdf_converter",
            component_kind="Service",
            name="PDF to JSON Converter",
            description="Converts PDF documents to structured JSON with chapter segmentation",
            owner_team="document-processing",
            inputs=["entity_pdf_document"],
            outputs=["entity_json_text", "entity_chapter_segments"]
        ),
        Component(
            component_id="svc_metadata_extractor",
            component_kind="Service",
            name="Metadata Extraction Service",
            description="Extracts keywords, concepts, and summaries using YAKE and Summa",
            owner_team="nlp-platform",
            inputs=["entity_json_text", "entity_chapter_segments"],
            outputs=["entity_book_metadata"]
        ),
        Component(
            component_id="svc_taxonomy_builder",
            component_kind="Service",
            name="Taxonomy Builder Service",
            description="Builds hierarchical taxonomy from extracted metadata",
            owner_team="knowledge-graph",
            inputs=["entity_book_metadata"],
            outputs=["entity_taxonomy"]
        ),
        Component(
            component_id="svc_metadata_enricher",
            component_kind="Service",
            name="Metadata Enrichment Service",
            description="Enriches metadata with cross-book references using TF-IDF similarity",
            owner_team="nlp-platform",
            inputs=["entity_book_metadata", "entity_taxonomy"],
            outputs=["entity_enriched_metadata"]
        ),
        Component(
            component_id="svc_guideline_generator",
            component_kind="Service",
            name="Guideline Generator Service",
            description="Generates base guidelines from enriched metadata",
            owner_team="content-generation",
            inputs=["entity_enriched_metadata"],
            outputs=["entity_base_guideline"]
        ),
        Component(
            component_id="svc_llm_enhancer",
            component_kind="Service",
            name="LLM Enhancement Service",
            description="Enhances guidelines using multiple LLM providers",
            owner_team="llm-platform",
            inputs=["entity_base_guideline"],
            outputs=["entity_enhanced_guideline"]
        ),
        Component(
            component_id="svc_statistical_extractor",
            component_kind="Service",
            name="Statistical Extractor Adapter",
            description="Adapts YAKE and Summa libraries for keyword/concept extraction",
            owner_team="nlp-platform",
            inputs=["entity_chapter_text"],
            outputs=["entity_keywords", "entity_concepts"]
        ),
    ]
    
    # ==========
    # ENDPOINTS (for future HTTP API)
    # ==========
    endpoints = [
        Component(
            component_id="ep_pdf_upload",
            component_kind="Endpoint",
            name="PDF Upload Endpoint",
            description="Accepts PDF file uploads for processing",
            service_id="svc_pdf_converter",
            protocol="http",
            method="POST",
            path="/api/v1/documents/upload",
            consumes=["entity_pdf_document"],
            produces=["entity_json_text"]
        ),
        Component(
            component_id="ep_extract_metadata",
            component_kind="Endpoint",
            name="Metadata Extraction Endpoint",
            description="Triggers metadata extraction for a document",
            service_id="svc_metadata_extractor",
            protocol="http",
            method="POST",
            path="/api/v1/metadata/extract",
            consumes=["entity_json_text"],
            produces=["entity_book_metadata"]
        ),
        Component(
            component_id="ep_enrich_metadata",
            component_kind="Endpoint",
            name="Metadata Enrichment Endpoint",
            description="Triggers cross-book enrichment",
            service_id="svc_metadata_enricher",
            protocol="http",
            method="POST",
            path="/api/v1/metadata/enrich",
            consumes=["entity_book_metadata", "entity_taxonomy"],
            produces=["entity_enriched_metadata"]
        ),
        Component(
            component_id="ep_generate_guideline",
            component_kind="Endpoint",
            name="Guideline Generation Endpoint",
            description="Generates base guideline from enriched metadata",
            service_id="svc_guideline_generator",
            protocol="http",
            method="POST",
            path="/api/v1/guidelines/generate",
            consumes=["entity_enriched_metadata"],
            produces=["entity_base_guideline"]
        ),
        Component(
            component_id="ep_enhance_guideline",
            component_kind="Endpoint",
            name="LLM Enhancement Endpoint",
            description="Enhances guideline using LLMs",
            service_id="svc_llm_enhancer",
            protocol="http",
            method="POST",
            path="/api/v1/guidelines/enhance",
            consumes=["entity_base_guideline"],
            produces=["entity_enhanced_guideline"]
        ),
    ]
    
    # ==========
    # DATABASES
    # ==========
    databases = [
        Component(
            component_id="db_document_store",
            component_kind="Database",
            name="Document Store",
            description="Stores PDF documents and JSON text outputs",
            engine="filesystem"
        ),
        Component(
            component_id="db_metadata_store",
            component_kind="Database",
            name="Metadata Store",
            description="Stores extracted metadata JSON files",
            engine="filesystem"
        ),
        Component(
            component_id="db_taxonomy_store",
            component_kind="Database",
            name="Taxonomy Store",
            description="Stores taxonomy JSON files",
            engine="filesystem"
        ),
        Component(
            component_id="db_guideline_store",
            component_kind="Database",
            name="Guideline Store",
            description="Stores generated guideline documents",
            engine="filesystem"
        ),
        Component(
            component_id="db_llm_cache",
            component_kind="Database",
            name="LLM Response Cache",
            description="Caches LLM API responses",
            engine="filesystem"
        ),
    ]
    
    # ==========
    # EXTERNAL SYSTEMS
    # ==========
    external_systems = [
        Component(
            component_id="ext_openai_api",
            component_kind="ExternalSystem",
            name="OpenAI API",
            description="GPT-4o LLM provider",
            contact_type="http",
            base_url="https://api.openai.com"
        ),
        Component(
            component_id="ext_anthropic_api",
            component_kind="ExternalSystem",
            name="Anthropic API",
            description="Claude LLM provider",
            contact_type="http",
            base_url="https://api.anthropic.com"
        ),
        Component(
            component_id="ext_gemini_api",
            component_kind="ExternalSystem",
            name="Google Gemini API",
            description="Gemini LLM provider",
            contact_type="http",
            base_url="https://generativelanguage.googleapis.com"
        ),
        Component(
            component_id="ext_deepseek_api",
            component_kind="ExternalSystem",
            name="DeepSeek API",
            description="DeepSeek LLM provider",
            contact_type="http",
            base_url="https://api.deepseek.com"
        ),
    ]
    
    # ==========
    # RELATIONSHIPS
    # ==========
    relationships = [
        # Services expose endpoints
        Relationship("svc_pdf_converter", "ep_pdf_upload", "EXPOSES"),
        Relationship("svc_metadata_extractor", "ep_extract_metadata", "EXPOSES"),
        Relationship("svc_metadata_enricher", "ep_enrich_metadata", "EXPOSES"),
        Relationship("svc_guideline_generator", "ep_generate_guideline", "EXPOSES"),
        Relationship("svc_llm_enhancer", "ep_enhance_guideline", "EXPOSES"),
        
        # Services write to databases
        Relationship("svc_pdf_converter", "db_document_store", "WRITES_TO"),
        Relationship("svc_metadata_extractor", "db_metadata_store", "WRITES_TO"),
        Relationship("svc_taxonomy_builder", "db_taxonomy_store", "WRITES_TO"),
        Relationship("svc_guideline_generator", "db_guideline_store", "WRITES_TO"),
        Relationship("svc_llm_enhancer", "db_llm_cache", "WRITES_TO"),
        
        # Services read from databases
        Relationship("svc_metadata_extractor", "db_document_store", "READS_FROM"),
        Relationship("svc_metadata_enricher", "db_metadata_store", "READS_FROM"),
        Relationship("svc_metadata_enricher", "db_taxonomy_store", "READS_FROM"),
        Relationship("svc_guideline_generator", "db_metadata_store", "READS_FROM"),
        Relationship("svc_llm_enhancer", "db_llm_cache", "READS_FROM"),
        
        # LLM enhancer integrates with external APIs
        Relationship("svc_llm_enhancer", "ext_openai_api", "INTEGRATES_WITH"),
        Relationship("svc_llm_enhancer", "ext_anthropic_api", "INTEGRATES_WITH"),
        Relationship("svc_llm_enhancer", "ext_gemini_api", "INTEGRATES_WITH"),
        Relationship("svc_llm_enhancer", "ext_deepseek_api", "INTEGRATES_WITH"),
    ]
    
    # ==========
    # DOMAIN ENTITIES
    # ==========
    entities = [
        EntityDefinition(
            entity_id="entity_pdf_document",
            name="PDF Document",
            description="Source PDF file for processing",
            states=["uploaded", "processing", "converted", "failed"],
            primary_key="document_id"
        ),
        EntityDefinition(
            entity_id="entity_json_text",
            name="JSON Text",
            description="Extracted text from PDF in JSON format",
            states=["pending", "extracted", "validated"],
            primary_key="json_id"
        ),
        EntityDefinition(
            entity_id="entity_chapter_segments",
            name="Chapter Segments",
            description="Identified chapter boundaries with page ranges",
            states=["detected", "validated"],
            primary_key="segment_id"
        ),
        EntityDefinition(
            entity_id="entity_book_metadata",
            name="Book Metadata",
            description="Extracted keywords, concepts, summaries per chapter",
            states=["pending", "extracted", "validated"],
            primary_key="metadata_id"
        ),
        EntityDefinition(
            entity_id="entity_taxonomy",
            name="Taxonomy",
            description="Hierarchical classification of topics and concepts",
            states=["pending", "built", "validated"],
            primary_key="taxonomy_id"
        ),
        EntityDefinition(
            entity_id="entity_enriched_metadata",
            name="Enriched Metadata",
            description="Metadata with cross-book references and topic clusters",
            states=["pending", "enriched", "validated"],
            primary_key="enriched_id"
        ),
        EntityDefinition(
            entity_id="entity_base_guideline",
            name="Base Guideline",
            description="Generated guideline document before LLM enhancement",
            states=["pending", "generated", "validated"],
            primary_key="guideline_id"
        ),
        EntityDefinition(
            entity_id="entity_enhanced_guideline",
            name="Enhanced Guideline",
            description="LLM-enhanced guideline document",
            states=["pending", "enhanced", "validated", "failed"],
            primary_key="enhanced_id"
        ),
        EntityDefinition(
            entity_id="entity_aggregate",
            name="Evaluation Aggregate",
            description="Aggregated extraction metrics for LLM evaluation",
            states=["pending", "created", "validated"],
            primary_key="aggregate_id"
        ),
    ]
    
    # ==========
    # BUSINESS PROCESSES
    # ==========
    processes = [
        ProcessDefinition(
            process_id="proc_document_ingestion",
            name="Document Ingestion",
            description="Ingest PDF document and convert to structured JSON",
            trigger_type="user_action",
            trigger_source="frontend_app",
            success_criteria="JSON text created with chapter segments",
            failure_criteria="PDF conversion fails or no chapters detected"
        ),
        ProcessDefinition(
            process_id="proc_metadata_extraction",
            name="Metadata Extraction",
            description="Extract keywords, concepts, summaries from document",
            trigger_type="internal_event",
            trigger_source="document_ingestion",
            success_criteria="Metadata JSON created with keywords and concepts",
            failure_criteria="Extraction produces empty results"
        ),
        ProcessDefinition(
            process_id="proc_taxonomy_building",
            name="Taxonomy Building",
            description="Build hierarchical taxonomy from metadata",
            trigger_type="internal_event",
            trigger_source="metadata_extraction",
            success_criteria="Taxonomy JSON with valid tier structure",
            failure_criteria="Taxonomy generation fails"
        ),
        ProcessDefinition(
            process_id="proc_enrichment",
            name="Metadata Enrichment",
            description="Enrich metadata with cross-book references",
            trigger_type="internal_event",
            trigger_source="taxonomy_building",
            success_criteria="Enriched metadata with related chapters",
            failure_criteria="Enrichment produces no cross-references"
        ),
        ProcessDefinition(
            process_id="proc_guideline_generation",
            name="Guideline Generation",
            description="Full pipeline from metadata to enhanced guideline",
            trigger_type="user_action",
            trigger_source="frontend_app",
            success_criteria="Enhanced guideline document created",
            failure_criteria="Any pipeline step fails"
        ),
        ProcessDefinition(
            process_id="proc_extraction_evaluation",
            name="Extraction Evaluation",
            description="Run 4-profile extraction test with LLM evaluation",
            trigger_type="user_action",
            trigger_source="observability_runner",
            success_criteria="All 4 aggregates created and LLMs evaluate",
            failure_criteria="Profile extraction fails or LLM calls error"
        ),
    ]
    
    return {
        "services": services,
        "endpoints": endpoints,
        "databases": databases,
        "external_systems": external_systems,
        "relationships": relationships,
        "entities": entities,
        "processes": processes,
    }


def get_runtime_context() -> Dict[str, Any]:
    """
    Get current runtime/infrastructure context.
    
    Returns info about the host machine, Python environment, etc.
    """
    return {
        "component_id": f"node_{socket.gethostname().replace('.', '_').lower()}",
        "component_kind": "InfraNode",
        "provider": "local",
        "hostname": socket.gethostname(),
        "platform": platform.system(),
        "platform_version": platform.version(),
        "python_version": platform.python_version(),
        "cwd": str(Path.cwd()),
        "user": os.environ.get("USER", "unknown"),
        "environment": os.environ.get("ENVIRONMENT", "development"),
    }


# =============================================================================
# Log Architecture Context (Static definitions)
# =============================================================================

def log_meta_record() -> None:
    """Log the meta/schema version record."""
    log_record({
        "record_type": "meta",
        "schema_version": SCHEMA_VERSION,
        "generated_by": GENERATOR_ID,
        "created_at": now_iso(),
    })


def log_architecture_context() -> None:
    """
    Log all architecture context records.
    
    This includes services, endpoints, databases, entities, processes, etc.
    Should be called once at the start of a run.
    """
    print("\n📐 Logging architecture context...")
    
    context = get_architecture_context()
    runtime = get_runtime_context()
    
    records = []
    
    # Meta record
    records.append({
        "record_type": "meta",
        "schema_version": SCHEMA_VERSION,
        "generated_by": GENERATOR_ID,
        "created_at": now_iso(),
    })
    
    # Runtime context
    records.append({
        "record_type": "component",
        **runtime,
    })
    
    # Components (services, endpoints, databases, external systems)
    for component_list_name in ["services", "endpoints", "databases", "external_systems"]:
        for component in context[component_list_name]:
            record = {"record_type": "component"}
            record.update({k: v for k, v in asdict(component).items() if v is not None})
            records.append(record)
    
    # Relationships
    for rel in context["relationships"]:
        records.append({
            "record_type": "relationship",
            "from_id": rel.from_id,
            "to_id": rel.to_id,
            "relationship_type": rel.relationship_type,
        })
    
    # Entity definitions
    for entity in context["entities"]:
        record = {"record_type": "entity_definition"}
        record.update({k: v for k, v in asdict(entity).items() if v is not None})
        records.append(record)
    
    # Process definitions
    for process in context["processes"]:
        record = {"record_type": "process_definition"}
        record.update({k: v for k, v in asdict(process).items() if v is not None})
        records.append(record)
    
    # Write all records
    log_records(records)
    
    print(f"  ✅ Logged {len(records)} architecture records")


# =============================================================================
# Scenario Definitions
# =============================================================================

def get_scenario_definitions() -> Dict[str, Scenario]:
    """
    Return all defined business scenarios.
    """
    
    # Scenario 1: Extraction Evaluation (4 profiles)
    extraction_evaluation = Scenario(
        scenario_id="scenario_extraction_evaluation",
        name="Extraction Profile Evaluation",
        description="Run 4 extraction profiles and evaluate with LLMs (Strategy B)",
        process_id="proc_extraction_evaluation",
        steps=[
            ScenarioStep(
                step_id="step_apply_baseline_config",
                name="Apply Baseline Configuration",
                order=1,
                function="apply_profile_env_vars",
                module="scripts.run_extraction_tests",
                entity_inputs=[{"entity_id": "entity_extraction_profile", "instance_id": "baseline"}],
                service_id="svc_statistical_extractor"
            ),
            ScenarioStep(
                step_id="step_run_baseline_extraction",
                name="Run Baseline Extraction",
                order=2,
                function="run_profile_pipeline",
                module="scripts.run_extraction_tests",
                entity_inputs=[{"entity_id": "entity_json_text", "instance_id": "ai_engineering"}],
                entity_outputs_keys=["aggregate_BASELINE.json"],
                service_id="svc_metadata_extractor"
            ),
            ScenarioStep(
                step_id="step_apply_current_config",
                name="Apply Current Configuration",
                order=3,
                function="apply_profile_env_vars",
                module="scripts.run_extraction_tests",
                entity_inputs=[{"entity_id": "entity_extraction_profile", "instance_id": "current"}],
                service_id="svc_statistical_extractor"
            ),
            ScenarioStep(
                step_id="step_run_current_extraction",
                name="Run Current Extraction",
                order=4,
                function="run_profile_pipeline",
                module="scripts.run_extraction_tests",
                entity_inputs=[{"entity_id": "entity_json_text", "instance_id": "ai_engineering"}],
                entity_outputs_keys=["aggregate_CURRENT.json"],
                service_id="svc_metadata_extractor"
            ),
            ScenarioStep(
                step_id="step_apply_moderate_config",
                name="Apply Moderate Configuration",
                order=5,
                function="apply_profile_env_vars",
                module="scripts.run_extraction_tests",
                entity_inputs=[{"entity_id": "entity_extraction_profile", "instance_id": "moderate"}],
                service_id="svc_statistical_extractor"
            ),
            ScenarioStep(
                step_id="step_run_moderate_extraction",
                name="Run Moderate Extraction",
                order=6,
                function="run_profile_pipeline",
                module="scripts.run_extraction_tests",
                entity_inputs=[{"entity_id": "entity_json_text", "instance_id": "ai_engineering"}],
                entity_outputs_keys=["aggregate_MODERATE.json"],
                service_id="svc_metadata_extractor"
            ),
            ScenarioStep(
                step_id="step_apply_aggressive_config",
                name="Apply Aggressive Configuration",
                order=7,
                function="apply_profile_env_vars",
                module="scripts.run_extraction_tests",
                entity_inputs=[{"entity_id": "entity_extraction_profile", "instance_id": "aggressive"}],
                service_id="svc_statistical_extractor"
            ),
            ScenarioStep(
                step_id="step_run_aggressive_extraction",
                name="Run Aggressive Extraction",
                order=8,
                function="run_profile_pipeline",
                module="scripts.run_extraction_tests",
                entity_inputs=[{"entity_id": "entity_json_text", "instance_id": "ai_engineering"}],
                entity_outputs_keys=["aggregate_AGGRESSIVE.json"],
                service_id="svc_metadata_extractor"
            ),
            ScenarioStep(
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
                service_id="svc_llm_enhancer"
            ),
        ]
    )
    
    # Scenario 2: Single Book Metadata Extraction
    single_extraction = Scenario(
        scenario_id="scenario_single_extraction",
        name="Single Book Metadata Extraction",
        description="Extract metadata from a single book's JSON text",
        process_id="proc_metadata_extraction",
        steps=[
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
    )
    
    # Scenario 3: Full Enrichment Pipeline
    enrichment_pipeline = Scenario(
        scenario_id="scenario_enrichment_pipeline",
        name="Full Enrichment Pipeline",
        description="Run complete enrichment from metadata to aggregate",
        process_id="proc_enrichment",
        steps=[
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
    )
    
    return {
        "extraction_evaluation": extraction_evaluation,
        "single_extraction": single_extraction,
        "enrichment_pipeline": enrichment_pipeline,
    }


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


# =============================================================================
# Scenario Execution Engine
# =============================================================================

@dataclass
class StepExecutionResult:
    """Result of executing a single scenario step."""
    status: str  # "success", "failed", "skipped"
    result: Any = None
    error: Optional[str] = None
    latency_ms: float = 0.0


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
    import importlib
    
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
        # Specific import/call errors
        elapsed_ms = (time.time() - t0) * 1000
        return False, str(e), elapsed_ms
    except Exception as e:
        # General execution errors
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
    except requests.RequestException as e:
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


def run_scenario(scenario: Scenario, step_args: Optional[Dict[str, Dict[str, Any]]] = None) -> Dict[str, Any]:
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
        
        # Execute step using extracted helper
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
# Log Validation
# =============================================================================

def validate_log() -> Dict[str, Any]:
    """
    Validate the JSONL log file.
    
    Returns statistics and any validation errors.
    """
    if not LOG_FILE.exists():
        return {"error": f"Log file not found: {LOG_FILE}"}
    
    stats = {
        "total_records": 0,
        "record_types": {},
        "errors": [],
        "file_size_bytes": LOG_FILE.stat().st_size,
    }
    
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
                
            try:
                record = json.loads(line)
                stats["total_records"] += 1
                
                record_type = record.get("record_type", "unknown")
                stats["record_types"][record_type] = stats["record_types"].get(record_type, 0) + 1
                
            except json.JSONDecodeError as e:
                stats["errors"].append({
                    "line": line_num,
                    "error": str(e),
                })
    
    return stats


def print_log_summary() -> None:
    """Print summary of the log file."""
    stats = validate_log()
    
    if "error" in stats:
        print(f"\n❌ {stats['error']}")
        return
    
    print(f"\n📊 Log File Summary: {LOG_FILE}")
    print("=" * 60)
    print(f"  Total records: {stats['total_records']}")
    print(f"  File size: {stats['file_size_bytes']:,} bytes")
    print(f"  Validation errors: {len(stats['errors'])}")
    
    print("\n  Record types:")
    for rtype, count in sorted(stats["record_types"].items()):
        print(f"    {rtype}: {count}")
    
    if stats["errors"]:
        print("\n  ⚠️ Errors:")
        for err in stats["errors"][:5]:
            print(f"    Line {err['line']}: {err['error']}")


# =============================================================================
# Main Entry Point
# =============================================================================

def main() -> None:
    parser = argparse.ArgumentParser(
        description="System Observability Runner - Synthetic user scenarios with JSONL logging"
    )
    
    parser.add_argument(
        "--run-scenario",
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
        "--validate-log",
        action="store_true",
        help="Validate and summarize the log file"
    )
    
    parser.add_argument(
        "--clear-log",
        action="store_true",
        help="Clear the existing log file"
    )
    
    parser.add_argument(
        "--list-scenarios",
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
    
    if args.validate_log:
        print_log_summary()
        return
    
    if args.list_scenarios:
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
    
    if args.run_scenario:
        # First log architecture context
        log_architecture_context()
        
        # Get and run scenario
        scenarios = get_scenario_definitions()
        scenario = scenarios.get(args.run_scenario)
        
        if not scenario:
            print(f"❌ Unknown scenario: {args.run_scenario}")
            return
        
        result = run_scenario(scenario)
        
        print(f"\n✅ Scenario logged to: {LOG_FILE}")
        return
    
    if args.run_all:
        # First log architecture context
        log_architecture_context()
        
        # Run all scenarios
        scenarios = get_scenario_definitions()
        
        for name, scenario in scenarios.items():
            print(f"\n{'='*60}")
            result = run_scenario(scenario)
        
        print(f"\n✅ All scenarios logged to: {LOG_FILE}")
        print_log_summary()
        return
    
    # Default: show help
    parser.print_help()


if __name__ == "__main__":
    main()
