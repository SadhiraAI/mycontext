# SDK Optimization Research & Implementation Plan

**mycontext-ai: Research-Backed Optimization Opportunities**

**Document Version:** 2.0  
**Date:** February 23, 2025  
**Based on:** Full `/src` codebase analysis + external research

---

## TL;DR — Do I Buy It?

**Yes, but the original v1.0 was incomplete.** After reading the full codebase and external research, the bottlenecks are real, the infrastructure to fix them already exists (BatchProcessor, LiteLLM acompletion), and the fixes align directly with our product vision. This revised report adds exact file/line citations, research citations, and an honest assessment of what will help vs. what would be over-engineering.

---

## 1. What the Codebase Actually Does (Mapped Precisely)

### 1.1 LLM Call Audit — Every Sequential Chain

| Call Site | File | Lines | LLM Calls | Sequential? |
|-----------|------|-------|-----------|-------------|
| `compose_from_templates()` loop | prompt_composer.py | 265–279 | N (per template, when refine=True) | **Yes — main bottleneck** |
| `compose()` merge | prompt_composer.py | 213 | 1 | N/A |
| `measure()` raw vs template | context_amplification.py | 94–95 | 2 | **Yes — could be parallel** |
| `measure_chain()` | context_amplification.py | 149–152 | 2+ | **Yes — first two could be parallel** |
| `build_workflow_chain()` question_analyzer | chain_orchestration_agent.py | 145 | 1 | Sequential before orchestration |
| `build_workflow_chain()` chain selection | chain_orchestration_agent.py | 222 | 1 | Sequential after above |
| `suggest_and_integrate()` | template_integrator_agent.py | 179, 364 | 2 | Sequential but by design |
| `smart_execute()` complexity assess | pattern_suggester.py | 606 | 1 | Sequential before execution |
| `smart_execute()` execute | pattern_suggester.py | 618/631 | 1 | Sequential after above |

### 1.2 What Is and Isn't Used

| Component | Exists? | Used in Intelligence Layer? |
|-----------|---------|----------------------------|
| `BatchProcessor` (ThreadPoolExecutor) | Yes — `utils/batch.py:9` | **No — not imported anywhere in intelligence/** |
| `litellm.acompletion()` | Yes — LiteLLM native async | **No — only sync `litellm.completion()` used** |
| `litellm.batch_completion()` | Yes | **No** |
| `Context.aexecute()` | No — doesn't exist | N/A |
| `BaseProvider.agenerate()` | No — doesn't exist | N/A |

### 1.3 The Critical Path for Tier 2 (smart_prompt)

```
smart_prompt()
  → assess_complexity()          [1 LLM call]
  → suggest_patterns(mode=hybrid) [1 LLM call]
  → compose_from_templates(refine=True)
      → template 1: ctx.to_prompt(refine=True)  [1 LLM call — sequential]
      → template 2: ctx.to_prompt(refine=True)  [1 LLM call — sequential]
      → template 3: ctx.to_prompt(refine=True)  [1 LLM call — sequential]
      → compose()                                [1 LLM call — sequential]

Total: 2 + 3 + 1 = 6 sequential LLM calls for a 3-template smart_prompt()
Wall time at 2s/call: ~12 seconds
With parallelization of template refine steps: ~2+1+2 = ~5-6 seconds
```

---

## 2. Research Foundations

### 2.1 Parallel LLM Calls Are Safe and Well-Studied

**ParallelPrompt (2025):** Identifies latent semantic parallelism in ~10% of real-world prompts. Decomposed parallel execution achieves **up to 5× latency speedups** on comprehension, translation, and comparative analysis tasks with minimal quality degradation.  
*arxiv pending; presented at major venues.*

**ParaThinker (2025):** Native parallel thinking — LLMs generate multiple diverse reasoning paths simultaneously rather than sequentially. Shows **+12.3% accuracy for 1.5B models** and **+7.5% for 7B models** with only 7.1% latency overhead when running 8 parallel paths.  
*arxiv 2509.04475*

**Key takeaway for us:** Our 3 template refinement calls in `compose_from_templates()` are **semantically independent** (each refines a different template with the same question). This is the canonical case for parallelization — and the research shows it works.

### 2.2 asyncio Is Definitively Better Than ThreadPoolExecutor for LLM Calls

**TechFrontier (2026-02), Unite.ai:** For I/O-bound LLM API calls, `asyncio` is the preferred approach. ThreadPoolExecutor causes CPU saturation and context-switching overhead at scale. LangChain's own fallback: when no native async is available, they wrap sync calls in asyncio's thread pool — they treat ThreadPoolExecutor as a fallback, not a first choice.

**LiteLLM provides `acompletion()` natively.** We use only `litellm.completion()`. Adding `agenerate()` to `LiteLLMProvider` is a direct, low-risk translation:
```python
async def agenerate(self, context, **kwargs) -> ProviderResponse:
    response = await litellm.acompletion(...)
    return ProviderResponse(...)
```

### 2.3 Multi-Perspective Template Execution Improves Output Quality

**Prompt Sketching (ICML 2024):** LLMs predicting multiple template variables simultaneously rather than sequentially outperforms chain-of-thought on **7 of 8 benchmarking tasks**. Parallel template application, then synthesis, is a research-validated pattern.

**Our own 85 patterns:** The Template Integrator's core premise is already validated — fusing perspectives from multiple templates produces richer outputs. The question is whether executing them and then integrating (instead of just merging metadata) produces even richer outputs. ParaThinker's results suggest yes.

### 2.4 Intermediate Summarization Improves Chain Quality

**RAPTOR (2024):** Hierarchical recursive summarization. Each layer summarizes into a denser representation, reducing token count while preserving key information. Tested on multi-hop QA tasks.

**Our own summarization research** (`SUMMARIZATION_COGNITIVE_TEMPLATE_RESEARCH.md`): Kintsch construction-integration + Van Dijk macro-operators + ARC coverage. The faithfulness verification step prevents information loss.

**Direct application:** In chain execution, each step output is passed raw to the next. For a 3-step chain, step 1's output (2,000 tokens) → step 2's input. Summarizing step 1's output before step 2 reduces context noise and focuses the next step. Our own research backs this.

---

## 3. Honest Assessment — What Will Actually Help

### Definitely Do

| Optimization | Why It Directly Serves Our Vision |
|-------------|-----------------------------------|
| **Parallel template refinement in `compose_from_templates()`** | Tier 2 (`smart_prompt`) is our "balanced cost/quality" tier — it needs to be fast enough to use. 12s is too slow for production. 5s is viable. |
| **`agenerate()` on LiteLLMProvider + `aexecute()` on Context** | Unlocks everything else. Low risk because litellm.acompletion() exists. Required for any async pattern. |
| **Parallel raw vs template in `context_amplification.py`** | CAI measurement is our differentiator. Making it 2× faster directly improves developer experience. |
| **Summarization between chain steps (optional flag)** | Our summarization research is done. Connecting it to chain execution realizes the research investment. |

### Do If Time Permits

| Optimization | Caveat |
|-------------|--------|
| **"Parallel Lens" mode in Template Integrator** | Higher cost (7 calls vs 1). But aligned with "Best of All Worlds" tagline. Should be opt-in with explicit cost warning. |
| **Parallel question_analyzer + orchestration** | Small gain (saves ~2s). Question_analyzer output feeds orchestration prompt, so not fully parallelizable unless we restructure the prompt. |

### Do Not Do (Yet)

| Item | Reason |
|------|--------|
| Rewrite BatchProcessor to use asyncio | BatchProcessor already works for the use cases it serves. Replace only if we add async context throughout. |
| LiteLLM `batch_completion` for template loop | Requires reformatting messages per template; adds complexity. ThreadPoolExecutor or asyncio is simpler. |

---

## 4. Implementation Plan

### Phase 1: Foundation — Async Provider + Context (2–3 days)

These are prerequisites for everything else and have the lowest risk.

**4.1 `providers/litellm_provider.py` — Add `agenerate()`**
```python
async def agenerate(
    self,
    context: "Context",
    user: str | None = None,
    model: str | None = None,
    temperature: float = 0.7,
    max_tokens: int | None = None,
    **kwargs: Any,
) -> ProviderResponse:
    """Async version using litellm.acompletion()."""
    model = model or self.default_model
    litellm_model = _litellm_model_name(self._provider, model)
    messages = self._build_messages(context, user)
    call_kwargs = self._build_call_kwargs(litellm_model, messages, temperature, max_tokens, **kwargs)

    response = await litellm.acompletion(**call_kwargs)
    return self._parse_response(response, model)
```

**4.2 `providers/base.py` — Add abstract `agenerate()`**
```python
@abstractmethod
async def agenerate(self, context: "Context", **kwargs) -> ProviderResponse: ...
```

**4.3 `core.py` — Add `Context.aexecute()`**
```python
async def aexecute(self, provider: str = "openai", **kwargs) -> Any:
    """Async execution via provider.agenerate()."""
    from .providers import get_provider
    api_key = kwargs.pop("api_key", None)
    provider_instance = get_provider(provider, api_key=api_key)
    return await provider_instance.agenerate(self, **kwargs)
```

**Research basis:** LiteLLM acompletion docs; Python asyncio best practices.

---

### Phase 2: Parallel Template Refinement (1 day)

**The #1 bottleneck. In `prompt_composer.py`, lines 265-279.**

**Current (sequential):**
```python
for name in template_names:
    ctx = klass().build_context(**params)
    prompt = ctx.to_prompt(refine=refine, provider=provider, model=model)
    prompts.append(prompt)
```

**Proposed (parallel via asyncio):**
```python
import asyncio

async def _refine_one(name, question, provider, model) -> tuple[str, str]:
    klass = get_pattern_class(name, include_enterprise=self.include_enterprise)
    reg = PATTERN_BUILD_CONTEXT_REGISTRY.get(name, ("input", {}))
    primary_key, defaults = reg
    params = {**defaults, primary_key: question}
    ctx = klass().build_context(**params)
    if refine:
        prompt = await ctx.aexecute(...)  # Use new async path
    else:
        prompt = ctx.to_prompt(refine=False)
    return name, prompt

results = await asyncio.gather(*[_refine_one(n, ...) for n in template_names])
```

**Immediate fallback (ThreadPoolExecutor, no async stack needed):**
```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def _refine_one(name):
    klass = get_pattern_class(name, include_enterprise=self.include_enterprise)
    ...
    return name, ctx.to_prompt(refine=refine, provider=provider, model=model)

with ThreadPoolExecutor(max_workers=min(len(template_names), 5)) as ex:
    futures = {ex.submit(_refine_one, n): n for n in template_names}
    name_to_prompt = {}
    for future in as_completed(futures):
        name, prompt = future.result()
        name_to_prompt[name] = prompt

# Preserve original order
prompts = [name_to_prompt[n] for n in valid_names]
```

**Expected gain:** 3 templates × ~2s = 6s sequential → ~2s parallel (3× improvement). Direct improvement to Tier 2 wall time.

**Research basis:** ParallelPrompt (5× speedup), asyncio > ThreadPoolExecutor for LLM I/O (TechFrontier 2026).

---

### Phase 3: Parallel CAI Measurement (0.5 days)

**In `context_amplification.py`, lines 94–95:**
```python
# Current — sequential
raw_output = self._execute_raw(question, **exec_kwargs)
templated_output = self._execute_template(question, template_name, **exec_kwargs)

# Proposed — parallel
raw_output, templated_output = await asyncio.gather(
    self._aexecute_raw(question, **exec_kwargs),
    self._aexecute_template(question, template_name, **exec_kwargs),
)
```

**Why this matters:** CAI is our key differentiator. Developers use it to prove value. Making it 2× faster encourages more measurement. Aligns with our goal of "measurable quality."

---

### Phase 4: Summarization Between Chain Steps (3–5 days)

**Optional flag `summarize_between_steps=True` in chain execution.**

The chain executor (currently in pattern_suggester.py smart_execute or wherever chain steps are executed) would:
1. Execute step N → get output
2. Run `build_summarization_context(text=output, goal="preserve key findings for next analysis step")` → execute
3. Pass summary as input to step N+1

**Implementation sketch:**
```python
def execute_chain_with_summarization(chain, question, provider, summarize=False):
    prev_output = question
    for name in chain:
        klass = get_pattern_class(name)
        ctx = klass().build_context(**{primary_key: prev_output})
        result = ctx.execute(provider=provider)
        prev_output = result.response

        if summarize and name != chain[-1]:
            from docs.examples.summarization_custom_template import build_summarization_context
            sum_ctx = build_summarization_context(
                text=prev_output,
                goal="Preserve key findings for next analysis step",
                target_length="brief",
            )
            sum_result = sum_ctx.execute(provider=provider)
            prev_output = sum_result.response
    return prev_output
```

**Research basis:** RAPTOR hierarchical compression; our own summarization research (SUMMARIZATION_COGNITIVE_TEMPLATE_RESEARCH.md); Kintsch macro-operators for faithful condensation.

---

### Phase 5: "Parallel Lens" Mode (Optional, Post-Phase 1–4)

**New method: `TemplateIntegratorAgent.parallel_lens_integrate()`**

Executes 3 templates fully, summarizes each, then integrates:

```
Step 1: Execute template A, B, C in parallel  (3 LLM calls, concurrent)
Step 2: Summarize each output (optional, 3 LLM calls, concurrent)
Step 3: Integrate the 3 (summaries or raw) into one (1 LLM call)
```

**Trade-off:** 3+1 = 4 calls (no summarize) or 3+3+1 = 7 calls (with summarize) vs. current 1 call.

**When to use:** When user wants maximum perspective richness, not cost efficiency. Explicit opt-in with cost estimate shown before execution.

**Research basis:** ParaThinker (+7.5–12.3% accuracy from parallel reasoning paths); Prompt Sketching (multi-template outperforms CoT on 7/8 tasks).

---

## 5. Priority Summary

| Phase | What | Effort | Impact | Aligns With |
|-------|------|--------|--------|-------------|
| 1 | Async provider layer | 2–3 days | Foundational | All tiers |
| 2 | Parallel template refinement | 1 day | 3× Tier 2 speedup | Tier 2 cost/quality balance |
| 3 | Parallel CAI measurement | 0.5 day | 2× faster measurement | CAI differentiator |
| 4 | Summarization in chain steps | 3–5 days | Context quality in Tier 3 | Tier 3 max quality |
| 5 | Parallel Lens mode | 4–6 days | Richer multi-perspective | "Best of All Worlds" |

---

## 6. What Each Fix Does for Our Vision

**Vision: Universal Context Transformation Engine — measurable quality, universal portability, automatic intelligence.**

| Fix | Vision dimension |
|-----|-----------------|
| Async provider layer | **Automatic intelligence** — enables concurrent pattern execution; required for any modern orchestration |
| Parallel template refinement | **Cost/quality tradeoff** — Tier 2 needs to be fast enough to be chosen over Tier 3; currently it's arguably slower than just doing Tier 3 |
| Parallel CAI measurement | **Measurable quality** — CAI is THE differentiator; faster measurement = more usage |
| Summarization in chains | **Research-backed quality** — directly applies our summarization research investment to the chain execution path |
| Parallel Lens mode | **"Best of All Worlds" tagline** — executing templates, not just reading metadata, makes this claim literal |

---

## 7. References

### Codebase (Exact Files)
- `src/mycontext/intelligence/prompt_composer.py` — lines 265–279 (sequential refine loop)
- `src/mycontext/intelligence/context_amplification.py` — lines 94–95 (sequential raw/template)
- `src/mycontext/providers/litellm_provider.py` — sync only, litellm.acompletion available
- `src/mycontext/utils/batch.py` — ThreadPoolExecutor unused by intelligence layer
- `src/mycontext/core.py` — no aexecute()

### Research
- ParallelPrompt (2025): 5× speedup from semantic parallel decomposition
- ParaThinker (arxiv 2509.04475): +7.5–12.3% accuracy from parallel reasoning paths
- Prompt Sketching (ICML 2024): Multi-template outperforms CoT on 7/8 tasks
- Asyncio for LLM I/O: TechFrontier (2026-02), Unite.ai best practices
- RAPTOR: Hierarchical recursive summarization for chain compression
- Our own: docs/SUMMARIZATION_COGNITIVE_TEMPLATE_RESEARCH.md

### Internal Docs
- docs/EXECUTIVE_SUMMARY_CAPABILITIES.md — Three-tier execution targets
- docs/COGNITIVE_PATTERNS_RESEARCH_FOUNDATIONS.md — Research methodology
- docs/BRAINSTORM_NEXT_FRONTIERS.md — Product roadmap
