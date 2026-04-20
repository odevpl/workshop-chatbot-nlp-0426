import json
import random
import re

from config import TEMPLATES_PATH


def _normalize(text):
    return re.sub(r"\s+", " ", text.strip().lower())


def load_templates():
    if not TEMPLATES_PATH.exists():
        return []
    with open(TEMPLATES_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def find_template_response(message):
    normalized_message = _normalize(message)
    for template in load_templates():
        patterns = template.get("patterns", [])
        responses = template.get("responses", [])
        for pattern in patterns:
            normalized_pattern = _normalize(pattern)
            if normalized_message == normalized_pattern or normalized_pattern in normalized_message:
                return random.choice(responses) if responses else None
    return None
