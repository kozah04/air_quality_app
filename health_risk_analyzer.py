import google.generativeai as genai


class HealthRiskAnalyzer:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-3.6-flash')

    def build_prompt(self, reading, cleanest_hour=None):
        prompt = (
            f"The air quality in {reading.location} right now is:\n"
            f"- US AQI: {reading.aqi}\n"
            f"- PM2.5: {reading.pm2_5}\n"
            f"- PM10: {reading.pm10}\n"
            f"- Ozone: {reading.ozone}\n"
            f"- Nitrogen dioxide: {reading.nitrogen_dioxide}\n\n"
            
            "Please explain in simple, everyday language what these numbers mean. "
            "Say clearly whether it is safe to be outside right now while referencing the city,country, especially "
            "for children, elderly people, and people with asthma or other "
            "breathing problems. Then give 2 to 3 short protective tips (like "
            "wearing a mask, closing windows, or using an air purifier) if "
            "needed. Keep the whole answer to about 5-6 sentences, no headings "
            "or bullet points."
        )

        if cleanest_hour is not None:
            prompt += f"\nAlso mention the cleanest time today looks like around {cleanest_hour['time']}."

        return prompt

    def get_health_advice(self, reading, cleanest_hour=None):
        prompt = self.build_prompt(reading, cleanest_hour)

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return (
                f"Sorry, could not get AI advice right now ({e}). "
                "Check the raw numbers above and be careful if the AQI looks high."
            )
