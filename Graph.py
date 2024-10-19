import sys
import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer, QElapsedTimer, Qt
from Signal import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout

class CustomViewBox(pg.ViewBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_user_panning = False
        self.elapsed_timer = QElapsedTimer()
        self.signal_min_x = 0
        self.signal_max_x = 10
        self.signal_min_y = -1
        self.signal_max_y = 1
        self.roi :pg.RectROI= None
        self.roi_start_pos = None
        self.roi_end_pos = None
        self.selectfirstX = None
        self.selectseoncdX = None

    def mousePressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier and event.button() == Qt.LeftButton:
            if self.roi is not None:
                self.removeItem(self.roi)
                self.roi = None
            pos = self.mapToView(event.pos())
            self.roi_start_pos = pos
            self.roi = pg.RectROI([pos.x(), pos.y()], [1, 1], pen='r')
            self.addItem(self.roi)
            self.roi.setZValue(10)  # Ensure ROI is on top
        else:
            self.is_user_panning = True
            self.elapsed_timer.start()
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.roi is not None:
            self.roi_end_pos = self.mapToView(event.pos())
        self.is_user_panning = False
        self.elapsed_timer.start()
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.roi is not None:
            pos = self.mapToView(event.pos())
            self.roi.setSize([pos.x() - self.roi.pos()[0], pos.y() - self.roi.pos()[1]])
        else:
            super().mouseMoveEvent(event)

    def wheelEvent(self, event):
        self.is_user_panning = True
        self.elapsed_timer.start()
        super().wheelEvent(event)

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C:
            if self.roi is not None:
                pos = self.roi.pos() 
                size = self.roi.size() 
                bottom_left = pos.x()
                bottom_right = pos.x() + size.x()
                self.selectfirstX = bottom_left
                self.selectseoncdX = bottom_right
                self.removeItem(self.roi)
                self.roi = None
                # print(f"Selected X range: {bottom_left} to {bottom_right}")


        super().keyPressEvent(event)

    def set_dynamic_limits(self, min_x, max_x, min_y, max_y):
        self.setLimits(
            xMin=min_x,
            xMax=max_x,
            maxXRange=max_x - min_x,
            minXRange=(max_x - min_x) / 10,
            yMin=min_y,
            yMax=max_y,
            maxYRange=max_y - min_y,
            minYRange=(max_y - min_y) / 10
        )

class Plot:
    def __init__(self, plot: pg.PlotDataItem, signal: Signal, label: pg.TextItem):
        self.plot = plot
        self.signal = signal
        self.label = label
        self.isRunning = True
        self.last_point = int(len(signal.data_pnts) * 0.1)

class Graph(QWidget):
    def __init__(self, ):
        super().__init__()
        self.custom_viewbox = CustomViewBox()
        self.plot_widget = pg.PlotWidget(viewBox=self.custom_viewbox)
        self.plot_widget.setBackground('#2b2b2b')
        self.plot_widget.showGrid(x=True, y=True)
        
        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)
        self.plot_to_track = None
        self.AllSignals :list[Signal] = Signal.get_all_signals(True)
        self.panWidth = 10
        self.plots: list[Plot] = []
        self.last_point = 100
        self.shift_slide = 0.0
        self.croped_count = 0
        self.plot_widget.setXRange(0, 10, padding=0)
        self.plot_widget.setYRange(-1, 1, padding=0)
        self.timer = QTimer()


    def change_speed(self,speed:int):
        self.timer.start(speed)
    
    def play_pause(self, plot: Plot = None , play:bool = True):
        if plot is None:
            for plot in self.plots:
                plot.isRunning = play
        else:
            plot.isRunning = play

    def delete_signal(self,signal:Signal):
        # print("Signal not found")
        for plot in self.plots:
            if plot.signal.label == signal.label:
                self.plot_widget.removeItem(plot.plot)
                self.plot_widget.removeItem(plot.label)
                self.plots.remove(plot)
                if len(self.plots) == 0:
                    self.timer.stop()
                break
    def crop_signal(self):
        if self.custom_viewbox.selectfirstX is None or self.custom_viewbox.selectseoncdX is None:
            return
        plot = self.plot_to_track
        cropped_data = [
            point for point in plot.signal.data_pnts
            if self.custom_viewbox.selectfirstX <= point[0] <= self.custom_viewbox.selectseoncdX
        ]
        if cropped_data:
            self.croped_count += 1
            cropped_signal = Signal(
                label=f"Cropped_{plot.signal.label} {self.croped_count}",
                data_pnts=cropped_data,
                color=plot.signal.color
            )
            self.custom_viewbox.selectfirstX = None
            self.custom_viewbox.selectseoncdX = None
            return cropped_signal
        return None
    def plot_signal(self, signal: Signal):
        # if signal already plotted
        for plot in self.plots:
            if plot.signal.label == signal.label:
                return plot
        x_values = [point[0] for point in signal.data_pnts]
        y_values = [point[1] for point in signal.data_pnts]
        curve = pg.PlotDataItem(x_values[:self.last_point], y_values[:self.last_point], pen=pg.mkPen(signal.color, width=2))
        label = pg.TextItem(text=signal.label, color=signal.color, anchor=(1, 1))
        self.plot_widget.addItem(label)
        plot = Plot(curve, signal, label)
        self.plots.append(plot)
        self.plot_widget.addItem(plot.plot)
        if len(self.plots) == 1:
            self.plot_to_track = plot
            self.change_pan_window(plot,0.1)
            self.timer.timeout.connect(self.update)
            self.timer.start(50)
        return plot

    def Calculate_min_max(self):
        all_x_values = []
        all_y_values = []

        for plot in self.plots:
            x_values = [point[0] for point in plot.signal.data_pnts[:plot.last_point]]
            y_values = [point[1] for point in plot.signal.data_pnts[:plot.last_point]]
            all_x_values.extend(x_values)
            all_y_values.extend(y_values)

        min_x = int(min(all_x_values) if all_x_values else 0)
        max_x = int(max(all_x_values) if all_x_values else 10)
        min_y = int(min(all_y_values) if all_y_values else -1)
        max_y = int(max(all_y_values) if all_y_values else 1)

        return min_x, max_x, min_y, max_y

    def longest_signal(self) -> Plot:
        longest = self.plots[0]
        for plot in self.plots:
            if len(plot.signal.data_pnts) > len(longest.signal.data_pnts):
                longest = plot
        return longest

    def rewind(self , Plot:Plot = None):
        if Plot is None:
            for plot in self.plots:
                plot.last_point = 0
                plot.isRunning = True
        else:
            Plot.last_point = 0
            Plot.isRunning = True

    def fast_forward(self):
        longest = self.longest_signal()
        for plot in self.plots:
            plot.last_point = len(longest.signal.data_pnts) - 1
            plot.isRunning = False
            
    def change_pan_window(self,Plot:Plot ,ratio:float = 0.1):
        self.panWidth = int(len(Plot.signal.data_pnts) * ratio)
        self.plot_to_track = Plot

    def change_bg_color(self,color:str):
        self.plot_widget.setBackground(color)

    def change_color(self,Plot:Plot,color:str):
        Plot.plot.setPen(pg.mkPen(color, width=2))
        Plot.label.setColor(color)

    def change_shift_slide(self,shift:int):
        self.shift_slide = shift
        
    def update(self):
        for plot in self.plots:
            if plot.last_point >= len(plot.signal.data_pnts) - 1:
                plot.isRunning = False
            if plot.isRunning:
                plot.last_point += 1
            plot.plot.setData([point[0] for point in plot.signal.data_pnts[:plot.last_point]], 
                              [point[1] for point in plot.signal.data_pnts[:plot.last_point]])
            # Update label position
            plot.label.setPos(plot.signal.data_pnts[plot.last_point - 1][0], plot.signal.data_pnts[plot.last_point - 1][1])

        min_x, max_x, min_y, max_y = self.Calculate_min_max()
        margin_x = (max_x - min_x) * 0.01
        margin_y = (max_y - min_y) * 0.1
        # min_x -= margin_x
        max_x += margin_x
        min_y -= margin_y
        max_y += margin_y
        self.custom_viewbox.signal_max_x = max_x
        self.custom_viewbox.signal_min_x = min_x
        self.custom_viewbox.signal_max_y = max_y
        self.custom_viewbox.signal_min_y = min_y
        self.custom_viewbox.set_dynamic_limits(
            min_x,
            max_x,
            min_y,
            max_y
        )

        longest = self.plot_to_track
        if self.custom_viewbox.elapsed_timer.elapsed() > 2000 and longest.signal.data_pnts[longest.last_point][0] >= self.plot_widget.viewRange()[0][1]:
            self.custom_viewbox.is_user_panning = False

        if not self.custom_viewbox.is_user_panning and longest.isRunning:
            self.plot_widget.setXRange(longest.last_point - self.shift_slide * longest.last_point, self.panWidth + longest.last_point - self.shift_slide * longest.last_point, padding=0)
            self.plot_widget.setYRange(min_y, max_y, padding=0)
    
    
class test(QMainWindow):
    def __init__(self):
        super().__init__()
        self.graph_widget = Graph()
        self.setCentralWidget(self.graph_widget)
        self.setWindowTitle("Real-Time Plotting with Zoom and Pan Limits")
        self.show()

# app = QApplication([])

# win = QMainWindow()

# graph = test()


# sys.exit(app.exec())
