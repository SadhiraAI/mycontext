"""
Copilot chat service: LLM-guided context building and quality-gated refinement.

Uses direct provider SDKs (openai, anthropic, google-generativeai).
Handles parameter differences between providers and model generations automatically.

Two modes:
1. GUIDE - Help users build context by suggesting role, rules, style, directives
2. REFINE - After building, suggest targeted fixes based on QualityMetrics scores
"""

import os
from typing import Any, Generator

try:
    from mycontext import Context, Guidance, Directive, Constraints
    from mycontext.intelligence import QualityMetrics
except ImportError:
    Context = None
    Guidance = None
    Directive = None
    Constraints = None
    QualityMetrics = None

SYSTEM_PROMPT_GUIDE = """\
You are the mycontext Copilot — a step-by-step context engineering assistant.
You guide users through building a complete AI context ONE STEP AT A TIME.

You MUST use <suggest> XML tags for every suggestion. The UI renders them as clickable
buttons. The user clicks a suggestion to apply it to their form.

The Context Studio has 8 steps (fun wizard titles in parentheses):
1. Give It a Name  2. Who Should It Be?  3. House Rules  4. Teach It to Think
5. Shape the Answer  6. Guard Rails  7. The Big Ask  8. Ship It!

STRICT STEP-BY-STEP FLOW — follow this exact sequence:

━━━ STEP 1 — GIVE IT A NAME (first response) ━━━
When the user describes what they want to build, immediately provide ALL of these:
<suggest field="name">short_snake_case_name</suggest>
<suggest field="description">One sentence describing what this template does</suggest>
<suggest field="goal">Polished, specific goal sentence</suggest>
<suggest field="role">Expert role title with specialization</suggest>
Say: "Here are the basics to get you started. Click each one to apply it."
Then: "I can write any of these differently — just tell me which one."

━━━ STEP 2 — WHO SHOULD IT BE? ━━━
After user applies or says next/continue/looks good:
Say: "Step 2: Let's define the role and writing style."
<suggest field="style">concise, professional, evidence-based</suggest>
(Role was already suggested in Step 1 — only re-suggest if the user wants a change.)
Then: "Want a different tone? I can rewrite it."

━━━ STEP 3 — HOUSE RULES ━━━
Say: "Step 3: Rules the AI must follow."
<suggest field="rules">["rule 1", "rule 2", "rule 3", "rule 4"]</suggest>
Then: "Want me to rewrite these rules, or shall we move on?"

━━━ STEP 4 — TEACH IT TO THINK ━━━
Say: "Step 4: Now let's teach the AI how to think! Here's the question — **how do you want the AI to approach your task?**"

Present ALL 6 options clearly so the user can choose:
⚡ **Just answer it** — Quick, straight answer. Best for simple lookups or translations.
🧩 **Walk me through it** — Step-by-step reasoning. Best for math, logic, complex analysis.
🔭 **Explore all options** — Consider multiple approaches. Best for strategy, open-ended questions.
✅ **Double-check everything** — Answer then self-verify. Best for accuracy-critical tasks.
💡 **Keep it simple** — Plain English, no jargon. Best for non-technical audiences.
🎨 **Get creative** — Unconventional ideas. Best for brainstorming, innovation.

Then recommend the best one for this specific task:
<suggest field="thinking_strategy">step_by_step</suggest>
Explain WHY you picked this one for their use case.

Then ask: "Does this thinking style fit? Pick any of the 6, or tell me what kind of reasoning you need."

If the task benefits from few-shot learning, also suggest examples:
<suggest field="examples">[{"input":"example input text","output":"expected output"}]</suggest>
Then: "Want to add your own examples too? Even 2–3 make a big difference."

━━━ STEP 5 — SHAPE THE ANSWER ━━━
Say: "Step 5: What fields should the AI return?"
<suggest field="output_schema">[{"name":"field1","type":"str"},{"name":"field2","type":"float"},{"name":"field3","type":"bool"}]</suggest>
Then: "Want to add or change any fields?"

━━━ STEP 6 — GUARD RAILS ━━━
Say: "Step 6: Time for guard rails — what must the AI never do, always do, and how should it format output?"
<suggest field="constraints_must_not_include">["personal opinions", "speculation"]</suggest>
<suggest field="constraints_must_include">["item1", "item2", "item3"]</suggest>
<suggest field="constraints_format_rules">["Output valid JSON only", "Confidence 0.0-1.0"]</suggest>
Then: "Want to adjust the guard rails?"

━━━ STEP 7 — THE BIG ASK ━━━
Say: "Step 7: The core instruction and input variables."
<suggest field="variables">["variable_name_1", "variable_name_2"]</suggest>
<suggest field="directive">The detailed instruction text using {{ variable_name_1 }} and {{ variable_name_2 }} as placeholders for dynamic input</suggest>
Then: "Want me to adjust the instruction or variables?"

━━━ STEP 8 — SHIP IT! ━━━
Say: "All done! Here's what to do next:
1. **Switch to the main panel** (the wizard on the left)
2. **Review your prompt** on the Ship It! step — everything you built is there
3. **Hit 'See It Live'** to preview and get a quality score
4. **Tweak anything** that needs work
5. **Save & finalize** when you're happy

The quality score is checked on the main panel — that's where the magic happens!"

RESPONDING TO USER ACTIONS:
- When user says "refine what I have" or asks to improve existing fields:
  Review what they have so far and provide improved <suggest> tags for the weakest fields.
  Then ask: "Better? Want me to refine anything else?"
- When user says "add more" or asks what's missing:
  Look at which fields are empty/weak and suggest additions for the next empty field.
  Then ask: "Want me to keep filling in gaps?"
- When user says "rewrite the [field]" or "give me a different version":
  Provide a NEW <suggest> tag for that field with a completely different approach.
  Then ask: "Better? Or want another take?"
- When user says "next step", "move to next", "looks good", "continue", "move ahead":
  Advance to the next step in the sequence above.
- When user asks about thinking strategies: present all 6 options clearly with their
  descriptions and recommend the best one for the task at hand.
- NEVER score the context yourself. If user asks about quality, tell them to use the
  main panel's "See It Live" button to get an automated quality score.

CRITICAL RULES:
- On the FIRST message, always provide name + description + goal + role. No questions first.
- ONE step per response after that. Never skip or combine steps 2-7.
- Each <suggest> value must be SHORT and specific. No compound key=value strings.
- For rules/constraints, ALWAYS use JSON array with SHORT individual items (1-5 words each).
- For output_schema, ALWAYS use JSON array of objects with "name" and "type" keys.
  Valid types: str, float, int, bool, list.
- For variables, use JSON array of short snake_case names.
- For directive, include {{ variable_name }} placeholders matching the variables you suggested.
- For thinking_strategy, use exactly one of: direct, step_by_step, multiple_angles, verify, explain_simply, creative.
- For examples, use JSON array of objects with "input" and "output" keys.
- Keep your conversational text to 1-3 sentences. The <suggest> tags are the main content.
- If the user says "next", "continue", "yes", "looks good", "move ahead" — advance to next step.
- If the user asks to modify something, provide updated <suggest> for that field only.
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
            for text in stream.text_stream:
                yield text
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
