"""
Provider Layer - LLM Provider Integration

Uses LiteLLM as the unified backend for OpenAI, Anthropic, Google Gemini,
and 100+ other providers through a single interface.

Individual provider wrappers (openai.py, anthropic.py, gemini.py) have been
removed in favour of the single LiteLLMProvider.  Custom providers can still
be registered via register_provider().
"""

from typing import Any, Dict, Optional

from .base import BaseProvider, ProviderResponse
from .mock import MockProvider

_PROVIDER_CACHE: dict[str, BaseProvider] = {}

_DEFAULT_MODELS: dict[str, str] = {
    "openai": "gpt-4o-mini",
    "anthropic": "claude-3-5-haiku-20241022",
    "gemini": "gemini-2.0-flash",
}

__all__ = [
    "BaseProvider",
    "ProviderResponse",
    "MockProvider",
    "LiteLLMProvider",
    "get_provider",
    "register_provider",
    "list_providers",
]


def __getattr__(name: str) -> Any:
    """Lazy import LiteLLMProvider to avoid requiring litellm at import time."""
    if name == "LiteLLMProvider":
        from .litellm_provider import LiteLLMProvider
        return LiteLLMProvider
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


_PROVIDER_REGISTRY: dict[str, type[BaseProvider]] = {
    "mock": MockProvider,
}


def register_provider(name: str, provider_class: type[BaseProvider]) -> None:
    """Register a custom provider."""
    if not issubclass(provider_class, BaseProvider):
        raise TypeError(f"{provider_class} must inherit from BaseProvider")
    _PROVIDER_REGISTRY[name] = provider_class


def get_provider(
    name: str,
    api_key: str | None = None,
    **kwargs: Any
) -> BaseProvider:
    """Get a provider instance by name.

    Supported built-in providers: ``"mock"``, ``"openai"``, ``"anthropic"``,
    ``"gemini"`` (alias ``"google"``), plus any custom provider registered
    via :func:`register_provider`.

    OpenAI, Anthropic, and Gemini are routed through LiteLLM automatically.
    """
    provider_name = {"google": "gemini"}.get(name, name)
    model = kwargs.get("model", "")
    cache_key = f"{provider_name}:{api_key}:{model}"
    if cache_key in _PROVIDER_CACHE:
        return _PROVIDER_CACHE[cache_key]

    if provider_name in _PROVIDER_REGISTRY:
        provider_class = _PROVIDER_REGISTRY[provider_name]
        if api_key:
            kwargs["api_key"] = api_key
        provider = provider_class(**kwargs)
        _PROVIDER_CACHE[cache_key] = provider
        return provider

    if provider_name in _DEFAULT_MODELS:
        from .litellm_provider import LiteLLMProvider
        kw = dict(kwargs)
        resolved_model = kw.pop("model", _DEFAULT_MODELS[provider_name])
        provider = LiteLLMProvider(
            model=resolved_model,
            provider=provider_name,
            api_key=api_key,
            **kw,
        )
        _PROVIDER_CACHE[cache_key] = provider
        return provider

    available = sorted(set(_PROVIDER_REGISTRY.keys()) | set(_DEFAULT_MODELS.keys()))
    raise ValueError(f"Provider '{name}' not found. Available: {', '.join(available)}")


def list_providers() -> list[str]:
    """List all available providers."""
    available = set(_PROVIDER_REGISTRY.keys())
    available.update(_DEFAULT_MODELS.keys())
    return sorted(available)
