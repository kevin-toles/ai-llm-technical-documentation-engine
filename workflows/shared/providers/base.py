"""
Base protocol and data structures for LLM providers.
"""

from dataclasses import dataclass
from typing import Protocol, Optional


@dataclass
class LLMResponse:
    """Standardized response from any LLM provider."""
    content: str
    model: str
    input_tokens: int
    output_tokens: int
    stop_reason: Optional[str] = None
    
    @property
    def total_tokens(self) -> int:
        """Total tokens used in this request."""
        return self.input_tokens + self.output_tokens


class LLMError(Exception):
    """Base exception for LLM provider errors."""
    pass


class LLMProvider(Protocol):
    """Protocol defining the interface all LLM providers must implement."""
    
    def call(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float = 0.0,
        system_prompt: Optional[str] = None,
    ) -> LLMResponse:
        """
        Make a synchronous call to the LLM provider.
        
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
        ...
    
    @property
    def model_name(self) -> str:
        """The model identifier being used."""
        ...
    
    @property
    def provider_name(self) -> str:
        """The provider name (e.g., 'anthropic', 'openai')."""
        ...
