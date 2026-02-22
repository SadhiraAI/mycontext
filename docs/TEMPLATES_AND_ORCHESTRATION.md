# Templates and Multi-Agent Orchestration — How the Codebase Is Designed

**Honest summary:** The codebase is built so that **templates can be chained and used like agents**, but it does **not** today provide full “multi-agent orchestration” out of the box. Below is what exists, what’s missing, and how to get to the vision.

---

## What you’re aiming for (the vision)

- **Template = agent:** DataAnalyzer analyzes, Reasoner reasons, some template scores, etc. Each template is one “agent” with a clear role.
- **Automatic suggestion:** For a given ask (e.g. “sentiment analysis agent”), the system suggests which of **all** templates (e.g. 85) fit, including edge cases and groups.
- **Chain = multi-agent orchestration:** Suggest a **chain** of templates (e.g. QuestionAnalyzer → StepByStepReasoner → something that scores), then **run** that chain: step 1 runs, its output is fed into step 2, and so on — like an orchestra of agents.

---

## How it actually works today

### 1. How many templates the suggester knows

- The repo has **many** pattern classes (50+ free, 35+ enterprise).
- The **pattern suggester** does **not** see all of them. It only uses:
  - **PATTERN_MAP:** keyword → pattern name (about **24** patterns).
  - **VALID_PATTERN_NAMES:** same ~24 names.
  - **PATTERN_CATALOG:** short descriptions for the LLM for those ~24.
- **get_pattern_class(name)** has a **hardcoded map** only for those ~24 (enterprise_map + free_map). Other pattern classes exist in the codebase but are **not** suggestable or loadable by name from the suggester.

So: **suggestion is over a curated subset (~24), not “all 85 templates.”**

### 2. How suggestion works

- **Keyword mode:** Matches the user question against PATTERN_MAP keywords; returns matching pattern names and a **suggested_chain** (an ordered list).
- **LLM mode:** Sends PATTERN_CATALOG (the ~24 names + one-line descriptions) to the LLM; LLM returns a comma-separated list of names; those are validated against VALID_PATTERN_NAMES and turned into a suggestion (and chain).
- **Chain order:** `_order_chain()` takes the suggested names and reorders them by a **fixed** workflow: e.g. temporal → root_cause → causal → differential → future_scenario → synthesis. It does **not** reason about “for this specific task (e.g. sentiment), what order makes sense?” or “output of A feeds input of B.”

So: **suggestion is “which of these ~24 patterns match?”** plus a **generic** chain order, not “consider all groups and edge cases for this agent type and suggest a task-specific chain.”

### 3. Chaining and orchestration

- **Each template** has:
  - `build_context(**inputs)` → returns a `Context`
  - `execute(provider, **inputs)` → runs that context (builds it then calls `context.execute()`).
- **Suggested chain:** The API returns `suggested_chain` = ordered list of pattern names. So you **know** “run A then B then C.”
- **Running the chain:** There is **no** built-in orchestrator that:
  - Takes `suggested_chain`,
  - Runs step 1,
  - Takes the **output** of step 1 and passes it as the **input** to step 2’s `build_context(...)` or `execute(...)`,
  - Repeats to the end.
- **Today you do that manually:** e.g. in examples you build `ctx1`, get `s1 = ctx1.directive.content` (or run `ctx1.execute()` and use the response), then build `ctx2 = Pattern2().build_context(symptoms=s1, ...)`, etc. So **orchestration = you wire outputs to inputs yourself**.

So: **templates can be chained and used as agents, but “run this chain and auto-wire output of one into the next” is not implemented** — it’s a pattern you implement on top of the existing primitives.

### 4. Task-specific chains (e.g. “sentiment analysis agent”)

- There is **no** built-in “agent type” or “task type” (e.g. “sentiment analysis”) that:
  - Defines what such an agent should do (clarify, reason, score, handle edge cases),
  - Scans **all** template groups,
  - Suggests a **task-specific** chain (e.g. QuestionAnalyzer → StepByStepReasoner → rubric/scoring) with edge cases.
- For sentiment, the only way to get suggestions is to use words that appear in PATTERN_MAP (e.g. “analyze”, “reasoning”, “data”); the chain order is still the generic timeline → diagnose → synthesis order, not “optimized for classification + reasoning + scoring.”

So: **the codebase is not designed (yet) so that “sentiment analysis agent” automatically gets a suggested chain over all groups with edge cases.** You can build that **on top** of the existing suggestion + chaining primitives.

---

## Summary table

| Aspect | Designed? | Current behavior |
|--------|-----------|-------------------|
| Template = agent (build_context + execute) | Yes | Each pattern is one “agent.” |
| Suggest which templates fit a question | Yes | Keyword or LLM over **~24** patterns. |
| Suggest a **chain** (ordered list) | Yes | suggested_chain with a **fixed** workflow order. |
| Suggest from **all 85** templates | No | Only ~24 in PATTERN_MAP / get_pattern_class. |
| Task-specific chain (e.g. sentiment) | No | No “agent type” or “check all groups + edge cases.” |
| Run chain and auto-wire output → next input | No | You implement this (e.g. loop: execute step, pass result into next build_context). |
| Multi-agent orchestration out of the box | No | Building block is there; orchestrator layer is not. |

---

## How to get to the vision

1. **Expand suggestion to more (or all) templates**  
   - Register more patterns in PATTERN_MAP / VALID_PATTERN_NAMES / PATTERN_CATALOG and in get_pattern_class (or a registry), so the suggester can suggest from a larger set (e.g. all 85).

2. **Task-aware chain suggestion**  
   - For high-level goals like “sentiment analysis agent,” add a layer (e.g. LLM or rules) that:
     - Defines what such an agent should do (clarify, reason, score, edge cases),
     - Maps that to **groups** (e.g. analysis, reasoning, evaluation),
     - Suggests an **ordered** list of templates and, if needed, how outputs map to next inputs (e.g. “step 1 output = ‘clarified question’ → step 2 problem”).

3. **Orchestrator**  
   - Add a small “chain runner” that:
     - Takes a list of pattern names and (optionally) per-step input mapping,
     - For each step: build_context(...), execute(...),
     - Passes the chosen output (e.g. last response or directive content) into the next step’s inputs,
     - Returns the last result or a summary of all steps.

4. **Use templates as agents in that orchestrator**  
   - Each step = one template’s `build_context` + `execute`. So the codebase **is** designed so templates can be used as agents; the missing piece is the orchestrator and (if you want) task-aware chain suggestion over all templates.

---

## Short answer to “is the codebase designed that way?”

- **Yes** for: templates as agents, suggesting **some** templates for a question, and returning an ordered **suggested_chain**.
- **No** for: suggesting from **all** 85 templates, task-specific chains (e.g. “sentiment agent” with edge cases), and **automatic** execution of a chain with output of one step fed into the next (multi-agent orchestration).

So: the **primitives** (templates, suggestion, chain order) are there; the **orchestration** and **task-aware suggestion over all templates** are what you’d add (or have already started adding) on top.

---

## Target flow: all templates → workflow → HolisticIntegrator → LLM

When you **execute a prompt** (any prompt), the desired flow is:

1. **Auto-suggester** (with or without LLM) searches **all** templates (free + enterprise), finds the relevant ones, and suggests a **workflow** (ordered chain).
2. That **workflow is run**: each template in the chain executes; its output is passed as input to the next.
3. **HolisticIntegrator** takes the outputs from all previous steps (as `perspectives`) and **integrates** them into one coherent context.
4. That **integrated context is passed to the LLM** → you get the final result.

**You are describing this correctly.** It is possible if the auto-suggester is upgraded to include all free and enterprise templates. The chain execution and HolisticIntegrator step already exist in spirit (see `examples/template_chaining_demo.ipynb`).

### Upgrade path: include all free and enterprise in the suggester

1. **Expand the suggester catalog** so it knows **all** pattern names (free + enterprise): add every pattern to **PATTERN_MAP** (keywords), **VALID_PATTERN_NAMES**, and **PATTERN_CATALOG** (for the LLM).
2. **Expand get_pattern_class(name)** so every pattern class is loadable by name (add the rest to enterprise_map/free_map, or add a pattern registry that discovers Pattern subclasses by `name`).
3. **Optional:** a chain runner that takes `suggested_chain` + user input, runs each step, passes step N output into step N+1, then calls **HolisticIntegrator** with `perspectives` = combined output from all steps → one LLM call on the integrated context.
