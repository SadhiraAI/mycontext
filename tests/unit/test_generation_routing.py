"""Unit tests for generation_routing (no LLM calls)."""

from __future__ import annotations

from mycontext.foundation.task_contract import TaskContract
from mycontext.intelligence.generation_routing import (
    classify_generation_intent,
    model_allows_sampling,
    resolve_generation_kwargs,
)
from mycontext.intelligence.prompt_architect import _merge_auto_generation_execute_kwargs


def test_model_allows_sampling_openai_o_series() -> None:
    assert not model_allows_sampling("o3-mini")
    assert not model_allows_sampling("o1-preview")


def test_model_allows_sampling_gpt5_family() -> None:
    assert not model_allows_sampling("gpt-5")
    assert not model_allows_sampling("gpt-5-pro")
    assert model_allows_sampling("gpt-5-chat")
    assert model_allows_sampling("gpt-5.2-chat-latest")


def test_model_allows_sampling_gpt4() -> None:
    assert model_allows_sampling("gpt-4o-mini")


def test_classify_json_question() -> None:
    assert classify_generation_intent("Return strictly valid JSON for the user") == "structured"


def test_classify_task_contract_genre_json() -> None:
    tc = TaskContract(genre="json api response")
    assert classify_generation_intent("Summarize the packet", tc) == "structured"


def test_classify_creative() -> None:
    assert classify_generation_intent("Brainstorm ten taglines for our launch") == "creative"


def test_classify_judge() -> None:
    assert classify_generation_intent("Score both answers on a 1-5 rubric") == "judge"


def test_resolve_chat_internal_vs_downstream() -> None:
    kw_i, _ = resolve_generation_kwargs(
        question="Brainstorm ideas",
        provider="openai",
        model="gpt-4o-mini",
        task_contract=None,
        mode="internal",
    )
    assert kw_i["temperature"] == 0.25
    assert kw_i["n"] == 1

    kw_d, _ = resolve_generation_kwargs(
        question="Brainstorm ideas",
        provider="openai",
        model="gpt-4o-mini",
        task_contract=None,
        mode="downstream",
    )
    assert kw_d["temperature"] == 0.9
    assert kw_d["n"] == 1


def test_resolve_reasoning_model_omits_sampling() -> None:
    kw, r = resolve_generation_kwargs(
        question="Return JSON for sections",
        provider="openai",
        model="gpt-5",
        task_contract=None,
        mode="internal",
    )
    assert "temperature" not in kw
    assert kw.get("reasoning_effort") == "low"
    assert "omit sampling" in r.lower()


def test_resolve_gemini_resets_n() -> None:
    kw, r = resolve_generation_kwargs(
        question="Give me several options and multiple drafts",
        provider="gemini",
        model="gemini-2.0-flash",
        task_contract=None,
        mode="downstream",
    )
    assert kw["n"] == 1
    assert "gemini" in r.lower()


def test_merge_respects_explicit_execute_override() -> None:
    merged, meta = _merge_auto_generation_execute_kwargs(
        question="Brainstorm",
        provider="openai",
        model="gpt-4o-mini",
        task_contract=None,
        auto_generation_params=True,
        generation_profile="internal",
        execute_kwargs={"temperature": 0.01},
    )
    assert merged["temperature"] == 0.01
    assert "internal_generation_kwargs" in meta


def test_merge_downstream_metadata_when_both() -> None:
    _, meta = _merge_auto_generation_execute_kwargs(
        question="Brainstorm",
        provider="openai",
        model="gpt-4o-mini",
        task_contract=None,
        auto_generation_params=True,
        generation_profile="both",
        execute_kwargs={},
    )
    assert "suggested_execute_kwargs" in meta
    assert meta["suggested_execute_kwargs"]["temperature"] == 0.9
