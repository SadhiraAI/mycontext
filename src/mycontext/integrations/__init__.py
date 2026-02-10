"""
Integrations - Seamless interoperability with popular AI frameworks

Helper modules for integrating mycontext with:
- LangChain
- LlamaIndex
- CrewAI
- AutoGen
- DSPy
- Semantic Kernel
"""

from .helpers import (
    LangChainHelper,
    LlamaIndexHelper,
    CrewAIHelper,
    AutoGenHelper,
    DSPyHelper,
    SemanticKernelHelper,
    auto_integrate
)

__all__ = [
    "LangChainHelper",
    "LlamaIndexHelper",
    "CrewAIHelper",
    "AutoGenHelper",
    "DSPyHelper",
    "SemanticKernelHelper",
    "auto_integrate",
]
