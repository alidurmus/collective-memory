#!/usr/bin/env python3
"""
Windows-Compatible WebSocket Manager for Collective Memory API
Handles WebSocket connections with Windows-specific optimizations and fallback mechanisms
"""

import os
import sys
import logging
import platform
import threading
import time
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from datetime import datetime, timezone

from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import request

logger = logging.getLogger(__name__)


@dataclass
class WebSocketConfig:
    """WebSocket configuration settings"""
    async_mode: str = "threading"
    cors_allowed_origins: List[str] = None
    ping_timeout: int = 60
    ping_interval: int = 25
    max_http_buffer_size: int = 1000000
    logger: bool = False
    engineio_logger: bool = False
    
    def __post_init__(self):
        if self.cors_allowed_origins is None:
            self.cors_allowed_origins = ["http://localhost:3000", "http://127.0.0.1:3000"]


@dataclass
class ConnectionInfo:
    """Connection information for tracking"""
    sid: str
    connected_at: datetime
    last_activity: datetime
    room: str = "general"
    user_agent: str = ""
    ip_address: str = ""


class WindowsCompatibleSocketIO:
    """Windows-compatible SocketIO implementation with fallback mechanisms"""
    
    def __init__(self, app, config: WebSocketConfig = None):
        self.app = app
        self.config = config or WebSocketConfig()
        self.socketio = None
        self.connections: Dict[str, ConnectionInfo] = {}
        self.event_handlers: Dict[str, Callable] = {}
        self.is_windows = platform.system().lower() == "windows"
        
        # Windows-specific settings
        if self.is_windows:
            self._configure_windows_settings()
        
        self._initialize_socketio()
        self._setup_default_handlers()
    
    def _configure_windows_settings(self):
        """Configure Windows-specific WebSocket settings"""
        logger.info("Configuring Windows-specific WebSocket settings")
        
        # Use threading async mode for Windows compatibility
        self.config.async_mode = "threading"
        
        # Increase ping intervals for Windows network stability
        self.config.ping_timeout = 120
        self.config.ping_interval = 30
        
        # Windows-specific transport fallback order
        self.transport_fallback_order = [
            "websocket",
            "polling",
            "xhr-polling"
        ]
        
        logger.info(f"Windows WebSocket config: async_mode={self.config.async_mode}, "
                   f"ping_timeout={self.config.ping_timeout}, ping_interval={self.config.ping_interval}")
    
    def _initialize_socketio(self):
        """Initialize SocketIO with Windows-compatible configuration"""
        try:
            self.socketio = SocketIO(
                self.app,
                async_mode=self.config.async_mode,
                cors_allowed_origins=self.config.cors_allowed_origins,
                ping_timeout=self.config.ping_timeout,
                ping_interval=self.config.ping_interval,
                max_http_buffer_size=self.config.max_http_buffer_size,
                logger=self.config.logger,
                engineio_logger=self.config.engineio_logger
            )
            
            logger.info(f"SocketIO initialized successfully with async_mode: {self.config.async_mode}")
            
        except Exception as e:
            logger.error(f"Failed to initialize SocketIO: {e}")
            self.socketio = None
            raise
    
    def _setup_default_handlers(self):
        """Setup default WebSocket event handlers"""
        if not self.socketio:
            return
        
        @self.socketio.on("connect")
        def handle_connect():
            self._handle_connect()
        
        @self.socketio.on("disconnect")
        def handle_disconnect():
            self._handle_disconnect()
        
        @self.socketio.on("join_room")
        def handle_join_room(data):
            self._handle_join_room(data)
        
        @self.socketio.on("leave_room")
        def handle_leave_room(data):
            self._handle_leave_room(data)
        
        @self.socketio.on("ping")
        def handle_ping():
            self._handle_ping()
    
    def _handle_connect(self):
        """Handle client connection"""
        try:
            sid = request.sid
            connection_info = ConnectionInfo(
                sid=sid,
                connected_at=datetime.now(timezone.utc),
                last_activity=datetime.now(timezone.utc),
                user_agent=request.headers.get("User-Agent", ""),
                ip_address=request.remote_addr
            )
            
            self.connections[sid] = connection_info
            
            logger.info(f"Client connected: {sid} from {request.remote_addr}")
            emit("connected", {
                "message": "Connected to Collective Memory API",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "platform": platform.system(),
                "websocket_enabled": True
            })
            
            # Emit connection event to other handlers
            self._emit_event("client_connected", {
                "sid": sid,
                "ip_address": request.remote_addr,
                "user_agent": request.headers.get("User-Agent", "")
            })
            
        except Exception as e:
            logger.error(f"Error handling connect: {e}")
    
    def _handle_disconnect(self):
        """Handle client disconnection"""
        try:
            sid = request.sid
            if sid in self.connections:
                connection_info = self.connections.pop(sid)
                logger.info(f"Client disconnected: {sid} (connected for "
                           f"{(datetime.now(timezone.utc) - connection_info.connected_at).total_seconds():.1f}s)")
                
                # Emit disconnection event to other handlers
                self._emit_event("client_disconnected", {
                    "sid": sid,
                    "duration": (datetime.now(timezone.utc) - connection_info.connected_at).total_seconds()
                })
            
        except Exception as e:
            logger.error(f"Error handling disconnect: {e}")
    
    def _handle_join_room(self, data):
        """Handle room join request"""
        try:
            sid = request.sid
            room = data.get("room", "general")
            
            if sid in self.connections:
                self.connections[sid].room = room
                self.connections[sid].last_activity = datetime.now(timezone.utc)
            
            join_room(room)
            emit("joined_room", {
                "room": room,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            
            logger.info(f"Client {sid} joined room: {room}")
            
        except Exception as e:
            logger.error(f"Error handling join_room: {e}")
    
    def _handle_leave_room(self, data):
        """Handle room leave request"""
        try:
            sid = request.sid
            room = data.get("room", "general")
            
            if sid in self.connections:
                self.connections[sid].last_activity = datetime.now(timezone.utc)
            
            leave_room(room)
            emit("left_room", {
                "room": room,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            
            logger.info(f"Client {sid} left room: {room}")
            
        except Exception as e:
            logger.error(f"Error handling leave_room: {e}")
    
    def _handle_ping(self):
        """Handle ping request"""
        try:
            sid = request.sid
            if sid in self.connections:
                self.connections[sid].last_activity = datetime.now(timezone.utc)
            
            emit("pong", {
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            
        except Exception as e:
            logger.error(f"Error handling ping: {e}")
    
    def _emit_event(self, event_name: str, data: Dict):
        """Emit event to registered handlers"""
        if event_name in self.event_handlers:
            try:
                self.event_handlers[event_name](data)
            except Exception as e:
                logger.error(f"Error in event handler {event_name}: {e}")
    
    def register_event_handler(self, event_name: str, handler: Callable):
        """Register custom event handler"""
        self.event_handlers[event_name] = handler
        logger.info(f"Registered event handler for: {event_name}")
    
    def emit_to_room(self, room: str, event: str, data: Dict):
        """Emit event to specific room"""
        if self.socketio:
            try:
                self.socketio.emit(event, data, room=room)
                logger.debug(f"Emitted {event} to room {room}")
            except Exception as e:
                logger.error(f"Error emitting to room {room}: {e}")
    
    def emit_to_all(self, event: str, data: Dict):
        """Emit event to all connected clients"""
        if self.socketio:
            try:
                self.socketio.emit(event, data)
                logger.debug(f"Emitted {event} to all clients")
            except Exception as e:
                logger.error(f"Error emitting to all clients: {e}")
    
    def get_connection_count(self) -> int:
        """Get current connection count"""
        return len(self.connections)
    
    def get_connection_info(self, sid: str) -> Optional[ConnectionInfo]:
        """Get connection information for specific client"""
        return self.connections.get(sid)
    
    def get_all_connections(self) -> Dict[str, ConnectionInfo]:
        """Get all connection information"""
        return self.connections.copy()
    
    def is_connected(self, sid: str) -> bool:
        """Check if client is connected"""
        return sid in self.connections
    
    def cleanup_inactive_connections(self, timeout_seconds: int = 300):
        """Clean up inactive connections"""
        if not self.socketio:
            return
        
        current_time = datetime.now(timezone.utc)
        inactive_sids = []
        
        for sid, connection_info in self.connections.items():
            if (current_time - connection_info.last_activity).total_seconds() > timeout_seconds:
                inactive_sids.append(sid)
        
        for sid in inactive_sids:
            self.connections.pop(sid, None)
            logger.info(f"Cleaned up inactive connection: {sid}")
    
    def get_status(self) -> Dict:
        """Get WebSocket status information"""
        return {
            "enabled": self.socketio is not None,
            "platform": platform.system(),
            "async_mode": self.config.async_mode,
            "connection_count": self.get_connection_count(),
            "ping_timeout": self.config.ping_timeout,
            "ping_interval": self.config.ping_interval,
            "is_windows": self.is_windows,
            "transport_fallback_order": self.transport_fallback_order if self.is_windows else None
        }


class WebSocketConnectionManager:
    """Manages WebSocket connections with session tracking and health monitoring"""
    
    def __init__(self, socketio_manager: WindowsCompatibleSocketIO):
        self.socketio_manager = socketio_manager
        self.sessions: Dict[str, Dict] = {}
        self.health_check_interval = 30  # seconds
        self.health_check_thread = None
        self.running = False
        
        # Start health monitoring
        self._start_health_monitoring()
    
    def _start_health_monitoring(self):
        """Start health monitoring thread"""
        if self.health_check_thread is None or not self.health_check_thread.is_alive():
            self.running = True
            self.health_check_thread = threading.Thread(
                target=self._health_monitor_loop,
                daemon=True
            )
            self.health_check_thread.start()
            logger.info("WebSocket health monitoring started")
    
    def _health_monitor_loop(self):
        """Health monitoring loop"""
        while self.running:
            try:
                self._perform_health_check()
                time.sleep(self.health_check_interval)
            except Exception as e:
                logger.error(f"Error in health monitor loop: {e}")
                time.sleep(5)  # Short delay on error
    
    def _perform_health_check(self):
        """Perform health check on all connections"""
        try:
            connections = self.socketio_manager.get_all_connections()
            current_time = datetime.now(timezone.utc)
            
            for sid, connection_info in connections.items():
                # Check for inactive connections
                if (current_time - connection_info.last_activity).total_seconds() > 300:  # 5 minutes
                    logger.warning(f"Inactive connection detected: {sid}")
                
                # Update session information
                if sid in self.sessions:
                    self.sessions[sid]["last_health_check"] = current_time.isoformat()
                    self.sessions[sid]["is_active"] = True
            
            # Clean up inactive connections
            self.socketio_manager.cleanup_inactive_connections()
            
        except Exception as e:
            logger.error(f"Error performing health check: {e}")
    
    def create_session(self, sid: str, user_data: Dict = None) -> str:
        """Create new session for client"""
        session_id = f"session_{sid}_{int(time.time())}"
        
        self.sessions[sid] = {
            "session_id": session_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "last_activity": datetime.now(timezone.utc).isoformat(),
            "user_data": user_data or {},
            "is_active": True,
            "room": "general"
        }
        
        logger.info(f"Created session {session_id} for client {sid}")
        return session_id
    
    def update_session_activity(self, sid: str):
        """Update session activity timestamp"""
        if sid in self.sessions:
            self.sessions[sid]["last_activity"] = datetime.now(timezone.utc).isoformat()
    
    def get_session(self, sid: str) -> Optional[Dict]:
        """Get session information"""
        return self.sessions.get(sid)
    
    def remove_session(self, sid: str):
        """Remove session"""
        if sid in self.sessions:
            session_id = self.sessions[sid]["session_id"]
            del self.sessions[sid]
            logger.info(f"Removed session {session_id} for client {sid}")
    
    def get_session_count(self) -> int:
        """Get current session count"""
        return len(self.sessions)
    
    def get_all_sessions(self) -> Dict[str, Dict]:
        """Get all session information"""
        return self.sessions.copy()
    
    def stop(self):
        """Stop health monitoring"""
        self.running = False
        if self.health_check_thread and self.health_check_thread.is_alive():
            self.health_check_thread.join(timeout=5)
        logger.info("WebSocket connection manager stopped")


class TransportFallbackManager:
    """Manages transport fallback mechanisms for WebSocket connections"""
    
    def __init__(self, app):
        self.app = app
        self.fallback_endpoints = {}
        self.polling_clients = {}
        self.event_queue = []
        
        self._setup_fallback_endpoints()
    
    def _setup_fallback_endpoints(self):
        """Setup fallback HTTP endpoints"""
        
        @self.app.route("/api/events/poll", methods=["GET"])
        def events_poll():
            """HTTP polling endpoint for events"""
            try:
                client_id = request.args.get("client_id", "anonymous")
                last_event_id = request.args.get("last_event_id", "0")
                
                # Get new events for this client
                events = self._get_events_for_client(client_id, last_event_id)
                
                return {
                    "success": True,
                    "events": events,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                
            except Exception as e:
                logger.error(f"Error in events poll: {e}")
                return {"success": False, "error": str(e)}, 500
        
        @self.app.route("/api/events/stream", methods=["GET"])
        def events_stream():
            """Server-Sent Events stream endpoint"""
            try:
                from flask import Response, stream_with_context
                
                def generate():
                    client_id = request.args.get("client_id", "anonymous")
                    while True:
                        # Get new events
                        events = self._get_events_for_client(client_id)
                        if events:
                            for event in events:
                                yield f"data: {event}\n\n"
                        
                        time.sleep(1)  # Check every second
                
                return Response(
                    stream_with_context(generate()),
                    mimetype="text/event-stream",
                    headers={
                        "Cache-Control": "no-cache",
                        "Connection": "keep-alive",
                        "Access-Control-Allow-Origin": "*"
                    }
                )
                
            except Exception as e:
                logger.error(f"Error in events stream: {e}")
                return {"success": False, "error": str(e)}, 500
    
    def _get_events_for_client(self, client_id: str, last_event_id: str = "0") -> List[Dict]:
        """Get events for specific client"""
        # This is a simplified implementation
        # In a real system, you would maintain a proper event queue per client
        return []
    
    def add_event(self, event_type: str, data: Dict, target_clients: List[str] = None):
        """Add event to queue for polling clients"""
        event = {
            "id": str(len(self.event_queue) + 1),
            "type": event_type,
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "target_clients": target_clients or []
        }
        
        self.event_queue.append(event)
        
        # Keep only last 1000 events
        if len(self.event_queue) > 1000:
            self.event_queue = self.event_queue[-1000:]
        
        logger.debug(f"Added event {event['id']} of type {event_type}")
    
    def register_polling_client(self, client_id: str):
        """Register client for polling"""
        self.polling_clients[client_id] = {
            "registered_at": datetime.now(timezone.utc).isoformat(),
            "last_poll": datetime.now(timezone.utc).isoformat()
        }
        logger.info(f"Registered polling client: {client_id}")
    
    def unregister_polling_client(self, client_id: str):
        """Unregister polling client"""
        if client_id in self.polling_clients:
            del self.polling_clients[client_id]
            logger.info(f"Unregistered polling client: {client_id}")
    
    def get_polling_client_count(self) -> int:
        """Get number of polling clients"""
        return len(self.polling_clients)
    
    def get_event_queue_size(self) -> int:
        """Get current event queue size"""
        return len(self.event_queue) 