from PySide6.QtWidgets import (QApplication, QMainWindow ,QWidget, QLabel, QVBoxLayout,
QHBoxLayout, QPushButton ,QScrollBar)
from PySide6.QtCore import Qt 
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
        graph.chart.addSeries(graph.series)
        graph.chart.createDefaultAxes()
        
        graph._layout_.addWidget(graph.horizontal_scroll_bar)
 
    @staticmethod            
    def update_graph_name(graph:Graph, new_name:str):
        graph.name_label.setText(new_name) 
        
    @staticmethod    
    def reset_graph(graph:Graph):
        pass
    
    @staticmethod
    def delete_graph(graph:Graph):
        pass              
        