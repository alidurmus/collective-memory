#!/usr/bin/env python3
"""
Simple API Test - Collective Memory API Testing
Basic functionality tests for core components
"""

import sys
sys.path.append('.')


def test_chat_api():
    """Test Chat API functionality"""
    print("🧪 Testing Chat API...")
    try:
        from src.chat_api import ChatAPI
        ChatAPI()  # Initialize to test
        print("✅ ChatAPI imported and initialized successfully")
        return True
    except Exception as e:
        print(f"❌ ChatAPI test failed: {e}")
        return False


def test_json_chat_manager():
    """Test JSON Chat Manager functionality"""
    print("🧪 Testing JSON Chat Manager...")
    try:
        from src.json_chat_manager import JSONChatManager
        manager = JSONChatManager()
        print("✅ JSONChatManager imported and initialized successfully")
        
        # Test CRUD operations
        test_id = manager.create_conversation("Test Conversation", 
                                            "Test Project")
        print(f"✅ Yeni konuşma oluşturuldu: Test Conversation ({test_id})")
        
        message_id = manager.add_message(test_id, "user", 
                                       "Test message from API")
        print(f"✅ Created conversation: {test_id}")
        print(f"✅ Added message: {message_id}")
        
        conversation = manager.load_conversation(test_id)
        title = conversation.title if conversation else None
        print(f"✅ Loaded conversation: {title}")
        
        stats = manager.get_conversation_stats()
        count = stats.get('total_conversations', 0)
        print(f"✅ Got stats: {count} conversations")
        
        return True
    except Exception as e:
        print(f"❌ JSONChatManager test failed: {e}")
        return False


def test_enhanced_query_engine():
    """Test Enhanced Query Engine functionality"""
    print("🧪 Testing Enhanced Query Engine...")
    try:
        from src.enhanced_query_engine import EnhancedQueryEngine
        from src.database_manager import DatabaseManager
        
        db = DatabaseManager()
        engine = EnhancedQueryEngine(db)
        print("✅ EnhancedQueryEngine imported and initialized successfully")
        return True
    except Exception as e:
        print(f"❌ EnhancedQueryEngine test failed: {e}")
        return False


def test_database_manager():
    """Test Database Manager functionality"""
    print("🧪 Testing Database Manager...")
    try:
        from src.database_manager import DatabaseManager
        db = DatabaseManager()
        print("✅ DatabaseManager imported and initialized successfully")
        return True
    except Exception as e:
        print(f"❌ DatabaseManager test failed: {e}")
        return False


def test_performance_monitor():
    """Test Performance Monitor functionality"""
    print("🧪 Testing Performance Monitor...")
    try:
        import src.performance_monitor
        print("✅ PerformanceMonitor imported successfully")
        return True
    except Exception as e:
        print(f"❌ PerformanceMonitor test failed: {e}")
        return False


def test_smart_context_bridge():
    """Test Smart Context Bridge functionality"""
    print("🧪 Testing Smart Context Bridge...")
    try:
        from src.smart_context_bridge import SmartContextBridge
        bridge = SmartContextBridge()
        print("✅ SmartContextBridge imported successfully")
        return True
    except Exception as e:
        print(f"❌ SmartContextBridge test failed: {e}")
        return False


def test_context_bridge_cli():
    """Test Context Bridge CLI functionality"""
    print("🧪 Testing Context Bridge CLI...")
    try:
        import src.context_bridge_cli
        print("✅ ContextBridgeCLI imported successfully")
        return True
    except Exception as e:
        print(f"❌ ContextBridgeCLI test failed: {e}")
        return False


def run_all_tests():
    """Run all API tests"""
    print("🚀 Starting Collective Memory API Tests...")
    
    tests = [
        test_chat_api,
        test_json_chat_manager,
        test_enhanced_query_engine,
        test_database_manager,
        test_performance_monitor,
        test_smart_context_bridge,
        test_context_bridge_cli
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is operational.")
        return True
    else:
        print("⚠️ Some tests failed. Check the output above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1) 