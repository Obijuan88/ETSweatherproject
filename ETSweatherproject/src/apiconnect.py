import sys
import csv
import os
import requests
print(sys.path)

class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://opendata.aemet.es/opendata/api"
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.provincias_csv = os.path.join(base_dir, "../CSV/provincias.csv")
        self.diccionario_csv = os.path.join(base_dir, "../CSV/diccionario24.csv")

    def obtener_lista_provincias(self):
        provincias = {}
        with open(self.provincias_csv, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            next(reader)  # Skip header
            for row in reader:
                cpro = int(row[0])  # Province code
                provincia = row[1]  # Province name
                provincias[cpro] = provincia
        return provincias

    def mostrar_provincias(self, provincias):
        print("\nSelecciona una provincia:")
        for idx, (cpro, provincia) in enumerate(provincias.items(), start=1):
            print(f"{idx}. {provincia}")

    def seleccionar_provincia(self, provincias):
        while True:
            try:
                provincia_idx = int(input("Introduce el número de la provincia: ")) - 1
                if 0 <= provincia_idx < len(provincias):
                    cpro, provincia = list(provincias.items())[provincia_idx]
                    return cpro, provincia
                else:
                    print("Por favor, introduce un número válido.")
            except ValueError:
                print("Entrada no válida. Por favor, introduce un número.")

    def obtener_lista_municipios(self, cpro):
        municipios = {}
        with open(self.diccionario_csv, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            next(reader)  # Skip header
            for row in reader:
                if int(row[0]) == cpro:  # Match province code
                    cmun = int(row[1])  # Municipality code
                    municipio = row[2]  # Municipality name
                    municipios[cmun] = municipio
        return municipios

    def mostrar_municipios(self, municipios):
        print("\nMunicipios disponibles:")
        for cmun, municipio in municipios.items():
            print(f"{cmun:03d}, {municipio}")

    def seleccionar_municipio(self, municipios):
        while True:
            try:
                municipio_idx = int(input("\nIntroduce el código del municipio: "))
                if municipio_idx in municipios:
                    return municipio_idx, municipios[municipio_idx]
                else:
                    print("Por favor, introduce un código de municipio válido.")
            except ValueError:
                print("Entrada no válida. Por favor, introduce un número.")

    def obtener_datos_actuales_de_municipio(self, cpro, codigo_municipio):
        # Combine province code and municipality code
        codigo_completo = f"{cpro:02d}{codigo_municipio:03d}"
        url = f"{self.base_url}/prediccion/especifica/municipio/diaria/{codigo_completo}"
        headers = {
            "accept": "application/json",
            "api_key": self.api_key
        }

        try:
            # Step 1: Fetch the data from the API
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
            data = response.json()

            # Step 2: Extract the URL for the actual data
            datos_url = data.get("datos")
            if not datos_url:
                print("No se encontró la URL de los datos en la respuesta.")
                return None, None

            # Step 3: Fetch the actual data from the "datos" URL
            datos_response = requests.get(datos_url)
            datos_response.raise_for_status()
            datos = datos_response.json()

            # Step 4: Extract temperature data from the JSON
            # Assuming the structure contains a list of days with temperature data
            if datos and isinstance(datos, list):
                prediccion = datos[0].get("prediccion", {})
                temperaturas = prediccion.get("dia", [])[0]  # First day of prediction
                temp_max = temperaturas.get("temperatura", {}).get("maxima", "N/A")
                temp_min = temperaturas.get("temperatura", {}).get("minima", "N/A")
                return temp_max, temp_min
            else:
                print("No se encontraron datos de predicción.")
                return None, None

        except requests.exceptions.RequestException as e:
            print(f"Error al obtener los datos del municipio: {e}")
            return None, None
        except (KeyError, IndexError) as e:
            print(f"Error al procesar los datos del municipio: {e}")
            return None, None