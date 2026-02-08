"""
Context Caching - Cache contexts and responses for efficiency.

Reduce costs and latency by caching repeated contexts.
"""

import hashlib
import json
from typing import Any, Dict, Optional, Callable
from datetime import datetime, timedelta
from pathlib import Path


class CacheStrategy:
    """Strategy for cache invalidation."""
    
    TTL = "ttl"  # Time-to-live
    LRU = "lru"  # Least Recently Used
    LFU = "lfu"  # Least Frequently Used
    NONE = "none"  # No eviction


class ContextCache:
    """
    Cache for contexts to avoid regeneration.
    
    Examples:
        >>> cache = ContextCache(max_size=100, ttl_seconds=3600)
        >>> 
        >>> # Check cache first
        >>> key = cache.get_key(context)
        >>> if cached := cache.get(key):
        ...     return cached
        >>> 
        >>> # Generate and cache
        >>> result = provider.generate(context, user="...")
        >>> cache.set(key, result)
    """
    
    def __init__(
        self,
        max_size: int = 1000,
        ttl_seconds: int = 3600,
        strategy: str = CacheStrategy.LRU,
        persist_to: Optional[str] = None
    ):
        """
        Initialize context cache.
        
        Args:
            max_size: Maximum cache entries
            ttl_seconds: Time-to-live in seconds
            strategy: Eviction strategy
            persist_to: Optional file for persistence
        """
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.strategy = strategy
        self.persist_to = Path(persist_to) if persist_to else None
        
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._access_counts: Dict[str, int] = {}
        self._access_times: Dict[str, datetime] = {}
        
        # Load from disk if available
        if self.persist_to and self.persist_to.exists():
            self._load()
    
    def get_key(self, obj: Any) -> str:
        """
        Generate cache key from object.
        
        Args:
            obj: Object to generate key for (Context, dict, etc.)
            
        Returns:
            Hash key
        """
        if hasattr(obj, 'assemble'):
            # Context object
            content = obj.assemble()
        elif isinstance(obj, dict):
            content = json.dumps(obj, sort_keys=True)
        else:
            content = str(obj)
        
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get cached value.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None
        """
        if key not in self._cache:
            return None
        
        entry = self._cache[key]
        
        # Check TTL
        if self.ttl_seconds > 0:
            cached_time = datetime.fromisoformat(entry["cached_at"])
            if datetime.now() - cached_time > timedelta(seconds=self.ttl_seconds):
                # Expired
                del self._cache[key]
                return None
        
        # Update access tracking
        self._access_counts[key] = self._access_counts.get(key, 0) + 1
        self._access_times[key] = datetime.now()
        
        return entry["value"]
    
    def set(self, key: str, value: Any):
        """
        Set cache value.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        # Evict if at capacity
        if len(self._cache) >= self.max_size:
            self._evict()
        
        self._cache[key] = {
            "value": value,
            "cached_at": datetime.now().isoformat()
        }
        
        self._access_counts[key] = 1
        self._access_times[key] = datetime.now()
        
        # Persist if configured
        if self.persist_to:
            self._save()
    
    def clear(self):
        """Clear all cache entries."""
        self._cache.clear()
        self._access_counts.clear()
        self._access_times.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "size": len(self._cache),
            "max_size": self.max_size,
            "hit_rate": self._calculate_hit_rate(),
            "total_accesses": sum(self._access_counts.values()),
        }
    
    def _evict(self):
        """Evict entries based on strategy."""
        if not self._cache:
            return
        
        if self.strategy == CacheStrategy.LRU:
            # Remove least recently used
            oldest_key = min(self._access_times.keys(), key=lambda k: self._access_times[k])
            del self._cache[oldest_key]
            del self._access_counts[oldest_key]
            del self._access_times[oldest_key]
        
        elif self.strategy == CacheStrategy.LFU:
            # Remove least frequently used
            least_used = min(self._access_counts.keys(), key=lambda k: self._access_counts[k])
            del self._cache[least_used]
            del self._access_counts[least_used]
            del self._access_times[least_used]
        
        else:
            # Remove oldest
            first_key = next(iter(self._cache))
            del self._cache[first_key]
    
    def _calculate_hit_rate(self) -> str:
        """Calculate cache hit rate."""
        # This would require tracking hits/misses
        return "N/A"
    
    def _save(self):
        """Save cache to disk."""
        if not self.persist_to:
            return
        
        data = {
            "cache": self._cache,
            "access_counts": self._access_counts,
            "access_times": {k: v.isoformat() for k, v in self._access_times.items()}
        }
        
        self.persist_to.write_text(json.dumps(data, indent=2, default=str))
    
    def _load(self):
        """Load cache from disk."""
        if not self.persist_to or not self.persist_to.exists():
            return
        
        data = json.loads(self.persist_to.read_text())
        
        self._cache = data.get("cache", {})
        self._access_counts = data.get("access_counts", {})
        self._access_times = {
            k: datetime.fromisoformat(v)
            for k, v in data.get("access_times", {}).items()
        }


class ResponseCache:
    """
    Cache for LLM responses based on input.
    
    More efficient than ContextCache - caches final responses.
    """
    
    def __init__(self, max_size: int = 500, ttl_seconds: int = 3600):
        """
        Initialize response cache.
        
        Args:
            max_size: Maximum cached responses
            ttl_seconds: Time-to-live
        """
        self.cache = ContextCache(
            max_size=max_size,
            ttl_seconds=ttl_seconds,
            strategy=CacheStrategy.LRU
        )
    
    def get_or_generate(
        self,
        context: Any,
        user_input: str,
        generate_func: Callable,
        **kwargs
    ) -> Any:
        """
        Get cached response or generate new one.
        
        Args:
            context: Context object
            user_input: User input
            generate_func: Function to call if not cached
            **kwargs: Additional args for generate_func
            
        Returns:
            Cached or newly generated response
        """
        # Create cache key from context + input
        cache_key = self.cache.get_key(f"{context}{user_input}")
        
        # Check cache
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        
        # Generate
        result = generate_func(context, user=user_input, **kwargs)
        
        # Cache result
        self.cache.set(cache_key, result)
        
        return result


# Convenience function

def with_cache(cache: ContextCache, key_func: Optional[Callable] = None):
    """
    Decorator for caching function results.
    
    Example:
        >>> cache = ContextCache()
        >>> 
        >>> @with_cache(cache)
        >>> def analyze(question):
        ...     return analyzer.execute(provider="gemini", question=question)
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Generate key
            if key_func:
                key = key_func(*args, **kwargs)
            else:
                key = cache.get_key(str(args) + str(kwargs))
            
            # Check cache
            cached = cache.get(key)
            if cached:
                return cached
            
            # Execute and cache
            result = func(*args, **kwargs)
            cache.set(key, result)
            
            return result
        
        return wrapper
    return decorator
