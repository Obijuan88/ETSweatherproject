from apiconnect import WeatherAPI
from telegrambot import send_weather_to_telegram
import csv
from decouple import config

def main():
    API_KEY = config
    weather_api = WeatherAPI(API_KEY)

    print("Bienvenido al sistema de selección de provincias y municipios.")

    # Fetch and display provinces
    provincias = weather_api.obtener_lista_provincias()
    weather_api.mostrar_provincias(provincias)
    cpro, provincia = weather_api.seleccionar_provincia(provincias)
    cpro = str(cpro).zfill(2)  # Convierte cpro a cadena antes de aplicar zfill

    # Fetch and display municipalities
    municipios = weather_api.obtener_lista_municipios(cpro)
    if not municipios:
        print("No se encontraron municipios para esta provincia.")
        return
    weather_api.mostrar_municipios(municipios)
    cmun, municipio = weather_api.seleccionar_municipio(municipios)

    # Fetch and display weather data
    codigo_municipio = f"{int(cpro):02d}{int(cmun):03d}"  # Convierte cpro y cmun a enteros antes de aplicar el formato
    print(f"\nHas seleccionado la provincia '{provincia}' y el municipio '{municipio}'.")
    print(f"Código del municipio seleccionado: {codigo_municipio}")

    try:
        temp_max, temp_min = weather_api.obtener_datos_actuales_de_municipio(cpro, cmun)
        print(f"\nTemperatura máxima: {temp_max} °C")
        print(f"Temperatura mínima: {temp_min} °C")

        # Send weather data to Telegram bot
        send_weather_to_telegram(provincia, municipio, temp_max, temp_min)

    except Exception as e:
        print(f"Ocurrió un error al obtener los datos meteorológicos: {e}")

if __name__ == "__main__":
    main()