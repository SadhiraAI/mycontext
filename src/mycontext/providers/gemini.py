"""
Google Gemini Provider Implementation

Integrates with Google's Gemini API using the new google.genai library
"""

import time
from typing import Any, Dict, Optional

try:
    from google import genai
    GEMINI_AVAILABLE = True
    USING_NEW_API = True
except ImportError:
    # Fallback to old library if new one isn't available
    try:
        import google.generativeai as genai
        GEMINI_AVAILABLE = True
        USING_NEW_API = False
    except ImportError:
        GEMINI_AVAILABLE = False
        USING_NEW_API = False

from .base import BaseProvider, ProviderResponse


class GeminiProvider(BaseProvider):
    """
    Google Gemini provider implementation.
    
    Supports Gemini Pro, Gemini Pro Vision, and other Gemini models.
    
    Args:
        api_key: Google API key (or set GOOGLE_API_KEY env var)
        model: Default model to use
        
    Example:
        >>> from mycontext import Context
        >>> from mycontext.providers import GeminiProvider
        >>> 
        >>> provider = GeminiProvider(api_key="...")
        >>> context = Context("You are a helpful assistant")
        >>> response = provider.generate(context, user="Hello!")
        >>> print(response.response)
    """
    
    # Pricing per 1M tokens (updated for Gemini 2.0+)
    PRICING = {
        # Gemini 2.5 (latest, Feb 2026)
        "gemini-2.5-flash": {"input": 0.075, "output": 0.30},
        "gemini-2.5-flash-latest": {"input": 0.075, "output": 0.30},
        "gemini-2.5-pro": {"input": 3.50, "output": 10.50},
        "gemini-2.5-pro-latest": {"input": 3.50, "output": 10.50},
        
        # Gemini 2.0 (current generation)
        "gemini-2.0-flash": {"input": 0.10, "output": 0.40},
        "gemini-2.0-flash-001": {"input": 0.10, "output": 0.40},
        "gemini-2.0-flash-exp": {"input": 0.10, "output": 0.40},
        "gemini-2.0-flash-thinking-exp": {"input": 0.10, "output": 0.40},
        "gemini-2.0-flash-exp-image-generation": {"input": 0.10, "output": 0.40},
        
        # Gemini 1.5 (previous generation - may be deprecated)
        "gemini-1.5-pro": {"input": 3.50, "output": 10.50},
        "gemini-1.5-pro-latest": {"input": 3.50, "output": 10.50},
        "gemini-1.5-pro-001": {"input": 3.50, "output": 10.50},
        "gemini-1.5-pro-002": {"input": 3.50, "output": 10.50},
        "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
        "gemini-1.5-flash-latest": {"input": 0.075, "output": 0.30},
        "gemini-1.5-flash-001": {"input": 0.075, "output": 0.30},
        "gemini-1.5-flash-002": {"input": 0.075, "output": 0.30},
        "gemini-1.5-flash-8b": {"input": 0.0375, "output": 0.15},
        
        # Gemini 1.0 (legacy)
        "gemini-1.0-pro": {"input": 0.50, "output": 1.50},
        "gemini-1.0-pro-001": {"input": 0.50, "output": 1.50},
        "gemini-1.0-pro-002": {"input": 0.50, "output": 1.50},
        "gemini-pro": {"input": 0.50, "output": 1.50},
        "gemini-pro-vision": {"input": 0.50, "output": 1.50},
        "gemini-1.0-pro-vision": {"input": 0.50, "output": 1.50},
        
        # Experimental models
        "gemini-exp-1114": {"input": 0.075, "output": 0.30},
        "gemini-exp-1121": {"input": 0.075, "output": 0.30},
        "gemini-exp-1206": {"input": 0.075, "output": 0.30},
    }
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gemini-2.5-flash",  # Updated to latest model
        **kwargs: Any
    ):
        if not GEMINI_AVAILABLE:
            raise ImportError(
                "Google Generative AI package not installed. "
                "Install with: pip install 'mycontext[google]'"
            )
        
        # Get API key
        if not api_key:
            import os
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError(
                    "GOOGLE_API_KEY environment variable not set. "
                    "Either set it or pass api_key parameter."
                )
        
        # Configure based on library version
        if USING_NEW_API:
            # New google.genai library
            self.client = genai.Client(api_key=api_key)
        else:
            # Old google.generativeai library
            genai.configure(api_key=api_key)
            self.client = None
        
        self.api_key = api_key
        self.default_model = model
        self._model = None  # Lazy initialize
    
    def generate(
        self,
        context: "Context",
        user: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 1.0,
        max_tokens: Optional[int] = None,
        **kwargs: Any
    ) -> ProviderResponse:
        """
        Generate a response using Google Gemini.
        
        Args:
            context: Context to execute
            user: User message (if any)
            model: Model to use (overrides default)
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional Gemini API parameters
            
        Returns:
            Standardized provider response
        """
        model_name = model or self.default_model
        
        # Build prompt
        system_prompt = context.assemble()
        
        # Combine system and user messages
        if user:
            full_prompt = f"{system_prompt}\n\nUser: {user}\n\nAssistant:"
        else:
            full_prompt = system_prompt
        
        # Make API call with timing
        start_time = time.time()
        
        generation_config = {
            "temperature": temperature,
        }
        if max_tokens:
            generation_config["max_output_tokens"] = max_tokens
        
        try:
            if USING_NEW_API:
                # New google.genai library
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=full_prompt,
                    config=generation_config
                )
            else:
                # Old google.generativeai library
                model_instance = genai.GenerativeModel(model_name)
                response = model_instance.generate_content(
                    full_prompt,
                    generation_config=generation_config,
                    **kwargs
                )
        except Exception as e:
            # Better error message
            if "not found" in str(e).lower():
                available_models = self._get_available_models()
                raise ValueError(
                    f"Model '{model_name}' not found. "
                    f"Try one of: {', '.join(available_models[:5])}"
                ) from e
            raise
        
        latency_ms = int((time.time() - start_time) * 1000)
        
        # Extract response text
        try:
            content = response.text
        except (ValueError, AttributeError):
            # Handle blocked responses or different response structure
            try:
                content = response.candidates[0].content.parts[0].text
            except:
                content = "[Response blocked by safety filters]"
        
        # Calculate usage (Gemini doesn't always provide token counts)
        # We'll estimate based on character count
        prompt_chars = len(full_prompt)
        response_chars = len(content)
        
        # Rough estimate: 4 chars ≈ 1 token
        input_tokens = prompt_chars // 4
        output_tokens = response_chars // 4
        tokens_used = input_tokens + output_tokens
        
        # Calculate cost
        cost = self._calculate_cost(
            model=model_name,
            input_tokens=input_tokens,
            output_tokens=output_tokens
        )
        
        return ProviderResponse(
            response=content,
            tokens_used=tokens_used,
            cost_usd=cost,
            latency_ms=latency_ms,
            model=model_name,
            metadata={
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "safety_ratings": getattr(response, 'safety_ratings', None),
                "using_new_api": USING_NEW_API,
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
        return "gemini"
    
    @property
    def models(self) -> list[str]:
        """Available models"""
        return list(self.PRICING.keys())
    
    def _get_available_models(self) -> list[str]:
        """Get list of available models from Google API"""
        try:
            if USING_NEW_API:
                # New API
                models = self.client.models.list()
                return [m.name.replace("models/", "") for m in models if hasattr(m, 'supported_generation_methods')]
            else:
                # Old API
                models = genai.list_models()
                return [m.name.replace("models/", "") for m in models if "generateContent" in m.supported_generation_methods]
        except:
            # Fallback to our hardcoded list
            return self.models
