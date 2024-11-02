import copy
from Graph import Graph, Plot
from Signal import Signal
import pandas as pd
import numpy as np
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QVBoxLayout , QHBoxLayout, QPushButton , QLabel
from PySide6.QtGui import QFont
import pyqtgraph as pg
import sys
from styleSheet import styleSheet
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QComboBox, QLabel
from PySide6.QtCore import QTimer
from scipy.interpolate import interp1d
def glue_signals(signal1: Signal, signal2: Signal, interpolation_degree='linear'):
    signal1_df = pd.DataFrame(signal1.data_pnts, columns=['x', 'y'])
    signal2_df = pd.DataFrame(signal2.data_pnts, columns=['x', 'y'])

    # Handle NaN values
    signal1_df.dropna(inplace=True)
    signal2_df.dropna(inplace=True)

    # Handle single point signals
    if len(signal1_df) <= 1 and len(signal2_df) <= 1:
        result = pd.concat([signal1_df, signal2_df]).sort_values(by='x').reset_index(drop=True)
        return Signal.from_pd_df(result)

    if len(signal1_df) <= 1:
        result = signal2_df.reset_index(drop=True)
        return Signal.from_pd_df(result)
    if len(signal2_df) <= 1:
        result = signal1_df.reset_index(drop=True)
        return Signal.from_pd_df(result)

    overlap_start = max(signal1_df['x'].min(), signal2_df['x'].min())
    overlap_end = min(signal1_df['x'].max(), signal2_df['x'].max())

    if overlap_start < overlap_end:  # If there's an overlap
        return combine_overlap(signal1_df, signal2_df)
    else:
        return combine_gap(signal1_df, signal2_df, interpolation_degree)


def combine_overlap(signal1_df: pd.DataFrame, signal2_df: pd.DataFrame):
    overlap_start = max(signal1_df['x'].min(), signal2_df['x'].min())
    overlap_end = min(signal1_df['x'].max(), signal2_df['x'].max())

    number_of_points = max(10, int((overlap_end - overlap_start)))  # change this to dynamically reflect the overlap duration

    interpolation_points = np.linspace(overlap_start, overlap_end, number_of_points)

    interpolated_signal1 = np.interp(interpolation_points, signal1_df['x'], signal1_df['y'], left=np.nan, right=np.nan)
    interpolated_signal2 = np.interp(interpolation_points, signal2_df['x'], signal2_df['y'], left=np.nan, right=np.nan)

    valid_mask = np.isfinite(interpolated_signal1) & np.isfinite(interpolated_signal2)
    average_y = np.full(interpolation_points.shape, np.nan)
    average_y[valid_mask] = (interpolated_signal1[valid_mask] + interpolated_signal2[valid_mask]) / 2

    before_overlap_signal1 = signal1_df[signal1_df['x'] < overlap_start]
    before_overlap_signal2 = signal2_df[signal2_df['x'] < overlap_start]

    after_overlap_signal1 = signal1_df[signal1_df['x'] > overlap_end]
    after_overlap_signal2 = signal2_df[signal2_df['x'] > overlap_end]

    result = pd.concat([
        before_overlap_signal1,
        before_overlap_signal2,
        pd.DataFrame({'x': interpolation_points, 'y': average_y}),
        after_overlap_signal1,
        after_overlap_signal2
    ])

    result = result.sort_values(by='x').reset_index(drop=True)
    return Signal.from_pd_df(result)


import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

def combine_gap(signal1_df: pd.DataFrame, signal2_df: pd.DataFrame, interpolation_degree):
    # Ensure signal1_df's maximum x is less than signal2_df's minimum x
    if signal1_df['x'].max() > signal2_df['x'].min():
        return combine_gap(signal2_df, signal1_df, interpolation_degree)

    gap_start = signal1_df['x'].max()
    gap_end = signal2_df['x'].min()

    # Ensure there is a gap
    if gap_start >= gap_end:
        return Signal.from_pd_df(pd.concat([signal1_df, signal2_df]).sort_values(by='x').reset_index(drop=True))

    # Define interpolators for the ends of signal1 and the start of signal2
    interp1 = interp1d(signal1_df['x'], signal1_df['y'], kind=interpolation_degree, fill_value="extrapolate")
    interp2 = interp1d(signal2_df['x'], signal2_df['y'], kind=interpolation_degree, fill_value="extrapolate")

    # Generate gap points
    number_of_points = max(10, int((gap_end - gap_start) * 10))  # Adjust number of points
    gap_x = np.linspace(gap_start, gap_end, number_of_points)
    if interpolation_degree in ['linear', 'nearest']:
        gap_x = gap_x[(gap_x >= signal1_df['x'].min()) & (gap_x <= signal1_df['x'].max()) & (gap_x >= signal2_df['x'].min()) & (gap_x <= signal2_df['x'].max())]

    # Interpolating values
    gap_y1 = interp1(gap_x)
    gap_y2 = interp2(gap_x)

    # Determine how to handle gap_y based on the interpolation degree
    if interpolation_degree in ['linear', 'nearest']:
        # For linear or nearest, use average of the interpolated values as-is
        gap_y = (gap_y1 + gap_y2) / 2
    else:
        # For other interpolation types, average and then normalize
        gap_y = (gap_y1 + gap_y2) / 2
        
        # Normalize gap_y to be between the min and max of the two signals
        combined_min = min(signal1_df['y'].min(), signal2_df['y'].min())
        combined_max = max(signal1_df['y'].max(), signal2_df['y'].max())

        # Normalize gap_y to [0, 1]
        gap_y_normalized = (gap_y - gap_y.min()) / (gap_y.max() - gap_y.min())

        # Scale normalized values to the combined range [combined_min, combined_max]
        gap_y = gap_y_normalized * (combined_max - combined_min) + combined_min
        gap_y = gap_y/2

    # Create DataFrame for the gap
    gap_df = pd.DataFrame({'x': gap_x, 'y': gap_y})

    # Combine signal1, gap, and signal2
    result = pd.concat([signal1_df, gap_df, signal2_df]).sort_values(by='x').reset_index(drop=True)

    return Signal.from_pd_df(result)


class GluePopUp(QWidget):
    def __init__(self, parent=None, signals: list[Signal] = None, ui=None):
        super().__init__(parent)
        self.ui = ui
        self.signals = copy.deepcopy(signals) if signals else []
        self.original_signals = signals
        self.signal1 = None
        self.signal2 = None
        self.interpolation_degree = 'linear'
        self.graph1 = Graph()
        self.graph2 = Graph()
        self.shift = 0
        self.init_ui()

    def init_ui(self):
        styleSheet(self)
        layout = QVBoxLayout()
        controls_layout = QHBoxLayout()
        self.combo_signal1 = QComboBox()
        self.combo_signal2 = QComboBox()
        self.combo_interpolation = QComboBox()
        self.shift_right = QPushButton("→")
        # ok cancel buttons
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        self.ok_cancel_layout = QHBoxLayout()
        self.ok_cancel_layout.addWidget(self.cancel_button)
        self.ok_cancel_layout.addWidget(self.ok_button)
        self.shift_right.setFont(QFont('Arial', weight=QFont.Bold, pointSize=12))
        self.shift_left = QPushButton("←")
        self.shift_left.setFont(QFont('Arial', weight=QFont.Bold, pointSize=12))
        self.shift_layout = QHBoxLayout()
        self.shift_layout.addWidget(self.shift_left)
        self.shift_layout.addWidget(self.shift_right)
        self.combo_signal1.addItems([signal.label for signal in self.signals])
        self.combo_signal2.addItems([signal.label for signal in self.signals])
        # self.combo_interpolation.addItems([str(i) for i in range(1, 6)])  # Adding interpolation degrees 1 to 5
        self.combo_interpolation.addItems(['linear', 'nearest', 'slinear', 'quadratic', 'cubic'])

        self.combo_signal1.currentIndexChanged.connect(self.update_signal1)
        self.combo_signal2.currentIndexChanged.connect(self.update_signal2)
        self.combo_interpolation.currentIndexChanged.connect(lambda index: self.set_interpolation_degree(self.combo_interpolation.currentText()))
        controls_layout.addWidget(QLabel("Select Signal 1:"))
        controls_layout.addWidget(self.combo_signal1)
        controls_layout.addWidget(QLabel("Select Signal 2:"))
        controls_layout.addWidget(self.combo_signal2)
        controls_layout.addWidget(QLabel("Interpolation Degree:"))
        controls_layout.addWidget(self.combo_interpolation)
        layout.addLayout(controls_layout)
        layout.addLayout(self.shift_layout)
        self.shift_right.pressed.connect(self.start_shift_right)
        self.shift_right.released.connect(self.stop_shift)
        self.shift_left.pressed.connect(self.start_shift_left)
        self.shift_left.released.connect(self.stop_shift)
        # self.shift_right.clicked.connect(lambda:self.set_shift(1))
        # self.shift_left.clicked.connect(lambda:self.set_shift(-1))
        layout.addWidget(self.graph1.plot_widget)
        layout.addWidget(self.graph2.plot_widget)

        self.setLayout(layout)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.cancel)

        #link the viewboxes of the two graphs
        self.graph1.plot_widget.getViewBox().sigXRangeChanged.connect(lambda: self.link_view(self.graph1.plot_widget.getViewBox(), self.graph2.plot_widget.getViewBox()))
        self.graph1.plot_widget.getViewBox().sigYRangeChanged.connect(lambda: self.link_view(self.graph1.plot_widget.getViewBox(), self.graph2.plot_widget.getViewBox()))
        self.graph2.plot_widget.getViewBox().sigXRangeChanged.connect(lambda: self.link_view(self.graph2.plot_widget.getViewBox(), self.graph1.plot_widget.getViewBox()))
        self.graph2.plot_widget.getViewBox().sigYRangeChanged.connect(lambda: self.link_view(self.graph2.plot_widget.getViewBox(), self.graph1.plot_widget.getViewBox()))
        layout.addLayout(self.ok_cancel_layout)
    def accept(self):
        Signal.glued_signal_counter += 1
        glued_signal = self.glue_signals()
        self.original_signals.append(glued_signal)

        self.ui.addsignalChannel1_combo.clear()
        self.ui.addsignalChannel2_combo.clear()
        self.ui.addsignalChannel1_combo.addItem("Choose Signal")
        self.ui.addsignalChannel2_combo.addItem("Choose Signal")
        self.ui.addsignalChannel1_combo.addItems([signal.label for signal in self.original_signals])
        self.ui.addsignalChannel2_combo.addItems([signal.label for signal in self.original_signals])
        self.close()
    def cancel(self):
        self.close()
    def start_shift_right(self):
        self.set_shift(1)
        self.shift_timer = self.startTimer(100)
        self.shift_direction = 0.1

    def start_shift_left(self):
        self.set_shift(-1)
        self.shift_timer = self.startTimer(100)
        self.shift_direction = -0.1

    def stop_shift(self):
        self.killTimer(self.shift_timer)
        self.update_interpolation()
        
    def link_view(self,source_viewbox, target_viewbox):
        # Sync x-axis range
        target_viewbox.setXRange(*source_viewbox.viewRange()[0], padding=0)
        # Sync y-axis range
        target_viewbox.setYRange(*source_viewbox.viewRange()[1], padding=0)

    def update_interpolation(self):
        if not self.signal2:
            return
        
        glued_signal = self.glue_signals()
        curve = pg.PlotDataItem([p[0] for p in glued_signal.data_pnts], [p[1] for p in glued_signal.data_pnts], pen='g')
        plot = Plot(curve, glued_signal, f'Glued{self.signal1.label} and {self.signal2.label}')
        self.graph2.plot_widget.clear()
        self.graph2.plots = []
        self.graph2.plots.append(plot)
        self.graph2.plot_widget.addItem(plot.plot)
        # self.graph2.plot_widget.setXRange(min([p[0] for p in glued_signal.data_pnts]), max([p[0] for p in glued_signal.data_pnts]))
        # self.graph2.plot_widget.setYRange(min([p[1] for p in glued_signal.data_pnts]), max([p[1] for p in glued_signal.data_pnts]))
        self.graph2.custom_viewbox.set_dynamic_limits(min([p[0] for p in glued_signal.data_pnts]), max([p[0] for p in glued_signal.data_pnts]), min([p[1] for p in glued_signal.data_pnts]), max([p[1] for p in glued_signal.data_pnts]))
        self.graph2.plots = [plot]

    def timerEvent(self, event):
        if self.signal2:
            shift_amount = self.shift_direction * (self.signal2.data_pnts[-1][0] - self.signal2.data_pnts[0][0])
            QTimer.singleShot(0, lambda: self.set_shift(shift_amount))


    def set_shift(self, shift):
        if not self.signal2:
            return
        self.signal2.data_pnts = [(p[0] + shift, p[1]) for p in self.signal2.data_pnts]
        self.graph1.plots[1].plot.setData([p[0] for p in self.signal2.data_pnts], [p[1] for p in self.signal2.data_pnts])
        self.update_limits()
    
    def remove_shift(self):
        if not self.signal2:
            return
        shift = self.signal2.data_pnts[0][0]
        self.signal2.data_pnts = [(p[0] - shift , p[1]) for p in self.signal2.data_pnts]
        if not self.signal2:
            return
        shift = self.signal1.data_pnts[0][0]
        self.signal1.data_pnts = [(p[0] - shift , p[1]) for p in self.signal1.data_pnts]


    def glue_signals(self):
        if self.signal1 and self.signal2:
            glued_signal = glue_signals(self.signal1, self.signal2, self.interpolation_degree)
            return glued_signal
        return None

    def set_signals(self, signal1: Signal, signal2: Signal):
        self.signal1 = signal1
        self.signal2 = signal2
        self.update_plots()

    def set_interpolation_degree(self, degree):
        self.interpolation_degree = degree
        self.update_interpolation()


    def update_plots(self):
        self.graph1.plot_widget.clear()
        self.graph1.plots = []
        self.graph2.plot_widget.clear()
        self.graph2.plots = []
        if self.signal1:
            curve = pg.PlotDataItem([p[0] for p in self.signal1.data_pnts], [p[1] for p in self.signal1.data_pnts], pen='b')
            plot = Plot(curve, self.signal1,self.signal1.label)
            self.graph1.plots.append(plot)
            self.graph1.plot_widget.addItem(plot.plot)
        if self.signal2:
            curve = pg.PlotDataItem([p[0] for p in self.signal2.data_pnts], [p[1] for p in self.signal2.data_pnts], pen='r')
            plot = Plot(curve, self.signal2,self.signal2.label)
            self.graph1.plots.append(plot)
            self.graph1.plot_widget.addItem(plot.plot)
        
        self.set_shift(self.signal1.data_pnts[-1][0] - self.signal1.data_pnts[0][0])
        self.update_limits()
        self.update_interpolation()

        
    def update_limits(self):
        min_x = min(self.signal1.data_pnts[0][0], self.signal2.data_pnts[0][0])
        max_x = max(self.signal1.data_pnts[-1][0], self.signal2.data_pnts[-1][0])
        # self.graph1.plot_widget.setXRange(min_x, max_x)
        min_y = min(min([p[1] for p in self.signal1.data_pnts]), min([p[1] for p in self.signal2.data_pnts]))
        max_y = max(max([p[1] for p in self.signal1.data_pnts]), max([p[1] for p in self.signal2.data_pnts]))
        # self.graph1.plot_widget.setYRange(min_y, max_y)
        self.graph1.custom_viewbox.set_dynamic_limits(min_x, max_x, min_y, max_y)
    def update_signal1(self, index):
        self.signal1 = copy.deepcopy(self.signals[index])
        self.remove_shift()
        self.update_plots()

    def update_signal2(self, index):
        self.signal2 = copy.deepcopy(self.signals[index])
        self.remove_shift()
        self.update_plots()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    signals = copy.deepcopy(Signal.get_all_signals(True))
    glue_popup = GluePopUp(signals=signals)
    glue_popup.set_signals(signals[0], signals[1])
    glue_popup.combo_signal1.setCurrentIndex(0)
    glue_popup.combo_signal2.setCurrentIndex(1)
    #shift the signal2 to the right by 100% of signal1 length
    # glue_popup.set_shift(signals[0].data_pnts[-1][0] - signals[0].data_pnts[0][0])
    glue_popup.show()
    sys.exit(app.exec())