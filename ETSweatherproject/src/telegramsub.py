import sqlite3
import os
from decouple import config
from bbdd import save_temperature_query, get_last_temperatures_for_municipio, get_all_subscriptions, init_db
from telebot import TeleBot
from datetime import datetime
from apiconnect import WeatherAPI

# Definir DB_PATH
DB_PATH = config('DB_PATH', default='/app/ETSweatherproject/BBDD/weather.db')

# Inicializar la base de datos
init_db()

BOT_TOKEN = config('BOT_TOKEN')
bot = TeleBot(BOT_TOKEN)

def send_weather_to_telegram(chat_id, provincia, municipio, temp_max, temp_min):
    """
    Envía los datos meteorológicos al usuario a través de Telegram.
    """
    fecha = datetime.now().strftime("%d/%m/%Y")
    if temp_max is None or temp_min is None:
        message = (
            f"No hay datos meteorológicos disponibles para {municipio} ({provincia}) en este momento."
        )
    else:
        message = (
            f"Datos del municipio:\n"
            f"Provincia: {provincia}\n"
            f"Municipio: {municipio}\n"
            f"Fecha: {fecha}\n"
            f"Temperatura máxima: {temp_max} °C\n"
            f"Temperatura mínima: {temp_min} °C\n"
            f"Temperatura media: {(temp_max + temp_min) / 2:.2f} °C\n"
        )
    bot.send_message(chat_id, message)
    if temp_max is not None and temp_min is not None:
        save_temperature_query(chat_id, temp_min, temp_max, f"{municipio}, {provincia}")

def send_weather_if_changes_to_telegram(chat_id, provincia, municipio, cpro, municipio_code):
    """
    Envía los datos meteorológicos al usuario solo si hay cambios en las temperaturas.
    """
    # Obtener las últimas temperaturas registradas para el municipio desde la base de datos
    last_temperatures = get_last_temperatures_for_municipio(chat_id, municipio)
    
    # Consultar las temperaturas actuales desde la API
    weather_api = WeatherAPI(config('API_KEY'))
    temp_max, temp_min = weather_api.obtener_datos_actuales_de_municipio(cpro, municipio_code)
    
    if last_temperatures:
        last_temp_max, last_temp_min = last_temperatures
        
        # Comparar las temperaturas actuales con las registradas anteriormente
        if temp_max != last_temp_max or temp_min != last_temp_min:
            message = (
                f"¡Actualización de temperaturas!\n"
                f"Municipio: {municipio} ({provincia})\n"
                f"Temperatura máxima anterior: {last_temp_max} °C\n"
                f"Temperatura mínima anterior: {last_temp_min} °C\n"
                f"Temperatura máxima actual: {temp_max} °C\n"
                f"Temperatura mínima actual: {temp_min} °C\n"
            )
            bot.send_message(chat_id, message)
            
            # Guardar las nuevas temperaturas en la base de datos
            save_temperature_query(chat_id, temp_min, temp_max, f"{municipio}, {provincia}")
    else:
        # Si no hay registros anteriores, enviar los datos actuales
        send_weather_to_telegram(chat_id, provincia, municipio, temp_max, temp_min)

def send_updates_to_subscribers():
    """
    Envía actualizaciones meteorológicas a todos los suscriptores.
    """
    subscriptions = get_all_subscriptions()
    for chat_id, cpro, municipio_code, provincia, municipio, tipo in subscriptions:
        temp_max, temp_min = get_last_temperatures_for_municipio(chat_id, municipio)
        if tipo == "diaria":
            send_weather_to_telegram(chat_id, provincia, municipio, temp_max, temp_min)
        elif tipo == "cambio":
            send_weather_if_changes_to_telegram(chat_id, provincia, municipio, cpro, municipio_code)

if __name__ == "__main__":
    send_updates_to_subscribers()