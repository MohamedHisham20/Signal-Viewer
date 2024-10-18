from MainWindow import Ui_MainWindow
from NonRectGraphController import NonRectGraph
from PySide6 import QtWidgets

def NonRect_connections(graph: NonRectGraph , ui: Ui_MainWindow):
    ui.Channels.setFixedHeight(400)
    if ui.nonRect_widget.layout() is None:
        layout = QtWidgets.QHBoxLayout(ui.nonRect_widget)
        ui.nonRect_widget.setLayout(layout)
    graph.pause_radar()
    ui.nonRect_widget.layout().addWidget(graph)
    ui.stop_c4.clicked.connect(lambda: graph.pause_radar())
    ui.play_c4.clicked.connect(lambda: graph.play_radar())
    ui.replay_c4.clicked.connect(lambda: graph.rewind_radar())
    ui.dial_slide_c4.valueChanged.connect(lambda: graph.scroll_radar(ui.dial_slide_c4.value()))
    ui.dial_slide_c4.sliderPressed.connect(lambda: graph.pause_radar())
    ui.dial_slide_c4.sliderReleased.connect(lambda: graph.play_radar())
    ui.dial_slide_c4.setRange(0, 360)
    ui.dial_speed_c4.valueChanged.connect(lambda: graph.change_speed(ui.dial_speed_c4.value()))
    ui.dial_speed_c4.setRange(1, 20)
    return ui
    
