"""
Memory Manager Core for Collective Memory v3.0
A-Mem + Mem0 Hybrid Memory System
"""

import json
import logging
import threading
from typing import Dict, List, Optional, Any
from datetime import datetime
import hashlib
from dataclasses import dataclass

# Project imports (relative)
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
    context: Optional[str] = None
    memory_type: str = "fact"
    importance_score: Optional[float] = None
    project_path: Optional[str] = None
    cursor_session_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    auto_link: bool = True


@dataclass
class MemorySearchRequest:
    """Request for searching memories."""

    query: Optional[str] = None
    memory_type: Optional[str] = None
    project_path: Optional[str] = None
    min_importance: float = 0.0
    max_results: int = 10
    include_links: bool = True
    semantic_search: bool = False


@dataclass
class MemoryUpdateRequest:
    """Request for updating a memory."""

    memory_id: int
    content: Optional[str] = None
    importance_score: Optional[float] = None
    status: Optional[str] = None
    evolution_reason: Optional[str] = None
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

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize Memory Manager."""
        self.config = config or self._load_default_config()

        # Initialize core components
        self.database = MemoryDatabase(
            self.config.get("database_path", "../data/memory_system.db")
        )
        self.importance_scorer = ImportanceScorer()
        self.evolution_engine = MemoryEvolutionEngine(self.database)

        # Initialize Cursor integration
        self.cursor_integration = CursorIntegrationManager(
            memory_database=self.database
        )

        # Memory cache for performance
        self.memory_cache: Dict[str, List[Dict[str, Any]]] = {}
        self.cache_size = self.config.get("cache_size", 1000)
        self.cache_lock = threading.Lock()

        # Performance metrics
        self.metrics = {
            "total_memories": 0,
            "search_requests": 0,
            "avg_search_time": 0.0,
            "cache_hits": 0,
            "cache_misses": 0,
        }

        # Auto-linking settings
        self.auto_linking_enabled = self.config.get("auto_linking_enabled", True)
        self.linking_threshold = self.config.get("linking_threshold", 0.7)

        # Start background tasks
        self._start_background_tasks()

        logger.info("Memory Manager initialized successfully")

    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration."""
        return {
            "database_path": "../data/memory_system.db",
            "cache_size": 1000,
            "auto_linking_enabled": True,
            "linking_threshold": 0.7,
            "cleanup_interval_hours": 24,
            "cursor_monitoring_enabled": True,
            "semantic_search_enabled": True,
            "max_memories": 10000,
        }

    def _start_background_tasks(self):
        """Start background tasks."""
        # Start periodic cleanup
        cleanup_thread = threading.Thread(
            target=self._periodic_cleanup, daemon=True
        )
        cleanup_thread.start()

        # Start Cursor monitoring if enabled
        if self.config.get("cursor_monitoring_enabled", True):
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
            logger.error("Error starting Cursor monitoring: %s", e)

    def _periodic_cleanup(self):
        """Periodic cleanup of old memories."""
        while True:
            try:
                # Sleep for cleanup interval
                interval = self.config.get("cleanup_interval_hours", 24) * 3600
                threading.Event().wait(interval)

                # Perform cleanup
                self._cleanup_old_memories()

            except Exception as e:
                logger.error("Error in periodic cleanup: %s", e)

    def _cleanup_old_memories(self):
        """Clean up old, low-importance memories."""
        try:
            # Get cleanup settings
            max_memories = self.config.get("max_memories", 10000)

            # Count current memories
            stats = self.database.get_system_stats()
            current_count = stats["memories"]["total_memories"]

            if current_count > max_memories:
                # Archive old memories
                archived_count = self.database.cleanup_old_memories(days_old=30)
                logger.info("Archived %d old memories", archived_count)

                # Clear cache
                self._clear_cache()

        except Exception as e:
            logger.error("Error in memory cleanup: %s", e)

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
                    context=request.context or "",
                    metadata=request.metadata or {},
                )

            # Store memory in database
            memory_id = self.database.store_memory(
                content=request.content,
                memory_type=request.memory_type,
                importance_score=request.importance_score,
                context=request.context,
                project_path=request.project_path,
                cursor_session_id=request.cursor_session_id,
                metadata=request.metadata,
            )

            # Auto-link if enabled
            if request.auto_link and memory_id is not None:
                self._auto_link_memory(
                    memory_id, request.content, request.context
                )

            # Update cache
            if memory_id is not None:
                self._update_memory_cache(memory_id)

            # Update metrics
            self.metrics["total_memories"] += 1

            processing_time = (datetime.now() - start_time).total_seconds()
            logger.info(
                "Memory created in %.3f seconds (ID: %s)",
                processing_time,
                memory_id,
            )

            return memory_id or 0

        except Exception as e:
            logger.error("Error creating memory: %s", e)
            return 0

    def search_memories(self, request: MemorySearchRequest) -> List[Dict[str, Any]]:
        """Search memories based on criteria."""
        try:
            start_time = datetime.now()

            # Check cache first
            cache_key = self._generate_cache_key(request)
            cached_result = self._get_from_cache(cache_key)
            if cached_result is not None:
                self.metrics["cache_hits"] += 1
                return cached_result

            self.metrics["cache_misses"] += 1

            # Build search parameters
            search_params = {
                "query": request.query,
                "memory_type": request.memory_type,
                "project_path": request.project_path,
                "min_importance": request.min_importance,
                "limit": request.max_results,
            }

            # Remove None values
            search_params = {k: v for k, v in search_params.items() if v is not None}

            # Search database
            memories = self.database.retrieve_memories(**search_params)

            # Enhance with semantic search if enabled
            if request.semantic_search and request.query:
                memories = self._enhance_with_semantic_search(
                    memories, request.query
                )

            # Include links if requested
            if request.include_links:
                for memory in memories:
                    memory["links"] = self.database.get_memory_links(
                        memory["id"]
                    )

            # Cache results
            self._add_to_cache(cache_key, memories)

            # Update metrics
            self.metrics["search_requests"] += 1
            processing_time = (datetime.now() - start_time).total_seconds()
            self.metrics["avg_search_time"] = (
                self.metrics["avg_search_time"] + processing_time
            ) / 2

            logger.info(
                "Search completed in %.3f seconds (%d results)",
                processing_time,
                len(memories),
            )

            return memories

        except Exception as e:
            logger.error("Error searching memories: %s", e)
            return []

    def update_memory(self, request: MemoryUpdateRequest) -> bool:
        """Update an existing memory."""
        try:
            # Get current memory
            current_memory = self.database.retrieve_memory(request.memory_id)
            if not current_memory:
                logger.warning("Memory %d not found", request.memory_id)
                return False

            # Prepare update data
            updates = []
            if request.content is not None:
                updates.append(("content", request.content))
            if request.importance_score is not None:
                updates.append(("importance_score", request.importance_score))
            if request.status is not None:
                updates.append(("status", request.status))

            # Update in database
            success = self.database.update_memory(
                request.memory_id, updates
            )

            if success and request.auto_relink:
                # Re-link memory
                content = request.content or current_memory["content"]
                self._auto_link_memory(
                    request.memory_id, content, current_memory.get("context")
                )

            # Update cache
            if success:
                self._update_memory_cache(request.memory_id)

            logger.info("Memory %d updated successfully", request.memory_id)
            return success

        except Exception as e:
            logger.error("Error updating memory: %s", e)
            return False

    def delete_memory(self, memory_id: int, soft_delete: bool = True) -> bool:
        """Delete a memory."""
        try:
            success = self.database.delete_memory(memory_id, soft_delete)
            if success:
                self._remove_from_cache(memory_id)
                logger.info("Memory %d deleted successfully", memory_id)
            return success

        except Exception as e:
            logger.error("Error deleting memory: %s", e)
            return False

    def process_user_interaction(
        self,
        user_input: str,
        ai_response: str,
        context: str,
        cursor_session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Process a user-AI interaction and evolve memory."""
        try:
            # Extract facts from interaction
            extracted_facts = self._extract_facts(user_input, ai_response)

            actions_taken = []

            for fact in extracted_facts:
                # Determine action needed
                action = self._determine_action(fact, context)

                if action == "ADD":
                    memory_id = self.database.store_memory(
                        content=fact["content"],
                        memory_type="fact",
                        context=context,
                        cursor_session_id=cursor_session_id,
                    )
                    actions_taken.append({"action": "ADD", "memory_id": memory_id})

                elif action == "UPDATE":
                    related_memory = self._find_related_memory(fact["content"])
                    if related_memory:
                        self.database.update_memory(
                            related_memory["id"],
                            [("content", fact["content"])],
                        )
                        actions_taken.append(
                            {"action": "UPDATE", "memory_id": related_memory["id"]}
                        )

                elif action == "DELETE":
                    contradicted_memory = self._find_contradicted_memory(
                        fact["content"]
                    )
                    if contradicted_memory is not None:
                        self.database.delete_memory(contradicted_memory["id"])
                        actions_taken.append(
                            {
                                "action": "DELETE",
                                "memory_id": contradicted_memory["id"],
                            }
                        )

            return {
                "facts_extracted": len(extracted_facts),
                "actions_taken": actions_taken,
                "success": True,
            }

        except Exception as e:
            logger.error("Error processing interaction: %s", e)
            return {"success": False, "error": str(e)}

    def evolve_memory_from_cursor(
        self, conversations: List[CursorConversation]
    ) -> Dict[str, Any]:
        """Evolve memory from Cursor conversations."""
        try:
            total_memories = 0
            evolved_count = 0

            for conversation in conversations:
                # Extract memories from conversation
                memories = self._extract_memories_from_conversation(conversation)

                for memory_data in memories:
                    total_memories += 1

                    # Check if memory already exists
                    existing = self.database.retrieve_memories(
                        query=memory_data["content"], limit=1
                    )

                    if existing:
                        # Update existing memory
                        self.database.update_memory(
                            existing[0]["id"],
                            [("content", memory_data["content"])],
                        )
                    else:
                        # Create new memory
                        self.database.store_memory(
                            content=memory_data["content"],
                            memory_type="conversation",
                            context=memory_data.get("context"),
                        )

                    evolved_count += 1

            return {
                "total_conversations": len(conversations),
                "total_memories": total_memories,
                "evolved_count": evolved_count,
                "success": True,
            }

        except Exception as e:
            logger.error("Error evolving memory from Cursor: %s", e)
            return {"success": False, "error": str(e)}

    def _auto_link_memory(
        self, memory_id: int, content: str, context: Optional[str] = None
    ):
        """Automatically link memory to related memories."""
        if not self.auto_linking_enabled or memory_id is None:
            return

        try:
            # Find related memories
            related_memories = self.database.retrieve_memories(
                query=content, limit=10
            )

            for related in related_memories:
                if related["id"] != memory_id:
                    # Calculate link strength
                    strength = self._calculate_link_strength(
                        content, related["content"]
                    )

                    if strength >= self.linking_threshold:
                        # Create link
                        relationship_type = self._determine_relationship_type(
                            content, related["content"]
                        )

                        self.database.create_memory_link(
                            memory_id, related["id"], relationship_type, strength
                        )

        except Exception as e:
            logger.error("Error auto-linking memory: %s", e)

    def _calculate_link_strength(self, content1: str, content2: str) -> float:
        """Calculate semantic similarity between two contents."""
        try:
            # Simple keyword overlap for now
            words1 = set(content1.lower().split())
            words2 = set(content2.lower().split())

            if not words1 or not words2:
                return 0.0

            intersection = words1.intersection(words2)
            union = words1.union(words2)

            return len(intersection) / len(union)

        except Exception as e:
            logger.error("Error calculating link strength: %s", e)
            return 0.0

    def _determine_relationship_type(self, content1: str, content2: str) -> str:
        """Determine the type of relationship between two memories."""
        # Simple heuristic for now
        if any(word in content2.lower() for word in content1.lower().split()[:3]):
            return "elaborates"
        elif any(word in content1.lower() for word in content2.lower().split()[:3]):
            return "elaborated_by"
        else:
            return "related"

    def _enhance_with_semantic_search(
        self, memories: List[Dict[str, Any]], query: str
    ) -> List[Dict[str, Any]]:
        """Enhance search results with semantic similarity."""
        try:
            # Simple semantic enhancement for now
            enhanced_memories = []
            for memory in memories:
                relevance = self._calculate_relevance(query, memory["content"])
                memory["semantic_relevance"] = relevance
                enhanced_memories.append(memory)

            # Sort by semantic relevance
            enhanced_memories.sort(
                key=lambda x: x.get("semantic_relevance", 0), reverse=True
            )

            return enhanced_memories

        except Exception as e:
            logger.error("Error in semantic search enhancement: %s", e)
            return memories

    def _generate_cache_key(self, request: MemorySearchRequest) -> str:
        """Generate cache key for search request."""
        try:
            key_data = {
                "query": request.query,
                "memory_type": request.memory_type,
                "project_path": request.project_path,
                "min_importance": request.min_importance,
                "max_results": request.max_results,
                "include_links": request.include_links,
                "semantic_search": request.semantic_search,
            }

            # Create hash of key data
            key_string = json.dumps(key_data, sort_keys=True)
            return hashlib.md5(key_string.encode()).hexdigest()

        except Exception as e:
            logger.error("Error generating cache key: %s", e)
            return ""

    def _get_from_cache(self, key: str) -> Optional[List[Dict[str, Any]]]:
        """Get data from cache."""
        try:
            with self.cache_lock:
                return self.memory_cache.get(key)
        except Exception as e:
            logger.error("Error getting from cache: %s", e)
            return None

    def _add_to_cache(self, key: str, data: List[Dict[str, Any]]):
        """Add data to cache."""
        try:
            with self.cache_lock:
                # Check cache size
                if len(self.memory_cache) >= self.cache_size:
                    # Remove oldest entry
                    oldest_key = next(iter(self.memory_cache))
                    del self.memory_cache[oldest_key]

                self.memory_cache[key] = data

        except Exception as e:
            logger.error("Error adding to cache: %s", e)

    def _update_memory_cache(self, memory_id: int):
        """Update cache when memory is modified."""
        try:
            with self.cache_lock:
                # Remove cache entries that might be affected
                keys_to_remove = []
                for key in self.memory_cache:
                    # Simple heuristic: remove if key contains memory_id
                    if str(memory_id) in key:
                        keys_to_remove.append(key)

                for key in keys_to_remove:
                    del self.memory_cache[key]

        except Exception as e:
            logger.error("Error updating memory cache: %s", e)

    def _remove_from_cache(self, memory_id: int):
        """Remove memory from cache."""
        self._update_memory_cache(memory_id)

    def _clear_cache(self):
        """Clear entire cache."""
        try:
            with self.cache_lock:
                self.memory_cache.clear()
        except Exception as e:
            logger.error("Error clearing cache: %s", e)

    def suggest_context_for_cursor(
        self,
        current_input: str,
        project_path: Optional[str] = None,
        max_suggestions: int = 5,
    ) -> List[Dict[str, Any]]:
        """Suggest relevant context for Cursor based on current input."""
        try:
            # Search for relevant memories
            search_request = MemorySearchRequest(
                query=current_input,
                project_path=project_path,
                max_results=max_suggestions * 2,  # Get more for filtering
                semantic_search=True,
            )

            memories = self.search_memories(search_request)

            # Calculate relevance and filter
            suggestions = []
            for memory in memories:
                relevance = self._calculate_relevance(
                    current_input, memory["content"]
                )
                if relevance > 0.3:  # Minimum relevance threshold
                    suggestions.append(
                        {
                            "memory_id": memory["id"],
                            "content": memory["content"],
                            "relevance": relevance,
                            "memory_type": memory.get("memory_type", "unknown"),
                        }
                    )

            # Sort by relevance and limit
            suggestions.sort(key=lambda x: x["relevance"], reverse=True)
            return suggestions[:max_suggestions]

        except Exception as e:
            logger.error("Error suggesting context: %s", e)
            return []

    def _calculate_relevance(self, input_text: str, memory_content: str) -> float:
        """Calculate relevance between input text and memory content."""
        try:
            # Simple keyword-based relevance
            input_words = set(input_text.lower().split())
            memory_words = set(memory_content.lower().split())

            if not input_words or not memory_words:
                return 0.0

            intersection = input_words.intersection(memory_words)
            return len(intersection) / len(input_words)

        except Exception as e:
            logger.error("Error calculating relevance: %s", e)
            return 0.0

    def get_system_status(self) -> Dict[str, Any]:
        """Get system status and metrics."""
        try:
            # Get database stats
            db_stats = self.database.get_system_stats()

            # Get Cursor integration status
            cursor_status = {
                "monitoring_active": getattr(
                    self.cursor_integration, "is_monitoring_active", False
                ),
                "last_sync": getattr(
                    self.cursor_integration, "get_last_sync_time", lambda: None
                )(),
            }

            return {
                "database": db_stats,
                "cursor_integration": cursor_status,
                "cache": {
                    "size": len(self.memory_cache),
                    "max_size": self.cache_size,
                    "hits": self.metrics["cache_hits"],
                    "misses": self.metrics["cache_misses"],
                },
                "metrics": self.metrics,
                "config": {
                    "auto_linking_enabled": self.auto_linking_enabled,
                    "linking_threshold": self.linking_threshold,
                },
            }

        except Exception as e:
            logger.error("Error getting system status: %s", e)
            return {"error": str(e)}

    def shutdown(self):
        """Shutdown the memory manager."""
        try:
            # Stop Cursor monitoring
            if hasattr(self.cursor_integration, "stop_monitoring"):
                self.cursor_integration.stop_monitoring()

            # Clear cache
            self._clear_cache()

            # Close database connections
            if hasattr(self.database, "close"):
                self.database.close()

            logger.info("Memory Manager shutdown complete")

        except Exception as e:
            logger.error("Error during shutdown: %s", e)

    # ================================
    # HELPER METHODS
    # ================================

    def _extract_facts(self, user_input: str, ai_response: str) -> List[Dict[str, Any]]:
        """Extract facts from user-AI interaction."""
        try:
            facts = []

            # Simple fact extraction for now
            # Look for declarative statements in AI response
            sentences = ai_response.split(".")
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) > 10 and any(
                    word in sentence.lower()
                    for word in ["is", "are", "was", "were", "has", "have"]
                ):
                    facts.append({"content": sentence, "source": "ai_response"})

            return facts

        except Exception as e:
            logger.error("Error extracting facts: %s", e)
            return []

    def _determine_action(
        self, fact: Dict[str, Any], context: str
    ) -> str:
        """Determine what action to take for a fact."""
        try:
            # Simple action determination for now
            content = fact["content"].lower()

            # Check for contradictions
            if any(word in content for word in ["not", "never", "false", "wrong"]):
                return "DELETE"

            # Check for updates
            if any(word in content for word in ["update", "change", "modify"]):
                return "UPDATE"

            # Default to ADD
            return "ADD"

        except Exception as e:
            logger.error("Error determining action: %s", e)
            return "NOOP"

    def _find_related_memory(self, content: str) -> Optional[Dict[str, Any]]:
        """Find a related memory for the given content."""
        try:
            memories = self.database.retrieve_memories(query=content, limit=1)
            return memories[0] if memories else None

        except Exception as e:
            logger.error("Error finding related memory: %s", e)
            return None

    def _find_contradicted_memory(self, content: str) -> Optional[Dict[str, Any]]:
        """Find a memory that contradicts the given content."""
        try:
            # Look for memories with opposite meaning
            opposite_keywords = ["not", "never", "false", "wrong"]
            if any(word in content.lower() for word in opposite_keywords):
                # Find positive version
                positive_content = content.lower()
                for word in opposite_keywords:
                    positive_content = positive_content.replace(word, "")
                positive_content = positive_content.strip()

                memories = self.database.retrieve_memories(
                    query=positive_content, limit=1
                )
                return memories[0] if memories else None

            return None

        except Exception as e:
            logger.error("Error finding contradicted memory: %s", e)
            return None

    def _extract_memories_from_conversation(
        self, conversation: CursorConversation
    ) -> List[Dict[str, Any]]:
        """Extract memories from a Cursor conversation."""
        try:
            memories = []

            # Extract from conversation content
            if hasattr(conversation, "content") and conversation.content:
                # Split into sentences and extract facts
                sentences = conversation.content.split(".")
                for sentence in sentences:
                    sentence = sentence.strip()
                    if len(sentence) > 10:
                        memories.append(
                            {
                                "content": sentence,
                                "context": getattr(conversation, "context", ""),
                            }
                        )

            return memories

        except Exception as e:
            logger.error("Error extracting memories from conversation: %s", e)
            return []
