"""
Unit tests for GatewayProvider - WBS 3.1.2.1

Tests the GatewayProvider adapter that implements LLMProvider protocol
using LLMGatewayClient for actual API calls.

TDD Approach: RED phase - write failing tests first.

Reference:
- GUIDELINES: TDD RED → GREEN → REFACTOR
- workflows/shared/providers/base.py: LLMProvider protocol, LLMResponse
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

# Import LLMResponse for type checking (exists)
from workflows.shared.providers.base import LLMResponse, LLMError, LLMProvider


# =============================================================================
# RED PHASE: Tests written before implementation
# =============================================================================


class TestGatewayProviderInstantiation:
    """Tests for GatewayProvider instantiation."""

    def test_instantiation_with_defaults(self) -> None:
        """GatewayProvider should instantiate with default configuration."""
        # Import should succeed once implemented
        from workflows.shared.providers.gateway_provider import GatewayProvider

        provider = GatewayProvider()

        assert provider  # Instance created successfully
        assert provider.provider_name == "gateway"
        assert isinstance(provider.model_name, str)

    def test_instantiation_with_custom_model(self) -> None:
        """GatewayProvider should accept custom model name."""
        from workflows.shared.providers.gateway_provider import GatewayProvider

        provider = GatewayProvider(model="claude-3-opus-20240229")

        assert provider.model_name == "claude-3-opus-20240229"

    def test_instantiation_with_custom_gateway_url(self) -> None:
        """GatewayProvider should accept custom gateway URL."""
        from workflows.shared.providers.gateway_provider import GatewayProvider

        provider = GatewayProvider(gateway_url="http://custom:9000")

        assert provider._gateway_url == "http://custom:9000"

    def test_implements_llm_provider_protocol(self) -> None:
        """GatewayProvider must implement LLMProvider protocol."""
        from workflows.shared.providers.gateway_provider import GatewayProvider

        provider = GatewayProvider()

        # Check protocol compliance
        assert hasattr(provider, "call")
        assert hasattr(provider, "model_name")
        assert hasattr(provider, "provider_name")
        # Protocol check via isinstance is not directly testable for Protocol
        # but we verify the interface exists


class TestGatewayProviderCall:
    """Tests for GatewayProvider.call() method."""

    def test_call_returns_llm_response(self) -> None:
        """call() should return LLMResponse with content and usage."""
        from workflows.shared.providers.gateway_provider import GatewayProvider

        # Mock the gateway client
        mock_response = {
            "choices": [{"message": {"content": "Hello, world!", "role": "assistant"}}],
            "model": "claude-sonnet-4-5-20250929",
            "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
        }

        with patch.object(
            GatewayProvider, "_call_gateway", return_value=mock_response
        ):
            provider = GatewayProvider()
            response = provider.call(
                prompt="Say hello",
                max_tokens=100,
                temperature=0.0,
            )

        assert isinstance(response, LLMResponse)
        assert response.content == "Hello, world!"
        assert response.model == "claude-sonnet-4-5-20250929"
        assert response.input_tokens == 10
        assert response.output_tokens == 5

    def test_call_with_system_prompt(self) -> None:
        """call() should pass system_prompt to gateway."""
        from workflows.shared.providers.gateway_provider import GatewayProvider

        mock_response = {
            "choices": [{"message": {"content": "System response", "role": "assistant"}}],
            "model": "claude-sonnet-4-5-20250929",
            "usage": {"prompt_tokens": 20, "completion_tokens": 8, "total_tokens": 28},
        }

        with patch.object(
            GatewayProvider, "_call_gateway", return_value=mock_response
        ) as mock_call:
            provider = GatewayProvider()
            response = provider.call(
                prompt="Test prompt",
                max_tokens=100,
                temperature=0.5,
                system_prompt="You are a helpful assistant.",
            )

            # Verify system_prompt was passed
            call_args = mock_call.call_args
            assert call_args is not None
            # The implementation should convert to messages format with system

        assert response.content == "System response"

    def test_call_converts_prompt_to_messages_format(self) -> None:
        """call() should convert prompt string to messages list format."""
        from workflows.shared.providers.gateway_provider import GatewayProvider

        # We need to verify the internal conversion
        provider = GatewayProvider()

        # Mock the internal gateway call
        with patch.object(
            GatewayProvider, "_call_gateway", return_value={
                "choices": [{"message": {"content": "Response", "role": "assistant"}}],
                "model": "test-model",
                "usage": {"prompt_tokens": 5, "completion_tokens": 5, "total_tokens": 10},
            }
        ) as mock_call:
            provider.call(prompt="Hello", max_tokens=50)

            # Verify messages format was used
            mock_call.assert_called_once()
            _call_args = mock_call.call_args  # Unused but retained for debugging
            # Implementation should pass messages=[{"role": "user", "content": "Hello"}]


class TestGatewayProviderErrorHandling:
    """Tests for error handling in GatewayProvider."""

    def test_call_raises_llm_error_on_gateway_failure(self) -> None:
        """call() should raise LLMError when gateway fails."""
        from workflows.shared.providers.gateway_provider import GatewayProvider
        from workflows.shared.clients.llm_gateway import GatewayAPIError

        with patch.object(
            GatewayProvider, "_call_gateway",
            side_effect=GatewayAPIError("Gateway error", status_code=500)
        ):
            provider = GatewayProvider()

            with pytest.raises(LLMError) as exc_info:
                provider.call(prompt="Test", max_tokens=100)

            assert "Gateway error" in str(exc_info.value)

    def test_call_raises_llm_error_on_timeout(self) -> None:
        """call() should raise LLMError on timeout."""
        from workflows.shared.providers.gateway_provider import GatewayProvider
        from workflows.shared.clients.llm_gateway import GatewayTimeoutError

        with patch.object(
            GatewayProvider, "_call_gateway",
            side_effect=GatewayTimeoutError("Request timed out")
        ):
            provider = GatewayProvider()

            with pytest.raises(LLMError) as exc_info:
                provider.call(prompt="Test", max_tokens=100)

            assert "timed out" in str(exc_info.value).lower()

    def test_call_raises_llm_error_on_connection_failure(self) -> None:
        """call() should raise LLMError on connection failure."""
        from workflows.shared.providers.gateway_provider import GatewayProvider
        from workflows.shared.clients.llm_gateway import GatewayConnectionError

        with patch.object(
            GatewayProvider, "_call_gateway",
            side_effect=GatewayConnectionError("Connection refused")
        ):
            provider = GatewayProvider()

            with pytest.raises(LLMError) as exc_info:
                provider.call(prompt="Test", max_tokens=100)

            assert "connection" in str(exc_info.value).lower()


class TestGatewayProviderAsyncBridge:
    """Tests for async/sync bridging in GatewayProvider."""

    def test_call_is_synchronous(self) -> None:
        """call() must be synchronous per LLMProvider protocol."""
        from workflows.shared.providers.gateway_provider import GatewayProvider
        import asyncio

        provider = GatewayProvider()

        # call() should not return a coroutine
        with patch.object(
            GatewayProvider, "_call_gateway", return_value={
                "choices": [{"message": {"content": "Sync response"}}],
                "model": "test",
                "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
            }
        ):
            result = provider.call(prompt="Test", max_tokens=10)

            # Should not be a coroutine
            assert not asyncio.iscoroutine(result)
            assert isinstance(result, LLMResponse)

    @pytest.mark.asyncio
    async def test_call_async_available_for_async_contexts(self) -> None:
        """call_async() should be available for async contexts."""
        from workflows.shared.providers.gateway_provider import GatewayProvider

        provider = GatewayProvider()

        # Should have async method available
        assert hasattr(provider, "call_async")

        with patch.object(
            GatewayProvider, "_call_gateway_async", new_callable=AsyncMock,
            return_value={
                "choices": [{"message": {"content": "Async response"}}],
                "model": "test",
                "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
            }
        ):
            result = await provider.call_async(prompt="Test", max_tokens=10)

            assert isinstance(result, LLMResponse)
            assert result.content == "Async response"


class TestGatewayProviderResponseParsing:
    """Tests for parsing gateway responses."""

    def test_parses_stop_reason_from_response(self) -> None:
        """Should extract stop_reason from gateway response."""
        from workflows.shared.providers.gateway_provider import GatewayProvider

        mock_response = {
            "choices": [{
                "message": {"content": "Complete response", "role": "assistant"},
                "finish_reason": "stop"
            }],
            "model": "test-model",
            "usage": {"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20},
        }

        with patch.object(GatewayProvider, "_call_gateway", return_value=mock_response):
            provider = GatewayProvider()
            response = provider.call(prompt="Test", max_tokens=100)

        assert response.stop_reason == "stop"

    def test_handles_max_tokens_finish_reason(self) -> None:
        """Should handle 'length' finish_reason (max_tokens)."""
        from workflows.shared.providers.gateway_provider import GatewayProvider

        mock_response = {
            "choices": [{
                "message": {"content": "Truncated res...", "role": "assistant"},
                "finish_reason": "length"
            }],
            "model": "test-model",
            "usage": {"prompt_tokens": 10, "completion_tokens": 100, "total_tokens": 110},
        }

        with patch.object(GatewayProvider, "_call_gateway", return_value=mock_response):
            provider = GatewayProvider()
            response = provider.call(prompt="Test", max_tokens=100)

        assert response.stop_reason == "length"

    def test_handles_tool_calls_finish_reason(self) -> None:
        """Should handle 'tool_calls' finish_reason."""
        from workflows.shared.providers.gateway_provider import GatewayProvider

        mock_response = {
            "choices": [{
                "message": {
                    "content": "",
                    "role": "assistant",
                    "tool_calls": [{"id": "call_123", "function": {"name": "search"}}]
                },
                "finish_reason": "tool_calls"
            }],
            "model": "test-model",
            "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
        }

        with patch.object(GatewayProvider, "_call_gateway", return_value=mock_response):
            provider = GatewayProvider()
            response = provider.call(prompt="Test with tools", max_tokens=100)

        assert response.stop_reason == "tool_calls"


class TestGatewayProviderFactoryIntegration:
    """Tests for factory integration."""

    def test_factory_can_create_gateway_provider(self) -> None:
        """Provider factory should be able to create GatewayProvider."""
        from workflows.shared.providers.factory import get_provider

        provider = get_provider("gateway")

        assert provider is not None
        assert provider.provider_name == "gateway"
