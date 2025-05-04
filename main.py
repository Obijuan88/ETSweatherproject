def main():
    print("Welcome to the ETS Weather Project!")
    # Add your weather project logic here

if __name__ == "__main__":
    main()
    import requests

API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqdWFuLmFsZWphbmRyby5oaEBnbWFpbC5jb20iLCJqdGkiOiI1NGFlMzYzMC0wMzdmLTQ0NzMtYTFlYy1jMDk4NzY5ZTk2OGMiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTc0NjIxMjM0NCwidXNlcklkIjoiNTRhZTM2MzAtMDM3Zi00NDczLWExZWMtYzA5ODc2OWU5NjhjIiwicm9sZSI6IiJ9.wSrXhd45UFgntTyCeRlPrDv9EqBsZIJdgcUH9qkyLQk'  # reemplázalo por tu clave personal

def obtener_estaciones():
    url = f"https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todas/?api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and 'datos' in data:
        estaciones_url = data['datos']
        estaciones_response = requests.get(estaciones_url)
        return estaciones_response.json()
    else:
        print("Error al obtener las estaciones")
        return []

def obtener_datos_estacion(indicativo):
    url = f"https://opendata.aemet.es/opendata/api/observacion/convencional/datos/estacion/{indicativo}/?api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and 'datos' in data:
        datos_url = data['datos']
        datos_response = requests.get(datos_url)
        return datos_response.json()
    else:
        print("Error al obtener los datos de la estación")
        return []

def mostrar_temperatura_por_provincia(nombre_provincia):
    estaciones = obtener_estaciones()
    estaciones_prov = [e for e in estaciones if e['provincia'].lower() == nombre_provincia.lower()]

    if not estaciones_prov:
        print("No se encontraron estaciones para esa provincia.")
        return

    # Tomamos la primera estación disponible
    estacion = estaciones_prov[0]
    datos = obtener_datos_estacion(estacion['indicativo'])

    if datos:
        ultima_obs = datos[-1]
        print(f"Temperatura en {nombre_provincia} ({estacion['nombre']}): {ultima_obs['ta']} °C")
    else:
        print("No se pudieron obtener los datos de temperatura.")

    def listar_provincias_disponibles():
        estaciones = obtener_estaciones()
        provincias = sorted(set(e['provincia'] for e in estaciones))
        print("Provincias disponibles:")
        for p in provincias:
            print(f"- {p}")
# Ejecución
provincia = input("Introduce una provincia: ")
mostrar_temperatura_por_provincia(provincia)
