"""
Eval Criteria — Pre-built DeepEval GEval criteria for mycontext outputs.

Provides a catalog of ready-to-use GEval metric definitions, grouped by
evaluation purpose. Use these with DeepEval's GEval metric to avoid writing
rubric prompts from scratch.

Design philosophy (borrowed from OpenAI Evals open-source rubrics):
  - Each criterion has ONE clear question it answers.
  - Rubrics use a numeric scale (0–10) with labeled anchor points.
  - Criteria are composable — combine them for richer evaluations.

Usage::

    from mycontext.intelligence.eval_criteria import (
        EVIDENCE_CITATION,
        CAUSATION_DISCIPLINE,
        DATA_GAP_HONESTY,
        INSTRUCTION_ADHERENCE,
        ACTIONABILITY,
        REASONING_SOUNDNESS,
        get_criteria,
        CATALOG,
    )

    # Use with DeepEval (requires: pip install deepeval)
    from deepeval.metrics import GEval
    from deepeval.test_case import LLMTestCase

    metric = GEval(
        name=EVIDENCE_CITATION.name,
        criteria=EVIDENCE_CITATION.criteria,
        evaluation_steps=EVIDENCE_CITATION.evaluation_steps,
    )

    # Or get a pre-assembled bundle:
    criteria_bundle = get_criteria("data_analysis")
    metrics = [GEval(name=c.name, criteria=c.criteria, evaluation_steps=c.evaluation_steps)
               for c in criteria_bundle]

Research basis:
  - OpenAI Evals (github.com/openai/evals) — rubric structure and anchor-point design
  - Habernal & Gurevych (2016) — argument quality decomposition
  - IFEval (Zhou et al. 2023) — instruction-following evaluation
  - FLASK benchmark (Ye et al. 2023) — fine-grained LLM evaluation dimensions
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class GEvalCriteria:
    """
    A single GEval criterion definition, ready to pass to ``deepeval.metrics.GEval``.

    Attributes:
        name:             Short identifier used as the metric name.
        description:      One-sentence explanation of what this measures.
        criteria:         The rubric question (passed to GEval's ``criteria`` arg).
        evaluation_steps: Ordered steps the LLM judge should follow (``evaluation_steps`` arg).
        tags:             Category tags for filtering via ``get_criteria()``.
        threshold:        Minimum passing score (0.0–1.0). Default 0.5.
    """

    name: str
    description: str
    criteria: str
    evaluation_steps: list[str]
    tags: list[str] = field(default_factory=list)
    threshold: float = 0.5


# ── Core analytical quality criteria ────────────────────────────────────────

EVIDENCE_CITATION = GEvalCriteria(
    name="evidence_citation",
    description="Does every factual claim or pattern cite a specific metric, value, or data point?",
    criteria=(
        "Does the response cite specific evidence (metrics, numbers, percentages, named entities, "
        "or concrete data points) to support every factual claim it makes? "
        "Unsupported assertions like 'performance declined' or 'users were unhappy' without "
        "a specific measure score low."
    ),
    evaluation_steps=[
        "Read each factual claim or identified pattern in the response.",
        "For each claim, check whether it is supported by a specific metric, number, date, "
        "percentage, or named data point.",
        "Count supported claims vs. total claims.",
        "Score 0–10: 0 = no evidence cited anywhere; 5 = roughly half of claims are evidenced; "
        "10 = every claim traces to a specific, named data point.",
    ],
    tags=["data_analysis", "reasoning", "general"],
    threshold=0.5,
)

CAUSATION_DISCIPLINE = GEvalCriteria(
    name="causation_discipline",
    description="Does the response correctly distinguish correlation from causation?",
    criteria=(
        "When the response identifies a relationship between two variables (e.g. 'X increased "
        "as Y increased'), does it explicitly note whether this is a correlation or a demonstrated "
        "causal relationship? Does it avoid asserting causation without evidence of a mechanism?"
    ),
    evaluation_steps=[
        "Identify all statements in the response that describe a relationship between two variables.",
        "For each relationship statement, determine whether the response claims correlation, "
        "causation, or is ambiguous.",
        "A causal claim requires either: (a) a stated mechanism, (b) an experimental design "
        "(A/B test, controlled study), or (c) an explicit caveat acknowledging it is correlational.",
        "Score 0–10: 0 = multiple causal claims with no support; 5 = most correlations are "
        "labelled but some causal overreach present; 10 = every relationship is correctly typed "
        "and caveated.",
    ],
    tags=["data_analysis", "reasoning"],
    threshold=0.5,
)

DATA_GAP_HONESTY = GEvalCriteria(
    name="data_gap_honesty",
    description=(
        "When data is insufficient to answer a question, does the response say so explicitly "
        "rather than speculate?"
    ),
    criteria=(
        "If the input data is insufficient to answer a goal or sub-question, does the response "
        "explicitly state what is missing, why it matters, and what would be needed — rather than "
        "filling the gap with speculation or hedged guesses?"
    ),
    evaluation_steps=[
        "Identify any goals or questions in the prompt that the available data cannot fully answer.",
        "Check whether the response addresses each of these gaps explicitly.",
        "A good gap statement names: (1) what data is absent, (2) which conclusion it prevents, "
        "(3) what data would resolve it. A poor gap statement speculates or gives a hedged answer.",
        "Score 0–10: 0 = no gaps acknowledged, speculation present; 5 = some gaps mentioned "
        "but without specifics; 10 = every data gap is named, blocked conclusion identified, "
        "and required data specified.",
    ],
    tags=["data_analysis", "honesty", "general"],
    threshold=0.5,
)

INSTRUCTION_ADHERENCE = GEvalCriteria(
    name="instruction_adherence",
    description="Does the response follow the specific instructions given in the prompt?",
    criteria=(
        "Does the response follow all explicit instructions in the prompt? "
        "This includes: output format (sections, lists, JSON), required content items, "
        "ordering of sections, length constraints, and any must-include or must-not-include rules."
    ),
    evaluation_steps=[
        "List all explicit instructions in the prompt (format, required sections, constraints).",
        "For each instruction, check whether the response complied.",
        "Note any instruction that was ignored, partially followed, or contradicted.",
        "Score 0–10: 0 = most instructions ignored; 5 = roughly half followed; "
        "10 = every instruction followed with no omissions.",
    ],
    tags=["general", "instruction_following"],
    threshold=0.6,
)

ACTIONABILITY = GEvalCriteria(
    name="actionability",
    description="Are the recommendations concrete and implementable, not just general advice?",
    criteria=(
        "Are the recommendations in the response concrete enough to act on immediately? "
        "Each recommendation should specify: (1) what to do, (2) who should do it or what "
        "system is affected, and (3) a timeframe or measurable target. Generic advice like "
        "'improve your process' or 'consider monitoring' scores low."
    ),
    evaluation_steps=[
        "Identify all recommendation or next-step statements in the response.",
        "For each recommendation, check whether it specifies: an action verb, an owner/target, "
        "and a timeframe or success metric.",
        "Recommendations that hedge ('you might consider', 'it could help to') lose points.",
        "Score 0–10: 0 = only vague suggestions; 5 = some recommendations have specifics; "
        "10 = every recommendation is a concrete, ownable, time-bound action.",
    ],
    tags=["general", "reasoning", "data_analysis"],
    threshold=0.5,
)

REASONING_SOUNDNESS = GEvalCriteria(
    name="reasoning_soundness",
    description="Is the reasoning logically sound — no contradictions, unsupported leaps, or circular logic?",
    criteria=(
        "Is the reasoning in the response logically sound? Check for: (1) conclusions that "
        "follow from the stated evidence, (2) absence of contradictions between sections, "
        "(3) no circular arguments, and (4) explicit handling of counter-evidence or alternative "
        "explanations where relevant."
    ),
    evaluation_steps=[
        "Trace the main argument chain: premises → intermediate conclusions → final conclusions.",
        "Check each step: does the conclusion follow from the stated evidence?",
        "Identify any contradictions between different parts of the response.",
        "Check whether obvious counter-evidence or alternative explanations were acknowledged.",
        "Score 0–10: 0 = major logical flaws or contradictions; 5 = mostly sound with "
        "one or two unsupported leaps; 10 = fully coherent, evidence-grounded reasoning.",
    ],
    tags=["reasoning", "general"],
    threshold=0.5,
)

STRUCTURE_COMPLIANCE = GEvalCriteria(
    name="structure_compliance",
    description="Does the output follow the requested section structure or format exactly?",
    criteria=(
        "Does the response follow the exact section structure, format, or schema requested in "
        "the prompt? If a numbered section list was requested, are all sections present in order? "
        "If JSON was requested, is it valid and complete? If a specific heading format was "
        "requested, is it used consistently?"
    ),
    evaluation_steps=[
        "Extract the required output structure from the prompt (sections, format, schema).",
        "Check whether every required section or field is present in the response.",
        "Check whether sections appear in the requested order.",
        "Check formatting consistency (heading levels, numbering, JSON validity).",
        "Score 0–10: 0 = structure completely ignored; 5 = roughly half the structure present; "
        "10 = exact structure match, every section present and correctly formatted.",
    ],
    tags=["general", "instruction_following"],
    threshold=0.6,
)

COGNITIVE_SCAFFOLDING_USE = GEvalCriteria(
    name="cognitive_scaffolding_use",
    description="Does the response actively use the analytical framework the prompt was designed to apply?",
    criteria=(
        "If the prompt was built around a specific analytical framework (root cause analysis, "
        "SWOT, causal reasoning, risk assessment, etc.), does the response actually apply that "
        "framework — naming its components and structuring the output accordingly — or does it "
        "give a generic answer that ignores the framework?"
    ),
    evaluation_steps=[
        "Identify the analytical framework(s) the prompt was designed to apply.",
        "Check whether the response explicitly names and applies the framework's components "
        "(e.g. for root cause: symptoms → contributing factors → root cause → corrective action).",
        "Check whether the response structure mirrors the framework structure.",
        "Score 0–10: 0 = framework completely ignored, generic answer given; "
        "5 = framework partially applied with some components present; "
        "10 = framework fully applied with all key components explicitly addressed.",
    ],
    tags=["reasoning", "general"],
    threshold=0.5,
)

# ── Code review specific ─────────────────────────────────────────────────────

CODE_REVIEW_SEVERITY_ACCURACY = GEvalCriteria(
    name="code_review_severity_accuracy",
    description="Are code review findings assigned the correct severity level?",
    criteria=(
        "Are the severity levels assigned to code review findings appropriate? "
        "Critical issues (security vulnerabilities, data loss risks, crashes) should be CRITICAL. "
        "Logic bugs affecting correctness are HIGH. Style and maintainability are LOW. "
        "Misclassification — e.g. marking a null pointer dereference as LOW — scores low."
    ),
    evaluation_steps=[
        "For each finding in the code review, note the assigned severity.",
        "Classify the finding's actual impact: security/data-loss/crash vs logic bug vs style.",
        "Check whether the severity matches the impact category.",
        "Score 0–10: 0 = most severities are wrong; 5 = roughly half correct; "
        "10 = every severity accurately reflects the real-world impact.",
    ],
    tags=["code_review"],
    threshold=0.6,
)

CODE_REVIEW_ACTIONABILITY = GEvalCriteria(
    name="code_review_actionability",
    description="Does each code review finding include a specific, implementable fix?",
    criteria=(
        "For each finding in the code review, is there a specific, implementable suggestion "
        "for how to fix it? A good suggestion names the exact change needed "
        "(e.g. 'replace X with Y', 'add null check before line 42'). "
        "Generic suggestions like 'improve error handling' or 'consider refactoring' score low."
    ),
    evaluation_steps=[
        "For each finding, check whether a fix suggestion is provided.",
        "Evaluate whether each suggestion is specific (names what to change) vs generic.",
        "Check whether the suggestion is implementable without additional clarification.",
        "Score 0–10: 0 = no fix suggestions; 5 = half have specific fixes; "
        "10 = every finding has a specific, directly implementable fix.",
    ],
    tags=["code_review"],
    threshold=0.6,
)

# ── Catalog & lookup ─────────────────────────────────────────────────────────

CATALOG: dict[str, GEvalCriteria] = {
    c.name: c
    for c in [
        EVIDENCE_CITATION,
        CAUSATION_DISCIPLINE,
        DATA_GAP_HONESTY,
        INSTRUCTION_ADHERENCE,
        ACTIONABILITY,
        REASONING_SOUNDNESS,
        STRUCTURE_COMPLIANCE,
        COGNITIVE_SCAFFOLDING_USE,
        CODE_REVIEW_SEVERITY_ACCURACY,
        CODE_REVIEW_ACTIONABILITY,
    ]
}

# Tag-based bundles
_BUNDLES: dict[str, list[str]] = {
    "data_analysis": [
        "evidence_citation",
        "causation_discipline",
        "data_gap_honesty",
        "actionability",
    ],
    "reasoning": [
        "reasoning_soundness",
        "evidence_citation",
        "causation_discipline",
        "cognitive_scaffolding_use",
    ],
    "instruction_following": [
        "instruction_adherence",
        "structure_compliance",
    ],
    "code_review": [
        "code_review_severity_accuracy",
        "code_review_actionability",
        "instruction_adherence",
    ],
    "general": [
        "instruction_adherence",
        "actionability",
        "reasoning_soundness",
        "structure_compliance",
    ],
}


def get_criteria(bundle: str | None = None, tags: list[str] | None = None) -> list[GEvalCriteria]:
    """
    Retrieve pre-built criteria by bundle name or tag filter.

    Args:
        bundle: One of ``"data_analysis"``, ``"reasoning"``,
                ``"instruction_following"``, ``"code_review"``, ``"general"``.
                Returns the curated criteria set for that use case.
        tags:   List of tag strings. Returns all criteria that match ANY tag.
                Ignored when ``bundle`` is provided.

    Returns:
        List of GEvalCriteria objects, ready to pass to ``deepeval.metrics.GEval``.

    Example::

        from mycontext.intelligence.eval_criteria import get_criteria
        from deepeval.metrics import GEval

        criteria = get_criteria("data_analysis")
        metrics = [
            GEval(
                name=c.name,
                criteria=c.criteria,
                evaluation_steps=c.evaluation_steps,
                threshold=c.threshold,
            )
            for c in criteria
        ]
    """
    if bundle:
        names = _BUNDLES.get(bundle, [])
        return [CATALOG[n] for n in names if n in CATALOG]

    if tags:
        tag_set = set(tags)
        return [c for c in CATALOG.values() if tag_set.intersection(c.tags)]

    return list(CATALOG.values())


def to_deepeval_metrics(
    criteria: list[GEvalCriteria],
    model: str = "gpt-4o-mini",
) -> list:
    """
    Convert a list of GEvalCriteria into deepeval GEval metric objects.

    Requires ``deepeval`` to be installed (``pip install deepeval``).

    Args:
        criteria: List of GEvalCriteria (from ``get_criteria()`` or individual constants).
        model:    Model to use for the LLM judge. Default ``"gpt-4o-mini"``.

    Returns:
        List of ``deepeval.metrics.GEval`` objects ready for use in a test suite.

    Example::

        from mycontext.intelligence.eval_criteria import get_criteria, to_deepeval_metrics

        metrics = to_deepeval_metrics(get_criteria("data_analysis"))
    """
    try:
        from deepeval.metrics import GEval  # type: ignore[import]
    except ImportError as exc:
        raise ImportError(
            "deepeval is required to use to_deepeval_metrics(). "
            "Install it with: pip install deepeval"
        ) from exc

    return [
        GEval(
            name=c.name,
            criteria=c.criteria,
            evaluation_steps=c.evaluation_steps,
            model=model,
            threshold=c.threshold,
        )
        for c in criteria
    ]
