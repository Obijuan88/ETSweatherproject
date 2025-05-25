from apiconnect import WeatherAPI
from telegrambot import send_weather_to_telegram

def main():
    API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqdWFuLmFsZWphbmRyby5oaEBnbWFpbC5jb20iLCJqdGkiOiI1NGFlMzYzMC0wMzdmLTQ0NzMtYTFlYy1jMDk4NzY5ZTk2OGMiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTc0NjIxMjM0NCwidXNlcklkIjoiNTRhZTM2MzAtMDM3Zi00NDczLWExZWMtYzA5ODc2OWU5NjhjIiwicm9sZSI6IiJ9.wSrXhd45UFgntTyCeRlPrDv9EqBsZIJdgcUH9qkyLQk'  # Replace with your actual API key
    weather_api = WeatherAPI(API_KEY)

    print("Bienvenido al sistema de selección de provincias y municipios.")

    # Fetch and display provinces
    provincias = weather_api.obtener_lista_provincias()
    weather_api.mostrar_provincias(provincias)
    cpro, provincia = weather_api.seleccionar_provincia(provincias)

    # Fetch and display municipalities
    municipios = weather_api.obtener_lista_municipios(cpro)
    if not municipios:
        print("No se encontraron municipios para esta provincia.")
        return
    weather_api.mostrar_municipios(municipios)
    cmun, municipio = weather_api.seleccionar_municipio(municipios)

    # Fetch and display weather data
    codigo_municipio = f"{cpro:02d}{cmun:03d}"
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