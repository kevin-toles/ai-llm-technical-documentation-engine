"""
Metrics Module - WBS 6.2 Observability

Prometheus-style metrics collection and performance logging.

Reference Documents:
- WBS_IMPLEMENTATION.md: Phase 6.2 - Observability
- GUIDELINES p. 2309: Prometheus metrics patterns
- GUIDELINES p. 2145: Structured logging, tracing

WBS Items:
- 6.2.1: Prometheus metrics - counters and histograms
- 6.2.2: Trace spans - distributed tracing support
- 6.2.3: Performance logs - structured timing logs

Usage:
    collector = MetricsCollector()
    collector.increment_counter("requests_total", labels={"endpoint": "/search"})
    collector.observe_histogram("latency_seconds", 0.5)

    with create_span("operation") as span:
        # do work
        pass

    logger = PerformanceLogger()
    logger.log_timing("search", duration_ms=150)
"""

import json
import logging
import threading
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Dict, Generator, List, Optional


# =============================================================================
# Logging Setup
# =============================================================================

logger = logging.getLogger(__name__)


# =============================================================================
# WBS 6.2.1: Prometheus-style Metrics
# =============================================================================


@dataclass
class CounterValue:
    """Counter metric value with labels."""
    value: float = 0.0


@dataclass
class HistogramValue:
    """Histogram metric value tracking observations."""
    observations: List[float] = field(default_factory=list)

    @property
    def count(self) -> int:
        return len(self.observations)

    @property
    def sum(self) -> float:
        return sum(self.observations)


class MetricsCollector:
    """
    Prometheus-style metrics collector.

    Reference: WBS 6.2.1 - Prometheus metrics

    Collects counters and histograms for observability.
    Thread-safe for concurrent access.

    Example:
        collector = MetricsCollector()
        collector.increment_counter("requests_total")
        collector.observe_histogram("latency_seconds", 0.5)
    """

    def __init__(self) -> None:
        """Initialize metrics collector."""
        self._counters: Dict[str, float] = {}
        self._histograms: Dict[str, List[float]] = {}
        self._lock = threading.RLock()

    def _make_key(self, name: str, labels: Optional[Dict[str, str]] = None) -> str:
        """Generate unique key for metric with labels."""
        if not labels:
            return name
        label_str = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
        return f"{name}{{{label_str}}}"

    def increment_counter(
        self,
        name: str,
        value: float = 1.0,
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        Increment a counter metric.

        Args:
            name: Metric name
            value: Amount to increment (default 1.0)
            labels: Optional label key-value pairs
        """
        key = self._make_key(name, labels)
        with self._lock:
            self._counters[key] = self._counters.get(key, 0.0) + value

    def get_counter_value(
        self,
        name: str,
        labels: Optional[Dict[str, str]] = None,
    ) -> float:
        """
        Get current counter value.

        Args:
            name: Metric name
            labels: Optional label key-value pairs

        Returns:
            Current counter value (0.0 if not set)
        """
        key = self._make_key(name, labels)
        with self._lock:
            return self._counters.get(key, 0.0)

    def observe_histogram(
        self,
        name: str,
        value: float,
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        Record observation in histogram.

        Args:
            name: Metric name
            value: Observed value
            labels: Optional label key-value pairs
        """
        key = self._make_key(name, labels)
        with self._lock:
            if key not in self._histograms:
                self._histograms[key] = []
            self._histograms[key].append(value)

    def get_histogram_count(
        self,
        name: str,
        labels: Optional[Dict[str, str]] = None,
    ) -> int:
        """
        Get histogram observation count.

        Args:
            name: Metric name
            labels: Optional label key-value pairs

        Returns:
            Number of observations
        """
        key = self._make_key(name, labels)
        with self._lock:
            return len(self._histograms.get(key, []))

    def get_histogram_sum(
        self,
        name: str,
        labels: Optional[Dict[str, str]] = None,
    ) -> float:
        """
        Get histogram observation sum.

        Args:
            name: Metric name
            labels: Optional label key-value pairs

        Returns:
            Sum of all observations
        """
        key = self._make_key(name, labels)
        with self._lock:
            return sum(self._histograms.get(key, []))

    def reset(self) -> None:
        """Reset all metrics."""
        with self._lock:
            self._counters.clear()
            self._histograms.clear()


# =============================================================================
# WBS 6.2.2: Trace Spans
# =============================================================================


@dataclass
class Span:
    """
    Trace span for distributed tracing.

    Reference: WBS 6.2.2 - Trace spans

    Attributes:
        span_id: Unique span identifier
        operation_name: Name of the operation
        start_time: Start timestamp
        end_time: End timestamp (set on exit)
        duration_ms: Duration in milliseconds
        attributes: Custom span attributes
        parent_id: Parent span ID (if nested)
    """

    span_id: str
    operation_name: str
    start_time: float
    end_time: Optional[float] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    parent_id: Optional[str] = None

    @property
    def duration_ms(self) -> float:
        """Get span duration in milliseconds."""
        if self.end_time is None:
            return (time.time() - self.start_time) * 1000
        return (self.end_time - self.start_time) * 1000


@contextmanager
def create_span(
    operation_name: str,
    attributes: Optional[Dict[str, Any]] = None,
    parent: Optional[Span] = None,
) -> Generator[Span, None, None]:
    """
    Create a trace span as context manager.

    Reference: WBS 6.2.2 - Trace spans

    Args:
        operation_name: Name of the operation being traced
        attributes: Optional custom attributes
        parent: Optional parent span for nesting

    Yields:
        Span object with timing information

    Example:
        with create_span("search", attributes={"query": "DDD"}) as span:
            # do work
            pass
        print(f"Duration: {span.duration_ms}ms")
    """
    span = Span(
        span_id=str(uuid.uuid4())[:8],
        operation_name=operation_name,
        start_time=time.time(),
        attributes=attributes or {},
        parent_id=parent.span_id if parent else None,
    )

    try:
        yield span
    finally:
        span.end_time = time.time()


# =============================================================================
# WBS 6.2.3: Performance Logging
# =============================================================================


@dataclass
class TimerContext:
    """Context for timed operations."""
    operation: str
    start_time: float
    duration_ms: float = 0.0

    def stop(self) -> float:
        """Stop timer and return duration."""
        self.duration_ms = (time.time() - self.start_time) * 1000
        return self.duration_ms


class PerformanceLogger:
    """
    Performance logger with aggregate statistics.

    Reference: WBS 6.2.3 - Performance logs

    Logs timing information and tracks aggregate stats.

    Example:
        logger = PerformanceLogger()
        logger.log_timing("search", duration_ms=150)
        stats = logger.get_stats("search")
    """

    def __init__(self) -> None:
        """Initialize performance logger."""
        self._timings: Dict[str, List[float]] = {}
        self._lock = threading.RLock()
        self._logger = logging.getLogger(f"{__name__}.performance")

    def log_timing(
        self,
        operation: str,
        duration_ms: float,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log timing for an operation.

        Args:
            operation: Operation name
            duration_ms: Duration in milliseconds
            metadata: Optional additional context
        """
        # Store for aggregates
        with self._lock:
            if operation not in self._timings:
                self._timings[operation] = []
            self._timings[operation].append(duration_ms)

        # Log as JSON
        log_entry = {
            "operation": operation,
            "duration_ms": duration_ms,
            "timestamp": time.time(),
        }
        if metadata:
            log_entry.update(metadata)

        self._logger.info(json.dumps(log_entry))

    @contextmanager
    def timed(
        self,
        operation: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Generator[TimerContext, None, None]:
        """
        Context manager for auto-timing operations.

        Args:
            operation: Operation name
            metadata: Optional additional context

        Yields:
            TimerContext with duration_ms after exit

        Example:
            with logger.timed("search") as timer:
                # do work
                pass
            print(f"Took {timer.duration_ms}ms")
        """
        timer = TimerContext(operation=operation, start_time=time.time())
        try:
            yield timer
        finally:
            timer.stop()
            self.log_timing(operation, timer.duration_ms, metadata)

    def get_stats(self, operation: str) -> Dict[str, Any]:
        """
        Get aggregate statistics for an operation.

        Args:
            operation: Operation name

        Returns:
            Dict with count, avg_ms, min_ms, max_ms
        """
        with self._lock:
            timings = self._timings.get(operation, [])

        if not timings:
            return {"count": 0, "avg_ms": 0, "min_ms": 0, "max_ms": 0}

        return {
            "count": len(timings),
            "avg_ms": sum(timings) / len(timings),
            "min_ms": min(timings),
            "max_ms": max(timings),
        }

    def reset(self) -> None:
        """Reset all timing statistics."""
        with self._lock:
            self._timings.clear()
