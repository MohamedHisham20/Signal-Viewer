from PySide6.QtWidgets import (QApplication, QMainWindow ,QWidget, QLabel, QVBoxLayout,
    QHBoxLayout, QPushButton) 
from PySide6 import QtCharts
import numpy as np
import sys

class Graph(QWidget):
    def __init__(self, name = "graph1"):
        """ Construct a Graph with name if given """
        super().__init__()
        #Graph member variables initialization
        #Direct children of graph are label, btns and chart_view
        
        self._layout_ = QVBoxLayout(self)
        
        self.name_label = QLabel(name,self)
        self.change_name_btn = QPushButton("change name",self)
        self.reset_btn = QPushButton("reset",self)
        self.delete_btn = QPushButton("delete Graph",self)
        
        self.chart = QtCharts.QChart()
        self.chart_view = QtCharts.QChartView(self.chart,self)
        self.series = QtCharts.QLineSeries()
        
        GraphController.construct_graph(self)
  
class GraphController:
    @staticmethod
    def construct_graph(graph:Graph):
        GraphController.init_layout(graph)
    
    @staticmethod
    def init_layout(graph:Graph):
        """ Initialize graph layout as a QHBoxLayout and add its children"""    
        graph._layout_.addWidget(graph.name_label)
        graph._layout_.addWidget(graph.change_name_btn)        
        graph._layout_.addWidget(graph.reset_btn)
        graph._layout_.addWidget(graph.delete_btn)
        graph._layout_.addWidget(graph.chart_view)
        graph.chart.addSeries(graph.series)
        graph.chart.createDefaultAxes()
 
    @staticmethod            
    def update_graph_name(graph:Graph, new_name:str):
        graph.name_label.setText(new_name) 
        
    @staticmethod    
    def reset_graph(graph:Graph):
        pass
    
    @staticmethod
    def delete_graph(graph:Graph):
        pass                 

class MainWindow(QMainWindow):
    def __init__(self,name:str):
        super().__init__()
        self.setGeometry(0,0,500,500)
        self.setWindowTitle(name)  
        self.graph = Graph("Test")
        self.setCentralWidget(self.graph)
 
def main():
    app = QApplication([])
    window = MainWindow("test window")
    window.show()
    sys.exit(app.exec_())

      
main()    