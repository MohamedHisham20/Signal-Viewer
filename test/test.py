from PySide6.QtWidgets import (QApplication, QMainWindow ,QWidget, QLabel, QVBoxLayout,
QHBoxLayout, QPushButton ,QScrollBar)
from PySide6.QtCore import Qt 
from PySide6.QtCharts import QChart, QChartView, QLineSeries
import numpy as np
import sys
import csv
import os
  
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))              
from Controllers.GraphController import Graph

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
    file_path = r".C:\Users\moham\OneDrive\Desktop\Boda\CUFE\SBE 3\Projects\DSP\Signal_Viewer\Signal-Viewer\signal.csv"
    try:
        window.graph.draw_signal(file_path)
        print("Signal drawn successfully.")
    except Exception as e:
        print(f"Error drawing signal: {e}")
    sys.exit(app.exec())

      
main()    