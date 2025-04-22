import sqlite3
import datetime

DB_NAME = "logs.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            user_id TEXT,
            source TEXT,
            text_input TEXT,
            emotion TEXT,
            confidence REAL,
            recommended_tasks TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_emotion(user_id, source, text_input, emotion, confidence, tasks):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    task_str = ", ".join(tasks)
    c.execute('''
        INSERT INTO logs (timestamp, user_id, source, text_input, emotion, confidence, recommended_tasks)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (timestamp, user_id, source, text_input, emotion, confidence, task_str))
    conn.commit()
    conn.close()