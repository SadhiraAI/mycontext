"""
Quality Metrics - Measure and improve context quality

Provides measurable metrics for context engineering quality.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

from ..core import Context


class QualityDimension(Enum):
    """Dimensions of context quality."""
    CLARITY = "clarity"
    COMPLETENESS = "completeness"
    SPECIFICITY = "specificity"
    RELEVANCE = "relevance"
    STRUCTURE = "structure"
    EFFICIENCY = "efficiency"


@dataclass
class QualityScore:
    """Quality score for a context."""
    overall: float  # 0.0 to 1.0
    dimensions: Dict[QualityDimension, float]
    issues: List[str]
    strengths: List[str]
    suggestions: List[str]
    metadata: Dict[str, Any]


class QualityMetrics:
    """
    Measure context quality across multiple dimensions.
    
    Provides:
    - Quantitative quality scores
    - Dimension-specific analysis
    - Improvement recommendations
    - Before/after comparisons
    
    Example:
        >>> from mycontext.intelligence import QualityMetrics
        >>> metrics = QualityMetrics()
        >>> 
        >>> context = Context(guidance="Expert", directive="Analyze")
        >>> score = metrics.evaluate(context)
        >>> 
        >>> print(f"Quality Score: {score.overall:.2%}")
        >>> print(f"Clarity: {score.dimensions[QualityDimension.CLARITY]:.2%}")
        >>> 
        >>> for suggestion in score.suggestions:
        ...     print(f"- {suggestion}")
    """
    
    def __init__(self):
        """Initialize quality metrics system."""
        self.weights = {
            QualityDimension.CLARITY: 0.20,
            QualityDimension.COMPLETENESS: 0.20,
            QualityDimension.SPECIFICITY: 0.15,
            QualityDimension.RELEVANCE: 0.20,
            QualityDimension.STRUCTURE: 0.15,
            QualityDimension.EFFICIENCY: 0.10,
        }
    
    def evaluate(
        self,
        context: Context,
        reference: Optional[str] = None
    ) -> QualityScore:
        """
        Evaluate context quality.
        
        Args:
            context: The context to evaluate
            reference: Optional reference for comparison
        
        Returns:
            QualityScore with detailed metrics
        """
        dimensions = {}
        issues = []
        strengths = []
        suggestions = []
        
        # Evaluate each dimension
        clarity_score, clarity_issues, clarity_strengths = self._evaluate_clarity(context)
        dimensions[QualityDimension.CLARITY] = clarity_score
        issues.extend(clarity_issues)
        strengths.extend(clarity_strengths)
        
        completeness_score, comp_issues, comp_strengths = self._evaluate_completeness(context)
        dimensions[QualityDimension.COMPLETENESS] = completeness_score
        issues.extend(comp_issues)
        strengths.extend(comp_strengths)
        
        specificity_score, spec_issues, spec_strengths = self._evaluate_specificity(context)
        dimensions[QualityDimension.SPECIFICITY] = specificity_score
        issues.extend(spec_issues)
        strengths.extend(spec_strengths)
        
        relevance_score, rel_issues, rel_strengths = self._evaluate_relevance(context)
        dimensions[QualityDimension.RELEVANCE] = relevance_score
        issues.extend(rel_issues)
        strengths.extend(rel_strengths)
        
        structure_score, struct_issues, struct_strengths = self._evaluate_structure(context)
        dimensions[QualityDimension.STRUCTURE] = structure_score
        issues.extend(struct_issues)
        strengths.extend(struct_strengths)
        
        efficiency_score, eff_issues, eff_strengths = self._evaluate_efficiency(context)
        dimensions[QualityDimension.EFFICIENCY] = efficiency_score
        issues.extend(eff_issues)
        strengths.extend(eff_strengths)
        
        # Calculate weighted overall score
        overall = sum(
            score * self.weights[dim]
            for dim, score in dimensions.items()
        )
        
        # Generate suggestions
        suggestions = self._generate_suggestions(dimensions, issues)
        
        return QualityScore(
            overall=overall,
            dimensions=dimensions,
            issues=issues,
            strengths=strengths,
            suggestions=suggestions,
            metadata={
                "assembled_length": len(context.assemble()),
                "has_guidance": context.guidance is not None,
                "has_directive": context.directive is not None,
                "has_knowledge": context.knowledge is not None,
            }
        )
    
    def _evaluate_clarity(self, context: Context) -> tuple[float, List[str], List[str]]:
        """Evaluate clarity dimension."""
        score = 1.0
        issues = []
        strengths = []
        
        assembled = context.assemble()
        
        # Check for vague language
        vague_words = ["thing", "stuff", "something", "somehow", "maybe"]
        vague_count = sum(1 for word in vague_words if word in assembled.lower())
        if vague_count > 3:
            score -= 0.2
            issues.append(f"Contains {vague_count} vague terms")
        elif vague_count == 0:
            strengths.append("No vague language")
        
        # Check for clear structure
        if context.guidance and context.directive:
            strengths.append("Clear role and directive structure")
        else:
            score -= 0.3
            issues.append("Missing guidance or directive")
        
        # Check for ambiguous pronouns
        pronouns = ["it", "this", "that", "these", "those"]
        pronoun_count = sum(1 for p in pronouns if assembled.lower().count(f" {p} ") > 2)
        if pronoun_count > 0:
            score -= 0.1
            issues.append("Excessive ambiguous pronouns")
        
        return max(0.0, score), issues, strengths
    
    def _evaluate_completeness(self, context: Context) -> tuple[float, List[str], List[str]]:
        """Evaluate completeness dimension."""
        score = 0.0
        issues = []
        strengths = []
        
        # Check component presence
        if context.guidance:
            score += 0.3
            strengths.append("Has guidance component")
        else:
            issues.append("Missing guidance component")
        
        if context.directive:
            score += 0.3
            strengths.append("Has directive component")
        else:
            issues.append("Missing directive component")
        
        if context.guidance and context.guidance.rules:
            score += 0.2
            strengths.append("Has behavioral rules")
        else:
            issues.append("No behavioral rules defined")
        
        if context.constraints:
            score += 0.2
            strengths.append("Has constraints defined")
        else:
            issues.append("No constraints defined")
        
        return score, issues, strengths
    
    def _evaluate_specificity(self, context: Context) -> tuple[float, List[str], List[str]]:
        """Evaluate specificity dimension."""
        score = 1.0
        issues = []
        strengths = []
        
        assembled = context.assemble()
        
        # Check for generic language
        generic_phrases = [
            "be helpful", "do your best", "try to", "work on",
            "general", "basic", "simple", "standard"
        ]
        generic_count = sum(1 for phrase in generic_phrases if phrase in assembled.lower())
        
        if generic_count > 3:
            score -= 0.3
            issues.append(f"Contains {generic_count} generic phrases")
        elif generic_count <= 1:
            strengths.append("Highly specific language")
        
        # Check for concrete details
        if context.directive and len(context.directive.content) > 50:
            strengths.append("Detailed directive")
        elif context.directive and len(context.directive.content) < 20:
            score -= 0.2
            issues.append("Directive lacks detail")
        
        # Check for examples or specifics
        has_examples = "example" in assembled.lower() or "specifically" in assembled.lower()
        if has_examples:
            strengths.append("Includes examples or specifics")
        else:
            score -= 0.1
            issues.append("No examples or specific details")
        
        return max(0.0, score), issues, strengths
    
    def _evaluate_relevance(self, context: Context) -> tuple[float, List[str], List[str]]:
        """Evaluate relevance dimension."""
        score = 0.8  # Base score
        issues = []
        strengths = []
        
        # Check for focused scope
        if context.directive:
            directive_words = context.directive.content.split()
            if len(directive_words) < 100:
                strengths.append("Focused, concise directive")
                score += 0.2
            elif len(directive_words) > 300:
                issues.append("Overly verbose directive")
                score -= 0.2
        
        # Check for knowledge integration
        if context.knowledge:
            strengths.append("Includes relevant knowledge")
            score += 0.1
        
        return max(0.0, min(1.0, score)), issues, strengths
    
    def _evaluate_structure(self, context: Context) -> tuple[float, List[str], List[str]]:
        """Evaluate structure dimension."""
        score = 0.0
        issues = []
        strengths = []
        
        assembled = context.assemble()
        
        # Check for logical organization
        has_sections = assembled.count("\n\n") >= 2
        if has_sections:
            score += 0.4
            strengths.append("Well-organized sections")
        else:
            issues.append("Lacks clear section structure")
        
        # Check for hierarchy
        if context.guidance and context.directive:
            score += 0.3
            strengths.append("Clear hierarchical structure")
        
        # Check for formatting
        has_formatting = any(marker in assembled for marker in ["**", "##", "- ", "1."])
        if has_formatting:
            score += 0.3
            strengths.append("Uses formatting for readability")
        else:
            issues.append("No formatting for readability")
        
        return score, issues, strengths
    
    def _evaluate_efficiency(self, context: Context) -> tuple[float, List[str], List[str]]:
        """Evaluate efficiency dimension."""
        score = 1.0
        issues = []
        strengths = []
        
        assembled = context.assemble()
        token_estimate = len(assembled.split())
        
        # Check token efficiency
        if token_estimate < 100:
            strengths.append("Very token-efficient")
        elif token_estimate < 300:
            strengths.append("Good token efficiency")
        elif token_estimate > 1000:
            score -= 0.3
            issues.append(f"High token count (~{token_estimate} tokens)")
        elif token_estimate > 500:
            score -= 0.1
            issues.append("Moderate token usage")
        
        # Check for redundancy
        words = assembled.lower().split()
        unique_ratio = len(set(words)) / len(words) if words else 0
        if unique_ratio < 0.5:
            score -= 0.2
            issues.append("Contains repetitive content")
        elif unique_ratio > 0.7:
            strengths.append("Minimal redundancy")
        
        return max(0.0, score), issues, strengths
    
    def _generate_suggestions(
        self,
        dimensions: Dict[QualityDimension, float],
        issues: List[str]
    ) -> List[str]:
        """Generate improvement suggestions."""
        suggestions = []
        
        # Suggest improvements for low-scoring dimensions
        for dim, score in dimensions.items():
            if score < 0.6:
                if dim == QualityDimension.CLARITY:
                    suggestions.append("Improve clarity: Use precise language and avoid vague terms")
                elif dim == QualityDimension.COMPLETENESS:
                    suggestions.append("Improve completeness: Add missing components (guidance, directive, constraints)")
                elif dim == QualityDimension.SPECIFICITY:
                    suggestions.append("Improve specificity: Replace generic phrases with concrete details")
                elif dim == QualityDimension.RELEVANCE:
                    suggestions.append("Improve relevance: Focus on essential information only")
                elif dim == QualityDimension.STRUCTURE:
                    suggestions.append("Improve structure: Organize content into clear sections")
                elif dim == QualityDimension.EFFICIENCY:
                    suggestions.append("Improve efficiency: Reduce token usage and eliminate redundancy")
        
        # Add issue-specific suggestions
        if not suggestions:
            suggestions.append("Context quality is good! Consider minor refinements based on specific use case.")
        
        return suggestions
    
    def compare(
        self,
        context1: Context,
        context2: Context
    ) -> Dict[str, Any]:
        """
        Compare two contexts and show improvement.
        
        Args:
            context1: Original context
            context2: Improved context
        
        Returns:
            Comparison report
        """
        score1 = self.evaluate(context1)
        score2 = self.evaluate(context2)
        
        improvement = score2.overall - score1.overall
        
        dimension_changes = {
            dim: score2.dimensions[dim] - score1.dimensions[dim]
            for dim in QualityDimension
        }
        
        return {
            "original_score": score1.overall,
            "improved_score": score2.overall,
            "improvement": improvement,
            "improvement_percentage": improvement * 100,
            "dimension_changes": dimension_changes,
            "resolved_issues": set(score1.issues) - set(score2.issues),
            "new_strengths": set(score2.strengths) - set(score1.strengths),
        }
    
    def report(self, score: QualityScore) -> str:
        """
        Generate human-readable quality report.
        
        Args:
            score: QualityScore to report on
        
        Returns:
            Formatted report string
        """
        report = f"""Context Quality Report
=====================

Overall Score: {score.overall:.1%} {'✅' if score.overall >= 0.8 else '⚠️' if score.overall >= 0.6 else '❌'}

Dimension Scores:
"""
        for dim, dim_score in score.dimensions.items():
            emoji = '✅' if dim_score >= 0.8 else '⚠️' if dim_score >= 0.6 else '❌'
            report += f"  {emoji} {dim.value.title()}: {dim_score:.1%}\n"
        
        if score.strengths:
            report += f"\nStrengths ({len(score.strengths)}):\n"
            for strength in score.strengths:
                report += f"  ✓ {strength}\n"
        
        if score.issues:
            report += f"\nIssues ({len(score.issues)}):\n"
            for issue in score.issues:
                report += f"  ✗ {issue}\n"
        
        if score.suggestions:
            report += f"\nSuggestions for Improvement:\n"
            for i, suggestion in enumerate(score.suggestions, 1):
                report += f"  {i}. {suggestion}\n"
        
        report += f"\nMetadata:\n"
        for key, value in score.metadata.items():
            report += f"  {key}: {value}\n"
        
        return report
