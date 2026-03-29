# Orchestration Examples

**Minimal scripts (Tier 1 ICP):** [`../tier1_python_agents/`](../tier1_python_agents/README.md) — tiny OpenAI / LangChain / LiteLLM flows without notebooks.

**Tier 1 curriculum (numbered adoption notebooks):** [CURRICULUM.md](../../docs/adoption/tier1-python-agents/CURRICULUM.md) · [`notebooks/`](../../docs/adoption/tier1-python-agents/notebooks/) (exports, PromptArchitect, suggest/transform, Blueprint, quality eval, chains, Skills, plus **08** daily scenarios & **09** token/cost controls).

Simple notebooks that verify mycontext templates work with popular AI orchestrators.

| Notebook | Orchestrator | Template |
|----------|--------------|----------|
| langchain_code_reviewer.ipynb | LangChain | code_reviewer |
| langgraph_root_cause.ipynb | LangGraph | root_cause_analyzer |
| crewai_feedback_composer.ipynb | CrewAI | feedback_composer |
| autogen_risk_assessor.ipynb | AutoGen | risk_assessor |
| semantic_kernel_technical_translator.ipynb | Semantic Kernel | technical_translator |
| google_adk_concept_explainer.ipynb | Google ADK | concept_explainer |
| microsoft_agent_framework_narrative_builder.ipynb | Microsoft Agent Framework | narrative_builder |
| a2a_synthesis_builder.ipynb | A2A (Agent2Agent) | synthesis_builder |

## Prerequisites

pip install "mycontext-ai[openai]"

Set OPENAI_API_KEY. Each notebook lists its orchestrator-specific deps.

## Integrations

Uses mycontext.integrations: LangChainHelper, CrewAIHelper, AutoGenHelper, SemanticKernelHelper, GoogleADKHelper. Microsoft Agent Framework and A2A use context.assemble() directly.
