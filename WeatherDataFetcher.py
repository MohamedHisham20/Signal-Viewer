import os
import requests
from dotenv import load_dotenv
import time
import random

from PySide6.QtCore import QThread
from PySide6.QtCore import Signal as QTSignal


class WeatherDataFetcher(QThread):
    weather_data_fetched = QTSignal(float, float)

    def __init__(self):
        super().__init__()
        self.Gaza_lat = 31.4
        self.Gaza_lon = 34.3
        self.Fukuoka_lat = 33.6
        self.Fukuoka_lon = 130.4
        self.start_time = None

    def run(self):
        load_dotenv()
        api_key = os.getenv('OPENWEATHER_API_KEY')

        if not api_key:
            raise Exception("API key not found. Set it in a .env file or as an environment variable.")

        url = f"http://api.openweathermap.org/data/2.5/weather?lat={self.Gaza_lat}&lon={self.Gaza_lon}&appid={api_key}&units=metric"
        # Data in this api is updated around every 10 minutes

        while True:
            response = requests.get(url)
            weather_data = response.json()
            if self.start_time is None:
                self.start_time = time.time()
                elapsed_time = 0
            else:
                elapsed_time = time.time() - self.start_time

            if response.status_code == 200:
                wind_speed = weather_data["wind"]["speed"]

                adjustment_factor = random.uniform(0.9, 1.1)
                adjusted_wind_speed = wind_speed * adjustment_factor

                self.weather_data_fetched.emit(adjusted_wind_speed, elapsed_time)
            else:
                print("Failed to retrieve weather data:", weather_data.get("message", "Unknown error"))

            time.sleep(1)  # every n seconds

    def stop(self):
        self.terminate()
