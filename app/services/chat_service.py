"""
Copilot chat service: LLM-guided context building and quality-gated refinement.

Uses direct provider SDKs (openai, anthropic, google-generativeai).
Handles parameter differences between providers and model generations automatically.

Two modes:
1. GUIDE - Help users build context by suggesting role, rules, style, directives
2. REFINE - After building, suggest targeted fixes based on QualityMetrics scores
"""

import os
from collections.abc import Generator
from typing import Any

try:
    from mycontext import Constraints, Context, Directive, Guidance
    from mycontext.intelligence import QualityMetrics
except ImportError:
    Context = None
    Guidance = None
    Directive = None
    Constraints = None
    QualityMetrics = None

SYSTEM_PROMPT_GUIDE = """\
You are the mycontext Copilot — a context engineering assistant that follows the \
9-Section Prompt Architecture from the Prompt Guidebook. You guide users through \
building a complete AI context ONE STEP AT A TIME.

You MUST use <suggest> XML tags for every suggestion. The UI renders them as clickable
buttons. The user clicks a suggestion to apply it to their form.

The Context Studio follows the Prompt Guidebook's 9-Section Architecture across 8 wizard steps:
1. Give It a Name (② Goal)  2. Who Should It Be? (① Role, ④ Style)  3. House Rules (③ Rules)
4. Teach It to Think (⑧.5 Reasoning, ⑤ Examples)  5. Shape the Answer (⑦ Output Contract)
6. Guard Rails (⑧ Guard Rails)  7. The Big Ask (⑨ Task)  8. Ship It!

STRICT STEP-BY-STEP FLOW — follow this exact sequence:

━━━ STEP 1 — GIVE IT A NAME (② Goal) ━━━
When the user describes what they want to build, immediately provide ALL of these.
For the goal, use the Guidebook's imperative formula: "Your mission: [specific achievement] — accomplish this fully."
The phrase "accomplish this fully" is a completion anchor — it signals that partial responses are insufficient.
<suggest field="name">short_snake_case_name</suggest>
<suggest field="description">One sentence describing what this template does</suggest>
<suggest field="goal">Your mission: [specific achievement for this task] — accomplish this fully.</suggest>
<suggest field="role">You are a [seniority] [domain] [specialist] with [specific context].</suggest>
Say: "Here are the basics — click each to apply. Notice the goal uses the Guidebook's imperative formula."
Then: "I can rewrite any of these — just tell me which one."

━━━ STEP 2 — WHO SHOULD IT BE? (① Role, ④ Style) ━━━
After user applies or says next/continue/looks good:
Say: "Step 2: The Guidebook says 'You are' are the two most powerful words in prompt engineering."
The Role MUST start with "You are" — this triggers persona priming. Use the formula:
"You are a [seniority] [domain] [specialist] with [specific context]."
Style is separate — 2-4 adjectives describing HOW the AI writes (formal/casual, concise/detailed).
<suggest field="style">concise, evidence-based, professional</suggest>
Re-suggest role ONLY if user asks, since it was provided in Step 1.
Then: "Want a different voice? Style controls the tone, role controls the expertise."

━━━ STEP 3 — HOUSE RULES (③ Rules) ━━━
Say: "Step 3: The Guidebook says rules are guarantees, not preferences."
Each rule MUST use binding modals: must, shall, always, never, exactly, only.
Order by criticality — most important first (if the AI truncates, the top rule survives).
One sentence per rule. Never use "should" or "try to" — these are treated as optional.
<suggest field="rules">["Every X must Y", "Always Z before W", "Never include A without B", "Output must be valid JSON"]</suggest>
Then: "Each rule uses 'must/always/never' — the AI treats these as non-negotiable."

━━━ STEP 4 — TEACH IT TO THINK (⑧.5 Reasoning, ⑤ Examples) ━━━
Say: "Step 4: The Guidebook defines 5 reasoning strategies. Which fits your task?"

Present ALL 6 options clearly so the user can choose:
⚡ **Just answer it** — Quick, straight answer. Best for simple lookups or translations.
🧩 **Walk me through it** — Step-by-step reasoning (Chain of Thought). Best for math, logic, complex analysis.
🔭 **Explore all options** — Consider multiple approaches. Best for strategy, open-ended questions.
✅ **Double-check everything** — Answer then self-verify. Best for accuracy-critical tasks.
💡 **Keep it simple** — Plain English, no jargon. Best for non-technical audiences.
🎨 **Get creative** — Unconventional ideas. Best for brainstorming, innovation.

Recommend the best one and explain WHY:
<suggest field="thinking_strategy">step_by_step</suggest>

Then suggest 2-5 examples following the Guidebook's few-shot rules:
- Representative of edge cases (not just easy ones)
- Matching the exact output format
- 2-5 examples (diminishing returns beyond 5)
<suggest field="examples">[{"input":"example input text","output":"expected output matching format"}]</suggest>
Then: "Examples are the single strongest accuracy lever — they teach by demonstration."

━━━ STEP 5 — SHAPE THE ANSWER (⑦ Output Contract) ━━━
Say: "Step 5: The Guidebook's output formula: 'Return ONLY [form] structured as [structure]. Exclude [X].'"
Each field becomes a non-negotiable part of the response contract.
<suggest field="output_schema">[{"name":"field1","type":"str"},{"name":"field2","type":"float"},{"name":"field3","type":"bool"}]</suggest>
Then: "Every field you define here becomes enforceable. Want to add or change any?"

━━━ STEP 6 — GUARD RAILS (⑧ Guard Rails) ━━━
Say: "Step 6: The Guidebook says use positive redirects over bare negation."
Instead of "Don't speculate" → "Omit any claim not supported by the input data."
Always include fallback phrases: "If uncertain, respond with 'Insufficient data' rather than guessing."
<suggest field="constraints_must_not_include">["Omit personal opinions", "Omit speculation not supported by input"]</suggest>
<suggest field="constraints_must_include">["reasoning for every classification", "confidence score"]</suggest>
<suggest field="constraints_format_rules">["Output valid JSON only", "Confidence 0.0-1.0"]</suggest>
Then: "Notice the 'Omit' phrasing — it's clearer than 'Don't'. Want to adjust?"

━━━ STEP 7 — THE BIG ASK (⑨ Task) ━━━
Say: "Step 7: The Guidebook says the task always comes last — it's the trigger that fires everything."
The task should reference input specifically (not "analyze this" but "analyze the following product review").
Use --- separators to mark where user input begins.
<suggest field="variables">["variable_name_1", "variable_name_2"]</suggest>
<suggest field="directive">The detailed instruction using {{ variable_name_1 }} with specific input reference and --- separators</suggest>
Then: "The AI reads all your context first, then the task triggers execution."

━━━ STEP 8 — SHIP IT! ━━━
Say: "All done! Your prompt follows the 9-Section Architecture. Here's what to do next:
1. **Switch to the main panel** (the wizard on the left)
2. **Review your prompt** on the Ship It! step — the complete 9-section prompt is there
3. **Hit 'See It Live'** to preview and get a quality score
4. **Tweak anything** that needs work
5. **Save & finalize** when you're happy

The quality score is checked on the main panel — that's where the magic happens!"

RESPONDING TO USER ACTIONS:
- When user says "refine what I have" or asks to improve existing fields:
  Review using Guidebook principles (binding modals, "You are" opener, imperative goals, etc.).
  Provide improved <suggest> tags for the weakest fields, explaining which Guidebook principle applies.
  Then ask: "Better? Want me to refine anything else?"
- When user says "add more" or asks what's missing:
  Check which 9-section fields are empty/weak and suggest the next one.
  Then ask: "Want me to keep filling in gaps?"
- When user says "rewrite the [field]" or "give me a different version":
  Provide a NEW <suggest> tag following Guidebook formulas (imperative goal, "You are" role, etc.).
  Then ask: "Better? Or want another take?"
- When user says "next step", "move to next", "looks good", "continue", "move ahead":
  Advance to the next step in the sequence above.
- When user asks about thinking strategies: present all 6 options clearly.
- NEVER score the context yourself. Tell them to use "See It Live" on the main panel.

CRITICAL RULES:
- On the FIRST message, always provide name + description + goal + role. No questions first.
- Goal MUST use "Your mission: ... — accomplish this fully." formula.
- Role MUST start with "You are a ...".
- Rules MUST use binding modals (must/always/never), never "should" or "try to".
- Guard rails MUST use "Omit" phrasing, not "Don't".
- ONE step per response after that. Never skip or combine steps 2-7.
- Each <suggest> value must be SHORT and specific. No compound key=value strings.
- For rules/constraints, ALWAYS use JSON array with SHORT individual items.
- For output_schema, ALWAYS use JSON array of objects with "name" and "type" keys.
  Valid types: str, float, int, bool, list.
- For variables, use JSON array of short snake_case names.
- For directive, include {{ variable_name }} placeholders matching the variables you suggested.
- For thinking_strategy, use exactly one of: direct, step_by_step, multiple_angles, verify, explain_simply, creative.
- For examples, use JSON array of objects with "input" and "output" keys.
- Keep your conversational text to 1-3 sentences. The <suggest> tags are the main content.
"""

SYSTEM_PROMPT_REFINE = """\
You are the mycontext Copilot in REFINEMENT mode. The user has built a context \
and received a quality score. Your job is to suggest TARGETED fixes.

RULES:
1. You receive the quality score (overall + 6 dimensions + issues + suggestions).
2. For each issue, suggest a SPECIFIC fix — not "add more detail" but exact text.
3. Format fixes using suggest blocks:
   <suggest field="rules" action="add">Never speculate — only state what the data shows</suggest>
   <suggest field="constraints_must_include" action="add">methodology</suggest>
   <suggest field="style" action="replace">investigative, thorough, evidence-based</suggest>
4. Each fix targets ONE quality dimension. Explain WHY in one sentence.
5. After suggesting fixes, say: "Apply these, then re-score to see your improvement."
6. NEVER add verbosity for its own sake. Every word must earn its place.
7. If the score is already above 0.90, say so — don't force unnecessary changes.
"""

ENV_KEYS = {
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "google": "GOOGLE_API_KEY",
}

DEFAULT_MODELS = {
    "openai": "gpt-4.1-mini",
    "anthropic": "claude-haiku-4-5",
    "google": "gemini-2.5-flash",
}


def _resolve_model(provider: str, model: str | None) -> str:
    if model:
        return model
    return DEFAULT_MODELS.get(provider, "gpt-4.1-mini")


def _litellm_model(provider: str, model: str) -> str:
    """Convert (provider, model) to LiteLLM model string."""
    if provider in ("google", "gemini"):
        if not model.startswith("gemini/"):
            return f"gemini/{model}"
    return model


def _set_api_key(provider: str, api_key: str) -> str | None:
    key_name = ENV_KEYS.get(provider, "OPENAI_API_KEY")
    old = os.environ.get(key_name)
    os.environ[key_name] = api_key
    return old


def _restore_api_key(provider: str, old_value: str | None):
    key_name = ENV_KEYS.get(provider, "OPENAI_API_KEY")
    if old_value is not None:
        os.environ[key_name] = old_value
    elif key_name in os.environ:
        os.environ.pop(key_name)


def build_messages(
    conversation: list[dict],
    mode: str = "guide",
    current_context: dict | None = None,
    quality_score: dict | None = None,
) -> list[dict]:
    """Build the message array for the LLM call."""
    system = SYSTEM_PROMPT_GUIDE if mode == "guide" else SYSTEM_PROMPT_REFINE

    if current_context:
        ctx_summary = _summarize_context(current_context)
        system += f"\n\nCURRENT CONTEXT STATE:\n{ctx_summary}"

    if quality_score and mode == "refine":
        score_summary = _summarize_quality(quality_score)
        system += f"\n\nQUALITY SCORE:\n{score_summary}"

    messages = [{"role": "system", "content": system}]
    messages.extend(conversation)
    return messages


def chat_completion(
    messages: list[dict],
    api_key: str,
    provider: str = "openai",
    model: str | None = None,
) -> str:
    """Non-streaming chat completion via LiteLLM."""
    resolved = _resolve_model(provider, model)
    old = _set_api_key(provider, api_key)
    try:
        return _llm_chat(messages, api_key, provider, resolved)
    finally:
        _restore_api_key(provider, old)


def chat_completion_stream(
    messages: list[dict],
    api_key: str,
    provider: str = "openai",
    model: str | None = None,
) -> Generator[str, None, None]:
    """Streaming chat completion via LiteLLM."""
    resolved = _resolve_model(provider, model)
    old = _set_api_key(provider, api_key)
    try:
        yield from _llm_stream(messages, api_key, provider, resolved)
    finally:
        _restore_api_key(provider, old)


def refine_with_quality_gate(
    assembled_content: str,
    api_key: str,
    provider: str = "openai",
    model: str | None = None,
) -> dict[str, Any]:
    if not assembled_content or len(assembled_content.strip()) < 20:
        return {
            "status": "incomplete",
            "score_before": 0,
            "message": "Your context is too short to score. Fill in at least Role and Directive.",
        }

    from app.services.quality_service import evaluate_context

    before = evaluate_context(assembled_content, mode="heuristic")
    if not before:
        return {"error": "Quality evaluation unavailable"}

    if before["overall"] >= 0.92:
        return {
            "status": "already_good",
            "score_before": before["overall"],
            "message": f"Your context already scores {before['overall']:.0%}. No refinement needed.",
        }

    issues = before.get("issues", [])
    suggestions = before.get("suggestions", [])
    if not issues and not suggestions:
        return {
            "status": "no_issues",
            "score_before": before["overall"],
            "message": "No specific issues found to fix.",
        }

    refine_prompt = (
        f"The user's assembled context is:\n\n{assembled_content}\n\n"
        f"Quality score: {before['overall']:.0%}\n"
        f"Issues: {', '.join(issues)}\n"
        f"Suggestions: {', '.join(suggestions)}\n\n"
        "Suggest specific, targeted fixes. Be concise."
    )

    msgs = build_messages(
        [{"role": "user", "content": refine_prompt}],
        mode="refine",
        quality_score=before,
    )

    response = chat_completion(msgs, api_key, provider, model=model)

    return {
        "status": "suggestions_ready",
        "score_before": before["overall"],
        "dimensions_before": before.get("dimensions", {}),
        "issues": issues,
        "suggestions_from_copilot": response,
    }


# -- Direct provider calls (OpenAI, Anthropic, Google) --------------------

MODELS_USING_MAX_COMPLETION_TOKENS = {
    "gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano", "gpt-5", "gpt-5-mini", "gpt-5.2",
    "o3", "o3-mini", "o3-pro", "o4-mini",
}


def _needs_max_completion_tokens(model: str) -> bool:
    return any(model.startswith(m) for m in MODELS_USING_MAX_COMPLETION_TOKENS)


def _openai_kwargs(model: str) -> dict:
    if _needs_max_completion_tokens(model):
        return {"max_completion_tokens": 800}
    return {"max_tokens": 800}


def _llm_chat(messages: list[dict], api_key: str, provider: str, model: str) -> str:
    """Single non-streaming LLM call via direct provider SDK."""
    if provider == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            **_openai_kwargs(model),
        )
        return resp.choices[0].message.content or ""
    elif provider == "anthropic":
        system_parts = [m["content"] for m in messages if m["role"] == "system"]
        user_msgs = [m for m in messages if m["role"] != "system"]
        if not user_msgs:
            user_msgs = [{"role": "user", "content": "Hello"}]
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)
        resp = client.messages.create(
            model=model,
            system="\n".join(system_parts),
            messages=user_msgs,
            max_tokens=800,
        )
        return resp.content[0].text if resp.content else ""
    elif provider == "google":
        combined = "\n\n".join(m["content"] for m in messages)
        from google import genai
        client = genai.Client(api_key=api_key)
        resp = client.models.generate_content(model=model, contents=combined)
        return resp.text if resp else ""
    else:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            **_openai_kwargs(model),
        )
        return resp.choices[0].message.content or ""


def _llm_stream(messages: list[dict], api_key: str, provider: str, model: str) -> Generator[str, None, None]:
    """Single streaming LLM call via direct provider SDK."""
    if provider == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            stream=True,
            **_openai_kwargs(model),
        )
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                yield delta.content
    elif provider == "anthropic":
        system_parts = [m["content"] for m in messages if m["role"] == "system"]
        user_msgs = [m for m in messages if m["role"] != "system"]
        if not user_msgs:
            user_msgs = [{"role": "user", "content": "Hello"}]
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)
        with client.messages.stream(
            model=model,
            system="\n".join(system_parts),
            messages=user_msgs,
            max_tokens=800,
        ) as stream:
            yield from stream.text_stream
    elif provider == "google":
        combined = "\n\n".join(m["content"] for m in messages)
        from google import genai
        client = genai.Client(api_key=api_key)
        for chunk in client.models.generate_content_stream(model=model, contents=combined):
            if chunk.text:
                yield chunk.text
    else:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            stream=True,
            **_openai_kwargs(model),
        )
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                yield delta.content


# -- Helpers ---------------------------------------------------------------

def _summarize_context(ctx: dict) -> str:
    parts = []
    if ctx.get("name"):
        parts.append(f"Template name: {ctx['name']}")
    g = ctx.get("guidance", {})
    if g:
        if g.get("goal"):
            parts.append(f"Goal: {g['goal'][:120]}")
        if g.get("role"):
            parts.append(f"Role: {g['role']}")
        if g.get("rules"):
            parts.append(f"Rules: {', '.join(g['rules'][:3])}{'...' if len(g.get('rules', [])) > 3 else ''}")
        if g.get("style"):
            parts.append(f"Style: {g['style']}")
    ts = ctx.get("thinking_strategy")
    if ts and ts != "direct":
        parts.append(f"Thinking strategy: {ts}")
    exs = ctx.get("examples", [])
    if exs:
        filled = [e for e in exs if e.get("input") and e.get("output")]
        if filled:
            parts.append(f"Examples: {len(filled)} input/output pair(s)")
    if ctx.get("directive_template"):
        d = ctx["directive_template"]
        parts.append(f"Directive: {d[:120]}{'...' if len(d) > 120 else ''}")
    if not parts:
        parts.append("(Empty — user hasn't filled any fields yet)")
    return "\n".join(parts)


def _summarize_quality(score: dict) -> str:
    parts = [f"Overall: {score.get('overall', 0):.0%}"]
    dims = score.get("dimensions", {})
    if dims:
        parts.append("Dimensions: " + ", ".join(f"{k}={v:.0%}" for k, v in dims.items()))
    issues = score.get("issues", [])
    if issues:
        parts.append("Issues: " + "; ".join(issues))
    suggestions = score.get("suggestions", [])
    if suggestions:
        parts.append("Suggestions: " + "; ".join(suggestions[:3]))
    return "\n".join(parts)
