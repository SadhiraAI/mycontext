# Changelog

All notable changes to mycontext-ai are documented here.  
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).  
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [0.5.0] — 2026-02-24

### Added

- **`Context.aexecute(provider, **kwargs)`** — async counterpart to `execute()`. Uses `litellm.acompletion` under the hood so multiple contexts can run concurrently with `asyncio.gather()` without blocking the event loop. Drop-in replacement for `execute()` inside `async` functions and FastAPI route handlers.

- **`BaseProvider.agenerate(context, **kwargs)`** — async method on the base provider interface. Default implementation runs `generate()` in a thread-pool executor (safe fallback for any provider). `LiteLLMProvider` overrides this with a native `litellm.acompletion()` call for true non-blocking I/O.

- **`LiteLLMProvider.agenerate(context, **kwargs)`** — full async LLM call with cache, retry, and tracing parity with the sync `generate()` path. Supports `use_cache=True/False`, automatic exponential backoff, and emits a `litellm_agenerate` span to the execution tracer.

- **`Context.assemble_for_model(model, max_tokens)`** — token-budget-aware context assembly. Sections are included in priority order (directive → guidance → constraints → knowledge) and the lowest-priority section that would overflow is trimmed to fit. Guarantees the assembled string is `≤ max_tokens` tokens as measured by `tiktoken` for the target model. Pass `max_tokens=None` (default) for a transparent pass-through to `assemble()`.

- **`mycontext.intelligence.schemas`** — Pydantic v2 schemas for all three intelligence-layer LLM parsing sites:
  - `PatternSuggestionResponse` — typed, validated output for `suggest_patterns()` / `_suggest_with_llm()`; normalises snake_case names and enforces 1–5 selection limit.
  - `IntegrationResponse` — typed output for `TemplateIntegratorAgent._parse_result()`; fields: `role`, `rules`, `directive`, `output_requirements`, `integration_rationale`.
  - `ContextSpec` — typed output for `generate_context()` / `_parse_llm_json()`; auto-normalises invalid `thinking_strategy` values to `step_by_step`.
  - `parse_with_fallback(schema_cls, raw_text)` — helper that extracts JSON from LLM output (strips markdown fences, finds outermost `{}`) and validates it against any of the three schemas.
  - `get_instructor_client()` — returns an `instructor`-wrapped `litellm.completion` client when the optional `instructor` package is installed; returns `None` otherwise.
  - When `instructor` is installed (`pip install instructor`), all three parsing sites use structured JSON-mode output with automatic retry on validation failure (~98% parse success rate). Falls back to `parse_with_fallback` → original regex parser without `instructor`.

- **`app/services/execute_service.execute_context_async()`** — async version of `execute_context()` for the web application. The FastAPI `POST /api/execute` route now uses this, eliminating event-loop blocking during LLM calls.

### Changed

- `_suggest_with_llm` in `pattern_suggester.py` now instructs the LLM to respond as JSON when the instructor path is unavailable, then parses via `PatternSuggestionResponse` before falling back to regex.
- `TemplateIntegratorAgent._call_llm` and `_parse_result` now try `IntegrationResponse` Pydantic parse before falling back to the original regex parser. External interface (`IntegrationResult` dataclass) is unchanged.
- `generate_context` now tries the `instructor` structured-output path first, then falls back to `_parse_llm_json` → `ContextSpec` validation → legacy dict parse. External interface (`GeneratedContext`) is unchanged.
- `app/api/execute.py` `POST /api/execute` route now calls `await execute_service.execute_context_async()` instead of the synchronous `execute_context()`.

### Security / Quality

- All lint errors in the five new utility modules and three changed intelligence modules resolved (`ruff check` clean on all modified files).
- `raise ... from exc` added to `LiteLLMProvider.__init__` exception chain (`B904`).
- Unused imports (`Literal`, `model_validator`, `litellm`) removed from `schemas.py` and `pattern_suggester.py`.
- `collections.abc.Callable/Iterator` used instead of deprecated `typing.Callable/Iterator` in `tracing.py` (`UP035`).

---

## [0.4.1] — 2026-02-23

### Added

- **`generate_context(role, goal, task?, provider, model)`** — new intelligence layer function that takes a role and goal, calls an LLM, and returns a fully-populated `Context(research_flow=True)` with generated rules, style, expertise, thinking strategy, few-shot examples, output schema, and guard rails. No manual prompt engineering required. ([`intelligence/context_generator.py`](src/mycontext/intelligence/context_generator.py))
- **`GeneratedContext`** dataclass — result object wrapping the generated Context with `.context`, `.generation_meta`, `.assemble()`, `.execute()`, and `.to_context()` convenience methods.
- `generate_context` and `GeneratedContext` exported from `mycontext.intelligence` and the top-level `mycontext` package.
- **`Guidance.goal`** field — optional string that sets the objective for the interaction. Rendered after `role` in the assembled prompt. Appears in the `## GOAL` section when `research_flow=True`.
- **`Context.thinking_strategy`** field — injects a named reasoning approach into section ⑤ of the assembled prompt. Five strategies: `step_by_step` (Chain of Thought), `multiple_angles` (Tree of Thought), `verify` (Self-Reflection), `explain_simply` (Simplification), `creative` (Divergent Thinking).
- **`Context.examples`** field — `list[dict[str, str]]` of `{"input": ..., "output": ...}` few-shot demonstrations, auto-positioned in section ⑥ when `research_flow=True`.
- **`Context.research_flow`** flag (`bool`, default `False`) — when `True`, `assemble()` uses the 9-section research-backed ordering: Role → Goal → Rules → Style → Reasoning → Examples → Output Format → Guard Rails → Task.
- **`Context.to_prompt(refine, provider, model)`** — converts a Context to a reusable prompt string. Zero-cost (`refine=False`) or LLM-distilled (`refine=True`).
- **`Context.from_skill(path, task, **params)`** — classmethod to build a Context from a SKILL.md Agent Skill.
- 27 new unit tests for `generate_context` covering JSON parsing, spec-to-context conversion, mock LLM calls, error handling, and top-level import verification.

### Changed

- `Context.assemble()` now has two code paths: classic linear assembly (default) and research-backed 9-section assembly (`research_flow=True`). Both are backward-compatible — `research_flow` defaults to `False`.
- `Guidance` constructor now accepts `goal` as an optional field between `role` and `rules`.

### Documentation

- New page: `website/docs/foundations/research-flow.md` — "Prompt Assembly & Thinking Strategies". Covers the 9-section structure, each thinking strategy in depth with decision criteria and code examples.
- Updated `website/docs/foundations/context-object.md` — all new fields documented, thinking strategies table, few-shot examples section.
- Updated `website/docs/foundations/guidance.md` — `goal` field documented with render output example.
- Updated `website/docs/getting-started/core-concepts.md` — new "Prompt Assembly & Thinking Strategies" section.
- Updated `website/docs/getting-started/quickstart.md` — `research_flow` and `generate_context` usage examples.
- Updated `website/docs/api/overview.md` — corrected Guidance, Directive, Constraints constructors; new Context fields; `generate_context` added.
- Added `foundations/research-flow` to `sidebars.ts`.

---

## [0.4.0] — 2026-02-18

### Added

- 85 cognitive patterns (16 free, 69 enterprise) across analysis, reasoning, planning, decision-making, systems thinking, ethical reasoning, metacognition, and more.
- Quality Metrics — 6-dimension context scoring (clarity, completeness, specificity, relevance, structure, efficiency).
- Output Evaluator — 5-dimension LLM response scoring.
- Context Amplification Index (CAI) — quantitative template effectiveness measurement.
- Template Integrator Agent — intelligent multi-pattern fusion.
- Chain Orchestration Agent — auto-build multi-step reasoning workflows.
- Pattern Suggester — keyword, LLM, and hybrid pattern recommendation.
- Transformation Engine — one-call auto-transform from raw question to Context.
- Blueprint — multi-component context with token budget management.
- Agent Skills with quality gates.
- Template Benchmarking CLI.
- Generic Prompts — zero-cost compiled prompt artifacts.
- Prompt Compilation Pipeline — static, dynamic, and full tiers.
- Three-Tier Execution Model.
- 13 export formats (OpenAI, Anthropic, Gemini, LangChain, LlamaIndex, CrewAI, AutoGen, YAML, JSON, XML, Markdown, Messages, Dict).
- 7 framework integration helpers (LangChain, LlamaIndex, CrewAI, AutoGen, DSPy, Semantic Kernel, Google ADK).
- Built-in retry with exponential backoff.
- Enterprise license gating with `activate_license()`.

---

## Format

- **Added** — new features and capabilities
- **Changed** — changes to existing functionality
- **Deprecated** — features that will be removed in a future version
- **Removed** — features removed in this version
- **Fixed** — bug fixes
- **Security** — security patches
- **Documentation** — documentation-only changes
