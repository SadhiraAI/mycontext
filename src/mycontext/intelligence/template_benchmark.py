"""
Template Benchmark - Automated test suites for cognitive templates

Loads YAML test cases and runs each template through a set of questions,
evaluating output quality and computing CAI scores.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .context_amplification import ContextAmplificationIndex

BENCHMARKS_DIR = Path(__file__).parent.parent / "benchmarks"


@dataclass
class CaseResult:
    question: str
    passed: bool
    output_score: float
    cai: float
    issues: list[str] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class BenchmarkResult:
    template_name: str
    total_cases: int
    passed: int
    failed: int
    avg_score: float
    avg_cai: float
    per_case: list[CaseResult] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


def _load_yaml(path):
    text = path.read_text(encoding="utf-8")
    try:
        import yaml
        return yaml.safe_load(text)
    except ImportError:
        return json.loads(text)


class TemplateBenchmark:
    """
    Run automated quality benchmarks for cognitive templates.

    Example::

        >>> from mycontext.intelligence.template_benchmark import TemplateBenchmark
        >>> bench = TemplateBenchmark(provider="openai")
        >>> result = bench.run("diagnostic_root_cause_analyzer", api_key="sk-...")
        >>> print(f"Passed {result.passed}/{result.total_cases}")
    """

    def __init__(
        self,
        provider: str = "openai",
        eval_mode: str = "heuristic",
        benchmarks_dir: Path | None = None,
        model: str | None = None,
    ):
        self.provider = provider
        self.eval_mode = eval_mode
        self.benchmarks_dir = benchmarks_dir or BENCHMARKS_DIR
        self.model = model
        self._cai = ContextAmplificationIndex(
            provider=provider, eval_mode=eval_mode, model=model
        )

    def list_benchmarks(self):
        if not self.benchmarks_dir.exists():
            return []
        names = []
        for f in sorted(self.benchmarks_dir.iterdir()):
            if f.suffix in (".yaml", ".yml", ".json"):
                names.append(f.stem)
        return names

    def run(self, template_name, **kwargs):
        bench_file = self._find_bench_file(template_name)
        if not bench_file:
            return BenchmarkResult(
                template_name=template_name, total_cases=0, passed=0,
                failed=0, avg_score=0.0, avg_cai=0.0,
                metadata={"error": "No benchmark file found for " + template_name},
            )
        spec = _load_yaml(bench_file)
        cases = spec.get("test_cases", [])
        if not cases:
            return BenchmarkResult(
                template_name=template_name, total_cases=0, passed=0,
                failed=0, avg_score=0.0, avg_cai=0.0,
                metadata={"error": "No test cases in benchmark file"},
            )

        results = []
        for case in cases:
            results.append(self._run_case(template_name, case, **kwargs))

        passed = sum(1 for r in results if r.passed)
        scores = [r.output_score for r in results]
        cais = [r.cai for r in results if r.cai > 0]

        return BenchmarkResult(
            template_name=template_name,
            total_cases=len(results),
            passed=passed,
            failed=len(results) - passed,
            avg_score=round(sum(scores) / len(scores), 3) if scores else 0.0,
            avg_cai=round(sum(cais) / len(cais), 3) if cais else 0.0,
            per_case=results,
            metadata={"provider": self.provider, "eval_mode": self.eval_mode},
        )

    def run_all(self, **kwargs):
        results = {}
        for name in self.list_benchmarks():
            results[name] = self.run(name, **kwargs)
        return results

    def _find_bench_file(self, template_name):
        for ext in (".yaml", ".yml", ".json"):
            path = self.benchmarks_dir / (template_name + ext)
            if path.exists():
                return path
        return None

    def _run_case(self, template_name, case, **kwargs):
        question = case.get("question", "")
        expected = case.get("expected", {})
        min_score = expected.get("min_score", 0.5)
        must_contain = expected.get("must_contain", [])

        try:
            cai_result = self._cai.measure(
                question=question, template_name=template_name, **kwargs,
            )
            output = cai_result.templated_output
            score = cai_result.templated_score.overall
            cai_val = cai_result.cai_overall
        except Exception as e:
            return CaseResult(
                question=question, passed=False, output_score=0.0, cai=0.0,
                issues=["Execution error: " + str(e)],
            )

        issues = []
        if score < min_score:
            issues.append("Score " + str(round(score, 2)) + " below minimum " + str(min_score))

        output_lower = output.lower()
        for term in must_contain:
            if term.lower() not in output_lower:
                issues.append("Missing required term: " + term)

        return CaseResult(
            question=question,
            passed=len(issues) == 0,
            output_score=round(score, 3),
            cai=round(cai_val, 3),
            issues=issues,
            details={
                "raw_score": round(cai_result.raw_score.overall, 3),
                "verdict": cai_result.verdict,
            },
        )

    @staticmethod
    def report(result):
        lines = [
            "Benchmark Report: " + result.template_name,
            "=" * (19 + len(result.template_name)), "",
            "Cases: " + str(result.total_cases) + "  |  Passed: " + str(result.passed) + "  |  Failed: " + str(result.failed),
            "Avg Output Score: " + str(round(result.avg_score * 100, 1)) + "%",
            "Avg CAI: " + str(round(result.avg_cai, 2)) + "x", "",
        ]
        for i, cr in enumerate(result.per_case, 1):
            status = "PASS" if cr.passed else "FAIL"
            lines.append("  [" + status + "] Case " + str(i) + ": score=" + str(round(cr.output_score * 100, 1)) + "%, CAI=" + str(round(cr.cai, 2)) + "x")
            lines.append("         Q: " + cr.question[:60] + "...")
            for iss in cr.issues:
                lines.append("         ! " + iss)
        return "\n".join(lines)
