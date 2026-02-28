# IntentRecognizer Use-Case Patternization — Brainstorm

**Goal**: Add an `intent` parameter (like DataAnalyzer) so IntentRecognizer can be tuned per use case. Each intent maps to a subset of sections — no need for full linguistic analysis when triaging a support ticket.

---

## Current State

- **depth**: `quick` (4 sections) | `standard` (8) | `comprehensive` (12)
- depth = *how many* sections, not *which* sections
- All use cases get the same section mix; only depth varies

## Proposed: intent + depth

| Parameter | Role | Values |
|-----------|------|--------|
| **intent** | *Which* sections (use-case fit) | triage, support, sales, feedback, stakeholder, product, comprehensive |
| **depth** | *How much* (token budget, verbosity) | quick, standard, thorough |

---

## Section Inventory (IntentRecognizer)

| ID | Section | Best for |
|----|---------|----------|
| surface | Surface Analysis | All — literal ask, key terms |
| goals | Goal Inference | All — immediate, underlying, long-term |
| motivation | Motivation Analysis | Support, sales, feedback |
| context | Context Interpretation | Support, sales, stakeholder |
| assumptions | Implicit Assumptions | Sales, feedback, stakeholder |
| needs | Need Classification | Triage, support, product |
| speech_acts | Speech Act Analysis | Stakeholder, legal, comprehensive |
| implicature | Conversational Implicature | Stakeholder, feedback, comprehensive |
| indirectness | Indirectness & Power Dynamics | Stakeholder, HR, comprehensive |
| frames | Frame & Absence Analysis | Product, comprehensive |
| reformulated | Reformulated Intent | All |
| recommendation | Recommendation | All |

---

## Use-Case → Section Mapping (Brainstorm)

### 1. **triage** — Fast routing (support tickets, chatbot)
*"What bucket does this go in?"*

| Sections | Rationale |
|----------|------------|
| surface, goals, needs, reformulated, recommendation | Minimal set for routing. Skip motivation, context, power dynamics. |

### 2. **support** — Customer support / help desk
*"What do they really need and how urgent?"*

| Sections | Rationale |
|----------|------------|
| surface, goals, motivation, context, needs, reformulated, recommendation | Pain points, urgency, stakeholders. Skip speech acts, implicature. |

### 3. **sales** — Deal qualification, discovery
*"Are they buying? What's driving them?"*

| Sections | Rationale |
|----------|------------|
| surface, goals, motivation, context, assumptions, reformulated, recommendation | Buying intent, pain, constraints, unstated beliefs. Skip linguistic theory. |

### 4. **feedback** — Survey / NPS / feedback analysis
*"What are they really saying?"*

| Sections | Rationale |
|----------|------------|
| surface, goals, motivation, assumptions, needs, reformulated, recommendation | Pain points, implicit beliefs, what they want. Often anonymous → skip power dynamics. |

### 5. **stakeholder** — Executive / political / cross-team
*"What do they want and what can't they say directly?"*

| Sections | Rationale |
|----------|------------|
| goals, motivation, context, assumptions, indirectness, speech_acts, implicature, reformulated, recommendation | Power dynamics, face-saving, what's NOT said. Core use case for Gricean + politeness. |

### 6. **product** — Feature requests, product feedback
*"What problem are they trying to solve?"*

| Sections | Rationale |
|----------|------------|
| surface, goals, motivation, needs, frames, reformulated, recommendation | Underlying problem vs stated want. Frame analysis helps (e.g. "faster" → bottleneck frame). |

### 7. **comprehensive** — Research, legal, full analysis
*"Everything."*

| Sections | Rationale |
|----------|------------|
| All 12 | Original behaviour. Linguistic rigor. |

---

## depth (Investment) — Unchanged Concept

| depth | Constraint | Token hint |
|-------|------------|------------|
| quick | Be concise. Max 3 key insights. | 800 |
| standard | Default | 1500 |
| thorough | Full evidence, detailed reasoning | 3000 |

---

## API Sketch (DataAnalyzer-style)

```python
recognizer = IntentRecognizer()

# Triage a support ticket
ctx = recognizer.build_context(
    input="I've been charged twice and the app keeps crashing",
    intent="triage",
    depth="quick",
)

# Stakeholder request (power dynamics matter)
ctx = recognizer.build_context(
    input="Would it be possible to maybe revisit the timeline?",
    context="From VP Engineering to PM",
    intent="stakeholder",
    depth="standard",
)

# Full linguistic analysis
ctx = recognizer.build_context(
    input="What's the best way to learn Python?",
    intent="comprehensive",
    depth="thorough",
)
```

---

## Open Questions

1. **Overlap with depth**: Today depth = quick/standard/comprehensive controls section count. With intent, depth could mean *verbosity* only (like DataAnalyzer's investment). Agree?
2. **Naming**: `triage` vs `routing`? `feedback` vs `survey`?
3. **HR / employee**: Separate intent or fold into `stakeholder`? (Power dynamics + indirectness apply.)
4. **Legal / compliance**: New intent or `comprehensive`?
5. **Backward compatibility**: `intent="comprehensive"` + `depth="comprehensive"` = current behaviour?

---

## Next Steps

1. Review and refine section mapping per use case
2. Implement `_INTENT_SECTIONS` dict in `intent_recognizer.py`
3. Add `intent` param to `build_context` / `execute`
4. Add `_build_intent_directive()` helper (mirror DataAnalyzer)
5. Update tests and docs
