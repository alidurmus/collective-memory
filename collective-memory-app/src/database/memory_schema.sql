-- =====================================
-- COLLECTIVE MEMORY v3.0 DATABASE SCHEMA
-- A-Mem + Mem0 Hybrid Memory System
-- =====================================

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- =====================================
-- 1. CORE MEMORY TABLES
-- =====================================

-- Main memory storage table (A-Mem inspired)
CREATE TABLE IF NOT EXISTS memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    context TEXT,
    summary TEXT,
    
    -- Memory classification
    memory_type TEXT CHECK(memory_type IN (
        'fact', 'pattern', 'preference', 'code', 'decision', 
        'error', 'solution', 'insight', 'relationship'
    )) NOT NULL DEFAULT 'fact',
    
    -- Importance and relevance scoring
    importance_score REAL DEFAULT 0.5 CHECK(importance_score >= 0.0 AND importance_score <= 1.0),
    relevance_score REAL DEFAULT 0.5 CHECK(relevance_score >= 0.0 AND relevance_score <= 1.0),
    access_count INTEGER DEFAULT 0,
    
    -- Memory evolution tracking (Mem0 inspired)
    version INTEGER DEFAULT 1,
    parent_memory_id INTEGER REFERENCES memories(id),
    evolution_reason TEXT,
    
    -- Context and source information
    source_file TEXT,
    source_line INTEGER,
    project_path TEXT,
    cursor_session_id TEXT,
    
    -- Embedding for semantic search
    embedding_vector BLOB,
    embedding_model TEXT DEFAULT 'sentence-transformers',
    
    -- Lifecycle management
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    
    -- Status and flags
    status TEXT CHECK(status IN ('active', 'deprecated', 'archived', 'deleted')) DEFAULT 'active',
    is_validated BOOLEAN DEFAULT FALSE,
    is_public BOOLEAN DEFAULT FALSE,
    
    -- Metadata
    tags TEXT, -- JSON array of tags
    metadata TEXT -- JSON object for additional data
);

-- Memory relationships and links (Zettelkasten inspired)
CREATE TABLE IF NOT EXISTS memory_links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    memory_id_1 INTEGER NOT NULL REFERENCES memories(id) ON DELETE CASCADE,
    memory_id_2 INTEGER NOT NULL REFERENCES memories(id) ON DELETE CASCADE,
    
    -- Relationship types
    relationship_type TEXT CHECK(relationship_type IN (
        'similar', 'contradicts', 'depends_on', 'explains', 'example_of',
        'caused_by', 'leads_to', 'related_to', 'part_of', 'references'
    )) NOT NULL DEFAULT 'related_to',
    
    -- Link strength and confidence
    strength REAL DEFAULT 0.5 CHECK(strength >= 0.0 AND strength <= 1.0),
    confidence REAL DEFAULT 0.5 CHECK(confidence >= 0.0 AND confidence <= 1.0),
    
    -- Bidirectional flag
    is_bidirectional BOOLEAN DEFAULT TRUE,
    
    -- Auto-generated vs manual
    is_auto_generated BOOLEAN DEFAULT TRUE,
    generation_algorithm TEXT,
    
    -- Lifecycle
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    validated_at TIMESTAMP,
    
    -- Unique constraint to prevent duplicates
    UNIQUE(memory_id_1, memory_id_2, relationship_type)
);

-- =====================================
-- 2. CONVERSATION CONTEXT TABLES
-- =====================================

-- Cursor conversation context tracking
CREATE TABLE IF NOT EXISTS conversation_context (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cursor_session_id TEXT NOT NULL,
    
    -- Project information
    project_path TEXT NOT NULL,
    project_name TEXT,
    
    -- Conversation summary
    conversation_summary TEXT,
    key_decisions TEXT, -- JSON array
    extracted_facts TEXT, -- JSON array
    
    -- Code context
    active_files TEXT, -- JSON array
    code_snippets TEXT, -- JSON array
    
    -- Timeline
    conversation_start TIMESTAMP,
    conversation_end TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Status
    status TEXT CHECK(status IN ('active', 'completed', 'abandoned')) DEFAULT 'active',
    
    -- Metadata
    total_messages INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Individual conversation messages
CREATE TABLE IF NOT EXISTS conversation_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    context_id INTEGER NOT NULL REFERENCES conversation_context(id) ON DELETE CASCADE,
    
    -- Message content
    message_type TEXT CHECK(message_type IN ('user', 'assistant', 'system')) NOT NULL,
    content TEXT NOT NULL,
    
    -- Code-related content
    code_snippet TEXT,
    file_path TEXT,
    line_number INTEGER,
    
    -- Extracted entities
    entities TEXT, -- JSON array
    intentions TEXT, -- JSON array
    
    -- Sequence and timing
    sequence_number INTEGER NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Memory associations
    generated_memories TEXT, -- JSON array of memory IDs
    
    UNIQUE(context_id, sequence_number)
);

-- =====================================
-- 3. KNOWLEDGE GRAPH TABLES
-- =====================================

-- Entities extracted from conversations and code
CREATE TABLE IF NOT EXISTS entities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT CHECK(type IN (
        'function', 'class', 'variable', 'file', 'concept', 
        'person', 'project', 'technology', 'error', 'solution'
    )) NOT NULL,
    
    -- Description and context
    description TEXT,
    context TEXT,
    
    -- Source information
    source_memory_id INTEGER REFERENCES memories(id),
    source_file TEXT,
    
    -- Frequency and importance
    mention_count INTEGER DEFAULT 1,
    importance_score REAL DEFAULT 0.5,
    
    -- Metadata
    properties TEXT, -- JSON object
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(name, type)
);

-- Relationships between entities
CREATE TABLE IF NOT EXISTS entity_relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id_1 INTEGER NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
    entity_id_2 INTEGER NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
    
    relationship_type TEXT NOT NULL,
    strength REAL DEFAULT 0.5,
    context TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(entity_id_1, entity_id_2, relationship_type)
);

-- =====================================
-- 4. SYSTEM TABLES
-- =====================================

-- Memory system configuration
CREATE TABLE IF NOT EXISTS memory_config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    config_key TEXT NOT NULL UNIQUE,
    config_value TEXT NOT NULL,
    config_type TEXT CHECK(config_type IN ('string', 'integer', 'float', 'boolean', 'json')) DEFAULT 'string',
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- System events and logs
CREATE TABLE IF NOT EXISTS memory_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    event_data TEXT, -- JSON object
    memory_id INTEGER REFERENCES memories(id),
    context_id INTEGER REFERENCES conversation_context(id),
    
    -- Performance metrics
    processing_time_ms INTEGER,
    memory_usage_bytes INTEGER,
    
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexing for performance
    INDEX idx_memory_events_timestamp(timestamp),
    INDEX idx_memory_events_type(event_type),
    INDEX idx_memory_events_memory_id(memory_id)
);

-- =====================================
-- 5. PERFORMANCE INDEXES
-- =====================================

-- Memories table indexes
CREATE INDEX IF NOT EXISTS idx_memories_importance ON memories(importance_score DESC);
CREATE INDEX IF NOT EXISTS idx_memories_type ON memories(memory_type);
CREATE INDEX IF NOT EXISTS idx_memories_created ON memories(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_memories_accessed ON memories(accessed_at DESC);
CREATE INDEX IF NOT EXISTS idx_memories_project ON memories(project_path);
CREATE INDEX IF NOT EXISTS idx_memories_session ON memories(cursor_session_id);
CREATE INDEX IF NOT EXISTS idx_memories_status ON memories(status);

-- Memory links indexes
CREATE INDEX IF NOT EXISTS idx_memory_links_memory1 ON memory_links(memory_id_1);
CREATE INDEX IF NOT EXISTS idx_memory_links_memory2 ON memory_links(memory_id_2);
CREATE INDEX IF NOT EXISTS idx_memory_links_strength ON memory_links(strength DESC);
CREATE INDEX IF NOT EXISTS idx_memory_links_type ON memory_links(relationship_type);

-- Conversation context indexes
CREATE INDEX IF NOT EXISTS idx_conversation_session ON conversation_context(cursor_session_id);
CREATE INDEX IF NOT EXISTS idx_conversation_project ON conversation_context(project_path);
CREATE INDEX IF NOT EXISTS idx_conversation_status ON conversation_context(status);
CREATE INDEX IF NOT EXISTS idx_conversation_activity ON conversation_context(last_activity DESC);

-- Messages indexes
CREATE INDEX IF NOT EXISTS idx_messages_context ON conversation_messages(context_id);
CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON conversation_messages(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_messages_type ON conversation_messages(message_type);

-- Entity indexes
CREATE INDEX IF NOT EXISTS idx_entities_type ON entities(type);
CREATE INDEX IF NOT EXISTS idx_entities_importance ON entities(importance_score DESC);
CREATE INDEX IF NOT EXISTS idx_entities_mentions ON entities(mention_count DESC);

-- =====================================
-- 6. INITIAL CONFIGURATION
-- =====================================

-- Default configuration values
INSERT OR IGNORE INTO memory_config (config_key, config_value, config_type, description) VALUES
('max_memories', '10000', 'integer', 'Maximum number of memories to store'),
('importance_threshold', '0.3', 'float', 'Minimum importance score for memory persistence'),
('auto_cleanup_days', '30', 'integer', 'Days after which inactive memories are archived'),
('link_strength_threshold', '0.5', 'float', 'Minimum strength for memory links'),
('embedding_model', 'sentence-transformers/all-MiniLM-L6-v2', 'string', 'Model for generating embeddings'),
('max_context_length', '1000', 'integer', 'Maximum length for context summaries'),
('auto_linking_enabled', 'true', 'boolean', 'Enable automatic memory linking'),
('conversation_tracking_enabled', 'true', 'boolean', 'Enable conversation context tracking');

-- =====================================
-- 7. TRIGGERS FOR AUTOMATION
-- =====================================

-- Update timestamp trigger for memories
CREATE TRIGGER IF NOT EXISTS update_memories_timestamp 
    AFTER UPDATE ON memories
    FOR EACH ROW
    BEGIN
        UPDATE memories SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

-- Update access timestamp and count
CREATE TRIGGER IF NOT EXISTS update_memory_access 
    AFTER UPDATE OF importance_score, relevance_score ON memories
    FOR EACH ROW
    BEGIN
        UPDATE memories SET 
            accessed_at = CURRENT_TIMESTAMP,
            access_count = access_count + 1
        WHERE id = NEW.id;
    END;

-- Update context timestamp
CREATE TRIGGER IF NOT EXISTS update_context_timestamp 
    AFTER UPDATE ON conversation_context
    FOR EACH ROW
    BEGIN
        UPDATE conversation_context SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

-- =====================================
-- 8. VIEWS FOR COMMON QUERIES
-- =====================================

-- Active memories with high importance
CREATE VIEW IF NOT EXISTS important_memories AS
SELECT m.*, 
       COUNT(ml.id) as link_count,
       AVG(ml.strength) as avg_link_strength
FROM memories m
LEFT JOIN memory_links ml ON (m.id = ml.memory_id_1 OR m.id = ml.memory_id_2)
WHERE m.status = 'active' AND m.importance_score >= 0.7
GROUP BY m.id
ORDER BY m.importance_score DESC, m.accessed_at DESC;

-- Recent conversation contexts
CREATE VIEW IF NOT EXISTS recent_contexts AS
SELECT cc.*,
       COUNT(cm.id) as message_count,
       MAX(cm.timestamp) as last_message_time
FROM conversation_context cc
LEFT JOIN conversation_messages cm ON cc.id = cm.context_id
WHERE cc.status = 'active'
GROUP BY cc.id
ORDER BY cc.last_activity DESC;

-- Memory network analysis
CREATE VIEW IF NOT EXISTS memory_network AS
SELECT m1.id as memory_id,
       m1.content as memory_content,
       COUNT(ml.id) as connection_count,
       AVG(ml.strength) as avg_connection_strength,
       GROUP_CONCAT(DISTINCT ml.relationship_type) as relationship_types
FROM memories m1
LEFT JOIN memory_links ml ON (m1.id = ml.memory_id_1 OR m1.id = ml.memory_id_2)
WHERE m1.status = 'active'
GROUP BY m1.id
ORDER BY connection_count DESC, avg_connection_strength DESC;

-- =====================================
-- SCHEMA COMPLETE
-- ===================================== 