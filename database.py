import sqlite3
import json

DB_NAME = "user_data.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            image_path TEXT NOT NULL,
            embedding TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_user(name, email, image_path, embedding):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    embedding_json = json.dumps(embedding)

    cursor.execute("""
        INSERT INTO users (name, email, image_path, embedding)
        VALUES (?, ?, ?, ?)
    """, (name, email, image_path, embedding_json))

    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    conn.close()
    return user