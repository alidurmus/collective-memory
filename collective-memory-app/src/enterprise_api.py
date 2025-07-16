from flask import Blueprint, jsonify

enterprise_bp = Blueprint('enterprise', __name__)


@enterprise_bp.route('/enterprise/ping')
def ping():
    return jsonify({'status': 'ok', 'message': 'Enterprise API alive'})


# Dummy websocket handlers (sunucu import hatası vermesin diye)
websocket_handlers = {}

