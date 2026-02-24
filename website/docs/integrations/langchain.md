---
sidebar_position: 2
title: LangChain
description: Use mycontext cognitive patterns as system prompts in LangChain chains, LCEL pipelines, and LangGraph agents. Convert any Context to messages, PromptTemplates, or ChatPromptTemplates.
---

# LangChain

Use any mycontext cognitive pattern as the system prompt in your LangChain chain. Three export paths: native `to_langchain()`, the `LangChainHelper` class, or direct `to_messages()`.

```bash
pip install mycontext-ai langchain-core langchain-openai
```

## Quick Start

```python
from mycontext.templates.free.specialized import CodeReviewer
from mycontext.integrations import LangChainHelper
from langchain_openai import ChatOpenAI

# Build context with cognitive framework
ctx = CodeReviewer().build_context(
    code=my_code,
    language="Python",
    focus_areas=["security", "performance"],
)

# Convert to LangChain messages
messages = LangChainHelper.to_messages(ctx)

# Use with any LangChain LLM
chat = ChatOpenAI(model="gpt-4o-mini")
response = chat.invoke(messages)
print(response.content)
```

## `ctx.to_langchain()`

The native export method returns a dict with the assembled system message and structured metadata:

```python
lc = ctx.to_langchain()
# {
#   "system_message": "## Role\nSenior code reviewer...\n## Directive\n...",
#   "context": {"guidance": {...}, "directive": {...}, ...},
#   "guidance": {"role": "Senior code reviewer", "rules": [...]},
#   "directive": {"content": "Review the following code...", "priority": 8},
#   "knowledge": None,
# }

from langchain_core.messages import SystemMessage
system_msg = SystemMessage(content=lc["system_message"])
```

## LangChainHelper Methods

### `to_messages(context, user_message=None)`

Convert to LangChain message objects:

```python
from mycontext.integrations import LangChainHelper
from langchain_openai import ChatOpenAI

ctx = RootCauseAnalyzer().build_context(
    problem="Database queries slowing down",
    depth="thorough",
)

# System message only
messages = LangChainHelper.to_messages(ctx)

# System + user message
messages = LangChainHelper.to_messages(
    ctx,
    user_message="Focus particularly on the caching layer",
)

chat = ChatOpenAI()
response = chat.invoke(messages)
```

### `to_prompt_template(context)`

Convert to LangChain `PromptTemplate`:

```python
from mycontext.integrations import LangChainHelper

template = LangChainHelper.to_prompt_template(ctx)
# → PromptTemplate with the assembled context as template
```

### `to_chat_prompt(context)`

Convert to `ChatPromptTemplate`:

```python
from mycontext.integrations import LangChainHelper
from langchain_openai import ChatOpenAI

chat_prompt = LangChainHelper.to_chat_prompt(ctx)
chat = ChatOpenAI()

chain = chat_prompt | chat
response = chain.invoke({})
```

## LCEL Pipeline

Use mycontext as the system prompt in an LCEL (LangChain Expression Language) chain:

```python
from mycontext.templates.free.analysis import DataAnalyzer
from mycontext.integrations import LangChainHelper
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# Build cognitive context
ctx = DataAnalyzer().build_context(
    data_description="Monthly SaaS metrics: MRR, churn, NPS, support tickets",
    goal="Identify leading indicators of churn",
)

# Build LCEL chain
chat = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

def make_messages(data):
    base_messages = LangChainHelper.to_messages(ctx)
    base_messages.append(HumanMessage(content=data["query"]))
    return base_messages

chain = make_messages | chat | parser

response = chain.invoke({"query": "What patterns do you see in the Q3 data?"})
print(response)
```

## LangGraph Agent

Use mycontext to power a LangGraph agent's system prompt:

```python
from mycontext.templates.free.reasoning import StepByStepReasoner
from mycontext.integrations import LangChainHelper
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

# Build a rich reasoning context
ctx = StepByStepReasoner().build_context(
    problem="Design a fault-tolerant distributed task queue",
    domain="software architecture",
)

# Get the system message
lc = ctx.to_langchain()
system_msg = lc["system_message"]

# Create LangGraph ReAct agent with mycontext system prompt
llm = ChatOpenAI(model="gpt-4o")
agent = create_react_agent(
    llm,
    tools=my_tools,
    state_modifier=system_msg,
)

result = agent.invoke({"messages": [("user", "Start the design process")]})
```

## Pattern + LangChain RAG

Combine mycontext patterns with LangChain RAG:

```python
from mycontext.templates.free.analysis import QuestionAnalyzer
from mycontext.integrations import LangChainHelper
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough

# Build question analysis context
ctx = QuestionAnalyzer().build_context(
    question="What are the main risks of our AWS migration?",
    depth="comprehensive",
)

# Set up RAG components
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(your_documents, embeddings)
retriever = vectorstore.as_retriever()

# Build RAG chain with cognitive framework as system prompt
messages = LangChainHelper.to_messages(ctx)
chat = ChatOpenAI(model="gpt-4o-mini")

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

from langchain_core.messages import HumanMessage

def rag_chain(question):
    docs = retriever.invoke(question)
    context_str = format_docs(docs)
    
    rag_messages = messages + [
        HumanMessage(content=f"Context from documents:\n{context_str}\n\nQuestion: {question}")
    ]
    return chat.invoke(rag_messages).content

result = rag_chain("What are the main risks of our AWS migration?")
```

## API Reference

### `LangChainHelper`

| Method | Returns | Description |
|--------|---------|-------------|
| `to_messages(context, user_message)` | `list` | LangChain message objects |
| `to_prompt_template(context)` | `PromptTemplate` | LangChain PromptTemplate |
| `to_chat_prompt(context)` | `ChatPromptTemplate` | LangChain ChatPromptTemplate |

### `ctx.to_langchain()`

```python
{
    "system_message": str,   # Assembled context string
    "context": dict,         # Full context as dict
    "guidance": dict | None, # Guidance component
    "directive": dict | None,# Directive component
    "knowledge": str | None, # Knowledge component
}
```
