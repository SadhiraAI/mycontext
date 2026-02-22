"""
LiteLLM-backed provider -- unified interface for all LLM providers.

Uses litellm.completion() which routes to OpenAI, Anthropic, Google,
and 100+ providers via a single OpenAI-compatible interface.

Includes automatic retry with exponential backoff and configurable timeout.
"""

import logging
import time
from typing import Any

try:
    import litellm

    litellm.drop_params = True
    LITELLM_AVAILABLE = True
except Exception:
    litellm = None  # type: ignore[assignment]
    LITELLM_AVAILABLE = False

from .base import BaseProvider, ProviderResponse

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 120
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_BACKOFF = 2.0


def _litellm_model_name(provider: str, model: str) -> str:
    """Map (provider, model) to the litellm model string.

    LiteLLM uses bare names for OpenAI and Anthropic, but requires a
    ``gemini/`` prefix for Google models.
    """
    if provider in ("gemini", "google"):
        if not model.startswith("gemini/"):
            return f"gemini/{model}"
    return model


class LiteLLMProvider(BaseProvider):
    """Unified LLM provider powered by LiteLLM.

    Supports OpenAI, Anthropic, Google Gemini, and 100+ other providers
    through a single interface.

    Args:
        model: Default model name (e.g. ``gpt-4o-mini``).
        provider: Provider identifier (``openai``, ``anthropic``, ``gemini``).
        api_key: Optional API key override.
        timeout: Request timeout in seconds (default 120).
        max_retries: Maximum retry attempts on transient failures (default 3).
        retry_backoff: Base backoff multiplier in seconds (default 2.0).
    """

    def __init__(
        self,
        model: str,
        provider: str = "openai",
        api_key: str | None = None,
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        retry_backoff: float = DEFAULT_RETRY_BACKOFF,
        **kwargs: Any,
    ):
        global LITELLM_AVAILABLE, litellm
        if not LITELLM_AVAILABLE:
            try:
                import litellm as _litellm
                _litellm.drop_params = True
                litellm = _litellm
                LITELLM_AVAILABLE = True
            except Exception:
                raise ImportError(
                    "LiteLLM not installed. Install with: pip install litellm"
                )
        self._provider = provider
        self.api_key = api_key
        self.default_model = model
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_backoff = retry_backoff

    def generate(
        self,
        context: "Context",
        user: str | None = None,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        **kwargs: Any,
    ) -> ProviderResponse:
        """Generate a response via LiteLLM with retry and timeout.

        Retries on rate-limit (429), server errors (500/502/503), and
        timeout exceptions using exponential backoff.
        """
        model = model or self.default_model
        litellm_model = _litellm_model_name(self._provider, model)

        messages: list[dict[str, str]] = []
        system_prompt = context.assemble()
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if user:
            messages.append({"role": "user", "content": user})

        api_key = kwargs.pop("api_key", self.api_key)

        call_kwargs: dict[str, Any] = {
            "model": litellm_model,
            "messages": messages,
            "temperature": temperature,
            "timeout": kwargs.pop("timeout", self.timeout),
        }
        if api_key:
            call_kwargs["api_key"] = api_key
        if max_tokens:
            call_kwargs["max_tokens"] = max_tokens

        call_kwargs.update(kwargs)

        last_exc: Exception | None = None
        for attempt in range(1, self.max_retries + 1):
            try:
                start = time.time()
                response = litellm.completion(**call_kwargs)
                latency_ms = int((time.time() - start) * 1000)

                content = response.choices[0].message.content or ""
                usage = response.usage
                tokens_used = usage.total_tokens if usage else 0
                input_tokens = usage.prompt_tokens if usage else 0
                output_tokens = usage.completion_tokens if usage else 0

                try:
                    cost = litellm.completion_cost(completion_response=response)
                except Exception:
                    cost = 0.0

                return ProviderResponse(
                    response=content,
                    tokens_used=tokens_used,
                    cost_usd=cost,
                    latency_ms=latency_ms,
                    model=model,
                    metadata={
                        "litellm_model": litellm_model,
                        "input_tokens": input_tokens,
                        "output_tokens": output_tokens,
                        "finish_reason": (
                            response.choices[0].finish_reason
                            if response.choices
                            else None
                        ),
                        "attempt": attempt,
                    },
                )
            except Exception as exc:
                last_exc = exc
                if not self._is_retryable(exc) or attempt == self.max_retries:
                    break
                wait = self.retry_backoff * (2 ** (attempt - 1))
                logger.warning(
                    "LLM call failed (attempt %d/%d): %s — retrying in %.1fs",
                    attempt,
                    self.max_retries,
                    exc,
                    wait,
                )
                time.sleep(wait)

        raise RuntimeError(
            f"LLM call failed after {self.max_retries} attempts: {last_exc}"
        ) from last_exc

    @staticmethod
    def _is_retryable(exc: Exception) -> bool:
        """Return True if the exception is transient and worth retrying."""
        exc_str = str(exc).lower()
        retryable_signals = [
            "rate_limit",
            "rate limit",
            "429",
            "timeout",
            "timed out",
            "502",
            "503",
            "server error",
            "overloaded",
            "connection",
        ]
        return any(signal in exc_str for signal in retryable_signals)

    def estimate_cost(self, tokens: int, model: str | None = None) -> float:
        """Rough cost estimate using LiteLLM pricing tables."""
        model = model or self.default_model
        litellm_model = _litellm_model_name(self._provider, model)
        try:
            prompt_cost, completion_cost = litellm.cost_per_token(
                model=litellm_model,
                prompt_tokens=tokens // 2,
                completion_tokens=tokens // 2,
            )
            return prompt_cost + completion_cost
        except Exception:
            return 0.0

    @property
    def name(self) -> str:
        return self._provider

    @property
    def models(self) -> list[str]:
        """Return known models for this provider from LiteLLM registry."""
        try:
            return litellm.models_by_provider.get(self._provider, [])
        except Exception:
            return []
