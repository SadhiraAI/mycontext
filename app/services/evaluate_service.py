"""Evaluate service: output quality, CAI measurement, benchmarks."""

from typing import Any

ENV_KEYS = {
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "google": "GOOGLE_API_KEY",
    "gemini": "GOOGLE_API_KEY",
}


def _inject_api_key_env(provider: str, api_key: str | None):
    """Temporarily set the provider env var so the SDK picks it up."""
    import os
    var = ENV_KEYS.get(provider)
    if var and api_key:
        os.environ[var] = api_key


def evaluate_output(
    assembled_content: str,
    llm_output: str,
    mode: str = "heuristic",
    provider: str = "openai",
    api_key: str | None = None,
) -> dict[str, Any] | None:
    """Score LLM output against the context that produced it."""
    try:
        from mycontext import Context
        from mycontext.intelligence.output_evaluator import (
            OutputEvaluator,
        )
    except ImportError:
        return None

    _inject_api_key_env(provider, api_key)

    eval_mode = {"fast": "heuristic", "accurate": "llm"}.get(mode, mode)
    evaluator = OutputEvaluator(mode=eval_mode, provider=provider)

    ctx = Context(directive=assembled_content)
    kwargs = {}
    if api_key:
        kwargs["api_key"] = api_key
    score = evaluator.evaluate(ctx, llm_output, **kwargs)

    dims = {}
    for d, v in score.dimensions.items():
        k = d.value if hasattr(d, "value") else str(d)
        dims[k] = round(float(v), 3)

    evidence = {}
    for d, v in score.evidence.items():
        k = d.value if hasattr(d, "value") else str(d)
        evidence[k] = v

    return {
        "overall": round(score.overall, 3),
        "dimensions": dims,
        "evidence": evidence,
        "strengths": list(score.strengths),
        "weaknesses": list(score.weaknesses),
        "metadata": score.metadata or {},
    }


def measure_cai(
    question: str,
    template_name: str,
    provider: str = "openai",
    api_key: str | None = None,
    eval_mode: str = "heuristic",
    model: str | None = None,
) -> dict[str, Any] | None:
    """Run Context Amplification Index measurement."""
    try:
        from mycontext.intelligence.context_amplification import (
            ContextAmplificationIndex,
        )
    except ImportError:
        return None

    _inject_api_key_env(provider, api_key)

    cai = ContextAmplificationIndex(
        provider=provider, eval_mode=eval_mode, model=model,
    )
    kwargs = {}
    if api_key:
        kwargs["api_key"] = api_key

    result = cai.measure(question=question, template_name=template_name, **kwargs)

    cai_dims = {}
    for d, v in result.cai_dimensions.items():
        k = d.value if hasattr(d, "value") else str(d)
        cai_dims[k] = round(float(v), 3)

    raw_dims = {}
    for d, v in result.raw_score.dimensions.items():
        k = d.value if hasattr(d, "value") else str(d)
        raw_dims[k] = round(float(v), 3)

    templated_dims = {}
    for d, v in result.templated_score.dimensions.items():
        k = d.value if hasattr(d, "value") else str(d)
        templated_dims[k] = round(float(v), 3)

    return {
        "question": result.question,
        "template_name": result.template_name,
        "cai_overall": result.cai_overall,
        "cai_dimensions": cai_dims,
        "verdict": result.verdict,
        "raw_score": {
            "overall": round(result.raw_score.overall, 3),
            "dimensions": raw_dims,
        },
        "templated_score": {
            "overall": round(result.templated_score.overall, 3),
            "dimensions": templated_dims,
        },
        "raw_output": result.raw_output[:2000],
        "templated_output": result.templated_output[:2000],
        "metadata": result.metadata or {},
    }


def run_benchmark(
    template_name: str,
    provider: str = "openai",
    api_key: str | None = None,
    eval_mode: str = "heuristic",
    model: str | None = None,
) -> dict[str, Any] | None:
    """Run benchmark for a template."""
    try:
        from mycontext.intelligence.template_benchmark import TemplateBenchmark
    except ImportError:
        return None

    _inject_api_key_env(provider, api_key)

    bench = TemplateBenchmark(
        provider=provider, eval_mode=eval_mode, model=model,
    )
    kwargs = {}
    if api_key:
        kwargs["api_key"] = api_key

    result = bench.run(template_name, **kwargs)

    return {
        "template_name": result.template_name,
        "total_cases": result.total_cases,
        "passed": result.passed,
        "failed": result.failed,
        "avg_score": result.avg_score,
        "avg_cai": result.avg_cai,
        "per_case": [
            {
                "question": c.question,
                "passed": c.passed,
                "output_score": c.output_score,
                "cai": c.cai,
                "issues": c.issues,
                "details": c.details,
            }
            for c in result.per_case
        ],
        "metadata": result.metadata or {},
    }
