#!/usr/bin/env python3
"""
Test Enhanced Query Engine
Comprehensive test suite for enhanced search capabilities
"""

import pytest
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import json

# Import the modules to test
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from enhanced_query_engine import (
    EnhancedQueryEngine, 
    EnhancedSearchQuery, 
    EnhancedSearchResult,
    _SEMANTIC_CACHE,
    _SCORING_CACHE
)
from database_manager import DatabaseManager
from query_engine import SearchResult

class TestEnhancedSearchQuery:
    """Test EnhancedSearchQuery class"""
    
    def test_default_parameters(self):
        """Test default parameter values"""
        query = EnhancedSearchQuery()
        
        assert query.text == ""
        assert query.use_semantic_search is True
        assert query.semantic_similarity_threshold == 0.7
        assert query.use_ai_scoring is True
        assert query.extract_entities is True
        assert query.use_caching is True
        assert query.parallel_processing is True
        assert query.max_workers == 4
    
    def test_custom_parameters(self):
        """Test custom parameter initialization"""
        query = EnhancedSearchQuery(
            text="test query",
            use_semantic_search=False,
            semantic_similarity_threshold=0.5,
            use_ai_scoring=False,
            extract_entities=False,
            use_caching=False,
            parallel_processing=False,
            max_workers=2
        )
        
        assert query.text == "test query"
        assert query.use_semantic_search is False
        assert query.semantic_similarity_threshold == 0.5
        assert query.use_ai_scoring is False
        assert query.extract_entities is False
        assert query.use_caching is False
        assert query.parallel_processing is False
        assert query.max_workers == 2

class TestEnhancedSearchResult:
    """Test EnhancedSearchResult class"""
    
    def test_default_enhanced_fields(self):
        """Test enhanced result fields"""
        result = EnhancedSearchResult(
            file_id=1,
            file_path="/test/path",
            file_name="test.md",
            file_extension=".md",
            file_size=1024,
            modified_at="2025-01-01T00:00:00Z",
            content_preview="Test content",
            relevance_score=0.8,
            match_highlights=[],
            content_type="text",
            line_count=10,
            word_count=100
        )
        
        assert result.semantic_score == 0.0
        assert result.context_relevance == 0.0
        assert result.content_quality_score == 0.0
        assert result.freshness_score == 0.0
        assert result.popularity_score == 0.0
        assert result.detected_entities == []
        assert result.sentiment_score == 0.0
        assert result.readability_score == 0.0
        assert result.contextual_snippets == []
        assert result.related_topics == []
        assert result.processing_time == 0.0
        assert result.cache_hit is False

@pytest.fixture
def mock_database_manager():
    """Create a mock database manager"""
    db_manager = Mock(spec=DatabaseManager)
    db_manager.connection = Mock()
    db_manager.connection.cursor.return_value.fetchall.return_value = [
        {
            'id': 1,
            'file_path': '/test/file1.md',
            'file_name': 'file1.md',
            'file_extension': '.md',
            'file_size': 1024,
            'modified_at': '2025-01-01T00:00:00Z',
            'content_preview': 'This is test content about Context7 framework',
            'line_count': 50,
            'word_count': 200
        },
        {
            'id': 2,
            'file_path': '/test/file2.py',
            'file_name': 'file2.py',
            'file_extension': '.py',
            'file_size': 2048,
            'modified_at': '2025-01-02T00:00:00Z',
            'content_preview': 'def test_function(): pass',
            'line_count': 25,
            'word_count': 100
        }
    ]
    return db_manager

@pytest.fixture
def enhanced_query_engine(mock_database_manager):
    """Create an enhanced query engine with mock database"""
    return EnhancedQueryEngine(mock_database_manager)

class TestEnhancedQueryEngine:
    """Test EnhancedQueryEngine class"""
    
    def test_initialization(self, enhanced_query_engine):
        """Test engine initialization"""
        engine = enhanced_query_engine
        
        assert engine.query_count == 0
        assert engine.total_query_time == 0.0
        assert engine.cache_hits == 0
        assert engine.cache_misses == 0
        assert hasattr(engine, 'ml_available')
    
    def test_get_cache_key(self, enhanced_query_engine):
        """Test cache key generation"""
        query = EnhancedSearchQuery(
            text="test query",
            use_semantic_search=True,
            semantic_similarity_threshold=0.7
        )
        
        cache_key = enhanced_query_engine._get_cache_key(query)
        
        assert isinstance(cache_key, str)
        assert len(cache_key) == 32  # MD5 hash length
        
        # Same query should produce same cache key
        cache_key2 = enhanced_query_engine._get_cache_key(query)
        assert cache_key == cache_key2
        
        # Different query should produce different cache key
        query2 = EnhancedSearchQuery(text="different query")
        cache_key3 = enhanced_query_engine._get_cache_key(query2)
        assert cache_key != cache_key3
    
    def test_clean_cache(self, enhanced_query_engine):
        """Test cache cleaning functionality"""
        global _SEMANTIC_CACHE, _SCORING_CACHE
        
        # Fill cache beyond limit
        _SEMANTIC_CACHE.clear()
        for i in range(1100):  # Beyond _CACHE_MAX_SIZE = 1000
            _SEMANTIC_CACHE[f"key_{i}"] = f"value_{i}"
        
        enhanced_query_engine._clean_cache()
        
        assert len(_SEMANTIC_CACHE) <= 500  # Should be reduced to half
    
    def test_convert_to_enhanced_result(self, enhanced_query_engine):
        """Test basic result conversion"""
        basic_result = SearchResult(
            file_id=1,
            file_path="/test/file.md",
            file_name="file.md",
            file_extension=".md",
            file_size=1024,
            modified_at="2025-01-01T00:00:00Z",
            content_preview="Test content",
            relevance_score=0.8,
            match_highlights=[],
            content_type="text",
            line_count=10,
            word_count=100
        )
        
        enhanced_result = enhanced_query_engine._convert_to_enhanced_result(basic_result)
        
        assert isinstance(enhanced_result, EnhancedSearchResult)
        assert enhanced_result.file_id == 1
        assert enhanced_result.file_path == "/test/file.md"
        assert enhanced_result.semantic_score == 0.0  # Default enhanced fields
    
    def test_calculate_content_quality(self, enhanced_query_engine):
        """Test content quality calculation"""
        
        # High quality content
        high_quality_content = """
        # Main Title
        
        This is a well-structured document with multiple paragraphs.
        It contains code examples like `print("hello")` and references to 
        https://example.com for additional information.
        
        ```python
        def example_function():
            return "This is code"
        ```
        
        The document has good sentence structure and appropriate length.
        """
        
        score = enhanced_query_engine._calculate_content_quality_impl(high_quality_content)
        assert score > 0.5  # Should be high quality
        
        # Low quality content
        low_quality_content = "short text"
        score = enhanced_query_engine._calculate_content_quality_impl(low_quality_content)
        assert score < 0.5  # Should be low quality
    
    def test_calculate_freshness_score(self, enhanced_query_engine):
        """Test freshness score calculation"""
        
        # Create a mock result with recent date
        recent_result = EnhancedSearchResult(
            file_id=1,
            file_path="/test/file.md",
            file_name="file.md",
            file_extension=".md",
            file_size=1024,
            modified_at=datetime.now().isoformat(),
            content_preview="Test content",
            relevance_score=0.8,
            match_highlights=[],
            content_type="text",
            line_count=10,
            word_count=100
        )
        
        score = enhanced_query_engine._calculate_freshness_score(recent_result)
        assert score >= 0.8  # Recent files should have high freshness
        
        # Old result
        old_result = EnhancedSearchResult(
            file_id=2,
            file_path="/test/old_file.md",
            file_name="old_file.md",
            file_extension=".md",
            file_size=1024,
            modified_at=(datetime.now() - timedelta(days=400)).isoformat(),
            content_preview="Old content",
            relevance_score=0.8,
            match_highlights=[],
            content_type="text",
            line_count=10,
            word_count=100
        )
        
        score = enhanced_query_engine._calculate_freshness_score(old_result)
        assert score <= 0.2  # Old files should have low freshness
    
    def test_calculate_popularity_score(self, enhanced_query_engine):
        """Test popularity score calculation"""
        
        # README file should have high popularity
        readme_result = EnhancedSearchResult(
            file_id=1,
            file_path="/test/README.md",
            file_name="README.md",
            file_extension=".md",
            file_size=1024,
            modified_at="2025-01-01T00:00:00Z",
            content_preview="Test content",
            relevance_score=0.8,
            match_highlights=[],
            content_type="text",
            line_count=10,
            word_count=100
        )
        
        score = enhanced_query_engine._calculate_popularity_score(readme_result)
        assert score > 0.5  # README should have high popularity
        
        # Random file should have lower popularity
        random_result = EnhancedSearchResult(
            file_id=2,
            file_path="/test/random.xyz",
            file_name="random.xyz",
            file_extension=".xyz",
            file_size=1024,
            modified_at="2025-01-01T00:00:00Z",
            content_preview="Test content",
            relevance_score=0.8,
            match_highlights=[],
            content_type="text",
            line_count=10,
            word_count=100
        )
        
        score = enhanced_query_engine._calculate_popularity_score(random_result)
        assert score <= 0.5  # Random files should have lower popularity
    
    def test_calculate_context_relevance(self, enhanced_query_engine):
        """Test context relevance calculation"""
        
        query = EnhancedSearchQuery(text="Context7 framework development")
        
        # Highly relevant result
        relevant_result = EnhancedSearchResult(
            file_id=1,
            file_path="/test/file.md",
            file_name="file.md",
            file_extension=".md",
            file_size=1024,
            modified_at="2025-01-01T00:00:00Z",
            content_preview="This document explains Context7 framework development best practices",
            relevance_score=0.8,
            match_highlights=[],
            content_type="text",
            line_count=10,
            word_count=100
        )
        
        score = enhanced_query_engine._calculate_context_relevance(relevant_result, query)
        assert score > 0.3  # Should have high relevance
        
        # Irrelevant result
        irrelevant_result = EnhancedSearchResult(
            file_id=2,
            file_path="/test/file2.md",
            file_name="file2.md",
            file_extension=".md",
            file_size=1024,
            modified_at="2025-01-01T00:00:00Z",
            content_preview="This is about cooking recipes and nothing else",
            relevance_score=0.8,
            match_highlights=[],
            content_type="text",
            line_count=10,
            word_count=100
        )
        
        score = enhanced_query_engine._calculate_context_relevance(irrelevant_result, query)
        assert score < 0.3  # Should have low relevance
    
    def test_extract_entities(self, enhanced_query_engine):
        """Test entity extraction"""
        
        content = """
        This document mentions Context7, Django, and Python.
        It was created on 2025-01-01 and updated on 12/15/2024.
        The author is John Smith and the project is OpenSource.
        """
        
        entities = enhanced_query_engine._extract_entities(content)
        
        assert len(entities) > 0
        assert any("Context7" in str(entity) for entity in entities)
        assert any("Django" in str(entity) for entity in entities)
        assert any("Python" in str(entity) for entity in entities)
    
    def test_calculate_readability(self, enhanced_query_engine):
        """Test readability score calculation"""
        
        # Simple, readable text
        readable_text = """
        This is a simple sentence. It has good structure.
        The text is easy to read and understand.
        """
        
        score = enhanced_query_engine._calculate_readability(readable_text)
        assert 0.0 <= score <= 1.0
        
        # Complex, less readable text
        complex_text = """
        Extraordinarily complicated terminology with sesquipedalian vocabulary 
        characteristics demonstrates inefficiently constructed communication 
        methodologies requiring comprehensive comprehension capabilities.
        """
        
        complex_score = enhanced_query_engine._calculate_readability(complex_text)
        assert complex_score < score  # Should be less readable
    
    def test_analyze_query_intent(self, enhanced_query_engine):
        """Test query intent analysis"""
        
        # Explain intent
        explain_queries = [
            "What is Context7?",
            "How does semantic search work?",
            "Explain the architecture",
            "Why use this framework?"
        ]
        
        for query in explain_queries:
            intent = enhanced_query_engine.analyze_query_intent(query)
            assert intent == "explain"
        
        # Find intent
        find_queries = [
            "Find all documentation",
            "Search for examples",
            "Where is the configuration?",
            "Locate the API reference"
        ]
        
        for query in find_queries:
            intent = enhanced_query_engine.analyze_query_intent(query)
            assert intent == "find"
        
        # List intent
        list_queries = [
            "List all features",
            "Show me every component",
            "All available options"
        ]
        
        for query in list_queries:
            intent = enhanced_query_engine.analyze_query_intent(query)
            assert intent == "list"
        
        # Compare intent
        compare_queries = [
            "Compare Context7 vs Django",
            "Difference between options",
            "A versus B"
        ]
        
        for query in compare_queries:
            intent = enhanced_query_engine.analyze_query_intent(query)
            assert intent == "compare"
    
    def test_get_performance_stats(self, enhanced_query_engine):
        """Test performance statistics"""
        
        # Initialize with some fake data
        enhanced_query_engine.query_count = 10
        enhanced_query_engine.total_query_time = 5.0
        enhanced_query_engine.cache_hits = 7
        enhanced_query_engine.cache_misses = 3
        
        stats = enhanced_query_engine.get_performance_stats()
        
        assert stats['query_count'] == 10
        assert stats['total_query_time'] == 5.0
        assert stats['average_query_time'] == 0.5
        assert stats['cache_hits'] == 7
        assert stats['cache_misses'] == 3
        assert stats['cache_hit_rate'] == 0.7
        assert 'cache_size' in stats
        assert 'ml_available' in stats
    
    def test_clear_cache(self, enhanced_query_engine):
        """Test cache clearing"""
        
        global _SEMANTIC_CACHE, _SCORING_CACHE
        
        # Add some data to cache
        _SEMANTIC_CACHE['test_key'] = 'test_value'
        _SCORING_CACHE['test_key'] = 'test_value'
        
        enhanced_query_engine.cache_hits = 5
        enhanced_query_engine.cache_misses = 3
        
        enhanced_query_engine.clear_cache()
        
        assert len(_SEMANTIC_CACHE) == 0
        assert len(_SCORING_CACHE) == 0
        assert enhanced_query_engine.cache_hits == 0
        assert enhanced_query_engine.cache_misses == 0
    
    @patch('enhanced_query_engine.ML_AVAILABLE', False)
    def test_search_without_ml(self, enhanced_query_engine):
        """Test search functionality without ML libraries"""
        
        query = EnhancedSearchQuery(text="test query")
        
        # Mock the parent search method
        with patch.object(enhanced_query_engine, 'search', wraps=enhanced_query_engine.search) as mock_search:
            with patch.object(enhanced_query_engine.__class__.__bases__[0], 'search') as mock_parent_search:
                mock_parent_search.return_value = []
                
                results = enhanced_query_engine.search(query)
                
                assert isinstance(results, list)
                mock_parent_search.assert_called_once()
    
    def test_search_with_caching(self, enhanced_query_engine):
        """Test search with caching enabled"""
        
        query = EnhancedSearchQuery(text="test query", use_caching=True)
        
        # Mock the parent search method
        with patch.object(enhanced_query_engine.__class__.__bases__[0], 'search') as mock_parent_search:
            mock_parent_search.return_value = []
            
            # First search - should miss cache
            results1 = enhanced_query_engine.search(query)
            assert enhanced_query_engine.cache_misses >= 1
            
            # Second search - should hit cache
            results2 = enhanced_query_engine.search(query)
            
            # Results should be the same
            assert len(results1) == len(results2)

class TestIntegration:
    """Integration tests for enhanced query engine"""
    
    def test_full_search_workflow(self, enhanced_query_engine):
        """Test complete search workflow"""
        
        query = EnhancedSearchQuery(
            text="Context7 framework",
            use_semantic_search=True,
            use_ai_scoring=True,
            extract_entities=True,
            use_caching=True
        )
        
        # Mock the parent search method to return some results
        with patch.object(enhanced_query_engine.__class__.__bases__[0], 'search') as mock_parent_search:
            mock_parent_search.return_value = [
                SearchResult(
                    file_id=1,
                    file_path="/test/file.md",
                    file_name="file.md",
                    file_extension=".md",
                    file_size=1024,
                    modified_at="2025-01-01T00:00:00Z",
                    content_preview="Context7 framework documentation",
                    relevance_score=0.8,
                    match_highlights=[],
                    content_type="text",
                    line_count=10,
                    word_count=100
                )
            ]
            
            results = enhanced_query_engine.search(query)
            
            assert len(results) > 0
            assert isinstance(results[0], EnhancedSearchResult)
            assert results[0].file_name == "file.md"
            assert enhanced_query_engine.query_count > 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 