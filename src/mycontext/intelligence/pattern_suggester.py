"""
Pattern Suggester - Auto-suggest essential templates for any question.

Maps question intent/keywords to optimal patterns (all 85 free + enterprise).
Always suggests from full catalog; enterprise patterns show license note when include_enterprise=False.
"""

import logging
import re
from dataclasses import asdict, dataclass, field
from typing import Any

from .pattern_catalog import (
    ENRICHED_CATALOG_TEXT,
    ENTERPRISE_LICENSE_NOTE,
    NAME_TO_CATEGORY,
    PATTERN_MAP,
    VALID_PATTERN_NAMES,
)

logger = logging.getLogger(__name__)


@dataclass
class PatternSuggestion:
    """A suggested pattern with reasoning."""

    name: str
    category: str  # "free" | "enterprise"
    reason: str
    confidence: float  # 0.0 to 1.0
    chain_position: int | None = None  # 1, 2, 3... if part of chain

    def to_dict(self) -> dict[str, Any]:
        """Export as dictionary."""
        return asdict(self)


@dataclass
class SuggestionResult:
    """Result of pattern suggestion."""

    question: str
    suggested_patterns: list[PatternSuggestion] = field(default_factory=list)
    suggested_chain: list[str] | None = None  # Ordered pattern names for chaining
    reasoning: str = ""
    source: str = "keyword"  # "keyword" | "llm" | "hybrid"
    llm_reasoning: str | None = None  # LLM's explanation (when hybrid/llm)

    def to_dict(self) -> dict[str, Any]:
        """Export as dictionary (for JSON, YAML, APIs)."""
        return {
            "question": self.question,
            "suggested_patterns": [s.to_dict() for s in self.suggested_patterns],
            "suggested_chain": self.suggested_chain,
            "reasoning": self.reasoning,
            "source": self.source,
            "llm_reasoning": self.llm_reasoning,
        }

    def to_markdown(self) -> str:
        """Export as human-readable Markdown (for display in notebooks, docs)."""
        lines = [f"### {self.question}\n"]
        lines.append(f"- **Source**: `{self.source}`")
        lines.append(f"- **Suggested**: `{', '.join(s.name for s in self.suggested_patterns)}`")
        if self.suggested_chain:
            lines.append(f"- **Workflow chain**: `{self.suggested_chain}`")
        else:
            lines.append("")
        lines.append("**Reasoning**:")
        for s in self.suggested_patterns:
            step = f" (step {s.chain_position})" if s.chain_position else ""
            lines.append(f"- `{s.name}`{step}: {s.reason}")
        if self.llm_reasoning:
            lines.append("\n**LLM raw**:")
            lines.append(
                f"> {self.llm_reasoning[:500]}{'...' if len(self.llm_reasoning) > 500 else ''}"
            )
        return "\n".join(lines)

    def to_json(self) -> str:
        """Export as JSON string (for APIs, storage)."""
        import json

        return json.dumps(self.to_dict(), indent=2)

    def to_yaml(self) -> str:
        """Export as YAML string (for configs, pipelines)."""
        import yaml

        return yaml.dump(self.to_dict(), default_flow_style=False, sort_keys=False)

    def to_xml(self) -> str:
        """Export as XML string (for XML-based systems)."""
        from xml.dom import minidom
        from xml.etree.ElementTree import Element, SubElement, tostring

        root = Element("suggestion_result")
        SubElement(root, "question").text = self.question
        SubElement(root, "source").text = self.source
        SubElement(root, "reasoning").text = self.reasoning
        if self.llm_reasoning:
            SubElement(root, "llm_reasoning").text = self.llm_reasoning
        chain_elem = SubElement(root, "suggested_chain")
        if self.suggested_chain:
            for name in self.suggested_chain:
                SubElement(chain_elem, "pattern").text = name
        patterns_elem = SubElement(root, "suggested_patterns")
        for s in self.suggested_patterns:
            p = SubElement(patterns_elem, "pattern")
            SubElement(p, "name").text = s.name
            SubElement(p, "category").text = s.category
            SubElement(p, "reason").text = s.reason
            SubElement(p, "confidence").text = str(s.confidence)
            if s.chain_position is not None:
                SubElement(p, "chain_position").text = str(s.chain_position)
        rough = tostring(root, encoding="unicode")
        reparsed = minidom.parseString(rough)
        return reparsed.toprettyxml(indent="  ")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SuggestionResult":
        """Create from dictionary (round-trip with to_dict)."""
        patterns = [
            PatternSuggestion(**p) if isinstance(p, dict) else p
            for p in data.get("suggested_patterns", [])
        ]
        return cls(
            question=data.get("question", ""),
            suggested_patterns=patterns,
            suggested_chain=data.get("suggested_chain"),
            reasoning=data.get("reasoning", ""),
            source=data.get("source", "keyword"),
            llm_reasoning=data.get("llm_reasoning"),
        )

    @classmethod
    def from_json(cls, json_str: str) -> "SuggestionResult":
        """Create from JSON string (round-trip with to_json)."""
        import json

        return cls.from_dict(json.loads(json_str))


def _try_suggest_routes(
    question: str,
    include_enterprise: bool,
    provider: str,
    temperature: float,
    model: str | None,
    **kwargs: Any,
):
    """Try to delegate to suggest_routes(); return None on any failure."""
    try:
        from .route_suggester import suggest_routes

        return suggest_routes(
            question=question,
            max_routes=1,
            include_enterprise=include_enterprise,
            provider=provider,
            temperature=temperature,
            model=model,
            **kwargs,
        )
    except Exception as exc:
        logger.debug(
            "suggest_patterns: suggest_routes delegation failed (%s), "
            "falling back to _suggest_with_llm. Error: %s",
            type(exc).__name__,
            exc,
        )
        return None


def suggest_patterns(
    question: str,
    include_enterprise: bool = True,
    suggest_chain: bool = True,
    max_patterns: int = 5,
    mode: str = "keyword",
    llm_provider: str = "openai",
    temperature: float = 0,
    model: str | None = None,
    **llm_kwargs: Any,
) -> SuggestionResult:
    """
    Suggest essential patterns for a given question.

    Always suggests from all 85 templates (free + enterprise). When include_enterprise=False,
    enterprise patterns still appear but with a note: "Requires enterprise license. Set include_enterprise=True to use."

    Args:
        question: The user's question or problem description
        include_enterprise: If False, enterprise patterns show license note (default True)
        suggest_chain: Suggest a chain order when multiple patterns apply
        max_patterns: Maximum patterns to suggest (default 5)
        mode: "keyword" (no LLM), "llm" (LLM only), "hybrid" (keyword + LLM merge)
        llm_provider: Provider for LLM mode ("openai", "anthropic", "gemini")
        temperature: LLM temperature (default 0 for determinism)
        model: Override model name
        **llm_kwargs: Extra kwargs passed to provider.generate()

    Returns:
        SuggestionResult with patterns, optional chain, and reasoning
    """
    keyword_result = _suggest_with_keywords(
        question, include_enterprise, suggest_chain, max_patterns
    )

    if mode == "keyword":
        return keyword_result

    if mode in ("llm", "hybrid"):
        # Primary path: delegate to suggest_routes() for richer intelligence
        kw_hints = [s.name for s in keyword_result.suggested_patterns]
        route_result = _try_suggest_routes(
            question,
            include_enterprise,
            llm_provider,
            temperature,
            model,
            **llm_kwargs,
        )
        if route_result is not None and route_result.routes:
            best = route_result.routes[0]
            names = [s.template for s in best.steps]
            reasons = {s.template: s.produces for s in best.steps}
            integration = route_result.recommendation
            if mode == "hybrid":
                kw_reasons = {s.name: s.reason for s in keyword_result.suggested_patterns}
                names = names + [n for n in kw_hints if n not in set(names)]
                names = names[:max_patterns]
                reasons = {**kw_reasons, **reasons}
            return _names_to_result(
                question,
                names,
                suggest_chain,
                max_patterns,
                "llm" if mode == "llm" else "hybrid",
                "",
                include_enterprise,
                reasons,
                integration,
            )

        # Fallback: original _suggest_with_llm if suggest_routes failed
        llm_selections, integration_note, llm_raw = _suggest_with_llm(
            question,
            llm_provider,
            temperature=temperature,
            model=model,
            keyword_hints=kw_hints if mode == "hybrid" else None,
            **llm_kwargs,
        )
        llm_names = [s[0] for s in llm_selections]
        llm_reasons = {s[0]: s[1] for s in llm_selections}

        if not llm_names and mode == "llm":
            return SuggestionResult(
                question=question,
                suggested_patterns=[],
                reasoning="LLM returned no valid patterns. Try keyword mode.",
                source="llm",
            )
        if mode == "llm":
            return _names_to_result(
                question,
                llm_names,
                suggest_chain,
                max_patterns,
                "llm",
                llm_raw,
                include_enterprise,
                llm_reasons,
                integration_note,
            )
        # hybrid: LLM selections are primary, keyword fills gaps
        kw_reasons = {s.name: s.reason for s in keyword_result.suggested_patterns}
        merged = llm_names + [n for n in kw_hints if n not in set(llm_names)]
        merged = merged[:max_patterns]
        merged_reasons = {**kw_reasons, **llm_reasons}
        return _names_to_result(
            question,
            merged,
            suggest_chain,
            max_patterns,
            "hybrid",
            llm_raw,
            include_enterprise,
            merged_reasons,
            integration_note,
        )

    return keyword_result


def _suggest_with_keywords(
    question: str,
    include_enterprise: bool,
    suggest_chain: bool,
    max_patterns: int,
) -> SuggestionResult:
    """Keyword-based suggestion. Always suggests from ALL patterns; adds license note for enterprise when include_enterprise=False."""
    question_lower = question.lower().strip()
    suggestions: list[PatternSuggestion] = []
    seen: set = set()

    for keywords, (pattern_name, category, reason) in PATTERN_MAP:
        if pattern_name in seen:
            continue
        for kw in keywords:
            if kw in question_lower:
                reason_text = f"Question mentions '{kw}' -> {reason}"
                if category == "enterprise" and not include_enterprise:
                    reason_text += ENTERPRISE_LICENSE_NOTE
                suggestions.append(
                    PatternSuggestion(
                        name=pattern_name,
                        category=category,
                        reason=reason_text,
                        confidence=0.85,
                    )
                )
                seen.add(pattern_name)
                break

    seen_unique: set = set()
    unique = []
    for s in suggestions:
        if s.name not in seen_unique:
            seen_unique.add(s.name)
            unique.append(s)
    suggestions = unique[:max_patterns]

    chain = None
    if suggest_chain and len(suggestions) >= 2:
        chain = _order_chain([s.name for s in suggestions])
        for s in suggestions:
            if s.name in chain:
                s.chain_position = chain.index(s.name) + 1
        by_name = {s.name: s for s in suggestions}
        suggestions = [by_name[n] for n in chain if n in by_name]

    reasoning_parts = []
    for s in suggestions:
        pos = f" (chain step {s.chain_position})" if s.chain_position else ""
        reasoning_parts.append(f"- {s.name}{pos}: {s.reason}")
    reasoning = (
        "\n".join(reasoning_parts) if reasoning_parts else "No strong match. Try question_analyzer."
    )

    return SuggestionResult(
        question=question,
        suggested_patterns=suggestions,
        suggested_chain=chain,
        reasoning=reasoning,
        source="keyword",
    )


def _suggest_with_llm(
    question: str,
    provider: str,
    temperature: float = 0,
    model: str | None = None,
    keyword_hints: list[str] | None = None,
    **kwargs: Any,
) -> tuple:
    """Call LLM to suggest patterns. Returns (list of (name, reason) tuples, integration_note, raw_text)."""
    from ..core import Context
    from ..foundation import Directive, Guidance

    hint_block = ""
    if keyword_hints:
        hint_block = (
            f"\nKeyword analysis already identified these candidates: {', '.join(keyword_hints)}\n"
            "You may keep, replace, or add to these. Think beyond the obvious.\n"
        )

    prompt = f"""USER QUESTION: "{question}"
{hint_block}
TEMPLATE CATALOG (85 cognitive reasoning frameworks, grouped by theme):
{ENRICHED_CATALOG_TEXT}

INSTRUCTIONS:
Think step-by-step about which templates would best address this question.
1. Identify the DOMAINS involved (business, technical, ethical, legal, scientific, etc.)
2. Identify the REASONING TYPE needed (diagnostic, comparative, strategic, creative, ethical, etc.)
3. Select 2-4 templates that DIRECTLY address the question's core requirements. Each must earn its place — do not add templates for marginal relevance.
4. Order them as a pipeline (what to apply first → last).
5. Explain WHY each template is needed for THIS specific question.

RESPOND IN THIS EXACT FORMAT:

TEMPLATE: exact_template_name
REASON: 1-2 sentences explaining why this is needed for the user's specific question

TEMPLATE: exact_template_name
REASON: 1-2 sentences...

(repeat for each)

INTEGRATION: 2-3 sentences explaining how these templates work together as a pipeline — what each stage contributes and why the combination produces better results than any single template."""

    from .schemas import (
        PatternSuggestionResponse,
        get_instructor_client,
        parse_with_fallback,
    )

    exec_kw: dict = {"temperature": temperature, **kwargs}
    if model:
        exec_kw["model"] = model
    resolved_model = exec_kw.get("model", "gpt-4o-mini")

    # ── Attempt instructor-structured path ───────────────────────────────────
    instructor_client = get_instructor_client(None)
    if instructor_client is not None:
        try:
            system_msg = (
                "You are an expert cognitive pattern architect. You match reasoning "
                "frameworks to questions with surgical precision, selecting from a "
                "catalog of 85 templates. Use ONLY exact snake_case names from the "
                "catalog. Select 2-4 templates in pipeline order."
            )
            response = instructor_client.chat.completions.create(
                model=resolved_model,
                response_model=PatternSuggestionResponse,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt},
                ],
                max_retries=2,
            )
            selections = [(s.name, s.reason) for s in response.selections]
            return (selections[:5], response.integration, "")
        except Exception as exc:
            logger.debug(
                "_suggest_with_llm: instructor path failed (%s), falling back to "
                "regex parse. Error: %s",
                type(exc).__name__,
                exc,
            )

    # ── Fallback: classic LLM call + Pydantic parse ──────────────────────────
    try:
        ctx = Context(
            guidance=Guidance(
                role="Expert cognitive pattern architect. You match reasoning frameworks to questions with surgical precision, selecting from a catalog of 85 templates.",
                rules=[
                    "Use ONLY template names from the catalog. Exact snake_case names.",
                    "Select 2-4 templates. Quality over quantity — each template must directly address a core aspect of the question.",
                    "Order them as a pipeline: investigation/analysis first, then reasoning/comparison, then synthesis/decision last.",
                    "Each REASON must be specific to the user's question, not generic.",
                    'Respond as valid JSON: {"selections":[{"name":"...","reason":"..."},...],"integration":"..."}',
                ],
            ),
            directive=Directive(content=prompt),
        )
        result = ctx.execute(provider=provider, **exec_kw)
        raw = result.response.strip()

        # Try Pydantic parse first, fall back to regex if needed
        try:
            parsed = parse_with_fallback(PatternSuggestionResponse, raw)
            selections = [(s.name, s.reason) for s in parsed.selections]
            return (selections[:5], parsed.integration, raw)
        except (ValueError, Exception):
            return _parse_llm_structured_response_regex(raw)

    except Exception as e:
        logger.warning(
            "_suggest_with_llm: LLM suggestion call failed (%s). "
            "Returning empty suggestions; caller will fall back to keyword mode. Error: %s",
            type(e).__name__,
            e,
            exc_info=True,
        )
        return ([], "", str(e))


def _parse_llm_structured_response_regex(raw: str) -> tuple:
    """Regex fallback parser — used when JSON parse fails."""
    import re as _re

    selections: list[tuple] = []
    integration = ""

    template_pattern = _re.compile(r"TEMPLATE:\s*(\S+)", _re.IGNORECASE)
    reason_pattern = _re.compile(r"REASON:\s*(.+)", _re.IGNORECASE)
    integration_pattern = _re.compile(r"INTEGRATION:\s*(.+)", _re.IGNORECASE | _re.DOTALL)

    int_match = integration_pattern.search(raw)
    if int_match:
        integration = int_match.group(1).strip().split("\n")[0].strip()

    template_matches = list(template_pattern.finditer(raw))
    for i, tm in enumerate(template_matches):
        name = tm.group(1).strip().lower().replace("-", "_").replace(" ", "_")
        if name not in VALID_PATTERN_NAMES:
            continue
        search_start = tm.end()
        search_end = (
            template_matches[i + 1].start()
            if i + 1 < len(template_matches)
            else (int_match.start() if int_match else len(raw))
        )
        chunk = raw[search_start:search_end]
        rm = reason_pattern.search(chunk)
        reason = rm.group(1).strip() if rm else "Selected by AI"
        selections.append((name, reason))

    if not selections:
        for part in raw.replace("\n", ",").split(","):
            name = part.strip().lower().replace("-", "_").replace(" ", "_")
            if name in VALID_PATTERN_NAMES:
                selections.append((name, "Selected by AI"))

    return (selections[:5], integration, raw)


def _names_to_result(
    question: str,
    names: list[str],
    suggest_chain: bool,
    max_patterns: int,
    source: str,
    llm_reasoning: str | None = None,
    include_enterprise: bool = True,
    per_template_reasons: dict | None = None,
    integration_note: str | None = None,
) -> SuggestionResult:
    """Convert list of pattern names to SuggestionResult. Adds license note when include_enterprise=False."""
    per_template_reasons = per_template_reasons or {}
    suggestions = []
    for name in names[:max_patterns]:
        cat = NAME_TO_CATEGORY.get(name, "free")
        reason = per_template_reasons.get(name, f"Selected by {source}")
        if cat == "enterprise" and not include_enterprise:
            reason += ENTERPRISE_LICENSE_NOTE
        suggestions.append(
            PatternSuggestion(
                name=name,
                category=cat,
                reason=reason,
                confidence=0.9 if source in ("llm", "hybrid") else 0.85,
            )
        )

    chain = _order_chain(names) if suggest_chain and len(names) >= 2 else None
    if chain:
        for s in suggestions:
            if s.name in chain:
                s.chain_position = chain.index(s.name) + 1
        by_chain = {s.name: s for s in suggestions}
        suggestions = [by_chain[n] for n in chain if n in by_chain]

    reasoning = integration_note or ""
    return SuggestionResult(
        question=question,
        suggested_patterns=suggestions,
        suggested_chain=chain,
        reasoning=reasoning,
        source=source,
        llm_reasoning=llm_reasoning,
    )


def _order_chain(pattern_names: list[str]) -> list[str]:
    """Order patterns into a sensible workflow chain."""
    order_priority = {
        "temporal_sequence_analyzer": 1,
        "historical_context_mapper": 2,
        "diagnostic_root_cause_analyzer": 3,
        "root_cause_analyzer": 3,  # free RCA
        "causal_reasoner": 4,
        "differential_diagnoser": 5,
        "future_scenario_planner": 6,
        "pattern_recognition_engine": 7,
        "cross_domain_synthesizer": 8,
        "holistic_integrator": 9,
    }
    others = [p for p in pattern_names if p not in order_priority]
    ordered = sorted(
        [p for p in pattern_names if p in order_priority],
        key=lambda x: order_priority[x],
    )
    return ordered + others


def get_pattern_class(pattern_name: str, include_enterprise: bool = True):
    """
    Get the Pattern class for a given pattern name.

    Delegates to the unified pattern registry. When include_enterprise=False
    and pattern is enterprise, returns None and emits a warning directing the
    user to either activate an enterprise license or use a free template.

    Pattern classes are stateless definitions — the result is cached with
    functools.lru_cache so repeated lookups (e.g., inside compose_from_templates
    or parallel refinement loops) pay the import cost only once.
    """
    import warnings

    category = NAME_TO_CATEGORY.get(pattern_name)
    if category is None:
        return None
    if category == "enterprise" and not include_enterprise:
        warnings.warn(
            f"Template '{pattern_name}' requires an enterprise license. "
            f"Activate with: mycontext.activate_license('MC-ENT-...'). "
            f"Free alternatives (16 templates) are available — use "
            f"include_enterprise=False to route to them automatically.",
            UserWarning,
            stacklevel=2,
        )
        return None
    return _get_pattern_class_cached(pattern_name)


import functools as _functools  # noqa: E402 — placed after the function that calls it


@_functools.lru_cache(maxsize=256)
def _get_pattern_class_cached(pattern_name: str):
    """LRU-cached registry lookup — called only after access control checks."""
    from ..skills.pattern_registry import get_pattern_registry

    registry = get_pattern_registry()
    return registry.get(pattern_name)


# ---------------------------------------------------------------------------
# Complexity Router — decide IF templates will help before selecting them
# ---------------------------------------------------------------------------


@dataclass
class ComplexityResult:
    """Result of question complexity assessment."""

    complexity: str  # "low", "medium", "high"
    domains: list[str]  # e.g. ["business", "technical", "ethical"]
    reasoning_type: str  # "diagnostic", "comparative", "strategic", etc.
    recommendation: str  # "raw", "single_template", "integrated"
    reasoning: str  # why this recommendation
    best_template: str | None = None  # for "single_template" recommendation

    def to_dict(self) -> dict[str, Any]:
        return {
            "complexity": self.complexity,
            "domains": self.domains,
            "reasoning_type": self.reasoning_type,
            "recommendation": self.recommendation,
            "reasoning": self.reasoning,
            "best_template": self.best_template,
        }


# ---------------------------------------------------------------------------
# Heuristic pre-screen for assess_complexity
# ---------------------------------------------------------------------------
#
# Research basis:
#   "System 1 / System 2" (Kahneman, 2011): fast heuristic decisions avoid
#   the cost of deliberate reasoning for routine cases.  Applied here: a
#   cheap lexical screen handles obvious questions so the expensive LLM call
#   is reserved for genuinely ambiguous inputs.
#
#   DistilBERT-based LLM routing (Ding et al., 2024, arXiv:2406.18665):
#   Lightweight classifiers applied before expensive models reduce cost by
#   40–60% with negligible accuracy loss.
#
#   This implementation uses zero external dependencies — pure regex + token
#   counting — making it sub-millisecond and safe in all environments.
#
# Confidence design:
#   0.9  Very high — single-fact questions (what is X?), greetings, arithmetic
#   0.75 High  — short questions with well-known answer patterns
#   0.0  Uncertain — pass to LLM

# Tokens below this → almost certainly "raw" (no scaffolding needed)
_HEURISTIC_SHORT_TOKEN_LIMIT = 15

# Signals that the question is genuinely complex (overrides short-length shortcut)
_COMPLEX_SIGNALS = re.compile(
    # Prefixes like "strateg" match "strategy", "strategic", "strategies" etc.
    # No trailing \b because these are prefix patterns, not full words.
    r"\b(strateg|roadmap|prioriti|trade.?off|recommend|analyz|compar|evaluat|"
    r"assess|risk|impact|diagnos|root.cause|investigat|framework|stakeholder|"
    r"organiz|systemic|policy|forecast|scenario|ethic|multi.domain|multi.facet|"
    r"compet|regulat)",
    re.IGNORECASE,
)

# Signals that raw is definitely fine (simple factual / greeting / arithmetic)
_RAW_SIGNALS = re.compile(
    r"^(what is|what are|who is|who was|when did|where is|how do i|how does|"
    r"define |tell me |explain |describe |list |give me |show me |can you |"
    r"please |hi |hello |hey )",
    re.IGNORECASE,
)

# Arithmetic-only expression (ignore whitespace and common operators)
_ARITHMETIC_RE = re.compile(r"^[\d\s\+\-\*\/\^\(\)\.]+[=?]?\s*$")


def _heuristic_classify(question: str) -> ComplexityResult | None:
    """Return a ``ComplexityResult`` if the question can be classified cheaply.

    Returns ``None`` when the heuristic is uncertain, meaning the full LLM
    assessment should be used.

    This function never calls an LLM, has O(1) runtime, and is thread-safe.
    """
    stripped = question.strip()
    if not stripped:
        return None

    # Pure arithmetic → raw, no templates needed
    if _ARITHMETIC_RE.match(stripped):
        return ComplexityResult(
            complexity="low",
            domains=["mathematics"],
            reasoning_type="analytical",
            recommendation="raw",
            reasoning="Arithmetic expression detected — no cognitive template needed.",
        )

    from ..utils.tokens import count_tokens

    token_count = count_tokens(stripped)

    # Very short questions without complexity signals → raw
    if token_count <= _HEURISTIC_SHORT_TOKEN_LIMIT:
        has_complex = bool(_COMPLEX_SIGNALS.search(stripped))
        if not has_complex:
            return ComplexityResult(
                complexity="low",
                domains=[],
                reasoning_type="explanatory",
                recommendation="raw",
                reasoning=(
                    f"Short question ({token_count} tokens) with no multi-domain "
                    "complexity signals — heuristic pre-screen classified as raw."
                ),
            )

    # Questions starting with a simple factual opener AND no complexity signals → raw
    if _RAW_SIGNALS.match(stripped) and not _COMPLEX_SIGNALS.search(stripped):
        return ComplexityResult(
            complexity="low",
            domains=[],
            reasoning_type="explanatory",
            recommendation="raw",
            reasoning=(
                "Simple factual or definitional question detected by heuristic "
                "pre-screen — no template scaffolding needed."
            ),
        )

    # Uncertain — let the LLM decide
    return None


def assess_complexity(
    question: str,
    provider: str = "openai",
    temperature: float = 0,
    model: str | None = None,
    skip_heuristic: bool = False,
    **kwargs: Any,
) -> ComplexityResult:
    """Assess question complexity to decide if templates will help.

    Routes:
    - low complexity (single domain, well-known): recommend "raw"
    - medium (single domain, specialized): recommend "single_template"
    - high (multi-domain, ambiguous, novel): recommend "integrated"

    Args:
        skip_heuristic: Force the full LLM assessment even for questions that
                        would normally be classified by the heuristic pre-screen.
                        Useful for evaluation and testing.
    """
    # ── Heuristic fast-path — skips LLM for obviously simple questions ─────
    if not skip_heuristic:
        heuristic_result = _heuristic_classify(question)
        if heuristic_result is not None:
            logger.debug(
                "assess_complexity: heuristic fast-path → %s (%s)",
                heuristic_result.recommendation,
                heuristic_result.reasoning,
            )
            return heuristic_result

    from ..core import Context
    from ..foundation import Directive, Guidance

    prompt = f"""Assess this question's complexity for deciding whether cognitive reasoning templates will add value.

QUESTION: "{question}"

AVAILABLE TEMPLATE CATALOG (use exact snake_case names):
{ENRICHED_CATALOG_TEXT}

Classify along these dimensions:

1. COMPLEXITY: "low" | "medium" | "high"
   - low: Single domain, well-known topic, straightforward answer structure
   - medium: Single domain but specialized, benefits from structured analytical framework
   - high: Multi-domain (spans technical + business + ethical + legal etc.), ambiguous, or requires novel reasoning

2. DOMAINS: List the knowledge domains involved (e.g. "business", "technical", "ethical", "legal", "medical", "organizational")

3. REASONING_TYPE: What kind of reasoning is needed?
   - diagnostic (why did X happen?)
   - comparative (A vs B vs C?)
   - strategic (what should we do?)
   - creative (generate new ideas)
   - ethical (evaluate moral implications)
   - analytical (analyze data/information)
   - explanatory (explain or teach something)

4. RECOMMENDATION: "raw" | "single_template" | "integrated"
   - raw: LLM can answer well without scaffolding (simple, well-known topics)
   - single_template: One specialized template adds clear value
   - integrated: Multiple frameworks needed for multi-domain complexity

5. BEST_TEMPLATE: If recommendation is "single_template", pick the SINGLE best template from the catalog above. Use the exact snake_case name. Leave empty string for "raw" or "integrated".

Respond in this EXACT JSON format:
{{"complexity": "...", "domains": [...], "reasoning_type": "...", "recommendation": "...", "best_template": "...", "reasoning": "1-2 sentences explaining why"}}

Respond with ONLY valid JSON."""

    try:
        ctx = Context(
            guidance=Guidance(
                role="Question complexity assessor",
                rules=[
                    "Be conservative: recommend templates ONLY when they clearly add value.",
                    "Most straightforward questions are best answered raw.",
                    "Recommend integration only for genuinely multi-domain problems.",
                ],
            ),
            directive=Directive(content=prompt),
        )
        exec_kw: dict = {"temperature": temperature, **kwargs}
        if model:
            exec_kw["model"] = model
        result = ctx.execute(provider=provider, **exec_kw)
        raw = result.response.strip()
        if raw.startswith("```"):
            lines = raw.split("\n")
            raw = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])

        import json

        data = json.loads(raw)
        best_tpl = data.get("best_template", "") or None
        if best_tpl and best_tpl not in VALID_PATTERN_NAMES:
            best_tpl = None
        return ComplexityResult(
            complexity=data.get("complexity", "medium"),
            domains=data.get("domains", []),
            reasoning_type=data.get("reasoning_type", "analytical"),
            recommendation=data.get("recommendation", "raw"),
            reasoning=data.get("reasoning", ""),
            best_template=best_tpl,
        )
    except Exception as e:
        return ComplexityResult(
            complexity="medium",
            domains=[],
            reasoning_type="analytical",
            recommendation="raw",
            reasoning=f"Assessment failed ({e}), defaulting to raw.",
        )


# ---------------------------------------------------------------------------
# Shared routing logic — used by smart_execute / smart_prompt / smart_generic_prompt
# ---------------------------------------------------------------------------


def _resolve_routing(
    question: str,
    provider: str,
    include_enterprise: bool,
    model: str | None,
    **kwargs: Any,
) -> tuple[str, list[str], "ComplexityResult"]:
    """Assess complexity and resolve the template list for a question.

    Returns:
        (tier, template_names, assessment)
        tier: "raw" | "single" | "multi"
        template_names: list of resolved template names (empty for "raw")
        assessment: ComplexityResult
    """
    assessment = assess_complexity(question, provider=provider, model=model, **kwargs)

    if assessment.recommendation == "raw":
        return "raw", [], assessment

    if assessment.recommendation == "single_template" and assessment.best_template:
        klass = get_pattern_class(assessment.best_template, include_enterprise=include_enterprise)
        if klass is not None:
            return "single", [assessment.best_template], assessment

    # "integrated" tier, or single_template fallback when class not found
    suggestion = suggest_patterns(
        question,
        include_enterprise=include_enterprise,
        max_patterns=3,
        mode="hybrid",
        llm_provider=provider,
        model=model,
    )
    names = [s.name for s in suggestion.suggested_patterns[:3]]
    if names:
        return "multi", names, assessment

    # Last resort — treat as raw
    return "raw", [], assessment


# ---------------------------------------------------------------------------
# Public smart_ functions — thin wrappers over _resolve_routing
# ---------------------------------------------------------------------------


def smart_execute(
    question: str,
    provider: str = "openai",
    include_enterprise: bool = True,
    model: str | None = None,
    **kwargs: Any,
):
    """Intelligently execute a question using the complexity router.

    Automatically decides whether to use raw execution, a single template,
    or integrated templates based on question complexity.

    Returns:
        tuple: (response_text, execution_metadata_dict)
    """
    from ..core import Context
    from ..foundation import Directive
    from .chain_orchestration_agent import PATTERN_BUILD_CONTEXT_REGISTRY
    from .template_integrator_agent import TemplateIntegratorAgent

    tier, template_names, assessment = _resolve_routing(
        question, provider, include_enterprise, model, **kwargs
    )
    meta: dict = {"assessment": assessment.to_dict(), "mode": tier}
    exec_kw: dict = dict(kwargs)
    if model:
        exec_kw["model"] = model

    if tier == "raw":
        ctx = Context(directive=Directive(content=question))
        result = ctx.execute(provider=provider, **exec_kw)
        meta["templates_used"] = []
        return result.response, meta

    if tier == "single":
        tpl_name = template_names[0]
        klass = get_pattern_class(tpl_name, include_enterprise=include_enterprise)
        if klass:
            reg = PATTERN_BUILD_CONTEXT_REGISTRY.get(tpl_name, ("input", {}))
            primary_key, defaults = reg
            params = {**defaults, primary_key: question}
            ctx = klass().build_context(**params)
            result = ctx.execute(provider=provider, **exec_kw)
            meta["templates_used"] = [tpl_name]
            return result.response, meta

    # "multi" tier
    integrator = TemplateIntegratorAgent(include_enterprise=include_enterprise)
    integration = integrator.suggest_and_integrate(
        question=question,
        provider=provider,
        max_patterns=3,
        integration_mode="focused",
        **kwargs,
    )
    ctx = integration.to_context()
    result = ctx.execute(provider=provider, **exec_kw)
    meta["templates_used"] = integration.source_templates
    return result.response, meta


def smart_prompt(
    question: str,
    provider: str = "openai",
    include_enterprise: bool = True,
    model: str | None = None,
    refine: bool = True,
    **kwargs: Any,
):
    """One-liner: analyze question, select templates, compose an optimized prompt.

    Uses the complexity router to decide which templates to apply, then
    generates and composes their prompts into a single, provider-agnostic
    prompt string.

    Args:
        question: The user's question or problem description.
        provider: LLM provider for prompt generation/refinement.
        include_enterprise: Include enterprise templates if licensed.
        model: Override model name.
        refine: Whether to LLM-refine individual template prompts before composing.

    Returns:
        ComposedPrompt that can be executed (``.execute()``) or exported
        (``.to_string()``).

    Example::

        >>> from mycontext.intelligence import smart_prompt
        >>> cp = smart_prompt("Why did churn spike 40%?")
        >>> print(cp.to_string())   # get the optimized prompt
        >>> print(cp.execute())     # or execute it directly
    """
    from .chain_orchestration_agent import PATTERN_BUILD_CONTEXT_REGISTRY
    from .prompt_composer import ComposedPrompt, PromptComposer

    _RAW_PROMPT = (
        f"Answer this question thoroughly and provide actionable recommendations:\n\n{question}"
    )

    tier, template_names, assessment = _resolve_routing(
        question, provider, include_enterprise, model, **kwargs
    )

    if tier == "raw":
        return ComposedPrompt(
            prompt=_RAW_PROMPT,
            source_templates=[],
            question=question,
            metadata={"assessment": assessment.to_dict(), "mode": "raw"},
        )

    if tier == "single":
        tpl_name = template_names[0]
        klass = get_pattern_class(tpl_name, include_enterprise=include_enterprise)
        if klass:
            reg = PATTERN_BUILD_CONTEXT_REGISTRY.get(tpl_name, ("input", {}))
            primary_key, defaults = reg
            params = {**defaults, primary_key: question}
            ctx = klass().build_context(**params)
            prompt = ctx.to_prompt(refine=refine, provider=provider, model=model)
            return ComposedPrompt(
                prompt=prompt,
                source_templates=[tpl_name],
                question=question,
                component_prompts=[prompt],
                metadata={"assessment": assessment.to_dict(), "mode": "single_template"},
            )

    # "multi" tier
    if not template_names:
        return ComposedPrompt(
            prompt=_RAW_PROMPT,
            source_templates=[],
            question=question,
            metadata={"assessment": assessment.to_dict(), "mode": "integrated_fallback"},
        )

    composer = PromptComposer(
        include_enterprise=include_enterprise,
        provider=provider,
        model=model or "gpt-4o-mini",
    )
    result = composer.compose_from_templates(
        question=question,
        template_names=template_names,
        refine=refine,
        provider=provider,
        model=model,
    )
    result.metadata["assessment"] = assessment.to_dict()
    result.metadata["mode"] = "composed"
    return result


def smart_generic_prompt(
    question: str,
    provider: str = "openai",
    include_enterprise: bool = True,
    model: str | None = None,
    **kwargs: Any,
):
    """One-liner: select templates via complexity router, compile generic prompts statically.

    This is the zero-cost counterpart to ``smart_prompt()``.  Instead of
    LLM-refined prompts, it uses the pre-authored generic prompts and
    merges them via pure string operations — **no LLM calls for compilation**.

    The only LLM call is the complexity assessment itself (one cheap call).

    Args:
        question: The user's question or problem description.
        provider: LLM provider for the complexity assessment.
        include_enterprise: Include enterprise templates if licensed.
        model: Override model name.

    Returns:
        ComposedPrompt with a statically compiled generic prompt.

    Example::

        >>> from mycontext.intelligence import smart_generic_prompt
        >>> cp = smart_generic_prompt("Why did churn spike 40%?")
        >>> print(cp.to_string())   # zero-LLM-cost prompt
        >>> print(cp.execute())     # execute it with one LLM call
    """
    from .prompt_composer import ComposedPrompt, PromptComposer

    _RAW_PROMPT = (
        f"Answer this question thoroughly and provide actionable recommendations:\n\n{question}"
    )

    tier, template_names, assessment = _resolve_routing(
        question, provider, include_enterprise, model, **kwargs
    )

    if tier == "raw":
        return ComposedPrompt(
            prompt=_RAW_PROMPT,
            source_templates=[],
            question=question,
            metadata={"assessment": assessment.to_dict(), "mode": "raw"},
        )

    if not template_names:
        return ComposedPrompt(
            prompt=_RAW_PROMPT,
            source_templates=[],
            question=question,
            metadata={"assessment": assessment.to_dict(), "mode": "generic_fallback"},
        )

    composer = PromptComposer(
        include_enterprise=include_enterprise,
        provider=provider,
        model=model or "gpt-4o-mini",
    )
    result = composer.compile_generic(
        question=question,
        template_names=template_names,
    )
    result.metadata["assessment"] = assessment.to_dict()
    result.metadata["mode"] = "generic_compiled"
    return result
