"""
Anthropic Provider Implementation

Integrates with Anthropic's Claude API
"""

import time
from typing import Any, Dict, Optional

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

from .base import BaseProvider, ProviderResponse


class AnthropicProvider(BaseProvider):
    """
    Anthropic (Claude) provider implementation.
    
    Supports Claude 3.5 Sonnet, Claude 3 Opus, Claude 3 Haiku, etc.
    
    Args:
        api_key: Anthropic API key (or set ANTHROPIC_API_KEY env var)
        model: Default model to use
        base_url: Custom API base URL (for proxies)
        
    Example:
        >>> from mycontext import Context
        >>> from mycontext.providers import AnthropicProvider
        >>> 
        >>> provider = AnthropicProvider(api_key="sk-ant-...")
        >>> context = Context("You are a helpful assistant")
        >>> response = provider.generate(context, user="Hello!")
        >>> print(response.response)
    """
    
    # Pricing per 1M tokens (as of 2024)
    PRICING = {
        "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
        "claude-3-5-sonnet-20240620": {"input": 3.00, "output": 15.00},
        "claude-3-opus-20240229": {"input": 15.00, "output": 75.00},
        "claude-3-sonnet-20240229": {"input": 3.00, "output": 15.00},
        "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},
    }
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-3-5-sonnet-20241022",
        base_url: Optional[str] = None,
        **kwargs: Any
    ):
        if not ANTHROPIC_AVAILABLE:
            raise ImportError(
                "Anthropic package not installed. "
                "Install with: pip install 'mycontext[anthropic]'"
            )
        
        self.client = Anthropic(
            api_key=api_key,
            base_url=base_url,
            **kwargs
        )
        self.default_model = model
    
    def generate(
        self,
        context: "Context",
        user: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 1.0,
        max_tokens: int = 4096,
        **kwargs: Any
    ) -> ProviderResponse:
        """
        Generate a response using Anthropic Claude.
        
        Args:
            context: Context to execute
            user: User message (if any)
            model: Model to use (overrides default)
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional Anthropic API parameters
            
        Returns:
            Standardized provider response
        """
        model = model or self.default_model
        
        # Build system prompt
        system = context.assemble()
        
        # Build messages
        messages = []
        if user:
            messages.append({
                "role": "user",
                "content": user
            })
        
        # Claude requires at least one message
        if not messages:
            raise ValueError(
                "Anthropic provider requires at least a user message. "
                "Pass 'user' parameter to generate()."
            )
        
        # Make API call with timing
        start_time = time.time()
        
        response = self.client.messages.create(
            model=model,
            system=system,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        latency_ms = int((time.time() - start_time) * 1000)
        
        # Extract response
        content_blocks = response.content
        if content_blocks:
            # Get text from first content block
            text_content = next(
                (block.text for block in content_blocks if hasattr(block, 'text')),
                ""
            )
        else:
            text_content = ""
        
        # Calculate usage and cost
        usage = response.usage
        input_tokens = usage.input_tokens
        output_tokens = usage.output_tokens
        tokens_used = input_tokens + output_tokens
        
        cost = self._calculate_cost(
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens
        )
        
        return ProviderResponse(
            response=text_content,
            tokens_used=tokens_used,
            cost_usd=cost,
            latency_ms=latency_ms,
            model=model,
            metadata={
                "stop_reason": response.stop_reason,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "stop_sequence": response.stop_sequence,
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
        return "anthropic"
    
    @property
    def models(self) -> list[str]:
        """Available models"""
        return list(self.PRICING.keys())
