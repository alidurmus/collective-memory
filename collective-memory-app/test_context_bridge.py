#!/usr/bin/env python3
"""
Smart Context Bridge Comprehensive Test Suite
Context Bridge sisteminin tüm bileşenlerini test eder
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
    ContextExtractor,
    CursorRulesUpdater
)


class TestSmartContextBridge:
    """Smart Context Bridge kapsamlı testleri"""
    
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
    
    def test_1_module_import(self):
        """Test 1: Module Import"""
        try:
            bridge = SmartContextBridge()
            return bridge is not None
        except Exception:
            return False
    
    def test_2_configuration(self):
        """Test 2: Configuration"""
        try:
            config = ContextBridgeConfig()
            required_fields = [
                'json_chat_path', 'cursor_rules_path', 'auto_context_file',
                'context_generation_enabled', 'max_context_length', 
                'min_relevance_score', 'update_interval_seconds',
                'max_conversations_to_analyze'
            ]
            
            for field in required_fields:
                if not hasattr(config, field):
                    return False
            return True
        except Exception:
            return False
    
    def test_3_context_extractor(self):
        """Test 3: Context Extractor"""
        try:
            bridge = SmartContextBridge()
            test_conversation = {
                'id': 'test_001',
                'title': 'Test Conversation',
                'messages': [
                    {'role': 'user', 'content': 'Test message'},
                    {'role': 'assistant', 'content': 'Test response'}
                ],
                'timestamp': time.time()
            }
            
            context = bridge.context_extractor.extract_context_from_conversation(test_conversation)
            
            required_keys = ['summary', 'key_decisions', 'technical_details', 
                           'next_steps', 'project_info', 'relevance_score']
            
            for key in required_keys:
                if key not in context:
                    return False
            return True
        except Exception:
            return False
    
    def test_4_rules_updater(self):
        """Test 4: Rules Updater"""
        try:
            config = ContextBridgeConfig()
            rules_updater = CursorRulesUpdater(config)
            return rules_updater is not None
        except Exception:
            return False
    
    def test_5_file_paths(self):
        """Test 5: File Paths"""
        try:
            config = ContextBridgeConfig()
            
            # Check if directories exist or can be created
            json_path = Path(config.json_chat_path)
            rules_path = Path(config.cursor_rules_path)
            
            # Create directories if they don't exist
            json_path.mkdir(parents=True, exist_ok=True)
            rules_path.mkdir(parents=True, exist_ok=True)
            
            return json_path.exists() and rules_path.exists()
        except Exception:
            return False
    
    def test_6_context_generation(self):
        """Test 6: Context Generation"""
        try:
            bridge = SmartContextBridge()
            
            # Test with different conversation types
            conversations = [
                {
                    'id': 'test_1',
                    'title': 'Simple Test',
                    'messages': [
                        {'role': 'user', 'content': 'Hello'},
                        {'role': 'assistant', 'content': 'Hi there!'}
                    ],
                    'timestamp': time.time()
                },
                {
                    'id': 'test_2',
                    'title': 'Technical Discussion',
                    'messages': [
                        {'role': 'user', 'content': 'We need to implement a REST API'},
                        {'role': 'assistant', 'content': 'Here is a REST API design...'}
                    ],
                    'timestamp': time.time()
                }
            ]
            
            for conv in conversations:
                context = bridge.context_extractor.extract_context_from_conversation(conv)
                if not context or 'summary' not in context:
                    return False
            
            return True
        except Exception:
            return False
    
    def test_7_relevance_scoring(self):
        """Test 7: Relevance Scoring"""
        try:
            bridge = SmartContextBridge()
            
            # Test relevance scoring
            test_messages = [
                {'role': 'user', 'content': 'This is a test message'},
                {'role': 'assistant', 'content': 'This is a test response'}
            ]
            
            score = bridge.context_extractor._calculate_relevance_score(test_messages)
            
            # Score should be between 0 and 1
            return 0 <= score <= 1
        except Exception:
            return False
    
    def test_8_cli_integration(self):
        """Test 8: CLI Integration"""
        try:
            from src.context_bridge_cli import ContextBridgeCLI
            cli = ContextBridgeCLI()
            
            # Test CLI methods exist
            required_methods = ['cmd_start', 'cmd_stop', 'cmd_status', 'cmd_config', 'cmd_test']
            
            for method in required_methods:
                if not hasattr(cli, method):
                    return False
            
            return True
        except Exception:
            return False
    
    def test_9_json_chat_files(self):
        """Test 9: JSON Chat Files"""
        try:
            config = ContextBridgeConfig()
            json_path = Path(config.json_chat_path)
            
            if not json_path.exists():
                json_path.mkdir(parents=True, exist_ok=True)
            
            # Create a test JSON file
            test_file = json_path / "test_conversation.json"
            test_data = {
                'id': 'test_cli_001',
                'title': 'CLI Test Conversation',
                'messages': [
                    {'role': 'user', 'content': 'CLI test message'},
                    {'role': 'assistant', 'content': 'CLI test response'}
                ],
                'timestamp': time.time()
            }
            
            with open(test_file, 'w', encoding='utf-8') as f:
                json.dump(test_data, f, indent=2, ensure_ascii=False)
            
            # Check if file was created
            if test_file.exists():
                # Clean up
                test_file.unlink()
                return True
            
            return False
        except Exception:
            return False
    
    def test_10_performance(self):
        """Test 10: Performance"""
        try:
            bridge = SmartContextBridge()
            start_time = time.time()
            
            # Test multiple context extractions
            for i in range(10):
                test_conv = {
                    'id': f'perf_test_{i}',
                    'title': f'Performance Test {i}',
                    'messages': [
                        {'role': 'user', 'content': f'Performance test message {i}'},
                        {'role': 'assistant', 'content': f'Performance test response {i}'}
                    ],
                    'timestamp': time.time()
                }
                
                context = bridge.context_extractor.extract_context_from_conversation(test_conv)
                if not context:
                    return False
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Should complete in reasonable time (less than 5 seconds)
            return execution_time < 5.0
        except Exception:
            return False
    
    def run_all_tests(self):
        """Tüm testleri çalıştır"""
        print("🚀 Smart Context Bridge Comprehensive Test Suite")
        print("=" * 60)
        
        tests = [
            ("Module Import", self.test_1_module_import),
            ("Configuration", self.test_2_configuration),
            ("Context Extractor", self.test_3_context_extractor),
            ("Rules Updater", self.test_4_rules_updater),
            ("File Paths", self.test_5_file_paths),
            ("Context Generation", self.test_6_context_generation),
            ("Relevance Scoring", self.test_7_relevance_scoring),
            ("CLI Integration", self.test_8_cli_integration),
            ("JSON Chat Files", self.test_9_json_chat_files),
            ("Performance", self.test_10_performance)
        ]
        
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
            print()
        
        self.print_summary()
    
    def print_summary(self):
        """Test özetini yazdır"""
        print("📊 Test Summary")
        print("=" * 60)
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"📈 Success Rate: {(self.passed / (self.passed + self.failed) * 100):.1f}%")
        
        if self.failed > 0:
            print("\n❌ Failed Tests:")
            for result in self.test_results:
                if result["status"] in ["FAILED", "ERROR"]:
                    print(f"  - {result['test']}: {result.get('error', 'Failed')}")
        
        print("\n🎯 Overall Status:")
        if self.failed == 0:
            print("🎉 ALL TESTS PASSED - Smart Context Bridge is working perfectly!")
        elif self.passed > self.failed:
            print("⚠️  MOST TESTS PASSED - Smart Context Bridge is working with minor issues")
        else:
            print("❌ MANY TESTS FAILED - Smart Context Bridge needs attention")


def main():
    """Ana test fonksiyonu"""
    tester = TestSmartContextBridge()
    tester.run_all_tests()


if __name__ == "__main__":
    main() 