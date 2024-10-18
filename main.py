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

MainWindow.show()
sys.exit(app.exec_())
