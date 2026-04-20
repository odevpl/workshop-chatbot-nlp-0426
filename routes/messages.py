from flask import Blueprint, jsonify, request

from database.database import add_message, get_conversation, list_messages
from handlers.chat_logic import get_bot_response


bp = Blueprint("messages", __name__, url_prefix="/api/conversations/<int:conversation_id>/messages")


@bp.get("")
def index(conversation_id):
    if not get_conversation(conversation_id):
        return jsonify({"error": "Rozmowa nie istnieje."}), 404
    return jsonify(list_messages(conversation_id))


@bp.post("")
def create(conversation_id):
    if not get_conversation(conversation_id):
        return jsonify({"error": "Rozmowa nie istnieje."}), 404

    payload = request.get_json(silent=True) or {}
    content = payload.get("content", "")
    if not content.strip():
        return jsonify({"error": "Tre\u015b\u0107 wiadomo\u015bci nie mo\u017ce by\u0107 pusta."}), 400

    history = list_messages(conversation_id)
    add_message(conversation_id, "user", content)
    bot_response = get_bot_response(content, history)
    bot_message = add_message(conversation_id, "bot", bot_response)
    return jsonify(bot_message), 201
