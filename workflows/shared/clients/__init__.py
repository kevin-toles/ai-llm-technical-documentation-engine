"""
Clients Package - WBS 3.1.1.1

HTTP clients for external service integration.

Reference Documents:
- GUIDELINES: Connection pooling (Newman p. 359-360 "different connection pools")
- GUIDELINES: Circuit breakers, timeouts, bulkheads (Newman p. 352-360)
- CODING_PATTERNS_ANALYSIS: Anti-Pattern - new httpx.AsyncClient per request (line 67)

Clients:
- LLMGatewayClient: Async client for llm-gateway microservice
- SemanticSearchClient: Async client for semantic-search-service (WBS 3.2.3)
- OrchestratorClient: Async client for Code-Orchestrator-Service (WBS 5.1.2)
- SBERTClient: Async client for Code-Orchestrator SBERT API (WBS M3.1)

Observability (WBS 6.2):
- cache: ResultCache for search result caching
- metrics: MetricsCollector, PerformanceLogger, create_span
"""

from workflows.shared.clients import cache
from workflows.shared.clients import metrics
from workflows.shared.clients.cache import (
    ResultCache,
    generate_cache_key,
    get_device,
    is_gpu_available,
)
from workflows.shared.clients.llm_gateway import LLMGatewayClient
from workflows.shared.clients.metrics import (
    MetricsCollector,
    PerformanceLogger,
    Span,
    create_span,
)
from workflows.shared.clients.orchestrator_client import (
    FakeOrchestratorClient,
    OrchestratorAPIError,
    OrchestratorClient,
    OrchestratorClientError,
    OrchestratorClientProtocol,
    OrchestratorConnectionError,
    OrchestratorTimeoutError,
    SEMANTIC_SIMILARITY_THRESHOLD,
)
from workflows.shared.clients.sbert_client import (
    EMBEDDING_DIMENSIONS,
    FakeSBERTClient,
    SBERTAPIError,
    SBERTClient,
    SBERTClientError,
    SBERTClientProtocol,
    SBERTConnectionError,
    SBERTTimeoutError,
)
from workflows.shared.clients.search_client import SemanticSearchClient

__all__ = [
    # Clients
    "LLMGatewayClient",
    "SemanticSearchClient",
    "OrchestratorClient",
    "OrchestratorClientError",
    "OrchestratorTimeoutError",
    "OrchestratorConnectionError",
    "OrchestratorAPIError",
    "OrchestratorClientProtocol",
    "FakeOrchestratorClient",
    "SEMANTIC_SIMILARITY_THRESHOLD",
    # SBERT Client (WBS M3.1)
    "SBERTClient",
    "SBERTClientError",
    "SBERTTimeoutError",
    "SBERTConnectionError",
    "SBERTAPIError",
    "SBERTClientProtocol",
    "FakeSBERTClient",
    "EMBEDDING_DIMENSIONS",
    # Cache (WBS 6.1)
    "cache",
    "ResultCache",
    "generate_cache_key",
    "is_gpu_available",
    "get_device",
    # Metrics (WBS 6.2)
    "metrics",
    "MetricsCollector",
    "PerformanceLogger",
    "Span",
    "create_span",
]

