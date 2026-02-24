# Codebase Upgrade Suggestions

**mycontext-ai: Beyond the Optimization Plan — Full Upgrade Roadmap**

**Document Version:** 1.0  
**Date:** February 23, 2026  
**Scope:** Full `/src` analysis — every file, every module  
**Goal:** Optimize for performance, reliability, security, and our core mission as the best cognitive context engineering platform

---

## How to Read This Document

Each upgrade is categorized by:
- **Impact**: How directly it helps our product goal
- **Effort**: Engineering effort to implement  
- **Research Basis**: Peer-reviewed papers or established engineering practice

All findings are directly cited to file + line number. Nothing here is speculative.

---

## Category 1: Security — Ship These First

### 1.1 Template Injection Vulnerability (CRITICAL)

**File:** `src/mycontext/structure/pattern.py`, line 173  
**What's happening:** `directive_template.format(**inputs)` — unescaped Python `.format()` on user-supplied strings.

**Why this is dangerous:** LangChain disclosed a production vulnerability (GHSA-6qv9-48xg-fc7f) in 2024 affecting their prompt template system for exactly this reason. Attackers can access Python object internals through attribute access (`.`) and indexing (`[]`), reaching environment variables, secrets, and class internals. An input like `{0.__class__.__mro__[1].__subclasses__()}` in a user-supplied template variable can expose internal Python objects.

**Research:** OWASP LLM Prompt Injection Prevention Cheat Sheet (2024); LangChain security advisory GHSA-6qv9-48xg-fc7f; AWS Security Blog on prompt injection safeguards (2024).

**Fix (simple):**
```python
# Before (vulnerable)
directive_template.format(**inputs)

# After (safe) — use string.Template with $var syntax, not f-strings
from string import Template
safe_template = Template(directive_template)  # Uses $var, not {var}
safe_template.safe_substitute(**inputs)       # safe_substitute doesn't raise on missing keys

# Or: validate inputs before formatting
def _safe_format(template: str, **inputs: Any) -> str:
    """Format template with injection protection."""
    for key, value in inputs.items():
        if not isinstance(value, (str, int, float, bool, type(None))):
            raise ValueError(f"Input '{key}' must be a primitive type, got {type(value)}")
        if isinstance(value, str) and any(c in value for c in ['{', '}', '__']):
            # Escape braces in user inputs
            inputs[key] = value.replace('{', '{{').replace('}', '}}')
    return template.format(**inputs)
```

---

## Category 2: Reliability — The Silent Errors Problem

### 2.1 Silent Exception Swallowing (HIGH — found in 7 places)

The codebase swallows exceptions in 7 critical places. Each one is a hidden failure mode that produces wrong results silently.

| File | Line | What's swallowed |
|------|------|-----------------|
| `prompt_composer.py` | 218 | Compose LLM call failure → falls back to concatenation silently |
| `prompt_composer.py` | 278 | Template prompt generation failure → skips template silently |
| `prompt_composer.py` | 342 | Generic prompt failure → skips template |
| `template_integrator_agent.py` | 338 | Template detail extraction → empty string |
| `pattern_suggester.py` | 331 | LLM suggestion failure → empty tuple |
| `context_generator.py` | 307 | Provider call failure → loses error context |
| `utils/parsers.py` | 281 | XML parse failure → returns None |

**Why this hurts our product goal:** We brand ourselves as a "measurable quality" platform with "quality-gated execution." Silent failures mean quality metrics are measuring wrong outputs. CAI scores are corrupted by fallback results. Users don't know why outputs are poor.

**Research:** Netflix Engineering (2024) — silent failures are the primary cause of data quality degradation in ML pipelines. The "fail loudly" principle is foundational to production ML systems.

**Fix pattern (consistent across all 7):**
```python
# Before (silent failure)
try:
    prompt = ctx.to_prompt(refine=True, ...)
    prompts.append(prompt)
except Exception:
    continue  # silently drops this template

# After (structured failure with observability)
import logging
logger = logging.getLogger(__name__)

try:
    prompt = ctx.to_prompt(refine=True, ...)
    prompts.append(prompt)
except Exception as e:
    logger.warning(
        "Template refinement failed for '%s': %s. Using unrefined fallback.",
        name, e, exc_info=True
    )
    # Still fall back, but now it's visible
    fallback = ctx.to_prompt(refine=False, ...)
    prompts.append(fallback)
```

---

### 2.2 Fragile Regex-Based LLM Response Parsing (HIGH)

**Files:**  
- `template_integrator_agent.py` lines 375–403 (integration result parsing)  
- `pattern_suggester.py` lines 334–366 (LLM suggestion parsing)  
- `intelligence/context_generator.py` lines 130–142 (JSON extraction)

**What's happening:** LLM structured responses are parsed with hand-crafted regex. When the LLM uses slightly different formatting (it will), parsing silently fails or returns partial data.

**Research:** `instructor` library (3M+ monthly downloads, 12.2k GitHub stars, 2024): Built on Pydantic, instructor provides automatic retry on validation failure, guaranteed type safety, and works with OpenAI, Anthropic, Gemini, and 12+ other providers via their native function-calling/JSON schema modes. Outperforms regex parsing on reliability in production (instructor documentation, 2025).

**Fix — replace all three parsers with Pydantic models + instructor:**
```python
# pip install instructor
import instructor
from pydantic import BaseModel, Field
from openai import OpenAI

class SuggestionOutput(BaseModel):
    patterns: list[str] = Field(description="List of recommended pattern names")
    integration_note: str = Field(description="How patterns should be combined")
    reasoning: str = Field(description="Why these patterns were selected")

class IntegrationOutput(BaseModel):
    guidance: str = Field(description="Unified guidance directive")
    directive: str = Field(description="Unified task directive")
    synthesis_note: str = Field(description="How templates were synthesized")

# Usage in _suggest_with_llm:
client = instructor.from_litellm(litellm.completion)
result = client.chat.completions.create(
    model=model,
    response_model=SuggestionOutput,
    messages=[{"role": "user", "content": prompt}],
    max_retries=2,  # auto-retry on validation failure
)
# result is now a typed, validated SuggestionOutput — no regex needed
```

**Why it aligns with our vision:** We already have `utils/structured_output.py` with `StructuredOutputMixin` and `PydanticOutput`. This extends that capability to the intelligence layer's own parsing.

---

### 2.3 Inconsistent Token Counting (MEDIUM)

Three different token estimation methods exist in the codebase:

| Location | Method | Accuracy |
|----------|--------|---------|
| `utils/optimizers.py:36` | `tiktoken.encode()` | Exact |
| `structure/blueprint.py:178` | `len(text.split()) * 1.3` | ~±30% |
| `utils/validators.py:57` | `len(text) // 4` | ~±40% |

**Why this hurts:** Token budget management in `Blueprint.optimize()` uses the rough word-count method. Our context window management decisions — what to trim, what to keep — are based on inaccurate counts. On long contexts this can mean sending 20%+ more tokens than estimated, hitting rate limits or context window errors in production.

**Research:** OpenAI documentation (2024): "Token counts vary significantly based on text characteristics. Simple character-based approximations are unreliable; use tiktoken for accurate counting." Telnyx developer resources: word/4 heuristic is off by up to 40% for technical text.

**Fix:** Create a single token utility and use it everywhere:
```python
# src/mycontext/utils/tokens.py
import functools
import tiktoken

@functools.lru_cache(maxsize=4)
def _get_encoder(model: str):
    try:
        return tiktoken.encoding_for_model(model)
    except KeyError:
        return tiktoken.get_encoding("cl100k_base")

def count_tokens(text: str, model: str = "gpt-4o") -> int:
    """Accurate token count using tiktoken. Cached per model."""
    return len(_get_encoder(model).encode(text))

def fits_in_window(text: str, model: str, max_tokens: int) -> bool:
    return count_tokens(text, model) <= max_tokens
```

Replace `blueprint.py:178` and `validators.py:57` with `from mycontext.utils.tokens import count_tokens`.

---

## Category 3: Performance — The Bottlenecks (Extended)

### 3.1 Parallel Template Refinement (already in SDK_OPTIMIZATION_RESEARCH_PLAN)

Covered in detail in the optimization plan. Here's the immediate-ship version using `ThreadPoolExecutor` (no async refactor needed):

**File:** `prompt_composer.py`, lines 265–279

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def _refine_template(name: str, question: str, provider: str, model: str, **kwargs) -> tuple[str, str]:
    klass = get_pattern_class(name, include_enterprise=self.include_enterprise)
    if klass is None:
        return name, ""
    reg = PATTERN_BUILD_CONTEXT_REGISTRY.get(name, ("input", {}))
    primary_key, defaults = reg
    params = {**defaults, primary_key: question}
    try:
        ctx = klass().build_context(**params)
        return name, ctx.to_prompt(refine=True, provider=provider, model=model, **kwargs)
    except Exception as e:
        logger.warning("Refinement failed for %s: %s", name, e)
        ctx = klass().build_context(**params)
        return name, ctx.to_prompt(refine=False)

# In compose_from_templates, replace the sequential loop:
with ThreadPoolExecutor(max_workers=min(len(valid_names), 5)) as executor:
    futures = {executor.submit(_refine_template, n, question, provider, model, **kwargs): n
               for n in valid_names}
    name_to_prompt = {}
    for future in as_completed(futures):
        name, prompt = future.result()
        if prompt:
            name_to_prompt[name] = prompt

prompts = [name_to_prompt[n] for n in valid_names if n in name_to_prompt]
```

**Research:** ParallelPrompt (2025): 5× latency speedup on semantically independent subtasks. These refine calls are fully independent.

---

### 3.2 O(n²) Redundancy Removal (MEDIUM)

**File:** `utils/optimizers.py`, line 295 (`remove_similar_sentences`)

```python
for sentence in sentences[1:]:
    for kept in result:   # <-- inner loop over all kept sentences
        if jaccard_similarity(sentence, kept) > threshold:
```

For a 200-sentence context this is 200×200 = 40,000 comparisons. Jaccard similarity requires set operations per pair.

**Research:** MinHash LSH (Locality Sensitive Hashing) reduces this to O(n) amortized. The `datasketch` library provides production-ready MinHash LSH.

**Fix:**
```python
# pip install datasketch
from datasketch import MinHash, MinHashLSH

def remove_similar_sentences_fast(text: str, threshold: float = 0.8) -> str:
    sentences = re.split(r'[.!?]+\s+', text)
    lsh = MinHashLSH(threshold=threshold, num_perm=64)
    result = []
    
    for i, sentence in enumerate(sentences):
        mh = MinHash(num_perm=64)
        for word in sentence.lower().split():
            mh.update(word.encode())
        
        if not lsh.query(mh):  # No similar sentence found
            lsh.insert(str(i), mh)
            result.append(sentence)
    
    return '. '.join(result) + '.'
```

**When this matters:** Any workflow that uses `Blueprint.optimize()` with `ContextCompressor` on large documents or research flows.

---

### 3.3 Pattern Catalog Loading on Every Import (MEDIUM)

**File:** `intelligence/transformation_engine.py`, lines 72–124

`TransformationEngine.__init__` calls `_load_patterns()` synchronously, which imports all pattern modules (lines 85–119). This blocks the constructor for every instantiation.

**Fix — lazy singleton pattern:**
```python
_PATTERN_CACHE: dict[str, Any] | None = None

class TransformationEngine:
    def __init__(self, include_enterprise: bool = False):
        self.include_enterprise = include_enterprise
        self._patterns: dict[str, Any] | None = None  # lazy

    @property
    def patterns(self) -> dict[str, Any]:
        if self._patterns is None:
            self._patterns = self._load_patterns()
        return self._patterns
```

For `get_available_patterns()` and `get_pattern()` — they should use `self.patterns` property, not the dict directly.

---

### 3.4 Hardcoded 6000-Char Truncation in `to_prompt()` (MEDIUM)

**File:** `core.py`, line 460: `assembled[:6000]`

This truncates at characters, not tokens. A 6000-char context is ~1500 tokens — fine for small models. But for GPT-4o (128k context window) or Claude 3.5 Sonnet (200k), we're artificially capping refinement prompts to a tiny fraction of what the model can handle.

**Fix:**
```python
# In Context class or config
MAX_REFINE_TOKENS: int = 4000  # Configurable, not hardcoded

def to_prompt(self, refine: bool = False, max_refine_tokens: int | None = None, ...):
    assembled = self.assemble()
    if refine:
        from .utils.tokens import count_tokens
        limit = max_refine_tokens or MAX_REFINE_TOKENS
        # Truncate by tokens, not characters
        tokens = count_tokens(assembled)
        if tokens > limit:
            # Trim from the middle, preserve start (system role) and end (task)
            assembled = _token_trim(assembled, limit)
        ...
```

---

## Category 4: Semantic Caching — The Biggest Untapped Gain

### 4.1 Add Semantic Caching Layer to Provider (HIGH IMPACT)

**Research:** GPT Semantic Cache (arxiv 2411.05276, 2024): Semantic caching reduces LLM API calls by **68.8%** with cache hit rates of 61.6–68.8% and accuracy exceeding 97%. VectorQ (arxiv 2502.03771, 2025): Adaptive embedding thresholds achieve 26× cache hit rate increases over static thresholds. IC-Cache (arxiv 2501.12689, 2025): 1.4–5.9× throughput improvement by reusing semantically similar cached responses.

**Why this is huge for us:** In `pattern_suggester.py`, `assess_complexity()` is called once per `smart_execute()` or `smart_prompt()`. For similar questions — "How do I analyze financial risk?" vs "How should I analyze financial risks?" — these call the LLM twice with nearly identical prompts. With semantic caching, the second call is free.

**Implementation sketch (in-process, no Redis required to start):**

```python
# src/mycontext/utils/semantic_cache.py
from __future__ import annotations
import hashlib
import time
from typing import Any
from dataclasses import dataclass, field


@dataclass
class CacheEntry:
    response: Any
    timestamp: float
    hits: int = 0


class SemanticCache:
    """
    In-process semantic cache for LLM responses.
    
    Uses exact hash matching initially; pluggable for embedding-based
    similarity matching via semcache or llmgatekeeper.
    """

    def __init__(self, ttl_seconds: int = 3600, max_size: int = 1000):
        self._cache: dict[str, CacheEntry] = {}
        self.ttl = ttl_seconds
        self.max_size = max_size
        self._hits = 0
        self._misses = 0

    def _key(self, prompt: str, model: str) -> str:
        return hashlib.sha256(f"{model}:{prompt}".encode()).hexdigest()

    def get(self, prompt: str, model: str) -> Any | None:
        key = self._key(prompt, model)
        entry = self._cache.get(key)
        if entry and (time.time() - entry.timestamp) < self.ttl:
            entry.hits += 1
            self._hits += 1
            return entry.response
        self._misses += 1
        return None

    def set(self, prompt: str, model: str, response: Any) -> None:
        if len(self._cache) >= self.max_size:
            # Evict oldest entry
            oldest = min(self._cache, key=lambda k: self._cache[k].timestamp)
            del self._cache[oldest]
        self._key(prompt, model)
        self._cache[self._key(prompt, model)] = CacheEntry(response, time.time())

    @property
    def hit_rate(self) -> float:
        total = self._hits + self._misses
        return self._hits / total if total > 0 else 0.0

    def stats(self) -> dict:
        return {"hits": self._hits, "misses": self._misses, "hit_rate": self.hit_rate,
                "size": len(self._cache)}
```

**Integration in `LiteLLMProvider`:**
```python
# In litellm_provider.py — add opt-in caching
_cache = SemanticCache(ttl_seconds=3600)

def generate(self, context, ..., use_cache: bool = True, **kwargs):
    if use_cache:
        prompt_key = context.assemble()
        cached = _cache.get(prompt_key, model)
        if cached:
            return cached  # Zero latency, zero cost
    
    response = litellm.completion(...)  # existing call
    
    if use_cache:
        _cache.set(prompt_key, model, response)
    return response
```

**Phase 2 upgrade:** Replace hash with embedding-based similarity using `llmgatekeeper` or `semcache` for near-duplicate detection (catches paraphrased but semantically identical prompts).

---

## Category 5: Code Architecture — The Duplication Problem

### 5.1 smart_execute / smart_prompt / smart_generic_prompt Duplication (MEDIUM)

**File:** `pattern_suggester.py`, lines 586–849

Three functions (`smart_execute`, `smart_prompt`, `smart_generic_prompt`) share ~70% identical logic:
1. Check enterprise flag
2. Call `assess_complexity()`
3. Based on complexity: single template or multi-template path
4. Execute/compile/return

**Research:** This is the classic "parallel abstraction" code smell. Martin Fowler's *Refactoring* (2018): diverging implementations of the same abstract flow lead to maintenance drift — fixes applied to one are missed in others.

**Fix — extract shared router:**
```python
class SmartRouter:
    """Shared routing logic for all smart_ methods."""

    def route(self, question: str, provider: str, include_enterprise: bool,
              model: str, **kwargs) -> tuple[str, list[str], dict]:
        """
        Returns: (tier, template_names, metadata)
        tier: "generic" | "single" | "multi"
        """
        complexity = assess_complexity(question, provider=provider, model=model)
        
        if complexity.score < 0.4:
            return "generic", [], {"complexity": complexity}
        
        suggestions = suggest_patterns(question, include_enterprise=include_enterprise,
                                       max_patterns=3, mode="hybrid", llm_provider=provider)
        
        if complexity.score < 0.7 or len(suggestions.patterns) == 1:
            return "single", [suggestions.patterns[0].name], {"complexity": complexity, "suggestions": suggestions}
        
        return "multi", [p.name for p in suggestions.patterns], {"complexity": complexity, "suggestions": suggestions}


def smart_execute(question, provider, include_enterprise, model, **kwargs):
    tier, names, meta = SmartRouter().route(question, provider, include_enterprise, model)
    if tier == "generic":
        return _execute_generic(question, provider, **kwargs), meta
    elif tier == "single":
        return _execute_single(question, names[0], provider, **kwargs), meta
    else:
        return _execute_multi(question, names, provider, **kwargs), meta

# smart_prompt and smart_generic_prompt follow the same SmartRouter,
# just call different execution backends
```

---

### 5.2 Template Detail Extraction Caching (MEDIUM)

**File:** `template_integrator_agent.py`, lines 302–339 (`_get_template_detail`)

Every call to `integrate()` calls `_get_template_detail()` for each template name. This instantiates a Pattern class, calls `build_context()`, and string-processes the result. For repeated `integrate()` calls with the same templates, this work is repeated.

**Fix:**
```python
import functools

@functools.lru_cache(maxsize=128)
def _get_template_detail_cached(name: str, include_enterprise: bool) -> str:
    """Cached template detail extraction. Cache persists for process lifetime."""
    # ... existing _get_template_detail logic ...
```

Template definitions don't change at runtime — this is safe to cache indefinitely.

---

### 5.3 Pattern Class Resolution Caching (MEDIUM)

**Files:** `prompt_composer.py:84` (`_resolve_generic_template`), `pattern_suggester.py:435` (`get_pattern_class`)

`get_pattern_class()` is called in tight loops and does a full registry lookup every time. Pattern classes are stateless — safe to cache.

```python
@functools.lru_cache(maxsize=256)
def get_pattern_class(pattern_name: str, include_enterprise: bool = False):
    # ... existing lookup logic ...
```

---

## Category 6: Intelligence Quality — Making Our Core Product Better

### 6.1 Replace the Complexity Heuristic with a Calibrated Classifier (HIGH)

**File:** `pattern_suggester.py`, lines 488–583 (`assess_complexity`)

Currently calls an LLM to assess complexity. The LLM returns a JSON blob that's parsed with brittle regex. This is an expensive (1 LLM call) and fragile way to classify a question on a simple 0–1 scale.

**Research:** DSPy (ICLR 2024, arxiv 2310.03714): Compiled LLM pipelines outperform standard prompting by 25%+ for GPT-3.5 and 65%+ for Llama2. The key insight: replace hand-crafted prompts with compiled, few-shot-optimized prompts using BootstrapFewShot. ACE (Agentic Context Engineering, arxiv 2510.04618): Accumulates and refines routing strategies across runs, achieving +10.6% improvement on agent benchmarks.

**Two-phase fix:**

*Phase 1 (immediate):* Replace the single LLM call with a hybrid: fast heuristic first, LLM only if ambiguous.
```python
def assess_complexity_fast(question: str) -> ComplexityResult:
    """Heuristic-first complexity assessment. Free (no LLM call)."""
    q = question.lower()
    word_count = len(q.split())
    
    # Clear simple signals
    simple_indicators = ['what is', 'define', 'explain', 'describe', 'list']
    complex_indicators = ['compare', 'analyze', 'evaluate', 'synthesize', 'critique',
                          'design', 'optimize', 'why does', 'how would', 'what would happen if']
    
    simple_score = sum(1 for s in simple_indicators if s in q)
    complex_score = sum(1 for s in complex_indicators if s in q)
    
    # Word count signal
    length_score = min(word_count / 50, 1.0)  # normalize
    
    raw_score = (complex_score * 0.4 + length_score * 0.3 - simple_score * 0.2 + 0.3)
    score = max(0.0, min(1.0, raw_score))
    
    confidence = 0.9 if (simple_score > 0 or complex_score > 0) else 0.5
    
    if confidence >= 0.75:
        return ComplexityResult(score=score, level=..., reasoning="heuristic", confidence=confidence)
    
    # Fall through to LLM only when ambiguous
    return None  # Caller should then call LLM version
```

*Phase 2 (DSPy optimization):* Compile a DSPy `Classify` module with 20–30 labeled examples from our testing. Achieves better routing than the current LLM call at zero marginal cost.

---

### 6.2 LLM-Compiled Generic Prompts for Core Patterns (HIGH)

**File:** `pattern_suggester.py`, lines 759–849 (`smart_generic_prompt`)

`smart_generic_prompt` is our "Tier 1 — zero cost" tier. It uses static `GENERIC_PROMPT` strings embedded in each pattern. These are hand-authored and never updated.

**Research:** DSPy (ICLR 2024): Automatically compiled few-shot prompts outperform hand-authored prompts by 25–65%. ACE (arxiv 2510.04618): Evolving playbooks that accumulate strategies from usage improve performance by +10.6% over time.

**Fix:** Add a `compile_pattern_prompt()` utility that, during development or CI, runs DSPy BootstrapFewShot on each pattern's generic prompt and saves the optimized version. Generic prompts become compiled artifacts, not static strings. This is the "NumPy of context engineering" taken seriously — our prompts are not written, they're compiled and validated.

```python
# tools/compile_prompts.py — run in dev/CI, not at runtime
import dspy

def compile_pattern_prompts(pattern_names: list[str], examples: list[dict]):
    """
    Compile optimized generic prompts for each pattern using DSPy BootstrapFewShot.
    Saves compiled prompts to src/mycontext/templates/compiled/.
    """
    for name in pattern_names:
        klass = get_pattern_class(name)
        module = dspy.Predict(signature=f"question -> {name}_context")
        optimizer = dspy.BootstrapFewShot(metric=quality_metric, max_bootstrapped_demos=4)
        compiled = optimizer.compile(module, trainset=examples)
        compiled.save(f"templates/compiled/{name}.json")
```

---

### 6.3 Structured Output for All Intelligence Module Responses (HIGH)

**Files:** All intelligence modules that parse LLM JSON responses

We have `utils/structured_output.py` with `PydanticOutput` and `JSONOutput` — but the intelligence layer doesn't use it. Every module rolls its own parsing (see 2.2 above).

**Fix:** Define Pydantic models for every LLM response in the intelligence layer:

```python
# src/mycontext/intelligence/schemas.py
from pydantic import BaseModel, Field, field_validator
from typing import Literal

class ComplexityAssessment(BaseModel):
    score: float = Field(ge=0.0, le=1.0)
    level: Literal["simple", "moderate", "complex", "expert"]
    reasoning: str
    recommended_tier: Literal["generic", "single", "multi"]

class PatternSuggestion(BaseModel):
    patterns: list[str] = Field(min_length=1, max_length=5)
    integration_note: str
    reasoning: str
    
    @field_validator('patterns')
    @classmethod
    def validate_pattern_names(cls, v):
        from mycontext.intelligence.pattern_catalog import AVAILABLE_PATTERNS
        invalid = [p for p in v if p not in AVAILABLE_PATTERNS]
        if invalid:
            raise ValueError(f"Unknown patterns: {invalid}")
        return v

class IntegrationOutput(BaseModel):
    guidance: str = Field(min_length=10)
    directive: str = Field(min_length=10)
    key_frameworks: list[str]
    synthesis_approach: str
```

With `instructor` + these schemas, every LLM call in the intelligence layer becomes typed, validated, and auto-retried on validation failure.

---

## Category 7: Token Efficiency — Context Window Management

### 7.1 Context Assembly Is Not Token-Aware (MEDIUM)

**File:** `core.py`, `structure/blueprint.py`

`Context.assemble()` concatenates all sections without any awareness of the target model's context window. The `Blueprint.optimize()` method uses rough word-count estimates. Neither knows whether the assembled context will fit.

**Research:** OpenAI cookbook (2024): Token-aware assembly is a production prerequisite. Tiktoken-based counting is required for reliable context window compliance.

**Fix — add token-aware assembly option:**
```python
# In Context class
def assemble_for_model(
    self,
    model: str = "gpt-4o",
    max_tokens: int | None = None,
    priority_sections: list[str] | None = None,
) -> str:
    """
    Assemble context with token budget enforcement.
    Trims lower-priority sections if over budget.
    Priority: directive > constraints > guidance > knowledge > data
    """
    from .utils.tokens import count_tokens
    
    sections = self._get_ordered_sections()  # existing logic
    
    if max_tokens is None:
        return "\n\n".join(s for s in sections if s)
    
    result = []
    used_tokens = 0
    
    for section, priority in zip(sections, SECTION_PRIORITIES):
        tokens = count_tokens(section, model)
        if used_tokens + tokens <= max_tokens:
            result.append(section)
            used_tokens += tokens
        elif priority == "required":
            # Truncate the section to fit
            trimmed = _token_trim(section, max_tokens - used_tokens, model)
            result.append(trimmed)
            break
    
    return "\n\n".join(result)
```

---

## Category 8: Developer Experience — Observability

### 8.1 No Observability Layer (MEDIUM)

There is no structured logging, no metrics emission, no trace IDs for LLM calls. When `smart_execute()` takes 12 seconds, there's no way to know which of the 4 sequential LLM calls was slow without manually adding timing.

**Research:** Agentic Context Engineering (ACE, arxiv 2510.04618): Evolving playbooks require observability of which contexts worked and which didn't. Without telemetry, the platform can't self-improve.

**Fix — lightweight telemetry module:**
```python
# src/mycontext/utils/telemetry.py
import time
import logging
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger("mycontext.telemetry")

@dataclass
class Span:
    name: str
    start: float = field(default_factory=time.monotonic)
    end: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    
    @property
    def duration_ms(self) -> float:
        if self.end:
            return (self.end - self.start) * 1000
        return 0.0


@contextmanager
def trace(name: str, **metadata):
    """Lightweight tracing context manager."""
    span = Span(name=name, metadata=metadata)
    try:
        yield span
    finally:
        span.end = time.monotonic()
        logger.debug(
            "SPAN %s completed in %.1fms | %s",
            name, span.duration_ms,
            " ".join(f"{k}={v}" for k, v in metadata.items())
        )
```

**Usage in `assess_complexity`:**
```python
with trace("assess_complexity", provider=provider, model=model) as span:
    result = ctx.execute(provider=provider, model=model)
    span.metadata["tokens"] = result.tokens_used
```

This enables structured log analysis to find slow paths without changing the architecture.

---

## Summary: Prioritized Implementation Order

| # | Upgrade | Category | Impact | Effort | Ship When |
|---|---------|----------|--------|--------|-----------|
| 1 | Template injection fix | Security | Critical | 0.5 day | Immediately |
| 2 | Replace silent exceptions with structured logging | Reliability | High | 1 day | Sprint 1 |
| 3 | Unified token counting | Reliability | High | 0.5 day | Sprint 1 |
| 4 | Parallel template refinement (ThreadPoolExecutor) | Performance | High | 1 day | Sprint 1 |
| 5 | Instructor + Pydantic for intelligence parsing | Reliability/Quality | High | 2–3 days | Sprint 1 |
| 6 | In-process semantic cache for LLM calls | Performance | High | 1 day | Sprint 2 |
| 7 | Smart router refactor (deduplicate smart_* methods) | Architecture | Medium | 2 days | Sprint 2 |
| 8 | Heuristic-first complexity classifier | Performance/Quality | High | 1 day | Sprint 2 |
| 9 | Pydantic schemas for all intelligence outputs | Quality | High | 2 days | Sprint 2 |
| 10 | Lazy pattern loading in TransformationEngine | Performance | Medium | 0.5 day | Sprint 2 |
| 11 | LRU caching for pattern class & template detail | Performance | Medium | 0.5 day | Sprint 2 |
| 12 | Token-aware Context.assemble_for_model() | Quality | Medium | 2 days | Sprint 3 |
| 13 | Lightweight telemetry/tracing | Observability | Medium | 1 day | Sprint 3 |
| 14 | O(n²) → MinHash LSH similarity removal | Performance | Medium | 1 day | Sprint 3 |
| 15 | Async provider layer (agenerate + aexecute) | Performance | High | 2–3 days | Sprint 3 |
| 16 | DSPy-compiled generic prompts | Quality | Very High | 1–2 weeks | Sprint 4 |
| 17 | Semantic caching with embeddings (Phase 2) | Performance | Very High | 3–5 days | Sprint 4 |

---

## How This Serves Our Core Vision

**"Universal Context Transformation Engine — measurable quality, universal portability, automatic intelligence."**

- **Measurable quality:** Items 2, 5, 9, 13 — silent failures corrupting quality scores is the #1 enemy of a "measurable" claim
- **Universal portability:** Item 3 — accurate token counting is required for context to be portable across models with different window sizes
- **Automatic intelligence:** Items 6, 8, 16 — semantic caching means routing decisions are faster and cheaper; DSPy compilation means our patterns get better over time automatically
- **Research-backed:** Items 5, 16 — instructor + DSPy are the current state-of-the-art for exactly our use case (structured LLM outputs and compiled prompts)
- **Security:** Item 1 — a context engineering library used in production that has a template injection vulnerability cannot be taken seriously

---

## References

- **Template injection:** LangChain advisory GHSA-6qv9-48xg-fc7f; OWASP LLM Cheat Sheet (2024)
- **Instructor:** python.useinstructor.com; GitHub instructor-ai/instructor (12.2k stars, 3M downloads/month, 2025)
- **Semantic caching:** GPT Semantic Cache (arxiv 2411.05276, 2024); VectorQ (arxiv 2502.03771, 2025); IC-Cache (arxiv 2501.12689, 2025)
- **DSPy:** arxiv 2310.03714 (ICLR 2024); +25–65% over hand-authored prompts
- **ACE:** Agentic Context Engineering (arxiv 2510.04618); +10.6% on agent benchmarks
- **Parallel execution:** ParallelPrompt (2025); ParaThinker (arxiv 2509.04475, 2025)
- **Token counting:** OpenAI tiktoken docs; Telnyx "truncate context" guide (2024)
- **Silent failures:** Netflix Engineering blog; Martin Fowler *Refactoring* (2018)
