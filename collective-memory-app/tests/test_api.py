#!/usr/bin/env python3
"""
API Test Suite - Collective Memory API Testing
Comprehensive testing for Chat API, Enterprise API, and related components
"""

import unittest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

# Import the modules to test
from src.chat_api import ChatAPI
from src.json_chat_manager import JSONChatManager
from src.enhanced_query_engine import EnhancedQueryEngine
from src.database_manager import DatabaseManager


class TestChatAPI(unittest.TestCase):
    """Chat API test cases"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.chat_api = ChatAPI(self.temp_dir)
        self.test_conversation_id = None

    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_chat_api_initialization(self):
        """Test ChatAPI initialization"""
        self.assertIsNotNone(self.chat_api)
        self.assertIsNotNone(self.chat_api.chat_manager)
        self.assertIsNotNone(self.chat_api.blueprint)

    def test_create_conversation(self):
        """Test conversation creation"""
        # Mock request data
        mock_request = Mock()
        mock_request.get_json.return_value = {
            "title": "Test Conversation",
            "project_path": "/test/project",
            "initial_message": "Hello, this is a test"
        }

        with patch('src.chat_api.request', mock_request):
            # Test the create_conversation endpoint
            response = self.chat_api.blueprint.view_functions[
                'create_conversation'
            ]()
            response_data = json.loads(response.get_data(as_text=True))

            self.assertEqual(response.status_code, 201)
            self.assertTrue(response_data['success'])
            self.assertIn('conversation_id', response_data['data'])

    def test_get_conversations(self):
        """Test getting conversations list"""
        # Mock request args
        mock_request = Mock()
        mock_request.args = {
            'query': '',
            'project_path': '',
            'tags': [],
            'limit': '10'
        }

        with patch('src.chat_api.request', mock_request):
            response = self.chat_api.blueprint.view_functions[
                'get_conversations'
            ]()
            response_data = json.loads(response.get_data(as_text=True))

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response_data['success'])
            self.assertIn('data', response_data)
            self.assertIn('count', response_data)

    def test_get_stats(self):
        """Test getting conversation statistics"""
        response = self.chat_api.blueprint.view_functions['get_stats']()
        response_data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_data['success'])
        self.assertIn('data', response_data)


class TestJSONChatManager(unittest.TestCase):
    """JSON Chat Manager test cases"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.chat_manager = JSONChatManager(self.temp_dir)

    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_chat_manager_initialization(self):
        """Test JSONChatManager initialization"""
        self.assertIsNotNone(self.chat_manager)
        self.assertEqual(self.chat_manager.data_folder, self.temp_dir)

    def test_create_conversation(self):
        """Test conversation creation"""
        conversation_id = self.chat_manager.create_conversation(
            title="Test Conversation",
            project_path="/test/project"
        )

        self.assertIsNotNone(conversation_id)
        self.assertIsInstance(conversation_id, str)

        # Verify conversation file exists
        conversation_file = Path(self.temp_dir) / "conversations" / f"{conversation_id}.json"
        self.assertTrue(conversation_file.exists())

    def test_add_message(self):
        """Test adding message to conversation"""
        # Create conversation first
        conversation_id = self.chat_manager.create_conversation(
            title="Test Conversation",
            project_path="/test/project"
        )

        # Add message
        message_id = self.chat_manager.add_message(
            conversation_id=conversation_id,
            role="user",
            content="Test message content"
        )

        self.assertIsNotNone(message_id)
        self.assertIsInstance(message_id, str)

    def test_load_conversation(self):
        """Test loading conversation"""
        # Create conversation first
        conversation_id = self.chat_manager.create_conversation(
            title="Test Conversation",
            project_path="/test/project"
        )

        # Load conversation
        conversation = self.chat_manager.load_conversation(conversation_id)

        self.assertIsNotNone(conversation)
        self.assertEqual(conversation.title, "Test Conversation")
        self.assertEqual(conversation.project_path, "/test/project")

    def test_search_conversations(self):
        """Test searching conversations"""
        # Create test conversations
        self.chat_manager.create_conversation("Test 1", "/project1")
        self.chat_manager.create_conversation("Test 2", "/project2")

        # Search conversations
        results = self.chat_manager.search_conversations(query="Test")

        self.assertIsInstance(results, list)
        self.assertGreaterEqual(len(results), 2)

    def test_get_conversation_stats(self):
        """Test getting conversation statistics"""
        # Create test conversations
        self.chat_manager.create_conversation("Test 1", "/project1")
        self.chat_manager.create_conversation("Test 2", "/project2")

        # Get stats
        stats = self.chat_manager.get_conversation_stats()

        self.assertIsInstance(stats, dict)
        self.assertIn('total_conversations', stats)
        self.assertIn('total_messages', stats)
        self.assertIn('projects', stats)


class TestEnhancedQueryEngine(unittest.TestCase):
    """Enhanced Query Engine test cases"""

    def setUp(self):
        """Set up test environment"""
        self.db_manager = DatabaseManager()
        self.query_engine = EnhancedQueryEngine(self.db_manager)

    def test_query_engine_initialization(self):
        """Test EnhancedQueryEngine initialization"""
        self.assertIsNotNone(self.query_engine)
        self.assertIsNotNone(self.query_engine.database_manager)

    def test_semantic_search(self):
        """Test semantic search functionality"""
        # This test would require actual data in the database
        # For now, we'll test that the method exists and doesn't crash
        try:
            results = self.query_engine.semantic_search("test query")
            self.assertIsInstance(results, list)
        except Exception as e:
            # If no data, that's expected
            self.assertIn("No data", str(e) or "empty")


class TestDatabaseManager(unittest.TestCase):
    """Database Manager test cases"""

    def setUp(self):
        """Set up test environment"""
        self.db_manager = DatabaseManager()

    def test_database_initialization(self):
        """Test DatabaseManager initialization"""
        self.assertIsNotNone(self.db_manager)

    def test_database_connection(self):
        """Test database connection"""
        # Test that we can connect to the database
        try:
            self.db_manager.connect()
            self.assertTrue(self.db_manager.is_connected())
            self.db_manager.disconnect()
        except Exception as e:
            self.fail(f"Database connection failed: {e}")

    def test_table_creation(self):
        """Test table creation"""
        try:
            self.db_manager.connect()
            # Test that tables can be created
            self.db_manager.create_tables()
            self.db_manager.disconnect()
        except Exception as e:
            self.fail(f"Table creation failed: {e}")


class TestPerformanceMonitor(unittest.TestCase):
    """Performance Monitor test cases"""

    def test_performance_monitor_import(self):
        """Test that performance monitor can be imported"""
        try:
            import src.performance_monitor
            self.assertTrue(True)  # Import successful
        except ImportError as e:
            self.fail(f"Performance monitor import failed: {e}")


class TestSmartContextBridge(unittest.TestCase):
    """Smart Context Bridge test cases"""

    def test_smart_context_bridge_import(self):
        """Test that smart context bridge can be imported"""
        try:
            from src.smart_context_bridge import SmartContextBridge
            self.assertTrue(True)  # Import successful
        except ImportError as e:
            self.fail(f"Smart Context Bridge import failed: {e}")

    def test_context_bridge_cli_import(self):
        """Test that context bridge CLI can be imported"""
        try:
            from src.context_bridge_cli import ContextBridgeCLI
            self.assertTrue(True)  # Import successful
        except ImportError as e:
            self.fail(f"Context Bridge CLI import failed: {e}")


def run_api_tests():
    """Run all API tests"""
    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test cases
    test_classes = [
        TestChatAPI,
        TestJSONChatManager,
        TestEnhancedQueryEngine,
        TestDatabaseManager,
        TestPerformanceMonitor,
        TestSmartContextBridge
    ]

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    return result.wasSuccessful()


if __name__ == '__main__':
    print("🧪 Running Collective Memory API Test Suite...")
    success = run_api_tests()
    
    if success:
        print("✅ All API tests passed!")
    else:
        print("❌ Some API tests failed!")
    
    exit(0 if success else 1) 