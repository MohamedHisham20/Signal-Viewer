from PySide6.QtCharts import QLineSeries, QValueAxis
from PySide6.QtCore import QPointF
from PySide6.QtGui import QPen, QColor
import sys
import csv
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
from GUI.Graph import Graph
from GUI.Signal import Signal
              

                       
class GraphController:
    """Methods marked with double underscore (__) as a prefix
    are of internal behaviour and should not be accessed by other developers
    outside this class.\n\n
    Hover over a function name for info
    """        
    
    def __init__(self):
        print("A Graph Controller has been constructed")    
    
    
    def mount_btns_actions(self,graph:Graph):
        """This method has to be called immediately after constructing a graph\n
        to mount action on buttons"""
        
        graph.play_pause_btn.clicked.connect(lambda:self.toggle_play_pause_btn(graph))
        graph.replay_btn.clicked.connect(lambda:self.replay_signal(graph))
        graph.reset_btn.clicked.connect(lambda:self.reset_graph(graph))
        graph.zoom_in_btn.clicked.connect(lambda:self.zoom_in(graph))
        graph.zoom_out_btn.clicked.connect(lambda:self.zoom_out(graph))
        graph.speed_up_btn.clicked.connect(lambda:self.increase_plotting_speed(graph))
        graph.slow_down_btn.clicked.connect(lambda:self.decrease_plotting_speed(graph))
        
        graph.timer.timeout.connect(lambda:self.plot_signals(graph))
            
    
    def get_number_of_signals_in_graph(self,graph:Graph):    
        return graph.signals_counter
    
    
    def add_signal_to_graph(self,signal_ID , data_pnts, graph:Graph):
        """stores data points in graph and turns signal"""
        new_signal = Signal(signal_ID, data_pnts)
        graph.signals.append(new_signal)
        graph.signals_counter+=1
        
    
    def show_signal(self, signal_id:int, graph:Graph):
        signal_id = str(signal_id)
        
        for series in graph.chart.series():
            if series.name() == signal_id:
                if series.isVisible(): return
                else:
                    series.show()
                    break
                
                
    def hide_signal(self, signal_id:int, graph:Graph):
        signal_id = str(signal_id)
        
        for series in graph.chart.series():
            if series.name() == signal_id:
                if series.isVisible():
                    series.hide()
                    break
                else: return                
                
        
    def toggle_play_pause_btn(self, graph:Graph):
        """Cotrols playing and pausing\n
        connected to play and pause button\n
        this method is connected to play_loaded_signals method"""
        
        if graph.signals_counter == 0: 
            print("Graph is empty. Add a signal first")
            return        
            
        if graph.timer.isActive():
            graph.timer.stop()
            graph.play_pause_btn.setText("play")
            
        else:
            if graph.plotting_index > 0:
                graph.timer.start(graph.timer.interval())
                graph.play_pause_btn.setText("pause")
            else:
                graph.timer.start(graph.timer.interval())
                graph.play_pause_btn.setText("pause")
                self.get_chart_ready(graph)    

                    
    def get_chart_ready(self, graph:Graph, interval:int = 20):
        graph.chart.removeAllSeries()
        graph.plotting_index = 0
        graph.active = True
        
        for signal in graph.signals:
            series = QLineSeries()
            series.setName(str(signal.ID))
            graph.chart.addSeries(series)
            
        graph.chart.createDefaultAxes()
        self.set_full_view_port(graph)
        
        
    def set_full_view_port(self, graph:Graph):
        if not graph.signals: return 
        
        all_x = [qpoint.x() for signal in graph.signals for qpoint in signal.data_qpnts]
        all_y = [qpoint.y() for signal in graph.signals for qpoint in signal.data_qpnts]        
    
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        
        axis_x = QValueAxis()
        axis_y = QValueAxis()
        
        axis_x.setRange(min_x, max_x)
        axis_y.setRange(min_y, max_y)
        
        graph.chart.setAxisX(axis_x)
        graph.chart.setAxisY(axis_y)        
      
        for series in graph.chart.series():
            series.attachAxis(axis_x)
            series.attachAxis(axis_y)    
        
         
    def plot_signals(self, graph:Graph):
        all_signals_data_pnts_plotted = True
        
        for i, signal in enumerate(graph.signals):
            if graph.plotting_index < len(signal.data_qpnts):
                signal_series = graph.chart.series()[i]
                if isinstance(signal_series, QLineSeries):
                    signal_series.append(signal.data_qpnts[graph.plotting_index])            
                all_signals_data_pnts_plotted = False
                
        if all_signals_data_pnts_plotted:
            graph.timer.stop()
            graph.active = False
        else: graph.plotting_index+=1    
            
    
    
    def reset_graph(self,graph:Graph):
        """Zeros the graph but the signals' files still exist.\n
        Signals are still attached to the graph so they can be played again"""
        
        if graph.signals_counter == 0:
            print("graph is already empty")
            return
        
        #checks if the signal was running
        if graph.timer.isActive(): 
            graph.timer.stop()
        else:
            print("Graph is already idle")
            return
           
        i = 0
        for series in graph.chart.series():
            if isinstance(series, QLineSeries):
                series.clear()
        
        graph.plotting_index = 0
        graph.active = False
            
                
    def replay_signal(self, graph:Graph,interval:int=5):
        """connected with replay button"""
        
        if graph.signals_counter==0:
            print("Graph is empty. Load a signal first")
            return
        
        if graph.timer.isActive(): 
            graph.timer.stop()
            self.reset_graph(graph)
        
        self.get_chart_ready(graph)

    def increase_plotting_speed(self, graph:Graph):
        """connected with + button"""
        self.__control_speed(graph,-(graph.delta_interval))
    
    def decrease_plotting_speed(self, graph:Graph):
        """connected with - button"""
        self.__control_speed(graph, graph.delta_interval)
        
    def __control_speed(self, graph:Graph, delta_speed:int):
        if (graph.signals_counter==0) or graph.play_pause_btn.text=="play": return
        
        current_interval = graph.timer.interval()
        if delta_speed < 0 : # speed up 
            new_interval = min(graph.min_plotting_interval, current_interval+delta_speed)
        else : new_interval = max(graph.max_plotting_interval, current_interval+delta_speed)
        graph.timer.setInterval(new_interval)         
    
    def zoom_in(self, graph:Graph):
        graph.chart_view.chart().zoomIn()
    
    def zoom_out(self, graph:Graph):
        graph.chart_view.chart().zoomOut()
    
    
                                   