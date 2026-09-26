# location_history_store.py
# This file handles saving and loading our data to/from JSON files:
# - past air quality readings (history.json)
# - favourite locations (favourites.json)

import json
import os


class LocationHistoryStore:
    """Handles reading and writing our saved data to JSON files."""

    def __init__(self, history_file="data/history.json", favourites_file="data/favourites.json"):
        self.history_file = history_file
        self.favourites_file = favourites_file

        # make sure the "data" folder exists before we try to read/write into it
        folder = os.path.dirname(self.history_file)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)

    def save_reading(self, reading):
        """Adds a new reading to the history file."""
        history = self.load_history()
        history.append(reading.to_dict())

        try:
            with open(self.history_file, "w") as file:
                json.dump(history, file, indent=2)
        except IOError as error:
            print(f"Could not save reading to file: {error}")

    def load_history(self):
        """Loads all past readings. Returns an empty list if the file doesn't exist yet."""
        if not os.path.exists(self.history_file):
            return []

        try:
            with open(self.history_file, "r") as file:
                return json.load(file)
        except (IOError, json.JSONDecodeError) as error:
            print(f"Could not read history file, starting fresh: {error}")
            return []

    def add_favourite(self, location_name):
        """Adds a location name to the favourites list, avoiding duplicates."""
        favourites = self.load_favourites()

        if location_name not in favourites:
            favourites.append(location_name)

        try:
            with open(self.favourites_file, "w") as file:
                json.dump(favourites, file, indent=2)
        except IOError as error:
            print(f"Could not save favourite: {error}")

    def load_favourites(self):
        """Loads the list of favourite locations."""
        if not os.path.exists(self.favourites_file):
            return []

        try:
            with open(self.favourites_file, "r") as file:
                return json.load(file)
        except (IOError, json.JSONDecodeError) as error:
            print(f"Could not read favourites file, starting fresh: {error}")
            return []
