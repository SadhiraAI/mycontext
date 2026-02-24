---
sidebar_position: 7
title: CodeReviewer
description: Comprehensive code review across security, performance, and maintainability. Severity-ranked findings with fix examples, security scores, and quality ratings.
---

# CodeReviewer

**Category:** Specialized | **Module:** `mycontext.templates.free.specialized`

Performs systematic, severity-ranked code reviews. Catches security vulnerabilities (SQL injection, XSS, etc.), performance bottlenecks (N+1 queries, inefficient algorithms), and best practice violations — with specific line references, explanations of why each issue matters, and working fix examples.

## When to Use

- Pull request review
- Security audit
- Onboarding code quality check
- Legacy code assessment
- Before production deployment
- Multi-language project review

## Quick Start

```python
from mycontext.templates.free.specialized import CodeReviewer

reviewer = CodeReviewer()

code = """
def fetch_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return db.execute(query)
"""

result = reviewer.execute(
    provider="gemini",
    code=code,
    language="Python",
    focus_areas=["security", "best_practices"],
)
print(result.response)
```

## Methods

### `build_context(code, language="Python", context=None, focus_areas=None)`

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `code` | `str` | `""` | The code to review |
| `language` | `str` | `"Python"` | Programming language |
| `context` | `str \| None` | `None` | Purpose, architecture context, constraints |
| `focus_areas` | `list[str] \| None` | All areas | Review focus areas |

**Default `focus_areas`**: `["security", "performance", "best_practices", "maintainability"]`

### `execute(provider, code, language="Python", context=None, focus_areas=None, **kwargs)`

```python
result = reviewer.execute(
    provider="gemini",
    code=your_code,
    language="Python",
    context="Payment processing module, PCI-DSS compliance required",
    focus_areas=["security"],
)
```

## Severity Framework

Every finding is categorized by severity with actionable fixes:

### 🔴 Critical — Must Fix
Security vulnerabilities, critical bugs, data exposure risks, injection vectors. For each: exact location, risk explanation, corrected code snippet.

```
### Security Vulnerabilities
- **Issue**: SQL Injection on line 2
- **Location**: `fetch_user()` function, f-string interpolation
- **Risk**: Attacker can execute arbitrary SQL: `user_id=1; DROP TABLE users`
- **Fix**:
  \`\`\`python
  # Bad
  query = f"SELECT * FROM users WHERE id = {user_id}"
  
  # Good
  query = "SELECT * FROM users WHERE id = ?"
  return db.execute(query, (user_id,))
  \`\`\`
```

### 🟠 High — Should Fix
Performance bottlenecks, missing error handling, significant best practice violations.

### 🟡 Medium — Consider Fixing
Code quality, readability, maintainability improvements.

### 🟢 Low — Nice to Have
Style inconsistencies, minor optimizations.

### ✅ Strengths — Good Practices
Acknowledges what's done well — keeps feedback constructive.

## Focus Areas

| Focus Area | What gets reviewed |
|-----------|-------------------|
| `"security"` | Injections, auth issues, data exposure, crypto misuse |
| `"performance"` | N+1 queries, inefficient algorithms, memory leaks |
| `"best_practices"` | SOLID principles, error handling, naming conventions |
| `"maintainability"` | Complexity, documentation, testability, modularity |

## Examples

### Security-Focused Review

```python
code = """
import os
import pickle

def load_user_data(filename):
    with open(f"/user_data/{filename}", 'rb') as f:
        return pickle.load(f)

def execute_command(cmd):
    os.system(cmd)
"""

result = reviewer.execute(
    provider="openai",
    code=code,
    language="Python",
    focus_areas=["security"],
)
```

### Full Review with Context

```python
result = reviewer.execute(
    provider="gemini",
    code=api_handler_code,
    language="Python",
    context="FastAPI endpoint handling user authentication and payment processing",
    focus_areas=["security", "performance", "best_practices"],
)
```

### JavaScript Review

```python
js_code = """
function getUserInput() {
    const input = document.getElementById('userInput').value;
    document.getElementById('output').innerHTML = input;
}
"""

result = reviewer.execute(
    provider="openai",
    code=js_code,
    language="JavaScript",
    focus_areas=["security"],
)
# Will catch XSS vulnerability
```

### Multi-File Context

```python
import json

result = reviewer.execute(
    provider="anthropic",
    code=open("src/auth/login.py").read(),
    language="Python",
    context=f"""
    Auth module in Django application.
    Database: PostgreSQL.
    External auth: OAuth2 with Google/GitHub.
    Runs behind nginx reverse proxy.
    """,
)
```

## Output Format

The review ends with an overall assessment:

```
## 6. OVERALL ASSESSMENT
- **Code Quality Score**: 4/10 — Multiple critical security issues
- **Security Score**: 2/10 — SQL injection, path traversal, command injection
- **Maintainability Score**: 6/10 — Clear structure but needs error handling

**Priority Actions**:
1. Fix SQL injection vulnerability (line 2)
2. Sanitize file path input (line 7)
3. Replace os.system() with subprocess with arguments list

## 7. RECOMMENDATIONS
**Immediate Actions**:
- Add parameterized queries for all DB operations
- Validate and sanitize all file paths
- Use subprocess.run(args_list) instead of os.system(string)

**Testing Recommendations**:
- Add security tests for injection attempts
- Test with malicious file path inputs
```

## Generic Prompt Mode

```python
# Zero-cost review prompt
prompt = reviewer.generic_prompt(
    code="def greet(name): return f'Hello {name}'",
    language="Python",
    focus_areas="security, best_practices",
)
```

## API Reference

| Method | Returns | Description |
|--------|---------|-------------|
| `build_context(code, language, context, focus_areas)` | `Context` | Assembled context |
| `execute(provider, code, language, context, focus_areas, **kwargs)` | `ProviderResponse` | Execute review |
| `generic_prompt(code, language, context_section, focus_areas)` | `str` | Zero-cost prompt string |
