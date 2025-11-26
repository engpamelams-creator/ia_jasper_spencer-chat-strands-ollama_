# app/memory/database.py

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "memory.db")


def init_db():
    """Cria as tabelas de memória se não existirem."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()


def save_message(session_id: str, role: str, content: str):
    """Salva uma mensagem no histórico persistente."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO memory (session_id, role, content)
        VALUES (?, ?, ?)
    """, (session_id, role, content))

    conn.commit()
    conn.close()


def load_memory(session_id: str, limit: int = 10):
    """
    Carrega histórico da sessão com limite para não deixar lento.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT role, content
        FROM memory
        WHERE session_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (session_id, limit))

    rows = cur.fetchall()
    conn.close()

    # Inverter para mensagens ficarem na ordem certa
    messages = [{"role": role, "content": content} for role, content in rows]
    return list(reversed(messages))
