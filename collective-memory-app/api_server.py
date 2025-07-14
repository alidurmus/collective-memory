#!/usr/bin/env python3
"""
Collective Memory REST API Server
Modern Flask API with WebSocket support for real-time communication
"""

import os
import sys
import json
import logging
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import tempfile
import zipfile
import io

from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError
import psutil

# Import our existing modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.database_manager import DatabaseManager
from src.enhanced_query_engine import EnhancedQueryEngine
from src.content_indexer import ContentIndexer
from src.file_monitor import DataFolderMonitor
from src.cursor_reader import EnhancedCursorDatabaseReader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
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
            self.timestamp = datetime.utcnow().isoformat()

class CollectiveMemoryAPI:
    """Main API class for Collective Memory system"""
    
    def __init__(self, data_folder: str = None):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'collective-memory-dev-key')
        
        # Enable CORS
        CORS(self.app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])
        
        # Initialize SocketIO
        self.socketio = SocketIO(
            self.app, 
            cors_allowed_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
            async_mode='threading'
        )
        
        # Initialize components
        self.data_folder = data_folder or os.getcwd()
        self.collective_memory_dir = os.path.join(self.data_folder, '.collective-memory')
        
        # Ensure directories exist
        os.makedirs(self.collective_memory_dir, exist_ok=True)
        os.makedirs(os.path.join(self.collective_memory_dir, 'database'), exist_ok=True)
        os.makedirs(os.path.join(self.collective_memory_dir, 'cache'), exist_ok=True)
        os.makedirs(os.path.join(self.collective_memory_dir, 'logs'), exist_ok=True)
        os.makedirs(os.path.join(self.collective_memory_dir, 'config'), exist_ok=True)
        
        # Initialize core components
        db_path = os.path.join(self.collective_memory_dir, 'database', 'collective_memory.db')
        self.db_manager = DatabaseManager(db_path)
        self.query_engine = EnhancedQueryEngine(self.db_manager)
        self.content_indexer = ContentIndexer()
        self.file_monitor = DataFolderMonitor(self.data_folder)
        
        # System stats
        self.start_time = datetime.utcnow()
        self.search_count = 0
        self.last_search_time = None
        
        # Setup routes
        self._setup_routes()
        self._setup_websocket_events()
        
        logger.info(f"Collective Memory API initialized for folder: {self.data_folder}")

    def _setup_routes(self):
        """Setup all API routes"""
        
        # Health check
        @self.app.route('/health', methods=['GET'])
        def health_check():
            return jsonify(APIResponse(success=True, data="OK").__dict__)
        
        # System endpoints
        @self.app.route('/system/status', methods=['GET'])
        def get_system_status():
            try:
                # Check if indexing is running
                is_indexing = hasattr(self.file_monitor, '_indexing') and self.file_monitor._indexing
                
                # Get basic stats
                file_count = self.db_manager.get_total_file_count()
                
                # Determine system health
                status = 'healthy'
                if is_indexing:
                    status = 'indexing'
                
                data = {
                    'status': status,
                    'uptime': str(datetime.utcnow() - self.start_time),
                    'file_count': file_count,
                    'last_search': self.last_search_time.isoformat() if self.last_search_time else None,
                    'search_count': self.search_count,
                    'is_indexing': is_indexing,
                    'notifications': 0
                }
                
                return jsonify(APIResponse(success=True, data=data).__dict__)
                
            except Exception as e:
                logger.error(f"Error getting system status: {e}")
                return jsonify(APIResponse(success=False, error=str(e)).__dict__), 500

        @self.app.route('/system/stats', methods=['GET'])
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
                    'totalFiles': file_count,
                    'filesChange': '+0',  # TODO: Calculate actual change
                    'indexSize': f"{index_size:.1f} MB",
                    'indexSizeChange': '+0 MB',
                    'averageSearchTime': '120ms',  # TODO: Calculate from actual data
                    'searchTimeChange': '-5ms',
                    'watchedDirectories': 1,
                    'watchedDirChange': '+0',
                    'cpuUsage': cpu_usage,
                    'memoryUsage': memory.percent,
                    'diskUsage': disk.percent,
                    'uptime': str(datetime.utcnow() - self.start_time)
                }
                
                return jsonify(APIResponse(success=True, data=data).__dict__)
                
            except Exception as e:
                logger.error(f"Error getting system stats: {e}")
                return jsonify(APIResponse(success=False, error=str(e)).__dict__), 500

        @self.app.route('/system/indexing', methods=['GET'])
        def get_indexing_status():
            try:
                is_indexing = hasattr(self.file_monitor, '_indexing') and self.file_monitor._indexing
                progress = getattr(self.file_monitor, '_progress', 0) if is_indexing else 100
                
                data = {
                    'isIndexing': is_indexing,
                    'progress': progress,
                    'currentFile': getattr(self.file_monitor, '_current_file', None),
                    'processedFiles': getattr(self.file_monitor, '_processed_files', 0),
                    'totalFiles': getattr(self.file_monitor, '_total_files', 0)
                }
                
                return jsonify(APIResponse(success=True, data=data).__dict__)
                
            except Exception as e:
                logger.error(f"Error getting indexing status: {e}")
                return jsonify(APIResponse(success=False, error=str(e)).__dict__), 500

        @self.app.route('/system/reindex', methods=['POST'])
        def trigger_reindex():
            try:
                data = request.get_json() or {}
                path = data.get('path', None)
                
                # Start reindexing in background
                if path:
                    self.file_monitor.scan_directory(path)
                else:
                    self.file_monitor.scan_directory(self.data_folder)
                
                # Emit WebSocket event
                self.socketio.emit('indexing_started', {'path': path or self.data_folder})
                
                return jsonify(APIResponse(success=True, data={'message': 'Reindexing started'}).__dict__)
                
            except Exception as e:
                logger.error(f"Error starting reindex: {e}")
                return jsonify(APIResponse(success=False, error=str(e)).__dict__), 500

        @self.app.route('/system/cache/clear', methods=['POST'])
        def clear_cache():
            try:
                # Clear query cache
                if hasattr(self.query_engine, 'clear_cache'):
                    self.query_engine.clear_cache()
                
                # Clear file system cache
                cache_dir = os.path.join(self.collective_memory_dir, 'cache')
                if os.path.exists(cache_dir):
                    import shutil
                    shutil.rmtree(cache_dir)
                    os.makedirs(cache_dir, exist_ok=True)
                
                return jsonify(APIResponse(success=True, data={'message': 'Cache cleared'}).__dict__)
                
            except Exception as e:
                logger.error(f"Error clearing cache: {e}")
                return jsonify(APIResponse(success=False, error=str(e)).__dict__), 500

        # Search endpoints
        @self.app.route('/search', methods=['GET'])
        def search():
            try:
                query = request.args.get('q', '').strip()
                if not query:
                    return jsonify(APIResponse(success=False, error='Query parameter "q" is required').__dict__), 400
                
                # Parse parameters
                semantic = request.args.get('semantic', 'false').lower() == 'true'
                limit = min(int(request.args.get('limit', 50)), 200)
                offset = max(int(request.args.get('offset', 0)), 0)
                
                # Track search
                self.search_count += 1
                self.last_search_time = datetime.utcnow()
                search_start = datetime.utcnow()
                
                # Perform search
                if semantic and hasattr(self.query_engine, 'semantic_search'):
                    results = self.query_engine.semantic_search(query, limit=limit, offset=offset)
                else:
                    results = self.query_engine.search(query, limit=limit, offset=offset)
                
                # Calculate search time
                search_time = (datetime.utcnow() - search_start).total_seconds() * 1000
                
                # Format results
                formatted_results = []
                for result in results:
                    formatted_results.append({
                        'id': result.get('id', ''),
                        'title': result.get('title', ''),
                        'filename': result.get('filename', ''),
                        'path': result.get('path', ''),
                        'content': result.get('content', ''),
                        'snippet': result.get('snippet', ''),
                        'score': result.get('score', 0),
                        'lastModified': result.get('last_modified', ''),
                        'size': result.get('size', 0)
                    })
                
                response_data = {
                    'results': formatted_results,
                    'total': len(formatted_results),  # TODO: Get actual total count
                    'limit': limit,
                    'offset': offset,
                    'searchTime': f"{search_time:.0f}ms",
                    'semantic': semantic
                }
                
                # Emit WebSocket event
                self.socketio.emit('search_performed', {
                    'query': query,
                    'results_count': len(formatted_results),
                    'search_time': search_time
                })
                
                return jsonify(APIResponse(success=True, data=response_data).__dict__)
                
            except Exception as e:
                logger.error(f"Error performing search: {e}")
                return jsonify(APIResponse(success=False, error=str(e)).__dict__), 500

        @self.app.route('/search/suggestions', methods=['GET'])
        def get_search_suggestions():
            try:
                query = request.args.get('q', '').strip()
                if len(query) < 2:
                    return jsonify(APIResponse(success=True, data=[]).__dict__)
                
                # Get suggestions (simple implementation)
                suggestions = []
                if hasattr(self.query_engine, 'get_suggestions'):
                    suggestions = self.query_engine.get_suggestions(query)
                else:
                    # Fallback: basic keyword suggestions
                    common_terms = ['Django', 'React', 'Python', 'JavaScript', 'API', 'database', 'error', 'config']
                    suggestions = [term for term in common_terms if query.lower() in term.lower()][:5]
                
                return jsonify(APIResponse(success=True, data=suggestions).__dict__)
                
            except Exception as e:
                logger.error(f"Error getting suggestions: {e}")
                return jsonify(APIResponse(success=False, error=str(e)).__dict__), 500

        @self.app.route('/search/export', methods=['POST'])
        def export_search_results():
            try:
                data = request.get_json()
                query = data.get('query', '')
                format_type = data.get('format', 'markdown')
                
                if not query:
                    return jsonify(APIResponse(success=False, error='Query is required').__dict__), 400
                
                # Perform search
                results = self.query_engine.search(query, limit=1000)
                
                # Generate export content
                if format_type == 'markdown':
                    content = self._generate_markdown_export(query, results)
                    filename = f"search-results-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
                    mimetype = 'text/markdown'
                else:
                    content = self._generate_text_export(query, results)
                    filename = f"search-results-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
                    mimetype = 'text/plain'
                
                # Create in-memory file
                output = io.BytesIO()
                output.write(content.encode('utf-8'))
                output.seek(0)
                
                return send_file(
                    output,
                    as_attachment=True,
                    download_name=filename,
                    mimetype=mimetype
                )
                
            except Exception as e:
                logger.error(f"Error exporting search results: {e}")
                return jsonify(APIResponse(success=False, error=str(e)).__dict__), 500

        # Configuration endpoints
        @self.app.route('/config', methods=['GET'])
        def get_config():
            try:
                config_path = os.path.join(self.collective_memory_dir, 'config', 'settings.json')
                
                # Default configuration
                default_config = {
                    'maxFileSize': 100,
                    'maxIndexSize': 1000,
                    'autoIndex': True,
                    'enableSemantic': True,
                    'defaultSearchLimit': 50,
                    'cacheEnabled': True,
                    'notifyOnIndex': True,
                    'notifyOnError': True,
                    'emailNotifications': False,
                    'enableAuth': False,
                    'sessionTimeout': 3600,
                    'logLevel': 'info',
                    'watchedPaths': [self.data_folder]
                }
                
                # Load existing config if available
                if os.path.exists(config_path):
                    with open(config_path, 'r') as f:
                        saved_config = json.load(f)
                        default_config.update(saved_config)
                
                return jsonify(APIResponse(success=True, data=default_config).__dict__)
                
            except Exception as e:
                logger.error(f"Error getting config: {e}")
                return jsonify(APIResponse(success=False, error=str(e)).__dict__), 500

        @self.app.route('/config', methods=['PUT'])
        def update_config():
            try:
                new_config = request.get_json()
                config_path = os.path.join(self.collective_memory_dir, 'config', 'settings.json')
                
                # Save configuration
                with open(config_path, 'w') as f:
                    json.dump(new_config, f, indent=2)
                
                # Apply configuration changes
                self._apply_config_changes(new_config)
                
                return jsonify(APIResponse(success=True, data={'message': 'Configuration updated'}).__dict__)
                
            except Exception as e:
                logger.error(f"Error updating config: {e}")
                return jsonify(APIResponse(success=False, error=str(e)).__dict__), 500

        # Error handlers
        @self.app.errorhandler(404)
        def not_found(error):
            return jsonify(APIResponse(success=False, error='Endpoint not found').__dict__), 404

        @self.app.errorhandler(500)
        def internal_error(error):
            return jsonify(APIResponse(success=False, error='Internal server error').__dict__), 500

    def _setup_websocket_events(self):
        """Setup WebSocket event handlers"""
        
        @self.socketio.on('connect')
        def handle_connect():
            logger.info(f"Client connected: {request.sid}")
            emit('connected', {'message': 'Connected to Collective Memory API'})

        @self.socketio.on('disconnect')
        def handle_disconnect():
            logger.info(f"Client disconnected: {request.sid}")

        @self.socketio.on('join_room')
        def handle_join_room(data):
            room = data.get('room', 'general')
            join_room(room)
            emit('joined_room', {'room': room})

        @self.socketio.on('leave_room')
        def handle_leave_room(data):
            room = data.get('room', 'general')
            leave_room(room)
            emit('left_room', {'room': room})

    def _get_index_size(self) -> float:
        """Calculate total index size in MB"""
        try:
            db_path = os.path.join(self.collective_memory_dir, 'database', 'collective_memory.db')
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

    def _apply_config_changes(self, config: Dict):
        """Apply configuration changes to system components"""
        try:
            # Update logging level
            log_level = config.get('logLevel', 'info').upper()
            logging.getLogger().setLevel(getattr(logging, log_level, logging.INFO))
            
            # Update watched paths
            watched_paths = config.get('watchedPaths', [])
            if watched_paths and self.file_monitor:
                # Update file monitor paths (implementation depends on monitor design)
                pass
                
            logger.info("Configuration changes applied successfully")
            
        except Exception as e:
            logger.error(f"Error applying config changes: {e}")

    def run(self, host='127.0.0.1', port=8000, debug=False):
        """Run the API server"""
        logger.info(f"Starting Collective Memory API server on {host}:{port}")
        self.socketio.run(self.app, host=host, port=port, debug=debug)

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Collective Memory REST API Server')
    parser.add_argument('--data-folder', '-d', default=os.getcwd(),
                      help='Data folder to index (default: current directory)')
    parser.add_argument('--host', default='127.0.0.1',
                      help='Host to bind to (default: 127.0.0.1)')
    parser.add_argument('--port', '-p', type=int, default=8000,
                      help='Port to bind to (default: 8000)')
    parser.add_argument('--debug', action='store_true',
                      help='Enable debug mode')
    
    args = parser.parse_args()
    
    # Create and run API server
    api = CollectiveMemoryAPI(data_folder=args.data_folder)
    api.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == '__main__':
    main() 