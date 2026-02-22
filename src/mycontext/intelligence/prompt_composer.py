"""
Prompt Composer — Merge multiple template-generated prompts into one.

The core innovation of the Prompt Compilation Pipeline: instead of executing
multiple templates and integrating their outputs (which compete for output
tokens), generate compact prompts from each template and compose them into a
single, comprehensive prompt that can be executed once.

Two usage patterns:
  1. ``compose()`` — merge pre-generated prompt strings.
  2. ``compose_from_templates()`` — generate prompts from templates and compose
     them in one call.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..core import Context
from ..foundation import Directive, Guidance


@dataclass
class ComposedPrompt:
    """Result of prompt composition — an optimized, self-contained prompt."""

    prompt: str
    source_templates: List[str] = field(default_factory=list)
    question: str = ""
    component_prompts: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def execute(self, provider: str = "openai", **kwargs) -> str:
        """Execute the composed prompt and return the response text."""
        ctx = self.to_context()
        result = ctx.execute(provider=provider, **kwargs)
        return result.response

    def to_context(self) -> Context:
        """Convert into a mycontext Context for execution or further processing."""
        return Context(directive=Directive(content=self.prompt))

    def to_string(self) -> str:
        """Return the prompt as a plain string (for use with any LLM)."""
        return self.prompt

    def to_messages(self) -> list:
        """Export as OpenAI-compatible message array."""
        return [{"role": "user", "content": self.prompt}]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "prompt": self.prompt,
            "source_templates": self.source_templates,
            "question": self.question,
            "component_prompts": self.component_prompts,
            "metadata": self.metadata,
        }


_COMPOSE_SYSTEM = (
    "You are a prompt composition expert. Your job is to merge multiple "
    "analytical prompts into ONE comprehensive, non-redundant prompt that "
    "another LLM can execute directly."
)

_COMPOSE_TEMPLATE = """ORIGINAL QUESTION: "{question}"

COMPONENT PROMPTS TO MERGE:
{numbered_prompts}

MERGE RULES:
1. Produce a SINGLE self-contained prompt (not an answer).
2. Preserve every unique analytical technique from the components (root cause analysis, comparative frameworks, ethical lenses, etc.).
3. Remove redundancy — if two components ask for "stakeholder analysis," include it once.
4. Structure the merged prompt clearly: role, analytical approach, output sections.
5. The merged prompt should be 1000-1800 characters — concise but comprehensive.
6. ALWAYS include an instruction to end with concrete Recommendations / Next Steps.

OUTPUT THE MERGED PROMPT ONLY:"""


def _resolve_generic_template(
    template_name: str,
    include_enterprise: bool = True,
    warn_on_fallback: bool = False,
):
    """Resolve a template name to a (pattern_instance, actual_name) with fallback.

    Two-stage resolution:
      1. Load the class; if inaccessible (enterprise in free mode), try fallback.
      2. Check the loaded class has GENERIC_PROMPT; if not, try fallback.

    Returns (instance, actual_name) or (None, None).
    """
    import warnings
    from .pattern_suggester import get_pattern_class
    from .pattern_catalog import GENERIC_PROMPT_FALLBACK

    actual_name = template_name
    klass = get_pattern_class(template_name, include_enterprise=include_enterprise)

    if klass is None:
        fb = GENERIC_PROMPT_FALLBACK.get(template_name)
        if not fb:
            return None, None
        klass = get_pattern_class(fb, include_enterprise=False)
        if klass is None:
            return None, None
        actual_name = fb
        if warn_on_fallback:
            warnings.warn(
                f"Enterprise template '{template_name}' is not available in free mode. "
                f"Using free fallback '{fb}' instead. For best results, activate an "
                f"enterprise license: mycontext.activate_license('MC-ENT-...')",
                UserWarning,
                stacklevel=3,
            )

    instance = klass()
    if instance.GENERIC_PROMPT is None:
        fb = GENERIC_PROMPT_FALLBACK.get(template_name)
        if not fb:
            return None, None
        fb_klass = get_pattern_class(fb, include_enterprise=False)
        if fb_klass is None or getattr(fb_klass, "GENERIC_PROMPT", None) is None:
            return None, None
        instance = fb_klass()
        actual_name = fb

    return instance, actual_name


class PromptComposer:
    """Compose multiple template-generated prompts into one comprehensive prompt.

    Example::

        >>> from mycontext.intelligence.prompt_composer import PromptComposer
        >>> composer = PromptComposer()
        >>> result = composer.compose_from_templates(
        ...     question="Why did churn spike 40%?",
        ...     template_names=["root_cause_analyzer", "decision_framework"],
        ... )
        >>> print(result.to_string())   # optimized prompt
        >>> print(result.execute())     # execute and get response
    """

    def __init__(
        self,
        include_enterprise: bool = True,
        provider: str = "openai",
        model: str = "gpt-4o-mini",
    ):
        self.include_enterprise = include_enterprise
        self.provider = provider
        self.model = model

    def compose(
        self,
        prompts: List[str],
        question: str,
        source_templates: Optional[List[str]] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs,
    ) -> ComposedPrompt:
        """Merge multiple prompt strings into one comprehensive prompt.

        Args:
            prompts: List of prompt strings (from ``Context.to_prompt()``).
            question: The original user question.
            source_templates: Optional list of template names that produced the prompts.
            provider: Override default provider.
            model: Override default model.

        Returns:
            ComposedPrompt with the merged prompt.
        """
        provider = provider or self.provider
        model = model or self.model

        if len(prompts) == 1:
            return ComposedPrompt(
                prompt=prompts[0],
                source_templates=source_templates or [],
                question=question,
                component_prompts=prompts,
                metadata={"composition_mode": "passthrough"},
            )

        numbered = "\n\n".join(
            f"--- Component {i+1} ---\n{p}" for i, p in enumerate(prompts)
        )
        merge_prompt = _COMPOSE_TEMPLATE.format(
            question=question, numbered_prompts=numbered
        )

        ctx = Context(
            guidance=Guidance(
                role=_COMPOSE_SYSTEM,
                rules=[
                    "Output ONLY the merged prompt — no commentary.",
                    "Keep merged prompt between 1000-1800 characters.",
                ],
            ),
            directive=Directive(content=merge_prompt),
        )

        try:
            result = ctx.execute(provider=provider, model=model, **kwargs)
            merged = result.response.strip()
            if merged.startswith("```"):
                lines = merged.split("\n")
                merged = "\n".join(lines[1:-1]).strip()
        except Exception as e:
            merged = self._fallback_merge(prompts, question)
            return ComposedPrompt(
                prompt=merged,
                source_templates=source_templates or [],
                question=question,
                component_prompts=prompts,
                metadata={"composition_mode": "fallback", "error": str(e)},
            )

        return ComposedPrompt(
            prompt=merged,
            source_templates=source_templates or [],
            question=question,
            component_prompts=prompts,
            metadata={"composition_mode": "llm", "model": model},
        )

    def compose_from_templates(
        self,
        question: str,
        template_names: List[str],
        refine: bool = True,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs,
    ) -> ComposedPrompt:
        """Generate prompts from templates and compose them in one call.

        Args:
            question: The user's question.
            template_names: Template names to generate prompts from.
            refine: Whether to LLM-refine individual prompts before composing.
            provider: Override default provider.
            model: Override default model.

        Returns:
            ComposedPrompt with the merged prompt.
        """
        from .pattern_suggester import get_pattern_class
        from .chain_orchestration_agent import PATTERN_BUILD_CONTEXT_REGISTRY

        provider = provider or self.provider
        model = model or self.model
        prompts: List[str] = []
        valid_names: List[str] = []

        for name in template_names:
            klass = get_pattern_class(name, include_enterprise=self.include_enterprise)
            if klass is None:
                continue
            reg = PATTERN_BUILD_CONTEXT_REGISTRY.get(name, ("input", {}))
            primary_key, defaults = reg
            params = dict(defaults)
            params[primary_key] = question
            try:
                ctx = klass().build_context(**params)
                prompt = ctx.to_prompt(refine=refine, provider=provider, model=model)
                prompts.append(prompt)
                valid_names.append(name)
            except Exception:
                continue

        if not prompts:
            fallback = f"Answer this question thoroughly: {question}"
            return ComposedPrompt(
                prompt=fallback,
                source_templates=[],
                question=question,
                metadata={"composition_mode": "empty_fallback"},
            )

        return self.compose(
            prompts=prompts,
            question=question,
            source_templates=valid_names,
            provider=provider,
            model=model,
            **kwargs,
        )

    def compile_generic(
        self,
        question: str,
        template_names: List[str],
        **template_kwargs: Any,
    ) -> ComposedPrompt:
        """Compile generic prompts from multiple templates — zero LLM calls.

        This is the static compilation path: each template's pre-authored
        generic prompt is filled with user inputs, then merged into a single
        self-contained prompt without any LLM refinement.

        Args:
            question: The user's question (injected as the primary input).
            template_names: Template names to compile.
            **template_kwargs: Extra keyword arguments forwarded to each
                template's ``generic_prompt()`` (e.g. ``depth="comprehensive"``).

        Returns:
            ComposedPrompt with the statically compiled prompt.
        """
        from .chain_orchestration_agent import PATTERN_BUILD_CONTEXT_REGISTRY

        prompts: List[str] = []
        valid_names: List[str] = []

        for name in template_names:
            instance, actual_name = _resolve_generic_template(
                name, include_enterprise=self.include_enterprise
            )
            if instance is None:
                continue

            reg = PATTERN_BUILD_CONTEXT_REGISTRY.get(actual_name, ("input", {}))
            primary_key, defaults = reg
            params = dict(defaults)
            params[primary_key] = question
            params.update(template_kwargs)

            try:
                prompt = instance.generic_prompt(**params)
                prompts.append(prompt)
                valid_names.append(actual_name)
            except Exception:
                continue

        if not prompts:
            fallback = f"Answer this question thoroughly: {question}"
            return ComposedPrompt(
                prompt=fallback,
                source_templates=[],
                question=question,
                metadata={"composition_mode": "empty_fallback"},
            )

        merged = self._static_merge(prompts, question, valid_names)
        return ComposedPrompt(
            prompt=merged,
            source_templates=valid_names,
            question=question,
            component_prompts=prompts,
            metadata={
                "composition_mode": "static_generic",
                "llm_calls": 0,
            },
        )

    @staticmethod
    def _static_merge(
        prompts: List[str], question: str, template_names: List[str]
    ) -> str:
        """Merge generic prompts into one prompt — no LLM, pure string ops."""
        if len(prompts) == 1:
            return prompts[0]

        sections = []
        for i, (name, p) in enumerate(zip(template_names, prompts), 1):
            label = name.replace("_", " ").title()
            sections.append(f"[Lens {i}: {label}]\n{p}")
        combined = "\n\n".join(sections)

        return (
            f"You are a multi-disciplinary analyst. Answer the following question "
            f"by applying ALL of the analytical lenses below. Synthesize their "
            f"insights into one unified, comprehensive response.\n\n"
            f"QUESTION: {question}\n\n"
            f"{combined}\n\n"
            f"Integrate findings across all lenses. Resolve any contradictions. "
            f"End with concrete Recommendations and Next Steps."
        )

    @staticmethod
    def _fallback_merge(prompts: List[str], question: str) -> str:
        """Zero-cost fallback: concatenate prompts with section separators."""
        sections = []
        for i, p in enumerate(prompts, 1):
            sections.append(f"[Analytical Lens {i}]\n{p}")
        combined = "\n\n".join(sections)
        return (
            f"Answer the following question using ALL of the analytical approaches below.\n\n"
            f"QUESTION: {question}\n\n"
            f"{combined}\n\n"
            f"Synthesize insights from all lenses into a unified response. "
            f"End with concrete Recommendations / Next Steps."
        )


def get_generic_prompt_for(
    template_name: str,
    question: str,
    include_enterprise: bool = True,
    **kwargs: Any,
) -> Optional[str]:
    """Get a generic prompt for any template, with automatic free-template fallback.

    If the requested template is enterprise and the user is in free mode,
    this function falls back to the closest free template that has a
    ``GENERIC_PROMPT`` and emits a warning so the user knows they're
    getting a simplified version.

    Args:
        template_name: Name of the template (free or enterprise).
        question: The user's question (injected as the primary input).
        include_enterprise: Whether enterprise templates are available.

    Returns:
        The filled generic prompt string, or None if no suitable template found.
    """
    from .chain_orchestration_agent import PATTERN_BUILD_CONTEXT_REGISTRY

    instance, actual_name = _resolve_generic_template(
        template_name,
        include_enterprise=include_enterprise,
        warn_on_fallback=True,
    )
    if instance is None:
        return None

    reg = PATTERN_BUILD_CONTEXT_REGISTRY.get(actual_name, ("input", {}))
    primary_key, defaults = reg
    params = dict(defaults)
    params[primary_key] = question
    params.update(kwargs)

    try:
        return instance.generic_prompt(**params)
    except Exception:
        return None
