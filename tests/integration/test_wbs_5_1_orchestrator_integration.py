#!/usr/bin/env python3
"""
WBS 5.1: Enrichment Script Integration Tests - OrchestratorClient & CLI Flag

Test-Driven Development (TDD) - RED Phase
These tests should FAIL initially until GREEN phase implementation.

Reference Documents:
- WBS_IMPLEMENTATION.md: Phase 5 - Integration with llm-document-enhancer
- CODING_PATTERNS_ANALYSIS.md: Anti-Pattern #12 (Connection Pooling), #2.3 (Retry Logic)
- ARCHITECTURE.md (llm-gateway): Code-Orchestrator-Service = Sous Chef (Port 8083)

Anti-Patterns Addressed:
- #12: Connection Pooling - Must reuse httpx.AsyncClient, not create new per request
- #2.3: Retry Logic - Implement _classify_error() helper with exponential backoff
- #7, #13: Exception Shadowing - Use namespaced OrchestratorClientError
- #4.4: Protocol Compliance - Use underscore prefix for unused protocol params
"""

import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

# Project root for path resolution
PROJECT_ROOT = Path(__file__).parent.parent.parent


# =============================================================================
# WBS 5.1.1: CLI Flag --use-orchestrator Tests
# =============================================================================
class TestCliOrchestratorFlag:
    """Test suite for WBS 5.1.1: Add --use-orchestrator flag."""

    def test_argparse_accepts_use_orchestrator_flag(self):
        """
        RED TEST: argparse should accept --use-orchestrator flag.
        
        Acceptance Criteria: CLI arg to enable orchestrator
        """
        import sys
        
        # Import the enrichment script's argument parser
        sys.path.insert(0, str(PROJECT_ROOT / "workflows" / "metadata_enrichment" / "scripts"))
        
        try:
            from enrich_metadata_per_book import create_argument_parser
            parser = create_argument_parser()
        except (ImportError, AttributeError):
            # Function doesn't exist yet - RED phase expected
            pytest.fail("create_argument_parser() function not found - implement in GREEN phase")
            return
        
        # Parse with --use-orchestrator flag
        args = parser.parse_args([
            "--input", "test.json",
            "--taxonomy", "tax.json",
            "--output", "out.json",
            "--use-orchestrator"
        ])
        
        assert hasattr(args, "use_orchestrator"), "--use-orchestrator flag not defined"
        assert args.use_orchestrator is True

    def test_argparse_accepts_orchestrator_url(self):
        """
        RED TEST: argparse should accept --orchestrator-url argument.
        
        Default should be http://localhost:8083 per ARCHITECTURE.md
        """
        import sys
        sys.path.insert(0, str(PROJECT_ROOT / "workflows" / "metadata_enrichment" / "scripts"))
        
        try:
            from enrich_metadata_per_book import create_argument_parser
            parser = create_argument_parser()
        except (ImportError, AttributeError):
            pytest.fail("create_argument_parser() function not found")
            return
        
        # Test default URL
        args = parser.parse_args([
            "--input", "test.json",
            "--taxonomy", "tax.json", 
            "--output", "out.json"
        ])
        assert args.orchestrator_url == "http://localhost:8083"
        
        # Test custom URL
        args = parser.parse_args([
            "--input", "test.json",
            "--taxonomy", "tax.json",
            "--output", "out.json",
            "--orchestrator-url", "http://custom:9000"
        ])
        assert args.orchestrator_url == "http://custom:9000"

    def test_use_orchestrator_defaults_to_false(self):
        """
        RED TEST: --use-orchestrator defaults to False (TF-IDF fallback).
        """
        import sys
        sys.path.insert(0, str(PROJECT_ROOT / "workflows" / "metadata_enrichment" / "scripts"))
        
        try:
            from enrich_metadata_per_book import create_argument_parser
            parser = create_argument_parser()
        except (ImportError, AttributeError):
            pytest.fail("create_argument_parser() function not found")
            return
        
        args = parser.parse_args([
            "--input", "test.json",
            "--taxonomy", "tax.json",
            "--output", "out.json"
        ])
        
        assert args.use_orchestrator is False


# =============================================================================
# WBS 5.1.2: OrchestratorClient Tests
# =============================================================================
class TestOrchestratorClientModule:
    """Test suite for WBS 5.1.2: Create OrchestratorClient."""

    def test_orchestrator_client_module_exists(self):
        """
        RED TEST: OrchestratorClient module should exist.
        
        Path: workflows/shared/clients/orchestrator_client.py
        """
        module_path = PROJECT_ROOT / "workflows" / "shared" / "clients" / "orchestrator_client.py"
        assert module_path.exists(), f"Module not found: {module_path}"

    def test_orchestrator_client_class_exists(self):
        """
        RED TEST: OrchestratorClient class should be importable.
        """
        try:
            from workflows.shared.clients.orchestrator_client import OrchestratorClient
            assert OrchestratorClient
        except ImportError:
            pytest.fail("OrchestratorClient class not found - implement in GREEN phase")

    def test_orchestrator_client_protocol_exists(self):
        """
        RED TEST: OrchestratorClientProtocol for duck typing.
        
        Anti-Pattern #4.4: Use Protocol for testable dependency injection.
        """
        try:
            from workflows.shared.clients.orchestrator_client import OrchestratorClientProtocol
            assert hasattr(OrchestratorClientProtocol, "search")
        except ImportError:
            pytest.fail("OrchestratorClientProtocol not found - implement in GREEN phase")


class TestOrchestratorClientInit:
    """Test OrchestratorClient initialization."""

    def test_client_init_with_base_url(self):
        """
        RED TEST: Client accepts base_url parameter.
        """
        try:
            from workflows.shared.clients.orchestrator_client import OrchestratorClient
            client = OrchestratorClient(base_url="http://localhost:8083")
            assert client.base_url == "http://localhost:8083"
        except ImportError:
            pytest.fail("OrchestratorClient not found")

    def test_client_init_with_timeout(self):
        """
        RED TEST: Client accepts timeout parameter (default 30s).
        """
        try:
            from workflows.shared.clients.orchestrator_client import OrchestratorClient
            client = OrchestratorClient(base_url="http://localhost:8083", timeout=60.0)
            assert client.timeout == pytest.approx(60.0)
        except ImportError:
            pytest.fail("OrchestratorClient not found")

    def test_client_init_with_max_retries(self):
        """
        RED TEST: Client accepts max_retries parameter (default 3).
        
        Anti-Pattern #2.3: Retry with exponential backoff.
        """
        try:
            from workflows.shared.clients.orchestrator_client import OrchestratorClient
            client = OrchestratorClient(base_url="http://localhost:8083", max_retries=5)
            assert client.max_retries == 5
        except ImportError:
            pytest.fail("OrchestratorClient not found")

    def test_client_reuses_httpx_client(self):
        """
        RED TEST: Client reuses httpx.AsyncClient (Anti-Pattern #12).
        
        Anti-Pattern #12: Connection Pooling - must not create new client per request.
        """
        try:
            from workflows.shared.clients.orchestrator_client import OrchestratorClient
            client = OrchestratorClient(base_url="http://localhost:8083")
            assert hasattr(client, "_client"), "Client should have _client attribute for connection pooling"
        except ImportError:
            pytest.fail("OrchestratorClient not found")


class TestOrchestratorClientSearch:
    """Test OrchestratorClient.search() method."""

    @pytest.mark.asyncio
    async def test_search_method_exists(self):
        """
        RED TEST: Client has async search() method.
        """
        try:
            from workflows.shared.clients.orchestrator_client import OrchestratorClient
            client = OrchestratorClient(base_url="http://localhost:8083")
            assert hasattr(client, "search"), "Client should have search() method"
            assert callable(client.search)
        except ImportError:
            pytest.fail("OrchestratorClient not found")

    @pytest.mark.asyncio
    async def test_search_accepts_query_and_domain(self):
        """
        RED TEST: search() accepts query and domain parameters.
        """
        try:
            from workflows.shared.clients.orchestrator_client import OrchestratorClient
            client = OrchestratorClient(base_url="http://localhost:8083")
            
            # Mock the HTTP call - use request method since that's what _request_with_retry uses
            with patch.object(client, "_client") as mock_client:
                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.json.return_value = {"results": []}
                mock_client.request = AsyncMock(return_value=mock_response)
                
                results = await client.search(
                    query="LLM document chunking",
                    domain="ai-ml"
                )
                
                assert isinstance(results, list)
        except ImportError:
            pytest.fail("OrchestratorClient not found")

    @pytest.mark.asyncio
    async def test_search_accepts_top_k(self):
        """
        RED TEST: search() accepts top_k parameter.
        """
        try:
            from workflows.shared.clients.orchestrator_client import OrchestratorClient
            client = OrchestratorClient(base_url="http://localhost:8083")
            
            with patch.object(client, "_client") as mock_client:
                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.json.return_value = {"results": []}
                mock_client.request = AsyncMock(return_value=mock_response)
                
                results = await client.search(
                    query="test",
                    domain="ai-ml",
                    top_k=10
                )
                
                assert isinstance(results, list)
        except ImportError:
            pytest.fail("OrchestratorClient not found")


class TestOrchestratorClientErrors:
    """Test OrchestratorClient error handling."""

    def test_orchestrator_client_error_exists(self):
        """
        RED TEST: OrchestratorClientError exception exists.
        
        Anti-Pattern #7, #13: Don't shadow builtins like ConnectionError.
        """
        try:
            from workflows.shared.clients.orchestrator_client import OrchestratorClientError
            assert issubclass(OrchestratorClientError, Exception)
        except ImportError:
            pytest.fail("OrchestratorClientError not found")

    def test_orchestrator_client_error_has_status_code(self):
        """
        RED TEST: OrchestratorClientError stores status_code.
        """
        try:
            from workflows.shared.clients.orchestrator_client import OrchestratorClientError
            error = OrchestratorClientError("Test error", status_code=500)
            assert error.status_code == 500
        except ImportError:
            pytest.fail("OrchestratorClientError not found")

    @pytest.mark.asyncio
    async def test_search_returns_empty_on_5xx(self):
        """
        RED TEST: search() returns empty list on 5xx errors (graceful degradation).
        """
        try:
            from workflows.shared.clients.orchestrator_client import OrchestratorClient
            client = OrchestratorClient(base_url="http://localhost:8083")
            
            with patch.object(client, "_client") as mock_client:
                mock_response = MagicMock()
                mock_response.status_code = 500
                mock_client.request = AsyncMock(return_value=mock_response)
                
                results = await client.search(query="test", domain="ai-ml")
                assert results == [], "Should return empty list on 5xx"
        except ImportError:
            pytest.fail("OrchestratorClient not found")

    @pytest.mark.asyncio
    async def test_search_raises_on_4xx(self):
        """
        RED TEST: search() raises OrchestratorClientError on 4xx errors.
        """
        try:
            from workflows.shared.clients.orchestrator_client import (
                OrchestratorClient,
                OrchestratorAPIError
            )
            client = OrchestratorClient(base_url="http://localhost:8083")
            
            with patch.object(client, "_client") as mock_client:
                mock_response = MagicMock()
                mock_response.status_code = 400
                mock_response.text = "Bad Request"
                mock_response.json.return_value = {"detail": "Bad Request"}
                mock_client.request = AsyncMock(return_value=mock_response)
                
                with pytest.raises(OrchestratorAPIError) as exc_info:
                    await client.search(query="test", domain="ai-ml")
                
                assert exc_info.value.status_code == 400
        except ImportError:
            pytest.fail("OrchestratorClient not found")

    @pytest.mark.asyncio  
    async def test_search_retries_on_timeout(self):
        """
        RED TEST: search() retries on timeout with exponential backoff.
        
        Anti-Pattern #2.3: Must use _classify_error() and exponential backoff.
        """
        try:
            from workflows.shared.clients.orchestrator_client import OrchestratorClient
            client = OrchestratorClient(
                base_url="http://localhost:8083",
                max_retries=3,
                retry_delay=0.01  # Fast for testing
            )
            
            call_count = 0
            
            async def mock_request(*_args, **_kwargs):
                import asyncio
                await asyncio.sleep(0)  # Yield to event loop
                nonlocal call_count
                call_count += 1
                if call_count < 3:
                    import httpx
                    raise httpx.TimeoutException("Connection timed out")
                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.json.return_value = {"results": []}
                return mock_response
            
            with patch.object(client, "_client") as mock_client:
                mock_client.request = mock_request
                
                results = await client.search(query="test", domain="ai-ml")
                
                assert call_count == 3, f"Expected 3 retries, got {call_count}"
                assert results == []
        except ImportError:
            pytest.fail("OrchestratorClient not found")


class TestFakeOrchestratorClient:
    """Test FakeOrchestratorClient for unit testing."""

    def test_fake_client_exists(self):
        """
        RED TEST: FakeOrchestratorClient for testing without real service.
        """
        try:
            from workflows.shared.clients.orchestrator_client import FakeOrchestratorClient
            assert FakeOrchestratorClient
        except ImportError:
            pytest.fail("FakeOrchestratorClient not found")

    def test_fake_client_implements_protocol(self):
        """
        RED TEST: FakeOrchestratorClient implements OrchestratorClientProtocol.
        """
        try:
            from workflows.shared.clients.orchestrator_client import (
                FakeOrchestratorClient,
                OrchestratorClientProtocol,  # noqa: F401 - imported for protocol documentation
            )
            client = FakeOrchestratorClient()
            assert hasattr(client, "search")
        except ImportError:
            pytest.fail("FakeOrchestratorClient not found")

    @pytest.mark.asyncio
    async def test_fake_client_returns_configured_results(self):
        """
        RED TEST: FakeOrchestratorClient returns preconfigured results.
        """
        try:
            from workflows.shared.clients.orchestrator_client import FakeOrchestratorClient
            
            fake_results = [
                {"book": "AI Engineering", "chapter": 5, "relevance_score": 0.85}
            ]
            client = FakeOrchestratorClient(results=fake_results)
            
            results = await client.search(query="test", domain="ai-ml")
            assert results == fake_results
        except ImportError:
            pytest.fail("FakeOrchestratorClient not found")
