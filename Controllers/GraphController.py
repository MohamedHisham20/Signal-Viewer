from PySide6.QtCharts import QLineSeries, QValueAxis
from PySide6.QtCore import QPointF, Qt, QObject, QEvent, QRectF
from PySide6.QtGui import QWheelEvent, QMouseEvent
from PySide6.QtWidgets import QPushButton
import sys
from typing import List, Dict
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
from GUI.Graph import Graph, Signal

                               
class GraphController():
    """Methods marked with double underscore (__) as a prefix
    are of internal behaviour and should not be accessed by other developers
    outside this class.\n\n
    Hover over a function name for info
    """        
    
    def __init__(self):
        print("A Graph Controller has been constructed")
        self.controlled_graphs: List[Graph] = []
            
    

            
    
    def get_graph(self, graph_id:int):
        for graph in self.controlled_graphs:
            if graph.ID == graph_id:        
                return graph
            
        print("Such Graph does not exist")    
    
    
    def get_number_of_signals_in_graph(self, graph_id:int):    
        return self.get_graph(graph_id).signals_counter        
    
    
    def add_signal_to_graph(self,signal_ID , data_pnts, graph_id:int):
        """stores data points in graph and turns signal"""
        
        graph = self.get_graph(graph_id)
        
        new_signal = Signal(signal_ID, data_pnts)
        graph.signals.append(new_signal)
        graph.signals_counter+=1
        
    
    def show_signal(self, signal_id:int, graph_id:int):
        graph = graph = self.get_graph(graph_id)
        
        signal_id = str(signal_id)
        
        for series in graph.chart.series():
            if series.name() == signal_id:
                if series.isVisible(): return
                else:
                    series.show()
                    break
                
                
    def hide_signal(self, signal_id:int, graph_id:int):
        graph = graph = self.get_graph(graph_id)
        
        signal_id = str(signal_id)
        
        for series in graph.chart.series():
            if series.name() == signal_id:
                if series.isVisible():
                    series.hide()
                    break
                else: return                
                
        
    

                    
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
         
        graph.timer.start(graph.timer.interval())    
                
    
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
            
    
    def reset_graph(self, graph_id:int):
        """Zeros the graph but the signals' files still exist.\n
        Signals are still attached to the graph so they can be played again"""
        graph = self.get_graph(graph_id)
        
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
            
                
    def replay_signal(self, graph_id:int, interval:int=5):
        """connected with replay button"""
        
        graph = self.get_graph(graph_id)
        if graph.signals_counter==0:
            print("Graph is empty. Load a signal first")
            return
        
        if graph.timer.isActive(): 
            graph.timer.stop()
            self.reset_graph(graph)
        
        self.get_chart_ready(graph)

    
    def increase_plotting_speed(self, graph_id:int):
        """connected with + button"""
        graph = self.get_graph(graph_id)
        self.__control_speed(graph.ID,-(graph.delta_interval))
    
    
    def decrease_plotting_speed(self, graph_id:int):
        """connected with - button"""
        graph = self.get_graph(graph_id)
        self.__control_speed(graph.id, graph.delta_interval)
        
    
    def __control_speed(self, graph_id:int, delta_speed:int):
        graph = self.get_graph(graph_id)
        if (graph.signals_counter==0) or graph.play_pause_btn.text=="play": return
        
        current_interval = graph.timer.interval()
        if delta_speed < 0 : # speed up 
            new_interval = min(graph.min_plotting_interval, current_interval+delta_speed)
        else : new_interval = max(graph.max_plotting_interval, current_interval+delta_speed)
        graph.timer.setInterval(new_interval)         
        
    
    def zoom_in(self, graph_id:int):
        graph = self.get_graph(graph_id)
        graph.chart_view.chart().zoomIn()
    
    def zoom_out(self, graph_id:int):
        graph = self.get_graph(graph_id)
        graph.chart_view.chart().zoomOut()
    
    
    def get_signal_from_graph(self, signal_id:int, graph:Graph):
        for signal in graph.signals:
            if signal.ID == signal_id:
                return signal
            
        print("Such signal is not in this graph")    
    
    
    def signal_part_selection_requested(self, graph_id:int):
        graph = self.get_graph(graph_id)
        graph.signal_part_selection_requested = True
              

    def plot_signals_selections(self, source_graph_id, new_graph_id):
        
        src_graph = self.get_graph(source_graph_id)
        new_graph = self.get_graph(new_graph_id)
        
        src_graph.signal_part_selection_requested = False
        new_graph.plotting_index = 0
        
        for key in src_graph.selected_signals_parts.keys():
            series = QLineSeries()
            series.setName(str(key))
            new_graph.chart.addSeries(series)        
        
        new_graph.chart.removeAllSeries()
        new_graph.active = True
        new_graph.timer.start(new_graph.timer.interval())
        new_graph.play_pause_btn.setText("pause")
        
        counter = 0
        while counter < len(src_graph.selected_signals_parts.values()):
            counter = 0
            for list in src_graph.selected_signals_parts.values():
                if new_graph.plotting_index < len(list):
                    signal_series = new_graph.chart.series()[key]
                    if isinstance(signal_series, QLineSeries):
                        signal_series.append(list[new_graph.plotting_index])
                else: counter+=1        
            new_graph.plotting_index+=1                        
                
        new_graph.timer.stop()
        new_graph.active = False