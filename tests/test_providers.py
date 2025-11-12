"""
Tests for LLM provider abstraction.
"""

import os
import pytest
from unittest.mock import Mock, patch, MagicMock

from src.providers import LLMProvider, LLMResponse, LLMError, AnthropicProvider


class TestLLMResponse:
    """Tests for LLMResponse data class."""
    
    def test_create_response(self):
        """Test creating an LLM response."""
        response = LLMResponse(
            content="Test response",
            model="claude-3-5-sonnet-20241022",
            input_tokens=100,
            output_tokens=50,
            stop_reason="end_turn",
        )
        
        assert response.content == "Test response"
        assert response.model == "claude-3-5-sonnet-20241022"
        assert response.input_tokens == 100
        assert response.output_tokens == 50
        assert response.stop_reason == "end_turn"
    
    def test_total_tokens(self):
        """Test total_tokens property calculation."""
        response = LLMResponse(
            content="Test",
            model="claude-3-5-sonnet-20241022",
            input_tokens=100,
            output_tokens=50,
        )
        
        assert response.total_tokens == 150


class TestAnthropicProvider:
    """Tests for AnthropicProvider."""
    
    def test_init_with_api_key(self):
        """Test initialization with explicit API key."""
        with patch('src.providers.anthropic_provider.anthropic') as mock_anthropic:
            mock_anthropic.Anthropic = Mock()
            
            provider = AnthropicProvider(api_key="test-key", model="claude-3-opus-20240229")
            
            assert provider.model_name == "claude-3-opus-20240229"
            assert provider.provider_name == "anthropic"
            mock_anthropic.Anthropic.assert_called_once_with(api_key="test-key")
    
    def test_init_from_env_var(self):
        """Test initialization using ANTHROPIC_API_KEY environment variable."""
        with patch('src.providers.anthropic_provider.anthropic') as mock_anthropic:
            mock_anthropic.Anthropic = Mock()
            
            with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'env-test-key'}):
                _ = AnthropicProvider()  # We just need to test initialization, not use the provider
                
                mock_anthropic.Anthropic.assert_called_once_with(api_key="env-test-key")
    
    def test_init_missing_api_key(self):
        """Test initialization fails without API key."""
        with patch('src.providers.anthropic_provider.anthropic'):
            with patch.dict(os.environ, {}, clear=True):
                with pytest.raises(LLMError, match="API key not provided"):
                    AnthropicProvider()
    
    def test_init_missing_anthropic_package(self):
        """Test initialization fails if anthropic package not installed."""
        with patch('src.providers.anthropic_provider.anthropic', None):
            with pytest.raises(LLMError, match="anthropic package not installed"):
                _provider = AnthropicProvider(api_key="test-key")
    
    def test_call_basic(self):
        """Test basic LLM call."""
        with patch('src.providers.anthropic_provider.anthropic') as mock_anthropic:
            # Setup mock response
            mock_response = Mock()
            mock_response.content = [Mock(text="Response text")]
            mock_response.model = "claude-3-5-sonnet-20241022"
            mock_response.usage.input_tokens = 100
            mock_response.usage.output_tokens = 50
            mock_response.stop_reason = "end_turn"
            
            mock_client = Mock()
            mock_client.messages.create.return_value = mock_response
            mock_anthropic.Anthropic.return_value = mock_client
            
            # Create provider and make call
            provider = AnthropicProvider(api_key="test-key")
            response = provider.call(
                prompt="Test prompt",
                max_tokens=1000,
                temperature=0.5,
            )
            
            # Verify call was made correctly
            mock_client.messages.create.assert_called_once_with(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                temperature=0.5,
                messages=[{"role": "user", "content": "Test prompt"}],
            )
            
            # Verify response
            assert response.content == "Response text"
            assert response.model == "claude-3-5-sonnet-20241022"
            assert response.input_tokens == 100
            assert response.output_tokens == 50
            assert response.stop_reason == "end_turn"
    
    def test_call_with_system_prompt(self):
        """Test LLM call with system prompt."""
        with patch('src.providers.anthropic_provider.anthropic') as mock_anthropic:
            mock_response = Mock()
            mock_response.content = [Mock(text="Response")]
            mock_response.model = "claude-3-5-sonnet-20241022"
            mock_response.usage.input_tokens = 100
            mock_response.usage.output_tokens = 50
            mock_response.stop_reason = "end_turn"
            
            mock_client = Mock()
            mock_client.messages.create.return_value = mock_response
            mock_anthropic.Anthropic.return_value = mock_client
            
            provider = AnthropicProvider(api_key="test-key")
            provider.call(
                prompt="Test prompt",
                max_tokens=1000,
                system_prompt="You are a helpful assistant.",
            )
            
            # Verify system prompt was included
            call_args = mock_client.messages.create.call_args[1]
            assert call_args["system"] == "You are a helpful assistant."
    
    def test_call_api_error(self):
        """Test handling of Anthropic API errors."""
        with patch('src.providers.anthropic_provider.anthropic') as mock_anthropic:
            # Create a proper exception class
            class MockAPIError(Exception):
                pass
            
            mock_anthropic.APIError = MockAPIError
            
            mock_client = Mock()
            mock_client.messages.create.side_effect = MockAPIError("API error")
            mock_anthropic.Anthropic.return_value = mock_client
            
            provider = AnthropicProvider(api_key="test-key")
            
            with pytest.raises(LLMError, match="Anthropic API error"):
                provider.call(prompt="Test", max_tokens=100)
    
    def test_call_unexpected_error(self):
        """Test handling of unexpected errors."""
        with patch('src.providers.anthropic_provider.anthropic') as mock_anthropic:
            # Create a proper exception class for APIError (won't be raised)
            class MockAPIError(Exception):
                pass
            
            mock_anthropic.APIError = MockAPIError
            
            mock_client = Mock()
            mock_client.messages.create.side_effect = ValueError("Unexpected error")
            mock_anthropic.Anthropic.return_value = mock_client
            
            provider = AnthropicProvider(api_key="test-key")
            
            with pytest.raises(LLMError, match="Unexpected error calling Anthropic"):
                provider.call(prompt="Test", max_tokens=100)


class TestProviderProtocol:
    """Tests to verify AnthropicProvider implements LLMProvider protocol."""
    
    def test_anthropic_provider_implements_protocol(self):
        """Verify AnthropicProvider has all required methods."""
        with patch('src.providers.anthropic_provider.anthropic') as mock_anthropic:
            mock_anthropic.Anthropic = Mock()
            
            provider = AnthropicProvider(api_key="test-key")
            
            # Check required methods exist
            assert hasattr(provider, 'call')
            assert hasattr(provider, 'model_name')
            assert hasattr(provider, 'provider_name')
            
            # Check they're callable/properties
            assert callable(provider.call)
            assert isinstance(provider.model_name, str)
            assert isinstance(provider.provider_name, str)
