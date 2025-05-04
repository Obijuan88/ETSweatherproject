import requests

API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqdWFuLmFsZWphbmRyby5oaEBnbWFpbC5jb20iLCJqdGkiOiI4Y2U0N2MxNS03NmUzLTQyZmYtYjcxMi1iNWMxZDM1ZjBhMjMiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTc0NjIxMzc3OSwidXNlcklkIjoiOGNlNDdjMTUtNzZlMy00MmZmLWI3MTItYjVjMWQzNWYwYTIzIiwicm9sZSI6IiJ9.dEJe_x7KactkK60URvv9mzlhFLg4Rn3T1OSmwaFwZvA'

def probar_clave():
    url = f"https://opendata.aemet.es/opendata/api/observacion/convencional/datos/estacion/C406G/?api_key={API_KEY}"
    response = requests.get(url)
    print(f"Código de estado HTTP: {response.status_code}")
    print("Contenido:")
    print(response.text)

probar_clave()
