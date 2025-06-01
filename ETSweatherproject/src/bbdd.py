import os
import sqlite3
from datetime import datetime
import decouple
from decouple import config
from apiconnect import WeatherAPI

# Importa la función si está en otro archivo, por ejemplo:
# from telegram_utils import send_weather_to_telegram

def send_weather_to_telegram(chat_id, provincia, municipio, temp_max, temp_min):
    """
    Envía un mensaje al usuario de Telegram con la información del clima.
    Esta es una función de ejemplo. Debes reemplazarla con la implementación real.
    """
    print(f"[Telegram] ChatID: {chat_id} | {provincia}, {municipio} | Max: {temp_max}°C, Min: {temp_min}°C")

# Cambia la ruta aquí:
DB_PATH = config('DB_PATH', default='/app/ETSweatherproject/BBDD/weather.db')

def init_db():
    try:
        # Crear el directorio si no existe
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

        ##print(f"[DEBUG] DB_PATH: {DB_PATH}")  # Depuración de la ruta
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
    except sqlite3.Error as e:
        print(f"[ERROR] Database error: {e}")

def save_temperature_query(chat_id, temp_min, temp_max, location):
    ##print(f"[DEBUG] Guardando datos: chat_id={chat_id}, temp_min={temp_min}, temp_max={temp_max}, location={location}")
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
    weather_api = WeatherAPI(config('API_KEY'))
    init_db()  # Asegúrate de que la base de datos está inicializada
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
    ##print(f"[DEBUG] Buscando temperaturas para chat_id={chat_id}, municipio={municipio}")
    c.execute('''
        SELECT temp_max, temp_min
        FROM temperature_queries
        WHERE chat_id = ? AND location LIKE ?
        ORDER BY date DESC
        LIMIT 1
    ''', (chat_id, f"%{municipio}%"))
    row = c.fetchone()
    conn.close()
    ##print(f"[DEBUG] Resultados encontrados: {row}")
    if row:
        return row  # (temp_max, temp_min)
    return None

def get_last_temperatures(chat_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT temp_max, temp_min
        FROM temperature_queries
        WHERE chat_id = ?
        ORDER BY date DESC
        LIMIT 1
    ''', (chat_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return row  # Devuelve (temp_max, temp_min)
    return None  # Si no hay datos, devuelve None

def obtener_datos_municipio(cpro, municipio_code):
    from apiconnect import WeatherAPI  # Importación dentro de la función
    weather_api = WeatherAPI(config('API_KEY'))
    return weather_api.obtener_datos_actuales_de_municipio(cpro, municipio_code)