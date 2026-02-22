"""Transform service: one-shot transform, explain selection."""

from typing import Any

try:
    from mycontext.intelligence import transform
    from mycontext.intelligence.transformation_engine import TransformationEngine
except ImportError:
    transform = None
    TransformationEngine = None

try:
    from mycontext.intelligence.pattern_suggester import NAME_TO_CATEGORY
except ImportError:
    NAME_TO_CATEGORY = {}


def transform_question(question: str, include_enterprise: bool = True) -> dict[str, Any] | None:
    """Transform question into context. Returns patterns, explanation, and categories (pipeline-style)."""
    if not transform or not TransformationEngine:
        return None
    engine = TransformationEngine(include_enterprise=include_enterprise)
    analysis = engine.analyze_input(question)
    explanation = engine.explain_selection(question)
    patterns = analysis.recommended_patterns or []
    pattern_categories = {p: NAME_TO_CATEGORY.get(p, "free") for p in patterns}
    selection_reasoning: dict[str, str] = {}
    for p in patterns:
        cat = pattern_categories.get(p, "free")
        selection_reasoning[p] = _build_reason(p, cat, question)
    return {
        "patterns_applied": patterns,
        "explanation": explanation,
        "pattern_categories": pattern_categories,
        "selection_reasoning": selection_reasoning,
        "input_type": analysis.input_type.value,
        "complexity": analysis.complexity.value,
        "domain": analysis.domain,
    }


def _build_reason(pattern: str, category: str, question: str) -> str:
    """Generate a human-readable reason for pattern selection."""
    _PATTERN_DESCRIPTIONS: dict[str, str] = {
        "root_cause_analyzer": "Investigates underlying causes using structured analysis",
        "causal_reasoner": "Traces cause-and-effect chains to explain outcomes",
        "step_by_step_reasoner": "Breaks complex problems into logical sequential steps",
        "question_analyzer": "Decomposes the question into sub-questions for clarity",
        "data_analyzer": "Structures data-driven analysis with metrics and trends",
        "socratic_questioner": "Uses probing questions to uncover hidden assumptions",
        "intent_recognizer": "Identifies the core intent behind the query",
        "analogical_reasoner": "Draws parallels from similar domains for insight",
        "risk_assessor": "Evaluates potential risks and their likelihood",
        "ambiguity_resolver": "Clarifies ambiguous terms and assumptions",
        "problem_decomposer": "Decomposes complex problems into manageable parts",
        "decision_framework": "Structures decision-making with criteria and trade-offs",
        "comparative_analyzer": "Systematically compares alternatives across dimensions",
        "tradeoff_analyzer": "Weighs pros and cons of competing options",
        "hypothesis_generator": "Generates testable hypotheses from observations",
    }
    desc = _PATTERN_DESCRIPTIONS.get(pattern, pattern.replace("_", " ").title())
    tier = "Free" if category != "enterprise" else "Enterprise"
    return f"{desc} ({tier})"
