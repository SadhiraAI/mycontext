"""
Transformation Engine - Automatic pattern selection and context transformation

Core intelligence layer that analyzes inputs and selects optimal cognitive patterns.
This is the heart of mycontext's automatic context engineering.
"""

import logging
import threading
from dataclasses import dataclass
from enum import Enum
from typing import Any

from ..core import Context
from ..structure.pattern import Pattern

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Module-level lazy singleton for the pattern registry
# ---------------------------------------------------------------------------
# Research basis:
#   "Lazy initialization" (GoF Design Patterns, 1994): defer expensive
#   work until first use.  TransformationEngine.__init__ previously called
#   _load_patterns() synchronously, importing all template modules even when
#   the engine was only being inspected or type-checked.  With a module-level
#   singleton, the import cost is paid once per Python process across all
#   instances, not once per instantiation.
#
#   Thread safety: a threading.Lock prevents the "double-checked locking"
#   race condition that would cause duplicate pattern loading under concurrent
#   instantiation.
#
# The registry is keyed by include_enterprise (True/False) so enterprise and
# free-only instances each get their own lazily-built cache.

_PATTERN_REGISTRY_CACHE: dict[bool, dict[str, Pattern]] = {}
_PATTERN_REGISTRY_LOCK = threading.Lock()


class InputType(Enum):
    """Types of inputs the engine can process."""
    QUESTION = "question"
    PROBLEM = "problem"
    DECISION = "decision"
    CONCEPT = "concept"
    COMPARISON = "comparison"
    CAUSAL = "causal"
    STATEMENT = "statement"
    TASK = "task"
    CONVERSATION = "conversation"


class ComplexityLevel(Enum):
    """Complexity assessment levels."""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    HIGHLY_COMPLEX = "highly_complex"


@dataclass
class InputAnalysis:
    """Analysis of an input for pattern selection."""
    input_type: InputType
    complexity: ComplexityLevel
    domain: str
    key_concepts: list[str]
    requires_reasoning: bool
    requires_comparison: bool
    requires_verification: bool
    ambiguity_level: str  # "low", "medium", "high"
    recommended_patterns: list[str]
    confidence: float  # 0.0 to 1.0


class TransformationEngine:
    """
    Intelligent context transformation engine with automatic pattern selection.
    
    Core features:
    - Analyzes input characteristics
    - Selects optimal cognitive patterns
    - Composes multi-pattern transformations
    
    Example:
        >>> engine = TransformationEngine()
        >>> context = engine.transform(
        ...     input="Should we migrate to microservices?",
        ...     metadata={"domain": "software", "user_level": "professional"}
        ... )
        >>> print(f"Patterns used: {context.metadata['patterns_applied']}")
    
    This is the core innovation of mycontext - automatic, intelligent transformation.
    """

    def __init__(self, include_enterprise: bool = True):
        """
        Initialize the transformation engine.

        Pattern modules are loaded once per (include_enterprise) variant and
        cached at module level — subsequent instantiations reuse the cached
        registry without re-importing any modules.

        Args:
            include_enterprise: If False, only free patterns are used.
        """
        self.include_enterprise = include_enterprise
        # Delegate to the lazy-loaded module-level cache.
        self._pattern_registry = self._get_registry(include_enterprise)

    # ------------------------------------------------------------------
    # Lazy singleton registry
    # ------------------------------------------------------------------

    @staticmethod
    def _get_registry(include_enterprise: bool) -> dict[str, "Pattern"]:
        """Return (and lazily build) the module-level pattern registry."""
        if include_enterprise in _PATTERN_REGISTRY_CACHE:
            return _PATTERN_REGISTRY_CACHE[include_enterprise]

        with _PATTERN_REGISTRY_LOCK:
            # Double-checked locking: re-test inside the lock to avoid
            # duplicate loading if two threads arrived simultaneously.
            if include_enterprise in _PATTERN_REGISTRY_CACHE:
                return _PATTERN_REGISTRY_CACHE[include_enterprise]

            registry: dict[str, Pattern] = {}
            TransformationEngine._load_patterns_into(registry, include_enterprise)
            _PATTERN_REGISTRY_CACHE[include_enterprise] = registry
            logger.debug(
                "TransformationEngine: loaded %d patterns (enterprise=%s)",
                len(registry),
                include_enterprise,
            )
            return registry

    @staticmethod
    def _load_patterns_into(registry: dict[str, "Pattern"], include_enterprise: bool) -> None:
        """Populate *registry* with all applicable patterns."""
        from ..templates.free import (
            IntentRecognizer,
            QuestionAnalyzer,
            RiskAssessor,
            RootCauseAnalyzer,
            SocraticQuestioner,
            StepByStepReasoner,
        )

        patterns: list[Pattern] = [
            QuestionAnalyzer(),
            StepByStepReasoner(),
            SocraticQuestioner(),
            RiskAssessor(),
            IntentRecognizer(),
            RootCauseAnalyzer(),
        ]

        if include_enterprise:
            try:
                from ..templates.enterprise import (
                    AmbiguityResolver,
                    AnalogicalReasoner,
                    CausalReasoner,
                )
                patterns.extend([CausalReasoner(), AmbiguityResolver(), AnalogicalReasoner()])

                from ..templates.enterprise.decision import (
                    ComparativeAnalyzer,
                    DecisionFramework,
                    TradeoffAnalyzer,
                )
                from ..templates.enterprise.problem_solving import ProblemDecomposer

                patterns.extend([
                    ComparativeAnalyzer(),
                    TradeoffAnalyzer(),
                    ProblemDecomposer(),
                    DecisionFramework(),
                ])
            except ImportError:
                pass

        for pattern in patterns:
            registry[pattern.name] = pattern

    def analyze_input(
        self,
        input: str,
        metadata: dict[str, Any] | None = None
    ) -> InputAnalysis:
        """
        Analyze input to determine characteristics and optimal patterns.
        
        Args:
            input: The raw input to analyze
            metadata: Optional metadata (domain, user_level, etc.)
        
        Returns:
            InputAnalysis with recommendations
        """
        metadata = metadata or {}

        input_lower = input.lower()

        # Detect input type
        input_type = self._detect_input_type(input_lower)

        # Assess complexity
        complexity = self._assess_complexity(input, metadata)

        # Detect domain
        domain = metadata.get("domain", self._infer_domain(input_lower))

        # Extract key concepts
        key_concepts = self._extract_concepts(input)

        # Assess requirements
        requires_reasoning = any(word in input_lower for word in [
            "why", "how", "explain", "reason", "cause", "because"
        ])

        requires_comparison = any(word in input_lower for word in [
            "compare", "versus", "vs", "better", "best", "which", "choose"
        ])

        requires_verification = any(word in input_lower for word in [
            "correct", "valid", "verify", "check", "confirm", "true"
        ])

        # Assess ambiguity
        ambiguity_level = self._assess_ambiguity(input)

        # Recommend patterns
        recommended_patterns = self._recommend_patterns(
            input_type,
            complexity,
            requires_reasoning,
            requires_comparison,
            requires_verification,
            ambiguity_level
        )
        # Filter to only patterns we have loaded (excludes enterprise when include_enterprise=False)
        recommended_patterns = [p for p in recommended_patterns if p in self._pattern_registry]

        # Calculate confidence
        confidence = self._calculate_confidence(input, recommended_patterns)

        return InputAnalysis(
            input_type=input_type,
            complexity=complexity,
            domain=domain,
            key_concepts=key_concepts,
            requires_reasoning=requires_reasoning,
            requires_comparison=requires_comparison,
            requires_verification=requires_verification,
            ambiguity_level=ambiguity_level,
            recommended_patterns=recommended_patterns,
            confidence=confidence
        )

    def _detect_input_type(self, input_lower: str) -> InputType:
        """Detect the type of input."""
        if any(phrase in input_lower for phrase in [
            "root cause", "why did", "why is", "why does", "why are", "why was",
            "what caused", "five whys", "fishbone", "led to", "resulted in",
            "cause of", "causes of", "reason for", "spike", "drop", "churn",
            "incident", "outage", "failure", "diagnos",
        ]):
            return InputType.CAUSAL
        elif any(word in input_lower for word in ["should i", "should we", "decide", "choose"]):
            return InputType.DECISION
        elif any(word in input_lower for word in ["compare", "versus", "vs", "better than"]):
            return InputType.COMPARISON
        elif any(word in input_lower for word in ["what is", "explain", "how does", "define"]):
            return InputType.CONCEPT
        elif any(word in input_lower for word in [
            "solve", "fix", "how to", "problem with", "troubleshoot",
            "issue", "bug", "broken", "error",
        ]):
            return InputType.PROBLEM
        elif any(word in input_lower for word in [
            "why", "cause", "causal", "because",
        ]):
            return InputType.CAUSAL
        elif "?" in input_lower:
            return InputType.QUESTION
        else:
            return InputType.STATEMENT

    def _assess_complexity(self, input: str, metadata: dict[str, Any]) -> ComplexityLevel:
        """Assess input complexity."""
        # Simple heuristic
        word_count = len(input.split())
        has_multiple_questions = input.count("?") > 1
        domain_complexity = metadata.get("complexity", "moderate")

        if word_count < 10 and not has_multiple_questions:
            return ComplexityLevel.SIMPLE
        elif word_count < 30 and not has_multiple_questions:
            return ComplexityLevel.MODERATE
        elif word_count < 60:
            return ComplexityLevel.COMPLEX
        else:
            return ComplexityLevel.HIGHLY_COMPLEX

    def _infer_domain(self, input_lower: str) -> str:
        """Infer domain from input content."""
        domain_keywords = {
            "technical": ["code", "software", "program", "api", "database"],
            "financial": ["invest", "money", "cost", "revenue", "profit"],
            "medical": ["health", "medical", "patient", "treatment", "diagnosis"],
            "business": ["business", "market", "customer", "strategy", "company"],
            "scientific": ["research", "experiment", "hypothesis", "theory", "data"],
        }

        for domain, keywords in domain_keywords.items():
            if any(kw in input_lower for kw in keywords):
                return domain

        return "general"

    def _extract_concepts(self, input: str) -> list[str]:
        """Extract key concepts from input."""
        # Simple extraction - could be enhanced
        words = input.split()
        # Return capitalized words and important terms (simplified)
        concepts = [w for w in words if len(w) > 5 and w[0].isupper()]
        return concepts[:5]  # Top 5

    def _assess_ambiguity(self, input: str) -> str:
        """Assess level of ambiguity in input."""
        ambiguity_indicators = ["it", "this", "that", "thing", "stuff", "something"]
        count = sum(1 for word in ambiguity_indicators if word in input.lower())

        if count >= 3:
            return "high"
        elif count >= 1:
            return "medium"
        else:
            return "low"

    def _recommend_patterns(
        self,
        input_type: InputType,
        complexity: ComplexityLevel,
        requires_reasoning: bool,
        requires_comparison: bool,
        requires_verification: bool,
        ambiguity_level: str
    ) -> list[str]:
        """Recommend optimal patterns based on analysis."""
        patterns = []

        # Handle ambiguity first
        if ambiguity_level == "high":
            patterns.append("ambiguity_resolver")

        # Pattern selection based on input type
        if input_type == InputType.CAUSAL:
            patterns.append("root_cause_analyzer")
            patterns.append("causal_reasoner")
            if complexity in [ComplexityLevel.COMPLEX, ComplexityLevel.HIGHLY_COMPLEX]:
                patterns.append("step_by_step_reasoner")

        elif input_type == InputType.QUESTION:
            patterns.append("question_analyzer")
            if requires_reasoning:
                patterns.append("step_by_step_reasoner")

        elif input_type == InputType.PROBLEM:
            if complexity in [ComplexityLevel.COMPLEX, ComplexityLevel.HIGHLY_COMPLEX]:
                patterns.append("problem_decomposer")
            patterns.append("root_cause_analyzer")
            patterns.append("step_by_step_reasoner")

        elif input_type == InputType.DECISION:
            patterns.append("decision_framework")
            patterns.append("risk_assessor")
            if requires_comparison:
                patterns.append("comparative_analyzer")

        elif input_type == InputType.COMPARISON:
            patterns.append("comparative_analyzer")
            patterns.append("tradeoff_analyzer")

        elif input_type == InputType.STATEMENT:
            patterns.append("socratic_questioner")
            patterns.append("intent_recognizer")

        elif input_type == InputType.CONCEPT:
            patterns.append("analogical_reasoner")
            patterns.append("question_analyzer")

        if requires_reasoning and "causal_reasoner" not in patterns:
            patterns.append("causal_reasoner")
        if requires_verification:
            patterns.append("causal_reasoner")

        seen = set()
        deduped = []
        for p in patterns:
            if p not in seen:
                seen.add(p)
                deduped.append(p)
        return deduped[:3]

    def _calculate_confidence(self, input: str, patterns: list[str]) -> float:
        """Calculate confidence in pattern selection."""
        # Simple heuristic
        if len(patterns) == 0:
            return 0.3
        elif len(patterns) == 1:
            return 0.9
        elif len(patterns) <= 3:
            return 0.8
        else:
            return 0.7

    def transform(
        self,
        input: str,
        metadata: dict[str, Any] | None = None,
        patterns: str | list[str] | None = "auto",
    ) -> Context:
        """
        Transform raw input into perfect context.
        
        This is the main API method - automatic, intelligent transformation.
        
        Args:
            input: Raw input to transform
            metadata: Optional metadata (domain, complexity, user_level, etc.)
            patterns: Pattern selection strategy:
                - "auto": Automatic selection (default)
                - ["pattern1", "pattern2"]: Specific patterns
        
        Returns:
            Context object with metadata about transformation
        """
        # Analyze input
        analysis = self.analyze_input(input, metadata)

        # Select patterns
        if patterns == "auto":
            selected_patterns = analysis.recommended_patterns
        elif isinstance(patterns, list):
            selected_patterns = patterns
        else:
            selected_patterns = [analysis.recommended_patterns[0]] if analysis.recommended_patterns else []

        # Apply primary pattern
        if selected_patterns:
            primary_pattern_name = selected_patterns[0]
            pattern = self._pattern_registry.get(primary_pattern_name)

            if pattern:
                # Build context using the pattern
                # Use generic parameters that work across patterns
                context = pattern.build_context(
                    **self._prepare_pattern_inputs(input, analysis, pattern)
                )

                # Add transformation metadata
                context.data = context.data or {}
                context.data["transformation_metadata"] = {
                    "patterns_applied": selected_patterns,
                    "input_analysis": {
                        "type": analysis.input_type.value,
                        "complexity": analysis.complexity.value,
                        "domain": analysis.domain,
                        "ambiguity": analysis.ambiguity_level
                    },
                    "confidence": analysis.confidence,
                }

                return context

        # Fallback: Create basic context
        from ..foundation import Directive, Guidance
        return Context(
            directive=Directive(
                content=input,
                priority=5
            ),
            guidance=Guidance(
                role="Helpful Assistant",
                rules=["Be clear and helpful"]
            )
        )

    def _prepare_pattern_inputs(
        self,
        input: str,
        analysis: InputAnalysis,
        pattern: Pattern
    ) -> dict[str, Any]:
        """Prepare inputs for a specific pattern."""
        # Generic mapping - each pattern has different parameter names
        # This is a simplified version

        inputs = {}

        # Try common parameter names
        if pattern.name in ["question_analyzer", "intent_recognizer"]:
            inputs["question"] = input
        elif pattern.name in ["step_by_step_reasoner", "problem_decomposer", "root_cause_analyzer", "diagnostic_root_cause_analyzer"]:
            inputs["problem"] = input
        elif pattern.name == "decision_framework":
            inputs["decision"] = input
        elif pattern.name == "socratic_questioner":
            inputs["statement"] = input
        elif pattern.name == "analogical_reasoner":
            inputs["concept"] = input
        elif pattern.name in ["comparative_analyzer"]:
            inputs["options"] = input
        elif pattern.name in ["data_analyzer"]:
            inputs["data_description"] = input
            inputs["goal"] = "Analyze the data"
        elif pattern.name in ["stakeholder_mapper"]:
            inputs["situation"] = input
        elif pattern.name in ["scenario_planner"]:
            inputs["situation"] = input
        elif pattern.name in ["risk_assessor"]:
            inputs["decision"] = input
        else:
            inputs["input"] = input

        # Add depth based on complexity — map to each pattern's vocabulary
        if analysis.complexity == ComplexityLevel.SIMPLE:
            engine_depth = "quick"
        elif analysis.complexity == ComplexityLevel.MODERATE:
            engine_depth = "standard"
        else:
            engine_depth = "comprehensive"

        # Per-pattern depth vocabularies (pattern -> light | medium | full)
        _DEPTH_MAP: dict[str, dict[str, str]] = {
            "quick": {
                "question_analyzer": "brief",
                "root_cause_analyzer": "quick",
                "socratic_questioner": "basic",
                "risk_assessor": "basic",
                "intent_recognizer": "quick",
                "decision_framework": "quick",
                "comparative_analyzer": "basic",
                "tradeoff_analyzer": "basic",
                "causal_reasoner": "basic",
                "problem_decomposer": "overview",
                "analogical_reasoner": "quick",
                "ambiguity_resolver": "quick",
            },
            "standard": {
                "question_analyzer": "moderate",
                "root_cause_analyzer": "standard",
                "socratic_questioner": "detailed",
                "risk_assessor": "detailed",
                "intent_recognizer": "standard",
                "decision_framework": "standard",
                "comparative_analyzer": "detailed",
                "tradeoff_analyzer": "detailed",
                "causal_reasoner": "detailed",
                "problem_decomposer": "detailed",
                "analogical_reasoner": "detailed",
                "ambiguity_resolver": "standard",
            },
            "comprehensive": {
                "question_analyzer": "comprehensive",
                "root_cause_analyzer": "thorough",
                "socratic_questioner": "thorough",
                "risk_assessor": "comprehensive",
                "intent_recognizer": "comprehensive",
                "decision_framework": "comprehensive",
                "comparative_analyzer": "comprehensive",
                "tradeoff_analyzer": "comprehensive",
                "causal_reasoner": "thorough",
                "problem_decomposer": "comprehensive",
                "analogical_reasoner": "deep",
                "ambiguity_resolver": "thorough",
            },
        }
        by_pattern = _DEPTH_MAP.get(engine_depth, _DEPTH_MAP["standard"])
        inputs["depth"] = by_pattern.get(
            pattern.name, by_pattern.get("risk_assessor", "detailed")  # fallback
        )

        return inputs

    def get_available_patterns(self) -> list[str]:
        """Get list of all available pattern names."""
        return list(self._pattern_registry.keys())

    def get_pattern(self, name: str) -> Pattern | None:
        """Get a specific pattern by name."""
        return self._pattern_registry.get(name)

    def explain_selection(
        self,
        input: str,
        metadata: dict[str, Any] | None = None
    ) -> str:
        """
        Explain why certain patterns were selected.
        
        Args:
            input: The input to analyze
            metadata: Optional metadata
        
        Returns:
            Human-readable explanation of pattern selection
        """
        analysis = self.analyze_input(input, metadata)

        explanation = f"""Input Analysis for: "{input}"

Input Type: {analysis.input_type.value}
Complexity: {analysis.complexity.value}
Domain: {analysis.domain}
Ambiguity Level: {analysis.ambiguity_level}

Reasoning Requirements:
- Requires reasoning: {analysis.requires_reasoning}
- Requires comparison: {analysis.requires_comparison}
- Requires verification: {analysis.requires_verification}

Recommended Patterns:
"""
        for i, pattern_name in enumerate(analysis.recommended_patterns, 1):
            explanation += f"{i}. {pattern_name}\n"

        explanation += f"\nConfidence in selection: {analysis.confidence:.1%}"

        return explanation


# Convenience function for quick transformation
def transform(
    input: str,
    metadata: dict[str, Any] | None = None,
    patterns: str | list[str] | None = "auto",
    include_enterprise: bool = True
) -> Context:
    """
    Quick transformation function.
    
    Args:
        input: Raw input to transform
        metadata: Optional metadata
        patterns: Pattern selection strategy
        include_enterprise: If False, only free patterns are used
    
    Returns:
        Transformed context
    
    Example:
        >>> from mycontext.intelligence import transform
        >>> context = transform("Should we use microservices?")
        >>> print(context.to_markdown())
    """
    engine = TransformationEngine(include_enterprise=include_enterprise)
    return engine.transform(input, metadata, patterns)
