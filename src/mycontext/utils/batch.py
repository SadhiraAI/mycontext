"""
Batch Processing - Execute multiple templates or contexts efficiently.

Process multiple inputs in parallel or sequence with progress tracking.
"""

import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Any


@dataclass
class BatchResult:
    """Result from batch processing."""

    results: list[Any]
    total_cost: float
    total_tokens: int
    total_time: float
    successful: int
    failed: int
    errors: list[dict[str, Any]]

    def summary(self) -> dict[str, Any]:
        """Get summary statistics."""
        return {
            "total_items": len(self.results),
            "successful": self.successful,
            "failed": self.failed,
            "total_cost": f"${self.total_cost:.4f}",
            "total_tokens": self.total_tokens,
            "total_time": f"{self.total_time:.2f}s",
            "avg_cost_per_item": f"${self.total_cost/self.successful:.6f}" if self.successful > 0 else "$0",
            "avg_time_per_item": f"{self.total_time/self.successful:.2f}s" if self.successful > 0 else "0s",
        }


class BatchProcessor:
    """
    Process multiple templates or contexts in batch.
    
    Examples:
        >>> from mycontext.templates.free import QuestionAnalyzer
        >>> 
        >>> processor = BatchProcessor(max_workers=5)
        >>> questions = ["Q1", "Q2", "Q3"]
        >>> 
        >>> def process_question(q):
        ...     analyzer = QuestionAnalyzer()
        ...     return analyzer.execute(provider="gemini", question=q)
        >>> 
        >>> results = processor.process(questions, process_question)
        >>> print(results.summary())
    """

    def __init__(
        self,
        max_workers: int = 5,
        show_progress: bool = True,
        stop_on_error: bool = False
    ):
        """
        Initialize batch processor.
        
        Args:
            max_workers: Maximum parallel workers
            show_progress: Show progress bar
            stop_on_error: Stop on first error
        """
        self.max_workers = max_workers
        self.show_progress = show_progress
        self.stop_on_error = stop_on_error

    def process(
        self,
        items: list[Any],
        process_func: Callable,
        parallel: bool = True
    ) -> BatchResult:
        """
        Process items in batch.
        
        Args:
            items: List of items to process
            process_func: Function to apply to each item
            parallel: Whether to process in parallel
            
        Returns:
            BatchResult with all results and statistics
        """
        start_time = time.time()

        results = []
        errors = []
        total_cost = 0.0
        total_tokens = 0
        successful = 0
        failed = 0

        if parallel:
            # Parallel processing
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {executor.submit(process_func, item): i for i, item in enumerate(items)}

                for future in as_completed(futures):
                    idx = futures[future]
                    try:
                        result = future.result()
                        results.append((idx, result))

                        # Track metrics if available
                        if hasattr(result, 'cost_usd'):
                            total_cost += result.cost_usd
                        if hasattr(result, 'tokens_used'):
                            total_tokens += result.tokens_used

                        successful += 1

                        if self.show_progress:
                            print(f"✅ Processed {successful}/{len(items)}")

                    except Exception as e:
                        failed += 1
                        errors.append({
                            "index": idx,
                            "item": str(items[idx])[:100],
                            "error": str(e)
                        })

                        if self.stop_on_error:
                            raise

                        if self.show_progress:
                            print(f"❌ Failed {failed}/{len(items)}: {e}")

            # Sort by original index
            results.sort(key=lambda x: x[0])
            results = [r[1] for r in results]

        else:
            # Sequential processing
            for i, item in enumerate(items):
                try:
                    result = process_func(item)
                    results.append(result)

                    if hasattr(result, 'cost_usd'):
                        total_cost += result.cost_usd
                    if hasattr(result, 'tokens_used'):
                        total_tokens += result.tokens_used

                    successful += 1

                    if self.show_progress:
                        print(f"✅ Processed {i+1}/{len(items)}")

                except Exception as e:
                    failed += 1
                    errors.append({
                        "index": i,
                        "item": str(item)[:100],
                        "error": str(e)
                    })

                    if self.stop_on_error:
                        raise

                    if self.show_progress:
                        print(f"❌ Failed {i+1}/{len(items)}: {e}")

        total_time = time.time() - start_time

        return BatchResult(
            results=results,
            total_cost=total_cost,
            total_tokens=total_tokens,
            total_time=total_time,
            successful=successful,
            failed=failed,
            errors=errors
        )

    def process_with_template(
        self,
        template,
        items: list[dict[str, Any]],
        provider: str = "gemini",
        parallel: bool = True,
        **common_kwargs
    ) -> BatchResult:
        """
        Process multiple inputs with the same template.
        
        Args:
            template: Template instance to use
            items: List of input dicts for template
            provider: Provider to use
            parallel: Process in parallel
            **common_kwargs: Common kwargs for all executions
            
        Returns:
            BatchResult
            
        Example:
            >>> from mycontext.templates.free import QuestionAnalyzer
            >>> 
            >>> analyzer = QuestionAnalyzer()
            >>> questions = [
            ...     {"question": "What is ML?"},
            ...     {"question": "What is DL?"},
            ... ]
            >>> 
            >>> results = processor.process_with_template(
            ...     analyzer,
            ...     questions,
            ...     provider="gemini"
            ... )
        """
        def process_item(inputs):
            merged = {**common_kwargs, **inputs}
            return template.execute(provider=provider, **merged)

        return self.process(items, process_item, parallel=parallel)


# Convenience function

def batch_execute(
    template,
    items: list[dict[str, Any]],
    provider: str = "gemini",
    max_workers: int = 5,
    parallel: bool = True
) -> BatchResult:
    """
    Quick batch execution.
    
    Example:
        >>> from mycontext.templates.free import QuestionAnalyzer
        >>> from mycontext.utils import batch_execute
        >>> 
        >>> questions = [
        ...     {"question": "What is Python?"},
        ...     {"question": "What is JavaScript?"},
        ... ]
        >>> 
        >>> results = batch_execute(QuestionAnalyzer(), questions)
        >>> print(results.summary())
    """
    processor = BatchProcessor(max_workers=max_workers)
    return processor.process_with_template(template, items, provider, parallel)
