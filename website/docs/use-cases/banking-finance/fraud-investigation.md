---
sidebar_position: 6
title: Fraud Pattern Investigation
description: Investigate suspicious transaction patterns with AnomalyDetector + PatternRecognitionEngine + CausalReasoner. An AutoGen investigator chain that traces anomalies to fraud hypotheses.
---

# Fraud Pattern Investigation

**Scenario:** Your fraud team has flagged a cluster of suspicious transactions. They need to move from "this looks odd" to "here is the likely fraud typology, the probable mechanism, and the evidence chain" — fast. Manual investigation is time-consuming and inconsistent across analysts.

**Patterns used:**
- `AnomalyDetector` — surfaces statistically and behaviourally unusual patterns
- `PatternRecognitionEngine` — identifies known fraud typologies in the transaction data
- `CausalReasoner` — builds the causal chain from anomaly to fraud mechanism

**Integration:** AutoGen sequential investigator chain — anomaly analyst feeds pattern recogniser feeds causal modeller

---

```python
import mycontext

from autogen import AssistantAgent, UserProxyAgent
from mycontext.templates.enterprise.analysis import AnomalyDetector
from mycontext.templates.enterprise.synthesis import PatternRecognitionEngine
from mycontext.templates.enterprise.reasoning import CausalReasoner
from mycontext.intelligence import QualityMetrics

metrics = QualityMetrics(mode="heuristic")


def investigate_fraud(transaction_data: str, account_profile: str) -> dict:
    # Each agent gets a purpose-built context
    anomaly_ctx = AnomalyDetector().build_context(
        data_description=transaction_data,
        context_section=f"Account profile: {account_profile}",
    )
    pattern_ctx = PatternRecognitionEngine().build_context(
        data_description=transaction_data,
        context_section="Known fraud typologies: card testing, account takeover, money mule, merchant fraud",
    )
    causal_ctx = CausalReasoner().build_context(
        phenomenon="Suspected fraudulent transaction pattern",
        context_section=f"Transaction data:\n{transaction_data}\nProfile:\n{account_profile}",
    )

    for name, ctx in [("anomaly", anomaly_ctx), ("pattern", pattern_ctx), ("causal", causal_ctx)]:
        s = metrics.evaluate(ctx)
        print(f"  {name}: {s.overall:.0%}")

    llm_config = {"config_list": [{"model": "gpt-4o-mini"}]}

    anomaly_agent = AssistantAgent(
        name="AnomalyAnalyst",
        system_message=anomaly_ctx.assemble(),
        llm_config=llm_config,
    )
    pattern_agent = AssistantAgent(
        name="FraudPatternRecogniser",
        system_message=pattern_ctx.assemble(),
        llm_config=llm_config,
    )
    causal_agent = AssistantAgent(
        name="CausalInvestigator",
        system_message=causal_ctx.assemble(),
        llm_config=llm_config,
    )
    investigator = UserProxyAgent(
        name="LeadInvestigator",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=1,
        code_execution_config=False,
    )

    findings = {}

    # Step 1: Anomaly analysis
    investigator.initiate_chat(
        anomaly_agent,
        message=f"Identify all statistically unusual patterns in:\n\n{transaction_data}",
        max_turns=2,
    )
    findings["anomalies"] = anomaly_agent.last_message()["content"]

    # Step 2: Pattern matching
    investigator.initiate_chat(
        pattern_agent,
        message=f"Given these anomalies:\n{findings['anomalies']}\n\nWhich fraud typologies do they match?",
        max_turns=2,
    )
    findings["fraud_type"] = pattern_agent.last_message()["content"]

    # Step 3: Causal chain
    investigator.initiate_chat(
        causal_agent,
        message=f"Build the causal chain from these anomalies to the suspected fraud mechanism:\n{findings['fraud_type']}",
        max_turns=2,
    )
    findings["causal_chain"] = causal_agent.last_message()["content"]

    return findings


transaction_data = """
Account #4421-XXXX-XXXX-8834 (opened 45 days ago):
- 47 micro-transactions ($0.50-$2.00) across 12 merchants in 6 hours
- 3 x $999 purchases at electronics retailers (card-present) within 30 min
- Location data: transactions span 4 cities simultaneously
- Previous 30-day average: 3 transactions/week, avg $45
- Card reported 'lost' by customer 6 hours after transaction cluster
"""

account_profile = "New account, first credit card, income unverified, applied online via VPN"

findings = investigate_fraud(transaction_data, account_profile)
print("=== ANOMALIES ===")
print(findings["anomalies"][:400])
print("\n=== FRAUD TYPE ===")
print(findings["fraud_type"][:400])
print("\n=== CAUSAL CHAIN ===")
print(findings["causal_chain"][:400])
```

## What You Get

A three-stage fraud investigation that moves from observation to conclusion:

| Stage | Output |
|-------|--------|
| **Anomaly Analysis** | Statistical outliers, behavioural deviations, velocity anomalies flagged with severity |
| **Pattern Matching** | Fraud typology match (e.g. "card testing followed by account takeover") with confidence |
| **Causal Chain** | Step-by-step reconstruction of how the fraud was likely executed |

The output gives an investigator a structured starting point with evidence — not just "this looks suspicious."

## SAR Report Integration

Feed the investigation into a `NarrativeBuilder` for automatic Suspicious Activity Report drafting:

```python
from mycontext.templates.enterprise.communication import NarrativeBuilder

sar_ctx = NarrativeBuilder().build_context(
    content="\n\n".join(findings.values()),
    context_section="Format as a Suspicious Activity Report (SAR) narrative",
)
sar_draft = sar_ctx.execute(provider="openai").response
```
