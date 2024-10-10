from PySide6.QtWidgets import (QWidget, QLabel, QVBoxLayout,
QHBoxLayout, QPushButton ,QScrollBar, QLineEdit)
from PySide6.QtCore import Qt, QTimer 
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis


class Graph(QWidget):
    def __init__(self):
        """ Construct a Graph with name if given """
        super().__init__()
        
        #Graph member variables initialization
        self.graph_layout = QVBoxLayout(self)
        
        #Container for graph btns
        self.graph_controls = QWidget(self)
        self.graph_controls_layout = QHBoxLayout(self.graph_controls)
           
        # Graph controls
        self.name_field = QLineEdit("Graph_Name",self)
        self.change_name_btn = QPushButton("change name",self)
        self.reset_btn = QPushButton("reset",self)
        self.delete_btn = QPushButton("delete Graph",self)
        
        #Chart Setup
        self.chart = QChart()
        self.chart_view = QChartView(self.chart,self)
        self.x_axis = QValueAxis()
        self.y_axis = QValueAxis()
        self.series = QLineSeries()
        self.data_pnts = []
        self.timer = QTimer()
        self.delta_interval = 2 #default change in timer interval
        self.min_plotting_interval = 5 # corresponds to fastest plotting
        self.max_plotting_interval = 50 # corresponds to slowest plotting
        self.horizontal_scroll_bar = QScrollBar(Qt.Orientation.Horizontal,self)
        
        #container for signal controls
        self.signal_controls = QWidget(self)
        self.signal_controls_layout = QHBoxLayout(self.signal_controls)
        
        #Signal Controls
        self.upload_btn = QPushButton("upload",self)
        self.play_pause_btn = QPushButton("play",self)
        self.replay_btn = QPushButton("replay",self)
        self.zoom_in_btn = QPushButton("zoom in",self)
        self.zoom_out_btn = QPushButton("zoom out",self)
        self.speed_up_btn = QPushButton("+speed",self)
        self.speed_down_btn = QPushButton("-speed",self)
        
        #Graph status
        self.signal_plotting_started  = False
        self.is_loaded = False
        self.uploaded_files = []
        self.active_file = ""
        self.signal_curr_indx = 0
        self.empty = True
        
        #Layout setup
        self.graph_controls_layout.addWidget(self.name_field)
        self.graph_controls_layout.addWidget(self.change_name_btn)
        self.graph_controls_layout.addWidget(self.reset_btn)
        self.graph_controls_layout.addWidget(self.delete_btn)
        
        self.signal_controls_layout.addWidget(self.upload_btn)
        self.signal_controls_layout.addWidget(self.play_pause_btn)
        self.signal_controls_layout.addWidget(self.replay_btn)
        self.signal_controls_layout.addWidget(self.zoom_in_btn)
        self.signal_controls_layout.addWidget(self.zoom_out_btn)
        self.signal_controls_layout.addWidget(self.speed_up_btn)
        self.signal_controls_layout.addWidget(self.speed_down_btn)
        
        self.graph_layout.addWidget(self.graph_controls)
        self.graph_layout.addWidget(self.chart_view)
        self.graph_layout.addWidget(self.horizontal_scroll_bar)
        self.graph_layout.addWidget(self.signal_controls)