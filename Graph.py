import copy
import sys
import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer, QElapsedTimer, Qt
from Signal import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout
# from Glue import glue_signals

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
        self.crop = lambda: print("No crop function set")

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
        self.is_user_panning = True
        self.elapsed_timer.start()
        if self.roi is not None:
            pos = self.mapToView(event.pos())
            self.roi.setSize([pos.x() - self.roi.pos()[0], pos.y() - self.roi.pos()[1]])
        else:
            super().mouseMoveEvent(event)

    def wheelEvent(self, event, *args, **kwargs):
        self.is_user_panning = True
        self.elapsed_timer.start()
        super().wheelEvent(event, *args, **kwargs)

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
                self.crop()
                # print(f"Selected X range: {bottom_left} to {bottom_right}")
                # print(f"Selected X range: {bottom_left} to {bottom_right}")


        super().keyPressEvent(event)

    def set_dynamic_limits(self, min_x, max_x, min_y, max_y):
        self.setLimits(
            xMin=min_x,
            xMax=max_x,
            maxXRange=max_x - min_x,
            minXRange=(max_x - min_x) / 100,
            yMin=min_y,
            yMax=max_y,
            maxYRange=max_y - min_y,
            minYRange=(max_y - min_y) / 100
        )

class Plot:
    def __init__(self, plot: pg.PlotDataItem, signal: Signal, label: pg.TextItem):
        self.plot = plot
        self.signal = signal
        self.label = label
        self.isRunning = True
        self.isRealTime = False
        self.last_point = int(len(signal.data_pnts) * 0.1)
        self.dynamic_interpolation = False
        self.plot1_interpolation = None
        self.plot2_interpolation = None

class Graph(QWidget):
    def __init__(self, ):
        super().__init__()
        self.custom_viewbox = CustomViewBox()
        self.plot_widget = pg.PlotWidget(viewBox=self.custom_viewbox)
        self.plot_widget.setBackground('#2b2b2b')
        self.plot_widget.showGrid(x=True, y=True)
        self.linked = False
        layout = QVBoxLayout()
        self.time_offset = 0
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)
        self.plot_to_track = None
        self.AllSignals :list[Signal] = Signal.get_all_signals(True)
        self.panWidth = 10
        self.plots: list[Plot] = []
        self.last_point = 0
        self.shift_slide = 0.0
        self.croped_count = 0
        self.plot_widget.setXRange(0, 10, padding=0)
        self.plot_widget.setYRange(-1, 1, padding=0)
        self.timer = QTimer()
        self.timer.setInterval(40)
        self.timer.timeout.connect(self.update)
        self.interploation_cool_down = False
        self.counter = 0
        self.slider = 0
        self.speed = 1


    def change_speed(self,speed:int):
        self.speed = speed
    
    def play_pause(self, plot: Plot = None ):
        if self.plots == [] :
            return
        if plot is None:
            state = self.plot_to_track.isRunning
            for plot in self.plots:
                plot.isRunning = not state
                if plot.last_point >= len(plot.signal.data_pnts) -1:
                    plot.isRunning = False
        self.custom_viewbox.is_user_panning = False



    def delete_signal(self,signal:Signal):
        # print("Signal not found")
        for plot in self.plots:
            if plot.signal.label == signal.label:
                self.plot_widget.removeItem(plot.plot)
                self.plot_widget.removeItem(plot.label)
                self.plots.remove(plot)
                del plot
                if len(self.plots) == 0:
                    self.timer.stop()
                break
        if self.plots == []:
            self.plot_to_track = None
    def crop_signal(self):
        if self.custom_viewbox.selectfirstX is None or self.custom_viewbox.selectseoncdX is None:
            return
        if self.plot_to_track is None:
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
                color=
            '#' + ''.join(np.random.choice(list('0123456789ABCDEF'), 6))
            )
            self.custom_viewbox.selectfirstX = None
            self.custom_viewbox.selectseoncdX = None
            return cropped_signal
        return None
    def plot_signal(self, signal: Signal,last_point:int = 0 , shift : int= 0) -> Plot:

        signal =copy.deepcopy(signal)
        # print(last_point)
        # add the shift to the x values
        signal.data_pnts = [(x + shift, y) for x, y in signal.data_pnts]
        for plot in self.plots:
            if plot.signal.label == signal.label:
                return plot
        x_values = [point[0] for point in signal.data_pnts]
        y_values = [point[1] for point in signal.data_pnts]
        curve = pg.PlotDataItem(x_values[:last_point], y_values[:last_point], pen=pg.mkPen(signal.color, width=2))
        label = pg.TextItem(text=signal.label, color=signal.color, anchor=(1, 1))
        self.plot_widget.addItem(label)
        plot = Plot(curve, signal, label)
        plot.last_point = last_point
        plot.signal.shift = shift
        self.plot_widget.addItem(plot.plot)
        if len(self.plots) == 0:
            self.plot_to_track = plot
            self.change_pan_window(plot,0.3)
            self.timer.start()
        self.plots.append(plot)
        self.plot_to_track = plot
        return plot
    
    def sihftX(self,shift:float):
        if self.plot_to_track is None:
            return
        minX = self.plot_to_track.signal.data_pnts[0][0]
        maxX = self.plot_to_track.signal.data_pnts[-1][0]
        shift = int((maxX - minX) * shift)
        plot = self.plot_to_track
        plot.signal.shift
        plot.signal.data_pnts = [(x - plot.signal.shift + shift, y) for x, y in plot.signal.data_pnts]
        plot.signal.shift = shift

    def Calculate_min_max(self):
        all_x_values = []
        all_y_values = []

        for plot in self.plots:
            margin = 0
            if plot.isRealTime:
                margin = 0

            x_values = [point[0] for point in plot.signal.data_pnts[:plot.last_point]]
            y_values = [point[1] + margin for point in plot.signal.data_pnts[:plot.last_point]]
            all_x_values.extend(x_values)
            all_y_values.extend(y_values)

        min_x = (min(all_x_values) if all_x_values else 0)
        max_x = (max(all_x_values) if all_x_values else 10)
        min_y = (min(all_y_values) if all_y_values else -1)
        max_y = (max(all_y_values) if all_y_values else 1)

        return min_x, max_x, min_y, max_y
    @staticmethod
    def get_range(signal:Signal):
        range = -signal.data_pnts[0][0] + signal.data_pnts[-1][0]
        return range


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
                Graph.remove_shift(plot.signal)
                plot.isRunning = True
        else:
            Plot.last_point = 0
            Graph.remove_shift(Plot.signal)
            Plot.isRunning = True
        self.custom_viewbox.is_user_panning = False
        self.plot_widget.setXRange(0, 10, padding=0)
        self.plot_widget.setYRange(-1, 1, padding=0)

    def fast_forward(self):
        longest = self.longest_signal()
        for plot in self.plots:
            plot.last_point = len(longest.signal.data_pnts) - 1
            plot.isRunning = False
            
    def change_pan_window(self,Plot:Plot ,ratio:float = 0.3):

        self.panWidth = Graph.get_range(Plot.signal) *ratio
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
            if plot.last_point >= len(plot.signal.data_pnts) - 1 and not plot.isRealTime:
                plot.isRunning = False
            if plot.isRunning:
                plot.last_point += self.speed
                #print the timer interval 
                print(self.timer.interval())
                plot.last_point = min(plot.last_point , len(plot.signal.data_pnts) - 1)
                plot.signal.last_point = plot.last_point
                if plot.isRealTime:
                    last_x = plot.signal.data_pnts[-1][0]
                    last_y = plot.signal.data_pnts[-1][1]
                    plot.signal.data_pnts.append((last_x +1, last_y))
            # if signal empty continue
            if len(plot.signal.data_pnts) == 0:
                continue
            plot.plot.setData([point[0] for point in plot.signal.data_pnts[:plot.last_point]], 
                              [point[1] for point in plot.signal.data_pnts[:plot.last_point]])
            index = plot.last_point - 1
            if index >= len(plot.signal.data_pnts) or index < 0:
                index = len(plot.signal.data_pnts) - 1
            # print(plot.last_point ,"len",len(plot.signal.data_pnts))

            plot.label.setPos(plot.signal.data_pnts[index][0], plot.signal.data_pnts[index][1])
        if len(self.plot_to_track.signal.data_pnts) == 0:
            self.timer.stop()
            return
        min_x, max_x, min_y, max_y = self.Calculate_min_max()
        self.custom_viewbox.signal_max_x = max_x
        self.custom_viewbox.signal_min_x = min_x
        self.custom_viewbox.signal_max_y = max_y
        self.custom_viewbox.signal_min_y = min_y
        margin_y = abs(max_y - min_y) * 0.4
        min_y -= margin_y
        max_y += margin_y
        start = max(max_x - self.panWidth, min_x)
        end = start + self.panWidth
        margin = max(self.panWidth - max_x,0)
        
        self.custom_viewbox.set_dynamic_limits(
            min_x,
            end +margin,
            min_y,
            max_y
        )
        self.farthest_plot()
        longest = self.plot_to_track
        # print("label",longest.signal.label)
        # print("last point",longest.last_point,"len",len(longest.signal.data_pnts))
        if self.custom_viewbox.elapsed_timer.elapsed() + self.time_offset > 2000 and longest.signal.data_pnts[longest.last_point][0] >= self.plot_widget.viewRange()[0][1]:
            self.time_offset = 0
            self.custom_viewbox.is_user_panning = False

        # print("is linked", self.linked , "is user panning",self.custom_viewbox.is_user_panning)
        if not self.custom_viewbox.is_user_panning and longest.isRunning:
            self.plot_widget.setXRange(start, end, padding=0)
            # if not self.linked:
                # self.plot_widget.setYRange(min_y, max_y, padding=0)
            self.plot_widget.setYRange(min_y, max_y, padding=0)
  
    def get_last_point(self):
        if self.plot_to_track:

            # print(self.plot_to_track.last_point)
            return self.plot_to_track.last_point
        return 0


    def plot_real_time(self,last_point = 0,shift:int = 0 ,label:str="Wind Speed") -> Plot:
        signal = Signal(label=label, data_pnts=[(0, 6.5), (1, 6.5)], color='#FF0000')
        # add the shift to the x values
        signal.data_pnts = [(x + shift, y) for x, y in signal.data_pnts]
        for plot in self.plots:
            if plot.signal.label == signal.label:
                return plot
        x_values = [point[0] for point in signal.data_pnts]
        y_values = [point[1] for point in signal.data_pnts]
        curve = pg.PlotDataItem(x_values, y_values, pen=pg.mkPen(signal.color, width=2))
        label = pg.TextItem(text=signal.label, color=signal.color, anchor=(1, 1))
        self.plot_widget.addItem(label)
        plot = Plot(curve, signal, label)
        self.plots.append(plot)
        plot.last_point = last_point
        plot.signal.shift = shift
        plot.isRealTime = True
        self.plot_widget.addItem(plot.plot)
        # print("here")
        if len(self.plots) == 1:
            self.plot_to_track = plot
            self.change_pan_window(plot,0.3)
            self.timer.timeout.connect(self.update)
            self.timer.start(40)
        self.plot_to_track = plot
        
        return plot
    

    def update_real_time(self,value:int):
        # get all realtime
        for plot in self.plots:
            if plot.isRunning and plot.isRealTime:
                last_x = plot.signal.data_pnts[-1][0]
                plot.signal.data_pnts.append((last_x+1, value))

    @staticmethod
    def remove_shift(signal:Signal):
        shift = signal.data_pnts[0][0]
        signal.data_pnts = [(x - shift, y) for x, y in signal.data_pnts]

    def farthest_plot(self):
        max_plot = self.plot_to_track
        maxX = max_plot.signal.data_pnts[max_plot.last_point][0]
        for plot in self.plots:
            X =  plot.signal.data_pnts[plot.last_point][0]
            if X > maxX:
                max_plot = plot
                maxX = X
        self.plot_to_track = max_plot
            
    def slide(self,ratio:float):
        min_x, max_x, min_y, max_y = self.Calculate_min_max()
        range = max_x - min_x
        slide = max_x - ratio * range
        self.slider = slide
    
    def x_zoom(self,ratio:float):
        if self.plot_to_track is None:
            return
        self.custom_viewbox.is_user_panning = True
        self.custom_viewbox.elapsed_timer.start()

        min_x, max_x, min_y, max_y = self.Calculate_min_max()
        range = max_x - min_x
        self.panWidth = range * ratio
        self.farthest_plot()
        longest = self.plot_to_track
        end = max(longest.signal.data_pnts[longest.last_point][0] - self.slider,self.panWidth + min_x)
        start = max(end - self.panWidth - self.slider , min_x)
        self.plot_widget.setXRange(start, end, padding=0)
        self.plot_widget.setYRange(min_y, max_y, padding=0)
        