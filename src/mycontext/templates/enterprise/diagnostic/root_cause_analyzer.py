"""
RootCauseAnalyzer Pattern (Enterprise)

Systematic root cause analysis using Five Whys, Ishikawa diagrams, and fault tree analysis.
Go beyond symptoms to find underlying causes.

Research Foundation:
- Ishikawa, K. (1968). Guide to quality control.
- Ohno, T. (1988). Toyota Production System: Beyond large-scale production.
- Rooney, J. J., & Vanden Heuvel, L. N. (2004). Root cause analysis for beginners.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class DiagnosticRootCauseAnalyzer(Pattern):
    """
    Systematic root cause analysis for problems.

    Methods:
    - Five Whys (iterative questioning)
    - Ishikawa/Fishbone diagram (categories of causes)
    - Fault tree analysis (logical breakdown)

    Use Cases:
    - Problem-solving
    - Incident analysis
    - Quality improvement
    - Debugging (technical and organizational)

    Example:
        >>> from mycontext.templates.enterprise.diagnostic import RootCauseAnalyzer
        >>>
        >>> pattern = RootCauseAnalyzer()
        >>> result = pattern.execute(
        ...     provider="openai",
        ...     problem="Production line defect rate increased 300%",
        ...     symptoms="High rejection rate, customer complaints"
        ... )

    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are an expert root cause analysis specialist. Go beyond symptoms to find the "
        "underlying causes using systematic diagnostic methodologies.\n\n"
        "Problem: {problem}\n"
        "Symptoms: {symptoms}\n\n"
        "Deliver your analysis:\n"
        "(1) Define the problem precisely — observable issue, impact, frequency, and severity.\n"
        "(2) Apply the Five Whys — ask 'Why?' iteratively until reaching the root cause.\n"
        "(3) Conduct Ishikawa (Fishbone) analysis across categories: People, Process, Equipment, "
        "Materials, Environment, and Measurement.\n"
        "(4) Identify and verify candidate root causes — test each with evidence and logic.\n"
        "(5) Map the causal chain from root causes through intermediate effects to symptoms.\n"
        "(6) Recommend corrective actions for each root cause and preventive measures to stop recurrence.\n\n"
        "Distinguish symptoms from causes. Find actionable root causes, not just descriptions.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="diagnostic_root_cause_analyzer",
            description="Systematic root cause analysis using Five Whys and Ishikawa",
            version="1.0.0",
            tags=["diagnostic", "enterprise", "root-cause", "troubleshooting"],
            metadata={"category": "diagnostic", "license": "enterprise", "tier": "enterprise"},
            guidance=Guidance(
                role="Root Cause Analysis Expert",
                rules=[
                    "Distinguish symptoms from root causes",
                    "Ask 'Why?' repeatedly until reaching root cause",
                    "Consider multiple causal categories (Ishikawa: Man, Machine, Material, Method, Environment)",
                    "Find actionable root causes (that can be addressed)",
                    "Verify root cause with evidence",
                ],
                style="systematic, thorough, evidence-based, actionable",
            ),
            directive_template="""**ROOT CAUSE ANALYSIS**

**PROBLEM**: {problem}

**SYMPTOMS OBSERVED**: {symptoms}

---

## PROBLEM DEFINITION

**What is the problem exactly?**
- Observable issue: [Specific, measurable problem]
- Impact: [Consequences]
- Frequency: [How often]
- Severity: [How serious]

**What is NOT the problem** (clarify boundaries):
- [What this isn't]

---

## METHOD 1: FIVE WHYS

**Start with the problem and ask "Why?" five times**:

**Problem**: {problem}

**Why 1**: Why is this happening?
→ **Answer**: [First-level cause]

**Why 2**: Why is [first-level cause] happening?
→ **Answer**: [Second-level cause]

**Why 3**: Why is [second-level cause] happening?
→ **Answer**: [Third-level cause]

**Why 4**: Why is [third-level cause] happening?
→ **Answer**: [Fourth-level cause]

**Why 5**: Why is [fourth-level cause] happening?
→ **Answer**: [ROOT CAUSE]

**Verification**: If we fix [root cause], will the problem go away? [Yes/No]

---

## METHOD 2: ISHIKAWA (FISHBONE) DIAGRAM

**Analyze causes by category**:

### CATEGORY 1: PEOPLE (Man)
**Human factors**:
- Skills: [Skill gaps or errors]
- Training: [Training deficiencies]
- Behavior: [Actions or inactions]
- Communication: [Information failures]

**Potential root causes in this category**:
- [Cause 1]
- [Cause 2]

---

### CATEGORY 2: PROCESS (Method)
**Process/procedure factors**:
- Procedures: [Process flaws]
- Standards: [Missing or unclear standards]
- Workflow: [Process design issues]
- Documentation: [Documentation problems]

**Potential root causes**:
- [Cause 1]
- [Cause 2]

---

### CATEGORY 3: EQUIPMENT (Machine)
**Equipment/technology factors**:
- Reliability: [Equipment failures]
- Maintenance: [Maintenance issues]
- Capacity: [Capability limitations]
- Age: [Obsolescence problems]

**Potential root causes**:
- [Cause 1]
- [Cause 2]

---

### CATEGORY 4: MATERIALS
**Input factors**:
- Quality: [Material quality issues]
- Availability: [Supply problems]
- Specifications: [Wrong materials]
- Suppliers: [Vendor problems]

**Potential root causes**:
- [Cause 1]
- [Cause 2]

---

### CATEGORY 5: ENVIRONMENT
**Environmental factors**:
- Physical: [Workspace conditions]
- Organizational: [Culture, structure]
- Market: [External pressures]
- Regulatory: [Compliance issues]

**Potential root causes**:
- [Cause 1]
- [Cause 2]

---

### CATEGORY 6: MEASUREMENT
**Measurement/information factors**:
- Data: [Data quality issues]
- Metrics: [Wrong metrics tracked]
- Visibility: [Lack of information]
- Timing: [Delayed feedback]

**Potential root causes**:
- [Cause 1]
- [Cause 2]

---

## ROOT CAUSE IDENTIFICATION

**Candidate root causes** (from all methods):
1. [Root cause 1]
   - Evidence: [What supports this]
   - Impact: [How this causes the problem]
   - Category: [Ishikawa category]

2. [Root cause 2]
   - Evidence: [Supporting data]
   - Impact: [Causal mechanism]
   - Category: [Category]

3. [Root cause 3]
   [Same structure]

---

## ROOT CAUSE VERIFICATION

**Test each candidate root cause**:

**Root Cause 1**: [Cause]

**Verification questions**:
- If we eliminate this, will problem go away? [Yes/No/Partially]
- Is this truly a cause, or just another symptom? [Cause/Symptom]
- Can we take action on this? [Yes/No]
- Is there evidence supporting this? [Strong/Weak]

**Verdict**: [Verified root cause / Need more investigation / Just a symptom]

[Repeat for each candidate]

---

## PRIMARY ROOT CAUSES

**Confirmed root causes** (verified):
1. **[Root Cause A]** ⭐ PRIMARY
   - Category: [Ishikawa category]
   - Impact: [How it causes problem]
   - Evidence: [Supporting data]
   - Addressability: [Can be fixed]

2. **[Root Cause B]** ⭐ CONTRIBUTING
   - Category: [Category]
   - Impact: [Contribution]
   - Evidence: [Data]

[May be multiple root causes - problems often have several]

---

## CAUSAL CHAIN

**How root causes → problem**:

```
[Root Cause A]
    ↓
[Intermediate effect 1]
    ↓
[Intermediate effect 2]
    ↓
[Symptom 1] + [Symptom 2]
    ↓
[PROBLEM]
```

**Explanation**: [Describe the causal chain step by step]

---

## CONTRIBUTING FACTORS

**Not root causes, but make problem worse**:

**Amplifying factors**:
- [Factor that magnifies the problem]
- [Another amplifier]

**Enabling factors**:
- [Condition that allows problem to occur]
- [Another enabler]

**These don't cause the problem, but addressing them may help**

---

## CORRECTIVE ACTIONS

**Address root causes directly**:

**For Root Cause A**:
- **Corrective action**: [Specific fix]
- **Implementation**: [How to do it]
- **Timeline**: [When]
- **Verification**: [How to confirm it worked]
- **Cost/effort**: [Resource requirement]

**For Root Cause B**:
[Same structure]

---

## PREVENTIVE ACTIONS

**Prevent recurrence**:

**Systemic changes**:
1. [Process improvement]
2. [System redesign]
3. [Control implementation]

**Monitoring**:
- Track: [Leading indicators]
- Alert if: [Early warning signs]
- Review: [Regular audits]

---

## VALIDATION PLAN

**Confirm root causes were correct**:

**If we're right** (correct root causes):
- Problem should: [Stop/Decrease significantly]
- Timeline: [Within X time]
- Metrics: [Specific improvements]

**If we're wrong** (missed real root cause):
- Problem will: [Persist/Recur]
- Indication: [How we'll know]
- Next step: [Repeat analysis with new information]

**Follow-up**: [When to check results]

---

## DOCUMENTATION

**Record for future reference**:
- Problem: [Description]
- Root causes found: [List]
- Actions taken: [Fixes implemented]
- Results: [Outcome]
- Lessons learned: [What we discovered]

**Purpose**: Build organizational memory, avoid repeating analysis""",
            input_schema={"problem": str, "symptoms": str},
            constraints=Constraints(
                must_include=[
                    "five_whys",
                    "ishikawa_categories",
                    "root_cause_verification",
                    "corrective_actions",
                ],
                must_not_include=["symptom_treating", "unverified_causes"],
                style_guide="Systematic and thorough. Distinguish symptoms from root causes. Multiple methods. Actionable solutions.",
            ),
        )

    def build_context(self, problem="", symptoms="", **kwargs):
        """Build context for root cause analysis."""
        return super().build_context(problem=problem, symptoms=symptoms, **kwargs)

    def execute(self, provider="openai", problem="", symptoms="", **kwargs):
        """Execute root cause analysis."""
        return super().execute(provider=provider, problem=problem, symptoms=symptoms, **kwargs)


RootCauseAnalyzer = DiagnosticRootCauseAnalyzer

__all__ = ["DiagnosticRootCauseAnalyzer", "RootCauseAnalyzer"]
