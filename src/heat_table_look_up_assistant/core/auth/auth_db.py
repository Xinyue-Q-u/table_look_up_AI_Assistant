import sqlite3
from pathlib import Path
from typing import Optional, Iterable
from heat_table_look_up_assistant.core.config import load_config


SCHEMA_SQL: Iterable[str] = [
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash BLOB NOT NULL,
        salt BLOB NOT NULL,
        iterations INTEGER NOT NULL,
        created_at TEXT NOT NULL DEFAULT (datetime('now'))
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        token_hash BLOB NOT NULL UNIQUE,
        created_at TEXT NOT NULL DEFAULT (datetime('now')),
        expires_at TEXT NOT NULL,
        revoked_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    """,
    "CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);",
    "CREATE INDEX IF NOT EXISTS idx_sessions_expires_at ON sessions(expires_at);",
]

def get_db_path(db_path:Optional[str|Path]=None)->Path:
    cfg = load_config()
    default_db_path=cfg.data_dir/"auth.db"
    db_path=Path(db_path) if db_path else default_db_path
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return db_path

def connect_db(db_path:Path)->sqlite3.Connection:
    db_path=get_db_path()
    conn=sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_auth_db(db_path:Path)->None:
    conn=connect_db(db_path)
    try:
        with conn:
            for stmt in SCHEMA_SQL:
                conn.execute(stmt)
    finally:
        conn.close()