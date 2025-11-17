"""
Anthropic Claude LLM provider implementation.
"""

import os
from typing import Optional

try:
    import anthropic
except ImportError:
    anthropic = None

from .base import LLMResponse, LLMError


class AnthropicProvider:
    """
    Anthropic Claude provider implementation.
    
    Uses the official Anthropic Python SDK to interact with Claude models.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-3-5-sonnet-20241022",
    ):
        """
        Initialize the Anthropic provider.
        
        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            model: Claude model to use
        """
        if anthropic is None:
            raise LLMError(
                "anthropic package not installed. "
                "Install with: pip install anthropic"
            )
        
        self._api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self._api_key:
            raise LLMError(
                "Anthropic API key not provided. "
                "Set ANTHROPIC_API_KEY environment variable or pass api_key parameter."
            )
        
        self._model = model
        self._client = anthropic.Anthropic(api_key=self._api_key)
    
    def call(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float = 0.0,
        system_prompt: Optional[str] = None,
    ) -> LLMResponse:
        """
        Make a synchronous call to Claude.
        
        Args:
            prompt: The user prompt/message
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0 = deterministic)
            system_prompt: Optional system prompt to set context
            
        Returns:
            LLMResponse with content and usage statistics
            
        Raises:
            LLMError: If the API call fails
        """
        try:
            # Build message parameters
            message_params = {
                "model": self._model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [{"role": "user", "content": prompt}],
            }
            
            # Add system prompt if provided
            if system_prompt:
                message_params["system"] = system_prompt
            
            # Make the API call
            response = self._client.messages.create(**message_params)
            
            # Extract content (handle both text and content blocks)
            if hasattr(response.content[0], 'text'):
                content = response.content[0].text
            else:
                content = str(response.content[0])
            
            # Build standardized response
            return LLMResponse(
                content=content,
                model=response.model,
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens,
                stop_reason=response.stop_reason,
            )
            
        except anthropic.APIError as e:
            raise LLMError(f"Anthropic API error: {e}") from e
        except Exception as e:
            raise LLMError(f"Unexpected error calling Anthropic: {e}") from e
    
    @property
    def model_name(self) -> str:
        """The Claude model being used."""
        return self._model
    
    @property
    def provider_name(self) -> str:
        """Returns 'anthropic'."""
        return "anthropic"
