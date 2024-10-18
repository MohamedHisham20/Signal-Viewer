from PySide6 import QtCore, QtGui, QtWidgets
from MainWindow import Ui_MainWindow
from NonRectGraphController import NonRectGraph
from Connections import NonRect_connections
import sys
from Signal import Signal

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

ui.Channels.setFixedHeight(400)
signals = Signal.get_all_signals()
ui.C1_list.addItems([signal.label for signal in signals])

NonRect_connections(NonRectGraph(ui.nonRect_widget), ui, signals)

MainWindow.show()
sys.exit(app.exec_())
