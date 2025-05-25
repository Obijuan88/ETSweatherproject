import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import csv
import telebot
from apiconnect import WeatherAPI
from datetime import datetime
from bbdd import save_temperature_query, init_db

# Token del bot
BOT_TOKEN = "8158572229:AAE9j62ezMnHr3XbbZU6wnm6gtps3TbGnn8"
bot = telebot.TeleBot(BOT_TOKEN)

# API Key de AEMET
API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqdWFuLmFsZWphbmRyby5oaEBnbWFpbC5jb20iLCJqdGkiOiI1NGFlMzYzMC0wMzdmLTQ0NzMtYTFlYy1jMDk4NzY5ZTk2OGMiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTc0NjIxMjM0NCwidXNlcklkIjoiNTRhZTM2MzAtMDM3Zi00NDczLWExZWMtYzA5ODc2OWU5NjhjIiwicm9sZSI6IiJ9.wSrXhd45UFgntTyCeRlPrDv9EqBsZIJdgcUH9qkyLQk'

base_dir = os.path.dirname(os.path.abspath(__file__))
provincias_csv = os.path.join(base_dir, "../CSV/provincias.csv")
municipios_csv = os.path.join(base_dir, "../CSV/diccionario24.csv")

user_data = {}

# Inicializa la base de datos y crea la tabla si no existe
init_db()

# Función para cargar las provincias desde el CSV respetando códigos
def obtener_lista_provincias():
    provincias = {}
    with open(provincias_csv, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)
        for row in reader:
            provincias[row[0].zfill(2)] = row[1]
    return provincias

# Función para cargar los municipios desde el CSV respetando códigos
def obtener_lista_municipios(cpro):
    municipios = {}
    with open(municipios_csv, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)
        for row in reader:
            if row[0].zfill(2) == cpro:
                municipios[row[1].zfill(3)] = row[2]
    return municipios

# Función para enviar los datos meteorológicos
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
    # Guardar en la base de datos
    
    # Puedes guardar la temperatura máxima, mínima o ambas. Aquí se guarda la máxima.
    save_temperature_query(chat_id, temp_min, temp_max, f"{municipio}, {provincia}")

# Comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    provincias = obtener_lista_provincias()
    options = '\n'.join([f"{cpro}. {nombre}" for cpro, nombre in provincias.items()])
    bot.send_message(chat_id, "Selecciona una provincia (escribe el código):\n" + options)
    user_data[chat_id] = {'provincias': provincias}

# Manejo de selección de provincia y municipio
@bot.message_handler(func=lambda msg: msg.text.isdigit())
def handle_selection(message):
    chat_id = message.chat.id
    if chat_id in user_data:
        # Si el usuario está seleccionando provincia
        if 'provincias' in user_data[chat_id] and 'cpro' not in user_data[chat_id]:
            provincias = user_data[chat_id]['provincias']
            cpro = message.text.zfill(2)
            if cpro in provincias:
                user_data[chat_id]['provincia'] = provincias[cpro]
                user_data[chat_id]['cpro'] = cpro

                municipios = obtener_lista_municipios(cpro)
                user_data[chat_id]['municipios'] = municipios

                options = '\n'.join([f"{codigo}. {nombre}" for codigo, nombre in municipios.items()])
                bot.send_message(chat_id, f"Provincia seleccionada: {provincias[cpro]}. Ahora elige un municipio (escribe el código):\n" + options)
            else:
                bot.send_message(chat_id, "Por favor selecciona una provincia válida (código completo).")
        # Si el usuario está seleccionando municipio
        elif 'municipios' in user_data[chat_id]:
            municipios = user_data[chat_id]['municipios']
            municipio_code = message.text.zfill(3)
            if municipio_code in municipios:
                municipio = municipios[municipio_code]
                cpro = user_data[chat_id]['cpro']
                weather_api = WeatherAPI(API_KEY)
                temp_max, temp_min = weather_api.obtener_datos_actuales_de_municipio(int(cpro), int(municipio_code))
                send_weather_to_telegram(chat_id, user_data[chat_id]['provincia'], municipio, temp_max, temp_min)
                user_data.pop(chat_id)
            else:
                bot.send_message(chat_id, "Código de municipio no válido. Intenta nuevamente.")

# Inicia el bot
if __name__ == "__main__":
    print("El bot está funcionando...")
    bot.infinity_polling()
