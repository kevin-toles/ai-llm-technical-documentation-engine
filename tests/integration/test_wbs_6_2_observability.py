"""
WBS 6.2: Observability Tests

TDD RED Phase - Tests written BEFORE implementation.

Reference Documents:
- WBS_IMPLEMENTATION.md: Phase 6.2 - Observability
- GUIDELINES p. 2309: Prometheus metrics patterns
- GUIDELINES p. 2145: Structured logging, tracing

WBS Items:
- 6.2.1: Prometheus metrics - /metrics endpoint with counters
- 6.2.2: Trace spans - spans for each pipeline stage
- 6.2.3: Performance logs - log inference times per model
"""

import json
import logging
import time
from unittest.mock import AsyncMock, patch

import pytest


# =============================================================================
# WBS 6.2.1: Prometheus Metrics Tests
# =============================================================================


class TestPrometheusMetrics:
    """Tests for Prometheus metrics collection."""

    def test_metrics_module_exists(self):
        """Metrics module exists in shared clients."""
        from workflows.shared.clients import metrics
        assert metrics is not None

    def test_metrics_collector_class_exists(self):
        """MetricsCollector class exists."""
        from workflows.shared.clients.metrics import MetricsCollector
        assert MetricsCollector is not None

    def test_metrics_has_increment_counter(self):
        """MetricsCollector has increment_counter method."""
        from workflows.shared.clients.metrics import MetricsCollector
        collector = MetricsCollector()
        assert hasattr(collector, "increment_counter")
        assert callable(collector.increment_counter)

    def test_metrics_has_observe_histogram(self):
        """MetricsCollector has observe_histogram method."""
        from workflows.shared.clients.metrics import MetricsCollector
        collector = MetricsCollector()
        assert hasattr(collector, "observe_histogram")
        assert callable(collector.observe_histogram)

    def test_metrics_counter_increments(self):
        """Counter increments correctly."""
        from workflows.shared.clients.metrics import MetricsCollector
        
        collector = MetricsCollector()
        collector.increment_counter("orchestrator_requests_total")
        collector.increment_counter("orchestrator_requests_total")
        
        value = collector.get_counter_value("orchestrator_requests_total")
        assert value == 2

    def test_metrics_histogram_observes(self):
        """Histogram observes values correctly."""
        from workflows.shared.clients.metrics import MetricsCollector
        
        collector = MetricsCollector()
        collector.observe_histogram("orchestrator_latency_seconds", 0.5)
        collector.observe_histogram("orchestrator_latency_seconds", 1.5)
        
        # Should have 2 observations
        count = collector.get_histogram_count("orchestrator_latency_seconds")
        assert count == 2

    def test_metrics_has_labels_support(self):
        """Metrics support labels for segmentation."""
        from workflows.shared.clients.metrics import MetricsCollector
        
        collector = MetricsCollector()
        collector.increment_counter(
            "orchestrator_requests_total",
            labels={"endpoint": "/api/v1/search", "status": "success"}
        )
        collector.increment_counter(
            "orchestrator_requests_total",
            labels={"endpoint": "/api/v1/search", "status": "error"}
        )
        
        success_value = collector.get_counter_value(
            "orchestrator_requests_total",
            labels={"endpoint": "/api/v1/search", "status": "success"}
        )
        assert success_value == 1


# =============================================================================
# WBS 6.2.2: Trace Spans Tests
# =============================================================================


class TestTraceSpans:
    """Tests for distributed tracing spans."""

    def test_tracer_module_exists(self):
        """Tracer module exists."""
        from workflows.shared.clients.metrics import create_span
        assert callable(create_span)

    def test_create_span_returns_context_manager(self):
        """create_span returns context manager."""
        from workflows.shared.clients.metrics import create_span
        
        with create_span("test_operation") as span:
            assert span is not None

    def test_span_captures_duration(self):
        """Span captures operation duration."""
        from workflows.shared.clients.metrics import create_span
        
        with create_span("test_operation") as span:
            time.sleep(0.1)
        
        assert hasattr(span, "duration_ms")
        assert span.duration_ms >= 100

    def test_span_captures_operation_name(self):
        """Span captures operation name."""
        from workflows.shared.clients.metrics import create_span
        
        with create_span("my_operation") as span:
            pass
        
        assert span.operation_name == "my_operation"

    def test_span_supports_attributes(self):
        """Span supports custom attributes."""
        from workflows.shared.clients.metrics import create_span
        
        with create_span("search", attributes={"query": "DDD", "domain": "ai-ml"}) as span:
            pass
        
        assert span.attributes["query"] == "DDD"
        assert span.attributes["domain"] == "ai-ml"

    def test_nested_spans_track_parent(self):
        """Nested spans track parent relationship."""
        from workflows.shared.clients.metrics import create_span
        
        with create_span("parent_op") as parent:
            with create_span("child_op", parent=parent) as child:
                pass
        
        assert child.parent_id == parent.span_id


# =============================================================================
# WBS 6.2.3: Performance Logging Tests
# =============================================================================


class TestPerformanceLogging:
    """Tests for performance logging."""

    def test_performance_logger_exists(self):
        """Performance logger exists."""
        from workflows.shared.clients.metrics import PerformanceLogger
        assert PerformanceLogger is not None

    def test_performance_logger_has_log_timing(self):
        """PerformanceLogger has log_timing method."""
        from workflows.shared.clients.metrics import PerformanceLogger
        logger = PerformanceLogger()
        assert hasattr(logger, "log_timing")
        assert callable(logger.log_timing)

    def test_log_timing_outputs_json(self, caplog):
        """log_timing outputs JSON-formatted log."""
        from workflows.shared.clients.metrics import PerformanceLogger
        
        logger = PerformanceLogger()
        
        with caplog.at_level(logging.INFO):
            logger.log_timing(
                operation="search",
                duration_ms=150.5,
                metadata={"query": "test", "cache_hit": False}
            )
        
        # Should have logged something
        assert len(caplog.records) > 0
        
        # Log should be JSON-parseable
        log_text = caplog.records[0].message
        try:
            log_data = json.loads(log_text)
            assert log_data["operation"] == "search"
            assert log_data["duration_ms"] == 150.5
        except json.JSONDecodeError:
            # If not JSON, check for structured format
            assert "search" in log_text
            assert "150.5" in log_text

    def test_log_timing_context_manager(self):
        """PerformanceLogger provides context manager for auto-timing."""
        from workflows.shared.clients.metrics import PerformanceLogger
        
        logger = PerformanceLogger()
        
        with logger.timed("my_operation") as timer:
            time.sleep(0.05)
        
        assert timer.duration_ms >= 50

    def test_performance_logger_tracks_aggregates(self):
        """PerformanceLogger tracks aggregate statistics."""
        from workflows.shared.clients.metrics import PerformanceLogger
        
        logger = PerformanceLogger()
        logger.log_timing("search", duration_ms=100)
        logger.log_timing("search", duration_ms=200)
        logger.log_timing("search", duration_ms=300)
        
        stats = logger.get_stats("search")
        assert stats["count"] == 3
        assert stats["avg_ms"] == 200
        assert stats["min_ms"] == 100
        assert stats["max_ms"] == 300


# =============================================================================
# WBS 6.2: OrchestratorClient Observability Integration
# =============================================================================


class TestOrchestratorClientObservability:
    """Tests for observability integration in OrchestratorClient."""

    @pytest.mark.asyncio
    async def test_client_accepts_metrics_collector(self):
        """OrchestratorClient accepts metrics_collector parameter."""
        from workflows.shared.clients.orchestrator_client import OrchestratorClient
        from workflows.shared.clients.metrics import MetricsCollector
        
        collector = MetricsCollector()
        async with OrchestratorClient(metrics=collector) as client:
            assert client.metrics is collector

    @pytest.mark.asyncio
    async def test_search_increments_request_counter(self):
        """search() increments request counter."""
        from workflows.shared.clients.orchestrator_client import OrchestratorClient
        from workflows.shared.clients.metrics import MetricsCollector
        
        collector = MetricsCollector()
        
        async with OrchestratorClient(metrics=collector) as client:
            mock_response = {"results": []}
            with patch.object(
                client, "_request_with_retry", new_callable=AsyncMock
            ) as mock_request:
                mock_request.return_value = mock_response
                await client.search(query="test", domain="ai-ml")
        
        count = collector.get_counter_value("orchestrator_requests_total")
        assert count >= 1

    @pytest.mark.asyncio
    async def test_search_records_latency_histogram(self):
        """search() records latency in histogram."""
        from workflows.shared.clients.orchestrator_client import OrchestratorClient
        from workflows.shared.clients.metrics import MetricsCollector
        
        collector = MetricsCollector()
        
        async with OrchestratorClient(metrics=collector) as client:
            mock_response = {"results": []}
            with patch.object(
                client, "_request_with_retry", new_callable=AsyncMock
            ) as mock_request:
                mock_request.return_value = mock_response
                await client.search(query="test", domain="ai-ml")
        
        count = collector.get_histogram_count("orchestrator_latency_seconds")
        assert count >= 1

    @pytest.mark.asyncio
    async def test_search_logs_performance(self, caplog):
        """search() logs performance timing."""
        from workflows.shared.clients.orchestrator_client import OrchestratorClient
        from workflows.shared.clients.metrics import MetricsCollector, PerformanceLogger
        
        collector = MetricsCollector()
        perf_logger = PerformanceLogger()
        
        async with OrchestratorClient(metrics=collector, perf_logger=perf_logger) as client:
            mock_response = {"results": []}
            with patch.object(
                client, "_request_with_retry", new_callable=AsyncMock
            ) as mock_request:
                mock_request.return_value = mock_response
                
                with caplog.at_level(logging.INFO):
                    await client.search(query="test", domain="ai-ml")
        
        # Should have timing stats
        stats = perf_logger.get_stats("search")
        assert stats["count"] >= 1


# =============================================================================
# WBS 6: Phase 6 Integration Test
# =============================================================================


class TestPhase6Integration:
    """Full Phase 6 integration tests."""

    @pytest.mark.asyncio
    async def test_phase6_caching_improves_performance(self):
        """Caching significantly improves repeated query performance."""
        from workflows.shared.clients.orchestrator_client import OrchestratorClient
        from workflows.shared.clients.cache import ResultCache
        
        cache = ResultCache()
        
        # Simulate first request (cache miss)
        async with OrchestratorClient(cache=cache) as client:
            mock_response = {"results": [{"id": "1", "score": 0.9}]}
            
            with patch.object(
                client, "_request_with_retry", new_callable=AsyncMock
            ) as mock_request:
                # First call - cache miss
                mock_request.return_value = mock_response
                start = time.time()
                await client.search(query="test", domain="ai-ml")
                first_duration = time.time() - start
                
                # Second call - cache hit (should NOT call HTTP)
                start = time.time()
                await client.search(query="test", domain="ai-ml")
                second_duration = time.time() - start
                
                # Only one HTTP call (first request)
                assert mock_request.call_count == 1
                
                # Cache hit should be faster (or at least not slower)
                # Note: In unit tests timing can be unreliable, 
                # so we just verify cache was used
                assert second_duration <= first_duration + 0.01

    @pytest.mark.asyncio
    async def test_phase6_metrics_track_all_requests(self):
        """Metrics track all request types."""
        from workflows.shared.clients.orchestrator_client import OrchestratorClient
        from workflows.shared.clients.cache import ResultCache
        from workflows.shared.clients.metrics import MetricsCollector
        
        cache = ResultCache()
        collector = MetricsCollector()
        
        async with OrchestratorClient(cache=cache, metrics=collector) as client:
            mock_response = {"results": []}
            
            with patch.object(
                client, "_request_with_retry", new_callable=AsyncMock
            ) as mock_request:
                mock_request.return_value = mock_response
                
                # Make several requests
                await client.search(query="q1", domain="ai-ml")
                await client.search(query="q2", domain="ai-ml")
                await client.search(query="q1", domain="ai-ml")  # Cache hit
        
        # Should track all requests (including cache hits)
        total = collector.get_counter_value("orchestrator_requests_total")
        assert total == 3
        
        # Should track cache hits separately
        cache_hits = collector.get_counter_value(
            "orchestrator_cache_hits_total"
        )
        assert cache_hits >= 1

    @pytest.mark.asyncio
    async def test_phase6_observability_complete(self):
        """Full observability stack works together."""
        from workflows.shared.clients.orchestrator_client import OrchestratorClient
        from workflows.shared.clients.cache import ResultCache
        from workflows.shared.clients.metrics import (
            MetricsCollector,
            PerformanceLogger,
        )
        
        cache = ResultCache()
        collector = MetricsCollector()
        perf_logger = PerformanceLogger()
        
        async with OrchestratorClient(
            cache=cache,
            metrics=collector,
            perf_logger=perf_logger
        ) as client:
            mock_response = {"results": [{"id": "1", "score": 0.8}]}
            
            with patch.object(
                client, "_request_with_retry", new_callable=AsyncMock
            ) as mock_request:
                mock_request.return_value = mock_response
                
                results = await client.search(query="test", domain="ai-ml")
        
        # Verify all observability components working
        assert len(results) == 1  # Results returned
        assert collector.get_counter_value("orchestrator_requests_total") >= 1
        assert collector.get_histogram_count("orchestrator_latency_seconds") >= 1
        assert perf_logger.get_stats("search")["count"] >= 1
