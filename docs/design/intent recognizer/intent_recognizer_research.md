# IntentRecognizer Research: Academic Foundations & Experimental Findings

> **Status**: Research Complete  
> **Created**: 2026-02-25  
> **Scope**: `src/mycontext/templates/free/specialized/intent_recognizer.py`  
> **Experiments**: `docs/examples/intent_recognizer_baseline.py`, `docs/examples/intent_recognizer_enhanced.ipynb`

---

## 1. Research Question

Can we make intent recognition more robust by grounding it in established theories from philosophy, linguistics, and cognitive psychology? The industry standard is flat intent classification — "what does the user want?" We set out to test whether structured multi-layer analysis, enhanced with academic frameworks, produces deeper and more actionable intent recognition.

---

## 2. Theoretical Foundations

### 2.1 Speech Act Theory (Austin & Searle)

Every utterance has three layers, not one:

| Layer | What It Is | Example: "Can you pass the salt?" |
|-------|-----------|----------------------------------|
| **Locutionary** | What was literally said | A question about physical ability |
| **Illocutionary** | What was intended | A request to hand over the salt |
| **Perlocutionary** | What effect was desired | The listener actually passes the salt |

The gap between locutionary and illocutionary IS the hidden intent. "Do you have an enterprise plan?" — Locutionary: pricing question. Illocutionary: vendor maturity evaluation. Perlocutionary: build confidence to recommend internally.

**Key References:**
- Austin, J. L. (1962). *How to Do Things with Words*. Harvard University Press.
- Searle, J. R. (1969). *Speech Acts: An Essay in the Philosophy of Language*. Cambridge University Press.

### 2.2 Gricean Implicature (What's Implied by What's NOT Said)

Grice identified 4 conversational maxims people normally follow. When they violate one, they're implying something:

| Maxim | Norm | Violation Signals |
|-------|------|-------------------|
| **Quality** | Be truthful | Sarcasm, irony, understatement |
| **Quantity** | Say enough, not too much | Withholding info = discomfort; over-explaining = insecurity |
| **Relation** | Be relevant | Topic change = avoidance; tangent = the tangent IS the real topic |
| **Manner** | Be clear | Vagueness = uncertainty or face-saving; jargon = establishing authority |

Research indicates that explicitly prompting LLMs with Gricean theory improves implicature detection by up to 9.6%.

**Key References:**
- Grice, H. P. (1975). Logic and conversation. In *Syntax and Semantics* (Vol. 3, pp. 41-58). Academic Press.

### 2.3 Politeness Theory & Indirectness (Brown & Levinson)

People are indirect because the request threatens "face" (self-image). The degree of indirectness reveals the weight of what's being asked:

| Directness Level | Example | What It Signals |
|-----------------|---------|-----------------|
| Direct | "Fix this bug" | Low stakes, high authority |
| Conventionally indirect | "Could you look at this bug?" | Standard professional request |
| Highly indirect | "I was wondering if someone might have time to maybe glance at..." | High stakes, low power, or sensitive topic |
| Off-record | "This module has been a bit flaky lately..." | Too face-threatening to ask directly |

Heavy hedging = the person is asking for something they think is a big deal, even if it sounds small.

**Key References:**
- Brown, P., & Levinson, S. C. (1987). *Politeness: Some Universals in Language Usage*. Cambridge University Press.

### 2.4 Frame Semantics (Fillmore)

Words activate entire conceptual frames — networks of related concepts. Identifying which frame is active reveals what's really in play:

| Input | Frame Activated | Implied Concepts |
|-------|----------------|-----------------|
| "Cancel my subscription" | RETENTION, DISSATISFACTION | Alternatives being considered, trigger event, winback opportunity |
| "What's the best language to learn?" | CAREER_TRANSITION | Risk, income change, learning curve, timeline pressure |
| "Make the app faster" | BOTTLENECK, USER_FRUSTRATION | Specific workflow, lost productivity, competing tool |

**Key References:**
- Fillmore, C. J. (1982). Frame semantics. In *Linguistics in the Morning Calm* (pp. 111-137). Hanshin Publishing.

### 2.5 Conceptual Metaphor Theory (Lakoff & Johnson)

The metaphors people choose reveal how they experience the situation:

| Metaphor Used | Conceptualization | What It Reveals |
|--------------|-------------------|-----------------|
| "I'm **drowning** in work" | OVERWHELM IS SUBMERSION | Feels helpless, needs rescue not productivity tips |
| "I'm **stuck** on this problem" | PROGRESS IS MOVEMENT | Needs a push/unblocking, not a complete solution |
| "I'm **lost** in this codebase" | UNDERSTANDING IS NAVIGATION | Needs a map/orientation, not code reviews |
| "This project is **on fire**" | CRISIS IS FIRE | Needs immediate containment, not long-term planning |

**Key References:**
- Lakoff, G., & Johnson, M. (1980). *Metaphors We Live By*. University of Chicago Press.

### 2.6 Relevance Theory — Absence Analysis (Sperber & Wilson)

If someone mentions A and B but NOT C, and C is the obvious thing to mention, the absence is data:

- Customer asks about cancellation but doesn't mention a specific problem → the problem might be embarrassment (billing issue?) or a competitor they don't want to name
- Developer asks for production access but doesn't say what they're debugging → might be their own mistake

**Key References:**
- Sperber, D., & Wilson, D. (1986). *Relevance: Communication and Cognition*. Blackwell.

---

## 3. Gap Analysis: Current Template vs Academic Frameworks

| Analytical Dimension | Current Template | Academic Framework |
|---------------------|-----------------|-------------------|
| What was said | Surface Analysis (basic) | Speech Act Theory: locutionary act |
| What was intended | Goal Inference (common sense) | Speech Act Theory: illocutionary force |
| Desired effect on listener | Not covered | Speech Act Theory: perlocutionary act |
| Reading between the lines | Not covered | Gricean maxim violation analysis |
| What's conspicuously absent | Not covered | Relevance Theory: absence signals |
| Degree of indirectness | Not covered | Politeness Theory: face-saving, power dynamics |
| Conceptual frames activated | Not covered | Frame Semantics: domain mapping |
| Metaphor analysis | Not covered | Conceptual Metaphor Theory |
| Urgency / constraints | Motivation Analysis (basic) | Enhanced with escalation signal detection |
| Implicit assumptions | Implicit Assumptions (generic) | Enhanced with cognitive bias identification |

The current template covers **3 of 10 analytical dimensions** (partially). The academic literature offers 7 new dimensions that the industry doesn't use.

---

## 4. Experimental Design

### 4.1 Baseline Experiment (Phase 1)

Compared raw prompts vs the original IntentRecognizer template across 8 test cases spanning Customer Support, Product, Sales, Career, Engineering, Stakeholder Management, HR, and Internal Tools.

**Configuration:**
- Model: gpt-4o-mini
- Raw prompt: "Analyze the following user input and determine their intent."
- Template: IntentRecognizer with depth=comprehensive
- Judge: gpt-4o scoring on 5 dimensions (intent accuracy, depth, assumption detection, actionability, precision)

### 4.2 Enhanced Template Experiment (Phase 2)

After identifying gaps, we enhanced the IntentRecognizer with:

1. **Depth-aware directive selection** — quick (4 sections), standard (8 sections), comprehensive (12 sections) now produce genuinely different prompts
2. **4 new academic layers** for comprehensive depth:
   - Speech Act Analysis (locutionary/illocutionary/perlocutionary)
   - Conversational Implicature (Gricean maxim analysis)
   - Indirectness & Power Dynamics (Politeness Theory)
   - Frame & Absence Analysis (Frame Semantics + Relevance Theory)

### 4.3 Model Capacity Test (Phase 3)

Tested whether a more capable model (gpt-4o) could handle the 12-section comprehensive template better than gpt-4o-mini.

---

## 5. Results

### 5.1 Phase 1: Raw vs Template (Baseline)

| Metric | Raw Prompt | Template (comp.) | Delta |
|--------|-----------|-------------------|-------|
| **Avg Score** | **6.1** | **6.9** | **+0.8** |
| Intent Accuracy | 6.5 | 6.6 | +0.1 |
| Depth | 7.1 | 7.6 | +0.5 |
| Assumption Detection | 5.5 | 6.5 | +1.0 |
| **Actionability** | **4.8** | **7.4** | **+2.6** |
| Precision | 6.5 | 6.5 | 0.0 |
| Avg Tokens | ~430 | ~1,498 | 3.5x |
| Avg Cost | $0.0002 | $0.0006 | 3x |

**Key finding:** Actionability is the killer dimension. Raw prompts identify intent reasonably well but give vague "what to do about it" advice. The structured template forces concrete recommendations.

### 5.2 Depth Parameter (Before Fix)

Before the fix, depth had no effect — the model produced ~1,470 tokens regardless:

| Depth | Score | Tokens |
|-------|-------|--------|
| Quick | 6.8 | ~1,475 |
| Standard | 6.7 | ~1,464 |
| Comprehensive | 6.9 | ~1,498 |

All three depths used the same static directive template. The "depth" label was decorative.

### 5.3 Enhanced Template Results

After the fix, tokens genuinely scale:

| Approach | Score | Tokens | Cost |
|----------|-------|--------|------|
| Enhanced Quick (4 sections) | 6.1 | ~914 | $0.0003 |
| Enhanced Standard (8 sections) | **6.9** | ~1,527 | $0.0006 |
| Enhanced Comprehensive (12 sections, gpt-4o-mini) | 5.8 | ~2,522 | $0.0010 |
| Enhanced Comprehensive (12 sections, gpt-4o) | 6.1 | ~2,284 | $0.0138 |

### 5.4 Full Comparison Table

| Configuration | Avg Score | Tokens | Cost | Best Use |
|--------------|-----------|--------|------|----------|
| Raw prompt | 6.1 | ~430 | $0.0002 | Quick triage |
| Baseline template | 6.9 | ~1,498 | $0.0006 | — (superseded) |
| **Enhanced Quick** | **6.1** | **~914** | **$0.0003** | **Budget-conscious, high-volume** |
| **Enhanced Standard** | **6.9** | **~1,527** | **$0.0006** | **Default — best quality/cost ratio** |
| Enhanced Comprehensive (mini) | 5.8 | ~2,522 | $0.0010 | Not recommended for lightweight models |
| Enhanced Comprehensive (4o) | 6.1 | ~2,284 | $0.0138 | Diminishing returns even with capable model |

---

## 6. Key Findings

### Finding 1: Structure IS the Value — Not More Structure

The 8-section standard template (6.9/10) is the optimal structure. Adding 4 academic layers to reach 12 sections actually *reduces* quality to 5.8 on gpt-4o-mini and only 6.1 on gpt-4o. The model spreads itself thin across too many analytical dimensions, sacrificing depth-per-section for breadth.

### Finding 2: Actionability Is the Template's Killer Advantage

The single biggest dimension improvement is actionability (+2.6 points over raw). Raw prompts can identify intent reasonably well (6.5/10 intent accuracy), but they produce vague response strategies. The template's structured Recommendation section forces concrete, specific guidance.

### Finding 3: Depth Parameter Now Genuinely Differentiates

Before the fix: quick/standard/comprehensive all produced ~1,470 tokens (decorative label). After: quick=914, standard=1,527, comprehensive=2,522 tokens. This enables genuine cost/quality budgeting.

### Finding 4: Model Capacity Ceiling Is Real

gpt-4o-mini handles 8 structured sections well but buckles under 12. gpt-4o handles 12 sections without the same token issues, but the *quality* doesn't improve — suggesting the problem isn't model capacity but analytical diminishing returns. More sections ≠ deeper analysis when the analytical layers become redundant.

### Finding 5: The Academic Frameworks Are Theoretically Sound but Practically Redundant

Speech Act Analysis, Gricean Implicature, Politeness Theory, and Frame Semantics are rigorous analytical dimensions. However, a well-designed Goal Inference + Motivation Analysis + Implicit Assumptions trio already captures most of what these frameworks surface — just without the academic labels. The labeled frameworks add precision in theory but don't produce meaningfully different outputs in practice when evaluated by LLM-as-judge.

---

## 7. Design Recommendation

### Keep: Depth-Aware Template Architecture

The fix to make depth control which sections appear (not just a label) is a genuine improvement. Ship it:

| Depth | Sections | Use Case |
|-------|----------|----------|
| **quick** | Surface, Goals, Reformulated Intent, Recommendation | High-volume, cost-sensitive, triage |
| **standard** | + Motivation, Context, Assumptions, Needs (8 total) | Default for all production use |
| **comprehensive** | + Speech Acts, Implicature, Indirectness, Frames (12 total) | Research, forensic analysis, expert users |

### Default to Standard

Standard (8 sections) should be the default depth. It matches or beats the old comprehensive in quality while maintaining the same cost profile.

### Keep Comprehensive as an Expert Option

The 12-section comprehensive may not improve LLM-as-judge scores, but it produces analytically richer output that domain experts may value for its structured coverage of linguistic dimensions. It should remain available for users who want the academic depth, with clear documentation that it requires more tokens and may not improve raw scores.

---

## 8. Theories Considered but Not Implemented

The following theories were researched during brainstorming but not added to the template, either because they overlap with existing sections or because they require modality-specific input (e.g., voice tone) that text-based analysis cannot capture:

| Theory | What It Offers | Why Not Implemented |
|--------|---------------|-------------------|
| **Conceptual Metaphor Theory** (Lakoff) | Metaphor choice reveals emotional framing | Overlaps with Context Interpretation; requires longer text to have metaphors to analyze |
| **Discourse Analysis** (conversation patterns) | Deviations from expected responses signal meaning | Better suited to multi-turn dialogue, not single-message analysis |
| **Cognitive Bias Recognition** | Identifies anchoring, framing, confirmation bias | Partially covered by Implicit Assumptions section |
| **Prosodic Analysis** | Voice tone, stress, pitch patterns | Text-only template; not applicable |
| **Relevance Theory** (full) | Effort-to-relevance ratio signaling | Simplified into Absence Analysis within Frame section |

---

## 9. Experiment Artifacts

| File | Description |
|------|-------------|
| `docs/examples/intent_recognizer_baseline.py` | Phase 1: Raw vs template, 32 runs + 32 judge calls |
| `docs/examples/intent_recognizer_results.json` | Baseline scores and metadata |
| `docs/examples/intent_recognizer_full_outputs.json` | Baseline full text outputs |
| `docs/examples/intent_recognizer_enhanced.ipynb` | Phase 2+3: Enhanced template, depth comparison, gpt-4o test |
| `docs/examples/intent_recognizer_enhanced_results.json` | Enhanced scores (gpt-4o-mini) |
| `docs/examples/intent_recognizer_gpt4o_results.json` | Enhanced scores (gpt-4o) |

---

## 10. References

1. Austin, J. L. (1962). *How to Do Things with Words*. Harvard University Press.
2. Searle, J. R. (1969). *Speech Acts: An Essay in the Philosophy of Language*. Cambridge University Press.
3. Grice, H. P. (1975). Logic and conversation. In *Syntax and Semantics* (Vol. 3, pp. 41-58). Academic Press.
4. Brown, P., & Levinson, S. C. (1987). *Politeness: Some Universals in Language Usage*. Cambridge University Press.
5. Fillmore, C. J. (1982). Frame semantics. In *Linguistics in the Morning Calm* (pp. 111-137). Hanshin Publishing.
6. Lakoff, G., & Johnson, M. (1980). *Metaphors We Live By*. University of Chicago Press.
7. Sperber, D., & Wilson, D. (1986). *Relevance: Communication and Cognition*. Blackwell.
8. Jurafsky, D., & Martin, J. H. (2023). *Speech and Language Processing* (3rd ed.). Prentice Hall.
9. Premack, D., & Woodruff, G. (1978). Does the chimpanzee have a theory of mind? *Behavioral and Brain Sciences*, 1(4), 515-526.
10. Traum, D. R. (1999). Speech acts for dialogue agents. In *Foundations of Rational Agency* (pp. 169-201). Springer.
