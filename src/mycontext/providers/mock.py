"""
Mock Provider for Testing

A simple mock provider for testing without API calls.
"""

from .base import BaseProvider, ProviderResponse


class MockProvider(BaseProvider):
    """
    Mock provider for testing.
    
    Returns canned responses without making real API calls.
    """

    def generate(self, context: "Context", **kwargs) -> ProviderResponse:
        """
        Generate a mock response.
        
        Args:
            context: Context to execute
            **kwargs: Additional parameters
            
        Returns:
            Mock response
        """
        # Assemble the context
        assembled = context.assemble()

        # Create a mock response
        return ProviderResponse(
            response=f"Mock response for: {assembled[:100]}...",
            tokens_used=100,
            cost_usd=0.001,
            latency_ms=50,
            model="mock-model-v1"
        )

    def estimate_cost(self, tokens: int) -> float:
        """
        Estimate cost (mock).
        
        Args:
            tokens: Token count
            
        Returns:
            Mock cost
        """
        return tokens * 0.00001

    @property
    def name(self) -> str:
        """Provider name"""
        return "mock"

    @property
    def models(self) -> list[str]:
        """Available models"""
        return ["mock-model-v1", "mock-model-v2"]
