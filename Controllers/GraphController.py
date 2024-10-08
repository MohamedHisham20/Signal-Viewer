from PyQt5.QtWidgets import (QWidget, QLabel, QLayout, QVBoxLayout,
    QHBoxLayout, QGridLayout, QPushButton, QLineEdit, QGraphicsWidget) 
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter
from PySide6 import QtCharts
import numpy as np
from GUI.Graph import Graph
        
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
        