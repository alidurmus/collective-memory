#!/usr/bin/env python3
"""
Chat API - JSON Chat Manager için REST API endpoints
Collective Memory Flask API'ye JSON chat management entegrasyonu
"""

from flask import Blueprint, request, jsonify, send_file
from pathlib import Path
from typing import Dict, Any, List
import json
from datetime import datetime

from json_chat_manager import JSONChatManager, ChatMessage, ChatConversation

class ChatAPI:
    """JSON Chat Manager için API sınıfı"""
    
    def __init__(self, data_folder: str = None):
        self.chat_manager = JSONChatManager(data_folder)
        self.blueprint = Blueprint('chat_api', __name__, url_prefix='/api/v1/chat')
        self._setup_routes()
    
    def _setup_routes(self):
        """API route'larını kur"""
        
        @self.blueprint.route('/conversations', methods=['GET'])
        def get_conversations():
            """Konuşmaları listele"""
            try:
                query = request.args.get('query', '')
                project_path = request.args.get('project_path', '')
                tags = request.args.getlist('tags')
                limit = int(request.args.get('limit', 50))
                
                conversations = self.chat_manager.search_conversations(
                    query=query if query else None,
                    project_path=project_path if project_path else None,
                    tags=tags if tags else None,
                    limit=limit
                )
                
                return jsonify({
                    'success': True,
                    'data': conversations,
                    'count': len(conversations)
                })
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.blueprint.route('/conversations', methods=['POST'])
        def create_conversation():
            """Yeni konuşma oluştur"""
            try:
                data = request.get_json()
                
                if not data.get('title'):
                    return jsonify({
                        'success': False,
                        'error': 'Title is required'
                    }), 400
                
                conversation_id = self.chat_manager.create_conversation(
                    title=data['title'],
                    project_path=data.get('project_path'),
                    initial_message=data.get('initial_message')
                )
                
                return jsonify({
                    'success': True,
                    'data': {
                        'conversation_id': conversation_id,
                        'message': 'Konuşma başarıyla oluşturuldu'
                    }
                }), 201
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.blueprint.route('/conversations/<conversation_id>', methods=['GET'])
        def get_conversation(conversation_id):
            """Belirli bir konuşmayı getir"""
            try:
                conversation = self.chat_manager.load_conversation(conversation_id)
                if not conversation:
                    return jsonify({
                        'success': False,
                        'error': 'Konuşma bulunamadı'
                    }), 404
                
                # ChatConversation'ı dict'e dönüştür
                from dataclasses import asdict
                conversation_dict = asdict(conversation)
                
                return jsonify({
                    'success': True,
                    'data': conversation_dict
                })
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.blueprint.route('/conversations/<conversation_id>/messages', methods=['POST'])
        def add_message(conversation_id):
            """Konuşmaya mesaj ekle"""
            try:
                data = request.get_json()
                
                if not data.get('content'):
                    return jsonify({
                        'success': False,
                        'error': 'Content is required'
                    }), 400
                
                message_id = self.chat_manager.add_message(
                    conversation_id=conversation_id,
                    role=data.get('role', 'user'),
                    content=data['content'],
                    metadata=data.get('metadata')
                )
                
                return jsonify({
                    'success': True,
                    'data': {
                        'message_id': message_id,
                        'message': 'Mesaj başarıyla eklendi'
                    }
                }), 201
                
            except ValueError as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 404
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.blueprint.route('/conversations/<conversation_id>/export', methods=['POST'])
        def export_conversation(conversation_id):
            """Konuşmayı export et"""
            try:
                data = request.get_json() or {}
                format = data.get('format', 'json')
                
                export_path = self.chat_manager.export_conversation(conversation_id, format)
                if not export_path:
                    return jsonify({
                        'success': False,
                        'error': 'Export başarısız veya konuşma bulunamadı'
                    }), 404
                
                # Dosyayı gönder
                return send_file(
                    export_path,
                    as_attachment=True,
                    download_name=Path(export_path).name
                )
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.blueprint.route('/stats', methods=['GET'])
        def get_stats():
            """Konuşma istatistikleri"""
            try:
                stats = self.chat_manager.get_conversation_stats()
                return jsonify({
                    'success': True,
                    'data': stats
                })
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.blueprint.route('/import/cursor', methods=['POST'])
        def import_from_cursor():
            """Cursor chat'lerini import et"""
            try:
                from cursor_reader import EnhancedCursorDatabaseReader
                cursor_reader = EnhancedCursorDatabaseReader()
                
                imported_count = self.chat_manager.import_from_cursor(cursor_reader)
                
                return jsonify({
                    'success': True,
                    'data': {
                        'imported_count': imported_count,
                        'message': f'{imported_count} konuşma başarıyla import edildi'
                    }
                })
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.blueprint.route('/search', methods=['POST'])
        def search_in_conversations():
            """Konuşmalarda gelişmiş arama"""
            try:
                data = request.get_json()
                query = data.get('query', '')
                filters = data.get('filters', {})
                
                # Gelişmiş arama parametreleri
                project_path = filters.get('project_path')
                tags = filters.get('tags', [])
                date_from = filters.get('date_from')
                date_to = filters.get('date_to')
                limit = filters.get('limit', 50)
                
                conversations = self.chat_manager.search_conversations(
                    query=query if query else None,
                    project_path=project_path,
                    tags=tags,
                    limit=limit
                )
                
                # Date filtering
                if date_from or date_to:
                    filtered_conversations = []
                    for conv in conversations:
                        conv_date = conv.get('created_at', '')
                        if date_from and conv_date < date_from:
                            continue
                        if date_to and conv_date > date_to:
                            continue
                        filtered_conversations.append(conv)
                    conversations = filtered_conversations
                
                return jsonify({
                    'success': True,
                    'data': conversations,
                    'count': len(conversations),
                    'query': query,
                    'filters': filters
                })
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500

def register_chat_api(app, data_folder: str = None):
    """Flask app'e chat API'yi kaydet"""
    chat_api = ChatAPI(data_folder)
    app.register_blueprint(chat_api.blueprint)
    return chat_api 