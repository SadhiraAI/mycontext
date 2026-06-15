"""Provider-aware default model resolution for the RaC LLM passes.

When ``execute=True`` is used without an explicit ``model``, we must pick a
sensible default *for the chosen provider* — never silently hand an OpenAI model
id to Anthropic/Gemini/etc. Providers without a known cheap default require the
caller to pass ``model=`` (or ``--model`` on the CLI) explicitly.
"""

from __future__ import annotations

# Cheap, capable default per provider (LiteLLM-compatible ids; the provider maps
# names like ``gemini/`` internally — see providers/litellm_provider.py).
DEFAULT_MODELS: dict[str, str] = {
    "openai": "gpt-4o-mini",
    "anthropic": "claude-3-5-haiku-latest",
    "gemini": "gemini-1.5-flash",
    "google": "gemini-1.5-flash",
}


def resolve_model(provider: str, model: str | None) -> str:
    """Return ``model`` if given, else the default for ``provider``.

    Raises ``ValueError`` if no model is given and the provider has no known
    default, so a non-OpenAI provider never silently runs an OpenAI model.
    """
    if model:
        return model
    try:
        return DEFAULT_MODELS[provider]
    except KeyError:
        known = ", ".join(sorted(DEFAULT_MODELS))
        raise ValueError(
            f"No default model for provider {provider!r}. Pass an explicit model "
            f"(e.g. model=... in code, or --model on the CLI). Providers with a "
            f"built-in default: {known}."
        ) from None
