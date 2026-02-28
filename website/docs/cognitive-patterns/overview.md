---
sidebar_position: 1
title: Cognitive Patterns Overview
description: 87 research-backed cognitive patterns for systematic reasoning — 16 free, 71 enterprise. Browse by category, understand the methodology, and pick the right pattern for your task.
---

# Cognitive Patterns

Cognitive patterns are the core of mycontext-ai. Each one implements a real cognitive or analytical methodology — not a generic template — grounded in research from cognitive science, decision theory, systems thinking, and organizational behavior.

Every pattern provides:
- **`build_context(**inputs)`** → a fully assembled `Context` ready to execute
- **`execute(provider, **inputs)`** → build + execute in one call
- **`generic_prompt(**inputs)`** → a zero-cost, pre-authored prompt string (~600–1200 chars)

## Why Patterns?

Without patterns, every developer writes ad-hoc prompts from scratch — reinventing the wheel every time. A prompt for root cause analysis has decades of methodology behind it (Five Whys, Ishikawa diagrams, contributing factor analysis). A prompt for scenario planning has its own framework (critical uncertainties, 2×2 matrix, signposts). Writing these correctly from scratch takes hours.

Patterns encode that methodology once. You bring the problem.

```python
from mycontext.templates.free.reasoning import RootCauseAnalyzer

# Five Whys + Ishikawa + contributing factors + prevention — encoded
ctx = RootCauseAnalyzer().build_context(
    problem="API response times tripled after last deployment",
    depth="comprehensive",
)
result = ctx.execute(provider="openai")
```

## All 87 Patterns at a Glance

### Free Patterns (16) — Included in Every Install

| Pattern | Category | What it does | Key inputs |
|---------|----------|-------------|------------|
| [RootCauseAnalyzer](./free/root-cause-analyzer) | Reasoning | Five Whys + Ishikawa systematic diagnosis | `problem`, `depth` |
| [StepByStepReasoner](./free/step-by-step-reasoner) | Reasoning | Chain-of-thought with transparent steps | `problem`, `domain` |
| [HypothesisGenerator](./free/hypothesis-generator) | Reasoning | Testable hypotheses with experimental design | `observation`, `domain` |
| [DataAnalyzer](./free/data-analyzer) | Analysis | Pattern detection + actionable insights | `data_description`, `goal` |
| [QuestionAnalyzer](./free/question-analyzer) | Analysis | Decompose questions before answering | `question`, `depth` |
| [Brainstormer](./free/brainstormer) | Creative | Divergent ideation + convergent selection | `topic`, `goal`, `constraints` |
| [CodeReviewer](./free/code-reviewer) | Specialized | Security, performance, maintainability review | `code`, `language`, `focus_areas` |
| [RiskAssessor](./free/risk-assessor) | Specialized | 5-category risk scoring + mitigation | `decision`, `depth` |
| [ScenarioPlanner](./free/scenario-planner) | Planning | 4-scenario 2×2 matrix + signposts | `topic`, `timeframe` |
| [StakeholderMapper](./free/stakeholder-mapper) | Planning | Power-interest matrix + engagement plan | `project` |
| [AudienceAdapter](./free/audience-adapter) | Communication | Reframe content for a different audience | `message`, `current_audience`, `target_audience` |
| [TechnicalTranslator](./free/technical-translator) | Communication | Jargon → plain language with translation map | `technical_text`, `target_audience` |
| [SocraticQuestioner](./free/socratic-questioner) | Specialized | 6-category probing questions on a statement | `statement`, `depth` |
| [SynthesisBuilder](./free/synthesis-builder) | Specialized | Integrate multiple sources into one narrative | `sources`, `goal` |
| [ConflictResolver](./free/conflict-resolver) | Specialized | Mediate disputes, find win-win resolutions | `conflict`, `parties` |
| [IntentRecognizer](./free/intent-recognizer) | Specialized | Uncover true intent behind a request | `input`, `depth` |

### Enterprise Patterns (71) — Requires License

Advanced patterns organized by category. Each requires a valid license key. [Learn more →](./enterprise-overview)

| Category | Patterns | Highlights |
|----------|----------|------------|
| **Specialized Intelligence** | 2 | **RagAnswerer** (+15% evidence recall, citations, abstention), **MemoryCompressor** (2x recall over summarization at scale) |
| **Advanced Analysis** | 4 | TrendIdentifier, GapAnalyzer, SWOTAnalyzer, AnomalyDetector |
| **Advanced Reasoning** | 2 | CausalReasoner, AnalogicalReasoner |
| **Advanced Creative** | 4 | IdeaGenerator, InnovationFramework, DesignThinker, MetaphorGenerator |
| **Advanced Communication** | 5 | SimplificationEngine, PersuasionFramework, NarrativeBuilder, FeedbackComposer, ClarityOptimizer |
| **Advanced Planning** | 3 | ResourceAllocator, PrioritySetter, DeadlineManager |
| **Advanced Specialized** | 5 | ContentOutliner, AmbiguityResolver, RiskMitigator, ImpactAssessor, ConceptExplainer |
| **Decision** | 5 | DecisionFramework, ComparativeAnalyzer, TradeoffAnalyzer, MultiObjectiveOptimizer, CostBenefitAnalyzer |
| **Problem Solving** | 6 | ProblemDecomposer, BottleneckIdentifier, ConstraintOptimizer, DependencyMapper, EfficiencyAnalyzer, TradeSpaceExplorer |
| **Temporal Reasoning** | 3 | TemporalSequenceAnalyzer, FutureScenarioPlanner, HistoricalContextMapper |
| **Diagnostic** | 3 | DiagnosticRootCauseAnalyzer, DifferentialDiagnoser, SystemHealthAuditor |
| **Synthesis** | 3 | HolisticIntegrator, PatternRecognitionEngine, CrossDomainSynthesizer |
| **Systems Thinking** | 6 | FeedbackLoopIdentifier, LeveragePointFinder, EmergenceDetector, SystemArchetypeAnalyzer, CausalLoopDiagrammer, StockFlowAnalyzer |
| **Metacognition** | 5 | MetacognitiveMonitor, SelfRegulationFramework, CognitiveStrategySelector, LearningFromExperience, ErrorDetectionFramework |
| **Ethical Reasoning** | 5 | EthicalFrameworkAnalyzer, MoralDilemmaResolver, StakeholderEthicsAssessor, ValueConflictNavigator, ConsequentialistAnalyzer |
| **Learning** | 5 | ScaffoldingFramework, SpacedRepetitionOptimizer, ZoneOfProximalDevelopment, CognitiveLoadManager, ConceptualChangeAnalyzer |
| **Evaluation** | 5 | RubricDesigner, FormativeAssessmentFramework, SummativeEvaluator, PeerAssessmentStructure, SelfAssessmentGuide |

## Two Execution Modes

Every pattern supports two modes. Choose based on your cost/quality needs:

### Mode 1: Full Context (Rich, Structured)

Uses the complete directive template — structured sections, numbered steps, output format instructions. Produces the richest, most thorough responses.

```python
from mycontext.templates.free.reasoning import RootCauseAnalyzer

# Build full context
ctx = RootCauseAnalyzer().build_context(
    problem="Server crashes during peak hours",
    depth="comprehensive",
)
result = ctx.execute(provider="openai")
```

### Mode 2: Generic Prompt (Zero-cost compilation)

Uses the hand-crafted `GENERIC_PROMPT` (~600–1200 chars). No context assembly, no extra LLM calls — just string substitution and a single execute call. Validated at ~95% of full mode quality.

```python
from mycontext.templates.free.reasoning import RootCauseAnalyzer

rca = RootCauseAnalyzer()

# Zero-cost: just string substitution
prompt = rca.generic_prompt(problem="Server crashes during peak hours")

# Or execute directly in generic mode (1 LLM call total)
result = rca.execute(
    provider="openai",
    mode="generic",
    problem="Server crashes during peak hours",
)
```

## Chaining Patterns

Complex questions often need multiple reasoning steps. Chain patterns so each stage feeds the next:

```python
from mycontext.templates.free.reasoning import RootCauseAnalyzer, HypothesisGenerator
from mycontext.templates.free.planning import ScenarioPlanner

# Stage 1: Root cause analysis
ctx1 = RootCauseAnalyzer().build_context(
    problem="Churn increased 40% this quarter",
    depth="thorough",
)
rca_result = ctx1.execute(provider="openai")

# Stage 2: Generate hypotheses based on root causes
ctx2 = HypothesisGenerator().build_context(
    observation=rca_result.response[:2000],
    domain="SaaS customer retention",
)
hyp_result = ctx2.execute(provider="openai")

# Stage 3: Plan scenarios for each hypothesis
ctx3 = ScenarioPlanner().build_context(
    topic="Customer retention recovery strategies",
    timeframe="6 months",
)
result = ctx3.execute(provider="openai")
```

## Automatic Pattern Selection

Don't know which pattern fits? Let the intelligence layer choose:

```python
from mycontext.intelligence import suggest_patterns, smart_execute

# Get recommendations
result = suggest_patterns(
    "Why did our churn spike? What should we do about it?",
    mode="hybrid",
    llm_provider="openai",
)
print(result.suggested_chain)
# → ['root_cause_analyzer', 'scenario_planner']

# Or just execute — auto-selects and runs
response, meta = smart_execute(
    "Why did our churn spike? What should we do about it?",
    provider="openai",
)
print(meta["templates_used"])
```

## The Research Foundation

Every pattern is backed by peer-reviewed research. Some examples:

| Pattern | Methodology | Research basis |
|---------|-------------|----------------|
| RootCauseAnalyzer | Five Whys, Ishikawa | Quality management, systems thinking |
| StepByStepReasoner | Chain-of-Thought | Wei et al. (2023), IBM Zurich (2025) |
| HypothesisGenerator | Scientific method | Experimental design research |
| SocraticQuestioner | Socratic method | Classical dialogue methodology |
| ScenarioPlanner | Scenario planning | Shell's scenario methodology, GBN |
| StakeholderMapper | Stakeholder theory | Freeman's stakeholder framework |

The full citation list (150+ papers) is in the [Research Foundations](/docs/cognitive-patterns/overview) document.

---

**Browse the free patterns:**

import DocCardList from '@theme/DocCardList';

<DocCardList />
