import sys
import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import decouple
from decouple import config
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import apiconnect
from apiconnect import WeatherAPI
import csv
from datetime import datetime
from bbdd import save_temperature_query, init_db, save_subscription, remove_subscription, is_user_subscribed

# Token del bot
BOT_TOKEN = config('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# API Key de AEMET
API_KEY = config('API_KEY')
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
    #print(f"[DEBUG] Cargando municipios para la provincia: {cpro}")
    try:
        with open(municipios_csv, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            next(reader)  # Saltar la cabecera si existe
            for row in reader:
                #print(f"[DEBUG] Leyendo fila: {row}")  # Depuración
                if row[0].zfill(2) == cpro:
                    municipios[row[1].zfill(3)] = row[2]
        #print(f"[DEBUG] Municipios cargados: {municipios}")
    except FileNotFoundError:
        print("[ERROR] El archivo diccionario24.csv no se encontró.")
    except Exception as e:
        print(f"[ERROR] Error al cargar municipios: {e}")
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

# Comando /sub
@bot.message_handler(commands=['sub'])
def handle_subscribe(message):
    chat_id = message.chat.id
    if chat_id not in user_data or 'provincias' not in user_data[chat_id]:
        bot.send_message(chat_id, "Primero debes iniciar con /start y seleccionar una provincia.")
        return

    if 'cpro' in user_data[chat_id] and 'municipios' in user_data[chat_id] and 'municipio_code' in user_data[chat_id]:
        provincia = user_data[chat_id]['provincia']
        municipio_code = user_data[chat_id]['municipio_code']
        municipio = user_data[chat_id]['municipios'][municipio_code]
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("Notificación diaria", callback_data="sub_diaria"),
            InlineKeyboardButton("Notificación solo si cambia temperatura", callback_data="sub_cambio")
        )
        bot.send_message(
            chat_id,
            f"¿Cómo quieres recibir las notificaciones para {municipio} ({provincia})?",
            reply_markup=markup
        )
        user_data[chat_id]['pending_sub'] = True
    elif 'cpro' in user_data[chat_id]:
        bot.send_message(chat_id, "Selecciona primero un municipio antes de suscribirte.")
    else:
        bot.send_message(chat_id, "Selecciona primero una provincia y un municipio antes de suscribirte.")

@bot.callback_query_handler(func=lambda call: call.data in ["sub_diaria", "sub_cambio"])
def callback_confirm_subscription(call):
    chat_id = call.message.chat.id
    if chat_id in user_data and user_data[chat_id].get('pending_sub'):
        cpro = user_data[chat_id]['cpro']
        municipio_code = user_data[chat_id]['municipio_code']
        provincia = user_data[chat_id]['provincia']
        municipio = user_data[chat_id]['municipios'][municipio_code]
        if call.data == "sub_diaria":
            tipo = "diaria"
            save_subscription(chat_id, cpro, municipio_code, provincia, municipio, tipo)
            bot.edit_message_text(
                f"Te has suscrito a notificaciones diarias para {municipio} ({provincia}).",
                chat_id=chat_id,
                message_id=call.message.message_id
            )
        else:
            tipo = "cambio"
            save_subscription(chat_id, cpro, municipio_code, provincia, municipio, tipo)
            bot.edit_message_text(
                f"Te has suscrito a notificaciones solo si cambia la temperatura máxima o mínima para {municipio} ({provincia}).",
                chat_id=chat_id,
                message_id=call.message.message_id
            )
        user_data[chat_id].pop('pending_sub', None)
    else:
        bot.answer_callback_query(call.id, "No hay ninguna suscripción pendiente de confirmar.")

# Comando /unsub
@bot.message_handler(commands=['unsub'])
def handle_unsubscribe(message):
    chat_id = message.chat.id
    sub_info = is_user_subscribed(chat_id)
    if sub_info:
        provincia, municipio = sub_info
        remove_subscription(chat_id)
        bot.send_message(chat_id, f"Tu suscripción al municipio {municipio} ({provincia}) ha sido eliminada. Si quieres volver a suscribirte, usa /sub.")
    else:
        bot.send_message(chat_id, "No tienes ninguna suscripción activa para eliminar. Usa /sub para suscribirte a un municipio.")

# Comando /help
@bot.message_handler(commands=['help', 'hepl'])
def send_help(message):
    help_text = (
        "Comandos disponibles:\n"
        "/start - Inicia la selección de provincia y municipio\n"
        "/sub - Suscríbete a las actualizaciones del municipio seleccionado\n"
        "/unsub - Elimina tu suscripción actual\n"
        "/help - Muestra este mensaje de ayuda\n"
    )
    bot.send_message(message.chat.id, help_text)

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

                # Código para enviar la lista de municipios en varios mensajes
                options_list = [f"{codigo}. {nombre}" for codigo, nombre in municipios.items()]
                max_len = 4000  # Un poco menos de 4096 para dejar margen al texto fijo
                mensaje_base = f"Provincia seleccionada: {provincias[cpro]}. Ahora elige un municipio (escribe el código):\n"

                mensaje = mensaje_base
                for option in options_list:
                    if len(mensaje) + len(option) + 1 > max_len:
                        bot.send_message(chat_id, mensaje)
                        mensaje = ""
                    mensaje += option + "\n"
                if mensaje:
                    bot.send_message(chat_id, mensaje)
            else:
                bot.send_message(chat_id, "Por favor selecciona una provincia válida (código completo).")
        # Si el usuario está seleccionando municipio
        elif 'municipios' in user_data[chat_id]:
            municipios = user_data[chat_id]['municipios']
            municipio_code = message.text.zfill(3)
            if municipio_code in municipios:
                municipio = municipios[municipio_code]
                cpro = user_data[chat_id]['cpro']
                user_data[chat_id]['municipio_code'] = municipio_code  # <-- Añade esta línea
                weather_api = WeatherAPI(API_KEY)
                temp_max, temp_min = weather_api.obtener_datos_actuales_de_municipio(int(cpro), int(municipio_code))
                send_weather_to_telegram(chat_id, user_data[chat_id]['provincia'], municipio, temp_max, temp_min)
                # NO elimines user_data[chat_id] aquí, así el usuario podrá suscribirse después
                # user_data.pop(chat_id)
            else:
                bot.send_message(chat_id, "Código de municipio no válido. Intenta nuevamente.")

# Inicia el bot
if __name__ == "__main__":
    print("El bot está funcionando...")
    bot.infinity_polling()
