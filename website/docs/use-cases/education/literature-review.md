---
sidebar_position: 6
title: Research Literature Review
description: Conduct systematic literature reviews with HypothesisGenerator + CrossDomainSynthesizer + SynthesisBuilder. LlamaIndex RAG with TemplateBenchmark for model comparison.
---

# Research Literature Review

**Scenario:** A doctoral student or researcher needs to synthesise a body of literature for a thesis chapter or grant proposal. They need to identify the state of the field, competing theoretical frameworks, methodological gaps, and where their own work fits. Manual literature reviews take weeks.

**Patterns used:**
- `HypothesisGenerator` — generates hypotheses about theoretical frameworks and research gaps
- `CrossDomainSynthesizer` — identifies connections across sub-fields and disciplines
- `SynthesisBuilder` — produces the final synthesised narrative

**Integration:** LlamaIndex RAG over paper corpus + `TemplateBenchmark` to validate model selection

---

```python
import mycontext

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI as LlamaOpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from mycontext.templates.free.reasoning import HypothesisGenerator, SynthesisBuilder
from mycontext.templates.enterprise.synthesis import CrossDomainSynthesizer
from mycontext.intelligence import QualityMetrics, TemplateBenchmark

llm = ChatOpenAI(model="gpt-4o", temperature=0)
metrics = QualityMetrics(mode="heuristic")


def build_paper_index(papers_dir: str) -> VectorStoreIndex:
    docs = SimpleDirectoryReader(papers_dir).load_data()
    return VectorStoreIndex.from_documents(
        docs, llm=LlamaOpenAI(model="gpt-4o-mini")
    )


def literature_review(
    research_question: str,
    field: str,
    index: VectorStoreIndex,
) -> dict:
    qe = index.as_query_engine(similarity_top_k=10)

    # Retrieve field overview
    raw_literature = str(qe.query(
        f"Key theories, methods, findings, and debates on: {research_question}"
    ))

    # Step 1: Generate hypotheses about theoretical frameworks
    hyp_ctx = HypothesisGenerator().build_context(
        phenomenon=f"State of research on: {research_question}",
        domain=field,
    )
    hyp_score = metrics.evaluate(hyp_ctx)
    print(f"Hypothesis context: {hyp_score.overall:.0%}")

    hypotheses = llm.invoke([
        SystemMessage(content=hyp_ctx.assemble()),
        HumanMessage(content=(
            f"Based on this literature:\n\n{raw_literature[:3000]}\n\n"
            "What are the competing theoretical frameworks? What are the key research gaps?"
        )),
    ]).content

    # Step 2: Cross-domain synthesis
    cross_ctx = CrossDomainSynthesizer().build_context(
        sources=raw_literature,
        topic=research_question,
    )
    cross_findings = llm.invoke([
        SystemMessage(content=cross_ctx.assemble()),
        HumanMessage(content=(
            "Identify connections to adjacent fields not typically cited in this literature. "
            "What insights from neighbouring disciplines are being missed?"
        )),
    ]).content

    # Step 3: Final synthesis
    synth_ctx = SynthesisBuilder().build_context(
        sources=f"Literature:\n{raw_literature}\n\nFrameworks:\n{hypotheses}\n\nCross-domain:\n{cross_findings}",
        topic=research_question,
    )
    review = llm.invoke([
        SystemMessage(content=synth_ctx.assemble()),
        HumanMessage(content=(
            "Write a systematic literature review with: "
            "(1) Current state of knowledge, "
            "(2) Theoretical frameworks in competition, "
            "(3) Methodological approaches and their limitations, "
            "(4) Key debates, "
            "(5) Research gaps and where new work could contribute. "
            "Use academic register."
        )),
    ]).content

    return {
        "theoretical_frameworks": hypotheses,
        "cross_domain_connections": cross_findings,
        "review": review,
    }


def validate_model_choice(question: str) -> None:
    """Compare models on this task before committing to the full review."""
    bench = TemplateBenchmark()
    for provider, model in [("openai", "gpt-4o-mini"), ("openai", "gpt-4o")]:
        result = bench.run(
            template=SynthesisBuilder,
            benchmark_name="literature_synthesis",
            provider=provider,
            model=model,
        )
        print(f"{provider}/{model}: {result.overall_score:.1%} quality, {result.avg_latency_ms:.0f}ms avg")


# Validate model first (one-time)
validate_model_choice("embodied cognition in language acquisition")

# Run the review
index = build_paper_index("./papers/cognitive-science/")
review = literature_review(
    research_question="What is the role of embodied experience in language acquisition?",
    field="cognitive science and developmental psychology",
    index=index,
)

print(review["review"])

from pathlib import Path
Path("reviews/embodied-cognition.md").write_text(
    f"# Literature Review\n\n## Theoretical Frameworks\n\n{review['theoretical_frameworks']}\n\n"
    f"## Cross-Disciplinary Connections\n\n{review['cross_domain_connections']}\n\n"
    f"## Synthesis\n\n{review['review']}"
)
```

## What You Get

A research-quality literature review with:
- **State of knowledge:** what is established, contested, and unknown
- **Theoretical framework map:** competing explanations and their evidence base
- **Methodological landscape:** dominant approaches, their assumptions, and limitations
- **Cross-disciplinary connections:** insights from adjacent fields the literature is missing
- **Research gaps:** specific, arguable gaps where new work could contribute

The benchmark step validates model selection before committing to the expensive full review run.
