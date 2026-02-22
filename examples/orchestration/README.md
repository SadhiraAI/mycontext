# Orchestration Examples

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
