"""
Unit tests for chain orchestration agent.
"""


from mycontext.intelligence import (
    PATTERN_BUILD_CONTEXT_REGISTRY,
    WorkflowChainResult,
    build_workflow_chain,
)
from mycontext.intelligence.pattern_suggester import VALID_PATTERN_NAMES


class TestChainOrchestrationAgent:
    """Tests for build_workflow_chain and related components."""

    def test_registry_has_all_patterns(self) -> None:
        """Registry should cover all valid pattern names."""
        for name in VALID_PATTERN_NAMES:
            assert name in PATTERN_BUILD_CONTEXT_REGISTRY, f"Missing registry entry for {name}"

    def test_registry_format(self) -> None:
        """Each registry entry should be (primary_key, dict)."""
        for name, entry in PATTERN_BUILD_CONTEXT_REGISTRY.items():
            assert isinstance(entry, tuple), f"{name}: expected tuple"
            assert len(entry) == 2, f"{name}: expected (primary, defaults)"
            primary, defaults = entry
            assert isinstance(primary, str), f"{name}: primary should be str"
            assert isinstance(defaults, dict), f"{name}: defaults should be dict"

    def test_build_workflow_chain_returns_result(self) -> None:
        """build_workflow_chain returns WorkflowChainResult (may have empty chain if no API key)."""
        r = build_workflow_chain("Classify sentiment.", max_patterns=None, temperature=0)
        assert isinstance(r, WorkflowChainResult)
        assert hasattr(r, "chain")
        assert hasattr(r, "chain_params")
        assert isinstance(r.chain, list)
        assert isinstance(r.chain_params, dict)

    def test_to_chain_params_tuple_format(self) -> None:
        """to_chain_params_tuple_format returns (primary_key, extra_dict) per pattern.

        Custom params override defaults; additional defaults from the real
        build_context() signature are preserved.
        """
        r = WorkflowChainResult(
            chain=["pattern_recognition_engine", "feedback_composer"],
            chain_params={
                "pattern_recognition_engine": {"data": "<from previous step>", "pattern_focus": "sentiment"},
                "feedback_composer": {"situation": "<from previous step>", "goal": "Feedback goal"},
            },
            reasoning="test",
        )
        ch = r.to_chain_params_tuple_format()

        pri_pre, extra_pre = ch["pattern_recognition_engine"]
        assert pri_pre == "data"
        assert extra_pre["pattern_focus"] == "sentiment"

        pri_fc, extra_fc = ch["feedback_composer"]
        assert pri_fc == "situation"
        assert extra_fc["goal"] == "Feedback goal"
