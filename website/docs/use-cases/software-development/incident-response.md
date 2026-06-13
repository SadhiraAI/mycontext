---
sidebar_position: 3
title: Incident Response & On-Call Triage
description: A three-agent AutoGen system that triages production incidents — one agent identifies the root cause, one audits system health, and one writes the postmortem.
---

# Incident Response & On-Call Triage

**Scenario:** Your on-call engineer gets paged at 2am. They need structured, fast analysis: what broke, why it broke, whether the system is still at risk, and what to do now. You want AI to do the first pass so the human can focus on fixing rather than diagnosing.

**Patterns used:**
- `RootCauseAnalyzer` — immediate cause + contributing factors + timeline
- `DiagnosticRootCauseAnalyzer` — deeper diagnostic with differential reasoning
- `SystemHealthAuditor` — assesses whether the system is in a stable state

**Integration:** AutoGen multi-agent conversation — triage agent, diagnostic agent, postmortem writer

---

```python
import mycontext

from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from mycontext.templates.free.reasoning import RootCauseAnalyzer
from mycontext.templates.enterprise.diagnostic import (
    DiagnosticRootCauseAnalyzer,
    SystemHealthAuditor,
)

def create_incident_crew(incident: dict) -> str:
    """
    incident = {
        "title": "Payment service 503s",
        "symptoms": "67% error rate since 14:32 UTC",
        "context": "Deployment 3.8.2 at 14:28, DB CPU spike at 14:31",
        "metrics": "p99 latency: 8.2s (was 220ms)",
    }
    """
    incident_brief = (
        f"Title: {incident['title']}\n"
        f"Symptoms: {incident['symptoms']}\n"
        f"Context: {incident['context']}\n"
        f"Metrics: {incident['metrics']}"
    )

    # Build specialized contexts for each agent
    triage_ctx = RootCauseAnalyzer().build_context(
        problem=incident_brief,
        depth="immediate",
    )
    diagnostic_ctx = DiagnosticRootCauseAnalyzer().build_context(
        observation=incident_brief,
        system="payment microservice",
    )
    health_ctx = SystemHealthAuditor().build_context(
        system="payment service + database cluster",
        observation=incident_brief,
    )

    llm_config = {"config_list": [{"model": "gpt-4o-mini"}]}

    triage_agent = AssistantAgent(
        name="TriageAgent",
        system_message=triage_ctx.assemble(),
        llm_config=llm_config,
    )
    diagnostic_agent = AssistantAgent(
        name="DiagnosticAgent",
        system_message=diagnostic_ctx.assemble(),
        llm_config=llm_config,
    )
    health_agent = AssistantAgent(
        name="HealthAuditor",
        system_message=health_ctx.assemble(),
        llm_config=llm_config,
    )
    user_proxy = UserProxyAgent(
        name="OnCallEngineer",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=1,
        code_execution_config=False,
    )

    group_chat = GroupChat(
        agents=[user_proxy, triage_agent, diagnostic_agent, health_agent],
        messages=[],
        max_round=6,
        speaker_selection_method="round_robin",
    )
    manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)

    user_proxy.initiate_chat(
        manager,
        message=(
            f"INCIDENT ACTIVE: {incident['title']}\n\n"
            f"{incident_brief}\n\n"
            "Each agent: provide your analysis. "
            "TriageAgent: immediate cause and action. "
            "DiagnosticAgent: differential diagnosis — what else could this be? "
            "HealthAuditor: is the system stable enough to continue or should we roll back now?"
        ),
    )
    return group_chat.messages


# Trigger from PagerDuty webhook or CLI
incident = {
    "title": "Payment service — 67% error rate",
    "symptoms": "503 errors from /api/checkout, /api/payment-methods since 14:32 UTC",
    "context": "Deployment 3.8.2 pushed at 14:28 UTC. DB CPU spiked to 98% at 14:31 UTC.",
    "metrics": "p99: 8200ms (baseline: 220ms). Connection pool exhausted.",
}

messages = create_incident_crew(incident)
```

## What You Get

Three independent analytical perspectives on the same incident — simultaneously:

| Agent | Analytical framework | Output |
|-------|---------------------|--------|
| TriageAgent | 5-why causal chain | Immediate cause + actions to take now |
| DiagnosticAgent | Differential diagnosis | Alternative hypotheses, rules out false leads |
| HealthAuditor | System health checklist | Stable/unstable verdict, rollback recommendation |

The conversation produces a structured incident analysis in under 60 seconds — equivalent to what typically takes an on-call engineer 20–30 minutes of log diving.

## Postmortem Integration

After the incident, feed the conversation into a `SynthesisBuilder` to auto-draft the postmortem:

```python
from mycontext.templates.free.reasoning import SynthesisBuilder

postmortem_ctx = SynthesisBuilder().build_context(
    sources="\n\n".join([m["content"] for m in messages]),
    topic="postmortem report",
)
postmortem = postmortem_ctx.execute(provider="openai").response
```
