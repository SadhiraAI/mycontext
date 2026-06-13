---
sidebar_position: 2
title: Contract Risk Review
description: Clause-by-clause contract risk analysis using RiskAssessor + RiskMitigator + ImpactAssessor over a LlamaIndex RAG pipeline of legal precedent and standard clause libraries.
---

# Contract Risk Review

**Scenario:** Your legal team reviews commercial contracts — NDAs, SaaS agreements, service contracts, partnership agreements. Each review takes hours, and coverage is inconsistent depending on who does the review. You want a first-pass AI review that flags risky clauses, compares them to market standards, and suggests alternative language.

**Patterns used:**
- `RiskAssessor` — evaluates each clause for legal and business risk
- `RiskMitigator` — proposes specific language changes that reduce identified risks
- `ImpactAssessor` — quantifies what each risk scenario could cost

**Integration:** LlamaIndex RAG over a clause precedent library + streaming LangChain output

---

```python
import mycontext

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from mycontext.templates.free.specialized import RiskAssessor
from mycontext.templates.enterprise.specialized import RiskMitigator, ImpactAssessor
from mycontext.intelligence import QualityMetrics

llm = ChatOpenAI(model="gpt-4o", temperature=0)
metrics = QualityMetrics(mode="heuristic")


def build_clause_index(precedent_dir: str) -> VectorStoreIndex:
    """Index of standard clauses, case law summaries, and market standards."""
    docs = SimpleDirectoryReader(precedent_dir).load_data()
    return VectorStoreIndex.from_documents(docs)


def review_contract(contract_text: str, contract_type: str, index: VectorStoreIndex) -> dict:
    # Retrieve comparable clauses and standards
    query_engine = index.as_query_engine(similarity_top_k=6)
    market_standards = str(query_engine.query(
        f"Standard and market-acceptable clauses for {contract_type}"
    ))

    full_context = f"Contract:\n{contract_text}\n\nMarket standards:\n{market_standards}"

    risk_ctx = RiskAssessor().build_context(
        decision=f"Signing this {contract_type}",
        depth="comprehensive",
    )
    risk_ctx.knowledge = full_context

    mitigant_ctx = RiskMitigator().build_context(
        challenge=f"Risky clauses in {contract_type}",
        context_section=full_context,
    )
    impact_ctx = ImpactAssessor().build_context(
        situation=f"Worst-case scenarios from {contract_type}",
        context_section=full_context,
    )

    results = {}
    for name, ctx, question in [
        ("risks", risk_ctx, "List every risky clause with severity (Critical/High/Medium) and why it is risky."),
        ("mitigants", mitigant_ctx, "For each high-risk clause, provide alternative language that protects our interests."),
        ("impact", impact_ctx, "What is the financial and operational impact if the worst-case scenarios in these clauses occur?"),
    ]:
        score = metrics.evaluate(ctx)
        print(f"  {name}: {score.overall:.0%}")
        results[name] = llm.invoke([
            SystemMessage(content=ctx.assemble()),
            HumanMessage(content=question),
        ]).content

    return results


saas_contract = """
7.3 LIMITATION OF LIABILITY. NOTWITHSTANDING ANYTHING TO THE CONTRARY, VENDOR'S 
TOTAL LIABILITY SHALL NOT EXCEED THE GREATER OF $100 OR THE AMOUNTS PAID IN THE 
PRIOR 30 DAYS.

8.1 DATA OWNERSHIP. ALL DATA PROCESSED THROUGH THE SERVICE MAY BE USED BY VENDOR 
FOR PRODUCT IMPROVEMENT, ANALYTICS, AND TRAINING PURPOSES WITHOUT RESTRICTION.

9.2 TERMINATION. VENDOR MAY TERMINATE THIS AGREEMENT WITH 24 HOURS NOTICE FOR ANY REASON.

11.1 GOVERNING LAW. This agreement shall be governed by the laws of Delaware. 
Customer irrevocably consents to exclusive jurisdiction in Delaware courts.

12.4 AUTO-RENEWAL. This agreement auto-renews for successive 3-year terms unless 
cancelled in writing 180 days prior to renewal date.
"""

index = build_clause_index("./legal/clause-library/")
review = review_contract(saas_contract, "SaaS Master Services Agreement", index)

print("=== RISK FLAGS ===")
print(review["risks"][:600])
print("\n=== SUGGESTED LANGUAGE ===")
print(review["mitigants"][:600])
print("\n=== IMPACT ASSESSMENT ===")
print(review["impact"][:400])
```

## What Gets Flagged in the Example

| Clause | Risk level | Issue |
|--------|-----------|-------|
| 7.3 Limitation of Liability | Critical | Cap of $100 or 30-day fees is unconscionable for enterprise contracts |
| 8.1 Data Ownership | Critical | Unlimited data use for training has GDPR and confidentiality implications |
| 9.2 Termination | High | 24-hour notice with no cause removes commercial certainty |
| 12.4 Auto-Renewal | High | 180-day cancellation window creates lock-in risk |

## Alternative Language Suggestions

The `RiskMitigator` produces specific redline language, not generic advice:

> **Clause 7.3 — Suggested replacement:**
> "Vendor's total liability shall not exceed the greater of (a) the total fees paid by Customer in the twelve (12) months preceding the claim, or (b) USD 100,000."
