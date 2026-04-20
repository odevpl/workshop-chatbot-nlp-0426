from flask import Blueprint, jsonify, request

from handlers.math_handler import calculate, is_math_expression
from handlers.template_handler import find_template_response
from routes.memory_store import add_message, get_conversation, list_messages


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

    add_message(conversation_id, "user", content)
    bot_response = None
    if is_math_expression(content):
        bot_response = calculate(content)
    if not bot_response:
        bot_response = find_template_response(content)
    if not bot_response:
        bot_response = "Nie mam jeszcze odpowiedzi w templates.json."
    bot_message = add_message(conversation_id, "bot", bot_response)
    return jsonify(bot_message), 201
