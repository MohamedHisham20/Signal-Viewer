
from PyQt5.QtWidgets import (QApplication, QMainWindow ,QWidget, QLabel, QLayout, QVBoxLayout,
    QHBoxLayout, QGridLayout, QPushButton, QLineEdit, QGraphicsWidget) 
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter
from PySide6 import QtCharts
import numpy as np
import sys
import os

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_path not in sys.path:
    sys.path.append(project_path)
    
from Controllers.GraphController import Graph    

class window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0,0,500,500)
        self.graph = Graph("test")
        

def main():
    app = QApplication([])
    window = QMainWindow()
    window.show()
    sys.exit(app.exec_());
    

    
main()    