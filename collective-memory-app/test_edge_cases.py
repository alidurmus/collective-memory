#!/usr/bin/env python3
"""
Edge Case Testing Suite - Phase 8
Smart Context Bridge için sınır durumları ve edge case testleri
"""

import sys
import os
import json
import time
from pathlib import Path
from unittest.mock import Mock, patch

# Add src to path
sys.path.append('.')

from src.smart_context_bridge import (
    SmartContextBridge, 
    ContextBridgeConfig, 
    ChatContext,
    ContextExtractor
)


class TestEdgeCases:
    """Edge case testleri"""
    
    def __init__(self):
        self.test_results = []
        self.passed = 0
        self.failed = 0
        
    def run_test(self, test_name, test_func):
        """Test çalıştır ve sonucu kaydet"""
        try:
            print(f"🧪 Running: {test_name}")
            result = test_func()
            if result:
                print(f"✅ {test_name} - PASSED")
                self.test_results.append({"test": test_name, "status": "PASSED"})
                self.passed += 1
            else:
                print(f"❌ {test_name} - FAILED")
                self.test_results.append({"test": test_name, "status": "FAILED"})
                self.failed += 1
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")
            self.test_results.append({"test": test_name, "status": "ERROR", "error": str(e)})
            self.failed += 1
    
    def test_1_empty_conversation(self):
        """Test 1: Empty Conversation"""
        try:
            bridge = SmartContextBridge()
            empty_conv = {
                'id': 'empty_test',
                'title': 'Empty Conversation',
                'messages': [],
                'timestamp': time.time()
            }
            
            context = bridge.context_extractor.extract_context_from_conversation(empty_conv)
            
            # Should handle empty conversation gracefully
            return context is not None and isinstance(context, dict)
        except Exception:
            return False
    
    def test_2_very_large_conversation(self):
        """Test 2: Very Large Conversation"""
        try:
            bridge = SmartContextBridge()
            
            # Create a very large conversation
            large_conv = {
                'id': 'large_test',
                'title': 'Very Large Conversation',
                'messages': [],
                'timestamp': time.time()
            }
            
            # Add 1000 messages
            for i in range(1000):
                large_conv['messages'].append({
                    'role': 'user' if i % 2 == 0 else 'assistant',
                    'content': f'Large message content {i} ' * 50  # 50x tekrar
                })
            
            context = bridge.context_extractor.extract_context_from_conversation(large_conv)
            
            # Should handle large conversation without crashing
            return context is not None and 'summary' in context
        except Exception:
            return False
    
    def test_3_malformed_messages(self):
        """Test 3: Malformed Messages"""
        try:
            bridge = SmartContextBridge()
            
            malformed_conv = {
                'id': 'malformed_test',
                'title': 'Malformed Conversation',
                'messages': [
                    {'role': 'user'},  # Missing content
                    {'content': 'No role'},  # Missing role
                    {'role': 'user', 'content': None},  # None content
                    {'role': 'user', 'content': ''},  # Empty content
                    {'role': 'invalid_role', 'content': 'Invalid role'},  # Invalid role
                ],
                'timestamp': time.time()
            }
            
            context = bridge.context_extractor.extract_context_from_conversation(malformed_conv)
            
            # Should handle malformed messages gracefully
            return context is not None
        except Exception:
            return False
    
    def test_4_unicode_characters(self):
        """Test 4: Unicode Characters"""
        try:
            bridge = SmartContextBridge()
            
            unicode_conv = {
                'id': 'unicode_test',
                'title': 'Unicode Test Conversation',
                'messages': [
                    {'role': 'user', 'content': '🚀 Test with emojis: 🎉✨🌟'},
                    {'role': 'assistant', 'content': 'Türkçe karakterler: ğüşıöçĞÜŞİÖÇ'},
                    {'role': 'user', 'content': '特殊字符: 中文测试 🎯'},
                    {'role': 'assistant', 'content': 'Русский текст: тест 🎨'},
                ],
                'timestamp': time.time()
            }
            
            context = bridge.context_extractor.extract_context_from_conversation(unicode_conv)
            
            # Should handle unicode characters correctly
            return context is not None and 'summary' in context
        except Exception:
            return False
    
    def test_5_extremely_long_message(self):
        """Test 5: Extremely Long Message"""
        try:
            bridge = SmartContextBridge()
            
            # Create extremely long message
            long_message = "This is a very long message. " * 1000  # 1000x tekrar
            
            long_conv = {
                'id': 'long_message_test',
                'title': 'Long Message Test',
                'messages': [
                    {'role': 'user', 'content': long_message},
                    {'role': 'assistant', 'content': 'Response to long message'},
                ],
                'timestamp': time.time()
            }
            
            context = bridge.context_extractor.extract_context_from_conversation(long_conv)
            
            # Should handle extremely long messages
            return context is not None
        except Exception:
            return False
    
    def test_6_missing_fields(self):
        """Test 6: Missing Fields"""
        try:
            bridge = SmartContextBridge()
            
            # Test with missing fields
            incomplete_conv = {
                'id': 'incomplete_test',
                # Missing title
                'messages': [
                    {'role': 'user', 'content': 'Test message'},
                ],
                # Missing timestamp
            }
            
            context = bridge.context_extractor.extract_context_from_conversation(incomplete_conv)
            
            # Should handle missing fields gracefully
            return context is not None
        except Exception:
            return False
    
    def test_7_nested_objects(self):
        """Test 7: Nested Objects in Messages"""
        try:
            bridge = SmartContextBridge()
            
            nested_conv = {
                'id': 'nested_test',
                'title': 'Nested Objects Test',
                'messages': [
                    {
                        'role': 'user', 
                        'content': 'Test message',
                        'metadata': {
                            'nested': {
                                'deep': {
                                    'object': 'value'
                                }
                            }
                        }
                    },
                    {
                        'role': 'assistant', 
                        'content': 'Response',
                        'extra_data': [1, 2, 3, {'nested': 'array'}]
                    },
                ],
                'timestamp': time.time()
            }
            
            context = bridge.context_extractor.extract_context_from_conversation(nested_conv)
            
            # Should handle nested objects
            return context is not None
        except Exception:
            return False
    
    def test_8_concurrent_access(self):
        """Test 8: Concurrent Access"""
        try:
            import threading
            import queue
            
            bridge = SmartContextBridge()
            results = queue.Queue()
            
            def worker(worker_id):
                try:
                    test_conv = {
                        'id': f'concurrent_test_{worker_id}',
                        'title': f'Concurrent Test {worker_id}',
                        'messages': [
                            {'role': 'user', 'content': f'Message from worker {worker_id}'},
                            {'role': 'assistant', 'content': f'Response to worker {worker_id}'},
                        ],
                        'timestamp': time.time()
                    }
                    
                    context = bridge.context_extractor.extract_context_from_conversation(test_conv)
                    results.put(('success', worker_id, context is not None))
                except Exception as e:
                    results.put(('error', worker_id, str(e)))
            
            # Start multiple threads
            threads = []
            for i in range(10):
                thread = threading.Thread(target=worker, args=(i,))
                threads.append(thread)
                thread.start()
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join()
            
            # Check results
            success_count = 0
            while not results.empty():
                status, worker_id, result = results.get()
                if status == 'success' and result:
                    success_count += 1
            
            # All threads should succeed
            return success_count == 10
        except Exception:
            return False
    
    def test_9_memory_pressure(self):
        """Test 9: Memory Pressure"""
        try:
            bridge = SmartContextBridge()
            
            # Create many conversations to test memory pressure
            conversations = []
            for i in range(100):
                conv = {
                    'id': f'memory_test_{i}',
                    'title': f'Memory Test {i}',
                    'messages': [
                        {'role': 'user', 'content': f'Memory test message {i} ' * 10},
                        {'role': 'assistant', 'content': f'Memory test response {i} ' * 10},
                    ],
                    'timestamp': time.time()
                }
                conversations.append(conv)
            
            # Process all conversations
            contexts = []
            for conv in conversations:
                context = bridge.context_extractor.extract_context_from_conversation(conv)
                contexts.append(context)
            
            # All should succeed
            return len(contexts) == 100 and all(ctx is not None for ctx in contexts)
        except Exception:
            return False
    
    def test_10_error_recovery(self):
        """Test 10: Error Recovery"""
        try:
            bridge = SmartContextBridge()
            
            # Test with various error conditions
            error_cases = [
                # None conversation
                None,
                # Empty dict
                {},
                # Invalid message format
                {'id': 'error_test', 'messages': 'not_a_list'},
                # Messages with invalid types
                {'id': 'error_test', 'messages': [123, 'string', None]},
            ]
            
            for error_case in error_cases:
                try:
                    context = bridge.context_extractor.extract_context_from_conversation(error_case)
                    # Should not crash, should return None or empty context
                    if context is not None:
                        # If it returns something, it should be a dict
                        if not isinstance(context, dict):
                            return False
                except Exception:
                    # Some errors are expected, but should not crash the system
                    pass
            
            return True
        except Exception:
            return False
    
    def run_all_tests(self):
        """Tüm edge case testlerini çalıştır"""
        print("🚀 Smart Context Bridge Edge Case Testing Suite")
        print("=" * 60)
        
        tests = [
            ("Empty Conversation", self.test_1_empty_conversation),
            ("Very Large Conversation", self.test_2_very_large_conversation),
            ("Malformed Messages", self.test_3_malformed_messages),
            ("Unicode Characters", self.test_4_unicode_characters),
            ("Extremely Long Message", self.test_5_extremely_long_message),
            ("Missing Fields", self.test_6_missing_fields),
            ("Nested Objects", self.test_7_nested_objects),
            ("Concurrent Access", self.test_8_concurrent_access),
            ("Memory Pressure", self.test_9_memory_pressure),
            ("Error Recovery", self.test_10_error_recovery)
        ]
        
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
            print()
        
        self.print_summary()
    
    def print_summary(self):
        """Test özetini yazdır"""
        print("📊 Edge Case Test Summary")
        print("=" * 60)
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"📈 Success Rate: {(self.passed / (self.passed + self.failed) * 100):.1f}%")
        
        if self.failed > 0:
            print("\n❌ Failed Tests:")
            for result in self.test_results:
                if result["status"] in ["FAILED", "ERROR"]:
                    print(f"  - {result['test']}: {result.get('error', 'Failed')}")
        
        print("\n🎯 Edge Case Status:")
        if self.failed == 0:
            print("🎉 ALL EDGE CASES HANDLED - System is robust!")
        elif self.passed > self.failed:
            print("⚠️  MOST EDGE CASES HANDLED - System is mostly robust")
        else:
            print("❌ MANY EDGE CASES FAILED - System needs improvement")


def main():
    """Ana test fonksiyonu"""
    tester = TestEdgeCases()
    tester.run_all_tests()


if __name__ == "__main__":
    main() 