---
sidebar_position: 5
title: Concept Explanation Engine
description: Generate multi-level explanations of complex concepts using ConceptExplainer + AnalogicalReasoner + MetaphorGenerator. Measure quality lift with ContextAmplificationIndex.
---

# Concept Explanation Engine

**Scenario:** You need to explain a difficult concept to different audiences: a technical deep-dive for experts, a conceptual overview for managers, and a plain-language version for a general audience. You want explanations that use the right analogies and metaphors for each audience — not the same explanation dumbed down.

**Patterns used:**
- `ConceptExplainer` (enterprise) — breaks complex concepts into structured, layered explanations
- `AnalogicalReasoner` (enterprise) — finds concrete analogies that make abstract concepts accessible
- `MetaphorGenerator` (enterprise) — creates vivid, memorable metaphors calibrated to the audience

**Integration:** Raw `Context` builds + `ContextAmplificationIndex` to measure how much the patterns add

---

```python
import mycontext
mycontext.activate_license("MC-ENT-YOUR-KEY")

from mycontext.templates.enterprise.specialized import ConceptExplainer
from mycontext.templates.enterprise.reasoning import AnalogicalReasoner
from mycontext.templates.enterprise.creative import MetaphorGenerator
from mycontext.intelligence import QualityMetrics, ContextAmplificationIndex

metrics = QualityMetrics(mode="heuristic")
cai = ContextAmplificationIndex()


AUDIENCES = {
    "expert": {
        "description": "Machine learning engineers with 5+ years experience",
        "depth": "technical, assume deep mathematical background",
    },
    "manager": {
        "description": "Technical product manager, understands systems but not ML internals",
        "depth": "conceptual, business implications, no math",
    },
    "general": {
        "description": "Curious adult, no technical background",
        "depth": "plain language, everyday analogies, practical relevance",
    },
}


def explain_for_audience(concept: str, audience_key: str) -> dict:
    audience = AUDIENCES[audience_key]

    explain_ctx = ConceptExplainer().build_context(
        concept=concept,
        context_section=f"Audience: {audience['description']}. Depth: {audience['depth']}",
    )
    analogy_ctx = AnalogicalReasoner().build_context(
        situation=f"Explaining {concept}",
        context_section=f"Find analogies accessible to: {audience['description']}",
    )
    metaphor_ctx = MetaphorGenerator().build_context(
        concept=concept,
        context_section=f"Audience: {audience['description']}",
    )

    score = metrics.evaluate(explain_ctx)
    print(f"  [{audience_key}] context quality: {score.overall:.0%}")

    # Merge into one explanation context
    explain_ctx.knowledge = (
        f"Useful analogies (select the most relevant):\n"
        f"{analogy_ctx.execute(provider='openai', model='gpt-4o-mini').response}\n\n"
        f"Vivid metaphors:\n"
        f"{metaphor_ctx.execute(provider='openai', model='gpt-4o-mini').response}"
    )

    result = explain_ctx.execute(provider="openai", model="gpt-4o")

    return {
        "audience": audience_key,
        "concept": concept,
        "explanation": result.response,
        "context_quality": score.overall,
    }


def explain_multi_audience(concept: str) -> dict:
    results = {}
    for audience_key in AUDIENCES:
        print(f"Building explanation for: {audience_key}")
        results[audience_key] = explain_for_audience(concept, audience_key)

    # Measure quality lift vs raw prompt
    cai_result = cai.measure(
        template=ConceptExplainer,
        input_data={"concept": concept, "context_section": "General audience"},
        provider="openai",
    )
    results["quality_lift"] = {
        "cai_score": cai_result.cai_score,
        "verdict": cai_result.verdict,
    }

    return results


# Explain "transformer attention mechanism" to all three audiences
explanations = explain_multi_audience("transformer attention mechanism in large language models")

for audience, data in explanations.items():
    if audience == "quality_lift":
        print(f"\nQuality lift vs raw prompt: {data['cai_score']:.2f}x ({data['verdict']})")
    else:
        print(f"\n=== {audience.upper()} ===")
        print(data["explanation"][:400])
```

## What You Get

Three explanations of the same concept, genuinely tailored:

**Expert version:** Discusses query/key/value matrices, scaled dot-product attention, multi-head mechanism, positional encoding — assumes fluency with linear algebra and neural networks.

**Manager version:** "Attention lets the model focus on the most relevant words when processing each word — like how you re-read the subject of a sentence before deciding what a pronoun refers to. This is what makes it good at long documents."

**General version:** "Imagine reading a paragraph and highlighting the words that matter most for understanding each word. Attention is the model doing that highlighting — automatically figuring out which parts of the text are most relevant to each other."

The CAI measurement shows exactly how much quality the structured patterns add over a raw "explain this concept" prompt — typically 30-60% by the output quality rubric.
