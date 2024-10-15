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
        """
        Interpolates or glues two signals, averaging overlapping points.

        Parameters:
        signal1 (array-like): First signal to glue.
        signal2 (array-like): Second signal to glue.
        order (int): Interpolation order (not used in the non-scipy version).
        overlap (int): Number of overlapping points.

        Returns:
        np.array: Glued signal with averaged overlap.
        """
        signal1 = np.array(signal1)
        signal2 = np.array(signal2)
        
        if overlap > 0:
            # Get the non-overlapping portions of each signal
            non_overlap_signal1 = signal1[:-overlap]
            non_overlap_signal2 = signal2[overlap:]

            # Averaging the overlapping region
            overlapped_avg = (signal1[-overlap:] + signal2[:overlap]) / 2
            
            # Concatenate the signals
            concatenated_signal = np.concatenate((non_overlap_signal1, overlapped_avg, signal2[overlap:]))
        else:
            # In case of negative overlap (gap), we create a linear bridge between the end of signal1 and start of signal2
            gap = -overlap
            x_values_glued = np.linspace(signal1[-1, 0], signal2[0, 0], gap)
            y_values_glued = np.linspace(signal1[-1, 1], signal2[0, 1], gap)
            
            # Stack x and y glued values to form the bridge
            glue_section = np.column_stack((x_values_glued, y_values_glued))
            
            # Concatenate signal1, bridge (glue_section), and signal2
            concatenated_signal = np.concatenate((signal1, glue_section, signal2))

        return concatenated_signal
