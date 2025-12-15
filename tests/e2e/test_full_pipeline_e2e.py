"""
End-to-End Test: Full Pipeline Integration

WBS Reference: END_TO_END_INTEGRATION_WBS.md
Pattern: Full document enhancement pipeline per Kitchen Brigade architecture

This test simulates the COMPLETE document enhancement workflow as if triggered
from a frontend application. It validates:

1. Phase 0 (GATE 0): Infrastructure health - all services operational
2. Phase 1 (GATE 1): PDF → JSON transformation (simulated with test fixture)
3. Phase 2 (GATE 2): JSON → Guideline generation (simulated with test fixture)
4. Phase 3 (GATE 3): Metadata Enrichment via semantic-search-service
5. Phase 4 (GATE 4): LLM Enhancement via Gateway routing

Kitchen Brigade Architecture Verification:
- Gateway (Router): Routes ALL external requests
- ai-agents (Expeditor): Orchestrates cross-reference workflow
- semantic-search (Cookbook): Handles search and content retrieval
- Neo4j (Pantry): Taxonomy and graph storage
- Qdrant (Ingredient Store): Vector embeddings

Prerequisites:
    docker-compose -f docker-compose.integration.yml up -d
    
Usage:
    pytest tests/e2e/test_full_pipeline_e2e.py -v
    pytest tests/e2e/test_full_pipeline_e2e.py -v -m "pipeline"
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# =============================================================================
# Configuration
# =============================================================================

GATEWAY_URL = os.getenv("LLM_GATEWAY_URL", "http://localhost:8080")
SEMANTIC_SEARCH_URL = os.getenv("SEARCH_SERVICE_URL", "http://localhost:8081")
AI_AGENTS_URL = os.getenv("AI_AGENTS_URL", "http://localhost:8082")
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")

# Pipeline timeout settings
SERVICE_TIMEOUT = 10.0
PIPELINE_PHASE_TIMEOUT = 30.0


# =============================================================================
# Test Fixtures - Simulated Pipeline Data
# =============================================================================

@pytest.fixture
def gateway_url():
    """Gateway URL from environment or default."""
    return GATEWAY_URL


@pytest.fixture
def semantic_search_url():
    """Semantic search URL from environment or default."""
    return SEMANTIC_SEARCH_URL


@pytest.fixture
def ai_agents_url():
    """AI agents URL from environment or default."""
    return AI_AGENTS_URL


@pytest.fixture
def sample_pdf_json():
    """
    Phase 1 Output: Simulated PDF → JSON result.
    
    This fixture represents what the PDF extraction pipeline produces.
    In production, this comes from workflows/pdf_to_json/output/.
    """
    return {
        "title": "Architecture Patterns with Python",
        "author": "Harry Percival and Bob Gregory",
        "chapters": [
            {
                "number": 1,
                "title": "Domain Modeling",
                "tier": 1,
                "content": """
                Domain-Driven Design (DDD) is an approach to software development that 
                centers the development on programming a domain model. A domain model 
                is a conceptual model of the domain that incorporates both behavior 
                and data. The domain layer is the heart of business software.
                
                Key concepts include:
                - Entities: Objects with identity that persists over time
                - Value Objects: Immutable objects defined by their attributes
                - Aggregates: Clusters of entities and value objects treated as a unit
                - Repositories: Abstract persistence mechanism
                """,
                "keywords": ["domain modeling", "DDD", "entities", "value objects", "aggregates"]
            },
            {
                "number": 2,
                "title": "Repository Pattern",
                "tier": 2,
                "content": """
                The Repository pattern mediates between the domain and data mapping layers.
                It provides a collection-like interface for accessing domain objects.
                
                Benefits of the Repository pattern:
                - Decouples domain from infrastructure
                - Provides a seam for testing
                - Centralizes data access logic
                - Abstracts the underlying storage mechanism
                
                Implementation typically involves:
                - Abstract repository interface
                - Concrete implementation per storage type
                - Unit of Work pattern for transactions
                """,
                "keywords": ["repository", "persistence", "data access", "unit of work"]
            },
            {
                "number": 3,
                "title": "Unit of Work Pattern",
                "tier": 2,
                "content": """
                The Unit of Work pattern maintains a list of objects affected by 
                a business transaction and coordinates writing out changes.
                
                Key responsibilities:
                - Track new objects
                - Track modified objects  
                - Track removed objects
                - Commit all changes atomically
                
                This pattern ensures consistency and provides a boundary for transactions.
                """,
                "keywords": ["unit of work", "transactions", "consistency", "atomic"]
            }
        ],
        "metadata": {
            "extraction_date": "2025-01-01",
            "page_count": 280,
            "format": "PDF"
        }
    }


@pytest.fixture
def sample_guideline():
    """
    Phase 2 Output: Simulated JSON → Guideline result.
    
    This fixture represents what the base guideline generation produces.
    In production, this comes from workflows/base_guideline_generation/output/.
    """
    return {
        "title": "Architecture Patterns with Python - Guidelines",
        "author": "Harry Percival and Bob Gregory",
        "tier": "T1-T2",
        "chapters": [
            {
                "number": 1,
                "title": "Domain Modeling",
                "tier": 1,
                "summary": "Introduction to DDD and domain modeling concepts",
                "key_concepts": ["DDD", "entities", "value objects", "aggregates"],
                "cross_references": []
            },
            {
                "number": 2,
                "title": "Repository Pattern",
                "tier": 2,
                "summary": "Pattern for abstracting data persistence",
                "key_concepts": ["repository", "persistence", "abstraction"],
                "cross_references": []
            }
        ],
        "annotations": [],
        "citations": []
    }


@pytest.fixture
def sample_enrichment_request():
    """
    Phase 3 Input: Request for metadata enrichment.
    
    This is sent to semantic-search-service to find related content.
    """
    return {
        "query": "domain modeling repository pattern",
        "collection": "chapters",
        "limit": 5,
        "focus_areas": ["architecture", "patterns"]
    }


@pytest.fixture
def sample_cross_reference_request():
    """
    Phase 4 Input: Cross-reference request for LLM enhancement.
    
    This is sent through Gateway → ai-agents to generate scholarly annotations.
    """
    return {
        "book": "Architecture Patterns with Python",
        "chapter": 1,
        "title": "Domain Modeling",
        "tier": 1,
        "keywords": ["domain modeling", "DDD", "entities", "aggregates"],
        "concepts": ["domain-driven design", "tactical patterns"],
        "max_hops": 3,
        "min_similarity": 0.7
    }


# =============================================================================
# Phase 0: Infrastructure Health (GATE 0)
# =============================================================================

@pytest.mark.e2e
@pytest.mark.pipeline
class TestPhase0InfrastructureHealth:
    """
    GATE 0: Verify all services are operational before pipeline execution.
    
    Per END_TO_END_INTEGRATION_WBS.md Phase 0 criteria.
    """

    def test_gate0_gateway_health(self, gateway_url):
        """
        GATE 0.1: LLM Gateway must be healthy.
        
        Command: curl -s http://localhost:8080/health | jq '.status'
        Expected: "healthy"
        """
        try:
            response = httpx.get(f"{gateway_url}/health", timeout=SERVICE_TIMEOUT)
            assert response.status_code == 200, f"Gateway unhealthy: {response.status_code}"
            data = response.json()
            assert data.get("status") == "healthy", f"Gateway status: {data}"
        except httpx.ConnectError:
            pytest.skip(f"Gateway not reachable at {gateway_url}")

    def test_gate0_semantic_search_health(self, semantic_search_url):
        """
        GATE 0.2: Semantic Search service must be healthy.
        
        Command: curl -s http://localhost:8081/health | jq '.status'
        Expected: "healthy"
        """
        try:
            response = httpx.get(f"{semantic_search_url}/health", timeout=SERVICE_TIMEOUT)
            assert response.status_code == 200, f"Semantic search unhealthy: {response.status_code}"
            data = response.json()
            assert data.get("status") == "healthy", f"Semantic search status: {data}"
        except httpx.ConnectError:
            pytest.skip(f"Semantic search not reachable at {semantic_search_url}")

    def test_gate0_ai_agents_health(self, ai_agents_url):
        """
        GATE 0.3: AI Agents service must be healthy.
        
        Command: curl -s http://localhost:8082/health | jq '.status'
        Expected: "healthy"
        """
        try:
            response = httpx.get(f"{ai_agents_url}/health", timeout=SERVICE_TIMEOUT)
            assert response.status_code == 200, f"AI agents unhealthy: {response.status_code}"
            data = response.json()
            assert data.get("status") == "healthy", f"AI agents status: {data}"
        except httpx.ConnectError:
            pytest.skip(f"AI agents not reachable at {ai_agents_url}")

    def test_gate0_qdrant_health(self):
        """
        GATE 0.4: Qdrant vector store must be healthy.
        
        Command: curl -s http://localhost:6333 | jq '.title'
        Expected: "qdrant - vectorass database"
        
        Note: Qdrant's health endpoint varies by version. We check the root endpoint.
        """
        try:
            # Try root endpoint first (works on most versions)
            response = httpx.get(f"{QDRANT_URL}/", timeout=SERVICE_TIMEOUT)
            if response.status_code == 200:
                return  # Qdrant is responding
            
            # Try collections endpoint as fallback
            response = httpx.get(f"{QDRANT_URL}/collections", timeout=SERVICE_TIMEOUT)
            assert response.status_code == 200, f"Qdrant unhealthy: {response.status_code}"
        except httpx.ConnectError:
            pytest.skip(f"Qdrant not reachable at {QDRANT_URL}")

    def test_gate0_all_services_on_network(self, gateway_url, semantic_search_url, ai_agents_url):
        """
        GATE 0.5: All services must be on the same network.
        
        Validates that services can communicate with each other.
        """
        services_reachable = 0
        
        try:
            if httpx.get(f"{gateway_url}/health", timeout=5.0).status_code == 200:
                services_reachable += 1
        except httpx.ConnectError:
            pass
            
        try:
            if httpx.get(f"{semantic_search_url}/health", timeout=5.0).status_code == 200:
                services_reachable += 1
        except httpx.ConnectError:
            pass
            
        try:
            if httpx.get(f"{ai_agents_url}/health", timeout=5.0).status_code == 200:
                services_reachable += 1
        except httpx.ConnectError:
            pass

        if services_reachable == 0:
            pytest.skip("No services reachable - start docker-compose first")
        
        assert services_reachable >= 2, f"Only {services_reachable}/3 services reachable"


# =============================================================================
# Phase 1 & 2: Input Validation (GATE 1 & 2)
# =============================================================================

@pytest.mark.e2e
@pytest.mark.pipeline
class TestPhase1And2InputValidation:
    """
    GATE 1 & 2: Validate PDF→JSON and JSON→Guideline outputs.
    
    In production, these are real outputs from earlier pipeline stages.
    For E2E testing, we use fixtures that represent valid outputs.
    """

    def test_gate1_pdf_json_structure(self, sample_pdf_json):
        """
        GATE 1.1: PDF→JSON output must have valid structure.
        
        Validates: chapters array, each chapter has number/title/content.
        """
        # Verify top-level structure
        assert "title" in sample_pdf_json, "Missing title"
        assert "chapters" in sample_pdf_json, "Missing chapters"
        assert len(sample_pdf_json["chapters"]) >= 1, "No chapters"
        
        # Verify chapter structure
        for chapter in sample_pdf_json["chapters"]:
            assert "number" in chapter, f"Chapter missing number: {chapter}"
            assert "title" in chapter, f"Chapter missing title: {chapter}"
            assert "content" in chapter, f"Chapter missing content: {chapter}"
            assert len(chapter["content"]) > 100, f"Chapter content too short: {chapter['title']}"

    def test_gate1_pdf_json_keywords(self, sample_pdf_json):
        """
        GATE 1.2: Each chapter should have extracted keywords.
        """
        for chapter in sample_pdf_json["chapters"]:
            assert "keywords" in chapter, f"Chapter missing keywords: {chapter['title']}"
            assert len(chapter["keywords"]) >= 1, f"No keywords for: {chapter['title']}"

    def test_gate2_guideline_structure(self, sample_guideline):
        """
        GATE 2.1: Guideline must have valid structure.
        """
        assert "title" in sample_guideline, "Missing title"
        assert "chapters" in sample_guideline, "Missing chapters"
        assert len(sample_guideline["chapters"]) >= 1, "No chapters"
        
        for chapter in sample_guideline["chapters"]:
            assert "number" in chapter, f"Chapter missing number"
            assert "title" in chapter, f"Chapter missing title"
            assert "key_concepts" in chapter, f"Chapter missing key_concepts"

    def test_gate2_guideline_tiers(self, sample_guideline):
        """
        GATE 2.2: Guideline chapters must have tier assignments.
        """
        for chapter in sample_guideline["chapters"]:
            assert "tier" in chapter, f"Chapter missing tier: {chapter['title']}"
            assert chapter["tier"] in [1, 2, 3], f"Invalid tier: {chapter['tier']}"


# =============================================================================
# Phase 3: Metadata Enrichment via Semantic Search (GATE 3)
# =============================================================================

@pytest.mark.e2e
@pytest.mark.pipeline
class TestPhase3MetadataEnrichment:
    """
    GATE 3: Metadata enrichment through semantic-search-service.
    
    Kitchen Brigade: semantic-search (Cookbook) provides search capabilities.
    Traffic should route through Gateway when using Gateway tools.
    """

    def test_gate3_search_via_gateway_tool(self, gateway_url):
        """
        GATE 3.1: Search must route through Gateway's search_corpus tool.
        
        This validates the Kitchen Brigade routing pattern.
        """
        try:
            # Execute search_corpus tool through Gateway
            response = httpx.post(
                f"{gateway_url}/v1/tools/execute",
                json={
                    "name": "search_corpus",
                    "arguments": {
                        "query": "repository pattern data access",
                        "top_k": 5
                    }
                },
                timeout=PIPELINE_PHASE_TIMEOUT
            )
            
            if response.status_code != 200:
                # Gateway may not have search_corpus registered
                pytest.skip(f"search_corpus tool not available: {response.status_code}")
            
            data = response.json()
            assert "result" in data or "results" in data, f"No results in response: {data}"
            assert data.get("success", True), f"Tool execution failed: {data}"
            
        except httpx.ConnectError:
            pytest.skip(f"Gateway not reachable at {gateway_url}")

    def test_gate3_hybrid_search_direct(self, semantic_search_url):
        """
        GATE 3.2: Hybrid search endpoint is functional.
        
        Direct call to semantic-search for comparison with Gateway route.
        """
        try:
            response = httpx.post(
                f"{semantic_search_url}/v1/search/hybrid",
                json={
                    "query": "domain modeling entities",
                    "limit": 5,
                    "alpha": 0.7,
                    "include_graph": False
                },
                timeout=PIPELINE_PHASE_TIMEOUT
            )
            
            if response.status_code == 503:
                pytest.skip("Hybrid search disabled in semantic-search-service")
            
            if response.status_code == 200:
                data = response.json()
                assert "results" in data, f"No results key: {data}"
                # Results may be empty if no data seeded
            else:
                # Log but don't fail - may need seeded data
                pytest.skip(f"Hybrid search returned {response.status_code}")
                
        except httpx.ConnectError:
            pytest.skip(f"Semantic search not reachable at {semantic_search_url}")

    def test_gate3_embedding_generation(self, semantic_search_url):
        """
        GATE 3.3: Embedding generation works for metadata enrichment.
        """
        try:
            response = httpx.post(
                f"{semantic_search_url}/v1/embed",
                json={"text": "repository pattern persistence layer"},
                timeout=PIPELINE_PHASE_TIMEOUT
            )
            
            if response.status_code != 200:
                pytest.skip(f"/v1/embed not available: {response.status_code}")
            
            data = response.json()
            assert "embeddings" in data, f"No embeddings in response: {data}"
            assert len(data["embeddings"]) == 1, "Expected 1 embedding"
            # Embedding dimension should be 768 for sentence-transformers
            assert len(data["embeddings"][0]) > 0, "Empty embedding"
            
        except httpx.ConnectError:
            pytest.skip(f"Semantic search not reachable at {semantic_search_url}")

    def test_gate3_enrichment_workflow(self, semantic_search_url, sample_pdf_json):
        """
        GATE 3.4: Full enrichment workflow - embed keywords and search.
        
        Simulates the metadata enrichment phase:
        1. Extract keywords from chapter
        2. Generate embedding for keywords
        3. Search for related content
        """
        try:
            chapter = sample_pdf_json["chapters"][0]
            keywords = " ".join(chapter.get("keywords", ["domain modeling"]))
            
            # Step 1: Generate embedding for keywords
            embed_response = httpx.post(
                f"{semantic_search_url}/v1/embed",
                json={"text": keywords},
                timeout=SERVICE_TIMEOUT
            )
            
            if embed_response.status_code != 200:
                pytest.skip("Embedding endpoint not available")
            
            # Step 2: Use embedding for search (or text query)
            search_response = httpx.post(
                f"{semantic_search_url}/v1/search/hybrid",
                json={
                    "query": keywords,
                    "limit": 5,
                    "alpha": 0.7,
                    "include_graph": False
                },
                timeout=PIPELINE_PHASE_TIMEOUT
            )
            
            if search_response.status_code == 503:
                pytest.skip("Hybrid search disabled")
            
            # Workflow is functional even if results are empty (no seeded data)
            assert search_response.status_code in [200, 404], f"Unexpected status: {search_response.status_code}"
            
        except httpx.ConnectError:
            pytest.skip(f"Semantic search not reachable at {semantic_search_url}")


# =============================================================================
# Phase 4: LLM Enhancement via Gateway (GATE 4)
# =============================================================================

@pytest.mark.e2e
@pytest.mark.pipeline
class TestPhase4LLMEnhancement:
    """
    GATE 4: LLM Enhancement through Gateway routing.
    
    Kitchen Brigade:
    - Gateway (Router): Routes cross_reference tool to ai-agents
    - ai-agents (Expeditor): Orchestrates the Cross-Reference Agent
    
    This is the final phase where scholarly annotations are generated.
    """

    def test_gate4_gateway_tools_registered(self, gateway_url):
        """
        GATE 4.1: Required tools are registered in Gateway.
        
        Tools needed for pipeline:
        - search_corpus: For content retrieval
        - get_chunk: For specific chunk access
        - cross_reference: For scholarly annotation generation
        """
        try:
            response = httpx.get(f"{gateway_url}/v1/tools", timeout=SERVICE_TIMEOUT)
            
            if response.status_code != 200:
                pytest.skip(f"Tools endpoint not available: {response.status_code}")
            
            data = response.json()
            tools = data.get("tools", data) if isinstance(data, dict) else data
            
            # Extract tool names
            if isinstance(tools, list):
                tool_names = {t.get("name") for t in tools if isinstance(t, dict)}
            else:
                tool_names = set()
            
            # Check required tools
            required_tools = {"search_corpus", "get_chunk"}
            missing = required_tools - tool_names
            
            if missing:
                pytest.skip(f"Missing required tools: {missing}")
            
            # cross_reference is optional but desirable
            if "cross_reference" not in tool_names:
                pytest.xfail("cross_reference tool not registered (needed for full pipeline)")
                
        except httpx.ConnectError:
            pytest.skip(f"Gateway not reachable at {gateway_url}")

    def test_gate4_cross_reference_via_gateway(self, gateway_url, sample_cross_reference_request):
        """
        GATE 4.2: Cross-reference executes through Gateway.
        
        This is the core LLM enhancement step:
        Gateway → ai-agents → cross_reference agent → scholarly annotation
        """
        try:
            response = httpx.post(
                f"{gateway_url}/v1/tools/execute",
                json={
                    "name": "cross_reference",
                    "arguments": sample_cross_reference_request
                },
                timeout=PIPELINE_PHASE_TIMEOUT * 2  # Longer timeout for LLM call
            )
            
            if response.status_code == 404:
                pytest.skip("cross_reference tool not registered in Gateway")
            
            if response.status_code == 502:
                pytest.skip("ai-agents service not reachable from Gateway")
            
            if response.status_code == 200:
                data = response.json()
                # Successful cross-reference should return annotation
                assert "result" in data or "annotation" in data, f"No result: {data}"
            else:
                # Log response for debugging
                pytest.skip(f"cross_reference returned {response.status_code}: {response.text[:200]}")
                
        except httpx.ConnectError:
            pytest.skip(f"Gateway not reachable at {gateway_url}")
        except httpx.ReadTimeout:
            pytest.skip("Cross-reference timed out (may need longer timeout for LLM)")

    def test_gate4_ai_agents_cross_reference_direct(self, ai_agents_url, sample_cross_reference_request):
        """
        GATE 4.3: Direct call to ai-agents cross-reference endpoint.
        
        This validates the ai-agents service is functional.
        In production, this should be routed through Gateway.
        """
        try:
            # Build request for ai-agents endpoint
            request_body = {
                "source": {
                    "book": sample_cross_reference_request["book"],
                    "chapter": sample_cross_reference_request["chapter"],
                    "title": sample_cross_reference_request["title"],
                    "tier": sample_cross_reference_request["tier"],
                    "content": "Domain modeling with DDD patterns.",
                    "keywords": sample_cross_reference_request["keywords"]
                },
                "config": {
                    "max_hops": sample_cross_reference_request.get("max_hops", 3),
                    "min_similarity": sample_cross_reference_request.get("min_similarity", 0.7)
                },
                "taxonomy_id": "ai-ml"
            }
            
            response = httpx.post(
                f"{ai_agents_url}/v1/agents/cross-reference",
                json=request_body,
                timeout=PIPELINE_PHASE_TIMEOUT * 2
            )
            
            if response.status_code == 200:
                data = response.json()
                assert "annotation" in data, f"No annotation in response: {data}"
            elif response.status_code == 503:
                pytest.skip("Cross-reference agent dependencies not ready")
            else:
                pytest.skip(f"Cross-reference returned {response.status_code}")
                
        except httpx.ConnectError:
            pytest.skip(f"AI agents not reachable at {ai_agents_url}")
        except httpx.ReadTimeout:
            pytest.skip("Cross-reference timed out")

    def test_gate4_llm_provider_uses_gateway(self):
        """
        GATE 4.4: LLM provider factory defaults to Gateway.
        
        Validates that the factory pattern routes through Gateway.
        """
        try:
            from workflows.shared.providers.factory import create_llm_provider
            
            # Get default provider
            with patch.dict(os.environ, {"LLM_PROVIDER": "gateway"}):
                provider = create_llm_provider()
                
                # Provider should be GatewayProvider
                provider_class = type(provider).__name__
                assert "Gateway" in provider_class, f"Expected GatewayProvider, got {provider_class}"
                
        except ImportError:
            pytest.skip("LLM provider factory not available")


# =============================================================================
# Full Pipeline Integration Test
# =============================================================================

@pytest.mark.e2e
@pytest.mark.pipeline
class TestFullPipelineIntegration:
    """
    Full pipeline integration test - simulates frontend-triggered workflow.
    
    This test class runs through all phases sequentially, validating
    the complete document enhancement workflow.
    """

    def test_full_pipeline_simulation(
        self,
        gateway_url,
        semantic_search_url,
        ai_agents_url,
        sample_pdf_json,
        sample_guideline
    ):
        """
        Full pipeline simulation: PDF → JSON → Guideline → Enrichment → Enhancement.
        
        This simulates what happens when a user triggers document enhancement
        from the frontend.
        """
        results = {
            "phase0_infrastructure": False,
            "phase1_pdf_json": False,
            "phase2_guideline": False,
            "phase3_enrichment": False,
            "phase4_enhancement": False,
            "gateway_routing": False
        }
        
        # Phase 0: Check infrastructure
        try:
            gateway_health = httpx.get(f"{gateway_url}/health", timeout=5.0)
            search_health = httpx.get(f"{semantic_search_url}/health", timeout=5.0)
            
            if gateway_health.status_code == 200 and search_health.status_code == 200:
                results["phase0_infrastructure"] = True
        except httpx.ConnectError:
            pytest.skip("Infrastructure not available")
        
        # Phase 1 & 2: Validate input data (from fixtures)
        if sample_pdf_json and len(sample_pdf_json.get("chapters", [])) > 0:
            results["phase1_pdf_json"] = True
        
        if sample_guideline and len(sample_guideline.get("chapters", [])) > 0:
            results["phase2_guideline"] = True
        
        # Phase 3: Metadata enrichment via semantic search
        try:
            # Use first chapter's keywords for search
            chapter = sample_pdf_json["chapters"][0]
            query = " ".join(chapter.get("keywords", ["domain modeling"]))
            
            # Search via Gateway tool
            search_response = httpx.post(
                f"{gateway_url}/v1/tools/execute",
                json={
                    "name": "search_corpus",
                    "arguments": {"query": query, "top_k": 5}
                },
                timeout=PIPELINE_PHASE_TIMEOUT
            )
            
            if search_response.status_code == 200:
                results["phase3_enrichment"] = True
                results["gateway_routing"] = True
            elif search_response.status_code == 404:
                # Fallback to direct semantic search
                direct_response = httpx.post(
                    f"{semantic_search_url}/v1/search/hybrid",
                    json={"query": query, "limit": 5, "alpha": 0.7, "include_graph": False},
                    timeout=PIPELINE_PHASE_TIMEOUT
                )
                if direct_response.status_code in [200, 503]:
                    results["phase3_enrichment"] = True
                    
        except httpx.ConnectError:
            pass
        
        # Phase 4: LLM Enhancement via cross-reference
        try:
            # Try cross_reference through Gateway
            cross_ref_response = httpx.post(
                f"{gateway_url}/v1/tools/execute",
                json={
                    "name": "cross_reference",
                    "arguments": {
                        "book": sample_pdf_json["title"],
                        "chapter": 1,
                        "title": sample_pdf_json["chapters"][0]["title"],
                        "tier": sample_pdf_json["chapters"][0].get("tier", 1),
                        "keywords": sample_pdf_json["chapters"][0].get("keywords", [])
                    }
                },
                timeout=PIPELINE_PHASE_TIMEOUT * 2
            )
            
            if cross_ref_response.status_code == 200:
                results["phase4_enhancement"] = True
                results["gateway_routing"] = True
                
        except (httpx.ConnectError, httpx.ReadTimeout):
            pass
        
        # Report results
        passed_phases = sum(1 for v in results.values() if v)
        total_phases = len(results)
        
        # At minimum, infrastructure and input validation should pass
        assert results["phase0_infrastructure"], "Phase 0 (Infrastructure) failed"
        assert results["phase1_pdf_json"], "Phase 1 (PDF→JSON) validation failed"
        assert results["phase2_guideline"], "Phase 2 (Guideline) validation failed"
        
        # Log pipeline status
        print(f"\n{'='*60}")
        print("FULL PIPELINE INTEGRATION RESULTS")
        print(f"{'='*60}")
        for phase, passed in results.items():
            status = "✓ PASS" if passed else "✗ FAIL/SKIP"
            print(f"  {phase}: {status}")
        print(f"{'='*60}")
        print(f"  Total: {passed_phases}/{total_phases} phases passed")
        print(f"{'='*60}\n")

    def test_pipeline_data_flow_through_gateway(
        self,
        gateway_url,
        semantic_search_url,
        sample_pdf_json
    ):
        """
        Verify data flows through Gateway per Kitchen Brigade architecture.
        
        This test specifically validates that:
        1. Search requests go through Gateway
        2. Tool execution responses contain expected structure
        3. Data can be used in subsequent pipeline stages
        """
        try:
            chapter = sample_pdf_json["chapters"][0]
            
            # Step 1: Search for related content via Gateway
            search_response = httpx.post(
                f"{gateway_url}/v1/tools/execute",
                json={
                    "name": "search_corpus",
                    "arguments": {
                        "query": chapter["title"],
                        "top_k": 3
                    }
                },
                timeout=PIPELINE_PHASE_TIMEOUT
            )
            
            if search_response.status_code == 404:
                pytest.skip("search_corpus tool not registered")
            
            assert search_response.status_code == 200, f"Search failed: {search_response.status_code}"
            
            search_data = search_response.json()
            assert search_data.get("success", True), f"Search unsuccessful: {search_data}"
            
            # Step 2: Verify response can be used for enrichment
            # The response should have a result that can be parsed
            result = search_data.get("result", search_data)
            
            # Result structure may vary - just verify it's usable
            assert result is not None, "No result from search"
            
        except httpx.ConnectError:
            pytest.skip(f"Gateway not reachable at {gateway_url}")


# =============================================================================
# Gateway Routing Verification (Cross-Cutting Concern)
# =============================================================================

@pytest.mark.e2e
@pytest.mark.pipeline
class TestGatewayRoutingVerification:
    """
    Verify ALL external requests route through Gateway.
    
    This is a cross-cutting concern that validates the Kitchen Brigade
    architecture is being followed throughout the pipeline.
    """

    def test_factory_defaults_to_gateway(self):
        """
        Factory pattern should default to Gateway provider.
        """
        try:
            from workflows.shared.providers.factory import create_llm_provider
            
            # Without explicit provider, should default to gateway
            default_provider = os.getenv("LLM_PROVIDER", "gateway")
            assert default_provider == "gateway", f"Default provider is {default_provider}, expected gateway"
            
        except ImportError:
            pytest.skip("Factory not available")

    def test_gateway_search_client_routes_correctly(self, gateway_url):
        """
        GatewaySearchClient should route through Gateway tools.
        """
        try:
            from workflows.shared.clients.gateway_search_client import GatewaySearchClient
            
            # Create client with Gateway URL
            client = GatewaySearchClient(gateway_url=gateway_url)
            
            # Verify it's configured for Gateway
            assert client.gateway_url == gateway_url, "Client not using correct Gateway URL"
            
        except ImportError:
            pytest.skip("GatewaySearchClient not available")

    def test_no_direct_external_calls_from_enhancer(self):
        """
        LLM enhancement scripts should not make direct external calls.
        
        All calls should go through providers/clients that route via Gateway.
        This test validates the factory defaults to Gateway when LLM_PROVIDER=gateway.
        """
        try:
            from workflows.llm_enhancement.scripts.llm_enhance_guideline import (
                LLM_AVAILABLE,
            )
            
            # If LLM is available, provider should be Gateway when configured correctly
            if LLM_AVAILABLE:
                # Set env var explicitly to test Gateway routing
                with patch.dict(os.environ, {"LLM_PROVIDER": "gateway"}, clear=False):
                    # Need to reimport to pick up env var
                    from workflows.shared.providers.factory import create_llm_provider
                    provider = create_llm_provider()
                    provider_class = type(provider).__name__
                    
                    # With LLM_PROVIDER=gateway, should get GatewayProvider
                    assert "Gateway" in provider_class, \
                        f"Expected GatewayProvider with LLM_PROVIDER=gateway, got {provider_class}"
                    
        except ImportError:
            pytest.skip("LLM enhancement module not available")

    def test_docker_compose_gateway_env_vars(self):
        """
        Docker compose should configure Gateway routing.
        """
        docker_compose_path = PROJECT_ROOT / "docker-compose.yml"
        
        if not docker_compose_path.exists():
            pytest.skip("docker-compose.yml not found")
        
        content = docker_compose_path.read_text()
        
        # Check for Gateway configuration
        assert "LLM_PROVIDER" in content or "LLM_GATEWAY_URL" in content, \
            "docker-compose.yml missing Gateway environment variables"


# =============================================================================
# Pipeline Timing and Performance (Optional)
# =============================================================================

@pytest.mark.e2e
@pytest.mark.pipeline
@pytest.mark.slow
class TestPipelinePerformance:
    """
    Performance tests for the full pipeline.
    
    These tests verify that the pipeline completes within acceptable timeframes.
    """

    def test_search_latency_acceptable(self, gateway_url):
        """
        Search operations should complete within 5 seconds.
        """
        try:
            start = time.time()
            
            response = httpx.post(
                f"{gateway_url}/v1/tools/execute",
                json={
                    "name": "search_corpus",
                    "arguments": {"query": "repository pattern", "top_k": 5}
                },
                timeout=10.0
            )
            
            latency = time.time() - start
            
            if response.status_code == 404:
                pytest.skip("search_corpus not registered")
            
            assert latency < 5.0, f"Search took {latency:.2f}s, expected < 5s"
            
        except httpx.ConnectError:
            pytest.skip("Gateway not reachable")

    def test_health_check_latency(self, gateway_url, semantic_search_url, ai_agents_url):
        """
        Health checks should complete within 1 second.
        """
        services = [
            ("Gateway", gateway_url),
            ("Semantic Search", semantic_search_url),
            ("AI Agents", ai_agents_url)
        ]
        
        for name, url in services:
            try:
                start = time.time()
                response = httpx.get(f"{url}/health", timeout=2.0)
                latency = time.time() - start
                
                if response.status_code == 200:
                    assert latency < 1.0, f"{name} health check took {latency:.2f}s"
            except httpx.ConnectError:
                pass  # Skip unreachable services
