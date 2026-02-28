---
sidebar_position: 2
title: Enterprise Patterns
description: 71 advanced cognitive patterns for specialized reasoning tasks. Requires a valid license key. Covers specialized intelligence, decision science, systems thinking, metacognition, ethics, and more.
---

# Enterprise Patterns (71)

Enterprise patterns extend the free tier with advanced reasoning capabilities across specialized domains. They follow the same API as free patterns — `build_context()`, `execute()`, `generic_prompt()` — and integrate seamlessly with the intelligence layer.

:::info License Required
Enterprise patterns require a valid license key. Set your key via:
```bash
export MYCONTEXT_LICENSE_KEY="your-license-key"
```
Or configure programmatically:
```python
import mycontext
mycontext.configure(license_key="your-license-key")
```
[Get a license →](https://sadhiraai.com)
:::

## Importing Enterprise Patterns

```python
from mycontext.templates.enterprise.decision import DecisionFramework
from mycontext.templates.enterprise.systems import FeedbackLoopIdentifier
from mycontext.templates.enterprise.metacognition import MetacognitiveMonitor

# Same API as free patterns
result = DecisionFramework().execute(
    provider="openai",
    decision="Which cloud provider to standardize on",
    options=["AWS", "GCP", "Azure"],
    criteria=["cost", "reliability", "team expertise", "vendor lock-in risk"],
)
```

## All 71 Enterprise Patterns

### Specialized Intelligence (2 patterns)

Research-validated templates for RAG generation and memory compression — the two most critical challenges in production AI systems.

| Pattern | What it does | Key inputs | Research |
|---------|-------------|-----------|----------|
| **RagAnswerer** | Grounded RAG generation with citation, abstention, and evidence extraction. Applies CRAG, Self-RAG, and Chain-of-Note principles. **+15% evidence recall** over plain RAG prompts. | `question`, `context`, `mode` | Validated |
| **MemoryCompressor** | Structured state extraction from conversations — entities, decisions, constraints, key numbers. **2x recall** over progressive summarization at scale. Plugs into any framework's memory middleware. | `content`, `intent`, `existing_memory`, `goal` | Validated |

```python
from mycontext.templates.enterprise.specialized import RagAnswerer, MemoryCompressor

# RAG with grounding and citation
rag = RagAnswerer()
result = rag.execute(
    provider="openai",
    question="What caused the outage?",
    context=retrieved_chunks,
    mode="answer",
)

# Memory compression for agent sessions
mc = MemoryCompressor()
result = mc.execute(
    provider="openai",
    content=conversation_history,
    intent="session",  # or "progressive" for updates
)
```

### Advanced Analysis (4 patterns)

Deeper analytical capabilities beyond the free `DataAnalyzer` and `QuestionAnalyzer`.

| Pattern | What it does |
|---------|-------------|
| **TrendIdentifier** | Detect and extrapolate trend lines with statistical confidence intervals |
| **GapAnalyzer** | Systematic gap analysis between current state and desired state |
| **SWOTAnalyzer** | Full SWOT with strategic implications and prioritized actions |
| **AnomalyDetector** | Statistical anomaly detection with severity scoring and causal hypotheses |

### Advanced Reasoning (2 patterns)

| Pattern | What it does |
|---------|-------------|
| **CausalReasoner** | Build causal models with confounders, mechanisms, and intervention analysis |
| **AnalogicalReasoner** | Structured analogical transfer — map solutions from other domains |

### Advanced Creative (4 patterns)

| Pattern | What it does |
|---------|-------------|
| **IdeaGenerator** | SCAMPER + design thinking hybrid for product innovation |
| **InnovationFramework** | Jobs-to-be-Done framework for disruptive opportunity identification |
| **DesignThinker** | Full design thinking cycle: empathize → define → ideate → prototype → test |
| **MetaphorGenerator** | Construct precise explanatory metaphors for complex concepts |

### Advanced Communication (5 patterns)

| Pattern | What it does |
|---------|-------------|
| **SimplificationEngine** | Multi-level simplification with readability scoring |
| **PersuasionFramework** | Aristotle's ethos/pathos/logos persuasion architecture |
| **NarrativeBuilder** | Construct compelling narratives with arc, tension, and resolution |
| **FeedbackComposer** | Structured feedback using SBI (Situation-Behavior-Impact) model |
| **ClarityOptimizer** | Detect and resolve ambiguity, vagueness, and jargon systematically |

### Advanced Planning (3 patterns)

| Pattern | What it does |
|---------|-------------|
| **ResourceAllocator** | Optimal resource allocation with constraint modeling |
| **PrioritySetter** | Multi-criteria prioritization with RICE, ICE, and custom frameworks |
| **DeadlineManager** | Timeline analysis with critical path identification and buffer optimization |

### Advanced Specialized (5 patterns)

| Pattern | What it does |
|---------|-------------|
| **ContentOutliner** | Hierarchical content architecture with narrative flow |
| **AmbiguityResolver** | Systematically identify and resolve ambiguous requirements |
| **RiskMitigator** | Extends `RiskAssessor` with FMEA and bowtie analysis |
| **ImpactAssessor** | Multi-stakeholder impact assessment with quantified projections |
| **ConceptExplainer** | Layered explanations calibrated to expertise level (Feynman technique) |

### Decision Patterns (5 patterns)

Comprehensive decision support frameworks.

| Pattern | What it does | Key inputs |
|---------|-------------|-----------|
| **DecisionFramework** | Structured decision analysis with criteria weighting | `decision`, `options`, `criteria` |
| **ComparativeAnalyzer** | Head-to-head comparison with normalized scoring | `items`, `dimensions` |
| **TradeoffAnalyzer** | Explicit tradeoff mapping across multiple dimensions | `options`, `tradeoffs` |
| **MultiObjectiveOptimizer** | Pareto-optimal solution finding with constraint satisfaction | `objectives`, `constraints` |
| **CostBenefitAnalyzer** | Quantified CBA with sensitivity analysis and NPV | `costs`, `benefits`, `timeframe` |

```python
from mycontext.templates.enterprise.decision import DecisionFramework

result = DecisionFramework().execute(
    provider="openai",
    decision="Choose our primary database technology",
    options=["PostgreSQL", "MongoDB", "DynamoDB"],
    criteria={
        "query_flexibility": 0.30,
        "operational_complexity": 0.25,
        "cost": 0.20,
        "team_expertise": 0.15,
        "scalability": 0.10,
    },
)
```

### Problem Solving (6 patterns)

| Pattern | What it does |
|---------|-------------|
| **ProblemDecomposer** | MECE decomposition into independently solvable sub-problems |
| **BottleneckIdentifier** | Throughput analysis using Theory of Constraints methodology |
| **ConstraintOptimizer** | Optimize outcomes within a constraint set |
| **DependencyMapper** | Map dependency graphs with critical path analysis |
| **EfficiencyAnalyzer** | Waste identification and process optimization (Lean principles) |
| **TradeSpaceExplorer** | Explore the full solution space before committing to one option |

### Temporal Reasoning (3 patterns)

| Pattern | What it does |
|---------|-------------|
| **TemporalSequenceAnalyzer** | Analyze causation and dependencies across time |
| **FutureScenarioPlanner** | Extended `ScenarioPlanner` with morphological analysis |
| **HistoricalContextMapper** | Map historical precedents and their implications for current decisions |

### Diagnostic (3 patterns)

Medical-grade diagnostic reasoning methodology applied to any domain.

| Pattern | What it does |
|---------|-------------|
| **DiagnosticRootCauseAnalyzer** | FMEA-integrated root cause analysis (extends free `RootCauseAnalyzer`) |
| **DifferentialDiagnoser** | Differential diagnosis — systematic elimination of alternative explanations |
| **SystemHealthAuditor** | Full-system health audit across multiple diagnostic dimensions |

### Synthesis (3 patterns)

| Pattern | What it does |
|---------|-------------|
| **HolisticIntegrator** | Cross-domain synthesis with emergence detection |
| **PatternRecognitionEngine** | Identify recurring patterns in complex, noisy data |
| **CrossDomainSynthesizer** | Transfer insights across domain boundaries |

### Systems Thinking (6 patterns)

The most sophisticated pattern category — models complex adaptive systems.

| Pattern | What it does |
|---------|-------------|
| **FeedbackLoopIdentifier** | Identify reinforcing and balancing feedback loops |
| **LeveragePointFinder** | Find highest-impact intervention points in a system (Meadows' leverage points) |
| **EmergenceDetector** | Identify emergent properties and non-linear dynamics |
| **SystemArchetypeAnalyzer** | Match system behavior to known archetypes (fixes that fail, tragedy of the commons, etc.) |
| **CausalLoopDiagrammer** | Build formal causal loop diagrams with polarity and delay notation |
| **StockFlowAnalyzer** | Model stocks, flows, and accumulation dynamics |

```python
from mycontext.templates.enterprise.systems import LeveragePointFinder

result = LeveragePointFinder().execute(
    provider="openai",
    system="Enterprise SaaS customer retention system",
    goal="Identify where small changes would have the largest impact on churn",
    context="Current churn: 3.2%/month. Top churn drivers: feature gaps, support responsiveness, pricing",
)
```

### Metacognition (5 patterns)

Patterns that think about thinking — improve reasoning quality and decision processes.

| Pattern | What it does |
|---------|-------------|
| **MetacognitiveMonitor** | Monitor and improve the quality of reasoning processes |
| **SelfRegulationFramework** | Structure self-correction and adaptive thinking |
| **CognitiveStrategySelector** | Select the optimal cognitive strategy for a given problem type |
| **LearningFromExperience** | Structured after-action review and lessons-learned extraction |
| **ErrorDetectionFramework** | Systematic identification of cognitive biases and reasoning errors |

### Ethical Reasoning (5 patterns)

Structured application of ethical frameworks to decisions and situations.

| Pattern | What it does |
|---------|-------------|
| **EthicalFrameworkAnalyzer** | Apply multiple ethical frameworks (consequentialist, deontological, virtue) to a situation |
| **MoralDilemmaResolver** | Structured approach to genuine moral dilemmas without easy answers |
| **StakeholderEthicsAssessor** | Assess ethical implications across all affected stakeholders |
| **ValueConflictNavigator** | Navigate situations where values genuinely conflict |
| **ConsequentialistAnalyzer** | Rigorous consequence mapping with probability-weighted impact |

### Learning (5 patterns)

Educational and knowledge-building patterns.

| Pattern | What it does |
|---------|-------------|
| **ScaffoldingFramework** | Build knowledge from existing foundations progressively |
| **SpacedRepetitionOptimizer** | Optimize learning sequences for retention |
| **ZoneOfProximalDevelopment** | Calibrate challenge level to maximize learning |
| **CognitiveLoadManager** | Reduce extraneous cognitive load in explanations |
| **ConceptualChangeAnalyzer** | Identify and address conceptual misconceptions |

### Evaluation (5 patterns)

Assessment and feedback patterns for systematic quality evaluation.

| Pattern | What it does |
|---------|-------------|
| **RubricDesigner** | Create evaluation rubrics with clear criteria and descriptors |
| **FormativeAssessmentFramework** | Ongoing assessment to guide improvement |
| **SummativeEvaluator** | Final evaluation against defined criteria |
| **PeerAssessmentStructure** | Structure effective peer review processes |
| **SelfAssessmentGuide** | Guide structured self-evaluation |

## Pattern Combinations

Enterprise patterns are designed to chain with each other and with free patterns:

```python
from mycontext.templates.enterprise.decision import TradeoffAnalyzer
from mycontext.templates.enterprise.systems import LeveragePointFinder
from mycontext.templates.free.planning import ScenarioPlanner

# Step 1: Map tradeoffs in the decision space
tradeoffs = TradeoffAnalyzer().execute(
    provider="openai",
    options=["Build in-house", "Use third-party API", "Acquire startup"],
    tradeoffs=["control", "cost", "speed", "technical risk"],
)

# Step 2: Find the highest-leverage choice
leverage = LeveragePointFinder().execute(
    provider="openai",
    system="AI feature development ecosystem",
    context=tradeoffs.response[:1000],
)

# Step 3: Plan for uncertainty
scenarios = ScenarioPlanner().execute(
    provider="openai",
    topic="Build vs. buy decision for core AI feature",
    timeframe="18 months",
)
```

## License and Pricing

Enterprise patterns are available in the following tiers:
- **Professional**: All 71 patterns, single workspace
- **Team**: All 71 patterns, up to 10 seats
- **Enterprise**: All patterns, unlimited seats, custom SLAs

[View pricing →](https://sadhiraai.com/pricing)
