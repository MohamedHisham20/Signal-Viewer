import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import skrf as rf  # Smith chart plotting
import pyqtgraph as pg  # Dynamic plotting


class SmithChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.graph_widget = pg.PlotWidget()
        layout.addWidget(self.graph_widget)
        self.setLayout(layout)

        # Load the S1P file
        self.network = rf.Network('example.s1p')
        self.s11 = self.network.s[:, 0, 0]  # Extract S11 parameter

        # Set up the graph: limit the axis ranges, labels, etc.
        self.graph_widget.setXRange(-1.5, 1.5)
        self.graph_widget.setYRange(-1.5, 1.5)
        self.graph_widget.setTitle("Dynamic Smith Chart")
        self.graph_widget.setLabel('left', 'Imaginary')
        self.graph_widget.setLabel('bottom', 'Real')

        # Prepare for dynamic plotting
        self.ptr = 0  # Pointer to the current point
        pen = pg.mkPen(color='r', width=2, style=pg.QtCore.Qt.DashLine)
        self.plot_data = self.graph_widget.plot([], [], pen=pen, symbol='o', symbolBrush='b')

        # Start a timer to update the graph dynamically
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(200)  # Update every 200 ms

    def update_plot(self):
        """Update the graph by adding one point at a time."""
        if self.ptr < len(self.s11):
            real_part = np.real(self.s11[:self.ptr + 1])
            imag_part = np.imag(self.s11[:self.ptr + 1])

            # Update the plot data
            self.plot_data.setData(real_part, imag_part)
            self.ptr += 1
        else:
            self.timer.stop()  # Stop the timer once all points are plotted


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
class DynamicSpiralGraph(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.graph_widget = pg.PlotWidget()
        layout.addWidget(self.graph_widget)
        self.setLayout(layout)

        # Generate spiral data
        self.theta = np.linspace(0, 10 * np.pi, 1000)  # Angle from 0 to 10π
        self.r = np.linspace(0, 10, 1000)  # Radius increasing from 0 to 10

        # Convert polar to Cartesian coordinates
        self.x = self.r * np.cos(self.theta)
        self.y = self.r * np.sin(self.theta)

        # Initialize plot
        self.spiral_data = self.graph_widget.plot([], [], pen=pg.mkPen('b', width=2))

        # Counter for dynamic drawing
        self.ptr = 0

        # Set up timer for dynamic updates
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(50)  # Update every 50 ms

    def update_plot(self):
        """Update the graph by adding one point at a time."""
        if self.ptr < len(self.x):
            self.spiral_data.setData(self.x[:self.ptr], self.y[:self.ptr])
            self.ptr += 10  # Increment the pointer to gradually draw the spiral
        else:
            self.timer.stop()  # Stop the timer when the plot is fully drawn

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
        # spiral_widget = DynamicSpiralGraph(self)
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
        # Create the phase portrait widget
        phase_portrait_widget = PhasePortraitWidget(self)

        # Set the central widget
        self.setCentralWidget(phase_portrait_widget)

        # Set the window title
        self.setWindowTitle("Phase Portrait in PyQt5")

        ################# Radar Display #################
        # # Create the radar display widget
        # radar_display_widget = RadarDisplayWidget(self)
        #
        # # Set the central widget
        # self.setCentralWidget(radar_display_widget)
        #
        # # Set the window title
        # self.setWindowTitle("Radar Display in PyQt5")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create the main window and show it
    main_window = MainWindow()
    main_window.show()

    # Start the Qt event loop
    sys.exit(app.exec_())
