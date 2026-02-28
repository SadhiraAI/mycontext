---
sidebar_position: 4
title: Enterprise License
description: Activate an enterprise license key to unlock all 71 enterprise cognitive patterns. One-line activation, persistent storage, and graceful free-tier fallback.
---

# Enterprise License

mycontext-ai has 16 free patterns included in every install, plus 71 enterprise patterns that require a license. Activation is a single function call — the key is stored locally and persists across sessions.

## Activation

```python
import mycontext

mycontext.activate_license("MC-ENT-YOUR-KEY-HERE")
print(mycontext.is_enterprise_active())  # True
```

That's it. All 71 enterprise patterns are now available for the rest of the session — and in every future session on this machine (stored at `~/.mycontext/license.json`).

## `activate_license(key)`

```python
import mycontext

success = mycontext.activate_license("MC-ENT-XXXX-XXXX-XXXX")
# → True
```

- Stores the key in `~/.mycontext/license.json`
- Activates immediately for the current session
- Persists across Python restarts and new terminals

## `is_enterprise_active()`

```python
import mycontext

if mycontext.is_enterprise_active():
    print("Enterprise patterns available")
else:
    print("Free tier — 16 patterns available")
```

Returns `True` if a license key is stored and active.

## `deactivate_license()`

```python
import mycontext

mycontext.deactivate_license()
print(mycontext.is_enterprise_active())  # False
```

Removes the stored key and reverts to the free tier. The 16 free patterns remain available.

## Using Enterprise Patterns

Once activated, import enterprise patterns the same way as free ones:

```python
import mycontext
mycontext.activate_license("MC-ENT-...")

# Enterprise patterns — same API as free patterns
from mycontext.templates.enterprise.decision import DecisionFramework, TradeoffAnalyzer
from mycontext.templates.enterprise.systems_thinking import FeedbackLoopIdentifier
from mycontext.templates.enterprise.metacognition import MetacognitiveMonitor
from mycontext.templates.enterprise.ethical_reasoning import EthicalFrameworkAnalyzer

result = DecisionFramework().execute(
    provider="openai",
    decision="Should we expand to Southeast Asia next year?",
)
```

## All 69 Enterprise Patterns

| Category | Patterns |
|----------|---------|
| **Advanced Analysis** (4) | TrendIdentifier, GapAnalyzer, SWOTAnalyzer, AnomalyDetector |
| **Advanced Reasoning** (2) | CausalReasoner, AnalogicalReasoner |
| **Advanced Creative** (4) | IdeaGenerator, InnovationFramework, DesignThinker, MetaphorGenerator |
| **Advanced Communication** (5) | SimplificationEngine, PersuasionFramework, NarrativeBuilder, FeedbackComposer, ClarityOptimizer |
| **Advanced Planning** (3) | ResourceAllocator, PrioritySetter, DeadlineManager |
| **Advanced Specialized** (5) | ContentOutliner, AmbiguityResolver, RiskMitigator, ImpactAssessor, ConceptExplainer |
| **Decision** (5) | DecisionFramework, ComparativeAnalyzer, TradeoffAnalyzer, MultiObjectiveOptimizer, CostBenefitAnalyzer |
| **Problem Solving** (6) | ProblemDecomposer, BottleneckIdentifier, ConstraintOptimizer, DependencyMapper, EfficiencyAnalyzer, TradeSpaceExplorer |
| **Temporal Reasoning** (3) | TemporalSequenceAnalyzer, FutureScenarioPlanner, HistoricalContextMapper |
| **Diagnostic** (3) | DiagnosticRootCauseAnalyzer, DifferentialDiagnoser, SystemHealthAuditor |
| **Synthesis** (3) | HolisticIntegrator, PatternRecognitionEngine, CrossDomainSynthesizer |
| **Systems Thinking** (6) | FeedbackLoopIdentifier, LeveragePointFinder, EmergenceDetector, SystemArchetypeAnalyzer, CausalLoopDiagrammer, StockFlowAnalyzer |
| **Metacognition** (5) | MetacognitiveMonitor, SelfRegulationFramework, CognitiveStrategySelector, LearningFromExperience, ErrorDetectionFramework |
| **Ethical Reasoning** (5) | EthicalFrameworkAnalyzer, MoralDilemmaResolver, StakeholderEthicsAssessor, ValueConflictNavigator, ConsequentialistAnalyzer |
| **Learning** (5) | ScaffoldingFramework, SpacedRepetitionOptimizer, ZoneOfProximalDevelopment, CognitiveLoadManager, ConceptualChangeAnalyzer |
| **Evaluation** (5) | RubricDesigner, FormativeAssessmentFramework, SummativeEvaluator, PeerAssessmentStructure, SelfAssessmentGuide |

## Graceful Free-Tier Fallback

If enterprise patterns are requested without a license, the SDK provides a clear warning and falls back gracefully — never a hard crash:

```python
# Without license — suggest_patterns still shows enterprise patterns
from mycontext.intelligence import suggest_patterns

result = suggest_patterns(
    "Complex multi-domain strategic question",
    include_enterprise=False,  # Free tier mode
    mode="keyword",
)

for p in result.suggested_patterns:
    print(f"{p.name} [{p.category}]: {p.reason}")
# → decision_framework [enterprise]: Selected because... Requires enterprise license.
# → root_cause_analyzer [free]: Selected because...
```

```python
# Without license — get_pattern_class returns None with a warning
from mycontext.intelligence import get_pattern_class

klass = get_pattern_class("decision_framework", include_enterprise=False)
# UserWarning: Template 'decision_framework' requires an enterprise license.
# Activate with: mycontext.activate_license('MC-ENT-...')
# klass is None — handle gracefully
```

## License Key Storage

The key is stored at `~/.mycontext/license.json`:

```json
{
  "key": "MC-ENT-XXXX-XXXX-XXXX",
  "active": true
}
```

You can also activate at runtime without persisting to disk:

```python
import mycontext

# Runtime-only (not persisted to disk)
from mycontext.license import _runtime_key
# Set programmatically if needed — but activate_license() is the preferred API
mycontext.activate_license(key)  # This persists
```

## CI/CD and Automation

For automated environments, set the key via environment variable and activate at startup:

```python
import os
import mycontext

license_key = os.environ.get("MYCONTEXT_LICENSE_KEY")
if license_key:
    mycontext.activate_license(license_key)
```

In CI (GitHub Actions, etc.):

```yaml
# .github/workflows/test.yml
env:
  MYCONTEXT_LICENSE_KEY: ${{ secrets.MYCONTEXT_LICENSE_KEY }}
```

## Free vs Enterprise

| Feature | Free | Enterprise |
|---------|------|------------|
| Core Context API | All | All |
| Cognitive Patterns | 16 free patterns | 16 + 71 = 87 patterns |
| Intelligence Layer | Full | Full |
| Quality Metrics | Full | Full |
| Integrations | Full | Full |
| Generic Prompts | Free patterns | All 87 patterns |
| `suggest_patterns()` | Shows all (license note for enterprise) | All, no notes |
| `smart_execute()` | Routes to free patterns | Routes to all 85 |

## API Reference

```python
import mycontext

mycontext.activate_license(key: str) -> bool
mycontext.deactivate_license() -> None
mycontext.is_enterprise_active() -> bool

# From license module directly
from mycontext.license import get_license_key
key = get_license_key()  # Returns key string or None
```

## Get a License

Enterprise licenses are available at [mycontext.ai](https://mycontext.ai). License keys start with `MC-ENT-`.
