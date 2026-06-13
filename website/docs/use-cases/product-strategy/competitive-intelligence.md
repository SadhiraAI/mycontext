---
sidebar_position: 3
title: Competitive Intelligence
description: Systematic competitor analysis using ComparativeAnalyzer + TrendIdentifier + GapAnalyzer over a LangChain + LlamaIndex RAG pipeline of competitor content.
---

# Competitive Intelligence

**Scenario:** Your product team needs to understand the competitive landscape: what competitors are doing, where the market is heading, and where genuine gaps exist that you could occupy. Manual competitive research is time-consuming and usually produces a stale slide deck. You want a living, queryable competitive intelligence pipeline.

**Patterns used:**
- `ComparativeAnalyzer` — structured head-to-head comparison across dimensions
- `TrendIdentifier` — identifies directional market movements from fragmented signals
- `GapAnalyzer` — finds underserved needs and market white spaces

**Integration:** LangChain + LlamaIndex RAG over competitor websites, docs, and press releases

---

```python
import mycontext

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage, HumanMessage

from mycontext.templates.enterprise.decision import ComparativeAnalyzer
from mycontext.templates.enterprise.analysis import TrendIdentifier, GapAnalyzer
from mycontext.intelligence import QualityMetrics

llm = ChatOpenAI(model="gpt-4o", temperature=0)
metrics = QualityMetrics(mode="heuristic")
memory = ConversationBufferMemory(return_messages=True)


def build_competitor_index(competitor_docs_dir: str) -> VectorStoreIndex:
    docs = SimpleDirectoryReader(competitor_docs_dir).load_data()
    return VectorStoreIndex.from_documents(docs)


def competitive_intelligence_report(
    our_product: str,
    competitors: list[str],
    evaluation_dimensions: list[str],
    index: VectorStoreIndex,
) -> dict:
    qe = index.as_query_engine(similarity_top_k=8)
    raw_intel = {}

    # Retrieve content about each competitor
    for competitor in competitors:
        raw_intel[competitor] = str(qe.query(
            f"What does {competitor} offer? Features, pricing, positioning, target market, recent launches."
        ))

    competitive_context = "\n\n".join(
        f"=== {name} ===\n{content}" for name, content in raw_intel.items()
    )

    # Three analytical lenses
    compare_ctx = ComparativeAnalyzer().build_context(
        decision=f"Comparing {our_product} against competitors",
        context_section=f"Dimensions: {', '.join(evaluation_dimensions)}\n\n{competitive_context}",
    )
    trend_ctx = TrendIdentifier().build_context(
        data_description=competitive_context,
        context_section="Identify directional market movements, feature convergence, and positioning shifts",
    )
    gap_ctx = GapAnalyzer().build_context(
        situation=f"Market for {our_product}",
        context_section=f"Competitive landscape:\n{competitive_context}",
    )

    results = {}
    for name, ctx, question in [
        ("comparison", compare_ctx, f"Compare {our_product} against each competitor on: {', '.join(evaluation_dimensions)}"),
        ("trends", trend_ctx, "What are the 3-5 most significant market trends in this space?"),
        ("gaps", gap_ctx, "What genuine market gaps exist that are underserved by current competitors?"),
    ]:
        score = metrics.evaluate(ctx)
        print(f"  {name}: {score.overall:.0%}")
        messages = [SystemMessage(content=ctx.assemble())]
        messages.extend(memory.chat_memory.messages[-4:])
        messages.append(HumanMessage(content=question))
        response = llm.invoke(messages).content
        memory.chat_memory.add_user_message(question)
        memory.chat_memory.add_ai_message(response)
        results[name] = response

    return results


competitors = ["LangChain", "DSPy", "PromptLayer", "Weights & Biases Prompts"]
dimensions = ["prompt management", "quality measurement", "cognitive frameworks", "integrations", "enterprise features", "pricing"]

index = build_competitor_index("./competitive/docs/")

report = competitive_intelligence_report(
    our_product="mycontext-ai",
    competitors=competitors,
    evaluation_dimensions=dimensions,
    index=index,
)

print("=== COMPARISON ===")
print(report["comparison"][:600])
print("\n=== MARKET TRENDS ===")
print(report["trends"][:500])
print("\n=== GAPS TO OWN ===")
print(report["gaps"][:500])
```

## What You Get

A competitive intelligence report with three sections:

| Section | Content |
|---------|---------|
| **Comparison matrix** | Head-to-head on each dimension — where you lead, where you trail, where parity exists |
| **Market trends** | Directional signals: feature convergence, pricing pressure, enterprise vs. developer focus |
| **Market gaps** | Specific underserved needs that represent positioning opportunities |

The memory chain means you can ask follow-up questions: "Which gaps align with our current roadmap?" or "Which competitor is most likely to address gap #2 first?"
