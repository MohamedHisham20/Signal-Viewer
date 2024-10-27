import numpy as np
import pandas as pd

from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QPainter, QPen, QFont, QBrush, QColor
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QScrollBar, QHBoxLayout, QFileDialog, QFrame




class RadarGraph(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.radius = 100  # Radar circle radius (relative value, actual will scale)
        self.data = np.array([])  # To hold the loaded signal data in angles (0 to 360 degrees)
        self.radar_angle = 0  # The starting angle for the radar line
        self.radar_speed = 5  # Speed of the radar line rotation
        self.hit_points = []  # Stores (i, angle) instead of (x, y)
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
            self.remaining_points = [(i, angle) for i, angle in enumerate(np.linspace(0, 360, len(self.data)))]
        except Exception as e:
            print(f"Error loading file: {e}")

    def load_y_axis(self, data, y_axis_header):
        """Load signal data from a CSV file."""
        try:
            # Scale the signal values to fit within 360 degrees (the data is array of y values)
            scaled_data = (data - np.min(data)) / (np.max(data) - np.min(data)) * 360
            self.data = scaled_data
            self.remaining_points = [(i, angle) for i, angle in enumerate(np.linspace(0, 360, len(self.data)))]
        except Exception as e:
            print(f"Error loading file: {e}")

    def update_radar(self):
        """Update the radar sweep and check for 'hits'."""
        # Increment the radar angle
        self.radar_angle += self.radar_speed
        # Reset the radar angle if it exceeds 360 degrees
        if self.radar_angle >= 360:
            self.start_over()
        else:
            self.update_hit_points()  # Update the hit points based on the current radar angle
            self.update()  # Trigger a repaint

    def start_over(self):
        self.radar_angle = 0
        self.hit_points.clear()  # Clear only hit points
        self.prev_hit_point = None
        # Here you might want to reset remaining points or ensure they still represent the current data
        self.remaining_points = [(i, angle) for i, angle in enumerate(np.linspace(0, 360, len(self.data)))]
        self.update_hit_points()  # Update the hit points based on the current radar angle
        self.update()  # Trigger a repaint

    def update_hit_points(self):
        """Update the hit points based on radar angle and mark points as hit."""
        to_remove = []
        for i, angle in self.remaining_points:
            if angle <= self.radar_angle:
                # Hit points now store (i, angle) instead of x, y
                self.hit_points.append((i, angle))
                to_remove.append((i, angle))

        # Remove points that have been hit
        self.remaining_points = [p for p in self.remaining_points if p not in to_remove]

    def scroll_radar_angle(self, angle):
        """Set radar angle manually based on scrollbar and update hit points accordingly."""
        self.radar_angle = angle

        to_hit = []
        still_remaining = []

        # Update hit points based on radar angle (add points that should now be hit)
        for i, point_angle in self.remaining_points:
            if point_angle <= self.radar_angle:  # Points at or before radar angle should be hit
                to_hit.append((i, point_angle))
            else:
                still_remaining.append((i, point_angle))  # Points after the radar angle remain

        # Add new points to the hit points
        self.hit_points.extend(to_hit)

        # Update remaining points
        self.remaining_points = still_remaining

        # Remove points that are after the radar angle when scrolling back
        for p in self.hit_points[:]:
            if p[1] > self.radar_angle:
                self.hit_points.remove(p)
                self.remaining_points.append(p)

        self.update()

    def calculate_xy(self, i, angle):
        """Calculate x, y coordinates for a point (i, angle) based on radar dimensions."""
        # Normalize the y value to be between 0 and 1
        normalized_y = (self.data[i] - np.min(self.data)) / (np.max(self.data) - np.min(self.data))
        distance = self.radius / 1.3 * normalized_y  # Scale based on the normalized data
        scaled_distance = distance * (min(self.width(), self.height()) / 250)  # Scale with window size
        x = self.width() // 2 + scaled_distance * np.cos(np.radians(angle))
        y = self.height() // 2 - scaled_distance * np.sin(np.radians(angle))
        return int(x), int(y)

    def paintEvent(self, event):
        """Draw the radar, dynamic points, lines between points, and axis with angle labels."""
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)

        center_x = self.width() // 2
        center_y = self.height() // 2
        radar_radius = min(center_x, center_y) - 20  # Adjusted radius to fit the window
        self.radius = radar_radius

        # Draw the radar base (a circle)

        # Set the brush for filling the circle with gray color
        qp.setBrush(QBrush(Qt.gray))  # Gray fill

        # Set the pen for drawing the border of the circle with black color
        qp.setPen(QPen(Qt.black, 2))  # Black border with 2-pixel width

        qp.drawEllipse(center_x - radar_radius, center_y - radar_radius, radar_radius * 2, radar_radius * 2)

        # Draw the radar axes (radial lines) and angle labels
        gray_color = QColor(128, 128, 128, 128)  # RGB values for gray and alpha value for transparency
        qp.setPen(QPen(gray_color, 2))

        # Draw concentric circles
        for i in reversed(range(1, 4)):  # Adjust the range for more or fewer circles
            radius = radar_radius / 4 * i  # Calculate the radius for each circle
            qp.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)

        # Draw the radar sweep (rotating line)
        qp.setPen(QPen(Qt.red, 2))
        x = center_x + radar_radius * np.cos(np.radians(self.radar_angle))
        y = center_y - radar_radius * np.sin(np.radians(self.radar_angle))
        qp.drawLine(center_x, center_y, int(x), int(y))

        # Draw the axes (radial lines) and angle labels
        qp.setPen(QPen(gray_color, 1))
        font = QFont("Arial", 8)
        qp.setFont(font)

        for angle in range(0, 360, 30):  # Draw axes every 30 degrees
            # Calculate the end point of the axis line
            x_axis = center_x + radar_radius * np.cos(np.radians(angle))
            y_axis = center_y - radar_radius * np.sin(np.radians(angle))
            qp.drawLine(center_x, center_y, int(x_axis), int(y_axis))

            # Draw the angle labels at the end of each axis
            label_x = center_x + (radar_radius + 15) * np.cos(
                np.radians(angle))  # Adjust the position slightly for the label
            label_y = center_y - (radar_radius + 15) * np.sin(np.radians(angle))
            qp.drawText(int(label_x) - 10, int(label_y) + 5, f"{angle}°")

        # Draw lines between consecutive hit points
        if len(self.hit_points) > 1:
            qp.setPen(QPen(Qt.blue, 2))
            for i in range(1, len(self.hit_points)):
                x1, y1 = self.calculate_xy(*self.hit_points[i - 1])
                x2, y2 = self.calculate_xy(*self.hit_points[i])
                qp.drawLine(x1, y1, x2, y2)

        # Draw the radar target points that have been hit
        qp.setPen(QPen(Qt.green, 6))
        for point in self.hit_points:
            x, y = self.calculate_xy(*point)
            qp.drawPoint(x, y)


class NonRectGraph(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.radar_widget = RadarGraph()
        
        self.play_button = QPushButton("Play")
        self.pause_button = QPushButton("Pause")
        self.play_button.clicked.connect(self.play_radar)
        self.pause_button.clicked.connect(self.pause_radar)

        self.rewind_button = QPushButton("Rewind")
        self.rewind_button.clicked.connect(self.rewind_radar)

        self.load_csv_button = QPushButton("Load CSV")
        self.load_csv_button.clicked.connect(self.load_csv)

        self.load_y_axis_button = QPushButton("Load Y Axis")
        self.load_y_axis_button.clicked.connect(self.signal_to_nonRect)

        self.scroll_panning = QScrollBar(Qt.Horizontal)
        self.scroll_panning.setMinimum(0)
        self.scroll_panning.setMaximum(360)
        self.scroll_panning.setValue(0)
        self.scroll_panning.sliderMoved.connect(self.scroll_radar)

        self.scroll_speed = QScrollBar(Qt.Horizontal)
        self.scroll_speed.setMinimum(1)
        self.scroll_speed.setMaximum(30)
        self.scroll_speed.setValue(1)
        self.scroll_speed.sliderMoved.connect(self.change_speed)
        self.isRunning = False
        layout = QVBoxLayout()
        layout.addWidget(self.radar_widget)

        # controls_layout = QHBoxLayout()
        # controls_layout.addWidget(self.play_button)
        # controls_layout.addWidget(self.pause_button)
        # # controls_layout.addWidget(self.load_csv_button)
        # controls_layout.addWidget(self.rewind_button)
        # controls_layout.addWidget(self.load_y_axis_button)
        # layout.addLayout(controls_layout)
        # layout.addWidget(self.scroll_panning)
        # layout.addWidget(self.scroll_speed)

        self.setLayout(layout)

    def play_radar(self):
        self.radar_widget.timer.start(50)
        self.isRunning = True

    def pause_radar(self):
        self.radar_widget.timer.stop()
        self.isRunning = False

    def rewind_radar(self):
        self.radar_widget.start_over()

    def scroll_radar(self, value):
        self.radar_widget.scroll_radar_angle(value)

    def change_speed(self, value):
        self.radar_widget.radar_speed = value

    def load_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Load CSV", "", "CSV Files (*.csv)")
        if file_path:
            self.radar_widget.load_data_from_csv(file_path)

    def signal_to_nonRect(self, signal):
        self.clear()
        y_values = signal.get_y_values()
        self.radar_widget.load_y_axis(y_values, signal.label)
    def clear(self):
        self.radar_widget.start_over()
        self.radar_widget.remaining_points = []
        self.radar_widget.hit_points = []
        self.radar_widget.prev_hit_point = None
        self.radar_widget.data = np.array([])
        self.radar_widget.update()
