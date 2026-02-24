---
sidebar_position: 3
title: Legal Research Synthesis
description: Multi-step legal research with SynthesisBuilder + AnalogicalReasoner + CrossDomainSynthesizer. A LangChain memory chain that threads case law across jurisdictions.
---

# Legal Research Synthesis

**Scenario:** A lawyer needs to research a novel legal question — one where the directly applicable case law is thin, but analogous principles from related areas might support an argument. Manual research across jurisdictions and legal domains takes days. You want an AI research assistant that retrieves, analyses, and synthesises across those sources.

**Patterns used:**
- `SynthesisBuilder` — synthesises findings from multiple cases and sources
- `AnalogicalReasoner` (enterprise) — draws analogies between this case and cases in other areas
- `CrossDomainSynthesizer` (enterprise) — identifies relevant principles from adjacent legal domains

**Integration:** LangChain with `ConversationBufferMemory` — multi-step research session with threading

---

```python
import mycontext
mycontext.activate_license("MC-ENT-YOUR-KEY")

from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage, HumanMessage

from mycontext.templates.free.reasoning import SynthesisBuilder
from mycontext.templates.enterprise.reasoning import AnalogicalReasoner
from mycontext.templates.enterprise.synthesis import CrossDomainSynthesizer
from mycontext.intelligence import QualityMetrics

llm = ChatOpenAI(model="gpt-4o", temperature=0)
metrics = QualityMetrics(mode="heuristic")
memory = ConversationBufferMemory(return_messages=True)


def legal_research_session(research_question: str, jurisdiction: str) -> dict:
    results = {}

    # Step 1: Direct case law synthesis
    synth_ctx = SynthesisBuilder().build_context(
        sources=f"Case law in {jurisdiction} relevant to: {research_question}",
        topic=research_question,
    )
    synth_score = metrics.evaluate(synth_ctx)
    print(f"Synthesis context: {synth_score.overall:.0%}")

    messages = [SystemMessage(content=synth_ctx.assemble())]
    messages.extend(memory.chat_memory.messages)
    messages.append(HumanMessage(content=f"Synthesise case law on: {research_question} in {jurisdiction}"))

    direct_research = llm.invoke(messages).content
    memory.chat_memory.add_user_message(research_question)
    memory.chat_memory.add_ai_message(direct_research)
    results["direct_case_law"] = direct_research

    # Step 2: Analogical reasoning from adjacent areas
    analogy_ctx = AnalogicalReasoner().build_context(
        situation=research_question,
        context_section=f"Jurisdiction: {jurisdiction}. Base findings:\n{direct_research[:1000]}",
    )
    messages2 = [SystemMessage(content=analogy_ctx.assemble())]
    messages2.extend(memory.chat_memory.messages)
    messages2.append(HumanMessage(
        content="What cases from analogous legal areas (contract, tort, IP, employment) support or challenge this position?"
    ))
    analogies = llm.invoke(messages2).content
    memory.chat_memory.add_user_message("Analogous areas")
    memory.chat_memory.add_ai_message(analogies)
    results["analogies"] = analogies

    # Step 3: Cross-domain synthesis (other jurisdictions, international law)
    cross_ctx = CrossDomainSynthesizer().build_context(
        sources=f"Direct findings:\n{direct_research}\n\nAnalogies:\n{analogies}",
        topic=f"Cross-jurisdictional synthesis for: {research_question}",
    )
    messages3 = [SystemMessage(content=cross_ctx.assemble())]
    messages3.extend(memory.chat_memory.messages)
    messages3.append(HumanMessage(
        content="Identify supporting principles from US, EU, and Commonwealth jurisdictions that strengthen the argument."
    ))
    cross_domain = llm.invoke(messages3).content
    results["cross_jurisdictional"] = cross_domain

    # Step 4: Research memo synthesis
    final_synth = SynthesisBuilder().build_context(
        sources="\n\n".join(results.values()),
        topic=f"Research memo: {research_question}",
    )
    research_memo = final_synth.execute(provider="openai").response
    results["research_memo"] = research_memo

    return results


research = legal_research_session(
    research_question=(
        "Does an AI-generated work constitute a 'work made for hire' under copyright law "
        "when a human provides the prompts but the AI generates the output?"
    ),
    jurisdiction="England and Wales",
)

print("=== RESEARCH MEMO ===")
print(research["research_memo"])
```

## What You Get

A multi-stage research memo covering:
- Direct case law and statute in your primary jurisdiction
- Analogous cases from adjacent legal domains (IP, contract, employment)
- Cross-jurisdictional perspective from US, EU, Commonwealth
- Synthesis into a coherent legal argument with citations

The memory chain means each step builds on the last — analogies are grounded in the direct research, and the cross-jurisdictional analysis references both.
