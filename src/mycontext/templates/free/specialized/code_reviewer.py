"""
Code Reviewer Template - Cognitive code review with risk-weighted findings.

Uses an orient-then-analyze cognitive flow based on CRDM research (2026),
Bacchelli & Bird (2013), and Google eng-practices. Focuses on dimensions
that linters cannot catch; deliberately excludes style/formatting.
Free tier template - part of mycontext open source.
"""

from typing import ClassVar

from mycontext.foundation import Constraints, Directive, Guidance
from mycontext.structure import Pattern
from mycontext.utils.format_directives import VALID_OUTPUT_FORMATS, get_format_directive


class CodeReviewer(Pattern):
    """
    Perform risk-aware code reviews using a four-phase cognitive flow.

    The template follows the ORIENT -> ANALYZE -> ASSESS -> RECOMMEND
    structure, mirroring how senior engineers actually review code.
    It focuses on 7 dimensions that linters cannot catch and explicitly
    excludes style/formatting to avoid the bikeshedding that accounts
    for 85% of low-value review comments (CodePulse 2025).

    Review dimensions: correctness, security, performance, design,
    resilience, testing, maintainability.

    Examples:
        >>> from mycontext.templates.free import CodeReviewer
        >>>
        >>> reviewer = CodeReviewer()
        >>> code = '''
        ... def fetch_user(user_id):
        ...     query = f"SELECT * FROM users WHERE id = {user_id}"
        ...     return db.execute(query)
        ... '''
        >>>
        >>> result = reviewer.execute(
        ...     provider="gemini",
        ...     code=code,
        ...     language="Python",
        ...     focus_areas=["security", "correctness"]
        ... )
        >>> print(result.response)

    Based on:
    - Code Review as Decision-Making / CRDM model (2026)
    - Bacchelli & Bird (2013) — Modern code review, Microsoft Research
    - Google eng-practices — "What to look for in a code review"
    - Fagan (1976) — Formal inspection methodology

    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "You are a senior software engineer performing a code review. "
        "Follow this cognitive process strictly:\n\n"
        "Code:\n{code}\n\n"
        "Language: {language}\n"
        "{context_section}\n"
        "Focus areas: {focus_areas}\n\n"
        "(1) ORIENT — Before any critique, state in 2-3 sentences what this code "
        "does, what its key abstractions are, and what assumptions it makes. "
        "Build a mental model first. "
        "(2) ANALYZE — Examine the code across the requested focus areas. For each "
        "finding, reference the exact location and explain the issue. Do NOT comment "
        "on style, formatting, naming conventions, or docstring presence — linters "
        "handle those. Focus on what linters cannot catch: logic errors, security "
        "flaws, failure modes, design problems, and missing tests. "
        "(3) ASSESS — For each finding, state three things: Impact (what happens if "
        "this manifests — data loss, crash, degradation, or cosmetic), Likelihood "
        "(always triggered, common path, edge case, or theoretical), and Blast Radius "
        "(full system, single service, one module, or local only). "
        "(4) RECOMMEND — Give exactly 3 priority actions. For each: the finding in "
        "one sentence, why it matters (the risk assessment), and a concrete code fix."
    )

    def __init__(self):
        super().__init__(
            name="code_reviewer",
            guidance=Guidance(
                role="Senior Software Engineer and Code Review Expert",
                rules=[
                    "Understand before criticizing — state what the code does before finding issues",
                    "Focus on what linters cannot catch — skip style, formatting, and naming",
                    "Assess risk, not just severity — every finding needs impact, likelihood, and blast radius",
                    "Think about failure modes — what breaks in production, not just what looks wrong",
                    "Provide concrete fixes — every finding must include a working code example",
                    "Acknowledge strengths — note what the code does well"
                ],
                style="risk-aware, specific, constructive, failure-mode-oriented"
            ),
            directive_template="""Review this {language} code using a structured cognitive process.

**CODE TO REVIEW**:
```{language}
{code}
```

{context_section}

**FOCUS AREAS**: {focus_areas}

---

## 1. ORIENT

Before finding any issues, build a mental model of this code:

- **Purpose**: What does this code do? (1-2 sentences)
- **Key abstractions**: What are the main data structures, functions, or classes and how do they relate?
- **Assumptions**: What does this code assume about its inputs, environment, or dependencies?
- **Data flow**: How does data move through this code? (input → processing → output)

---

## 2. ANALYZE

Examine the code across the requested focus areas. For each finding, use this format:

> **[Dimension] Finding: [One-sentence description]**
> - **Location**: [Function name, line number, or code reference]
> - **What's wrong**: [Specific technical explanation]
> - **What fails**: [The failure scenario — what breaks and under what conditions]

Dimensions to check (based on focus areas):

**Correctness** — Logic errors, edge cases, off-by-one errors, null/undefined handling, boundary conditions, race conditions. Does the code actually do what it claims to?

**Security** — Injection vectors (SQL, XSS, command), authentication/authorization flaws, data exposure, hardcoded secrets, insecure defaults. Can this be exploited?

**Performance** — Algorithmic complexity, N+1 queries, unnecessary allocations, resource leaks, missing connection pooling, unbounded growth. Will this scale?

**Design** — SOLID violations, inappropriate coupling, wrong abstraction level, over-engineering, missing separation of concerns. Is this well-structured for future change?

**Resilience** — Missing error handling, unhandled exception paths, no timeouts on external calls, no retry logic, silent failures, cascade failure risk. What happens when things go wrong?

**Testing** — Missing test coverage for critical paths, assertions that don't test meaningful behavior, untested error paths, missing edge case tests. Will the test suite catch regressions?

**Maintainability** — Unnecessary complexity, duplicated logic, functions doing too many things, unclear control flow. Can the next developer understand and safely modify this?

**IMPORTANT**: Do NOT comment on style, formatting, naming conventions, import ordering, or docstring presence. These are linter concerns. Spend your analysis on dimensions above that linters cannot catch.

Only analyze dimensions listed in the focus areas. If a dimension has no findings, state "No issues found" — do not force findings.

---

## 3. ASSESS

For each finding from the ANALYZE phase, assign a risk profile:

| Finding | Impact | Likelihood | Blast Radius | Priority |
|---------|--------|------------|--------------|----------|
| [Finding summary] | [Data loss / System crash / Degradation / Cosmetic] | [Always triggered / Common path / Edge case / Theoretical] | [Full system / Single service / One module / Local] | [Fix before merge / Fix soon / Track for later] |

**Impact**: What is the worst outcome if this issue manifests in production?
**Likelihood**: How probable is this failure path in real-world usage?
**Blast Radius**: If it fails, how much of the system is affected?
**Priority**: Based on the combination of the three factors above.

---

## 4. STRENGTHS

What this code does well (be specific — reference actual patterns, decisions, or techniques):
- [Strength 1]
- [Strength 2]

---

## 5. RECOMMEND

Exactly 3 priority actions, ordered by risk (highest first). For each:

### Action 1: [One-sentence finding]
- **Risk**: [Impact + Likelihood + Blast Radius summary from ASSESS]
- **Fix**:
```{language}
# Before
[problematic code]

# After
[fixed code]
```
- **Why this fix**: [Brief explanation of the approach]

### Action 2: [One-sentence finding]
[Same format]

### Action 3: [One-sentence finding]
[Same format]

If fewer than 3 issues were found, include only the issues that exist — do not invent findings to fill the slots.

---

**REQUIREMENTS**:
- Reference exact locations (function names, line numbers) for every finding
- Every finding MUST include a failure scenario (what breaks, not just what's wrong)
- Every recommendation MUST include a working code fix
- Do NOT include style, formatting, or naming feedback — linters handle those
- If a requested focus area has no issues, say so explicitly""",
            input_schema={
                "code": str,
                "language": str,
                "context_section": str,
                "focus_areas": str
            },
            constraints=Constraints(
                must_include=[
                    "orientation phase showing understanding of the code before critique",
                    "risk assessment with impact, likelihood, and blast radius for each finding",
                    "concrete code examples for fixes",
                    "failure scenarios for each finding"
                ],
                must_not_include=[
                    "style, formatting, or naming convention feedback",
                    "vague generalities without specific locations",
                    "criticisms without constructive solutions",
                    "invented findings when no real issues exist"
                ],
                style_guide="Use markdown formatting with code blocks and risk assessment tables"
            )
        )

    DEFAULT_FOCUS_AREAS: ClassVar[list[str]] = [
        "correctness", "security", "performance", "design",
        "resilience", "testing", "maintainability"
    ]

    def _render_context_section(self, context):
        """Render optional context section."""
        if context:
            return f"\n**ADDITIONAL CONTEXT**: {context}\n"
        return ""

    def _render_focus_areas(self, focus_areas):
        """Format focus areas list."""
        if isinstance(focus_areas, list):
            return ", ".join(focus_areas)
        return str(focus_areas)

    def build_context(
        self, code="", language="Python", context=None,
        focus_areas=None, output_format="structured", **kwargs
    ):
        """
        Build context for code review (without executing).

        Args:
            code: The code to review
            language: Programming language ("Python", "JavaScript", "Go", etc.)
            context: Optional context about the code's purpose or what changed
            focus_areas: Dimensions to review. Any subset of: correctness,
                security, performance, design, resilience, testing,
                maintainability. Default: all 7 dimensions.
            output_format: How to present results — ``"structured"`` (default)
                | ``"narrative"`` | ``"brief"`` | ``"actionable"``
                | ``"json"`` | ``"table"``
            **kwargs: Additional options

        Returns:
            Context object ready for export/use
        """
        if context is None:
            context = ""
        if focus_areas is None:
            focus_areas = self.DEFAULT_FOCUS_AREAS
        if output_format not in VALID_OUTPUT_FORMATS:
            raise ValueError(
                f"Invalid output_format {output_format!r}. "
                f"Choose from: {sorted(VALID_OUTPUT_FORMATS)}"
            )
        context_section = self._render_context_section(context)
        focus_areas_str = self._render_focus_areas(focus_areas)

        kwargs.pop('context_section', None)

        ctx = super().build_context(
            code=code,
            language=language,
            context_section=context_section,
            focus_areas=focus_areas_str,
            **kwargs
        )

        fmt = get_format_directive(output_format)
        if fmt and ctx.directive:
            ctx.directive = Directive(content=ctx.directive.content + fmt)
            ctx.metadata["output_format"] = output_format

        return ctx

    def execute(
        self,
        provider="gemini",
        code="",
        language="Python",
        context=None,
        focus_areas=None,
        output_format="structured",
        **kwargs
    ):
        """
        Execute code review.

        Args:
            provider: LLM provider to use ("gemini", "openai", "anthropic")
            code: The code to review
            language: Programming language ("Python", "JavaScript", "Go", etc.)
            context: Optional context about the code's purpose or what changed
            focus_areas: Dimensions to review. Any subset of: correctness,
                security, performance, design, resilience, testing,
                maintainability. Default: all 7 dimensions.
            output_format: How to present results — ``"structured"`` (default)
                | ``"narrative"`` | ``"brief"`` | ``"actionable"``
                | ``"json"`` | ``"table"``
            **kwargs: Additional provider options

        Returns:
            ProviderResponse with the review
        """
        if context is None:
            context = ""
        if focus_areas is None:
            focus_areas = self.DEFAULT_FOCUS_AREAS

        provider_params = {
            "model", "temperature", "max_tokens", "top_p",
            "frequency_penalty", "presence_penalty", "stop",
            "user", "api_key", "base_url",
        }
        provider_kwargs = {k: v for k, v in kwargs.items() if k in provider_params}

        ctx = self.build_context(
            code=code,
            language=language,
            context=context,
            focus_areas=focus_areas,
            output_format=output_format,
        )
        return ctx.execute(provider=provider, **provider_kwargs)
