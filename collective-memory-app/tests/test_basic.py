#!/usr/bin/env python3
"""
Collective Memory Basic Tests
"""

import pytest
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cursor_reader import CursorDatabaseReader
from context_collector import ContextCollector
from query_builder import QueryBuilder
from trigger_parser import TriggerParser

class TestCursorDatabaseReader:
    """Cursor Database Reader tests"""
    
    def test_initialization(self):
        """Test reader initialization"""
        reader = CursorDatabaseReader()
        assert reader is not None
        assert hasattr(reader, 'cursor_db_paths')
        
    def test_cursor_available(self):
        """Test cursor availability check"""
        reader = CursorDatabaseReader()
        # This should not raise an exception
        result = reader.is_cursor_available()
        assert isinstance(result, bool)

class TestContextCollector:
    """Context Collector tests"""
    
    def test_initialization(self):
        """Test collector initialization"""
        collector = ContextCollector()
        assert collector is not None
        assert hasattr(collector, 'supported_doc_extensions')
        assert hasattr(collector, 'supported_code_extensions')
        
    def test_fetch_rules_empty_project(self, tmp_path):
        """Test rules fetching with empty project"""
        collector = ContextCollector()
        rules_data = collector.fetch_rules(tmp_path)
        
        assert 'found' in rules_data
        assert rules_data['found'] == False
        assert 'rules' in rules_data
        assert 'source_files' in rules_data
        
    def test_fetch_rules_with_cursorrules(self, tmp_path):
        """Test rules fetching with .cursorrules file"""
        # Create test .cursorrules file
        cursorrules_file = tmp_path / ".cursorrules"
        cursorrules_file.write_text("Always use TypeScript")
        
        collector = ContextCollector()
        rules_data = collector.fetch_rules(tmp_path)
        
        assert rules_data['found'] == True
        assert len(rules_data['rules']) == 1
        assert rules_data['rules'][0]['type'] == 'legacy_cursorrules'
        assert "TypeScript" in rules_data['rules'][0]['content']

class TestQueryBuilder:
    """Query Builder tests"""
    
    def test_initialization(self):
        """Test builder initialization"""
        builder = QueryBuilder()
        assert builder is not None
        assert hasattr(builder, 'query_templates')
        
    def test_build_query_basic(self):
        """Test basic query building"""
        builder = QueryBuilder()
        
        context_data = {
            'project_path': '/test/project',
            'user_request': 'Test request',
            'sources': {
                'rules': {'found': False, 'rules': []},
                'chats': {'found': False, 'chats': []},
                'docs': {'found': False, 'docs': []}
            }
        }
        
        query = builder.build_query(context_data)
        
        assert isinstance(query, str)
        assert len(query) > 0
        assert "Collective Memory" in query
        assert "Test request" in query
        
    def test_query_stats(self):
        """Test query statistics"""
        builder = QueryBuilder()
        test_query = "# Test Query\nThis is a test query with multiple lines.\n## Section\nMore content."
        
        stats = builder.get_query_stats(test_query)
        
        assert 'total_chars' in stats
        assert 'total_words' in stats
        assert 'total_lines' in stats
        assert 'estimated_tokens' in stats
        assert stats['total_chars'] > 0
        assert stats['total_words'] > 0

class TestTriggerParser:
    """Trigger Parser tests"""
    
    def test_initialization(self):
        """Test parser initialization"""
        parser = TriggerParser()
        assert parser is not None
        assert hasattr(parser, 'comment_patterns')
        assert hasattr(parser, 'searchable_extensions')
        
    def test_supported_extensions(self):
        """Test supported extensions"""
        parser = TriggerParser()
        extensions = parser.get_supported_extensions()
        
        assert isinstance(extensions, list)
        assert len(extensions) > 0
        assert '.py' in extensions
        assert '.js' in extensions
        assert '.ts' in extensions
        
    def test_comment_syntax(self):
        """Test comment syntax for extensions"""
        parser = TriggerParser()
        
        py_syntax = parser.get_comment_syntax_for_extension('.py')
        js_syntax = parser.get_comment_syntax_for_extension('.js')
        
        assert '@collect-memory' in py_syntax
        assert '@collect-memory' in js_syntax
        assert py_syntax.startswith('#')
        assert js_syntax.startswith('//')
        
    def test_find_trigger_in_file(self, tmp_path):
        """Test finding trigger in file"""
        # Create test Python file with trigger
        test_file = tmp_path / "test.py"
        test_file.write_text("""
def main():
    # @collect-memory: Test request for optimization
    print("Hello World")
""")
        
        parser = TriggerParser()
        result = parser.find_trigger_in_file(test_file)
        
        assert result is not None
        assert result['found'] == True
        assert result['request'] == 'Test request for optimization'
        assert result['line_number'] == 3
        assert result['file_extension'] == '.py'
        
    def test_validate_trigger_syntax(self):
        """Test trigger syntax validation"""
        parser = TriggerParser()
        
        # Valid trigger
        valid_result = parser.validate_trigger_syntax("This is a valid request")
        assert valid_result['valid'] == True
        
        # Invalid trigger (empty)
        invalid_result = parser.validate_trigger_syntax("")
        assert invalid_result['valid'] == False
        
        # Warning trigger (too short)
        warning_result = parser.validate_trigger_syntax("Hi")
        assert len(warning_result['warnings']) > 0
        
    def test_extract_request_keywords(self):
        """Test keyword extraction"""
        parser = TriggerParser()
        
        keywords = parser.extract_request_keywords("Optimize this function for better performance")
        
        assert isinstance(keywords, list)
        assert len(keywords) > 0
        assert 'optimize' in [k.lower() for k in keywords]
        assert 'function' in [k.lower() for k in keywords]
        assert 'performance' in [k.lower() for k in keywords]

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 