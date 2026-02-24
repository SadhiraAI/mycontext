---
sidebar_position: 4
title: Regulatory Compliance Audit
description: Audit processes against regulatory requirements using SystemHealthAuditor + AnomalyDetector + EthicalFrameworkAnalyzer over a LlamaIndex RAG corpus of regulation docs.
---

# Regulatory Compliance Audit

**Scenario:** Your compliance team needs to audit internal processes against a growing body of financial regulations (Basel III, MiFID II, GDPR, AML directives). Manual review is slow and risks missing gaps. You want an AI audit that retrieves the relevant regulation, compares it to your process documentation, and surfaces gaps.

**Patterns used:**
- `SystemHealthAuditor` (enterprise) — assesses completeness and soundness of processes against standards
- `AnomalyDetector` (enterprise) — flags deviations from expected regulatory compliance patterns
- `EthicalFrameworkAnalyzer` (enterprise) — evaluates whether processes meet ethical and governance standards

**Integration:** LangChain + LlamaIndex RAG over a regulation document corpus

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


def build_regulation_index(regulations_dir: str) -> VectorStoreIndex:
    docs = SimpleDirectoryReader(regulations_dir).load_data()
    return VectorStoreIndex.from_documents(docs)


def compliance_audit(
    process_description: str,
    regulation_name: str,
    index: VectorStoreIndex,
) -> dict:
    # Retrieve relevant regulation passages via RAG
    query_engine = index.as_query_engine(similarity_top_k=8)
    regulation_text = str(query_engine.query(
        f"Requirements for {regulation_name} compliance related to: {process_description[:200]}"
    ))

    full_context = (
        f"Process under audit:\n{process_description}\n\n"
        f"Relevant regulatory requirements:\n{regulation_text}"
    )

    # Three-lens audit
    health_ctx = SystemHealthAuditor().build_context(
        system=f"Compliance process for {regulation_name}",
        observation=full_context,
    )
    anomaly_ctx = AnomalyDetector().build_context(
        data_description=process_description,
        context_section=f"Expected: compliance with {regulation_name}. Identify deviations.",
    )
    ethics_ctx = EthicalFrameworkAnalyzer().build_context(
        situation=full_context,
        context_section="Evaluate governance quality and ethical soundness",
    )

    results = {}
    for name, ctx in [("health", health_ctx), ("anomaly", anomaly_ctx), ("ethics", ethics_ctx)]:
        score = metrics.evaluate(ctx)
        if score.overall < 0.65:
            results[name] = f"Low quality context ({score.overall:.0%}) — review inputs"
            continue
        response = llm.invoke([
            SystemMessage(content=ctx.assemble()),
            HumanMessage(content=f"Audit this process for {regulation_name} compliance gaps."),
        ]).content
        results[name] = response

    return {
        "regulation": regulation_name,
        "process_audited": process_description[:100],
        "health_audit": results.get("health", ""),
        "anomalies": results.get("anomaly", ""),
        "ethics_assessment": results.get("ethics", ""),
    }


# Example: AML process audit
aml_process = """
Customer onboarding:
1. Online KYC form (name, DOB, address, nationality)
2. Document upload (passport or driving licence)
3. Automated PEP/sanctions screening via third-party API
4. Risk scoring (low/medium/high) based on country and occupation
5. High-risk customers: enhanced due diligence form sent by email
6. No face-to-face verification required for any tier
7. Ongoing monitoring: automated alerts for transactions >10,000 currency units
8. SAR filing: manual process, no documented escalation path
"""

index = build_regulation_index("./regulations/aml/")
audit = compliance_audit(aml_process, "FATF AML Recommendations 2023", index)

print("=== PROCESS HEALTH ===")
print(audit["health_audit"][:600])
print("\n=== COMPLIANCE ANOMALIES ===")
print(audit["anomalies"][:400])
```

## What Gets Flagged

In the example above, the audit typically surfaces:

| Gap | Regulation reference |
|-----|---------------------|
| No face-to-face or video verification for high-risk customers | FATF R.10, Enhanced Due Diligence |
| No documented SAR escalation path | FATF R.20, STR obligations |
| Automated monitoring threshold may miss structuring | FATF R.10, Transaction monitoring |
| No periodic re-screening of existing customers | FATF R.12, Ongoing monitoring |
