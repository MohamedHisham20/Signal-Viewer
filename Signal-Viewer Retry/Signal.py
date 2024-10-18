from PySide6.QtCore import QPointF
import numpy as np
import csv


class Signal:
    signal_counter = 0
    glued_signal_counter = 0

    def __init__(self, data_pnts=None, label=None):
        Signal.signal_counter += 1
        self.ID = "Signal_" + str(Signal.signal_counter)
        self.label = label
        self.data_qpnts = []
        self.data_pnts = []

        if data_pnts:
            for pnt in data_pnts:
                x, y = pnt[0], pnt[1]
                qpnt = QPointF(x, y)
                self.data_qpnts.append(qpnt)
                self.data_pnts.append(pnt)

    @staticmethod
    def from_file(file_path):
        data_pnts = []
        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                header = next(reader)
                for row in reader:
                    x, y = float(row[0]), float(row[1])
                    data_pnts.append((x, y))

        except Exception as e:
            return None
        return Signal(data_pnts)

    @staticmethod
    def from_NP_array(np_array):
        data_pnts = []
        for row in np_array:
            x, y = row[0], row[1]
            data_pnts.append((x, y))

        return Signal(data_pnts)
    
    @staticmethod
    def from_NP_array(np_array, label):
        data_pnts = []
        for row in np_array:
            x, y = row[0], row[1]
            data_pnts.append((x, y))

        return Signal(data_pnts, label)

    @staticmethod
    def from_pd_df(df, x_col='x', y_col='y'):
        Signal.glued_signal_counter += 1
        data_pnts = []
        for row in df.iterrows():
            x, y = row[1][x_col], row[1][y_col]
            data_pnts.append((x, y))

        label = "Glued_Signal_" + str(Signal.glued_signal_counter)
        return Signal(data_pnts, label)

    def append_point(self, x, y):
        self.data_pnts.append((x, y))
        self.data_qpnts.append(QPointF(x, y))

    def get_sampling_frequency(self):
        if len(self.data_pnts) < 2:
            return 0
        time_diffs = np.diff([x for x, y in self.data_pnts])
        return 1 / np.mean(time_diffs)

    def get_x_values(self):
        return [pnt[0] for pnt in self.data_pnts]

    def get_y_values(self):
        return [pnt[1] for pnt in self.data_pnts]
