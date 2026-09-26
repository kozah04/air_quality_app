# health_risk_analyzer.py
# This file sends the air quality numbers to Gemini (Google's AI)
# and asks it to explain them in plain English, plus give health advice.

import google.generativeai as genai


class HealthRiskAnalyzer:
    """Uses the Gemini API to turn raw pollution numbers into health advice."""

    def __init__(self, api_key):
        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing or empty.")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-3.6-flash")

    def build_prompt(self, reading, cleanest_hour=None):
        # this builds the text message we send to Gemini
        prompt = (
            f"The air quality in {reading.location} right now is:\n"
            f"- US AQI: {reading.aqi}\n"
            f"- PM2.5: {reading.pm2_5}\n"
            f"- PM10: {reading.pm10}\n"
            f"- Ozone: {reading.ozone}\n"
            f"- Nitrogen dioxide: {reading.nitrogen_dioxide}\n\n"
            "Please explain in simple, everyday language what these numbers mean. "
            "Say clearly whether it is safe to be outside right now, especially "
            "for children, elderly people, and people with asthma or other "
            "breathing problems. Then give 2 to 3 short protective tips (like "
            "wearing a mask, closing windows, or using an air purifier) if "
            "needed. Keep the whole answer to about 5-6 sentences, no headings "
            "or bullet points."
        )

        if cleanest_hour is not None:
            prompt += f"\nAlso mention that the cleanest time of day looks like around {cleanest_hour['time']}."

        return prompt

    def get_health_advice(self, reading, cleanest_hour=None):
        """
        Sends the reading to Gemini and returns the advice text.
        If the Gemini call fails for any reason (no internet, bad key,
        etc.) we don't want the whole app to crash, so we return a
        simple fallback message instead.
        """
        prompt = self.build_prompt(reading, cleanest_hour)

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as error:
            return (
                "Sorry, we could not get AI advice right now "
                f"({error}). Please check the raw numbers above and "
                "use general caution if the AQI looks high."
            )
