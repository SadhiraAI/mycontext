---
sidebar_position: 3
title: Job Description & Candidate Evaluation
description: Write inclusive job descriptions and evaluate candidates consistently using ComparativeAnalyzer + RiskAssessor + AudienceAdapter. LangChain pipeline for HR teams.
---

# Job Description & Candidate Evaluation

**Scenario:** Your job descriptions are written by hiring managers, resulting in inconsistent quality, hidden bias (language that deters qualified candidates), and requirements that don't actually predict success. Candidate evaluation is similarly inconsistent. You want AI to audit and improve JDs, and to structure candidate comparison.

**Patterns used:**
- `ComparativeAnalyzer` — structured head-to-head candidate comparison against criteria
- `RiskAssessor` — flags hiring risks (over-specified requirements, potential bias signals)
- `AudienceAdapter` — calibrates the JD to attract the right candidate audience

**Integration:** LangChain two-stage pipeline — JD improvement then candidate comparison

---

```python
import mycontext

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from mycontext.templates.enterprise.decision import ComparativeAnalyzer
from mycontext.templates.free.specialized import RiskAssessor
from mycontext.templates.free.communication import AudienceAdapter
from mycontext.intelligence import QualityMetrics

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
metrics = QualityMetrics(mode="heuristic")


def audit_job_description(jd: str, target_audience: str, role_type: str) -> dict:
    risk_ctx = RiskAssessor().build_context(
        decision=f"Publish this job description for: {role_type}",
        depth="standard",
    )
    risk_ctx.knowledge = jd

    audience_ctx = AudienceAdapter().build_context(
        content=jd,
        audience=target_audience,
    )

    risk_score = metrics.evaluate(risk_ctx)
    print(f"JD risk context: {risk_score.overall:.0%}")

    risks = llm.invoke([
        SystemMessage(content=risk_ctx.assemble()),
        HumanMessage(content=(
            "Audit this job description for: "
            "(1) Over-specified requirements that exclude qualified candidates, "
            "(2) Gendered or exclusionary language, "
            "(3) Requirements that don't predict job success. "
            "List specific issues with suggested rewrites."
        )),
    ]).content

    improved_jd = llm.invoke([
        SystemMessage(content=audience_ctx.assemble()),
        HumanMessage(content=f"Rewrite this JD to better attract {target_audience} while removing the issues identified:\n\nIssues:\n{risks}\n\nOriginal:\n{jd}"),
    ]).content

    return {"risks": risks, "improved_jd": improved_jd}


def compare_candidates(candidates: list[dict], criteria: list[str], role: str) -> str:
    candidate_summaries = "\n\n".join(
        f"CANDIDATE {i+1}: {c['name']}\n{c['summary']}"
        for i, c in enumerate(candidates)
    )

    compare_ctx = ComparativeAnalyzer().build_context(
        decision=f"Select the best candidate for: {role}",
        context_section=f"Evaluation criteria: {', '.join(criteria)}\n\nCandidates:\n{candidate_summaries}",
    )
    score = metrics.evaluate(compare_ctx)
    print(f"Comparison context: {score.overall:.0%}")

    return llm.invoke([
        SystemMessage(content=compare_ctx.assemble()),
        HumanMessage(content=(
            f"Compare all candidates against each criterion. "
            f"Produce a comparison table, then a ranked recommendation with reasoning. "
            f"Flag any gaps or risks for each candidate."
        )),
    ]).content


# Stage 1: Audit and improve the JD
original_jd = """
We are looking for a rockstar Senior Python Developer to join our elite team.
Requirements: 
- 10+ years Python experience
- PhD preferred
- Must be available for last-minute sprint changes
- Experience with every major cloud provider (AWS, GCP, Azure)
- Must work well in a fast-paced, high-pressure environment
- Ability to work independently without much guidance
"""

audit = audit_job_description(
    original_jd,
    target_audience="senior Python engineers from diverse backgrounds",
    role_type="Senior Python Developer",
)
print("=== ISSUES FOUND ===")
print(audit["risks"][:500])
print("\n=== IMPROVED JD ===")
print(audit["improved_jd"][:600])

# Stage 2: Compare shortlisted candidates
candidates = [
    {
        "name": "Alex Chen",
        "summary": "7 years Python, AWS certified, open source contributor, no PhD, led 3-person team",
    },
    {
        "name": "Sarah Park",
        "summary": "12 years Python, PhD in CS, strong Django/FastAPI, limited cloud experience",
    },
    {
        "name": "Marcus Williams",
        "summary": "9 years Python, GCP certified, previous lead role, strong on distributed systems",
    },
]

comparison = compare_candidates(
    candidates,
    criteria=["Python expertise", "leadership", "cloud infrastructure", "communication", "growth potential"],
    role="Senior Python Developer — payments team",
)
print("\n=== CANDIDATE COMPARISON ===")
print(comparison)
```

## What You Get

**JD audit catches:**
- "Rockstar" and "elite" — gendered, exclusionary language
- "10+ years" — arbitrary number requirement with no evidence basis
- "PhD preferred" — credential inflation that excludes qualified candidates
- "Every major cloud provider" — over-specification; one platform is sufficient for the role

**Candidate comparison produces:**
- A structured table: each candidate scored on each criterion with specific evidence
- A ranked recommendation with reasoning
- Risk flags: gaps in each candidate's profile that need addressing
