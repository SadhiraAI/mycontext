"""
Query Planner - Pre-retrieval cognitive analysis for RAG pipelines.

Analyzes a user query BEFORE it hits any retrieval system. Produces
structured output: query classification, sub-queries, step-back
abstractions, HyDE documents, and retrieval strategy hints.

Complements the RagAnswerer (post-retrieval) to bookend any RAG pipeline.

Research basis:
- Query decomposition: +36.7% MRR on multi-hop benchmarks (2025)
- Step-back prompting: +27% TimeQA (ICLR 2024, Google DeepMind)
- HyDE: matches fine-tuned retrievers in zero-shot (CMU 2023)
- UniRAG (EMNLP 2025): entity-grounded decomposition
- CoRAG (2025): chain-of-retrieval with dynamic reformulation
- Plan*RAG (2024): test-time reasoning plans as DAGs
"""

from __future__ import annotations

from typing import ClassVar

from mycontext.foundation import Constraints, Directive, Guidance
from mycontext.structure import Pattern

_MODE_INSTRUCTIONS = {
    "full": (
        "Perform ALL four phases: CLASSIFY, DECOMPOSE, REWRITE, and PLAN. "
        "Generate step-back queries, expanded queries, and a HyDE document."
    ),
    "decompose_only": (
        "Perform only CLASSIFY and DECOMPOSE. Skip REWRITE and PLAN. "
        "Do not generate step-back queries, expanded queries, or HyDE documents."
    ),
}

_DIRECTIVE_TEMPLATE = """{mode_instructions}

Analyze this query for optimal retrieval. Do NOT answer the question — your job
is to prepare it for a retrieval system.

**QUERY**: {query}

**DOMAIN**: {domain}

**AVAILABLE SOURCES**: {available_sources}

---

## 1. CLASSIFY

Determine the query type and complexity:

- **Type**: [factual / analytical / multi-hop / comparison / temporal / procedural]
- **Complexity**: [low / medium / high] — how many entities, relationships, or reasoning steps?
- **Requires retrieval**: [yes / no] — can this be answered from general knowledge, or does it need specific documents?
- **Key entities**: [List the specific entities, concepts, or terms the query is about]

Type definitions:
- **factual**: Single fact lookup ("What is X?")
- **analytical**: Requires reasoning over evidence ("How does X affect Y?")
- **multi-hop**: Chains across multiple pieces of information ("What did A do at B before C?")
- **comparison**: Needs parallel retrieval of multiple entities ("Compare X and Y")
- **temporal**: Time-sensitive, needs date filtering ("What changed in Q3 2025?")
- **procedural**: Step-by-step instructions ("How do I set up X?")

---

## 2. DECOMPOSE

Based on the classification:

- **If factual or procedural**: Pass the query through unchanged as a single sub-query.
- **If multi-hop**: Break into independent sub-queries, each targeting one piece of the reasoning chain. Each sub-query should be self-contained and answerable independently.
- **If comparison**: Create one sub-query per entity being compared, plus one for the comparison criteria.
- **If analytical**: Identify the core relationship and create sub-queries for each side.
- **If temporal**: Add the time constraint explicitly to the sub-query.

**SUB-QUERIES**:
1. [First sub-query — self-contained, specific]
2. [Second sub-query — if needed]
3. [Third sub-query — if needed]

For each sub-query, note which key entity or relationship it targets.

---

## 3. REWRITE

For each sub-query, generate three alternative forms:

### Step-Back Queries
Abstract each sub-query to its underlying concept or principle. Replace specific details with the general category they belong to.

### Expanded Queries
Add synonyms, related terms, and alternative phrasings to improve recall. Include technical terminology and common abbreviations.

### HyDE Document
Generate a single hypothetical answer paragraph (3-5 sentences) that would answer the original query. Write it as if it were an excerpt from an authoritative document. Use declarative statements, specific terminology, and factual tone. This document will be embedded for similarity search — it should look like the target document, not like a question.

---

## 4. PLAN

Produce retrieval strategy hints:

- **Suggested k**: How many chunks per sub-query? (factual: 3, analytical: 5, multi-hop: 5 per sub-query, comparison: 5 per entity)
- **Source types**: Which of the available sources are most likely to contain the answer?
- **Filters**: Any date ranges, entity types, categories, or metadata filters to apply?
- **Strategy**: How should retrieval be structured? (single pass, per-entity retrieval then combine, iterative refinement)
- **Merge strategy**: How should chunks from multiple sub-queries be combined before generation?

---

**REQUIREMENTS**:
- Do NOT answer the original question — only prepare it for retrieval
- Every sub-query must be self-contained and independently retrievable
- The HyDE document must be written in declarative style (like a reference document, not a question)
- Keep sub-queries focused — prefer 2-3 precise queries over 1 vague query
- If the query is simple and factual, say so — do not over-decompose"""


class QueryPlanner(Pattern):
    """
    Pre-retrieval cognitive analysis for RAG pipelines.

    Analyzes a user query before it reaches any retrieval system, producing:
    - Query classification (factual, analytical, multi-hop, comparison, temporal, procedural)
    - Sub-query decomposition for complex questions
    - Step-back abstractions and expanded queries for better retrieval
    - Hypothetical Document Embeddings (HyDE) for embedding-based search
    - Retrieval strategy hints (k value, source types, filters)

    Designed to complement RagAnswerer: QueryPlanner handles pre-retrieval
    cognition, RagAnswerer handles post-retrieval generation.

    Example:
        >>> from mycontext.templates.enterprise.specialized import QueryPlanner
        >>> planner = QueryPlanner()
        >>> result = planner.execute(
        ...     provider="openai",
        ...     query="How does RAPTOR compare to Adaptive RAG for multi-hop reasoning?",
        ...     domain="technical",
        ...     available_sources="research papers, documentation",
        ... )
        >>> print(result.response)

    Based on:
    - Query decomposition (+36.7% MRR on multi-hop, 2025)
    - Step-back prompting (+27% TimeQA, ICLR 2024)
    - HyDE (CMU 2023) — zero-shot dense retrieval
    - UniRAG (EMNLP 2025), CoRAG (2025), Plan*RAG (2024)
    """

    GENERIC_PROMPT = (
        "You are a retrieval query planner. Your job is to prepare a query "
        "for optimal retrieval — do NOT answer the question yourself.\n\n"
        "Query: {query}\n"
        "Domain: {domain}\n"
        "Available sources: {available_sources}\n\n"
        "Analyze this query in four steps:\n"
        "(1) CLASSIFY — What type of query is this? (factual, analytical, "
        "multi-hop, comparison, temporal, procedural). How complex is it?\n"
        "(2) DECOMPOSE — If multi-hop or comparison, break into independent "
        "sub-queries. If simple, pass through unchanged.\n"
        "(3) REWRITE — For each sub-query, generate: a step-back version "
        "(abstract to underlying concept), an expanded version (add synonyms "
        "and related terms), and a HyDE document (a hypothetical answer "
        "paragraph written in declarative style).\n"
        "(4) PLAN — Suggest retrieval parameters: k per sub-query, source "
        "types, filters, and merge strategy.\n\n"
        "Do not answer the question. Only prepare it for retrieval."
    )

    VALID_MODES: ClassVar[frozenset[str]] = frozenset({"full", "decompose_only"})

    def __init__(self):
        super().__init__(
            name="query_planner",
            description="Pre-retrieval query analysis for RAG pipelines",
            guidance=Guidance(
                role="Retrieval Query Planner",
                rules=[
                    "Do NOT answer the question — only prepare it for retrieval",
                    "Classify the query type before decomposing",
                    "Every sub-query must be self-contained and independently retrievable",
                    "Write HyDE documents in declarative style, like a reference document",
                    "Do not over-decompose simple factual queries",
                    "Retrieval hints are advisory — suggest, do not prescribe",
                ],
                style="analytical, structured, precise, retrieval-oriented",
            ),
            directive_template=_DIRECTIVE_TEMPLATE,
            input_schema={
                "query": str,
                "domain": str,
                "available_sources": str,
                "mode_instructions": str,
            },
            constraints=Constraints(
                must_include=[
                    "query classification with type and complexity",
                    "sub-queries for complex questions",
                    "retrieval strategy hints",
                ],
                must_not_include=[
                    "answers to the original question",
                    "fabricated facts or claims",
                ],
                style_guide=(
                    "Structured output with clear section headings. "
                    "Sub-queries must be specific and self-contained. "
                    "HyDE documents must be declarative, not interrogative."
                ),
            ),
        )

    def build_context(
        self,
        query: str = "",
        domain: str = "general",
        available_sources: str = "documentation",
        mode: str = "full",
        **kwargs,
    ):
        """
        Build context for query planning (without executing).

        Args:
            query: The user's question to analyze
            domain: Domain hint ("technical", "medical", "legal", "general")
            available_sources: What sources exist ("documentation, codebase, database, web")
            mode: "full" (all 4 phases) or "decompose_only" (classify + decompose only)
            **kwargs: Additional options

        Returns:
            Context object ready for export/use
        """
        from mycontext.core import Context
        from mycontext.utils.template_safety import safe_format_template

        if mode not in self.VALID_MODES:
            raise ValueError(f"Invalid mode {mode!r}. Choose from: {sorted(self.VALID_MODES)}")

        mode_instructions = _MODE_INSTRUCTIONS[mode]
        directive_content = safe_format_template(
            self.directive_template,
            query=query,
            domain=domain,
            available_sources=available_sources or "documentation",
            mode_instructions=mode_instructions,
        )

        ctx = Context(
            guidance=self.guidance,
            directive=Directive(content=directive_content),
            constraints=self.constraints,
            data={
                "query": query,
                "domain": domain,
                "available_sources": available_sources,
                "mode": mode,
            },
        )
        ctx.metadata["pattern"] = self.name
        ctx.metadata["pattern_version"] = self.version
        ctx.metadata["mode"] = mode
        return ctx

    def execute(
        self,
        provider: str = "openai",
        query: str = "",
        domain: str = "general",
        available_sources: str = "documentation",
        mode: str = "full",
        **kwargs,
    ):
        """
        Execute query planning.

        Args:
            provider: LLM provider ("openai", "gemini", "anthropic")
            query: The user's question to analyze
            domain: Domain hint ("technical", "medical", "legal", "general")
            available_sources: What sources exist ("documentation, codebase, database, web")
            mode: "full" (all 4 phases) or "decompose_only" (classify + decompose only)
            **kwargs: Provider params (model, temperature, etc.)

        Returns:
            ProviderResponse with the query analysis
        """
        ctx = self.build_context(
            query=query,
            domain=domain,
            available_sources=available_sources,
            mode=mode,
        )
        return ctx.execute(provider=provider, **kwargs)
