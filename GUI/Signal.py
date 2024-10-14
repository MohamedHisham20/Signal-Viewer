from PySide6.QtCore import QPointF
from PySide6.QtCharts import QLineSeries, QChart 
from typing import Optional, List, Tuple

class Signal():
    def __init__(self, ID:int, data_pnts:List[Tuple], label:str = None):
        self.ID = ID
        self.label = label
        self.data_qpnts:List[QPointF] = [] 
        
        for pnt in data_pnts:
            x,y = pnt[0], pnt[1]
            qpnt = QPointF(x,y)
            self.data_qpnts.append(qpnt)
        
        
        
        