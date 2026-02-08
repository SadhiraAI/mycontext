# mycontext

> **Transform any question into perfect context - use it anywhere**

[![PyPI](https://img.shields.io/pypi/v/mycontext)](https://pypi.org/project/mycontext/)
[![Python](https://img.shields.io/pypi/pyversions/mycontext)](https://pypi.org/project/mycontext/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/mycontext-ai/mycontext/workflows/tests/badge.svg)](https://github.com/mycontext-ai/mycontext/actions)
[![codecov](https://codecov.io/gh/mycontext-ai/mycontext/branch/main/graph/badge.svg)](https://codecov.io/gh/mycontext-ai/mycontext)

## What is mycontext?

**mycontext** is the universal context transformation engine for AI applications.

**The Problem:** Raw questions and unstructured prompts lead to inconsistent AI behavior, context rot, and wasted tokens.

**The Solution:** Transform questions into perfect, portable contexts that work with ANY AI system.

```python
from mycontext.templates.free import QuestionAnalyzer

# Step 1: Transform raw question into perfect context
question = "Should I invest in solar panels?"
analyzer = QuestionAnalyzer()

# This creates a structured, optimized context
context = analyzer.build_context(
    question=question,
    context="Home: 2000 sqft, California, $200/month bill",
    depth="comprehensive"
)

# Step 2: Use this context ANYWHERE!

# Option A: LangGraph
langgraph_agent.invoke(context.to_langchain())

# Option B: CrewAI  
crew.kickoff(context=context.to_dict())

# Option C: Direct OpenAI
openai.chat.completions.create(messages=context.to_messages())

# Option D: Any framework via JSON
requests.post(api_url, json=context.to_json())

# Option E: Even humans can read it!
print(context.to_markdown())
```

**One transformation → Infinite uses**

## Why mycontext?

### 🎯 The Core Insight

**Your questions need transformation, not just prompting.**

```
❌ Old Way: Raw Question → LLM
   "Should I invest in solar panels?"
   → Inconsistent, shallow responses

✅ New Way: Raw Question → mycontext → Perfect Context → LLM
   "Should I invest in solar panels?"
   → Structured analysis framework
   → Decision criteria
   → Evidence requirements
   → Financial calculations
   → Risk assessment
   = Consistent, thorough, high-quality responses
```

### 💡 What Makes mycontext Unique?

1. **Universal Transformation Engine**
   - Input: Raw questions/tasks
   - Process: Research-backed templates + RAG + optimization
   - Output: Perfect, portable contexts

2. **Works with EVERYTHING**
   - ✅ LangGraph, CrewAI, AutoGen (agent frameworks)
   - ✅ LangChain, LlamaIndex, Haystack (RAG frameworks)
   - ✅ OpenAI, Anthropic, Google (direct LLM APIs)
   - ✅ OpenCE (context engineering backends)
   - ✅ Custom APIs, internal tools
   - ✅ Even human analysts!

3. **Research-Backed Templates**
   - Based on "Context Engineering" book (IBM Zurich Research)
   - Cognitive tools from scientific research
   - Not hand-crafted prompts - engineered systems

4. **Three User Levels**
   - **General users:** Use templates (no coding)
   - **Professionals:** Customize patterns (light Python)
   - **Developers:** Build production systems (full SDK)

5. **API-Ready Architecture**
   - Universal export formats (JSON, messages, markdown)
   - RESTful API coming soon
   - Cloud platform in development  

---

## 🚀 Quick Start

### Installation

```bash
# Core SDK
pip install mycontext

# With OpenAI
pip install mycontext[openai]

# With all providers (OpenAI, Anthropic, Google)
pip install mycontext[all]
```

### 30-Second Example

```python
from mycontext.templates.free import QuestionAnalyzer

# Transform question into perfect context
analyzer = QuestionAnalyzer()
context = analyzer.build_context(
    question="Should I invest in solar panels?",
    context="California home, $200/mo electric bill"
)

# Use it anywhere!
# → Export for OpenAI
messages = context.to_messages()

# → Export for LangGraph
langchain_format = context.to_langchain()

# → Export as JSON for API
json_data = context.to_json()

# → Show to humans
print(context.to_markdown())
```

**That's it!** One transformation → Use anywhere.

## 🎯 Core Features

### 1. Universal Context Transformation

Transform raw questions into structured, optimized contexts:

```python
from mycontext import Context, Guidance, Directive

# Build a perfect context
context = Context(
    guidance=Guidance(
        role="Expert Financial Advisor",
        rules=[
            "Provide evidence-based analysis",
            "Consider risk factors",
            "Include calculations"
        ],
        style="analytical, balanced"
    ),
    directive=Directive("Should I invest in solar panels?")
)

# Export to any format
context.to_messages()      # → OpenAI, Anthropic, Google
context.to_langchain()     # → LangChain, LangGraph
context.to_json()          # → APIs, databases
context.to_markdown()      # → Humans, documentation
```

### 2. Research-Backed Templates

Pre-built cognitive tools from the "Context Engineering" book:

```python
from mycontext.templates.free import (
    QuestionAnalyzer,        # Systematic question analysis
    StepByStepReasoner,      # Methodical problem solving
    CodeReviewer,            # Expert code review
    ConceptExplainer,        # Clear explanations
    ContentOutliner          # Structured content planning
)

# Use like a function - no prompt engineering needed
analyzer = QuestionAnalyzer()
result = analyzer.execute(
    provider="openai",
    question="Should we migrate to microservices?"
)
```

### 3. RAG Integration (Knowledge Grounding)

Enrich contexts with relevant knowledge:

```python
from mycontext.intelligence.rag import create_retriever

# Create retriever with semantic chunking
retriever = create_retriever(
    documents=["doc1.pdf", "doc2.md", ...],
    embedder="openai",
    chunk_strategy="semantic",
    vector_store="faiss"
)

# Retrieve and build context
docs = retriever.retrieve("How do we handle auth?", k=3)
knowledge_context = retriever.build_context(docs)

# Add to any context
context = Context(
    guidance=Guidance(role="Expert"),
    knowledge=knowledge_context
)
```

### 4. Session Management (Prevents Context Rot)

Multi-turn conversations without unbounded growth:

```python
from mycontext import Session, FileArchive

# Create managed session
session = Session(
    max_tokens=4000,           # Token budget
    pruning_strategy="sliding" # Or "importance", "summary"
)

# Automatically manages context
session.add_user_message("What is context rot?")
session.add_assistant_message("Context rot is...")
session.add_user_message("How to prevent it?")  # Auto-prunes if needed

# Persist to disk
archive = FileArchive("./sessions")
archive.save_session(session, tags=["context-engineering"])
```

### 5. Production Utilities

Token optimization, cost tracking, validation:

```python
from mycontext.utils import (
    TokenOptimizer,     # Reduce token usage
    CostTracker,        # Monitor spending
    ContextValidator,   # Validate structure
    StructuredOutput    # Parse responses
)

# Optimize context
optimizer = TokenOptimizer(max_tokens=2000)
optimized = optimizer.optimize(context)

# Track costs
tracker = CostTracker()
tracker.track(result, session_id="user_123")
print(f"Total cost: ${tracker.total_cost()}")
```

---

## 🔌 Framework Integration

mycontext works with ANY framework or LLM:

```python
# LangGraph
from langgraph.graph import StateGraph
context = my_context.to_langchain()
graph.add_node("agent", lambda s: use_context(context))

# CrewAI
from crewai import Crew
crew = Crew(agents=[...], context=my_context.to_dict())

# Direct OpenAI
import openai
openai.chat.completions.create(messages=my_context.to_messages())

# Custom API
import requests
requests.post(api_url, json=my_context.to_json())
```

👉 **[LangGraph Integration Guide](LANGGRAPH_INTEGRATION.md)**

---

## 📚 Documentation & Examples

- 📖 **[POSITIONING.md](POSITIONING.md)** - Vision, strategy, competitive analysis
- 🔗 **[LANGGRAPH_INTEGRATION.md](LANGGRAPH_INTEGRATION.md)** - LangGraph integration guide
- 📓 **[transformation_showcase.ipynb](transformation_showcase.ipynb)** - Interactive demo
- 📦 **[Templates Documentation](src/mycontext/templates/README.md)** - All available templates
- 🎯 **[Examples](examples/)** - Reference implementations

---

## 🗺️ Roadmap

### Current (v0.1) ✅
- ✅ Core transformation engine
- ✅ Universal export formats (messages, JSON, markdown, LangChain)
- ✅ 5 free templates
- ✅ RAG with semantic chunking & reranking
- ✅ Session management
- ✅ Token optimization

### Q1 2026 🔄
- RESTful API
- Cloud platform (mycontext.ai)
- 10 more free templates
- Advanced RAG features
- Deep LangGraph/CrewAI integration

### Q2-Q3 2026 📅
- 50+ premium templates
- Visual context builder
- Team collaboration
- Enterprise features (SSO, teams)
- JavaScript/TypeScript SDK

### Q4 2026+ 🎯
- Template marketplace
- Multi-language support
- White-label solutions
- Self-improving contexts (ML)

---

## 🤝 Contributing

We love contributions! See **[CONTRIBUTING.md](CONTRIBUTING.md)** for guidelines.

### Development Setup

```bash
# Clone the repo
git clone https://github.com/mycontext-ai/mycontext.git
cd mycontext

# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .
mypy src/
```

---

## 📄 License

MIT © 2026 mycontext

---

## 🌟 Show Your Support

If mycontext helps you build better AI applications:

- ⭐ **Star us on GitHub**
- 💬 **Join our [Discord](https://discord.gg/mycontext)**
- 🐦 **Follow us on [Twitter/X](https://twitter.com/mycontext_ai)**
- 📧 **Subscribe to our [Newsletter](https://mycontext.ai/newsletter)**

---

**Built with ❤️ for anyone building with AI.**

**Transform your questions. Use them anywhere. Build better AI.**

[Get Started](https://docs.mycontext.ai) | [Discord](https://discord.gg/mycontext) | [GitHub](https://github.com/mycontext-ai/mycontext)
