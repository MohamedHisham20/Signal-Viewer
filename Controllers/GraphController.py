from PyQt5.QtWidgets import (QWidget, QLabel, QLayout, QVBoxLayout,
    QHBoxLayout, QGridLayout, QPushButton, QLineEdit, QGraphicsWidget) 
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter
from PySide6 import QtCharts
import numpy as np

from ..test.test import Graph
        
class GraphController:
    @staticmethod
    def construct_graph(graph:Graph):
        GraphController.construct_chart(graph)
    
    @staticmethod
    def construct_chart(graph:Graph):
        graph.chart.addSeries(graph.series)
        graph.chart.createDefaultAxes()
    
    @staticmethod
    def init_layout(graph:Graph):
        """ Initialize graph layout as a QHBoxLayout and add its buttons"""    
        graph.layout = QHBoxLayout(graph)
        
        graph.layout.addWidget(graph.name_label)
        
        graph.layout.addWidget(graph.change_name_btn)
        graph.change_name_btn.clicked.connect(graph.update_graph_name)
        
        graph.layout.addWidget(graph.reset_btn)
        graph.change_name_btn.clicked.connect(graph.reset_graph)
        
        graph.layout.addWidget(graph.delete_btn)
        graph.delete_btn.clicked.connect(graph.delete_graph)

     
    @staticmethod            
    def update_graph_name(graph:Graph, new_name:str):
        graph.name_label.setText(new_name) 
        
    
    @staticmethod    
    def reset_graph(graph:Graph):
        pass
    
    
    @staticmethod
    def delete_graph(graph:Graph):
        pass              
        