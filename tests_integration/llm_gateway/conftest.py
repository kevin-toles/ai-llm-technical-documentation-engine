"""
Conftest for llm-gateway integration tests.

Provides fixtures and configuration for cross-service integration testing.
Migrated from llm-gateway/tests/integration/conftest.py
"""

import os
import pytest
import httpx


# =============================================================================
# Service URLs (configured via environment or defaults for Docker)
# =============================================================================

GATEWAY_URL = os.getenv("GATEWAY_URL", "http://localhost:8080")
SEMANTIC_SEARCH_URL = os.getenv("SEMANTIC_SEARCH_URL", "http://localhost:8081")
AI_AGENTS_URL = os.getenv("AI_AGENTS_URL", "http://localhost:8082")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def gateway_url() -> str:
    """Return the gateway URL."""
    return GATEWAY_URL


@pytest.fixture
def semantic_search_url() -> str:
    """Return the semantic search service URL."""
    return SEMANTIC_SEARCH_URL


@pytest.fixture
def ai_agents_url() -> str:
    """Return the AI agents service URL."""
    return AI_AGENTS_URL


@pytest.fixture
def redis_url() -> str:
    """Return the Redis URL."""
    return REDIS_URL


@pytest.fixture
async def gateway_client() -> httpx.AsyncClient:
    """Create an async HTTP client for the gateway."""
    async with httpx.AsyncClient(base_url=GATEWAY_URL, timeout=30.0) as client:
        yield client


@pytest.fixture
async def semantic_search_client() -> httpx.AsyncClient:
    """Create an async HTTP client for semantic search service."""
    async with httpx.AsyncClient(base_url=SEMANTIC_SEARCH_URL, timeout=30.0) as client:
        yield client


@pytest.fixture
async def ai_agents_client() -> httpx.AsyncClient:
    """Create an async HTTP client for AI agents service."""
    async with httpx.AsyncClient(base_url=AI_AGENTS_URL, timeout=30.0) as client:
        yield client
