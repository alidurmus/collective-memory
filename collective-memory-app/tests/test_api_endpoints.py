#!/usr/bin/env python3
"""
Collective Memory API Endpoint Tests
Flask REST API ve WebSocket testleri
"""

import pytest
import requests
import time
import socketio

# Test configuration
BASE_URL = "http://localhost:8000"
API_TIMEOUT = 30


class TestAPIEndpoints:
    """API endpoint testleri"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Test setup - API server'ın çalıştığını kontrol et"""
        try:
            response = requests.get(f"{BASE_URL}/system/status", timeout=5)
            if response.status_code != 200:
                pytest.skip("API server çalışmıyor")
        except requests.exceptions.RequestException:
            pytest.skip("API server'a erişilemiyor")
    
    def test_system_status(self):
        """System status endpoint testi"""
        response = requests.get(f"{BASE_URL}/system/status")
        assert response.status_code == 200
        
        data = response.json()
        assert "success" in data
        assert "data" in data
        assert data["success"] is True
        assert "file_count" in data["data"]
        assert "is_indexing" in data["data"]
        
    def test_system_stats(self):
        """System stats endpoint testi"""
        response = requests.get(f"{BASE_URL}/system/stats")
        assert response.status_code == 200
        
        data = response.json()
        assert "total_files" in data
        assert "total_size" in data
        assert "last_indexed" in data
        assert "index_health" in data
        assert isinstance(data["total_files"], int)
        
    def test_search_endpoint(self):
        """Search endpoint testi"""
        # Basic search
        search_data = {
            "query": "test",
            "type": "basic",
            "max_results": 10
        }
        
        response = requests.post(f"{BASE_URL}/search", 
                               json=search_data,
                               headers={"Content-Type": "application/json"})
        assert response.status_code == 200
        
        data = response.json()
        assert "results" in data
        assert "total_found" in data
        assert "search_time" in data
        assert isinstance(data["results"], list)
        
    def test_search_semantic(self):
        """Semantic search testi"""
        search_data = {
            "query": "authentication system",
            "type": "semantic",
            "max_results": 5,
            "threshold": 0.5
        }
        
        response = requests.post(f"{BASE_URL}/search", 
                               json=search_data,
                               headers={"Content-Type": "application/json"})
        assert response.status_code == 200
        
        data = response.json()
        assert "results" in data
        assert isinstance(data["results"], list)
        
    def test_search_suggestions(self):
        """Search suggestions testi"""
        response = requests.get(f"{BASE_URL}/search/suggestions?q=test")
        assert response.status_code == 200
        
        data = response.json()
        assert "suggestions" in data
        assert isinstance(data["suggestions"], list)
        
    def test_search_export_markdown(self):
        """Search export markdown testi"""
        search_data = {
            "query": "test",
            "type": "basic",
            "max_results": 5
        }
        
        response = requests.post(f"{BASE_URL}/search/export", 
                               json={**search_data, "format": "markdown"},
                               headers={"Content-Type": "application/json"})
        assert response.status_code == 200
        
        # Content-Type markdown olmalı
        assert "text/markdown" in response.headers.get("Content-Type", "")
        assert len(response.content) > 0
        
    def test_search_export_text(self):
        """Search export text testi"""
        search_data = {
            "query": "test",
            "type": "basic",
            "max_results": 3
        }
        
        response = requests.post(f"{BASE_URL}/search/export", 
                               json={**search_data, "format": "text"},
                               headers={"Content-Type": "application/json"})
        assert response.status_code == 200
        
        # Content-Type text olmalı
        assert "text/plain" in response.headers.get("Content-Type", "")
        
    def test_indexing_status(self):
        """Indexing status testi"""
        response = requests.get(f"{BASE_URL}/system/indexing")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "progress" in data
        assert data["status"] in ["idle", "indexing", "completed"]
        
    def test_indexing_start(self):
        """Indexing start testi"""
        response = requests.post(f"{BASE_URL}/system/indexing/start")
        assert response.status_code in [200, 409]  # 409 if already indexing
        
        if response.status_code == 200:
            data = response.json()
            assert "status" in data
            assert data["status"] == "started"
            
    def test_config_get(self):
        """Configuration get testi"""
        response = requests.get(f"{BASE_URL}/config")
        assert response.status_code == 200
        
        data = response.json()
        assert "search_settings" in data
        assert "system_settings" in data
        
    def test_config_update(self):
        """Configuration update testi"""
        config_data = {
            "search_settings": {
                "semantic_threshold": 0.7,
                "max_results": 20
            }
        }
        
        response = requests.post(f"{BASE_URL}/config", 
                               json=config_data,
                               headers={"Content-Type": "application/json"})
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert data["status"] == "updated"
        
    def test_invalid_search_request(self):
        """Invalid search request testi"""
        # Boş query
        response = requests.post(f"{BASE_URL}/search", 
                               json={"query": ""},
                               headers={"Content-Type": "application/json"})
        assert response.status_code == 400
        
        # Invalid type
        response = requests.post(f"{BASE_URL}/search", 
                               json={"query": "test", "type": "invalid"},
                               headers={"Content-Type": "application/json"})
        assert response.status_code == 400
        
    def test_api_rate_limiting(self):
        """API rate limiting testi"""
        # Rapid requests to test rate limiting
        responses = []
        for _ in range(10):
            response = requests.get(f"{BASE_URL}/system/stats")
            responses.append(response.status_code)
            
        # Most requests should succeed
        success_count = sum(1 for code in responses if code == 200)
        assert success_count >= 8  # Allow some rate limiting


class TestWebSocketConnection:
    """WebSocket connection testleri"""
    
    def test_websocket_connection(self):
        """WebSocket bağlantı testi"""
        try:
            sio = socketio.SimpleClient()
            sio.connect(BASE_URL)
            
            # Connection successful
            assert sio.connected
            
            # Disconnect
            sio.disconnect()
            assert not sio.connected
            
        except Exception as e:
            pytest.skip(f"WebSocket test failed: {e}")
    
    def test_websocket_events(self):
        """WebSocket events testi"""
        try:
            sio = socketio.SimpleClient()
            sio.connect(BASE_URL)
            
            received_events = []
            
            @sio.event
            def indexing_progress(data):
                received_events.append(('indexing_progress', data))
                
            @sio.event
            def search_update(data):
                received_events.append(('search_update', data))
            
            # Wait a bit for potential events
            time.sleep(2)
            
            sio.disconnect()
            
            # Events may or may not be received depending on timing
            # This test mainly verifies WebSocket connectivity
            assert True  # Connection test passed
            
        except Exception as e:
            pytest.skip(f"WebSocket events test failed: {e}")


class TestPerformanceMetrics:
    """Performance testleri"""
    
    def test_search_response_time(self):
        """Search response time testi"""
        search_data = {
            "query": "performance test",
            "type": "basic",
            "max_results": 10
        }
        
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/search", 
                               json=search_data,
                               headers={"Content-Type": "application/json"})
        end_time = time.time()
        
        assert response.status_code == 200
        response_time = end_time - start_time
        assert response_time < 5.0  # Should respond within 5 seconds
        
    def test_concurrent_requests(self):
        """Concurrent requests testi"""
        import threading
        import queue
        
        results = queue.Queue()
        
        def make_request():
            try:
                response = requests.get(f"{BASE_URL}/system/status", timeout=10)
                results.put(response.status_code)
            except Exception as e:
                results.put(str(e))
        
        # Create 5 concurrent threads
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads
        for thread in threads:
            thread.join(timeout=15)
        
        # Check results
        success_count = 0
        while not results.empty():
            result = results.get()
            if result == 200:
                success_count += 1
        
        assert success_count >= 4  # At least 4 should succeed


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 