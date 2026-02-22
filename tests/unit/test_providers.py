"""
Tests for Provider Layer
"""

import pytest
from unittest.mock import Mock, patch

from mycontext import Context, Directive, Guidance
from mycontext.providers import (
    get_provider,
    register_provider,
    list_providers,
    MockProvider,
)
from mycontext.providers.base import BaseProvider, ProviderResponse


# ============================================================================
# Provider Registry Tests
# ============================================================================

def test_get_mock_provider():
    """Test getting mock provider"""
    provider = get_provider("mock")
    
    assert provider is not None
    assert isinstance(provider, MockProvider)
    assert provider.name == "mock"


def test_list_providers():
    """Test listing available providers"""
    providers = list_providers()
    
    assert "mock" in providers
    assert "openai" in providers
    assert "anthropic" in providers


def test_register_custom_provider():
    """Test registering a custom provider"""
    
    class CustomProvider(BaseProvider):
        def generate(self, context, **kwargs):
            return ProviderResponse(
                response="custom response",
                model="custom-model"
            )
        
        def estimate_cost(self, tokens):
            return 0.0
        
        @property
        def name(self):
            return "custom"
        
        @property
        def models(self):
            return ["custom-model"]
    
    # Register it
    register_provider("custom", CustomProvider)
    
    # Get it
    provider = get_provider("custom")
    assert provider.name == "custom"


def test_get_invalid_provider():
    """Test getting invalid provider raises error"""
    with pytest.raises(ValueError, match="Provider 'invalid' not found"):
        get_provider("invalid")


# ============================================================================
# MockProvider Tests
# ============================================================================

def test_mock_provider_generate():
    """Test mock provider generation"""
    provider = MockProvider()
    context = Context("You are helpful")
    
    response = provider.generate(context, user="Hello")
    
    assert "Mock response for:" in response.response
    assert response.tokens_used > 0
    assert response.cost_usd > 0.0
    assert response.model == "mock-model-v1"


def test_mock_provider_without_user():
    """Test mock provider without user message"""
    provider = MockProvider()
    context = Context("System message")
    
    response = provider.generate(context)
    
    assert "Mock response" in response.response


def test_mock_provider_estimate_cost():
    """Test mock cost estimation"""
    provider = MockProvider()
    
    cost = provider.estimate_cost(1000)
    assert cost > 0.0  # Mock returns non-zero cost


# ============================================================================
# LiteLLM-backed Provider Tests
# ============================================================================

def test_openai_in_provider_list():
    """Test that openai is available through LiteLLM routing"""
    providers = list_providers()
    assert "openai" in providers


def test_anthropic_in_provider_list():
    """Test that anthropic is available through LiteLLM routing"""
    providers = list_providers()
    assert "anthropic" in providers


def test_get_litellm_provider():
    """Test that known providers route to LiteLLMProvider when litellm is installed"""
    try:
        provider = get_provider("openai", api_key="test-key")
        from mycontext.providers.litellm_provider import LiteLLMProvider
        assert isinstance(provider, LiteLLMProvider)
    except ImportError:
        pytest.skip("LiteLLM not installed")


# ============================================================================
# Provider Response Tests
# ============================================================================

def test_provider_response_creation():
    """Test creating a provider response"""
    response = ProviderResponse(
        response="Hello world",
        tokens_used=10,
        cost_usd=0.001,
        latency_ms=250,
        model="test-model",
        metadata={"extra": "data"}
    )
    
    assert response.response == "Hello world"
    assert response.tokens_used == 10
    assert response.cost_usd == 0.001
    assert response.latency_ms == 250
    assert response.model == "test-model"
    assert response.metadata["extra"] == "data"


def test_provider_response_defaults():
    """Test provider response with defaults"""
    response = ProviderResponse(response="Test")
    
    assert response.response == "Test"
    assert response.tokens_used == 0
    assert response.cost_usd == 0.0
    assert response.latency_ms == 0
    assert response.model == "unknown"
    assert response.metadata == {}


# ============================================================================
# Integration Tests with Context
# ============================================================================

def test_context_execute_with_mock_provider():
    """Test Context.execute with mock provider"""
    context = Context(
        guidance=Guidance(role="Assistant"),
        directive=Directive(content="Be helpful")
    )
    
    response = context.execute(
        provider="mock",
        user="What is 2+2?"
    )
    
    assert response is not None
    assert isinstance(response, ProviderResponse)
    assert "Mock response" in response.response


def test_context_execute_with_complex_context():
    """Test executing complex context"""
    context = Context(
        guidance=Guidance(
            role="Expert Developer",
            rules=["Be thorough", "Provide examples"],
            style="professional"
        ),
        directive=Directive(
            content="Review the code",
            priority=9
        )
    )
    
    response = context.execute(
        provider="mock",
        user="Here is my code..."
    )
    
    assert response.response is not None
    assert response.tokens_used > 0


def test_provider_caching():
    """Test that providers are cached"""
    provider1 = get_provider("mock")
    provider2 = get_provider("mock")
    
    # Should be the same instance (cached)
    assert provider1 is provider2


# ============================================================================
# Error Handling Tests
# ============================================================================

def test_custom_provider_must_inherit_base():
    """Test that custom providers must inherit from BaseProvider"""
    
    class InvalidProvider:
        pass
    
    with pytest.raises(TypeError):
        register_provider("invalid", InvalidProvider)


def test_provider_interface():
    """Test that BaseProvider enforces interface"""
    
    # This should fail because methods aren't implemented
    with pytest.raises(TypeError):
        # Can't instantiate abstract class
        BaseProvider()
