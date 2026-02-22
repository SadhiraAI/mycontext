"""Chain service: build_workflow_chain, suggest_patterns, run orchestrator.

Depends on litellm for Smart/Hybrid modes via the SDK's LiteLLMProvider.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)

try:
    from mycontext.intelligence import (
        PATTERN_BUILD_CONTEXT_REGISTRY,
        build_workflow_chain,
        get_pattern_class,
        suggest_patterns,
    )
    from mycontext.intelligence.pattern_suggester import NAME_TO_CATEGORY
    from mycontext.templates.enterprise.synthesis import HolisticIntegrator
except ImportError:
    build_workflow_chain = None
    get_pattern_class = None
    PATTERN_BUILD_CONTEXT_REGISTRY = {}
    suggest_patterns = None
    NAME_TO_CATEGORY = {}
    HolisticIntegrator = None


def categories_for_chain(chain: list[str]) -> dict[str, str]:
    """Return {pattern_name: 'free'|'enterprise'} using the master catalog."""
    return {name: NAME_TO_CATEGORY.get(name, "free") for name in chain}


def _inject_api_key_env(provider: str, api_key: str | None):
    """Temporarily set the provider env var so the SDK picks it up."""
    import os
    env_map = {
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "google": "GOOGLE_API_KEY",
        "gemini": "GOOGLE_API_KEY",
    }
    var = env_map.get(provider)
    if var and api_key:
        os.environ[var] = api_key


def suggest_chain(question: str, **kwargs: Any) -> Any:
    """Call build_workflow_chain from SDK. Returns WorkflowChainResult or None."""
    if not build_workflow_chain:
        return None
    provider = kwargs.get("provider", "openai")
    _inject_api_key_env(provider, kwargs.get("api_key"))
    logger.info("suggest_chain: calling build_workflow_chain, provider=%s", provider)
    result = build_workflow_chain(question, **kwargs)
    if result:
        logger.info(
            "suggest_chain result: chain=%s, reasoning_start=%s",
            result.chain,
            (result.reasoning or "")[:200],
        )
    return result


def suggest_patterns_chain(
    question: str,
    mode: str = "keyword",
    include_enterprise: bool = True,
    max_patterns: int = 5,
    **llm_kwargs: Any,
) -> dict[str, Any] | None:
    """Call suggest_patterns. Returns chain, chain_params (registry defaults), reasoning."""
    if not suggest_patterns or not PATTERN_BUILD_CONTEXT_REGISTRY:
        return None
    _inject_api_key_env(llm_kwargs.get("llm_provider", "openai"), llm_kwargs.get("api_key"))
    mode_internal = {"quick": "keyword", "smart": "llm", "best": "hybrid"}.get(mode, mode)
    result = suggest_patterns(
        question,
        mode=mode_internal,
        include_enterprise=include_enterprise,
        suggest_chain=True,
        max_patterns=max_patterns,
        **llm_kwargs,
    )
    chain = result.suggested_chain or [s.name for s in result.suggested_patterns]
    chain = chain[:max_patterns]
    chain_params = {}
    for name in chain:
        reg = PATTERN_BUILD_CONTEXT_REGISTRY.get(name, ("problem", {}))
        primary, defaults = reg
        chain_params[name] = {primary: "<from previous step>", **dict(defaults)}
    return {
        "chain": chain,
        "chain_params": chain_params,
        "reasoning": result.reasoning,
        "selection_reasoning": {s.name: s.reason for s in result.suggested_patterns},
        "source": result.source,
        "suggested_patterns": [
            {"name": s.name, "reason": s.reason, "category": s.category}
            for s in result.suggested_patterns
        ],
    }


def run_orchestrator(
    chain: list[str],
    chain_params: dict[str, dict[str, Any]],
    initial_input: str,
    topic: str = "Task",
    max_chars_per_step: int = 4000,
) -> str | None:
    """Run the chain: each step feeds the next, then HolisticIntegrator."""
    if not get_pattern_class or not HolisticIntegrator:
        return None

    prev = initial_input
    for name in chain:
        Klass = get_pattern_class(name, include_enterprise=True)
        if not Klass:
            continue
        reg = PATTERN_BUILD_CONTEXT_REGISTRY.get(name)
        primary = reg[0] if reg else "problem"
        params = dict(chain_params.get(name, {}))
        params[primary] = prev
        ctx = Klass().build_context(**params)
        prev = ctx.directive.content[:max_chars_per_step] if ctx.directive else ""

    integrator = HolisticIntegrator()
    final = integrator.build_context(topic=topic, perspectives=f"Reasoning from chain:\n{prev}")
    return final.directive.content if final.directive else None


def generate_integrated_template(
    question: str,
    selected_templates: list[str],
    selection_reasoning: dict[str, str],
    provider: str = "openai",
    api_key: str | None = None,
    include_enterprise: bool = True,
) -> dict[str, Any] | None:
    """Use TemplateIntegratorAgent to merge selected templates into one unified context."""
    _inject_api_key_env(provider, api_key)
    try:
        from mycontext.intelligence import TemplateIntegratorAgent
    except ImportError:
        return None

    try:
        agent = TemplateIntegratorAgent(include_enterprise=include_enterprise)
        exec_kw: dict[str, Any] = {}
        if api_key:
            exec_kw["api_key"] = api_key
        result = agent.integrate(
            question=question,
            template_names=selected_templates,
            provider=provider,
            selection_reasoning=selection_reasoning,
            **exec_kw,
        )
        return {
            "integrated_template": result.integrated_context,
            "source_templates": result.source_templates,
            "question": result.question,
            "role": result.role,
            "rules": result.rules,
            "directive": result.directive,
            "output_requirements": result.output_requirements,
        }
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}


def compile_prompt(
    question: str,
    template_names: list[str],
    provider: str = "openai",
    api_key: str | None = None,
    include_enterprise: bool = True,
    refine: bool = True,
) -> dict[str, Any] | None:
    """Compile templates into a single reusable prompt (LLM-refined)."""
    _inject_api_key_env(provider, api_key)
    try:
        from mycontext.intelligence import PromptComposer
    except ImportError:
        return None
    try:
        composer = PromptComposer(include_enterprise=include_enterprise, provider=provider)
        result = composer.compose_from_templates(
            question=question, template_names=template_names, refine=refine, provider=provider,
        )
        return {
            "prompt": result.prompt,
            "source_templates": result.source_templates,
            "chars": len(result.prompt),
            "mode": "dynamic_compiled",
            "metadata": result.metadata,
        }
    except Exception as e:
        return {"error": str(e)}


def compile_generic(
    question: str,
    template_names: list[str],
    include_enterprise: bool = True,
) -> dict[str, Any] | None:
    """Compile generic prompts statically — zero LLM calls."""
    try:
        from mycontext.intelligence import PromptComposer
    except ImportError:
        return None
    try:
        composer = PromptComposer(include_enterprise=include_enterprise)
        result = composer.compile_generic(question=question, template_names=template_names)
        return {
            "prompt": result.prompt,
            "source_templates": result.source_templates,
            "chars": len(result.prompt),
            "mode": "static_generic",
            "metadata": result.metadata,
        }
    except Exception as e:
        return {"error": str(e)}


def export_context(assembled: str) -> dict[str, Any]:
    """Export assembled content to all formats."""
    try:
        from mycontext import Context

        ctx = Context(directive=assembled)
        return {
            "markdown": assembled,
            "json": ctx.to_json(),
            "yaml": ctx.to_yaml(),
            "openai": ctx.to_openai(),
            "anthropic": ctx.to_anthropic(),
            "google": ctx.to_google(),
            "langchain": ctx.to_langchain(),
            "llamaindex": ctx.to_llamaindex(),
        }
    except Exception:
        return {"markdown": assembled}
