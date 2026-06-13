---
sidebar_position: 4
title: Medical Literature Synthesis
description: Synthesize evidence across a corpus of medical papers using SynthesisBuilder + CrossDomainSynthesizer + PatternRecognitionEngine over a LlamaIndex RAG pipeline.
---

# Medical Literature Synthesis

**Scenario:** A researcher or clinician needs to synthesize evidence across dozens of papers on a specific treatment question. Manual literature reviews take weeks. You want an AI pipeline that can query a paper corpus, identify convergent evidence, surface contradictions, and produce a structured summary with confidence levels.

**Patterns used:**
- `SynthesisBuilder` — synthesizes findings across multiple sources into a coherent narrative
- `CrossDomainSynthesizer` — identifies connections and patterns that span different studies or specialties
- `PatternRecognitionEngine` — detects recurring themes, effect sizes, and inconsistencies across papers

**Integration:** LlamaIndex RAG over a PDF paper corpus + multi-stage synthesis chain

---

```python
import mycontext

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.llms.openai import OpenAI as LlamaOpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from mycontext.templates.free.reasoning import SynthesisBuilder
from mycontext.templates.enterprise.synthesis import (
    CrossDomainSynthesizer,
    PatternRecognitionEngine,
)
from mycontext.intelligence import QualityMetrics

llm = ChatOpenAI(model="gpt-4o", temperature=0)
metrics = QualityMetrics(mode="heuristic")


def build_literature_pipeline(papers_dir: str):
    """Build a RAG index over a directory of PDF papers."""
    documents = SimpleDirectoryReader(papers_dir).load_data()
    index = VectorStoreIndex.from_documents(
        documents,
        llm=LlamaOpenAI(model="gpt-4o-mini"),
    )
    return index


def synthesize_evidence(
    index: VectorStoreIndex,
    research_question: str,
    n_papers_to_retrieve: int = 10,
) -> dict:
    # Step 1: Retrieve relevant passages via RAG
    query_engine = index.as_query_engine(similarity_top_k=n_papers_to_retrieve)
    raw_evidence = str(query_engine.query(research_question))

    # Step 2: Pattern recognition across retrieved evidence
    pattern_ctx = PatternRecognitionEngine().build_context(
        data_description=raw_evidence,
        context_section=f"Research question: {research_question}",
    )
    pattern_score = metrics.evaluate(pattern_ctx)
    print(f"Pattern context quality: {pattern_score.overall:.0%}")

    patterns_found = llm.invoke([
        SystemMessage(content=pattern_ctx.assemble()),
        HumanMessage(content="Identify recurring findings, contradictions, and gaps across these studies."),
    ]).content

    # Step 3: Cross-domain synthesis (catches connections across specialties)
    cross_ctx = CrossDomainSynthesizer().build_context(
        sources=raw_evidence,
        topic=research_question,
    )
    cross_findings = llm.invoke([
        SystemMessage(content=cross_ctx.assemble()),
        HumanMessage(content="What cross-specialty or cross-domain insights emerge from this evidence?"),
    ]).content

    # Step 4: Final synthesis — coherent narrative
    synth_ctx = SynthesisBuilder().build_context(
        sources=f"Patterns found:\n{patterns_found}\n\nCross-domain insights:\n{cross_findings}",
        topic=research_question,
    )
    synth_score = metrics.evaluate(synth_ctx)
    print(f"Synthesis context quality: {synth_score.overall:.0%}")

    final_synthesis = llm.invoke([
        SystemMessage(content=synth_ctx.assemble()),
        HumanMessage(content=(
            "Write a structured evidence synthesis with: "
            "(1) Key findings, (2) Level of evidence, "
            "(3) Contradictions in the literature, (4) Research gaps, "
            "(5) Clinical implications."
        )),
    ]).content

    return {
        "research_question": research_question,
        "raw_evidence_retrieved": len(raw_evidence),
        "patterns": patterns_found,
        "cross_domain_insights": cross_findings,
        "synthesis": final_synthesis,
    }


# Usage
index = build_literature_pipeline("./papers/diabetes-management/")

result = synthesize_evidence(
    index,
    research_question=(
        "What is the comparative effectiveness of GLP-1 receptor agonists "
        "vs SGLT-2 inhibitors for cardiovascular outcomes in type 2 diabetes?"
    ),
)

print(result["synthesis"])

# Save for review
import json
from pathlib import Path
Path("synthesis_output.json").write_text(json.dumps(result, indent=2, default=str))
```

## What You Get

A structured evidence synthesis with:

- **Convergent findings:** where multiple studies agree and the strength of that consensus
- **Contradictions:** where studies conflict, with hypotheses about why (population differences, methodology, dosing)
- **Cross-domain patterns:** insights that emerge from looking across different specialties (e.g. cardiometabolic connections)
- **Research gaps:** what's not yet adequately studied
- **Clinical implications:** what the evidence actually means for practice

This is the structure of a systematic review, generated in minutes instead of months.

## Confidence Scoring

Add explicit confidence levels to the synthesis:

```python
from mycontext import Context
from mycontext.foundation import Directive, Constraints

confidence_ctx = Context(
    directive=Directive(content=(
        f"For each key finding in this synthesis, assign a confidence level "
        f"(High/Moderate/Low) based on number of studies, sample sizes, and consistency:\n\n{result['synthesis']}"
    )),
    constraints=Constraints(
        format_rules=["Format as a table: Finding | Confidence | Basis"],
    ),
)
confidence_table = confidence_ctx.execute(provider="openai").response
print(confidence_table)
```
