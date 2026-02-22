"""
Code Reviewer Template - Systematic code review with security, performance, and best practices.

Based on industry best practices and cognitive tools methodology.
Free tier template - part of mycontext open source.
"""

from mycontext import Constraints, Guidance, Pattern


class CodeReviewer(Pattern):
    """
    Perform comprehensive code reviews across security, performance, and quality dimensions.
    
    This template systematically analyzes code for:
    - Security vulnerabilities (SQL injection, XSS, etc.)
    - Performance issues (N+1 queries, inefficient algorithms)
    - Best practice violations (naming, structure, patterns)
    - Maintainability concerns (complexity, documentation)
    
    Examples:
        >>> from mycontext.templates.free import CodeReviewer
        >>> 
        >>> reviewer = CodeReviewer()
        >>> code = '''
        ... def fetch_user(user_id):
        ...     query = f"SELECT * FROM users WHERE id = {user_id}"
        ...     return db.execute(query)
        ... '''
        >>> 
        >>> result = reviewer.execute(
        ...     provider="gemini",
        ...     code=code,
        ...     language="Python",
        ...     focus_areas=["security", "best_practices"]
        ... )
        >>> print(result.response)
    
    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "You are a senior software engineer and security expert. Perform a systematic "
        "code review:\n\n"
        "Code:\n{code}\n\n"
        "Language: {language}\n"
        "{context_section}\n"
        "Focus areas: {focus_areas}\n\n"
        "Review by severity: "
        "(1) CRITICAL — identify security vulnerabilities, critical bugs, data exposure "
        "risks, and injection vectors. For each, specify the exact location, explain the "
        "risk, and provide a corrected code snippet. "
        "(2) HIGH — flag performance bottlenecks, missing error handling, and violations "
        "of best practices. "
        "(3) MEDIUM — note code quality issues, missing documentation, and "
        "maintainability concerns. "
        "(4) LOW — style inconsistencies and minor improvements. "
        "(5) STRENGTHS — acknowledge good practices in the code. "
        "(6) Provide an overall assessment: security score (1-10), code quality score "
        "(1-10), priority actions, and both immediate and long-term recommendations.\n\n"
        "Be specific — reference exact locations. Explain WHY each issue matters, not "
        "just what is wrong."
    )


    def __init__(self):
        super().__init__(
            name="code_reviewer",
            guidance=Guidance(
                role="Senior Software Engineer and Security Expert",
                rules=[
                    "Identify concrete, actionable issues with specific line references",
                    "Prioritize critical security vulnerabilities first",
                    "Explain WHY each issue matters, not just WHAT is wrong",
                    "Provide specific code examples for fixes",
                    "Be constructive - acknowledge good practices when present",
                    "Consider the broader context and architecture"
                ],
                style="professional, thorough, constructive, specific"
            ),
            directive_template="""Review this {language} code systematically across multiple dimensions.

**CODE TO REVIEW**:
```{language}
{code}
```

{context_section}

**FOCUS AREAS**: {focus_areas}

Provide a comprehensive code review organized by severity and category:

## 1. CRITICAL ISSUES (🔴 Must Fix)

Security vulnerabilities and bugs that could cause data loss, security breaches, or system crashes.

### Security Vulnerabilities
- **Issue**: [Specific vulnerability - e.g., "SQL Injection on line 5"]
- **Location**: [Line numbers or function names]
- **Risk**: [What could go wrong]
- **Fix**: [Specific code example]
```{language}
# Bad
[problematic code]

# Good
[fixed code with explanation]
```

### Critical Bugs
[Same format as above]

## 2. HIGH PRIORITY ISSUES (🟠 Should Fix)

Performance problems, code smells, and significant best practice violations.

### Performance Issues
- **Issue**: [e.g., "N+1 query problem in user_data() function"]
- **Impact**: [How this affects performance]
- **Fix**: [Optimized approach]

### Best Practice Violations
- **Issue**: [Specific violation]
- **Why it matters**: [Explanation]
- **Recommendation**: [How to improve]

## 3. MEDIUM PRIORITY (🟡 Consider Fixing)

Code quality, readability, and maintainability improvements.

### Code Quality
- Naming conventions
- Function complexity
- Code duplication
- Missing error handling

### Documentation
- Missing docstrings
- Unclear variable names
- Incomplete comments

## 4. LOW PRIORITY (🟢 Nice to Have)

Style preferences and minor optimizations.

### Style & Conventions
[Minor improvements]

## 5. STRENGTHS (✅ Good Practices)

Acknowledge what's done well:
- [Positive aspect 1]
- [Positive aspect 2]

## 6. OVERALL ASSESSMENT

- **Code Quality Score**: [1-10 with justification]
- **Security Score**: [1-10 with justification]
- **Maintainability Score**: [1-10 with justification]

**Priority Actions** (Top 3):
1. [Most important fix]
2. [Second priority]
3. [Third priority]

## 7. RECOMMENDATIONS

**Immediate Actions**:
- [What to fix first]

**Long-term Improvements**:
- [Architectural or design suggestions]

**Testing Recommendations**:
- [What tests should be added]

**OUTPUT REQUIREMENTS**:
- Be specific with line numbers and code examples
- Explain the "why" behind each issue
- Provide working fix examples
- Prioritize by severity and impact""",
            input_schema={
                "code": str,
                "language": str,
                "context": str,
                "focus_areas": str
            },
            constraints=Constraints(
                must_include=[
                    "specific line numbers or locations",
                    "code examples for fixes",
                    "explanation of why issues matter",
                    "prioritization by severity"
                ],
                must_not_include=[
                    "vague generalities without specifics",
                    "criticisms without constructive solutions"
                ],
                style_guide="Use markdown formatting with code blocks and severity indicators (🔴🟠🟡🟢✅)"
            )
        )

    def _render_context_section(self, context):
        """Render optional context section."""
        if context:
            return f"\n**ADDITIONAL CONTEXT**: {context}\n"
        return ""

    def _render_focus_areas(self, focus_areas):
        """Format focus areas list."""
        if isinstance(focus_areas, list):
            return ", ".join(focus_areas)
        return str(focus_areas)

    def build_context(self, code="", language="Python", context=None, focus_areas=None, **kwargs):
        if context is None:
            context = ""
        if focus_areas is None:
            focus_areas = ["security", "performance", "best_practices", "maintainability"]
        context_section = self._render_context_section(context)
        focus_areas_str = self._render_focus_areas(focus_areas)
        return super().build_context(
            code=code,
            language=language,
            context=context,
            context_section=context_section,
            focus_areas=focus_areas_str,
            **kwargs
        )

    def execute(
        self,
        provider="gemini",
        code="",
        language="Python",
        context=None,
        focus_areas=None,
        **kwargs
    ):
        """
        Execute code review.
        
        Args:
            provider: LLM provider to use ("gemini", "openai", "anthropic")
            code: The code to review
            language: Programming language ("Python", "JavaScript", "Go", etc.)
            context: Optional context about the code's purpose
            focus_areas: List of areas to focus on (default: all)
            **kwargs: Additional provider options
        
        Returns:
            ProviderResponse with the review
        """
        if context is None:
            context = ""
        if focus_areas is None:
            focus_areas = ["security", "performance", "best_practices", "maintainability"]

        context_section = self._render_context_section(context)
        focus_areas_str = self._render_focus_areas(focus_areas)

        return super().execute(
            provider=provider,
            code=code,
            language=language,
            context=context,
            context_section=context_section,
            focus_areas=focus_areas_str,
            **kwargs
        )
