"""
DifferentialDiagnoser Pattern (Enterprise)

Medical-style differential diagnosis for any domain.
Systematic evaluation of competing hypotheses.

Research Foundation:
- Elstein, A. S., et al. (1978). Medical problem solving: An analysis of clinical reasoning.
- Croskerry, P. (2009). A universal model of diagnostic reasoning.
- Norman, G. (2005). Research in clinical reasoning: past history and current trends.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class DifferentialDiagnoser(Pattern):
    """
    Systematic evaluation of competing diagnostic hypotheses.

    Process:
    1. Generate differential (list of possibilities)
    2. Rank by likelihood
    3. Test each hypothesis
    4. Narrow down to most likely
    5. Verify with evidence

    Use Cases:
    - Technical troubleshooting
    - Business problem diagnosis
    - Medical diagnosis
    - System debugging

    Example:
        >>> from mycontext.templates.enterprise.diagnostic import DifferentialDiagnoser
        >>>
        >>> pattern = DifferentialDiagnoser()
        >>> result = pattern.execute(
        ...     provider="openai",
        ...     presenting_problem="Website response time increased 10x",
        ...     observed_data="Affects all users, started 3 days ago, no code changes"
        ... )

    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are an expert diagnostic reasoning specialist. Apply medical-style differential "
        "diagnosis methodology to systematically evaluate competing hypotheses.\n\n"
        "Presenting Problem: {presenting_problem}\n"
        "Observed Data: {observed_data}\n"
        "Domain: {domain}\n\n"
        "Deliver your analysis:\n"
        "(1) Generate a comprehensive differential — common causes first, then uncommon and rare.\n"
        "(2) Rank hypotheses by likelihood based on available evidence (for and against each).\n"
        "(3) Identify discriminating tests that would distinguish between top hypotheses.\n"
        "(4) Analyze each leading hypothesis in detail — mechanism, fit with data, gaps.\n"
        "(5) Narrow the differential with updated probabilities after evaluating evidence.\n"
        "(6) State the primary diagnosis with confidence level and a verification strategy.\n\n"
        "Be systematic and evidence-based. Consider multiple hypotheses before narrowing.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="differential_diagnoser",
            description="Medical-style differential diagnosis for any domain",
            version="1.0.0",
            tags=["diagnostic", "enterprise", "differential", "troubleshooting"],
            metadata={"category": "diagnostic", "license": "enterprise", "tier": "enterprise"},
            guidance=Guidance(
                role="Diagnostic Reasoning Expert",
                rules=[
                    "Generate comprehensive differential (list all possibilities)",
                    "Use evidence to rank likelihood",
                    "Test most likely hypotheses first",
                    "Consider zebras but look for horses (common before rare)",
                    "Verify diagnosis with confirmatory evidence",
                ],
                style="systematic, evidence-based, methodical, thorough",
            ),
            directive_template="""**DIFFERENTIAL DIAGNOSIS**

**PRESENTING PROBLEM**: {presenting_problem}

**OBSERVED DATA**: {observed_data}

{domain_section}

---

## INITIAL DIFFERENTIAL (All Possibilities)

**Generate comprehensive list of potential causes**:

**Common causes** (likely - look for horses first):
1. [Common cause 1]
   - Frequency: [How often this occurs]
   - Typical presentation: [How it usually manifests]

2. [Common cause 2]
3. [Common cause 3]

**Uncommon causes** (possible but less likely):
4. [Uncommon cause 1]
5. [Uncommon cause 2]

**Rare causes** (zebras - consider but unlikely):
6. [Rare cause 1]
7. [Rare cause 2]

**Initial list**: [7-10 possibilities]

---

## HYPOTHESIS RANKING

**Rank by likelihood based on current evidence**:

| Rank | Hypothesis | Likelihood | Supporting Evidence | Against Evidence |
|------|------------|------------|-------------------|------------------|
| 1 | [Most likely cause] | High | [Evidence for] | [Evidence against] |
| 2 | [Second likely] | Medium-High | [Evidence] | [Counter-evidence] |
| 3 | [Third likely] | Medium | [Evidence] | [Counter-evidence] |
| 4 | [Fourth] | Low-Medium | [Evidence] | [Counter-evidence] |
| 5+ | [Others] | Low | [Minimal evidence] | [Reasons unlikely] |

---

## DISCRIMINATING FEATURES

**What would help distinguish between top hypotheses?**

**Test/Question 1**: [Specific test or data to check]
- If result is X: Supports hypothesis [A]
- If result is Y: Supports hypothesis [B]
- If result is Z: Supports hypothesis [C]

**Test/Question 2**: [Another discriminating test]
- Expected for A: [Result]
- Expected for B: [Different result]
- Expected for C: [Different result]

**Most informative test**: [Which single test narrows differential most]

---

## DETAILED HYPOTHESIS ANALYSIS

### HYPOTHESIS 1: [Most likely cause]

**Likelihood**: [High/Medium/Low] ([%] probability)

**Supporting evidence**:
- Finding 1: [Observation that supports this]
- Finding 2: [Another supporting fact]
- Pattern match: [How observed data fits this hypothesis]

**Evidence against**:
- Finding X: [Observation inconsistent with this]
- Expected but missing: [What we'd expect to see but don't]

**Mechanism**: [How this cause would produce observed problem]

**Fit with data**: [Good/Partial/Poor]

---

### HYPOTHESIS 2: [Second likely]

[Same detailed analysis]

---

### HYPOTHESIS 3: [Third likely]

[Same detailed analysis]

---

## DIAGNOSTIC TESTS

**Conduct tests to narrow differential**:

**Test 1**: [Specific investigation]
- **Purpose**: Distinguish between [A vs B]
- **Method**: [How to test]
- **Expected results**:
  - If A: [Result X]
  - If B: [Result Y]
- **Actual result**: [What we find]
- **Interpretation**: [What this tells us]

**Test 2**: [Another test]
[Same structure]

**Test 3**: [Confirmatory test]
[Same structure]

---

## NARROWING THE DIFFERENTIAL

**After tests, update probabilities**:

| Hypothesis | Initial % | After Tests | Status |
|------------|-----------|-------------|---------|
| [Hypothesis A] | [X%] | [Y%] | [Ruled in/out/uncertain] |
| [Hypothesis B] | [X%] | [Y%] | [Status] |
| [Hypothesis C] | [X%] | [Y%] | [Status] |

**Ruled out**: [Hypotheses eliminated by evidence]
**Ruled in**: [Most likely diagnosis]
**Still uncertain**: [Need more data]

---

## PRIMARY DIAGNOSIS

**Most likely cause**: **[Diagnosis]**

**Confidence**: [High/Medium/Low] ([%])

**Supporting evidence summary**:
1. [Key evidence 1]
2. [Key evidence 2]
3. [Key evidence 3]

**How this explains all findings**:
- Symptom A: [Explained by diagnosis because...]
- Symptom B: [Explained by...]
- Observation C: [Consistent with...]

**What doesn't fit perfectly**: [Any unexplained observations]

---

## ALTERNATIVE DIAGNOSES

**Keep in differential** (less likely but possible):

**Alternative 1**: [Diagnosis]
- Probability: [%]
- Why still possible: [Reason]
- Watch for: [What would increase likelihood]

**Alternative 2**: [Diagnosis]
- Probability: [%]
- Monitoring plan: [What to track]

---

## VERIFICATION STRATEGY

**Confirm primary diagnosis**:

**Confirmatory test**: [Definitive test]
- Expected result if diagnosis correct: [X]
- Timeline: [When to test]

**Treatment test**: [Try intervention]
- If diagnosis correct: [Problem should improve]
- If diagnosis wrong: [No improvement or worsening]
- Timeframe: [When to evaluate]

---

## TREATMENT/SOLUTION PLAN

**Based on primary diagnosis**:

**Immediate action**:
1. [Fix for root cause]
2. [Symptomatic relief if needed]

**Definitive solution**:
- [Long-term fix]
- [Implementation plan]

**Monitoring**:
- Track: [Metrics to follow]
- Expect: [Improvement timeline]
- If no improvement: [Revisit diagnosis]

---

## COGNITIVE BIASES TO AVOID

**Common diagnostic errors**:

❌ **Anchoring**: Fixating on first hypothesis
❌ **Confirmation bias**: Only seeing evidence that supports preferred diagnosis
❌ **Premature closure**: Stopping search too early
❌ **Availability bias**: Thinking of recent/memorable causes first
❌ **Framing effect**: Being influenced by how problem was described

✅ **Mitigation**: Consider alternatives, seek disconfirming evidence, systematic approach

---

## FOLLOW-UP PLAN

**After implementing solution**:

**Week 1**: [Check these metrics]
**Week 2**: [Verify improvement]
**Month 1**: [Confirm problem resolved]

**If problem persists**:
- Revisit differential
- Consider alternatives
- Gather more data

**Success criteria**: [How to know diagnosis was correct]""",
            input_schema={"presenting_problem": str, "observed_data": str, "domain_section": str},
            constraints=Constraints(
                must_include=[
                    "comprehensive_differential",
                    "hypothesis_ranking",
                    "discriminating_tests",
                    "primary_diagnosis",
                ],
                must_not_include=["premature_closure", "single_hypothesis"],
                style_guide="Systematic and evidence-based. Multiple hypotheses. Test and verify. Medical-style rigor.",
            ),
        )

    def build_context(self, presenting_problem="", observed_data="", domain="", **kwargs):
        """Build context for differential diagnosis."""
        domain_section = f"**DOMAIN**: {domain}" if domain else ""
        kwargs.pop("domain_section", None)

        return super().build_context(
            presenting_problem=presenting_problem,
            observed_data=observed_data,
            domain_section=domain_section,
            **kwargs,
        )

    def execute(
        self, provider="openai", presenting_problem="", observed_data="", domain="", **kwargs
    ):
        """Execute differential diagnosis."""
        domain_section = f"**DOMAIN**: {domain}" if domain else ""
        kwargs.pop("domain_section", None)

        return super().execute(
            provider=provider,
            presenting_problem=presenting_problem,
            observed_data=observed_data,
            domain_section=domain_section,
            **kwargs,
        )


__all__ = ["DifferentialDiagnoser"]
