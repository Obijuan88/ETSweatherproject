import os
import requests
import telebot

# Token del bot
BOT_TOKEN = "8158572229:AAE9j62ezMnHr3XbbZU6wnm6gtps3TbGnn8"
bot = telebot.TeleBot(BOT_TOKEN)

# Comando /start o /hello
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy tu bot de Telegram. ¿En qué puedo ayudarte?")

# Comando personalizado /weather
@bot.message_handler(commands=['weather'])
def send_weather(message):
    bot.reply_to(message, "Por favor, dime el código del municipio para obtener el clima.")

# Manejo de mensajes de texto
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Recibí tu mensaje: {message.text}")

# Inicia el bot
print("El bot está funcionando...")
bot.infinity_polling()