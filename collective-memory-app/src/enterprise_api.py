#!/usr/bin/env python3
"""
Enterprise API Endpoints for Collective Memory v3.0
Team Collaboration, User Management, and Analytics
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from functools import wraps

from flask import Blueprint, request, jsonify, session
from flask_socketio import emit, join_room, leave_room
from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden, NotFound

from enterprise_features import (
    enterprise_manager, cloud_sync_manager, 
    User, Team, UserRole, Permission,
    WorkspaceActivity
)

logger = logging.getLogger(__name__)

# Create enterprise blueprint
enterprise_bp = Blueprint('enterprise', __name__, url_prefix='/api/enterprise')

def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def require_permission(permission: Permission):
    """Decorator to require specific permission"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'error': 'Authentication required'}), 401
            
            user_id = session['user_id']
            if not enterprise_manager.check_permission(user_id, permission):
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Authentication endpoints
@enterprise_bp.route('/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        user = enterprise_manager.authenticate_user(username, password)
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role.value
            
            return jsonify({
                'success': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role.value,
                    'team_id': user.team_id,
                    'permissions': [p.value for p in user.permissions]
                }
            })
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Login failed'}), 500

@enterprise_bp.route('/auth/logout', methods=['POST'])
@require_auth
def logout():
    """User logout endpoint"""
    user_id = session.get('user_id')
    if user_id:
        enterprise_manager.log_activity(user_id, "logout", "system", "auth")
    
    session.clear()
    return jsonify({'success': True})

@enterprise_bp.route('/auth/me', methods=['GET'])
@require_auth
def get_current_user():
    """Get current user information"""
    user_id = session['user_id']
    user = enterprise_manager.get_user_by_id(user_id)
    
    if user:
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role.value,
                'team_id': user.team_id,
                'permissions': [p.value for p in user.permissions],
                'last_login': user.last_login.isoformat() if user.last_login else None
            }
        })
    else:
        return jsonify({'error': 'User not found'}), 404

# User management endpoints
@enterprise_bp.route('/users', methods=['POST'])
@require_permission(Permission.MANAGE_USERS)
def create_user():
    """Create new user"""
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'developer')
        team_id = data.get('team_id')
        
        if not all([username, email, password]):
            return jsonify({'error': 'Username, email, and password required'}), 400
        
        try:
            user_role = UserRole(role)
        except ValueError:
            return jsonify({'error': 'Invalid role'}), 400
        
        user = enterprise_manager.create_user(
            username=username,
            email=email,
            password=password,
            role=user_role,
            team_id=team_id
        )
        
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role.value,
                'team_id': user.team_id,
                'created_at': user.created_at.isoformat()
            }
        })
    
    except Exception as e:
        logger.error(f"Create user error: {str(e)}")
        return jsonify({'error': 'Failed to create user'}), 500

@enterprise_bp.route('/users/<user_id>', methods=['GET'])
@require_permission(Permission.MANAGE_USERS)
def get_user(user_id):
    """Get user by ID"""
    user = enterprise_manager.get_user_by_id(user_id)
    
    if user:
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role.value,
                'team_id': user.team_id,
                'permissions': [p.value for p in user.permissions],
                'created_at': user.created_at.isoformat(),
                'last_login': user.last_login.isoformat() if user.last_login else None,
                'is_active': user.is_active
            }
        })
    else:
        return jsonify({'error': 'User not found'}), 404

# Team management endpoints
@enterprise_bp.route('/teams', methods=['POST'])
@require_permission(Permission.MANAGE_TEAMS)
def create_team():
    """Create new team"""
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description', '')
        
        if not name:
            return jsonify({'error': 'Team name required'}), 400
        
        created_by = session['user_id']
        team = enterprise_manager.create_team(
            name=name,
            description=description,
            created_by=created_by
        )
        
        return jsonify({
            'success': True,
            'team': {
                'id': team.id,
                'name': team.name,
                'description': team.description,
                'created_by': team.created_by,
                'created_at': team.created_at.isoformat(),
                'members': team.members
            }
        })
    
    except Exception as e:
        logger.error(f"Create team error: {str(e)}")
        return jsonify({'error': 'Failed to create team'}), 500

@enterprise_bp.route('/teams/<team_id>', methods=['GET'])
@require_auth
def get_team(team_id):
    """Get team by ID"""
    team = enterprise_manager.get_team_by_id(team_id)
    
    if team:
        # Check if user has access to this team
        user_id = session['user_id']
        user = enterprise_manager.get_user_by_id(user_id)
        
        if user.team_id != team_id and not enterprise_manager.check_permission(user_id, Permission.MANAGE_TEAMS):
            return jsonify({'error': 'Access denied'}), 403
        
        # Get team members info
        members = enterprise_manager.get_team_members(team_id)
        members_info = [{
            'id': member.id,
            'username': member.username,
            'email': member.email,
            'role': member.role.value,
            'last_login': member.last_login.isoformat() if member.last_login else None
        } for member in members]
        
        return jsonify({
            'success': True,
            'team': {
                'id': team.id,
                'name': team.name,
                'description': team.description,
                'created_by': team.created_by,
                'created_at': team.created_at.isoformat(),
                'members': members_info,
                'settings': team.settings
            }
        })
    else:
        return jsonify({'error': 'Team not found'}), 404

@enterprise_bp.route('/teams/<team_id>/members', methods=['POST'])
@require_permission(Permission.MANAGE_TEAMS)
def add_team_member():
    """Add user to team"""
    try:
        team_id = request.view_args['team_id']
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        success = enterprise_manager.add_user_to_team(user_id, team_id)
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Failed to add user to team'}), 500
    
    except Exception as e:
        logger.error(f"Add team member error: {str(e)}")
        return jsonify({'error': 'Failed to add team member'}), 500

# Analytics endpoints
@enterprise_bp.route('/analytics', methods=['GET'])
@require_permission(Permission.ANALYTICS)
def get_enterprise_analytics():
    """Get enterprise analytics data"""
    try:
        analytics = enterprise_manager.get_enterprise_analytics()
        return jsonify({
            'success': True,
            'analytics': analytics
        })
    
    except Exception as e:
        logger.error(f"Analytics error: {str(e)}")
        return jsonify({'error': 'Failed to get analytics'}), 500

@enterprise_bp.route('/analytics/user/<user_id>/activity', methods=['GET'])
@require_auth
def get_user_activity(user_id):
    """Get user activity history"""
    try:
        # Check if user can access this data
        current_user_id = session['user_id']
        if current_user_id != user_id and not enterprise_manager.check_permission(current_user_id, Permission.ANALYTICS):
            return jsonify({'error': 'Access denied'}), 403
        
        limit = request.args.get('limit', 100, type=int)
        activities = enterprise_manager.get_user_activity(user_id, limit)
        
        activities_data = [{
            'id': activity.id,
            'action': activity.action,
            'resource_type': activity.resource_type,
            'resource_id': activity.resource_id,
            'timestamp': activity.timestamp.isoformat(),
            'metadata': activity.metadata
        } for activity in activities]
        
        return jsonify({
            'success': True,
            'activities': activities_data
        })
    
    except Exception as e:
        logger.error(f"User activity error: {str(e)}")
        return jsonify({'error': 'Failed to get user activity'}), 500

# Cloud sync endpoints
@enterprise_bp.route('/sync/status', methods=['GET'])
@require_auth
def get_sync_status():
    """Get cloud sync status"""
    try:
        status = cloud_sync_manager.get_sync_status()
        return jsonify({
            'success': True,
            'sync_status': status
        })
    
    except Exception as e:
        logger.error(f"Sync status error: {str(e)}")
        return jsonify({'error': 'Failed to get sync status'}), 500

@enterprise_bp.route('/sync/enable', methods=['POST'])
@require_permission(Permission.ADMIN)
def enable_sync():
    """Enable cloud synchronization"""
    try:
        cloud_sync_manager.enable_sync()
        return jsonify({'success': True})
    
    except Exception as e:
        logger.error(f"Enable sync error: {str(e)}")
        return jsonify({'error': 'Failed to enable sync'}), 500

@enterprise_bp.route('/sync/disable', methods=['POST'])
@require_permission(Permission.ADMIN)
def disable_sync():
    """Disable cloud synchronization"""
    try:
        cloud_sync_manager.disable_sync()
        return jsonify({'success': True})
    
    except Exception as e:
        logger.error(f"Disable sync error: {str(e)}")
        return jsonify({'error': 'Failed to disable sync'}), 500

# Real-time collaboration endpoints
@enterprise_bp.route('/collaboration/rooms', methods=['GET'])
@require_auth
def get_collaboration_rooms():
    """Get available collaboration rooms"""
    try:
        user_id = session['user_id']
        user = enterprise_manager.get_user_by_id(user_id)
        
        if not user or not user.team_id:
            return jsonify({'error': 'User not part of any team'}), 400
        
        # Get team-based collaboration rooms
        team = enterprise_manager.get_team_by_id(user.team_id)
        if not team:
            return jsonify({'error': 'Team not found'}), 404
        
        rooms = [
            {
                'id': f"team_{team.id}",
                'name': f"Team {team.name}",
                'type': 'team',
                'team_id': team.id
            },
            {
                'id': f"general_{team.id}",
                'name': f"General - {team.name}",
                'type': 'general',
                'team_id': team.id
            }
        ]
        
        return jsonify({
            'success': True,
            'rooms': rooms
        })
    
    except Exception as e:
        logger.error(f"Collaboration rooms error: {str(e)}")
        return jsonify({'error': 'Failed to get collaboration rooms'}), 500

# WebSocket events for real-time collaboration
def handle_join_room(data):
    """Handle user joining collaboration room"""
    try:
        room_id = data.get('room_id')
        user_id = session.get('user_id')
        
        if not user_id or not room_id:
            return
        
        user = enterprise_manager.get_user_by_id(user_id)
        if not user:
            return
        
        join_room(room_id)
        
        # Notify room members
        emit('user_joined', {
            'user': {
                'id': user.id,
                'username': user.username,
                'role': user.role.value
            },
            'room_id': room_id
        }, room=room_id)
        
        # Log activity
        enterprise_manager.log_activity(
            user_id, "join_room", "collaboration", room_id,
            team_id=user.team_id
        )
        
    except Exception as e:
        logger.error(f"Join room error: {str(e)}")

def handle_leave_room(data):
    """Handle user leaving collaboration room"""
    try:
        room_id = data.get('room_id')
        user_id = session.get('user_id')
        
        if not user_id or not room_id:
            return
        
        user = enterprise_manager.get_user_by_id(user_id)
        if not user:
            return
        
        leave_room(room_id)
        
        # Notify room members
        emit('user_left', {
            'user': {
                'id': user.id,
                'username': user.username
            },
            'room_id': room_id
        }, room=room_id)
        
        # Log activity
        enterprise_manager.log_activity(
            user_id, "leave_room", "collaboration", room_id,
            team_id=user.team_id
        )
        
    except Exception as e:
        logger.error(f"Leave room error: {str(e)}")

def handle_collaboration_message(data):
    """Handle real-time collaboration message"""
    try:
        room_id = data.get('room_id')
        message = data.get('message')
        user_id = session.get('user_id')
        
        if not all([room_id, message, user_id]):
            return
        
        user = enterprise_manager.get_user_by_id(user_id)
        if not user:
            return
        
        # Broadcast message to room
        emit('collaboration_message', {
            'user': {
                'id': user.id,
                'username': user.username,
                'role': user.role.value
            },
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'room_id': room_id
        }, room=room_id)
        
        # Log activity
        enterprise_manager.log_activity(
            user_id, "send_message", "collaboration", room_id,
            team_id=user.team_id,
            metadata={'message_length': len(message)}
        )
        
    except Exception as e:
        logger.error(f"Collaboration message error: {str(e)}")

# Export WebSocket handlers
websocket_handlers = {
    'join_room': handle_join_room,
    'leave_room': handle_leave_room,
    'collaboration_message': handle_collaboration_message
} 