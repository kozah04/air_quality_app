# main.py
# This is the main app file - it builds the screen the user sees.
# Run it with: streamlit run main.py

import streamlit as st

from air_quality_client import AirQualityClient
from air_reading import AirReading
from health_risk_analyzer import HealthRiskAnalyzer
from location_history_store import LocationHistoryStore
from validators import is_valid_location_name
from dotenv import load_dotenv 
import os 
load_dotenv() 
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# ---- basic page setup ----
st.set_page_config(page_title="Air Quality & Pollution Health Advisor", layout="centered")
st.title("Air Quality & Pollution Health Advisor")

# ---- set up our helper objects (one of each, shared across the whole app) ----
client = AirQualityClient()
store = LocationHistoryStore()

analyzer = HealthRiskAnalyzer(GEMINI_API_KEY) if GEMINI_API_KEY else None

if not GEMINI_API_KEY:
    st.warning("Set the GEMINI_API_KEY environment variable to enable AI health advice.")

# ---- sidebar: show favourite locations ----
st.sidebar.header("Favourite Locations")
favourites = store.load_favourites()

if favourites:
    for place in favourites:
        st.sidebar.write(f"- {place}")
else:
    st.sidebar.write("No favourites saved yet.")

# ---- tabs for the different features ----
tab1, tab2, tab3 = st.tabs(["Check a Location", "Compare Two Locations", "History"])

# ================= TAB 1: check one location =================
with tab1:
    location_input = st.text_input("Enter a location (e.g. Abuja):", key="single_location")

    if st.button("Check Air Quality"):
        if not is_valid_location_name(location_input):
            st.error("Please enter a valid location name (letters and spaces only).")
        else:
            try:
                latitude, longitude, full_name = client.get_coordinates(location_input)
                current_data = client.get_current_air_quality(latitude, longitude)
                forecast_data = client.get_forecast_air_quality(latitude, longitude)
                cleanest_hour = client.find_cleanest_hour(forecast_data)

                reading = AirReading(
                    location=full_name,
                    latitude=latitude,
                    longitude=longitude,
                    aqi=current_data["aqi"],
                    pm2_5=current_data["pm2_5"],
                    pm10=current_data["pm10"],
                    ozone=current_data["ozone"],
                    nitrogen_dioxide=current_data["nitrogen_dioxide"],
                )

                if analyzer is not None:
                    with st.spinner("Getting AI health advice..."):
                        advice = analyzer.get_health_advice(reading, cleanest_hour)
                else:
                    advice = (
                        "AI health advice is unavailable because GEMINI_API_KEY is not configured. "
                        "Please check the raw numbers above and use general caution if AQI is high."
                    )

                # save this reading to our history file automatically
                store.save_reading(reading)

                # Streamlit reruns this whole file every time you click a
                # button, so we save the results in st.session_state.
                # That way the results stay on screen even after we click
                # the "Save as Favourite" button further down.
                st.session_state["last_reading"] = reading
                st.session_state["last_cleanest_hour"] = cleanest_hour
                st.session_state["last_advice"] = advice

            except ValueError as error:
                st.error(str(error))
            except ConnectionError as error:
                st.error(str(error))
            except Exception as error:
                st.error(f"Something went wrong: {error}")

    # show the last result, if we have one saved in this session
    if "last_reading" in st.session_state:
        reading = st.session_state["last_reading"]
        cleanest_hour = st.session_state.get("last_cleanest_hour")
        advice = st.session_state.get("last_advice")

        st.subheader(f"Results for {reading.location}")
        st.write(f"**AQI:** {reading.aqi}")
        st.write(f"**PM2.5:** {reading.pm2_5}")
        st.write(f"**PM10:** {reading.pm10}")
        st.write(f"**Ozone:** {reading.ozone}")
        st.write(f"**Nitrogen dioxide:** {reading.nitrogen_dioxide}")

        if cleanest_hour:
            st.write(f"**Cleanest hour today looks like:** {cleanest_hour['time']}")

        st.info(advice)

        if st.button("Save as Favourite"):
            store.add_favourite(reading.location)
            st.success(f"{reading.location} added to favourites!")

# ================= TAB 2: compare two locations =================
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        location_a = st.text_input("First location:", key="location_a")
    with col2:
        location_b = st.text_input("Second location:", key="location_b")

    if st.button("Compare"):
        if not is_valid_location_name(location_a) or not is_valid_location_name(location_b):
            st.error("Please enter two valid location names.")
        else:
            try:
                lat_a, lon_a, name_a = client.get_coordinates(location_a)
                data_a = client.get_current_air_quality(lat_a, lon_a)

                lat_b, lon_b, name_b = client.get_coordinates(location_b)
                data_b = client.get_current_air_quality(lat_b, lon_b)

                result_col1, result_col2 = st.columns(2)
                with result_col1:
                    st.subheader(name_a)
                    st.write(f"AQI: {data_a['aqi']}")
                    st.write(f"PM2.5: {data_a['pm2_5']}")
                with result_col2:
                    st.subheader(name_b)
                    st.write(f"AQI: {data_b['aqi']}")
                    st.write(f"PM2.5: {data_b['pm2_5']}")

                if data_a["aqi"] is not None and data_b["aqi"] is not None:
                    if data_a["aqi"] < data_b["aqi"]:
                        st.success(f"{name_a} has cleaner air right now.")
                    elif data_b["aqi"] < data_a["aqi"]:
                        st.success(f"{name_b} has cleaner air right now.")
                    else:
                        st.info("Both locations have similar air quality.")

            except ValueError as error:
                st.error(str(error))
            except ConnectionError as error:
                st.error(str(error))
            except Exception as error:
                st.error(f"Something went wrong: {error}")

# ================= TAB 3: history =================
with tab3:
    st.subheader("Past Readings")
    history = store.load_history()

    if not history:
        st.write("No history saved yet. Check a location first!")
    else:
        # show the most recent readings first
        for entry in reversed(history):
            st.write(
                f"{entry['location']} — {entry['timestamp']} — "
                f"AQI: {entry['aqi']}, PM2.5: {entry['pm2_5']}"
            )
