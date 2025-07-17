#!/usr/bin/env python3
"""
Enhanced Query Engine - Semantic search ve AI-powered scoring sistemi
Gelişmiş arama algoritmaları ile güçlendirilmiş query engine
Performance optimized with caching and parallel processing
"""

import re
import json
import math
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from collections import defaultdict, Counter
import hashlib
import pickle
import time
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed

# AI/ML imports
try:
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    from sentence_transformers import SentenceTransformer
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.stem import PorterStemmer

    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("⚠️  ML libraries not available. Running in basic mode.")

from colorama import init, Fore, Style

# Fixed import - using relative import
try:
    from .query_engine import QueryEngine, SearchQuery, SearchResult
except ImportError:
    # Fallback for when running as main module
    from query_engine import QueryEngine, SearchQuery, SearchResult

# Colorama initialize
init()

# Performance cache
_SEMANTIC_CACHE = {}
_SCORING_CACHE = {}
_CACHE_MAX_SIZE = 1000


@dataclass
class EnhancedSearchQuery(SearchQuery):
    """Gelişmiş arama sorgusu veri yapısı"""

    # Semantic search parameters
    use_semantic_search: bool = True
    semantic_similarity_threshold: float = 0.7

    # AI scoring parameters
    use_ai_scoring: bool = True
    context_window: int = 100  # words around matches

    # Natural language processing
    query_intent: Optional[str] = None  # "find", "explain", "list", "compare"
    extract_entities: bool = True

    # Advanced filtering
    content_quality_filter: bool = False
    min_word_count: Optional[int] = None
    language_filter: Optional[str] = None

    # Performance settings
    use_caching: bool = True
    parallel_processing: bool = True
    max_workers: int = 4


@dataclass
class EnhancedSearchResult(SearchResult):
    """Gelişmiş arama sonucu veri yapısı"""

    # Semantic search scores
    semantic_score: float = 0.0
    context_relevance: float = 0.0

    # AI scoring components
    content_quality_score: float = 0.0
    freshness_score: float = 0.0
    popularity_score: float = 0.0

    # NLP analysis
    detected_entities: List[str] = field(default_factory=list)
    sentiment_score: float = 0.0
    readability_score: float = 0.0

    # Enhanced context
    contextual_snippets: List[str] = field(default_factory=list)
    related_topics: List[str] = field(default_factory=list)

    # Performance metrics
    processing_time: float = 0.0
    cache_hit: bool = False


class EnhancedQueryEngine(QueryEngine):
    """Gelişmiş query engine - Semantic search ve AI-powered scoring"""

    def __init__(self, database_manager):
        super().__init__(database_manager)

        self.ml_available = ML_AVAILABLE
        self.sentence_model = None
        self.tfidf_vectorizer = None
        self.document_vectors = None
        self.stemmer = PorterStemmer() if ML_AVAILABLE else None

        # Performance tracking
        self.query_count = 0
        self.total_query_time = 0.0
        self.cache_hits = 0
        self.cache_misses = 0

        # Download NLTK data if available
        if ML_AVAILABLE:
            self._initialize_nltk()
            self._initialize_models()

    def _initialize_nltk(self):
        """Initialize NLTK data"""
        try:
            nltk.download("punkt", quiet=True)
            nltk.download("stopwords", quiet=True)
            nltk.download("averaged_perceptron_tagger", quiet=True)
            nltk.download("wordnet", quiet=True)
        except Exception as e:
            logging.warning(f"NLTK initialization failed: {e}")

    def _initialize_models(self):
        """Initialize ML models for semantic search"""
        if not self.ml_available:
            return

        try:
            # Load sentence transformer model (lightweight model for faster processing)
            self.sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
            logging.info("✅ Sentence transformer model loaded")

            # Initialize TF-IDF vectorizer
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=5000,
                stop_words="english",
                ngram_range=(1, 2),
                max_df=0.8,
                min_df=2,
            )
            logging.info("✅ TF-IDF vectorizer initialized")

        except Exception as e:
            logging.error(f"❌ Model initialization failed: {e}")
            self.ml_available = False

    def _get_cache_key(self, query: EnhancedSearchQuery) -> str:
        """Generate cache key for query"""
        key_data = {
            "text": query.text,
            "use_semantic_search": query.use_semantic_search,
            "semantic_similarity_threshold": query.semantic_similarity_threshold,
            "use_ai_scoring": query.use_ai_scoring,
            "extract_entities": query.extract_entities,
        }
        return hashlib.md5(json.dumps(key_data, sort_keys=True).encode()).hexdigest()

    def _clean_cache(self):
        """Clean cache if it gets too large"""
        global _SEMANTIC_CACHE, _SCORING_CACHE

        if len(_SEMANTIC_CACHE) > _CACHE_MAX_SIZE:
            # Remove oldest entries
            _SEMANTIC_CACHE = dict(
                list(_SEMANTIC_CACHE.items())[-_CACHE_MAX_SIZE // 2 :]
            )

        if len(_SCORING_CACHE) > _CACHE_MAX_SIZE:
            _SCORING_CACHE = dict(list(_SCORING_CACHE.items())[-_CACHE_MAX_SIZE // 2 :])

    def search(self, query: EnhancedSearchQuery) -> List[EnhancedSearchResult]:
        """Gelişmiş arama işlemi - Performance optimized"""

        start_time = time.time()
        self.query_count += 1

        # Check cache first
        cache_key = self._get_cache_key(query) if query.use_caching else None
        if cache_key and cache_key in _SEMANTIC_CACHE:
            cached_results = _SEMANTIC_CACHE[cache_key]
            for result in cached_results:
                result.cache_hit = True
            self.cache_hits += 1
            return cached_results

        # Basic search first
        basic_results = super().search(query)

        # Convert to enhanced results
        enhanced_results = [
            self._convert_to_enhanced_result(result) for result in basic_results
        ]

        if not self.ml_available or not query.use_semantic_search:
            processing_time = time.time() - start_time
            self.total_query_time += processing_time
            for result in enhanced_results:
                result.processing_time = processing_time
            return enhanced_results

        # Apply semantic search enhancements
        try:
            if query.parallel_processing and len(enhanced_results) > 10:
                enhanced_results = self._parallel_enhance_results(
                    enhanced_results, query
                )
            else:
                enhanced_results = self._sequential_enhance_results(
                    enhanced_results, query
                )

        except Exception as e:
            logging.error(f"❌ Enhanced search failed: {e}")
            # Fall back to basic results

        # Sort by enhanced relevance
        enhanced_results = self._sort_enhanced_results(enhanced_results, query)

        # Cache results
        if query.use_caching and cache_key:
            _SEMANTIC_CACHE[cache_key] = enhanced_results[: query.limit]
            self._clean_cache()
            self.cache_misses += 1

        # Update performance metrics
        processing_time = time.time() - start_time
        self.total_query_time += processing_time
        for result in enhanced_results:
            result.processing_time = processing_time

        return enhanced_results[: query.limit]

    def _parallel_enhance_results(
        self, results: List[EnhancedSearchResult], query: EnhancedSearchQuery
    ) -> List[EnhancedSearchResult]:
        """Parallel processing for large result sets"""

        def process_result(result):
            result = self._apply_semantic_search_single(result, query)
            result = self._apply_ai_scoring_single(result, query)
            result = self._extract_contextual_information_single(result, query)
            return result

        with ThreadPoolExecutor(max_workers=query.max_workers) as executor:
            future_to_result = {
                executor.submit(process_result, result): result for result in results
            }

            enhanced_results = []
            for future in as_completed(future_to_result):
                try:
                    enhanced_result = future.result()
                    enhanced_results.append(enhanced_result)
                except Exception as e:
                    logging.error(f"Parallel processing error: {e}")
                    # Add original result if enhancement fails
                    enhanced_results.append(future_to_result[future])

        return enhanced_results

    def _sequential_enhance_results(
        self, results: List[EnhancedSearchResult], query: EnhancedSearchQuery
    ) -> List[EnhancedSearchResult]:
        """Sequential processing for smaller result sets"""

        results = self._apply_semantic_search(results, query)
        results = self._apply_ai_scoring(results, query)
        results = self._extract_contextual_information(results, query)

        return results

    @lru_cache(maxsize=256)
    def _calculate_content_quality_cached(
        self, content_hash: str, content: str
    ) -> float:
        """Cached content quality calculation"""
        return self._calculate_content_quality_impl(content)

    def _calculate_content_quality_impl(self, content: str) -> float:
        """Implementation of content quality calculation"""

        score = 0.0

        # Word count factor
        word_count = len(content.split())
        if word_count > 50:
            score += 0.3
        if word_count > 200:
            score += 0.2

        # Structure indicators
        if any(
            indicator in content.lower() for indicator in ["#", "##", "###", "####"]
        ):
            score += 0.2  # Has headings

        if any(indicator in content for indicator in ["```", "`", "code"]):
            score += 0.1  # Has code examples

        if any(indicator in content for indicator in ["http", "https", "[", "]"]):
            score += 0.1  # Has links or references

        # Language quality (simple heuristic)
        sentences = content.split(".")
        if len(sentences) > 3:
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(
                sentences
            )
            if 10 <= avg_sentence_length <= 25:  # Good sentence length
                score += 0.1

        return min(score, 1.0)

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""

        avg_query_time = (
            self.total_query_time / self.query_count if self.query_count > 0 else 0
        )
        cache_hit_rate = (
            self.cache_hits / (self.cache_hits + self.cache_misses)
            if (self.cache_hits + self.cache_misses) > 0
            else 0
        )

        return {
            "query_count": self.query_count,
            "total_query_time": self.total_query_time,
            "average_query_time": avg_query_time,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "cache_hit_rate": cache_hit_rate,
            "cache_size": len(_SEMANTIC_CACHE),
            "ml_available": self.ml_available,
        }

    def clear_cache(self):
        """Clear all caches"""
        global _SEMANTIC_CACHE, _SCORING_CACHE
        _SEMANTIC_CACHE.clear()
        _SCORING_CACHE.clear()
        self.cache_hits = 0
        self.cache_misses = 0
        logging.info("✅ Cache cleared")

    def _convert_to_enhanced_result(self, result: SearchResult) -> EnhancedSearchResult:
        """Convert basic result to enhanced result"""
        return EnhancedSearchResult(
            file_id=result.file_id,
            file_path=result.file_path,
            file_name=result.file_name,
            file_extension=result.file_extension,
            file_size=result.file_size,
            modified_at=result.modified_at,
            content_preview=result.content_preview,
            relevance_score=result.relevance_score,
            match_highlights=result.match_highlights,
            content_type=result.content_type,
            line_count=result.line_count,
            word_count=result.word_count,
        )

    def _apply_semantic_search(
        self, results: List[EnhancedSearchResult], query: EnhancedSearchQuery
    ) -> List[EnhancedSearchResult]:
        """Apply semantic search scoring"""

        if not query.text:
            return results

        try:
            # Generate query embedding
            query_embedding = self.sentence_model.encode([query.text])

            # Generate document embeddings for content previews
            documents = [result.content_preview for result in results]
            document_embeddings = self.sentence_model.encode(documents)

            # Calculate semantic similarities
            similarities = cosine_similarity(query_embedding, document_embeddings)[0]

            # Update results with semantic scores
            for i, result in enumerate(results):
                result.semantic_score = float(similarities[i])

                # Boost relevance score if semantic similarity is high
                if result.semantic_score > query.semantic_similarity_threshold:
                    result.relevance_score *= 1.0 + result.semantic_score

            logging.info(f"✅ Semantic search applied to {len(results)} results")

        except Exception as e:
            logging.error(f"❌ Semantic search failed: {e}")

        return results

    def _apply_ai_scoring(
        self, results: List[EnhancedSearchResult], query: EnhancedSearchQuery
    ) -> List[EnhancedSearchResult]:
        """Apply AI-powered scoring"""

        for result in results:
            try:
                # Content quality scoring
                result.content_quality_score = self._calculate_content_quality(result)

                # Freshness scoring
                result.freshness_score = self._calculate_freshness_score(result)

                # Popularity scoring (based on file access patterns)
                result.popularity_score = self._calculate_popularity_score(result)

                # Context relevance scoring
                result.context_relevance = self._calculate_context_relevance(
                    result, query
                )

                # Combine scores into enhanced relevance
                ai_boost = (
                    result.content_quality_score * 0.3
                    + result.freshness_score * 0.2
                    + result.popularity_score * 0.2
                    + result.context_relevance * 0.3
                )

                result.relevance_score *= 1.0 + ai_boost

            except Exception as e:
                logging.warning(f"AI scoring failed for {result.file_name}: {e}")

        return results

    def _calculate_content_quality(self, result: EnhancedSearchResult) -> float:
        """Calculate content quality score"""

        score = 0.0
        content = result.content_preview

        # Word count factor
        if result.word_count > 50:
            score += 0.3
        if result.word_count > 200:
            score += 0.2

        # Structure indicators
        if any(
            indicator in content.lower() for indicator in ["#", "##", "###", "####"]
        ):
            score += 0.2  # Has headings

        if any(indicator in content for indicator in ["```", "`", "code"]):
            score += 0.1  # Has code examples

        if any(indicator in content for indicator in ["http", "https", "[", "]"]):
            score += 0.1  # Has links or references

        # Language quality (simple heuristic)
        sentences = content.split(".")
        if len(sentences) > 3:
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(
                sentences
            )
            if 10 <= avg_sentence_length <= 25:  # Good sentence length
                score += 0.1

        return min(score, 1.0)

    def _calculate_freshness_score(self, result: EnhancedSearchResult) -> float:
        """Calculate freshness score based on modification date"""

        try:
            modified_date = datetime.fromisoformat(
                result.modified_at.replace("Z", "+00:00")
            )
            days_ago = (datetime.now() - modified_date.replace(tzinfo=None)).days

            # Fresher files get higher scores
            if days_ago <= 1:
                return 1.0
            elif days_ago <= 7:
                return 0.8
            elif days_ago <= 30:
                return 0.6
            elif days_ago <= 90:
                return 0.4
            elif days_ago <= 365:
                return 0.2
            else:
                return 0.1

        except Exception:
            return 0.5  # Default score if date parsing fails

    def _calculate_popularity_score(self, result: EnhancedSearchResult) -> float:
        """Calculate popularity score (placeholder for future implementation)"""

        # For now, use simple heuristics
        score = 0.0

        # Common important files
        important_keywords = ["readme", "index", "main", "config", "setup", "guide"]
        for keyword in important_keywords:
            if keyword in result.file_name.lower():
                score += 0.2

        # File type popularity
        popular_extensions = {
            ".md": 0.8,
            ".txt": 0.6,
            ".py": 0.7,
            ".js": 0.6,
            ".json": 0.5,
        }
        score += popular_extensions.get(result.file_extension.lower(), 0.3)

        return min(score, 1.0)

    def _calculate_context_relevance(
        self, result: EnhancedSearchResult, query: EnhancedSearchQuery
    ) -> float:
        """Calculate contextual relevance"""

        if not query.text:
            return 0.5

        # Simple TF-IDF like scoring for context
        query_terms = set(query.text.lower().split())
        content_terms = set(result.content_preview.lower().split())

        # Jaccard similarity
        intersection = len(query_terms.intersection(content_terms))
        union = len(query_terms.union(content_terms))

        if union == 0:
            return 0.0

        return intersection / union

    def _extract_contextual_information(
        self, results: List[EnhancedSearchResult], query: EnhancedSearchQuery
    ) -> List[EnhancedSearchResult]:
        """Extract contextual information and snippets"""

        for result in results:
            try:
                # Extract better contextual snippets
                result.contextual_snippets = self._extract_relevant_snippets(
                    result, query
                )

                # Extract entities if enabled
                if query.extract_entities:
                    result.detected_entities = self._extract_entities(
                        result.content_preview
                    )

                # Calculate readability score
                result.readability_score = self._calculate_readability(
                    result.content_preview
                )

            except Exception as e:
                logging.warning(
                    f"Context extraction failed for {result.file_name}: {e}"
                )

        return results

    def _extract_relevant_snippets(
        self, result: EnhancedSearchResult, query: EnhancedSearchQuery
    ) -> List[str]:
        """Extract relevant text snippets around matches"""

        if not query.text:
            return [result.content_preview[:200]]

        snippets = []
        content = result.content_preview
        query_terms = query.text.lower().split()

        sentences = sent_tokenize(content) if self.ml_available else content.split(".")

        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(term in sentence_lower for term in query_terms):
                # Add context around the sentence
                snippet = sentence.strip()
                if len(snippet) > 50:
                    snippets.append(snippet[:300])

        return snippets[:3]  # Return top 3 snippets

    def _extract_entities(self, content: str) -> List[str]:
        """Extract named entities from content (simplified)"""

        # Simple entity extraction (capitalized words, dates, etc.)
        entities = []

        # Find capitalized words (potential proper nouns)
        words = content.split()
        for word in words:
            if len(word) > 2 and word[0].isupper() and word.isalpha():
                entities.append(word)

        # Find dates
        date_patterns = [
            r"\d{4}-\d{2}-\d{2}",
            r"\d{2}/\d{2}/\d{4}",
            r"\w+\s+\d{1,2},\s+\d{4}",
        ]

        for pattern in date_patterns:
            matches = re.findall(pattern, content)
            entities.extend(matches)

        return list(set(entities))[:10]  # Return unique entities, max 10

    def _calculate_readability(self, content: str) -> float:
        """Calculate readability score (simplified Flesch reading ease)"""

        if not content:
            return 0.0

        # Count sentences, words, syllables
        sentences = (
            len(sent_tokenize(content))
            if self.ml_available
            else len(content.split("."))
        )
        words = len(content.split())

        if sentences == 0 or words == 0:
            return 0.0

        # Simplified syllable counting
        syllables = sum(
            max(1, len([c for c in word if c.lower() in "aeiou"]))
            for word in content.split()
        )

        # Simplified Flesch Reading Ease
        if sentences > 0 and words > 0:
            score = (
                206.835 - (1.015 * (words / sentences)) - (84.6 * (syllables / words))
            )
            return max(0.0, min(100.0, score)) / 100.0  # Normalize to 0-1

        return 0.5

    def _sort_enhanced_results(
        self, results: List[EnhancedSearchResult], query: EnhancedSearchQuery
    ) -> List[EnhancedSearchResult]:
        """Sort results using enhanced scoring"""

        if query.sort_by == "relevance":
            # Enhanced relevance sorting
            return sorted(
                results,
                key=lambda x: (
                    x.relevance_score * 0.4
                    + x.semantic_score * 0.3
                    + x.content_quality_score * 0.2
                    + x.freshness_score * 0.1
                ),
                reverse=True,
            )
        else:
            # Use parent class sorting for other criteria
            return super()._sort_results(results, query)

    def analyze_query_intent(self, query_text: str) -> str:
        """Analyze query intent"""

        query_lower = query_text.lower()

        if any(
            word in query_lower
            for word in ["what", "how", "why", "explain", "describe"]
        ):
            return "explain"
        elif any(word in query_lower for word in ["find", "search", "locate", "where"]):
            return "find"
        elif any(word in query_lower for word in ["list", "show", "all", "every"]):
            return "list"
        elif any(
            word in query_lower for word in ["compare", "difference", "vs", "versus"]
        ):
            return "compare"
        else:
            return "find"  # Default intent

    def get_semantic_suggestions(self, query_text: str, limit: int = 5) -> List[str]:
        """Get semantic query suggestions"""

        if not self.ml_available or not query_text:
            return []

        try:
            # This would typically use a pre-built index of common queries
            # For now, return some enhanced suggestions based on query analysis

            intent = self.analyze_query_intent(query_text)

            base_suggestions = []
            if intent == "explain":
                base_suggestions = [
                    f"How does {query_text} work?",
                    f"What is {query_text}?",
                    f"Explain {query_text} in detail",
                ]
            elif intent == "find":
                base_suggestions = [
                    f"Find all {query_text}",
                    f"Search for {query_text} examples",
                    f"Locate {query_text} documentation",
                ]

            return base_suggestions[:limit]

        except Exception as e:
            logging.error(f"Semantic suggestions failed: {e}")
            return []


def main():
    """Test the enhanced query engine"""

    # Simple test
    print(f"{Fore.GREEN}🚀 Enhanced Query Engine Test{Style.RESET_ALL}")
    print(f"ML Available: {ML_AVAILABLE}")

    if ML_AVAILABLE:
        print("✅ All ML features available")
    else:
        print("⚠️  Running in basic mode")


if __name__ == "__main__":
    main()
