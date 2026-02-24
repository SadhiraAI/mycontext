---
sidebar_position: 2
title: AI-Powered PR Review Pipeline
description: Automate pull request reviews using a three-stage LangChain LCEL chain — code quality, security risk, and performance bottleneck analysis in one pipeline.
---

# AI-Powered PR Review Pipeline

**Scenario:** Your team reviews dozens of PRs a day. Reviews are inconsistent — different engineers catch different things, tone varies, and security issues slip through. You want every PR to get the same rigorous, structured review before a human even looks at it.

**Patterns used:**
- `CodeReviewer` — severity-ranked code quality and maintainability analysis
- `RiskAssessor` — security vulnerability scanning with OWASP context
- `BottleneckIdentifier` (enterprise) — spots performance bottlenecks and inefficient patterns

**Integration:** LangChain LCEL chain with structured JSON output

---

```python
import mycontext
mycontext.activate_license("MC-ENT-YOUR-KEY")

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser

from mycontext.templates.free.specialized import CodeReviewer, RiskAssessor
from mycontext.templates.enterprise.problem_solving import BottleneckIdentifier
from mycontext.intelligence import QualityMetrics
from mycontext.utils.parsers import JSONParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = JSONParser(strict=False)
metrics = QualityMetrics(mode="heuristic")


def build_review_chain(diff: str, language: str):
    # Stage 1: Code quality review
    code_ctx = CodeReviewer().build_context(
        code=diff,
        language=language,
        focus="maintainability, readability, correctness",
    )
    
    # Stage 2: Security risk
    risk_ctx = RiskAssessor().build_context(
        decision=f"Merge this {language} code change:\n\n{diff}",
        depth="comprehensive",
    )
    
    # Stage 3: Performance bottlenecks
    perf_ctx = BottleneckIdentifier().build_context(
        system=f"{language} codebase",
        process=diff,
    )
    
    # Score all three before spending tokens
    for name, ctx in [("code", code_ctx), ("risk", risk_ctx), ("perf", perf_ctx)]:
        score = metrics.evaluate(ctx)
        if score.overall < 0.60:
            print(f"  Warning: {name} context quality low ({score.overall:.0%})")
    
    return code_ctx, risk_ctx, perf_ctx


def review_pr(diff: str, language: str = "Python") -> dict:
    code_ctx, risk_ctx, perf_ctx = build_review_chain(diff, language)
    
    def run(ctx, question):
        return llm.invoke([
            SystemMessage(content=ctx.assemble()),
            HumanMessage(content=question),
        ]).content

    code_review = run(code_ctx, "Review this code. Respond with JSON: {\"issues\": [], \"severity\": \"low|medium|high\", \"approved\": true|false}")
    security_review = run(risk_ctx, "Identify security risks. Respond with JSON: {\"risks\": [], \"owasp_categories\": [], \"block_merge\": true|false}")
    perf_review = run(perf_ctx, "Find performance issues. Respond with JSON: {\"bottlenecks\": [], \"severity\": \"low|medium|high\"}")
    
    code = parser.parse(code_review) or {}
    security = parser.parse(security_review) or {}
    perf = parser.parse(perf_review) or {}
    
    block = security.get("block_merge", False) or code.get("severity") == "high"
    
    return {
        "approved": not block,
        "code_review": code,
        "security": security,
        "performance": perf,
        "summary": f"{'BLOCKED' if block else 'APPROVED'} — "
                   f"{len(code.get('issues', []))} code issues, "
                   f"{len(security.get('risks', []))} security risks",
    }


# Use in CI
pr_diff = """
-def get_user(id):
-    query = f"SELECT * FROM users WHERE id = {id}"
+def get_user(user_id: int):
+    query = "SELECT * FROM users WHERE id = %s"
     return db.execute(query, [id])
"""

result = review_pr(pr_diff, "Python")
print(result["summary"])

if not result["approved"]:
    for risk in result["security"].get("risks", []):
        print(f"  SECURITY: {risk}")
    exit(1)
```

## What You Get

The pipeline catches three distinct categories of problem that a single-pass review misses:

- **Code quality:** naming, structure, test coverage, complexity
- **Security:** SQL injection, CSRF, auth flaws, OWASP Top 10 violations
- **Performance:** N+1 queries, blocking I/O, inefficient data structures

Each stage uses its own cognitive framework — not just different prompts, but different analytical methodologies. The code reviewer thinks like a senior engineer; the risk assessor thinks like a penetration tester; the bottleneck identifier thinks like a performance engineer.

## CI/CD Integration

Add to `.github/workflows/pr-review.yml`:

```yaml
- name: AI PR Review
  run: python scripts/pr_review.py ${{ github.event.pull_request.number }}
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
    MYCONTEXT_LICENSE_KEY: ${{ secrets.MYCONTEXT_LICENSE_KEY }}
```
