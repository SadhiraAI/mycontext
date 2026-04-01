"""
ZoneOfProximalDevelopment Pattern (Enterprise)

Identify tasks at the "just right" difficulty level - challenging but achievable with support.
Implements Vygotsky's ZPD theory.

Research Foundation:
- Vygotsky, L. S. (1978). Mind in society: Development of higher psychological processes.
- Chaiklin, S. (2003). The zone of proximal development in Vygotsky's analysis of learning.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class ZoneOfProximalDevelopment(Pattern):
    """
    Identify tasks in the Zone of Proximal Development.

    Three Zones:
    1. What learner can do independently (too easy)
    2. What learner can do with support (ZPD - optimal)
    3. What is beyond current reach (too hard)

    Use Cases:
    - Adaptive learning systems
    - Personalized curriculum design
    - Skill progression planning
    - Challenge calibration

    Example:
        >>> from mycontext.templates.enterprise.learning import ZoneOfProximalDevelopment
        >>>
        >>> pattern = ZoneOfProximalDevelopment()
        >>> result = pattern.execute(
        ...     provider="openai",
        ...     learner_current_abilities="Can write basic Python functions",
        ...     learning_goal="Master object-oriented programming"
        ... )

    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are a developmental learning expert applying Vygotsky's Zone of "
        "Proximal Development (ZPD) theory. Identify tasks at the optimal "
        "challenge level for the learner.\n\n"
        "Learner's Current Abilities: {learner_current_abilities}\n"
        "Learning Goal: {learning_goal}\n"
        "{context_section}\n\n"
        "Perform three-zone analysis: (1) Zone 1 — Independent Performance (too "
        "easy): list skills already mastered and tasks completable without help. "
        "Low learning value; use for warm-up only. (2) Zone 2 — ZPD (optimal): "
        "identify skills in development that the learner can accomplish WITH "
        "support. Design 3-5 specific tasks at this level with the required "
        "scaffolding for success. This is where maximum growth happens. "
        "(3) Zone 3 — Beyond Reach (too hard): identify skills with missing "
        "prerequisites; save these for later.\n\n"
        "Provide a learning pathway from current to goal, with ZPD tasks, support "
        "plans, and criteria for when to reassess the ZPD boundaries as the "
        "learner progresses.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="zone_of_proximal_development",
            description="Identify tasks at optimal difficulty level (ZPD)",
            version="1.0.0",
            tags=["learning", "enterprise", "zpd", "vygotsky"],
            metadata={"category": "learning", "license": "enterprise", "tier": "enterprise"},
            guidance=Guidance(
                role="Developmental Learning Expert",
                rules=[
                    "Apply Vygotsky's ZPD theory precisely",
                    "Identify three distinct zones (independent, ZPD, beyond reach)",
                    "Focus learning in the ZPD (challenging but achievable)",
                    "Avoid tasks that are too easy (no growth) or too hard (frustration)",
                    "Provide specific task examples for each zone",
                ],
                style="diagnostic, precise, developmental, strategic",
            ),
            directive_template="""**ZONE OF PROXIMAL DEVELOPMENT ANALYSIS**

**LEARNER'S CURRENT ABILITIES**: {learner_current_abilities}

**LEARNING GOAL**: {learning_goal}

---

## THREE-ZONE ANALYSIS

### ZONE 1: INDEPENDENT PERFORMANCE (Too Easy)
**What learner can do WITHOUT support**

Skills mastered:
- [Skill 1]
- [Skill 2]
...

Tasks learner can complete independently:
1. [Task example 1]
2. [Task example 2]
...

**Learning value**: ❌ LOW (already mastered)
**Recommendation**: Use for warm-up only, not main learning

---

### ZONE 2: ZONE OF PROXIMAL DEVELOPMENT (Optimal) ⭐
**What learner can do WITH support**

Skills in development:
- [Skill 1 - can do with help]
- [Skill 2 - can do with coaching]
...

Optimal learning tasks:
1. [Task that's challenging but doable with scaffolding]
2. [Task that stretches current abilities]
3. [Task that requires guided practice]
...

**Required support for success**:
- [Type of scaffolding needed]
- [Guidance required]
- [Resources helpful]

**Learning value**: ✅ HIGH (maximum growth)
**Recommendation**: **FOCUS HERE** - this is where learning happens

**Success indicators**:
- Initially struggles but succeeds with help
- Can explain reasoning with prompting
- Shows improvement with practice
- Difficulty is "just right" (not frustrating, not boring)

---

### ZONE 3: BEYOND CURRENT REACH (Too Hard)
**What is beyond learner's current abilities**

Skills not yet accessible:
- [Skill 1 - too advanced]
- [Skill 2 - missing prerequisites]
...

Tasks that are too difficult:
1. [Task that would cause frustration]
2. [Task with too many unknowns]
3. [Task requiring unlearned prerequisites]
...

**Why too hard**:
- Missing prerequisite knowledge: [X, Y, Z]
- Too many new concepts at once
- Cognitive load too high

**Learning value**: ❌ LOW (frustration, no progress)
**Recommendation**: Save for later, after mastering ZPD tasks

---

## LEARNING PATHWAY

**Step-by-Step Progression**:

**CURRENT** (Zone 1):
→ Master these independently

**NEXT** (Zone 2 - ZPD): ⭐
→ **Focus learning effort here**
→ Tasks: [List 3-5 specific ZPD tasks]
→ Support needed: [Scaffolding plan]

**FUTURE** (Zone 3):
→ Return to these after ZPD mastery

---

## ZPD TASK DESIGN

**For each ZPD task, ensure**:

✅ **Challenge**: Not too easy (learner must stretch)
✅ **Achievability**: Not too hard (success possible with support)
✅ **Support**: Clear scaffolding available
✅ **Feedback**: Immediate guidance when stuck
✅ **Progression**: Clear next steps

**Example ZPD Task Structure**:

Task: [Specific task in ZPD]

- Difficulty: Just beyond independent ability
- Support provided: [Hints, examples, coaching]
- Success criteria: [How to know they got it]
- Next task: [Slightly harder task]

---

## MONITORING ZPD BOUNDARIES

**ZPD moves as learner progresses**

**Check regularly**:

**Signs task is NOW too easy** (moved to Zone 1):
- Completes without help
- Bored or disengaged
- No mistakes

**Signs task is in ZPD** (optimal): ⭐
- Struggles initially, succeeds with support
- Engaged and focused
- Some mistakes, learns from them

**Signs task is NOW too hard** (still in Zone 3):
- Fails even with support
- Frustrated or gives up
- Too many mistakes

**Adjustment strategy**: Move learner to appropriate zone

---

## IMMEDIATE RECOMMENDATIONS

**Start here** (ZPD tasks):
1. [First ZPD task]
2. [Second ZPD task]
3. [Third ZPD task]

**Support plan**: [How to scaffold these tasks]

**Success milestones**: [How to know learner is progressing]

**Next reassessment**: [When to re-evaluate ZPD]""",
            input_schema={"learner_current_abilities": str, "learning_goal": str},
            constraints=Constraints(
                must_include=["three_zones", "zpd_tasks", "support_plan", "progression_pathway"],
                must_not_include=["one_size_fits_all", "tasks_too_easy_or_hard"],
                style_guide="Diagnostic and developmental. Clearly distinguish three zones. Focus on ZPD.",
            ),
        )

    def build_context(self, learner_current_abilities="", learning_goal="", **kwargs):
        """Build context for ZPD analysis."""
        return super().build_context(
            learner_current_abilities=learner_current_abilities,
            learning_goal=learning_goal,
            **kwargs,
        )

    def execute(self, provider="openai", learner_current_abilities="", learning_goal="", **kwargs):
        """Execute ZPD analysis."""
        return super().execute(
            provider=provider,
            learner_current_abilities=learner_current_abilities,
            learning_goal=learning_goal,
            **kwargs,
        )


__all__ = ["ZoneOfProximalDevelopment"]
