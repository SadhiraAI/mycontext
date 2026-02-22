"""
Question Analyzer Template - Systematically analyze and break down questions.

Based on "understand_question" cognitive tool from IBM research and Context-Engineering.
Free tier template - part of mycontext open source.
"""

from mycontext import Pattern, Guidance, Directive, Constraints


class QuestionAnalyzer(Pattern):
    """
    Analyze questions to identify type, complexity, components, and approach.
    
    This cognitive tool helps break down complex questions before attempting
    to answer them, ensuring all aspects are properly understood.
    
    Based on IBM Zurich research: "Eliciting Reasoning in Language Models 
    with Cognitive Tools" (June 2025).
    
    Examples:
        >>> from mycontext.templates.free import QuestionAnalyzer
        >>> 
        >>> analyzer = QuestionAnalyzer()
        >>> result = analyzer.execute(
        ...     provider="gemini",
        ...     question="How does quantum entanglement work?",
        ...     depth="comprehensive"
        ... )
        >>> print(result.response)
        >>>
        >>> # Generic prompt mode — lighter, zero-cost
        >>> prompt = analyzer.generic_prompt(question="How does quantum entanglement work?", depth="comprehensive")
    
    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        'You are an expert question analyst. Systematically analyze the following '
        'question before answering it: "{question}"\n\n'
        "{context_section}"
        "Perform a {depth} analysis covering: "
        "(1) Classify the question type (factual, conceptual, analytical, evaluative, "
        "procedural, or causal). "
        "(2) Identify what cognitive action is required and the expected output format. "
        "(3) List the primary concepts, related domains, and scope boundaries. "
        "(4) Surface any implicit assumptions, potential ambiguities, and unstated context. "
        "(5) Rate complexity on a 1-10 scale considering conceptual difficulty, breadth, "
        "and reasoning depth. "
        "(6) Recommend an optimal answer strategy with structure and key considerations. "
        "(7) Restate the question making all implicit elements explicit.\n\n"
        "Do NOT answer the question — only analyze it."
    )

    def __init__(self):
        super().__init__(
            name="question_analyzer",
            guidance=Guidance(
                role="Expert Question Analyst and Cognitive Scientist",
                rules=[
                    "Break down questions systematically using structured analysis",
                    "Identify implicit assumptions and knowledge requirements",
                    "Classify questions by type and complexity",
                    "Provide clear reformulations that capture intent",
                    "Consider multiple interpretation angles"
                ],
                style="analytical, structured, thorough, pedagogical"
            ),
            directive_template="""Analyze this question comprehensively before attempting to answer it:

**QUESTION**: {question}

{context_section}

**ANALYSIS DEPTH**: {depth}

Provide a systematic analysis:

1. **Question Type Classification**:
   Identify the primary question type:
   - **Factual**: Seeking specific information or facts
   - **Conceptual**: Exploring ideas, theories, or abstract concepts
   - **Analytical**: Breaking down and examining components
   - **Evaluative**: Making judgments, comparisons, or assessments
   - **Procedural**: Explaining how to do something or how something works
   - **Causal**: Explaining why something happens or happened
   
   Primary type: [Identify]
   Secondary type (if any): [Identify]

2. **Core Task Identification**:
   - What specific cognitive action is required? (explain, compare, analyze, evaluate, etc.)
   - What is the expected output format? (explanation, list, diagram, argument, etc.)

3. **Key Components**:
   - **Primary concepts**: [List main ideas or entities involved]
   - **Related domains**: [Relevant fields of knowledge]
   - **Relationships**: [How components connect]
   - **Scope boundaries**: [What's included/excluded]

4. **Knowledge Prerequisites**:
   What background knowledge is necessary to answer this well?
   - **Required**: [Essential knowledge]
   - **Helpful**: [Supporting knowledge]
   - **Advanced**: [Deep expertise areas]

5. **Implicit Assumptions**:
   - Unstated assumptions in the question: [Identify]
   - Context clues: [What's implied about audience, purpose, level]
   - Potential ambiguities: [What needs clarification]

6. **Complexity Assessment** (1-10 scale):
   - **Rating**: [1-10]
   - **Factors**:
     * Conceptual difficulty: [Low/Medium/High]
     * Breadth of knowledge required: [Narrow/Moderate/Broad]
     * Reasoning depth needed: [Shallow/Moderate/Deep]
     * Interdisciplinary connections: [None/Few/Many]

7. **Answer Strategy Recommendation**:
   - **Optimal approach**: [Suggest reasoning method]
   - **Structure**: [How to organize the answer]
   - **Key considerations**: [What to emphasize]
   - **Potential pitfalls**: [What to avoid]

8. **Clarified Restatement**:
   Restate the question in your own words, making all implicit elements explicit.
   
   **Original**: {question}
   **Clarified**: [Your reformulation]

**OUTPUT FORMAT**: Structured analysis with clear sections as above.

Once you've completed this analysis, you'll be well-prepared to address the question effectively.""",
            input_schema={
                "question": str,
                "context_section": str,
                "depth": str
            },
            constraints=Constraints(
                must_include=[
                    "question_type",
                    "complexity_rating",
                    "answer_strategy",
                    "clarified_restatement"
                ],
                must_not_include=["actual answer to the question"],
                style_guide="Use structured format with clear headings and bullet points"
            )
        )
    
    def _render_context_section(self, context):
        """Render optional context section."""
        if context:
            return f"\n**ADDITIONAL CONTEXT**: {context}\n"
        return ""
    
    def build_context(self, question="", context=None, depth="comprehensive", **kwargs):
        """
        Build context for question analysis (without executing).
        
        Args:
            question: The question to analyze
            context: Optional additional context
            depth: Analysis depth ("brief", "moderate", "comprehensive")
            **kwargs: Additional options
        
        Returns:
            Context object ready for export/use
        """
        # Provide defaults for optional fields
        if context is None:
            context = ""
        
        context_section = self._render_context_section(context)
        
        # Remove context_section from kwargs if present to avoid duplicate
        kwargs.pop('context_section', None)
        
        # Only pass template variables (not 'context', only 'context_section')
        return super().build_context(
            question=question,
            context_section=context_section,
            depth=depth,
            **kwargs
        )
    
    def execute(self, provider="gemini", question="", context=None, depth="comprehensive", **kwargs):
        """
        Execute question analysis.
        
        Args:
            provider: LLM provider to use ("gemini", "openai", "anthropic")
            question: The question to analyze
            context: Optional additional context
            depth: Analysis depth ("brief", "moderate", "comprehensive")
            **kwargs: Additional provider options (temperature, max_tokens, etc.)
        
        Returns:
            ProviderResponse with the analysis
        """
        # Provide defaults for optional fields
        if context is None:
            context = ""
        
        context_section = self._render_context_section(context)
        
        # Remove context_section from kwargs if present to avoid duplicate
        kwargs.pop('context_section', None)
        
        # Only pass template variables (not 'context', only 'context_section')
        return super().execute(
            provider=provider,
            question=question,
            context_section=context_section,
            depth=depth,
            **kwargs
        )
