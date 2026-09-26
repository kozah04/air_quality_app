# Air Quality & Pollution Health Advisor

A Streamlit app that checks air quality for a location, compares cities,
shows recent saved readings, and gives simple health guidance based on
pollution data and Gemini AI.

## Overview

This project uses:
- Open-Meteo geocoding and air-quality APIs
- Google Gemini for plain-language health advice
- JSON files for storing recent history and favourite locations
- Streamlit for the dashboard interface

## Project Structure

```text
air_quality_app/
├── main.py                     # Streamlit app entry point
├── air_quality_client.py       # Gets coordinates and air quality data
├── air_reading.py              # Stores one air quality reading
├── health_risk_analyzer.py     # Sends the reading to Gemini for advice
├── location_history_store.py   # Saves history and favourites to JSON
├── validators.py               # Input validation helpers
├── requirements.txt            # Python dependencies
├── data/                      # Auto-created folder for JSON files
│   ├── history.json
│   └── favourites.json
├── README.md
└── .env.example               # Optional example for local environment setup
```

## Setup

1. Install Python 3.9 or newer.
2. Open a terminal in the project folder and install dependencies:

```bash
pip install -r requirements.txt
```

3. Get a Gemini API key from Google AI Studio:
   https://aistudio.google.com/app/apikey

4. Set the environment variable before running the app.

Windows PowerShell:
```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

macOS/Linux:
```bash
export GEMINI_API_KEY="your_api_key_here"
```

You can also create a `.env` file in the project root if you want to use `python-dotenv`.

## Run the App

```bash
streamlit run main.py
```

## Features

- Check one location's current AQI and pollution values
- Compare two cities side by side
- View saved history from previous checks
- Save favourite locations
- Get a health-risk explanation from Gemini AI

## How It Works

1. The user enters a place name.
2. `AirQualityClient` converts it to coordinates and fetches current and forecast data from Open-Meteo.
3. `AirReading` stores all the air quality values in one object.
4. `HealthRiskAnalyzer` sends the reading to Gemini and returns simple advice.
5. `LocationHistoryStore` saves the reading and favourites to JSON.
6. `main.py` renders the dashboard and user interface.

## Notes

- The app is designed as a small project and uses friendly fallback messages when AI or network requests fail.
- If the Gemini API key is missing, the app warns the user instead of crashing.
- History files are stored locally in the `data` folder.
- The app is intentionally simple and easy to extend.

## Known Limitations

- It depends on external API availability and a valid Gemini key.
- It does not use a database or advanced caching.
- Validation is intentionally lightweight and suits a classroom-style project.
