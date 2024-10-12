import numpy as np
from scipy import interpolate
import sys
import os
import csv
import requests
from io import StringIO
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from GUI.glueWindow import glueWindow
from GUI.UI.Graph import Graph
from PySide6.QtCore import QPointF 
class GlueController:
    def __init__(self):
        self.signals = [np.linspace(0,1,100),np.linspace(0,1,100)]
        self.signal1=self.signals[0]
        self.signal2=self.signals[1]
        self.order=1
        self.overlap=0
        self.signal1_start=0
        self.signal2_start=0
        self.signal1_size=100
        self.signal2_size=100
    def setdefaults(self,window : glueWindow):
        window.comboBox_signal1.addItems(["signal1","signal2"])
        window.comboBox_signal2.addItems(["signal1","signal2"])
        window.spinBox_order.setValue(1)
        window.spinBox_overlap.setValue(0)
        window.spinBox_start1.setValue(0)
        window.spinBox_start2.setValue(0)
        window.spinBox_size1.setValue(100)
        window.spinBox_size2.setValue(100)
    
    def ComboBox_signal1(self,window : glueWindow):
        self.signal1 = self.signals[window.comboBox_signal1.currentIndex()]
    def ComboBox_signal2(self,window : glueWindow):
        self.signal2 = self.signals[window.comboBox_signal2.currentIndex()]
    def SpinBox_start1(self,window : glueWindow):
        self.signal1_start = window.spinBox_start1.value()
    def SpinBox_start2(self,window : glueWindow):
        self.signal2_start = window.spinBox_start2.value()
    def SpinBox_size1(self,window : glueWindow):
        self.signal1_size = window.spinBox_size1.value()
    def SpinBox_size2(self,window : glueWindow):
        self.signal2_size = window.spinBox_size2.value()
    def SpinBox_overlap(self,window : glueWindow):
        self.overlap = window.spinBox_overlap.value()
    def SpinBox_order(self,window : glueWindow):
        self.order = window.spinBox_order.value()
    def is_make_report(self,window : glueWindow):
        if window.checkBox.isChecked():
            return True
        return False
    @staticmethod
    def real_time_signal():
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo&datatype=csv"
        response = requests.get(url)    
        if response.status_code == 200:
            csv_content = response.content.decode('utf-8')
            csv_reader = csv.DictReader(StringIO(csv_content))
            data = [row for row in csv_reader]        
            return data
        else:
            raise Exception(f"Failed to fetch data: {response.status_code}")
        
    @staticmethod
    def process_signal_data(data):
        graphs = [Graph() for _ in range(5)]
        for idx, row in enumerate(data):
            x = idx 
            for i, key in enumerate(['open', 'high', 'low', 'close', 'volume']):
                y = float(row[key])  
                pnt = QPointF(x, y)
                graphs[i].data_pnts.append(pnt)  
        return graphs

    def InterPolate_signals(self,
    signal1,
    signal2,
    order,
    overlap,
    signal1_start,
    signal2_start ,
    signal1_size,
    signal2_size):
    
        signal1 = signal1[signal1_start:signal1_start+signal1_size]
        signal2 = signal2[signal2_start:signal2_start+signal2_size]

        signal1_normlized = np.linspace(0,1,signal1) 
        signal2_normlized = np.linspace(0,1,signal2)
        x_values_glued = np.empty()
        if overlap > 0:
            x_values_glued = np.linspace(signal1_normlized[-1],signal2_normlized[0],overlap)
        else: 
            x_values_glued = np.linspace(signal1_normlized[-overlap],signal2_normlized[overlap], -overlap)

        predict1 = interpolate.interp1d(signal1_normlized,signal1,kind=order)
        predict2 = interpolate.interp1d(signal2_normlized,signal2,kind=order)
        signal_glued = predict1(x_values_glued) + predict2(x_values_glued)
        concatenated_signal = np.concatenate((signal1,signal_glued,signal2))

        return concatenated_signal