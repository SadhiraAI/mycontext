---
sidebar_position: 6
title: Developer Onboarding Assistant
description: An Agent Skill + LangChain memory chatbot that adapts explanations to a new engineer's background — starts simple, gets deeper as understanding builds.
---

# Developer Onboarding Assistant

**Scenario:** A new engineer joins your team. They have good general skills but are unfamiliar with your specific stack, domain, and internal systems. You want a chatbot that explains things at the right level, asks questions to check understanding, and progressively deepens as they grow — rather than dumping everything at once.

**Patterns used:**
- `TechnicalTranslator` — adapts technical concepts to the reader's background
- `ScaffoldingFramework` — builds understanding incrementally (ZPD-based)
- `SocraticQuestioner` — tests understanding through questions rather than just delivering answers

**Integration:** Agent Skill loaded via `SkillRunner` + LangChain `ConversationBufferMemory`

---

## SKILL.md

Create `skills/onboarding-assistant/SKILL.md`:

```markdown
---
name: Developer Onboarding Assistant
description: Helps new engineers understand our codebase and domain progressively
license: internal
input_schema:
  engineer_background: str
  current_topic: str
  experience_level: str
pattern: technical_translator
---

You are onboarding {engineer_background} engineers into our system.

Current topic: {current_topic}
Experience level: {experience_level}

Start with the concrete and practical.
Build toward the abstract and principled.
Always check understanding before going deeper.
```

## Chatbot Implementation

```python
import mycontext

from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from mycontext.skills import SkillRunner
from mycontext.templates.enterprise.learning import ScaffoldingFramework
from mycontext.templates.free.specialized import SocraticQuestioner
from mycontext.intelligence import QualityMetrics

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
memory = ConversationBufferMemory(return_messages=True)
metrics = QualityMetrics(mode="heuristic")
runner = SkillRunner()


def get_onboarding_context(topic: str, background: str, level: str):
    """Build a context that scaffolds the explanation and checks understanding."""

    # Skill handles the translation layer
    skill_result = runner.run(
        skill_path=Path("skills/onboarding-assistant"),
        task=f"Explain: {topic}",
        execute=False,
        engineer_background=background,
        current_topic=topic,
        experience_level=level,
    )

    # Layer in scaffolding for progressive depth
    scaffold_ctx = ScaffoldingFramework().build_context(
        concept=topic,
        learner_level=level,
        prior_knowledge=background,
    )

    # Merge: use skill context as base, inject scaffolding rules into guidance
    ctx = skill_result.context
    if scaffold_ctx.guidance and ctx.guidance:
        ctx.guidance.rules.extend(scaffold_ctx.guidance.rules[:3])

    score = metrics.evaluate(ctx)
    print(f"  Context quality: {score.overall:.0%}")
    return ctx


def check_understanding_prompt(topic: str) -> str:
    """Use SocraticQuestioner to probe understanding before advancing."""
    sq_ctx = SocraticQuestioner().build_context(
        topic=topic,
        depth="surface",
    )
    result = llm.invoke([
        SystemMessage(content=sq_ctx.assemble()),
        HumanMessage(content=f"Ask ONE question to check if the engineer understood: {topic}"),
    ])
    return result.content


class OnboardingAssistant:
    def __init__(self, engineer_name: str, background: str, level: str = "mid"):
        self.name = engineer_name
        self.background = background
        self.level = level
        self.topics_covered = []
        self.memory = ConversationBufferMemory(return_messages=True)

    def explain(self, topic: str) -> str:
        ctx = get_onboarding_context(topic, self.background, self.level)
        messages = [SystemMessage(content=ctx.assemble())]
        messages.extend(self.memory.chat_memory.messages)
        messages.append(HumanMessage(content=f"Explain: {topic}"))

        response = llm.invoke(messages).content
        self.memory.chat_memory.add_user_message(f"Explain: {topic}")
        self.memory.chat_memory.add_ai_message(response)
        self.topics_covered.append(topic)
        return response

    def check_understanding(self, topic: str) -> str:
        question = check_understanding_prompt(topic)
        self.memory.chat_memory.add_ai_message(question)
        return question

    def answer(self, user_response: str) -> str:
        messages = [SystemMessage(content="You are a helpful technical mentor.")]
        messages.extend(self.memory.chat_memory.messages)
        messages.append(HumanMessage(content=user_response))
        response = llm.invoke(messages).content
        self.memory.chat_memory.add_user_message(user_response)
        self.memory.chat_memory.add_ai_message(response)
        return response


# Usage
assistant = OnboardingAssistant(
    engineer_name="Alex",
    background="backend Python developer, familiar with Django",
    level="mid",
)

# Start a learning session
print(assistant.explain("our event-driven architecture with Kafka"))
print(assistant.check_understanding("Kafka consumer groups"))

# After engineer replies:
print(assistant.answer("I think consumers in the same group share partitions?"))
```

## What You Get

- Explanations calibrated to the engineer's actual background — not generic docs
- Progressive scaffolding: simple → concrete → abstract → edge cases
- Socratic check-ins that expose gaps before moving on
- Full conversation memory so explanations build on each other
- Session logs you can use to identify where your documentation is unclear
