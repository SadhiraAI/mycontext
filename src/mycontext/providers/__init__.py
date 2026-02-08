"""
Provider Layer - LLM Provider Integration

This layer provides the interface to different LLM providers.
"""

from typing import Any, Dict, Optional

from .base import BaseProvider, ProviderResponse
from .mock import MockProvider

# Lazy imports for optional dependencies
_PROVIDER_CACHE: Dict[str, BaseProvider] = {}


__all__ = [
    "BaseProvider",
    "ProviderResponse",
    "MockProvider",
    "OpenAIProvider",
    "AnthropicProvider",
    "GeminiProvider",
    "get_provider",
    "register_provider",
    "list_providers",
]


def __getattr__(name: str) -> Any:
    """Lazy import providers to avoid unnecessary dependencies"""
    if name == "OpenAIProvider":
        from .openai import OpenAIProvider
        return OpenAIProvider
    elif name == "AnthropicProvider":
        from .anthropic import AnthropicProvider
        return AnthropicProvider
    elif name == "GeminiProvider":
        from .gemini import GeminiProvider
        return GeminiProvider
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


# Provider registry
_PROVIDER_REGISTRY: Dict[str, type[BaseProvider]] = {
    "mock": MockProvider,
}


def register_provider(name: str, provider_class: type[BaseProvider]) -> None:
    """
    Register a custom provider.
    
    Args:
        name: Provider name (used in get_provider)
        provider_class: Provider class (must inherit from BaseProvider)
        
    Example:
        >>> from mycontext.providers import register_provider
        >>> from mycontext.providers.base import BaseProvider
        >>> 
        >>> class MyCustomProvider(BaseProvider):
        ...     # implementation
        ...     pass
        >>> 
        >>> register_provider("custom", MyCustomProvider)
    """
    if not issubclass(provider_class, BaseProvider):
        raise TypeError(f"{provider_class} must inherit from BaseProvider")
    
    _PROVIDER_REGISTRY[name] = provider_class


def get_provider(
    name: str,
    api_key: Optional[str] = None,
    **kwargs: Any
) -> BaseProvider:
    """
    Get a provider instance by name.
    
    Args:
        name: Provider name ('openai', 'anthropic', 'mock', etc.)
        api_key: API key for the provider (optional, can use env var)
        **kwargs: Additional provider-specific arguments
        
    Returns:
        Provider instance
        
    Raises:
        ValueError: If provider not found
        ImportError: If provider package not installed
        
    Example:
        >>> from mycontext.providers import get_provider
        >>> 
        >>> # Get OpenAI provider
        >>> provider = get_provider("openai", api_key="sk-...")
        >>> 
        >>> # Get Anthropic provider
        >>> provider = get_provider("anthropic", api_key="sk-ant-...")
        >>> 
        >>> # Get mock provider (for testing)
        >>> provider = get_provider("mock")
    """
    # Check cache first
    cache_key = f"{name}:{api_key}"
    if cache_key in _PROVIDER_CACHE:
        return _PROVIDER_CACHE[cache_key]
    
    # Lazy register providers on first use
    if name == "openai" and name not in _PROVIDER_REGISTRY:
        from .openai import OpenAIProvider
        register_provider("openai", OpenAIProvider)
    elif name == "anthropic" and name not in _PROVIDER_REGISTRY:
        from .anthropic import AnthropicProvider
        register_provider("anthropic", AnthropicProvider)
    elif name == "gemini" and name not in _PROVIDER_REGISTRY:
        from .gemini import GeminiProvider
        register_provider("gemini", GeminiProvider)
    
    # Get provider class
    provider_class = _PROVIDER_REGISTRY.get(name)
    if not provider_class:
        available = ", ".join(_PROVIDER_REGISTRY.keys())
        raise ValueError(
            f"Provider '{name}' not found. "
            f"Available providers: {available}"
        )
    
    # Create instance
    if api_key:
        kwargs["api_key"] = api_key
    
    provider = provider_class(**kwargs)
    
    # Cache it
    _PROVIDER_CACHE[cache_key] = provider
    
    return provider


def list_providers() -> list[str]:
    """
    List all available providers.
    
    Returns:
        List of provider names
        
    Example:
        >>> from mycontext.providers import list_providers
        >>> print(list_providers())
        ['anthropic', 'gemini', 'mock', 'openai']
    """
    # Include lazy-loadable providers
    available = set(_PROVIDER_REGISTRY.keys())
    available.add("openai")
    available.add("anthropic")
    available.add("gemini")
    
    return sorted(available)
