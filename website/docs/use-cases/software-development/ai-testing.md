---
sidebar_position: 7
title: AI-Assisted Testing Strategy
description: Generate comprehensive test strategies using HypothesisGenerator + ErrorDetectionFramework + RiskAssessor. A CrewAI crew that writes test plans, edge cases, and security tests.
---

# AI-Assisted Testing Strategy

**Scenario:** Your team writes feature code but testing is an afterthought. Test coverage is inconsistent, edge cases are missed, and security testing never happens unless a pentest finds something. You want AI to generate thorough test strategies — covering unit, integration, edge case, and security angles — from the code or requirements alone.

**Patterns used:**
- `HypothesisGenerator` — generates hypotheses about what could go wrong (edge cases, failure modes)
- `ErrorDetectionFramework` (enterprise) — systematically identifies error conditions and failure states
- `RiskAssessor` — evaluates which scenarios pose the highest risk if untested
- `StepByStepReasoner` — builds a step-by-step test execution plan

**Integration:** CrewAI crew — test strategist, edge case analyst, and security tester working in parallel

---

```python
import mycontext
mycontext.activate_license("MC-ENT-YOUR-KEY")

from crewai import Agent, Task, Crew
from mycontext.templates.free.reasoning import HypothesisGenerator, StepByStepReasoner
from mycontext.templates.free.specialized import RiskAssessor
from mycontext.templates.enterprise.metacognition import ErrorDetectionFramework
from mycontext.intelligence import QualityMetrics

metrics = QualityMetrics(mode="heuristic")


def build_test_strategy(code: str, language: str, feature_description: str) -> dict:
    # Each agent gets a purpose-built context
    hypothesis_ctx = HypothesisGenerator().build_context(
        phenomenon=f"Testing {feature_description}",
        domain="software quality assurance",
    )
    error_ctx = ErrorDetectionFramework().build_context(
        process=f"{language} function:\n\n{code}",
        context_section=f"Feature: {feature_description}",
    )
    risk_ctx = RiskAssessor().build_context(
        decision=f"Ship {feature_description} without testing X, Y, or Z",
        depth="comprehensive",
    )
    plan_ctx = StepByStepReasoner().build_context(
        problem=f"Design a complete test plan for: {feature_description}",
    )

    # Score contexts
    for name, ctx in [
        ("hypothesis", hypothesis_ctx), ("error", error_ctx),
        ("risk", risk_ctx), ("plan", plan_ctx)
    ]:
        score = metrics.evaluate(ctx)
        print(f"  {name}: {score.overall:.0%}")

    llm_config = {"provider": "openai", "model": "gpt-4o-mini"}

    edge_case_agent = Agent(
        role="Edge Case Analyst",
        goal="Identify every non-obvious input, boundary, and failure scenario",
        backstory=hypothesis_ctx.assemble(),
        verbose=False,
    )
    error_agent = Agent(
        role="Error Detection Specialist",
        goal="Find all failure states, error conditions, and exception paths",
        backstory=error_ctx.assemble(),
        verbose=False,
    )
    security_agent = Agent(
        role="Security Tester",
        goal="Identify what security scenarios must be tested — injection, auth bypass, etc.",
        backstory=risk_ctx.assemble(),
        verbose=False,
    )
    planner_agent = Agent(
        role="Test Plan Writer",
        goal="Synthesize all findings into a structured, prioritized test plan",
        backstory=plan_ctx.assemble(),
        verbose=False,
    )

    edge_task = Task(
        description=f"Generate 10+ edge cases for:\n\n```{language}\n{code}\n```",
        expected_output="Numbered list of edge cases with input/expected output",
        agent=edge_case_agent,
    )
    error_task = Task(
        description=f"List all error states and failure modes in this code:\n\n```{language}\n{code}\n```",
        expected_output="Error conditions with trigger scenarios",
        agent=error_agent,
    )
    security_task = Task(
        description=f"What security scenarios must be tested for: {feature_description}",
        expected_output="Security test cases with attack vectors",
        agent=security_agent,
    )
    plan_task = Task(
        description="Using the edge cases, error states, and security findings — write a complete test plan",
        expected_output="Structured test plan: unit tests, integration tests, edge cases, security tests, priority order",
        agent=planner_agent,
        context=[edge_task, error_task, security_task],
    )

    crew = Crew(
        agents=[edge_case_agent, error_agent, security_agent, planner_agent],
        tasks=[edge_task, error_task, security_task, plan_task],
        verbose=False,
    )

    return crew.kickoff()


# Test a payment processing function
code = """
def process_payment(amount: float, card_token: str, currency: str = "USD") -> dict:
    if amount <= 0:
        raise ValueError("Amount must be positive")
    charge = stripe.charge.create(amount=int(amount * 100), currency=currency, source=card_token)
    return {"charge_id": charge.id, "status": charge.status}
"""

result = build_test_strategy(
    code=code,
    language="Python",
    feature_description="Stripe payment processing with currency support",
)
print(result)
```

## What Gets Tested That You'd Miss Manually

The four-agent approach covers angles a single prompt misses:

| Agent | What it finds |
|-------|--------------|
| Edge Case Analyst | `amount=0.001`, empty string tokens, currency codes that don't exist, integer overflow on `int(amount * 100)` |
| Error Detection | Network timeout mid-charge, Stripe API rate limits, partial charge states, DB write failure after successful charge |
| Security Tester | Token replay attacks, currency injection, negative amount bypass, race conditions in concurrent charges |
| Test Planner | Integrates all findings, assigns priority, suggests which to automate vs. manual |

## Bonus: Auto-Generate Pytest Stubs

```python
from mycontext import Context
from mycontext.foundation import Directive, Guidance

stub_ctx = Context(
    guidance=Guidance(
        role="Senior Python test engineer",
        rules=["Write pytest", "Use pytest.mark.parametrize for edge cases", "Mock external calls with pytest-mock"],
    ),
    directive=Directive(content=f"Convert this test plan to pytest stubs:\n\n{result}"),
)
stubs = stub_ctx.execute(provider="openai").response
print(stubs)
```
