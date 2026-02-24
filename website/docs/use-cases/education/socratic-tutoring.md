---
sidebar_position: 3
title: Socratic Tutoring Agent
description: Guide students to discover answers themselves with SocraticQuestioner + MetacognitiveMonitor + LearningFromExperience. An AutoGen tutor loop with reflection pauses.
---

# Socratic Tutoring Agent

**Scenario:** Traditional tutoring tells students the answer. Socratic tutoring guides them to discover it. You want an AI tutor that never gives the answer directly, monitors the student's thinking process, and helps them reflect on their own reasoning — building understanding that sticks.

**Patterns used:**
- `SocraticQuestioner` — probing questions that surface and challenge assumptions
- `MetacognitiveMonitor` (enterprise) — helps the student observe and regulate their own thinking
- `LearningFromExperience` (enterprise) — turns each exchange into a reusable mental model

**Integration:** AutoGen conversation loop with LangChain for non-interactive demo mode

---

```python
import mycontext
mycontext.activate_license("MC-ENT-YOUR-KEY")

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from mycontext.templates.free.specialized import SocraticQuestioner
from mycontext.templates.enterprise.metacognition import (
    MetacognitiveMonitor,
    LearningFromExperience,
)
from mycontext.intelligence import QualityMetrics

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4)
metrics = QualityMetrics(mode="heuristic")


def build_socratic_session(topic: str) -> tuple:
    socratic_ctx = SocraticQuestioner().build_context(topic=topic, depth="deep")
    meta_ctx = MetacognitiveMonitor().build_context(
        process=f"Student reasoning about: {topic}",
        context_section="Surface thinking gaps through questions only",
    )
    learn_ctx = LearningFromExperience().build_context(
        situation=f"Student discovering: {topic}",
        context_section="Turn each exchange into a reusable mental model",
    )

    for name, ctx in [("socratic", socratic_ctx), ("meta", meta_ctx), ("learning", learn_ctx)]:
        s = metrics.evaluate(ctx)
        print(f"  {name}: {s.overall:.0%}")

    return socratic_ctx, meta_ctx, learn_ctx


def run_session(topic: str, student_answers: list[str]) -> list[str]:
    socratic_ctx, meta_ctx, _ = build_socratic_session(topic)

    tutor_system = (
        f"{socratic_ctx.assemble()}\n\n"
        "CRITICAL RULE: Never give the answer directly. "
        "Only ask questions that help the student discover it. "
        "If the student is wrong, ask a question that reveals the gap."
    )

    history = [SystemMessage(content=tutor_system)]
    responses = []

    for i, student_answer in enumerate(student_answers):
        history.append(HumanMessage(content=student_answer))
        response = llm.invoke(history).content
        history.append(AIMessage(content=response))
        responses.append(response)

        if (i + 1) % 2 == 0:
            reflect_msgs = [SystemMessage(content=meta_ctx.assemble())]
            reflect_msgs.extend(history[-6:])
            reflect_msgs.append(HumanMessage(
                content="Prompt the student to reflect on their thinking process now."
            ))
            reflection = llm.invoke(reflect_msgs).content
            responses.append(f"[REFLECTION PROMPT] {reflection}")

    return responses


exchanges = run_session(
    topic="Why does adding salt lower the boiling point of water?",
    student_answers=[
        "Because salt makes water hotter?",
        "Something about the salt particles changing how the water behaves?",
        "Wait, so the salt molecules get in the way of water molecules escaping?",
        "The water molecules need more energy to escape because there are more particles?",
    ],
)

for i, response in enumerate(exchanges):
    tag = response[:20] if response.startswith("[REFLECTION") else f"Tutor {i+1}:"
    print(f"\n{tag}\n{response[:300]}")
```

## What You Get

A tutoring loop that:
- Never gives answers — only asks questions that guide discovery
- Tracks reasoning quality, not just answer correctness
- Pauses every 2 exchanges for metacognitive reflection
- Builds from wrong answer to correct understanding through questioning

The misconception path above ("salt makes water hotter" to "particles need more energy to escape") mirrors how human Socratic tutors work — finding where the student's mental model breaks down and asking the question that surfaces the gap.
