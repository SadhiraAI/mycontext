# Sprint 4 — Prompt Compilation Pipeline

**Date:** 2026-02-21  
**Status:** In Progress  
**Predecessor:** Sprint 3B (templates validated at 96.6% avg)

---

## Motivation

Sprint 3B proved that cognitive templates add measurable value (+2.2pp over raw). But the current architecture has a structural limitation: **templates compete for the LLM's output token budget**. When 3 templates are integrated, the combined framework is ambitious, and the LLM must fill all sections in a single response.

The Prompt Compilation Pipeline introduces a new paradigm: **templates as prompt compilers, not just response generators.** Instead of executing templates and integrating their outputs, we generate optimized prompts from each template and compose them into a single, comprehensive prompt that the user can execute once (or take elsewhere).

## Core Innovation

### Two Execution Modes

| Mode | What Happens | Output |
|---|---|---|
| **Response Mode** (current) | Template → LLM → Full analytical response | Answer text |
| **Prompt Design Mode** (new) | Template → Optimized prompt capturing the cognitive framework | Prompt string |

### Chain Prompt Composition

```
Current: Q → select templates → build contexts → integrate → execute → response
New:     Q → select templates → generate prompts → compose → execute OR return prompt
```

### Why This Matters

1. **Solves token competition permanently** — prompts are compact, execution gets full output budget
2. **Provider-agnostic** — generated prompts work with any LLM (GPT-4, Claude, Gemini, local)
3. **Composable** — compact prompts merge cleanly; no output truncation risk
4. **Unique positioning** — no other SDK offers "cognitive prompt compilation"
5. **Agent-framework compatible** — smolagents, CrewAI, LangChain can use mycontext as their prompt brain

---

## Implementation Plan

### Phase 1: `Context.to_prompt()` Method

Add to `src/mycontext/core.py`:

```python
def to_prompt(self, refine: bool = False, provider: str = "openai", **kwargs) -> str:
    """Convert this context into an optimized prompt string.
    
    Args:
        refine: If True, use LLM to distill the context into a refined prompt.
                If False, zero-cost assembly (no API call).
        provider: Provider for LLM refinement (only used when refine=True).
    
    Returns:
        Optimized prompt string
    """
```

- `refine=False`: Zero-cost — reformats `assemble()` output into a clean, self-contained prompt
- `refine=True`: One cheap LLM call to distill the framework into a concise, natural prompt

### Phase 2: `PromptComposer` Class

New file: `src/mycontext/intelligence/prompt_composer.py`

```python
class PromptComposer:
    """Compose multiple template-generated prompts into one comprehensive prompt."""
    
    def compose(self, prompts: List[str], question: str, ...) -> ComposedPrompt:
        """Merge multiple prompts into a single comprehensive prompt."""
    
    def compose_from_templates(self, question: str, template_names: List[str], ...) -> ComposedPrompt:
        """Generate prompts from templates and compose them."""

class ComposedPrompt:
    """Result of prompt composition."""
    prompt: str              # The final composed prompt
    source_templates: List[str]  # Which templates contributed
    question: str            # Original question
    
    def execute(self, provider, **kwargs) -> str:  # Response Mode
    def to_string(self) -> str:                    # Prompt Design Mode
    def to_context(self) -> Context:               # Convert back to Context
```

### Phase 3: `smart_prompt()` Function

Add to `src/mycontext/intelligence/pattern_suggester.py`:

```python
def smart_prompt(question: str, ...) -> ComposedPrompt:
    """One-liner: analyze question → select templates → compose prompt.
    
    Returns a ComposedPrompt that can be executed or exported.
    """
```

### Phase 4: Integrator Update

Add to `TemplateIntegratorAgent`:

```python
def suggest_and_compile(self, question, ...) -> ComposedPrompt:
    """Like suggest_and_integrate, but returns a composed prompt instead of executing."""
```

### Phase 5: Exports & Testing

- Update `intelligence/__init__.py` with new exports
- Create Sprint 4 notebook for validation
- Compare Prompt Mode vs Response Mode vs Raw

---

## Success Criteria

1. `to_prompt(refine=False)` produces clean, self-contained prompts with zero API cost
2. `to_prompt(refine=True)` produces natural, optimized prompts via one LLM call
3. `PromptComposer.compose()` merges 2-3 template prompts without redundancy
4. `smart_prompt()` produces prompts that, when executed, score >= 95% on our evaluation
5. Prompt mode output length < 1,500 chars (compact, composable)
6. Chain-composed prompts outperform individual template prompts on complex questions

---

## Differentiation Analysis

| Capability | mycontext-ai | LangChain | LlamaIndex | CrewAI | DSPy |
|---|---|---|---|---|---|
| Cognitive templates | 85 research-backed | No | No | No | No |
| Prompt compilation | **Yes (new)** | No | No | No | Partial (optimizers) |
| Template chaining | Yes | No | No | No | No |
| Quality metrics (CAI) | Yes | No | No | No | No |
| Provider-agnostic prompts | **Yes (new)** | Partial | Partial | No | Yes |
| Agent-framework compatible | Yes | N/A | N/A | N/A | Partial |
