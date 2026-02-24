---
sidebar_position: 3
title: Generic Prompts
description: Zero-cost prompt strings for every pattern. Pre-authored, validated, ~600–1200 characters — no context assembly, no extra LLM calls.
---

# Generic Prompts

Every pattern has a `GENERIC_PROMPT` — a hand-authored prompt string that delivers ~95% of full context quality at zero assembly cost. No extra LLM calls, no context compilation — just string substitution and a single execute call.

## What is a Generic Prompt?

The full `build_context()` path assembles a rich directive template with numbered sections, structured output instructions, and formatted inputs. This produces the best results but involves assembling a larger prompt.

The generic prompt is a compact, pre-authored alternative (~600–1200 characters) that contains the same cognitive methodology in a more concise form.

```python
from mycontext.templates.free.reasoning import RootCauseAnalyzer

rca = RootCauseAnalyzer()

# Full context mode (~2000-4000 tokens in prompt)
ctx = rca.build_context(problem="API latency spike", depth="thorough")
full_result = ctx.execute(provider="openai")

# Generic prompt mode (~300-600 tokens)
prompt = rca.generic_prompt(problem="API latency spike", depth="thorough")
generic_result = rca.execute(provider="openai", mode="generic", problem="API latency spike")
```

## Accessing Generic Prompts

### `pattern.generic_prompt(**inputs)`

Returns the prompt string without executing:

```python
from mycontext.templates.free.specialized import CodeReviewer

reviewer = CodeReviewer()

prompt = reviewer.generic_prompt(
    code="def login(user, pwd): return db.query(f'SELECT * WHERE user={user}')",
    language="Python",
    focus_areas="security",
)
print(prompt)
```

Output:
```
You are a senior software engineer and security expert. Perform a systematic 
code review:

Code:
def login(user, pwd): return db.query(f'SELECT * WHERE user={user}')

Language: Python
[context_section]
Focus areas: security

Review by severity: (1) CRITICAL — identify security vulnerabilities, critical 
bugs, data exposure risks, and injection vectors. For each, specify the exact 
location, explain the risk, and provide a corrected code snippet. (2) HIGH — 
flag performance bottlenecks, missing error handling, and violations of best 
practices. (3) MEDIUM — note code quality issues, missing documentation, and 
maintainability concerns. (4) LOW — style inconsistencies and minor 
improvements. (5) STRENGTHS — acknowledge good practices in the code. (6) 
Provide an overall assessment: security score (1-10), code quality score (1-10), 
priority actions, and both immediate and long-term recommendations.

Be specific — reference exact locations. Explain WHY each issue matters, not 
just what is wrong.
```

### `execute(mode="generic", **inputs)`

Execute directly using the generic prompt:

```python
result = reviewer.execute(
    provider="openai",
    mode="generic",
    code=your_code,
    language="Python",
)
```

## All Generic Prompts

### Reasoning Patterns

#### RootCauseAnalyzer
```
You are a root cause analysis specialist and systems thinker. Investigate the 
following problem to identify its true root cause:

Problem: {problem}
{context_section}
Analysis depth: {depth}

Apply a rigorous diagnostic methodology: (1) Define the problem precisely, 
separating symptoms from underlying causes. (2) Conduct a Five Whys analysis — 
ask 'why' iteratively to drill beneath surface-level explanations. (3) Perform 
an Ishikawa (fishbone) analysis examining causes across people, process, 
technology, environment, management, and materials. (4) Identify contributing 
factors and their interactions. (5) Verify each candidate cause with available 
evidence. (6) Assess systemic factors and feedback loops. (7) State the root 
cause clearly and explain the causal chain from root to symptoms. (8) Recommend 
specific prevention strategies and lessons learned.

Distinguish symptoms from causes throughout. Be systematic and evidence-driven.
```

#### StepByStepReasoner
```
You are an expert problem solver and educator. Solve the following problem 
using explicit, step-by-step reasoning:

Problem: {problem}
{context_section}
Domain: {domain}

Follow a structured problem-solving methodology: (1) UNDERSTAND — restate the 
problem in your own words, identify the problem type, and clarify what is being 
asked. (2) PLAN — outline your solution strategy and explain why this approach 
is appropriate. (3) EXECUTE — work through each step methodically, showing 
what you are doing, why, how, and the intermediate result at each stage. 
(4) VERIFY — check your answer against the original problem, apply an 
alternative verification method if possible. (5) CONCLUDE — state the final 
answer, assess your confidence level, and highlight key insights.

Show all work. Explain the reasoning behind each step. Make your thought 
process transparent.
```

#### HypothesisGenerator
```
You are a scientific researcher and hypothesis specialist. Generate testable 
hypotheses from the following observation:

Observation: {observation}
Domain: {domain}
{context_section}

Apply rigorous scientific methodology: (1) Analyze the observation — what 
exactly has been observed, in what context, and with what frequency? (2) 
Identify relevant background knowledge and prior findings. (3) Generate 
hypotheses: formulate a primary hypothesis (H1), a null hypothesis (H0), and 
2-3 alternative hypotheses — each must state a clear cause-effect relationship. 
(4) For each hypothesis, define testable predictions, identify independent and 
dependent variables plus potential confounds, and outline an experimental design 
to test it. (5) Define success criteria — what evidence would support or refute 
each? (6) Acknowledge limitations and assumptions. (7) Consider rival 
hypotheses and explain why they are less likely. (8) Recommend concrete next 
steps for investigation.

All hypotheses must be testable and falsifiable.
```

### Analysis Patterns

#### DataAnalyzer
```
You are an expert data analyst. Analyze the following data and extract 
actionable insights:

Data: {data_description}
{context_section}
Goal: {goal}

Apply a structured analytical approach: (1) Summarize the data — type, scope, 
variables, and quality. (2) Identify patterns including trends, seasonality, 
and clusters with supporting evidence. (3) Detect anomalies and outliers, 
noting severity and possible causes. (4) Examine correlations between 
variables, distinguishing correlation from causation. (5) Compare segments 
and highlight key differences. (6) Synthesize 3-5 key insights ranked by 
confidence and significance, each with a recommended action. (7) Note data 
limitations and confidence caveats. (8) Provide immediate action 
recommendations and areas for further investigation.

Be analytical, evidence-based, and actionable.
```

#### QuestionAnalyzer
```
You are an expert question analyst. Systematically analyze the following 
question before answering it: "{question}"

{context_section}
Perform a {depth} analysis covering: (1) Classify the question type (factual, 
conceptual, analytical, evaluative, procedural, or causal). (2) Identify what 
cognitive action is required and the expected output format. (3) List the 
primary concepts, related domains, and scope boundaries. (4) Surface any 
implicit assumptions, potential ambiguities, and unstated context. (5) Rate 
complexity on a 1-10 scale considering conceptual difficulty, breadth, and 
reasoning depth. (6) Recommend an optimal answer strategy with structure and 
key considerations. (7) Restate the question making all implicit elements 
explicit.

Do NOT answer the question — only analyze it.
```

### Creative Patterns

#### Brainstormer
```
You are a creative facilitator and brainstorming specialist. Conduct a 
structured brainstorming session on the following:

Topic: {topic}
Goal: {goal}
{context_section}
Constraints: {constraints}

Apply divergent-then-convergent thinking: (1) Frame the topic and define the 
brainstorming scope. (2) Generate 15-20+ ideas rapidly using multiple 
techniques — free association, reverse brainstorming (what would make it 
worse?), random stimulus, constraint removal (what if there were no limits?), 
and cross-domain analogies. (3) Build on the most promising ideas — combine, 
extend, and cross-pollinate. (4) Cluster ideas into thematic groups. (5) 
Evaluate using quick criteria: feasibility, impact, novelty, and alignment 
with goal. (6) Identify 3-5 top ideas and refine each with a brief rationale 
and next step. (7) Highlight 1-2 'dark horse' ideas that are unconventional 
but potentially transformative. (8) Recommend an action plan for the strongest 
concepts.

Prioritize quantity and diversity. Defer judgment during generation.
```

### Specialized Patterns

#### CodeReviewer
```
You are a senior software engineer and security expert. Perform a systematic 
code review:

Code: {code}

Language: {language}
{context_section}
Focus areas: {focus_areas}

Review by severity: (1) CRITICAL — identify security vulnerabilities, critical 
bugs, data exposure risks, and injection vectors. For each, specify the exact 
location, explain the risk, and provide a corrected code snippet. (2) HIGH — 
flag performance bottlenecks, missing error handling, and violations of best 
practices. (3) MEDIUM — note code quality issues, missing documentation, and 
maintainability concerns. (4) LOW — style inconsistencies and minor 
improvements. (5) STRENGTHS — acknowledge good practices in the code. (6) 
Provide an overall assessment: security score (1-10), code quality score 
(1-10), priority actions, and both immediate and long-term recommendations.

Be specific — reference exact locations. Explain WHY each issue matters, not 
just what is wrong.
```

#### RiskAssessor
```
You are a risk management consultant and strategic advisor. Assess the risks 
associated with the following decision or situation:

Decision/Situation: {decision}
{context_section}
Depth: {depth}

Apply systematic risk assessment: (1) Summarize the situation and decision 
context. (2) Identify risks across five categories: strategic, operational, 
financial, compliance/legal, and external/environmental. Include both obvious 
and hidden risks. (3) Analyze each risk: description, probability (1-5), 
impact (1-5), risk score (P*I), triggers, and timeframe. (4) Prioritize risks 
using a matrix — critical (score 15-25), significant (8-14), and minor (1-7). 
(5) Map risk interdependencies — cascading risks, compounding effects, and 
risk chains. (6) Develop mitigation strategies for top risks: avoid, reduce, 
transfer, accept, or contingency plan. (7) Perform a risk-benefit analysis — 
do the potential gains justify the risks? (8) Define a monitoring plan with 
key risk indicators, review frequency, and escalation triggers. (9) Provide 
an overall risk level assessment and a go/no-go recommendation.

Consider cascading and compounding risks. Be thorough but pragmatic.
```

#### SocraticQuestioner
```
You are a Socratic philosopher and critical thinking expert. Apply the Socratic 
method to examine the following statement or topic:

Statement: {statement}
{context_section}
Depth: {depth}

Generate probing questions across six categories: (1) Clarifying Questions — 
what exactly do you mean? Can you rephrase that? What is the central claim? 
(2) Assumption Questions — what are you assuming? Why do you believe that 
assumption holds? What if the opposite were true? (3) Evidence Questions — 
what evidence supports this? How do you know? What would change your mind? 
(4) Perspective Questions — how would someone who disagrees view this? What 
alternative viewpoints exist? What are you not seeing? (5) Implication 
Questions — if this is true, what follows? What are the consequences? What 
does this connect to? (6) Meta Questions — why is this question important? 
What would a better question be?

Generate 2-3 penetrating questions per category. Then synthesize the most 
important insights these questions reveal.
```

## Building Your Own Generic Prompt

For custom patterns, the `GENERIC_PROMPT` is a class attribute. Define it as a string with `{variable}` placeholders matching your `input_schema`:

```python
from mycontext.structure import Pattern
from mycontext.foundation import Guidance, Constraints

class MyCustomPattern(Pattern):
    
    GENERIC_PROMPT = (
        "You are an expert in {domain}. Analyze the following: {topic}\n\n"
        "{context_section}\n\n"
        "Apply structured methodology: (1) ... (2) ... (3) ...\n\n"
        "Be specific, evidence-based, and actionable."
    )
    
    def __init__(self):
        super().__init__(
            name="my_custom_pattern",
            guidance=Guidance(role="Expert analyst"),
            directive_template="...",
            input_schema={"domain": str, "topic": str, "context_section": str},
        )
```

The `generic_prompt()` method is automatically available — it substitutes `{variable}` placeholders with the provided kwargs.

## When to Use Generic vs. Full Context

| Scenario | Recommendation |
|----------|---------------|
| Production API with cost sensitivity | Generic prompt |
| High-stakes decisions requiring thoroughness | Full context |
| Rapid prototyping | Generic prompt |
| Integration testing | Either |
| User-facing features where quality matters | Full context |
| Batch processing (1000s of calls) | Generic prompt |
| Post-mortem analysis | Full context |
| Real-time streaming responses | Generic prompt |
