"""
StockFlowAnalyzer Pattern (Enterprise)

Understand accumulations (stocks) and rates of change (flows) in systems.

Research Foundation:
- Forrester, J. W. (1961). Industrial Dynamics. MIT Press.
- Sterman, J. D. (2000). Business Dynamics: Systems Thinking and Modeling for a Complex World.
- Sweeney, L. B. & Sterman, J. D. (2000). Bathtub dynamics: initial results of a systems
  thinking inventory. System Dynamics Review.

License: Enterprise
"""

from typing import Optional
from mycontext import Pattern, Guidance, Directive, Constraints


class StockFlowAnalyzer(Pattern):
    """
    Analyze systems through the lens of stocks (accumulations) and flows (rates of change).

    The bathtub metaphor: stocks are the water level, inflows are the faucet,
    outflows are the drain. The stock only changes when inflow != outflow.

    Use Cases:
    - Inventory and supply chain management
    - Cash flow and financial modeling
    - Technical debt accumulation analysis
    - Workforce planning (hiring vs attrition)
    - Environmental analysis (carbon stocks, resource depletion)

    Example:
        >>> from mycontext.templates.enterprise.systems_thinking import StockFlowAnalyzer
        >>>
        >>> pattern = StockFlowAnalyzer()
        >>> context = pattern.build_context(
        ...     system="Technical debt in a growing codebase",
        ...     focus="How tech debt accumulates from shortcuts and depletes from refactoring"
        ... )

    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are a system dynamics expert specializing in stock-flow modeling. "
        "Analyze accumulations and rates of change in the given system.\n\n"
        "System: {system}\n"
        "Focus: {focus}\n"
        "{context_section}\n\n"
        "Perform stock-flow analysis: (1) Identify all stocks (accumulations) with "
        "units and current levels. (2) Map all inflows and outflows for each stock "
        "with estimated rates (units/time). (3) Calculate net flow and predict "
        "trajectory — growing, shrinking, or stable. (4) Estimate time constants: "
        "time to double, halve, or reach equilibrium. (5) Identify feedback "
        "connections where stock levels influence their own flows. (6) Highlight "
        "common stock-flow reasoning errors people make with this system.\n\n"
        "Use precise language: stocks have levels (units), flows have rates "
        "(units/time). Recommend short-term flow adjustments and long-term "
        "structural changes.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="stock_flow_analyzer",
            description="Analyze accumulations (stocks) and rates of change (flows)",
            version="1.0.0",
            tags=["systems-thinking", "enterprise", "stock-flow", "dynamics"],
            metadata={
                "category": "systems_thinking",
                "license": "enterprise",
                "tier": "enterprise",
            },
            guidance=Guidance(
                role="System Dynamics Expert specializing in stock-flow modeling and bathtub dynamics",
                rules=[
                    "Identify ALL stocks (accumulations) and their units",
                    "Map ALL inflows and outflows for each stock",
                    "Stocks can only change through their flows — never instantaneously",
                    "Explain the bathtub dynamics: what happens when inflow > outflow and vice versa",
                    "Identify feedback loops that connect flows back to stocks",
                    "Calculate or estimate time constants (how long to fill/drain)",
                    "Highlight where people commonly make stock-flow errors",
                ],
                style="precise, quantitative where possible, uses bathtub metaphor for clarity",
            ),
            directive_template="""**STOCK-FLOW ANALYSIS**

**SYSTEM**: {system}

**FOCUS**: {focus}

{context_section}

---

## 1. STOCK IDENTIFICATION

Stocks are accumulations — things that build up or deplete over time.

| Stock | Description | Units | Current Level (est.) | Desired Level |
|-------|------------|-------|---------------------|---------------|
| [Stock 1] | [What accumulates?] | [Units] | [Current estimate] | [Target] |

**Key insight**: Stocks create inertia — they can't change instantly, only through flows.

---

## 2. FLOW MAPPING

For each stock, map all inflows (increase the stock) and outflows (decrease the stock):

### Stock: [Stock 1]

**Inflows** (what fills the stock):

| Inflow | Rate | Units/Time | Controlled By | Variable/Fixed |
|--------|------|-----------|---------------|----------------|
| [Inflow 1] | [Rate estimate] | [units/period] | [Who/what controls this?] | [Variable / Relatively fixed] |

**Outflows** (what drains the stock):

| Outflow | Rate | Units/Time | Controlled By | Variable/Fixed |
|---------|------|-----------|---------------|----------------|
| [Outflow 1] | [Rate estimate] | [units/period] | [Who/what controls this?] | [Variable / Relatively fixed] |

[Repeat for each stock...]

---

## 3. STOCK-FLOW DIAGRAM

```
                    [Inflow 1]        [Inflow 2]
                        │                 │
                        ▼                 ▼
                 ┌─────────────────────────────┐
 [Rate] ──────► │         STOCK 1              │ ──────► [Rate]
 units/time     │     [Current Level]          │         units/time
                │         [Units]              │
                └─────────────────────────────┘
                        │                 │
                        ▼                 ▼
                   [Outflow 1]       [Outflow 2]
```

[Draw for each stock in the system]

---

## 4. BATHTUB DYNAMICS

The fundamental stock-flow equation: **Stock Change = Inflows − Outflows**

### Current State Analysis

| Stock | Total Inflow Rate | Total Outflow Rate | Net Change | Trajectory |
|-------|-------------------|-------------------|------------|------------|
| [Stock 1] | [X units/period] | [Y units/period] | [X−Y units/period] | [↑ Growing / ↓ Shrinking / → Stable] |

### Scenario Analysis

**If inflows increase by 20%**:
- [Stock 1]: [New trajectory, time to reach critical level]

**If outflows increase by 20%**:
- [Stock 1]: [New trajectory, time to reach target level]

**If both stop (inflow = outflow = 0)**:
- [Stock 1]: [Stock remains at current level — stocks persist without flows]

---

## 5. TIME CONSTANTS & RESPONSE TIMES

How long does it take for stocks to change significantly?

| Stock | Time to Double (at current net inflow) | Time to Halve (at current net outflow) | Residence Time |
|-------|---------------------------------------|----------------------------------------|----------------|
| [Stock 1] | [Estimate] | [Estimate] | [Stock / Outflow rate] |

**Implication**: [What the time constants mean for management — e.g., "Tech debt takes 6 months to significantly reduce even with aggressive refactoring"]

---

## 6. FEEDBACK CONNECTIONS

How do stocks influence their own flows? (This creates feedback loops)

| Stock | Influences Which Flow? | Direction | Creates Loop |
|-------|----------------------|-----------|-------------|
| [Stock 1 level] | [Inflow/Outflow X] | [Higher stock → higher/lower flow] | [R/B loop] |

**Self-reinforcing dynamics**: [Where does a growing stock accelerate its own growth?]
**Self-correcting dynamics**: [Where does a growing stock slow its own growth?]

---

## 7. COMMON STOCK-FLOW ERRORS

People frequently make these mistakes with this system:

| Error | Explanation | Reality |
|-------|------------|---------|
| **Confusing stocks with flows** | [Example: "We need to reduce our [stock] rate"] | [Stocks have levels, flows have rates — different units] |
| **Ignoring inertia** | [Example: "If we stop [inflow], [stock] will drop immediately"] | [Stocks persist — outflows must drain them over time] |
| **Overlooking outflows** | [Example: "We need more [inflow]"] | [Often reducing outflows is easier/cheaper than increasing inflows] |

---

## 8. RECOMMENDATIONS

### Short-term (adjust flows within existing structure):
- [Intervention 1]: [Which flow to adjust, by how much, expected stock impact]

### Medium-term (add new flows or modify existing ones):
- [Intervention 2]: [Structural change to flow system]

### Long-term (redesign stock-flow architecture):
- [Intervention 3]: [Fundamental restructuring]

---

## 9. SUMMARY

**Critical stock**: [Which stock matters most?]
**Dominant dynamic**: [Is this stock growing, shrinking, or oscillating?]
**Time horizon**: [How long before stock reaches critical/target level?]
**Key lever**: [Which flow is most controllable and impactful?]
**Counter-intuitive insight**: [What's not obvious from surface-level observation?]""",
            input_schema={
                "system": str,
                "focus": str,
                "context_section": str,
            },
            constraints=Constraints(
                must_include=[
                    "stock_identification_with_units",
                    "inflow_outflow_mapping",
                    "bathtub_dynamics_analysis",
                    "time_constants",
                ],
                must_not_include=[
                    "confusing_stocks_with_flows",
                    "stocks_without_units",
                    "flows_without_rates",
                ],
                style_guide="Use stock-flow language precisely. Stocks have levels (units), flows have rates (units/time).",
            ),
        )

    def build_context(self, system="", focus="", context="", **kwargs):
        """Build context for stock-flow analysis."""
        context_section = f"**ADDITIONAL CONTEXT**: {context}" if context else ""
        kwargs.pop("context_section", None)
        return super().build_context(
            system=system, focus=focus, context_section=context_section, **kwargs
        )

    def execute(self, provider="gemini", system="", focus="", context="", **kwargs):
        """Execute stock-flow analysis."""
        return super().execute(
            provider=provider, system=system, focus=focus, context=context, **kwargs
        )


__all__ = ["StockFlowAnalyzer"]
