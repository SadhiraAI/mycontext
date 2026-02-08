"""
Cost Tracking & Analytics - Monitor usage, costs, and performance.

Track LLM usage across providers, projects, and templates.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field
import json
from pathlib import Path


@dataclass
class UsageRecord:
    """Single usage record."""
    
    timestamp: str
    provider: str
    model: str
    template: Optional[str]
    tokens_used: int
    cost_usd: float
    latency_ms: int
    success: bool
    metadata: Dict[str, Any] = field(default_factory=dict)


class CostTracker:
    """
    Track costs and usage across all LLM calls.
    
    Examples:
        >>> tracker = CostTracker()
        >>> 
        >>> # Track a call
        >>> result = provider.generate(context, user="...")
        >>> tracker.record(
        ...     provider="gemini",
        ...     model="gemini-2.5-flash",
        ...     tokens=result.tokens_used,
        ...     cost=result.cost_usd
        ... )
        >>> 
        >>> # Get statistics
        >>> print(tracker.get_summary())
    """
    
    def __init__(self, persist_to: Optional[str] = None):
        """
        Initialize cost tracker.
        
        Args:
            persist_to: Optional file path to persist records
        """
        self.records: List[UsageRecord] = []
        self.persist_to = Path(persist_to) if persist_to else None
        
        # Load existing records if file exists
        if self.persist_to and self.persist_to.exists():
            self._load_records()
    
    def record(
        self,
        provider: str,
        model: str,
        tokens: int,
        cost: float,
        latency_ms: int = 0,
        template: Optional[str] = None,
        success: bool = True,
        **metadata
    ):
        """
        Record a usage event.
        
        Args:
            provider: Provider name
            model: Model name
            tokens: Tokens used
            cost: Cost in USD
            latency_ms: Latency in milliseconds
            template: Template name (if applicable)
            success: Whether call succeeded
            **metadata: Additional metadata
        """
        record = UsageRecord(
            timestamp=datetime.now().isoformat(),
            provider=provider,
            model=model,
            template=template,
            tokens_used=tokens,
            cost_usd=cost,
            latency_ms=latency_ms,
            success=success,
            metadata=metadata
        )
        
        self.records.append(record)
        
        # Persist if configured
        if self.persist_to:
            self._save_records()
    
    def get_summary(
        self,
        provider: Optional[str] = None,
        template: Optional[str] = None,
        timeframe: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get usage summary.
        
        Args:
            provider: Filter by provider
            template: Filter by template
            timeframe: Filter by timeframe ("today", "week", "month")
            
        Returns:
            Summary statistics
        """
        # Filter records
        filtered = self.records
        
        if provider:
            filtered = [r for r in filtered if r.provider == provider]
        
        if template:
            filtered = [r for r in filtered if r.template == template]
        
        if timeframe:
            # Simple timeframe filtering (could be enhanced)
            filtered = [r for r in filtered if self._in_timeframe(r.timestamp, timeframe)]
        
        if not filtered:
            return {"message": "No records found"}
        
        # Calculate statistics
        total_cost = sum(r.cost_usd for r in filtered)
        total_tokens = sum(r.tokens_used for r in filtered)
        avg_latency = sum(r.latency_ms for r in filtered) / len(filtered)
        success_rate = sum(1 for r in filtered if r.success) / len(filtered) * 100
        
        # By provider
        by_provider = {}
        for record in filtered:
            if record.provider not in by_provider:
                by_provider[record.provider] = {
                    "calls": 0,
                    "tokens": 0,
                    "cost": 0.0
                }
            
            by_provider[record.provider]["calls"] += 1
            by_provider[record.provider]["tokens"] += record.tokens_used
            by_provider[record.provider]["cost"] += record.cost_usd
        
        return {
            "total_calls": len(filtered),
            "total_cost": f"${total_cost:.4f}",
            "total_tokens": total_tokens,
            "avg_cost_per_call": f"${total_cost/len(filtered):.6f}",
            "avg_tokens_per_call": int(total_tokens/len(filtered)),
            "avg_latency_ms": int(avg_latency),
            "success_rate": f"{success_rate:.1f}%",
            "by_provider": by_provider,
        }
    
    def get_recent(self, n: int = 10) -> List[UsageRecord]:
        """Get n most recent records."""
        return self.records[-n:]
    
    def get_most_expensive(self, n: int = 10) -> List[UsageRecord]:
        """Get n most expensive calls."""
        return sorted(self.records, key=lambda r: r.cost_usd, reverse=True)[:n]
    
    def _in_timeframe(self, timestamp: str, timeframe: str) -> bool:
        """Check if timestamp is in timeframe."""
        # Simplified - could use proper date parsing
        return True  # TODO: Implement proper timeframe checking
    
    def _save_records(self):
        """Save records to file."""
        if not self.persist_to:
            return
        
        data = [
            {
                "timestamp": r.timestamp,
                "provider": r.provider,
                "model": r.model,
                "template": r.template,
                "tokens_used": r.tokens_used,
                "cost_usd": r.cost_usd,
                "latency_ms": r.latency_ms,
                "success": r.success,
                "metadata": r.metadata,
            }
            for r in self.records
        ]
        
        self.persist_to.write_text(json.dumps(data, indent=2))
    
    def _load_records(self):
        """Load records from file."""
        if not self.persist_to or not self.persist_to.exists():
            return
        
        data = json.loads(self.persist_to.read_text())
        
        self.records = [
            UsageRecord(
                timestamp=r["timestamp"],
                provider=r["provider"],
                model=r["model"],
                template=r.get("template"),
                tokens_used=r["tokens_used"],
                cost_usd=r["cost_usd"],
                latency_ms=r["latency_ms"],
                success=r["success"],
                metadata=r.get("metadata", {})
            )
            for r in data
        ]


class UsageAnalytics:
    """
    Advanced analytics on usage patterns.
    
    Analyze trends, identify cost optimization opportunities, track performance.
    """
    
    def __init__(self, tracker: CostTracker):
        """
        Initialize analytics.
        
        Args:
            tracker: CostTracker instance
        """
        self.tracker = tracker
    
    def get_cost_breakdown(self) -> Dict[str, Any]:
        """Get detailed cost breakdown."""
        records = self.tracker.records
        
        by_provider = {}
        by_template = {}
        by_model = {}
        
        for record in records:
            # By provider
            if record.provider not in by_provider:
                by_provider[record.provider] = 0.0
            by_provider[record.provider] += record.cost_usd
            
            # By template
            if record.template:
                if record.template not in by_template:
                    by_template[record.template] = 0.0
                by_template[record.template] += record.cost_usd
            
            # By model
            if record.model not in by_model:
                by_model[record.model] = 0.0
            by_model[record.model] += record.cost_usd
        
        return {
            "by_provider": {k: f"${v:.4f}" for k, v in by_provider.items()},
            "by_template": {k: f"${v:.4f}" for k, v in by_template.items()},
            "by_model": {k: f"${v:.4f}" for k, v in by_model.items()},
        }
    
    def identify_cost_savings(self) -> List[Dict[str, Any]]:
        """Identify opportunities to reduce costs."""
        recommendations = []
        
        # Check if using expensive models for simple tasks
        expensive_models = ["gpt-4", "gpt-4-turbo", "claude-3-opus"]
        
        for record in self.tracker.records:
            if any(model in record.model for model in expensive_models):
                if record.tokens_used < 500:  # Simple task
                    recommendations.append({
                        "type": "expensive_model_for_simple_task",
                        "message": f"Used {record.model} for {record.tokens_used} tokens",
                        "suggestion": "Consider using gemini-2.5-flash or gpt-4o-mini",
                        "potential_savings": record.cost_usd * 0.9  # ~90% cheaper
                    })
        
        return recommendations
    
    def get_performance_trends(self) -> Dict[str, Any]:
        """Get performance trends over time."""
        if not self.tracker.records:
            return {}
        
        recent = self.tracker.records[-100:]  # Last 100 calls
        
        avg_latency = sum(r.latency_ms for r in recent) / len(recent)
        avg_tokens = sum(r.tokens_used for r in recent) / len(recent)
        avg_cost = sum(r.cost_usd for r in recent) / len(recent)
        
        return {
            "avg_latency_ms": int(avg_latency),
            "avg_tokens_per_call": int(avg_tokens),
            "avg_cost_per_call": f"${avg_cost:.6f}",
            "sample_size": len(recent),
        }


class PerformanceMonitor:
    """Monitor performance metrics for optimization."""
    
    def __init__(self):
        """Initialize performance monitor."""
        self.metrics = []
    
    def track_call(
        self,
        operation: str,
        duration_ms: int,
        tokens: int,
        cost: float,
        success: bool = True
    ):
        """Track a single call."""
        self.metrics.append({
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "duration_ms": duration_ms,
            "tokens": tokens,
            "cost": cost,
            "success": success
        })
    
    def get_slow_operations(self, threshold_ms: int = 5000) -> List[Dict]:
        """Identify slow operations."""
        return [
            m for m in self.metrics
            if m["duration_ms"] > threshold_ms
        ]
    
    def get_expensive_operations(self, threshold_usd: float = 0.01) -> List[Dict]:
        """Identify expensive operations."""
        return [
            m for m in self.metrics
            if m["cost"] > threshold_usd
        ]
