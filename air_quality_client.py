# air_quality_client.py
# This file is in charge of talking to the Open-Meteo API.
# It turns a location name into coordinates, then fetches the
# current and forecast air quality for those coordinates.

import requests


class AirQualityClient:
    """Handles all communication to the Open-Meteo API."""

    GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
    AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

    def get_coordinates(self, location_name):
        """
        Turns a location name like "Lagos" into (latitude, longitude, full_name).
        Raises a ValueError if the location can't be found, or a
        ConnectionError if the API can't be reached.
        """
        params = {"name": location_name, "count": 1}

        try:
            response = requests.get(self.GEOCODE_URL, params=params, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            raise ConnectionError(f"Could not reach geocoding service: {error}")

        data = response.json()
        results = data.get("results")

        if not results:
            raise ValueError(f"Could not find a place called '{location_name}'")

        place = results[0]
        latitude = place["latitude"]
        longitude = place["longitude"]
        full_name = place.get("name", location_name)

        return latitude, longitude, full_name

    def get_current_air_quality(self, latitude, longitude):
        """
        Gets the current air quality for a location.
        Returns a dictionary with aqi, pm2_5, pm10, ozone, nitrogen_dioxide.
        """
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "us_aqi,pm2_5,pm10,ozone,nitrogen_dioxide",
            "timezone": "auto",
        }

        try:
            response = requests.get(self.AIR_QUALITY_URL, params=params, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            raise ConnectionError(f"Could not reach air quality service: {error}")

        data = response.json()
        current = data.get("current")

        if not current:
            raise ValueError("No current air quality data available for this location")

        return {
            "aqi": current.get("us_aqi"),
            "pm2_5": current.get("pm2_5"),
            "pm10": current.get("pm10"),
            "ozone": current.get("ozone"),
            "nitrogen_dioxide": current.get("nitrogen_dioxide"),
        }

    def get_forecast_air_quality(self, latitude, longitude):
        """
        Gets an hour-by-hour air quality forecast for today, so we can
        work out the cleanest time to go outside.
        Returns a list of dictionaries like: {"time": ..., "aqi": ...}
        """
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "us_aqi,pm2_5",
            "timezone": "auto",
            "forecast_days": 1,
        }

        try:
            response = requests.get(self.AIR_QUALITY_URL, params=params, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            raise ConnectionError(f"Could not reach forecast service: {error}")

        data = response.json()
        hourly = data.get("hourly")

        if not hourly:
            raise ValueError("No forecast data available for this location")

        times = hourly.get("time", [])
        aqi_values = hourly.get("us_aqi", [])

        forecast_list = []
        for i in range(len(times)):
            forecast_list.append({
                "time": times[i],
                "aqi": aqi_values[i] if i < len(aqi_values) else None,
            })

        return forecast_list

    def find_cleanest_hour(self, forecast_list):
        """
        Goes through the forecast list and returns the hour with the
        lowest AQI (i.e. the cleanest air). Returns None if the list is empty.
        """
        cleanest = None

        for entry in forecast_list:
            if entry["aqi"] is None:
                continue
            if cleanest is None or entry["aqi"] < cleanest["aqi"]:
                cleanest = entry

        return cleanest
