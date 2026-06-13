"""Tests for the Requirements-as-Code authoring + scoring bridge (offline)."""

import yaml

from mycontext.rac import draft_requirements, score_output, to_yaml
from mycontext.rac.author import SECTION_TEMPLATES, RequirementsAuthor

TASK = "Build a support copilot that drafts replies to billing tickets."


def test_draft_has_all_sections():
    doc = draft_requirements(TASK)
    for section in SECTION_TEMPLATES:
        assert section in doc
        assert doc[section]["templates"] == SECTION_TEMPLATES[section]


def test_draft_is_offline_and_emits_prompts():
    """Without execute=True, each section emits prompts and never an LLM draft."""
    doc = draft_requirements(TASK, execute=False)
    for section in SECTION_TEMPLATES:
        for entry in doc[section]["drafts"]:
            assert entry["prompt"]
            assert "draft" not in entry


def test_metadata_states_authoring_only():
    doc = draft_requirements(TASK)
    assert doc["metadata"]["mode"] == "authoring"
    assert "enforcement" in doc["metadata"]["note"].lower()


def test_to_yaml_roundtrips():
    doc = draft_requirements(TASK)
    text = to_yaml(doc)
    loaded = yaml.safe_load(text)
    assert loaded["task"] == TASK
    assert set(SECTION_TEMPLATES).issubset(loaded.keys())


def test_score_output_offline():
    result = score_output(
        "Identify the root causes of the outage and propose fixes.",
        "Root cause: a misconfigured timeout. Fix: add validation. Step 1: ... Step 2: ...",
    )
    assert 0.0 <= result["overall"] <= 1.0
    assert "dimensions" in result


def test_author_default_sections():
    author = RequirementsAuthor()
    assert author.execute is False
    assert set(author.sections) == set(SECTION_TEMPLATES)
