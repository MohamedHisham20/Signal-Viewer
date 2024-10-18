from PySide6 import QtCore, QtGui, QtWidgets
from MainWindow import Ui_MainWindow
from NonRectGraphController import NonRectGraph
from Connections import NonRect_connections
import sys
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

ui.Channels.setFixedHeight(400)

NonRect_connections(NonRectGraph(ui.nonRect_widget), ui)

# # Ensure nonRect_widget has a layout
# if ui.nonRect_widget.layout() is None:
#     layout = QtWidgets.QHBoxLayout(ui.nonRect_widget)
#     # layout.setContentsMargins(0, 20, 0, 20)
#     ui.nonRect_widget.setLayout(layout)

# non_rect_graph = NonRectGraph(ui.nonRect_widget)

# ui.nonRect_widget.layout().addWidget(non_rect_graph)

MainWindow.show()
sys.exit(app.exec_())
