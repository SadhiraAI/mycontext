"""
Chain Orchestration Agent - LLM-driven workflow chain + chain_params generation.

Analyzes the user question, selects and orders patterns from the full catalog,
and produces both workflow_chain and chain_params automatically. Uses temperature=0
for deterministic output and supports LLM overrides for task-specific params.
"""

from dataclasses import dataclass, field
from typing import Any

from .pattern_catalog import ENRICHED_CATALOG_TEXT, ENTERPRISE_LICENSE_NOTE, NAME_TO_CATEGORY
from .pattern_suggester import (
    VALID_PATTERN_NAMES,
    get_pattern_class,
)


class _DynamicBuildContextRegistry:
    """Lazy registry that introspects pattern build_context() signatures at runtime.

    Replaces the old manually-maintained dict.  Accessed like a dict
    (``registry[name]``, ``registry.get(name)``, ``name in registry``,
    ``registry.items()``) but builds entries on first access from the
    unified pattern registry.
    """

    def __init__(self) -> None:
        self._cache: dict[str, tuple] | None = None

    def _ensure(self) -> dict[str, tuple]:
        if self._cache is None:
            from ..skills.pattern_registry import (
                get_pattern_build_params,
                get_pattern_registry,
            )

            registry = get_pattern_registry()
            self._cache = {name: get_pattern_build_params(name) for name in registry}
        return self._cache

    def __getitem__(self, key: str) -> tuple:
        return self._ensure()[key]

    def get(self, key: str, default: Any = None) -> Any:
        return self._ensure().get(key, default)

    def __contains__(self, key: object) -> bool:
        return key in self._ensure()

    def items(self):
        return self._ensure().items()

    def keys(self):
        return self._ensure().keys()

    def values(self):
        return self._ensure().values()

    def __iter__(self):
        return iter(self._ensure())

    def __len__(self):
        return len(self._ensure())


PATTERN_BUILD_CONTEXT_REGISTRY: Any = _DynamicBuildContextRegistry()


@dataclass
class WorkflowChainResult:
    """Result of chain orchestration: chain + chain_params + selection reasoning."""

    chain: list[str]
    chain_params: dict[str, dict[str, Any]]
    reasoning: str = ""
    selection_reasoning: dict[str, str] = field(
        default_factory=dict
    )  # pattern_name -> why chosen, how it relates
    pattern_categories: dict[str, str] = field(
        default_factory=dict
    )  # pattern_name -> "free"|"enterprise"
    question_analysis: dict[str, Any] | None = None  # facets, key_concerns, decomposition
    template_decomposition: str | None = (
        None  # raw output from question_analyzer template (when used)
    )
    llm_raw: str | None = None

    def to_chain_params_tuple_format(self) -> dict[str, tuple]:
        """Convert to (primary_key, extra_dict) format for orchestrator loop.
        Returns dict: name -> (primary_input_key, extra_kwargs_for_build_context)
        Always merges registry defaults so required fields (depth, context_section, etc.) are present.
        """
        out = {}
        for name in self.chain:
            params = self.chain_params.get(name, {})
            reg = PATTERN_BUILD_CONTEXT_REGISTRY.get(name, ("input", {}))
            primary, defaults = reg
            # Start with defaults (ensures depth, context, etc. are present)
            extra = dict(defaults)
            # Overlay custom params (excluding primary, which gets prev at runtime)
            for k, v in params.items():
                if k != primary:
                    extra[k] = v
            out[name] = (primary, extra)
        return out


def build_workflow_chain(
    question: str,
    include_enterprise: bool = True,
    max_patterns: int | None = None,
    use_question_analyzer: bool = True,
    provider: str = "openai",
    temperature: float = 0,
    model: str | None = None,
    **llm_kwargs: Any,
) -> WorkflowChainResult:
    """Use LLM to select, order, and generate chain_params for a workflow chain.

    .. deprecated::
        Use :func:`mycontext.intelligence.route_suggester.suggest_routes`
        instead for richer, multi-route output with agent-level detail.
        This function now delegates to ``suggest_routes(max_routes=1)``
        and reformats the result for backward compatibility.

    Args:
        question: User's question or task description
        include_enterprise: Include enterprise patterns (default True)
        max_patterns: Max patterns in chain (None = no limit)
        use_question_analyzer: Run question_analyzer template first for decomposition (default True)
        provider: LLM provider ("openai", "anthropic", "gemini")
        temperature: LLM temperature (default 0 for determinism)
        model: Override model name
        **llm_kwargs: Extra kwargs passed to provider.generate()

    Returns:
        WorkflowChainResult with chain, chain_params, and reasoning
    """
    import warnings

    warnings.warn(
        "build_workflow_chain() is deprecated. Use suggest_routes() for richer, "
        "multi-route output with agent-level detail.",
        DeprecationWarning,
        stacklevel=2,
    )

    # Try delegating to suggest_routes
    try:
        from .route_suggester import suggest_routes

        route_result = suggest_routes(
            question=question,
            max_routes=1,
            include_enterprise=include_enterprise,
            provider=provider,
            temperature=temperature,
            model=model,
            **llm_kwargs,
        )
        if route_result.routes:
            best = route_result.routes[0]
            chain = [s.template for s in best.steps]
            chain_params = {s.template: s.params for s in best.steps}
            selection_reasoning = {s.template: f"{s.agent_role}: {s.produces}" for s in best.steps}
            return WorkflowChainResult(
                chain=chain[:max_patterns] if max_patterns else chain,
                chain_params=chain_params,
                reasoning=route_result.recommendation,
                selection_reasoning=selection_reasoning,
                pattern_categories={
                    s.template: NAME_TO_CATEGORY.get(s.template, "free") for s in best.steps
                },
                question_analysis={
                    "decomposition": route_result.question_decomposition,
                },
            )
    except Exception:
        pass  # Fall through to original implementation
    from ..core import Context
    from ..foundation import Directive, Guidance

    template_decomposition: str | None = None
    if use_question_analyzer:
        try:
            analyzer = get_pattern_class("question_analyzer")
            if analyzer is not None:
                exec_kw = {"provider": provider, "temperature": temperature, **llm_kwargs}
                if model:
                    exec_kw["model"] = model
                qa_result = analyzer().execute(question=question, **exec_kw)
                template_decomposition = (qa_result.response or "").strip()[:4000]  # bound size
        except Exception:
            pass  # fall back to selection without template output

    # Always show the LLM the full catalog (all 85 templates) so it picks
    # the objectively best chain.  When include_enterprise=False, enterprise
    # patterns are still returned but tagged with a license note — matching
    # the behaviour of heuristic / hybrid modes.
    catalog = ENRICHED_CATALOG_TEXT
    valid = VALID_PATTERN_NAMES

    # Schema excerpt for LLM
    schema_example = """
For each pattern, provide optional overrides. Common keys: data, data_description, goal, baseline, problem, situation, input, context, pattern_focus, etc.
Use exact pattern names from the catalog.
"""

    pre_analysis_block = ""
    if template_decomposition:
        pre_analysis_block = f"""## Pre-analysis of the user goal (from question_analyzer template):

{template_decomposition}

**Use this analysis above** to inform your pattern selection. The template has decomposed the question - identify the core domains, reasoning requirements, and map them to the most relevant patterns.\n\n"""
    else:
        pre_analysis_block = """**Step 1** - Analyze the question: what domains does it span (business, technical, ethical, legal, etc.)? What type of reasoning is needed (diagnostic, comparative, strategic, creative)?
**Step 2** - Select ONLY the patterns that directly address the question's core requirements. Fewer, better-matched patterns beat many tangentially related ones.\n\n"""

    prompt = f"""Task: "{question}"

{pre_analysis_block}Available patterns (use EXACT names):
{catalog}
{schema_example}

Return a JSON object with these keys:
1. "question_analysis": {{"domains": ["list of knowledge domains involved"], "reasoning_type": "diagnostic|comparative|strategic|creative|ethical|analytical", "complexity": "low|medium|high", "decomposition": "brief summary of what the task entails"}}
2. "chain": array of 2-4 pattern names in workflow order. Select ONLY patterns that directly address the question. Quality over quantity.
3. "chain_params": object mapping each pattern name to its build_context params. Primary input key = "<from previous step>", plus task-specific overrides.
4. "selection_reasoning": object mapping each pattern name to a short explanation: WHY you chose it, WHAT specific aspect of the question it addresses.

Example for business diagnostic:
{{
  "question_analysis": {{
    "domains": ["business operations", "customer retention", "product management"],
    "reasoning_type": "diagnostic",
    "complexity": "high",
    "decomposition": "Diagnose root causes of customer churn spike, identify contributing factors across product, pricing, and support, then recommend prioritized fixes."
  }},
  "chain": ["root_cause_analyzer", "trend_identifier", "decision_framework"],
  "chain_params": {{ ... }},
  "selection_reasoning": {{
    "root_cause_analyzer": "Core diagnostic tool - applies Five Whys and Ishikawa to systematically identify why churn spiked.",
    "trend_identifier": "Identifies temporal patterns in the churn data to distinguish one-time events from systemic issues.",
    "decision_framework": "Structures the final recommendations with weighted criteria so the team can prioritize fixes."
  }}
}}

Respond with ONLY valid JSON. No markdown, no explanation outside JSON."""

    try:
        ctx = Context(
            guidance=Guidance(
                role="Workflow chain orchestrator specializing in matching cognitive reasoning frameworks to complex questions",
                rules=[
                    "Analyze the question: identify domains (business, technical, ethical, legal, etc.) and the type of reasoning needed.",
                    "Select 2-4 patterns that DIRECTLY address the question's core requirements. Each pattern must earn its place.",
                    "Pick only from the catalog. Return valid JSON only.",
                    "Order patterns logically: investigation/analysis first, then reasoning/comparison, then synthesis/decision last.",
                ],
            ),
            directive=Directive(content=prompt),
        )
        exec_kwargs = dict(llm_kwargs)
        exec_kwargs["temperature"] = temperature
        if model:
            exec_kwargs["model"] = model
        result = ctx.execute(provider=provider, **exec_kwargs)
    except Exception as e:
        return WorkflowChainResult(
            chain=[],
            chain_params={},
            reasoning=f"Error: {e}",
            llm_raw=str(e),
        )

    raw = result.response.strip()
    # Strip markdown code blocks if present
    if raw.startswith("```"):
        lines = raw.split("\n")
        raw = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])

    import json

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        return WorkflowChainResult(
            chain=[],
            chain_params={},
            reasoning=f"Invalid JSON: {e}",
            llm_raw=raw[:1000],
        )

    chain = data.get("chain", [])
    chain_params = data.get("chain_params", {})
    selection_reasoning = data.get("selection_reasoning", {})
    question_analysis = data.get("question_analysis")

    # Validate and filter to valid pattern names
    chain = [n for n in chain if n in valid]
    if max_patterns is not None:
        chain = chain[:max_patterns]
    chain_params = {k: v for k, v in chain_params.items() if k in valid}
    selection_reasoning = {k: v for k, v in selection_reasoning.items() if k in valid}

    # Ensure chain_params has entries for all chain patterns; merge with registry
    merged_params = {}
    for name in chain:
        reg = PATTERN_BUILD_CONTEXT_REGISTRY.get(name, ("input", {}))
        primary, defaults = reg
        custom = chain_params.get(name, {})
        merged = dict(defaults)
        for k, v in custom.items():
            if v != "<from previous step>" or k == primary:
                merged[k] = v
        if primary not in merged and name in chain_params:
            merged[primary] = chain_params[name].get(primary, "<from previous step>")
        elif primary not in merged:
            merged[primary] = "<from previous step>"
        merged_params[name] = merged

    # Tag each pattern with its category and append license note for
    # enterprise patterns when the user doesn't have enterprise access —
    # mirrors the behaviour of heuristic / hybrid modes.
    categories: dict[str, str] = {}
    for name in chain:
        categories[name] = NAME_TO_CATEGORY.get(name, "free")
    if not include_enterprise:
        for name in chain:
            if categories.get(name) == "enterprise":
                existing = selection_reasoning.get(name, "")
                if ENTERPRISE_LICENSE_NOTE not in existing:
                    selection_reasoning[name] = existing + ENTERPRISE_LICENSE_NOTE

    reasoning_parts = []
    if question_analysis:
        decomp = question_analysis.get("decomposition", "")
        facets = question_analysis.get("facets", [])
        if decomp:
            reasoning_parts.append(decomp)
        if facets:
            reasoning_parts.append("Facets: " + ", ".join(facets[:6]))
    if selection_reasoning:
        reasoning_parts.append(f"Selected {len(chain)} patterns: " + " → ".join(chain[:8]))
    reasoning_text = (
        ". ".join(reasoning_parts)
        if reasoning_parts
        else f"Selected {len(chain)} patterns for this task."
    )

    return WorkflowChainResult(
        chain=chain,
        chain_params=merged_params,
        reasoning=reasoning_text,
        selection_reasoning=selection_reasoning,
        pattern_categories=categories,
        question_analysis=question_analysis,
        template_decomposition=template_decomposition,
        llm_raw=raw[:2000],
    )
