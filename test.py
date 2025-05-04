
import requests

url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones/"

querystring = {"api_key":"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqdWFuLmFsZWphbmRyby5oaEBnbWFpbC5jb20iLCJqdGkiOiI4Y2U0N2MxNS03NmUzLTQyZmYtYjcxMi1iNWMxZDM1ZjBhMjMiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTc0NjIxMzc3OSwidXNlcklkIjoiOGNlNDdjMTUtNzZlMy00MmZmLWI3MTItYjVjMWQzNWYwYTIzIiwicm9sZSI6IiJ9.dEJe_x7KactkK60URvv9mzlhFLg4Rn3T1OSmwaFwZvA"}

headers = {
    'cache-control': "no-cache"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)