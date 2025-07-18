#!/usr/bin/env python3
"""
Test suite for WebSocket Windows Compatibility
Tests Windows-specific WebSocket functionality and fallback mechanisms
"""

import unittest
import sys
import os
import time
import threading
import platform
from unittest.mock import Mock, patch, MagicMock

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from websocket_manager import WindowsCompatibleSocketIO, WebSocketConfig, WebSocketConnectionManager
from windows_websocket_errors import WindowsWebSocketErrorHandler, WindowsNetworkingConfig


class TestWebSocketConfig(unittest.TestCase):
    """Test WebSocket configuration"""
    
    def test_default_config(self):
        """Test default WebSocket configuration"""
        config = WebSocketConfig()
        
        self.assertEqual(config.async_mode, "threading")
        self.assertEqual(config.ping_timeout, 60)
        self.assertEqual(config.ping_interval, 25)
        self.assertIsNotNone(config.cors_allowed_origins)
        self.assertIn("http://localhost:3000", config.cors_allowed_origins)
    
    def test_custom_config(self):
        """Test custom WebSocket configuration"""
        config = WebSocketConfig(
            async_mode="eventlet",
            ping_timeout=120,
            ping_interval=30,
            cors_allowed_origins=["http://test.com"]
        )
        
        self.assertEqual(config.async_mode, "eventlet")
        self.assertEqual(config.ping_timeout, 120)
        self.assertEqual(config.ping_interval, 30)
        self.assertEqual(config.cors_allowed_origins, ["http://test.com"])


class TestWindowsCompatibleSocketIO(unittest.TestCase):
    """Test Windows-compatible SocketIO implementation"""
    
    def setUp(self):
        """Set up test environment"""
        self.mock_app = Mock()
        self.config = WebSocketConfig()
    
    @patch('websocket_manager.SocketIO')
    def test_initialization_success(self, mock_socketio):
        """Test successful SocketIO initialization"""
        mock_socketio_instance = Mock()
        mock_socketio.return_value = mock_socketio_instance
        
        manager = WindowsCompatibleSocketIO(self.mock_app, self.config)
        
        self.assertIsNotNone(manager.socketio)
        self.assertEqual(len(manager.connections), 0)
        self.assertEqual(len(manager.event_handlers), 0)
    
    @patch('websocket_manager.SocketIO')
    def test_initialization_failure(self, mock_socketio):
        """Test SocketIO initialization failure"""
        mock_socketio.side_effect = Exception("SocketIO initialization failed")
        
        with self.assertRaises(Exception):
            WindowsCompatibleSocketIO(self.mock_app, self.config)
    
    def test_windows_detection(self):
        """Test Windows platform detection"""
        manager = WindowsCompatibleSocketIO(self.mock_app, self.config)
        
        # This test will pass on both Windows and non-Windows systems
        self.assertIsInstance(manager.is_windows, bool)
    
    def test_connection_management(self):
        """Test connection management functionality"""
        manager = WindowsCompatibleSocketIO(self.mock_app, self.config)
        
        # Test connection count
        self.assertEqual(manager.get_connection_count(), 0)
        
        # Test connection info
        self.assertIsNone(manager.get_connection_info("nonexistent"))
        
        # Test connection status
        self.assertFalse(manager.is_connected("nonexistent"))
    
    def test_event_handler_registration(self):
        """Test event handler registration"""
        manager = WindowsCompatibleSocketIO(self.mock_app, self.config)
        
        def test_handler(data):
            pass
        
        manager.register_event_handler("test_event", test_handler)
        
        self.assertIn("test_event", manager.event_handlers)
        self.assertEqual(manager.event_handlers["test_event"], test_handler)
    
    def test_status_information(self):
        """Test status information retrieval"""
        manager = WindowsCompatibleSocketIO(self.mock_app, self.config)
        
        status = manager.get_status()
        
        self.assertIn("enabled", status)
        self.assertIn("platform", status)
        self.assertIn("async_mode", status)
        self.assertIn("connection_count", status)
        self.assertIn("is_windows", status)


class TestWebSocketConnectionManager(unittest.TestCase):
    """Test WebSocket connection manager"""
    
    def setUp(self):
        """Set up test environment"""
        self.mock_socketio_manager = Mock()
        self.mock_socketio_manager.get_all_connections.return_value = {}
        self.mock_socketio_manager.get_connection_count.return_value = 0
    
    def test_initialization(self):
        """Test connection manager initialization"""
        manager = WebSocketConnectionManager(self.mock_socketio_manager)
        
        self.assertIsNotNone(manager.socketio_manager)
        self.assertEqual(len(manager.sessions), 0)
        self.assertTrue(manager.running)
    
    def test_session_management(self):
        """Test session management functionality"""
        manager = WebSocketConnectionManager(self.mock_socketio_manager)
        
        # Test session creation
        session_id = manager.create_session("test_sid", {"user": "test"})
        self.assertIsNotNone(session_id)
        self.assertIn("test_sid", manager.sessions)
        
        # Test session retrieval
        session = manager.get_session("test_sid")
        self.assertIsNotNone(session)
        self.assertEqual(session["user_data"]["user"], "test")
        
        # Test session count
        self.assertEqual(manager.get_session_count(), 1)
        
        # Test session removal
        manager.remove_session("test_sid")
        self.assertNotIn("test_sid", manager.sessions)
        self.assertEqual(manager.get_session_count(), 0)
    
    def test_health_monitoring(self):
        """Test health monitoring functionality"""
        manager = WebSocketConnectionManager(self.mock_socketio_manager)
        
        # Test health check
        manager._perform_health_check()
        
        # Verify cleanup was called
        self.mock_socketio_manager.cleanup_inactive_connections.assert_called_once()
    
    def test_stop_functionality(self):
        """Test stop functionality"""
        manager = WebSocketConnectionManager(self.mock_socketio_manager)
        
        # Stop the manager
        manager.stop()
        
        self.assertFalse(manager.running)


class TestWindowsWebSocketErrorHandler(unittest.TestCase):
    """Test Windows WebSocket error handler"""
    
    def setUp(self):
        """Set up test environment"""
        self.error_handler = WindowsWebSocketErrorHandler()
    
    def test_initialization(self):
        """Test error handler initialization"""
        self.assertIsNotNone(self.error_handler.error_patterns)
        self.assertIsNotNone(self.error_handler.solution_registry)
        self.assertEqual(len(self.error_handler.error_history), 0)
    
    def test_error_analysis(self):
        """Test error analysis functionality"""
        error_message = "Connection refused"
        error = self.error_handler.analyze_error(error_message, "10061")
        
        self.assertEqual(error.error_message, error_message)
        self.assertEqual(error.error_code, "10061")
        self.assertEqual(error.error_type, "connection_refused")
        self.assertEqual(error.severity, "HIGH")
        self.assertIsNotNone(error.suggested_solutions)
    
    def test_error_pattern_matching(self):
        """Test error pattern matching"""
        test_cases = [
            ("Connection refused", "connection_refused"),
            ("Connection timed out", "timeout"),
            ("Permission denied", "firewall_blocked"),
            ("Proxy connection failed", "proxy_issues"),
            ("Too many open files", "socket_limit"),
            ("Address already in use", "port_in_use"),
            ("Name or service not known", "dns_resolution"),
            ("SSL handshake failed", "ssl_tls")
        ]
        
        for error_message, expected_type in test_cases:
            error = self.error_handler.analyze_error(error_message)
            self.assertEqual(error.error_type, expected_type)
    
    def test_error_history(self):
        """Test error history functionality"""
        # Add some errors
        self.error_handler.analyze_error("Connection refused")
        self.error_handler.analyze_error("Connection timed out")
        
        # Test history retrieval
        history = self.error_handler.get_error_history(hours=1)
        self.assertEqual(len(history), 2)
        
        # Test error summary
        summary = self.error_handler.get_error_summary()
        self.assertEqual(summary["total_errors"], 2)
        self.assertIn("error_types", summary)
    
    def test_error_clearing(self):
        """Test error history clearing"""
        self.error_handler.analyze_error("Connection refused")
        self.assertEqual(len(self.error_handler.error_history), 1)
        
        self.error_handler.clear_error_history()
        self.assertEqual(len(self.error_handler.error_history), 0)
    
    def test_diagnostic_info(self):
        """Test diagnostic information retrieval"""
        diagnostic_info = self.error_handler.get_diagnostic_info()
        
        self.assertIn("platform", diagnostic_info)
        self.assertIn("network", diagnostic_info)
        self.assertIn("firewall", diagnostic_info)
        self.assertIn("proxy", diagnostic_info)
        self.assertIn("error_summary", diagnostic_info)


class TestWindowsNetworkingConfig(unittest.TestCase):
    """Test Windows networking configuration"""
    
    def setUp(self):
        """Set up test environment"""
        self.networking_config = WindowsNetworkingConfig()
    
    def test_initialization(self):
        """Test networking config initialization"""
        self.assertIsInstance(self.networking_config.is_windows, bool)
    
    @patch('socket.socket')
    def test_tcp_keepalive_configuration(self, mock_socket):
        """Test TCP keepalive configuration"""
        mock_socket_obj = Mock()
        
        self.networking_config.configure_tcp_keepalive(mock_socket_obj)
        
        # Verify socket options were set
        mock_socket_obj.setsockopt.assert_called()
    
    @patch('socket.socket')
    def test_tcp_nodelay_configuration(self, mock_socket):
        """Test TCP nodelay configuration"""
        mock_socket_obj = Mock()
        
        self.networking_config.configure_tcp_nodelay(mock_socket_obj)
        
        # Verify socket options were set
        mock_socket_obj.setsockopt.assert_called()
    
    @patch('subprocess.run')
    def test_firewall_exception_management(self, mock_run):
        """Test firewall exception management"""
        mock_run.return_value.returncode = 0
        
        # Test adding firewall exception
        result = self.networking_config.add_firewall_exception("/path/to/app", "Test App")
        self.assertTrue(result)
        
        # Test removing firewall exception
        result = self.networking_config.remove_firewall_exception("Test App")
        self.assertTrue(result)
    
    @patch('subprocess.run')
    def test_network_adapters_retrieval(self, mock_run):
        """Test network adapters information retrieval"""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "Ethernet adapter Local Area Connection:\n   IPv4 Address: 192.168.1.100"
        
        adapters = self.networking_config.get_network_adapters()
        
        self.assertIsInstance(adapters, list)
    
    def test_connectivity_testing(self):
        """Test connectivity testing"""
        result = self.networking_config.test_connectivity("localhost", 80)
        
        self.assertIn("success", result)
        self.assertIn("error", result)
        self.assertIn("response_time", result)
        self.assertIn("timestamp", result)


class TestWebSocketIntegration(unittest.TestCase):
    """Integration tests for WebSocket functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.mock_app = Mock()
        self.config = WebSocketConfig()
    
    @patch('websocket_manager.SocketIO')
    def test_full_websocket_workflow(self, mock_socketio):
        """Test complete WebSocket workflow"""
        mock_socketio_instance = Mock()
        mock_socketio.return_value = mock_socketio_instance
        
        # Initialize WebSocket manager
        manager = WindowsCompatibleSocketIO(self.mock_app, self.config)
        
        # Test connection manager
        connection_manager = WebSocketConnectionManager(manager)
        
        # Test error handler
        error_handler = WindowsWebSocketErrorHandler()
        
        # Test networking config
        networking_config = WindowsNetworkingConfig()
        
        # Verify all components work together
        self.assertIsNotNone(manager)
        self.assertIsNotNone(connection_manager)
        self.assertIsNotNone(error_handler)
        self.assertIsNotNone(networking_config)
    
    def test_error_handling_integration(self):
        """Test error handling integration"""
        error_handler = WindowsWebSocketErrorHandler()
        
        # Simulate various error scenarios
        errors = [
            "Connection refused by target machine",
            "Operation timed out after 30 seconds",
            "Firewall blocked connection attempt",
            "Proxy authentication required",
            "Too many open socket connections"
        ]
        
        for error_message in errors:
            error = error_handler.analyze_error(error_message)
            self.assertIsNotNone(error.error_type)
            self.assertIsNotNone(error.suggested_solutions)
            self.assertGreater(len(error.suggested_solutions), 0)


class TestWebSocketPerformance(unittest.TestCase):
    """Performance tests for WebSocket functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.mock_app = Mock()
        self.config = WebSocketConfig()
    
    @patch('websocket_manager.SocketIO')
    def test_connection_cleanup_performance(self, mock_socketio):
        """Test connection cleanup performance"""
        mock_socketio_instance = Mock()
        mock_socketio.return_value = mock_socketio_instance
        
        manager = WindowsCompatibleSocketIO(self.mock_app, self.config)
        
        # Simulate many connections
        for i in range(100):
            manager.connections[f"sid_{i}"] = Mock()
        
        start_time = time.time()
        manager.cleanup_inactive_connections()
        cleanup_time = time.time() - start_time
        
        # Cleanup should be fast (< 100ms)
        self.assertLess(cleanup_time, 0.1)
    
    def test_error_analysis_performance(self):
        """Test error analysis performance"""
        error_handler = WindowsWebSocketErrorHandler()
        
        # Test multiple error analyses
        start_time = time.time()
        
        for i in range(100):
            error_handler.analyze_error(f"Test error {i}")
        
        analysis_time = time.time() - start_time
        
        # Error analysis should be fast (< 1 second for 100 errors)
        self.assertLess(analysis_time, 1.0)


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2) 