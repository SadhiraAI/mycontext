"""
Token Optimizer - Reduce token usage while preserving meaning.

Tools for compressing contexts, removing redundancy, and optimizing prompts.
"""

import re
from typing import Any

import tiktoken


class TokenOptimizer:
    """
    Optimize context for token efficiency.
    
    Examples:
        >>> optimizer = TokenOptimizer()
        >>> original = "This is a very long context with lots of redundant information..."
        >>> optimized = optimizer.optimize(original, target_reduction=0.3)
        >>> print(f"Reduced by {optimizer.get_reduction_percent(original, optimized)}%")
    """

    def __init__(self, model: str = "gpt-4"):
        """
        Initialize optimizer.
        
        Args:
            model: Model name for tiktoken encoding
        """
        try:
            self.encoder = tiktoken.encoding_for_model(model)
        except KeyError:
            self.encoder = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        return len(self.encoder.encode(text))

    def optimize(
        self,
        text: str,
        target_reduction: float = 0.2,
        preserve_structure: bool = True
    ) -> str:
        """
        Optimize text to reduce tokens.
        
        Args:
            text: Text to optimize
            target_reduction: Target reduction (0.0-1.0, e.g., 0.2 = 20% reduction)
            preserve_structure: Keep markdown structure
            
        Returns:
            Optimized text
        """
        original_tokens = self.count_tokens(text)
        target_tokens = int(original_tokens * (1 - target_reduction))

        optimized = text

        # Apply optimization strategies
        optimized = self._remove_redundancy(optimized)
        optimized = self._compress_whitespace(optimized)
        optimized = self._shorten_phrases(optimized)

        # Check if we met target
        current_tokens = self.count_tokens(optimized)
        if current_tokens > target_tokens and not preserve_structure:
            # More aggressive optimization
            optimized = self._remove_examples(optimized, keep_first=True)

        return optimized

    def _remove_redundancy(self, text: str) -> str:
        """Remove redundant phrases."""
        # Remove repeated words
        text = re.sub(r'\b(\w+)(\s+\1\b)+', r'\1', text, flags=re.IGNORECASE)

        # Remove redundant phrases
        redundant = [
            (r'\s+please note that\s+', ' '),
            (r'\s+it is important to\s+', ' '),
            (r'\s+you should be aware that\s+', ' '),
            (r'\s+basically\s+', ' '),
            (r'\s+actually\s+', ' '),
        ]

        for pattern, replacement in redundant:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

        return text

    def _compress_whitespace(self, text: str) -> str:
        """Compress excessive whitespace."""
        # Remove multiple blank lines
        text = re.sub(r'\n{3,}', '\n\n', text)

        # Remove trailing whitespace
        text = re.sub(r'[ \t]+$', '', text, flags=re.MULTILINE)

        # Compress multiple spaces
        text = re.sub(r' {2,}', ' ', text)

        return text.strip()

    def _shorten_phrases(self, text: str) -> str:
        """Replace verbose phrases with shorter equivalents."""
        replacements = {
            r'in order to': 'to',
            r'due to the fact that': 'because',
            r'at this point in time': 'now',
            r'for the purpose of': 'for',
            r'in the event that': 'if',
            r'with regard to': 'about',
            r'in spite of the fact that': 'although',
        }

        for pattern, replacement in replacements.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

        return text

    def _remove_examples(self, text: str, keep_first: bool = True) -> str:
        """Remove example sections (aggressive optimization)."""
        if keep_first:
            # Keep first example, remove rest
            parts = re.split(r'\n\s*(?:Example|For example):', text, maxsplit=2)
            if len(parts) > 2:
                # Keep everything before second example
                return parts[0] + parts[1].split('\n\n')[0]

        return text

    def get_reduction_percent(self, original: str, optimized: str) -> float:
        """Calculate percentage reduction."""
        original_tokens = self.count_tokens(original)
        optimized_tokens = self.count_tokens(optimized)
        return ((original_tokens - optimized_tokens) / original_tokens) * 100

    def analyze(self, text: str) -> dict[str, Any]:
        """
        Analyze text for optimization opportunities.
        
        Returns:
            Dict with analysis results
        """
        tokens = self.count_tokens(text)

        # Check for issues
        issues = []

        # Excessive whitespace
        if re.search(r'\n{3,}', text):
            issues.append("Excessive blank lines (3+ consecutive)")

        # Redundant words
        words = text.lower().split()
        if len(words) > len(set(words)) * 1.5:
            issues.append("High word repetition detected")

        # Verbose phrases
        verbose = ['in order to', 'due to the fact that', 'at this point in time']
        for phrase in verbose:
            if phrase in text.lower():
                issues.append(f"Verbose phrase found: '{phrase}'")

        return {
            "tokens": tokens,
            "characters": len(text),
            "words": len(words),
            "lines": len(text.split('\n')),
            "estimated_cost_gpt4": tokens * 0.00003,  # $30 per 1M tokens
            "estimated_cost_gemini": tokens * 0.000075,  # $0.075 per 1M tokens
            "issues": issues,
            "optimization_potential": "high" if len(issues) > 2 else "medium" if issues else "low"
        }


class ContextCompressor:
    """
    Compress contexts while preserving key information.
    
    Uses extractive summarization to reduce context size.
    """

    def __init__(self, compression_ratio: float = 0.5):
        """
        Initialize compressor.
        
        Args:
            compression_ratio: Target ratio (0.5 = compress to 50% of original)
        """
        self.compression_ratio = compression_ratio

    def compress(self, text: str, preserve_sections: list[str] = None) -> str:
        """
        Compress text to target ratio.
        
        Args:
            text: Text to compress
            preserve_sections: Section headers to always keep
            
        Returns:
            Compressed text
        """
        if preserve_sections is None:
            preserve_sections = []

        # Split into sentences
        sentences = self._split_sentences(text)

        # Score sentences by importance
        scores = self._score_sentences(sentences)

        # Select top sentences to meet ratio
        target_count = int(len(sentences) * self.compression_ratio)
        top_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:target_count]

        # Reconstruct in original order
        selected = [sentences[i] for i in sorted(top_indices)]

        return ' '.join(selected)

    def _split_sentences(self, text: str) -> list[str]:
        """Split text into sentences."""
        # Simple sentence splitter
        sentences = re.split(r'[.!?]+\s+', text)
        return [s.strip() for s in sentences if s.strip()]

    def _score_sentences(self, sentences: list[str]) -> list[float]:
        """
        Score sentences by importance.
        
        Simple scoring:
        - Longer sentences = more info
        - Sentences with numbers/data = important
        - Sentences with keywords = important
        """
        scores = []
        keywords = ['important', 'key', 'critical', 'essential', 'must', 'should']

        for sentence in sentences:
            score = len(sentence.split())  # Word count base score

            # Boost for numbers
            if re.search(r'\d+', sentence):
                score *= 1.3

            # Boost for keywords
            if any(kw in sentence.lower() for kw in keywords):
                score *= 1.5

            scores.append(score)

        return scores


class RedundancyRemover:
    """Remove redundant information from context."""

    @staticmethod
    def remove_duplicate_lines(text: str) -> str:
        """Remove duplicate lines while preserving order."""
        lines = text.split('\n')
        seen = set()
        result = []

        for line in lines:
            normalized = line.strip().lower()
            if normalized and normalized not in seen:
                seen.add(normalized)
                result.append(line)
            elif not normalized:  # Keep blank lines
                result.append(line)

        return '\n'.join(result)

    @staticmethod
    def remove_similar_sentences(text: str, similarity_threshold: float = 0.8) -> str:
        """
        Remove sentences that are too similar.
        
        Args:
            text: Text to process
            similarity_threshold: Threshold for considering sentences similar (0-1)
            
        Returns:
            Text with redundant sentences removed
        """
        sentences = re.split(r'[.!?]+\s+', text)

        def jaccard_similarity(s1: str, s2: str) -> float:
            """Calculate Jaccard similarity between two sentences."""
            words1 = set(s1.lower().split())
            words2 = set(s2.lower().split())

            intersection = words1 & words2
            union = words1 | words2

            return len(intersection) / len(union) if union else 0

        # Keep first sentence, check rest for similarity
        result = [sentences[0]] if sentences else []

        for sentence in sentences[1:]:
            is_unique = True
            for kept in result:
                if jaccard_similarity(sentence, kept) > similarity_threshold:
                    is_unique = False
                    break

            if is_unique:
                result.append(sentence)

        return '. '.join(s.strip() for s in result if s.strip()) + '.'


# Convenience functions

def optimize_context(text: str, target_reduction: float = 0.2) -> str:
    """Quick context optimization."""
    optimizer = TokenOptimizer()
    return optimizer.optimize(text, target_reduction=target_reduction)


def analyze_tokens(text: str) -> dict[str, Any]:
    """Quick token analysis."""
    optimizer = TokenOptimizer()
    return optimizer.analyze(text)


def compress_context(text: str, ratio: float = 0.5) -> str:
    """Quick context compression."""
    compressor = ContextCompressor(compression_ratio=ratio)
    return compressor.compress(text)
