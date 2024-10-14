from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QSlider, QLabel, QComboBox, QCheckBox, QFrame
from PySide6.QtCore import Qt
from pyqtgraph import PlotWidget


class GlueSignalsPopup(QDialog):
    def __init__(self, signal1, signal2, glue_function, report_function, parent=None):
        super().__init__(parent)
        self.signal1 = signal1
        self.signal2 = signal2
        self.adjusted_signal1 = signal1
        self.adjusted_signal2 = signal2
        self.glue_function = glue_function
        self.report_function = report_function
        self.slider1_initial_value = None
        self.slider2_initial_value = None

        self.interpolation_methods = {
            "Linear": 1,
            "Quadratic": 2,
            "Cubic": 3,
            "Quartic": 4,
            "Quintic": 5
        }

        self.setWindowTitle("Glue Signals")
        self.setGeometry(300, 300, 600, 550)

        # Layout
        layout = QVBoxLayout()

        # Plot Widget
        self.plot_widget = PlotWidget(self)
        layout.addWidget(self.plot_widget)
        layout.setStretch(0, 2)

        self.plot_signals(self.signal1, self.signal2)

        self.slider1 = QSlider(self)
        self.slider2 = QSlider(self)

        self.init_slider_values()

        self.slider1.setOrientation(Qt.Horizontal)
        self.slider1.valueChanged.connect(self.update_plot)

        self.slider2.setOrientation(Qt.Horizontal)
        self.slider2.valueChanged.connect(self.update_plot)

        layout.addWidget(QLabel("Adjust Signal 1"))
        layout.addWidget(self.slider1)

        layout.addWidget(QLabel("Adjust Signal 2"))
        layout.addWidget(self.slider2)

        layout.addWidget(QLabel("Select Interpolation Order"))
        self.interpolation_order_combo = QComboBox(self)
        self.interpolation_order_combo.addItems(self.interpolation_methods.keys())
        layout.addWidget(self.interpolation_order_combo)

        divider = QFrame(self)
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        layout.addWidget(divider)

        self.generate_report_checkbox = QCheckBox("Automatically Generate Report")
        layout.addWidget(self.generate_report_checkbox)

        self.glue_button = QPushButton("Glue Signals")
        self.glue_button.clicked.connect(self.glue_signals)
        layout.addWidget(self.glue_button)

        self.setLayout(layout)
        self.setModal(True)

    def init_slider_values(self):
        x_axis_range = self.plot_widget.getAxis('bottom').range
        signal1_mid = (self.signal1[0][0] + self.signal1[-1][0]) / 2
        signal2_mid = (self.signal2[0][0] + self.signal2[-1][0]) / 2
        self.slider1_initial_value = (signal1_mid - x_axis_range[0]) / (x_axis_range[1] - x_axis_range[0]) * 100
        self.slider2_initial_value = (signal2_mid - x_axis_range[0]) / (x_axis_range[1] - x_axis_range[0]) * 100
        self.slider1.setValue(self.slider1_initial_value)
        self.slider2.setValue(self.slider2_initial_value)

    def plot_signals(self, signal1, signal2):
        self.plot_widget.clear()
        signal1_x, signal1_y = zip(*signal1)
        signal2_x, signal2_y = zip(*signal2)
        self.plot_widget.plot(signal1_x, signal1_y, pen='r')
        self.plot_widget.plot(signal2_x, signal2_y, pen='b')

    def update_plot(self):
        offset1 = self.slider1.value()
        offset2 = self.slider2.value()
        self.adjusted_signal1 = self.adjust_signal(self.signal1, offset1 - self.slider1_initial_value)
        self.adjusted_signal2 = self.adjust_signal(self.signal2, offset2 - self.slider2_initial_value)

        self.plot_signals(self.adjusted_signal1, self.adjusted_signal2)

    def adjust_signal(self, signal, offset):
        return [(x + offset * 0.1, y) for x, y in signal]

    def glue_signals(self):
        interpolation_order = self.interpolation_methods[self.interpolation_order_combo.currentText()]

        self.glue_function(self.adjusted_signal1, self.adjusted_signal2, interpolation_order)

        if self.generate_report_checkbox.isChecked():
            self.report_function(self.adjusted_signal1, self.adjusted_signal2, interpolation_order)

        self.accept()