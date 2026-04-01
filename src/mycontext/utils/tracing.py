"""
Execution Tracing — lightweight observability for LLM calls.

Research basis:
  "Observability in ML Systems" (Klaise et al., 2022): Structured per-request
  traces are the primary mechanism for diagnosing latency regressions and
  quality degradation in production ML serving pipelines.

  "The Building Blocks of Interpretability" (Olah et al., 2018): Step-level
  logging of intermediate computations enables post-hoc analysis that is
  impossible when only final outputs are recorded.

  Without this layer, when smart_execute() takes 12 seconds, there is no way
  to determine which of the potentially 4+ sequential LLM calls was slow.

Design
------
A "trace" is a tree of "spans" — each span represents one logical unit of
work (one LLM call, one template resolution, one routing decision).  This
mirrors OpenTelemetry's data model without requiring the OTel SDK as a
dependency.

Spans are lightweight dataclasses.  The in-process tracer stores spans in a
thread-local deque (configurable max depth).  For production integration,
callers can register a custom exporter that forwards spans to any backend
(LangSmith, Weights & Biases, DataDog, OpenTelemetry Collector, etc.).

Usage::

    from mycontext.utils.tracing import get_tracer

    tracer = get_tracer()

    with tracer.span("llm_call", metadata={"model": "gpt-4o"}) as span:
        result = provider.generate(ctx)
        span.set("tokens", result.tokens_used)
        span.set("cost_usd", result.cost_usd)

    # Get all spans from the current trace
    spans = tracer.current_spans()
    tracer.log_summary()      # one-line summary to logger
    tracer.clear()            # reset for next request
"""

from __future__ import annotations

import logging
import threading
import time
import uuid
from collections import deque
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)

_TRACE_ID_VAR: threading.local = threading.local()


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class Span:
    """One unit of traced work."""

    name: str
    trace_id: str
    span_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    parent_id: str | None = None
    started_at: float = field(default_factory=time.monotonic)
    ended_at: float | None = None
    status: str = "ok"  # "ok" | "error"
    attributes: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

    @property
    def duration_ms(self) -> float | None:
        if self.ended_at is None:
            return None
        return round((self.ended_at - self.started_at) * 1000, 2)

    def set(self, key: str, value: Any) -> None:
        """Record an attribute on this span."""
        self.attributes[key] = value

    def end(self, error: str | None = None) -> None:
        self.ended_at = time.monotonic()
        if error:
            self.status = "error"
            self.error = error

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_id": self.parent_id,
            "duration_ms": self.duration_ms,
            "status": self.status,
            "attributes": self.attributes,
            "error": self.error,
        }


# ---------------------------------------------------------------------------
# Tracer
# ---------------------------------------------------------------------------


class Tracer:
    """
    Lightweight in-process tracer.

    One ``Tracer`` instance is shared per process via ``get_tracer()``.
    Spans are stored in a thread-local bounded deque so concurrent requests
    don't mix their traces.

    Args:
        max_spans: Maximum spans retained per thread (older spans are evicted).
        exporters: Optional list of callables that receive each completed Span
                   for forwarding to external backends (LangSmith, OTel, etc.).

    Example::

        tracer = get_tracer()
        with tracer.span("assess_complexity") as s:
            result = assess_complexity(question)
            s.set("recommendation", result.recommendation)
        tracer.log_summary()
    """

    def __init__(
        self,
        max_spans: int = 200,
        exporters: list[Callable[[Span], None]] | None = None,
    ) -> None:
        self.max_spans = max_spans
        self._exporters: list[Callable[[Span], None]] = exporters or []
        self._local = threading.local()

    # ------------------------------------------------------------------
    # Thread-local store
    # ------------------------------------------------------------------

    def _get_spans(self) -> deque[Span]:
        if not hasattr(self._local, "spans"):
            self._local.spans = deque(maxlen=self.max_spans)
        return self._local.spans

    def _get_trace_id(self) -> str:
        if not hasattr(self._local, "trace_id") or self._local.trace_id is None:
            self._local.trace_id = uuid.uuid4().hex
        return self._local.trace_id

    def _get_active_span(self) -> Span | None:
        if not hasattr(self._local, "active_span"):
            self._local.active_span = None
        return self._local.active_span

    def _set_active_span(self, span: Span | None) -> None:
        self._local.active_span = span

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @contextmanager
    def span(
        self,
        name: str,
        metadata: dict[str, Any] | None = None,
    ) -> Iterator[Span]:
        """Context manager that creates, yields, and closes a Span.

        Args:
            name:     Descriptive name for this unit of work (e.g. "llm_call",
                      "assess_complexity", "template_refinement").
            metadata: Initial attributes to record on the span.

        Yields:
            The active Span — call ``span.set(key, value)`` to add attributes.
        """
        trace_id = self._get_trace_id()
        parent = self._get_active_span()
        s = Span(
            name=name,
            trace_id=trace_id,
            parent_id=parent.span_id if parent else None,
            attributes=dict(metadata or {}),
        )
        self._get_spans().append(s)
        self._set_active_span(s)
        try:
            yield s
        except Exception as exc:
            s.end(error=str(exc))
            self._export(s)
            raise
        else:
            s.end()
            self._export(s)
        finally:
            self._set_active_span(parent)

    def current_spans(self) -> list[Span]:
        """Return all spans recorded in the current thread's trace."""
        return list(self._get_spans())

    def current_trace_id(self) -> str:
        """Return the current thread's trace ID."""
        return self._get_trace_id()

    def clear(self) -> None:
        """Reset the current thread's trace (call between requests)."""
        self._get_spans().clear()
        self._local.trace_id = uuid.uuid4().hex
        self._set_active_span(None)

    def log_summary(self) -> None:
        """Log a one-line summary of all completed spans to the module logger."""
        spans = self.current_spans()
        if not spans:
            return
        total_ms = sum(s.duration_ms or 0 for s in spans)
        errors = [s for s in spans if s.status == "error"]
        llm_spans = [s for s in spans if "llm" in s.name.lower() or "generate" in s.name.lower()]
        llm_tokens = sum(s.attributes.get("tokens", 0) for s in llm_spans)
        llm_cost = sum(s.attributes.get("cost_usd", 0.0) for s in llm_spans)
        logger.info(
            "Trace %s | %d spans | %.0fms total | %d LLM calls | %d tokens | $%.6f | %d errors",
            self._get_trace_id()[:8],
            len(spans),
            total_ms,
            len(llm_spans),
            llm_tokens,
            llm_cost,
            len(errors),
        )

    def register_exporter(self, fn: Callable[[Span], None]) -> None:
        """Register a function to call with each completed Span.

        Args:
            fn: Callable that receives a :class:`Span` and forwards it to an
                external backend (LangSmith, DataDog, OTel Collector, etc.).
        """
        self._exporters.append(fn)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _export(self, span: Span) -> None:
        for exporter in self._exporters:
            try:
                exporter(span)
            except Exception as exc:
                logger.debug("Span exporter error: %s", exc)


# ---------------------------------------------------------------------------
# Module-level default instance
# ---------------------------------------------------------------------------

_default_tracer = Tracer(max_spans=200)


def get_tracer() -> Tracer:
    """Return the shared default Tracer instance."""
    return _default_tracer
