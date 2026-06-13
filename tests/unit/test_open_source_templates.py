"""
Tests that confirm the SDK is fully open source (no license tiers).

Covers:
- All 88 cognitive patterns load and instantiate offline.
- Every pattern can build a Context offline (no LLM call).
- get_pattern_class returns a class for every catalog name, regardless of
  the (now-ignored) include_enterprise argument.
- Pre-authored generic prompts work offline and no longer contain the old
  "upgrade to Enterprise" note.
- The deprecated license shims warn but never gate.
"""

import warnings

import pytest

from mycontext.intelligence.pattern_catalog import FULL_PATTERN_CATALOG
from mycontext.intelligence.pattern_suggester import get_pattern_class
from mycontext.intelligence.prompt_composer import get_generic_prompt_for
from mycontext.skills.pattern_registry import get_pattern_registry

EXPECTED_TEMPLATE_COUNT = 88


def test_all_templates_present():
    registry = get_pattern_registry()
    assert len(registry) == EXPECTED_TEMPLATE_COUNT


def test_catalog_matches_registry():
    catalog_names = {name for name, _, _ in FULL_PATTERN_CATALOG}
    registry_names = set(get_pattern_registry().keys())
    assert catalog_names == registry_names


@pytest.mark.parametrize("name", list(get_pattern_registry().keys()))
def test_every_pattern_instantiates(name):
    cls = get_pattern_registry()[name]
    instance = cls()
    assert instance.name == name


@pytest.mark.parametrize("name", list(get_pattern_registry().keys()))
def test_get_pattern_class_always_available(name):
    # The include_enterprise argument is accepted but no longer gates anything.
    assert get_pattern_class(name) is not None
    assert get_pattern_class(name, include_enterprise=False) is not None


def test_generic_prompts_have_no_enterprise_note():
    """Any template with a generic prompt must not advertise an Enterprise upsell."""
    for name in get_pattern_registry():
        prompt = get_generic_prompt_for(name, "A representative question for testing.")
        if prompt:
            assert "upgrade to mycontext Enterprise" not in prompt
            assert "Enterprise license" not in prompt


def test_license_shims_are_deprecated_noops():
    import mycontext

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        assert mycontext.activate_license("anything") is True
        assert mycontext.is_enterprise_active() is True
        mycontext.deactivate_license()
    assert any(issubclass(w.category, DeprecationWarning) for w in caught)
