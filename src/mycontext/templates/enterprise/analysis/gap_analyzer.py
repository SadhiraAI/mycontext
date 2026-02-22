"""
Gap Analyzer - Identify gaps between current and desired state

Systematic gap identification and closure planning.
Based on gap analysis methodologies and strategic planning.
"""


from mycontext.foundation import Constraints, Guidance
from mycontext.structure import Pattern


class GapAnalyzer(Pattern):
    """
    Identify and analyze gaps systematically.
    
    Identifies:
    - Current vs. desired state gaps
    - Capability gaps
    - Knowledge gaps
    - Resource gaps
    - Performance gaps
    
    Based on: Gap analysis and needs assessment
    
    Example:
        >>> analyzer = GapAnalyzer()
        >>> context = analyzer.build_context(
        ...     current_state="Current team capabilities",
        ...     desired_state="World-class AI engineering team"
        ... )
    
    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "You are an expert gap analysis strategist. Conduct a thorough gap "
        "analysis between the current and desired states:\n\n"
        "Current State: {current_state}\n"
        "Desired State: {desired_state}\n"
        "Focus Area: {focus_area}\n"
        "{context_section}\n\n"
        "Apply this methodology: "
        "(1) Define both states clearly - describe current reality and desired "
        "future with measurable attributes and success criteria. "
        "(2) Identify gaps - catalog capability, knowledge, resource, process, "
        "and technology gaps between the two states. "
        "(3) Quantify gaps - measure each gap's size with concrete metrics, "
        "percentages, or maturity levels where possible. "
        "(4) Analyze root causes - determine why each gap exists and what "
        "systemic factors sustain it. "
        "(5) Prioritize - rank gaps by business impact, urgency, and "
        "feasibility of closing, identifying critical-path dependencies. "
        "(6) Create bridge plans - develop specific, phased strategies to "
        "close each critical gap with timelines, resources, and milestones.\n\n"
        "Be realistic about effort and specific about actions.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="gap_analyzer",
            description="Identify and analyze gaps",
            guidance=Guidance(
                role="Expert Gap Analysis and Strategic Planning Specialist",
                rules=[
                    "Clearly define both states",
                    "Quantify gaps where possible",
                    "Prioritize critical gaps",
                    "Provide actionable bridge plans",
                    "Consider root causes of gaps"
                ],
                style="analytical, systematic, solution-focused"
            ),
            directive_template="""Analyze gaps between states:

**CURRENT STATE**: {current_state}

**DESIRED STATE**: {desired_state}

{context_section}

**AREA OF FOCUS**: {focus_area}

Comprehensive gap analysis:

1. **STATE DEFINITIONS**
   
   **Current State (As-Is)**:
   - Description: [Where we are now]
   - Key characteristics: [Current attributes]
   - Strengths: [What's working]
   - Weaknesses: [What's lacking]
   - Metrics: [Current measurements]
   
   **Desired State (To-Be)**:
   - Description: [Where we want to be]
   - Key characteristics: [Target attributes]
   - Success criteria: [How we'll know we're there]
   - Timeline: [When we want to achieve this]
   - Metrics: [Target measurements]

2. **GAP IDENTIFICATION**
   What's missing between states?
   
   **Capability Gaps**:
   - Gap 1: [Missing capability]
     - Current: [What we have]
     - Need: [What we need]
     - Size: [Large/Medium/Small]
   
   - Gap 2: [Another capability]
     - [Same structure]
   
   **Knowledge Gaps**:
   - Gap 1: [Missing knowledge]
   - Gap 2: [Skills shortage]
   
   **Resource Gaps**:
   - Gap 1: [Missing resources]
   - Gap 2: [Insufficient assets]
   
   **Process Gaps**:
   - Gap 1: [Missing processes]
   - Gap 2: [Ineffective workflows]
   
   **Technology Gaps**:
   - Gap 1: [Missing tools]
   - Gap 2: [Outdated systems]

3. **GAP QUANTIFICATION**
   Measure each critical gap:
   
   | Gap | Current | Target | Difference | % Gap |
   |-----|---------|--------|------------|-------|
   | [Gap 1] | [Value] | [Goal] | [Delta] | [%] |
   | [Gap 2] | [Value] | [Goal] | [Delta] | [%] |

4. **ROOT CAUSE ANALYSIS**
   Why do these gaps exist?
   
   - Gap 1 root causes:
     - Cause A: [Underlying reason]
     - Cause B: [Contributing factor]
   
   - Gap 2 root causes:
     - [Same structure]

5. **GAP PRIORITIZATION**
   
   **Critical Gaps** (Must close first):
   - Gap: [Name]
     - Impact if not closed: [Consequence]
     - Urgency: [Why now]
     - Difficulty: [Effort needed]
   
   **Important Gaps** (Should close soon):
   - [List with reasoning]
   
   **Nice-to-Have Gaps** (Can defer):
   - [List with reasoning]

6. **DEPENDENCIES**
   Which gaps must be closed before others?
   
   - Close [Gap A] before [Gap B]
     - Reason: [Dependency explanation]
   
   - [Gap C] and [Gap D] can be parallel
   
   **Critical Path**: [Sequence of gaps to close]

7. **BRIDGE STRATEGIES**
   How to close each gap:
   
   **Gap 1: [Name]**
   - Strategy: [Approach]
   - Actions:
     1. [Specific action]
     2. [Next action]
     3. [Following action]
   - Resources needed: [What's required]
   - Timeline: [Duration]
   - Cost estimate: [Budget]
   - Success metric: [How to measure]
   
   [Repeat for each critical gap]

8. **QUICK WINS**
   Gaps that can be closed easily:
   
   - Quick Win 1: [Low effort, visible impact]
     - Action: [What to do]
     - Timeline: [Days/weeks]
   
   - Quick Win 2: [Another easy win]

9. **RISK ASSESSMENT**
   Risks in gap closure:
   
   - Risk 1: [What could go wrong]
     - Likelihood: [High/Med/Low]
     - Impact: [Effect]
     - Mitigation: [How to reduce risk]
   
   - Risk 2: [Another risk]

10. **PHASED IMPLEMENTATION PLAN**
    
    **Phase 1** (0-3 months):
    - Close gaps: [A, B, C]
    - Key milestones: [Achievements]
    - Resources: [What's needed]
    
    **Phase 2** (3-6 months):
    - Close gaps: [D, E, F]
    - Key milestones: [Progress markers]
    - Resources: [Requirements]
    
    **Phase 3** (6-12 months):
    - Close gaps: [G, H, I]
    - Key milestones: [Final goals]
    - Resources: [Needs]

11. **SUCCESS METRICS**
    How to measure gap closure:
    
    - Metric 1: [Measurement]
      - Current: [Baseline]
      - Target: [Goal]
      - Frequency: [How often to check]
    
    - Metric 2: [Another KPI]

12. **RESOURCE REQUIREMENTS**
    What's needed to close gaps:
    
    **Budget**:
    - Total: [Amount]
    - Breakdown: [By category]
    
    **People**:
    - Roles needed: [Positions]
    - Time commitment: [FTEs]
    
    **Technology**:
    - Tools: [What to acquire]
    - Systems: [Infrastructure needs]
    
    **Training**:
    - Programs: [Required training]
    - Investment: [Cost/time]

13. **INTERIM SOLUTIONS**
    Temporary bridges while closing gaps:
    
    - Workaround 1: [Temporary solution]
      - Duration: [How long]
      - Limitations: [What it doesn't solve]
    
    - Workaround 2: [Another stopgap]

14. **PROGRESS TRACKING**
    
    **Review cadence**: [How often to check]
    
    **Dashboard metrics**:
    - [Key indicators to track]
    
    **Go/No-Go decision points**:
    - Checkpoint 1: [When/what]
    - Checkpoint 2: [Assessment point]

**OUTPUT FORMAT**: Actionable gap analysis with phased closure plan.""",
            input_schema={
                "current_state": str,
                "desired_state": str,
                "context_section": str,
                "focus_area": str
            },
            constraints=Constraints(
                must_include=[
                    "quantified_gaps",
                    "prioritization",
                    "bridge_strategies",
                    "phased_plan"
                ],
                style_guide="Be realistic about effort, specific about actions"
            )
        )

    def _render_context_section(self, context: str | None) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""

    def build_context(
        self,
        current_state: str = "",
        desired_state: str = "",
        focus_area: str = "general",
        context: str | None = None,
        **kwargs
    ):
        context_section = self._render_context_section(context)

        return super().build_context(
            current_state=current_state,
            desired_state=desired_state,
            focus_area=focus_area,
            context_section=context_section,
            **kwargs
        )

    def execute(
        self,
        provider: str = "openai",
        current_state: str = "",
        desired_state: str = "",
        focus_area: str = "general",
        context: str | None = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            current_state=current_state,
            desired_state=desired_state,
            focus_area=focus_area,
            context=context,
            **kwargs
        )
