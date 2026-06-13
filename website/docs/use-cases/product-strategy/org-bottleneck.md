---
sidebar_position: 4
title: Organizational Bottleneck Diagnosis
description: Find what is slowing your org with FeedbackLoopIdentifier + BottleneckIdentifier + SystemArchetypeAnalyzer. AutoGen systems thinking workshop.
---

# Organizational Bottleneck Diagnosis

**Scenario:** Something is slowing your organization — but it is not obvious what. Decisions take too long, teams are blocked, output is below what the headcount would suggest. You want structured systems thinking that finds the root constraint, not just visible symptoms.

**Patterns used:**
- `FeedbackLoopIdentifier` — maps reinforcing and balancing feedback loops
- `BottleneckIdentifier` — finds the single constraint limiting the whole system
- `SystemArchetypeAnalyzer` — identifies which systemic archetype is in play

**Integration:** AutoGen three-agent workshop with round-robin expert analysis

---

```python
import mycontext

from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from mycontext.templates.enterprise.systems_thinking import (
    FeedbackLoopIdentifier,
    BottleneckIdentifier,
    SystemArchetypeAnalyzer,
)
from mycontext.intelligence import QualityMetrics

metrics = QualityMetrics(mode="heuristic")


def org_diagnosis(org_description: str, symptoms: str) -> str:
    context = f"Organization:\n{org_description}\n\nSymptoms:\n{symptoms}"

    feedback_ctx = FeedbackLoopIdentifier().build_context(
        system=org_description,
        observation=symptoms,
    )
    bottleneck_ctx = BottleneckIdentifier().build_context(
        system=org_description,
        process=symptoms,
    )
    archetype_ctx = SystemArchetypeAnalyzer().build_context(
        system=org_description,
        observation=symptoms,
    )

    llm_config = {"config_list": [{"model": "gpt-4o-mini"}]}

    systems_analyst = AssistantAgent(
        name="SystemsAnalyst",
        system_message=feedback_ctx.assemble(),
        llm_config=llm_config,
    )
    bottleneck_specialist = AssistantAgent(
        name="BottleneckSpecialist",
        system_message=bottleneck_ctx.assemble(),
        llm_config=llm_config,
    )
    archetype_expert = AssistantAgent(
        name="ArchetypeExpert",
        system_message=archetype_ctx.assemble(),
        llm_config=llm_config,
    )
    facilitator = UserProxyAgent(
        name="WorkshopFacilitator",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=1,
        code_execution_config=False,
    )

    group_chat = GroupChat(
        agents=[facilitator, systems_analyst, bottleneck_specialist, archetype_expert],
        messages=[],
        max_round=6,
        speaker_selection_method="round_robin",
    )
    manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)

    facilitator.initiate_chat(
        manager,
        message=(
            f"Diagnose what is slowing this organization:\n\n{context}\n\n"
            "SystemsAnalyst: map the feedback loops. "
            "BottleneckSpecialist: find the primary constraint. "
            "ArchetypeExpert: name the system archetype and its prediction. "
            "Then agree on the highest-leverage intervention."
        ),
    )

    return "\n\n".join(
        m["content"] for m in group_chat.messages
        if m.get("name") != "WorkshopFacilitator"
    )


diagnosis = org_diagnosis(
    org_description=(
        "150-person SaaS company. 6 engineering squads, product owns roadmap but not capacity. "
        "Sales closes deals with custom feature promises. CS escalates customer issues to Engineering directly."
    ),
    symptoms=(
        "Sprints constantly disrupted by urgent escalations. "
        "Roadmap items delayed 2-3 quarters. "
        "Engineers burned out, 3 senior departures in 6 months. "
        "Sales frustrated. Product team feels powerless."
    ),
)

print(diagnosis)
```

## What You Get

A systems diagnosis that goes beyond surface symptoms:

- **Feedback loops:** the reinforcing cycles making the situation worse over time
- **Bottleneck:** the single constraint limiting the system (often not what leadership assumes)
- **System archetype:** which classic dysfunction is in play and what it predicts if untreated
- **High-leverage intervention:** the one structural change with the most systemic impact
