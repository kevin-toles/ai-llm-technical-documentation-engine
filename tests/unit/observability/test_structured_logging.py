"""
WBS 2.8.1.1: Structured Logging Configuration Tests

Tests for structured JSON logging per GUIDELINES pp. 2309-2319.

TDD RED Phase: All tests should FAIL initially.
"""

import json
import pytest
from io import StringIO


class TestObservabilityPackage:
    """Test observability package structure."""

    def test_structured_logging_module_exists(self):
        """Structured logging module should exist."""
        from observability_platform.src import structured_logging
        assert structured_logging is not None

    def test_get_logger_function_exists(self):
        """get_logger function should exist."""
        from observability_platform.src.structured_logging import get_logger
        assert callable(get_logger)

    def test_set_correlation_id_function_exists(self):
        """set_correlation_id function should exist."""
        from observability_platform.src.structured_logging import set_correlation_id
        assert callable(set_correlation_id)

    def test_clear_correlation_id_function_exists(self):
        """clear_correlation_id function should exist."""
        from observability_platform.src.structured_logging import clear_correlation_id
        assert callable(clear_correlation_id)


class TestJSONFormatter:
    """Test JSON log formatting."""

    def test_logger_outputs_valid_json(self):
        """Logger should output valid JSON."""
        from observability_platform.src.structured_logging import get_logger
        
        stream = StringIO()
        logger = get_logger("test", stream=stream)
        logger.info("test message")
        
        output = stream.getvalue().strip()
        log_entry = json.loads(output)
        assert isinstance(log_entry, dict)

    def test_log_entry_contains_event_field(self):
        """Log entry should contain 'event' field with message."""
        from observability_platform.src.structured_logging import get_logger
        
        stream = StringIO()
        logger = get_logger("test", stream=stream)
        logger.info("test message")
        
        output = stream.getvalue().strip()
        log_entry = json.loads(output)
        assert "event" in log_entry
        assert log_entry["event"] == "test message"

    def test_log_entry_contains_timestamp(self):
        """Log entry should contain timestamp."""
        from observability_platform.src.structured_logging import get_logger
        
        stream = StringIO()
        logger = get_logger("test", stream=stream)
        logger.info("test message")
        
        output = stream.getvalue().strip()
        log_entry = json.loads(output)
        assert "timestamp" in log_entry


class TestLogProcessors:
    """Test log processors add required fields."""

    def test_log_entry_contains_level(self):
        """Log entry should contain log level."""
        from observability_platform.src.structured_logging import get_logger
        
        stream = StringIO()
        logger = get_logger("test", stream=stream)
        logger.info("test message")
        
        output = stream.getvalue().strip()
        log_entry = json.loads(output)
        assert "level" in log_entry
        assert log_entry["level"].lower() == "info"

    def test_log_entry_contains_logger_name(self):
        """Log entry should contain logger name."""
        from observability_platform.src.structured_logging import get_logger
        
        stream = StringIO()
        logger = get_logger("my_module", stream=stream)
        logger.info("test message")
        
        output = stream.getvalue().strip()
        log_entry = json.loads(output)
        assert "logger" in log_entry or "logger_name" in log_entry


class TestCorrelationID:
    """Test correlation ID support."""

    def test_set_and_get_correlation_id(self):
        """Should be able to set and get correlation ID."""
        from observability_platform.src.structured_logging import (
            set_correlation_id, 
            clear_correlation_id,
            get_logger,
        )
        
        stream = StringIO()
        logger = get_logger("test", stream=stream)
        
        set_correlation_id("test-correlation-123")
        logger.info("test message")
        clear_correlation_id()
        
        output = stream.getvalue().strip()
        log_entry = json.loads(output)
        assert "correlation_id" in log_entry
        assert log_entry["correlation_id"] == "test-correlation-123"

    def test_clear_correlation_id(self):
        """Should be able to clear correlation ID."""
        from observability_platform.src.structured_logging import (
            set_correlation_id, 
            clear_correlation_id,
            get_logger,
        )
        
        stream = StringIO()
        logger = get_logger("test", stream=stream)
        
        set_correlation_id("test-correlation")
        clear_correlation_id()
        logger.info("test message")
        
        output = stream.getvalue().strip()
        log_entry = json.loads(output)
        # correlation_id should be None or not present after clearing
        assert log_entry.get("correlation_id") is None


class TestLogLevelConfiguration:
    """Test log level configuration."""

    def test_default_log_level_is_info(self):
        """Default log level should be INFO."""
        from observability_platform.src.structured_logging import get_logger
        
        stream = StringIO()
        logger = get_logger("test", stream=stream)
        logger.debug("debug message")
        
        output = stream.getvalue().strip()
        # Debug messages should not appear at INFO level
        assert output == "" or "debug message" not in output

    def test_can_set_debug_level(self):
        """Should be able to set DEBUG level."""
        from observability_platform.src.structured_logging import get_logger
        
        stream = StringIO()
        logger = get_logger("test", stream=stream, level="DEBUG")
        logger.debug("debug message")
        
        output = stream.getvalue().strip()
        log_entry = json.loads(output)
        assert log_entry["event"] == "debug message"


class TestLoggerExports:
    """Test logger method exports."""

    def test_logger_has_info_method(self):
        """Logger should have info method."""
        from observability_platform.src.structured_logging import get_logger
        
        logger = get_logger("test")
        assert hasattr(logger, "info")
        assert callable(logger.info)

    def test_logger_has_warning_method(self):
        """Logger should have warning method."""
        from observability_platform.src.structured_logging import get_logger
        
        logger = get_logger("test")
        assert hasattr(logger, "warning")
        assert callable(logger.warning)

    def test_logger_has_error_method(self):
        """Logger should have error method."""
        from observability_platform.src.structured_logging import get_logger
        
        logger = get_logger("test")
        assert hasattr(logger, "error")
        assert callable(logger.error)

    def test_logger_has_debug_method(self):
        """Logger should have debug method."""
        from observability_platform.src.structured_logging import get_logger
        
        logger = get_logger("test")
        assert hasattr(logger, "debug")
        assert callable(logger.debug)


class TestStructuredData:
    """Test structured data in log entries."""

    def test_can_log_additional_fields(self):
        """Should be able to log additional structured fields."""
        from observability_platform.src.structured_logging import get_logger
        
        stream = StringIO()
        logger = get_logger("test", stream=stream)
        logger.info("test message", user_id="123", action="login")
        
        output = stream.getvalue().strip()
        log_entry = json.loads(output)
        assert log_entry.get("user_id") == "123"
        assert log_entry.get("action") == "login"

    def test_can_log_nested_data(self):
        """Should be able to log nested data structures."""
        from observability_platform.src.structured_logging import get_logger
        
        stream = StringIO()
        logger = get_logger("test", stream=stream)
        logger.info("test message", metadata={"key": "value"})
        
        output = stream.getvalue().strip()
        log_entry = json.loads(output)
        assert "metadata" in log_entry
        assert log_entry["metadata"]["key"] == "value"
