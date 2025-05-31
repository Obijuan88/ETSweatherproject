import os
import sqlite3
from datetime import datetime

# Cambia la ruta aquí:
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../BBDD/weather.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS temperature_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            temp_min REAL,
            temp_max REAL,
            location TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions (
            chat_id INTEGER PRIMARY KEY,
            cpro TEXT,
            municipio_code TEXT,
            provincia TEXT,
            municipio TEXT,
            tipo TEXT DEFAULT 'diaria'
        )
    ''')
    conn.commit()
    conn.close()

def save_temperature_query(chat_id, temp_min, temp_max, location):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO temperature_queries (chat_id, temp_min, temp_max, location)
        VALUES (?, ?, ?, ?)
    ''', (chat_id, temp_min, temp_max, location))
    conn.commit()
    conn.close()

def save_subscription(chat_id, cpro, municipio_code, provincia, municipio, tipo):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO subscriptions (chat_id, cpro, municipio_code, provincia, municipio, tipo)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (chat_id, cpro, municipio_code, provincia, municipio, tipo))
    conn.commit()
    conn.close()

def remove_subscription(chat_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM subscriptions WHERE chat_id = ?', (chat_id,))
    conn.commit()
    conn.close()

def get_all_subscriptions():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT chat_id, cpro, municipio_code, provincia, municipio, tipo FROM subscriptions')
    subs = c.fetchall()
    conn.close()
    return subs

def send_updates_to_subscribers():
    weather_api = WeatherAPI(API_KEY)
    subs = get_all_subscriptions()
    print(f"Suscripciones encontradas: {subs}")  # <-- Añade esto
    for chat_id, cpro, municipio_code, provincia, municipio in subs:
        try:
            temp_max, temp_min = weather_api.obtener_datos_actuales_de_municipio(int(cpro), int(municipio_code))
            print(f"Enviando a {chat_id}: {provincia}, {municipio}, {temp_max}, {temp_min}")  # <-- Añade esto
            send_weather_to_telegram(chat_id, provincia, municipio, temp_max, temp_min)
        except Exception as e:
            print(f"Error enviando a {chat_id}: {e}")

def is_user_subscribed(chat_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT provincia, municipio FROM subscriptions WHERE chat_id = ?', (chat_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return row  # (provincia, municipio)
    return None

def get_last_temperatures_for_municipio(chat_id, municipio):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT temp_max, temp_min
        FROM temperature_queries
        WHERE chat_id = ? AND location LIKE ?
        ORDER BY date DESC
        LIMIT 1
    ''', (chat_id, f"%{municipio}%"))
    row = c.fetchone()
    conn.close()
    if row:
        return row  # (temp_max, temp_min)
    return None