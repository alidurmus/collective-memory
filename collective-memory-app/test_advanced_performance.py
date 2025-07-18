#!/usr/bin/env python3
"""
Advanced Performance Testing Suite - Phase 7
Smart Context Bridge için gelişmiş performans testleri
"""

import pytest
import time
import psutil
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import Mock, patch

# Local imports
from src.smart_context_bridge import SmartContextBridge, ContextBridgeConfig
from src.websocket_manager import WindowsCompatibleSocketIO


class PerformanceMetrics:
    """Performans metrikleri toplama sınıfı"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.memory_start = None
        self.memory_end = None
        self.cpu_start = None
        self.cpu_end = None
        
    def start_measurement(self):
        """Ölçüm başlat"""
        self.start_time = time.time()
        self.memory_start = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        self.cpu_start = psutil.cpu_percent()
        
    def end_measurement(self):
        """Ölçüm bitir"""
        self.end_time = time.time()
        self.memory_end = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        self.cpu_end = psutil.cpu_percent()
        
    def get_metrics(self):
        """Metrikleri döndür"""
        if not self.start_time or not self.end_time:
            return None
            
        return {
            'execution_time': self.end_time - self.start_time,
            'memory_usage': self.memory_end - self.memory_start,
            'cpu_usage': self.cpu_end - self.cpu_start,
            'memory_peak': self.memory_end
        }


class TestAdvancedPerformance:
    """Gelişmiş performans testleri"""
    
    @pytest.fixture
    def config(self):
        """Test konfigürasyonu"""
        return ContextBridgeConfig(
            json_chat_path=".collective-memory/test_conversations/",
            cursor_rules_path=".cursor/rules/",
            auto_context_file="auto_context.md",
            context_generation_enabled=True,
            max_context_length=5000,
            min_relevance_score=0.7,
            update_interval_seconds=1,
            max_conversations_to_analyze=10
        )
    
    @pytest.fixture
    def bridge(self, config):
        """Smart Context Bridge instance"""
        return SmartContextBridge(config)
    
    @pytest.fixture
    def websocket_manager(self):
        """WebSocket manager instance"""
        return WindowsCompatibleSocketIO()
    
    def test_context_generation_performance(self, bridge):
        """Context generation performans testi"""
        metrics = PerformanceMetrics()
        
        # Test data oluştur
        test_conversations = []
        for i in range(100):
            conversation = {
                'id': f'test_conv_{i}',
                'title': f'Test Conversation {i}',
                'messages': [
                    {'role': 'user', 'content': f'Test message {i} from user'},
                    {'role': 'assistant', 'content': f'Test response {i} from assistant'}
                ],
                'timestamp': time.time()
            }
            test_conversations.append(conversation)
        
        # Performans ölçümü başlat
        metrics.start_measurement()
        
        # Context generation test et
        for conversation in test_conversations:
            context = bridge.context_extractor.extract_context_from_conversation(conversation)
            assert context is not None
            assert len(context.get('summary', '')) > 0
        
        # Performans ölçümü bitir
        metrics.end_measurement()
        result = metrics.get_metrics()
        
        # Assertions
        assert result['execution_time'] < 5.0  # 5 saniyeden az
        assert result['memory_usage'] < 100  # 100MB'dan az memory artışı
        print(f"Context Generation Performance: {result}")
    
    def test_concurrent_context_generation(self, bridge):
        """Eşzamanlı context generation testi"""
        def generate_context(conv_id):
            conversation = {
                'id': f'conv_{conv_id}',
                'title': f'Conversation {conv_id}',
                'messages': [
                    {'role': 'user', 'content': f'Message {conv_id}'},
                    {'role': 'assistant', 'content': f'Response {conv_id}'}
                ],
                'timestamp': time.time()
            }
            return bridge.context_extractor.extract_context_from_conversation(conversation)
        
        # Thread pool ile eşzamanlı test
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(generate_context, i) for i in range(50)]
            results = [future.result() for future in futures]
        
        # Tüm sonuçlar başarılı olmalı
        assert len(results) == 50
        assert all(result is not None for result in results)
        print("Concurrent Context Generation: PASSED")
    
    def test_memory_usage_under_load(self, bridge):
        """Yük altında bellek kullanımı testi"""
        initial_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        # Yoğun işlem yap
        for i in range(1000):
            conversation = {
                'id': f'load_test_{i}',
                'title': f'Load Test {i}',
                'messages': [
                    {'role': 'user', 'content': f'Load test message {i}'},
                    {'role': 'assistant', 'content': f'Load test response {i}'}
                ],
                'timestamp': time.time()
            }
            bridge.context_extractor.extract_context_from_conversation(conversation)
        
        final_memory = psutil.Process().memory_info().rss / 1024 / 1024
        memory_increase = final_memory - initial_memory
        
        # Bellek artışı makul seviyede olmalı
        assert memory_increase < 200  # 200MB'dan az artış
        print(f"Memory Usage Under Load: {memory_increase:.2f}MB increase")
    
    def test_websocket_connection_performance(self, websocket_manager):
        """WebSocket bağlantı performansı testi"""
        metrics = PerformanceMetrics()
        
        # Mock Flask app
        mock_app = Mock()
        mock_app.config = {'SECRET_KEY': 'test'}
        
        metrics.start_measurement()
        
        # WebSocket manager başlat
        websocket_manager.init_app(mock_app)
        
        metrics.end_measurement()
        result = metrics.get_metrics()
        
        # WebSocket başlatma hızlı olmalı
        assert result['execution_time'] < 1.0  # 1 saniyeden az
        print(f"WebSocket Connection Performance: {result}")
    
    def test_file_monitoring_performance(self, bridge):
        """Dosya izleme performansı testi"""
        metrics = PerformanceMetrics()
        
        # Test dosyaları oluştur
        test_dir = Path(".collective-memory/test_monitoring/")
        test_dir.mkdir(parents=True, exist_ok=True)
        
        for i in range(50):
            test_file = test_dir / f"test_{i}.json"
            with open(test_file, 'w') as f:
                json.dump({'test': f'data_{i}'}, f)
        
        metrics.start_measurement()
        
        # Dosya izleme başlat
        bridge._setup_file_monitoring()
        
        metrics.end_measurement()
        result = metrics.get_metrics()
        
        # Dosya izleme hızlı başlamalı
        assert result['execution_time'] < 2.0  # 2 saniyeden az
        
        # Temizlik
        import shutil
        shutil.rmtree(test_dir)
        print(f"File Monitoring Performance: {result}")
    
    def test_context_relevance_scoring_performance(self, bridge):
        """Context relevance scoring performansı testi"""
        metrics = PerformanceMetrics()
        
        # Test context'leri oluştur
        contexts = []
        for i in range(100):
            context = Mock()
            context.summary = f"Test context summary {i}"
            context.key_decisions = [f"Decision {i}"]
            context.technical_context = f"Technical context {i}"
            contexts.append(context)
        
        metrics.start_measurement()
        
        # Relevance scoring test et
        for context in contexts:
            score = bridge._calculate_relevance_score(context, "test query")
            assert 0 <= score <= 1
        
        metrics.end_measurement()
        result = metrics.get_metrics()
        
        # Scoring hızlı olmalı
        assert result['execution_time'] < 1.0  # 1 saniyeden az
        print(f"Context Relevance Scoring Performance: {result}")
    
    def test_stress_test_large_conversations(self, bridge):
        """Büyük konuşmalar için stress testi"""
        # Büyük konuşma oluştur
        large_conversation = {
            'id': 'stress_test_large',
            'title': 'Large Conversation Stress Test',
            'messages': []
        }
        
        # 1000 mesaj ekle
        for i in range(1000):
            large_conversation['messages'].append({
                'role': 'user' if i % 2 == 0 else 'assistant',
                'content': f'Large message content {i} ' * 10  # 10x tekrar
            })
        
        metrics = PerformanceMetrics()
        metrics.start_measurement()
        
        # Büyük konuşmayı işle
        context = bridge._generate_context_from_conversation(large_conversation)
        
        metrics.end_measurement()
        result = metrics.get_metrics()
        
        # Büyük konuşma işleme makul sürede olmalı
        assert result['execution_time'] < 10.0  # 10 saniyeden az
        assert context is not None
        print(f"Large Conversation Stress Test: {result}")
    
    def test_concurrent_file_operations(self, bridge):
        """Eşzamanlı dosya operasyonları testi"""
        test_dir = Path(".collective-memory/test_concurrent/")
        test_dir.mkdir(parents=True, exist_ok=True)
        
        def create_file(file_id):
            file_path = test_dir / f"concurrent_{file_id}.json"
            with open(file_path, 'w') as f:
                json.dump({'id': file_id, 'data': f'concurrent_data_{file_id}'}, f)
            return file_path
        
        def read_file(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        
        # Eşzamanlı dosya oluşturma
        with ThreadPoolExecutor(max_workers=20) as executor:
            file_paths = list(executor.map(create_file, range(100)))
        
        # Eşzamanlı dosya okuma
        with ThreadPoolExecutor(max_workers=20) as executor:
            results = list(executor.map(read_file, file_paths))
        
        # Tüm dosyalar başarıyla işlenmeli
        assert len(results) == 100
        assert all('id' in result for result in results)
        
        # Temizlik
        import shutil
        shutil.rmtree(test_dir)
        print("Concurrent File Operations: PASSED")
    
    def test_error_recovery_performance(self, bridge):
        """Hata kurtarma performansı testi"""
        metrics = PerformanceMetrics()
        
        # Hata durumu simüle et
        with patch.object(bridge, '_generate_context_from_conversation', 
                         side_effect=Exception("Test error")):
            
            metrics.start_measurement()
            
            # Hata ile karşılaşan işlem
            try:
                bridge._generate_context_from_conversation({'id': 'error_test'})
            except Exception:
                pass  # Hata bekleniyor
            
            metrics.end_measurement()
            result = metrics.get_metrics()
        
        # Hata kurtarma hızlı olmalı
        assert result['execution_time'] < 0.5  # 0.5 saniyeden az
        print(f"Error Recovery Performance: {result}")
    
    def test_memory_leak_detection(self, bridge):
        """Bellek sızıntısı tespiti testi"""
        initial_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        # Çoklu iterasyon
        for iteration in range(10):
            for i in range(100):
                conversation = {
                    'id': f'leak_test_{iteration}_{i}',
                    'title': f'Leak Test {iteration}_{i}',
                    'messages': [
                        {'role': 'user', 'content': f'Leak test message {i}'},
                        {'role': 'assistant', 'content': f'Leak test response {i}'}
                    ],
                    'timestamp': time.time()
                }
                bridge._generate_context_from_conversation(conversation)
            
            # Her iterasyonda bellek kontrolü
            current_memory = psutil.Process().memory_info().rss / 1024 / 1024
            memory_increase = current_memory - initial_memory
            
            # Bellek artışı makul seviyede olmalı
            assert memory_increase < 500  # 500MB'dan az artış
            print(f"Iteration {iteration}: Memory increase: {memory_increase:.2f}MB")
    
    def test_cpu_usage_under_load(self, bridge):
        """Yük altında CPU kullanımı testi"""
        initial_cpu = psutil.cpu_percent()
        
        # Yoğun işlem
        for i in range(500):
            conversation = {
                'id': f'cpu_test_{i}',
                'title': f'CPU Test {i}',
                'messages': [
                    {'role': 'user', 'content': f'CPU test message {i}'},
                    {'role': 'assistant', 'content': f'CPU test response {i}'}
                ],
                'timestamp': time.time()
            }
            bridge._generate_context_from_conversation(conversation)
        
        final_cpu = psutil.cpu_percent()
        cpu_increase = final_cpu - initial_cpu
        
        # CPU artışı makul seviyede olmalı
        assert cpu_increase < 50  # %50'den az artış
        print(f"CPU Usage Under Load: {cpu_increase:.2f}% increase")


class TestErrorHandlingEnhancement:
    """Gelişmiş hata yakalama testleri"""
    
    @pytest.fixture
    def config(self):
        return ContextBridgeConfig()
    
    @pytest.fixture
    def bridge(self, config):
        return SmartContextBridge(config)
    
    def test_graceful_degradation_on_file_error(self, bridge):
        """Dosya hatası durumunda graceful degradation"""
        # Geçersiz dosya yolu
        invalid_path = "/invalid/path/that/does/not/exist"
        
        # Hata durumunda graceful degradation
        result = bridge._safe_file_operation(
            lambda: bridge._read_json_file(invalid_path),
            default_value={}
        )
        
        assert result == {}
        print("Graceful Degradation on File Error: PASSED")
    
    def test_network_error_recovery(self, bridge):
        """Ağ hatası kurtarma testi"""
        with patch('requests.get', side_effect=Exception("Network error")):
            # Ağ hatası durumunda fallback
            result = bridge._safe_network_operation(
                lambda: bridge._fetch_external_data("http://invalid-url.com"),
                default_value={"fallback": "data"}
            )
            
            assert result["fallback"] == "data"
            print("Network Error Recovery: PASSED")
    
    def test_memory_error_handling(self, bridge):
        """Bellek hatası yönetimi testi"""
        # Bellek hatası simüle et
        with patch('psutil.Process.memory_info', 
                  side_effect=MemoryError("Out of memory")):
            
            # Bellek hatası durumunda graceful handling
            result = bridge._safe_memory_operation(
                lambda: bridge._get_memory_usage(),
                default_value=0
            )
            
            assert result == 0
            print("Memory Error Handling: PASSED")
    
    def test_concurrent_error_handling(self, bridge):
        """Eşzamanlı hata yönetimi testi"""
        def error_prone_operation(operation_id):
            if operation_id % 3 == 0:  # Her 3. operasyonda hata
                raise Exception(f"Simulated error {operation_id}")
            return f"success_{operation_id}"
        
        # Eşzamanlı hata yönetimi
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for i in range(30):
                future = executor.submit(
                    bridge._safe_operation,
                    lambda x=i: error_prone_operation(x),
                    default_value=f"fallback_{i}"
                )
                futures.append(future)
            
            results = [future.result() for future in futures]
        
        # Tüm operasyonlar tamamlanmalı (hata olsa bile)
        assert len(results) == 30
        print("Concurrent Error Handling: PASSED")
    
    def test_error_logging_and_monitoring(self, bridge):
        """Hata loglama ve izleme testi"""
        # Hata loglama test et
        test_error = Exception("Test error for logging")
        
        with patch('logging.error') as mock_logger:
            bridge._log_error("test_operation", test_error)
            
            # Loglama çağrıldı mı kontrol et
            mock_logger.assert_called_once()
            print("Error Logging and Monitoring: PASSED")


if __name__ == "__main__":
    # Test çalıştır
    pytest.main([__file__, "-v", "--tb=short"]) 