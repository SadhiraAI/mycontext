"""PromptArchitect structural correctness tests (no LLM calls)."""

from __future__ import annotations

from mycontext.intelligence.prompt_architect import (
    REASONING_STRATEGY_CHOICES,
    PromptArchitect,
)


# ── normalization ──────────────────────────────────────────────────────────────

def test_normalize_reasoning_strategies() -> None:
    assert PromptArchitect._normalize_reasoning_strategies(None) == []
    assert PromptArchitect._normalize_reasoning_strategies("") == []
    assert PromptArchitect._normalize_reasoning_strategies("null") == []
    assert PromptArchitect._normalize_reasoning_strategies("  step_by_step  ") == ["step_by_step"]
    assert PromptArchitect._normalize_reasoning_strategies(
        ["verify", "step_by_step", "verify"]
    ) == ["verify", "step_by_step"]


def test_reasoning_choices_tuple_documented() -> None:
    assert "step_by_step" in REASONING_STRATEGY_CHOICES
    assert len(REASONING_STRATEGY_CHOICES) == 5


# ── reasoning NOT in RULES ─────────────────────────────────────────────────────

def test_reasoning_not_injected_into_rules() -> None:
    arch = PromptArchitect()
    data = {
        "role": "You are X",
        "goal": "G",
        "rules": ["r1", "r2"],
        "style": None,
        "reasoning_strategies": ["step_by_step", "verify"],
        "examples": [],
        "output_contract": None,
        "guard_rails": [],
        "task": "Do t",
    }
    ctx = arch._json_to_context(data, "fallback")
    # Rules must contain only the explicit rules — no reasoning pollution
    assert ctx.guidance is not None
    for rule in ctx.guidance.rules:
        assert "Reasoning" not in rule, f"Reasoning leaked into RULES: {rule}"
        assert "step_by_step" not in rule
        assert "verify" not in rule


def test_reasoning_stored_in_analytical_approach() -> None:
    arch = PromptArchitect()
    data = {
        "role": "You are X",
        "goal": "G",
        "rules": ["r1"],
        "style": None,
        "reasoning_strategies": ["step_by_step", "verify"],
        "examples": [],
        "output_contract": None,
        "guard_rails": [],
        "task": "Do t",
    }
    ctx = arch._json_to_context(data, "fallback")
    assert ctx.analytical_approach is not None
    assert "step_by_step" in ctx.analytical_approach or "Chain of Thought" in ctx.analytical_approach


def test_single_strategy_stored_in_analytical_approach() -> None:
    arch = PromptArchitect()
    data = {
        "role": "You are X",
        "goal": "G",
        "rules": ["r1"],
        "reasoning": "explain_simply",
        "examples": [],
        "output_contract": None,
        "guard_rails": [],
        "task": "Do t",
    }
    ctx = arch._json_to_context(data, "fallback")
    assert ctx.analytical_approach is not None
    assert "explain_simply" in ctx.analytical_approach or "Simplification" in ctx.analytical_approach


# ── reasoning renders AFTER GUARD RAILS, BEFORE YOUR TASK ─────────────────────

def test_reasoning_renders_before_task_after_guard_rails() -> None:
    arch = PromptArchitect()
    data = {
        "role": "You are an analyst",
        "goal": "Find anomalies",
        "rules": ["Rule A"],
        "style": "Formal",
        "reasoning_strategies": ["step_by_step", "verify"],
        "examples": [],
        "output_contract": "Return ONLY JSON",
        "guard_rails": ["Omit hedging: probably, might"],
        "task": "Analyze this data",
    }
    ctx = arch._json_to_context(data, "Analyze this data")
    assembled = ctx.assemble()

    guard_pos = assembled.find("GUARD RAILS")
    reasoning_pos = assembled.find("ANALYTICAL AND REPORTING APPROACH")
    task_pos = assembled.find("YOUR TASK")

    assert guard_pos != -1, "GUARD RAILS section missing"
    assert reasoning_pos != -1, "ANALYTICAL AND REPORTING APPROACH section missing"
    assert task_pos != -1, "YOUR TASK section missing"
    assert guard_pos < reasoning_pos < task_pos, (
        f"Wrong order: GUARD RAILS={guard_pos}, REASONING={reasoning_pos}, TASK={task_pos}"
    )


# ── examples go to Context.examples, not Directive ────────────────────────────

def test_examples_go_to_context_not_directive() -> None:
    arch = PromptArchitect()
    data = {
        "role": "You are X",
        "goal": "G",
        "rules": ["r1"],
        "style": None,
        "reasoning_strategies": [],
        "examples": [
            {"input": "Ticket: login fails", "output": "1) LOGIN ISSUES (1 sentence). 2) 15 occurrences. 3) Tickets 001, 002, 003 all report OAuth timeout. 4) Rotate OAuth credentials."},
        ],
        "output_contract": "Return ONLY a 4-part structure",
        "guard_rails": [],
        "task": "Categorize tickets",
    }
    ctx = arch._json_to_context(data, "Categorize tickets")

    # Context.examples must be populated
    assert ctx.examples is not None and len(ctx.examples) == 1
    assert ctx.examples[0]["input"] == "Ticket: login fails"

    # Directive must NOT contain the raw examples block
    assert ctx.directive is not None
    assert "**EXAMPLES**" not in ctx.directive.content
    assert "Example 1:" not in ctx.directive.content


def test_examples_render_in_examples_section() -> None:
    arch = PromptArchitect()
    data = {
        "role": "You are X",
        "goal": "G",
        "rules": [],
        "style": None,
        "reasoning_strategies": [],
        "examples": [
            {"input": "user question", "output": "model answer"},
        ],
        "output_contract": None,
        "guard_rails": [],
        "task": "Do something",
    }
    ctx = arch._json_to_context(data, "Do something")
    assembled = ctx.assemble()
    assert "## EXAMPLES" in assembled
    assert "user question" in assembled
    assert "model answer" in assembled


def test_legacy_string_examples_converted() -> None:
    arch = PromptArchitect()
    data = {
        "role": "You are X",
        "goal": "G",
        "rules": [],
        "style": None,
        "reasoning_strategies": [],
        "examples": ["Input → Output result", "plain string example"],
        "output_contract": None,
        "guard_rails": [],
        "task": "Do t",
    }
    ctx = arch._json_to_context(data, "Do t")
    assert ctx.examples is not None
    assert len(ctx.examples) == 2
    # Arrow-split example
    assert ctx.examples[0]["input"] == "Input"
    assert ctx.examples[0]["output"] == "Output result"
    # Plain string falls back to generic input label
    assert ctx.examples[1]["output"] == "plain string example"


# ── guard_rails rescue ─────────────────────────────────────────────────────────

def test_guard_rails_rescue_grounding_rule() -> None:
    arch = PromptArchitect()
    data = {
        "role": "You are X",
        "goal": "G",
        "rules": ["r1"],
        "style": None,
        "reasoning_strategies": [],
        "examples": [],
        "output_contract": None,
        "guard_rails": [
            "Every claim must be grounded in the provided ticket data. If absent, state: 'Not found in the provided material.'",
            "Omit hedging language: probably, might, could be",
        ],
        "task": "Do t",
    }
    ctx = arch._json_to_context(data, "Do t")
    # Grounding rule rescued to rules
    grounding_in_rules = any("grounded" in r for r in ctx.guidance.rules)
    assert grounding_in_rules, "Grounding rule should have been rescued into rules"
    # Guard rails should only keep the Omit statement
    if ctx.constraints and ctx.constraints.must_not_include:
        for item in ctx.constraints.must_not_include:
            assert "grounded" not in item.lower(), "Grounding rule leaked into guard_rails"


# ── provider-specific format ───────────────────────────────────────────────────

def test_render_for_anthropic_gives_xml() -> None:
    arch = PromptArchitect(provider="openai", render_for="anthropic")
    data = {
        "role": "You are an analyst",
        "goal": "Find patterns",
        "rules": ["Rule A"],
        "style": "Formal",
        "reasoning_strategies": ["step_by_step"],
        "examples": [],
        "output_contract": "Return ONLY JSON",
        "guard_rails": ["Omit hedging"],
        "task": "Analyze data",
    }
    ctx = arch._json_to_context(data, "Analyze data")
    assembled = ctx.assemble()
    assert "<role>" in assembled or "<goal>" in assembled, (
        "Expected XML delimiters for anthropic target but got markdown"
    )


def test_render_for_openai_gives_markdown() -> None:
    arch = PromptArchitect(provider="openai")
    data = {
        "role": "You are an analyst",
        "goal": "Find patterns",
        "rules": ["Rule A"],
        "style": "Formal",
        "reasoning_strategies": [],
        "examples": [],
        "output_contract": None,
        "guard_rails": [],
        "task": "Analyze data",
    }
    ctx = arch._json_to_context(data, "Analyze data")
    assembled = ctx.assemble()
    assert "## ROLE" in assembled, "Expected markdown headings for openai target"


def test_target_provider_in_metadata_build_result() -> None:
    arch = PromptArchitect(provider="openai", render_for="anthropic")
    assert arch._resolve_assembly_provider_hint() == "anthropic"
