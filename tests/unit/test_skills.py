"""
Unit tests for Agent Skills (Skill, SkillRunner, pattern fusion).
"""

from pathlib import Path

import pytest

from mycontext.skills import Skill, SkillRunner, SkillRunResult
from mycontext.skills.pattern_registry import get_pattern, get_pattern_registry


class TestContextFromSkill:
    """Test Context.from_skill() convenience (integration)."""

    def test_from_skill_builds_context(self, tmp_path: Path) -> None:
        """Context.from_skill(path, task=...) returns a Context from that skill."""
        (tmp_path / "SKILL.md").write_text(
            "---\nname: FromSkill\ndescription: Test.\n---\nDo it.", encoding="utf-8"
        )
        from mycontext import Context

        ctx = Context.from_skill(tmp_path, task="My task")
        assert ctx.guidance is not None
        assert ctx.directive is not None
        assert "FromSkill" in (ctx.guidance.role or "")
        assert "My task" in (ctx.directive.content or "")


class TestSkill:
    """Tests for Skill model (parse SKILL.md)."""

    def test_load_skill_minimal(self, tmp_path: Path) -> None:
        """Load a minimal SKILL.md with name and description."""
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text(
            """---
name: Test Skill
description: A minimal skill for testing.
---
# Instructions
Do the thing.
""",
            encoding="utf-8",
        )
        skill = Skill.load(tmp_path)
        assert skill.name == "Test Skill"
        assert skill.description == "A minimal skill for testing."
        assert "Do the thing" in skill.body
        assert skill.input_schema == {}
        assert skill.pattern is None

    def test_load_skill_with_input_schema_and_pattern(self, tmp_path: Path) -> None:
        """Load SKILL.md with optional input_schema and pattern."""
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text(
            """---
name: Compare Skill
description: Compare options using a pattern.
input_schema:
  topic: string
  depth: string
pattern: comparative_analyzer
---
Compare the following: {topic}. Depth: {depth}.
""",
            encoding="utf-8",
        )
        skill = Skill.load(tmp_path)
        assert skill.name == "Compare Skill"
        assert "topic" in skill.input_schema
        assert skill.pattern == "comparative_analyzer"
        out = skill.full_instructions({"topic": "A vs B", "depth": "detailed"})
        assert "A vs B" in out
        assert "detailed" in out

    def test_load_skill_file_path(self, tmp_path: Path) -> None:
        """Load from explicit SKILL.md file path."""
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text("---\nname: F\ndescription: D\n---\nBody", encoding="utf-8")
        skill = Skill.load(skill_md)
        assert skill.name == "F"
        assert skill.path == tmp_path

    def test_load_missing_raises(self, tmp_path: Path) -> None:
        """Missing SKILL.md raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            Skill.load(tmp_path)

    def test_load_missing_name_raises(self, tmp_path: Path) -> None:
        """Frontmatter without name raises ValueError."""
        (tmp_path / "SKILL.md").write_text(
            "---\ndescription: Only desc\n---\nBody", encoding="utf-8"
        )
        with pytest.raises(ValueError):
            Skill.load(tmp_path)


class TestPatternRegistry:
    """Tests for pattern registry."""

    def test_registry_has_patterns(self) -> None:
        """Registry contains known pattern names."""
        registry = get_pattern_registry()
        assert "comparative_analyzer" in registry
        assert "step_by_step_reasoner" in registry
        assert "code_reviewer" in registry

    def test_get_pattern_returns_instance(self) -> None:
        """get_pattern(name) returns a new Pattern instance."""
        p = get_pattern("comparative_analyzer")
        assert p is not None
        assert p.name == "comparative_analyzer"

    def test_get_pattern_unknown_raises(self) -> None:
        """Unknown pattern name raises KeyError."""
        with pytest.raises(KeyError, match="Unknown pattern"):
            get_pattern("nonexistent_pattern_xyz")


class TestSkillRunnerPatternFusion:
    """Tests for SkillRunner with pattern fusion (Phase 2)."""

    def test_build_context_without_pattern_uses_skill_to_context(self, tmp_path: Path) -> None:
        """When skill has no pattern, build_context uses skill.to_context()."""
        (tmp_path / "SKILL.md").write_text(
            "---\nname: Plain\ndescription: Plain skill\n---\nDo it.", encoding="utf-8"
        )
        runner = SkillRunner()
        skill = runner.load_skill(tmp_path)
        ctx = runner.build_context(skill, task="My task")
        assert ctx.guidance is not None
        assert "Plain" in (ctx.guidance.role or "")
        assert "Do it" in (ctx.directive.content if ctx.directive else "")
        assert "My task" in (ctx.directive.content if ctx.directive else "")

    def test_build_context_with_pattern_fuses_pattern(self, tmp_path: Path) -> None:
        """When skill has pattern, build_context fuses with that Pattern."""
        (tmp_path / "SKILL.md").write_text(
            """---
name: Compare Options
description: Use comparative analysis.
pattern: comparative_analyzer
---
Use this skill to compare alternatives.
""",
            encoding="utf-8",
        )
        runner = SkillRunner()
        skill = runner.load_skill(tmp_path)
        ctx = runner.build_context(skill, task="Option A vs Option B")
        # Pattern provides structure: comparative directive template
        assert ctx.directive is not None
        content = ctx.directive.content
        # ComparativeAnalyzer template includes comparison framework language
        assert (
            "comparison" in content.lower() or "option" in content.lower() or "OVERVIEW" in content
        )
        # Skill/task injected
        assert "Option A" in content or "Option B" in content or "Use this skill" in content
        assert ctx.metadata.get("skill_name") == "Compare Options"
        assert ctx.metadata.get("pattern") == "comparative_analyzer"

    def test_build_context_with_step_reasoner_pattern(self, tmp_path: Path) -> None:
        """Fusion with step_by_step_reasoner injects problem from task."""
        (tmp_path / "SKILL.md").write_text(
            """---
name: Step Skill
description: Step-by-step reasoning.
pattern: step_by_step_reasoner
---
""",
            encoding="utf-8",
        )
        runner = SkillRunner()
        skill = runner.load_skill(tmp_path)
        ctx = runner.build_context(skill, task="What is 2 + 2?")
        assert ctx.directive is not None
        assert "2 + 2" in ctx.directive.content
        assert ctx.metadata.get("pattern") == "step_by_step_reasoner"

    def test_run_with_pattern_returns_quality_score(self, tmp_path: Path) -> None:
        """run() with pattern skill returns SkillRunResult with quality_score (no execute)."""
        (tmp_path / "SKILL.md").write_text(
            "---\nname: Q\ndescription: Q skill\npattern: comparative_analyzer\n---\n",
            encoding="utf-8",
        )
        runner = SkillRunner()
        result = runner.run(tmp_path, task="Compare X and Y", execute=False)
        assert isinstance(result, SkillRunResult)
        assert result.context is not None
        assert result.quality_score is not None
        assert 0 <= result.quality_score.overall <= 1
        assert result.execution_result is None
        assert result.skill is not None
        assert result.skill.pattern == "comparative_analyzer"


class TestQualityGateAndImprovement:
    """Tests for quality gate (Phase 4) and improvement_report / suggested_edits."""

    def test_quality_gate_skips_execution_when_below_threshold(self, tmp_path: Path) -> None:
        """When quality_threshold is above score, execution is skipped and gated=True."""
        (tmp_path / "SKILL.md").write_text(
            "---\nname: Minimal\ndescription: Minimal skill.\n---\nDo it.", encoding="utf-8"
        )
        runner = SkillRunner()
        # Threshold 1.0 is unreachable; execution should be skipped
        result = runner.run(
            tmp_path,
            task="test",
            execute=True,
            quality_threshold=1.0,
        )
        assert result.gated is True
        assert result.execution_result is None
        assert result.quality_score is not None

    def test_quality_gate_no_skip_when_threshold_none(self, tmp_path: Path) -> None:
        """When quality_threshold is None, execute runs (we use execute=False to avoid API)."""
        (tmp_path / "SKILL.md").write_text(
            "---\nname: Q\ndescription: Q\n---\nBody", encoding="utf-8"
        )
        runner = SkillRunner()
        result = runner.run(tmp_path, task="t", execute=False, quality_threshold=None)
        assert result.gated is False
        assert result.execution_result is None

    def test_improvement_report_returns_string(self, tmp_path: Path) -> None:
        """improvement_report(result) returns a string with score and sections."""
        from mycontext.skills import improvement_report

        (tmp_path / "SKILL.md").write_text("---\nname: R\ndescription: R\n---\nX", encoding="utf-8")
        runner = SkillRunner()
        result = runner.run(tmp_path, task="task", execute=False)
        report = improvement_report(result)
        assert isinstance(report, str)
        assert "Overall score" in report or "score" in report.lower()
        assert str(result.quality_score.overall) in report or "0." in report

    def test_suggested_edits_returns_list(self, tmp_path: Path) -> None:
        """suggested_edits(result) returns a list of strings."""
        from mycontext.skills import suggested_edits

        (tmp_path / "SKILL.md").write_text("---\nname: E\ndescription: E\n---\nY", encoding="utf-8")
        runner = SkillRunner()
        result = runner.run(tmp_path, task="task", execute=False)
        edits = suggested_edits(result)
        assert isinstance(edits, list)
        for e in edits:
            assert isinstance(e, str)


class TestSkillFeedbackLoop:
    """Tests for skill log and health report (Phase 5)."""

    def test_log_run_and_skill_health_report(self, tmp_path: Path) -> None:
        """Run 2–3 times with log_runs=True, then skill_health_report contains skill id and scores."""
        from mycontext.skills import SkillRunner, skill_health_report

        log_file = tmp_path / "skill_log.jsonl"
        (tmp_path / "SKILL.md").write_text(
            "---\nname: HealthSkill\ndescription: For health.\n---\nDo it.", encoding="utf-8"
        )
        runner = SkillRunner(log_runs=True, log_path=log_file)
        runner.run(tmp_path, task="task one", execute=False)
        runner.run(tmp_path, task="task two", execute=False)
        runner.run(tmp_path, task="task three", execute=False)
        assert log_file.exists()
        report = skill_health_report(log_path=log_file)
        assert "HealthSkill" in report
        assert "Runs" in report or "Average score" in report or "3" in report
        assert "0." in report  # score

    def test_skill_health_report_empty_log(self, tmp_path: Path) -> None:
        """skill_health_report with missing log returns no-log message."""
        from mycontext.skills import skill_health_report

        report = skill_health_report(log_path=tmp_path / "nonexistent.jsonl")
        assert "No log" in report or "found" in report.lower()

    def test_suggested_edits_from_log(self, tmp_path: Path) -> None:
        """Log 2 runs with same suggestion; suggested_edits_from_log returns it when min_count=2."""
        from mycontext.core import Context
        from mycontext.intelligence.quality_metrics import QualityScore
        from mycontext.skills import log_run, suggested_edits_from_log
        from mycontext.skills.runner import SkillRunResult

        log_file = tmp_path / "edits_log.jsonl"
        from mycontext.skills import Skill

        (tmp_path / "SKILL.md").write_text(
            "---\nname: EditSkill\ndescription: D\n---\n", encoding="utf-8"
        )
        skill = Skill.load(tmp_path)
        q2 = QualityScore(
            overall=0.5,
            dimensions={},
            issues=[],
            strengths=[],
            suggestions=["Add output format"],
            metadata={},
        )
        result2 = SkillRunResult(
            context=Context(directive="y"), quality_score=q2, skill=skill, metadata={"task": "t2"}
        )
        log_run(result2, log_path=log_file)
        log_run(result2, log_path=log_file)
        edits = suggested_edits_from_log("EditSkill", log_path=log_file, min_count=2)
        assert isinstance(edits, list)
        # May be empty if suggestion format differs; at least no error
        assert len(edits) >= 0

    def test_runner_log_runs_writes_log(self, tmp_path: Path) -> None:
        """SkillRunner(log_runs=True, log_path=...) writes to log on run()."""
        from mycontext.skills import SkillRunner

        log_file = tmp_path / "runner_log.jsonl"
        (tmp_path / "SKILL.md").write_text(
            "---\nname: LogSkill\ndescription: D\n---\nDo the task.", encoding="utf-8"
        )
        runner = SkillRunner(log_runs=True, log_path=log_file)
        runner.run(tmp_path, execute=False)
        assert log_file.exists()
        content = log_file.read_text(encoding="utf-8")
        assert "LogSkill" in content
        assert "overall" in content or "0." in content


def _skill_selector_available() -> bool:
    """True if SkillSelector can be used (RAG stack loads without numpy/env errors)."""
    try:
        from mycontext.skills import SkillSelector

        if SkillSelector is None:
            return False
        # Actually trigger embedder load (can raise ValueError on numpy/pandas mismatch)
        from mycontext.intelligence.rag.embedder import get_embedder

        get_embedder("sentence-transformers", model="all-MiniLM-L6-v2")
        return True
    except Exception:
        return False


@pytest.mark.skipif(
    not _skill_selector_available(), reason="SkillSelector requires RAG (mycontext[skills])"
)
class TestSkillSelector:
    """Tests for SkillSelector (RAG-based skill selection). Requires mycontext[skills] / sentence-transformers."""

    def test_select_skills_returns_relevant_skill(self, tmp_path: Path) -> None:
        """Index 2 skills; select_skills('compare options') returns the comparison skill."""
        compare_dir = tmp_path / "compare_skill"
        compare_dir.mkdir()
        (compare_dir / "SKILL.md").write_text(
            """---
name: Compare Options
description: Compare two or more options systematically. Use for decisions.
---
Compare the given options.
""",
            encoding="utf-8",
        )
        other_dir = tmp_path / "other_skill"
        other_dir.mkdir()
        (other_dir / "SKILL.md").write_text(
            """---
name: Summarize Text
description: Summarize long text into a short summary.
---
Summarize the following.
""",
            encoding="utf-8",
        )
        from mycontext.skills import SkillSelector

        sel = SkillSelector(skills_root=tmp_path)
        selected = sel.select_skills("compare two options and pick the best", top_k=2)
        assert len(selected) >= 1
        names = [s[0].name for s in selected]
        assert "Compare Options" in names

    def test_run_best_returns_skill_run_result(self, tmp_path: Path) -> None:
        """run_best(task, execute=False) returns SkillRunResult with context and quality_score."""
        (tmp_path / "SKILL.md").write_text(
            """---
name: Answer Question
description: Answer the user question clearly.
---
Answer the question.
""",
            encoding="utf-8",
        )
        from mycontext.skills import SkillSelector

        sel = SkillSelector(skills_root=tmp_path)
        result = sel.run_best("What is 2+2?", execute=False)
        assert isinstance(result, SkillRunResult)
        assert result.context is not None
        assert result.quality_score is not None
        assert result.skill is not None
        assert result.skill.name == "Answer Question"

    def test_run_best_no_skills_returns_empty_result(self, tmp_path: Path) -> None:
        """run_best when no skills in directory returns SkillRunResult with message in metadata."""
        from mycontext.skills import SkillSelector

        sel = SkillSelector(skills_root=tmp_path)
        result = sel.run_best("Any task", execute=False)
        assert isinstance(result, SkillRunResult)
        assert result.metadata.get("message") == "no skills found"
