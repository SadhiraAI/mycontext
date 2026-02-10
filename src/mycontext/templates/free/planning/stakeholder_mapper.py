"""
Stakeholder Mapper - Identify and analyze stakeholders

Comprehensive stakeholder identification, analysis, and engagement strategy.
Based on stakeholder theory and engagement frameworks.
"""

from typing import Optional
from mycontext.structure import Pattern
from mycontext.foundation import Guidance, Directive, Constraints


class StakeholderMapper(Pattern):
    """
    Map and analyze stakeholders systematically.
    
    Identifies:
    - Key stakeholders
    - Interests and influence
    - Power dynamics
    - Engagement strategies
    
    Based on: Stakeholder analysis frameworks
    
    Example:
        >>> mapper = StakeholderMapper()
        >>> context = mapper.build_context(
        ...     project="Launch new AI product",
        ...     context="B2B enterprise market"
        ... )
    
    Free Template - Part of mycontext open source edition.
    """
    
    def __init__(self):
        super().__init__(
            name="stakeholder_mapper",
            description="Map and analyze stakeholders",
            guidance=Guidance(
                role="Expert Stakeholder Analyst and Engagement Strategist",
                rules=[
                    "Identify all relevant stakeholders",
                    "Assess power and interest objectively",
                    "Consider hidden stakeholders",
                    "Plan engagement strategies",
                    "Address concerns and objections"
                ],
                style="diplomatic, strategic, thorough"
            ),
            directive_template="""Map stakeholders for:

**PROJECT/INITIATIVE**: {project}

{context_section}

Stakeholder analysis:

1. **STAKEHOLDER IDENTIFICATION**
   Who is affected or can affect this?
   
   **Primary Stakeholders** (Directly affected):
   - [Stakeholder 1]: [Role/relationship]
   - [Stakeholder 2]: [Role/relationship]
   - [Stakeholder 3]: [Role/relationship]
   
   **Secondary Stakeholders** (Indirectly affected):
   - [Stakeholder 4]: [Connection]
   - [Stakeholder 5]: [Connection]
   
   **Key Stakeholders** (High influence):
   - [Stakeholder 6]: [Why influential]
   - [Stakeholder 7]: [Power source]

2. **STAKEHOLDER PROFILES**
   For each key stakeholder:
   
   **Stakeholder: [Name/Group]**
   - Role: [What they do]
   - Interest level: [High/Medium/Low]
   - Power level: [High/Medium/Low]
   - Current stance: [Supportive/Neutral/Opposed]
   - What they want: [Interests]
   - What they fear: [Concerns]
   - Influence: [How they can affect outcome]
   
   [Repeat for each key stakeholder]

3. **POWER-INTEREST MATRIX**
   
   **HIGH POWER, HIGH INTEREST** (Key Players - Manage Closely):
   - [Stakeholder A]: [Strategy]
   - [Stakeholder B]: [Engagement plan]
   
   **HIGH POWER, LOW INTEREST** (Keep Satisfied):
   - [Stakeholder C]: [Monitoring approach]
   - [Stakeholder D]: [Minimal effort]
   
   **LOW POWER, HIGH INTEREST** (Keep Informed):
   - [Stakeholder E]: [Communication plan]
   - [Stakeholder F]: [Update strategy]
   
   **LOW POWER, LOW INTEREST** (Monitor):
   - [Stakeholder G]: [Minimal engagement]
   - [Stakeholder H]: [Awareness only]

4. **STAKEHOLDER NEEDS & CONCERNS**
   
   What each group needs:
   - [Group 1]: [Primary needs]
   - [Group 2]: [Requirements]
   - [Group 3]: [Expectations]
   
   Major concerns to address:
   - Concern 1: [What worries them]
     - Mitigation: [How to address]
   - Concern 2: [Another worry]
     - Mitigation: [Response strategy]

5. **INFLUENCE MAPPING**
   
   Who influences whom?
   - [Influencer A] → [Stakeholder B]
   - [Influencer C] → [Stakeholder D]
   
   Coalition possibilities:
   - Alliance 1: [Stakeholders who align]
   - Alliance 2: [Natural partnerships]
   
   Potential blockers:
   - Blocker 1: [Who could stop this]
     - Reason: [Why they'd block]
     - Strategy: [How to address]

6. **ENGAGEMENT STRATEGIES**
   
   For Key Players:
   - **[Stakeholder Name]**:
     - Engagement frequency: [How often]
     - Communication channel: [Method]
     - Key messages: [What to emphasize]
     - Success criteria: [What winning looks like]
   
   For Each Group:
   - Supporters: [How to mobilize]
   - Neutrals: [How to persuade]
   - Opponents: [How to address objections]

7. **COMMUNICATION PLAN**
   
   | Stakeholder | Message | Channel | Frequency | Owner |
   |-------------|---------|---------|-----------|-------|
   | [Name] | [Key msg] | [Method] | [How often] | [Who] |
   | [Name] | [Key msg] | [Method] | [How often] | [Who] |

8. **RISK MANAGEMENT**
   
   Stakeholder risks:
   - Risk 1: [Stakeholder X withdraws support]
     - Likelihood: [High/Med/Low]
     - Impact: [Severity]
     - Mitigation: [Prevention strategy]
   
   - Risk 2: [Opposition coalition forms]
     - Likelihood: [Probability]
     - Impact: [Effect]
     - Mitigation: [How to prevent]

9. **SUCCESS METRICS**
   How to measure stakeholder engagement:
   - Metric 1: [Satisfaction scores]
   - Metric 2: [Support levels]
   - Metric 3: [Participation rates]

10. **ACTION PLAN**
    **Immediate (Week 1)**:
    - [Reach out to key player A]
    - [Address major concern B]
    
    **Short-term (Month 1)**:
    - [Build coalition with C]
    - [Neutralize opposition from D]
    
    **Ongoing**:
    - [Regular updates to E]
    - [Monitor sentiment of F]

**OUTPUT FORMAT**: Comprehensive stakeholder map with engagement strategy.""",
            input_schema={
                "project": str,
                "context_section": str
            },
            constraints=Constraints(
                must_include=[
                    "stakeholder_matrix",
                    "engagement_strategies",
                    "action_plan"
                ],
                style_guide="Be diplomatic but realistic, strategic and actionable"
            )
        )
    
    def _render_context_section(self, context: Optional[str]) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""
    
    def build_context(
        self,
        project: str = "",
        context: Optional[str] = None,
        **kwargs
    ):
        context_section = self._render_context_section(context)
        
        return super().build_context(
            project=project,
            context_section=context_section,
            **kwargs
        )
    
    def execute(
        self,
        provider: str = "openai",
        project: str = "",
        context: Optional[str] = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            project=project,
            context=context,
            **kwargs
        )
