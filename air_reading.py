# air_reading.py
# This file has a simple class that holds one air quality reading.
# Think of it like a container that keeps all the numbers for one
# location at one point in time, together in one place.

import datetime


class AirReading:
    """Holds all the info for one air quality check."""

    def __init__(self, location, latitude, longitude, aqi, pm2_5, pm10,
                 ozone, nitrogen_dioxide, timestamp=None):
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.aqi = aqi
        self.pm2_5 = pm2_5
        self.pm10 = pm10
        self.ozone = ozone
        self.nitrogen_dioxide = nitrogen_dioxide

        # if no timestamp was given, just use right now
        if timestamp is None:
            self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.timestamp = timestamp

    def to_dict(self):
        # turns this reading into a normal dictionary so we can save it as JSON
        return {
            "location": self.location,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "aqi": self.aqi,
            "pm2_5": self.pm2_5,
            "pm10": self.pm10,
            "ozone": self.ozone,
            "nitrogen_dioxide": self.nitrogen_dioxide,
            "timestamp": self.timestamp,
        }

    @staticmethod
    def from_dict(data):
        # rebuilds an AirReading object from a dictionary
        # (used when we load old readings back from the JSON file)
        return AirReading(
            location=data.get("location"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            aqi=data.get("aqi"),
            pm2_5=data.get("pm2_5"),
            pm10=data.get("pm10"),
            ozone=data.get("ozone"),
            nitrogen_dioxide=data.get("nitrogen_dioxide"),
            timestamp=data.get("timestamp"),
        )

    def __str__(self):
        # this controls what gets printed if you do print(some_reading)
        return f"{self.location} at {self.timestamp} - AQI: {self.aqi}"
