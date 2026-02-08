"""
OpenAI Provider Implementation

Integrates with OpenAI's API (GPT-4, GPT-3.5, etc.)
"""

import time
from typing import Any, Dict, Optional

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from .base import BaseProvider, ProviderResponse


class OpenAIProvider(BaseProvider):
    """
    OpenAI provider implementation.
    
    Supports all OpenAI models including GPT-4, GPT-4 Turbo, GPT-3.5, etc.
    
    Args:
        api_key: OpenAI API key (or set OPENAI_API_KEY env var)
        model: Default model to use
        organization: OpenAI organization ID (optional)
        base_url: Custom API base URL (for proxies/local deployments)
        
    Example:
        >>> from mycontext import Context
        >>> from mycontext.providers import OpenAIProvider
        >>> 
        >>> provider = OpenAIProvider(api_key="sk-...")
        >>> context = Context("You are a helpful assistant")
        >>> response = provider.generate(context, user="Hello!")
        >>> print(response.response)
    """
    
    # Pricing per 1M tokens (as of 2024)
    PRICING = {
        "gpt-4o": {"input": 5.00, "output": 15.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-4-turbo": {"input": 10.00, "output": 30.00},
        "gpt-4": {"input": 30.00, "output": 60.00},
        "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    }
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4o-mini",
        organization: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs: Any
    ):
        if not OPENAI_AVAILABLE:
            raise ImportError(
                "OpenAI package not installed. "
                "Install with: pip install 'mycontext[openai]'"
            )
        
        self.client = OpenAI(
            api_key=api_key,
            organization=organization,
            base_url=base_url,
            **kwargs
        )
        self.default_model = model
    
    def generate(
        self,
        context: "Context",
        user: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI.
        
        Args:
            context: Context to execute
            user: User message (if any)
            model: Model to use (overrides default)
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional OpenAI API parameters
            
        Returns:
            Standardized provider response
        """
        model = model or self.default_model
        
        # Build messages
        messages = []
        
        # Add system message from context
        system_prompt = context.assemble()
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        # Add user message if provided
        if user:
            messages.append({
                "role": "user",
                "content": user
            })
        
        # Make API call with timing
        start_time = time.time()
        
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        latency_ms = int((time.time() - start_time) * 1000)
        
        # Extract response
        choice = response.choices[0]
        content = choice.message.content or ""
        
        # Calculate usage and cost
        usage = response.usage
        if usage:
            tokens_used = usage.total_tokens
            input_tokens = usage.prompt_tokens
            output_tokens = usage.completion_tokens
            
            # Estimate cost
            cost = self._calculate_cost(
                model=model,
                input_tokens=input_tokens,
                output_tokens=output_tokens
            )
        else:
            tokens_used = 0
            cost = 0.0
        
        return ProviderResponse(
            response=content,
            tokens_used=tokens_used,
            cost_usd=cost,
            latency_ms=latency_ms,
            model=model,
            metadata={
                "finish_reason": choice.finish_reason,
                "input_tokens": usage.prompt_tokens if usage else 0,
                "output_tokens": usage.completion_tokens if usage else 0,
            }
        )
    
    def _calculate_cost(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """Calculate cost in USD"""
        # Get pricing for model
        pricing = self.PRICING.get(model)
        if not pricing:
            # Unknown model, return 0
            return 0.0
        
        # Calculate cost (pricing is per 1M tokens)
        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        
        return input_cost + output_cost
    
    def estimate_cost(self, tokens: int, model: Optional[str] = None) -> float:
        """
        Estimate cost for given token count.
        
        Uses average of input/output pricing as estimate.
        
        Args:
            tokens: Number of tokens
            model: Model to estimate for
            
        Returns:
            Estimated cost in USD
        """
        model = model or self.default_model
        
        pricing = self.PRICING.get(model)
        if not pricing:
            return 0.0
        
        # Use average of input/output
        avg_price = (pricing["input"] + pricing["output"]) / 2
        return (tokens / 1_000_000) * avg_price
    
    @property
    def name(self) -> str:
        """Provider name"""
        return "openai"
    
    @property
    def models(self) -> list[str]:
        """Available models"""
        return list(self.PRICING.keys())
