# Changelog

All notable changes to mycontext-ai are documented here.  
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).  
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Added

- **AI-Native Requirements Guidebook** — 103-page, 6-chapter PDF guidebook on writing requirements for AI agents (GRADED framework, golden trajectories, rubric-based eval, Requirements-as-Code) now available at `/guidebooks` on the web app.

---

## [0.14.0] — 2026-06-20

### Added

- **LLM-native Requirements-as-Code rebuild** — every RaC generator (`assess`, `product`, `technical`, `validate`, `trace`, `project`) is fully LLM-driven; there is no offline/deterministic skeleton. A Pydantic structured-output contract (`mycontext.rac.schema`) enforces typed-ID grammar and referential integrity with a self-repair loop.
- **`assess()` / `IntakeBrief`** — Step 0 intent assessment: natural language or `.txt`/`.md` → structured brief with system name, task types, must-never lines, tools, stakeholders, and open questions.
- **`mycontext rac intake`** — CLI subcommand for intent assessment (`--format md|json`).
- **`normalize_product()` / `normalize_technical()`** — mechanical fixes for common LLM structural mistakes (rubric criteria as sibling keys, empty gates, string open_questions, assumptions in meta).
- **Two-pass technical generation** — 24 Fable sections authored in two focused LLM calls to avoid truncation; `technical()` accepts product specs as dict or YAML string.
- **Expanded RaC documentation** — Docusaurus pages for CLI reference, API reference, and overview updated to reflect the LLM-native pipeline.

### Changed

- **`product()` / `technical()`** — removed `execute` flag; LLM is always required. Meta fields (`system_name`, `kind`, `intent`) are force-set from the intake brief / product spec so LLM placeholders never survive.
- **`complete_json()`** — default `max_tokens=None` so the provider controls output length (prevents truncated specs).
- **`OpenQuestion.id`** — optional with auto-assignment (`OQ-01`, …) during normalization.
- **`validate()`** — combines structural contract checks with an optional LLM quality critique (`llm=True` by default).
- **`trace()`** — LLM-driven coverage/drift report with optional unified diff analysis.
- **README (PyPI landing page)** — Requirements-as-Code added to Core Strengths #28, At a Glance table, How It Works diagram, and CLI section.

### Removed

- Deterministic RaC authoring (`fill.py`, `diffparse.py`, regex-based generation).
- Deprecated APIs: `parse_intent`, `Intake`, `RequirementsArchitect`, `TechnicalArchitect`, `complete()`, `draft_requirements`, `RequirementsAuthor`, `architect()` tier shim.
- `--execute` flag from all `mycontext rac` CLI commands.

### Fixed

- `technical()` `AttributeError` when `product` was passed as a YAML string.
- `_repair()` `IndexError` in technical spec self-repair loop on certain error message shapes.
- Empty product/technical sections from LLM truncation — raised as `RuntimeError` instead of silently emitting unusable specs.
- `open_questions` ValidationError when LLM returned bare strings instead of dicts with IDs.

---

### Added

- **Requirements Architect** (`mycontext.rac`) — turn a plain-English intent into a complete, reviewable specification:
  - `product(text, *, execute=False, provider, model)` — generates a **product-requirements** spec (the *what & why*): eval-first tasks, rubrics, an action risk matrix, a safety pre-mortem, datasets, baselines, release gates, and monitoring, with typed IDs. Gaps never block generation — each becomes a non-blocking `open_questions` entry plus an inline `TODO(OQ-n)` marker.
  - `technical(text=None, *, product=None, frontier=False, execute=False, ...)` — generates a **technical-requirements** spec (the *how*): architecture, guardrails, tools, cost, deployment, observability, security (OWASP agentic), and failure behavior. Every control carries a `serves:` list linking it to the product requirement it implements.
  - `trace(product, technical, diff=None)` — deterministic coverage/drift check: uncovered risk-bearing requirements, orphan `serves:` references, and code-diff impact (flags forbidden-tool usage). `format_report()` renders it as markdown.
  - `project(doc, to=...)` — render a spec to `AGENTS.md`, `CLAUDE.md`, Cursor `.mdc`, GitHub Spec Kit, AWS Kiro (EARS), or an ADR.
  - `validate(doc)` — structural lint for product and technical specs.
  - `parse_intent(text)` / `Intake` — offline intent parsing (name, kind, must-never lines, volume, constraints).
- **Cognitive-pattern grounding for `execute=True`** — `product()`/`technical()` now run a curated set of cognitive patterns over the intent and feed their analyses to the LLM fill pass, so answers are grounded in real reasoning (task decomposition, rubric design, pre-mortem, architecture trade-offs). The spec keeps a clean `meta.informed_by` provenance map.
  - `analyze(text, *, kind="product"|"technical", provider, model)` and `format_brief(notes)` — read or render the pattern brief directly.
  - `complete(doc, *, provider, model, extra_context=None)` — fill an existing draft's open questions with an LLM.
- **Provider-aware default models** (`mycontext.rac.models.resolve_model`) — when `model` is omitted, RaC picks a provider-appropriate default (`openai` → `gpt-4o-mini`, `anthropic` → `claude-3-5-haiku-latest`, `gemini`/`google` → `gemini-1.5-flash`) and raises a clear error for providers with no built-in default instead of silently sending an OpenAI model id.
- **`mycontext rac` CLI** — `product`, `technical`, `analyze`, `trace`, `validate`, and `project` subcommands, with `--from`, `--out`, `--execute`, `--provider`, `--model`, `--from-product`, `--frontier`, `--diff`, and `--to` flags. `trace` exits non-zero on detected drift (CI-friendly).
- **Documentation** — a comprehensive **Requirements-as-Code** docs category (overview, a non-technical guide for business teams, deep dives on `product`/`technical`/`trace`/`validate`/grounding/projections, a CLI reference, and an API reference).

### Notes

- All Requirements-as-Code generation is offline and deterministic by default; only `execute=True` / `analyze` contact an LLM, and only through your own provider/key.
- The original authoring + scoring bridge (`draft_requirements`, `RequirementsAuthor`, `score_output`) is retained for backwards compatibility.

---

## [0.12.0] — 2026-06-13

### Changed

- **All 88 cognitive patterns are now open source.** Every pattern — core and advanced — ships in the PyPI wheel and runs offline with your own LLM key. The `templates/free/` and `templates/enterprise/` folders are now taxonomy only; both are packaged. The wheel/sdist no longer exclude `templates/enterprise`, and the Dockerfile no longer strips them.
- **License tiers removed end to end** — SDK, web app (FastAPI), React frontend, and database. The `include_enterprise` parameter is now a no-op accepted only for backwards compatibility (all patterns are always available).

### Added

- **`mycontext` CLI** — `mycontext list`, `mycontext run <pattern> [--generic|--execute]`, `mycontext skills export <name|all> [--plugin]`, and `mycontext mcp`. Offline-first; only `run --execute` contacts an LLM (with your own key).
- **Skills export** — emit progressive-disclosure `SKILL.md` packages (Tier-1 frontmatter, Tier-2 body with pre-authored prompt + SDK scaffold, Tier-3 `references/`), or a Claude Code / Cowork plugin directory.
- **Local MCP server** (`mycontext mcp`, optional `mcp` extra) — a stdio FastMCP server exposing `suggest_patterns`, `transform`, and `score_output`. Local-only, $0.
- **Requirements-as-Code authoring + scoring** (`mycontext.rac`) — drafts a `requirements.yaml` (task taxonomy, rubrics, action risk matrix, pre-mortem) from cognitive patterns and scores outputs via `OutputEvaluator`. Authoring and scoring only — no compiler, CI gate executor, or HITL/budget runtime.

### Deprecated

- `mycontext.activate_license`, `deactivate_license`, `get_license_key`, and `is_enterprise_active` are now no-op shims that emit `DeprecationWarning` and will be removed in a future release.

### Fixed

- `execute_service.smart_execute` now accepts and forwards `quality` overrides to the SDK instead of raising `TypeError`.

### Removed

- Web app license router, license-generation CLI, the `LicenseKey` model, and the `User.enterprise_license` column (Alembic migration `b1c2d3e4f5a6` drops the table and column). Dead code: `CategoryFilter.jsx`, the synchronous `execute_context`, and orphaned `SkillSelector`/RAG tests.

### Migration

- Delete any `activate_license(...)` / `is_enterprise_active()` calls and drop the `include_enterprise` argument — all 88 patterns are always available.
- Apply the database migration: `alembic upgrade head` (back up first; it drops `license_keys` and `users.enterprise_license`).

---

## [0.11.0] — 2026-03-31

### Added

- **Quality Controls on `Constraints`** — Five new optional fields auto-suggested by `PromptArchitect` and overridable by the user:
  - `verbosity: "minimal" | "standard" | "detailed"` — output detail level, auto-inferred from task complexity
  - `communication_posture: "direct" | "collaborative" | "educational"` — interaction tone, auto-inferred from audience
  - `answer_first: bool` — when `True`, the LLM states its conclusion before supporting reasoning
  - `forbidden_phrases: list[str]` — phrases the LLM must never use, extending the built-in anti-boilerplate list
  - `self_check: list[str]` — domain-specific verification questions the LLM must confirm before finalizing
  All five fields render into the prompt via `Constraints.render()` and are scored by `QualityMetrics` and `OutputEvaluator`.

- **`PromptArchitect` auto-suggestion** — `build()` and `improve()` now instruct the LLM to infer all 5 quality control fields from the task description. The JSON schema, inference instructions, and per-section upgrade hints are updated. `_json_to_context()` parses and validates the new fields from the LLM response and populates `Constraints` accordingly.

- **Template self-check defaults** — All 16 free templates now set domain-specific `self_check` defaults in `build_context()` via the new `Pattern._apply_default_self_check()` helper. User-provided values are never overwritten.

- **Objectivity rules** — Six evaluative templates (RiskAssessor, ConflictResolver, HypothesisGenerator, ScenarioPlanner, DataAnalyzer, SocraticQuestioner) now include objectivity-enforcing rules in `Guidance.rules`.

- **Few-shot examples** — Ten templates now include curated good-output examples in `Context.examples` for better LLM calibration.

- **Fragment library** (`mycontext.fragments`) — New module with ~12 reusable quality-enhancing `Fragment` objects (`anti_fluff`, `answer_first_fragment`, `objectivity`, `self_check_analysis`, `structured_json`, `grounding_strict`, etc.). Each fragment can be applied to any `Context` to merge constraints and guidance rules. Designed for Blueprint composition.

- **Web app quality controls** — `SmartExecutePanel` now exposes an "Output Style" section with verbosity dropdown, "Answer first" checkbox, and "Self-verify" checkbox. Values are sent as `quality` overrides to the API and applied to the LLM-generated context.

### Changed

- **`TransformationEngine.transform()`** — Auto-sets `verbosity` on the resulting `Context.constraints` based on the complexity assessment (`SIMPLE` → `minimal`, `MODERATE` → `standard`, `COMPLEX`/`HIGHLY_COMPLEX` → `detailed`) when not already set.

- **`OutputEvaluator._score_register_fit()`** — Now checks user-defined `forbidden_phrases` from `context.constraints` and penalizes the score when found in the output.

- **`QualityMetrics._detect_quality_issues()`** — Gives positive score credit when the assembled `Context` includes `self_check`, `verbosity`, or `forbidden_phrases`.

- **`Pattern` base class** — Added `_apply_default_self_check(ctx, defaults)` static method for templates to set `self_check` defaults without overwriting user values.

---

## [0.10.2] — 2026-03-28

### Added

- **`PromptArchitect.build(reasoning_strategies=...)`** — New parameter that lets callers pin the thinking strategy explicitly instead of relying on LLM inference. Accepts a list of atomic slugs (e.g. `["step_by_step", "verify"]`) or a named archetype (e.g. `["deliberative"]`). When supplied, the caller's value overrides whatever the LLM inferred from the task description. Valid atomic slugs: `step_by_step`, `multiple_angles`, `verify`, `explain_simply`, `creative`. Valid archetypes: `analytical`, `deliberative`, `explanatory`, `creative`, `high_stakes`.

### Fixed

- **`PromptArchitect.build()`** — Passing an unknown keyword argument (e.g. `THINKING_STRATEGIES=`) no longer silently flows into `ctx.execute()` with no effect; callers should use the new `reasoning_strategies=` parameter.

---

## [0.10.1] — 2026-03-28

### Fixed

- **`PromptArchitect`** — Reasoning strategies are no longer injected into the `RULES` section. They now render as a dedicated **`ANALYTICAL AND REPORTING APPROACH`** section placed immediately before `YOUR TASK` (recency zone) for stronger recall in long-context prompts (Li et al. 2023).
- **`PromptArchitect`** — `examples` from the LLM JSON are now mapped to `Context.examples` as `{"input", "output"}` dicts, rendering as a proper `## EXAMPLES` section in the middle zone (⑤). They were previously baked as raw text into `Directive.content` (inside `YOUR TASK`), causing format/output-contract mismatches.
- **`PromptArchitect`** — Guard-rails rescue: items that look like grounding rules (`"Every claim must be grounded…"`) are automatically moved from `guard_rails` into `rules` where they belong, so the `GUARD RAILS` section only contains true `Omit X` exclusions.
- **`PromptArchitect`** — LLM JSON schema hints for `examples` updated to `{input, output}` dict format, and `guard_rails` hint tightened to `Omit X`-only statements with an explicit CRITICAL note.
- **`Context._assemble_research_flow`** — Prompt section order updated: `⑤ Examples → ⑥ Knowledge → ⑦ Output Format → ⑧ Guard Rails → ⑧.5 Reasoning → ⑨ Task`. Reasoning was previously at ⑤ (middle zone) and got lost in long-context prompts.

### Added

- **`PromptArchitect(render_for=...)`** — New constructor parameter (alias for `assembly_provider_hint`) to set the target provider for output formatting independently of the LLM call provider. Example: `PromptArchitect(provider="openai", render_for="anthropic")` calls OpenAI but emits XML-delimited output for Anthropic consumption.
- **`ArchitectResult.metadata["target_provider"]`** — Reports the resolved output format provider (`openai` / `anthropic` / `gemini` / `generic`) on every `build()` and `improve()` result.

---

## [0.10.0] — 2026-03-25

### Added

- **`suggest_routes()`** (`mycontext.intelligence.suggest_routes`) — LLM-powered multi-route analysis: decomposes a question into differentiated template pipelines with **agent-level steps** (`RouteStep`: `template`, `agent_role`, `receives`, `produces`, `params`). Use it to plan LangGraph / CrewAI-style multi-agent flows. Exported types: `RouteAnalysis`, `AnalysisRoute`, `RouteStep`.
- **Catalog `output_type`** — Every entry in `ENRICHED_CATALOG` includes an `output_type` string; `ENRICHED_CATALOG_TEXT` now shows a **PRODUCES:** line per template for better LLM routing.

### Changed

- **`suggest_patterns(mode="llm"|"hybrid")`** — Tries `suggest_routes(max_routes=1)` first and maps the best route into `SuggestionResult`; falls back to the legacy `_suggest_with_llm` path on failure.
- **`build_workflow_chain()`** — **Deprecated** (emits `DeprecationWarning`). Prefer `suggest_routes()`. When delegation succeeds, builds `WorkflowChainResult` from the first route’s steps.
- **`TemplateIntegratorAgent`** — Default integration model is **`gpt-4o`** (was `gpt-4o-mini`). Template fingerprints use each pattern’s **`GENERIC_PROMPT`** instead of heuristic directive line extraction. Instructor path forwards **`max_tokens`**, **`temperature`**, **`top_p`** when provided.
- **`IntegrationResult`** — New field **`integration_rationale`**. **`integrated_context`** / **`raw_llm_response`** are no longer sentinel strings on the instructor path; they contain reconstructed readable text.

---

## [0.9.0] — 2026-03-24

### Added

- **`TaskContract`** (`mycontext.foundation.TaskContract`, also exported from `mycontext`) — L0 metadata model: `domain`, `audience`, `genre`, `grounding`, `metaphor`. Use it to declare task type and evidential rules in one place; it renders as the **L0 — TASK CONTRACT** table at the top of research-flow prompts when `research_flow=True`.
- **`Context.task_contract`** — First-class field for L0. If unset, legacy `metadata["l0"]` dicts are still read for backward compatibility.
- **`PromptArchitect.improve()` / `build()`** — Optional `user_message` and `task_contract` arguments so the rewriter sees the real user task and L0 dimensions; improves alignment between `output_contract` and expected format (e.g. markdown brief vs JSON).
- **`PromptArchitect`** — `_GENRE_FORMAT_HINTS` and post-processing in `_json_to_context()` reduce genre/format mismatches when `task_contract.genre` is set.
- **`OutputEvaluator`** — Optional `dimension_weights: dict[str, float] | None` in the constructor; keys are dimension value strings (e.g. `instruction_following`). Custom weights apply to heuristic scoring and to the weighted overall when the LLM judge returns per-dimension scores.

### Changed

- **`OutputEvaluator`** — Overall score in heuristic and LLM paths uses custom weights when provided; otherwise unchanged defaults.

---

## [0.8.1] — 2026-03-20

### Changed

- **`PromptArchitect`** (`improve` / `build`) — Internal rewriting LLM is now instructed with distilled linguistic rules from the project prompt-engineering guidebook (imperative framing, positive redirects, binding modals, testable specificity, scope bounding, “Return ONLY” output contracts, recency-zone task placement). Per-section upgrade hints were expanded with concrete BAD/GOOD patterns and formulas for role, goal, rules, style, reasoning strategies, examples, output contract, guard rails, and task.
- **`PromptArchitect`** — Contexts produced from LLM JSON now use `research_flow=True` and a resolved `provider_hint` so assembled prompts match the 9-section research-backed renderer and provider-specific formatting (when the architect’s provider maps to OpenAI, Anthropic, or Gemini).

---

## [Unreleased] — Web app (planned; was 0.9.0 draft)

### Added

- **Pit Stop** — Prompt improver integrated into the Pick Your Adventure panel alongside Take the Wheel and Let AI Drive. Three equal path cards with amber styling for the tune-up flow.
- **Model dropdown** in Pit Stop — Provider and model selectors with choices from `MODEL_CATALOG` (OpenAI, Anthropic, Google models).

### Changed

- **Let AI Drive layout** — Copilot panel fixed to the right edge of the viewport instead of inline flex. Wizard gets full width like Take the Wheel; copilot no longer crowds the prompt panel.
- **`POST /api/architect/parse`** — No longer requires authentication. Analyze (Free) works without login; heuristic section detection only, no LLM call.
- **Output format handling** — `build-preview`, `build`, and `execute` endpoints no longer append a duplicate OUTPUT FORMAT block when the assembled prompt already contains one. Fixes double "OUTPUT FORMAT" and empty `{}` schema at the end.
- **Guidance rendering** — Role and goal text no longer duplicated when user input already includes "You are" or "Your mission: ... — accomplish this fully." Prefixes/suffixes are stripped before wrapping.
- **Profile dropdown z-index** — Lowered copilot panel z-index (90) below header (100) so the profile dropdown is always visible when the copilot is open.

### Fixed

- Pit Stop provider/model dropdowns and blocks now visible (CSS uses `--text` and `--bg` instead of undefined `--text-primary` / `--bg-input`).
- Profile dropdown hidden behind copilot when Let AI Drive or FAB copilot was open — resolved by z-index hierarchy.

---

## [0.8.0] — 2026-03-18

### Added

- **`PromptArchitect`** (`mycontext.intelligence.PromptArchitect`) — Applies the 9-section prompt architecture to any raw prompt string. Three entry points:
  - `parse(prompt)` — heuristic section detection, no LLM call
  - `build(task)` — constructs a complete 9-section prompt from a plain task description (1 LLM call)
  - `improve(prompt)` — parse + score + rewrite weak/missing sections + score again + section-level diff (1 LLM call)
  - Returns `ArchitectResult` with `improved_context`, `improved_prompt`, `before_score`, `after_score`, `score_delta`, `parsed`, and `diffs`

- **`GuidanceOptimizer`** (`mycontext.intelligence.GuidanceOptimizer`) — Audits and upgrades `Guidance` objects in SDK templates. Targets three weaknesses: suggestive modals (`should/try to/ideally` → `must/always/never`), vague directives (`be accurate` → specific testable criterion), and under-specified rules (< 5 words). Only weak rules are sent to the LLM — binding rules are kept exactly as written.
  - `audit(guidance)` — heuristic weakness detection, no LLM call. Returns `GuidanceAuditResult` with per-rule `RuleAudit` records and a `rule_strength_score`
  - `optimize(guidance)` — rewrites weak rules via LLM. Returns `OptimizedGuidance` with before/after scores and full audit trail

- **`eval_criteria`** (`mycontext.intelligence.eval_criteria`) — Pre-built LLM-judge rubrics for use with DeepEval's `GEval` metric. Ten criteria organized into five bundles (`data_analysis`, `reasoning`, `instruction_following`, `code_review`, `general`):
  - `EVIDENCE_CITATION`, `CAUSATION_DISCIPLINE`, `DATA_GAP_HONESTY`, `INSTRUCTION_ADHERENCE`, `ACTIONABILITY`, `REASONING_SOUNDNESS`, `STRUCTURE_COMPLIANCE`, `COGNITIVE_SCAFFOLDING_USE`, `CODE_REVIEW_SEVERITY_ACCURACY`, `CODE_REVIEW_ACTIONABILITY`
  - `get_criteria(bundle)` — retrieve a pre-assembled bundle
  - `to_deepeval_metrics(criteria)` — convert to `deepeval.metrics.GEval` objects

- **`OutputEvaluator` improvements** — `_score_actionability` now rewards explicit data-gap statements before applying hedge penalties; `_score_reasoning_depth` rewards explicit `Evidence:` labels. Both changes reduce false penalization of analytically rigorous outputs.

### Changed

- `QualityMetrics._evaluate_clarity` — added modal commitment ratio scoring: prompts with ≥60% binding modals (`must/shall/will/always/never`) receive a positive signal; prompts with <25% are flagged. Hedge density now also factors in `try to / if applicable / as needed`.

---

## [0.7.0] — 2026-03-11

### Added

- **`output_format` parameter on all templates** — Every template's `build_context()` and `execute()` now accepts an `output_format` argument that appends a format instruction to the assembled directive. 10 formats available:
  - Human formats: `"structured"` (default, no change), `"narrative"`, `"brief"`, `"actionable"`, `"slides"`, `"email"`, `"qa"`, `"checklist"`
  - Machine formats: `"json"`, `"table"` (auto-sets temperature to 0.0 for structured output)
  - Implemented at the `Pattern` base class level — all 87 templates inherit it automatically.

- **`mycontext.utils.format_directives`** — new public utility module exposing:
  - `get_format_directive(output_format)` — returns the format instruction string for appending to directives
  - `is_machine_format(output_format)` — returns `True` for `"json"` and `"table"` formats
  - `VALID_OUTPUT_FORMATS`, `HUMAN_OUTPUT_FORMATS`, `MACHINE_OUTPUT_FORMATS` — frozensets of valid format names

- **`QueryPlanner`** (enterprise) — Pre-retrieval query analysis template for RAG pipelines. Classifies, decomposes, rewrites (HyDE + step-back), and plans retrieval strategy before hitting the vector store. Complements `RagAnswerer`. Available via `mycontext.templates.enterprise.specialized.QueryPlanner`.

- **`CodeReviewer`** — completely reworked with a research-backed ORIENT→ANALYZE→ASSESS→RECOMMEND cognitive flow based on the Code Review as Decision-Making (CRDM) model (2026), Bacchelli & Bird (2013), and Google eng-practices. Focuses on 7 dimensions linters cannot catch (correctness, security, performance, design, resilience, testing, maintainability). Explicitly excludes style/formatting to avoid the low-value bikeshedding that accounts for 85% of review comments.

### Changed

- **`MemoryCompressor`** moved from free → enterprise tier. Available via `mycontext.templates.enterprise.specialized.MemoryCompressor`. Removed from `mycontext.templates.free.specialized`.

- **`RagAnswerer`** moved from free → enterprise tier. Available via `mycontext.templates.enterprise.specialized.RagAnswerer`. Removed from `mycontext.templates.free.specialized`.

- **Free tier** now ships 16 patterns (unchanged count — `MemoryCompressor` and `RagAnswerer` were already deprecated from free in 0.6.0 and are now formally removed).

- **Pattern catalog** (`mycontext.intelligence.pattern_catalog`) updated with enriched metadata (`when_to_use`, `use_cases`, `theme`) for all 87 patterns, and full keyword routing entries for `QueryPlanner`, `MemoryCompressor`, and `RagAnswerer`.

- **`Pattern.build_context()`** base method signature updated: `output_format: str = "structured"` added as a keyword argument. Raises `ValueError` for unrecognised format values.

- **`Pattern.execute()`** base method signature updated: `output_format: str = "structured"` added. Machine formats (`json`, `table`) automatically set `temperature=0.0` unless the caller overrides it.

### Migration

If you were importing `MemoryCompressor` or `RagAnswerer` from the free tier:

```python
# Before (0.6.x — these no longer exist in the free package)
from mycontext.templates.free.specialized import MemoryCompressor, RagAnswerer

# After (0.7.0 — enterprise tier, requires license)
from mycontext.templates.enterprise.specialized import MemoryCompressor, RagAnswerer
```

---

## [0.6.0] — 2026-02-28

### Added

- **`RagAnswerer`** (enterprise) — Grounded answer generation from retrieved context for RAG pipelines. Incorporates generation-side best practices from Chain-of-Note, Self-RAG, CRAG, and multi-granularity reasoning. Supports three tasks: `answer`, `summarize`, `synthesize`. Enforces citation, reduces hallucination, and preserves specific terminology.

- **`MemoryCompressor`** (enterprise) — Structured state extraction from conversations and documents for long-context agent memory. Extracts entities, decisions, constraints, and quantitative data instead of prose summaries. Three intents: `session` (full compression), `progressive` (incremental update), `context` (document compression). Research basis: SimpleMem, CDIC, RECOMP, Cognitive Load Theory.

- **`OutputEvaluator`** — 5-dimension LLM output quality scoring: Instruction Following, Reasoning Depth, Actionability, Structure Compliance, Cognitive Scaffolding. Available via `mycontext.intelligence.OutputEvaluator`.

- **`QualityMetrics`** — 7-dimension context quality scoring: Clarity, Completeness, Specificity, Relevance, Structure, Efficiency. Available via `mycontext.intelligence.QualityMetrics`.

### Changed

- **`DataAnalyzer`** now supports `intent` and `investment` parameters for controlling analysis scope and depth:
  - `intent`: `"executive"` | `"analyst"` | `"operations"` | `"summary"` | `"comprehensive"` (default) — controls which sections are produced.
  - `investment`: `"quick"` | `"standard"` (default) | `"thorough"` — controls depth and token budget.
  - Backward compatible: omitting both parameters gives the original full report behavior.

- Pattern count updated from 85 to 87 (16 free + 71 enterprise).

- **`SemanticCache`** test suite fixed — cache key now correctly includes the default user turn, matching the provider's internal key format.

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
