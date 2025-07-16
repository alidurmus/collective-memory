"""
Memory Manager Core for Collective Memory v3.0
A-Mem + Mem0 Hybrid Memory System
"""

import os
import json
import logging
import threading
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import numpy as np
from pathlib import Path
import hashlib
import sqlite3

# Import our custom modules
from .memory_database import MemoryDatabase, MemoryEvolutionEngine
from .importance_scorer import ImportanceScorer
from ..cursor.cursor_integration import CursorIntegrationManager, CursorConversation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MemoryCreationRequest:
    """Request for creating a new memory."""
    content: str
    context: str = None
    memory_type: str = "fact"
    importance_score: float = None
    project_path: str = None
    cursor_session_id: str = None
    metadata: Dict = None
    auto_link: bool = True

@dataclass
class MemorySearchRequest:
    """Request for searching memories."""
    query: str = None
    memory_type: str = None
    project_path: str = None
    min_importance: float = 0.0
    max_results: int = 10
    include_links: bool = True
    semantic_search: bool = False

@dataclass
class MemoryUpdateRequest:
    """Request for updating a memory."""
    memory_id: int
    content: str = None
    importance_score: float = None
    status: str = None
    evolution_reason: str = None
    auto_relink: bool = True

class MemoryManager:
    """
    Core Memory Manager - A-Mem + Mem0 Hybrid System
    
    Features:
    - Intelligent memory storage and retrieval
    - Automatic importance scoring
    - Dynamic memory evolution (ADD/UPDATE/DELETE/NOOP)
    - Automatic memory linking (Zettelkasten style)
    - Cursor integration for real-time context
    - Semantic search capabilities
    - Performance optimization
    """
    
    def __init__(self, config: Dict = None):
        """Initialize Memory Manager."""
        self.config = config or self._load_default_config()
        
        # Initialize core components
        self.database = MemoryDatabase(self.config.get('database_path', 'data/memory_system.db'))
        self.importance_scorer = ImportanceScorer()
        self.evolution_engine = MemoryEvolutionEngine(self.database)
        
        # Initialize Cursor integration
        self.cursor_integration = CursorIntegrationManager(memory_database=self.database)
        
        # Memory cache for performance
        self.memory_cache = {}
        self.cache_size = self.config.get('cache_size', 1000)
        self.cache_lock = threading.Lock()
        
        # Performance metrics
        self.metrics = {
            'total_memories': 0,
            'search_requests': 0,
            'avg_search_time': 0.0,
            'cache_hits': 0,
            'cache_misses': 0
        }
        
        # Auto-linking settings
        self.auto_linking_enabled = self.config.get('auto_linking_enabled', True)
        self.linking_threshold = self.config.get('linking_threshold', 0.7)
        
        # Start background tasks
        self._start_background_tasks()
        
        logger.info("Memory Manager initialized successfully")
    
    def _load_default_config(self) -> Dict:
        """Load default configuration."""
        return {
            'database_path': 'data/memory_system.db',
            'cache_size': 1000,
            'auto_linking_enabled': True,
            'linking_threshold': 0.7,
            'cleanup_interval_hours': 24,
            'cursor_monitoring_enabled': True,
            'semantic_search_enabled': True,
            'max_memories': 10000,
            'importance_threshold': 0.3
        }
    
    def _start_background_tasks(self):
        """Start background tasks."""
        # Start periodic cleanup
        cleanup_thread = threading.Thread(target=self._periodic_cleanup, daemon=True)
        cleanup_thread.start()
        
        # Start Cursor monitoring if enabled
        if self.config.get('cursor_monitoring_enabled', True):
            self._start_cursor_monitoring()
    
    def _start_cursor_monitoring(self):
        """Start Cursor real-time monitoring."""
        try:
            success = self.cursor_integration.start_real_time_monitoring()
            if success:
                logger.info("Cursor monitoring started")
            else:
                logger.warning("Cursor monitoring failed to start")
        except Exception as e:
            logger.error(f"Error starting Cursor monitoring: {e}")
    
    def _periodic_cleanup(self):
        """Periodic cleanup of old memories."""
        while True:
            try:
                # Sleep for cleanup interval
                interval = self.config.get('cleanup_interval_hours', 24) * 3600
                threading.Event().wait(interval)
                
                # Perform cleanup
                self._cleanup_old_memories()
                
            except Exception as e:
                logger.error(f"Error in periodic cleanup: {e}")
    
    def _cleanup_old_memories(self):
        """Clean up old, low-importance memories."""
        try:
            # Get cleanup settings
            max_memories = self.config.get('max_memories', 10000)
            importance_threshold = self.config.get('importance_threshold', 0.3)
            
            # Count current memories
            stats = self.database.get_system_stats()
            current_count = stats['memories']['total_memories']
            
            if current_count > max_memories:
                # Archive old memories
                archived_count = self.database.cleanup_old_memories(days_old=30)
                logger.info(f"Archived {archived_count} old memories")
                
                # Clear cache
                self._clear_cache()
                
        except Exception as e:
            logger.error(f"Error in memory cleanup: {e}")
    
    # ================================
    # CORE MEMORY OPERATIONS
    # ================================
    
    def create_memory(self, request: MemoryCreationRequest) -> int:
        """Create a new memory."""
        try:
            start_time = datetime.now()
            
            # Calculate importance score if not provided
            if request.importance_score is None:
                request.importance_score = self.importance_scorer.calculate_importance(
                    content=request.content,
                    memory_type=request.memory_type,
                    context=request.context,
                    metadata=request.metadata
                )
            
            # Store memory in database
            memory_id = self.database.store_memory(
                content=request.content,
                context=request.context,
                memory_type=request.memory_type,
                importance_score=request.importance_score,
                project_path=request.project_path,
                cursor_session_id=request.cursor_session_id,
                metadata=request.metadata
            )
            
            # Auto-link if enabled
            if request.auto_link and self.auto_linking_enabled:
                self._auto_link_memory(memory_id, request.content, request.context)
            
            # Update cache
            self._update_memory_cache(memory_id)
            
            # Update metrics
            self.metrics['total_memories'] += 1
            
            processing_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"Memory created: {memory_id} (importance: {request.importance_score:.3f}, time: {processing_time:.3f}s)")
            
            return memory_id
            
        except Exception as e:
            logger.error(f"Error creating memory: {e}")
            raise
    
    def search_memories(self, request: MemorySearchRequest) -> List[Dict]:
        """Search for memories."""
        try:
            start_time = datetime.now()
            
            # Check cache first
            cache_key = self._generate_cache_key(request)
            cached_result = self._get_from_cache(cache_key)
            
            if cached_result:
                self.metrics['cache_hits'] += 1
                return cached_result
            
            # Search in database
            memories = self.database.retrieve_memories(
                query=request.query,
                memory_type=request.memory_type,
                project_path=request.project_path,
                limit=request.max_results,
                min_importance=request.min_importance
            )
            
            # Add links if requested
            if request.include_links:
                for memory in memories:
                    links = self.database.get_memory_links(memory['id'])
                    memory['links'] = links
            
            # Semantic search enhancement (if enabled)
            if request.semantic_search and self.config.get('semantic_search_enabled', True):
                memories = self._enhance_with_semantic_search(memories, request.query)
            
            # Cache result
            self._add_to_cache(cache_key, memories)
            self.metrics['cache_misses'] += 1
            
            # Update metrics
            self.metrics['search_requests'] += 1
            processing_time = (datetime.now() - start_time).total_seconds()
            current_avg = self.metrics['avg_search_time']
            self.metrics['avg_search_time'] = (current_avg + processing_time) / 2
            
            logger.info(f"Search completed: {len(memories)} results (time: {processing_time:.3f}s)")
            
            return memories
            
        except Exception as e:
            logger.error(f"Error searching memories: {e}")
            raise
    
    def update_memory(self, request: MemoryUpdateRequest) -> bool:
        """Update an existing memory."""
        try:
            # Get current memory
            current_memories = self.database.retrieve_memories(limit=1)
            current_memory = None
            
            for memory in current_memories:
                if memory['id'] == request.memory_id:
                    current_memory = memory
                    break
            
            if not current_memory:
                logger.warning(f"Memory not found for update: {request.memory_id}")
                return False
            
            # Update importance score if content changed
            if request.content and request.importance_score is None:
                request.importance_score = self.importance_scorer.calculate_importance(
                    content=request.content,
                    memory_type=current_memory['memory_type'],
                    context=current_memory['context'],
                    metadata=current_memory
                )
            
            # Update in database
            success = self.database.update_memory(
                memory_id=request.memory_id,
                content=request.content,
                importance_score=request.importance_score,
                status=request.status,
                evolution_reason=request.evolution_reason
            )
            
            if success:
                # Re-link if content changed
                if request.auto_relink and request.content:
                    self._auto_link_memory(request.memory_id, request.content, current_memory['context'])
                
                # Update cache
                self._update_memory_cache(request.memory_id)
                
                logger.info(f"Memory updated: {request.memory_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error updating memory: {e}")
            raise
    
    def delete_memory(self, memory_id: int, soft_delete: bool = True) -> bool:
        """Delete a memory."""
        try:
            success = self.database.delete_memory(memory_id, soft_delete)
            
            if success:
                # Remove from cache
                self._remove_from_cache(memory_id)
                
                # Update metrics
                self.metrics['total_memories'] -= 1
                
                logger.info(f"Memory deleted: {memory_id} (soft: {soft_delete})")
            
            return success
            
        except Exception as e:
            logger.error(f"Error deleting memory: {e}")
            raise
    
    # ================================
    # MEMORY EVOLUTION (Mem0 inspired)
    # ================================
    
    def process_user_interaction(self, user_input: str, ai_response: str,
                               context: str, cursor_session_id: str = None) -> Dict:
        """Process user-AI interaction and evolve memory."""
        try:
            # Use evolution engine
            result = self.evolution_engine.process_interaction(
                user_input=user_input,
                ai_response=ai_response,
                context=context,
                cursor_session_id=cursor_session_id
            )
            
            # Update cache for any created/updated memories
            for action in result['actions_taken']:
                if action['action'] in ['ADD', 'UPDATE']:
                    self._update_memory_cache(action['memory_id'])
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing interaction: {e}")
            raise
    
    def evolve_memory_from_cursor(self, conversations: List[CursorConversation]) -> Dict:
        """Evolve memory from Cursor conversations."""
        try:
            evolution_results = []
            
            for conversation in conversations:
                # Convert conversation to interactions
                messages = conversation.messages
                
                for i in range(0, len(messages) - 1, 2):
                    if i + 1 < len(messages):
                        user_msg = messages[i]
                        ai_msg = messages[i + 1]
                        
                        if user_msg.get('role') == 'user' and ai_msg.get('role') == 'assistant':
                            result = self.process_user_interaction(
                                user_input=user_msg.get('content', ''),
                                ai_response=ai_msg.get('content', ''),
                                context=f"Project: {conversation.project_path}",
                                cursor_session_id=conversation.session_id
                            )
                            evolution_results.append(result)
            
            return {
                'conversations_processed': len(conversations),
                'evolution_results': evolution_results
            }
            
        except Exception as e:
            logger.error(f"Error evolving memory from Cursor: {e}")
            raise
    
    # ================================
    # AUTO-LINKING (Zettelkasten inspired)
    # ================================
    
    def _auto_link_memory(self, memory_id: int, content: str, context: str = None):
        """Automatically create links to related memories."""
        try:
            if not self.auto_linking_enabled:
                return
            
            # Find similar memories
            similar_memories = self.database.retrieve_memories(
                query=content[:100],  # Use first 100 chars for similarity
                limit=10,
                min_importance=0.3
            )
            
            # Create links to similar memories
            for similar_memory in similar_memories:
                if similar_memory['id'] != memory_id:
                    # Calculate link strength
                    link_strength = self._calculate_link_strength(
                        content, similar_memory['content']
                    )
                    
                    if link_strength >= self.linking_threshold:
                        # Determine relationship type
                        relationship_type = self._determine_relationship_type(
                            content, similar_memory['content']
                        )
                        
                        # Create link
                        self.database.create_memory_link(
                            memory_id_1=memory_id,
                            memory_id_2=similar_memory['id'],
                            relationship_type=relationship_type,
                            strength=link_strength,
                            is_auto_generated=True
                        )
        
        except Exception as e:
            logger.error(f"Error auto-linking memory {memory_id}: {e}")
    
    def _calculate_link_strength(self, content1: str, content2: str) -> float:
        """Calculate link strength between two contents."""
        # Simple word overlap calculation
        words1 = set(content1.lower().split())
        words2 = set(content2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def _determine_relationship_type(self, content1: str, content2: str) -> str:
        """Determine relationship type between two contents."""
        # Simple heuristic-based relationship detection
        
        # Check for contradiction
        if any(word in content1.lower() for word in ['not', 'no', 'never', 'wrong']):
            return 'contradicts'
        
        # Check for causation
        if any(word in content1.lower() for word in ['because', 'since', 'due to']):
            return 'caused_by'
        
        # Check for examples
        if any(word in content1.lower() for word in ['example', 'instance', 'such as']):
            return 'example_of'
        
        # Check for dependency
        if any(word in content1.lower() for word in ['depends', 'requires', 'needs']):
            return 'depends_on'
        
        # Default to related
        return 'related_to'
    
    # ================================
    # SEMANTIC SEARCH ENHANCEMENT
    # ================================
    
    def _enhance_with_semantic_search(self, memories: List[Dict], query: str) -> List[Dict]:
        """Enhance search results with semantic similarity."""
        try:
            # This is a placeholder for semantic search enhancement
            # In a real implementation, you would use sentence transformers
            # or other embedding models to calculate semantic similarity
            
            # For now, just return the memories as-is
            return memories
            
        except Exception as e:
            logger.error(f"Error in semantic search enhancement: {e}")
            return memories
    
    # ================================
    # CACHE MANAGEMENT
    # ================================
    
    def _generate_cache_key(self, request: MemorySearchRequest) -> str:
        """Generate cache key for search request."""
        key_data = {
            'query': request.query,
            'memory_type': request.memory_type,
            'project_path': request.project_path,
            'min_importance': request.min_importance,
            'max_results': request.max_results
        }
        
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _get_from_cache(self, key: str) -> Optional[List[Dict]]:
        """Get result from cache."""
        with self.cache_lock:
            return self.memory_cache.get(key)
    
    def _add_to_cache(self, key: str, data: List[Dict]):
        """Add result to cache."""
        with self.cache_lock:
            # Remove oldest entries if cache is full
            if len(self.memory_cache) >= self.cache_size:
                oldest_key = next(iter(self.memory_cache))
                del self.memory_cache[oldest_key]
            
            self.memory_cache[key] = data
    
    def _update_memory_cache(self, memory_id: int):
        """Update cache after memory change."""
        with self.cache_lock:
            # Simple cache invalidation - clear all entries
            # In a more sophisticated implementation, you would
            # selectively invalidate only affected entries
            self.memory_cache.clear()
    
    def _remove_from_cache(self, memory_id: int):
        """Remove memory from cache."""
        with self.cache_lock:
            # Simple cache invalidation
            self.memory_cache.clear()
    
    def _clear_cache(self):
        """Clear entire cache."""
        with self.cache_lock:
            self.memory_cache.clear()
    
    # ================================
    # CONTEXT SUGGESTIONS
    # ================================
    
    def suggest_context_for_cursor(self, current_input: str,
                                  project_path: str = None,
                                  max_suggestions: int = 5) -> List[Dict]:
        """Suggest relevant context for Cursor based on current input."""
        try:
            # Search for relevant memories
            search_request = MemorySearchRequest(
                query=current_input,
                project_path=project_path,
                max_results=max_suggestions * 2,  # Get more to filter
                min_importance=0.5,
                include_links=True
            )
            
            memories = self.search_memories(search_request)
            
            # Convert to context suggestions
            suggestions = []
            for memory in memories[:max_suggestions]:
                suggestion = {
                    'content': memory['content'],
                    'type': memory['memory_type'],
                    'importance': memory['importance_score'],
                    'relevance': self._calculate_relevance(current_input, memory['content']),
                    'context': memory.get('context', ''),
                    'memory_id': memory['id']
                }
                suggestions.append(suggestion)
            
            # Sort by relevance
            suggestions.sort(key=lambda x: x['relevance'], reverse=True)
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Error suggesting context: {e}")
            return []
    
    def _calculate_relevance(self, input_text: str, memory_content: str) -> float:
        """Calculate relevance score between input and memory content."""
        # Simple word overlap relevance
        input_words = set(input_text.lower().split())
        memory_words = set(memory_content.lower().split())
        
        if not input_words or not memory_words:
            return 0.0
        
        intersection = len(input_words & memory_words)
        union = len(input_words | memory_words)
        
        return intersection / union if union > 0 else 0.0
    
    # ================================
    # SYSTEM MANAGEMENT
    # ================================
    
    def get_system_status(self) -> Dict:
        """Get comprehensive system status."""
        try:
            # Get database stats
            db_stats = self.database.get_system_stats()
            
            # Get cache stats
            cache_stats = {
                'cache_size': len(self.memory_cache),
                'cache_hits': self.metrics['cache_hits'],
                'cache_misses': self.metrics['cache_misses'],
                'hit_rate': self.metrics['cache_hits'] / (self.metrics['cache_hits'] + self.metrics['cache_misses']) if (self.metrics['cache_hits'] + self.metrics['cache_misses']) > 0 else 0.0
            }
            
            # Get cursor integration status
            cursor_status = {
                'monitoring_enabled': self.config.get('cursor_monitoring_enabled', True),
                'monitoring_active': self.cursor_integration.monitor.monitoring
            }
            
            return {
                'database': db_stats,
                'cache': cache_stats,
                'cursor_integration': cursor_status,
                'performance': self.metrics,
                'config': self.config
            }
            
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {'error': str(e)}
    
    def shutdown(self):
        """Shutdown memory manager."""
        try:
            # Stop Cursor monitoring
            self.cursor_integration.stop_real_time_monitoring()
            
            # Clear cache
            self._clear_cache()
            
            # Close database
            self.database.close()
            
            logger.info("Memory Manager shutdown completed")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")

# Example usage
if __name__ == "__main__":
    # Create memory manager
    manager = MemoryManager()
    
    # Test memory creation
    request = MemoryCreationRequest(
        content="We decided to use React for the frontend framework",
        memory_type="decision",
        context="Frontend architecture discussion",
        project_path="/home/user/myproject"
    )
    
    memory_id = manager.create_memory(request)
    print(f"Created memory: {memory_id}")
    
    # Test memory search
    search_request = MemorySearchRequest(
        query="React frontend",
        max_results=5
    )
    
    results = manager.search_memories(search_request)
    print(f"Search results: {len(results)}")
    
    # Test context suggestions
    suggestions = manager.suggest_context_for_cursor(
        "How to set up React components?",
        project_path="/home/user/myproject"
    )
    print(f"Context suggestions: {len(suggestions)}")
    
    # Get system status
    status = manager.get_system_status()
    print(f"System status: {status}")
    
    # Shutdown
    manager.shutdown() 