"""
WBS 2.8.1.2: Request Logging Middleware Tests

Tests for HTTP request/response logging middleware per GUIDELINES pp. 2309-2319
and ARCHITECTURE.md Line 30: src/api/middleware/logging.py

TDD RED Phase: All tests should FAIL initially.
"""

import json
import pytest
from io import StringIO
from unittest.mock import AsyncMock, MagicMock, patch
import time


class TestRequestLoggingMiddlewareExists:
    """Test that request logging middleware module exists."""

    def test_request_logging_module_exists(self):
        """Request logging middleware module should exist."""
        from observability_platform.src import request_logging
        assert request_logging is not None

    def test_request_logging_middleware_class_exists(self):
        """RequestLoggingMiddleware class should exist."""
        from observability_platform.src.request_logging import RequestLoggingMiddleware
        assert RequestLoggingMiddleware is not None

    def test_middleware_is_callable(self):
        """Middleware should be callable for ASGI integration."""
        from observability_platform.src.request_logging import RequestLoggingMiddleware
        app = MagicMock()
        middleware = RequestLoggingMiddleware(app)
        assert callable(middleware)


class TestRequestLogging:
    """Test request logging functionality."""

    @pytest.fixture
    def mock_app(self):
        """Create a mock ASGI app."""
        async def app(scope, receive, send):
            await send({
                "type": "http.response.start",
                "status": 200,
                "headers": [(b"content-type", b"application/json")],
            })
            await send({
                "type": "http.response.body",
                "body": b'{"status": "ok"}',
            })
        return app

    @pytest.fixture
    def log_stream(self):
        """Create a string stream for capturing logs."""
        return StringIO()

    def test_logs_request_method(self, mock_app, log_stream):
        """Should log HTTP method (GET, POST, etc.)."""
        from observability_platform.src.request_logging import RequestLoggingMiddleware
        
        middleware = RequestLoggingMiddleware(mock_app, log_stream=log_stream)
        
        scope = {
            "type": "http",
            "method": "POST",
            "path": "/api/test",
            "headers": [],
        }
        
        import asyncio
        asyncio.run(middleware(scope, AsyncMock(), AsyncMock()))
        
        log_output = log_stream.getvalue()
        assert "POST" in log_output

    def test_logs_request_path(self, mock_app, log_stream):
        """Should log request path."""
        from observability_platform.src.request_logging import RequestLoggingMiddleware
        
        middleware = RequestLoggingMiddleware(mock_app, log_stream=log_stream)
        
        scope = {
            "type": "http",
            "method": "GET",
            "path": "/api/documents/123",
            "headers": [],
        }
        
        import asyncio
        asyncio.run(middleware(scope, AsyncMock(), AsyncMock()))
        
        log_output = log_stream.getvalue()
        assert "/api/documents/123" in log_output

    def test_logs_response_status_code(self, mock_app, log_stream):
        """Should log response status code."""
        from observability_platform.src.request_logging import RequestLoggingMiddleware
        
        middleware = RequestLoggingMiddleware(mock_app, log_stream=log_stream)
        
        scope = {
            "type": "http",
            "method": "GET",
            "path": "/api/test",
            "headers": [],
        }
        
        import asyncio
        asyncio.run(middleware(scope, AsyncMock(), AsyncMock()))
        
        log_output = log_stream.getvalue()
        assert "200" in log_output

    def test_logs_request_duration(self, mock_app, log_stream):
        """Should log request duration in milliseconds."""
        from observability_platform.src.request_logging import RequestLoggingMiddleware
        
        middleware = RequestLoggingMiddleware(mock_app, log_stream=log_stream)
        
        scope = {
            "type": "http",
            "method": "GET",
            "path": "/api/test",
            "headers": [],
        }
        
        import asyncio
        asyncio.run(middleware(scope, AsyncMock(), AsyncMock()))
        
        log_output = log_stream.getvalue()
        # Should contain duration_ms field
        assert "duration_ms" in log_output or "duration" in log_output


class TestCorrelationIDIntegration:
    """Test correlation ID integration with request logging."""

    @pytest.fixture
    def mock_app(self):
        """Create a mock ASGI app."""
        async def app(scope, receive, send):
            await send({
                "type": "http.response.start",
                "status": 200,
                "headers": [],
            })
            await send({
                "type": "http.response.body",
                "body": b"",
            })
        return app

    @pytest.fixture
    def log_stream(self):
        """Create a string stream for capturing logs."""
        return StringIO()

    def test_generates_correlation_id_if_not_present(self, mock_app, log_stream):
        """Should generate correlation ID if not in request headers."""
        from observability_platform.src.request_logging import RequestLoggingMiddleware
        
        middleware = RequestLoggingMiddleware(mock_app, log_stream=log_stream)
        
        scope = {
            "type": "http",
            "method": "GET",
            "path": "/api/test",
            "headers": [],
        }
        
        import asyncio
        asyncio.run(middleware(scope, AsyncMock(), AsyncMock()))
        
        log_output = log_stream.getvalue()
        assert "correlation_id" in log_output

    def test_uses_correlation_id_from_header(self, mock_app, log_stream):
        """Should use correlation ID from X-Correlation-ID header."""
        from observability_platform.src.request_logging import RequestLoggingMiddleware
        
        middleware = RequestLoggingMiddleware(mock_app, log_stream=log_stream)
        
        scope = {
            "type": "http",
            "method": "GET",
            "path": "/api/test",
            "headers": [(b"x-correlation-id", b"test-correlation-123")],
        }
        
        import asyncio
        asyncio.run(middleware(scope, AsyncMock(), AsyncMock()))
        
        log_output = log_stream.getvalue()
        assert "test-correlation-123" in log_output


class TestErrorLogging:
    """Test error logging scenarios."""

    @pytest.fixture
    def log_stream(self):
        """Create a string stream for capturing logs."""
        return StringIO()

    def test_logs_error_response_status(self, log_stream):
        """Should log error status codes (4xx, 5xx)."""
        async def error_app(scope, receive, send):
            await send({
                "type": "http.response.start",
                "status": 500,
                "headers": [],
            })
            await send({
                "type": "http.response.body",
                "body": b'{"error": "Internal Server Error"}',
            })
        
        from observability_platform.src.request_logging import RequestLoggingMiddleware
        
        middleware = RequestLoggingMiddleware(error_app, log_stream=log_stream)
        
        scope = {
            "type": "http",
            "method": "GET",
            "path": "/api/test",
            "headers": [],
        }
        
        import asyncio
        asyncio.run(middleware(scope, AsyncMock(), AsyncMock()))
        
        log_output = log_stream.getvalue()
        assert "500" in log_output

    def test_logs_exception_on_app_error(self, log_stream):
        """Should log exception details when app raises error."""
        async def failing_app(scope, receive, send):
            raise ValueError("Test error")
        
        from observability_platform.src.request_logging import RequestLoggingMiddleware
        
        middleware = RequestLoggingMiddleware(failing_app, log_stream=log_stream)
        
        scope = {
            "type": "http",
            "method": "GET",
            "path": "/api/test",
            "headers": [],
        }
        
        import asyncio
        with pytest.raises(ValueError):
            asyncio.run(middleware(scope, AsyncMock(), AsyncMock()))
        
        log_output = log_stream.getvalue()
        assert "error" in log_output.lower() or "exception" in log_output.lower()


class TestHealthCheckExclusion:
    """Test that health check endpoints can be excluded from logging."""

    @pytest.fixture
    def mock_app(self):
        """Create a mock ASGI app."""
        async def app(scope, receive, send):
            await send({
                "type": "http.response.start",
                "status": 200,
                "headers": [],
            })
            await send({
                "type": "http.response.body",
                "body": b"",
            })
        return app

    @pytest.fixture
    def log_stream(self):
        """Create a string stream for capturing logs."""
        return StringIO()

    def test_can_exclude_health_check_paths(self, mock_app, log_stream):
        """Should be able to exclude health check paths from logging."""
        from observability_platform.src.request_logging import RequestLoggingMiddleware
        
        middleware = RequestLoggingMiddleware(
            mock_app, 
            log_stream=log_stream,
            exclude_paths=["/health", "/ready"]
        )
        
        scope = {
            "type": "http",
            "method": "GET",
            "path": "/health",
            "headers": [],
        }
        
        import asyncio
        asyncio.run(middleware(scope, AsyncMock(), AsyncMock()))
        
        log_output = log_stream.getvalue()
        # Health check should not be logged
        assert "/health" not in log_output or log_output.strip() == ""

    def test_logs_non_excluded_paths(self, mock_app, log_stream):
        """Should log non-excluded paths normally."""
        from observability_platform.src.request_logging import RequestLoggingMiddleware
        
        middleware = RequestLoggingMiddleware(
            mock_app, 
            log_stream=log_stream,
            exclude_paths=["/health"]
        )
        
        scope = {
            "type": "http",
            "method": "GET",
            "path": "/api/data",
            "headers": [],
        }
        
        import asyncio
        asyncio.run(middleware(scope, AsyncMock(), AsyncMock()))
        
        log_output = log_stream.getvalue()
        assert "/api/data" in log_output


class TestJSONLogFormat:
    """Test JSON log output format."""

    @pytest.fixture
    def mock_app(self):
        """Create a mock ASGI app."""
        async def app(scope, receive, send):
            await send({
                "type": "http.response.start",
                "status": 200,
                "headers": [],
            })
            await send({
                "type": "http.response.body",
                "body": b"",
            })
        return app

    @pytest.fixture
    def log_stream(self):
        """Create a string stream for capturing logs."""
        return StringIO()

    def test_log_output_is_valid_json(self, mock_app, log_stream):
        """Log output should be valid JSON."""
        from observability_platform.src.request_logging import RequestLoggingMiddleware
        
        middleware = RequestLoggingMiddleware(mock_app, log_stream=log_stream)
        
        scope = {
            "type": "http",
            "method": "GET",
            "path": "/api/test",
            "headers": [],
        }
        
        import asyncio
        asyncio.run(middleware(scope, AsyncMock(), AsyncMock()))
        
        log_output = log_stream.getvalue().strip()
        # Should parse as valid JSON
        log_data = json.loads(log_output)
        assert isinstance(log_data, dict)

    def test_log_contains_required_fields(self, mock_app, log_stream):
        """Log should contain required fields: method, path, status, duration."""
        from observability_platform.src.request_logging import RequestLoggingMiddleware
        
        middleware = RequestLoggingMiddleware(mock_app, log_stream=log_stream)
        
        scope = {
            "type": "http",
            "method": "GET",
            "path": "/api/test",
            "headers": [],
        }
        
        import asyncio
        asyncio.run(middleware(scope, AsyncMock(), AsyncMock()))
        
        log_output = log_stream.getvalue().strip()
        log_data = json.loads(log_output)
        
        assert "method" in log_data
        assert "path" in log_data
        assert "status" in log_data or "status_code" in log_data


class TestNonHTTPRequests:
    """Test handling of non-HTTP requests (WebSocket, etc.)."""

    @pytest.fixture
    def mock_app(self):
        """Create a mock ASGI app."""
        async def app(scope, receive, send):
            # No-op mock - intentionally empty to simulate minimal ASGI app
            pass
        return app

    @pytest.fixture
    def log_stream(self):
        """Create a string stream for capturing logs."""
        return StringIO()

    def test_passes_through_websocket_requests(self, mock_app, log_stream):
        """Should pass through WebSocket requests without logging."""
        from observability_platform.src.request_logging import RequestLoggingMiddleware
        
        middleware = RequestLoggingMiddleware(mock_app, log_stream=log_stream)
        
        scope = {
            "type": "websocket",
            "path": "/ws",
        }
        
        import asyncio
        asyncio.run(middleware(scope, AsyncMock(), AsyncMock()))
        
        log_output = log_stream.getvalue()
        # WebSocket should not be logged as HTTP request
        assert log_output.strip() == "" or "websocket" not in log_output.lower()

    def test_passes_through_lifespan_events(self, mock_app, log_stream):
        """Should pass through lifespan events without logging."""
        from observability_platform.src.request_logging import RequestLoggingMiddleware
        
        middleware = RequestLoggingMiddleware(mock_app, log_stream=log_stream)
        
        scope = {
            "type": "lifespan",
        }
        
        import asyncio
        asyncio.run(middleware(scope, AsyncMock(), AsyncMock()))
        
        log_output = log_stream.getvalue()
        # Lifespan events should not be logged
        assert log_output.strip() == ""
