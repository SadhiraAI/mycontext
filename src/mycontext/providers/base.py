"""
Base Provider Interface

All LLM providers must implement this interface.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


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
    
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Provider-specific data"
    )


class BaseProvider(ABC):
    """
    Abstract base class for all LLM providers.
    
    All providers (OpenAI, Anthropic, Google, etc.) must implement
    this interface to ensure consistent behavior.
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
