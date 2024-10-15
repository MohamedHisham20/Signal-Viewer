from PySide6.QtWidgets import (QWidget, QVBoxLayout,
QHBoxLayout, QPushButton ,QGraphicsView)
from PySide6.QtCore import Qt, QTimer, QPointF, QObject, QEvent
from PySide6.QtGui import QPainter, QMouseEvent, QWheelEvent
from PySide6.QtCharts import QChart, QChartView, QValueAxis, QColorAxis
from GUI.Signal import Signal
from typing import List

class Graph(QWidget):
    def __init__(self, ID:int):
        """ Construct a Graph with name if given """
        
        super().__init__()
        self.graph_layout = QVBoxLayout(self)
        self.ID = ID
        
        #Graph states       
        self.plotting_index = 0
        self.signals_counter = 0
        self.active = False
        
        #Container for graph controls
        self.graph_controls = QWidget(self)
        self.graph_controls_layout = QHBoxLayout(self.graph_controls)
        self.play_pause_btn = QPushButton("play",self)
        self.replay_btn = QPushButton("replay",self)
        self.zoom_in_btn = QPushButton("zoom in",self)
        self.zoom_out_btn = QPushButton("zoom out",self)
        self.speed_up_btn = QPushButton("speed up",self)
        self.slow_down_btn = QPushButton("slow down",self)
        self.reset_btn = QPushButton("reset",self)   
        
        #Chart Setup;
        self.chart = QChart()
        
        self.chart_view = QChartView(self.chart,self)
        self.chart_view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.chart_view.setMouseTracking(True)
        self.chart_zoom_factor = 1.1
        self.chart_view.installEventFilter(self.chart_view)
        
        self.chart.zoom(self.chart_zoom_factor)
        self.chart_last_mouse_pos:QPointF = None
        self.x_axis = QValueAxis()
        self.y_axis = QValueAxis()
        self.timer = QTimer()
        self.timer.setInterval(20)
        self.delta_interval = 0.2 #default change in timer interval
        self.min_plotting_interval = 5 # corresponds to fastest plotting
        self.max_plotting_interval = 50 # corresponds to slowest plotting
        self.signals: List[Signal] = []
                
        #Layout setup
        self.graph_controls_layout.addWidget(self.play_pause_btn)
        self.graph_controls_layout.addWidget(self.replay_btn)
        self.graph_controls_layout.addWidget(self.reset_btn)
        self.graph_controls_layout.addWidget(self.zoom_in_btn)
        self.graph_controls_layout.addWidget(self.zoom_out_btn)
        self.graph_controls_layout.addWidget(self.speed_up_btn)
        self.graph_controls_layout.addWidget(self.slow_down_btn)
        
        self.graph_layout.addWidget(self.graph_controls)
        self.graph_layout.addWidget(self.chart_view)
        
    
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if watched == self.chart_view:
            if isinstance(event, QWheelEvent):
                self.listen_to_chart_wheel(event)
                return True
            elif event.type() == QEvent.Type.MouseButtonPress:
                self.mouse_press_event(event)
                return True
            elif event.type() == QEvent.Type.MouseButtonRelease:
                self.mouse_release_event(event)
                return True
            elif event.type() == QEvent.Type.MouseMove:
                self.mouse_move_event(event)
                return True
        return super().eventFilter(watched, event)
    

    def listen_to_chart_wheel(self, event: QWheelEvent):
        """Handle Mouse Zooming\n
        A zooming factor > 1 zooms in while if < 1 zooms out"""
        if event.angleDelta().y() > 0:
            self.chart_view.chart().zoom(self.chart_zoom_factor)
        else:
            self.chart_view.chart().zoom(1 / self.chart_zoom_factor)
        
        # Check if the left mouse button is pressed for panning
        if self.chart_last_mouse_pos:
            delta: QPointF = event.position() - self.chart_last_mouse_pos
            self.chart.scroll(-delta.x(), delta.y())
            self.chart_last_mouse_pos = event.position()
    
    
    def mouse_press_event(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.chart_last_mouse_pos = event.position()
        self.chart_view.mousePressEvent(event)
        
    
    def mouse_release_event(self, event: QMouseEvent):       
        if event.button() == Qt.MouseButton.LeftButton:
            self.chart_last_mouse_pos = None
        self.chart_view.mouseReleaseEvent(event)
        
        
    def mouse_move_event(self, event: QMouseEvent):        
        if self.chart_last_mouse_pos:
            delta: QPointF = event.position() - self.chart_last_mouse_pos
            self.chart.scroll(-delta.x(), delta.y())
            self.chart_last_mouse_pos = event.position()
        self.chart_view.mouseMoveEvent(event) 
