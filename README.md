# ETS Weather Project

## Overview
The ETS Weather Project is a Python application that allows users to select a province and municipality in Spain and fetch current weather data for the selected municipality. The application utilizes the AEMET Open Data API to retrieve weather information and provides functionality to update temperature data in a local SQLite database.

## Project Structure
```
ETSweatherproject
├── src
│   ├── apiconnect.py        # Contains functions for obtaining province and municipality data, and fetching weather data.
│   ├── main.py              # Entry point of the application.
│   ├── bbdd.py              # Functions for interacting with the SQLite database.
│   └── utils
│       ├── __init__.py      # Marks the utils directory as a package.
│       └── data_loader.py   # Utility functions for loading data from CSV files.
├── CSV
│   ├── provincias.csv       # CSV file containing province data (codes and names).
│   └── diccionario24.csv    # CSV file containing municipality data (codes and names).
├── BBDD
│   └── weather.db           # SQLite database containing weather data.
├── requirements.txt         # Lists the dependencies required for the project.
└── README.md                # Documentation for the project.
```

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd ETSweatherproject
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
### Fetch Weather Data
1. Run the application:
   ```bash
   python src/main.py
   ```
2. Follow the prompts to select a province and municipality.
3. The application will display the current maximum and minimum temperatures for the selected municipality.

### Update Temperature Data
1. Run the database update script:
   ```bash
   python src/bbdd.py
   ```
2. This will adjust the date (subtract one day) and decrease the minimum temperature by 2 degrees in the `temperature_queries` table.

## Dependencies
- `requests`: For making HTTP requests to the AEMET Open Data API.
- `pandas`: For handling CSV data.
- `pyTelegramBotAPI`: For interacting with Telegram bots.
- `python-decouple`: For managing environment variables and sensitive configurations.
- `sqlite3`: For interacting with the SQLite database.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## Contact
For questions or support, please contact [juan.alejandro.hh@gmail.com].