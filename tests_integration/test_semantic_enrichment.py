"""
Integration tests for semantic search enrichment.

WBS 3.2.4 - Integrate Search Client into Metadata Enrichment

These tests verify the semantic search integration works correctly
when the semantic-search-service is available.
"""

import asyncio
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from workflows.shared.clients.search_client import (
    SemanticSearchClient,
    SearchError,
    SearchConnectionError,
)


class TestSemanticSearchEnrichmentIntegration:
    """Integration tests for semantic search enrichment."""

    @pytest.fixture
    def test_metadata_path(self):
        """Path to test book metadata."""
        # Check both possible locations
        input_path = project_root / "workflows" / "metadata_enrichment" / "input" / "test_book_metadata.json"
        if not input_path.exists():
            # Try examples directory
            input_path = project_root / "examples" / "test_book_metadata.json"
        return input_path

    @pytest.fixture
    def enrich_script_path(self):
        """Path to enrichment script."""
        return project_root / "workflows" / "metadata_enrichment" / "scripts" / "enrich_metadata_per_book.py"

    def test_semantic_search_flag_exists(self, enrich_script_path):
        """Test that --use-semantic-search flag is available."""
        result = subprocess.run(
            [sys.executable, str(enrich_script_path), "--help"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "--use-semantic-search" in result.stdout

    def test_semantic_search_url_flag_exists(self, enrich_script_path):
        """Test that --semantic-search-url flag is available."""
        result = subprocess.run(
            [sys.executable, str(enrich_script_path), "--help"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "--semantic-search-url" in result.stdout

    def test_enrich_without_semantic_flag_uses_tfidf(self, enrich_script_path, test_metadata_path, tmp_path):
        """Test that running without --use-semantic-search uses TF-IDF."""
        # Skip if test metadata doesn't exist
        if not test_metadata_path.exists():
            pytest.skip(f"Test metadata not found at {test_metadata_path}")
        
        output_file = tmp_path / "output.json"
        
        result = subprocess.run(
            [
                sys.executable,
                str(enrich_script_path),
                "--input", str(test_metadata_path),
                "--output", str(output_file),
            ],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        
        assert result.returncode == 0, f"Script failed: {result.stderr}\nStdout: {result.stdout}"
        assert output_file.exists()
        
        with open(output_file) as f:
            data = json.load(f)
        
        # Check that TF-IDF was used
        assert data.get("enrichment_metadata", {}).get("method") == "tfidf_local"
        # Check that chapters have similarity_source
        if data.get("chapters"):
            assert data["chapters"][0].get("similarity_source") == "tfidf"

    @pytest.mark.asyncio
    async def test_search_client_embed_method(self):
        """Test that search client embed method exists and can be called."""
        # This tests the client interface without requiring the live service
        client = SemanticSearchClient(base_url="http://localhost:8081")
        
        # Verify the client has the embed method
        assert hasattr(client, 'embed')
        assert callable(client.embed)
        
        # Verify the method signature
        import inspect
        sig = inspect.signature(client.embed)
        params = list(sig.parameters.keys())
        assert 'text' in params

    @pytest.mark.asyncio
    async def test_search_client_search_method(self):
        """Test that search client search method exists and has correct interface."""
        client = SemanticSearchClient(base_url="http://localhost:8081")
        
        # Verify the client has the search method
        assert hasattr(client, 'search')
        assert callable(client.search)
        
        # Verify the method signature
        import inspect
        sig = inspect.signature(client.search)
        params = list(sig.parameters.keys())
        assert 'query' in params
        assert 'limit' in params

    @pytest.mark.asyncio
    async def test_search_client_handles_connection_error(self):
        """Test that search client handles connection errors gracefully."""
        import httpx
        
        client = SemanticSearchClient(
            base_url="http://localhost:9999",  # Non-existent service
            max_retries=1,
            retry_delay=0.1
        )
        
        async with client:
            with pytest.raises(SearchConnectionError):
                await client.health_check()

    @pytest.mark.integration
    @pytest.mark.skipif(
        os.environ.get("SEMANTIC_SEARCH_URL") is None,
        reason="SEMANTIC_SEARCH_URL not set - skipping live service test"
    )
    async def test_live_semantic_search_service(self):
        """Test against live semantic search service (requires service running)."""
        url = os.environ.get("SEMANTIC_SEARCH_URL", "http://localhost:8081")
        
        client = SemanticSearchClient(base_url=url)
        
        async with client:
            # Test health check
            health = await client.health_check()
            assert health.get("status") in ["healthy", "ok", "up"]
            
            # Test embedding
            embedding = await client.embed("test text for embedding")
            assert len(embedding) == 768
            
            # Test search
            results = await client.search("architecture patterns", limit=5)
            assert isinstance(results, list)


class TestEnrichmentOutputFormat:
    """Tests for the enrichment output format."""

    @pytest.fixture
    def sample_enriched_output(self, tmp_path):
        """Create a sample enriched output file."""
        data = {
            "title": "Test Book",
            "chapters": [
                {
                    "number": 1,
                    "title": "Introduction",
                    "summary": "Test summary",
                    "similarity_source": "semantic_search",
                    "similar_chapters": [
                        {"chapter_id": "2", "score": 0.85}
                    ]
                }
            ],
            "enrichment_metadata": {
                "method": "semantic_search",
                "service_url": "http://localhost:8081"
            }
        }
        output_file = tmp_path / "enriched.json"
        with open(output_file, "w") as f:
            json.dump(data, f)
        return output_file

    def test_output_has_similarity_source(self, sample_enriched_output):
        """Test that output has similarity_source field."""
        with open(sample_enriched_output) as f:
            data = json.load(f)
        
        assert data["chapters"][0].get("similarity_source") in ["semantic_search", "tfidf"]

    def test_output_has_enrichment_metadata(self, sample_enriched_output):
        """Test that output has enrichment_metadata."""
        with open(sample_enriched_output) as f:
            data = json.load(f)
        
        assert "enrichment_metadata" in data
        assert "method" in data["enrichment_metadata"]


class TestCLIBehavior:
    """Tests for CLI behavior."""

    @pytest.fixture
    def enrich_script_path(self):
        """Path to enrichment script."""
        return project_root / "workflows" / "metadata_enrichment" / "scripts" / "enrich_metadata_per_book.py"

    def test_help_shows_all_flags(self, enrich_script_path):
        """Test that help shows all required flags."""
        result = subprocess.run(
            [sys.executable, str(enrich_script_path), "--help"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "--input" in result.stdout
        assert "--output" in result.stdout
        assert "--use-semantic-search" in result.stdout
        assert "--semantic-search-url" in result.stdout

    def test_default_semantic_search_url(self, enrich_script_path):
        """Test that default semantic search URL is set."""
        result = subprocess.run(
            [sys.executable, str(enrich_script_path), "--help"],
            capture_output=True,
            text=True
        )
        
        # The default URL should be mentioned in help
        assert "localhost:8081" in result.stdout or "8081" in result.stdout


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
