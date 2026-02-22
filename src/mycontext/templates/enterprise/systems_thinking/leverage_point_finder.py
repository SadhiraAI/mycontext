"""
LeveragePointFinder Pattern (Enterprise)

Find high-impact intervention points using Meadows' 12 leverage points framework.

Research Foundation:
- Meadows, D. H. (1999). Leverage Points: Places to Intervene in a System.
- Meadows, D. H. (2008). Thinking in Systems: A Primer.
- Abson, D. J. et al. (2017). Leverage points for sustainability transformation.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class LeveragePointFinder(Pattern):
    """
    Identify high-impact intervention points using Meadows' 12 leverage points.

    Analyzes a system from weakest to strongest leverage:
    12. Constants/parameters → 1. Transcending paradigms

    Use Cases:
    - Organizational transformation strategy
    - Policy design and reform
    - Product strategy and growth
    - Process improvement prioritization

    Example:
        >>> from mycontext.templates.enterprise.systems_thinking import LeveragePointFinder
        >>>
        >>> pattern = LeveragePointFinder()
        >>> context = pattern.build_context(
        ...     system="Enterprise sales: Lead gen → Qualification → Demo → Proposal → Close",
        ...     goal="Double close rate from 15% to 30%"
        ... )

    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are a systems intervention expert applying Donella Meadows' leverage "
        "points framework. Find high-impact intervention points.\n\n"
        "System: {system}\n"
        "Goal: {goal}\n"
        "{context_section}\n\n"
        "Apply Meadows' 12 leverage points from weakest to strongest: "
        "(12) Constants/parameters, (11) Buffer sizes, (10) Stock-flow structure, "
        "(9) Delay lengths, (8) Balancing feedback strength, (7) Reinforcing "
        "feedback gain, (6) Information flow structure, (5) System rules, "
        "(4) Self-organization power, (3) System goals, (2) Paradigm/mindset, "
        "(1) Transcending paradigms.\n\n"
        "For each relevant level, propose a concrete intervention with expected "
        "impact and feasibility. Rank the top 3 by impact-to-effort ratio and "
        "suggest implementation sequencing. Warn about counter-intuitive dynamics "
        "and unintended consequences.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="leverage_point_finder",
            description="Identify high-impact intervention points using Meadows' 12 leverage points",
            version="1.0.0",
            tags=["systems-thinking", "enterprise", "leverage-points", "intervention"],
            metadata={
                "category": "systems_thinking",
                "license": "enterprise",
                "tier": "enterprise",
            },
            guidance=Guidance(
                role="Systems Intervention Expert applying Donella Meadows' leverage points framework",
                rules=[
                    "Evaluate ALL 12 leverage points from weakest to strongest",
                    "For each point, assess relevance and feasibility in this specific system",
                    "Provide concrete, actionable interventions — not generic advice",
                    "Rank the top 3 interventions by impact-to-effort ratio",
                    "Warn about counter-intuitive dynamics and unintended consequences",
                ],
                style="strategic, evidence-based, ordered from shallow to deep interventions",
            ),
            directive_template="""**LEVERAGE POINT ANALYSIS**

**SYSTEM**: {system}

**GOAL**: {goal}

{context_section}

---

Apply Meadows' 12 leverage points framework, ordered from **weakest** (easiest but least impactful) to **strongest** (hardest but most transformative):

## SHALLOW LEVERAGE (Easy to implement, limited impact)

### 12. CONSTANTS, PARAMETERS, NUMBERS
*Adjusting quantities within existing structures*
- **Relevant parameters**: [What numbers could be changed?]
- **Possible intervention**: [Specific change]
- **Expected impact**: [Low / Medium] — Why: [Explanation]

### 11. BUFFER SIZES
*Stabilizing stocks relative to their flows*
- **System buffers**: [What buffers exist? Inventory, cash reserves, capacity?]
- **Possible intervention**: [Increase/decrease which buffer?]
- **Expected impact**: [Low / Medium] — Why: [Explanation]

### 10. STRUCTURE OF MATERIAL STOCKS AND FLOWS
*Physical structure — pipes, roads, networks*
- **Current structure**: [How does material/information physically flow?]
- **Possible intervention**: [Restructure how?]
- **Expected impact**: [Low / Medium] — Why: [Explanation]

## MODERATE LEVERAGE (Requires more effort, meaningful impact)

### 9. LENGTH OF DELAYS
*How quickly does the system respond to change?*
- **Key delays**: [Where are the time lags?]
- **Possible intervention**: [Shorten or lengthen which delay?]
- **Expected impact**: [Medium] — Why: [Explanation]
- **Warning**: [Delays too short can cause oscillation]

### 8. STRENGTH OF BALANCING FEEDBACK LOOPS
*How strongly does the system self-correct?*
- **Existing balancing loops**: [What keeps the system in check?]
- **Possible intervention**: [Strengthen or weaken which loop?]
- **Expected impact**: [Medium / High] — Why: [Explanation]

### 7. GAIN AROUND REINFORCING FEEDBACK LOOPS
*How fast do virtuous/vicious cycles spin?*
- **Existing reinforcing loops**: [What drives growth or decline?]
- **Possible intervention**: [Amplify or dampen which loop?]
- **Expected impact**: [Medium / High] — Why: [Explanation]

### 6. STRUCTURE OF INFORMATION FLOWS
*Who has access to what information?*
- **Information gaps**: [Who doesn't know what they need to?]
- **Possible intervention**: [Create/redirect which information flow?]
- **Expected impact**: [High] — Why: [Explanation]

## DEEP LEVERAGE (Harder to change, high impact)

### 5. RULES OF THE SYSTEM
*Incentives, constraints, punishments, permissions*
- **Current rules**: [What rules govern behavior?]
- **Possible intervention**: [Change which rule?]
- **Expected impact**: [High] — Why: [Explanation]

### 4. POWER TO ADD/CHANGE/SELF-ORGANIZE
*Ability of the system to evolve its own structure*
- **Self-organization capacity**: [Can the system adapt?]
- **Possible intervention**: [Enable what kind of self-organization?]
- **Expected impact**: [High] — Why: [Explanation]

### 3. GOALS OF THE SYSTEM
*What the system is trying to achieve*
- **Current goals**: [Explicit and implicit goals?]
- **Possible intervention**: [Redefine goals to what?]
- **Expected impact**: [Very High] — Why: [Explanation]

### 2. MINDSET OR PARADIGM
*The shared beliefs from which the system arises*
- **Current paradigm**: [What assumptions does the system rest on?]
- **Possible intervention**: [Challenge which assumption?]
- **Expected impact**: [Very High] — Why: [Explanation]

### 1. POWER TO TRANSCEND PARADIGMS
*Recognizing that no paradigm is "true"*
- **Applicability**: [Is paradigm-level change relevant here?]
- **Expected impact**: [Transformative if applicable]

---

## TOP 3 RECOMMENDED INTERVENTIONS

| Rank | Leverage Point | Intervention | Impact | Feasibility | Timeline |
|------|---------------|-------------|--------|-------------|----------|
| 1 | [#] [Name] | [Specific action] | [High/Very High] | [High/Med/Low] | [Timeframe] |
| 2 | [#] [Name] | [Specific action] | [High/Very High] | [High/Med/Low] | [Timeframe] |
| 3 | [#] [Name] | [Specific action] | [Medium/High] | [High/Med/Low] | [Timeframe] |

**Sequencing**: [Which to do first, second, third — and why]

## WARNINGS & UNINTENDED CONSEQUENCES

- [Intervention X] may trigger [unexpected effect] because [reason]
- [Intervention Y] has a delay of [timeframe] before effects are visible""",
            input_schema={
                "system": str,
                "goal": str,
                "context_section": str,
            },
            constraints=Constraints(
                must_include=[
                    "all_12_leverage_points",
                    "concrete_interventions",
                    "ranked_recommendations",
                ],
                must_not_include=[
                    "generic_advice",
                    "skipped_leverage_points",
                ],
                style_guide="Order by effectiveness (12→1). Provide specific, actionable interventions.",
            ),
        )

    def build_context(self, system="", goal="", context="", **kwargs):
        """Build context for leverage point analysis."""
        context_section = f"**ADDITIONAL CONTEXT**: {context}" if context else ""
        kwargs.pop("context_section", None)
        return super().build_context(
            system=system, goal=goal, context_section=context_section, **kwargs
        )

    def execute(self, provider="gemini", system="", goal="", context="", **kwargs):
        """Execute leverage point analysis."""
        return super().execute(
            provider=provider, system=system, goal=goal, context=context, **kwargs
        )


__all__ = ["LeveragePointFinder"]
