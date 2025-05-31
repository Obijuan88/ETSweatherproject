import sys
import os
from datetime import datetime
import csv
import requests
import json
import time

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
        #print(f"[DEBUG] Cargando municipios para la provincia: {cpro}")
        try:
            with open(self.diccionario_csv, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=';')
                next(reader)  # Skip header
                for row in reader:
                    if row[0].zfill(2) == cpro:
                        municipios[row[1].zfill(3)] = row[2]
            #print(f"[DEBUG] Municipios cargados: {municipios}")
        except FileNotFoundError:
            print("[ERROR] El archivo diccionario24.csv no se encontró.")
        except Exception as e:
            print(f"[ERROR] Error al cargar municipios: {e}")
        return municipios

    def mostrar_municipios(self, municipios):
        print("Municipios disponibles:")
        for cmun, municipio in municipios.items():
            print(f"{int(cmun):03d}, {municipio}")  # Convierte cmun a entero antes de aplicar :03d

    def seleccionar_municipio(self, municipios):
        #print(f"[DEBUG] Municipios disponibles: {municipios}")
        while True:
            cmun = input("Introduce el código del municipio: ").zfill(3)
            #print(f"[DEBUG] Código ingresado: {cmun}")
            if cmun in municipios:
                return cmun, municipios[cmun]
            print("Por favor, introduce un código de municipio válido.")

    def obtener_datos_actuales_de_municipio(self, cpro, codigo_municipio):
        try:
            codigo_completo = f"{int(cpro):02d}{int(codigo_municipio):03d}"
            url = f"{self.base_url}/prediccion/especifica/municipio/diaria/{codigo_completo}"
            headers = {
                "accept": "application/json",
                "api_key": self.api_key
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            # Procesar los datos obtenidos
            datos_url = data.get("datos")
            if not datos_url:
                print("[ERROR] No se encontró la URL de los datos en la respuesta.")
                return None, None
            
            datos_response = requests.get(datos_url)
            datos_response.raise_for_status()
            datos = datos_response.json()
            
            if datos and isinstance(datos, list):
                prediccion = datos[0].get("prediccion", {})
                temperaturas = prediccion.get("dia", [])[0]
                temp_max = temperaturas.get("temperatura", {}).get("maxima", None)
                temp_min = temperaturas.get("temperatura", {}).get("minima", None)
                return temp_max, temp_min
            else:
                print("[ERROR] No se encontraron datos de predicción.")
                return None, None
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Error al obtener los datos del municipio: {e}")
            return None, None