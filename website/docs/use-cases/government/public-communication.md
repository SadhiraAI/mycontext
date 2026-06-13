---
sidebar_position: 3
title: Public Communication Simplifier
description: Translate complex government documents into accessible public notices using SimplificationEngine + AudienceAdapter + ClarityOptimizer. Blueprint + LangChain streaming.
---

# Public Communication Simplifier

**Scenario:** Government agencies produce legislation, regulations, and public notices in complex legal and bureaucratic language. Citizens cannot understand what they are required to do, leading to non-compliance, public distrust, and avoidable helpline calls. You want plain-language versions generated automatically.

**Patterns used:**
- `SimplificationEngine` — removes jargon without losing accuracy
- `AudienceAdapter` — adapts the communication to the target public audience
- `ClarityOptimizer` — ensures every instruction is unambiguous and actionable

**Integration:** Blueprint + LangChain streaming for real-time portal delivery

---

```python
import mycontext

from mycontext.structure import Blueprint
from mycontext.foundation import Guidance, Constraints
from mycontext.templates.enterprise.communication import SimplificationEngine, ClarityOptimizer
from mycontext.templates.free.communication import AudienceAdapter
from mycontext.intelligence import QualityMetrics
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
metrics = QualityMetrics(mode="heuristic")

public_comm_blueprint = Blueprint(
    name="public_communication",
    guidance=Guidance(
        role="Government plain language writer following GOV.UK style guide",
        rules=[
            "Use grade 8 reading level or below",
            "Active voice always: use 'You must' not 'It is required that'",
            "Lead with what the person needs to do, not the legal context",
            "Every deadline must be a specific date",
            "Include: what to do, by when, what happens if you do not, where to get help",
        ],
    ),
    directive_template=(
        "Translate this official document for the public:\n\n"
        "{official_document}\n\n"
        "Target audience: {audience}\n"
        "Key action required: {key_action}"
    ),
    constraints=Constraints(
        must_include=["what to do", "deadline", "consequences of inaction", "contact for help"],
        must_not_include=["Section references without explanation", "Latin terms"],
        format_rules=[
            "Start with a one-sentence summary",
            "Numbered steps for actions",
            "Bold every deadline",
        ],
    ),
    token_budget=2000,
    optimization="quality",
)


def simplify_document(official_document: str, audience: str, key_action: str = "") -> str:
    ctx = public_comm_blueprint.build(
        official_document=official_document,
        audience=audience,
        key_action=key_action,
    )
    score = metrics.evaluate(ctx)
    print(f"Context quality: {score.overall:.0%}")
    if score.overall < 0.68:
        raise ValueError(f"Context quality too low: {score.overall:.0%}")
    return ctx.execute(provider="openai").response


official_notice = (
    "Pursuant to Section 47(2)(b) of the Local Government Finance Act 1992, "
    "ratepayers who have not submitted the requisite documentation evidencing continued eligibility "
    "within the prescribed period of 30 days from the date of notification hereof, "
    "shall be liable to reassessment of their relief entitlement with retrospective effect."
)

plain_version = simplify_document(
    official_notice,
    audience="small business owners",
    key_action="Submit proof of eligibility to keep your business rates relief",
)
print(plain_version)
```

## What You Get

**Official notice:**
> "...ratepayers who have not submitted the requisite documentation within the prescribed period of 30 days shall be liable to reassessment with retrospective effect..."

**Plain language version:**
> **You need to send us documents to keep your business rates discount.**
>
> **What to do:**
> 1. Gather documents showing your business still meets the eligibility criteria
> 2. Send them to us by **[specific date]**
>
> **If you do not respond:** Your discount will be removed and you may owe the full business rates amount going back to the start of this financial year.
>
> **Help:** Call 0300 XXX XXXX or email businessrates@council.gov.uk

## Multilingual Output

```python
ctx = public_comm_blueprint.build(
    official_document=official_notice,
    audience="Polish-speaking residents",
    key_action="Submit documents to keep your housing benefit",
)
ctx.constraints.format_rules.append("Translate the entire output into Polish")
result = ctx.execute(provider="openai").response
```
