"""
Intelligence Layer - Automatic cognitive pattern selection and transformation

This layer provides intelligent, automatic context transformation capabilities.
"""

from .transformation_engine import (
    TransformationEngine,
    InputAnalysis,
    InputType,
    ComplexityLevel,
    transform
)
from .quality_metrics import (
    QualityMetrics,
    QualityScore,
    QualityDimension
)
from .pattern_catalog import (
    FULL_PATTERN_CATALOG,
    NAME_TO_CATEGORY,
    VALID_PATTERN_NAMES,
    PATTERN_CATALOG,
    CATALOG_FOR_LLM,
    PATTERN_MAP,
)
from .pattern_suggester import (
    suggest_patterns,
    PatternSuggestion,
    SuggestionResult,
    get_pattern_class,
    assess_complexity,
    smart_execute,
    smart_prompt,
    smart_generic_prompt,
    ComplexityResult,
)
from .prompt_composer import (
    PromptComposer,
    ComposedPrompt,
    get_generic_prompt_for,
)
from .chain_orchestration_agent import (
    build_workflow_chain,
    WorkflowChainResult,
    PATTERN_BUILD_CONTEXT_REGISTRY,
)
from .template_integrator_agent import (
    TemplateIntegratorAgent,
    IntegrationResult,
)
from .output_evaluator import (
    OutputEvaluator,
    OutputQualityScore,
    OutputDimension,
)
from .context_amplification import (
    ContextAmplificationIndex,
    CAIResult,
)
from .template_benchmark import (
    TemplateBenchmark,
    BenchmarkResult,
    CaseResult,
)

__all__ = [
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
]
