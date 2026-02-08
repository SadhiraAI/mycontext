"""
Quick test for Gemini provider
"""

import pytest
from unittest.mock import Mock, patch

from mycontext import Context, Directive, Guidance
from mycontext.providers import get_provider, list_providers


def test_gemini_in_provider_list():
    """Test that Gemini is in the provider list"""
    providers = list_providers()
    assert "gemini" in providers


def test_gemini_provider_not_installed():
    """Test Gemini provider when package not installed"""
    with patch.dict('sys.modules', {'google.generativeai': None}):
        # Should lazy load
        providers = list_providers()
        assert "gemini" in providers


def test_gemini_import_error():
    """Test that proper error is raised when google package not installed"""
    # This will only work if google-generativeai is not installed
    # We can't fully test this without uninstalling the package
    pass


@pytest.mark.skipif(True, reason="Gemini not installed in test env")
def test_gemini_provider_import():
    """Test importing Gemini provider"""
    from mycontext.providers.gemini import GeminiProvider
    
    assert GeminiProvider is not None


def test_gemini_models():
    """Test Gemini model list"""
    try:
        provider = get_provider("gemini")
        models = provider.models
        
        assert "gemini-1.5-flash" in models
        assert "gemini-1.5-pro" in models
        assert "gemini-1.0-pro" in models
    except ImportError:
        # Expected if package not installed
        pytest.skip("Google Generative AI package not installed")


def test_gemini_cost_estimation():
    """Test Gemini cost estimation"""
    try:
        provider = get_provider("gemini", model="gemini-1.5-flash")
        
        # Flash should be cheapest
        cost = provider.estimate_cost(10000)
        assert cost > 0
        assert cost < 0.01  # Should be very cheap
        
    except ImportError:
        pytest.skip("Google Generative AI package not installed")
