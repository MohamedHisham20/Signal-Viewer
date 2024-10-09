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
    def construct_graph(graph:Graph):
        GraphController.init_layout(graph)
    
    @staticmethod
    def init_layout(graph:Graph):
        """ Initialize graph layout as a QHBoxLayout and append its children.
        """    
        graph._layout_.addWidget(graph.graph_controls)
        
        graph.graph_controls_layout.addWidget(graph.name_label)
        graph.graph_controls_layout.addWidget(graph.change_name_btn)        
        graph.graph_controls_layout.addWidget(graph.reset_btn)
        graph.graph_controls_layout.addWidget(graph.delete_btn)
        
        graph._layout_.addWidget(graph.chart_view)        
        graph._layout_.addWidget(graph.horizontal_scroll_bar)

    @staticmethod
    def load_signal(graph:Graph,file_path:str):
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
        GraphController.load_signal(graph,file_path)
        graph.series.clear()
        graph.chart.addSeries(graph.series)
        graph.signal_curr_indx=0
        graph.timer.timeout.connect(lambda: GraphController.start_drawing(graph))
        graph.timer.start(interval)
        GraphController.start_drawing(graph)
        
    @staticmethod
    def start_drawing(graph:Graph):
        if graph.signal_curr_indx < len(graph.data_pnts):
            graph.series.append(graph.data_pnts[graph.signal_curr_indx])
            graph.chart.createDefaultAxes()
            graph.signal_curr_indx += 1
        else:
            graph.timer.stop()