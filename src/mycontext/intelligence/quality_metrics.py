"""
Quality Metrics - Measure and improve context quality

Provides measurable metrics for context engineering quality.

Based on research from:
- ResearchRubrics (ICLR 2026): factual grounding, reasoning soundness, clarity
- LMUNIT (ACL 2025): decomposed natural language unit tests
- Standard Quality Criteria for NLP (ACL Findings 2025): standardized assessment
- FLASK benchmark: fine-grained language model evaluation
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


# Minimum word thresholds for meaningful prompts
MIN_WORDS_MEANINGFUL = 30
MIN_WORDS_ADEQUATE = 80
MIN_WORDS_GOOD = 150


class QualityMetrics:
    """
    Measure context quality across multiple dimensions.

    Scoring philosophy (calibrated to research benchmarks):
      0-25%  -- Broken / empty / placeholder
      25-45% -- Minimal / generic (e.g. "Expert Assistant, be helpful")
      45-65% -- Adequate basics but missing depth
      65-80% -- Good: clear role, specific directive, some constraints
      80-95% -- Very good: comprehensive, examples, tight constraints
      95-100% -- Exceptional: publishable quality

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

    def __init__(
        self,
        mode: str = "heuristic",
        llm_provider: str = "openai",
        llm_model: str = "gpt-4o-mini",
    ):
        self.mode = mode
        self.llm_provider = llm_provider
        self.llm_model = llm_model
        self.weights = {
            QualityDimension.CLARITY: 0.20,
            QualityDimension.COMPLETENESS: 0.25,
            QualityDimension.SPECIFICITY: 0.15,
            QualityDimension.RELEVANCE: 0.15,
            QualityDimension.STRUCTURE: 0.15,
            QualityDimension.EFFICIENCY: 0.10,
        }

    def evaluate(
        self,
        context: Context,
        reference: Optional[str] = None
    ) -> QualityScore:
        if self.mode == "llm":
            return self._evaluate_llm(context)
        elif self.mode == "hybrid":
            return self._evaluate_hybrid(context)
        else:
            return self._evaluate_heuristic(context)

    # ── Structural inference ────────────────────────────────────────────

    @staticmethod
    def _infer_structure_from_assembled(text: str) -> dict:
        """Infer guidance/directive/constraints from assembled text."""
        lower = text.lower()
        lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
        word_count = len(text.split())

        has_role_like = any(
            p in lower
            for p in [
                "you are", "you're", "act as", "role:", "## role", "### role",
                "**role**", "guidance:", "## guidance", "system:"
            ]
        )
        has_directive_like = any(
            p in lower
            for p in [
                "analyze", "review", "identify", "instructions:", "## instructions",
                "## task", "**task**", "directive:", "## directive", "goal:",
                "## goal", "evaluate", "summarize", "generate", "create", "write",
                "classify", "compare", "assess", "diagnose", "explain"
            ]
        ) and word_count > 25

        has_constraints = any(
            p in lower
            for p in [
                "do not", "don't", "never", "always", "constraints:", "## constraints",
                "avoid", "must not", "should not", "must be", "limit",
                "must include", "must_include", "format_rules", "format rules"
            ]
        )
        has_rules = any(
            p in lower
            for p in [
                "rules:", "## rules", "guidelines:", "## guidelines",
                "principles:", "steps:", "follow these"
            ]
        ) or sum(1 for ln in lines if ln.startswith(("- ", "* ", "1.", "2.", "3."))) >= 2

        has_examples = any(
            p in lower
            for p in [
                "example:", "for example", "e.g.", "**example**",
                "sample output", "sample response"
            ]
        ) or ("```" in text and any(p in lower for p in ["example", "output", "response"]))

        has_output_format = any(
            p in lower
            for p in [
                "output format", "output_format", "respond with", "respond in",
                "json schema", "expected schema", "format:", "## format"
            ]
        )

        has_goal = False
        if "## goal" in lower or "goal:" in lower or "objective:" in lower:
            for line in text.split("\n"):
                if any(g in line.lower() for g in ["goal", "objective"]) and len(line.strip()) > 15:
                    has_goal = True
                    break
        # A substantive directive with role = goal is implicitly present
        if not has_goal and has_role_like and has_directive_like and word_count > 50:
            has_goal = True

        return {
            "has_role_like": has_role_like,
            "has_directive_like": has_directive_like,
            "has_constraints": has_constraints,
            "has_rules": has_rules,
            "has_examples": has_examples,
            "has_output_format": has_output_format,
            "has_goal": has_goal,
            "word_count": word_count,
        }

    # ── Quality issue detection ─────────────────────────────────────────

    @staticmethod
    def _detect_quality_issues(text: str, context=None) -> tuple:
        """Detect low-quality patterns. Returns (issues, penalty 0-0.7)."""
        import re

        lower = text.lower()
        issues = []
        penalty = 0.0
        word_count = len(text.split())

        # Extremely short content
        if word_count < 10:
            issues.append("Content is too short to be a useful prompt")
            penalty = max(penalty, 0.6)
        elif word_count < MIN_WORDS_MEANINGFUL:
            issues.append(f"Prompt is very short ({word_count} words) -- add more detail")
            penalty = max(penalty, 0.3)

        # Typos / gibberish
        typo_patterns = [
            ("objecive", "objective"), ("objetive", "objective"), ("thte", "the"),
            ("teh", "the"), ("analzy", "analyze"), ("analyise", "analyze"),
            ("folow", "follow"), ("recomend", "recommend"), ("imporant", "important"),
        ]
        typo_count = 0
        for bad, good in typo_patterns:
            if bad in lower and good not in lower:
                typo_count += 1
        if typo_count > 0:
            issues.append(f"Contains {typo_count} likely typo(s)")
            penalty = max(penalty, 0.05 * typo_count)

        if " asas " in lower or " asas" in lower or "asas " in lower:
            issues.append("Contains gibberish or placeholder text")
            penalty = max(penalty, 0.25)

        # Empty JSON schema
        has_empty_schema = bool(re.search(r'```\s*json\s*\{\s*\}\s*```', text, re.DOTALL | re.IGNORECASE))
        has_json_example = bool(re.search(r'\{[^{}]*"[a-z_]+"\s*:', text))
        if has_empty_schema and not has_json_example:
            issues.append("Empty JSON schema -- add fields showing expected output")
            penalty = max(penalty, 0.10)

        # Garbage placeholders
        if "{{" in lower and "}}" in lower:
            placeholders = re.findall(r"\{\{\s*([^}]+)\s*\}\}", text)
            for p in placeholders:
                if len(p) < 3 or "asas" in p.lower() or p.count(" ") > 4:
                    issues.append("Placeholder contains garbage text")
                    penalty = max(penalty, 0.15)
                    break

        # Minimal / generic prompt detection
        core = lower[:200]
        generic_role = any(p in core for p in ["expert assistant", "helpful assistant", "ai assistant"])
        generic_rules = any(p in core for p in ["be clear and helpful", "do your best", "be helpful"])
        minimal_directive = any(
            p in core
            for p in ["analyze the following", "help me with", "do the following"]
        )
        if generic_role and generic_rules:
            issues.append("Generic role and rules -- be specific about expertise and behavior")
            penalty = max(penalty, 0.30)
        if generic_role and minimal_directive and word_count < 60:
            issues.append("Minimal generic prompt -- add specific goal, detailed directive, and constraints")
            penalty = max(penalty, 0.45)

        # Missing essential components (heavy penalty)
        # Skip this check when the Context has structured components -- the
        # completeness evaluator handles those properly.
        has_structured = context and (context.guidance or context.constraints)
        if not has_structured:
            has_goal = "## goal" in lower or "goal:" in lower or (
                # A substantive directive IS the goal
                any(p in lower for p in [
                    "analyze", "review", "identify", "evaluate", "summarize",
                    "classify", "compare", "generate", "create", "write",
                    "assess", "diagnose", "explain", "provide", "determine",
                    "extract", "describe", "recommend", "suggest", "calculate"
                ]) and word_count > 40
            )
            has_guidance = any(
                p in lower
                for p in [
                    "you are", "you're", "act as", "role:", "## role",
                    "guidance:", "**role**", "system:", "follow these rules"
                ]
            )
            has_directive = any(
                p in lower
                for p in [
                    "analyze", "review", "identify", "instructions:", "## instructions",
                    "## task", "**task**", "directive:", "## directive",
                    "evaluate", "summarize", "classify", "compare", "generate",
                    "create", "write", "assess", "diagnose", "explain",
                    "provide", "determine", "extract", "describe"
                ]
            ) and word_count > 20

            missing = []
            if not has_goal:
                missing.append("goal")
            if not has_guidance:
                missing.append("guidance/role")
            if not has_directive:
                missing.append("directive")
            if missing:
                per_missing = 0.15
                issues.append(f"Missing essential components: {', '.join(missing)}")
                penalty = max(penalty, per_missing * len(missing))

        return issues, min(0.70, penalty)

    # ── Heuristic evaluation ────────────────────────────────────────────

    def _evaluate_heuristic(self, context: Context) -> QualityScore:
        """Evaluate using calibrated rule-based heuristics."""
        assembled = context.assemble()
        word_count = len(assembled.split())
        assembled_only = not context.guidance and not context.constraints
        inferred = self._infer_structure_from_assembled(assembled) if assembled_only else None

        quality_issues, quality_penalty = self._detect_quality_issues(assembled, context)

        dimensions = {}
        issues = list(quality_issues)
        strengths = []
        suggestions = []

        clarity_score, c_iss, c_str = self._evaluate_clarity(context, inferred, word_count)
        dimensions[QualityDimension.CLARITY] = clarity_score
        issues.extend(c_iss)
        strengths.extend(c_str)

        comp_score, co_iss, co_str = self._evaluate_completeness(context, inferred, word_count)
        dimensions[QualityDimension.COMPLETENESS] = comp_score
        issues.extend(co_iss)
        strengths.extend(co_str)

        spec_score, sp_iss, sp_str = self._evaluate_specificity(context, inferred, word_count)
        dimensions[QualityDimension.SPECIFICITY] = spec_score
        issues.extend(sp_iss)
        strengths.extend(sp_str)

        rel_score, r_iss, r_str = self._evaluate_relevance(context, inferred, word_count)
        dimensions[QualityDimension.RELEVANCE] = rel_score
        issues.extend(r_iss)
        strengths.extend(r_str)

        struct_score, st_iss, st_str = self._evaluate_structure(context, inferred, word_count)
        dimensions[QualityDimension.STRUCTURE] = struct_score
        issues.extend(st_iss)
        strengths.extend(st_str)

        eff_score, e_iss, e_str = self._evaluate_efficiency(context, inferred, word_count)
        dimensions[QualityDimension.EFFICIENCY] = eff_score
        issues.extend(e_iss)
        strengths.extend(e_str)

        # Weighted overall
        overall = sum(score * self.weights[dim] for dim, score in dimensions.items())

        # Apply quality penalty
        if quality_penalty > 0:
            overall = max(0.0, overall - quality_penalty)

        # Hard caps for very short / empty prompts.
        # Structured contexts (with guidance + directive) are exempt from
        # word-count caps since they encode specifics in structured fields.
        is_structured = bool(context.guidance and context.directive)
        if word_count < 10:
            overall = min(overall, 0.10)
        elif not is_structured:
            if word_count < MIN_WORDS_MEANINGFUL:
                overall = min(overall, 0.35)
            elif word_count < MIN_WORDS_ADEQUATE:
                overall = min(overall, 0.65)

        overall = max(0.0, min(1.0, overall))

        # Suppress misleading strengths for bad prompts
        if quality_penalty >= 0.15 or overall < 0.45:
            strengths = []

        suggestions = self._generate_suggestions(dimensions, issues, overall, word_count)

        return QualityScore(
            overall=overall,
            dimensions=dimensions,
            issues=issues,
            strengths=strengths,
            suggestions=suggestions,
            metadata={
                "mode": "heuristic",
                "assembled_length": len(assembled),
                "word_count": word_count,
                "has_guidance": context.guidance is not None,
                "has_directive": context.directive is not None,
                "has_constraints": context.constraints is not None,
                "has_knowledge": context.knowledge is not None,
            }
        )

    # ── Dimension evaluators ────────────────────────────────────────────

    def _evaluate_clarity(self, context, inferred, word_count):
        """
        Clarity: Is every instruction clear and unambiguous?
        Base: 0.25 -- must earn up to 1.0.
        """
        score = 0.25
        issues = []
        strengths = []
        assembled = context.assemble()
        lower = assembled.lower()

        if word_count < 10:
            return 0.0, ["Too short to evaluate clarity"], []

        # Vague words penalty
        # Only count truly vague usages; words like "something" in instructional
        # context (e.g., "how something works") are fine in structured templates.
        vague_words = ["thing", "stuff", "somehow", "maybe", "probably", "whatever"]
        vague_count = sum(1 for w in vague_words if f" {w} " in f" {lower} ")
        # "something" is only vague in short/unstructured prompts
        something_count = lower.count(" something ")
        is_structured = context.guidance and context.directive
        if not is_structured:
            vague_count += something_count
        if vague_count > 3:
            score -= 0.15
            issues.append(f"Uses {vague_count} vague terms (thing, stuff, maybe, etc.)")
        elif vague_count > 0:
            score -= 0.05
        else:
            score += 0.15
            strengths.append("No vague language")

        # Clear role + directive structure
        has_structure = context.guidance and context.directive
        if inferred and not has_structure:
            has_structure = inferred.get("has_role_like") and inferred.get("has_directive_like")
        if has_structure:
            score += 0.20
            strengths.append("Clear role and directive structure")
        else:
            score -= 0.10
            issues.append("Lacks clear role-directive structure")

        # Defined output format
        has_format = any(
            p in lower
            for p in ["output format", "respond with", "respond in", "json schema",
                       "output_format", "expected schema", "format rules"]
        )
        if has_format:
            score += 0.15
            strengths.append("Output format specified")

        # Ambiguous pronouns
        pronouns = ["it", "this", "that", "these", "those"]
        pronoun_count = sum(1 for p in pronouns if lower.count(f" {p} ") > 3)
        if pronoun_count > 1:
            score -= 0.10
            issues.append("Excessive ambiguous pronouns without clear referents")

        # Consistent terminology (no contradictions)
        if word_count > 50:
            score += 0.10
            strengths.append("Sufficient detail for clear instructions")

        # Bonus for well-defined terms
        if any(p in lower for p in ["defined as", "means", "refers to", "i.e.", "specifically"]):
            score += 0.05

        return max(0.0, min(1.0, score)), issues, strengths

    def _evaluate_completeness(self, context, inferred, word_count):
        """
        Completeness: Are all necessary components present?
        Additive from 0.0 -- each component adds score.
        """
        score = 0.0
        issues = []
        strengths = []

        if word_count < 10:
            return 0.0, ["Too short -- missing all components"], []

        # Guidance / Role (+0.20)
        has_guidance = bool(context.guidance)
        if inferred and not has_guidance:
            has_guidance = inferred.get("has_role_like", False)
        if has_guidance:
            # Check if role is specific (not generic)
            assembled_lower = context.assemble().lower()
            generic_roles = ["expert assistant", "helpful assistant", "ai assistant", "assistant"]
            role_text = ""
            if context.guidance and hasattr(context.guidance, 'role'):
                role_text = (context.guidance.role or "").lower()
            is_generic = any(role_text.strip() == g for g in generic_roles)
            if is_generic:
                score += 0.10
                issues.append("Role is too generic -- specify domain expertise")
            else:
                score += 0.20
                strengths.append("Specific role/guidance defined")
        else:
            issues.append("Missing guidance/role component")

        # Directive (+0.20)
        has_directive = bool(context.directive)
        if inferred and not has_directive:
            has_directive = inferred.get("has_directive_like", False)
        if has_directive:
            dir_content = (context.directive.content if context.directive else "") or ""
            dir_words = len(dir_content.split())
            if dir_words > 15:
                score += 0.20
                strengths.append("Substantive directive")
            else:
                score += 0.10
                issues.append("Directive is too brief -- add more detail")
        else:
            issues.append("Missing directive component")

        # Goal (+0.15)
        # When a structured context has guidance + substantive directive, the
        # directive serves as the task goal. Only penalize if truly absent.
        has_goal = False
        if context.guidance and hasattr(context.guidance, 'goal') and context.guidance.goal:
            has_goal = len(str(context.guidance.goal).strip()) > 10
        if not has_goal and context.directive and context.directive.content:
            # A substantive directive (>20 words) with a role = goal is defined
            dir_words = len(context.directive.content.split())
            if dir_words > 20 and has_guidance:
                has_goal = True
        if inferred and not has_goal:
            has_goal = inferred.get("has_goal", False)
        if has_goal:
            score += 0.15
            strengths.append("Clear goal/task defined")
        else:
            issues.append("No explicit goal -- add a clear objective")

        # Rules (+0.15)
        has_rules = context.guidance and context.guidance.rules if context.guidance else False
        if inferred and not has_rules:
            has_rules = inferred.get("has_rules", False)
        if has_rules:
            rule_count = len(context.guidance.rules) if context.guidance and context.guidance.rules else 0
            if rule_count >= 3:
                score += 0.15
                strengths.append(f"Well-defined rules ({rule_count})")
            elif rule_count >= 1:
                score += 0.10
                strengths.append("Has behavioral rules")
            else:
                score += 0.08
        else:
            issues.append("No behavioral rules defined")

        # Constraints (+0.15)
        has_constraints = bool(context.constraints)
        if inferred and not has_constraints:
            has_constraints = inferred.get("has_constraints", False)
        if has_constraints:
            score += 0.15
            strengths.append("Constraints defined")
        else:
            issues.append("No constraints -- add must_include, must_not_include, or format_rules")

        # Examples (+0.15)
        has_examples = False
        assembled = context.assemble()
        if inferred:
            has_examples = inferred.get("has_examples", False)
        else:
            lower = assembled.lower()
            has_examples = any(
                p in lower
                for p in ["example:", "for example", "e.g.", "**example**", "sample output"]
            )
        if has_examples:
            score += 0.15
            strengths.append("Includes examples")
        else:
            issues.append("No examples -- add concrete examples of expected input/output")

        return min(1.0, score), issues, strengths

    def _evaluate_specificity(self, context, inferred, word_count):
        """
        Specificity: Are instructions concrete and detailed?
        Base: 0.15 -- must earn up to 1.0.
        """
        score = 0.15
        issues = []
        strengths = []
        assembled = context.assemble()
        lower = assembled.lower()

        if word_count < 10:
            return 0.0, ["Too short to be specific"], []

        # Generic language penalty
        generic_phrases = [
            "be helpful", "do your best", "try to", "work on",
            "general", "basic", "simple approach", "standard"
        ]
        generic_count = sum(1 for p in generic_phrases if p in lower)
        if generic_count > 2:
            score -= 0.10
            issues.append(f"Contains {generic_count} generic phrases -- be more specific")
        elif generic_count == 0:
            score += 0.15
            strengths.append("Uses specific, concrete language")

        # Domain-specific terminology
        domain_indicators = [
            "algorithm", "methodology", "framework", "criteria", "metric",
            "protocol", "taxonomy", "schema", "pipeline", "workflow",
            "stakeholder", "baseline", "benchmark", "hypothesis"
        ]
        domain_count = sum(1 for t in domain_indicators if t in lower)
        if domain_count >= 3:
            score += 0.15
            strengths.append("Rich domain-specific terminology")
        elif domain_count >= 1:
            score += 0.08

        # Directive detail
        dir_content = (context.directive.content if context.directive else "") or assembled
        dir_words = len(dir_content.split())
        if dir_words > 80:
            score += 0.15
            strengths.append("Detailed, comprehensive directive")
        elif dir_words > 30:
            score += 0.10
            strengths.append("Adequate directive detail")
        elif dir_words < 15:
            score -= 0.10
            issues.append("Directive is too brief -- add specifics")

        # Concrete examples or specifics
        has_real_examples = (
            "example:" in lower
            or "for example" in lower
            or "e.g." in lower
            or "such as" in lower
            or ("```" in assembled and any(p in lower for p in ["example", "output", "response"]))
        )
        if has_real_examples:
            score += 0.20
            strengths.append("Includes concrete examples")
        else:
            score -= 0.05
            issues.append("No examples or concrete specifics")

        # Structured specifics (constraints, rules, format specs add to specificity)
        if context.constraints:
            constraint_items = 0
            if context.constraints.must_include:
                constraint_items += len(context.constraints.must_include)
            if context.constraints.must_not_include:
                constraint_items += len(context.constraints.must_not_include)
            if context.constraints.format_rules:
                constraint_items += len(context.constraints.format_rules)
            if constraint_items >= 3:
                score += 0.15
                strengths.append("Well-defined constraints add specificity")
            elif constraint_items >= 1:
                score += 0.08
        elif inferred and inferred.get("has_constraints"):
            score += 0.08

        if context.guidance and context.guidance.rules and len(context.guidance.rules) >= 3:
            score += 0.10
            strengths.append("Behavioral rules add specificity")
        elif inferred and inferred.get("has_rules"):
            score += 0.05

        # Measurable criteria
        measurable = any(
            p in lower
            for p in ["confidence", "score", "rating", "percentage", "0.0", "1.0",
                       "scale of", "1 to ", "0 to ", "between"]
        )
        if measurable:
            score += 0.10
            strengths.append("Includes measurable criteria")

        return max(0.0, min(1.0, score)), issues, strengths

    def _evaluate_relevance(self, context, inferred, word_count):
        """
        Relevance: Is everything focused on the task?
        Base: 0.20 -- must earn up to 1.0.
        """
        score = 0.20
        issues = []
        strengths = []

        if word_count < 10:
            return 0.0, ["Too short to assess relevance"], []

        # Directive focus
        dir_content = (context.directive.content if context.directive else "") or ""
        dir_words = len(dir_content.split())
        # Long directives with structure (headings, numbered lists) are
        # intentionally detailed, not verbose.
        has_internal_structure = (
            "**" in dir_content or "##" in dir_content or
            any(dir_content.strip().find(f"\n{i}.") >= 0 for i in range(1, 10))
        )
        if 15 < dir_words < 150:
            score += 0.25
            strengths.append("Focused, well-scoped directive")
        elif dir_words >= 150 and dir_words < 300:
            score += 0.20
            if has_internal_structure:
                strengths.append("Detailed directive with clear structure")
        elif dir_words >= 300:
            if has_internal_structure:
                score += 0.20
                strengths.append("Comprehensive directive with organized sections")
            else:
                score += 0.10
                issues.append("Directive may be overly verbose")
        elif dir_words <= 15 and dir_words > 0:
            score += 0.10
            issues.append("Directive is too brief for adequate focus")
        else:
            issues.append("No directive content")

        # Knowledge integration
        if context.knowledge:
            score += 0.15
            strengths.append("Includes relevant knowledge/context")

        # Constraints help focus
        if context.constraints:
            score += 0.15
            strengths.append("Constraints help maintain focus")
        elif inferred and inferred.get("has_constraints"):
            score += 0.10

        # Topic coherence (role aligns with directive)
        if context.guidance and context.directive:
            score += 0.15
            strengths.append("Role-directive alignment")
        elif inferred and inferred.get("has_role_like") and inferred.get("has_directive_like"):
            score += 0.10

        return max(0.0, min(1.0, score)), issues, strengths

    def _evaluate_structure(self, context, inferred, word_count):
        """
        Structure: Well-organized content with clear hierarchy?
        Additive from 0.0.
        """
        score = 0.0
        issues = []
        strengths = []
        assembled = context.assemble()

        if word_count < 10:
            return 0.0, ["Too short to have meaningful structure"], []

        # Section separation
        section_breaks = assembled.count("\n\n")
        if section_breaks >= 4:
            score += 0.25
            strengths.append("Well-organized with clear sections")
        elif section_breaks >= 2:
            score += 0.15
            strengths.append("Has section separation")
        else:
            issues.append("Lacks clear section breaks")

        # Formatting markers
        has_headers = "##" in assembled or "**" in assembled
        has_lists = any(m in assembled for m in ["- ", "* ", "1. ", "2. "])
        if has_headers and has_lists:
            score += 0.30
            strengths.append("Good formatting with headers and lists")
        elif has_headers or has_lists:
            score += 0.15
            strengths.append("Uses some formatting")
        else:
            score -= 0.05
            issues.append("No formatting aids (headers, lists, bold)")

        # Hierarchical organization (guidance → directive → constraints)
        has_hierarchy = context.guidance and context.directive
        if inferred and not has_hierarchy:
            has_hierarchy = inferred.get("has_role_like") and inferred.get("has_directive_like")
        if has_hierarchy:
            score += 0.25
            strengths.append("Clear guidance-directive hierarchy")

        # Constraints add structural completeness
        has_constraints_section = bool(context.constraints) or (inferred and inferred.get("has_constraints"))
        if has_constraints_section:
            score += 0.20
            strengths.append("Includes constraints section")

        return max(0.0, min(1.0, score)), issues, strengths

    def _evaluate_efficiency(self, context, inferred, word_count):
        """
        Efficiency: Concise without being incomplete?
        Base: 0.50 -- penalize both extremes.
        """
        score = 0.50
        issues = []
        strengths = []
        assembled = context.assemble()

        if word_count < 10:
            score = 0.10
            issues.append("Too short -- brevity without content is not efficiency")
            return score, issues, strengths

        is_structured = bool(context.guidance and context.directive)
        if word_count < MIN_WORDS_MEANINGFUL:
            score = 0.20
            issues.append(f"Only {word_count} words -- too brief to be complete")
        elif word_count < MIN_WORDS_ADEQUATE:
            if is_structured:
                score += 0.25
            else:
                score += 0.15
        elif word_count < 300:
            score += 0.30
            strengths.append("Good balance of detail and conciseness")
        elif word_count < 500:
            score += 0.25
            strengths.append("Adequate length")
        elif word_count > 1000:
            score -= 0.15
            issues.append(f"Very long ({word_count} words) -- consider trimming redundancy")
        else:
            score += 0.15

        # Redundancy check
        words = assembled.lower().split()
        unique_ratio = len(set(words)) / len(words) if words else 0
        if unique_ratio < 0.40:
            score -= 0.15
            issues.append("High redundancy detected")
        elif unique_ratio < 0.55:
            score -= 0.05
            issues.append("Some repetitive content")
        elif unique_ratio > 0.70:
            score += 0.15
            strengths.append("Minimal redundancy")
        else:
            score += 0.05

        return max(0.0, min(1.0, score)), issues, strengths

    # ── Suggestion generation ───────────────────────────────────────────

    def _generate_suggestions(self, dimensions, issues, overall, word_count):
        """Generate specific, actionable improvement suggestions."""
        suggestions = []
        issues_text = " ".join(issues).lower()

        # Critical issues
        if "missing essential" in issues_text or "missing guidance" in issues_text:
            suggestions.append("Add the missing components: a specific Role, a clear Goal, a detailed Directive, and Constraints")

        if "minimal generic prompt" in issues_text or "generic role and rules" in issues_text:
            suggestions.append("Replace generic role with domain expertise (e.g. 'Senior data analyst' instead of 'Expert Assistant')")

        if "too short" in issues_text or "too brief" in issues_text:
            suggestions.append("Expand the prompt with more specific instructions, examples, and constraints")

        if "empty json schema" in issues_text:
            suggestions.append("Replace the empty JSON schema with concrete field names and types")

        if "gibberish" in issues_text or "garbage" in issues_text:
            suggestions.append("Remove placeholder and test text before scoring")

        # Dimension-specific suggestions
        if not suggestions:
            for dim, score in dimensions.items():
                if score < 0.50:
                    if dim == QualityDimension.CLARITY:
                        suggestions.append("Improve clarity: use precise terms, define ambiguous concepts, remove vague language")
                    elif dim == QualityDimension.COMPLETENESS:
                        suggestions.append("Add missing components: Goal, Role, Rules, Constraints, and Examples")
                    elif dim == QualityDimension.SPECIFICITY:
                        suggestions.append("Add concrete examples and domain-specific details instead of generic instructions")
                    elif dim == QualityDimension.RELEVANCE:
                        suggestions.append("Focus the directive on the core task and add constraints to scope the output")
                    elif dim == QualityDimension.STRUCTURE:
                        suggestions.append("Organize with clear sections: Role, Goal, Directive, Constraints")
                    elif dim == QualityDimension.EFFICIENCY:
                        suggestions.append("Balance detail and conciseness -- ensure all content serves a purpose")

        if not suggestions and overall >= 0.80:
            suggestions.append("Strong prompt. Consider adding edge cases or constraints for even better results.")
        elif not suggestions and overall >= 0.65:
            suggestions.append("Good foundation. Add examples and tighter constraints to reach excellence.")
        elif not suggestions:
            suggestions.append("Review each dimension and address the issues listed above.")

        return suggestions

    # ── Compare & Report ────────────────────────────────────────────────

    def compare(self, context1: Context, context2: Context) -> Dict[str, Any]:
        """Compare two contexts and show improvement."""
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
        """Generate human-readable quality report."""
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

    # ── LLM evaluation ──────────────────────────────────────────────────

    def _evaluate_llm(self, context: Context) -> QualityScore:
        """Evaluate using LLM (accurate but slow, ~$0.02/eval)."""
        import json
        import os

        assembled = context.assemble()

        if self.llm_provider == "openai" and not os.environ.get("OPENAI_API_KEY"):
            return self._evaluate_heuristic(context)

        prompt = f"""You are an expert context quality evaluator for LLM prompts. Rate this context on 6 dimensions (0.0-1.0 scale).

Be STRICT. Most prompts should score 0.4-0.7. Only truly excellent prompts score above 0.85.

Calibration guide:
- 0.0-0.2: Missing or broken
- 0.2-0.4: Minimal, generic
- 0.4-0.6: Adequate but improvable
- 0.6-0.8: Good, well-structured
- 0.8-1.0: Excellent, comprehensive

<context>
{assembled}
</context>

Rate each dimension:

1. **CLARITY** (0.0-1.0): Clear, unambiguous instructions? Well-defined terms? Penalize vague words.
2. **COMPLETENESS** (0.0-1.0): All components present (role, goal, directive, rules, constraints, examples)?
3. **SPECIFICITY** (0.0-1.0): Concrete, detailed instructions with examples? Not generic?
4. **RELEVANCE** (0.0-1.0): Focused on the task? No unnecessary information?
5. **STRUCTURE** (0.0-1.0): Well-organized sections? Easy to follow? Good formatting?
6. **EFFICIENCY** (0.0-1.0): Concise but complete? No redundancy?

Output ONLY valid JSON:
{{"clarity": 0.0, "completeness": 0.0, "specificity": 0.0, "relevance": 0.0, "structure": 0.0, "efficiency": 0.0, "overall_issues": ["..."], "overall_strengths": ["..."], "improvement_suggestions": ["..."]}}"""

        try:
            evaluator_context = Context(
                guidance="You are a strict, honest context quality evaluator. Be critical but fair. Output ONLY valid JSON.",
                directive=prompt
            )
            response = evaluator_context.execute(
                provider=self.llm_provider,
                model=self.llm_model,
                temperature=0.3,
            )
            response_text = response.response.strip()
            if response_text.startswith("```"):
                lines = response_text.split("\n")
                response_text = "\n".join(lines[1:-1]) if len(lines) > 2 else response_text
                response_text = response_text.replace("```json", "").replace("```", "").strip()

            scores_json = json.loads(response_text)
            dimensions = {
                QualityDimension.CLARITY: scores_json["clarity"],
                QualityDimension.COMPLETENESS: scores_json["completeness"],
                QualityDimension.SPECIFICITY: scores_json["specificity"],
                QualityDimension.RELEVANCE: scores_json["relevance"],
                QualityDimension.STRUCTURE: scores_json["structure"],
                QualityDimension.EFFICIENCY: scores_json["efficiency"],
            }
            overall = sum(
                score * self.weights[dim]
                for dim, score in dimensions.items()
            )
            return QualityScore(
                overall=overall,
                dimensions=dimensions,
                issues=scores_json.get("overall_issues", []),
                strengths=scores_json.get("overall_strengths", []),
                suggestions=scores_json.get("improvement_suggestions", []),
                metadata={"mode": "llm", "model": self.llm_model, "provider": self.llm_provider}
            )
        except Exception as e:
            result = self._evaluate_heuristic(context)
            result.metadata["llm_error"] = str(e)
            result.metadata["mode"] = "heuristic_fallback"
            return result

    def _evaluate_hybrid(self, context: Context) -> QualityScore:
        """Hybrid: heuristic first, LLM for borderline 0.45-0.75."""
        heuristic_score = self._evaluate_heuristic(context)
        if heuristic_score.overall > 0.75:
            heuristic_score.metadata["mode"] = "hybrid_fast_good"
            return heuristic_score
        elif heuristic_score.overall < 0.45:
            heuristic_score.metadata["mode"] = "hybrid_fast_bad"
            return heuristic_score
        llm_score = self._evaluate_llm(context)
        llm_score.metadata["mode"] = "hybrid_llm_borderline"
        llm_score.metadata["heuristic_score"] = heuristic_score.overall
        return llm_score
