import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel , QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task1")
        self.setGeometry(100, 100, 800, 600)
        #add lable
        self.label = QLabel("Hello World",self)
        self.btn = QPushButton("click" , self)




