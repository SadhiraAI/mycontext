"""
Memory Compressor — Structured state extraction from conversations and documents

The industry default for agent memory is "summarize the conversation." That
loses entities, decisions, constraints, and intent.  MemoryCompressor extracts
**structured state**, not prose summaries — so downstream agents can reconstruct
context from a fraction of the original tokens.

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

Additional sources:
- MemWalker (Chen et al. 2023): Tree-structured long-context navigation
- ReadAgent (Lee et al. 2024): Episode-based compression with gist memory
"""

from __future__ import annotations

from typing import ClassVar

from mycontext.foundation import Constraints, Directive, Guidance
from mycontext.structure import Pattern

# ---------------------------------------------------------------------------
# Intent-specific directive fragments
# ---------------------------------------------------------------------------

_INTENT_INSTRUCTIONS: dict[str, str] = {
    "session": (
        "You are compressing a conversation into structured state.\n\n"
        "Process:\n"
        "1. ENUMERATE first — before writing anything, mentally list:\n"
        "   a. Every PERSON mentioned (name, role, what they own)\n"
        "   b. Every TECHNOLOGY/TOOL with version numbers\n"
        "   c. Every DOLLAR AMOUNT, cost, and budget figure\n"
        "   d. Every DATE, deadline, and duration\n"
        "   e. Every DECISION and who made it\n"
        "   f. Every CONSTRAINT, SLA, or hard requirement\n"
        "   If a person, number, or technology appears even once, it must "
        "appear in your output.\n"
        "2. DISCARD filler: greetings, confirmations ('sounds good'), "
        "repeated statements, thinking-out-loud, pleasantries.\n"
        "3. EXTRACT into the structured sections below. "
        "Preserve exact names, versions, dates, numbers, and technical terms — "
        "do NOT paraphrase away precision.\n"
        "4. INLINE ALL NUMBERS — every dollar amount, percentage, duration, "
        "size, latency, date, count, and threshold MUST appear in the same "
        "bullet point as the entity or decision it belongs to. "
        "Do NOT strip numbers from context. If the database is 847GB, "
        "the entity bullet must say '847GB'. If the budget is $15,000 "
        "broken into $4,200 + $8,500, the decision bullet must include all three.\n"
        "5. CROSS-CHECK: Count every dollar amount in the conversation. "
        "Count every dollar amount in your output. They MUST match. "
        "Do the same for dates, person names, and technology names. "
        "If any count is lower in your output, you dropped information — "
        "go back and add the missing items.\n\n"
        "Output ONLY the structured sections. No prose introduction or summary paragraph."
    ),
    "progressive": (
        "You are UPDATING an existing compressed memory with new conversation turns.\n\n"
        "CRITICAL RULE: Treat existing memory as GROUND TRUTH. Every entity, "
        "number, decision, and constraint in the existing memory MUST appear "
        "in your output unless the new turns EXPLICITLY invalidate it. "
        "When in doubt, KEEP the existing information.\n\n"
        "Process:\n"
        "1. READ the existing memory state. Count its entities, decisions, "
        "and constraints.\n"
        "2. SCAN the new turns for: new entities, changed decisions, "
        "resolved questions, new constraints, updated preferences.\n"
        "3. MERGE:\n"
        "   - KEEP all existing items that are not contradicted by new turns\n"
        "   - ADD new entities, decisions, constraints from the new turns\n"
        "   - UPDATE items where new turns explicitly change them "
        "(mark: CHANGED from [old] → [new])\n"
        "   - RESOLVE open items that new turns answer\n"
        "   - Only REMOVE an item if new turns explicitly invalidate it\n"
        "4. CROSS-CHECK: Your output must have AT LEAST as many entities "
        "and numbers as the existing memory plus any new ones from the new turns. "
        "If your entity count is LOWER than the existing memory, you dropped "
        "information — go back and restore it.\n"
        "5. VERIFY: the updated state is complete and self-contained — "
        "someone reading ONLY this state should understand the full context.\n\n"
        "Output the complete updated structured state (not a diff)."
    ),
    "context": (
        "You are compressing a large document into a dense factual representation.\n\n"
        "Process:\n"
        "1. EXTRACT all key claims, facts, figures, names, dates, and relationships.\n"
        "2. PRESERVE exact terminology — do not substitute synonyms for technical terms.\n"
        "3. ORGANIZE by topic/theme rather than by document order.\n"
        "4. MAXIMIZE information density — every sentence should carry facts, "
        "not transitions or filler.\n"
        "5. VERIFY: could someone answer detailed questions about the original document "
        "using only your compression? If not, add what's missing.\n\n"
        "Optimize for information density, not readability."
    ),
}

_OUTPUT_STRUCTURES: dict[str, str] = {
    "session": """
## ENTITIES
(Every person, company, project, system, tool, standard, version — include ALL associated numbers inline)
- [Entity]: [Role] — [every fact, number, size, cost, date associated with this entity]
Example: "Rachel Kim: [CTO] — leads 23-person team, approved $2.4M budget for 18-month timeline"

## DECISIONS
(What was decided — include the numbers/metrics that informed the decision)
- [Decision]: [Full rationale with specific numbers] — decided by [who]

## CONSTRAINTS & REQUIREMENTS
(Hard limits with exact thresholds — every number matters)
- [Constraint]: [Exact value/threshold/date] — [source/reason]

## TIMELINE & ACTION ITEMS
(Who does what, by when — include every mentioned date and deadline)
- [Person]: [Task] — [deadline/schedule]

## OPEN ITEMS
(Unresolved questions, pending decisions, blockers)
- [Item]: [Status/context]

## KEY NUMBERS INDEX
(Safety net — list EVERY quantitative value from the conversation, grouped naturally. This index must be complete even if numbers also appear above.)
- Monetary values: [list all dollar amounts, costs, budgets, prices, revenue figures]
- Dates & durations: [list all dates, deadlines, timelines, durations]
- Measurements & metrics: [list all percentages, sizes, counts, rates, thresholds, SLAs, scores]
""",
    "progressive": """
## ENTITIES (updated)
(Carry forward ALL existing entities. Add new ones. Update changed ones.)
- [Entity]: [Role] — [all numbers/facts inline] [NEW/UPDATED/unchanged]

## DECISIONS (updated)
(Carry forward ALL existing decisions. Add new ones. Mark changes.)
- [Decision]: [Rationale with numbers] — [who] [NEW/CHANGED from: X/unchanged]

## CONSTRAINTS & REQUIREMENTS (updated)
(Carry forward ALL existing constraints. Add new ones.)
- [Constraint]: [Exact value/threshold] — [source] [NEW/UPDATED/unchanged]

## TIMELINE & ACTION ITEMS (updated)
- [Person]: [Task] — [deadline] [NEW/UPDATED/unchanged]

## OPEN ITEMS (updated)
- [Item]: [Status] [NEW/RESOLVED/unchanged]

## KEY NUMBERS INDEX (updated)
(Carry forward ALL numbers from existing memory + add new numbers from new turns)
- Monetary values: [list all — existing + new]
- Dates & durations: [list all — existing + new]
- Measurements & metrics: [list all — existing + new]

## CHANGES THIS UPDATE
(Brief list of what changed from the previous memory state)
""",
    "context": """
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
""",
}

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

    Research basis:
        SimpleMem (entity-level), CDIC (progressive), RECOMP (extractive+abstractive),
        Cognitive Load Theory (discard extraneous, preserve germane).

    Example:
        >>> from mycontext.templates.free.specialized import MemoryCompressor
        >>> mc = MemoryCompressor()
        >>> ctx = mc.build_context(
        ...     content=conversation_text,
        ...     intent="session",
        ... )
        >>> result = ctx.execute(provider="openai")

    Example (progressive update):
        >>> ctx = mc.build_context(
        ...     content=new_turns,
        ...     intent="progressive",
        ...     existing_memory=previous_compressed_state,
        ... )
        >>> result = ctx.execute(provider="openai")

    Free Template — Part of mycontext open source edition.
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
        **kwargs,
    ):
        """
        Build context for memory compression.

        Args:
            content: Conversation history or document text to compress.
            intent: ``"session"`` | ``"progressive"`` | ``"context"``
            existing_memory: For ``progressive`` — the previous compressed state.
            goal: Optional hint about what the memory will be used for.

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

        instructions = _INTENT_INSTRUCTIONS[intent]
        output_structure = _OUTPUT_STRUCTURES[intent]

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
            },
        )
        ctx.metadata["pattern"] = self.name
        ctx.metadata["pattern_version"] = self.version
        ctx.metadata["intent"] = intent
        return ctx

    def execute(
        self,
        provider: str = "openai",
        content: str = "",
        intent: str = "session",
        existing_memory: str = "",
        goal: str = "",
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
            **kwargs: Provider params (model, temperature, etc.)

        Returns:
            ProviderResponse with the structured compressed state.
        """
        ctx = self.build_context(
            content=content,
            intent=intent,
            existing_memory=existing_memory,
            goal=goal,
        )
        return ctx.execute(provider=provider, **kwargs)
