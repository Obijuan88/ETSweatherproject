import os
import requests
import telebot
from datetime import datetime

# Token del bot
BOT_TOKEN = "8158572229:AAE9j62ezMnHr3XbbZU6wnm6gtps3TbGnn8"
bot = telebot.TeleBot(BOT_TOKEN)

# Function to send weather data to Telegram
def send_weather_to_telegram(provincia, municipio, temp_max, temp_min):
    chat_id = "473053437"  # Replace with your Telegram chat ID
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = (
        f"Datos del municipio:\n"
        f"Provincia: {provincia}\n"
        f"Municipio: {municipio}\n"
        f"Fecha: {fecha}\n"
        f"Temperatura máxima: {temp_max} °C\n"
        f"Temperatura mínima: {temp_min} °C"
    )
    bot.send_message(chat_id, message)

# Comando /start o /hello
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy tu bot de Telegram. ¿En qué puedo ayudarte?")

# Comando personalizado /weather
@bot.message_handler(commands=['weather'])
def send_weather(message):
    bot.reply_to(message, "Por favor, dime el código del municipio para obtener el clima.")

# # Manejo de mensajes de texto
# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     chat_id = message.chat.id
#     print(f"Chat ID: {chat_id}")  # Imprime el chat_id en la consola
#     bot.reply_to(message, f"Tu chat ID es: {chat_id}")

# Inicia el bot
if __name__ == "__main__":
    print("El bot está funcionando...")
    bot.infinity_polling()