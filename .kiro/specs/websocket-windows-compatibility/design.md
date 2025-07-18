# Design Document

## Overview

This design addresses the WebSocket compatibility issues on Windows systems in the Collective Memory API server. The current implementation has WebSocket support completely disabled due to Windows-specific socket handling problems. The solution involves implementing a robust, Windows-compatible WebSocket architecture using Flask-SocketIO with proper Windows-specific configurations, fallback mechanisms, and error handling.

## Architecture

### Current Issues
- WebSocket support completely disabled on Windows (`self.socketio = None`)
- No fallback mechanism for real-time features
- Missing Windows-specific socket configuration
- No error handling for Windows networking constraints
- Real-time features (search updates, indexing progress, team collaboration) are non-functional

### Proposed Solution
- Implement conditional WebSocket initialization with Windows-specific settings
- Add transport method fallbacks (WebSocket → Long Polling → XHR Polling)
- Implement robust connection management with automatic reconnection
- Add Windows-specific networking configuration
- Provide graceful degradation when WebSocket is unavailable

## Components and Interfaces

### 1. Windows-Compatible WebSocket Manager
```python
class WindowsCompatibleSocketIO:
    def __init__(self, app, data_folder):
        self.app = app
        self.data_folder = data_folder
        self.socketio = None
        self.is_windows = platform.system() == 'Windows'
        self.websocket_enabled = False
        
    def initialize_socketio(self):
        """Initialize SocketIO with Windows-compatible settings"""
        try:
            if self.is_windows:
                # Windows-specific configuration
                socketio_config = {
                    'cors_allowed_origins': ["http://localhost:3000", "http://127.0.0.1:3000"],
                    'async_mode': 'threading',  # More stable on Windows
                    'transports': ['websocket', 'polling'],  # Fallback support
                    'ping_timeout': 60,
                    'ping_interval': 25,
                    'max_http_buffer_size': 1000000,
                    'allow_upgrades': True,
                    'http_compression': True,
                    'compression': True
                }
            else:
                # Standard configuration for other platforms
                socketio_config = {
                    'cors_allowed_origins': ["http://localhost:3000", "http://127.0.0.1:3000"],
                    'async_mode': 'eventlet',
                    'transports': ['websocket', 'polling']
                }
                
            self.socketio = SocketIO(self.app, **socketio_config)
            self.websocket_enabled = True
            logger.info(f"WebSocket initialized successfully (Windows: {self.is_windows})")
            
        except Exception as e:
            logger.warning(f"WebSocket initialization failed: {e}")
            self._setup_fallback_mode()
```

### 2. Connection Management
```python
class WebSocketConnectionManager:
    def __init__(self, socketio_manager):
        self.socketio_manager = socketio_manager
        self.connected_clients = set()
        self.reconnection_attempts = {}
        
    def handle_connect(self, sid):
        """Handle client connection with Windows-specific logic"""
        self.connected_clients.add(sid)
        logger.info(f"Client connected: {sid}")
        
        # Send initial system status
        self.emit_to_client(sid, 'system_status', self._get_system_status())
        
    def handle_disconnect(self, sid):
        """Handle client disconnection"""
        self.connected_clients.discard(sid)
        logger.info(f"Client disconnected: {sid}")
        
    def emit_to_all(self, event, data):
        """Emit event to all connected clients with error handling"""
        if not self.socketio_manager.websocket_enabled:
            return self._fallback_broadcast(event, data)
            
        try:
            self.socketio_manager.socketio.emit(event, data)
        except Exception as e:
            logger.error(f"WebSocket emit failed: {e}")
            self._fallback_broadcast(event, data)
```

### 3. Transport Fallback System
```python
class TransportFallbackManager:
    def __init__(self):
        self.fallback_mode = False
        self.polling_clients = {}
        
    def enable_fallback_mode(self):
        """Enable polling-based fallback for real-time features"""
        self.fallback_mode = True
        logger.info("WebSocket fallback mode enabled - using HTTP polling")
        
    def register_polling_client(self, client_id):
        """Register client for polling-based updates"""
        self.polling_clients[client_id] = {
            'last_poll': datetime.now(timezone.utc),
            'pending_events': []
        }
        
    def add_pending_event(self, event_type, data):
        """Add event to pending queue for polling clients"""
        for client_id in self.polling_clients:
            self.polling_clients[client_id]['pending_events'].append({
                'type': event_type,
                'data': data,
                'timestamp': datetime.now(timezone.utc).isoformat()
            })
```

### 4. Windows-Specific Configuration
```python
class WindowsNetworkingConfig:
    @staticmethod
    def get_windows_socket_config():
        """Get Windows-specific socket configuration"""
        return {
            'SO_REUSEADDR': True,
            'TCP_NODELAY': True,
            'SO_KEEPALIVE': True,
            'TCP_KEEPIDLE': 600,
            'TCP_KEEPINTVL': 60,
            'TCP_KEEPCNT': 3
        }
        
    @staticmethod
    def configure_windows_firewall_exception():
        """Configure Windows Firewall exception for WebSocket port"""
        try:
            import subprocess
            port = os.environ.get('WEBSOCKET_PORT', '8000')
            cmd = f'netsh advfirewall firewall add rule name="Collective Memory WebSocket" dir=in action=allow protocol=TCP localport={port}'
            subprocess.run(cmd, shell=True, check=False)
            logger.info(f"Windows Firewall exception configured for port {port}")
        except Exception as e:
            logger.warning(f"Could not configure Windows Firewall: {e}")
```

## Data Models

### WebSocket Event Models
```python
@dataclass
class WebSocketEvent:
    event_type: str
    data: Dict[str, Any]
    timestamp: str
    client_id: Optional[str] = None
    room: Optional[str] = None

@dataclass
class SystemStatusEvent(WebSocketEvent):
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    indexing_status: Dict[str, Any]

@dataclass
class SearchEvent(WebSocketEvent):
    query: str
    results_count: int
    search_time: float
    user_session: str

@dataclass
class IndexingEvent(WebSocketEvent):
    progress: int
    current_file: str
    processed_files: int
    total_files: int
```

### Connection State Management
```python
@dataclass
class ClientConnection:
    sid: str
    connected_at: datetime
    last_ping: datetime
    transport_method: str  # 'websocket', 'polling', 'xhr-polling'
    user_agent: str
    ip_address: str
    room_memberships: List[str]
```

## Error Handling

### Windows-Specific Error Handling
```python
class WindowsWebSocketErrorHandler:
    def __init__(self):
        self.error_patterns = {
            'WSAECONNRESET': 'Connection reset by peer - likely firewall issue',
            'WSAECONNREFUSED': 'Connection refused - check port availability',
            'WSAENETUNREACH': 'Network unreachable - check network configuration',
            'WSAETIMEDOUT': 'Connection timeout - adjust timeout settings'
        }
        
    def handle_windows_socket_error(self, error):
        """Handle Windows-specific socket errors"""
        error_str = str(error)
        for pattern, description in self.error_patterns.items():
            if pattern in error_str:
                logger.error(f"Windows socket error: {description}")
                return self._suggest_resolution(pattern)
        
        logger.error(f"Unknown Windows socket error: {error}")
        return self._generic_fallback()
        
    def _suggest_resolution(self, error_pattern):
        """Suggest resolution based on error pattern"""
        resolutions = {
            'WSAECONNRESET': 'Try disabling Windows Firewall temporarily or add exception',
            'WSAECONNREFUSED': 'Check if another application is using the port',
            'WSAENETUNREACH': 'Verify network adapter configuration',
            'WSAETIMEDOUT': 'Increase connection timeout values'
        }
        return resolutions.get(error_pattern, 'Enable fallback polling mode')
```

### Graceful Degradation
```python
def setup_graceful_degradation(self):
    """Setup fallback mechanisms when WebSocket fails"""
    
    # HTTP polling endpoints for real-time features
    @self.app.route('/api/events/poll', methods=['GET'])
    def poll_events():
        """Polling endpoint for clients without WebSocket support"""
        client_id = request.args.get('client_id')
        last_poll = request.args.get('last_poll')
        
        if not client_id:
            return jsonify({'error': 'client_id required'}), 400
            
        # Get pending events for this client
        events = self.fallback_manager.get_pending_events(client_id, last_poll)
        
        return jsonify({
            'events': events,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'polling_interval': 5000  # 5 seconds
        })
    
    # Server-Sent Events as another fallback
    @self.app.route('/api/events/stream')
    def event_stream():
        """Server-Sent Events stream for real-time updates"""
        def generate():
            while True:
                # Get latest system events
                events = self._get_recent_events()
                for event in events:
                    yield f"data: {json.dumps(event)}\n\n"
                time.sleep(2)
                
        return Response(generate(), mimetype='text/plain')
```

## Testing Strategy

### Unit Tests
- Test Windows-specific WebSocket configuration
- Test transport fallback mechanisms
- Test error handling for Windows socket errors
- Test connection management and reconnection logic

### Integration Tests
- Test WebSocket functionality on Windows 10 and Windows 11
- Test behavior with Windows Firewall enabled/disabled
- Test corporate network environments with proxies
- Test fallback mode when WebSocket is unavailable

### Windows-Specific Tests
```python
class TestWindowsWebSocketCompatibility:
    def test_windows_socketio_initialization(self):
        """Test SocketIO initializes correctly on Windows"""
        
    def test_windows_firewall_compatibility(self):
        """Test WebSocket works with Windows Firewall"""
        
    def test_corporate_proxy_compatibility(self):
        """Test WebSocket works through corporate proxies"""
        
    def test_transport_fallback_on_windows(self):
        """Test fallback to polling when WebSocket fails"""
        
    def test_windows_socket_error_handling(self):
        """Test handling of Windows-specific socket errors"""
```

### Performance Tests
- Test WebSocket performance on Windows vs other platforms
- Test memory usage with long-running WebSocket connections
- Test connection stability under load
- Test reconnection performance after network interruptions