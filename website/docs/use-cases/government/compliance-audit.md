---
sidebar_position: 4
title: Regulatory Compliance Audit
description: Audit public sector processes against statutory obligations using SystemHealthAuditor + AnomalyDetector + EthicalFrameworkAnalyzer. LlamaIndex RAG over statute and guidance.
---

# Regulatory Compliance Audit

**Scenario:** A government body or publicly funded organisation must demonstrate compliance with statutory obligations, procurement rules, data protection legislation, or sector-specific regulation. Manual audits are slow and subjective. You want a structured AI audit that compares processes against the actual statutory text.

**Patterns used:**
- `SystemHealthAuditor` (enterprise) — assesses completeness and soundness of processes against standards
- `AnomalyDetector` (enterprise) — flags deviations from expected compliance patterns
- `EthicalFrameworkAnalyzer` (enterprise) — evaluates whether processes meet governance and ethical standards

**Integration:** LlamaIndex RAG over statute corpus + quality-gated Context pipeline

---

```python
import mycontext
mycontext.activate_license("MC-ENT-YOUR-KEY")

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from mycontext.templates.enterprise.diagnostic import SystemHealthAuditor
from mycontext.templates.enterprise.analysis import AnomalyDetector
from mycontext.templates.enterprise.ethical_reasoning import EthicalFrameworkAnalyzer
from mycontext.intelligence import QualityMetrics

llm = ChatOpenAI(model="gpt-4o", temperature=0)
metrics = QualityMetrics(mode="heuristic")


def build_statute_index(statutes_dir: str) -> VectorStoreIndex:
    docs = SimpleDirectoryReader(statutes_dir).load_data()
    return VectorStoreIndex.from_documents(docs)


def statutory_compliance_audit(
    process_description: str,
    statutory_framework: str,
    index: VectorStoreIndex,
) -> dict:
    qe = index.as_query_engine(similarity_top_k=8)
    statute_text = str(qe.query(
        f"Statutory obligations and requirements for: {statutory_framework} "
        f"as they apply to: {process_description[:200]}"
    ))

    full_context = f"Process:\n{process_description}\n\nStatutory requirements:\n{statute_text}"

    health_ctx = SystemHealthAuditor().build_context(
        system=f"Public sector process under {statutory_framework}",
        observation=full_context,
    )
    anomaly_ctx = AnomalyDetector().build_context(
        data_description=process_description,
        context_section=f"Expected: compliance with {statutory_framework}. Find deviations.",
    )
    ethics_ctx = EthicalFrameworkAnalyzer().build_context(
        situation=full_context,
        context_section="Assess governance quality, fairness, and public interest obligations",
    )

    results = {}
    for name, ctx, question in [
        ("health_audit", health_ctx, f"Audit this process against {statutory_framework} requirements. Identify all gaps."),
        ("anomalies", anomaly_ctx, f"What compliance anomalies are present relative to {statutory_framework}?"),
        ("ethics", ethics_ctx, "Does this process meet public sector governance and ethical standards?"),
    ]:
        score = metrics.evaluate(ctx)
        print(f"  {name}: {score.overall:.0%}")
        if score.overall >= 0.65:
            results[name] = llm.invoke([
                SystemMessage(content=ctx.assemble()),
                HumanMessage(content=question),
            ]).content

    return {
        "framework": statutory_framework,
        "process": process_description[:200],
        **results,
    }


procurement_process = """
Our procurement process:
1. Need identified by department head
2. Quotes requested from 2-3 preferred suppliers (no open tender for contracts <50,000)
3. Decision made by procurement manager, signed off by Finance Director
4. No conflicts of interest register maintained
5. Contract awarded via email, no formal contract document for purchases <10,000
6. No supplier diversity monitoring
7. No post-contract performance review
"""

index = build_statute_index("./statutes/procurement/")
audit = statutory_compliance_audit(
    procurement_process,
    "UK Public Contracts Regulations 2015 and Government Procurement Policy",
    index,
)

print("=== STATUTORY AUDIT ===")
print(audit["health_audit"][:600])
print("\n=== ANOMALIES ===")
print(audit["anomalies"][:400])
```

## Typical Findings

In the procurement process example above, the audit surfaces:

| Gap | Statutory basis |
|-----|----------------|
| No conflicts of interest register | PCR 2015 Reg.24 |
| Threshold for open competition may be set too high | PCR 2015 — below-threshold guidance |
| No formal contract for sub-10K purchases creates accountability gap | Government Accounting |
| No supplier diversity monitoring | Government Commercial Function guidance |
| No post-contract review | Best value duty, Local Government Act 1999 |
