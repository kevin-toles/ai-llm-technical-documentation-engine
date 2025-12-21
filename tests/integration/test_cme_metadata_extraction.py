"""Integration tests for CME-1.0 Metadata Extraction.

WBS-AC7.6-7.11: Integration tests for CME feature.

These tests require the Code-Orchestrator-Service to be running.
Use pytest -m "integration" to run these tests when the service is available.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict

import pytest

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def orchestrator_url() -> str:
    """Get orchestrator URL from environment or default."""
    return os.environ.get("ORCHESTRATOR_URL", "http://localhost:8083")


@pytest.fixture
def sample_text() -> str:
    """Sample text for extraction testing."""
    return """
    Machine learning is a subset of artificial intelligence that enables 
    systems to learn from data. Deep learning neural networks use multiple 
    layers to progressively extract higher-level features. Transformers 
    revolutionized natural language processing with attention mechanisms.
    Kubernetes orchestrates containerized applications across clusters.
    """


# =============================================================================
# AC7.6: Integration Test - Endpoint Health
# =============================================================================


@pytest.mark.integration
class TestEndpointHealth:
    """AC7.6: Test orchestrator endpoint health."""

    @pytest.mark.asyncio
    async def test_orchestrator_health_endpoint(self, orchestrator_url: str) -> None:
        """AC7.6: Health endpoint returns 200 when service is running."""
        from workflows.shared.clients.metadata_client import MetadataExtractionClient

        async with MetadataExtractionClient(base_url=orchestrator_url) as client:
            is_healthy = await client.health_check()
            
            # If we can connect, service is healthy
            assert is_healthy is True

    @pytest.mark.asyncio
    async def test_client_connects_successfully(self, orchestrator_url: str) -> None:
        """AC7.6: MetadataExtractionClient connects to running service."""
        from workflows.shared.clients.metadata_client import MetadataExtractionClient

        async with MetadataExtractionClient(base_url=orchestrator_url) as client:
            # Should be able to enter context without error
            assert client._http_client is not None


# =============================================================================
# AC7.7: Integration Test - Full Extraction
# =============================================================================


@pytest.mark.integration
class TestFullExtraction:
    """AC7.7: Test full metadata extraction via orchestrator."""

    @pytest.mark.asyncio
    async def test_extract_metadata_returns_keywords(
        self, orchestrator_url: str, sample_text: str
    ) -> None:
        """AC7.7: Extract metadata returns keywords from text."""
        from workflows.shared.clients.metadata_client import MetadataExtractionClient

        async with MetadataExtractionClient(base_url=orchestrator_url) as client:
            result = await client.extract_metadata(sample_text)
            
            # Should have keywords
            assert len(result.keywords) > 0
            assert all(hasattr(k, 'term') and hasattr(k, 'score') for k in result.keywords)

    @pytest.mark.asyncio
    async def test_extract_metadata_returns_concepts(
        self, orchestrator_url: str, sample_text: str
    ) -> None:
        """AC7.7: Extract metadata returns concepts from text."""
        from workflows.shared.clients.metadata_client import MetadataExtractionClient

        async with MetadataExtractionClient(base_url=orchestrator_url) as client:
            result = await client.extract_metadata(sample_text)
            
            # Should have concepts
            assert hasattr(result, 'concepts')

    @pytest.mark.asyncio
    async def test_extract_metadata_returns_quality_score(
        self, orchestrator_url: str, sample_text: str
    ) -> None:
        """AC7.7: Extract metadata returns quality score between 0-1."""
        from workflows.shared.clients.metadata_client import MetadataExtractionClient

        async with MetadataExtractionClient(base_url=orchestrator_url) as client:
            result = await client.extract_metadata(sample_text)
            
            # Quality score should be between 0 and 1
            assert 0.0 <= result.quality_score <= 1.0


# =============================================================================
# AC7.8: Integration Test - Client → Service
# =============================================================================


@pytest.mark.integration
class TestClientServiceCommunication:
    """AC7.8: Test client to service communication."""

    @pytest.mark.asyncio
    async def test_client_sends_correct_payload(
        self, orchestrator_url: str, sample_text: str
    ) -> None:
        """AC7.8: Client sends properly formatted request to service."""
        from workflows.shared.clients.metadata_client import MetadataExtractionClient

        async with MetadataExtractionClient(base_url=orchestrator_url) as client:
            # Should not raise on valid request
            result = await client.extract_metadata(sample_text)
            
            assert result is not None

    @pytest.mark.asyncio
    async def test_client_handles_options(
        self, orchestrator_url: str, sample_text: str
    ) -> None:
        """AC7.8: Client passes extraction options to service."""
        from workflows.shared.clients.metadata_client import MetadataExtractionClient

        async with MetadataExtractionClient(base_url=orchestrator_url) as client:
            result = await client.extract_metadata(
                sample_text,
                top_k_keywords=5,
                filter_noise=True
            )
            
            # Should respect top_k_keywords limit
            assert len(result.keywords) <= 5


# =============================================================================
# AC7.9: Integration Test - Fallback Scenario
# =============================================================================


@pytest.mark.integration
class TestFallbackScenario:
    """AC7.9: Test fallback to local extraction on error."""

    @pytest.mark.asyncio
    async def test_generator_fallback_on_service_down(self, tmp_path: Path) -> None:
        """AC7.9: Generator falls back to local when service unavailable."""
        from workflows.metadata_extraction.scripts.generate_metadata_universal import (
            UniversalMetadataGenerator,
        )

        book_data = {
            "title": "Fallback Test Book",
            "pages": [
                {"page_number": 1, "content": "Machine learning and neural networks content."},
            ]
        }
        json_file = tmp_path / "fallback_book.json"
        json_file.write_text(json.dumps(book_data))

        # Use orchestrator mode with fallback, pointing to non-existent service
        generator = UniversalMetadataGenerator(
            json_file,
            use_orchestrator=True,
            fallback_on_error=True,
            orchestrator_url="http://localhost:9999"  # Not running
        )

        chapters = [(1, "Chapter 1", 1, 1)]
        
        # Should fall back to local extraction without error
        metadata_list = generator.generate_metadata(chapters)
        
        assert len(metadata_list) == 1
        assert metadata_list[0].chapter_number == 1


# =============================================================================
# AC7.10: Integration Test - Generator End-to-End
# =============================================================================


@pytest.mark.integration
class TestGeneratorEndToEnd:
    """AC7.10: Test generator end-to-end with orchestrator."""

    @pytest.mark.asyncio
    async def test_generator_orchestrator_mode(
        self, orchestrator_url: str, tmp_path: Path
    ) -> None:
        """AC7.10: Generator uses orchestrator for extraction."""
        from workflows.metadata_extraction.scripts.generate_metadata_universal import (
            UniversalMetadataGenerator,
        )

        book_data = {
            "title": "E2E Test Book",
            "pages": [
                {"page_number": 1, "content": "Introduction to machine learning algorithms and neural network architectures. Deep learning has revolutionized computer vision."},
                {"page_number": 2, "content": "Kubernetes container orchestration enables scalable microservices deployments across cloud infrastructure."},
            ]
        }
        json_file = tmp_path / "e2e_book.json"
        json_file.write_text(json.dumps(book_data))

        generator = UniversalMetadataGenerator(
            json_file,
            use_orchestrator=True,
            orchestrator_url=orchestrator_url
        )

        chapters = [(1, "ML Chapter", 1, 2)]
        metadata_list = generator.generate_metadata(chapters)

        assert len(metadata_list) == 1
        assert len(metadata_list[0].keywords) > 0

    @pytest.mark.asyncio
    async def test_generator_output_schema_matches(
        self, orchestrator_url: str, tmp_path: Path
    ) -> None:
        """AC7.10: Output schema identical between orchestrator and local modes."""
        from workflows.metadata_extraction.scripts.generate_metadata_universal import (
            UniversalMetadataGenerator,
        )

        book_data = {
            "title": "Schema Test Book",
            "pages": [
                {"page_number": 1, "content": "Machine learning neural networks deep learning."},
            ]
        }
        json_file = tmp_path / "schema_book.json"
        json_file.write_text(json.dumps(book_data))

        chapters = [(1, "Test Chapter", 1, 1)]

        # Orchestrator mode
        orch_generator = UniversalMetadataGenerator(
            json_file,
            use_orchestrator=True,
            orchestrator_url=orchestrator_url
        )
        orch_result = orch_generator.generate_metadata(chapters)

        # Local mode
        local_generator = UniversalMetadataGenerator(
            json_file,
            use_orchestrator=False
        )
        local_result = local_generator.generate_metadata(chapters)

        # Both should have same structure
        assert type(orch_result[0]) == type(local_result[0])
        assert hasattr(orch_result[0], 'chapter_number')
        assert hasattr(orch_result[0], 'title')
        assert hasattr(orch_result[0], 'keywords')
        assert hasattr(orch_result[0], 'concepts')
        assert hasattr(orch_result[0], 'summary')
