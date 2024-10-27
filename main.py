from PySide6 import QtCore, QtGui, QtWidgets
from MainWindow import DragDropList, Ui_MainWindow
from NonRectGraphController import NonRectGraph
from Connections import (
    NonRect_connections,
    Graph_connections,
    all_Channels_connections,
    add_lists,
    general_connections,
    report_connections,   
)
import sys
from Signal import Signal
from Graph import Graph

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

ui.Channels.setFixedHeight(400)
signals = Signal.get_all_signals(True)
Signal.signals = signals

graph_Channel1 = Graph()
graph_Channel2 = Graph()
graph_C3 = Graph()

add_lists(ui, graph_Channel1, graph_Channel2, graph_C3,signals)
Graph_connections(graph_Channel1, ui, signals,1)
Graph_connections(graph_Channel2, ui, signals,2)
Graph_connections(graph_C3, ui, signals,3)
all_Channels_connections(graph1=graph_Channel1,graph2=graph_Channel2,graph3=graph_C3,ui=ui,signals=signals)
NonRect_connections(NonRectGraph(ui.nonRect_widget), ui, signals)
general_connections( ui,graph_Channel1,graph_Channel2,graph_C3,signals)
report_connections(ui,signals)
# glue_connections(ui,graph_Channel1,graph_Channel2,graph_C3,signals)



MainWindow.showMaximized()
sys.exit(app.exec())
