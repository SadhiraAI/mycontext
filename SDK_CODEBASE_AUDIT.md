# mycontext SDK Codebase Audit (Revised)

**Date:** February 15, 2026
**Scope:** `src/mycontext/` -- full SDK source, every file read and verified
**Goal:** Identify what to keep, refactor, or remove before the next release

> **Corrections from v1:** The first audit incorrectly stated that `output_evaluator.py`
> and `template_integrator_agent.py` were missing -- both files exist. The `benchmarks/`
> directory is not empty (has YAML test cases). Several phantom dependencies were missed.
> This revision is line-number verified.

---

## Table of Contents

1. [Codebase Overview](#1-codebase-overview)
2. [CRITICAL -- Broken at Runtime](#2-critical----broken-at-runtime)
3. [Phantom Dependencies -- Installed But Never Used](#3-phantom-dependencies----installed-but-never-used)
4. [Superfluous -- Remove Candidates](#4-superfluous----remove-candidates)
5. [Refactor Candidates](#5-refactor-candidates)
6. [Deprecated / Incorrect Code](#6-deprecated--incorrect-code)
7. [Incomplete Implementations (TODO Stubs)](#7-incomplete-implementations-todo-stubs)
8. [Questionable -- Needs a Decision](#8-questionable----needs-a-decision)
9. [Solid -- Keep As-Is](#9-solid----keep-as-is)
10. [Dependency Audit](#10-dependency-audit)
11. [Template Inventory](#11-template-inventory)
12. [Recommended Action Plan](#12-recommended-action-plan)

---

## 1. Codebase Overview

### Verified File Counts and Line Counts

| Area | Files | Lines (verified) | Key Classes |
|------|-------|-------------------|-------------|
| core.py | 1 | 591 | Context |
| foundation/ | 4 | ~264 (guidance 86, directive 77, constraints 101) | Guidance, Directive, Constraints |
| structure/ | 3 | ~617 (pattern 337, blueprint 280) | Pattern, Blueprint |
| intelligence/ | 9 | ~4,361 | Engines, metrics, suggesters, evaluators, agents |
| intelligence/rag/ | 5 | ~386 | Chunkers, embedders, vector stores |
| templates/free/ | 46 files (39 templates + 7 __init__) | ~6,000+ | 39 Pattern subclasses |
| templates/enterprise/ | 57 files (46 templates + 11 __init__) | ~6,000+ | 46 Pattern subclasses |
| integrations/ | 2 | ~430 (helpers 398, __init__ 32) | 7 helper classes (incl GoogleADKHelper) |
| providers/ | 7 | ~1,135 (__init__ 102, base 91, mock 62, openai 213, anthropic 214, gemini 300, litellm 153) | 4 concrete + 1 meta-provider |
| skills/ | 6 | ~1,188 (skill 229, runner 205, selector 232, improvement 319, pattern_registry 161, __init__ 42) | Skill, SkillRunner, SkillSelector |
| utils/ | 8 | ~2,238 (structured_output 331, parsers 333, optimizers 340, batch 253, tracking 350, validators 229, cache 305, __init__ 97) | 15+ utility classes |
| knowledge/ | 3 | ~644 (session 259, archive 385) | Session, Archive, FileArchive, MemoryArchive |
| benchmarks/ | 6 | ~50 (__init__ 2 + 5 YAML test case files) | Benchmark test cases |
| license.py | 1 | 77 | activate_license, is_enterprise_active |
| licensing.py | 1 | 106 | activate_license, is_enterprise (ORPHANED) |
| benchmark_cli.py | 1 | 117 | CLI for template benchmarks |
| version.py | 1 | 5 | __version__ |
| __init__.py | 1 | 105 | Top-level exports |
| **Total** | **~160+** | **~24,000+** | |

### Intelligence Module Detail (9 files, verified)

| File | Lines | Status |
|------|-------|--------|
| quality_metrics.py | 822 | Solid |
| pattern_suggester.py | 689 | Works, needs refactor |
| transformation_engine.py | 547 | Works, has 3 TODOs |
| output_evaluator.py | 437 | Exists and works |
| chain_orchestration_agent.py | 342 | Works |
| context_amplification.py | 298 | Works, has dead method |
| template_benchmark.py | 195 | Works |
| template_integrator_agent.py | 292 | Works (uses LLM) |
| __init__.py | 76 | All imports verified |

---

## 2. CRITICAL -- Broken at Runtime

### 2.1 `licensing.py` is Completely Orphaned

**File:** `src/mycontext/licensing.py` (106 lines)
**Problem:** ZERO imports of this file anywhere in the codebase.

The SDK uses `license.py` (imported in `__init__.py` line 49). `licensing.py` is a completely separate, dead file with:
- Different function name: `is_enterprise()` vs `is_enterprise_active()`
- Different key format: `ENT-XXXX-XXXX-XXXX-XXXX` vs `MC-ENT-XXXX...`
- Different validation logic (regex pattern matching vs none)

**Risk:** Confuses developers. If someone imports from `licensing.py` thinking it's the right one, behavior will differ from the actual license system.

**Action:** Delete `licensing.py`, or merge its better validation (regex) into `license.py`.

### 2.2 `litellm_provider.py` Has Invalid Default Model Names

**File:** `src/mycontext/providers/litellm_provider.py` lines 42-43

```python
DEFAULT_MODELS = {
    "openai": "gpt-4.1-mini",       # <-- Not a real model
    "anthropic": "claude-haiku-4-5", # <-- Not a real model
    ...
}
```

Also line 61: `self.default_model = model or self.DEFAULT_MODELS.get(provider, "gpt-4.1-mini")`

These model names don't exist. Any user relying on defaults will get API errors. Should be `gpt-4o-mini` and `claude-3-5-haiku-20241022` (or whatever is current).

### 2.3 Pattern Count Mismatch in Marketing

**Actual code:** 39 free + 46 enterprise = 85 total
**pyproject.toml says:** "50 Free + 35 Enterprise"

The total (85) is correct, but the free/enterprise split is wrong. Either:
- A) 11 free patterns are missing from code, or
- B) The marketing copy needs updating to "39 Free + 46 Enterprise"

---

## 3. Phantom Dependencies -- Installed But Never Used

These are in `pyproject.toml` core `dependencies` (installed for EVERY user) but have **zero imports** in the entire `src/mycontext/` source tree:

| Dependency | In pyproject.toml | Imports Found | Verdict |
|------------|-------------------|---------------|---------|
| `structlog>=24.4.0` | Core dep (line 27) | **0** -- not imported anywhere | PHANTOM -- remove from core |
| `httpx>=0.27.2` | Core dep (line 28) | **0** -- not imported anywhere | PHANTOM -- remove from core |
| `jinja2>=3.1.4` | Core dep (line 25) | **0** -- not imported anywhere | PHANTOM -- remove from core |
| `openai>=1.54.0` | Core dep (line 29) | 3 files (core.py, providers/openai.py, rag/embedder.py) | SHOULD BE OPTIONAL -- only for execution |
| `tiktoken>=0.8.0` | Core dep (line 24) | 1 file (utils/optimizers.py line 9) | SHOULD BE OPTIONAL -- only for token counting |

**Impact:** Every `pip install mycontext-ai` forces users to download structlog, httpx, jinja2, openai, and tiktoken even though some are **literally never imported** and others are only used in optional features.

**Recommended minimal core deps:**
```toml
dependencies = [
    "pydantic>=2.9.0",
    "pyyaml>=6.0.2",
]
```

Everything else should move to optional extras.

---

## 4. Superfluous -- Remove Candidates

### 4.1 `intelligence/rag/` -- Full RAG Pipeline

**Files:** 5 (`__init__.py`, `chunker.py`, `embedder.py`, `retriever.py`, `vector_store.py`)
**Lines:** ~386
**Heavy deps pulled in:** chromadb, faiss-cpu, sentence-transformers

**What it does:** Chunks documents, generates embeddings, stores/retrieves vectors.

**Why remove:**

| Reason | Detail |
|--------|--------|
| Not core value | mycontext structures prompts. RAG is a retrieval problem. |
| Heavy deps | chromadb, faiss-cpu, sentence-transformers are large packages |
| Better alternatives | LangChain, LlamaIndex, Haystack do RAG far better with active ecosystems |
| Sufficient without it | `Context(knowledge=my_retriever.search("query"))` already works |
| Only 1 consumer | Only `skills/selector.py` uses it (line 17-18) |

**Downstream impact:** `SkillSelector` in `skills/selector.py` uses RAG for semantic skill selection -- needs simplification.

### 4.2 `knowledge/` -- Session and Archive

**Files:** 3 (`__init__.py`, `session.py`, `archive.py`)
**Lines:** ~644 (much more than the first audit estimated)

**What it does:** Session/Message conversation history, FileArchive/MemoryArchive for persistence.

**Why remove:**

| Reason | Detail |
|--------|--------|
| Not referenced by core | `core.py` and templates never use it |
| Incomplete | `archive.py` has two TODO stubs (lines 230, 269) |
| Every framework has this | LangChain, CrewAI, AutoGen all do conversation history |
| Exported but unused | Exported in `__init__.py` (lines 24-29) but no example/test uses them |

### 4.3 Dead Code in `structure/`

**`structure/pattern.py` (lines ~278-336):**
- `CODE_REVIEW_PATTERN` and `DECISION_MATRIX_PATTERN` -- hardcoded example Pattern instances
- Not imported, not used anywhere

**`structure/blueprint.py` (lines ~254-279):**
- `SIMPLE_ASSISTANT_BLUEPRINT` and `RESEARCH_ASSISTANT_BLUEPRINT` -- hardcoded examples
- Not imported, not used anywhere

### 4.4 `licensing.py` (Redundant)

See [2.1](#21-licensingpy-is-completely-orphaned). This is a dead file -- `license.py` is the one the SDK actually uses.

### 4.5 Unused `pyproject.toml` Optional Extras

Several extras declare dependencies for features that have **no corresponding code** in the SDK:

| Extra | Dependencies | Code Using It? |
|-------|-------------|----------------|
| `redis` | `redis>=5.2.0` | No Redis code in SDK |
| `postgres` | `psycopg[binary]>=3.2.0` | No Postgres code in SDK |
| `sqlite` | `aiosqlite>=0.20.0` | No SQLite code in SDK |
| `monitoring` | prometheus-client, opentelemetry-* | No monitoring code in SDK |
| `smolagents` | `smolagents[toolkit]>=1.0.0` | No smolagents code in SDK |
| `aws` | `boto3>=1.35.0` | No AWS provider in SDK |
| `azure` | `azure-ai-inference>=1.0.0b4` | No Azure provider in SDK |

These extras promise features that don't exist. Users who install them get nothing.

Also: `skills` and `rag` extras are **byte-for-byte identical** (both install chromadb, faiss-cpu, sentence-transformers).

---

## 5. Refactor Candidates

### 5.1 `intelligence/pattern_suggester.py` -- Too Many Responsibilities (689 lines)

Three distinct jobs in one file:

| Responsibility | Approx Lines | Should Be |
|----------------|-------------|-----------|
| Pattern catalog (FULL_PATTERN_CATALOG, PATTERN_MAP) | ~350 | Separate catalog.py or config |
| Suggestion logic (suggest_patterns()) | ~150 | Keep here |
| Pattern class lookup (get_pattern_class()) | ~50 | Merge with pattern_registry.py |
| Serialization (to_dict/json/yaml/xml/markdown) | ~100 | Simplify |

### 5.2 Duplicate Pattern Registries

Two places maintain pattern-name-to-class mappings, **manually**:

1. `intelligence/pattern_suggester.py` -- `get_pattern_class()` with inline imports (lines 588-686)
2. `skills/pattern_registry.py` -- `get_pattern()` with a hardcoded dict (lines 76-127)

Key differences:
- `pattern_registry.py` only has free patterns, `pattern_suggester.py` has both
- `pattern_registry.py` returns instances, `pattern_suggester.py` returns classes
- Both are manually maintained and can drift

**Action:** Unify into one registry.

### 5.3 `intelligence/chain_orchestration_agent.py` -- Brittle Registry

`PATTERN_BUILD_CONTEXT_REGISTRY` (line 21) is a ~103-line hardcoded dict mapping pattern names to their `build_context()` parameter signatures:

```python
"question_analyzer": ("question", {"depth": "standard", "audience": "technical"}),
"code_reviewer": ("code", {"language": "python", "focus_areas": "all"}),
```

Every time a pattern changes its signature, this dict must be manually updated. Should introspect `build_context()` signatures at runtime instead.

### 5.4 `context_amplification.py` -- Dead Method

`_measure_heuristic_only()` (line 130) -- defined but never called from anywhere.

### 5.5 Duplicate `RootCauseAnalyzer`

Exists in both:
- `templates/free/reasoning/root_cause_analyzer.py`
- `templates/enterprise/diagnostic/root_cause_analyzer.py`

Same class name, potentially different implementations. Can cause import confusion.

---

## 6. Deprecated / Incorrect Code

### 6.1 `integrations/helpers.py` -- Deprecated LangChain Imports

Four import paths use the old `langchain` package names that are deprecated since LangChain v0.1+:

| Line | Current (Deprecated) | Should Be |
|------|---------------------|-----------|
| 38 | `from langchain_core.messages import ...` | OK (already updated) |
| 40 | `from langchain.schema import SystemMessage, HumanMessage` | `from langchain_core.messages import ...` |
| 63 | `from langchain.prompts import PromptTemplate` | `from langchain_core.prompts import ...` |
| 81 | `from langchain.prompts import ChatPromptTemplate, ...` | `from langchain_core.prompts import ...` |

Note: Line 38 is already correct (uses `langchain_core`), but lines 40, 63, 81 fall back to deprecated paths. Line 28 in the docstring example shows `from langchain.chat_models import ChatOpenAI` which should be `from langchain_openai import ChatOpenAI`.

### 6.2 `integrations/helpers.py` -- SemanticKernelHelper Deprecated API

`SemanticKernelHelper.create_semantic_function()` (line ~310+) uses `kernel.create_semantic_function()` which is deprecated in Semantic Kernel 1.x. Should use `kernel.add_function()` or similar.

### 6.3 `providers/openai.py` and `providers/anthropic.py` -- Stale Pricing

Both files have hardcoded pricing tables with comments saying "as of 2024" (openai line 41, anthropic line 40). These will become inaccurate over time.

### 6.4 `providers/gemini.py` -- Token Estimation Inaccuracy

Lines 208-210: Token count estimated via character count (4 chars ≈ 1 token). This is a rough approximation that can be significantly off.

### 6.5 `core.py` -- `to_xml()` Incomplete

`to_xml()` (lines 462-500):
- Does not include `constraints` or `data` fields in XML output
- No XML escaping for special characters (`&`, `<`, `>`)
- No error handling for `minidom.parseString()` failures

### 6.6 `core.py` -- `to_yaml()` Missing Error Handling

`to_yaml()` (line 459): Bare `import yaml` with no try/except. If a user somehow doesn't have pyyaml (it's a core dep currently, but if we make it optional later), this crashes with an unhelpful ImportError.

---

## 7. Incomplete Implementations (TODO Stubs)

| File | Line | What's Broken | Impact |
|------|------|--------------|--------|
| `utils/tracking.py` | 180 | `_in_timeframe()` always returns `True` | Time-based cost filtering silently wrong |
| `utils/cache.py` | 184 | `_calculate_hit_rate()` returns "N/A" | Cache stats broken |
| `knowledge/archive.py` | 230 | `delete_session()` -- `# TODO: Update index` | Stale index after delete |
| `knowledge/archive.py` | 269 | `_update_index()` -- `# TODO: Implement proper indexing` | Search index never updates |
| `intelligence/transformation_engine.py` | 141 | `# TODO: Could be enhanced with ML` | Minor |
| `intelligence/transformation_engine.py` | 368 | `# TODO: Expand to all applicable` | Pattern coverage incomplete |
| `intelligence/transformation_engine.py` | 464 | `_optimize_context()` -- only sets metadata, no optimization | Feature is a no-op |

---

## 8. Questionable -- Needs a Decision

### 8.1 `providers/` -- Built-in LLM Execution

**Files:** 7 (base, mock, openai, anthropic, gemini, litellm, __init__)
**Lines:** ~1,135

**Arguments to keep:**
- Convenient one-liner for demos: `ctx.execute(provider="openai")`
- Makes the SDK self-contained
- `litellm_provider.py` provides universal backend

**Arguments to remove or slim down:**
- `openai` is a core dependency because of this -- forces install on everyone
- Individual provider files (openai.py, anthropic.py, gemini.py) duplicate what litellm does
- Users already have their own LLM client setup

**Middle ground:** Keep `providers/` but:
- Move openai from core deps to optional `[openai]` extra
- Consider keeping only mock + litellm, removing individual provider files (openai, anthropic, gemini)

### 8.2 `skills/` -- Agent Skill System

**Files:** 6
**Lines:** ~1,188

**Arguments to keep:**
- Differentiating feature -- no other SDK does this
- Integrates well with Context
- Agent Skills are gaining traction

**Arguments to simplify:**
- `SkillSelector` depends on RAG (which we might remove)
- `improvement.py` (319 lines) is practically a sub-product
- Only useful if users write SKILL.md files

**If keeping:** Simplify SkillSelector to keyword-based matching (no RAG needed).

### 8.3 `utils/` -- How Much Utility is Too Much?

| File | Lines | Purpose | Verdict |
|------|-------|---------|---------|
| structured_output.py | 331 | JSON/Pydantic output formatting | Useful, keep |
| parsers.py | 333 | Parse JSON, XML, Markdown output | Useful, keep |
| validators.py | 229 | Context/output validation | Useful, keep |
| optimizers.py | 340 | Token reduction, compression | Useful if tiktoken stays |
| batch.py | 253 | Parallel context processing | Niche, needs evaluation |
| tracking.py | 350 | Cost tracking (**incomplete**) | Fix or remove |
| cache.py | 305 | Context/response caching (**incomplete**) | Fix or remove |

### 8.4 `benchmarks/` Directory

Not empty (has 5 YAML test case files for template benchmarking). These are consumed by `intelligence/template_benchmark.py` and `benchmark_cli.py`.

**Decision:** Keep if benchmark feature is kept. Remove if benchmark feature is deferred.

### 8.5 Enterprise Template Stubs (systems_thinking/)

Six `systems_thinking/` templates are 14-line stubs:

```
feedback_loop_identifier.py   -- ~14 lines
leverage_point_finder.py      -- ~14 lines
emergence_detector.py         -- ~14 lines
system_archetype_analyzer.py  -- ~14 lines
causal_loop_diagrammer.py     -- ~14 lines
stock_flow_analyzer.py        -- ~14 lines
```

Compare to full templates like `ethical_framework_analyzer.py` (118 lines) or `scaffolding_framework.py` (99 lines). These stubs give a poor impression.

**Options:** Flesh out properly, or remove and adjust the count.

---

## 9. Solid -- Keep As-Is

These are well-implemented, focused, and aligned with the core value proposition:

| Module | Lines | Why It Is Good |
|--------|-------|----------------|
| **core.py** | 591 | Clean Context class, Pydantic-based, 20+ export methods, well-documented |
| **foundation/** | 264 | Guidance, Directive, Constraints -- simple, focused, correct |
| **structure/pattern.py** | 337 | Pattern base class for all 85 templates (minus dead example code at bottom) |
| **structure/blueprint.py** | 280 | Multi-component context architecture (minus dead example code at bottom) |
| **intelligence/quality_metrics.py** | 822 | 6-dimension quality evaluation -- core differentiator |
| **intelligence/transformation_engine.py** | 547 | Auto pattern selection from raw input (has TODOs but core logic works) |
| **intelligence/output_evaluator.py** | 437 | Heuristic + LLM + hybrid output quality scoring -- valuable feature |
| **intelligence/template_integrator_agent.py** | 292 | "Best of All Worlds" multi-template fusion -- unique feature |
| **intelligence/chain_orchestration_agent.py** | 342 | Workflow chain building (registry is brittle but logic works) |
| **intelligence/context_amplification.py** | 298 | CAI measurement (has 1 dead method but otherwise solid) |
| **intelligence/pattern_suggester.py** | 689 | Pattern suggestion engine (needs refactor but works well) |
| **templates/free/** | 39 | Well-structured cognitive patterns |
| **templates/enterprise/** | 46 | Solid architecture (some stubs need work) |
| **integrations/helpers.py** | 398 | 7 framework helpers including GoogleADKHelper (needs deprecated API fixes) |

---

## 10. Dependency Audit

### Core Dependencies (installed for every user)

```toml
dependencies = [
    "pydantic>=2.9.0",        # ESSENTIAL -- Context is a BaseModel
    "tiktoken>=0.8.0",        # OPTIONAL -- only utils/optimizers.py (1 file)
    "jinja2>=3.1.4",          # PHANTOM -- zero imports in entire SDK
    "pyyaml>=6.0.2",          # ESSENTIAL -- to_yaml(), skill loading, pattern config
    "structlog>=24.4.0",      # PHANTOM -- zero imports in entire SDK
    "httpx>=0.27.2",          # PHANTOM -- zero imports in entire SDK
    "openai>=1.54.0",         # OPTIONAL -- only providers/openai.py, core.py example, rag/embedder.py
]
```

**3 phantom dependencies** (jinja2, structlog, httpx) are forcing every user to install packages the SDK never actually imports. These should be removed immediately.

**Recommended core deps:**
```toml
dependencies = [
    "pydantic>=2.9.0",
    "pyyaml>=6.0.2",
]
```

**Recommended optional extras (only real features):**
```toml
[project.optional-dependencies]
openai = ["openai>=1.54.0"]
anthropic = ["anthropic>=0.39.0"]
google = ["google-genai>=0.3.0"]
litellm = ["litellm"]
tokens = ["tiktoken>=0.8.0"]
rag = ["faiss-cpu>=1.9.0", "sentence-transformers>=3.3.0"]  # if keeping RAG
```

**Extras to remove (no corresponding code):**
- `redis`, `postgres`, `sqlite`, `monitoring`, `smolagents`, `aws`, `azure`

### Install Size Impact

Current `pip install mycontext-ai` pulls: pydantic + tiktoken + jinja2 + pyyaml + structlog + httpx + openai + all their transitive deps.

After cleanup: pydantic + pyyaml. **Massive reduction.**

---

## 11. Template Inventory

### Verified Counts

- **Free:** 39 templates (in 6 categories + 7 `__init__.py` files = 46 files)
- **Enterprise:** 46 templates (in 10 categories + 11 `__init__.py` files = 57 files)
- **Total:** 85 templates

### Free Templates (39)

| Category | Count | Templates |
|----------|-------|-----------|
| Analysis | 6 | QuestionAnalyzer, DataAnalyzer, TrendIdentifier, GapAnalyzer, SWOTAnalyzer, AnomalyDetector |
| Reasoning | 5 | StepByStepReasoner, AnalogicalReasoner, CausalReasoner, RootCauseAnalyzer, HypothesisGenerator |
| Creative | 5 | IdeaGenerator, Brainstormer, InnovationFramework, DesignThinker, MetaphorGenerator |
| Communication | 7 | SimplificationEngine, ClarityOptimizer, AudienceAdapter, PersuasionFramework, NarrativeBuilder, TechnicalTranslator, FeedbackComposer |
| Planning | 5 | ScenarioPlanner, StakeholderMapper, PrioritySetter, DeadlineManager, ResourceAllocator |
| Specialized | 11 | CodeReviewer, ContentOutliner, SocraticQuestioner, IntentRecognizer, AmbiguityResolver, RiskAssessor, RiskMitigator, ImpactAssessor, ConflictResolver, ConceptExplainer, SynthesisBuilder |

### Enterprise Templates (46)

| Category | Count | Quality |
|----------|-------|---------|
| Decision | 5 | Full implementations |
| Problem Solving | 6 | Full implementations |
| Metacognition | 5 | Full implementations |
| Ethical Reasoning | 5 | Full implementations |
| Systems Thinking | 6 | **STUBS** (~14 lines each) |
| Learning | 5 | Mixed (some full, some partial) |
| Evaluation | 5 | Mixed |
| Temporal | 3 | Full implementations |
| Diagnostic | 3 | Full implementations |
| Synthesis | 3 | Mixed |

### Issues
- **Duplicate:** `RootCauseAnalyzer` exists in both `free/reasoning/` AND `enterprise/diagnostic/`
- **Stubs:** 6 systems_thinking templates are minimal (~14 lines each)

---

## 12. Recommended Action Plan

### Phase 1: Fix What Is Broken (Do First)

| # | Action | Effort | Impact |
|---|--------|--------|--------|
| 1.1 | Fix `litellm_provider.py` default model names (`gpt-4.1-mini` -> `gpt-4o-mini`, `claude-haiku-4-5` -> real name) | Trivial | Prevents API errors |
| 1.2 | Fix pattern count in README + pyproject.toml (39 Free + 46 Enterprise) | Trivial | Accurate marketing |
| 1.3 | Delete orphaned `licensing.py` (or merge its regex validation into `license.py`) | Small | No confusion |

### Phase 2: Clean Phantom Dependencies

| # | Action | Effort | Impact |
|---|--------|--------|--------|
| 2.1 | Remove `structlog` from core deps (zero imports) | Trivial | Lighter install |
| 2.2 | Remove `httpx` from core deps (zero imports) | Trivial | Lighter install |
| 2.3 | Remove `jinja2` from core deps (zero imports) | Trivial | Lighter install |
| 2.4 | Move `openai` from core deps to optional `[openai]` extra | Small | Much lighter install |
| 2.5 | Move `tiktoken` from core deps to optional `[tokens]` extra | Small | Lighter install |
| 2.6 | Remove fake extras (redis, postgres, sqlite, monitoring, smolagents, aws, azure) | Small | Honest dep list |
| 2.7 | De-duplicate `rag` and `skills` extras (currently identical) | Trivial | Cleaner config |

### Phase 3: Remove Superfluous Code

| # | Action | Effort | Impact |
|---|--------|--------|--------|
| 3.1 | Remove `intelligence/rag/` entirely (5 files, ~386 lines) | Small | Clearer scope |
| 3.2 | Remove `knowledge/` entirely (3 files, ~644 lines) | Small | Less surface area |
| 3.3 | Remove dead example code from `structure/pattern.py` and `structure/blueprint.py` | Trivial | Cleaner source |
| 3.4 | Remove `licensing.py` (if not done in Phase 1) | Trivial | Already covered |
| 3.5 | Update `skills/selector.py` to not require RAG (if RAG removed) | Medium | Skills still work |
| 3.6 | Update `__init__.py` and `intelligence/__init__.py` exports to match removals | Small | Clean imports |

### Phase 4: Fix Deprecated / Incorrect Code

| # | Action | Effort | Impact |
|---|--------|--------|--------|
| 4.1 | Update LangChain imports in `helpers.py` (langchain -> langchain_core) | Small | Working LangChain integration |
| 4.2 | Update SemanticKernelHelper for SK 1.x API | Small | Working SK integration |
| 4.3 | Fix `core.py` `to_xml()` to include constraints, handle escaping | Small | Correct XML output |
| 4.4 | Resolve duplicate `RootCauseAnalyzer` | Small | No import confusion |

### Phase 5: Refactor for Quality

| # | Action | Effort | Impact |
|---|--------|--------|--------|
| 5.1 | Unify pattern registries (pattern_registry.py + pattern_suggester.get_pattern_class) | Medium | Single source of truth |
| 5.2 | Split `pattern_suggester.py` into catalog + suggestion engine | Medium | Maintainability |
| 5.3 | Fix or remove incomplete utils (tracking._in_timeframe, cache._calculate_hit_rate) | Medium | No half-baked features |
| 5.4 | Remove dead method `context_amplification._measure_heuristic_only()` | Trivial | Clean code |
| 5.5 | Make `chain_orchestration_agent.py` registry derive from pattern introspection | Medium | No manual sync |

### Phase 6: Strategic Decisions (Discuss First)

| # | Decision | Options |
|---|----------|---------|
| 6.1 | `providers/` module | Keep all 4 providers OR keep only mock + litellm |
| 6.2 | `skills/` module | Keep (simplified) OR extract to separate package |
| 6.3 | `utils/` scope | Keep all OR trim to parsers + structured_output + validators |
| 6.4 | Enterprise template stubs | Flesh out OR remove + adjust count |
| 6.5 | Benchmark system | Keep (benchmarks/ + template_benchmark + benchmark_cli) OR defer |
| 6.6 | `providers/` pricing tables | Keep hardcoded OR remove and rely on litellm |

---

## Appendix A: Files to Delete (if all removal phases approved)

```
src/mycontext/licensing.py                          # Orphaned, 106 lines
src/mycontext/intelligence/rag/__init__.py          # RAG removal
src/mycontext/intelligence/rag/chunker.py           # RAG removal
src/mycontext/intelligence/rag/embedder.py          # RAG removal
src/mycontext/intelligence/rag/retriever.py         # RAG removal
src/mycontext/intelligence/rag/vector_store.py      # RAG removal
src/mycontext/knowledge/__init__.py                 # Knowledge removal
src/mycontext/knowledge/session.py                  # Knowledge removal
src/mycontext/knowledge/archive.py                  # Knowledge removal
```

Dead code sections to remove (not full files):
```
src/mycontext/structure/pattern.py lines ~278-336   # Dead example patterns
src/mycontext/structure/blueprint.py lines ~254-279 # Dead example blueprints
```

**Lines removed:** ~1,200+
**Dependencies removed from core:** structlog, httpx, jinja2 (phantom), openai + tiktoken (moved to optional)
**Extras removed:** redis, postgres, sqlite, monitoring, smolagents, aws, azure
**Net effect:** Dramatically lighter SDK, honest dependency list, clearer value proposition

## Appendix B: Files That Are Fine (Verified, No Action Needed)

```
src/mycontext/core.py                               # 591 lines, solid
src/mycontext/foundation/guidance.py                 # 86 lines, solid
src/mycontext/foundation/directive.py                # 77 lines, solid
src/mycontext/foundation/constraints.py              # 101 lines, solid
src/mycontext/structure/pattern.py                   # 337 lines (minus dead code at bottom)
src/mycontext/structure/blueprint.py                 # 280 lines (minus dead code at bottom)
src/mycontext/intelligence/quality_metrics.py        # 822 lines, solid
src/mycontext/intelligence/output_evaluator.py       # 437 lines, solid
src/mycontext/intelligence/template_integrator_agent.py  # 292 lines, solid
src/mycontext/intelligence/chain_orchestration_agent.py  # 342 lines (needs registry refactor)
src/mycontext/intelligence/context_amplification.py  # 298 lines (1 dead method)
src/mycontext/intelligence/template_benchmark.py     # 195 lines, solid
src/mycontext/intelligence/transformation_engine.py  # 547 lines (3 TODOs, works)
src/mycontext/intelligence/pattern_suggester.py      # 689 lines (needs split, works)
src/mycontext/providers/base.py                      # 91 lines, solid
src/mycontext/providers/mock.py                      # 62 lines, solid
src/mycontext/skills/skill.py                        # 229 lines, solid
src/mycontext/skills/runner.py                       # 205 lines, solid
src/mycontext/skills/improvement.py                  # 319 lines, solid
src/mycontext/utils/parsers.py                       # 333 lines, solid
src/mycontext/utils/structured_output.py             # 331 lines, solid
src/mycontext/utils/validators.py                    # 229 lines, solid
src/mycontext/utils/optimizers.py                    # 340 lines, solid
src/mycontext/utils/batch.py                         # 253 lines, solid
src/mycontext/license.py                             # 77 lines, solid
src/mycontext/benchmark_cli.py                       # 117 lines, solid
src/mycontext/version.py                             # 5 lines, solid
```
