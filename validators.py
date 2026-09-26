# validators.py
# Small helper functions that use regex (regular expressions) to check
# user input before we try to use it. Keeping these separate from the
# rest of the app makes it easy to test them on their own.

import re


def is_valid_location_name(text):
    """
    Checks if the text looks like a real place name.
    Allows letters, spaces, commas and hyphens (e.g. "Abuja, Nigeria").
    Returns True or False.
    """
    if not text:
        return False

    text = text.strip()
    pattern = r"^[A-Za-z\s,\-]+$"
    return bool(re.match(pattern, text))


def is_valid_coordinates(text):
    """
    Checks if text looks like "latitude, longitude",
    for example "9.0765, 7.3986"
    """
    pattern = r"^\s*-?\d{1,3}(\.\d+)?\s*,\s*-?\d{1,3}(\.\d+)?\s*$"
    return bool(re.match(pattern, text))


def extract_numbers(text):
    """
    Pulls out every number (including decimals) from a piece of text.
    Example: "AQI is 42.5 today" -> ["42.5"]
    """
    pattern = r"-?\d+\.?\d*"
    return re.findall(pattern, text)


def is_valid_date(text):
    """
    Checks if a date string looks like YYYY-MM-DD, e.g. "2026-09-24"
    """
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    return bool(re.match(pattern, text))
