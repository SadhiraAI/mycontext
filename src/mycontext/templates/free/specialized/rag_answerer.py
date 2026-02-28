"""
RAG Answerer - Grounded answer generation from retrieved context

A specialized template for Retrieval-Augmented Generation (RAG) pipelines.
Designed to maximize grounding, reduce hallucination, and enforce citation.

Incorporates generation-side best practices from RAG research:
- **Chain-of-Note** (Yu et al. 2023): Write intermediate reasoning notes before
  answering to reduce hallucination and improve faithfulness.
- **Self-RAG** (Asai et al. 2023): Self-reflection — verify that the generated
  answer is actually supported by the retrieved evidence.
- **CRAG / Corrective RAG** (Yan et al. 2024): Relevance grading — assess each
  chunk's relevance before incorporating it; discard noise.
- **Multi-granularity reasoning**: Reason at both detail level (specific facts)
  and synthesis level (cross-document patterns).
- **Knowledge strip decomposition**: Treat each chunk as discrete evidence strips;
  grade and use individually rather than as a monolithic block.

Additional sources:
- Context Engineering: retrieval_indexing.md (Semantic Integration)
- Stack AI: RAG prompt engineering guide
- ChatNexus: Advanced prompt engineering for RAG applications
"""

from __future__ import annotations

from typing import ClassVar

from mycontext.foundation import Constraints, Directive, Guidance
from mycontext.structure import Pattern


# ---------------------------------------------------------------------------
# Mode-specific directive fragments (answer, summarize, synthesize)
# ---------------------------------------------------------------------------

_TASK_INSTRUCTIONS = {
    "answer": (
        "Answer the question using ONLY the retrieved context below. "
        "Skip any retrieved chunks that are off-topic. "
        "Include ALL specific names, terms, numbers, frameworks, and technical vocabulary "
        "from the relevant chunks — preserve exact terminology, do not paraphrase away precision. "
        "For comparisons or lists: enumerate EVERY item mentioned with its key properties. "
        "Cite sources for each factual claim. "
        "After drafting, verify: (1) every claim is supported by the context, "
        "(2) no specific names or numbers were missed, (3) citations are accurate. "
        "If the context does not contain enough information, say: "
        "\"I cannot find enough information in the provided context to answer this.\" "
        "Do not guess or use external knowledge."
    ),
    "summarize": (
        "Summarize the retrieved context. Skip off-topic chunks. "
        "Extract ALL key facts, figures, names, and specifics — preserve exact terminology. "
        "Cite which source each fact comes from. "
        "After drafting, verify completeness and citation accuracy. "
        "If the context is empty or irrelevant, say so."
    ),
    "synthesize": (
        "Synthesize information from the retrieved context. Skip off-topic chunks. "
        "Combine evidence across sources, preserving all specific names, terms, and numbers. "
        "Note where sources agree or contradict. "
        "After drafting, verify every claim is grounded and no details were missed. "
        "If critical information is missing, acknowledge the gap. "
        "Prioritize retrieved context over general knowledge."
    ),
}

_DIRECTIVE_TEMPLATE = """{instructions}

**Rules**: Cite as (Source: [document/section]). If sources contradict, present both.

---

### RETRIEVED CONTEXT

{retrieved_docs}

---

### QUESTION

{question}
"""


class RagAnswerer(Pattern):
    """
    Generate grounded answers from retrieved documents (RAG).

    Designed for RAG pipelines where retrieved chunks are injected into context.
    Incorporates generation-side best practices from modern RAG research to
    maximize extraction, grounding, and faithfulness from any retrieval pipeline.

    **Generation-side techniques incorporated**:

    - **Corrective RAG (CRAG)**: Relevance grading — assess each chunk before
      using it; discard off-topic or low-quality content.
    - **Chain-of-Note**: Extract structured evidence notes from each relevant
      chunk before generating the answer. Reduces hallucination.
    - **Self-RAG**: Self-reflection — after drafting, verify that every claim
      is supported by the retrieved evidence. Remove unsupported claims.
    - **Multi-granularity reasoning**: Reason at detail level (per-chunk facts,
      names, numbers) AND synthesis level (cross-chunk patterns, contradictions).
    - **Knowledge strip decomposition**: Treat each chunk as discrete evidence;
      grade and attribute individually.

    **task** controls the task type:

    - ``answer``: 4-step process — grade relevance → extract evidence →
      generate grounded answer → self-reflect
    - ``summarize``: Grade → extract → organize by theme → self-check
    - ``synthesize``: Grade → extract → cross-reference → build synthesis → verify

    Example:
        >>> from mycontext.templates.free.specialized import RagAnswerer
        >>> rag = RagAnswerer()
        >>> ctx = rag.build_context(
        ...     question="Why did churn spike?",
        ...     retrieved_docs=retrieved_chunks_text,
        ...     task="answer",
        ... )
        >>> result = ctx.execute(provider="openai")
    """

    GENERIC_PROMPT = (
        "You are a retrieval-augmented assistant. Answer using ONLY the provided context.\n\n"
        "Context:\n{retrieved_docs}\n\n"
        "Question: {question}\n\n"
        "Rules: Skip off-topic chunks. Include ALL specific names, terms, numbers, and "
        "technical vocabulary from relevant chunks. Cite sources (Source: [doc]). "
        "For lists/comparisons: enumerate every item. "
        "After drafting, verify all claims are supported and no specifics were missed. "
        "If the context lacks the answer, say "
        "\"I cannot find enough information in the provided context.\" "
        "Do not guess or hallucinate."
    )

    VALID_TASKS: ClassVar[frozenset[str]] = frozenset({"answer", "summarize", "synthesize"})

    def __init__(self):
        super().__init__(
            name="rag_answerer",
            description="Grounded answer generation from retrieved context",
            guidance=Guidance(
                role="Retrieval-Augmented Answer Specialist",
                rules=[
                    "Use only the retrieved context; skip off-topic chunks",
                    "Preserve ALL specific names, terms, numbers, and technical vocabulary",
                    "Cite sources for every factual claim",
                    "For enumerations: list every item — do not merge or omit",
                    "After drafting, verify: claims supported, no specifics missed, citations accurate",
                    "Abstain when context is insufficient — do not guess",
                ],
                style="evidence-based, traceable, exhaustive, precise",
            ),
            directive_template=_DIRECTIVE_TEMPLATE,
            input_schema={
                "question": str,
                "retrieved_docs": str,
                "task": str,
            },
            constraints=Constraints(
                must_include=["citation", "evidence"],
                style_guide=(
                    "Be exhaustive and precise. Cite sources. "
                    "Preserve all specific terms from context. Abstain when uncertain."
                ),
            ),
        )

    def build_context(
        self,
        question: str = "",
        retrieved_docs: str = "",
        task: str = "answer",
        **kwargs,
    ):
        """
        Build context for RAG answer generation.

        Args:
            question: The user's question
            retrieved_docs: Retrieved document chunks (from vector store, etc.)
            task: "answer" | "summarize" | "synthesize"

        Returns:
            Context ready for execute/export
        """
        from mycontext.core import Context
        from mycontext.utils.template_safety import safe_format_template

        if task not in self.VALID_TASKS:
            raise ValueError(
                f"Invalid task {task!r}. Choose from: {sorted(self.VALID_TASKS)}"
            )

        instructions = _TASK_INSTRUCTIONS[task]
        directive_content = safe_format_template(
            self.directive_template,
            question=question,
            retrieved_docs=retrieved_docs or "(No context provided.)",
            instructions=instructions,
        )

        ctx = Context(
            guidance=self.guidance,
            directive=Directive(content=directive_content),
            constraints=self.constraints,
            knowledge=retrieved_docs or "",
            data={
                "question": question,
                "retrieved_docs": retrieved_docs,
                "task": task,
            },
        )
        ctx.metadata["pattern"] = self.name
        ctx.metadata["pattern_version"] = self.version
        ctx.metadata["task"] = task
        return ctx

    def execute(
        self,
        provider: str = "openai",
        question: str = "",
        retrieved_docs: str = "",
        task: str = "answer",
        **kwargs,
    ):
        """
        Execute RAG answer generation.

        Args:
            provider: LLM provider
            question: User question
            retrieved_docs: Retrieved context
            task: "answer" | "summarize" | "synthesize"
            **kwargs: Provider params (model, temperature, etc.)

        Returns:
            ProviderResponse with the grounded answer
        """
        ctx = self.build_context(
            question=question,
            retrieved_docs=retrieved_docs,
            task=task,
        )
        return ctx.execute(provider=provider, **kwargs)
