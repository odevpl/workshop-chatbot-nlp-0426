import sqlite3
from datetime import datetime

from config import DATABASE_PATH


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def row_to_dict(row):
    return dict(row) if row else None


def list_conversations():
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, title, created_at, updated_at
            FROM conversations
            ORDER BY updated_at DESC, id DESC
            """
        ).fetchall()
    return [row_to_dict(row) for row in rows]


def get_conversation(conversation_id):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT id, title, created_at, updated_at FROM conversations WHERE id = ?",
            (conversation_id,),
        ).fetchone()
    return row_to_dict(row)


def create_conversation(title=None):
    title = title.strip() if title else datetime.now().strftime("%Y-%m-%d - nowa rozmowa")
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO conversations (title) VALUES (?)",
            (title,),
        )
        conversation_id = cursor.lastrowid
        row = connection.execute(
            "SELECT id, title, created_at, updated_at FROM conversations WHERE id = ?",
            (conversation_id,),
        ).fetchone()
    return row_to_dict(row)


def update_conversation_title(conversation_id, title):
    title = title.strip()
    if not title:
        raise ValueError("Tytuł rozmowy nie może być pusty.")

    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE conversations
            SET title = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (title, conversation_id),
        )
        if cursor.rowcount == 0:
            return None
        row = connection.execute(
            "SELECT id, title, created_at, updated_at FROM conversations WHERE id = ?",
            (conversation_id,),
        ).fetchone()
    return row_to_dict(row)


def delete_conversation(conversation_id):
    with get_connection() as connection:
        cursor = connection.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
    return cursor.rowcount > 0


def list_messages(conversation_id):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, role, content, created_at
            FROM messages
            WHERE conversation_id = ?
            ORDER BY id ASC
            """,
            (conversation_id,),
        ).fetchall()
    return [row_to_dict(row) for row in rows]


def add_message(conversation_id, role, content):
    content = content.strip()
    if not content:
        raise ValueError("Treść wiadomości nie może być pusta.")

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO messages (conversation_id, role, content)
            VALUES (?, ?, ?)
            """,
            (conversation_id, role, content),
        )
        connection.execute(
            "UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (conversation_id,),
        )
        row = connection.execute(
            """
            SELECT id, role, content, created_at
            FROM messages
            WHERE id = ?
            """,
            (cursor.lastrowid,),
        ).fetchone()
    return row_to_dict(row)
