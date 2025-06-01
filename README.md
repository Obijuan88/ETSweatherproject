# Proyecto ETS Weather

## Descripción
El proyecto ETS Weather es una aplicación en Python que permite a los usuarios seleccionar una provincia y un municipio en España para obtener datos meteorológicos actuales de dicho municipio. La aplicación utiliza la API de AEMET Open Data para recuperar información meteorológica y proporciona funcionalidad para actualizar los datos de temperatura en una base de datos SQLite local.

## Estructura del Proyecto
```
ETSweatherproject
├── src
│   ├── apiconnect.py        # Funciones para obtener datos de provincias y municipios, y recuperar datos meteorológicos.
│   ├── main.py              # Punto de entrada de la aplicación.
│   ├── bbdd.py              # Funciones para interactuar con la base de datos SQLite.
│   ├── telegrambot.py       # Funciones para interactuar con bots de Telegram.
│   ├── telegramsub.py       # Funciones para gestionar suscripciones de Telegram.
│   └── utils
│       ├── __init__.py      # Marca el directorio utils como un paquete.
│       └── data_loader.py   # Funciones utilitarias para cargar datos desde archivos CSV.
├── CSV
│   ├── provincias.csv       # Archivo CSV con datos de provincias (códigos y nombres).
│   └── diccionario24.csv    # Archivo CSV con datos de municipios (códigos y nombres).
├── BBDD
│   └── weather.db           # Base de datos SQLite con datos meteorológicos.
├── Docker
│   ├── compose.yml          # Archivo de configuración para Docker Compose.
│   ├── cronjob              # Script para tareas programadas.
│   ├── Dockerfile           # Archivo Dockerfile para construir la imagen.
│   ├── requirements.txt     # Dependencias necesarias para el contenedor.
│   └── start.sh             # Script de inicio para el contenedor.
├── uml
│   └── diagram.png          # Diagrama UML del proyecto.
├── requirements.txt         # Lista de dependencias necesarias para el proyecto.
└── README.md                # Documentación del proyecto.
```

## Instalación
### Instalación Local
1. Clona el repositorio:
   ```bash
   git clone <url-del-repositorio>
   ```
2. Navega al directorio del proyecto:
   ```bash
   cd ETSweatherproject
   ```
3. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```

### Instalación en Docker
1. Asegúrate de tener Docker y Docker Compose instalados en tu sistema.
2. Clona el repositorio:
   ```bash
   git clone <url-del-repositorio>
   ```
3. Navega al directorio del proyecto:
   ```bash
   cd ETSweatherproject/Docker
   ```
4. Construye y ejecuta el contenedor:
   ```bash
   docker-compose up --build
   ```
5. Una vez que el contenedor esté en ejecución, puedes interactuar con la aplicación desde el terminal o mediante los scripts disponibles.

## Uso
### Obtener Datos Meteorológicos
1. Ejecuta la aplicación:
   ```bash
   python src/main.py
   ```
2. Sigue las instrucciones para seleccionar una provincia y un municipio.
3. La aplicación mostrará las temperaturas máximas y mínimas actuales del municipio seleccionado.

### Actualizar Datos de Temperatura
1. Ejecuta el script de actualización de la base de datos:
   ```bash
   python src/bbdd.py
   ```
2. Este script ajustará la fecha (restando un día) y disminuirá la temperatura mínima en 2 grados en la tabla `temperature_queries`.

## Dependencias
- `requests`: Para realizar solicitudes HTTP a la API de AEMET Open Data.
- `pandas`: Para manejar datos en formato CSV.
- `pyTelegramBotAPI`: Para interactuar con bots de Telegram.
- `python-decouple`: Para gestionar variables de entorno y configuraciones sensibles.
- `sqlite3`: Para interactuar con la base de datos SQLite.

## Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

## Contribuciones
¡Las contribuciones son bienvenidas! Por favor, haz un fork del repositorio y envía un pull request con tus cambios.

## Contacto
Para preguntas o soporte, contacta a [juan.alejandro.hh@gmail.com].