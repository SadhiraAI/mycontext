"""
CrossDomainSynthesizer Pattern (Enterprise)

Integrate insights from multiple domains to create novel solutions.
Apply knowledge from one field to problems in another.

Research Foundation:
- Gentner, D. (1983). Structure-mapping: A theoretical framework for analogy.
- Holyoak, K. J., & Thagard, P. (1995). Mental leaps: Analogy in creative thought.
- Root-Bernstein, R., & Root-Bernstein, M. (1999). Sparks of genius: The 13 thinking tools.

License: Enterprise
"""

from mycontext import Pattern, Guidance, Constraints

class CrossDomainSynthesizer(Pattern):
    """
    Synthesize insights across multiple domains.
    
    Process:
    - Identify parallel structures across domains
    - Map concepts from source to target domain
    - Generate novel insights through cross-pollination
    - Create innovative solutions
    
    Use Cases:
    - Innovation
    - Problem-solving
    - Strategy development
    - Research synthesis
    
    Example:
        >>> from mycontext.templates.enterprise.synthesis import CrossDomainSynthesizer
        >>> 
        >>> pattern = CrossDomainSynthesizer()
        >>> result = pattern.execute(
        ...     provider="openai",
        ...     target_problem="Improve customer retention",
        ...     source_domains="Biology (immune system), Psychology (habit formation)"
        ... )
    
    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are an expert in cross-domain innovation and analogical reasoning. "
        "Synthesize insights from multiple domains to generate novel solutions.\n\n"
        "Target Problem: {target_problem}\n"
        "Source Domains: {source_domains}\n\n"
        "Deliver your analysis:\n"
        "(1) For each source domain: identify key principles and map structural parallels to the target.\n"
        "(2) Create rigorous concept mappings — source domain elements to target domain equivalents.\n"
        "(3) Extract cross-domain patterns that appear across multiple source domains.\n"
        "(4) Construct deep analogies with structural alignment and testable inferences.\n"
        "(5) Generate synthesized solutions that combine insights from multiple domains.\n"
        "(6) Assess innovation potential — novelty, feasibility, and expected impact of each solution.\n"
        "(7) Recommend the most promising cross-domain solution with a validation approach.\n\n"
        "Seek deep structural similarities, not superficial connections.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="cross_domain_synthesizer",
            description="Integrate insights from multiple domains",
            version="1.0.0",
            tags=["synthesis", "enterprise", "cross-domain", "innovation"],
            metadata={
                "category": "synthesis",
                "license": "enterprise",
                "tier": "enterprise"
            },
            guidance=Guidance(
                role="Cross-Domain Innovation Expert",
                rules=[
                    "Identify deep structural similarities (not superficial)",
                    "Map concepts rigorously from source to target domain",
                    "Generate novel insights through analogical reasoning",
                    "Test applicability of cross-domain solutions",
                    "Combine insights from multiple domains"
                ],
                style="creative, rigorous, analogical, integrative"
            ),
            directive_template="""**CROSS-DOMAIN SYNTHESIS**

**TARGET PROBLEM** (what we're trying to solve): {target_problem}

**SOURCE DOMAINS** (where we'll draw insights): {source_domains}

---

## DOMAIN MAPPING

**For each source domain, map to target**:

### SOURCE DOMAIN 1: [Name]

**Key principles from this domain**:
1. [Principle 1]
2. [Principle 2]
3. [Principle 3]

**Structural mapping to target problem**:

| Source Domain Element | Target Domain Equivalent |
|----------------------|--------------------------|
| [Concept A in source] | [Maps to X in target] |
| [Concept B] | [Maps to Y] |
| [Mechanism C] | [Analogous to Z] |

**Insights from mapping**:
- [Insight 1: What this domain teaches about target problem]
- [Insight 2]

**Novel solution idea**:
- [Specific solution inspired by this domain]
- [How it would work in target domain]

---

### SOURCE DOMAIN 2: [Name]

[Same structure]

---

### SOURCE DOMAIN 3: [Name]

[Same structure]

---

## CROSS-DOMAIN INSIGHTS

**Patterns that emerge across domains**:

**Pattern 1**: [Common principle across multiple domains]
- Appears in [Domain A] as: [Example]
- Appears in [Domain B] as: [Example]
- **Universal principle**: [Abstract formulation]
- **Application to target**: [How to use this insight]

**Pattern 2**: [Another cross-domain pattern]
[Same analysis]

---

## ANALOGICAL REASONING

**Deep analogy construction**:

**Source**: [Well-understood domain]

**Target**: [Problem domain]

**Structural alignment**:
- Source structure: [How source domain works]
- Target structure: [How target domain works]
- Mapping: [Correspondence between structures]

**Inference**:
- In source domain: [What we know works]
- By analogy, in target domain: [What might work]
- **Novel hypothesis**: [Testable prediction]

---

## SYNTHESIZED SOLUTIONS

**Solution 1**: [Idea combining Domain A + Domain B]
- **From Domain A**: [Borrowed principle]
- **From Domain B**: [Borrowed mechanism]
- **Integration**: [How they combine]
- **Application**: [Specific implementation in target]
- **Expected outcome**: [What this would achieve]
- **Feasibility**: [High/Medium/Low]

**Solution 2**: [Another cross-domain solution]
[Same structure]

**Solution 3**: [Third synthesis]
[Same structure]

---

## INNOVATION ASSESSMENT

**Novelty**: [How new is this approach?]
- Precedents: [Has anything like this been tried?]
- Uniqueness: [What makes this different]

**Feasibility**: [Can this actually be implemented?]
- Resources needed: [Requirements]
- Technical challenges: [Obstacles]
- Time to implement: [Estimate]

**Potential impact**: [If successful, what's the upside?]
- Benefits: [Expected gains]
- Risks: [Possible downsides]

---

## CROSS-DOMAIN PRINCIPLES EXTRACTED

**Universal principles** (work in any domain):

1. **Principle**: [Abstract formulation]
   - Examples: [Domains where this appears]
   - Application: [How to use in target]

2. **Principle**: [Another universal]
   - Examples: [Instances]
   - Application: [Target use]

---

## TESTING CROSS-DOMAIN SOLUTIONS

**Validation approach**:

**Small-scale pilot**:
- Test: [How to test solution 1]
- Metrics: [Success criteria]
- Timeline: [Duration]

**Iterate based on results**:
- If successful: [Scale up]
- If failed: [Learn and adapt]

---

## DOMAIN EXPERT CONSULTATION

**Validate with experts from each domain**:

**Domain A expert**:
- Consult: [Expert in source domain]
- Verify: [Is our understanding of Domain A correct?]
- Ask: [Does our analogy hold?]

**Target domain expert**:
- Consult: [Expert in target]
- Verify: [Is cross-domain solution viable here?]

---

## SYNTHESIS SUMMARY

**Key insights from cross-domain analysis**:
1. [Major insight 1]
2. [Major insight 2]
3. [Major insight 3]

**Most promising solution**: [Which cross-domain idea]

**Why**: [Reasoning for selection]

**Next steps**: [How to pursue this]""",
            input_schema={
                "target_problem": str,
                "source_domains": str
            },
            constraints=Constraints(
                must_include=[
                    "domain_mapping",
                    "structural_alignment",
                    "novel_insights",
                    "synthesized_solutions"
                ],
                must_not_include=[
                    "superficial_analogies",
                    "forced_connections"
                ],
                style_guide="Creative and rigorous. Deep structural mapping. Novel but grounded solutions."
            )
        )
    
    def build_context(self, target_problem="", source_domains="", **kwargs):
        """Build context for cross-domain synthesis."""
        return super().build_context(
            target_problem=target_problem,
            source_domains=source_domains,
            **kwargs
        )
    
    def execute(self, provider="openai", target_problem="", source_domains="", **kwargs):
        """Execute cross-domain synthesis."""
        return super().execute(
            provider=provider,
            target_problem=target_problem,
            source_domains=source_domains,
            **kwargs
        )


__all__ = ["CrossDomainSynthesizer"]
