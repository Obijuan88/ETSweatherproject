import sqlite3
from datetime import datetime

DB_PATH = "weather_data.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS temperature_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            temperature_min TEXT,
            temperature_max REAL,
            city TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_temperature_query(user_id, username, temperature, city):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO temperature_queries (user_id, temperature_min, temperature_max, city, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, username, temperature, city, datetime.now().isoformat()))
    conn.commit()
    conn.close()