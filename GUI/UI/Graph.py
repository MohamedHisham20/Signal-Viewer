from PySide6.QtWidgets import (QWidget, QLabel, QVBoxLayout,
QHBoxLayout, QPushButton ,QScrollBar, QLineEdit)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from GUI.Signal import Signal
from typing import List, Dict

class Graph(QWidget):
    def __init__(self):
        """ Construct a Graph with name if given """
        
        super().__init__()
        self.graph_layout = QVBoxLayout(self)
        self.setMinimumHeight(400)
        
        #Graph states       
        self.plotting_index = 0
        self.signals_counter = 0
        self.active = False
        
        #Container for graph controls
        # self.graph_controls = QWidget(self)
        # self.graph_controls_layout = QHBoxLayout(self.graph_controls)
        # self.play_pause_btn = QPushButton("play",self)
        # self.replay_btn = QPushButton("replay",self)
        # self.zoom_in_btn = QPushButton("zoom in",self)
        # self.zoom_out_btn = QPushButton("zoom out",self)
        # self.speed_up_btn = QPushButton("speed up",self)
        # self.slow_down_btn = QPushButton("slow down",self)
        # self.reset_btn = QPushButton("reset",self)
        
        #Chart Setup;
        self.chart = QChart()
        self.chart_view = QChartView(self.chart,self)
        self.chart_view.setRubberBand(QChartView.RubberBand.RectangleRubberBand)
        self.chart.zoom(5)
        self.x_axis = QValueAxis()
        self.y_axis = QValueAxis()
        self.timer = QTimer()
        self.delta_interval = 0.2 #default change in timer interval
        self.min_plotting_interval = 5 # corresponds to fastest plotting
        self.max_plotting_interval = 50 # corresponds to slowest plotting
        self.signals: List[Signal] = []
                
        #Layout setup
        # self.graph_controls_layout.addWidget(self.play_pause_btn)
        # self.graph_controls_layout.addWidget(self.replay_btn)
        # self.graph_controls_layout.addWidget(self.reset_btn)
        # self.graph_controls_layout.addWidget(self.zoom_in_btn)
        # self.graph_controls_layout.addWidget(self.zoom_out_btn)
        # self.graph_controls_layout.addWidget(self.speed_up_btn)
        # self.graph_controls_layout.addWidget(self.slow_down_btn)
        
        # self.graph_layout.addWidget(self.graph_controls)
        self.graph_layout.addWidget(self.chart_view)
