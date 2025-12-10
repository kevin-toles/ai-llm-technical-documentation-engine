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
"""

from workflows.shared.clients.llm_gateway import LLMGatewayClient
from workflows.shared.clients.search_client import SemanticSearchClient

__all__ = ["LLMGatewayClient", "SemanticSearchClient"]

