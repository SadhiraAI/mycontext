"""
Content Outliner Template - Create structured outlines for any content type.

Based on content strategy best practices and cognitive tools methodology.
Free tier template - part of mycontext open source.
"""

from mycontext import Pattern, Guidance, Directive, Constraints


class ContentOutliner(Pattern):
    """
    Generate comprehensive, structured outlines for articles, docs, presentations, etc.
    
    This template creates content outlines using proven content strategy principles:
    - Audience-first approach
    - Clear hierarchical structure
    - Logical flow and progression
    - Actionable section descriptions
    - Hooks, transitions, and CTAs
    
    Examples:
        >>> from mycontext.templates.free import ContentOutliner
        >>> 
        >>> outliner = ContentOutliner()
        >>> result = outliner.execute(
        ...     provider="gemini",
        ...     topic="Introduction to Context Engineering",
        ...     content_type="blog post",
        ...     target_length="2000 words",
        ...     audience="developers new to LLM applications"
        ... )
        >>> print(result.response)
    
    Free Template - Part of mycontext open source edition.
    """
    
    def __init__(self):
        super().__init__(
            name="content_outliner",
            guidance=Guidance(
                role="Expert Content Strategist and Technical Writer",
                rules=[
                    "Design outlines with audience needs and goals first",
                    "Create clear hierarchical structure (H1, H2, H3 levels)",
                    "Ensure logical flow from section to section",
                    "Include specific, actionable content for each section",
                    "Add hooks, transitions, and calls-to-action where appropriate",
                    "Balance depth with readability"
                ],
                style="structured, clear, strategic, audience-focused"
            ),
            directive_template="""Create a comprehensive outline for this content.

**TOPIC**: {topic}

**CONTENT TYPE**: {content_type}

**TARGET LENGTH**: {target_length}

**TARGET AUDIENCE**: {audience}

{context_section}

**PURPOSE**: {purpose}

Generate a detailed, actionable content outline:

## 1. CONTENT STRATEGY

**Primary Goal**:
- What this content aims to achieve: [Main objective]
- Success metrics: [How you'll know it worked]

**Audience Analysis**:
- **Who**: {audience}
- **What they know**: [Current knowledge level]
- **What they need**: [Knowledge gap or problem]
- **What they'll do**: [Desired action after reading]

**Key Message**:
- Core takeaway: [The one thing readers must remember]

**Tone & Style**:
- [Formal/Informal, Technical/Accessible, etc.]

## 2. CONTENT OUTLINE

### Title Options (3-5 compelling options):
1. [Working title 1] - [Why this works]
2. [Working title 2] - [Why this works]
3. [Working title 3] - [Why this works]

### Opening Hook (First 100 words)
**Hook Strategy**: [Question/Story/Statistic/Problem]
- Opening line: [Attention-grabbing first sentence]
- Problem/Question: [What hooks the reader]
- Promise: [What they'll learn/gain]

---

### Section 1: [Title] (~{section_length} words)

**Purpose**: [What this section accomplishes]

**Key Points**:
- [Main point 1]
- [Main point 2]
- [Main point 3]

**Content Elements**:
- Subsection A: [Specific content]
- Subsection B: [Specific content]
- Example: [Type of example to include]
- Visual: [Diagram/Code/Screenshot to add]

**Transition**: [How this leads to next section]

---

### Section 2: [Title] (~{section_length} words)

**Purpose**: [What this section accomplishes]

[Same structure as Section 1]

---

### Section 3: [Title] (~{section_length} words)

[Continue pattern for all major sections]

---

### [Add 3-7 main sections based on {target_length}]

---

### Conclusion: [Title] (~{conclusion_length} words)

**Summary Strategy**: [How to wrap up]

**Elements**:
- Recap: [Key points to reinforce]
- Implications: [Why this matters]
- Call to Action: [What reader should do next]

**Memorable Closing**: [Strong final thought]

## 3. SUPPORTING ELEMENTS

**Visual Assets Needed**:
1. [Chart/Diagram description]
2. [Code example or screenshot]
3. [Infographic or visual]

**Code Examples** (if applicable):
- Example 1: [What it demonstrates]
- Example 2: [What it demonstrates]

**Links & References**:
- Internal links: [Where to link within content]
- External resources: [Authoritative sources]
- Related reading: [Further exploration]

**SEO Keywords** (for digital content):
- Primary: [Main keyword]
- Secondary: [2-3 related terms]

## 4. CONTENT METADATA

**Estimated Word Count Breakdown**:
| Section | Words | % of Total |
|---------|-------|------------|
| Introduction | [N] | [%] |
| Section 1 | [N] | [%] |
| ... | ... | ... |
| Conclusion | [N] | [%] |
| **Total** | **{target_length}** | **100%** |

**Reading Time**: [X minutes at 200-250 words/min]

**Complexity Level**: [1-10 scale with justification]

## 5. PRODUCTION NOTES

**Research Required**:
- [Topic 1 to research]
- [Topic 2 to research]

**Subject Matter Experts to Consult**:
- [If applicable]

**Review Checklist**:
- [ ] Addresses audience needs
- [ ] Logical flow between sections
- [ ] Concrete examples throughout
- [ ] Clear action items
- [ ] Proofread and fact-checked

---

**REQUIREMENTS**:
- Outline should be specific enough to write from directly
- Each section has clear purpose and content description
- Flow is logical and builds toward conclusion
- Appropriate for {content_type} and {audience}
- Balances depth with {target_length}""",
            input_schema={
                "topic": str,
                "content_type": str,
                "target_length": str,
                "audience": str,
                "purpose": str,
                "context": str
            },
            constraints=Constraints(
                must_include=[
                    "content strategy",
                    "hierarchical outline with specific sections",
                    "word count breakdown",
                    "supporting elements (visuals, examples)"
                ],
                must_not_include=[
                    "vague section descriptions",
                    "missing transitions between sections"
                ],
                style_guide="Use clear hierarchy (###), specific content descriptions, word counts for sections"
            )
        )
    
    def _render_context_section(self, context):
        """Render optional context section."""
        if context:
            return f"\n**ADDITIONAL CONTEXT**: {context}\n"
        return ""
    
    def _calculate_section_lengths(self, target_length_str):
        """Estimate section lengths based on total."""
        # Simple parsing - extract number
        import re
        match = re.search(r'(\d+)', target_length_str)
        if match:
            total = int(match.group(1))
            # Rough distribution: intro 10%, sections 70%, conclusion 10%, buffer 10%
            section_length = int(total * 0.15)  # Each of ~5 sections
            conclusion_length = int(total * 0.10)
            return str(section_length), str(conclusion_length)
        return "200", "150"
    
    def execute(
        self,
        provider="gemini",
        topic="",
        content_type="blog post",
        target_length="1500 words",
        audience="general audience",
        purpose="educate and inform",
        context=None,
        temperature=0.7,
        **kwargs
    ):
        """
        Execute content outlining.
        
        Args:
            provider: LLM provider to use ("gemini", "openai", "anthropic")
            topic: The content topic
            content_type: Type of content ("blog post", "article", "documentation", 
                         "presentation", "tutorial", "whitepaper")
            target_length: Target length ("1500 words", "10 minutes", "20 slides", etc.)
            audience: Target audience description
            purpose: Primary purpose ("educate", "persuade", "inspire", "instruct", etc.)
            context: Optional additional context
            temperature: Moderate values (0.6-0.8) for creative but structured outlines
            **kwargs: Additional provider options
        
        Returns:
            ProviderResponse with the outline
        """
        # Provide defaults for optional fields
        if context is None:
            context = ""
        
        context_section = self._render_context_section(context)
        section_length, conclusion_length = self._calculate_section_lengths(target_length)
        
        return super().execute(
            provider=provider,
            topic=topic,
            content_type=content_type,
            target_length=target_length,
            audience=audience,
            purpose=purpose,
            context=context,
            context_section=context_section,
            section_length=section_length,
            conclusion_length=conclusion_length,
            temperature=temperature,
            **kwargs
        )
