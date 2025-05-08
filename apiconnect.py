import requests
import pandas as pd  # Para manejar el archivo CSV
import os

API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqdWFuLmFsZWphbmRyby5oaEBnbWFpbC5jb20iLCJqdGkiOiI4Y2U0N2MxNS03NmUzLTQyZmYtYjcxMi1iNWMxZDM1ZjBhMjMiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTc0NjIxMzc3OSwidXNlcklkIjoiOGNlNDdjMTUtNzZlMy00MmZmLWI3MTItYjVjMWQzNWYwYTIzIiwicm9sZSI6IiJ9.dEJe_x7KactkK60URvv9mzlhFLg4Rn3T1OSmwaFwZvA'  # ← Reemplaza por tu clave real

# Función para obtener el nombre de la provincia
def obtener_provincia():
    # Ruta al archivo provincias.csv
    provincias_path = os.path.join('CSV', 'provincias.csv')
    provincias_df = pd.read_csv(provincias_path, delimiter=';')

    print("Lista de provincias disponibles:")
    for index, row in provincias_df.iterrows():
        print(f"{row['CPRO']}: {row['NPRO']}")  # Usa los nombres reales de las columnas

    while True:
        cpro = input("Por favor, introduce el código de la provincia (CPRO): ")
        if cpro.isdigit() and int(cpro) in provincias_df['CPRO'].values:
            provincia = provincias_df[provincias_df['CPRO'] == int(cpro)]['NPRO'].values[0]
            print(f"Has seleccionado la provincia: {provincia}")
            return int(cpro), provincia
        else:
            print("Código de provincia no válido. Inténtalo de nuevo.")

# Función para obtener el municipio
def obtener_municipio(cpro):
    # Ruta al archivo diccionario24.csv
    municipios_path = os.path.join('CSV', 'diccionario24.csv')
    municipios_df = pd.read_csv(municipios_path, delimiter=';')

    # Filtrar los municipios por la provincia seleccionada
    municipios_provincia = municipios_df[municipios_df['CPRO'] == cpro]

    print("Lista de municipios disponibles:")
    for index, row in municipios_provincia.iterrows():
        print(f"{row['CMUN']}: {row['NOMBRE']}")  # Usa los nombres reales de las columnas

    while True:
        cmun = input("Por favor, introduce el código del municipio (CMUN): ")
        if cmun.isdigit() and int(cmun) in municipios_provincia['CMUN'].values:
            municipio = municipios_provincia[municipios_provincia['CMUN'] == int(cmun)]['NOMBRE'].values[0]
            print(f"Has seleccionado el municipio: {municipio}")
            return int(cmun), municipio
        else:
            print("Código de municipio no válido. Inténtalo de nuevo.")

def obtener_datos_actuales_de_municipio(codigo_municipio):
    url = f'https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/{codigo_municipio}'
    params = {'api_key': API_KEY}
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code != 200:
            print(f"Error al obtener observaciones: {response.status_code}")
            print(f"Respuesta del servidor: {response.text}")
            raise Exception(f"Error al obtener observaciones: {response.status_code}")

        datos_url = response.json().get('datos')
        if not datos_url:
            raise Exception("No se encontró la URL de datos meteorológicos.")

        datos_response = requests.get(datos_url)
        if datos_response.status_code != 200:
            print(f"Error al obtener datos meteorológicos: {datos_response.status_code}")
            print(f"Respuesta del servidor: {datos_response.text}")
            raise Exception(f"Error al obtener datos meteorológicos: {datos_response.status_code}")

        datos = datos_response.json()
        # Extraer temperaturas máxima y mínima
        if datos and isinstance(datos, list):
            prediccion = datos[0].get('prediccion', {}).get('dia', [])
            if prediccion:
                temperaturas = prediccion[0].get('temperatura', {})
                temp_max = temperaturas.get('maxima')
                temp_min = temperaturas.get('minima')
                return temp_max, temp_min
        raise Exception("No se pudieron extraer las temperaturas.")
    except Exception as e:
        print(f"Excepción al obtener datos del municipio: {e}")
        raise

# Flujo principal
def main():
    print("Bienvenido al sistema de selección de provincias y municipios.")
    cpro, provincia = obtener_provincia()
    cmun, municipio = obtener_municipio(cpro)
    codigo_municipio = f"{cpro:02d}{cmun:03d}"
    print(f"Has seleccionado la provincia '{provincia}' y el municipio '{municipio}'.")
    print(f"Código del municipio seleccionado: {codigo_municipio}")

    # Obtener y mostrar las temperaturas
    try:
        temp_max, temp_min = obtener_datos_actuales_de_municipio(codigo_municipio)
        print(f"\nTemperatura máxima: {temp_max} °C")
        print(f"Temperatura mínima: {temp_min} °C")
    except Exception as e:
        print(f"Ocurrió un error al obtener los datos meteorológicos: {e}")

