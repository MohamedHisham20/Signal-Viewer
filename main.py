import sys
from PyQt5.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task1")
        self.setGeometry(100, 100, 800, 600)


app = QApplication(sys.argv)    
window = MainWindow()
window.show()
sys.exit(app.exec_())

