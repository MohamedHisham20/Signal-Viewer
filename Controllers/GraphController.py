from PySide6.QtWidgets import (QApplication, QMainWindow ,QWidget, QLabel, QVBoxLayout,
QHBoxLayout, QPushButton ,QScrollBar)
from PySide6.QtCore import Qt, QPointF 
from PySide6.QtCharts import QChart, QChartView, QLineSeries
import numpy as np
import sys
import csv
import os


class Graph(QWidget):
    def __init__(self, name = "graph1"):
        """ Construct a Graph with name if given """
        super().__init__()
        
        #Graph member variables initialization
        self._layout_ = QVBoxLayout(self)
        
        # Child 1 of Graph Widget. A container for the following 4 btns
        self.graph_controls = QWidget(self)
        self.graph_controls_layout = QHBoxLayout(self.graph_controls)
        
        # Children of graph_controls
        self.name_label = QLabel(name,self)
        self.change_name_btn = QPushButton("change name",self)
        self.reset_btn = QPushButton("reset",self)
        self.delete_btn = QPushButton("delete Graph",self)
        
        #Child 2 of Graph Widget
        self.chart = QChart()
        self.chart_view = QChartView(self.chart,self)
        self.series = QLineSeries()
        
        #child 3 of Graph Widget
        self.horizontal_scroll_bar = QScrollBar(Qt.Orientation.Horizontal,self)        
        
        #this method shall execute all code needed to construct the graph layout
        GraphController.construct_graph(self)

    def draw_signal(self,file_path):
        GraphController.draw_signal(self,file_path)
        
            
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
    def draw_signal(graph:Graph,file_path:str):
        try:
            with open(file_path, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    x, y = float(row[0]), float(row[1])
                    pnt = QPointF(x,y)
                    graph.series.append(pnt)
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            
        graph.chart.addSeries(graph.series)
        graph.chart.createDefaultAxes()
        
    def pan_chart(graph):
        pass        
        