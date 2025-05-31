import os
import telebot
from apiconnect import WeatherAPI
from datetime import datetime
from bbdd import save_temperature_query, get_all_subscriptions

BOT_TOKEN = "8158572229:AAE9j62ezMnHr3XbbZU6wnm6gtps3TbGnn8"
API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqdWFuLmFsZWphbmRyby5oaEBnbWFpbC5jb20iLCJqdGkiOiI1NGFlMzYzMC0wMzdmLTQ0NzMtYTFlYy1jMDk4NzY5ZTk2OGMiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTc0NjIxMjM0NCwidXNlcklkIjoiNVRhZTM2MzAtMDM3Zi00NDczLWExZWMtYzA5ODc2OWU5NjhjIiwicm9sZSI6IiJ9.wSrXhd45UFgntTyCeRlPrDv9EqBsZIJdgcUH9qkyLQk'

bot = telebot.TeleBot(BOT_TOKEN)

def send_weather_to_telegram(chat_id, provincia, municipio, temp_max, temp_min):
    fecha = datetime.now().strftime("%d/%m/%Y")
    message = (
        f"Datos del municipio:\n"
        f"Provincia: {provincia}\n"
        f"Municipio: {municipio}\n"
        f"Fecha: {fecha}\n"
        f"Temperatura máxima: {temp_max} °C\n"
        f"Temperatura mínima: {temp_min} °C\n"
        f"Temperatura media:  {(temp_max + temp_min)/2} °C\n"
    )
    bot.send_message(chat_id, message)
    save_temperature_query(chat_id, temp_min, temp_max, f"{municipio}, {provincia}")

def send_weather_if_changes_to_telegram(chat_id, provincia, municipio, temp_max, temp_min):
    # Importa la función para obtener las temperaturas anteriores
    from bbdd import get_last_temperatures
    last = get_last_temperatures(chat_id)
    if last:
        last_max, last_min = last
        cambios = []
        if temp_max != last_max:
            variacion_max = abs(temp_max - last_max)
            cambios.append(f"La temperatura máxima ha variado {variacion_max} ºC. Ha pasado de {last_max} ºC ayer a {temp_max} ºC hoy.")
        if temp_min != last_min:
            variacion_min = abs(temp_min - last_min)
            cambios.append(f"La temperatura mínima ha variado {variacion_min} ºC. Ha pasado de {last_min} ºC ayer a {temp_min} ºC hoy.")
        
        if cambios:
            cambios_texto = "\n".join(cambios)
            message = (
                f"¡Hola! Se han detectado cambios en las temperaturas para {municipio} ({provincia}):\n\n"
                f"{cambios_texto}\n\n"
                f"Datos actuales:\n"
                f"Temperatura máxima: {temp_max} ºC\n"
                f"Temperatura mínima: {temp_min} ºC\n"
                f"Temperatura media: {(temp_max + temp_min) / 2:.1f} ºC\n"
            )
            bot.send_message(chat_id, message)
        else:
            # No hay cambios, no se envía mensaje
            pass
    else:
        # Si no hay datos previos, envía el mensaje completo
        send_weather_to_telegram(chat_id, provincia, municipio, temp_max, temp_min)

def send_updates_to_subscribers():
    subs = get_all_subscriptions()
    from bbdd import get_last_temperatures_for_municipio
    for chat_id, cpro, municipio_code, provincia, municipio, tipo in subs:
        last = get_last_temperatures_for_municipio(chat_id, municipio)
        if last:
            temp_max, temp_min = last
            if tipo == "diaria":
                send_weather_to_telegram(chat_id, provincia, municipio, temp_max, temp_min)
            elif tipo == "cambio":
                send_weather_if_changes_to_telegram(chat_id, provincia, municipio, temp_max, temp_min)
        else:
            # Si no hay datos previos, puedes decidir si envías un mensaje o lo omites
            pass

if __name__ == "__main__":
    send_updates_to_subscribers()