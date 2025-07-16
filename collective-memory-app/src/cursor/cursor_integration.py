"""
Cursor Integration Layer for Collective Memory v3.0
Real-time Cursor chat monitoring and analysis system
"""

import os
import sqlite3
import json
import logging
from typing import List, Dict, Optional, Set
from datetime import datetime
from pathlib import Path
import threading
import time
from dataclasses import dataclass
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CursorConversation:
    """Represents a Cursor conversation."""
    session_id: str
    project_path: str
    messages: List[Dict]
    created_at: datetime
    updated_at: datetime
    
@dataclass
class CursorMessage:
    """Represents a single message in Cursor."""
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime
    code_blocks: List[str]
    file_references: List[str]

class CursorDatabaseReader:
    """
    Reads Cursor's SQLite databases to extract conversation data
    
    Cursor stores data in:
    - Windows: ~/AppData/Roaming/Cursor/User/workspaceStorage/
    - macOS: ~/Library/Application Support/Cursor/User/workspaceStorage/
    - Linux: ~/.config/Cursor/User/workspaceStorage/
    """
    
    def __init__(self):
        self.base_path = self._get_cursor_data_path()
        self.workspace_storage_path = None
        self.conversation_cache = {}
        
        if self.base_path and os.path.exists(self.base_path):
            self.workspace_storage_path = os.path.join(self.base_path, "workspaceStorage")
            logger.info(f"Cursor data path found: {self.base_path}")
        else:
            logger.warning("Cursor data path not found")
    
    def _get_cursor_data_path(self) -> Optional[str]:
        """Get Cursor data directory path based on OS."""
        import platform
        
        system = platform.system()
        home = Path.home()
        
        if system == "Windows":
            path = home / "AppData" / "Roaming" / "Cursor" / "User"
        elif system == "Darwin":  # macOS
            path = home / "Library" / "Application Support" / "Cursor" / "User"
        elif system == "Linux":
            path = home / ".config" / "Cursor" / "User"
        else:
            return None
        
        return str(path) if path.exists() else None
    
    def find_workspace_databases(self) -> List[str]:
        """Find all workspace SQLite databases."""
        if not self.workspace_storage_path:
            return []
        
        databases = []
        
        try:
            for root, dirs, files in os.walk(self.workspace_storage_path):
                for file in files:
                    if file.endswith('.vscdb'):
                        databases.append(os.path.join(root, file))
        except Exception as e:
            logger.error(f"Error scanning workspace storage: {e}")
        
        logger.info(f"Found {len(databases)} workspace databases")
        return databases
    
    def extract_conversations_from_db(self, db_path: str) -> List[CursorConversation]:
        """Extract conversations from a specific database."""
        conversations = []
        
        try:
            with sqlite3.connect(db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                # Get workspace info
                workspace_info = self._get_workspace_info(cursor)
                project_path = workspace_info.get('folder_path', 'Unknown')
                
                # Extract chat data
                chat_data = self._extract_chat_data(cursor)
                
                if chat_data:
                    conversation = CursorConversation(
                        session_id=self._generate_session_id(db_path),
                        project_path=project_path,
                        messages=chat_data,
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                    conversations.append(conversation)
                    
        except Exception as e:
            logger.error(f"Error reading database {db_path}: {e}")
        
        return conversations
    
    def _get_workspace_info(self, cursor: sqlite3.Cursor) -> Dict:
        """Extract workspace information from database."""
        workspace_info = {}
        
        try:
            # Try to get workspace folder path
            cursor.execute("""
                SELECT key, value 
                FROM ItemTable 
                WHERE key LIKE '%folderUri%' OR key LIKE '%workspace%'
            """)
            
            for row in cursor.fetchall():
                key = row['key']
                value = row['value']
                
                if 'folderUri' in key and value:
                    try:
                        # Parse URI to get folder path
                        uri_data = json.loads(value)
                        if isinstance(uri_data, dict) and 'external' in uri_data:
                            workspace_info['folder_path'] = uri_data['external']
                    except:
                        pass
                        
        except Exception as e:
            logger.debug(f"Error getting workspace info: {e}")
        
        return workspace_info
    
    def _extract_chat_data(self, cursor: sqlite3.Cursor) -> List[Dict]:
        """Extract chat messages from database."""
        messages = []
        
        try:
            # Look for chat-related keys
            cursor.execute("""
                SELECT key, value 
                FROM ItemTable 
                WHERE key LIKE '%chat%' OR key LIKE '%aichat%' OR key LIKE '%prompts%'
            """)
            
            for row in cursor.fetchall():
                key = row['key']
                value = row['value']
                
                if value:
                    try:
                        # Parse JSON value
                        data = json.loads(value)
                        
                        # Extract messages from various formats
                        parsed_messages = self._parse_chat_messages(data, key)
                        messages.extend(parsed_messages)
                        
                    except json.JSONDecodeError:
                        # Try to extract plain text
                        if len(value) > 10:  # Ignore very short values
                            messages.append({
                                'role': 'unknown',
                                'content': str(value)[:500],  # Truncate long content
                                'timestamp': datetime.now().isoformat(),
                                'source_key': key
                            })
                    except Exception as e:
                        logger.debug(f"Error parsing chat data from key {key}: {e}")
        
        except Exception as e:
            logger.error(f"Error extracting chat data: {e}")
        
        return messages
    
    def _parse_chat_messages(self, data: any, source_key: str) -> List[Dict]:
        """Parse chat messages from various data formats."""
        messages = []
        
        try:
            if isinstance(data, dict):
                # Check for different message formats
                if 'messages' in data:
                    # Standard messages format
                    for msg in data['messages']:
                        parsed = self._parse_single_message(msg)
                        if parsed:
                            messages.append(parsed)
                
                elif 'conversations' in data:
                    # Conversations format
                    for conv in data['conversations']:
                        if 'messages' in conv:
                            for msg in conv['messages']:
                                parsed = self._parse_single_message(msg)
                                if parsed:
                                    messages.append(parsed)
                
                elif 'content' in data and 'role' in data:
                    # Single message format
                    parsed = self._parse_single_message(data)
                    if parsed:
                        messages.append(parsed)
                
                elif isinstance(data, str) and len(data) > 10:
                    # Plain text content
                    messages.append({
                        'role': 'unknown',
                        'content': data,
                        'timestamp': datetime.now().isoformat(),
                        'source_key': source_key
                    })
            
            elif isinstance(data, list):
                # Array of messages
                for item in data:
                    if isinstance(item, dict):
                        parsed = self._parse_single_message(item)
                        if parsed:
                            messages.append(parsed)
        
        except Exception as e:
            logger.debug(f"Error parsing chat messages: {e}")
        
        return messages
    
    def _parse_single_message(self, msg: Dict) -> Optional[Dict]:
        """Parse a single message object."""
        try:
            # Extract basic message info
            message = {
                'role': msg.get('role', 'unknown'),
                'content': msg.get('content', ''),
                'timestamp': msg.get('timestamp', datetime.now().isoformat()),
                'code_blocks': [],
                'file_references': []
            }
            
            # Extract code blocks
            content = message['content']
            if '```' in content:
                code_blocks = self._extract_code_blocks(content)
                message['code_blocks'] = code_blocks
            
            # Extract file references
            file_refs = self._extract_file_references(content)
            message['file_references'] = file_refs
            
            return message if message['content'] else None
            
        except Exception as e:
            logger.debug(f"Error parsing single message: {e}")
            return None
    
    def _extract_code_blocks(self, content: str) -> List[str]:
        """Extract code blocks from message content."""
        code_blocks = []
        
        # Find code blocks between ```
        import re
        pattern = r'```(?:\w+)?\n(.*?)```'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for match in matches:
            code_blocks.append(match.strip())
        
        return code_blocks
    
    def _extract_file_references(self, content: str) -> List[str]:
        """Extract file references from message content."""
        file_refs = []
        
        # Look for common file patterns
        import re
        
        # File paths
        file_patterns = [
            r'([a-zA-Z]:[\\/][\w\\/.-]+\.\w+)',  # Windows paths
            r'([/~][\w/.-]+\.\w+)',  # Unix paths
            r'([\w.-]+\.\w+)',  # Relative paths
        ]
        
        for pattern in file_patterns:
            matches = re.findall(pattern, content)
            file_refs.extend(matches)
        
        return list(set(file_refs))  # Remove duplicates
    
    def _generate_session_id(self, db_path: str) -> str:
        """Generate a unique session ID from database path."""
        import hashlib
        return hashlib.md5(db_path.encode()).hexdigest()[:12]
    
    def get_all_conversations(self) -> List[CursorConversation]:
        """Get all conversations from all workspace databases."""
        all_conversations = []
        
        databases = self.find_workspace_databases()
        
        for db_path in databases:
            conversations = self.extract_conversations_from_db(db_path)
            all_conversations.extend(conversations)
        
        logger.info(f"Retrieved {len(all_conversations)} conversations")
        return all_conversations

class CursorMonitor(FileSystemEventHandler):
    """
    Real-time monitoring of Cursor database changes
    """
    
    def __init__(self, callback_function=None):
        self.callback_function = callback_function
        self.reader = CursorDatabaseReader()
        self.observer = Observer()
        self.monitoring = False
        
    def start_monitoring(self):
        """Start monitoring Cursor database changes."""
        if not self.reader.workspace_storage_path:
            logger.error("Cannot start monitoring: Cursor workspace path not found")
            return False
        
        try:
            self.observer.schedule(self, self.reader.workspace_storage_path, recursive=True)
            self.observer.start()
            self.monitoring = True
            logger.info("Cursor monitoring started")
            return True
        except Exception as e:
            logger.error(f"Error starting Cursor monitoring: {e}")
            return False
    
    def stop_monitoring(self):
        """Stop monitoring Cursor database changes."""
        if self.monitoring:
            self.observer.stop()
            self.observer.join()
            self.monitoring = False
            logger.info("Cursor monitoring stopped")
    
    def on_modified(self, event):
        """Handle file modification events."""
        if not event.is_directory and event.src_path.endswith('.vscdb'):
            logger.info(f"Cursor database modified: {event.src_path}")
            
            # Extract new conversations
            try:
                conversations = self.reader.extract_conversations_from_db(event.src_path)
                
                if conversations and self.callback_function:
                    self.callback_function(conversations)
                    
            except Exception as e:
                logger.error(f"Error processing database update: {e}")

class CursorAnalyzer:
    """
    Analyzes Cursor conversations for memory extraction
    """
    
    def __init__(self):
        self.patterns = {
            'code_changes': r'(added|modified|deleted|created|updated)\s+(.+)',
            'errors': r'(error|exception|failed|bug):\s*(.+)',
            'decisions': r'(decided|chose|selected|will use)\s+(.+)',
            'preferences': r'(prefer|like|want|need)\s+(.+)',
            'file_operations': r'(create|edit|delete|move|rename)\s+(.+)',
        }
    
    def analyze_conversation(self, conversation: CursorConversation) -> Dict:
        """Analyze a conversation for memory-worthy content."""
        analysis = {
            'session_id': conversation.session_id,
            'project_path': conversation.project_path,
            'extracted_facts': [],
            'code_snippets': [],
            'decisions': [],
            'errors': [],
            'preferences': [],
            'file_operations': []
        }
        
        for message in conversation.messages:
            # Analyze message content
            facts = self._extract_facts_from_message(message)
            analysis['extracted_facts'].extend(facts)
            
            # Extract code snippets
            if message.get('code_blocks'):
                analysis['code_snippets'].extend(message['code_blocks'])
            
            # Categorize content
            content = message.get('content', '')
            
            for category, pattern in self.patterns.items():
                import re
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    analysis[category].extend(matches)
        
        return analysis
    
    def _extract_facts_from_message(self, message: Dict) -> List[Dict]:
        """Extract facts from a single message."""
        facts = []
        content = message.get('content', '')
        role = message.get('role', 'unknown')
        
        # Skip very short messages
        if len(content) < 10:
            return facts
        
        # Extract different types of facts
        if role == 'user':
            # User requests and questions
            if '?' in content:
                facts.append({
                    'type': 'question',
                    'content': content,
                    'importance': 0.6
                })
            
            # User instructions
            if any(word in content.lower() for word in ['create', 'add', 'fix', 'change', 'update']):
                facts.append({
                    'type': 'instruction',
                    'content': content,
                    'importance': 0.8
                })
        
        elif role == 'assistant':
            # Code explanations
            if 'explain' in content.lower() or 'because' in content.lower():
                facts.append({
                    'type': 'explanation',
                    'content': content,
                    'importance': 0.7
                })
            
            # Solutions provided
            if message.get('code_blocks'):
                facts.append({
                    'type': 'solution',
                    'content': content,
                    'importance': 0.9
                })
        
        return facts

class CursorIntegrationManager:
    """
    Main manager for Cursor integration
    """
    
    def __init__(self, memory_database=None):
        self.reader = CursorDatabaseReader()
        self.analyzer = CursorAnalyzer()
        self.monitor = CursorMonitor(callback_function=self._on_conversation_update)
        self.memory_db = memory_database
        
    def _on_conversation_update(self, conversations: List[CursorConversation]):
        """Handle new conversation updates."""
        for conversation in conversations:
            try:
                # Analyze conversation
                analysis = self.analyzer.analyze_conversation(conversation)
                
                # Store in memory database if available
                if self.memory_db:
                    self._store_conversation_memories(analysis)
                
                logger.info(f"Processed conversation: {conversation.session_id}")
                
            except Exception as e:
                logger.error(f"Error processing conversation: {e}")
    
    def _store_conversation_memories(self, analysis: Dict):
        """Store conversation analysis in memory database."""
        if not self.memory_db:
            return
        
        # Store extracted facts
        for fact in analysis['extracted_facts']:
            self.memory_db.store_memory(
                content=fact['content'],
                memory_type=fact['type'],
                importance_score=fact['importance'],
                project_path=analysis['project_path'],
                cursor_session_id=analysis['session_id']
            )
        
        # Store code snippets
        for code in analysis['code_snippets']:
            self.memory_db.store_memory(
                content=f"Code snippet: {code[:200]}...",
                memory_type='code',
                importance_score=0.8,
                project_path=analysis['project_path'],
                cursor_session_id=analysis['session_id']
            )
        
        # Store decisions
        for decision in analysis['decisions']:
            self.memory_db.store_memory(
                content=f"Decision: {decision}",
                memory_type='decision',
                importance_score=0.9,
                project_path=analysis['project_path'],
                cursor_session_id=analysis['session_id']
            )
    
    def start_real_time_monitoring(self):
        """Start real-time monitoring of Cursor."""
        return self.monitor.start_monitoring()
    
    def stop_real_time_monitoring(self):
        """Stop real-time monitoring."""
        self.monitor.stop_monitoring()
    
    def get_recent_conversations(self, limit: int = 10) -> List[CursorConversation]:
        """Get recent conversations from Cursor."""
        conversations = self.reader.get_all_conversations()
        
        # Sort by update time and limit
        conversations.sort(key=lambda x: x.updated_at, reverse=True)
        return conversations[:limit]
    
    def analyze_project_context(self, project_path: str) -> Dict:
        """Analyze all conversations for a specific project."""
        conversations = self.reader.get_all_conversations()
        
        project_conversations = [
            conv for conv in conversations 
            if conv.project_path == project_path
        ]
        
        # Combine analysis from all project conversations
        combined_analysis = {
            'project_path': project_path,
            'total_conversations': len(project_conversations),
            'extracted_facts': [],
            'code_snippets': [],
            'decisions': [],
            'errors': [],
            'preferences': [],
            'file_operations': []
        }
        
        for conversation in project_conversations:
            analysis = self.analyzer.analyze_conversation(conversation)
            
            # Merge analysis results
            for key in ['extracted_facts', 'code_snippets', 'decisions', 'errors', 'preferences', 'file_operations']:
                combined_analysis[key].extend(analysis[key])
        
        return combined_analysis

# Example usage
if __name__ == "__main__":
    # Test the integration
    manager = CursorIntegrationManager()
    
    # Get recent conversations
    conversations = manager.get_recent_conversations(5)
    
    for conv in conversations:
        print(f"Session: {conv.session_id}")
        print(f"Project: {conv.project_path}")
        print(f"Messages: {len(conv.messages)}")
        print("---")
    
    # Start monitoring (optional)
    # manager.start_real_time_monitoring()
    
    # Keep running to monitor changes
    # try:
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     manager.stop_real_time_monitoring()
    #     print("Monitoring stopped") 