"""
Local SQLite database for tracking operations and backups
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from contextlib import contextmanager


DB_PATH = 'kb_tracker.db'


@contextmanager
def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """Initialize database tables"""
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS operations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation_type TEXT NOT NULL,
                document_id TEXT,
                document_name TEXT,
                metadata TEXT,
                status TEXT,
                error_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS backups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id TEXT NOT NULL,
                document_data TEXT NOT NULL,
                backed_up_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.execute('''
            CREATE INDEX IF NOT EXISTS idx_operations_doc_id ON operations(document_id)
        ''')
        
        conn.execute('''
            CREATE INDEX IF NOT EXISTS idx_backups_doc_id ON backups(document_id)
        ''')
        
        conn.commit()


def log_operation(
    operation_type: str,
    document_id: Optional[str] = None,
    document_name: Optional[str] = None,
    metadata: Optional[Dict] = None,
    status: str = 'success',
    error_message: Optional[str] = None
) -> int:
    """Log an operation to the database"""
    with get_db() as conn:
        cursor = conn.execute('''
            INSERT INTO operations (operation_type, document_id, document_name, metadata, status, error_message)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            operation_type,
            document_id,
            document_name,
            json.dumps(metadata) if metadata else None,
            status,
            error_message
        ))
        conn.commit()
        return cursor.lastrowid


def backup_document(document_id: str, document_data: Dict) -> int:
    """Backup document data before deletion"""
    with get_db() as conn:
        cursor = conn.execute('''
            INSERT INTO backups (document_id, document_data)
            VALUES (?, ?)
        ''', (document_id, json.dumps(document_data)))
        conn.commit()
        return cursor.lastrowid


def get_backup(document_id: str) -> Optional[Dict]:
    """Get most recent backup for a document"""
    with get_db() as conn:
        row = conn.execute('''
            SELECT document_data, backed_up_at
            FROM backups
            WHERE document_id = ?
            ORDER BY backed_up_at DESC
            LIMIT 1
        ''', (document_id,)).fetchone()
        
        if row:
            return {
                'data': json.loads(row['document_data']),
                'backed_up_at': row['backed_up_at']
            }
        return None


def get_operations(limit: int = 50) -> List[Dict]:
    """Get recent operations"""
    with get_db() as conn:
        rows = conn.execute('''
            SELECT * FROM operations
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,)).fetchall()
        
        return [dict(row) for row in rows]


def get_deleted_documents(limit: int = 50) -> List[Dict]:
    """Get list of deleted documents (with backups)"""
    with get_db() as conn:
        rows = conn.execute('''
            SELECT DISTINCT b.document_id, b.backed_up_at, b.document_data
            FROM backups b
            INNER JOIN operations o ON b.document_id = o.document_id
            WHERE o.operation_type = 'delete'
            ORDER BY b.backed_up_at DESC
            LIMIT ?
        ''', (limit,)).fetchall()
        
        result = []
        for row in rows:
            data = json.loads(row['document_data'])
            result.append({
                'document_id': row['document_id'],
                'backed_up_at': row['backed_up_at'],
                'name': data.get('name', 'Unnamed'),
                'type': data.get('type', 'Unknown')
            })
        return result


# Initialize database on import
init_db()

