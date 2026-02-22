"""
ErrorDetectionFramework Pattern (Enterprise)

Systematically identify mistakes, biases, and reasoning flaws.
Implements self-explanation and debiasing strategies.

Research Foundation:
- Chi, M. T. H., et al. (1989). Self-explanations. Cognitive Science, 13(2), 145-182.
- Tversky, A., & Kahneman, D. (1974). Judgment under uncertainty: Heuristics and biases. Science, 185(4157), 1124-1131.
- Lilienfeld, S. O., et al. (2009). Giving debiasing away. Perspectives on Psychological Science, 4(4), 390-398.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class ErrorDetectionFramework(Pattern):
    """
    Systematically detect errors, biases, and flaws in reasoning or work.
    
    Implements:
    - Self-explanation (Chi et al. 1989)
    - Cognitive bias identification (Kahneman & Tversky)
    - Error taxonomy and detection strategies
    
    Use Cases:
    - Code review (find bugs)
    - Argument analysis (find logical flaws)
    - Decision review (find biases)
    - Writing review (find errors)
    - Math/calculation checking
    
    Example:
        >>> from mycontext.templates.enterprise.metacognition import ErrorDetectionFramework
        >>> 
        >>> pattern = ErrorDetectionFramework()
        >>> result = pattern.execute(
        ...     provider="gemini",
        ...     work_to_check="My implementation of quicksort",
        ...     domain="programming"
        ... )
    
    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are an error detection specialist and critical thinking expert. "
        "Systematically identify mistakes, biases, and reasoning flaws.\n\n"
        "Work to Check: {work_to_check}\n"
        "Domain: {domain}\n"
        "{context_section}\n\n"
        "Apply systematic error detection: (1) Self-explanation check — explain each "
        "part step-by-step to detect gaps in understanding. (2) Domain-specific error "
        "checklist — check for conceptual, procedural, computational, and logical "
        "errors typical in this domain. (3) Cognitive bias scan — check for "
        "confirmation bias, anchoring, availability heuristic, overconfidence, "
        "hindsight bias, and sunk cost fallacy. (4) For each error found, specify "
        "type, location, evidence, severity (critical/major/minor), and fix.\n\n"
        "Provide verification strategies to catch remaining errors and prevention "
        "recommendations for future work.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="error_detection_framework",
            description="Systematically identify mistakes, biases, and reasoning flaws",
            version="1.0.0",
            tags=["metacognition", "enterprise", "error-detection", "debugging"],
            metadata={
                "category": "metacognition",
                "license": "enterprise",
                "tier": "enterprise"
            },
            guidance=Guidance(
                role="Error Detection Specialist and Critical Thinking Expert",
                rules=[
                    "Use systematic error detection strategies (self-explanation, checklists, bias awareness)",
                    "Check for domain-specific error types",
                    "Distinguish error types: conceptual, procedural, computational, logical",
                    "Identify cognitive biases (confirmation, anchoring, availability, etc.)",
                    "Provide specific evidence for each error found"
                ],
                style="thorough, systematic, specific, constructive, bias-aware"
            ),
            directive_template="""**ERROR DETECTION ANALYSIS**

**WORK TO CHECK**: {work_to_check}

**DOMAIN**: {domain}

{error_types_section}

---

## SYSTEMATIC ERROR DETECTION

### 1. SELF-EXPLANATION CHECK (Chi et al. 1989)

**Purpose**: Explain the work step-by-step to detect gaps in understanding.

For each part of the work:
- Can you explain WHY this step/component exists?
- Can you explain HOW it works?
- Can you explain WHEN it applies?
- Are there any parts you can't fully explain?

**Gaps in explanation** (what you can't explain fully):
[List any parts that are unclear or unjustified]

---

### 2. ERROR TYPE CHECKLIST

{error_type_checklist}

---

### 3. COGNITIVE BIAS CHECK

**Common biases that lead to errors** (Kahneman & Tversky):

| Bias | Description | Evidence in this work? |
|------|-------------|------------------------|
| **Confirmation bias** | Seeking info that confirms beliefs | [Yes/No + Evidence] |
| **Anchoring** | Over-relying on first information | [Yes/No + Evidence] |
| **Availability** | Judging by easily recalled examples | [Yes/No + Evidence] |
| **Overconfidence** | Excessive certainty in judgments | [Yes/No + Evidence] |
| **Hindsight bias** | "I knew it all along" | [Yes/No + Evidence] |
| **Sunk cost fallacy** | Continuing due to past investment | [Yes/No + Evidence] |

---

### 4. SPECIFIC ERRORS FOUND

For each error:

**ERROR #1:**
- **Type**: [Conceptual / Procedural / Computational / Logical / Bias]
- **Location**: [Where in the work?]
- **Description**: [What's wrong?]
- **Evidence**: [How do you know it's an error?]
- **Severity**: [Critical / Major / Minor]
- **Fix**: [How to correct it?]

**ERROR #2:**
[Repeat format...]

---

### 5. VERIFICATION STRATEGIES

**Recommended checks to catch remaining errors:**
1. [Specific verification method]
2. [Another method]
3. [Another method]

**Confidence in error detection:**
- Likelihood of missed errors: [Low / Medium / High]
- Areas needing additional review: [Specify]

---

### 6. ERROR PREVENTION

**How to avoid these errors in future:**
- **Process improvements**: [What to do differently]
- **Checklist items**: [What to verify each time]
- **Warning signs**: [Early indicators of these errors]

**Remember**: The goal is not just to find errors, but to understand WHY they occurred and how to prevent them.""",
            input_schema={
                "work_to_check": str,
                "domain": str,
                "error_types_section": str,
                "error_type_checklist": str
            },
            constraints=Constraints(
                must_include=[
                    "specific_errors_with_evidence",
                    "error_types",
                    "cognitive_biases",
                    "prevention_strategies"
                ],
                must_not_include=[
                    "vague_criticisms",
                    "errors_without_evidence"
                ],
                style_guide="Be specific with evidence. Distinguish error types. Explain WHY something is an error."
            )
        )

    def _get_error_checklist(self, domain: str) -> str:
        """Get domain-specific error checklist."""

        checklists = {
            "programming": """
**Programming-Specific Errors:**
- [ ] **Logic errors**: Does the algorithm produce correct results?
- [ ] **Edge cases**: What happens with empty input, null, max/min values?
- [ ] **Off-by-one errors**: Array indices, loop bounds correct?
- [ ] **Type errors**: Correct data types used throughout?
- [ ] **Null/undefined handling**: Are null checks present?
- [ ] **Performance issues**: Time/space complexity acceptable?
- [ ] **Concurrency**: Race conditions, deadlocks possible?
- [ ] **Error handling**: Exceptions caught and handled?
- [ ] **API misuse**: Libraries used correctly?
- [ ] **Security**: Input validation, SQL injection, XSS?
            """,

            "writing": """
**Writing-Specific Errors:**
- [ ] **Grammar**: Subject-verb agreement, tense consistency?
- [ ] **Spelling**: Typos, wrong word forms?
- [ ] **Punctuation**: Commas, periods, quotes correct?
- [ ] **Clarity**: Ambiguous pronouns, unclear references?
- [ ] **Logic**: Argument flow makes sense?
- [ ] **Evidence**: Claims supported with sources?
- [ ] **Structure**: Paragraphs organized logically?
- [ ] **Tone**: Appropriate for audience?
- [ ] **Redundancy**: Unnecessary repetition?
- [ ] **Factual accuracy**: Are facts correct?
            """,

            "math": """
**Mathematical Errors:**
- [ ] **Arithmetic**: Calculations correct?
- [ ] **Sign errors**: Negative/positive signs correct?
- [ ] **Algebraic manipulation**: Steps valid?
- [ ] **Order of operations**: PEMDAS followed?
- [ ] **Units**: Consistent throughout?
- [ ] **Fractions/decimals**: Conversions correct?
- [ ] **Equation solving**: Each step justified?
- [ ] **Proof logic**: Each implication valid?
- [ ] **Boundary conditions**: Edge cases considered?
- [ ] **Assumptions**: Stated and valid?
            """,

            "reasoning": """
**Logical Reasoning Errors:**
- [ ] **Invalid inference**: Conclusions follow from premises?
- [ ] **False assumptions**: Are assumptions correct?
- [ ] **Circular reasoning**: Conclusion assumes what it proves?
- [ ] **False dichotomy**: Only two options when more exist?
- [ ] **Hasty generalization**: Sample size sufficient?
- [ ] **Post hoc fallacy**: Correlation vs. causation?
- [ ] **Ad hominem**: Attacking person not argument?
- [ ] **Straw man**: Misrepresenting opponent's position?
- [ ] **Appeal to authority**: Expert opinion appropriate?
- [ ] **Slippery slope**: Chain of causation justified?
            """,
        }

        return checklists.get(domain.lower(), """
**General Error Checklist:**
- [ ] **Factual accuracy**: Are facts correct?
- [ ] **Logical consistency**: Do parts contradict?
- [ ] **Completeness**: Anything missing?
- [ ] **Clarity**: Is it understandable?
- [ ] **Assumptions**: Are they valid?
- [ ] **Evidence**: Claims supported?
        """)

    def build_context(
        self,
        work_to_check="",
        domain="",
        known_error_types="",
        **kwargs
    ):
        """
        Build context for error detection.
        
        Args:
            work_to_check: The work/reasoning to check for errors
            domain: Domain (e.g., "programming", "writing", "math", "reasoning")
            known_error_types: Optional specific error types to look for
            **kwargs: Additional options
        
        Returns:
            Context object ready for use
        """
        error_types_section = f"**SPECIFIC ERROR TYPES TO CHECK**: {known_error_types}" if known_error_types else ""
        error_type_checklist = self._get_error_checklist(domain)

        kwargs.pop('error_types_section', None)
        kwargs.pop('error_type_checklist', None)

        return super().build_context(
            work_to_check=work_to_check,
            domain=domain,
            error_types_section=error_types_section,
            error_type_checklist=error_type_checklist,
            **kwargs
        )

    def execute(
        self,
        provider="gemini",
        work_to_check="",
        domain="",
        known_error_types="",
        **kwargs
    ):
        """
        Execute error detection framework.
        
        Args:
            provider: LLM provider
            work_to_check: Work to check for errors
            domain: Domain of the work
            known_error_types: Optional specific error types to check
            **kwargs: Additional provider options
        
        Returns:
            ProviderResponse with error analysis
        """
        error_types_section = f"**SPECIFIC ERROR TYPES TO CHECK**: {known_error_types}" if known_error_types else ""
        error_type_checklist = self._get_error_checklist(domain)

        kwargs.pop('error_types_section', None)
        kwargs.pop('error_type_checklist', None)

        return super().execute(
            provider=provider,
            work_to_check=work_to_check,
            domain=domain,
            error_types_section=error_types_section,
            error_type_checklist=error_type_checklist,
            **kwargs
        )


__all__ = ["ErrorDetectionFramework"]
