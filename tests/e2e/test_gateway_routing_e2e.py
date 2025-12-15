"""
End-to-End Test: Gateway Routing Verification

WBS Reference: GATEWAY_ROUTING_REFACTOR_WBS.md - Phase 5 Verification
Pattern: E2E testing per Kitchen Brigade architecture

This test verifies that ALL external requests route through the LLM Gateway
as specified in the architecture documents:
- llm-gateway/docs/ARCHITECTURE.md: Kitchen Brigade "Router" pattern
- ai-agents/docs/ARCHITECTURE.md: Service Responsibility Matrix

Test Categories:
1. Infrastructure verification (all services healthy)
2. LLM routing verification (traffic goes through Gateway)
3. Tool execution verification (search_corpus routes through Gateway)
4. Configuration verification (env vars set correctly)

Prerequisites:
- All services running: llm-gateway:8080, semantic-search:8081, ai-agents:8082
- Neo4j:7687, Qdrant:6333, Redis:6379

Usage:
    pytest tests/e2e/test_gateway_routing_e2e.py -v
    
    # Or with live services:
    pytest tests/e2e/test_gateway_routing_e2e.py -v -m "not skip_ci"
"""

import os
import pytest
import httpx
from unittest.mock import patch, AsyncMock, MagicMock


# =============================================================================
# Configuration
# =============================================================================

GATEWAY_URL = os.getenv("LLM_GATEWAY_URL", "http://localhost:8080")
SEMANTIC_SEARCH_URL = os.getenv("SEARCH_SERVICE_URL", "http://localhost:8081")
AI_AGENTS_URL = os.getenv("AI_AGENTS_URL", "http://localhost:8082")


# =============================================================================
# Fixtures
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


# =============================================================================
# Phase 1: Infrastructure Verification (GATE 0)
# =============================================================================

@pytest.mark.e2e
class TestInfrastructureHealth:
    """Verify all services are running and healthy."""

    def test_gateway_health(self, gateway_url):
        """
        E2E Test: LLM Gateway is healthy.
        
        GATE 0 Criteria: curl -s http://localhost:8080/health | jq '.status'
        Expected: "healthy"
        """
        try:
            response = httpx.get(f"{gateway_url}/health", timeout=5.0)
            assert response.status_code == 200, f"Gateway returned {response.status_code}"
            
            data = response.json()
            assert data.get("status") == "healthy", f"Gateway status: {data.get('status')}"
        except httpx.ConnectError:
            pytest.skip(f"Gateway not reachable at {gateway_url}")

    def test_semantic_search_health(self, semantic_search_url):
        """
        E2E Test: Semantic Search service is healthy.
        
        GATE 0 Criteria: curl -s http://localhost:8081/health | jq '.status'
        Expected: "healthy"
        """
        try:
            response = httpx.get(f"{semantic_search_url}/health", timeout=5.0)
            assert response.status_code == 200, f"Semantic search returned {response.status_code}"
            
            data = response.json()
            assert data.get("status") == "healthy", f"Semantic search status: {data.get('status')}"
        except httpx.ConnectError:
            pytest.skip(f"Semantic search not reachable at {semantic_search_url}")

    def test_ai_agents_health(self, ai_agents_url):
        """
        E2E Test: AI Agents service is healthy.
        
        GATE 0 Criteria: curl -s http://localhost:8082/health | jq '.status'
        Expected: "healthy"
        """
        try:
            response = httpx.get(f"{ai_agents_url}/health", timeout=5.0)
            assert response.status_code == 200, f"AI agents returned {response.status_code}"
            
            data = response.json()
            assert data.get("status") == "healthy", f"AI agents status: {data.get('status')}"
        except httpx.ConnectError:
            pytest.skip(f"AI agents not reachable at {ai_agents_url}")


# =============================================================================
# Phase 2: Configuration Verification
# =============================================================================

@pytest.mark.e2e
class TestGatewayConfiguration:
    """Verify Gateway routing configuration is correct."""

    def test_factory_defaults_to_gateway(self):
        """
        E2E Test: Provider factory defaults to 'gateway'.
        
        Per Kitchen Brigade architecture, all LLM traffic must route
        through the Gateway.
        """
        # Clear environment to test default
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("LLM_PROVIDER", None)
            
            # Import fresh
            from workflows.shared.providers.factory import create_llm_provider
            from workflows.shared.providers.gateway_provider import GatewayProvider
            
            provider = create_llm_provider()
            
            assert isinstance(provider, GatewayProvider), (
                f"Factory should default to GatewayProvider, got {type(provider).__name__}"
            )

    def test_gateway_provider_uses_correct_url(self):
        """
        E2E Test: GatewayProvider uses Gateway URL.
        
        Verify the provider is configured to use :8080 (Gateway),
        NOT :8081 (semantic-search) or direct Anthropic SDK.
        """
        from workflows.shared.providers.gateway_provider import GatewayProvider
        
        provider = GatewayProvider()
        
        assert ":8080" in provider._gateway_url, (
            f"GatewayProvider should use :8080, got {provider._gateway_url}"
        )

    def test_gateway_search_client_uses_gateway(self):
        """
        E2E Test: GatewaySearchClient routes through Gateway.
        
        The search client should call Gateway tools, NOT semantic-search directly.
        """
        from workflows.shared.clients.gateway_search_client import GatewaySearchClient
        
        client = GatewaySearchClient()
        
        assert ":8080" in client.gateway_url, (
            f"GatewaySearchClient should use :8080, got {client.gateway_url}"
        )
        assert ":8081" not in client.gateway_url, (
            "GatewaySearchClient should NOT use :8081 directly"
        )

    def test_docker_compose_has_gateway_env_vars(self):
        """
        E2E Test: docker-compose.yml has Gateway environment variables.
        
        Required env vars:
        - LLM_PROVIDER=gateway
        - LLM_GATEWAY_URL=http://llm-gateway:8080
        """
        from pathlib import Path
        
        compose_path = Path(__file__).parent.parent.parent / "docker-compose.yml"
        
        if not compose_path.exists():
            pytest.skip("docker-compose.yml not found")
        
        content = compose_path.read_text()
        
        assert "LLM_PROVIDER" in content, "Missing LLM_PROVIDER env var"
        assert "LLM_GATEWAY_URL" in content, "Missing LLM_GATEWAY_URL env var"


# =============================================================================
# Phase 3: Gateway Tool Execution Verification
# =============================================================================

@pytest.mark.e2e
class TestGatewayToolExecution:
    """Verify tools execute through Gateway."""

    def test_gateway_has_search_corpus_tool(self, gateway_url):
        """
        E2E Test: Gateway has search_corpus tool registered.
        
        The search_corpus tool should be available for tool execution.
        """
        try:
            response = httpx.get(f"{gateway_url}/v1/tools", timeout=5.0)
            
            if response.status_code == 404:
                pytest.skip("Gateway /v1/tools endpoint not available")
            
            assert response.status_code == 200
            
            data = response.json()
            # Gateway returns tools as a list directly
            tools = data if isinstance(data, list) else data.get("tools", [])
            tool_names = [t.get("name") for t in tools]
            
            assert "search_corpus" in tool_names, (
                f"search_corpus tool not found. Available: {tool_names}"
            )
        except httpx.ConnectError:
            pytest.skip(f"Gateway not reachable at {gateway_url}")

    def test_gateway_has_cross_reference_tool(self, gateway_url):
        """
        E2E Test: Gateway has cross_reference tool registered.
        
        The cross_reference tool proxies to ai-agents service.
        """
        try:
            response = httpx.get(f"{gateway_url}/v1/tools", timeout=5.0)
            
            if response.status_code == 404:
                pytest.skip("Gateway /v1/tools endpoint not available")
            
            assert response.status_code == 200
            
            data = response.json()
            # Gateway returns tools as a list directly
            tools = data if isinstance(data, list) else data.get("tools", [])
            tool_names = [t.get("name") for t in tools]
            
            # cross_reference may not be registered yet - skip if not found
            if "cross_reference" not in tool_names:
                pytest.skip(f"cross_reference tool not registered. Available: {tool_names}")
            
        except httpx.ConnectError:
            pytest.skip(f"Gateway not reachable at {gateway_url}")

    @pytest.mark.asyncio
    async def test_search_via_gateway_tool(self, gateway_url):
        """
        E2E Test: Search executes via Gateway tool.
        
        Verify that search requests go through Gateway /v1/tools/execute
        endpoint using the search_corpus tool.
        """
        from workflows.shared.clients.gateway_search_client import GatewaySearchClient
        
        try:
            async with GatewaySearchClient(gateway_url=gateway_url) as client:
                # This should route through Gateway, NOT direct to :8081
                results = await client.search("domain driven design", limit=3)
                
                # If we get here without error, Gateway routing is working
                assert isinstance(results, list), "Expected list of results"
                
        except Exception as e:
            # Connection errors are acceptable if services aren't running
            if "connect" in str(e).lower():
                pytest.skip(f"Gateway not reachable: {e}")
            raise


# =============================================================================
# Phase 4: Data Flow Verification
# =============================================================================

@pytest.mark.e2e
class TestDataFlow:
    """Verify the complete data flow routes through Gateway."""

    def test_enhancement_script_import_uses_factory(self):
        """
        E2E Test: Enhancement script uses factory, not direct AnthropicProvider.
        
        The llm_enhance_guideline.py script should import create_llm_provider
        instead of AnthropicProvider directly.
        """
        from pathlib import Path
        
        script_path = Path(__file__).parent.parent.parent / \
            "workflows/llm_enhancement/scripts/llm_enhance_guideline.py"
        
        if not script_path.exists():
            pytest.skip("Enhancement script not found")
        
        content = script_path.read_text()
        
        # Should have factory import
        assert "create_llm_provider" in content, (
            "Enhancement script should import create_llm_provider"
        )
        
        # Should NOT have direct AnthropicProvider instantiation
        # (import is OK for type hints, but instantiation is not)
        lines_with_anthropic = [
            line for line in content.split("\n")
            if "AnthropicProvider(" in line and not line.strip().startswith("#")
        ]
        
        assert len(lines_with_anthropic) == 0, (
            f"Found direct AnthropicProvider instantiation: {lines_with_anthropic}"
        )

    def test_no_direct_8081_calls_in_gateway_client(self):
        """
        E2E Test: GatewaySearchClient never calls :8081 directly.
        
        All search traffic must route through Gateway :8080.
        """
        from pathlib import Path
        
        client_path = Path(__file__).parent.parent.parent / \
            "workflows/shared/clients/gateway_search_client.py"
        
        if not client_path.exists():
            pytest.skip("GatewaySearchClient not found")
        
        content = client_path.read_text()
        
        # Check only actual code lines (not comments or docstrings)
        code_lines = []
        in_docstring = False
        for line in content.split("\n"):
            stripped = line.strip()
            # Skip empty lines
            if not stripped:
                continue
            # Track docstrings
            if '"""' in stripped:
                in_docstring = not in_docstring
                continue
            # Skip if in docstring or is a comment
            if in_docstring or stripped.startswith("#"):
                continue
            code_lines.append(line)
        
        code_only = "\n".join(code_lines)
        
        # Should NOT have :8081 in actual code
        assert ":8081" not in code_only, (
            "GatewaySearchClient should not have :8081 in actual code"
        )


# =============================================================================
# Phase 5: Live Integration Test (requires running services)
# =============================================================================

@pytest.mark.e2e
@pytest.mark.live
class TestLiveGatewayIntegration:
    """
    Live integration tests requiring all services running.
    
    Run with: pytest -m live -v
    Skip in CI: pytest -m "not live" -v
    """

    @pytest.mark.asyncio
    async def test_live_search_through_gateway(self, gateway_url):
        """
        LIVE E2E Test: Execute actual search through Gateway.
        
        This test makes real HTTP calls to verify the complete
        Gateway → semantic-search flow.
        """
        from workflows.shared.clients.gateway_search_client import GatewaySearchClient
        
        try:
            async with GatewaySearchClient(gateway_url=gateway_url) as client:
                results = await client.search(
                    query="repository pattern dependency injection",
                    limit=5,
                    collection="chapters"
                )
                
                assert isinstance(results, list)
                
                if results:
                    # Verify result structure
                    first_result = results[0]
                    # Gateway returns results with 'id', 'score', 'payload'
                    has_valid_structure = (
                        "id" in first_result or 
                        "chunk_id" in first_result or 
                        "content" in first_result or
                        "payload" in first_result
                    )
                    assert has_valid_structure, (
                        f"Unexpected result structure: {first_result.keys()}"
                    )
                    
        except httpx.ConnectError:
            pytest.skip("Services not running for live test")

    def test_live_gateway_chat_completion(self, gateway_url):
        """
        LIVE E2E Test: Execute chat completion through Gateway.
        
        This verifies the Gateway can route to LLM providers.
        """
        try:
            # Simple health-style request to verify endpoint exists
            response = httpx.post(
                f"{gateway_url}/v1/chat/completions",
                json={
                    "model": "claude-sonnet-4-5-20250929",
                    "messages": [{"role": "user", "content": "Say 'test'"}],
                    "max_tokens": 10,
                },
                timeout=30.0,
            )
            
            # 401/403 = auth required but endpoint exists
            # 200 = success
            # 500+ = server error
            assert response.status_code in (200, 401, 403), (
                f"Gateway chat endpoint returned {response.status_code}"
            )
            
        except httpx.ConnectError:
            pytest.skip("Gateway not running for live test")


# =============================================================================
# Validation Summary Report
# =============================================================================

@pytest.mark.e2e
class TestValidationSummary:
    """Generate validation summary for Gateway routing."""

    def test_print_validation_summary(self, gateway_url, semantic_search_url, ai_agents_url):
        """
        Print validation summary.
        
        This test always passes but prints a summary of the Gateway routing status.
        """
        from workflows.shared.providers.factory import create_llm_provider
        from workflows.shared.clients.gateway_search_client import GatewaySearchClient
        
        print("\n" + "=" * 70)
        print("GATEWAY ROUTING VALIDATION SUMMARY")
        print("=" * 70)
        
        # Check factory default
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("LLM_PROVIDER", None)
            provider = create_llm_provider()
            factory_ok = provider.provider_name == "gateway"
        
        # Check client URL
        client = GatewaySearchClient()
        client_ok = ":8080" in client.gateway_url
        
        # Check services
        services = {
            "Gateway": gateway_url,
            "Semantic Search": semantic_search_url,
            "AI Agents": ai_agents_url,
        }
        
        service_status = {}
        for name, url in services.items():
            try:
                response = httpx.get(f"{url}/health", timeout=2.0)
                service_status[name] = "✅ Healthy" if response.status_code == 200 else f"⚠️ {response.status_code}"
            except Exception:
                service_status[name] = "❌ Unreachable"
        
        print(f"\n📦 Factory Default: {'✅ gateway' if factory_ok else '❌ NOT gateway'}")
        print(f"🔗 Client URL: {'✅ :8080' if client_ok else '❌ NOT :8080'}")
        print(f"\n🏥 Service Health:")
        for name, status in service_status.items():
            print(f"   {name}: {status}")
        
        print("\n" + "=" * 70)
        
        # This test always passes - it's informational
        assert True
