from PySide6 import QtCore, QtGui, QtWidgets
from MainWindow import DragDropList, Ui_MainWindow
from NonRectGraphController import NonRectGraph
from Connections import (
    NonRect_connections,
    Graph_connections,
    all_channels_connections,
    # drag_drop_list_connections,
    general_connections,
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

# ui.C1_list.addItems([signal.label for signal in signals])
graph_C1 = Graph()
graph_C2 = Graph()
graph_C3 = Graph()
horizontalLayout = QtWidgets.QHBoxLayout()
ui.horizontalLayout.setObjectName("horizontalLayout")
ui.C1_list = DragDropList()
ui.C1_list.setupParameters(ui, graph_C1, graph_C2, graph_C3)
ui.C1_list.setObjectName("C1_list")
ui.horizontalLayout.addWidget(ui.C1_list)
ui.C2_list = DragDropList()
ui.C2_list.setupParameters(ui, graph_C1, graph_C2, graph_C3)
ui.C2_list.setObjectName("C2_list")
ui.horizontalLayout.addWidget(ui.C2_list)
ui.C3_list = DragDropList()
ui.C3_list.setupParameters(ui, graph_C1, graph_C2, graph_C3)
ui.C3_list.setObjectName("C3_list")
ui.horizontalLayout.addWidget(ui.C3_list)
ui.verticalLayout_13.addLayout(ui.horizontalLayout)
ui.verticalLayout_4.addLayout(ui.verticalLayout_13)
ui.C1_widget.layout().addWidget(graph_C1.plot_widget)
ui.C2_widget.layout().addWidget(graph_C2.plot_widget)
ui.C3_widget.layout().addWidget(graph_C3.plot_widget)

Graph_connections(graph_C1, ui, signals,1)
Graph_connections(graph_C2, ui, signals,2)
Graph_connections(graph_C3, ui, signals,3)
all_channels_connections(graph1=graph_C1,graph2=graph_C2,graph3=graph_C3,ui=ui,signals=signals)
# drag_drop_list_connections(ui,graph_C1,graph_C2,graph_C3)
NonRect_connections(NonRectGraph(ui.nonRect_widget), ui, signals)
general_connections( ui,graph_C1,graph_C2,graph_C3,signals)

MainWindow.show()
sys.exit(app.exec())
