#!/usr/bin/env python3
"""
Collective Memory REST API Server
Modern Flask API with WebSocket support for real-time communication
"""
from dataclasses import dataclass
import os
import sys
import json
import logging
import platform
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError
import psutil

# Import our existing modules

from src.database_manager import DatabaseManager
from src.enhanced_query_engine import EnhancedQueryEngine, EnhancedSearchQuery
from src.query_engine import SearchQuery
from src.content_indexer import ContentIndexer
from src.file_monitor import DataFolderMonitor
from src.cursor_reader import EnhancedCursorDatabaseReader
from src.enterprise_api import enterprise_bp, websocket_handlers
from src.chat_api import register_chat_api, ChatAPI
from src.performance_monitor import get_monitor

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class APIResponse:
    """Standard API response structure"""

    success: bool
    data: Any = None
    error: Optional[str] = None
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc).isoformat()


class CollectiveMemoryAPI:
    """Main API class for Collective Memory system"""

    def __init__(self, data_folder: str = None):
        static_folder = os.environ.get("FLASK_STATIC_FOLDER", "frontend-dist")
        self.app = Flask(__name__, static_folder=static_folder, static_url_path="")
        self.app.config["SECRET_KEY"] = os.environ.get(
            "SECRET_KEY", "collective-memory-dev-key"
        )

        # Enable CORS
        CORS(self.app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

        # Initialize Windows-compatible WebSocket system
        try:
            from src.websocket_manager import WindowsCompatibleSocketIO, WebSocketConfig
            from src.windows_websocket_errors import WindowsWebSocketErrorHandler
            
            # Configure WebSocket for Windows compatibility
            websocket_config = WebSocketConfig(
                async_mode="threading",  # Windows-compatible async mode
                cors_allowed_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
                ping_timeout=120,  # Increased for Windows stability
                ping_interval=30,
                logger=True,
                engineio_logger=False
            )
            
            self.websocket_manager = WindowsCompatibleSocketIO(self.app, websocket_config)
            self.socketio = self.websocket_manager.socketio
            self.websocket_enabled = True
            
            # Initialize error handler
            self.websocket_error_handler = WindowsWebSocketErrorHandler()
            
            logger.info("Windows-compatible WebSocket system initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize WebSocket system: {e}")
            self.socketio = None
            self.websocket_enabled = False
            self.websocket_manager = None
            self.websocket_error_handler = None

        # Initialize components
        self.data_folder = data_folder or os.getcwd()
        self.collective_memory_dir = os.path.join(
            self.data_folder, ".collective-memory"
        )

        # Ensure directories exist
        os.makedirs(self.collective_memory_dir, exist_ok=True)
        os.makedirs(os.path.join(self.collective_memory_dir, "database"), exist_ok=True)
        os.makedirs(os.path.join(self.collective_memory_dir, "cache"), exist_ok=True)
        os.makedirs(os.path.join(self.collective_memory_dir, "logs"), exist_ok=True)
        os.makedirs(os.path.join(self.collective_memory_dir, "config"), exist_ok=True)

        # Initialize core components
        db_path = os.path.join(
            self.collective_memory_dir, "database", "collective_memory.db"
        )
        self.db_manager = DatabaseManager(db_path)
        self.query_engine = EnhancedQueryEngine(self.db_manager)
        self.content_indexer = ContentIndexer()
        self.file_monitor = DataFolderMonitor(self.data_folder)

        # Initialize JSON Chat Manager
        self.chat_api = register_chat_api(self.app, self.data_folder)

        # System stats
        self.start_time = datetime.now(timezone.utc)
        self.search_count = 0
        self.last_search_time = None

        # Setup routes
        self._setup_routes()
        self._setup_websocket_events()

        # Register JSON Chat API
        self._setup_json_chat_api()
        self._setup_frontend_routes(static_folder)

        logger.info(f"Collective Memory API initialized for folder: {self.data_folder}")
        logger.info(f"Flask route map: {self.app.url_map}")
        # Start system health monitoring
        from src.performance_monitor import start_system_monitoring

        start_system_monitoring(self.data_folder, interval=30)

    def _setup_routes(self):
        """Setup all API routes"""

        # Register enterprise blueprint for Phase 3 features
        self.app.register_blueprint(enterprise_bp)

        # Health check
        @self.app.route("/health", methods=["GET"])
        def health_check():
            return jsonify(APIResponse(success=True, data="OK").__dict__)

        # System Health Monitoring Endpoints
        @self.app.route("/api/system/health", methods=["GET"])
        def get_system_health():
            """Get current system health status"""
            try:
                monitor = get_monitor()
                status = monitor.get_current_status()
                return jsonify(status)
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route("/api/system/metrics", methods=["GET"])
        def get_system_metrics():
            """Get system metrics summary"""
            try:
                hours = request.args.get("hours", 24, type=int)
                monitor = get_monitor()
                summary = monitor.get_metrics_summary(hours=hours)
                return jsonify(summary)
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        # WebSocket diagnostic endpoints
        @self.app.route("/api/websocket/status", methods=["GET"])
        def get_websocket_status():
            """Get WebSocket status and diagnostic information"""
            try:
                status = {
                    "enabled": self.websocket_enabled,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                
                if self.websocket_enabled and hasattr(self, 'websocket_manager'):
                    status.update(self.websocket_manager.get_status())
                    
                    # Add connection information
                    status["connections"] = {
                        "total": self.websocket_manager.get_connection_count(),
                        "details": [
                            {
                                "sid": conn.sid,
                                "connected_at": conn.connected_at.isoformat(),
                                "last_activity": conn.last_activity.isoformat(),
                                "room": conn.room,
                                "ip_address": conn.ip_address
                            }
                            for conn in self.websocket_manager.get_all_connections().values()
                        ]
                    }
                
                # Add error information if available
                if hasattr(self, 'websocket_error_handler'):
                    status["errors"] = self.websocket_error_handler.get_error_summary()
                    status["diagnostics"] = self.websocket_error_handler.get_diagnostic_info()
                
                return jsonify(APIResponse(success=True, data=status).__dict__)
                
            except Exception as e:
                logger.error(f"Error getting WebSocket status: {e}")
                return jsonify(APIResponse(success=False, error=str(e)).__dict__), 500

        @self.app.route("/api/websocket/errors", methods=["GET"])
        def get_websocket_errors():
            """Get WebSocket error history"""
            try:
                if not hasattr(self, 'websocket_error_handler'):
                    return jsonify(APIResponse(success=False, error="WebSocket error handler not available").__dict__), 404
                
                hours = request.args.get("hours", 24, type=int)
                errors = self.websocket_error_handler.get_error_history(hours)
                
                error_data = [
                    {
                        "error_code": error.error_code,
                        "error_message": error.error_message,
                        "error_type": error.error_type,
                        "timestamp": error.timestamp.isoformat(),
                        "severity": error.severity,
                        "suggested_solutions": error.suggested_solutions
                    }
                    for error in errors
                ]
                
                return jsonify(APIResponse(success=True, data=error_data).__dict__)
                
            except Exception as e:
                logger.error(f"Error getting WebSocket errors: {e}")
                return jsonify(APIResponse(success=False, error=str(e)).__dict__), 500

        @self.app.route("/api/websocket/clear-errors", methods=["POST"])
        def clear_websocket_errors():
            """Clear WebSocket error history"""
            try:
                if not hasattr(self, 'websocket_error_handler'):
                    return jsonify(APIResponse(success=False, error="WebSocket error handler not available").__dict__), 404
                
                self.websocket_error_handler.clear_error_history()
                return jsonify(APIResponse(success=True, data="Error history cleared").__dict__)
                
            except Exception as e:
                logger.error(f"Error clearing WebSocket errors: {e}")
                return jsonify(APIResponse(success=False, error=str(e)).__dict__), 500

        # Stub endpoint removed - real implementation is later in the file

        @self.app.route("/api/auth/login", methods=["POST"])
        def api_auth_login():
            data = request.get_json() or {}
            username = data.get("username")
            password = data.get("password")
            # Dummy auth logic
            if username == "admin" and password == "admin123":
                return jsonify(
                    {
                        "success": True,
                        "token": "dummy-token",
                        "user": {"username": username},
                    }
                )
            return jsonify({"success": False, "error": "Invalid credentials"}), 401

        # /api/v1/chat/ index endpoint
        @self.app.route("/api/v1/chat/", methods=["GET"])
        def chat_api_index():
            return jsonify(
                {
                    "success": True,
                    "message": "Chat API root",
                    "endpoints": [
                        "/conversations",
                        "/stats",
                        "/import/cursor",
                        "/search",
                    ],
                }
            )

        # /system/status endpointini try/except ile sarmala
        @self.app.route("/system/status", methods=["GET"])
        def system_status():
            try:
                # Get file count and index size
                file_count = self.db_manager.get_total_file_count()
                index_size = self._get_index_size()

                # Get system resource usage
                cpu_usage = psutil.cpu_percent()
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage(self.data_folder)

                data = {
                    "totalFiles": file_count,
                    "filesChange": "+0",  # TODO: Calculate actual change
                    "indexSize": f"{index_size:.1f} MB",
                    "indexSizeChange": "+0 MB",
                    "averageSearchTime": "120ms",  # TODO: Calculate from actual data
                    "searchTimeChange": "-5ms",
                    "watchedDirectories": 1,
                    "watchedDirChange": "+0",
                    "cpuUsage": cpu_usage,
                    "memoryUsage": memory.percent,
                    "diskUsage": disk.percent,
                    "uptime": str(datetime.now(timezone.utc) - self.start_time),
                }

                return jsonify(APIResponse(success=True, data=data).__dict__)

            except Exception as e:
                logging.exception("Error in /system/status")
                return jsonify({"success": False, "error": str(e)}), 500

        @self.app.route("/system/stats", methods=["GET"])
        def get_system_stats():
            try:
                # Get file count and index size
                file_count = self.db_manager.get_total_file_count()
                index_size = self._get_index_size()

                # Get system resource usage
                cpu_usage = psutil.cpu_percent()
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage(self.data_folder)

                data = {
                    "totalFiles": file_count,
                    "filesChange": "+0",  # TODO: Calculate actual change
                    "indexSize": f"{index_size:.1f} MB",
                    "indexSizeChange": "+0 MB",
                    "averageSearchTime": "120ms",  # TODO: Calculate from actual data
                    "searchTimeChange": "-5ms",
                    "watchedDirectories": 1,
                    "watchedDirChange": "+0",
                    "cpuUsage": cpu_usage,
                    "memoryUsage": memory.percent,
                    "diskUsage": disk.percent,
                    "uptime": str(datetime.now(timezone.utc) - self.start_time),
                }

                return jsonify(APIResponse(success=True, data=data).__dict__)

            except Exception as e:
                logger.error(f"Error getting system stats: {e}")
                return jsonify(APIResponse(success=False, error=str(e)).__dict__), 500

        @self.app.route("/system/indexing", methods=["GET"])
        def get_indexing_status():
            try:
                is_indexing = (
                    hasattr(self.file_monitor, "_indexing")
                    and self.file_monitor._indexing
                )
                progress = (
                    getattr(self.file_monitor, "_progress", 0) if is_indexing else 100
                )

                data = {
                    "isIndexing": is_indexing,
                    "progress": progress,
                    "currentFile": getattr(self.file_monitor, "_current_file", None),
                    "processedFiles": getattr(self.file_monitor, "_processed_files", 0),
                    "totalFiles": getattr(self.file_monitor, "_total_files", 0),
                }

                return jsonify(APIResponse(success=True, data=data).__dict__)

            except Exception as e:
                logger.error(f"Error getting indexing status: {e}")
                return jsonify(APIResponse(success=False, error=str(e)).__dict__), 500

        @self.app.route("/system/reindex", methods=["POST"])
        def trigger_reindex():
            try:
                data = request.get_json() or {}
                path = data.get("path", None)

                # Start reindexing in background
                if path:
                    self.file_monitor.scan_directory(path)
                else:
                    self.file_monitor.scan_directory(self.data_folder)

                # Emit WebSocket event
                if self.socketio:
                    self.socketio.emit(
                        "indexing_started", {"path": path or self.data_folder}
                    )

                return jsonify(
                    APIResponse(
                        success=True, data={"message": "Reindexing started"}
                    ).__dict__
                )

            except Exception as e:
                logger.error(f"Error starting reindex: {e}")
                return jsonify(APIResponse(success=False, error=str(e)).__dict__), 500

        @self.app.route("/system/cache/clear", methods=["POST"])
        def clear_cache():
            try:
                # Clear query cache
                if hasattr(self.query_engine, "clear_cache"):
                    self.query_engine.clear_cache()

                # Clear file system cache
                cache_dir = os.path.join(self.collective_memory_dir, "cache")
                if os.path.exists(cache_dir):
                    import shutil

                    shutil.rmtree(cache_dir)
                    os.makedirs(cache_dir, exist_ok=True)

                return jsonify(
                    APIResponse(
                        success=True, data={"message": "Cache cleared"}
                    ).__dict__
                )

            except Exception as e:
                logger.error(f"Error clearing cache: {e}")
                return jsonify(APIResponse(success=False, error=str(e)).__dict__), 500

        # Search endpoints
        @self.app.route("/search", methods=["GET"])
        def search():
            try:
                query = request.args.get("q", "").strip()
                if not query:
                    return (
                        jsonify(
                            APIResponse(
                                success=False, error='Query parameter "q" is required'
                            ).__dict__
                        ),
                        400,
                    )

                # Parse parameters
                semantic = request.args.get("semantic", "false").lower() == "true"
                limit = min(int(request.args.get("limit", 50)), 200)
                offset = max(int(request.args.get("offset", 0)), 0)

                # Track search
                self.search_count += 1
                self.last_search_time = datetime.now(timezone.utc)
                search_start = datetime.now(timezone.utc)

                # Perform search
                from src.query_engine import SearchQuery

                search_query = SearchQuery(text=query, limit=limit, sort_by="relevance")

                results = self.query_engine.search(search_query)

                # Calculate search time
                search_time = (datetime.now(timezone.utc) - search_start).total_seconds() * 1000

                # Format results
                formatted_results = []
                for result in results:
                    formatted_results.append(
                        {
                            "id": result.get("id", ""),
                            "title": result.get("title", ""),
                            "filename": result.get("filename", ""),
                            "path": result.get("path", ""),
                            "content": result.get("content", ""),
                            "snippet": result.get("snippet", ""),
                            "score": result.get("score", 0),
                            "lastModified": result.get("last_modified", ""),
                            "size": result.get("size", 0),
                        }
                    )

                response_data = {
                    "results": formatted_results,
                    "total": len(formatted_results),  # TODO: Get actual total count
                    "limit": limit,
                    "offset": offset,
                    "searchTime": f"{search_time:.0f}ms",
                    "semantic": semantic,
                }

                # Add prompt to database and get related prompts
                try:
                    search_type = "semantic" if semantic else "basic"
                    user_session = request.headers.get("X-Session-ID", "anonymous")

                    # Save current prompt
                    prompt_id = self.db_manager.add_prompt(
                        prompt_text=query,
                        search_type=search_type,
                        results_count=len(formatted_results),
                        response_time_ms=int(search_time),
                        user_session=user_session,
                    )

                    # Get similar prompts for context suggestions
                    similar_prompts = self.db_manager.get_similar_prompts(
                        prompt_text=query, limit=3, similarity_threshold=0.6
                    )

                    # Get context suggestions
                    context_suggestions = (
                        self.db_manager.get_prompt_context_suggestions(
                            current_prompt=query, limit=3
                        )
                    )

                    # Add prompt relationship data to response
                    response_data["promptRelationships"] = {
                        "promptId": prompt_id,
                        "similarPrompts": similar_prompts,
                        "contextSuggestions": context_suggestions,
                    }

                except Exception as e:
                    logger.warning(f"Prompt tracking failed: {e}")
                    # Don't fail the search if prompt tracking fails
                    response_data["promptRelationships"] = {
                        "promptId": None,
                        "similarPrompts": [],
                        "contextSuggestions": [],
                    }

                # Emit WebSocket event
                if self.socketio:
                    self.socketio.emit(
                        "search_performed",
                        {
                            "query": query,
                            "results_count": len(formatted_results),
                            "search_time": search_time,
                        },
                    )

                return jsonify(APIResponse(success=True, data=response_data).__dict__)

            except Exception as e:
                logger.error(f"Error performing search: {e}")
                return jsonify(APIResponse(success=False, error=str(e)).__dict__), 500

        # /api/search unified endpoint (GET, POST)
        @self.app.route("/api/search", methods=["GET", "POST"])
        def api_search():
            """Unified search endpoint handling both GET and POST requests"""
            if request.method == "GET":
                return self._handle_get_search()
            elif request.method == "POST":
                return self._handle_post_search()

        @self.app.route("/search/suggestions", methods=["GET"])
        def get_search_suggestions():
            try:
                query = request.args.get("q", "").strip()
                if len(query) < 2:
                    return jsonify(APIResponse(success=True, data=[]).__dict__)

                # Get suggestions (simple implementation)
                suggestions = []
                if hasattr(self.query_engine, "get_suggestions"):
                    suggestions = self.query_engine.get_suggestions(query)
                else:
                    # Fallback: basic keyword suggestions
                    common_terms = [
                        "Django",
                        "React",
                        "Python",
                        "JavaScript",
                        "API",
                        "database",
                        "error",
                        "config",
                    ]
                    suggestions = [
                        term for term in common_terms if query.lower() in term.lower()
                    ][:5]

                return jsonify(APIResponse(success=True, data=suggestions).__dict__)

            except Exception as e:
                logger.error(f"Error getting suggestions: {e}")
                return jsonify(APIResponse(success=False, error=str(e)).__dict__), 500

        @self.app.route("/search/export", methods=["POST"])
        def export_search_results():
            try:
                data = request.get_json()
                query = data.get("query", "").strip()
                format_type = data.get("format", "markdown").lower()

                if not query:
                    return (
                        jsonify(
                            APIResponse(
                                success=False, error="Query is required"
                            ).__dict__
                        ),
                        400,
                    )

                # Perform search
                results = self.query_engine.search(query)

                # Generate export content
                if format_type == "markdown":
                    content = self._generate_markdown_export(query, results)
                    filename = f"search-results-{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.md"
                elif format_type == "text":
                    content = self._generate_text_export(query, results)
                    filename = f"search-results-{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.txt"
                else:
                    return (
                        jsonify(
                            APIResponse(
                                success=False,
                                error='Invalid format. Use "markdown" or "text"',
                            ).__dict__
                        ),
                        400,
                    )

                # Return file content
                response_data = {
                    "content": content,
                    "filename": filename,
                    "query": query,
                    "results_count": len(results),
                    "format": format_type,
                }

                return jsonify(APIResponse(success=True, data=response_data).__dict__)

            except Exception as e:
                logger.error(f"Error exporting search results: {e}")
                return jsonify(APIResponse(success=False, error=str(e)).__dict__), 500

        # Prompt relationship endpoints
        @self.app.route("/prompts", methods=["POST"])
        def add_prompt():
            try:
                data = request.get_json()
                prompt_text = data.get("prompt_text", "").strip()
                search_type = data.get("search_type", "basic")
                results_count = data.get("results_count", 0)
                response_time_ms = data.get("response_time_ms", 0)
                context_preserved = data.get("context_preserved")
                user_session = data.get("user_session")

                if not prompt_text:
                    return (
                        jsonify(
                            APIResponse(
                                success=False, error="Prompt text is required"
                            ).__dict__
                        ),
                        400,
                    )

                # Add prompt to database
                prompt_id = self.db_manager.add_prompt(
                    prompt_text=prompt_text,
                    search_type=search_type,
                    results_count=results_count,
                    response_time_ms=response_time_ms,
                    context_preserved=context_preserved,
                    user_session=user_session,
                )

                if prompt_id:
                    response_data = {
                        "prompt_id": prompt_id,
                        "message": "Prompt added successfully",
                    }
                    return jsonify(
                        APIResponse(success=True, data=response_data).__dict__
                    )
                else:
                    return (
                        jsonify(
                            APIResponse(
                                success=False, error="Failed to add prompt"
                            ).__dict__
                        ),
                        500,
                    )

            except Exception as e:
                logger.error(f"Error adding prompt: {e}")
                return jsonify(APIResponse(success=False, error=str(e)).__dict__), 500

        @self.app.route("/prompts/similar", methods=["GET"])
        def get_similar_prompts():
            try:
                prompt_text = request.args.get("prompt", "").strip()
                limit = min(int(request.args.get("limit", 5)), 20)
                threshold = float(request.args.get("threshold", 0.6))

                if not prompt_text:
                    return (
                        jsonify(
                            APIResponse(
                                success=False, error="Prompt parameter is required"
                            ).__dict__
                        ),
                        400,
                    )

                # Get similar prompts
                similar_prompts = self.db_manager.get_similar_prompts(
                    prompt_text=prompt_text, limit=limit, similarity_threshold=threshold
                )

                response_data = {
                    "query_prompt": prompt_text,
                    "similar_prompts": similar_prompts,
                    "count": len(similar_prompts),
                }

                return jsonify(APIResponse(success=True, data=response_data).__dict__)

            except Exception as e:
                logger.error(f"Error getting similar prompts: {e}")
                return jsonify(APIResponse(success=False, error=str(e)).__dict__), 500

        @self.app.route("/prompts/<int:prompt_id>/related", methods=["GET"])
        def get_related_prompts(prompt_id):
            try:
                limit = min(int(request.args.get("limit", 5)), 20)

                # Get related prompts
                related_prompts = self.db_manager.get_related_prompts(
                    prompt_id=prompt_id, limit=limit
                )

                response_data = {
                    "prompt_id": prompt_id,
                    "related_prompts": related_prompts,
                    "count": len(related_prompts),
                }

                return jsonify(APIResponse(success=True, data=response_data).__dict__)

            except Exception as e:
                logger.error(f"Error getting related prompts: {e}")
                return jsonify(APIResponse(success=False, error=str(e)).__dict__), 500

        @self.app.route("/prompts/context-suggestions", methods=["GET"])
        def get_context_suggestions():
            try:
                current_prompt = request.args.get("prompt", "").strip()
                limit = min(int(request.args.get("limit", 3)), 10)

                if not current_prompt:
                    return (
                        jsonify(
                            APIResponse(
                                success=False, error="Prompt parameter is required"
                            ).__dict__
                        ),
                        400,
                    )

                # Get context suggestions
                suggestions = self.db_manager.get_prompt_context_suggestions(
                    current_prompt=current_prompt, limit=limit
                )

                response_data = {
                    "current_prompt": current_prompt,
                    "suggestions": suggestions,
                    "count": len(suggestions),
                }

                return jsonify(APIResponse(success=True, data=response_data).__dict__)

            except Exception as e:
                logger.error(f"Error getting context suggestions: {e}")
                return jsonify(APIResponse(success=False, error=str(e)).__dict__), 500

        # Configuration endpoints
        @self.app.route("/config", methods=["GET"])
        def get_config():
            try:
                config_path = os.path.join(
                    self.collective_memory_dir, "config", "settings.json"
                )

                # Default configuration
                default_config = {
                    "maxFileSize": 100,
                    "maxIndexSize": 1000,
                    "autoIndex": True,
                    "enableSemantic": True,
                    "defaultSearchLimit": 50,
                    "cacheEnabled": True,
                    "notifyOnIndex": True,
                    "notifyOnError": True,
                    "emailNotifications": False,
                    "enableAuth": False,
                    "sessionTimeout": 3600,
                    "logLevel": "info",
                    "watchedPaths": [self.data_folder],
                }

                # Load existing config if available
                if os.path.exists(config_path):
                    with open(config_path, "r") as f:
                        saved_config = json.load(f)
                        default_config.update(saved_config)

                return jsonify(APIResponse(success=True, data=default_config).__dict__)

            except Exception as e:
                logger.error(f"Error getting config: {e}")
                return jsonify(APIResponse(success=False, error=str(e)).__dict__), 500

        @self.app.route("/config", methods=["PUT"])
        def update_config():
            try:
                new_config = request.get_json()
                config_path = os.path.join(
                    self.collective_memory_dir, "config", "settings.json"
                )

                # Save configuration
                with open(config_path, "w") as f:
                    json.dump(new_config, f, indent=2)

                # Apply configuration changes
                self._apply_config_changes(new_config)

                return jsonify(
                    APIResponse(
                        success=True, data={"message": "Configuration updated"}
                    ).__dict__
                )

            except Exception as e:
                logger.error(f"Error updating config: {e}")
                return jsonify(APIResponse(success=False, error=str(e)).__dict__), 500

        # Error handlers
        @self.app.errorhandler(404)
        def not_found(error):
            return (
                jsonify(
                    APIResponse(success=False, error="Endpoint not found").__dict__
                ),
                404,
            )

        @self.app.errorhandler(500)
        def internal_error(error):
            return (
                jsonify(
                    APIResponse(success=False, error="Internal server error").__dict__
                ),
                500,
            )

    def _setup_websocket_events(self):
        """Setup WebSocket event handlers"""
        if not self.socketio or not self.websocket_enabled:
            logger.info("Skipping WebSocket event setup - WebSocket disabled")
            return

        # Register custom event handlers with the WebSocket manager
        if hasattr(self, 'websocket_manager'):
            self.websocket_manager.register_event_handler("search_started", self._handle_search_started)
            self.websocket_manager.register_event_handler("search_completed", self._handle_search_completed)
            self.websocket_manager.register_event_handler("system_update", self._handle_system_update)
            self.websocket_manager.register_event_handler("team_message", self._handle_team_message)

        # Enterprise WebSocket handlers for Phase 3
        if hasattr(self, 'websocket_handlers'):
            for event_name, handler in websocket_handlers.items():
                if self.socketio:
                    self.socketio.on(event_name)(handler)
    
    def _handle_search_started(self, data):
        """Handle search started event"""
        try:
            if self.websocket_manager:
                self.websocket_manager.emit_to_all("search_started", {
                    "query": data.get("query", ""),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "user": data.get("user", "anonymous")
                })
        except Exception as e:
            logger.error(f"Error handling search started: {e}")
            if self.websocket_error_handler:
                self.websocket_error_handler.analyze_error(str(e))
    
    def _handle_search_completed(self, data):
        """Handle search completed event"""
        try:
            if self.websocket_manager:
                self.websocket_manager.emit_to_all("search_completed", {
                    "query": data.get("query", ""),
                    "results_count": data.get("results_count", 0),
                    "search_time": data.get("search_time", 0),
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })
        except Exception as e:
            logger.error(f"Error handling search completed: {e}")
            if self.websocket_error_handler:
                self.websocket_error_handler.analyze_error(str(e))
    
    def _handle_system_update(self, data):
        """Handle system update event"""
        try:
            if self.websocket_manager:
                self.websocket_manager.emit_to_all("system_update", {
                    "type": data.get("type", "general"),
                    "message": data.get("message", ""),
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })
        except Exception as e:
            logger.error(f"Error handling system update: {e}")
            if self.websocket_error_handler:
                self.websocket_error_handler.analyze_error(str(e))
    
    def _handle_team_message(self, data):
        """Handle team message event"""
        try:
            room = data.get("room", "general")
            if self.websocket_manager:
                self.websocket_manager.emit_to_room(room, "team_message", {
                    "user": data.get("user", "anonymous"),
                    "message": data.get("message", ""),
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })
        except Exception as e:
            logger.error(f"Error handling team message: {e}")
            if self.websocket_error_handler:
                self.websocket_error_handler.analyze_error(str(e))

    def _get_index_size(self) -> float:
        """Calculate total index size in MB"""
        try:
            db_path = os.path.join(
                self.collective_memory_dir, "database", "collective_memory.db"
            )
            if os.path.exists(db_path):
                size_bytes = os.path.getsize(db_path)
                return size_bytes / (1024 * 1024)  # Convert to MB
            return 0.0
        except:
            return 0.0

    def _generate_markdown_export(self, query: str, results: List[Dict]) -> str:
        """Generate markdown export of search results"""
        content = f"""# Search Results for "{query}"

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total results: {len(results)}

---

"""

        for i, result in enumerate(results, 1):
            content += f"""## {i}. {result.get('filename', 'Unknown File')}

**Path:** `{result.get('path', 'Unknown')}`
**Score:** {result.get('score', 0):.2f}
**Last Modified:** {result.get('last_modified', 'Unknown')}

### Content Preview:
```
{result.get('snippet', result.get('content', 'No content available')[:500])}
```

---

"""

        return content

    def _generate_text_export(self, query: str, results: List[Dict]) -> str:
        """Generate text export of search results"""
        content = f"""Search Results for "{query}"
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total results: {len(results)}

{'='*80}

"""

        for i, result in enumerate(results, 1):
            content += f"""{i}. {result.get('filename', 'Unknown File')}
   Path: {result.get('path', 'Unknown')}
   Score: {result.get('score', 0):.2f}
   Last Modified: {result.get('last_modified', 'Unknown')}
   
   Content:
   {result.get('snippet', result.get('content', 'No content available')[:300])}
   
{'-'*80}

"""

        return content

    def _handle_get_search(self):
        """Handle GET requests with query parameters"""
        query = request.args.get("q", "").strip()
        if not query:
            return (
                jsonify(
                    APIResponse(
                        success=False, error='Query parameter "q" is required'
                    ).__dict__
                ),
                400,
            )
        
        # Parse additional parameters
        semantic = request.args.get("semantic", "false").lower() == "true"
        limit = min(int(request.args.get("limit", 50)), 200)
        offset = max(int(request.args.get("offset", 0)), 0)
        
        return self._perform_search(query, semantic, limit, offset)

    def _handle_post_search(self):
        """Handle POST requests with JSON body"""
        data = request.get_json() or {}
        query = data.get("q", "").strip()
        if not query:
            return (
                jsonify(
                    APIResponse(
                        success=False, error='Query parameter "q" is required'
                    ).__dict__
                ),
                400,
            )
        
        # Parse additional parameters
        semantic = data.get("semantic", False)
        limit = min(int(data.get("limit", 50)), 200)
        offset = max(int(data.get("offset", 0)), 0)
        
        return self._perform_search(query, semantic, limit, offset)

    def _perform_search(self, query: str, semantic: bool = False, limit: int = 50, offset: int = 0):
        """Common search logic for both GET and POST"""
        try:
            # Track search
            self.search_count += 1
            self.last_search_time = datetime.now(timezone.utc)
            search_start = datetime.now(timezone.utc)

            # Emit search started event via WebSocket
            if self.websocket_enabled and hasattr(self, 'websocket_manager'):
                try:
                    self.websocket_manager.emit_to_all("search_started", {
                        "query": query,
                        "semantic": semantic,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "user": request.headers.get("X-Session-ID", "anonymous")
                    })
                except Exception as e:
                    logger.error(f"Error emitting search started event: {e}")
                    if hasattr(self, 'websocket_error_handler'):
                        self.websocket_error_handler.analyze_error(str(e))

            # Perform search
            from src.query_engine import SearchQuery

            search_query = SearchQuery(text=query, limit=limit, sort_by="relevance")
            results = self.query_engine.search(search_query)

            # Calculate search time
            search_time = (datetime.now(timezone.utc) - search_start).total_seconds() * 1000

            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append(
                    {
                        "id": result.get("id", ""),
                        "title": result.get("title", ""),
                        "filename": result.get("filename", ""),
                        "path": result.get("path", ""),
                        "content": result.get("content", ""),
                        "snippet": result.get("snippet", ""),
                        "score": result.get("score", 0),
                        "lastModified": result.get("last_modified", ""),
                        "size": result.get("size", 0),
                    }
                )

            response_data = {
                "results": formatted_results,
                "total": len(formatted_results),
                "limit": limit,
                "offset": offset,
                "searchTime": f"{search_time:.0f}ms",
                "semantic": semantic,
            }

            # Emit search completed event via WebSocket
            if self.websocket_enabled and hasattr(self, 'websocket_manager'):
                try:
                    self.websocket_manager.emit_to_all("search_completed", {
                        "query": query,
                        "results_count": len(formatted_results),
                        "search_time": search_time,
                        "semantic": semantic,
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    })
                except Exception as e:
                    logger.error(f"Error emitting search completed event: {e}")
                    if hasattr(self, 'websocket_error_handler'):
                        self.websocket_error_handler.analyze_error(str(e))

            # Add prompt to database and get related prompts
            try:
                search_type = "semantic" if semantic else "basic"
                user_session = request.headers.get("X-Session-ID", "anonymous")

                # Save current prompt
                prompt_id = self.db_manager.add_prompt(
                    prompt_text=query,
                    search_type=search_type,
                    results_count=len(formatted_results),
                    response_time_ms=int(search_time),
                    user_session=user_session,
                )

                # Get similar prompts for context suggestions
                similar_prompts = self.db_manager.get_similar_prompts(
                    prompt_text=query, limit=3, similarity_threshold=0.6
                )

                # Get context suggestions
                context_suggestions = (
                    self.db_manager.get_prompt_context_suggestions(
                        current_prompt=query, limit=3
                    )
                )

                # Add prompt relationship data to response
                response_data["promptRelationships"] = {
                    "promptId": prompt_id,
                    "similarPrompts": similar_prompts,
                    "contextSuggestions": context_suggestions,
                }

            except Exception as e:
                logger.warning(f"Prompt tracking failed: {e}")
                # Don't fail the search if prompt tracking fails
                response_data["promptRelationships"] = {
                    "promptId": None,
                    "similarPrompts": [],
                    "contextSuggestions": [],
                }

            # Emit WebSocket event
            if self.socketio:
                self.socketio.emit(
                    "search_performed",
                    {
                        "query": query,
                        "results_count": len(formatted_results),
                        "search_time": search_time,
                    },
                )

            return jsonify(APIResponse(success=True, data=response_data).__dict__)

        except Exception as e:
            logger.error(f"Error performing search: {e}")
            return jsonify(APIResponse(success=False, error=str(e)).__dict__), 500

    def _apply_config_changes(self, config: Dict):
        """Apply configuration changes to system components"""
        try:
            # Update logging level
            log_level = config.get("logLevel", "info").upper()
            logging.getLogger().setLevel(getattr(logging, log_level, logging.INFO))

            # Update watched paths
            watched_paths = config.get("watchedPaths", [])
            if watched_paths and self.file_monitor:
                # Update file monitor paths (implementation depends on monitor design)
                pass

            logger.info("Configuration changes applied successfully")

        except Exception as e:
            logger.error(f"Error applying config changes: {e}")

    def _setup_json_chat_api(self):
        """Dummy setup for JSON Chat API (to prevent AttributeError)"""
        pass

    def _setup_frontend_routes(self, static_folder):
        """Setup routes for serving static files and SPA fallback"""

        @self.app.route("/", defaults={"path": ""})
        @self.app.route("/<path:path>")
        def serve_frontend(path):
            # Skip API routes
            if path.startswith("api/") or path.startswith("socket.io"):
                return NotFound()
            
            # Check if static folder exists
            if not os.path.exists(static_folder):
                return self._generate_fallback_page()
            
            # Try to serve static file
            file_path = os.path.join(static_folder, path)
            if path != "" and os.path.exists(file_path):
                return send_from_directory(static_folder, path)
            else:
                # Try to serve index.html
                index_path = os.path.join(static_folder, "index.html")
                if os.path.exists(index_path):
                    return send_from_directory(static_folder, "index.html")
                else:
                    return self._generate_fallback_page()

    def _generate_fallback_page(self):
        """Generate a helpful fallback page when frontend build is missing"""
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Collective Memory API Server</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #333; border-bottom: 2px solid #007acc; padding-bottom: 10px; }
                .status { background: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0; }
                .warning { background: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #ffc107; }
                .api-list { background: #f8f9fa; padding: 20px; border-radius: 5px; }
                .api-endpoint { margin: 10px 0; padding: 8px; background: white; border-radius: 3px; font-family: monospace; }
                .method { padding: 2px 8px; border-radius: 3px; color: white; font-size: 12px; margin-right: 10px; }
                .get { background: #28a745; }
                .post { background: #007bff; }
                .put { background: #ffc107; color: black; }
                code { background: #f1f1f1; padding: 2px 6px; border-radius: 3px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Collective Memory API Server</h1>
                
                <div class="status">
                    <strong>✅ API Server is Running</strong><br>
                    The backend API is operational and ready to serve requests.
                </div>
                
                <div class="warning">
                    <strong>⚠️ Frontend Build Missing</strong><br>
                    The frontend application build is not available. To build the frontend:
                    <br><br>
                    <code>cd frontend && npm install && npm run build</code>
                </div>
                
                <h2>Available API Endpoints</h2>
                <div class="api-list">
                    <div class="api-endpoint">
                        <span class="method get">GET</span> <strong>/health</strong> - Server health check
                    </div>
                    <div class="api-endpoint">
                        <span class="method get">GET</span> <strong>/system/status</strong> - System status and metrics
                    </div>
                    <div class="api-endpoint">
                        <span class="method get">GET</span> <strong>/search?q=query</strong> - Search content
                    </div>
                    <div class="api-endpoint">
                        <span class="method post">POST</span> <strong>/api/search</strong> - Advanced search with JSON body
                    </div>
                    <div class="api-endpoint">
                        <span class="method get">GET</span> <strong>/api/v1/chat/conversations</strong> - List conversations
                    </div>
                    <div class="api-endpoint">
                        <span class="method get">GET</span> <strong>/config</strong> - Get configuration
                    </div>
                    <div class="api-endpoint">
                        <span class="method put">PUT</span> <strong>/config</strong> - Update configuration
                    </div>
                </div>
                
                <h2>Quick Test</h2>
                <p>Try these endpoints to test the API:</p>
                <ul>
                    <li><a href="/health" target="_blank">/health</a> - Check if server is healthy</li>
                    <li><a href="/system/status" target="_blank">/system/status</a> - View system metrics</li>
                    <li><a href="/api/v1/chat/" target="_blank">/api/v1/chat/</a> - Chat API info</li>
                </ul>
                
                <h2>Documentation</h2>
                <p>For complete API documentation and usage examples, please refer to the project README.</p>
            </div>
        </body>
        </html>
        """
        return html_content

    def run(self, host="127.0.0.1", port=8000, debug=False):
        """Run the API server"""
        logger.info(f"Starting Collective Memory API server on {host}:{port}")
        if self.socketio and self.websocket_enabled:
            self.socketio.run(self.app, host=host, port=port, debug=debug)
        else:
            logger.info("Running without WebSocket support")
            self.app.run(host=host, port=port, debug=debug)


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Collective Memory REST API Server")
    parser.add_argument(
        "--data-folder",
        "-d",
        default=os.getcwd(),
        help="Data folder to index (default: current directory)",
    )
    parser.add_argument(
        "--host", default="127.0.0.1", help="Host to bind to (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port", "-p", type=int, default=8000, help="Port to bind to (default: 8000)"
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    # Create and run API server
    api = CollectiveMemoryAPI(data_folder=args.data_folder)
    api.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()

# Gunicorn için Flask app'i expose et
app = CollectiveMemoryAPI().app
