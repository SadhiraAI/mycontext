"""Tests for the Requirements Architect: product, technical, and trace (offline)."""

import yaml

from mycontext.rac import (
    parse_intent,
    product,
    project,
    technical,
    to_yaml,
    trace,
    validate,
)

INTENT = (
    "Brightcart support gets ~2,000 emails/day. Leadership wants Aurora: an agent "
    "that reads each email, looks up the order, and drafts (eventually sends) a "
    "reply -- refunds require human approval. Success means faster replies without "
    "wrong refunds, leaked customer data, or brand-damaging replies."
)


# --------------------------------------------------------------------------- #
# Intake
# --------------------------------------------------------------------------- #
def test_intake_detects_name_and_constraints():
    intake = parse_intent(INTENT)
    assert intake.name == "Aurora"
    assert intake.constraints.get("hitl") is True
    assert intake.constraints.get("money_actions") is True
    assert intake.must_never  # mined the "without ..." clause


# --------------------------------------------------------------------------- #
# Product
# --------------------------------------------------------------------------- #
def test_product_has_core_sections_and_type():
    doc = product(INTENT)
    assert doc["meta"]["spec_type"] == "product_requirements"
    for section in ("tasks", "rubrics", "actions", "safety", "gates", "open_questions"):
        assert section in doc
    # Mandatory refusal row exists.
    assert any(t.get("no_draft") for t in doc["tasks"].values())
    # Money action is gated, destructive tools are forbidden.
    policies = {a["id"]: a.get("policy") for a in doc["actions"]}
    assert policies.get("A-4") == "approve"
    assert policies.get("A-X") == "forbidden"


def test_product_gaps_are_open_questions_not_blockers():
    doc = product(INTENT)
    assert doc["meta"]["status"] == "draft"
    assert doc["open_questions"]
    issues = validate(doc)
    assert any("blocking open question" in i for i in issues)


def test_product_yaml_roundtrips():
    doc = product(INTENT)
    loaded = yaml.safe_load(to_yaml(doc))
    assert loaded["meta"]["system_name"] == "aurora"


# --------------------------------------------------------------------------- #
# Technical
# --------------------------------------------------------------------------- #
def test_technical_from_product_is_traceable():
    prod = product(INTENT)
    tech = technical(product=prod, frontier=True)
    assert tech["meta"]["spec_type"] == "technical_requirements"
    assert tech["meta"]["source"] == "product_requirements"
    for section in ("architecture", "guardrails", "tools", "cost", "security", "frontier"):
        assert section in tech
    # Forbidden product action is reflected in the technical tool policy.
    forbidden = tech["tools"]["forbidden"]
    assert any("A-X" in f.get("serves", []) for f in forbidden)


def test_technical_from_text_only():
    tech = technical("A RAG assistant answers questions from our wiki; never invent answers.")
    assert tech["meta"]["source"] == "natural_language"
    assert "retrieve_then_generate" in tech["architecture"]["pattern"]


def test_technical_validation_dispatches_on_type():
    tech = technical(product=product(INTENT))
    issues = validate(tech)
    # Technical validator only emits OQ warnings here, never the product-only errors.
    assert all("Uncovered" not in i for i in issues)


# --------------------------------------------------------------------------- #
# Trace
# --------------------------------------------------------------------------- #
def test_trace_full_coverage_in_sync():
    prod = product(INTENT)
    tech = technical(product=prod)
    report = trace(prod, tech)
    assert report["coverage"]["ratio"] == 1.0
    assert report["status"] in ("in_sync", "review")


def test_trace_diff_flags_forbidden_action():
    prod = product(INTENT)
    tech = technical(product=prod)
    diff = (
        "diff --git a/r.py b/r.py\n--- a/r.py\n+++ b/r.py\n@@ -1 +1,2 @@\n"
        "+    delete_record(o)\n"
    )
    report = trace(prod, tech, diff=diff)
    assert report["status"] == "drift_detected"
    assert any("forbidden" in f.lower() for f in report["findings"])


def test_trace_detects_uncovered_requirement():
    prod = product(INTENT)
    # An empty technical spec covers nothing.
    empty_tech = {"meta": {"spec_type": "technical_requirements"}}
    report = trace(prod, empty_tech)
    assert report["status"] == "drift_detected"
    assert report["coverage"]["uncovered"]


# --------------------------------------------------------------------------- #
# Projections
# --------------------------------------------------------------------------- #
def test_project_product_and_technical_targets():
    prod = product(INTENT)
    tech = technical(product=prod)
    assert "AGENTS.md" in project(prod, "agents-md")
    assert "EARS" in project(prod, "kiro") or "WHEN" in project(prod, "kiro")
    assert "Architecture" in project(tech, "adr")


def test_complete_fills_open_questions_offline(monkeypatch):
    """The LLM fill pass substitutes answers and resolves TODO markers (mocked)."""
    from mycontext.rac import complete, to_yaml
    from mycontext.rac import fill as fill_mod

    doc = product(INTENT)
    questions = [q["id"] for q in doc["open_questions"]]

    def fake_ask(_doc, _questions, _provider, _model, _extra=None):
        # Answer every question with a plausible typed value.
        out = {}
        for q in _questions:
            affects = q.get("affects", "")
            if "categories" in affects:
                out[q["id"]] = ["legal", "press", "self-harm"]
            elif "cases" in affects or "usd" in affects.lower() or "max_amount" in affects:
                out[q["id"]] = 25
            else:
                out[q["id"]] = "resolved value"
        return out

    monkeypatch.setattr(fill_mod, "_ask_llm", fake_ask)
    filled = complete(doc, provider="openai", model="gpt-4o-mini")

    import re

    assert not re.search(r"TODO\(OQ-\d+\)", to_yaml(filled))
    assert filled["meta"]["status"] == "filled"
    assert all(q.get("status") == "answered" for q in filled["open_questions"] if q["id"] in questions)


def test_product_execute_uses_fill(monkeypatch):
    """product(execute=True) routes through the fill pass (mocked LLM)."""
    from mycontext.rac import fill as fill_mod
    from mycontext.rac import patterns as patterns_mod

    monkeypatch.setattr(patterns_mod, "run_pattern", lambda *a, **k: "")
    monkeypatch.setattr(fill_mod, "_ask_llm", lambda d, qs, p, m, x=None: {q["id"]: "x" for q in qs})
    doc = product(INTENT, execute=True)
    assert doc["meta"].get("filled_by", "").startswith("openai:")


def test_product_execute_runs_patterns_and_grounds_fill(monkeypatch):
    """execute=True runs the curated patterns and feeds their brief to the fill."""
    from mycontext.rac import fill as fill_mod
    from mycontext.rac import patterns as patterns_mod

    seen: dict[str, str | None] = {}

    monkeypatch.setattr(
        patterns_mod, "run_pattern", lambda name, text, **k: f"analysis::{name}"
    )

    def capture_ask(_doc, _questions, _provider, _model, extra=None):
        seen["extra"] = extra
        return {q["id"]: "x" for q in _questions}

    monkeypatch.setattr(fill_mod, "_ask_llm", capture_ask)
    doc = product(INTENT, execute=True)

    # Only a clean provenance map is persisted (never the verbose prose)...
    informed = doc["meta"]["informed_by"]
    assert informed["rubrics"] == ["rubric_designer"]
    assert "_pattern_notes" not in doc
    # ...while the full analyses are handed to the fill model as expert grounding.
    assert seen["extra"] and "analysis::rubric_designer" in seen["extra"]


def test_technical_execute_runs_patterns(monkeypatch):
    """technical(execute=True) also runs its curated patterns and grounds the fill."""
    from mycontext.rac import fill as fill_mod
    from mycontext.rac import patterns as patterns_mod

    seen: dict[str, str | None] = {}
    monkeypatch.setattr(
        patterns_mod, "run_pattern", lambda name, text, **k: f"analysis::{name}"
    )

    def capture_ask(_doc, _questions, _provider, _model, extra=None):
        seen["extra"] = extra
        return {q["id"]: "x" for q in _questions}

    monkeypatch.setattr(fill_mod, "_ask_llm", capture_ask)
    tech = technical(product=product(INTENT), execute=True)

    informed = tech["meta"]["informed_by"]
    assert "architecture" in informed
    assert "design_thinker" in informed["architecture"]
    assert "_pattern_notes" not in tech
    assert seen["extra"] and "analysis::design_thinker" in seen["extra"]


def test_analyze_and_format_brief(monkeypatch):
    """analyze() returns the pattern notes; format_brief() renders clean markdown."""
    from mycontext.rac import analyze, format_brief
    from mycontext.rac import patterns as patterns_mod

    monkeypatch.setattr(patterns_mod, "run_pattern", lambda name, text, **k: f"analysis::{name}")
    notes = analyze(INTENT, kind="product")
    assert "rubrics" in notes and "rubric_designer" in notes["rubrics"]

    md = format_brief(notes)
    assert "## `rubrics`" in md and "### rubric_designer" in md and "analysis::rubric_designer" in md


def test_analyze_rejects_unknown_kind():
    from mycontext.rac import analyze

    try:
        analyze(INTENT, kind="nonsense")
    except ValueError as exc:
        assert "product" in str(exc)
    else:
        raise AssertionError("expected ValueError for unknown kind")


def test_format_brief_empty_is_friendly():
    from mycontext.rac import format_brief

    assert "No pattern analyses" in format_brief({})


def test_resolve_model_provider_aware():
    from mycontext.rac.models import resolve_model

    assert resolve_model("openai", None) == "gpt-4o-mini"
    assert resolve_model("anthropic", None) == "claude-3-5-haiku-latest"
    assert resolve_model("gemini", None) == "gemini-1.5-flash"
    # An explicit model always wins.
    assert resolve_model("openai", "gpt-4o") == "gpt-4o"
    # Unknown provider without a model is a hard, helpful error (never an OpenAI id).
    try:
        resolve_model("groq", None)
    except ValueError as exc:
        assert "groq" in str(exc) and "--model" in str(exc)
    else:
        raise AssertionError("expected ValueError for provider with no default model")


def test_execute_custom_model_propagates(monkeypatch):
    """A custom model flows to both the pattern brief and the fill pass."""
    from mycontext.rac import fill as fill_mod
    from mycontext.rac import patterns as patterns_mod

    seen: dict[str, object] = {}

    def fake_run(name, text, *, provider, model):
        seen["pattern_model"] = model
        return f"analysis::{name}"

    def fake_ask(_doc, _questions, _provider, model, _extra=None):
        seen["fill_model"] = model
        return {q["id"]: "x" for q in _questions}

    monkeypatch.setattr(patterns_mod, "run_pattern", fake_run)
    monkeypatch.setattr(fill_mod, "_ask_llm", fake_ask)

    doc = product(INTENT, execute=True, model="gpt-4o")
    assert seen["pattern_model"] == "gpt-4o"
    assert seen["fill_model"] == "gpt-4o"
    assert doc["meta"]["filled_by"] == "openai:gpt-4o"


def test_execute_unknown_provider_without_model_raises(monkeypatch):
    """execute=True on a provider with no default model fails fast and clearly."""
    import pytest

    with pytest.raises(ValueError, match="groq"):
        product(INTENT, execute=True, provider="groq")


def test_project_rejects_product_target_on_technical():
    tech = technical(product=product(INTENT))
    try:
        project(tech, "kiro")
    except ValueError as exc:
        assert "product spec" in str(exc)
    else:
        raise AssertionError("expected ValueError projecting technical spec to kiro")
