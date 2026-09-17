import sqlite3
from pathlib import Path
from datetime import datetime


DB_PATH = Path("data/memorial.db")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            speaker TEXT NOT NULL,
            text TEXT NOT NULL,
            source TEXT
        )
    """)

    connection.commit()

    return connection


def save_message(
    conversation_id: str,
    speaker: str,
    text: str,
    source: str = "chat"
):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO messages
        (conversation_id, timestamp, speaker, text, source)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            conversation_id,
            datetime.now().isoformat(),
            speaker,
            text,
            source
        )
    )

    connection.commit()
    connection.close()


def get_messages(conversation_id: str):
    connection = get_connection()

    cursor = connection.execute(
        """
        SELECT id, timestamp, speaker, text, source
        FROM messages
        WHERE conversation_id = ?
        ORDER BY id
        """,
        (conversation_id,)
    )

    messages = cursor.fetchall()
    connection.close()

    return messages