import numpy as np
import csv
import os
from PySide6.QtCore import QPointF

class Signal:
    signal_counter = 0
    glued_signal_counter = 0

    def __init__(self, data_pnts=None, label=None, color=None, is_normalized=False):
        Signal.signal_counter += 1
        self.ID = "Signal_" + str(Signal.signal_counter)
        self.label = label
        self.data_qpnts = []
        self.data_pnts = []
        self.shift = 0
        self.last_point = 0
        if color is None:
            self.color = "#{:06x}".format(np.random.randint(0, 0xFFFFFF))
        else:
            self.color = color

        if data_pnts:
            for pnt in data_pnts:
                x, y = pnt[0], pnt[1]
                qpnt = QPointF(x, y)
                self.data_qpnts.append(qpnt)
                self.data_pnts.append(pnt)
            
            if is_normalized:
                self.normalize_y_values()

    def normalize_y_values(self):
        """Normalize y-values to be between -10 and 10."""
        y_values = np.array([y for _, y in self.data_pnts])
        
        # Scale y values
        min_y = y_values.min()
        max_y = y_values.max()

        # Avoid division by zero
        if min_y == max_y:
            scaled_y = np.zeros_like(y_values)  # All y values are the same, scale to 0
        else:
            scaled_y = -10 + (y_values - min_y) * (20 / (max_y - min_y))

        # Update data points with normalized y-values
        for i in range(len(self.data_pnts)):
            x = self.data_pnts[i][0]
            self.data_pnts[i] = (x, scaled_y[i])

    @staticmethod
    def get_all_signals(is_normalized=False):
        folderPath = os.path.dirname(os.path.abspath(__file__))
        return Signal.load_directory(folderPath, is_normalized)

    @staticmethod
    def load_directory(directory_path, is_normalized=False):
        signals = []
        for file_name in os.listdir(directory_path):
            if file_name.endswith('.csv'):
                file_path = os.path.join(directory_path, file_name)
                signal = Signal.from_file(file_path, is_normalized)
                if signal:
                    signal.label = file_name.split('/')[-1].split('.')[0]
                    signals.append(signal)
        return signals

    @staticmethod
    def from_file(file_path, is_normalized=False):
        data_pnts = []
        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                header = next(reader)
                if len(header) == 1:
                    data_pnts = [(i, float(row[0])) for i, row in enumerate(reader)]
                else:
                    for row in reader:
                        x, y = float(row[0]), float(row[1])
                        data_pnts.append((x, y))

        except Exception as e:
            return None
        return Signal(data_pnts, is_normalized=is_normalized)

    @staticmethod
    def from_NP_array(np_array, label=None, is_normalized=False):
        data_pnts = [(row[0], row[1]) for row in np_array]
        return Signal(data_pnts, label, is_normalized=is_normalized)

    @staticmethod
    def from_pd_df(df):
        Signal.glued_signal_counter += 1
        data_pnts = [(row[0], row[1]) for row in df.iterrows()]
        label = "Glued_Signal_" + str(Signal.glued_signal_counter)
        return Signal(data_pnts, label)

    def get_y_values(self):
        return [pnt[1] for pnt in self.data_pnts]

    def append_point(self, x, y):
        self.data_pnts.append((x, y))
        self.data_qpnts.append(QPointF(x, y))

    def get_sampling_frequency(self):
        if len(self.data_pnts) < 2:
            return 0
        time_diffs = np.diff([x for x, _ in self.data_pnts])
        return 1 / np.mean(time_diffs)
