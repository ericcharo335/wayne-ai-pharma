"""
Wayne AI Pharma - Database Layer
sqlite3 with encryption support for stored files.
"""
import sqlite3
import os
import datetime
import json
from cryptography.fernet import Fernet
from config import DB_PATH

# ---- Encryption Setup ----
_KEY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".encryption_key")

def _get_or_create_key():
    if os.path.exists(_KEY_FILE):
        with open(_KEY_FILE, "rb") as f:
            return f.read()
    key = Fernet.generate_key()
    with open(_KEY_FILE, "wb") as f:
        f.write(key)
    return key

_fernet = Fernet(_get_or_create_key())

def encrypt_bytes(data: bytes) -> bytes:
    return _fernet.encrypt(data)

def decrypt_bytes(data: bytes) -> bytes:
    return _fernet.decrypt(data)


def get_connection() -> sqlite3.Connection:
    """Get a connection to the database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    """Initialize all tables. Safe to call multiple times."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            auto_delete_enabled INTEGER DEFAULT 0,
            auto_delete_days INTEGER DEFAULT 90
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            original_filename TEXT NOT NULL,
            file_type TEXT NOT NULL,
            encrypted_content BLOB NOT NULL,
            file_size_bytes INTEGER,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            upload_id INTEGER NOT NULL,
            redacted_text TEXT,
            analysis_json TEXT,
            timeline TEXT,
            cost TEXT,
            confidence REAL,
            pdf_report BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (upload_id) REFERENCES uploads(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT NOT NULL,
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# ---- User Operations ----
def create_user(email: str, password_hash: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", (email, password_hash))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id


def get_user_by_email(email: str):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return row


def get_user_by_id(user_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return row


def update_user_settings(user_id: int, auto_delete_enabled: bool, auto_delete_days: int):
    conn = get_connection()
    conn.execute(
        "UPDATE users SET auto_delete_enabled = ?, auto_delete_days = ? WHERE id = ?",
        (int(auto_delete_enabled), auto_delete_days, user_id)
    )
    conn.commit()
    conn.close()


def delete_user_data(user_id: int):
    """Delete all data for a user (analyses + uploads). Keep user record."""
    conn = get_connection()
    conn.execute("DELETE FROM analyses WHERE user_id = ?", (user_id,))
    conn.execute("DELETE FROM uploads WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


# ---- Upload Operations ----
def save_upload(user_id: int, filename: str, file_type: str, content: bytes) -> int:
    encrypted = encrypt_bytes(content)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO uploads (user_id, original_filename, file_type, encrypted_content, file_size_bytes) VALUES (?, ?, ?, ?, ?)",
        (user_id, filename, file_type, encrypted, len(content))
    )
    conn.commit()
    upload_id = cursor.lastrowid
    conn.close()
    return upload_id


def get_upload(upload_id: int, user_id: int):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM uploads WHERE id = ? AND user_id = ?", (upload_id, user_id)
    ).fetchone()
    conn.close()
    return row


def get_upload_content(upload_id: int, user_id: int) -> bytes:
    row = get_upload(upload_id, user_id)
    if row is None:
        return None
    return decrypt_bytes(row["encrypted_content"])


def get_user_uploads(user_id: int, limit: int = 50):
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, original_filename, file_type, file_size_bytes, uploaded_at FROM uploads WHERE user_id = ? ORDER BY uploaded_at DESC LIMIT ?",
        (user_id, limit)
    ).fetchall()
    conn.close()
    return rows


# ---- Analysis Operations ----
def save_analysis(user_id: int, upload_id: int, redacted_text: str, analysis_json: str,
                   timeline: str, cost: str, confidence: float, pdf_report: bytes = None) -> int:
    encrypted_pdf = encrypt_bytes(pdf_report) if pdf_report else None
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO analyses (user_id, upload_id, redacted_text, analysis_json, timeline, cost, confidence, pdf_report) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (user_id, upload_id, redacted_text, analysis_json, timeline, cost, confidence, encrypted_pdf)
    )
    conn.commit()
    analysis_id = cursor.lastrowid
    conn.close()
    return analysis_id


def get_user_analyses(user_id: int, limit: int = 50):
    conn = get_connection()
    rows = conn.execute("""
        SELECT a.id, a.upload_id, a.timeline, a.cost, a.confidence, a.created_at,
               u.original_filename
        FROM analyses a
        JOIN uploads u ON a.upload_id = u.id
        WHERE a.user_id = ?
        ORDER BY a.created_at DESC
        LIMIT ?
    """, (user_id, limit)).fetchall()
    conn.close()
    return rows


def get_analysis(analysis_id: int, user_id: int):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM analyses WHERE id = ? AND user_id = ?", (analysis_id, user_id)
    ).fetchone()
    conn.close()
    return row


def get_analysis_pdf(analysis_id: int, user_id: int) -> bytes:
    row = get_analysis(analysis_id, user_id)
    if row is None or row["pdf_report"] is None:
        return None
    return decrypt_bytes(row["pdf_report"])


def log_audit(user_id: int, action: str, details: str = ""):
    conn = get_connection()
    conn.execute("INSERT INTO audit_log (user_id, action, details) VALUES (?, ?, ?)",
                 (user_id, action, details))
    conn.commit()
    conn.close()


# ---- Auto-Delete ----
def run_auto_delete():
    """Delete data for users who have auto-delete enabled and data older than threshold."""
    conn = get_connection()
    # Find users with auto-delete enabled
    users = conn.execute(
        "SELECT id, auto_delete_days FROM users WHERE auto_delete_enabled = 1"
    ).fetchall()
    for user in users:
        cutoff = (datetime.datetime.now() - datetime.timedelta(days=user["auto_delete_days"])).isoformat()
        conn.execute("DELETE FROM analyses WHERE user_id = ? AND created_at < ?", (user["id"], cutoff))
        conn.execute("DELETE FROM uploads WHERE user_id = ? AND uploaded_at < ?", (user["id"], cutoff))
    conn.commit()
    conn.close()
