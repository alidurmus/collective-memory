"""
Memory Database Manager for Collective Memory v3.0
A-Mem + Mem0 Hybrid Memory System
"""

import sqlite3
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Any
import numpy as np
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MemoryDatabase:
    """
    Advanced Memory Database Manager
    
    Features:
    - A-Mem inspired memory storage with automatic linking
    - Mem0 inspired memory evolution (ADD/UPDATE/DELETE/NOOP)
    - Conversation context tracking
    - Entity relationship management
    - Performance optimization with indexes
    """
    
    def __init__(self, db_path: str = "data/memory_system.db"):
        """Initialize the memory database."""
        self.db_path = db_path
        self.schema_path = "src/database/memory_schema.sql"
        
        # Ensure database directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialize database
        self._init_database()
        
        logger.info(f"Memory Database initialized at: {db_path}")
    
    def _init_database(self):
        """Initialize database with schema."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Read and execute schema
                if os.path.exists(self.schema_path):
                    with open(self.schema_path, 'r', encoding='utf-8') as f:
                        schema_sql = f.read()
                    
                    # Execute schema in parts (SQLite doesn't like multiple statements)
                    for statement in schema_sql.split(';'):
                        if statement.strip():
                            conn.execute(statement)
                    
                    conn.commit()
                    logger.info("Database schema initialized successfully")
                else:
                    logger.warning(f"Schema file not found: {self.schema_path}")
                    
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
            raise
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection with optimized settings."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")  # Better concurrency
        conn.execute("PRAGMA cache_size = 10000")  # Increase cache
        return conn
    
    # ================================
    # MEMORY OPERATIONS (A-Mem inspired)
    # ================================
    
    def store_memory(self, content: str, context: str = None, 
                    memory_type: str = "fact", importance_score: float = 0.5,
                    project_path: str = None, cursor_session_id: str = None,
                    metadata: Dict = None) -> int:
        """Store a new memory in the database."""
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Generate summary (truncate content if too long)
            summary = content[:200] + "..." if len(content) > 200 else content
            
            # Prepare metadata
            metadata_json = json.dumps(metadata) if metadata else None
            
            # Insert memory
            cursor.execute("""
                INSERT INTO memories (
                    content, context, summary, memory_type, importance_score,
                    project_path, cursor_session_id, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (content, context, summary, memory_type, importance_score,
                  project_path, cursor_session_id, metadata_json))
            
            memory_id = cursor.lastrowid
            
            # Log event
            self._log_event("memory_stored", {"memory_id": memory_id})
            
            logger.info(f"Memory stored with ID: {memory_id}")
            return memory_id
    
    def retrieve_memories(self, query: str = None, memory_type: str = None,
                         project_path: str = None, limit: int = 10,
                         min_importance: float = 0.0) -> List[Dict]:
        """Retrieve memories based on criteria."""
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Build query
            sql = """
                SELECT m.*, 
                       COUNT(ml.id) as link_count,
                       AVG(ml.strength) as avg_link_strength
                FROM memories m
                LEFT JOIN memory_links ml ON (m.id = ml.memory_id_1 OR m.id = ml.memory_id_2)
                WHERE m.status = 'active' AND m.importance_score >= ?
            """
            params = [min_importance]
            
            if query:
                sql += " AND (m.content LIKE ? OR m.summary LIKE ?)"
                params.extend([f"%{query}%", f"%{query}%"])
            
            if memory_type:
                sql += " AND m.memory_type = ?"
                params.append(memory_type)
            
            if project_path:
                sql += " AND m.project_path = ?"
                params.append(project_path)
            
            sql += """
                GROUP BY m.id
                ORDER BY m.importance_score DESC, m.accessed_at DESC
                LIMIT ?
            """
            params.append(limit)
            
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            
            # Convert to dictionaries
            memories = []
            for row in rows:
                memory = dict(row)
                # Parse JSON fields
                if memory['metadata']:
                    memory['metadata'] = json.loads(memory['metadata'])
                memories.append(memory)
            
            logger.info(f"Retrieved {len(memories)} memories")
            return memories
    
    def update_memory(self, memory_id: int, content: str = None,
                     importance_score: float = None, status: str = None,
                     evolution_reason: str = None) -> bool:
        """Update an existing memory (Mem0 inspired)."""
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Build update query
            updates = []
            params = []
            
            if content is not None:
                updates.append("content = ?")
                params.append(content)
                # Update summary too
                summary = content[:200] + "..." if len(content) > 200 else content
                updates.append("summary = ?")
                params.append(summary)
            
            if importance_score is not None:
                updates.append("importance_score = ?")
                params.append(importance_score)
            
            if status is not None:
                updates.append("status = ?")
                params.append(status)
            
            if evolution_reason is not None:
                updates.append("evolution_reason = ?")
                params.append(evolution_reason)
                updates.append("version = version + 1")
            
            if not updates:
                return False
            
            # Add memory_id to params
            params.append(memory_id)
            
            # Execute update
            sql = f"UPDATE memories SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(sql, params)
            
            success = cursor.rowcount > 0
            
            if success:
                self._log_event("memory_updated", {"memory_id": memory_id})
                logger.info(f"Memory {memory_id} updated successfully")
            
            return success
    
    def delete_memory(self, memory_id: int, soft_delete: bool = True) -> bool:
        """Delete a memory (soft or hard delete)."""
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            if soft_delete:
                # Soft delete - just mark as deleted
                cursor.execute(
                    "UPDATE memories SET status = 'deleted' WHERE id = ?",
                    (memory_id,)
                )
            else:
                # Hard delete - remove from database
                cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
            
            success = cursor.rowcount > 0
            
            if success:
                self._log_event("memory_deleted", {
                    "memory_id": memory_id,
                    "soft_delete": soft_delete
                })
                logger.info(f"Memory {memory_id} deleted (soft: {soft_delete})")
            
            return success
    
    # ================================
    # MEMORY LINKING (Zettelkasten inspired)
    # ================================
    
    def create_memory_link(self, memory_id_1: int, memory_id_2: int,
                          relationship_type: str = "related_to",
                          strength: float = 0.5, is_auto_generated: bool = True) -> int:
        """Create a link between two memories."""
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                cursor.execute("""
                    INSERT INTO memory_links (
                        memory_id_1, memory_id_2, relationship_type, 
                        strength, is_auto_generated
                    ) VALUES (?, ?, ?, ?, ?)
                """, (memory_id_1, memory_id_2, relationship_type, 
                      strength, is_auto_generated))
                
                link_id = cursor.lastrowid
                
                self._log_event("memory_link_created", {
                    "link_id": link_id,
                    "memory_id_1": memory_id_1,
                    "memory_id_2": memory_id_2,
                    "relationship_type": relationship_type
                })
                
                logger.info(f"Memory link created: {memory_id_1} -> {memory_id_2}")
                return link_id
                
            except sqlite3.IntegrityError:
                # Link already exists
                logger.warning(f"Memory link already exists: {memory_id_1} -> {memory_id_2}")
                return None
    
    def get_memory_links(self, memory_id: int) -> List[Dict]:
        """Get all links for a specific memory."""
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT ml.*, 
                       m1.content as memory_1_content,
                       m2.content as memory_2_content
                FROM memory_links ml
                JOIN memories m1 ON ml.memory_id_1 = m1.id
                JOIN memories m2 ON ml.memory_id_2 = m2.id
                WHERE ml.memory_id_1 = ? OR ml.memory_id_2 = ?
                ORDER BY ml.strength DESC
            """, (memory_id, memory_id))
            
            return [dict(row) for row in cursor.fetchall()]
    
    # ================================
    # CONVERSATION CONTEXT
    # ================================
    
    def create_conversation_context(self, cursor_session_id: str,
                                   project_path: str, project_name: str = None) -> int:
        """Create a new conversation context."""
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO conversation_context (
                    cursor_session_id, project_path, project_name,
                    conversation_start
                ) VALUES (?, ?, ?, ?)
            """, (cursor_session_id, project_path, project_name, datetime.now()))
            
            context_id = cursor.lastrowid
            
            self._log_event("conversation_started", {
                "context_id": context_id,
                "cursor_session_id": cursor_session_id
            })
            
            logger.info(f"Conversation context created: {context_id}")
            return context_id
    
    def add_conversation_message(self, context_id: int, message_type: str,
                               content: str, code_snippet: str = None,
                               file_path: str = None) -> int:
        """Add a message to conversation context."""
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get next sequence number
            cursor.execute("""
                SELECT COALESCE(MAX(sequence_number), 0) + 1 
                FROM conversation_messages 
                WHERE context_id = ?
            """, (context_id,))
            
            sequence_number = cursor.fetchone()[0]
            
            # Insert message
            cursor.execute("""
                INSERT INTO conversation_messages (
                    context_id, message_type, content, code_snippet,
                    file_path, sequence_number
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (context_id, message_type, content, code_snippet,
                  file_path, sequence_number))
            
            message_id = cursor.lastrowid
            
            # Update context message count
            cursor.execute("""
                UPDATE conversation_context 
                SET total_messages = total_messages + 1,
                    last_activity = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (context_id,))
            
            return message_id
    
    # ================================
    # UTILITY METHODS
    # ================================
    
    def _log_event(self, event_type: str, event_data: Dict = None):
        """Log system events."""
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO memory_events (event_type, event_data)
                    VALUES (?, ?)
                """, (event_type, json.dumps(event_data) if event_data else None))
                
        except Exception as e:
            logger.error(f"Error logging event: {e}")
    
    def get_system_stats(self) -> Dict:
        """Get system statistics."""
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            stats = {}
            
            # Memory statistics
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_memories,
                    COUNT(CASE WHEN status = 'active' THEN 1 END) as active_memories,
                    AVG(importance_score) as avg_importance,
                    MAX(importance_score) as max_importance
                FROM memories
            """)
            
            memory_stats = dict(cursor.fetchone())
            stats['memories'] = memory_stats
            
            # Link statistics
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_links,
                    AVG(strength) as avg_strength,
                    COUNT(DISTINCT relationship_type) as unique_relationships
                FROM memory_links
            """)
            
            link_stats = dict(cursor.fetchone())
            stats['links'] = link_stats
            
            # Conversation statistics
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_contexts,
                    COUNT(CASE WHEN status = 'active' THEN 1 END) as active_contexts,
                    SUM(total_messages) as total_messages
                FROM conversation_context
            """)
            
            context_stats = dict(cursor.fetchone())
            stats['conversations'] = context_stats
            
            return stats
    
    def cleanup_old_memories(self, days_old: int = 30):
        """Clean up old, inactive memories."""
        
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Archive old memories with low importance
            cursor.execute("""
                UPDATE memories 
                SET status = 'archived'
                WHERE status = 'active' 
                AND importance_score < 0.3
                AND accessed_at < ?
            """, (cutoff_date,))
            
            archived_count = cursor.rowcount
            
            self._log_event("memory_cleanup", {
                "archived_count": archived_count,
                "cutoff_date": cutoff_date.isoformat()
            })
            
            logger.info(f"Archived {archived_count} old memories")
            return archived_count
    
    def close(self):
        """Close database connection."""
        logger.info("Memory Database closed")

# ================================
# MEMORY EVOLUTION ENGINE (Mem0 inspired)
# ================================

class MemoryEvolutionEngine:
    """
    Handles memory evolution operations: ADD, UPDATE, DELETE, NOOP
    """
    
    def __init__(self, db: MemoryDatabase):
        self.db = db
    
    def process_interaction(self, user_input: str, ai_response: str,
                          context: str, cursor_session_id: str = None) -> Dict:
        """Process a user-AI interaction and evolve memory."""
        
        # Extract facts from interaction
        extracted_facts = self._extract_facts(user_input, ai_response)
        
        actions_taken = []
        
        for fact in extracted_facts:
            # Determine action needed
            action = self._determine_action(fact, context)
            
            if action == "ADD":
                memory_id = self.db.store_memory(
                    content=fact['content'],
                    context=context,
                    memory_type=fact.get('type', 'fact'),
                    importance_score=fact.get('importance', 0.5),
                    cursor_session_id=cursor_session_id
                )
                actions_taken.append({"action": "ADD", "memory_id": memory_id})
                
            elif action == "UPDATE":
                # Find existing memory and update
                existing_memory = self._find_similar_memory(fact['content'])
                if existing_memory:
                    self.db.update_memory(
                        memory_id=existing_memory['id'],
                        content=fact['content'],
                        importance_score=fact.get('importance', existing_memory['importance_score']),
                        evolution_reason="Updated from conversation"
                    )
                    actions_taken.append({"action": "UPDATE", "memory_id": existing_memory['id']})
                
            elif action == "DELETE":
                # Find and delete contradicted memory
                contradicted_memory = self._find_contradicted_memory(fact['content'])
                if contradicted_memory:
                    self.db.delete_memory(contradicted_memory['id'])
                    actions_taken.append({"action": "DELETE", "memory_id": contradicted_memory['id']})
            
            # NOOP - no action needed
        
        return {
            "extracted_facts": extracted_facts,
            "actions_taken": actions_taken
        }
    
    def _extract_facts(self, user_input: str, ai_response: str) -> List[Dict]:
        """Extract facts from user-AI interaction."""
        # This is a simplified version - in practice, you'd use NLP
        facts = []
        
        # Look for code snippets
        if "```" in ai_response:
            facts.append({
                "content": "Code snippet provided",
                "type": "code",
                "importance": 0.7
            })
        
        # Look for error messages
        if "error" in user_input.lower():
            facts.append({
                "content": f"Error encountered: {user_input}",
                "type": "error",
                "importance": 0.8
            })
        
        # Look for decisions
        if any(word in user_input.lower() for word in ["decided", "chose", "selected"]):
            facts.append({
                "content": f"Decision made: {user_input}",
                "type": "decision",
                "importance": 0.9
            })
        
        return facts
    
    def _determine_action(self, fact: Dict, context: str) -> str:
        """Determine what action to take for a fact."""
        # Simplified logic - in practice, this would be more sophisticated
        
        # Check if similar memory exists
        similar_memory = self._find_similar_memory(fact['content'])
        
        if similar_memory:
            # If importance increased, update
            if fact.get('importance', 0.5) > similar_memory['importance_score']:
                return "UPDATE"
            else:
                return "NOOP"
        else:
            # New fact, add it
            return "ADD"
    
    def _find_similar_memory(self, content: str) -> Optional[Dict]:
        """Find similar memory in database."""
        memories = self.db.retrieve_memories(query=content[:50], limit=1)
        return memories[0] if memories else None
    
    def _find_contradicted_memory(self, content: str) -> Optional[Dict]:
        """Find memory that contradicts the given content."""
        # This would need more sophisticated logic
        return None 