# The Science Behind Our Prompt Flow

**A Research-Backed Framework for Structuring LLM Prompts**

*This document explains why mycontext's Context Studio assembles prompts in a specific order, grounded in peer-reviewed research and industry best practices.*

---

## The Problem: Order Matters More Than You Think

Most prompt builders treat prompt sections as interchangeable blocks. But research shows that **where you place information in a prompt dramatically affects how well the AI follows it** — sometimes by margins of 76 accuracy points between formats (Sclar et al., ICLR 2024).

The question isn't just *what* to tell the AI — it's **in what order**.

---

## The Research Foundation

### 1. The "Lost in the Middle" Effect

**Paper:** Liu et al. (2023). *"Lost in the Middle: How Language Models Use Long Contexts."* TACL 2024.

LLMs exhibit a U-shaped attention curve: they recall information best from the **beginning** (primacy bias) and **end** (recency bias) of prompts, but struggle with content in the middle. This was observed across GPT-3.5-Turbo, Claude-1.3, MPT-30B, and LongChat-13B on both question answering and key-value retrieval tasks.

**Implication for our flow:** Place the most critical identity and objective information at the very beginning (ROLE, GOAL), and the actionable task at the very end (TASK). Middle sections contain supporting — but reinforcing — material.

### 2. Primacy Bias Dominates

**Paper:** Wang et al. (2025). *"Serial Position Effects of Large Language Models."*

Across GPT, Llama 2, and T5 models, primacy bias (preference for early information) is consistently stronger than recency bias. Placing demonstrations at the start yields up to **+6 accuracy points** compared to other positions.

**Implication:** ROLE and GOAL go first. Always. The AI's identity and mission are the foundation everything else builds on.

### 3. Task Placement: Instructions After Context

**Paper:** Li et al. (2023). *"Instruction Position Matters in Sequence Generation with Large Language Models."*

Placing task instructions **after** supporting context (rather than before) improves instruction-following by up to **+9.7 BLEU points** on zero-shot tasks and doubles instruction adherence. This "post-instruction" approach works because the AI reads all context before encountering what to do with it.

**Implication:** The TASK (the actual instruction with variables filled in) is **always the last section**. The AI reads role, rules, examples, constraints, and output format before seeing the task — just like a well-briefed employee.

### 4. Constraint Ordering: Hard Before Easy

**Paper:** Zhang et al. (2025). *"Hard-to-Easy Constraint Ordering."*

LLMs perform better when constraints are ordered from **hardest (most restrictive) to easiest**. This generalizes across model architectures and sizes.

**Implication:** In the GUARD RAILS section, "Must NOT include" (hard prohibitions) appears before "Must include" (softer requirements) and "Format rules" (least restrictive).

### 5. Emphasis Markers Work

**Paper:** Zhang et al. (ICLR 2024). *"PASTA: Post-hoc Attention Steering Approach."*
**Paper:** Zhu et al. (ICLR 2024). *"GUIDE: Guided Understanding with Instruction-Driven Enhancements."*

PASTA showed that emphasis markers (analogous to bold/italics) achieve **+22% average accuracy** by steering attention heads. GUIDE demonstrated that tagged emphasis improved instruction-following from **29.4% to 60.4%**, outperforming even supervised fine-tuning.

**Implication:** We use `**bold**` markers, `## CAPS HEADERS`, and `---` separators throughout the assembled prompt. These aren't decoration — they mechanistically increase attention to critical instructions.

### 6. Structured Prompting Reduces Variance

**Paper:** Zheng et al. (2025). *"Structured Prompting Enables More Robust Evaluation."*

Structured prompting methods reduce underestimation of model performance by ~4% and decrease variance across benchmarks. Models become less sensitive to prompt phrasing when structure is consistent.

**Implication:** Every prompt from Context Studio follows the same section order. This isn't just clean — it's statistically more reliable.

### 7. The CO-STAR Framework

**Source:** Government Technology Agency of Singapore (2023). Winner of the inaugural GPT-4 Prompt Engineering Competition.

The CO-STAR framework structures prompts as: **Context → Objective → Style → Tone → Audience → Response**. The key insight is that context and objective come first, followed by style modifiers, and the response format specification comes last (closest to where the AI generates output).

**Implication:** Our flow parallels CO-STAR: ROLE+GOAL (Context+Objective) → RULES+STYLE (Style+Tone) → OUTPUT FORMAT (Response) → TASK.

### 8. OpenAI and Anthropic Official Guidance

**OpenAI Prompt Engineering Guide:** "Put instructions at the beginning of the prompt and use ### or """ to separate the instruction and context." Also: "Use capitalized text for emphasis."

**Anthropic Claude Prompt Engineering Guide:** Structure prompts with clear XML-tagged sections. Place role setting first, followed by context, then instructions, then examples.

---

## Our Prompt Flow: The Evidence Map

```
┌─────────────────────────────────────────────────────────────────┐
│  PRIMACY ZONE  (strongest recall — Liu et al. 2023)            │
│  ① ROLE        — who the AI is         ← Identity anchoring    │
│  ② GOAL        — what success looks like ← Objective clarity   │
├─────────────────────────────────────────────────────────────────┤
│  EARLY INSTRUCTIONS  (OpenAI: "instructions at the beginning") │
│  ③ RULES       — behavioral constraints ← Hard→Easy ordering   │
│  ④ STYLE       — communication tone     ← CO-STAR style slot   │
├─────────────────────────────────────────────────────────────────┤
│  MIDDLE  (demos stabilise here — Wang et al. 2025, +6 pts)     │
│  ⑤ REASONING   — thinking strategy      ← CoT/ToT injection   │
│  ⑥ EXAMPLES    — few-shot demos         ← Start-placed demos   │
├─────────────────────────────────────────────────────────────────┤
│  LATE  (output spec close to the ask — CO-STAR Response slot)  │
│  ⑦ OUTPUT FORMAT — structured schema    ← Shape before asking  │
│  ⑧ GUARD RAILS — must/must-not/format   ← Constraints recap    │
├─────────────────────────────────────────────────────────────────┤
│  RECENCY ZONE  (up to +9.7 BLEU — Li et al. 2023)             │
│  ⑨ TASK        — the actual instruction ← ALWAYS LAST          │
└─────────────────────────────────────────────────────────────────┘
```

### Why This Order Specifically

| Position | What goes here | Why |
|----------|---------------|-----|
| **First** | ROLE + GOAL | Primacy bias ensures the AI *becomes* this persona. The goal frames everything that follows. (Liu et al. 2023, Wang et al. 2025) |
| **Early** | RULES + STYLE | Instructions at the top get followed more reliably. (OpenAI Guide, Anthropic Guide) |
| **Middle** | REASONING + EXAMPLES | Few-shot demos placed early are more stable (+6 pts). Reasoning strategy primes the approach before examples demonstrate it. (Wang et al. 2025) |
| **Late** | OUTPUT FORMAT + GUARD RAILS | The shape of the answer and its constraints are fresh in memory when the AI starts generating. (CO-STAR Response slot, Zhang et al. 2025) |
| **Last** | TASK | Post-instruction placement: the AI reads all setup before the actual ask. Up to +9.7 BLEU improvement. (Li et al. 2023) |

### Why Bold, Caps, and Separators

Every section header uses `## CAPS` and key phrases use `**bold**`:
- PASTA (ICLR 2024): Emphasis markers → +22% accuracy
- GUIDE (ICLR 2024): Tagged emphasis → 29.4% to 60.4% instruction compliance
- OpenAI Guide: "Use capitalized text for emphasis"
- The `---` separator before TASK creates a visual and semantic break, signaling "everything above is setup, everything below is the actual work."

---

## Example: What Gets Assembled

Given a Sentiment Analyzer built in Context Studio, the assembled prompt looks like:

```
## ROLE

**You are Expert Sentiment Analyst and NLP Specialist.**

## GOAL

**Objective:** Analyze text for emotional tone, providing structured sentiment
classification with confidence scores and actionable recommendations.

## RULES

**You MUST follow these rules at all times:**
  1. Base all judgments on textual evidence, not assumptions
  2. Always provide a confidence score between 0.0 and 1.0
  3. Flag ambiguous or mixed-sentiment text for human review
  4. Include specific quotes from the text to support your analysis

## STYLE

**Tone & voice:** Precise, evidence-based, professional but accessible

## REASONING APPROACH (Chain of Thought)

**Important — Think through this step by step. Break the problem down into stages,
show your reasoning at each stage, then give your final answer.**

## EXAMPLES

Learn from these examples of expected input → output:

**Example 1:**
Input: This product is amazing! Best purchase this year.
Output: Positive — strong enthusiasm with superlative language (confidence: 0.95)

**Example 2:**
Input: Delivery was fast but the item broke after two days.
Output: Mixed — positive logistics, negative product quality (confidence: 0.70)

## OUTPUT FORMAT

**Return your response as a JSON object** with these required fields:

- **`sentiment`** (str)
- **`confidence`** (float)
- **`reasoning`** (str)

```json
{"sentiment": ..., "confidence": ..., "reasoning": ...}
```

## GUARD RAILS

**NEVER include the following:**
  - personal opinions
  - speculation

**ALWAYS include the following:**
  - sentiment
  - confidence
  - reasoning

**Format rules:**
  - Output valid JSON only
  - Confidence must be 0.0 to 1.0

---

## YOUR TASK

Analyze the user's text for sentiment. Provide reasoning and recommendations.
I love this product! Best purchase this year, but shipping was really slow.
```

---

## References

1. Liu, N.F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2023). *Lost in the Middle: How Language Models Use Long Contexts.* Transactions of the ACL, 2024.
2. Wang, Z., et al. (2025). *Serial Position Effects of Large Language Models.*
3. Li, H., et al. (2023). *Instruction Position Matters in Sequence Generation with Large Language Models.* Findings of ACL, 2024.
4. Zhang, H., et al. (2025). *Hard-to-Easy Constraint Ordering for LLMs.*
5. Zhang, Q., et al. (2024). *PASTA: Post-hoc Attention STeering Approach.* ICLR 2024.
6. Zhu, W., et al. (2024). *GUIDE: Guided Understanding with Instruction-Driven Enhancements.* ICLR 2024.
7. Zheng, C., et al. (2025). *Structured Prompting Enables More Robust Evaluation of Language Models.*
8. Sclar, M., et al. (2024). *Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design.* ICLR 2024.
9. GovTech Singapore (2023). *CO-STAR Prompt Framework.* Winner, GPT-4 Prompt Engineering Competition.
10. OpenAI. *Prompt Engineering Guide.* https://platform.openai.com/docs/guides/prompt-engineering
11. Anthropic. *Prompt Engineering Best Practices.* https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering
12. Schulhoff, S., et al. (2024). *The Prompt Report: A Systematic Survey of Prompt Engineering Techniques.* arXiv:2406.06608.
13. Hewing, M., & Leinhos, V. (2024). *The Prompt Canvas: A Literature-Based Practitioner Guide for Creating Effective Prompts.* arXiv:2412.05127.

---

*This prompt flow is used by mycontext's Context Studio. Every user-built prompt follows this exact structure, ensuring research-backed quality regardless of the user's prompting experience.*
