"""
Base Provider Interface

All LLM providers must implement this interface.
"""

import asyncio as _asyncio
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from ..core import Context


class ProviderResponse(BaseModel):
    """
    Standardized response from any provider.

    Attributes:
        response: The generated text response
        tokens_used: Number of tokens consumed
        cost_usd: Estimated cost in USD
        latency_ms: Response time in milliseconds
        model: Model used
        metadata: Additional provider-specific data
    """

    response: str = Field(..., description="Generated text")

    tokens_used: int = Field(default=0, description="Tokens consumed")

    cost_usd: float = Field(default=0.0, description="Estimated cost")

    latency_ms: int = Field(default=0, description="Response time")

    model: str = Field(default="unknown", description="Model used")

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Provider-specific data"
    )


class BaseProvider(ABC):
    """
    Abstract base class for all LLM providers.

    All providers (OpenAI, Anthropic, Google, etc.) must implement
    this interface to ensure consistent behavior.

    Async support
    -------------
    Subclasses MAY override ``agenerate()`` for a true coroutine path.
    The default implementation runs ``generate()`` in a thread executor via
    ``asyncio.get_event_loop().run_in_executor()``, which is safe but does not
    yield the GIL while waiting.  LiteLLMProvider overrides this with a real
    ``litellm.acompletion()`` call.
    """

    @abstractmethod
    def generate(
        self,
        context: "Context",
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using this provider.

        Args:
            context: Context to execute
            **kwargs: Provider-specific parameters

        Returns:
            Standardized response
        """
        pass

    async def agenerate(
        self,
        context: "Context",
        **kwargs,
    ) -> ProviderResponse:
        """Async version of :meth:`generate`.

        Default: runs ``generate()`` in a thread-pool executor so it does not
        block the event loop.  Subclasses should override with a native async
        implementation for better performance.

        Args:
            context: Context to execute.
            **kwargs: Provider-specific parameters (same as ``generate``).

        Returns:
            Standardized ProviderResponse.
        """
        loop = _asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.generate(context, **kwargs))

    @abstractmethod
    def estimate_cost(self, tokens: int) -> float:
        """
        Estimate cost for given token count.

        Args:
            tokens: Number of tokens

        Returns:
            Estimated cost in USD
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name"""
        pass

    @property
    @abstractmethod
    def models(self) -> list[str]:
        """Available models"""
        pass
