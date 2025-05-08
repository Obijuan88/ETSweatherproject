from apiconnect import WeatherAPI

def main():
    API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqdWFuLmFsZWphbmRyby5oaEBnbWFpbC5jb20iLCJqdGkiOiI4Y2U0N2MxNS03NmUzLTQyZmYtYjcxMi1iNWMxZDM1ZjBhMjMiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTc0NjIxMzc3OSwidXNlcklkIjoiOGNlNDdjMTUtNzZlMy00MmZmLWI3MTItYjVjMWQzNWYwYTIzIiwicm9sZSI6IiJ9.dEJe_x7KactkK60URvv9mzlhFLg4Rn3T1OSmwaFwZvA'  # Replace with your actual API key
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
    print(f"\nHas seleccionado la provincia '{provincia}' y el municipio '{municipio}'.")
    print(f"Código del municipio seleccionado: {cpro:02d}{cmun:03d}")

    try:
        temp_max, temp_min = weather_api.obtener_datos_actuales_de_municipio(cpro, cmun)
        print(f"\nTemperatura máxima: {temp_max} °C")
        print(f"Temperatura mínima: {temp_min} °C")
    except Exception as e:
        print(f"Ocurrió un error al obtener los datos meteorológicos: {e}")

if __name__ == "__main__":
    main()