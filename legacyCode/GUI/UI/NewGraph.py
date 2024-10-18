from pyqtgraph import PlotWidget, mkPen
from PySide6.QtCore import QTimer


class NewGraph(PlotWidget):
    def __init__(self, signals=None, parent=None):
        super().__init__(parent)
        if signals is None:
            signals = []

        self.signals = signals
        self.plot_signals()
        self.current_time = 0
        self.current_speed = 1
        self.max_speed = 5
        self.timer_interval = 50  # Assumed resolution of samples???
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)

        self.plot_item = self.getPlotItem()
        self.plot_item.setXRange(0, 10)
        self.curves = []
        self.init_curves()

        if len(self.signals) != 0:
            self.timer.start(self.timer_interval)

    def init_curves(self):
        for signal in self.signals:
            curve = self.plot_item.plot(pen=mkPen('r', width=2))
            self.curves.append(curve)

    def plot_signals(self):
        if self.signals:
            self.update_plot()

    def update_plot(self):
        if self.signals:
            self.current_time += self.current_speed * (self.timer_interval / 1000.0)

            # Get current axis ranges after the plot is updated
            x_axis = self.plot_item.getAxis('bottom')
            y_axis = self.plot_item.getAxis('left')

            # Ensure to print out current ranges to see their values
            current_xmin, current_xmax = x_axis.range
            current_ymin, current_ymax = y_axis.range

            print("current_xmin ", current_xmin, " current_xmax ", current_xmax)

            # Define time window for updating
            time_window = current_xmax - current_xmin
            print("time window ", time_window)
            start_time = self.current_time - time_window
            end_time = self.current_time

            start_time = max(0, start_time)

            for i, signal in enumerate(self.signals):
                x_data, y_data = zip(*signal.data_pnts)
                indices = [j for j, x in enumerate(x_data) if start_time <= x <= end_time]

                if indices:
                    start_index, end_index = indices[0], indices[-1]
                    self.curves[i].setData(x_data[start_index:end_index], y_data[start_index:end_index])

                    print("start_index ", start_index, " end_index ", end_index)
                    print("start_time ", start_time, " end time ", end_time)
                    print("min y in data ", min(y_data[start_index:end_index]))

                    # Update current ymin and ymax
                    current_ymin, current_ymax = min(current_ymin, min(y_data[start_index:end_index])), max(
                        current_ymax, max(y_data[start_index:end_index]))

            # Update the x-axis range to reflect the current time window
            self.plot_item.getViewBox().setXRange(start_time, end_time)
            print(current_ymin, current_ymax)

            # Update the y-axis range if necessary
            # self.plot_item.getViewBox().setYRange(current_ymin, current_ymax)

            if self.__get_last_time() <= self.current_time:
                self.timer.stop()

    def speed_up(self):
        self.current_speed = min(self.points_per_second + 0.5, self.max_speed)

    def slow_down(self):
        self.current_speed = max(self.points_per_second - 0.5, 0)

    def zoom_in(self):
        pass

    def zoom_out(self):
        pass

    def toggle_play_pause(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(self.timer_interval)

    def __get_last_time(self):
        last_time = 0
        for signal in self.signals:
            last_time = max(last_time, signal.data_pnts[-1][0])
        return last_time

    def add_signal(self, signal):
        # Add to signal_list, and maybe change the starting value of the signal to match the graph's current time???
        if len(self.signals) == 0:
            self.timer.start(self.timer_interval)
        self.signals.append(signal)
        curve = self.plot_item.plot(pen=mkPen('r', width=2))
        self.curves.append(curve)
