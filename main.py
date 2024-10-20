from PySide6 import QtCore, QtGui, QtWidgets
from MainWindow import DragDropList, Ui_MainWindow
from NonRectGraphController import NonRectGraph
from Connections import (
    NonRect_connections,
    Graph_connections,
    all_channels_connections,
    add_lists,
    general_connections,
)
import sys
from Signal import Signal
from Graph import Graph
import random
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

ui.Channels.setFixedHeight(400)
signals = Signal.get_all_signals(True)

graph_C1 = Graph()
graph_C2 = Graph()
graph_C3 = Graph()

add_lists(ui, graph_C1, graph_C2, graph_C3,signals)
Graph_connections(graph_C1, ui, signals,1)
Graph_connections(graph_C2, ui, signals,2)
Graph_connections(graph_C3, ui, signals,3)
all_channels_connections(graph1=graph_C1,graph2=graph_C2,graph3=graph_C3,ui=ui,signals=signals)
NonRect_connections(NonRectGraph(ui.nonRect_widget), ui, signals)
general_connections( ui,graph_C1,graph_C2,graph_C3,signals)

# graph_C1.plot_real_time()
# Qtimer = QtCore.QTimer()
# Qtimer.timeout.connect(lambda: graph_C1.update_real_time(random.uniform(0, 1)))
# Qtimer.start(1000)


MainWindow.show()
sys.exit(app.exec())
