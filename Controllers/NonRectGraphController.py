import numpy as np
import pandas as pd
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QScrollBar, QHBoxLayout, QFileDialog, QFrame

from GUI import Signal


class RadarGraph(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setMinimumSize(400, 400)
        self.radius = 100  # Radar circle radius (relative value, actual will scale)
        self.data = np.array([])  # To hold the loaded signal data in angles (0 to 360 degrees)
        self.radar_angle = 0  # The starting angle for the radar line
        self.radar_speed = 5  # Speed of the radar line rotation
        self.hit_points = []  # Points that have been hit by radar (persist)
        self.remaining_points = []  # Points still visible, disappear when radar passes
        self.prev_hit_point = None  # Previous point to draw lines

        # Start a timer to update the radar sweep dynamically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_radar)
        self.timer.start(50)  # Update every 50ms

    def load_data_from_csv(self, file_path):
        """Load signal data from a CSV file."""
        try:
            data = pd.read_csv(file_path)
            # Scale the signal values to fit within 360 degrees
            scaled_data = (data["hart"].values - np.min(data["hart"].values)) / (
                        np.max(data["hart"].values) - np.min(data["hart"].values)) * 360
            self.data = scaled_data
            self.remaining_points = [(i, angle) for i, angle in enumerate(self.data)]
        except Exception as e:
            print(f"Error loading file: {e}")

    def load_y_axis(self, data, y_axis_header):
        """Load signal data from a CSV file."""
        try:
            # Scale the signal values to fit within 360 degrees (the data is array of y values)
            scaled_data = (data - np.min(data)) / (np.max(data) - np.min(data)) * 360
            self.data = scaled_data
            self.remaining_points = [(i, angle) for i, angle in enumerate(self.data)]
        except Exception as e:
            print(f"Error loading file: {e}")

    def update_radar(self):
        """Update the radar sweep and check for 'hits'."""
        # Increment the radar angle
        self.radar_angle += self.radar_speed
        if self.radar_angle >= 360:
            self.radar_angle = 0
            self.hit_points.clear()
            self.prev_hit_point = None
            self.remaining_points = [(i, angle) for i, angle in enumerate(self.data)]

        self.update_hit_points()
        self.update()

    def update_hit_points(self):
        """Update the hit points based on radar angle and mark points as hit."""
        to_remove = []
        for i, angle in self.remaining_points:
            if angle <= self.radar_angle:
                # Random distance within the radar circle (scaled)
                distance = np.random.randint(30, self.radius)
                scaled_distance = distance * (min(self.width(), self.height()) / 250)  # Scale with window size
                x = self.width() // 2 + scaled_distance * np.cos(np.radians(angle))
                y = self.height() // 2 - scaled_distance * np.sin(np.radians(angle))
                self.hit_points.append((int(x), int(y)))
                to_remove.append((i, angle))

                # Save the last point to draw lines
                if len(self.hit_points) > 1:
                    self.prev_hit_point = self.hit_points[-2]

        # Remove points that have been hit
        self.remaining_points = [p for p in self.remaining_points if p not in to_remove]

    def scroll_radar_angle(self, angle):
        """Set radar angle manually based on scrollbar and update hit points accordingly."""
        self.radar_angle = angle

        # Create a list of points that should be hit (at or before radar_angle)
        to_hit = []
        still_remaining = []

        # Update hit points based on radar angle (add points that should now be hit)
        for i, point_angle in self.remaining_points:
            if point_angle <= self.radar_angle:  # Points at or before radar angle should be hit
                to_hit.append((i, point_angle))
            else:
                still_remaining.append((i, point_angle))  # Points after the radar angle remain

        # Add new points to the hit points
        for i, point_angle in to_hit:
            # Calculate position for the hit points
            distance = np.random.randint(30, self.radius)
            scaled_distance = distance * (min(self.width(), self.height()) / 250)  # Scale with window size
            x = self.width() // 2 + scaled_distance * np.cos(np.radians(point_angle))
            y = self.height() // 2 - scaled_distance * np.sin(np.radians(point_angle))

            self.hit_points.append((int(x), int(y)))

        # Update remaining points
        self.remaining_points = still_remaining

        # Remove points that are after the radar angle when scrolling back
        for point in self.hit_points[:]:
            # Convert the x and y coordinates back to angle (reverse calculation)
            center_x = self.width() // 2
            center_y = self.height() // 2
            dx = point[0] - center_x
            dy = center_y - point[1]
            point_angle = np.degrees(np.arctan2(dy, dx)) % 360

            if point_angle > self.radar_angle:
                self.hit_points.remove(point)

                self.remaining_points.append((1, point_angle))

        self.update()

    def paintEvent(self, event):
        """Draw the radar, dynamic points, and lines between points."""
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)

        # Set the center and radius based on window size
        center_x = self.width() // 2
        center_y = self.height() // 2
        radar_radius = min(center_x, center_y) - 20  # Adjusted radius to fit the window
        self.radius = radar_radius

        # Draw the radar base (a circle)
        qp.setPen(QPen(Qt.black, 2))
        qp.setBrush(Qt.black)
        qp.drawEllipse(center_x - radar_radius, center_y - radar_radius, radar_radius * 2,
                       radar_radius * 2)  # Radar base

        # Draw the radar sweep (rotating line)
        qp.setPen(QPen(Qt.red, 2))

        # Calculate the end of the radar sweep based on the current angle
        x = center_x + radar_radius * np.cos(np.radians(self.radar_angle))
        y = center_y - radar_radius * np.sin(np.radians(self.radar_angle))
        qp.drawLine(center_x, center_y, int(x), int(y))

        # Draw lines between consecutive hit points
        if len(self.hit_points) > 1:
            qp.setPen(QPen(Qt.blue, 2))
            for i in range(1, len(self.hit_points)):
                qp.drawLine(self.hit_points[i - 1][0], self.hit_points[i - 1][1], self.hit_points[i][0],
                            self.hit_points[i][1])

        # Draw the radar target points that have been hit
        qp.setPen(QPen(Qt.green, 6))
        for point in self.hit_points:
            qp.drawPoint(*point)


class NonRectGraph(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create radar graph widget
        self.radar_widget = RadarGraph()

        # Create play and pause buttons
        self.play_button = QPushButton("Play")
        self.pause_button = QPushButton("Pause")
        self.play_button.clicked.connect(self.play_radar)
        self.pause_button.clicked.connect(self.pause_radar)

        # Create a button to load CSV
        self.load_csv_button = QPushButton("Load CSV")
        self.load_csv_button.clicked.connect(self.load_csv)

        #create button to load y axis
        self.load_y_axis_button = QPushButton("Load Y Axis")
        self.load_y_axis_button.clicked.connect(self.signal_to_nonRect)

        # Create a horizontal scrollbar
        self.scroll_bar = QScrollBar(Qt.Horizontal)
        self.scroll_bar.setMinimum(0)
        self.scroll_bar.setMaximum(360)
        self.scroll_bar.setValue(0)
        self.scroll_bar.sliderMoved.connect(self.scroll_radar)

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.radar_widget)

        # Add buttons and scrollbar
        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.play_button)
        controls_layout.addWidget(self.pause_button)
        controls_layout.addWidget(self.load_csv_button)
        controls_layout.addWidget(self.load_y_axis_button)
        layout.addLayout(controls_layout)
        layout.addWidget(self.scroll_bar)

        self.setLayout(layout)

    def play_radar(self):
        """Resume radar rotation."""
        self.radar_widget.timer.start(50)

    def pause_radar(self):
        """Pause radar rotation."""
        self.radar_widget.timer.stop()

    def scroll_radar(self, value):
        """Move radar sweep based on scrollbar."""
        self.radar_widget.scroll_radar_angle(value)

    def load_csv(self):
        """Open a file dialog to load CSV data."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Load CSV", "", "CSV Files (*.csv)")
        if file_path:
            self.radar_widget.load_data_from_csv(file_path)

    def signal_to_nonRect(self, signal: Signal):
        """" get a signal object passed from the main window and load the y axis"""
        y_values = signal.get_y_values()
        self.radar_widget.load_y_axis(y_values, signal.label)

