from flask import Blueprint, jsonify, request

from database.database import (
    create_conversation,
    delete_conversation,
    get_conversation,
    list_conversations,
    update_conversation_title,
)


bp = Blueprint("conversations", __name__, url_prefix="/api/conversations")


@bp.get("")
def index():
    return jsonify(list_conversations())


@bp.post("")
def create():
    payload = request.get_json(silent=True) or {}
    conversation = create_conversation(payload.get("title"))
    return jsonify(conversation), 201


@bp.patch("/<int:conversation_id>")
def update(conversation_id):
    payload = request.get_json(silent=True) or {}
    title = payload.get("title", "")

    try:
        conversation = update_conversation_title(conversation_id, title)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    if conversation is None:
        return jsonify({"error": "Rozmowa nie istnieje."}), 404
    return jsonify(conversation)


@bp.delete("/<int:conversation_id>")
def delete(conversation_id):
    if not delete_conversation(conversation_id):
        return jsonify({"error": "Rozmowa nie istnieje."}), 404
    return jsonify({"success": True})
