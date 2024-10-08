from PySide6.QtWidgets import (QApplication, QMainWindow ,QWidget, QLabel, QVBoxLayout,
QHBoxLayout, QPushButton ,QScrollBar)
from PySide6.QtCore import Qt 
from PySide6.QtCharts import QChart, QChartView, QLineSeries
import numpy as np
import sys
import csv
  
import GUI              

class MainWindow(QMainWindow):
    def __init__(self,name:str):
        super().__init__()
        self.setGeometry(0,0,500,500)
        self.setWindowTitle(name)  
        self.graph = Graph("This Label should display the graph name")
        self.setCentralWidget(self.graph)
 
def main():
    app = QApplication([])
    window = MainWindow("test window")
    window.show()
    sys.exit(app.exec())

      
main()    