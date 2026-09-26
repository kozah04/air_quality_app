# Air Quality & Pollution Health Advisor

A simple Python + Streamlit app that checks the air quality for any
location, explains what the numbers mean using Gemini AI, and gives
health advice.

## Project Structure

```
air_quality_app/
├── main.py                     # Streamlit app - the screen you see
├── air_quality_client.py       # Talks to the Open-Meteo API
├── air_reading.py              # AirReading class - holds one reading's data
├── health_risk_analyzer.py     # Talks to Gemini API for health advice
├── location_history_store.py   # Saves/loads data to JSON files
├── validators.py                # Regex checks for user input
├── requirements.txt            # Python packages needed
├── data/                       # Created automatically - stores history.json and favourites.json
└── README.md
```