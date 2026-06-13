"""Execute service: run Context against LLM with user's API key."""

import os
from typing import Any

try:
    from mycontext import Context
    from mycontext.providers import get_provider
except ImportError:
    Context = None
    get_provider = None

try:
    from mycontext.intelligence import smart_execute as sdk_smart_execute
except ImportError:
    sdk_smart_execute = None


async def execute_context_async(
    assembled_content: str,
    provider: str,
    api_key: str | None,
    user_message: str = "",
    **kwargs: Any,
) -> dict[str, Any] | None:
    """Execute assembled context with the LLM via provider.agenerate() (litellm.acompletion).

    Does not block the FastAPI event loop while waiting for the LLM response.
    """
    if not Context or not get_provider:
        return None

    ctx = Context(directive=assembled_content)
    provider_kwargs = {"api_key": api_key} if api_key else {}
    provider_kwargs.update(kwargs)

    try:
        p = get_provider(provider, **provider_kwargs)
        result = await p.agenerate(ctx, user=user_message or None)
        return {
            "response": result.response,
            "tokens_used": result.tokens_used,
            "model": result.model,
        }
    except Exception as e:
        return {"error": str(e)}


def _inject_api_key_env(provider: str, api_key: str | None):
    env_map = {
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "google": "GOOGLE_API_KEY",
        "gemini": "GOOGLE_API_KEY",
    }
    var = env_map.get(provider)
    if var and api_key:
        os.environ[var] = api_key


def smart_execute(
    question: str,
    provider: str,
    api_key: str | None,
    **kwargs: Any,
) -> dict[str, Any] | None:
    """Smart three-tier execution via the SDK complexity router.

    Extra keyword arguments (e.g. quality overrides like ``verbosity`` or
    ``answer_first``) are forwarded to the SDK's ``smart_execute``.
    """
    if not sdk_smart_execute:
        return None
    _inject_api_key_env(provider, api_key)
    try:
        response, meta = sdk_smart_execute(
            question, provider=provider, **kwargs,
        )
        return {
            "response": response,
            "mode": meta.get("mode", "unknown"),
            "templates_used": meta.get("templates_used", []),
            "assessment": meta.get("assessment", {}),
        }
    except Exception as e:
        return {"error": str(e)}
