from PySide6.QtWidgets import QMainWindow, QApplication
import sys

from Signal import Signal
from WeatherDataFetcher import WeatherDataFetcher


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.weather_fetcher = WeatherDataFetcher()
        self.weather_fetcher.weather_data_fetched.connect(self.update_points_from_api)
        self.weather_fetcher.start()  # call this when the "connect to api" button is clicked

        # A signal to hold the api data, also initialized when the "connect to api" button is clicked
        self.wind_speed_signal = Signal(label="Wind Speed Signal")

        # How will the connection with the graph look like, will points be passed to the graph directly without
        # referencing the "api signal" object if so, 2 problems might arise: how will the graph know which signal to
        # add the point to, and what will happen if multiple graphs connect to the api
        #
        # Another approach might be to update the signal from the list of signals, and keep a list of all channels
        # that use the api signal to update their plots a problem with this might arise when signals are switched
        # from a graph to another

    def update_points_from_api(self, wind_speed, time):
        # Choose from the weather data what you need, temperature, humidity, wind speed...
        # Also save the signal data to the signals list
        # Loop through channels containing the api signal, and either append a point to be plotted,
        # or repass the api signal
        self.wind_speed_signal.append_point(time, wind_speed)
        print("Wind Speed: ", wind_speed, "m/s, Time: ", time, "seconds")

    # Use this to stop the thread when the window is closed
    def closeEvent(self, event):
        self.weather_fetcher.stop()
        self.weather_fetcher.quit()
        event.accept()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
