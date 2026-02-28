"""
IntentRecognizer Baseline Experiment
=====================================
Phase 1: Raw prompt vs IntentRecognizer template (gpt-4o-mini × 2 approaches × 8 cases = 16 runs)
Phase 2: Depth comparison — quick vs standard vs comprehensive (gpt-4o-mini × 2 new depths × 8 cases = 16 runs)
Phase 3: LLM-as-judge scoring (32 judge calls)

Total: 32 experiment runs + 32 judge calls = 64 API calls
"""

import os
import re
import sys
import time
import json

sys.stdout.reconfigure(encoding="utf-8")

os.environ["OPENAI_API_KEY"] = "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"

from mycontext.templates.free.specialized import IntentRecognizer
import litellm
litellm.drop_params = True

recognizer = IntentRecognizer()

# ── Test Cases ──────────────────────────────────────────────────────────────

TEST_CASES = [
    {
        "id": "cancel_sub",
        "domain": "Customer Support",
        "input": "How do I cancel my subscription?",
        "context": "Paying customer for 8 months, submitted this ticket right after a failed payment retry",
        "true_intent": "Frustrated with a billing/payment issue, not genuinely wanting to leave the service",
        "hidden_aspects": [
            "The failed payment is the trigger, not dissatisfaction with the product",
            "They may want help fixing the payment method, not cancellation",
            "Asking about cancellation is a leverage/escalation tactic",
        ],
    },
    {
        "id": "dark_mode",
        "domain": "Product/Engineering",
        "input": "Can we add a dark mode to the app?",
        "context": "Request from the head of compliance at a healthcare company, sent Monday morning",
        "true_intent": "Needs to meet WCAG accessibility compliance requirements, dark mode is one checkbox on an audit",
        "hidden_aspects": [
            "This is compliance-driven, not a personal preference",
            "There's likely an audit deadline they haven't mentioned",
            "They may need documentation of accessibility features, not just the feature itself",
        ],
    },
    {
        "id": "enterprise_plan",
        "domain": "Sales",
        "input": "Do you have an enterprise plan?",
        "context": "Inbound inquiry from a VP of Engineering at a Fortune 500 company",
        "true_intent": "Evaluating whether the vendor is enterprise-ready and mature enough to recommend internally",
        "hidden_aspects": [
            "Not a pricing question — it's a maturity/trust evaluation",
            "They need to build a business case for internal stakeholders",
            "Security, SLAs, and support matter more than features",
        ],
    },
    {
        "id": "best_language",
        "domain": "Career",
        "input": "What's the best programming language to learn?",
        "context": "Asked by a 35-year-old accountant who wants to switch careers into tech",
        "true_intent": "Needs a concrete career transition plan, not a language comparison",
        "hidden_aspects": [
            "Assumes 'best' is universal when it depends on career goals",
            "May not know that starting matters more than which language",
            "Underlying anxiety about age and career switching viability",
        ],
    },
    {
        "id": "make_faster",
        "domain": "Engineering",
        "input": "Can you make the app faster?",
        "context": "From a sales director who demos the product to prospects daily",
        "true_intent": "A specific workflow in the demo is embarrassingly slow in front of prospects, costing deals",
        "hidden_aspects": [
            "Not asking for general optimization — one specific flow is the problem",
            "There's revenue impact they haven't quantified",
            "They may have already lost deals because of this",
        ],
    },
    {
        "id": "when_done",
        "domain": "Stakeholder Management",
        "input": "When will this feature be done?",
        "context": "From the CEO, asked in a Slack DM on a Friday afternoon",
        "true_intent": "Has made a commitment to a client or board and needs a date they can relay with confidence",
        "hidden_aspects": [
            "Not tracking progress — needs to make an external promise",
            "The Friday timing suggests urgency or a Monday deadline",
            "They need a date they can commit to, not a status update",
        ],
    },
    {
        "id": "resignation",
        "domain": "HR",
        "input": "Can you help me write a resignation letter?",
        "context": "From a mid-level manager who recently got passed over for promotion",
        "true_intent": "Processing frustration about being passed over; may not have decided to leave yet",
        "hidden_aspects": [
            "Writing the letter may be therapeutic, not a final decision",
            "They may want to be talked out of it or get advice on alternatives",
            "The real question might be 'should I leave or fight for the promotion?'",
        ],
    },
    {
        "id": "prod_access",
        "domain": "Internal Tools",
        "input": "Can I get access to the production database?",
        "context": "From a junior developer, 3 months into the job, sent at 11pm on a weeknight",
        "true_intent": "Trying to debug a production incident they may have caused, panicking",
        "hidden_aspects": [
            "The late hour suggests urgency/panic, not routine work",
            "They may have caused the issue and are afraid to escalate",
            "They need incident support, not raw database access",
            "Giving production access to a junior dev at 11pm is a security risk",
        ],
    },
]

# ── Raw Prompt (Industry Standard) ─────────────────────────────────────────

RAW_PROMPT = """Analyze the following user input and determine their intent.

Input: {input}
Context: {context}

What is the user's true intent? What do they really want? Provide your analysis."""

# ── Sections to detect in template output ──────────────────────────────────

SECTIONS = [
    "SURFACE ANALYSIS",
    "GOAL INFERENCE",
    "MOTIVATION ANALYSIS",
    "CONTEXT INTERPRETATION",
    "IMPLICIT ASSUMPTIONS",
    "NEED CLASSIFICATION",
    "REFORMULATED INTENT",
    "RECOMMENDATION",
]

# ── Judge Prompt ───────────────────────────────────────────────────────────

JUDGE_PROMPT = """You are evaluating an intent recognition analysis. Given a user input, context, and the KNOWN true intent, score how well the analysis performed.

## User Input
{input}

## Context
{context}

## Known True Intent
{true_intent}

## Key Hidden Aspects That Should Be Detected
{hidden_aspects}

## Analysis Being Evaluated
{analysis}

---

Score each dimension from 1-10. Be strict — a score of 7 means "good but missed something important."

1. **intent_accuracy**: Did it correctly identify the TRUE underlying intent (not just the surface request)?
2. **depth**: How many layers beyond the surface did it uncover? (goals, motivations, assumptions, context)
3. **assumption_detection**: Did it identify implicit assumptions the user is making but not stating?
4. **actionability**: Is the recommended response strategy specific, concrete, and useful?
5. **precision**: Did it stay grounded in evidence, or did it invent motivations not supported by the input/context?

Return ONLY valid JSON:
{{"intent_accuracy": N, "depth": N, "assumption_detection": N, "actionability": N, "precision": N}}"""


def _extract(result):
    if hasattr(result, "response"):
        return result.response or ""
    return str(result)


def count_sections(text):
    upper = text.upper()
    found = {}
    for s in SECTIONS:
        found[s] = s in upper
    return found


def run_raw(model, case):
    """Run the raw/generic prompt via litellm directly."""
    prompt = RAW_PROMPT.format(input=case["input"], context=case["context"])
    t0 = time.time()
    resp = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert at understanding human communication and intent."},
            {"role": "user", "content": prompt},
        ],
    )
    elapsed = time.time() - t0
    out = resp.choices[0].message.content or ""
    tokens = resp.usage.total_tokens if resp.usage else 0
    cost = litellm.completion_cost(completion_response=resp) if resp.usage else 0
    return {
        "approach": "raw",
        "depth": "N/A",
        "output": out,
        "output_chars": len(out),
        "tokens": tokens,
        "cost": cost,
        "elapsed": elapsed,
        "sections_found": count_sections(out),
        "sections_count": sum(1 for s in SECTIONS if s in out.upper()),
    }


def run_template(model, case, depth="comprehensive"):
    """Run the IntentRecognizer template."""
    t0 = time.time()
    result = recognizer.execute(
        provider="openai",
        model=model,
        input=case["input"],
        context=case["context"],
        depth=depth,
        use_cache=False,
    )
    elapsed = time.time() - t0
    out = _extract(result)
    tokens = result.tokens_used if hasattr(result, "tokens_used") else 0
    cost = result.cost_usd if hasattr(result, "cost_usd") else 0
    return {
        "approach": "template",
        "depth": depth,
        "output": out,
        "output_chars": len(out),
        "tokens": tokens,
        "cost": cost,
        "elapsed": elapsed,
        "sections_found": count_sections(out),
        "sections_count": sum(1 for s in SECTIONS if s in out.upper()),
    }


def judge_output(analysis, case):
    """Score an analysis using LLM-as-judge via litellm."""
    prompt = JUDGE_PROMPT.format(
        input=case["input"],
        context=case["context"],
        true_intent=case["true_intent"],
        hidden_aspects="\n".join(f"- {a}" for a in case["hidden_aspects"]),
        analysis=analysis[:4000],
    )
    resp = litellm.completion(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a strict evaluator. Return only valid JSON."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
    )
    text = resp.choices[0].message.content or ""
    try:
        match = re.search(r"\{[^}]+\}", text)
        if match:
            scores = json.loads(match.group())
            scores["avg_score"] = sum(scores.values()) / len(scores)
            return scores
    except (json.JSONDecodeError, ValueError):
        pass
    return {"intent_accuracy": 0, "depth": 0, "assumption_detection": 0,
            "actionability": 0, "precision": 0, "avg_score": 0}


# ═══════════════════════════════════════════════════════════════════════════
# PHASE 1: Raw vs Template (2 models × 2 approaches × 8 cases = 32 runs)
# ═══════════════════════════════════════════════════════════════════════════

MODELS = ["gpt-4o-mini"]

print("=" * 80)
print("PHASE 1: Raw Prompt vs IntentRecognizer Template (gpt-4o-mini)")
print("=" * 80)

all_results = []
total = len(MODELS) * 2 * len(TEST_CASES)
i = 0

for model in MODELS:
    for case in TEST_CASES:
        # Raw
        i += 1
        tag = f"{model} x {case['id']} x raw"
        sys.stdout.write(f"{i:2d}/{total}  {tag}... ")
        sys.stdout.flush()
        try:
            r = run_raw(model, case)
            r["model"] = model
            r["case_id"] = case["id"]
            r["domain"] = case["domain"]
            all_results.append(r)
            print(f"{r['output_chars']} chars  {r['tokens']} tok  ${r['cost']:.4f}  ({r['elapsed']:.1f}s)")
        except Exception as e:
            print(f"ERROR: {e}")
            all_results.append({"model": model, "case_id": case["id"], "domain": case["domain"],
                                "approach": "raw", "depth": "N/A", "output": "", "output_chars": 0,
                                "tokens": 0, "cost": 0, "elapsed": 0, "sections_found": {},
                                "sections_count": 0})

        # Template (comprehensive)
        i += 1
        tag = f"{model} x {case['id']} x template"
        sys.stdout.write(f"{i:2d}/{total}  {tag}... ")
        sys.stdout.flush()
        try:
            r = run_template(model, case, depth="comprehensive")
            r["model"] = model
            r["case_id"] = case["id"]
            r["domain"] = case["domain"]
            all_results.append(r)
            print(f"{r['output_chars']} chars  {r['tokens']} tok  ${r['cost']:.4f}  ({r['elapsed']:.1f}s)")
        except Exception as e:
            print(f"ERROR: {e}")
            all_results.append({"model": model, "case_id": case["id"], "domain": case["domain"],
                                "approach": "template", "depth": "comprehensive", "output": "",
                                "output_chars": 0, "tokens": 0, "cost": 0, "elapsed": 0,
                                "sections_found": {}, "sections_count": 0})

print(f"\nPhase 1 complete: {len(all_results)} runs.\n")

# ═══════════════════════════════════════════════════════════════════════════
# PHASE 2: Depth comparison (gpt-4o-mini × quick/standard × 8 cases = 16 runs)
# ═══════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("PHASE 2: Depth Comparison (gpt-4o-mini: quick, standard)")
print("=" * 80)

depth_model = "gpt-4o-mini"
total2 = 2 * len(TEST_CASES)
j = 0

for depth in ["quick", "standard"]:
    for case in TEST_CASES:
        j += 1
        tag = f"{depth_model} x {case['id']} x {depth}"
        sys.stdout.write(f"{j:2d}/{total2}  {tag}... ")
        sys.stdout.flush()
        try:
            r = run_template(depth_model, case, depth=depth)
            r["model"] = depth_model
            r["case_id"] = case["id"]
            r["domain"] = case["domain"]
            all_results.append(r)
            print(f"{r['output_chars']} chars  {r['tokens']} tok  ${r['cost']:.4f}  ({r['elapsed']:.1f}s)")
        except Exception as e:
            print(f"ERROR: {e}")
            all_results.append({"model": depth_model, "case_id": case["id"], "domain": case["domain"],
                                "approach": "template", "depth": depth, "output": "",
                                "output_chars": 0, "tokens": 0, "cost": 0, "elapsed": 0,
                                "sections_found": {}, "sections_count": 0})

print(f"\nPhase 2 complete. Total runs: {len(all_results)}.\n")

# ═══════════════════════════════════════════════════════════════════════════
# PHASE 3: LLM-as-Judge Scoring
# ═══════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("PHASE 3: LLM-as-Judge Scoring")
print("=" * 80)

case_lookup = {c["id"]: c for c in TEST_CASES}

for idx, r in enumerate(all_results):
    case = case_lookup[r["case_id"]]
    label = f"{r['model']} / {r['case_id']} / {r['approach']}"
    if r["approach"] == "template":
        label += f" ({r['depth']})"
    sys.stdout.write(f"{idx+1:2d}/{len(all_results)}  Judging {label}... ")
    sys.stdout.flush()
    try:
        scores = judge_output(r["output"], case)
        r["scores"] = scores
        print(f"avg={scores['avg_score']:.1f}")
    except Exception as e:
        print(f"ERROR: {e}")
        r["scores"] = {"intent_accuracy": 0, "depth": 0, "assumption_detection": 0,
                        "actionability": 0, "precision": 0, "avg_score": 0}

# ═══════════════════════════════════════════════════════════════════════════
# ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 80)
print("RESULTS: Phase 1 — Raw vs Template")
print("=" * 80)

for model in MODELS:
    print(f"\n  {model}:")
    for approach in ["raw", "template"]:
        subset = [r for r in all_results
                  if r["model"] == model and r["approach"] == approach
                  and (r["depth"] == "N/A" or r["depth"] == "comprehensive")]
        if not subset:
            continue
        avg_score = sum(r["scores"]["avg_score"] for r in subset) / len(subset)
        avg_intent = sum(r["scores"]["intent_accuracy"] for r in subset) / len(subset)
        avg_depth = sum(r["scores"]["depth"] for r in subset) / len(subset)
        avg_assump = sum(r["scores"]["assumption_detection"] for r in subset) / len(subset)
        avg_action = sum(r["scores"]["actionability"] for r in subset) / len(subset)
        avg_prec = sum(r["scores"]["precision"] for r in subset) / len(subset)
        avg_chars = sum(r["output_chars"] for r in subset) / len(subset)
        avg_tokens = sum(r["tokens"] for r in subset) / len(subset)
        avg_cost = sum(r["cost"] for r in subset) / len(subset)
        avg_sections = sum(r["sections_count"] for r in subset) / len(subset)
        label = approach if approach == "raw" else "template (comprehensive)"
        print(f"    {label}:")
        print(f"      Avg Score:    {avg_score:.1f}/10")
        print(f"      Intent Acc:   {avg_intent:.1f}  Depth: {avg_depth:.1f}  Assumptions: {avg_assump:.1f}  Actionability: {avg_action:.1f}  Precision: {avg_prec:.1f}")
        print(f"      Sections:     {avg_sections:.1f}/8  |  Chars: {avg_chars:.0f}  |  Tokens: {avg_tokens:.0f}  |  Cost: ${avg_cost:.4f}")

print("\n" + "=" * 80)
print("RESULTS: Phase 2 — Depth Comparison (gpt-4o-mini)")
print("=" * 80)

for depth in ["quick", "standard", "comprehensive"]:
    if depth == "comprehensive":
        subset = [r for r in all_results
                  if r["model"] == "gpt-4o-mini" and r["approach"] == "template" and r["depth"] == "comprehensive"]
    else:
        subset = [r for r in all_results
                  if r["model"] == "gpt-4o-mini" and r["depth"] == depth]
    if not subset:
        continue
    avg_score = sum(r["scores"]["avg_score"] for r in subset) / len(subset)
    avg_intent = sum(r["scores"]["intent_accuracy"] for r in subset) / len(subset)
    avg_depth_s = sum(r["scores"]["depth"] for r in subset) / len(subset)
    avg_chars = sum(r["output_chars"] for r in subset) / len(subset)
    avg_tokens = sum(r["tokens"] for r in subset) / len(subset)
    avg_cost = sum(r["cost"] for r in subset) / len(subset)
    print(f"\n  {depth}:")
    print(f"    Avg Score: {avg_score:.1f}/10  |  Intent Acc: {avg_intent:.1f}  |  Depth: {avg_depth_s:.1f}")
    print(f"    Chars: {avg_chars:.0f}  |  Tokens: {avg_tokens:.0f}  |  Cost: ${avg_cost:.4f}")

# Per-case breakdown
print("\n" + "=" * 80)
print("PER-CASE BREAKDOWN (gpt-4o-mini)")
print("=" * 80)

for case in TEST_CASES:
    print(f"\n  [{case['id']}] {case['domain']}: \"{case['input'][:60]}...\"")
    print(f"  True intent: {case['true_intent'][:80]}...")
    for r in all_results:
        if r["case_id"] == case["id"] and r["model"] == "gpt-4o-mini":
            label = r["approach"]
            if r["approach"] == "template":
                label = f"template/{r['depth']}"
            s = r["scores"]
            print(f"    {label:<25s}  avg={s['avg_score']:.1f}  intent={s['intent_accuracy']}  depth={s['depth']}  assump={s['assumption_detection']}  action={s['actionability']}  prec={s['precision']}")

# ── Verdict ─────────────────────────────────────────────────────────────────

print("\n" + "=" * 80)
print("VERDICT")
print("=" * 80)

raw_runs = [r for r in all_results if r["approach"] == "raw"]
tmpl_runs = [r for r in all_results if r["approach"] == "template" and r["depth"] == "comprehensive"]

def avg(lst, key):
    return sum(r["scores"][key] for r in lst) / len(lst) if lst else 0

print(f"\n  Q1: Does the template add value over raw prompts?")
raw_avg = avg(raw_runs, "avg_score")
tmpl_avg = avg(tmpl_runs, "avg_score")
uplift = tmpl_avg - raw_avg

print(f"     raw={raw_avg:.1f} → template={tmpl_avg:.1f} (Δ={uplift:+.1f})")
if uplift > 0.5:
    print(f"  -> YES: Template improves score by {uplift:.1f} points.")
else:
    print(f"  -> MARGINAL: Template uplift is only {uplift:.1f} points.")

print(f"\n  Q2: Which dimension benefits most from the template?")
for dim in ["intent_accuracy", "depth", "assumption_detection", "actionability", "precision"]:
    r_avg = avg(raw_runs, dim)
    t_avg = avg(tmpl_runs, dim)
    delta = t_avg - r_avg
    bar = "█" * int(abs(delta) * 5)
    sign = "+" if delta > 0 else ""
    print(f"     {dim:<25s}  raw={r_avg:.1f}  template={t_avg:.1f}  Δ={sign}{delta:.1f}  {bar}")

print(f"\n  Q3: Do depth levels work for intent recognition?")
for depth in ["quick", "standard", "comprehensive"]:
    if depth == "comprehensive":
        subset = tmpl_runs
    else:
        subset = [r for r in all_results if r["depth"] == depth]
    if not subset:
        continue
    d_avg = avg(subset, "avg_score")
    d_intent = avg(subset, "intent_accuracy")
    d_chars = sum(r["output_chars"] for r in subset) / len(subset)
    d_tokens = sum(r["tokens"] for r in subset) / len(subset)
    d_cost = sum(r["cost"] for r in subset) / len(subset)
    print(f"     {depth:<15s}  score={d_avg:.1f}  intent={d_intent:.1f}  chars={d_chars:.0f}  tokens={d_tokens:.0f}  cost=${d_cost:.4f}")

print(f"\n  Q4: Token efficiency (cost per quality point)?")
raw_cost = sum(r["cost"] for r in raw_runs) / len(raw_runs) if raw_runs else 0
tmpl_cost = sum(r["cost"] for r in tmpl_runs) / len(tmpl_runs) if tmpl_runs else 0
print(f"     Raw:      ${raw_cost:.4f}/call  →  {raw_avg:.1f} score  →  ${raw_cost/max(raw_avg,0.1):.5f}/point")
print(f"     Template: ${tmpl_cost:.4f}/call  →  {tmpl_avg:.1f} score  →  ${tmpl_cost/max(tmpl_avg,0.1):.5f}/point")

# Save results
save_data = []
for r in all_results:
    save_data.append({k: v for k, v in r.items() if k != "output" and k != "sections_found"})

with open("docs/examples/intent_recognizer_results.json", "w") as f:
    json.dump(save_data, f, indent=2)

with open("docs/examples/intent_recognizer_full_outputs.json", "w", encoding="utf-8") as f:
    json.dump([{"model": r["model"], "case_id": r["case_id"], "approach": r["approach"],
                "depth": r["depth"], "output": r["output"]} for r in all_results], f, indent=2)

print("\nResults saved to docs/examples/intent_recognizer_results.json")
print("Full outputs saved to docs/examples/intent_recognizer_full_outputs.json")
