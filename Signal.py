from PySide6.QtCore import QPointF
import numpy as np
import csv
import os

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
    def get_all_signals():
        folderPath = os.path.dirname(os.path.abspath(__file__))
        return Signal.load_directory(folderPath)
    

    @staticmethod
    def load_file(file_path):
        signal = Signal.from_file(file_path)
        if signal:
            signal.label = file_path.split('/')[-1].split('.')[0]
        return signal

    @staticmethod
    def load_directory(directory_path):
        signals = []
        for file_name in os.listdir(directory_path):
            if file_name.endswith('.csv'):
                file_path = os.path.join(directory_path, file_name)
                signal = Signal.from_file(file_path)
                if signal:
                    signal.label = file_name.split('/')[-1].split('.')[0]
                    signals.append(signal)
        return signals

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
    def from_pd_df(df):
        Signal.glued_signal_counter += 1
        data_pnts = []
        for row in df.iterrows():
            x, y = row[0], row[1]
            data_pnts.append((x, y))

        label = "Glued_Signal_" + str(Signal.glued_signal_counter)
        return Signal(data_pnts, label)

    
    def get_y_values(self):
        y_values = []
        for pnt in self.data_pnts:
            y_values.append(pnt[1])
        return y_values

    def append_point(self, x, y):
        self.data_pnts.append((x, y))
        self.data_qpnts.append(QPointF(x, y))

    def get_sampling_frequency(self):
        if len(self.data_pnts) < 2:
            return 0
        time_diffs = np.diff([x for x, y in self.data_pnts])
        return 1 / np.mean(time_diffs)
