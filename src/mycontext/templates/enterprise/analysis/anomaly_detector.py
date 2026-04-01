"""
Anomaly Detector - Detect anomalies and outliers

Systematic anomaly detection and investigation.
Based on statistical analysis and pattern recognition.
"""

from mycontext.foundation import Constraints, Guidance
from mycontext.structure import Pattern


class AnomalyDetector(Pattern):
    """
    Detect and analyze anomalies.

    Identifies:
    - Statistical outliers
    - Pattern breaks
    - Unexpected events
    - System anomalies

    Based on: Anomaly detection and statistical analysis

    Example:
        >>> detector = AnomalyDetector()
        >>> context = detector.build_context(
        ...     data="Server response times over past week",
        ...     baseline="Average 200ms"
        ... )

    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "You are an expert anomaly detection analyst. Perform a systematic "
        "anomaly analysis on the following data:\n\n"
        "Data: {data}\n"
        "Baseline: {baseline}\n"
        "{context_section}\n\n"
        "Apply this methodology: "
        "(1) Define the normal baseline - establish expected ranges, averages, "
        "and standard deviations for the data. "
        "(2) Identify anomalies - detect all data points or patterns that "
        "deviate significantly from the baseline. "
        "(3) Quantify deviations - measure how far each anomaly deviates from "
        "normal in concrete terms (magnitude, percentage, sigma). "
        "(4) Classify severity - rate each anomaly as Critical, High, Medium, "
        "or Low based on deviation magnitude and potential impact. "
        "(5) Investigate root causes - hypothesize the most likely causes for "
        "each anomaly with supporting evidence and probability estimates. "
        "(6) Recommend actions - provide specific, prioritized steps to "
        "address each anomaly and prevent recurrence.\n\n"
        "Be specific, evidence-based, and actionable in your analysis.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="anomaly_detector",
            description="Detect anomalies and outliers",
            guidance=Guidance(
                role="Expert Data Analyst and Anomaly Detection Specialist",
                rules=[
                    "Define normal baseline",
                    "Quantify deviation",
                    "Investigate causes",
                    "Distinguish signal from noise",
                    "Recommend action",
                ],
                style="analytical, methodical, inquisitive",
            ),
            directive_template="""Detect anomalies in:

**DATA**: {data}

**BASELINE**: {baseline}

{context_section}

Anomaly detection:

1. **BASELINE DEFINITION**
   Normal behavior:
   - Typical range: [Min-Max]
   - Average: [Mean]
   - Standard deviation: [σ]
   - Expected pattern: [Description]

2. **ANOMALY IDENTIFICATION**
   Detected anomalies:
   
   **Anomaly 1**:
   - Value: [Observed]
   - Expected: [Normal range]
   - Deviation: [How far from normal]
   - Severity: [High/Med/Low]
   - When: [Timestamp]
   
   **Anomaly 2**:
   - [Same structure]

3. **ANOMALY CLASSIFICATION**
   - Type: [Point/Contextual/Collective]
   - Frequency: [One-time/Recurring]
   - Direction: [Higher/Lower than normal]

4. **ROOT CAUSE INVESTIGATION**
   Potential causes:
   - Cause 1: [Hypothesis]
     - Evidence: [Supporting data]
     - Likelihood: [Probability]
   
   - Cause 2: [Another possibility]

5. **IMPACT ASSESSMENT**
   - Affected systems: [What's impacted]
   - Severity: [How serious]
   - Urgency: [How quickly to address]

6. **RECOMMENDATION**
   - Action: [What to do]
   - Priority: [How urgent]
   - Investigation: [What to check next]
   - Prevention: [How to avoid future]

**OUTPUT FORMAT**: Clear anomaly analysis with actionable next steps.""",
            input_schema={"data": str, "baseline": str, "context_section": str},
            constraints=Constraints(
                must_include=["anomalies", "causes", "recommendations"],
                style_guide="Be specific and evidence-based",
            ),
        )

    def _render_context_section(self, context: str | None) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""

    def build_context(
        self, data: str = "", baseline: str = "", context: str | None = None, **kwargs
    ):
        context_section = self._render_context_section(context)

        return super().build_context(
            data=data, baseline=baseline, context_section=context_section, **kwargs
        )

    def execute(
        self,
        provider: str = "openai",
        data: str = "",
        baseline: str = "",
        context: str | None = None,
        **kwargs,
    ):
        return super().execute(
            provider=provider, data=data, baseline=baseline, context=context, **kwargs
        )
