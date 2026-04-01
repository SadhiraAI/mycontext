"""
Tests for Gemini provider (routed through LiteLLM)
"""

import pytest

from mycontext.providers import get_provider, list_providers


def test_gemini_in_provider_list():
    """Test that Gemini is in the provider list"""
    providers = list_providers()
    assert "gemini" in providers


def test_google_alias_in_get_provider():
    """Test that 'google' is accepted as alias for 'gemini'"""
    try:
        provider = get_provider("google", api_key="test-key")
        from mycontext.providers.litellm_provider import LiteLLMProvider

        assert isinstance(provider, LiteLLMProvider)
    except ImportError:
        pytest.skip("LiteLLM not installed")


def test_gemini_provider_via_litellm():
    """Test creating gemini provider through LiteLLM"""
    try:
        provider = get_provider("gemini", api_key="test-key")
        from mycontext.providers.litellm_provider import LiteLLMProvider

        assert isinstance(provider, LiteLLMProvider)
        assert provider.default_model == "gemini-2.0-flash"
    except ImportError:
        pytest.skip("LiteLLM not installed")


def test_gemini_custom_model():
    """Test creating gemini provider with custom model"""
    try:
        provider = get_provider("gemini", api_key="test-key", model="gemini-1.5-pro")
        assert provider.default_model == "gemini-1.5-pro"
    except ImportError:
        pytest.skip("LiteLLM not installed")
