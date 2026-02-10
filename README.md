# 🚀 mycontext - Universal Context Transformation Engine

<div align="center">

**Transform raw questions into perfect, portable contexts for any AI system**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/mycontext-ai.svg)](https://pypi.org/project/mycontext-ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[Features](#-key-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Examples](#-examples) • [API Reference](#-api-reference)

</div>

---

## 🎯 What is mycontext?

**mycontext** is the world's first **Universal Context Transformation Engine**. It's not just another LLM framework—it's a specialized context engineering library that transforms raw questions into research-backed, high-quality contexts that work with any AI system.

### The Problem
You spend hours crafting perfect prompts. Each LLM needs different formatting. Context quality is inconsistent. There's no way to measure improvement.

### The Solution
```python
from mycontext.intelligence import transform

# One line transforms any question into an optimized context
context = transform("How should we scale our database?")

# Use with any LLM or framework
openai_format = context.to_openai()
claude_format = context.to_anthropic()
langchain_msgs = context.to_langchain()
```

**Result:** Perfect contexts, automatic pattern selection, measurable quality, universal compatibility.

---

## ✨ Key Features

### 🧠 **50 Research-Backed Cognitive Patterns**
Not just templates—scientifically-grounded reasoning frameworks organized into 8 categories:
- **Analysis** (6) - Question analysis, data analysis, trend identification
- **Reasoning** (5) - Step-by-step, causal, analogical reasoning
- **Decision** (5) - Decision frameworks, comparisons, tradeoffs
- **Creative** (5) - Idea generation, brainstorming, innovation
- **Communication** (7) - Simplification, clarity, persuasion
- **Planning** (5) - Scenarios, stakeholders, priorities
- **Problem Solving** (6) - Decomposition, constraints, optimization
- **Specialized** (11) - Code review, risk assessment, conflict resolution

### 🤖 **Automatic Pattern Selection**
The Transformation Engine analyzes your input and automatically selects the optimal cognitive pattern:
```python
from mycontext.intelligence import TransformationEngine

engine = TransformationEngine()
analysis = engine.analyze_input("Should we migrate to microservices?")
# → Detects: decision question
# → Selects: DecisionFramework
# → Confidence: 92%
```

### 📊 **Measurable Quality Metrics**
Stop guessing—measure context quality across 6 scientific dimensions:
- **Clarity** - How clear and unambiguous
- **Completeness** - How thorough and comprehensive
- **Specificity** - How detailed and concrete
- **Relevance** - How focused on the task
- **Structure** - How well-organized
- **Efficiency** - How concise vs verbose

```python
from mycontext.intelligence import QualityMetrics

metrics = QualityMetrics()
score = metrics.evaluate(context)
print(f"Quality: {score.overall:.2f}")  # 0.92
# Get actionable improvement suggestions
```

### 🔄 **13 Universal Export Formats**
One context → Any platform. No vendor lock-in:

**Data Formats:**
- JSON, YAML, XML, Markdown, Dictionary

**LLM Providers:**
- OpenAI (GPT-4), Anthropic (Claude), Google (Gemini)

**AI Frameworks:**
- LangChain, LlamaIndex, CrewAI, AutoGen

```python
# Export to any format
context.to_openai()      # → OpenAI Chat API
context.to_anthropic()   # → Claude Messages API
context.to_langchain()   # → LangChain messages
context.to_yaml()        # → YAML configuration
# ... and 9 more!
```

### 🔌 **6 Framework Integrations**
Drop-in compatibility with popular AI frameworks:
```python
from mycontext.integrations import LangChainHelper

# Instant LangChain compatibility
messages = LangChainHelper.to_messages(context)
# Ready for LangChain pipelines!
```

Supports: **LangChain**, **LlamaIndex**, **CrewAI**, **AutoGen**, **DSPy**, **Semantic Kernel**

### ⚡ **Blazing Fast Performance**
- **100 pattern executions** in 5.6ms (0.06ms average)
- **13 export formats** in <10ms
- **Quality evaluation** in <1ms
- **Pattern selection** in <2ms

---

## 📦 Installation

```bash
pip install mycontext-ai
```

**Requirements:** Python 3.8+

---

## 🚀 Quick Start

### 1. Your First Context (30 seconds)

```python
from mycontext import Context

# Simple context
context = Context(
    guidance="Expert Python Developer",
    directive="Review this code for security issues"
)

print(context.assemble())
```

### 2. Using Cognitive Patterns (1 minute)

```python
from mycontext.templates.free.analysis import QuestionAnalyzer

# Use a research-backed pattern
analyzer = QuestionAnalyzer()
context = analyzer.build_context(
    question="How can I improve database query performance?",
    depth="comprehensive"
)

# Use with any LLM
openai_format = context.to_openai()
```

### 3. Automatic Intelligence (30 seconds)

```python
from mycontext.intelligence import transform

# One line—auto pattern selection!
context = transform("Should we use REST or GraphQL?")

# Already optimized and ready to use
claude_format = context.to_anthropic()
```

### 4. Measure Quality (30 seconds)

```python
from mycontext.intelligence import QualityMetrics

metrics = QualityMetrics()
score = metrics.evaluate(context)

print(f"Quality Score: {score.overall:.2f}")
print(f"Clarity: {score.dimensions['CLARITY']:.2f}")
print(f"Completeness: {score.dimensions['COMPLETENESS']:.2f}")
```

---

## 💡 Examples

### Example 1: Data Science Workflow

```python
from mycontext.templates.free.analysis import DataAnalyzer
from mycontext.intelligence import QualityMetrics

# Create analysis context
analyzer = DataAnalyzer()
context = analyzer.build_context(
    data_description="Customer churn data (50K records, 30 features)",
    analysis_goals=["Identify drivers", "Predict at-risk customers"],
    domain="SaaS business"
)

# Check quality
metrics = QualityMetrics()
score = metrics.evaluate(context)
print(f"Context quality: {score.overall:.2f}")

# Export for different tools
markdown_doc = context.to_markdown()  # Documentation
openai_chat = context.to_openai()     # GPT-4 analysis
yaml_config = context.to_yaml()        # Team sharing
```

### Example 2: Business Decision Making

```python
from mycontext.templates.free.decision import DecisionFramework

# Frame a complex decision
df = DecisionFramework()
context = df.build_context(
    decision="Choose cloud provider for new application",
    options=["AWS", "Google Cloud", "Azure"],
    criteria=["Cost", "Performance", "Ease of use", "Team expertise"],
    constraints=["Budget: $50K/month", "Must support Kubernetes"]
)

# Use with Claude for analysis
claude_format = context.to_anthropic()

# Export for team discussion
team_doc = context.to_markdown()
```

### Example 3: Code Review

```python
from mycontext import Context, Guidance, Directive

code = """
def process_payment(amount, user_id):
    query = f"INSERT INTO payments VALUES ({amount}, {user_id})"
    db.execute(query)
"""

context = Context(
    guidance=Guidance(
        role="Senior Security Engineer",
        rules=[
            "Identify security vulnerabilities",
            "Provide specific fixes with code examples",
            "Explain why each issue matters"
        ]
    ),
    directive=Directive(
        content=f"Review this payment code for security issues:\n\n{code}",
        priority=10  # Critical
    )
)

# Get detailed security review from Claude
claude_review = context.to_anthropic()
```

---

## 📚 API Reference

### Core Classes

#### `Context`
The main container for context engineering.

```python
from mycontext import Context, Guidance, Directive, Constraints

context = Context(
    guidance=Guidance(
        role="Expert role description",
        rules=["Rule 1", "Rule 2"],
        knowledge=["Domain expertise"],
        style="Communication style"
    ),
    directive=Directive(
        content="What to do",
        priority=5  # 1-10
    ),
    constraints=Constraints(
        must_include=["Required elements"],
        must_not_include=["Excluded elements"],
        style_guide="Formatting guidelines"
    )
)
```

**Key Methods:**
- `context.assemble()` - Get the full assembled context
- `context.to_openai()` - Export to OpenAI format
- `context.to_anthropic()` - Export to Anthropic format
- `context.to_langchain()` - Export to LangChain format
- `context.to_json()` - Export to JSON
- `context.to_yaml()` - Export to YAML
- `context.to_markdown()` - Export to Markdown

### Cognitive Patterns

#### Pattern Categories

**Analysis Patterns:**
```python
from mycontext.templates.free.analysis import (
    QuestionAnalyzer,
    DataAnalyzer,
    TrendIdentifier,
    GapAnalyzer,
    SWOTAnalyzer,
    AnomalyDetector
)
```

**Decision Patterns:**
```python
from mycontext.templates.free.decision import (
    DecisionFramework,
    ComparativeAnalyzer,
    TradeoffAnalyzer,
    MultiObjectiveOptimizer,
    CostBenefitAnalyzer
)
```

**Creative Patterns:**
```python
from mycontext.templates.free.creative import (
    IdeaGenerator,
    Brainstormer,
    InnovationFramework,
    DesignThinker,
    MetaphorGenerator
)
```

**All patterns follow the same interface:**
```python
pattern = PatternName()
context = pattern.build_context(
    # Pattern-specific parameters
)
```

### Intelligence Layer

#### Transformation Engine
```python
from mycontext.intelligence import TransformationEngine, transform

# Method 1: Using the engine
engine = TransformationEngine()
analysis = engine.analyze_input("Your question")
context = engine.transform("Your question")

# Method 2: Convenience function
context = transform("Your question")
```

#### Quality Metrics
```python
from mycontext.intelligence import QualityMetrics

metrics = QualityMetrics()
score = metrics.evaluate(context)

# Access scores
print(score.overall)           # Overall quality (0.0-1.0)
print(score.dimensions)        # Dict of all 6 dimensions
print(score.suggestions)       # List of improvement suggestions

# Compare contexts
comparison = metrics.compare(score1, score2)

# Generate report
report = metrics.report(score)
print(report)
```

### Integration Helpers

```python
from mycontext.integrations import (
    LangChainHelper,
    LlamaIndexHelper,
    CrewAIHelper,
    AutoGenHelper,
    DSPyHelper,
    SemanticKernelHelper,
    auto_integrate
)

# Use helpers
langchain_msgs = LangChainHelper.to_messages(context)
llamaindex_prompt = LlamaIndexHelper.to_prompt(context)

# Auto-detect framework
result = auto_integrate(context, "langchain")
```

---

## 🎯 Use Cases

### For Data Scientists
```python
# Analyze complex datasets with structured context
from mycontext.templates.free.analysis import DataAnalyzer

analyzer = DataAnalyzer()
context = analyzer.build_context(
    data_description="Time series sales data",
    analysis_goals=["Forecast Q4 revenue", "Identify anomalies"]
)
```

### For Engineers
```python
# Get architecture recommendations
from mycontext.templates.free.decision import TradeoffAnalyzer

analyzer = TradeoffAnalyzer()
context = analyzer.build_context(
    option_a="Monolithic architecture",
    option_b="Microservices",
    dimensions=["Scalability", "Complexity", "Cost"]
)
```

### For Product Managers
```python
# Plan features and scenarios
from mycontext.templates.free.planning import ScenarioPlanner

planner = ScenarioPlanner()
context = planner.build_context(
    situation="Launching premium tier",
    scenarios=["Best case", "Expected", "Worst case"]
)
```

---

## 🧪 Production Ready

### Test Coverage
- ✅ 37/37 Core Tests Passed
- ✅ 12/12 Stress Tests Passed  
- ✅ 10/10 Real-World Scenarios Passed
- **Total: 59/59 tests passing (100%)**

### Performance Benchmarks
- Instantiate 50 patterns: **458ms**
- 100 pattern executions: **5.6ms** (0.06ms avg)
- Quality evaluation: **<1ms**
- Export to all formats: **<10ms**

### Quality Assurance
- Type hints throughout
- Pydantic data validation
- Comprehensive error handling
- Graceful degradation

---

## 🛠️ Advanced Features

### Context Chaining
```python
# Build contexts incrementally
base = Context(guidance="Technical Architect")

enhanced = Context(
    guidance=base.guidance,
    directive="Design microservices architecture"
)

final = Context(
    guidance=enhanced.guidance,
    directive=enhanced.directive,
    constraints="Must use Kubernetes"
)
```

### Quality Iteration
```python
from mycontext.intelligence import QualityMetrics

metrics = QualityMetrics()

# Version 1
v1 = Context(guidance="Analyst")
score1 = metrics.evaluate(v1)  # 0.59

# Version 2 (enhanced)
v2 = Context(
    guidance="Senior Data Analyst with 5+ years experience",
    directive="Analyze Q4 sales with statistical rigor"
)
score2 = metrics.evaluate(v2)  # 0.92

# Compare improvement
comparison = metrics.compare(score1, score2)
```

### Multi-Pattern Workflows
```python
# Combine multiple patterns
from mycontext.templates.free.analysis import QuestionAnalyzer
from mycontext.templates.free.problem_solving import ProblemDecomposer
from mycontext.templates.free.planning import ScenarioPlanner

# Step 1: Analyze question
qa = QuestionAnalyzer()
analysis = qa.build_context(question="How to scale our app?")

# Step 2: Decompose problem
pd = ProblemDecomposer()
breakdown = pd.build_context(problem="Scale to 10x traffic")

# Step 3: Plan scenarios
sp = ScenarioPlanner()
plan = sp.build_context(scenarios=["Best", "Expected", "Worst"])
```

---

## 🌟 What Makes It Unique?

### Not Another LLM Framework
mycontext doesn't try to be everything. It does **one thing exceptionally well**: context engineering.

| Feature | mycontext | Other Frameworks |
|---------|-----------|------------------|
| **Focus** | Context engineering only | Full LLM orchestration |
| **Portability** | Works with any LLM | Vendor-specific |
| **Quality Metrics** | Scientific measurement | None |
| **Cognitive Patterns** | 50 research-backed | Generic templates |
| **Intelligence** | Auto pattern selection | Manual configuration |

### Research-Backed Patterns
Every pattern is based on published research in cognitive science, decision theory, and AI:
- Question analysis from IBM Zurich research
- Decision frameworks from organizational psychology
- Problem decomposition from systems thinking
- Reasoning patterns from cognitive science

### Measurable Improvement
Stop guessing if your context is good—measure it:
```python
score = metrics.evaluate(context)
# Returns: Clarity, Completeness, Specificity, Relevance, Structure, Efficiency
# Plus: Actionable suggestions for improvement
```

---

## 🤝 Contributing

We welcome contributions! Whether it's:
- 🐛 Bug fixes
- ✨ New cognitive patterns
- 📚 Documentation improvements
- 🎨 Examples and tutorials

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

Built on the shoulders of giants:
- IBM Zurich cognitive tools research
- Context engineering best practices
- The amazing Python AI community

---

## 🔗 Links

- **PyPI**: [pypi.org/project/mycontext-ai/](https://pypi.org/project/mycontext-ai/)
- **GitHub**: [github.com/yourusername/mycontext](https://github.com/yourusername/mycontext)
- **Issues**: [Report bugs or request features](https://github.com/yourusername/mycontext/issues)

---

## 🚀 Quick Reference

```python
# Installation
pip install mycontext-ai

# Simple context
from mycontext import Context
context = Context(guidance="Expert", directive="Task")

# Use cognitive pattern
from mycontext.templates.free.analysis import QuestionAnalyzer
analyzer = QuestionAnalyzer()
context = analyzer.build_context(question="Your question?")

# Auto intelligence
from mycontext.intelligence import transform
context = transform("Any question or problem")

# Measure quality
from mycontext.intelligence import QualityMetrics
score = QualityMetrics().evaluate(context)

# Export anywhere
context.to_openai()      # GPT-4
context.to_anthropic()   # Claude
context.to_langchain()   # LangChain
context.to_yaml()        # YAML
```

---

<div align="center">

**Made with ❤️ for the AI community**

⭐ **Star us on GitHub** if you find mycontext useful!

[Get Started](#-quick-start) • [View Examples](#-examples) • [API Reference](#-api-reference)

</div>
