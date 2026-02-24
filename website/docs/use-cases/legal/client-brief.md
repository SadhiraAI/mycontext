---
sidebar_position: 6
title: Client Brief Simplifier
description: Convert complex legal opinions into accessible client briefings using SimplificationEngine + AudienceAdapter + PersuasionFramework. A Blueprint with streaming FastAPI delivery.
---

# Client Brief Simplifier

**Scenario:** Your firm produces detailed legal opinions in dense professional language. Clients often don't read them, don't understand the implications, or need to share them with non-lawyers (board members, investors). You want to generate plain-language client briefings that retain accuracy while being accessible and actionable.

**Patterns used:**
- `SimplificationEngine` (enterprise) — removes legal jargon without losing precision
- `AudienceAdapter` — adapts structure and vocabulary to the specific client audience
- `PersuasionFramework` (enterprise) — structures the briefing so the key message lands clearly

**Integration:** Blueprint + streaming FastAPI endpoint

---

```python
import mycontext
mycontext.activate_license("MC-ENT-YOUR-KEY")

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from mycontext.structure import Blueprint
from mycontext.foundation import Guidance, Constraints
from mycontext.templates.enterprise.communication import (
    SimplificationEngine,
    PersuasionFramework,
)
from mycontext.templates.free.communication import AudienceAdapter
from mycontext.intelligence import QualityMetrics, TemplateIntegratorAgent
from langchain_openai import ChatOpenAI

app = FastAPI()
llm = ChatOpenAI(model="gpt-4o-mini", streaming=True, temperature=0.3)
metrics = QualityMetrics(mode="heuristic")

brief_blueprint = Blueprint(
    name="client_legal_brief",
    guidance=Guidance(
        role="Partner-level lawyer writing for a sophisticated but non-legal client audience",
        rules=[
            "Lead with what the client needs to do, not the legal analysis",
            "State the bottom line in the first paragraph",
            "Explain legal concepts using business analogies",
            "Flag deadlines and required actions explicitly",
            "Quantify risks in commercial terms where possible",
        ],
    ),
    directive_template=(
        "Translate this legal opinion into a client briefing:\n\n"
        "{legal_opinion}\n\n"
        "Client: {client_description}\n"
        "Context: {business_context}\n"
        "Key question the client asked: {client_question}"
    ),
    constraints=Constraints(
        must_include=["bottom line", "required actions", "key risks", "timeline", "next steps"],
        must_not_include=["Latin phrases", "section numbers without explanation", "unexplained citations"],
        format_rules=[
            "Bottom line in bold at the top",
            "Required actions as a numbered checklist",
            "Max 600 words total",
        ],
    ),
    token_budget=2000,
    optimization="quality",
)


@app.post("/brief")
async def generate_brief(
    legal_opinion: str,
    client_description: str,
    business_context: str,
    client_question: str,
):
    ctx = brief_blueprint.build(
        legal_opinion=legal_opinion,
        client_description=client_description,
        business_context=business_context,
        client_question=client_question,
    )
    score = metrics.evaluate(ctx)
    if score.overall < 0.68:
        return {"error": f"Context quality too low: {score.overall:.0%}"}

    messages = ctx.to_messages(user_message="Generate the client briefing now.")

    async def generate():
        async for chunk in llm.astream(messages):
            if chunk.content:
                yield chunk.content

    return StreamingResponse(generate(), media_type="text/plain")


# Sync usage
def generate_brief_sync(legal_opinion: str, client_info: dict) -> str:
    ctx = brief_blueprint.build(legal_opinion=legal_opinion, **client_info)
    return ctx.execute(provider="openai").response


legal_opinion = """
In our considered view, the proposed data sharing arrangement as currently structured 
is likely to constitute a restricted transfer of personal data to a third country 
for the purposes of the UK GDPR, specifically Chapter V thereof. The absence of 
adequate safeguards within the meaning of Article 46 UK GDPR, including but not 
limited to standard contractual clauses or binding corporate rules, renders the 
proposed arrangement non-compliant. We recommend immediate cessation pending 
implementation of appropriate transfer mechanisms...
"""

brief = generate_brief_sync(
    legal_opinion,
    {
        "client_description": "SaaS CEO, technically literate but not a lawyer",
        "business_context": "B2B data analytics company expanding to UK market",
        "client_question": "Can we share our UK customers' data with our US analytics platform?",
    },
)
print(brief)
```

## What You Get

**Input (legal opinion):**
> "...the proposed data sharing arrangement is likely to constitute a restricted transfer... absence of adequate safeguards... renders the proposed arrangement non-compliant..."

**Output (client briefing):**
> **Bottom line: Your current plan to share UK customer data with your US platform is not compliant with UK data protection law. Do not proceed until the steps below are completed.**
>
> **What you need to do (in order):**
> 1. Pause the US data transfer immediately
> 2. Sign Standard Contractual Clauses with your US platform provider (we can draft these — 2 weeks)
> 3. Update your privacy policy to disclose the transfer mechanism
> 4. Complete a Transfer Impact Assessment (we recommend this as a precaution)
>
> **Why this matters commercially:** UK ICO fines for non-compliant data transfers can reach 4% of global annual turnover...
