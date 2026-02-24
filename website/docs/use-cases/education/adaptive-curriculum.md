---
sidebar_position: 2
title: Adaptive Curriculum Builder
description: Build learning paths that adjust to each student's level using ScaffoldingFramework + ZoneOfProximalDevelopment + CognitiveLoadManager. LangChain memory-backed tutor.
---

# Adaptive Curriculum Builder

**Scenario:** A student is learning a complex subject — say, machine learning or financial modelling. Static course content ignores where they actually are. You want a curriculum that starts at their current level, builds progressively, avoids overwhelming them, and adjusts based on how they respond to each step.

**Patterns used:**
- `ScaffoldingFramework` (enterprise) — provides the right level of support, incrementally withdrawn as competence builds
- `ZoneOfProximalDevelopment` (enterprise) — targets concepts just beyond current competence (Vygotsky-based)
- `CognitiveLoadManager` (enterprise) — prevents overload by controlling complexity and pacing

**Integration:** LangChain with `ConversationBufferMemory` — persistent session that updates as the student progresses

---

```python
import mycontext
mycontext.activate_license("MC-ENT-YOUR-KEY")

from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage, HumanMessage

from mycontext.templates.enterprise.learning import (
    ScaffoldingFramework,
    ZoneOfProximalDevelopment,
    CognitiveLoadManager,
)
from mycontext.intelligence import QualityMetrics

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4)
metrics = QualityMetrics(mode="heuristic")


class AdaptiveTutor:
    def __init__(self, subject: str, student_profile: str):
        self.subject = subject
        self.student_profile = student_profile
        self.memory = ConversationBufferMemory(return_messages=True)
        self.current_level = "beginner"
        self.session_count = 0

    def _build_tutor_context(self):
        """Rebuild context based on current student level."""
        scaffold_ctx = ScaffoldingFramework().build_context(
            concept=self.subject,
            learner_level=self.current_level,
            prior_knowledge=self.student_profile,
        )
        zpd_ctx = ZoneOfProximalDevelopment().build_context(
            concept=self.subject,
            learner_level=self.current_level,
        )
        load_ctx = CognitiveLoadManager().build_context(
            complex_topic=self.subject,
            learner_level=self.current_level,
        )

        # Merge scaffolding rules into a single teaching context
        combined_rules = []
        for ctx in [scaffold_ctx, zpd_ctx, load_ctx]:
            if ctx.guidance and ctx.guidance.rules:
                combined_rules.extend(ctx.guidance.rules[:2])

        scaffold_ctx.guidance.rules = combined_rules
        score = metrics.evaluate(scaffold_ctx)
        print(f"  Tutor context quality: {score.overall:.0%}")
        return scaffold_ctx

    def teach(self, topic: str) -> str:
        self.session_count += 1
        ctx = self._build_tutor_context()

        messages = [SystemMessage(content=ctx.assemble())]
        messages.extend(self.memory.chat_memory.messages[-8:])  # Last 4 exchanges
        messages.append(HumanMessage(
            content=f"Teach me: {topic}. My current level: {self.current_level}."
        ))

        response = llm.invoke(messages).content
        self.memory.chat_memory.add_user_message(f"Teach: {topic}")
        self.memory.chat_memory.add_ai_message(response)
        return response

    def check_understanding(self, topic: str) -> str:
        messages = [SystemMessage(content=(
            "You are a patient tutor. Ask ONE diagnostic question to check "
            "if the student understood the concept. Make it a practical application question."
        ))]
        messages.extend(self.memory.chat_memory.messages[-4:])
        messages.append(HumanMessage(content=f"Check my understanding of: {topic}"))

        question = llm.invoke(messages).content
        self.memory.chat_memory.add_ai_message(question)
        return question

    def update_level(self, student_response: str, topic: str) -> str:
        """Evaluate response and potentially advance level."""
        messages = [SystemMessage(content=(
            "You are an expert educator. Evaluate this student response. "
            "If they demonstrate solid understanding, respond with 'ADVANCE'. "
            "Otherwise, clarify the misconception gently. Be encouraging."
        ))]
        messages.extend(self.memory.chat_memory.messages[-6:])
        messages.append(HumanMessage(content=student_response))

        feedback = llm.invoke(messages).content
        if "ADVANCE" in feedback:
            levels = ["beginner", "intermediate", "advanced", "expert"]
            idx = levels.index(self.current_level)
            if idx < len(levels) - 1:
                self.current_level = levels[idx + 1]
                feedback = f"Excellent! Moving to {self.current_level} level.\n\n{feedback}"

        self.memory.chat_memory.add_user_message(student_response)
        self.memory.chat_memory.add_ai_message(feedback)
        return feedback


# Usage
tutor = AdaptiveTutor(
    subject="backpropagation in neural networks",
    student_profile="Software engineer, comfortable with Python and calculus basics, no ML background",
)

# Session
print(tutor.teach("what a neural network is"))
print(tutor.check_understanding("neural networks"))
print(tutor.update_level("A network of nodes that pass numbers through layers?", "neural networks"))
print(tutor.teach("gradient descent"))
```

## What You Get

A tutor that teaches differently depending on where the student is:

- **Beginner:** concrete analogies, worked examples, no assumed knowledge
- **Intermediate:** concepts with some formalism, application exercises
- **Advanced:** edge cases, trade-offs, real-world limitations

The memory means each session builds on the last. The ZPD logic means topics are always at the right difficulty — challenging but achievable. CognitiveLoadManager prevents the tutor from introducing too many concepts at once.
