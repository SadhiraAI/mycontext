"""
Custom Summarization Template

Standalone template using mycontext's Context API. No package changes.
Based on: docs/SUMMARIZATION_COGNITIVE_TEMPLATE_RESEARCH.md

Usage:
    from summarization_custom_template import build_summarization_context, summarize

    ctx = build_summarization_context(text="Long document...", goal="Executive summary")
    result = ctx.execute(provider="openai")
"""

from __future__ import annotations

from typing import Literal


def _render(prefix: str, value: str | None) -> str:
    if value:
        return f"\n**{prefix}**: {value}\n"
    return ""


def _render_list(prefix: str, items: list[str] | None) -> str:
    if items:
        return f"\n**{prefix}**: {', '.join(items)}\n"
    return ""


DIRECTIVE_TEMPLATE = """Summarize this text preserving key information.

**SOURCE TEXT TO SUMMARIZE**:
{source_text}

**GOAL**: {goal}
{target_length_section}{domain_section}{preserve_section}
{context_section}

**METHODOLOGY** (research-backed: Kintsch–van Dijk, ARC principles):

1. **SOURCE & DOMAIN ANALYSIS**
   - Domain type: [legal | scientific | narrative | technical | general]
   - Expected schema: [key slots to preserve—e.g., claim, evidence, conclusion]

2. **PROPOSITION & CHUNK EXTRACTION**
   - Identify main propositions and local coherence
   - Note natural chunk boundaries (sections, paragraphs, arguments)

3. **ARGUMENT STRUCTURE MAP**
   - Claims: [main assertions]
   - Evidence: [supporting facts, data]
   - Warrants/reasoning: [connective logic]
   - Caveats/qualifiers: [nuances that must not be lost]

4. **MACRO-OPERATOR APPLICATION**
   - Delete: irrelevant detail
   - Generalize: specifics → superordinates where appropriate
   - Construct: infer high-level gist where needed

5. **HIERARCHICAL SUMMARY**
   - Executive summary (2–4 sentences)
   - Key points (bulleted, ordered by importance)
   - Critical details (numbers, names, dates, caveats) as needed for goal

6. **COVERAGE CHECK**
   - For each argument role: is it represented in the summary?
   - Flag any omission of critical information

7. **FAITHFULNESS VERIFICATION**
   - Each summary claim must trace to source
   - Remove or qualify any claim that cannot be traced
   - No unsupported inferences

**OUTPUT FORMAT**:
- **Executive Summary**: [2–4 sentences]
- **Key Points**: [numbered list]
- **Critical Details**: [if applicable: numbers, dates, parties, caveats]
- **Omissions/Scope**: [brief note on what was excluded and why]
"""

TARGET_LENGTH_MAP = {
    "brief": "Target: Brief (1–2 paragraphs, ~100–150 words)",
    "moderate": "Target: Moderate (3–5 key points + executive summary)",
    "comprehensive": "Target: Comprehensive (full key points, evidence trace, caveats)",
}


def build_summarization_context(
    text: str,
    goal: str = "Preserve key information for downstream use",
    target_length: Literal["brief", "moderate", "comprehensive"] = "moderate",
    domain: str | None = None,
    preserve: list[str] | None = None,
    context: str | None = None,
):
    """
    Build a mycontext Context with the summarization cognitive template.

    Uses existing mycontext API — no package modifications.

    Args:
        text: Source text to summarize
        goal: What the summary is for
        target_length: brief | moderate | comprehensive
        domain: Optional hint (legal, scientific, narrative, technical)
        preserve: Optional list of what must not be dropped
        context: Optional additional context

    Returns:
        Context ready for ctx.execute(provider="openai")
    """
    from mycontext import Context, Directive, Guidance, Constraints

    source_text = text.strip() if text else "[Provide text to summarize]"
    target_section = _render(
        "TARGET LENGTH",
        TARGET_LENGTH_MAP.get(target_length, TARGET_LENGTH_MAP["moderate"]),
    )
    domain_section = _render("DOMAIN HINT", domain)
    preserve_section = _render_list("MUST PRESERVE", preserve)
    context_section = _render("ADDITIONAL CONTEXT", context)

    directive_content = DIRECTIVE_TEMPLATE.format(
        source_text=source_text,
        goal=goal,
        target_length_section=target_section,
        domain_section=domain_section,
        preserve_section=preserve_section,
        context_section=context_section,
    )

    guidance = Guidance(
        role="Expert Summarization Specialist",
        rules=[
            "Preserve argument structure (claims, evidence, warrants)",
            "Trace every summary claim to source",
            "Omit uncertain or unsupported content",
            "Apply macro-operators: delete, generalize, construct",
            "Produce hierarchical key points when helpful",
        ],
        style="faithful, structured, concise",
    )

    constraints = Constraints(
        must_include=["executive_summary", "key_points"],
        must_not_include=["unsupported_claims", "hallucinations"],
        style_guide="Be faithful to the source. Preserve argument structure. Omit uncertain content.",
    )

    return Context(
        guidance=guidance,
        directive=Directive(content=directive_content),
        constraints=constraints,
        data={"text": text, "goal": goal},
        metadata={"template": "summarization_custom"},
    )


def get_langchain_prompts(
    map_goal: str = "Extract key facts for roll-up into final summary",
    combine_goal: str = "Integrate into a single coherent executive summary",
    domain: str | None = None,
) -> tuple[str, str]:
    """
    Return (map_template, combine_template) for LangChain load_summarize_chain.

    Both use {text} as the input variable (LangChain convention).
    Map step: summarizes each chunk.
    Combine step: integrates chunk summaries into final summary.

    Usage:
        from langchain.chains.summarize import load_summarize_chain
        from langchain_core.prompts import PromptTemplate

        map_tpl, combine_tpl = get_langchain_prompts()
        chain = load_summarize_chain(
            llm=...,
            chain_type="map_reduce",
            map_prompt=PromptTemplate(template=map_tpl, input_variables=["text"]),
            combine_prompt=PromptTemplate(template=combine_tpl, input_variables=["text"]),
        )
    """
    domain_section = _render("DOMAIN HINT", domain) if domain else ""

    map_template = f"""You are an Expert Summarization Specialist. Preserve key information.

RULES: Preserve argument structure (claims, evidence). Trace claims to source. Omit uncertain content.

**SOURCE CHUNK TO SUMMARIZE** (section of a longer document):
{{text}}

**GOAL**: {map_goal}
**TARGET**: Brief — key facts, numbers, dates, names. ~100-150 words.
{domain_section}

Apply: identify main propositions, argument structure, macro-operators (delete/generalize/construct). Output key points only."""

    combine_template = f"""You are an Expert Summarization Specialist. Integrate section summaries into one coherent whole.

RULES: Preserve all key facts from the section summaries. Deduplicate. Maintain chronological/causal order. No new information not in the summaries.

**SECTION SUMMARIES TO INTEGRATE**:
{{text}}

**GOAL**: {combine_goal}
**TARGET**: Executive summary + numbered key points. Critical details (numbers, dates) preserved.

Output format:
- **Executive Summary**: [2-4 sentences]
- **Key Points**: [numbered list]
- **Critical Details**: [if applicable]"""

    return map_template, combine_template


def summarize(
    text: str,
    provider: str = "openai",
    goal: str = "Preserve key information for downstream use",
    target_length: Literal["brief", "moderate", "comprehensive"] = "moderate",
    domain: str | None = None,
    preserve: list[str] | None = None,
    context: str | None = None,
    **provider_kwargs,
):
    """
    One-liner: build context and execute.

    Returns:
        ProviderResponse with .response and .metadata
    """
    ctx = build_summarization_context(
        text=text,
        goal=goal,
        target_length=target_length,
        domain=domain,
        preserve=preserve,
        context=context,
    )
    return ctx.execute(provider=provider, **provider_kwargs)
