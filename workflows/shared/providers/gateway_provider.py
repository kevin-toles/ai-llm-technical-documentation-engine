"""
Gateway Provider - WBS 3.1.2.1 Replace Direct LLM Calls

Adapter that implements LLMProvider protocol using LLMGatewayClient.
Provides synchronous interface to async gateway client.

Reference Documents:
- GUIDELINES: TDD RED → GREEN → REFACTOR
- workflows/shared/providers/base.py: LLMProvider protocol, LLMResponse
- workflows/shared/clients/llm_gateway.py: LLMGatewayClient async client

Pattern: Adapter Pattern
- Adapts async LLMGatewayClient to sync LLMProvider protocol
- Bridges message formats: prompt → messages list
- Converts gateway dict response → LLMResponse dataclass
"""

import asyncio
import os
from typing import Optional, Any

from .base import LLMResponse, LLMError
from ..clients.llm_gateway import (
    LLMGatewayClient,
    GatewayError,
    GatewayTimeoutError,
    GatewayConnectionError,
    GatewayAPIError,
)


class GatewayProvider:
    """
    LLM Gateway provider implementing LLMProvider protocol.

    Adapter Pattern: Bridges async LLMGatewayClient to synchronous LLMProvider interface.
    This allows existing code using AnthropicProvider to switch to gateway seamlessly.

    Example:
        provider = GatewayProvider()
        response = provider.call(
            prompt="Hello world",
            max_tokens=100,
            temperature=0.0
        )
        print(response.content)

    Reference:
    - workflows/shared/providers/base.py: LLMProvider protocol
    - GUIDELINES p. 2313: Connection pooling for downstream services
    """

    # Default model - can be overridden
    DEFAULT_MODEL = "claude-sonnet-4-5-20250929"

    def __init__(
        self,
        model: Optional[str] = None,
        gateway_url: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> None:
        """
        Initialize GatewayProvider.

        Args:
            model: Model identifier. Defaults to DEFAULT_MODEL.
            gateway_url: Gateway base URL. Defaults to LLM_GATEWAY_URL env or localhost.
            timeout: Request timeout in seconds.

        Pattern: Environment variable configuration with sensible defaults
        """
        self._model: str = model or os.getenv("LLM_MODEL") or self.DEFAULT_MODEL
        self._gateway_url: str = gateway_url or os.getenv("LLM_GATEWAY_URL") or "http://localhost:8080"
        self._timeout = timeout

    def call(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float = 0.0,
        system_prompt: Optional[str] = None,
    ) -> LLMResponse:
        """
        Make a synchronous call to the LLM via gateway.

        Implements LLMProvider protocol interface.
        Internally uses async gateway client with asyncio.run().

        Args:
            prompt: The user prompt/message
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0 = deterministic)
            system_prompt: Optional system prompt to set context

        Returns:
            LLMResponse with content and usage statistics

        Raises:
            LLMError: If the gateway call fails
        """
        try:
            response_dict = self._call_gateway(
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                system_prompt=system_prompt,
            )
            return self._parse_response(response_dict)
        except GatewayTimeoutError as e:
            raise LLMError(f"Gateway request timed out: {e}") from e
        except GatewayConnectionError as e:
            raise LLMError(f"Gateway connection failed: {e}") from e
        except GatewayAPIError as e:
            raise LLMError(f"Gateway error: {e}") from e
        except GatewayError as e:
            raise LLMError(f"Gateway error: {e}") from e

    async def call_async(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float = 0.0,
        system_prompt: Optional[str] = None,
    ) -> LLMResponse:
        """
        Async version of call() for use in async contexts.

        Args:
            prompt: The user prompt/message
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            system_prompt: Optional system prompt

        Returns:
            LLMResponse with content and usage statistics

        Raises:
            LLMError: If the gateway call fails
        """
        try:
            response_dict = await self._call_gateway_async(
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                system_prompt=system_prompt,
            )
            return self._parse_response(response_dict)
        except GatewayTimeoutError as e:
            raise LLMError(f"Gateway request timed out: {e}") from e
        except GatewayConnectionError as e:
            raise LLMError(f"Gateway connection failed: {e}") from e
        except GatewayAPIError as e:
            raise LLMError(f"Gateway error: {e}") from e
        except GatewayError as e:
            raise LLMError(f"Gateway error: {e}") from e

    def _call_gateway(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float,
        system_prompt: Optional[str],
    ) -> dict[str, Any]:
        """
        Internal: Make synchronous gateway call using asyncio.run().

        Pattern: Async-to-sync bridge for protocol compliance.

        Args:
            prompt: User prompt
            max_tokens: Max response tokens
            temperature: Sampling temperature
            system_prompt: Optional system prompt

        Returns:
            Raw gateway response dict
        """
        return asyncio.run(
            self._call_gateway_async(prompt, max_tokens, temperature, system_prompt)
        )

    async def _call_gateway_async(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float,
        system_prompt: Optional[str],
    ) -> dict[str, Any]:
        """
        Internal: Make async gateway call.

        Converts prompt to OpenAI-compatible messages format.

        Args:
            prompt: User prompt
            max_tokens: Max response tokens
            temperature: Sampling temperature
            system_prompt: Optional system prompt

        Returns:
            Raw gateway response dict
        """
        # Convert to messages format
        messages: list[dict[str, Any]] = []

        # Add system message if provided
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        # Add user message
        messages.append({"role": "user", "content": prompt})

        # Make gateway call
        client_kwargs: dict[str, Any] = {"base_url": self._gateway_url}
        if self._timeout is not None:
            client_kwargs["timeout"] = self._timeout

        async with LLMGatewayClient(**client_kwargs) as client:
            return await client.chat_completion(
                model=self._model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

    def _parse_response(self, response: dict[str, Any]) -> LLMResponse:
        """
        Parse gateway response dict into LLMResponse.

        Handles OpenAI-compatible response format from llm-gateway.

        Args:
            response: Gateway response dict

        Returns:
            LLMResponse dataclass

        Reference: llm-gateway/src/models/responses.py
        """
        # Extract content from choices
        choices = response.get("choices", [])
        if not choices:
            raise LLMError("No choices in gateway response")

        message = choices[0].get("message", {})
        content = message.get("content", "")

        # Extract finish reason
        finish_reason = choices[0].get("finish_reason")

        # Extract usage
        usage = response.get("usage", {})
        input_tokens = usage.get("prompt_tokens", 0)
        output_tokens = usage.get("completion_tokens", 0)

        # Get model from response (fallback to configured model)
        model: str = response.get("model") or self._model

        return LLMResponse(
            content=content,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            stop_reason=finish_reason,
        )

    @property
    def model_name(self) -> str:
        """The model identifier being used."""
        return self._model

    @property
    def provider_name(self) -> str:
        """Returns 'gateway'."""
        return "gateway"
