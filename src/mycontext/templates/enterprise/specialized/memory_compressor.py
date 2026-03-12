"""
Memory Compressor — Structured state extraction from conversations and documents

The industry default for agent memory is "summarize the conversation." That
loses entities, decisions, constraints, and intent.  MemoryCompressor extracts
**structured state**, not prose summaries — so downstream agents can reconstruct
context from a fraction of the original tokens.

Supports configurable **detail levels** that control the trade-off between
compression ratio and information preservation:

- ``minimal``: Maximum compression — entities, decisions, constraints only.
- ``standard``: Balanced (default) — adds timeline, open items, numbers index.
- ``narrative``: Adds episodic sections — events, causal chains.
- ``full``: Complete extraction — adds state transitions and rationale.

Research foundation:
- **SimpleMem** (Modarressi et al. 2024): Entity-level memory compression —
  extract and maintain per-entity state instead of running summaries.
- **CDIC** (Ge et al. 2024): Revisable Compression with progressive updates —
  compressed states can be incrementally updated, not rebuilt from scratch.
- **RECOMP** (Xu et al. 2024): Extractive + abstractive compression for RAG —
  pull key sentences first, then compress.
- **Running Summary** (LangChain default): Baseline progressive approach that
  loses specifics over multiple compressions.
- **Cognitive Load Theory** (Sweller 1988): Reduce extraneous load, preserve
  germane load — applied to memory: discard filler, preserve decisions.

Episodic/narrative memory research:
- **SEEM** (arXiv 2601.06411): Structured Episodic Event Memory — graph layer
  for relational facts + temporal event layer with provenance pointers.
- **TraceMem** (arXiv 2602.09712): Three-stage cognitive pipeline — episode
  segmentation, episodic summarization, narrative thread consolidation.
- **ENGRAM** (arXiv 2511.12960): Episodic/semantic/procedural memory types
  with a router — exceeds full-context by 15 points using ~1% of tokens.
- **CogMem** (arXiv 2512.14118): Three-layer cognitive architecture — LTM,
  direct-access memory, and focus of attention for multi-turn reasoning.
- **GSW** (arXiv 2511.07587, NeurIPS 2025): Structured workspace tracking
  entities through evolving roles — outperforms RAG by 20%, 51% fewer tokens.
- **Nature Reviews Psychology 2025**: Memory as adaptive compression — semantic
  memory provides the compression codebook, episodic memory preserves what the
  codebook can't yet explain. Surprise determines preservation detail.

Additional sources:
- MemWalker (Chen et al. 2023): Tree-structured long-context navigation
- ReadAgent (Lee et al. 2024): Episode-based compression with gist memory
"""

from __future__ import annotations

from typing import ClassVar

from mycontext.foundation import Constraints, Directive, Guidance
from mycontext.structure import Pattern

# ---------------------------------------------------------------------------
# Modular section definitions — each section has session & progressive variants
# ---------------------------------------------------------------------------

_SECTION_DEFINITIONS: dict[str, dict[str, str]] = {
    "entities": {
        "session": (
            "## ENTITIES\n"
            "(Every person, company, project, system, tool, standard, version "
            "— include ALL associated numbers inline)\n"
            "- [Entity]: [Role] — [every fact, number, size, cost, date "
            "associated with this entity]\n"
            'Example: "Rachel Kim: [CTO] — leads 23-person team, approved '
            '$2.4M budget for 18-month timeline"'
        ),
        "progressive": (
            "## ENTITIES (updated)\n"
            "(Carry forward ALL existing entities. Add new ones. "
            "Update changed ones.)\n"
            "- [Entity]: [Role] — [all numbers/facts inline] "
            "[NEW/UPDATED/unchanged]"
        ),
    },
    "decisions": {
        "session": (
            "## DECISIONS\n"
            "(What was decided — include the numbers/metrics that "
            "informed the decision)\n"
            "- [Decision]: [Full rationale with specific numbers] "
            "— decided by [who]"
        ),
        "progressive": (
            "## DECISIONS (updated)\n"
            "(Carry forward ALL existing decisions. Add new ones. "
            "Mark changes.)\n"
            "- [Decision]: [Rationale with numbers] — [who] "
            "[NEW/CHANGED from: X/unchanged]"
        ),
    },
    "constraints": {
        "session": (
            "## CONSTRAINTS & REQUIREMENTS\n"
            "(Hard limits with exact thresholds — every number matters)\n"
            "- [Constraint]: [Exact value/threshold/date] — [source/reason]"
        ),
        "progressive": (
            "## CONSTRAINTS & REQUIREMENTS (updated)\n"
            "(Carry forward ALL existing constraints. Add new ones.)\n"
            "- [Constraint]: [Exact value/threshold] — [source] "
            "[NEW/UPDATED/unchanged]"
        ),
    },
    "events": {
        "session": (
            "## KEY EVENTS & INCIDENTS\n"
            "(Significant things that HAPPENED — incidents, discoveries, "
            "changes, milestones, failures, breakthroughs.\n"
            "CRITICAL: Include the SPECIFIC TECHNICAL DETAILS of each event — "
            "exact component names, error types, quantities affected, durations, "
            "thresholds breached. Do NOT summarize an event as 'security issue found' "
            "when the source says WHAT the issue was, WHERE it was, WHEN it started, "
            "and HOW MANY items were affected.)\n"
            "- [Date/When]: [What happened — with exact technical specifics] "
            "— [Quantified impact] — [Who was involved]\n"
            'Example: "March 5: Token refresh middleware writing full OAuth bearer '
            "tokens to application log file since Feb 1 — ~14,000 tokens exposed, "
            'required immediate invalidation — discovered by Frank during security audit"'
        ),
        "progressive": (
            "## KEY EVENTS & INCIDENTS (updated)\n"
            "(Carry forward ALL existing events with their full technical detail. "
            "Add new events from new turns.)\n"
            "- [Date/When]: [What happened — exact specifics] — [Impact] — [Who] "
            "[NEW/unchanged]"
        ),
    },
    "causal_chains": {
        "session": (
            "## CAUSAL CHAINS\n"
            "(Why things happened — trace cause to effect with SPECIFIC details "
            "at each step. Each link in the chain must include the exact technical "
            "facts, not vague summaries.)\n"
            "- [Specific trigger with details] \u2192 [Specific consequence with "
            "numbers] \u2192 [Specific outcome/decision]\n"
            'Example: "SQLAlchemy 2.1.0 JSONB query bug \u2192 3 failing unit tests '
            "on PostgreSQL 15 \u2192 downgraded to 2.0.23, all tests passing\"\n"
            'Example: "No rate limiting on POST /auth/login \u2192 unlimited brute-force '
            "possible \u2192 Bob added 10 req/s/IP middleware + Dave added WAF rule "
            '100 attempts/hr/IP"'
        ),
        "progressive": (
            "## CAUSAL CHAINS (updated)\n"
            "(Carry forward ALL existing chains with full detail. Extend where "
            "new turns reveal additional consequences.)\n"
            "- [Specific trigger] \u2192 [Specific consequence] \u2192 [Outcome] "
            "[NEW/EXTENDED/unchanged]"
        ),
    },
    "state_transitions": {
        "session": (
            "## STATE TRANSITIONS\n"
            "(Before/after snapshots for significant changes — "
            "technology swaps, role changes, scope adjustments)\n"
            "- [What changed]: [Before] \u2192 [After] — [When/Why]\n"
            'Example: "Cache layer: Redis 7.2 \u2192 Valkey 8.0 — '
            'Week 3, triggered by March 5 outage"'
        ),
        "progressive": (
            "## STATE TRANSITIONS (updated)\n"
            "(Carry forward ALL existing transitions. Add new transitions "
            "from new turns.)\n"
            "- [What changed]: [Before] \u2192 [After] — [When/Why] "
            "[NEW/unchanged]"
        ),
    },
    "context_rationale": {
        "session": (
            "## CONTEXT & RATIONALE\n"
            "(Background reasoning and motivations that explain the 'why' "
            "behind decisions — alternatives considered, trade-offs weighed)\n"
            "- [Decision/Choice]: [Why this was chosen over alternatives]"
        ),
        "progressive": (
            "## CONTEXT & RATIONALE (updated)\n"
            "(Carry forward ALL existing rationale. Add new reasoning "
            "from new turns.)\n"
            "- [Decision/Choice]: [Why this over alternatives] "
            "[NEW/UPDATED/unchanged]"
        ),
    },
    "timeline": {
        "session": (
            "## TIMELINE & ACTION ITEMS\n"
            "(Who does what, by when — include every mentioned date "
            "and deadline)\n"
            "- [Person]: [Task] — [deadline/schedule]"
        ),
        "progressive": (
            "## TIMELINE & ACTION ITEMS (updated)\n"
            "- [Person]: [Task] — [deadline] [NEW/UPDATED/unchanged]"
        ),
    },
    "open_items": {
        "session": (
            "## OPEN ITEMS\n"
            "(Unresolved questions, pending decisions, blockers)\n"
            "- [Item]: [Status/context]"
        ),
        "progressive": (
            "## OPEN ITEMS (updated)\n"
            "- [Item]: [Status] [NEW/RESOLVED/unchanged]"
        ),
    },
    "key_numbers": {
        "session": (
            "## KEY NUMBERS INDEX\n"
            "(Safety net — list EVERY quantitative value from the "
            "conversation, grouped naturally. This index must be complete "
            "even if numbers also appear above.)\n"
            "- Monetary values: [list all dollar amounts, costs, budgets, "
            "prices, revenue figures]\n"
            "- Dates & durations: [list all dates, deadlines, timelines, "
            "durations]\n"
            "- Measurements & metrics: [list all percentages, sizes, counts, "
            "rates, thresholds, SLAs, scores]"
        ),
        "progressive": (
            "## KEY NUMBERS INDEX (updated)\n"
            "(Carry forward ALL numbers from existing memory + add new "
            "numbers from new turns)\n"
            "- Monetary values: [list all \u2014 existing + new]\n"
            "- Dates & durations: [list all \u2014 existing + new]\n"
            "- Measurements & metrics: [list all \u2014 existing + new]"
        ),
    },
    "changes_this_update": {
        "progressive": (
            "## CHANGES THIS UPDATE\n"
            "(Brief list of what changed from the previous memory state)"
        ),
    },
}

# ---------------------------------------------------------------------------
# Detail level presets — map level name → ordered list of section keys
# ---------------------------------------------------------------------------

_DETAIL_LEVELS: dict[str, list[str]] = {
    "minimal": [
        "entities", "decisions", "constraints",
    ],
    "standard": [
        "entities", "decisions", "constraints",
        "timeline", "open_items", "key_numbers",
    ],
    "narrative": [
        "entities", "decisions", "constraints",
        "events", "causal_chains",
        "timeline", "open_items", "key_numbers",
    ],
    "full": [
        "entities", "decisions", "constraints",
        "events", "causal_chains", "state_transitions", "context_rationale",
        "timeline", "open_items", "key_numbers",
    ],
}

VALID_DETAIL_LEVELS: frozenset[str] = frozenset(_DETAIL_LEVELS)

_EPISODIC_SECTION_KEYS: frozenset[str] = frozenset({
    "events", "causal_chains", "state_transitions", "context_rationale",
})


# ---------------------------------------------------------------------------
# Dynamic output structure composition
# ---------------------------------------------------------------------------

def _compose_output_structure(sections: list[str], intent: str) -> str:
    """Build output structure text by joining section templates for *intent*."""
    parts = []
    for key in sections:
        defn = _SECTION_DEFINITIONS[key]
        if intent in defn:
            parts.append(defn[intent])
    if intent == "progressive":
        parts.append(_SECTION_DEFINITIONS["changes_this_update"]["progressive"])
    return "\n" + "\n\n".join(parts) + "\n"


# ---------------------------------------------------------------------------
# Intent-specific instruction builders
# ---------------------------------------------------------------------------

_WORD_BUDGET: dict[str, str] = {
    "minimal": "300–450",
    "standard": "450–600",
    "narrative": "700–1000",
    "full": "900–1200",
}


def _build_session_instructions(sections: list[str], detail_level: str = "standard") -> str:
    """Build session-intent instructions with enumeration steps matching *sections*."""
    section_set = set(sections)

    base_enum = (
        "1. ENUMERATE first \u2014 before writing anything, mentally list:\n"
        "   a. Every PERSON mentioned (name, role, what they own)\n"
        "   b. Every TECHNOLOGY/TOOL with version numbers\n"
        "   c. Every DOLLAR AMOUNT, cost, and budget figure\n"
        "   d. Every DATE, deadline, and duration\n"
        "   e. Every DECISION and who made it\n"
        "   f. Every CONSTRAINT, SLA, or hard requirement\n"
    )

    addon_parts: list[str] = []
    letter = ord("g")
    if "events" in section_set:
        addon_parts.append(
            f"   {chr(letter)}. Every significant EVENT or INCIDENT — with FULL "
            f"technical specifics: exact component/system affected, what went wrong "
            f"or changed, quantities involved, dates, duration. Never reduce an "
            f"event to a vague label like 'security issue' — spell out the specifics.\n"
        )
        letter += 1
    if "causal_chains" in section_set:
        addon_parts.append(
            f"   {chr(letter)}. Every CAUSE\u2192EFFECT chain with specific details "
            f"at each step (not 'problem found \u2192 fixed' but 'specific problem "
            f"with exact details \u2192 specific fix with parameters')\n"
        )
        letter += 1
    if "state_transitions" in section_set:
        addon_parts.append(
            f"   {chr(letter)}. Every STATE TRANSITION "
            f"(before/after for significant changes)\n"
        )
        letter += 1
    if "context_rationale" in section_set:
        addon_parts.append(
            f"   {chr(letter)}. The RATIONALE behind each major decision "
            f"(why this over alternatives)\n"
        )
        letter += 1

    enumeration = base_enum + "".join(addon_parts) + (
        "   If a person, number, or technology appears even once, it must "
        "appear in your output.\n"
    )

    return (
        "You are compressing a conversation into structured state.\n\n"
        "Process:\n"
        + enumeration
        + "2. DISCARD filler: greetings, confirmations ('sounds good'), "
        "repeated statements, thinking-out-loud, pleasantries.\n"
        "3. EXTRACT into the structured sections below. "
        "Preserve exact names, versions, dates, numbers, and technical terms \u2014 "
        "do NOT paraphrase away precision.\n"
        "4. INLINE ALL NUMBERS \u2014 every dollar amount, percentage, duration, "
        "size, latency, date, count, and threshold MUST appear in the same "
        "bullet point as the entity or decision it belongs to. "
        "Do NOT strip numbers from context. If the database is 847GB, "
        "the entity bullet must say '847GB'. If the budget is $15,000 "
        "broken into $4,200 + $8,500, the decision bullet must include all three.\n"
        "5. CROSS-CHECK: Count every dollar amount in the conversation. "
        "Count every dollar amount in your output. They MUST match. "
        "Do the same for dates, person names, and technology names. "
        "If any count is lower in your output, you dropped information \u2014 "
        "go back and add the missing items.\n\n"
        "Output ONLY the structured sections. No prose introduction or summary paragraph.\n\n"
        + (
            f"TARGET LENGTH: {_WORD_BUDGET[detail_level]} words. "
            "Use the full budget to preserve detail — do NOT over-compress. "
            "It is better to include a specific fact you're unsure about than "
            "to omit it for brevity."
            if detail_level in _WORD_BUDGET
            else ""
        )
    )


def _build_progressive_instructions(sections: list[str], detail_level: str = "standard") -> str:
    """Build progressive-intent instructions adapted for *sections*."""
    section_set = set(sections)
    has_episodic = bool(section_set & _EPISODIC_SECTION_KEYS)

    scan_items = (
        "new entities, changed decisions, resolved questions, "
        "new constraints, updated preferences"
    )
    if "events" in section_set:
        scan_items += ", new events/incidents"
    if "causal_chains" in section_set:
        scan_items += ", cause\u2192effect chains"
    if "state_transitions" in section_set:
        scan_items += ", state transitions"
    if "context_rationale" in section_set:
        scan_items += ", new rationale/reasoning"

    merge_addon = ""
    if has_episodic:
        merge_addon = (
            "   - KEEP all existing events, causal chains, and state transitions\n"
            "   - ADD new events from new turns with timestamps\n"
            "   - EXTEND causal chains where new turns reveal additional "
            "consequences\n"
        )

    return (
        "You are UPDATING an existing compressed memory with new conversation "
        "turns.\n\n"
        "CRITICAL RULE: Treat existing memory as GROUND TRUTH. Every entity, "
        "number, decision, and constraint in the existing memory MUST appear "
        "in your output unless the new turns EXPLICITLY invalidate it. "
        "When in doubt, KEEP the existing information.\n\n"
        "Process:\n"
        "1. READ the existing memory state. Count its entities, decisions, "
        "and constraints.\n"
        f"2. SCAN the new turns for: {scan_items}.\n"
        "3. MERGE:\n"
        "   - KEEP all existing items that are not contradicted by new turns\n"
        "   - ADD new entities, decisions, constraints from the new turns\n"
        "   - UPDATE items where new turns explicitly change them "
        "(mark: CHANGED from [old] \u2192 [new])\n"
        "   - RESOLVE open items that new turns answer\n"
        "   - Only REMOVE an item if new turns explicitly invalidate it\n"
        + merge_addon
        + "4. CROSS-CHECK: Your output must have AT LEAST as many entities "
        "and numbers as the existing memory plus any new ones from the new turns. "
        "If your entity count is LOWER than the existing memory, you dropped "
        "information \u2014 go back and restore it.\n"
        "5. VERIFY: the updated state is complete and self-contained \u2014 "
        "someone reading ONLY this state should understand the full context.\n\n"
        "Output the complete updated structured state (not a diff).\n\n"
        + (
            f"TARGET LENGTH: {_WORD_BUDGET[detail_level]} words. "
            "Use the full budget — do NOT over-compress."
            if detail_level in _WORD_BUDGET
            else ""
        )
    )


_CONTEXT_INSTRUCTIONS: str = (
    "You are compressing a large document into a dense factual representation.\n\n"
    "Process:\n"
    "1. EXTRACT all key claims, facts, figures, names, dates, and relationships.\n"
    "2. PRESERVE exact terminology \u2014 do not substitute synonyms for technical terms.\n"
    "3. ORGANIZE by topic/theme rather than by document order.\n"
    "4. MAXIMIZE information density \u2014 every sentence should carry facts, "
    "not transitions or filler.\n"
    "5. VERIFY: could someone answer detailed questions about the original document "
    "using only your compression? If not, add what's missing.\n\n"
    "Optimize for information density, not readability."
)

_CONTEXT_OUTPUT_STRUCTURE: str = """
## KEY FACTS & CLAIMS
(Core factual content, preserving all specifics)
- [Fact]: [Supporting detail]

## ENTITIES & RELATIONSHIPS
(People, organizations, systems mentioned — with connections)
- [Entity]: [Role/relationship]

## QUANTITATIVE DATA
(Numbers, dates, metrics, measurements)
- [Data point]: [Context]

## ARGUMENTS & CONCLUSIONS
(Main arguments, their evidence, and conclusions drawn)
- [Argument]: [Evidence] → [Conclusion]

## GAPS & CAVEATS
(What the document doesn't cover, acknowledged limitations)
- [Gap/caveat]
"""

# ---------------------------------------------------------------------------
# Directive template (unchanged)
# ---------------------------------------------------------------------------

_DIRECTIVE_TEMPLATE = """{instructions}

{goal_section}

---

### INPUT

{content}

{existing_memory_section}

---

### OUTPUT STRUCTURE

{output_structure}"""


class MemoryCompressor(Pattern):
    """
    Compress conversations and documents into structured, recall-optimized state.

    Unlike plain summarization which produces readable prose, MemoryCompressor
    extracts **structured state** — entities, decisions, constraints, and open
    items — that downstream agents can use to reconstruct context from a
    fraction of the original tokens.

    **intent** controls the compression mode:

    - ``session``: Full conversation → structured state (entities, decisions,
      constraints, preferences, open items). Discards filler and pleasantries.
    - ``progressive``: Update existing compressed memory with new conversation
      turns. Merges, resolves contradictions, marks changes.
    - ``context``: Large document → dense factual representation optimized for
      information density over readability.

    **detail_level** controls the recall-vs-compression trade-off (``session``
    and ``progressive`` intents only):

    - ``minimal``: Maximum compression — entities, decisions, constraints.
    - ``standard``: Balanced (default) — adds timeline, open items, numbers index.
    - ``narrative``: Adds episodic sections — events/incidents, causal chains.
    - ``full``: Complete extraction — adds state transitions and rationale.

    Alternatively, pass ``custom_sections`` as a list of section keys for
    full control over which sections are extracted.  Available section keys:
    ``entities``, ``decisions``, ``constraints``, ``events``, ``causal_chains``,
    ``state_transitions``, ``context_rationale``, ``timeline``, ``open_items``,
    ``key_numbers``.

    Research basis:
        SimpleMem (entity-level), CDIC (progressive), RECOMP (extractive+abstractive),
        Cognitive Load Theory (discard extraneous, preserve germane),
        SEEM (episodic events), TraceMem (narrative consolidation),
        ENGRAM (typed memory), CogMem (cognitive architecture).

    Example:
        >>> from mycontext.templates.enterprise.specialized import MemoryCompressor
        >>> mc = MemoryCompressor()
        >>> ctx = mc.build_context(
        ...     content=conversation_text,
        ...     intent="session",
        ... )
        >>> result = ctx.execute(provider="openai")

    Example (narrative detail level):
        >>> result = mc.execute(
        ...     provider="openai",
        ...     content=conversation_text,
        ...     intent="session",
        ...     detail_level="narrative",
        ... )

    Example (custom sections):
        >>> result = mc.execute(
        ...     provider="openai",
        ...     content=conversation_text,
        ...     intent="session",
        ...     custom_sections=["entities", "decisions", "events", "causal_chains"],
        ... )

    Example (progressive update):
        >>> ctx = mc.build_context(
        ...     content=new_turns,
        ...     intent="progressive",
        ...     existing_memory=previous_compressed_state,
        ... )
        >>> result = ctx.execute(provider="openai")

    Enterprise Template — Requires enterprise license.
    """

    GENERIC_PROMPT = (
        "You are a context compression specialist. Extract structured state "
        "from conversations and documents — not prose summaries.\n\n"
        "Content to compress:\n{content}\n\n"
        "Rules: Extract ALL entities (names, systems, versions, dates) with "
        "relationships. Extract ALL decisions with rationale. Extract ALL "
        "constraints and requirements. Discard filler (greetings, confirmations, "
        "repetition, thinking-out-loud). Preserve exact terminology — never "
        "substitute synonyms for technical terms. After compressing, verify: "
        "could someone reconstruct the key intent and state from your output alone? "
        "If content is empty or incoherent, say so."
    )

    VALID_INTENTS: ClassVar[frozenset[str]] = frozenset({
        "session", "progressive", "context"
    })

    VALID_DETAIL_LEVELS: ClassVar[frozenset[str]] = VALID_DETAIL_LEVELS

    AVAILABLE_SECTIONS: ClassVar[frozenset[str]] = frozenset(
        k for k in _SECTION_DEFINITIONS if k != "changes_this_update"
    )

    def __init__(self):
        super().__init__(
            name="memory_compressor",
            description="Compress conversations/documents into structured state",
            guidance=Guidance(
                role="Context Compression Specialist",
                rules=[
                    "Extract structured state, not prose summaries",
                    "Preserve ALL entities (people, companies, projects, acquisitions, systems, tools, compliance standards, dates, versions) with relationships",
                    "Preserve ALL decisions and their rationale",
                    "Preserve ALL numbers: dollar amounts, sizes, latencies, thresholds, percentages, durations — ZERO tolerance for dropping numbers",
                    "Preserve constraints, requirements, SLAs, and budget details",
                    "Discard filler: greetings, confirmations, repetition, thinking-out-loud",
                    "CROSS-CHECK before finishing: count persons, dollar amounts, and dates in input vs output — output count must be >= input count",
                    "If content is empty or incoherent, say so",
                ],
                style="structured, precise, exhaustive on facts, zero filler",
            ),
            directive_template=_DIRECTIVE_TEMPLATE,
            input_schema={
                "content": str,
                "intent": str,
                "existing_memory": str,
                "goal": str,
                "detail_level": str,
                "custom_sections": list,
            },
            constraints=Constraints(
                must_include=["entities", "decisions", "constraints", "key numbers index"],
                style_guide=(
                    "Maximize factual density. Preserve every specific name, number, "
                    "date, and technical term. No prose filler. The KEY NUMBERS INDEX "
                    "must be a complete enumeration of all quantitative data."
                ),
            ),
        )

    def build_context(
        self,
        content: str = "",
        intent: str = "session",
        existing_memory: str = "",
        goal: str = "",
        detail_level: str = "standard",
        custom_sections: list[str] | None = None,
        **kwargs,
    ):
        """
        Build context for memory compression.

        Args:
            content: Conversation history or document text to compress.
            intent: ``"session"`` | ``"progressive"`` | ``"context"``
            existing_memory: For ``progressive`` — the previous compressed state.
            goal: Optional hint about what the memory will be used for.
            detail_level: ``"minimal"`` | ``"standard"`` | ``"narrative"`` |
                ``"full"`` — controls which sections are extracted.  Ignored
                when *intent* is ``"context"``.
            custom_sections: Explicit list of section keys to extract.
                Overrides *detail_level* when provided.

        Returns:
            Context ready for execute/export.
        """
        from mycontext.core import Context
        from mycontext.utils.template_safety import safe_format_template

        if intent not in self.VALID_INTENTS:
            raise ValueError(
                f"Invalid intent {intent!r}. Choose from: {sorted(self.VALID_INTENTS)}"
            )

        if intent == "progressive" and not existing_memory:
            raise ValueError(
                "The 'progressive' intent requires existing_memory — "
                "the previous compressed state to update."
            )

        if intent == "context":
            instructions = _CONTEXT_INSTRUCTIONS
            output_structure = _CONTEXT_OUTPUT_STRUCTURE
        else:
            sections = self._resolve_sections(detail_level, custom_sections)
            output_structure = _compose_output_structure(sections, intent)
            if intent == "session":
                instructions = _build_session_instructions(sections, detail_level)
            else:
                instructions = _build_progressive_instructions(sections, detail_level)

        goal_section = f"**Compression goal**: {goal}" if goal else ""

        if intent == "progressive" and existing_memory:
            existing_memory_section = (
                "### EXISTING MEMORY STATE (to update)\n\n"
                f"{existing_memory}"
            )
        else:
            existing_memory_section = ""

        directive_content = safe_format_template(
            self.directive_template,
            instructions=instructions,
            content=content or "(No content provided.)",
            goal_section=goal_section,
            existing_memory_section=existing_memory_section,
            output_structure=output_structure,
        )

        ctx = Context(
            guidance=self.guidance,
            directive=Directive(content=directive_content),
            constraints=self.constraints,
            knowledge=content or "",
            data={
                "content": content,
                "intent": intent,
                "existing_memory": existing_memory,
                "goal": goal,
                "detail_level": detail_level,
                "custom_sections": custom_sections,
            },
        )
        ctx.metadata["pattern"] = self.name
        ctx.metadata["pattern_version"] = self.version
        ctx.metadata["intent"] = intent
        ctx.metadata["detail_level"] = detail_level
        return ctx

    def execute(
        self,
        provider: str = "openai",
        content: str = "",
        intent: str = "session",
        existing_memory: str = "",
        goal: str = "",
        detail_level: str = "standard",
        custom_sections: list[str] | None = None,
        **kwargs,
    ):
        """
        Execute memory compression.

        Args:
            provider: LLM provider.
            content: Conversation or document to compress.
            intent: ``"session"`` | ``"progressive"`` | ``"context"``
            existing_memory: For ``progressive`` — previous compressed state.
            goal: Optional hint for compression focus.
            detail_level: ``"minimal"`` | ``"standard"`` | ``"narrative"`` |
                ``"full"`` — controls which sections are extracted.
            custom_sections: Explicit list of section keys (overrides
                *detail_level*).
            **kwargs: Provider params (model, temperature, etc.)

        Returns:
            ProviderResponse with the structured compressed state.
        """
        ctx = self.build_context(
            content=content,
            intent=intent,
            existing_memory=existing_memory,
            goal=goal,
            detail_level=detail_level,
            custom_sections=custom_sections,
        )
        return ctx.execute(provider=provider, **kwargs)

    @staticmethod
    def _resolve_sections(
        detail_level: str,
        custom_sections: list[str] | None,
    ) -> list[str]:
        """Return the ordered list of section keys to extract."""
        if custom_sections is not None:
            valid_keys = set(_SECTION_DEFINITIONS) - {"changes_this_update"}
            invalid = set(custom_sections) - valid_keys
            if invalid:
                raise ValueError(
                    f"Unknown section(s): {sorted(invalid)}. "
                    f"Available: {sorted(valid_keys)}"
                )
            return list(custom_sections)

        if detail_level not in _DETAIL_LEVELS:
            raise ValueError(
                f"Invalid detail_level {detail_level!r}. "
                f"Choose from: {sorted(_DETAIL_LEVELS)}"
            )
        return list(_DETAIL_LEVELS[detail_level])
