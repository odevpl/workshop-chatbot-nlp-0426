from datetime import datetime


_conversations = []
_messages = {}
_next_conversation_id = 1
_next_message_id = 1


def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def list_conversations():
    return sorted(_conversations, key=lambda item: (item["updated_at"], item["id"]), reverse=True)


def get_conversation(conversation_id):
    return next((item for item in _conversations if item["id"] == conversation_id), None)


def create_conversation(title=None):
    global _next_conversation_id

    timestamp = _now()
    conversation = {
        "id": _next_conversation_id,
        "title": title.strip() if title else datetime.now().strftime("%Y-%m-%d - nowa rozmowa"),
        "created_at": timestamp,
        "updated_at": timestamp,
    }
    _next_conversation_id += 1
    _conversations.append(conversation)
    _messages[conversation["id"]] = []
    return conversation


def update_conversation_title(conversation_id, title):
    title = title.strip()
    if not title:
        raise ValueError("Tytu\u0142 rozmowy nie mo\u017ce by\u0107 pusty.")

    conversation = get_conversation(conversation_id)
    if conversation is None:
        return None
    conversation["title"] = title
    conversation["updated_at"] = _now()
    return conversation


def delete_conversation(conversation_id):
    conversation = get_conversation(conversation_id)
    if conversation is None:
        return False
    _conversations.remove(conversation)
    _messages.pop(conversation_id, None)
    return True


def list_messages(conversation_id):
    return _messages.get(conversation_id, [])


def add_message(conversation_id, role, content):
    global _next_message_id

    content = content.strip()
    if not content:
        raise ValueError("Tre\u015b\u0107 wiadomo\u015bci nie mo\u017ce by\u0107 pusta.")

    message = {
        "id": _next_message_id,
        "role": role,
        "content": content,
        "created_at": _now(),
    }
    _next_message_id += 1
    _messages.setdefault(conversation_id, []).append(message)

    conversation = get_conversation(conversation_id)
    if conversation is not None:
        conversation["updated_at"] = _now()

    return message
