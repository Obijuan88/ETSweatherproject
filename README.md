# ETS Weather Project

## Overview
The ETS Weather Project is a Python application that allows users to select a province and municipality in Spain and fetch current weather data for the selected municipality. The application utilizes the AEMET Open Data API to retrieve weather information.

## Project Structure
```
ETSweatherproject
├── src
│   ├── apiconnect.py        # Contains functions for obtaining province and municipality data, and fetching weather data.
│   ├── main.py              # Entry point of the application.
│   └── utils
│       ├── __init__.py      # Marks the utils directory as a package.
│       └── data_loader.py    # Utility functions for loading data from CSV files.
├── CSV
│   ├── provincias.csv        # CSV file containing province data (codes and names).
│   └── diccionario24.csv     # CSV file containing municipality data (codes and names).
├── requirements.txt          # Lists the dependencies required for the project.
└── README.md                 # Documentation for the project.
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd ETSweatherproject
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```
   python src/main.py
   ```
2. Follow the prompts to select a province and municipality.
3. The application will display the current maximum and minimum temperatures for the selected municipality.

## Dependencies
- `requests`: For making HTTP requests to the AEMET Open Data API.
- `pandas`: For handling CSV data.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.