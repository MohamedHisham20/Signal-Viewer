from PySide6.QtWidgets import (QApplication, QMainWindow ,QWidget, QLabel, QVBoxLayout,
QHBoxLayout, QPushButton ,QScrollBar)
from PySide6.QtCore import Qt, QTimer 
from PySide6.QtCharts import QChart, QChartView, QLineSeries

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
        
        self.chart = QChart()
        self.chart_view = QChartView(self.chart,self)
        self.series = QLineSeries()
        self.data_pnts = []
        
        self.timer = QTimer()
        self.signal_curr_indx = 0
        
        self.horizontal_scroll_bar = QScrollBar(Qt.Orientation.Horizontal,self)