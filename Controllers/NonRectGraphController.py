import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import skrf as rf  # Smith chart plotting


class SmithChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.plot_smith_chart()

    def plot_smith_chart(self):
        ax = self.figure.add_subplot(111)

        # Generate an example network for plotting (50 ohms reference impedance)
        network = rf.Network('example.s1p')  # You can load your own S-parameters here
        network.plot_s_smith(ax=ax)

        self.canvas.draw()


class PhasePortraitWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.plot_phase_portrait()

    def plot_phase_portrait(self):
        ax = self.figure.add_subplot(111)

        # Simulate a simple harmonic oscillator for phase portrait (e.g., pendulum)
        t = np.linspace(0, 10, 1000)
        x = np.sin(t)
        v = np.cos(t)

        ax.plot(x, v)

        ax.set_xlabel("Position")
        ax.set_ylabel("Velocity")
        ax.set_title("Phase Portrait (Simple Harmonic Oscillator)")
        self.canvas.draw()


class RadarDisplayWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.plot_radar_display()

    def plot_radar_display(self):
        ax = self.figure.add_subplot(111, projection='polar')

        # Simulating radar data
        theta = np.linspace(0, 2 * np.pi, 500)
        r = np.random.random(500) * 10  # Simulated distances

        ax.scatter(theta, r, c='green', marker='o')  # Radar points

        ax.set_title("Radar Display (PPI)")
        ax.set_ylim(0, 10)
        self.canvas.draw()


class PolarGraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create the layout
        layout = QVBoxLayout()

        # Create a figure
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Add the canvas to the layout
        layout.addWidget(self.canvas)

        # Set the layout for the widget
        self.setLayout(layout)

        # Call the method to plot the polar graph
        self.plot_polar()

    def plot_polar(self):
        # Create a polar subplot
        ax = self.figure.add_subplot(111, projection='polar')

        # Generate data for the polar plot
        theta = np.linspace(0, 2 * np.pi, 100)
        r = np.abs(np.sin(2 * theta))

        # Plot the data
        ax.plot(theta, r)

        # Set title
        ax.set_title('Polar Graph Example in PyQt5', va='bottom')

        # Redraw the canvas to display the plot
        self.canvas.draw()


# create class for spiral graph
class SpiralGraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create the layout
        layout = QVBoxLayout()

        # Create a figure
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Add the canvas to the layout
        layout.addWidget(self.canvas)

        # Set the layout for the widget
        self.setLayout(layout)

        # Call the method to plot the polar graph
        self.plot_spiral()

    def plot_spiral(self):
        # Create a polar subplot
        ax = self.figure.add_subplot(111, projection='polar')

        # Generate data for the polar plot
        theta = np.linspace(0, 10 * np.pi, 1000)
        r = theta

        # Plot the data
        ax.plot(theta, r)

        # Set title
        ax.set_title('Spiral Graph Example in PyQt5', va='bottom')

        # Redraw the canvas to display the plot
        self.canvas.draw()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ################# Polar Graph #################
        # # Set the window title
        # self.setWindowTitle("Polar Graph in PyQt5")
        #
        # # Create the central widget
        # central_widget = PolarGraphWidget(self)
        #
        # # Set the central widget
        # self.setCentralWidget(central_widget)

        ################# Spiral Graph #################
        # # Create the spiral widget
        # spiral_widget = SpiralGraphWidget(self)
        #
        # # Set the central widget
        # self.setCentralWidget(spiral_widget)
        #
        # # Set the window title
        # self.setWindowTitle("Spiral Graph in PyQt5")

        ################# Smith Chart #################
        # # Create the smith chart widget
        # smith_widget = SmithChartWidget(self)
        #
        # # Set the central widget
        # self.setCentralWidget(smith_widget)
        #
        # # Set the window title
        # self.setWindowTitle("Smith Chart in PyQt5")

        ################# Phase Portrait #################
        # # Create the phase portrait widget
        # phase_portrait_widget = PhasePortraitWidget(self)
        #
        # # Set the central widget
        # self.setCentralWidget(phase_portrait_widget)
        #
        # # Set the window title
        # self.setWindowTitle("Phase Portrait in PyQt5")

        ################# Radar Display #################
        # Create the radar display widget
        radar_display_widget = RadarDisplayWidget(self)

        # Set the central widget
        self.setCentralWidget(radar_display_widget)

        # Set the window title
        self.setWindowTitle("Radar Display in PyQt5")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create the main window and show it
    main_window = MainWindow()
    main_window.show()

    # Start the Qt event loop
    sys.exit(app.exec_())
