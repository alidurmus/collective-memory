#!/usr/bin/env python3
"""
Enterprise Features Module for Collective Memory v3.0
Team Collaboration, User Management, and Enterprise Security
"""

import os
import json
import uuid
import hashlib
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class UserRole(Enum):
    """User role definitions for enterprise features"""
    ADMIN = "admin"
    MANAGER = "manager"
    DEVELOPER = "developer"
    VIEWER = "viewer"

class Permission(Enum):
    """Permission definitions for role-based access control"""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"
    MANAGE_USERS = "manage_users"
    MANAGE_TEAMS = "manage_teams"
    ANALYTICS = "analytics"

@dataclass
class User:
    """User entity for enterprise features"""
    id: str
    username: str
    email: str
    role: UserRole
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool = True
    team_id: Optional[str] = None
    permissions: List[Permission] = None
    
    def __post_init__(self):
        if self.permissions is None:
            self.permissions = self._get_default_permissions()
    
    def _get_default_permissions(self) -> List[Permission]:
        """Get default permissions based on user role"""
        if self.role == UserRole.ADMIN:
            return [Permission.READ, Permission.WRITE, Permission.DELETE, 
                   Permission.ADMIN, Permission.MANAGE_USERS, 
                   Permission.MANAGE_TEAMS, Permission.ANALYTICS]
        elif self.role == UserRole.MANAGER:
            return [Permission.READ, Permission.WRITE, Permission.DELETE,
                   Permission.MANAGE_TEAMS, Permission.ANALYTICS]
        elif self.role == UserRole.DEVELOPER:
            return [Permission.READ, Permission.WRITE]
        else:  # VIEWER
            return [Permission.READ]

@dataclass
class Team:
    """Team entity for workspace management"""
    id: str
    name: str
    description: str
    created_at: datetime
    created_by: str
    is_active: bool = True
    members: List[str] = None
    settings: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.members is None:
            self.members = []
        if self.settings is None:
            self.settings = {}

@dataclass
class WorkspaceActivity:
    """Activity tracking for audit trails"""
    id: str
    user_id: str
    team_id: Optional[str]
    action: str
    resource_type: str
    resource_id: str
    timestamp: datetime
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class EnterpriseManager:
    """Main enterprise features manager"""
    
    def __init__(self, db_path: str = "enterprise.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize enterprise database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE,
                team_id TEXT,
                permissions TEXT,
                FOREIGN KEY (team_id) REFERENCES teams(id)
            )
        ''')
        
        # Teams table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP NOT NULL,
                created_by TEXT NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                members TEXT,
                settings TEXT,
                FOREIGN KEY (created_by) REFERENCES users(id)
            )
        ''')
        
        # Activity log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_log (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                team_id TEXT,
                action TEXT NOT NULL,
                resource_type TEXT NOT NULL,
                resource_id TEXT NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                metadata TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (team_id) REFERENCES teams(id)
            )
        ''')
        
        # Shared workspaces table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shared_workspaces (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                team_id TEXT NOT NULL,
                created_by TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL,
                config TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (team_id) REFERENCES teams(id),
                FOREIGN KEY (created_by) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Enterprise database initialized")
    
    def create_user(self, username: str, email: str, password: str, 
                   role: UserRole = UserRole.DEVELOPER, 
                   team_id: Optional[str] = None) -> User:
        """Create a new user"""
        user_id = str(uuid.uuid4())
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        user = User(
            id=user_id,
            username=username,
            email=email,
            role=role,
            created_at=datetime.now(),
            team_id=team_id
        )
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO users (id, username, email, password_hash, role, 
                             created_at, team_id, permissions)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user.id, user.username, user.email, password_hash, 
              user.role.value, user.created_at, user.team_id,
              json.dumps([p.value for p in user.permissions])))
        
        conn.commit()
        conn.close()
        
        self.log_activity(user.id, "create", "user", user.id, 
                         metadata={"username": username, "role": role.value})
        
        logger.info(f"User created: {username} ({role.value})")
        return user
    
    def create_team(self, name: str, description: str, created_by: str) -> Team:
        """Create a new team"""
        team_id = str(uuid.uuid4())
        
        team = Team(
            id=team_id,
            name=name,
            description=description,
            created_at=datetime.now(),
            created_by=created_by
        )
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO teams (id, name, description, created_at, created_by,
                             members, settings)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (team.id, team.name, team.description, team.created_at,
              team.created_by, json.dumps(team.members), 
              json.dumps(team.settings)))
        
        conn.commit()
        conn.close()
        
        self.log_activity(created_by, "create", "team", team.id,
                         metadata={"name": name})
        
        logger.info(f"Team created: {name} by {created_by}")
        return team
    
    def add_user_to_team(self, user_id: str, team_id: str) -> bool:
        """Add user to team"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Update user's team_id
        cursor.execute('UPDATE users SET team_id = ? WHERE id = ?', 
                      (team_id, user_id))
        
        # Update team's members list
        cursor.execute('SELECT members FROM teams WHERE id = ?', (team_id,))
        result = cursor.fetchone()
        if result:
            members = json.loads(result[0]) if result[0] else []
            if user_id not in members:
                members.append(user_id)
                cursor.execute('UPDATE teams SET members = ? WHERE id = ?',
                              (json.dumps(members), team_id))
        
        conn.commit()
        conn.close()
        
        self.log_activity(user_id, "join", "team", team_id)
        logger.info(f"User {user_id} added to team {team_id}")
        return True
    
    def log_activity(self, user_id: str, action: str, resource_type: str, 
                    resource_id: str, team_id: Optional[str] = None,
                    metadata: Dict[str, Any] = None):
        """Log user activity for audit trail"""
        activity = WorkspaceActivity(
            id=str(uuid.uuid4()),
            user_id=user_id,
            team_id=team_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            timestamp=datetime.now(),
            metadata=metadata or {}
        )
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO activity_log (id, user_id, team_id, action, 
                                    resource_type, resource_id, timestamp, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (activity.id, activity.user_id, activity.team_id, activity.action,
              activity.resource_type, activity.resource_id, activity.timestamp,
              json.dumps(activity.metadata)))
        
        conn.commit()
        conn.close()
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, email, role, created_at, last_login, 
                   is_active, team_id, permissions
            FROM users WHERE id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            permissions = [Permission(p) for p in json.loads(result[8] or '[]')]
            return User(
                id=result[0],
                username=result[1],
                email=result[2],
                role=UserRole(result[3]),
                created_at=datetime.fromisoformat(result[4]),
                last_login=datetime.fromisoformat(result[5]) if result[5] else None,
                is_active=result[6],
                team_id=result[7],
                permissions=permissions
            )
        return None
    
    def get_team_by_id(self, team_id: str) -> Optional[Team]:
        """Get team by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, description, created_at, created_by,
                   is_active, members, settings
            FROM teams WHERE id = ?
        ''', (team_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return Team(
                id=result[0],
                name=result[1],
                description=result[2],
                created_at=datetime.fromisoformat(result[3]),
                created_by=result[4],
                is_active=result[5],
                members=json.loads(result[6] or '[]'),
                settings=json.loads(result[7] or '{}')
            )
        return None
    
    def get_user_activity(self, user_id: str, limit: int = 100) -> List[WorkspaceActivity]:
        """Get user activity history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, user_id, team_id, action, resource_type, resource_id,
                   timestamp, metadata
            FROM activity_log 
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (user_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        activities = []
        for result in results:
            activities.append(WorkspaceActivity(
                id=result[0],
                user_id=result[1],
                team_id=result[2],
                action=result[3],
                resource_type=result[4],
                resource_id=result[5],
                timestamp=datetime.fromisoformat(result[6]),
                metadata=json.loads(result[7] or '{}')
            ))
        
        return activities
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user credentials"""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, email, role, created_at, last_login, 
                   is_active, team_id, permissions
            FROM users 
            WHERE username = ? AND password_hash = ? AND is_active = TRUE
        ''', (username, password_hash))
        
        result = cursor.fetchone()
        
        if result:
            # Update last login
            cursor.execute('UPDATE users SET last_login = ? WHERE id = ?',
                          (datetime.now(), result[0]))
            conn.commit()
            
            permissions = [Permission(p) for p in json.loads(result[8] or '[]')]
            user = User(
                id=result[0],
                username=result[1],
                email=result[2],
                role=UserRole(result[3]),
                created_at=datetime.fromisoformat(result[4]),
                last_login=datetime.now(),
                is_active=result[6],
                team_id=result[7],
                permissions=permissions
            )
            
            self.log_activity(user.id, "login", "system", "auth")
            conn.close()
            return user
        
        conn.close()
        return None
    
    def check_permission(self, user_id: str, permission: Permission) -> bool:
        """Check if user has specific permission"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        return permission in user.permissions
    
    def get_team_members(self, team_id: str) -> List[User]:
        """Get all members of a team"""
        team = self.get_team_by_id(team_id)
        if not team:
            return []
        
        members = []
        for member_id in team.members:
            user = self.get_user_by_id(member_id)
            if user:
                members.append(user)
        
        return members
    
    def get_enterprise_analytics(self) -> Dict[str, Any]:
        """Get enterprise analytics data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # User statistics
        cursor.execute('SELECT COUNT(*) FROM users WHERE is_active = TRUE')
        active_users = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM teams WHERE is_active = TRUE')
        active_teams = cursor.fetchone()[0]
        
        # Activity statistics (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        cursor.execute('''
            SELECT COUNT(*) FROM activity_log 
            WHERE timestamp > ?
        ''', (thirty_days_ago,))
        recent_activities = cursor.fetchone()[0]
        
        # Most active users
        cursor.execute('''
            SELECT user_id, COUNT(*) as activity_count
            FROM activity_log
            WHERE timestamp > ?
            GROUP BY user_id
            ORDER BY activity_count DESC
            LIMIT 10
        ''', (thirty_days_ago,))
        most_active_users = cursor.fetchall()
        
        conn.close()
        
        return {
            "active_users": active_users,
            "active_teams": active_teams,
            "recent_activities": recent_activities,
            "most_active_users": [
                {"user_id": user[0], "activity_count": user[1]} 
                for user in most_active_users
            ],
            "timestamp": datetime.now().isoformat()
        }

class CloudSyncManager:
    """Cloud synchronization manager for enterprise features"""
    
    def __init__(self, sync_provider: str = "local"):
        self.sync_provider = sync_provider
        self.sync_enabled = False
        self.sync_interval = 300  # 5 minutes
        self.last_sync = None
    
    def enable_sync(self):
        """Enable cloud synchronization"""
        self.sync_enabled = True
        logger.info("Cloud synchronization enabled")
    
    def disable_sync(self):
        """Disable cloud synchronization"""
        self.sync_enabled = False
        logger.info("Cloud synchronization disabled")
    
    def sync_data(self, data_type: str, data: Any) -> bool:
        """Sync data to cloud provider"""
        if not self.sync_enabled:
            return False
        
        # Placeholder for cloud sync implementation
        logger.info(f"Syncing {data_type} to cloud provider: {self.sync_provider}")
        self.last_sync = datetime.now()
        return True
    
    def get_sync_status(self) -> Dict[str, Any]:
        """Get current sync status"""
        return {
            "enabled": self.sync_enabled,
            "provider": self.sync_provider,
            "last_sync": self.last_sync.isoformat() if self.last_sync else None,
            "interval": self.sync_interval
        }

# Global enterprise manager instance
enterprise_manager = EnterpriseManager()
cloud_sync_manager = CloudSyncManager() 