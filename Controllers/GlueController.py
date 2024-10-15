import numpy as np
from scipy import interpolate
import sys
import os
import csv
import requests
from io import StringIO
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GUI.UI.Graph import Graph
from PySide6.QtCore import QPointF 
class GlueController:
    def __init__(self):
        pass
  
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
    def process_data(data):
        processed_data = {
            'open': [],
            'high': [],
            'low': [],
            'close': []
        }
        for i, row in enumerate(data):
            y_open = float(row['open'])
            y_high = float(row['high'])
            y_low = float(row['low'])
            y_close = float(row['close'])
            y_open = (y_open - np.min([y_open, y_high, y_low, y_close])) / (np.max([y_open, y_high, y_low, y_close]) - np.min([y_open, y_high, y_low, y_close]))
            y_high = (y_high - np.min([y_open, y_high, y_low, y_close])) / (np.max([y_open, y_high, y_low, y_close]) - np.min([y_open, y_high, y_low, y_close]))
            y_low = (y_low - np.min([y_open, y_high, y_low, y_close])) / (np.max([y_open, y_high, y_low, y_close]) - np.min([y_open, y_high, y_low, y_close]))
            y_close = (y_close - np.min([y_open, y_high, y_low, y_close])) / (np.max([y_open, y_high, y_low, y_close]) - np.min([y_open, y_high, y_low, y_close]))
            processed_data['open'].append([i, y_open])
            processed_data['high'].append([i, y_high])
            processed_data['low'].append([i, y_low])
            processed_data['close'].append([i, y_close])
        return processed_data


    @staticmethod
    def InterPolate_signals(signal1, signal2, order, overlap):
        kinds = ['linear', 'nearest', 'zero', 'slinear', 'quadratic', 'cubic']
        order =int(order)
        order = kinds[order]
        overlap = int(overlap)        
        signal1 = np.array(signal1)
        signal2 = np.array(signal2)
        signal1_normalized = np.linspace(0, 1, len(signal1)) 
        signal2_normalized = np.linspace(0, 1, len(signal2))
        if overlap > 0:
            predict1 = interpolate.interp1d(signal1_normalized, signal1, kind =order, axis=0)
            predict2 = interpolate.interp1d(signal2_normalized, signal2, kind =order,axis=0)
            overlap_x = np.linspace(0, 1, overlap)
            weights1 = np.linspace(1, 0, overlap)  
            weights2 = np.linspace(0, 1, overlap)  
            overlap_section = weights1[:, None] * predict1(overlap_x) + weights2[:, None] * predict2(overlap_x)
            concatenated_signal = np.concatenate((signal1, overlap_section, signal2[overlap:]))
            concatenated_signal = np.unique(concatenated_signal, axis=0)
        else:
            x_values_glued = np.linspace(signal1[-1, 0], signal2[0, 0], -overlap)
            y_values_glued = np.linspace(signal1[-1, 1], signal2[0, 1], -overlap)
            glue_section = np.column_stack((x_values_glued, y_values_glued))
            concatenated_signal = np.concatenate((signal1, glue_section, signal2))
        return concatenated_signal