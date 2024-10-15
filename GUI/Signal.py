from PySide6.QtCore import QPointF
import csv


class Signal():
    signal_counter = 0

    def __init__(self, data_pnts, label=None):
        Signal.signal_counter += 1
        self.ID = "Signal_" + str(Signal.signal_counter)
        self.label = label
        self.data_qpnts = []
        self.data_pnts = data_pnts

        for pnt in data_pnts:
            x, y = pnt[0], pnt[1]
            qpnt = QPointF(x, y)
            self.data_qpnts.append(qpnt)

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


    def get_y_values(self):
        y_values = []
        for pnt in self.data_pnts:
            y_values.append(pnt[1])
        return y_values
