"""
Intelligence Layer - Automatic cognitive pattern selection and transformation

This layer provides intelligent, automatic context transformation capabilities.
"""

from .chain_orchestration_agent import (
    PATTERN_BUILD_CONTEXT_REGISTRY,
    WorkflowChainResult,
    build_workflow_chain,
)
from .context_amplification import (
    CAIResult,
    ContextAmplificationIndex,
)
from .context_generator import GeneratedContext, generate_context
from .eval_criteria import (
    ACTIONABILITY as EVAL_ACTIONABILITY,
)
from .eval_criteria import (
    CATALOG as EVAL_CRITERIA_CATALOG,
)
from .eval_criteria import (
    CAUSATION_DISCIPLINE,
    COGNITIVE_SCAFFOLDING_USE,
    DATA_GAP_HONESTY,
    EVIDENCE_CITATION,
    INSTRUCTION_ADHERENCE,
    REASONING_SOUNDNESS,
    STRUCTURE_COMPLIANCE,
    GEvalCriteria,
    get_criteria,
    to_deepeval_metrics,
)
from .guidance_optimizer import (
    GuidanceAuditResult,
    GuidanceOptimizer,
    OptimizedGuidance,
    RuleAudit,
)
from .output_evaluator import (
    OutputDimension,
    OutputEvaluator,
    OutputQualityScore,
)
from .pattern_catalog import (
    CATALOG_FOR_LLM,
    FULL_PATTERN_CATALOG,
    NAME_TO_CATEGORY,
    PATTERN_CATALOG,
    PATTERN_MAP,
    VALID_PATTERN_NAMES,
)
from .pattern_suggester import (
    ComplexityResult,
    PatternSuggestion,
    SuggestionResult,
    assess_complexity,
    get_pattern_class,
    smart_execute,
    smart_generic_prompt,
    smart_prompt,
    suggest_patterns,
)
from .prompt_architect import (
    ArchitectResult,
    ParsedSections,
    PromptArchitect,
    SectionDiff,
)
from .prompt_composer import (
    ComposedPrompt,
    PromptComposer,
    get_generic_prompt_for,
)
from .quality_metrics import QualityDimension, QualityMetrics, QualityScore
from .route_suggester import suggest_routes
from .schemas import AnalysisRoute, RouteAnalysis, RouteStep
from .template_benchmark import (
    BenchmarkResult,
    CaseResult,
    TemplateBenchmark,
)
from .template_integrator_agent import (
    IntegrationResult,
    TemplateIntegratorAgent,
)
from .transformation_engine import (
    ComplexityLevel,
    InputAnalysis,
    InputType,
    TransformationEngine,
    transform,
)

__all__ = [
    "generate_context",
    "GeneratedContext",
    "TransformationEngine",
    "InputAnalysis",
    "InputType",
    "ComplexityLevel",
    "transform",
    "QualityMetrics",
    "QualityScore",
    "QualityDimension",
    "suggest_patterns",
    "PatternSuggestion",
    "SuggestionResult",
    "get_pattern_class",
    "assess_complexity",
    "smart_execute",
    "smart_prompt",
    "smart_generic_prompt",
    "ComplexityResult",
    "build_workflow_chain",
    "WorkflowChainResult",
    "PATTERN_BUILD_CONTEXT_REGISTRY",
    "TemplateIntegratorAgent",
    "IntegrationResult",
    "OutputEvaluator",
    "OutputQualityScore",
    "OutputDimension",
    "ContextAmplificationIndex",
    "CAIResult",
    "TemplateBenchmark",
    "BenchmarkResult",
    "CaseResult",
    "PromptComposer",
    "ComposedPrompt",
    "get_generic_prompt_for",
    "PromptArchitect",
    "ArchitectResult",
    "ParsedSections",
    "SectionDiff",
    "GuidanceOptimizer",
    "OptimizedGuidance",
    "GuidanceAuditResult",
    "RuleAudit",
    # Route suggestion
    "suggest_routes",
    "RouteAnalysis",
    "AnalysisRoute",
    "RouteStep",
    # Eval criteria
    "GEvalCriteria",
    "EVIDENCE_CITATION",
    "CAUSATION_DISCIPLINE",
    "DATA_GAP_HONESTY",
    "INSTRUCTION_ADHERENCE",
    "EVAL_ACTIONABILITY",
    "REASONING_SOUNDNESS",
    "STRUCTURE_COMPLIANCE",
    "COGNITIVE_SCAFFOLDING_USE",
    "EVAL_CRITERIA_CATALOG",
    "get_criteria",
    "to_deepeval_metrics",
]
