from PySide6.QtWidgets import (QFileDialog)
from PySide6.QtCharts import QLineSeries
import sys
import csv
import os


from GUI.Graph import Graph
from GUI.Signal import Signal
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))              

                       
class GraphController:
    """Methods marked with double underscore (__) as a prefix
    are of internal behaviour and should not be accessed by other developers
    outside this class.\n\n
    Hover over a function name for info
    """        
    
    def __init__(self):
        print("A new Graph has been constructed")
    
    
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
            
    
    def get_number_of_signals_in_graph(self,graph:Graph):    
        return graph.signals_counter
    
    
    def add_signal_to_graph(self,signal_ID ,data_pnts, graph:Graph):
        """stores data points in graph and turns signal"""
        new_signal = Signal(signal_ID, data_pnts)
        graph.signals.append(new_signal)
        
    
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
            if graph.active:
                graph.timer.start(graph.timer.interval())
                graph.play_pause_btn.setText("pause")
            else:
                graph.timer.start()
                self.get_chart_ready(graph)    

                    
    def get_chart_ready(self, graph:Graph):
        graph.chart.removeAllSeries()
        graph.plotting_index = 0
        
        for _ in graph.signals:
            series = QLineSeries()
            graph.chart.addSeries(series)
            
        graph.chart.createDefaultAxes()
        graph.timer.start()
         
    def plot_signals(self, graph:Graph):
        all_signals_plotted = False
        i = 0
        graph.active = True
        
        while not all_signals_plotted:
            signals_skipped_per_plotting_indx = 0
            for signal in graph.signals:
                if graph.plotting_index < len(signal.data_qpnts):
                    signal_series = graph.chart.series()[i]
                    if isinstance(signal_series, QLineSeries):
                        signal_series.append(signal.data_qpnts[graph.plotting_index])
                else : signals_skipped_per_plotting_indx+=1
                i+=1
            
            if signals_skipped_per_plotting_indx == len(graph.signals):
                all_signals_plotted = True        
            else: graph.plotting_index+=1            
                
        graph.timer.stop()
        graph.active = False
    
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
    
    
                                   