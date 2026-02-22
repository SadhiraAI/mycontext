"""
Bottleneck Identifier (Enterprise) - Find performance bottlenecks and constraints

Systematic identification of bottlenecks, constraints, and limiting factors.
Based on theory of constraints and systems optimization.

License: Enterprise
"""


from mycontext import Constraints, Guidance, Pattern


class BottleneckIdentifier(Pattern):
    """
    Identify bottlenecks and constraints systematically.
    
    Finds:
    - Process bottlenecks
    - Resource constraints
    - System limitations
    - Throughput limiters
    - Performance blockers
    
    Based on: Theory of Constraints (Goldratt) and systems analysis
    
    Example:
        >>> identifier = BottleneckIdentifier()
        >>> context = identifier.build_context(
        ...     system="Software deployment pipeline",
        ...     goal="Reduce deployment time"
        ... )
    
    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are an expert systems analyst specializing in performance optimization and the "
        "Theory of Constraints. Identify bottlenecks limiting system throughput.\n\n"
        "System: {system}\n"
        "Goal: {goal}\n"
        "{context_section}\n\n"
        "Deliver your analysis:\n"
        "(1) Map the system flow — key steps, inputs, outputs, and current performance.\n"
        "(2) Measure throughput at each step — identify utilization, queue times, and capacity.\n"
        "(3) Pinpoint the primary bottleneck with evidence (highest utilization, longest queues).\n"
        "(4) Identify secondary bottlenecks and hidden constraints.\n"
        "(5) Propose exploitation strategies (optimize the constraint without adding resources).\n"
        "(6) Provide an optimization roadmap: quick wins, subordination, and elevation options.\n\n"
        "Be data-driven and systematic. Focus on the true constraint, not symptoms.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="bottleneck_identifier",
            description="Find bottlenecks and constraints",
            version="1.0.0",
            tags=["problem_solving", "enterprise", "bottleneck", "optimization"],
            metadata={"category": "problem_solving", "license": "enterprise", "tier": "enterprise"},
            guidance=Guidance(
                role="Expert Systems Analyst and Performance Optimization Specialist",
                rules=[
                    "Focus on the constraint",
                    "Measure throughput at each step",
                    "Identify the true bottleneck, not symptoms",
                    "Consider upstream and downstream effects",
                    "Optimize the constraint first"
                ],
                style="analytical, systematic, data-driven"
            ),
            directive_template="""Identify bottlenecks in:

**SYSTEM/PROCESS**: {system}

{context_section}

**OPTIMIZATION GOAL**: {goal}

Bottleneck identification:

1. **SYSTEM OVERVIEW**
   - Description: [What the system does]
   - Inputs: [What goes in]
   - Outputs: [What comes out]
   - Key steps: [Major stages]
   - Current performance: [Baseline metrics]
   - Desired performance: [Target]

2. **PROCESS MAPPING**
   Map the flow:
   
   Step 1: [Name]
   - Duration: [Time]
   - Throughput: [Rate]
   - Capacity: [Maximum]
   - Utilization: [% of capacity]
   
   Step 2: [Name]
   - [Same metrics]
   
   Step 3: [Name]
   - [Same metrics]
   
   [Continue for all steps]
   
   **Flow Diagram**:
   [Input] → [Step 1] → [Step 2] → [Step 3] → [Output]

3. **THROUGHPUT ANALYSIS**
   
   | Step | Throughput | Capacity | Utilization | Queue/Wait |
   |------|------------|----------|-------------|------------|
   | Step 1 | [Rate] | [Max] | [%] | [Time] |
   | Step 2 | [Rate] | [Max] | [%] | [Time] |
   | Step 3 | [Rate] | [Max] | [%] | [Time] |
   
   **Lowest Throughput**: [Which step]
   **Highest Utilization**: [Which step]

4. **PRIMARY BOTTLENECK**
   
   **Identified Constraint**: [Specific step/resource]
   
   **Evidence**:
   - Utilization: [Near 100%]
   - Queue buildup: [Work waiting here]
   - Impact: [Limits overall throughput]
   - Duration: [Longest step time]
   
   **Type of Bottleneck**:
   - [ ] Process bottleneck
   - [ ] Resource constraint
   - [ ] Capacity limit
   - [ ] Knowledge gap
   - [ ] Policy constraint

5. **SECONDARY BOTTLENECKS**
   Other constraints to address:
   
   - Bottleneck 2: [Name]
     - Impact: [Effect on system]
     - Priority: [High/Med/Low]
   
   - Bottleneck 3: [Name]
     - [Same structure]

6. **ROOT CAUSE ANALYSIS**
   Why is this the bottleneck?
   
   **Primary Bottleneck Causes**:
   - Cause 1: [Underlying reason]
   - Cause 2: [Contributing factor]
   - Cause 3: [Additional issue]
   
   **Systemic Issues**:
   - [Deeper problems]

7. **IMPACT QUANTIFICATION**
   
   **Current Cost of Bottleneck**:
   - Time cost: [Delay added]
   - Financial cost: [Money impact]
   - Opportunity cost: [Lost potential]
   - Quality cost: [Errors/issues]
   
   **Downstream Effects**:
   - Impact on [Step X]: [Effect]
   - Impact on [Resource Y]: [Consequence]
   - Impact on [Output Z]: [Result]

8. **CONSTRAINT EXPLOITATION**
   Maximize throughput of bottleneck:
   
   **Quick Wins** (No additional resources):
   - Action 1: [Optimize current process]
   - Action 2: [Reduce waste]
   - Action 3: [Better scheduling]
   
   **Expected Gain**: [Improvement %]

9. **SUBORDINATION STRATEGY**
   Adjust upstream/downstream to bottleneck:
   
   **Upstream Adjustments**:
   - [Don't overproduce to bottleneck]
   - [Feed bottleneck optimally]
   
   **Downstream Adjustments**:
   - [Process bottleneck output efficiently]

10. **ELEVATION OPTIONS**
    Increase bottleneck capacity:
    
    **Option A: Add Resources**
    - What: [More of constraint resource]
    - Cost: [Investment needed]
    - Gain: [Expected improvement]
    - Timeline: [Implementation time]
    
    **Option B: Improve Process**
    - What: [Better method]
    - Cost: [Investment]
    - Gain: [Expected improvement]
    - Timeline: [How long]
    
    **Option C: Eliminate Step**
    - What: [Remove or automate]
    - Cost: [Investment]
    - Gain: [Breakthrough improvement]
    - Timeline: [Duration]
    
    **Recommended**: [Which option]

11. **TEMPORARY WORKAROUNDS**
    While fixing bottleneck:
    
    - Workaround 1: [Short-term solution]
      - Relief: [How much help]
      - Duration: [How long viable]
    
    - Workaround 2: [Another stopgap]

12. **HIDDEN BOTTLENECKS**
    What might emerge after fixing primary:
    
    - Next constraint: [Likely next bottleneck]
      - Current capacity: [Status]
      - Will become issue when: [Trigger]
      - Prepare by: [Proactive step]

13. **OPTIMIZATION ROADMAP**
    
    **Phase 1 - Exploit** (Immediate):
    - [ ] [Quick optimization 1]
    - [ ] [Quick optimization 2]
    - Expected: [X% improvement]
    
    **Phase 2 - Subordinate** (This month):
    - [ ] [Adjust upstream]
    - [ ] [Adjust downstream]
    - Expected: [Y% improvement]
    
    **Phase 3 - Elevate** (This quarter):
    - [ ] [Increase capacity]
    - [ ] [Redesign process]
    - Expected: [Z% improvement]
    
    **Total Improvement**: [Overall gain]

14. **SUCCESS METRICS**
    How to measure improvement:
    
    - Primary metric: [Key indicator]
      - Current: [Baseline]
      - Target: [Goal]
    
    - Secondary metrics: [Supporting KPIs]
    
    **Review frequency**: [How often to check]

**OUTPUT FORMAT**: Data-driven bottleneck analysis with actionable optimization plan.""",
            input_schema={
                "system": str,
                "context_section": str,
                "goal": str
            },
            constraints=Constraints(
                must_include=[
                    "primary_bottleneck",
                    "impact_quantification",
                    "optimization_roadmap"
                ],
                style_guide="Be systematic and evidence-based"
            )
        )

    def _render_context_section(self, context: str | None) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""

    def build_context(
        self,
        system: str = "",
        goal: str = "Improve throughput",
        context: str | None = None,
        **kwargs
    ):
        context_section = self._render_context_section(context)

        return super().build_context(
            system=system,
            goal=goal,
            context_section=context_section,
            **kwargs
        )

    def execute(
        self,
        provider: str = "openai",
        system: str = "",
        goal: str = "Improve throughput",
        context: str | None = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            system=system,
            goal=goal,
            context=context,
            **kwargs
        )
