from PySide6.QtWidgets import (QApplication, QMainWindow ,QWidget, QLabel, QVBoxLayout,
QHBoxLayout, QPushButton ,QScrollBar)
from PySide6.QtCore import Qt, QPointF, QTimer 
from PySide6.QtCharts import QChart, QChartView, QLineSeries
import numpy as np
import sys
import csv
import os


from GUI.Graph import Graph
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))              

                       
class GraphController:        
    @staticmethod
    def connect_graph_btns_signals(graph:Graph):
        graph.speed_up_btn.clicked.connect(GraphController.increase_plotting_speed)
        graph.speed_down_btn.clicked.connect(GraphController.decrease_plotting_speed)
    
    
    @staticmethod
    def load_signal(graph:Graph,file_path:str):
        """Load the signal data points into graph\n
        a necessary step before static or real time plotting
        """
        try:
            with open(file_path, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    x, y = float(row[0]), float(row[1])
                    pnt = QPointF(x,y)
                    graph.data_pnts.append(pnt)
                print("Signal loaded successfully")    
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")

    
    @staticmethod   
    def draw_signal_static(graph:Graph, file_path:str):
        GraphController.load_signal(graph,file_path)
        graph.series.append(graph.data_pnts)
        graph.chart.addSeries(graph.series)
        graph.chart.createDefaultAxes()        
    
    
    @staticmethod
    def draw_signal_realtime(graph:Graph, file_path:str, interval:int =100):
        """The interval controls the plotting speed.\n
        smaller intervals correspond to faster plotting
        """
        GraphController.load_signal(graph,file_path)
        graph.series.clear()
        graph.chart.addSeries(graph.series)
        graph.signal_curr_indx=0
        
        graph.chart.setAxisX(graph.x_axis, graph.series)
        graph.chart.setAxisY(graph.y_axis, graph.series)
        
        GraphController.set_full_view_port(graph)
                
        graph.timer.timeout.connect(lambda: GraphController.animate_signal(graph))
        graph.timer.start(interval)
        GraphController.animate_signal(graph)
        
    
    @staticmethod
    def animate_signal(graph:Graph):
        if graph.signal_curr_indx < len(graph.data_pnts):
            graph.series.append(graph.data_pnts[graph.signal_curr_indx])
            graph.signal_curr_indx += 1
        else:
            graph.timer.stop()
    
    
    @staticmethod
    def set_full_view_port(graph: Graph):
        """Sets the view port to fit the whole signal in real time\n
        No need for the user to pan the signal.
        """
        if not graph.data_pnts:
            return

        x_min = graph.data_pnts[0].x()
        x_max = graph.data_pnts[-1].x()

        y_values = [point.y() for point in graph.data_pnts]
        y_min = min(y_values) if y_values else 0
        y_max = max(y_values) if y_values else 0

        graph.chart.axisX().setRange(x_min, x_max)
        graph.chart.axisY().setRange(y_min, y_max)
        
        
    @staticmethod
    def increase_plotting_speed(graph:Graph):
        GraphController.control_speed(graph,graph.delta_speed)
    
    
    @staticmethod
    def decrease_plotting_speed(graph:Graph):
        GraphController.control_speed(graph, -(graph.delta_speed))
    
    
    @staticmethod
    def control_speed(graph:Graph, delta_speed:int):
        current_interval = graph.timer.interval()
        if delta_speed > 0 : 
            new_interval = max(graph.min_plotting_interval, current_interval+delta_speed)
        else : new_interval = min(graph.max_plotting_interval, current_interval+delta_speed)
        graph.timer.setInterval(new_interval)
        