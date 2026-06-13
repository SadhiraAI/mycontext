---
sidebar_position: 1
title: API Reference
description: Complete quick-reference for every class, method, and function in the mycontext-ai SDK.
---

# API Reference

Complete quick-reference for the mycontext-ai SDK. For detailed explanations, see the dedicated section for each topic.

---

## Core — `mycontext.Context`

```python
from mycontext import Context
```

### Constructor

```python
Context(
    guidance: Guidance | str | None = None,
    directive: Directive | str | None = None,
    constraints: Constraints | None = None,
    knowledge: str | None = None,
    data: dict = {},
    metadata: dict = {},
    thinking_strategy: str | None = None,
    examples: list[dict[str, str]] | None = None,
    research_flow: bool = False,
    provider_hint: str | None = None,
    task_contract: TaskContract | None = None,
)
```

Strings passed to `guidance` or `directive` are automatically promoted to `Guidance(role=...)` and `Directive(content=...)`.

### Research Flow Fields

| Field | Type | Description |
|-------|------|-------------|
| `research_flow` | `bool` | When `True`, uses 9-section research-backed assembly. Default `False` |
| `thinking_strategy` | `str \| None` | Reasoning strategy: `step_by_step`, `multiple_angles`, `verify`, `explain_simply`, `creative` |
| `examples` | `list[dict] \| None` | Few-shot pairs `[{"input": "...", "output": "..."}]` — placed in middle zone when `research_flow=True` |
| `provider_hint` | `str \| None` | `openai`, `anthropic`, `gemini`, or `generic` — assembly formatting only |
| `task_contract` | `TaskContract \| None` | L0 table at top of research-flow prompt when set. See below. |

### Class Methods

| Method | Signature | Returns | Description |
|--------|-----------|---------|-------------|
| `from_dict` | `from_dict(data)` | `Context` | Deserialize from dict |
| `from_json` | `from_json(json_str)` | `Context` | Deserialize from JSON |
| `from_skill` | `from_skill(path, task?, **params)` | `Context` | Build from a SKILL.md Agent Skill |

### Execution

| Method | Signature | Returns | Description |
|--------|-----------|---------|-------------|
| `execute` | `execute(provider, **kwargs)` | `ProviderResponse` | Run with an LLM (synchronous) |
| `aexecute` | `aexecute(provider, **kwargs)` | `Coroutine[ProviderResponse]` | Run asynchronously — native `async`/`await` |
| `assemble_for_model` | `assemble_for_model(model, max_tokens?)` | `str` | Token-budget assembly — tiktoken-accurate, trims to fit |
| `to_prompt` | `to_prompt(refine=False, provider="openai", model="gpt-4o-mini")` | `str` | Zero-cost restructuring (`refine=False`) or LLM-distilled prompt (`refine=True`) |

`ProviderResponse.response` — the LLM output text.

### Export Formats

| Method | Returns | Description |
|--------|---------|-------------|
| `assemble()` | `str` | Assembled prompt. Uses classic or 9-section ordering based on `research_flow` |
| `to_messages(user_message?)` | `list[dict]` | OpenAI-style messages array |
| `to_openai()` | `dict` | `chat.completions.create()` kwargs |
| `to_anthropic()` | `dict` | `messages.create()` kwargs |
| `to_google()` | `dict` | `generate_content()` kwargs |
| `to_langchain()` | `dict` | LangChain format |
| `to_llamaindex()` | `dict` | LlamaIndex format |
| `to_crewai()` | `dict` | CrewAI Agent + Task format |
| `to_autogen()` | `dict` | AutoGen format |
| `to_json()` | `str` | JSON string |
| `to_yaml()` | `str` | YAML string |
| `to_xml()` | `str` | XML string |
| `to_markdown()` | `str` | Markdown string |
| `to_dict()` | `dict` | Python dict |

---

## Foundations — `mycontext.foundation`

### `TaskContract`

```python
from mycontext import TaskContract
# or: from mycontext.foundation import TaskContract

TaskContract(
    domain: str | None = None,
    audience: str | None = None,
    genre: str | None = None,
    grounding: str | None = None,
    metaphor: str | None = None,
)
```

| Method | Returns | Description |
|--------|---------|-------------|
| `has_content()` | `bool` | Any field populated |
| `to_dict()` | `dict[str, str]` | Non-null fields only |
| `from_dict(d)` | `TaskContract` | Class method — e.g. migrate `metadata["l0"]` |

Full guide: [Task Contract (L0)](../foundations/task-contract).

### `Guidance`

```python
from mycontext.foundation import Guidance

Guidance(
    role: str,                           # required
    goal: str | None = None,
    rules: list[str] = [],
    style: str | None = None,
    expertise: list[str] | None = None,
)
```

| Field | Description |
|-------|-------------|
| `role` | The persona or identity the LLM adopts |
| `goal` | The objective — what success looks like for this interaction |
| `rules` | Behavioral rules rendered as a numbered list |
| `style` | Communication tone and style |
| `expertise` | Domain expertise areas |

| Method | Returns | Description |
|--------|---------|-------------|
| `render()` | `str` | Rendered guidance string |

### `Directive`

```python
from mycontext.foundation import Directive

Directive(
    content: str,                        # required
    priority: int = 5,                   # 1-10
    constraints: list[str] | None = None,
    tags: list[str] | None = None,
)
```

| Method | Returns | Description |
|--------|---------|-------------|
| `render()` | `str` | Rendered directive string |

### `Constraints`

```python
from mycontext.foundation import Constraints

Constraints(
    must_include: list[str] | None = None,
    must_not_include: list[str] | None = None,
    format_rules: list[str] | None = None,
    max_length: int | None = None,
    language: str | None = None,
    output_schema: list[dict] | None = None,
    # Quality controls (auto-suggested by PromptArchitect) — new in 0.11.0
    verbosity: "minimal" | "standard" | "detailed" | None = None,
    communication_posture: "direct" | "collaborative" | "educational" | None = None,
    answer_first: bool | None = None,
    forbidden_phrases: list[str] | None = None,
    self_check: list[str] | None = None,
)
```

`output_schema` takes a list of `{"name": str, "type": str}` dicts. In `research_flow=True` mode, this generates a dedicated `## OUTPUT FORMAT` section with a JSON skeleton.

The five quality control fields (`verbosity`, `communication_posture`, `answer_first`, `forbidden_phrases`, `self_check`) are auto-suggested by `PromptArchitect.build()` and `improve()` and can be overridden by the user. See [Constraints → Quality Controls](../foundations/constraints#quality-controls-new-in-0110).

| Method | Returns | Description |
|--------|---------|-------------|
| `render()` | `str` | Rendered constraints string |

---

## Cognitive Patterns — `mycontext.templates`

All patterns share the same interface:

```python
pattern = PatternName()
ctx: Context = pattern.build_context(**inputs)
result = pattern.execute(provider="openai", **inputs)
```

### Free Patterns (16)

```python
from mycontext.templates.free.reasoning import (
    RootCauseAnalyzer,    # build_context(problem, depth)
    StepByStepReasoner,   # build_context(problem, steps)
    HypothesisGenerator,  # build_context(phenomenon, domain)
)
from mycontext.templates.free.analysis import (
    DataAnalyzer,         # build_context(data_description, analysis_type)
    QuestionAnalyzer,     # build_context(question, context)
)
from mycontext.templates.free.creative import (
    Brainstormer,         # build_context(topic, constraints)
)
from mycontext.templates.free.specialized import (
    CodeReviewer,         # build_context(code, language, focus)
    RiskAssessor,         # build_context(decision, depth)
    ConflictResolver,     # build_context(conflict, parties)
    SocraticQuestioner,   # build_context(topic, depth)
    IntentRecognizer,     # build_context(input, context)
)
from mycontext.templates.free.planning import (
    ScenarioPlanner,      # build_context(situation, horizon)
    StakeholderMapper,    # build_context(project, objective)
)
from mycontext.templates.free.communication import (
    AudienceAdapter,      # build_context(content, audience)
    TechnicalTranslator,  # build_context(technical_text, audience)
)
from mycontext.templates.free.reasoning import (
    SynthesisBuilder,     # build_context(sources, topic)
)
```

### Advanced Patterns

All open source — import directly, no activation step:

```python
from mycontext.templates.enterprise.decision import (
    DecisionFramework, ComparativeAnalyzer, TradeoffAnalyzer,
    CostBenefitAnalyzer, MultiObjectiveOptimizer,
)
from mycontext.templates.enterprise.systems_thinking import (
    FeedbackLoopIdentifier, LeveragePointFinder, SystemArchetypeAnalyzer,
)
from mycontext.templates.enterprise.ethical_reasoning import (
    EthicalFrameworkAnalyzer, MoralDilemmaResolver,
)
# ... and 60+ more
```

---

## Intelligence Layer — `mycontext.intelligence`

### Top-level Functions

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `generate_context` | `generate_context(role, goal, task?, provider, model, **kwargs)` | `GeneratedContext` | LLM generates full context from role + goal |
| `transform` | `transform(input_text, provider?, model?)` | `Context` | Auto-select pattern + build context |
| `suggest_patterns` | `suggest_patterns(text, mode, top_k)` | `SuggestionResult` | Pattern recommendations |
| `assess_complexity` | `assess_complexity(text, provider?)` | `ComplexityResult` | Template needed? |
| `smart_execute` | `smart_execute(text, provider, model?)` | `ProviderResponse` | One-liner intelligent execution |
| `smart_prompt` | `smart_prompt(text, provider?, model?)` | `str` | One-liner prompt generation |
| `smart_generic_prompt` | `smart_generic_prompt(text, provider?, model?)` | `str` | LLM-optimized generic prompt |
| `build_workflow_chain` | `build_workflow_chain(goal, provider, model?)` | `WorkflowChainResult` | LLM-designed multi-pattern chain |

```python
from mycontext.intelligence import (
    generate_context, GeneratedContext,
    transform, suggest_patterns, assess_complexity,
    smart_execute, smart_prompt, smart_generic_prompt,
    build_workflow_chain,
)
```

### `GeneratedContext`

```python
@dataclass
class GeneratedContext:
    context: Context            # Fully-populated Context(research_flow=True)
    generation_meta: dict       # Raw spec produced by the LLM

    def assemble(self) -> str               # Pass-through to context.assemble()
    def execute(self, provider, **kwargs)   # Pass-through to context.execute()
    def to_context(self) -> Context         # Return the underlying Context
```

### `SuggestionResult`

```python
@dataclass
class SuggestionResult:
    suggested_patterns: list[PatternSuggestion]
    input_type: str
    complexity: str
    reasoning: str
    used_llm: bool
```

### `PatternSuggestion`

```python
@dataclass
class PatternSuggestion:
    name: str
    category: str
    reason: str
    confidence: float
    chain_position: int | None = None
```

### `ComplexityResult`

```python
@dataclass
class ComplexityResult:
    needs_template: bool
    complexity_level: str   # "simple" | "moderate" | "complex"
    reasoning: str
    recommended_pattern: str | None
```

### `WorkflowChainResult`

```python
@dataclass
class WorkflowChainResult:
    steps: list[ChainStep]
    total_steps: int
    reasoning: str
```

### `PromptComposer`

```python
from mycontext.intelligence import PromptComposer

composer = PromptComposer(provider="openai", model="gpt-4o-mini")
composed: ComposedPrompt = composer.compose(contexts=[ctx1, ctx2])
composed: ComposedPrompt = composer.compose_from_templates(
    templates=[Template1, Template2],
    input_data={"key": "value"},
)
```

### `TransformationEngine`

```python
from mycontext.intelligence import TransformationEngine

engine = TransformationEngine()
ctx = engine.transform(input_text="Analyze X")
analysis: InputAnalysis = engine.analyze_input(input_text)
```

### `TemplateIntegratorAgent`

```python
from mycontext.intelligence import TemplateIntegratorAgent

agent = TemplateIntegratorAgent(provider="openai")
result: IntegrationResult = agent.integrate(
    templates=[T1, T2],
    input_data={"key": "value"},
)
result: IntegrationResult = agent.suggest_and_integrate(text="...", input_data={})
composed: ComposedPrompt = agent.suggest_and_compile(text="...")
```

---

## Quality & Metrics — `mycontext.intelligence`

### `QualityMetrics`

```python
from mycontext.intelligence import QualityMetrics

metrics = QualityMetrics(mode="heuristic")  # or "llm"
score: QualityScore = metrics.evaluate(ctx)
report: str = metrics.report(score)
comparison: dict = metrics.compare(ctx1, ctx2)
```

**`QualityScore`**

```python
score.overall          # float 0-1
score.dimensions       # dict[QualityDimension, float]
score.issues           # list[str] — improvement suggestions
score.strengths        # list[str]
```

**Dimensions:** `CLARITY`, `COMPLETENESS`, `SPECIFICITY`, `RELEVANCE`, `STRUCTURE`, `EFFICIENCY`

### `OutputEvaluator`

```python
from mycontext.intelligence import OutputEvaluator

evaluator = OutputEvaluator()
score: OutputQualityScore = evaluator.evaluate(context=ctx, output=response_text)
report: str = evaluator.report(score)
```

**Dimensions:** `INSTRUCTION_FOLLOWING`, `REASONING_DEPTH`, `ACTIONABILITY`, `STRUCTURE_COMPLIANCE`, `COGNITIVE_SCAFFOLDING`

### `ContextAmplificationIndex`

```python
from mycontext.intelligence import ContextAmplificationIndex

cai = ContextAmplificationIndex()
result: CAIResult = cai.measure(
    template=MyPattern,
    input_data={"key": "value"},
    provider="openai",
)
result.cai_score    # float (1.0 = neutral, >1.2 = significant lift)
result.verdict      # "significant_improvement" | "moderate_improvement" | ...
```

### `TemplateBenchmark`

```python
from mycontext.intelligence import TemplateBenchmark

bench = TemplateBenchmark()
result: BenchmarkResult = bench.run(
    template=MyPattern,
    benchmark_name="my_benchmark",
    provider="openai",
)
result.overall_score     # float
result.pass_rate         # float
result.avg_latency_ms    # float
```

---

## Integrations — `mycontext.integrations`

### Helper Classes

```python
from mycontext.integrations import (
    LangChainHelper,
    LlamaIndexHelper,
    CrewAIHelper,
    AutoGenHelper,
    DSPyHelper,
    SemanticKernelHelper,
    GoogleADKHelper,
    auto_integrate,
)
```

| Helper | Key Methods |
|--------|-------------|
| `LangChainHelper` | `to_chat_prompt()`, `to_lcel_chain()`, `to_langchain_messages()` |
| `LlamaIndexHelper` | `to_query_engine()`, `to_chat_engine()` |
| `CrewAIHelper` | `to_agent()`, `to_task()`, `to_crew()` |
| `AutoGenHelper` | `to_assistant_agent()`, `to_user_proxy()` |
| `DSPyHelper` | `to_signature()`, `to_program()` |
| `SemanticKernelHelper` | `to_semantic_function()`, `to_kernel_function()` |
| `GoogleADKHelper` | `to_agent()`, `to_pipeline()` |

### `auto_integrate(ctx, framework)`

```python
result = auto_integrate(ctx, framework="langchain")
result = auto_integrate(ctx, framework="crewai")
result = auto_integrate(ctx, framework="autogen")
```

---

## Advanced

### `Blueprint` — `mycontext.structure`

```python
from mycontext.structure import Blueprint

bp = Blueprint(
    name="my_blueprint",
    guidance=Guidance(...),
    directive_template="Do {task} for {subject}",
    constraints=Constraints(...),
    token_budget=4000,
    optimization="balanced",  # "speed" | "quality" | "cost" | "balanced"
)

ctx: Context = bp.build(task="analysis", subject="Q3 data")
bp_optimized: Blueprint = bp.optimize("quality")
tokens: int = bp.estimate_tokens()
```

### `Skill` + `SkillRunner` — `mycontext.skills`

```python
from mycontext.skills.skill import Skill
from mycontext.skills import SkillRunner
from pathlib import Path

skill = Skill.load(Path("./skills/my-skill"))
runner = SkillRunner(log_runs=True)

result: SkillRunResult = runner.run(
    skill_path=Path("./skills/my-skill"),
    task="Specific task",
    execute=True,
    provider="openai",
    quality_threshold=0.65,
    **skill_params,
)

result.context         # Context
result.quality_score   # QualityScore
result.execution_result  # ProviderResponse | None
result.gated           # bool
```

---

## Fragments — `mycontext.fragments`

Reusable quality-enhancing building blocks for Blueprint composition. Each fragment can be applied to any `Context` to merge constraints and guidance rules.

```python
from mycontext.fragments import (
    anti_fluff,              # Sets verbosity="minimal", bans filler phrases
    answer_first_fragment,   # Sets answer_first=True
    objectivity,             # Adds objectivity rules to guidance
    self_check_analysis,     # Adds analysis-focused self-check questions
    self_check_creative,     # Adds creative-focused self-check questions
    self_check_risk,         # Adds risk-focused self-check questions
    structured_json,         # Sets output_contract for JSON output
    grounding_strict,        # Adds strict grounding rules
    educational_posture,     # Sets communication_posture="educational"
    collaborative_posture,   # Sets communication_posture="collaborative"
    hedging_ban,             # Bans hedging phrases
    executive_brevity,       # Sets verbosity="minimal", answer_first=True, direct posture
)

# Apply to any Context
ctx = some_template.build_context(...)
anti_fluff.apply(ctx)
objectivity.apply(ctx)
```

| Method | Returns | Description |
|--------|---------|-------------|
| `fragment.apply(ctx)` | `None` | Merge fragment settings into Context in-place |
| `fragment.constraints()` | `Constraints \| None` | Get the fragment's Constraints object |
| `fragment.guidance_rules()` | `list[str]` | Get the fragment's guidance rules |

---

## Structured Output — `mycontext.utils`

```python
from mycontext.utils.structured_output import (
    extract_json,
    StructuredOutputMixin,
    PydanticOutput,
    JSONOutput,
    output_format,
)
from mycontext.utils.parsers import (
    JSONParser,
    ListParser,
    CodeBlockParser,
    MarkdownParser,
    parse_json_response,
    parse_code_blocks,
    parse_list_items,
)
```

---

## Token Utilities — `mycontext.utils.tokens`

```python
from mycontext.utils.tokens import (
    count_tokens,           # count_tokens(text, model) → int
    fits_in_window,         # fits_in_window(text, model) → bool
    token_budget_remaining, # token_budget_remaining(text, model) → int
    estimate_cost_usd,      # estimate_cost_usd(input_tokens, output_tokens, model) → float
)
```

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `count_tokens` | `(text, model)` | `int` | Exact token count via tiktoken, falls back to char estimate |
| `fits_in_window` | `(text, model)` | `bool` | `True` if text fits in model's context window |
| `token_budget_remaining` | `(text, model)` | `int` | Tokens remaining after `text` for the model's window |
| `estimate_cost_usd` | `(input_tokens, output_tokens, model)` | `float` | USD cost estimate for a call |

---

## Tracing — `mycontext.utils.tracing`

```python
from mycontext.utils.tracing import get_tracer, Span, Tracer

tracer = get_tracer()  # Module-level singleton

# Read spans after execution
result = ctx.execute(provider="openai")
spans = tracer.get_spans()
span = spans[-1]

span.name          # "litellm_generate"
span.metadata      # {"model": "gpt-4o-mini", "tokens": 312, "cost_usd": 0.00012, "latency_ms": 1842}
span.duration_ms   # float
span.error         # str | None
```

---

## Semantic Cache — `mycontext.utils`

```python
from mycontext.utils import get_default_cache, reset_default_cache

cache = get_default_cache()
cache.size()   # int — current entries
cache.clear()  # wipe all entries

# Per-call cache bypass
result = ctx.execute(provider="openai", use_cache=False)
```

---

## Security — `mycontext.utils.template_safety`

```python
from mycontext.utils.template_safety import safe_format_template

# Safe substitution — rejects attribute/item access patterns
prompt = safe_format_template("Analyze {topic} for {audience}.", topic="revenue", audience="CFO")

# Raises ValueError for unsafe patterns like {obj.attr} or {obj[key]}
```

---

## License API — `mycontext` (deprecated)

mycontext is fully open source — all 88 patterns ship in the package with no
license keys. These functions are **deprecated no-op shims** kept for one
release; they emit a `DeprecationWarning` and otherwise do nothing.

```python
import mycontext

mycontext.activate_license("...")   # no-op, returns True, warns
mycontext.deactivate_license()       # no-op, warns
mycontext.is_enterprise_active()     # always True, warns
```

---

## Provider Configuration

```python
# Default provider selection
ctx.execute(provider="openai")
ctx.execute(provider="anthropic")
ctx.execute(provider="gemini")

# With explicit model + API key
ctx.execute(
    provider="openai",
    model="gpt-4o",
    api_key="sk-...",
    temperature=0,
    max_tokens=4096,
)
```

---

## Common Import Paths

```python
# Core
from mycontext import Context
from mycontext.foundation import Guidance, Directive, Constraints

# Patterns
from mycontext.templates.free.reasoning import RootCauseAnalyzer
from mycontext.templates.enterprise.decision import DecisionFramework

# Intelligence
from mycontext.intelligence import (
    generate_context, GeneratedContext,
    transform, suggest_patterns, smart_execute, smart_prompt,
    QualityMetrics, OutputEvaluator, ContextAmplificationIndex,
    TemplateBenchmark, TemplateIntegratorAgent, PromptComposer,
    build_workflow_chain,
)

# Integrations
from mycontext.integrations import LangChainHelper, auto_integrate

# Advanced
from mycontext.structure import Blueprint
from mycontext.skills import SkillRunner
from mycontext.skills.skill import Skill

# Token utilities
from mycontext.utils.tokens import count_tokens, fits_in_window, estimate_cost_usd

# Tracing
from mycontext.utils.tracing import get_tracer

# Cache
from mycontext.utils import get_default_cache

# Security
from mycontext.utils.template_safety import safe_format_template

# Structured output
from mycontext.utils.structured_output import extract_json, PydanticOutput
from mycontext.utils.parsers import JSONParser, ListParser
```
