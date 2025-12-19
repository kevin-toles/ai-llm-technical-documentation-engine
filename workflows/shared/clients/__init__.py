"""
Clients Package - WBS 3.1.1.1

HTTP clients for external service integration.

Reference Documents:
- GUIDELINES: Connection pooling (Newman p. 359-360 "different connection pools")
- GUIDELINES: Circuit breakers, timeouts, bulkheads (Newman p. 352-360)
- CODING_PATTERNS_ANALYSIS: Anti-Pattern - new httpx.AsyncClient per request (line 67)

Clients:
- LLMGatewayClient: Async client for llm-gateway microservice
- MSEPClient: Async client for Gateway -> ai-agents MSEP API (WBS MSE-6.1)
- SemanticSearchClient: Async client for semantic-search-service (WBS 3.2.3)
- OrchestratorClient: Async client for Code-Orchestrator-Service (WBS 5.1.2)

NOTE: All external clients MUST route through Gateway:8080 per Kitchen Brigade architecture.
Direct calls to platform services (ai-agents:8082, Code-Orchestrator:8083) are VIOLATIONS.

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
from workflows.shared.clients.msep_client import (
    ChapterMeta,
    CrossReference,
    EnrichedChapter,
    EnrichedMetadataResponse,
    MergedKeywords,
    MSEPAPIError,
    MSEPClient,
    MSEPClientError,
    MSEPClientProtocol,
    MSEPConfig,
    MSEPConnectionError,
    MSEPTimeoutError,
    Provenance,
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
from workflows.shared.clients.search_client import SemanticSearchClient

__all__ = [
    # Gateway Clients (Kitchen Brigade: CUSTOMER -> ROUTER)
    "LLMGatewayClient",
    "MSEPClient",
    "MSEPClientError",
    "MSEPTimeoutError",
    "MSEPConnectionError",
    "MSEPAPIError",
    "MSEPClientProtocol",
    "ChapterMeta",
    "MSEPConfig",
    "CrossReference",
    "MergedKeywords",
    "Provenance",
    "EnrichedChapter",
    "EnrichedMetadataResponse",
    # Search Client
    "SemanticSearchClient",
    # Orchestrator Client (internal platform use only)
    "OrchestratorClient",
    "OrchestratorClientError",
    "OrchestratorTimeoutError",
    "OrchestratorConnectionError",
    "OrchestratorAPIError",
    "OrchestratorClientProtocol",
    "FakeOrchestratorClient",
    "SEMANTIC_SIMILARITY_THRESHOLD",
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

