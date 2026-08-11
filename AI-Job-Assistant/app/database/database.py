import sqlite3


DATABASE_NAME = "data/assistant.db"


def get_connection():
    connection = sqlite3.connect(
        DATABASE_NAME,
        check_same_thread=False
    )

    return connection


def create_tables():

    connection = get_connection()

    cursor = connection.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Short-term conversation memory
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Long-term user memory
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            memory_key TEXT NOT NULL,
            memory_value TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, memory_key)
        )
    """)

    connection.commit()

    connection.close()


def save_message(session_id: str, role: str, message: str):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO conversations
        (session_id, role, message)
        VALUES (?, ?, ?)
        """,
        (session_id, role, message)
    )

    connection.commit()

    connection.close()


def get_conversation_history(session_id: str):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT role, message
        FROM conversations
        WHERE session_id = ?
        ORDER BY id ASC
        """,
        (session_id,)
    )

    rows = cursor.fetchall()

    connection.close()

    return rows


def save_memory(
    user_id: str,
    memory_key: str,
    memory_value: str
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO user_memory
        (user_id, memory_key, memory_value)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, memory_key)
        DO UPDATE SET
            memory_value = excluded.memory_value,
            updated_at = CURRENT_TIMESTAMP
        """,
        (user_id, memory_key, memory_value)
    )

    connection.commit()

    connection.close()


def get_memories(user_id: str):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT memory_key, memory_value
        FROM user_memory
        WHERE user_id = ?
        ORDER BY id ASC
        """,
        (user_id,)
    )

    rows = cursor.fetchall()

    connection.close()

    return rows