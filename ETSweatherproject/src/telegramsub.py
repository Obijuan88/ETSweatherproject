import os
import telebot
from apiconnect import WeatherAPI
from datetime import datetime
from bbdd import save_temperature_query, get_all_subscriptions

BOT_TOKEN = "8158572229:AAE9j62ezMnHr3XbbZU6wnm6gtps3TbGnn8"
API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqdWFuLmFsZWphbmRyby5oaEBnbWFpbC5jb20iLCJqdGkiOiI1NGFlMzYzMC0wMzdmLTQ0NzMtYTFlYy1jMDk4NzY5ZTk2OGMiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTc0NjIxMjM0NCwidXNlcklkIjoiNTRhZTM2MzAtMDM3Zi00NDczLWExZWMtYzA5ODc2OWU5NjhjIiwicm9sZSI6IiJ9.wSrXhd45UFgntTyCeRlPrDv9EqBsZIJdgcUH9qkyLQk'

bot = telebot.TeleBot(BOT_TOKEN)

def send_weather_to_telegram(chat_id, provincia, municipio, temp_max, temp_min):
    fecha = datetime.now().strftime("%d/%m/%Y")
    message = (
        f"Datos del municipio:\n"
        f"Provincia: {provincia}\n"
        f"Municipio: {municipio}\n"
        f"Fecha: {fecha}\n"
        f"Temperatura máxima: {temp_max} °C\n"
        f"Temperatura mínima: {temp_min} °C"
    )
    bot.send_message(chat_id, message)
    save_temperature_query(chat_id, temp_min, temp_max, f"{municipio}, {provincia}")

def send_updates_to_subscribers():
    weather_api = WeatherAPI(API_KEY)
    subs = get_all_subscriptions()
    for chat_id, cpro, municipio_code, provincia, municipio in subs:
        temp_max, temp_min = weather_api.obtener_datos_actuales_de_municipio(int(cpro), int(municipio_code))
        send_weather_to_telegram(chat_id, provincia, municipio, temp_max, temp_min)

if __name__ == "__main__":
    send_updates_to_subscribers()