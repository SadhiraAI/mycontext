"""
Output format directives for template parameterization.

Templates accept an ``output_format`` parameter that appends a format
instruction to the assembled directive.  This controls *how* the model
presents results without changing *what* it analyses.

Two conceptual groups
---------------------
Human-consumption formats  (control presentation style for a person)
    structured, narrative, brief, actionable, slides, email, qa, checklist

Machine-consumption formats  (control serialization for downstream code)
    json, table

Note: ``json`` and ``table`` should ideally be paired with lower temperature
(0.0–0.2) and, when the provider supports it, ``response_format`` enforcement.
The other formats work well at the default temperature (0.7).

Available formats
-----------------
structured  (default)
    Current behaviour — sections with headers and bullet points.
    No directive is appended; nothing changes.

narrative
    Flowing prose paragraphs, no headers or lists.
    Useful for reports, presentations, and executive summaries.

brief
    Bullet points only, max 2 sentences each, under 300 words total.
    Ideal for Slack/Teams messages, notifications, quick reviews.

actionable
    Actionable items only, each starting with an imperative verb.
    No background analysis. Ideal for ticket creation and ops handoff.

slides
    Slide-ready content: one slide title per finding, 3–5 bullet points
    per slide, no prose paragraphs. Ideal for PowerPoint/Google Slides prep.

email
    Formal email structure: Subject line, short opening, body paragraphs,
    clear ask or next step, sign-off. Ideal for executive communications.

qa
    Question-and-answer pairs. Each finding becomes a Q: / A: pair.
    Ideal for FAQs, knowledge bases, onboarding docs, and chatbot training.

checklist
    Plain checklist items with [ ] prefix, grouped by category.
    Each item is one concise action or verification step.
    Ideal for review checklists, runbooks, and process templates.

json
    Raw JSON object only (no markdown fences, no prose).
    Useful for pipelines, dashboards, and downstream LLM calls.

table
    Markdown table(s) only.
    Useful for risk registers, comparison matrices, tracking views.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Human-consumption formats
# ---------------------------------------------------------------------------
_HUMAN_FORMATS: dict[str, str] = {
    "structured": "",
    "narrative": (
        "\n\n**OUTPUT FORMAT**: Write as flowing prose paragraphs ONLY. "
        "STRICTLY no headers, no bullet lists, no numbered sections. "
        "2–4 paragraphs total. Coherent, readable document."
    ),
    "brief": (
        "\n\n**OUTPUT FORMAT — CRITICAL LENGTH CONSTRAINT**: "
        "Your response MUST be under 150 words total. Count words. "
        "Output ONLY 3–5 bullet points. One short sentence per bullet. "
        "Include ONLY the most critical findings — omit everything else. "
        "If you exceed 150 words, the output is wrong."
    ),
    "actionable": (
        "\n\n**OUTPUT FORMAT — CRITICAL**: "
        "Output ONLY a list of 5–10 items. Each item = ONE line starting with an imperative verb "
        "(Fix, Add, Remove, Update, Implement, Review, Check, Deploy). "
        "NO explanations. NO context. NO paragraphs. NO bullet sub-items. "
        "Example: 'Fix connection pool size.' — that is the entire item. "
        "If any item has more than one line, the output is wrong."
    ),
    "slides": (
        "\n\n**OUTPUT FORMAT — CRITICAL**: "
        "Output EXACTLY 3–5 slides. Each slide:\n"
        "## [Slide Title — one short line]\n"
        "- [Bullet 1]\n- [Bullet 2]\n- [Bullet 3]\n"
        "Maximum 4 bullets per slide. No prose. No paragraphs. "
        "Each bullet = one concise line. Total: 3–5 slides only. "
        "If you produce more than 5 slides or add prose, the output is wrong."
    ),
    "email": (
        "\n\n**OUTPUT FORMAT**: Format as a professional email. "
        "Structure:\n"
        "Subject: [One-line summary]\n\n"
        "[Opening sentence — who this is for and why it matters]\n\n"
        "[2–3 short body paragraphs covering key findings]\n\n"
        "[Clear next step or ask]\n\n"
        "Best regards"
        "\n\nNo bullet lists. Formal but direct tone."
    ),
    "qa": (
        "\n\n**OUTPUT FORMAT**: Format as question-and-answer pairs. "
        "For each key finding or topic, produce:\n"
        "**Q: [Question a reader would ask]**\n"
        "A: [Concise answer, 2–4 sentences]\n\n"
        "Cover all major findings. "
        "Questions should be self-contained — readable without surrounding context."
    ),
    "checklist": (
        "\n\n**OUTPUT FORMAT — CRITICAL**: "
        "Output ONLY a checklist. Group by category with ## heading. "
        "Each item: - [ ] [One action or verification step — single line]\n"
        "5–12 items total. No prose. No explanations. No nested bullets. "
        "Items must be concrete and independently actionable. "
        "If you add paragraphs or explanations, the output is wrong."
    ),
}

# ---------------------------------------------------------------------------
# Machine-consumption formats
# ---------------------------------------------------------------------------
_MACHINE_FORMATS: dict[str, str] = {
    "json": (
        "\n\n**OUTPUT FORMAT**: Respond with a valid JSON object ONLY. "
        "No prose, no markdown code fences, no explanation outside the JSON. "
        "Output raw JSON that can be parsed directly."
    ),
    "table": (
        "\n\n**OUTPUT FORMAT**: Present findings as markdown table(s) only. "
        "Every table must have clear column headers. "
        "No prose sections outside the tables."
    ),
}

_FORMAT_DIRECTIVES: dict[str, str] = {**_HUMAN_FORMATS, **_MACHINE_FORMATS}

# Exposed sets so callers can check format type
HUMAN_OUTPUT_FORMATS: frozenset[str] = frozenset(_HUMAN_FORMATS.keys())
MACHINE_OUTPUT_FORMATS: frozenset[str] = frozenset(_MACHINE_FORMATS.keys())
VALID_OUTPUT_FORMATS: frozenset[str] = frozenset(_FORMAT_DIRECTIVES.keys())


def get_format_directive(output_format: str) -> str:
    """Return the format directive string for the given *output_format*.

    Returns an empty string for ``"structured"`` — the default, which
    leaves the assembled directive unchanged.  All other formats return
    an instruction string to append to the end of the directive.

    Parameters
    ----------
    output_format:
        One of the values in ``VALID_OUTPUT_FORMATS``:
        ``"structured"``, ``"narrative"``, ``"brief"``, ``"actionable"``,
        ``"slides"``, ``"email"``, ``"qa"``, ``"checklist"``,
        ``"json"``, ``"table"``.

    Raises
    ------
    ValueError
        If *output_format* is not a recognised value.
    """
    if output_format not in VALID_OUTPUT_FORMATS:
        raise ValueError(
            f"Invalid output_format {output_format!r}. Choose from: {sorted(VALID_OUTPUT_FORMATS)}"
        )
    return _FORMAT_DIRECTIVES[output_format]


def is_machine_format(output_format: str) -> bool:
    """Return True if *output_format* targets machine consumption (json, table).

    Machine formats benefit from lower temperature and, when supported,
    provider-level response_format enforcement.
    """
    return output_format in MACHINE_OUTPUT_FORMATS
