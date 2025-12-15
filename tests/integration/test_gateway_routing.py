"""
TDD RED Phase: Integration Tests for Gateway Routing

WBS Reference: GATEWAY_ROUTING_REFACTOR_WBS.md - Phase 2.3
Pattern: TDD RED → GREEN → REFACTOR

These integration tests verify that ALL external requests from
llm-document-enhancer route through the LLM Gateway.

Expected Behavior:
- No direct HTTP traffic to semantic-search:8081
- All LLM requests via Gateway:8080/v1/chat/completions
- All search requests via Gateway:8080/v1/tools/execute

Reference Documents:
- ARCHITECTURE.md: Kitchen Brigade "Router" pattern
- TIER_RELATIONSHIP_DIAGRAM.md: Content retrieval flow
"""

import os
import pytest
from unittest.mock import patch, AsyncMock, MagicMock


@pytest.mark.integration
class TestGatewayRoutingIntegration:
    """
    TDD RED Phase: Integration tests for Gateway routing.
    
    These tests verify the complete data flow routes through Gateway.
    """

    def test_no_direct_8081_calls_in_search_client(self):
        """
        GREEN TEST: GatewaySearchClient should use Gateway:8080, not :8081.
        
        Verification that the new GatewaySearchClient routes through Gateway
        instead of calling semantic-search directly.
        
        WBS 2.3.1: test_no_direct_8081_calls
        """
        # Verify GatewaySearchClient exists and uses Gateway URL
        from workflows.shared.clients.gateway_search_client import GatewaySearchClient
        
        # Create client with default URL
        client = GatewaySearchClient()
        
        # GatewaySearchClient should use Gateway:8080
        assert ":8081" not in client.gateway_url, (
            f"GatewaySearchClient uses direct URL {client.gateway_url}. "
            "Should use Gateway:8080, not semantic-search:8081."
        )
        assert ":8080" in client.gateway_url or "gateway" in client.gateway_url.lower(), (
            f"GatewaySearchClient should use Gateway URL. Got: {client.gateway_url}"
        )

    def test_all_llm_traffic_via_8080(self):
        """
        RED TEST: All LLM requests should go through Gateway:8080.
        
        Current behavior: AnthropicProvider calls Anthropic SDK directly (WRONG)
        Expected behavior: GatewayProvider calls Gateway:8080 (CORRECT)
        
        WBS 2.3.2: test_all_traffic_via_8080
        """
        # When factory defaults to gateway, this should pass
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("LLM_PROVIDER", None)
            
            from workflows.shared.providers.factory import create_llm_provider
            
            provider = create_llm_provider()
            
            # Check provider is GatewayProvider
            assert provider.provider_name == "gateway", (
                f"Default provider should be 'gateway', got '{provider.provider_name}'. "
                "All LLM traffic must route through Gateway:8080."
            )
            
            # Verify gateway URL
            if hasattr(provider, "_gateway_url"):
                assert ":8080" in provider._gateway_url, (
                    f"GatewayProvider should use :8080, got {provider._gateway_url}"
                )

    @pytest.mark.asyncio
    async def test_tool_execution_via_gateway(self):
        """
        RED TEST: Tool execution should use Gateway /v1/tools/execute.
        
        WBS 2.3.3: test_tool_execution_via_gateway
        """
        try:
            from workflows.shared.clients.gateway_search_client import GatewaySearchClient
        except ImportError:
            pytest.fail(
                "GatewaySearchClient not found. "
                "Tool execution should use this client to route through Gateway."
            )
        
        # Mock Gateway response for tool execution
        mock_tool_response = {
            "tool_call_id": "call_123",
            "output": {
                "results": [
                    {"chunk_id": "ch1", "content": "Test", "score": 0.9}
                ]
            }
        }
        
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client.post = AsyncMock(return_value=MagicMock(
                status_code=200,
                json=MagicMock(return_value=mock_tool_response),
                raise_for_status=MagicMock()
            ))
            mock_client_class.return_value = mock_client
            
            async with GatewaySearchClient(gateway_url="http://localhost:8080") as client:
                await client.search("test query", limit=5)
            
            # Verify the call was made to Gateway tool execution endpoint
            mock_client.post.assert_called()
            call_args = mock_client.post.call_args
            
            # Verify /v1/tools/execute endpoint was called
            call_url = call_args[0][0] if call_args[0] else ""
            assert "/v1/tools/execute" in call_url, (
                f"Tool execution should call /v1/tools/execute endpoint. Got: {call_url}"
            )
            
            # Verify search_corpus tool was invoked
            call_json = call_args[1].get("json", {}) if len(call_args) > 1 else {}
            assert call_json.get("name") == "search_corpus", (
                f"Should invoke search_corpus tool. Got: {call_json}"
            )


@pytest.mark.integration
class TestEnhancementScriptRouting:
    """
    Tests for llm_enhance_guideline.py routing through Gateway.
    """

    def test_enhancement_script_uses_factory(self):
        """
        RED TEST: Enhancement script should use factory, not direct AnthropicProvider.
        
        Current behavior: Imports AnthropicProvider directly (WRONG)
        Expected behavior: Uses create_llm_provider() factory (CORRECT)
        """
        import ast
        from pathlib import Path
        
        script_path = Path("/Users/kevintoles/POC/llm-document-enhancer/workflows/llm_enhancement/scripts/llm_enhance_guideline.py")
        
        if not script_path.exists():
            pytest.skip("Enhancement script not found")
        
        content = script_path.read_text()
        
        # Check for direct AnthropicProvider import
        has_direct_import = "from workflows.shared.providers import AnthropicProvider" in content
        has_direct_import = has_direct_import or "from workflows.shared.providers.anthropic_provider import AnthropicProvider" in content
        
        # Check for factory usage
        has_factory_import = "from workflows.shared.providers.factory import create_llm_provider" in content
        has_factory_import = has_factory_import or "from workflows.shared.providers import create_llm_provider" in content
        
        assert not has_direct_import or has_factory_import, (
            "llm_enhance_guideline.py should use create_llm_provider() factory "
            "instead of importing AnthropicProvider directly. "
            "This ensures traffic routes through Gateway based on LLM_PROVIDER env var."
        )

    def test_enhancement_script_no_hardcoded_provider(self):
        """
        RED TEST: Enhancement script should not instantiate AnthropicProvider directly.
        
        Check that the script doesn't have hardcoded:
        - provider = AnthropicProvider()
        - AnthropicProvider(api_key=...)
        """
        from pathlib import Path
        
        script_path = Path("/Users/kevintoles/POC/llm-document-enhancer/workflows/llm_enhancement/scripts/llm_enhance_guideline.py")
        
        if not script_path.exists():
            pytest.skip("Enhancement script not found")
        
        content = script_path.read_text()
        
        # Look for direct instantiation patterns
        problematic_patterns = [
            "AnthropicProvider(",
            "= AnthropicProvider",
        ]
        
        for pattern in problematic_patterns:
            if pattern in content:
                # This is acceptable ONLY in factory.py, not in the script
                pytest.fail(
                    f"Found '{pattern}' in llm_enhance_guideline.py. "
                    "Direct provider instantiation bypasses Gateway routing. "
                    "Use create_llm_provider() factory instead."
                )


@pytest.mark.integration
class TestDockerComposeConfiguration:
    """
    Tests for docker-compose.yml Gateway configuration.
    """

    def test_docker_compose_has_llm_provider_env(self):
        """
        RED TEST: docker-compose.yml should set LLM_PROVIDER=gateway.
        
        This ensures containers default to using Gateway.
        """
        from pathlib import Path
        import yaml
        
        compose_path = Path("/Users/kevintoles/POC/llm-document-enhancer/docker-compose.yml")
        
        if not compose_path.exists():
            pytest.skip("docker-compose.yml not found")
        
        content = compose_path.read_text()
        
        # Check if LLM_PROVIDER is set anywhere
        has_llm_provider = "LLM_PROVIDER" in content
        
        if has_llm_provider:
            # Verify it's set to gateway
            assert "LLM_PROVIDER=gateway" in content or "LLM_PROVIDER: gateway" in content, (
                "docker-compose.yml has LLM_PROVIDER but it's not set to 'gateway'. "
                "All containers should default to routing through Gateway."
            )
        else:
            pytest.fail(
                "docker-compose.yml is missing LLM_PROVIDER environment variable. "
                "Add 'LLM_PROVIDER=gateway' to ensure Gateway routing."
            )

    def test_docker_compose_has_gateway_url(self):
        """
        RED TEST: docker-compose.yml should set LLM_GATEWAY_URL.
        
        Containers need to know the Gateway address.
        """
        from pathlib import Path
        
        compose_path = Path("/Users/kevintoles/POC/llm-document-enhancer/docker-compose.yml")
        
        if not compose_path.exists():
            pytest.skip("docker-compose.yml not found")
        
        content = compose_path.read_text()
        
        has_gateway_url = "LLM_GATEWAY_URL" in content
        
        assert has_gateway_url, (
            "docker-compose.yml is missing LLM_GATEWAY_URL environment variable. "
            "Add 'LLM_GATEWAY_URL=http://llm-gateway:8080' for container-to-container communication."
        )
