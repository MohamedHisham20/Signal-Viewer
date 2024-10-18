import pyqtgraph as pg
from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPen
from typing import List, Dict, Tuple
import sys
import os
import numpy as np


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))


class Signal():
    def __init__(self, ID:int, x_pnts:list, y_pnts:List):
        self.ID = ID
        self.X = x_pnts 
        self.Y = y_pnts
        

class Graph(QWidget):
    def __init__(self, ID:int, label:str=None):    
        super().__init__()
        self.show() 
        #self.setGeometry(500, 0, 200, 200)
        self.setWindowTitle(label)
        
        self.ID = ID
        self.plotArea = pg.PlotWidget()
        self.internalLayout = QVBoxLayout(self)
        self.controllers = QWidget()
        self.controllersLayout = QHBoxLayout(self.controllers)
        self.timer = QTimer()
        self.timer.timeout.connect(self.plotSignals)
        self.deltaInterval = 10
        self.minInterval = 10
        self.maxInterval = 100
        self.timer.setInterval(50)
        self.signals: List[Signal] = []
        
        #Self States
        self.plottingIndex = 0
        self.selectionRequested = False
        self.plottingStarted = False
        self.minYFromSignals = 0
        self.MaxYFromSignals = 0
        self.maxXFromSignals = 0
        self.maxXPerCurrPlottingIndex =0
        self.allSignalsPlotted = False
        self.minYSignal:Signal = None
        self.maxYSignal: Signal = None
        self.maxXSignal: Signal= None

        #Plot Widget Setup
        self.plotItem = self.plotArea.plotItem
        self.viewBox= self.plotArea.plotItem.getViewBox()
        
        self.plotItem.setTitle(title=label)
        self.plotItem.setLabel(axis='left', text="Y-Axis")
        self.plotItem.setLabel(axis='bottom', text="X-Axis")
            
        self.viewBox.setXRange(min=0,max=self.maxXFromSignals)
        self.viewBox.enableAutoRange(axis=self.viewBox.XAxis, enable=True)
        self.viewBox.enableAutoRange(axis=self.viewBox.YAxis, enable=False)
        
        #self.viewBox.setLimits(xMin=0,xMax=self.maxXPerCurrPlottingIndex, yMin=self.minYFromSignals, yMax=self.MaxYFromSignals)
        self.viewBox.setAutoPan(x=True, y=True)
        self.viewBox.setMouseEnabled(x=True, y=True)
        
        self.ROI = pg.RectROI(pos=[0,0], size=[0,0])
        self.ROI.setPen(width=4.5, color="#16adee")
        self.plotItem.addItem(self.ROI)
        self.ROI.hide()
        self.ROI.sigRegionChanged.connect(self.selectSignalPoints)
        
        # Controllers Setup
        self.playPauseBtn = QPushButton("play",self)
        self.replayBtn = QPushButton("replay",self)
        self.speedUpBtn = QPushButton("speed up",self)
        self.slowDownBtn = QPushButton("slow down",self)
        
        # LayoutSetup
        self.controllersLayout.addWidget(self.playPauseBtn)
        self.controllersLayout.addWidget(self.replayBtn)
        self.controllersLayout.addWidget(self.speedUpBtn)
        self.controllersLayout.addWidget(self.slowDownBtn)
        
        self.layout().addWidget(self.plotArea)
        self.layout().addWidget(self.controllers)
        
        self.mountBtnsActions()
        self.plotItem.showGrid(x=True, y=True)
        
        
    def addSignal(self, signal:Signal):
        self.signals.append(signal)
        signal_item = pg.PlotDataItem([], [])
        signal_item.opts["name"] = str(signal.ID)
        self.plotArea.plotItem.addItem(signal_item)
        
        minY = min(signal.Y)
        maxY = max(signal.Y)
        maxX = max(signal.X)
        
        if minY < self.minYFromSignals:
            self.minYFromSignals = minY
            self.minYSignal = signal
            
        if maxY > self.MaxYFromSignals:
            self.MinYFromSignals = maxY
            self.maxYSignal = signal
            
        if maxX > self.maxXFromSignals:
            self.maxXFromSignals = maxX
            self.maxXSignal = signal                

           
    def getSignal(self, signalID:str):
        """return the signal index in the graph and signal object"""
        
        for index, signal in enumerate(self.signals):
            if signalID == str(signal.ID):
                    return index, signal
    
    
    def deleteSignalFromGraph(self, signalID:str):
        index, signal = self.getSignal(signalID)
        for signal_item in self.plotArea.plotItem.dataItems:
            if isinstance(signal_item, pg.PlotDataItem):
                if signal_item.name() == signalID:
                    self.plotArea.plotItem.removeItem(signal_item) 
        self.signals.remove(signal)
    
                                    
    def clearDataItems(self):
        for signal_item in self.plotArea.plotItem.dataItems:
            if isinstance(signal_item, pg.PlotDataItem):
                signal_item.clear()
    
    
    def showSignal(self, signalID:str, hideOtherSignals = False):
        for signalItem in self.plotArea.plotItem.dataItems:
            if isinstance(signalItem, pg.PlotDataItem):
                if signalItem.name() == signalID: signalItem.show()
                else: 
                    if hideOtherSignals: signalItem.hide()
                
    
    def hideSignal(self, signalID:str, showOtherSignals=False):
        for signalItem in self.plotArea.plotItem.dataItems:
            if isinstance(signalItem, pg.PlotDataItem):
                if signalItem.name() == signalID: signalItem.hide()
                else:
                    if showOtherSignals: signalItem.show()    
                                               
    
    def togglePlayPauseBtn(self):
        """Cotrols playing and pausing\n
        connected to play and pause button\n"""
        
        if len(self.signals) == 0: 
            print("Graph is empty. Add a signal first")
            return        
            
        self.playPauseBtn.show()
        if self.timer.isActive():
            self.timer.stop()
            self.playPauseBtn.setText("play")
        else:
            self.playPauseBtn.setText("pause")
            self.timer.start(self.timer.interval())
            
            if self.plottingStarted==False: 
                self.clearDataItems()
                self.allSignalsPlotted = False
                self.plottingIndex = 0
                self.plottingStarted = True
                self.viewBox.setXRange(min=0, max=1)
                self.plotSignals()
                
                
    def plotSignals(self):
        self.viewBox.setLimits(xMin=0, xMax=self.maxXPerCurrPlottingIndex, yMin=self.minYFromSignals, yMax=self.MaxYFromSignals)
        self.viewBox.setYRange(self.minYFromSignals, self.MaxYFromSignals)
        
        allPlotted = True
        
        for index, signal_item in enumerate(self.plotArea.plotItem.dataItems):
            if isinstance(signal_item, pg.PlotDataItem):  
                if self.plottingIndex < len(self.signals[index].X):
                    signal_item.setData(self.signals[index].X[:self.plottingIndex], self.signals[index].Y[:self.plottingIndex])
                    self.maxXPerCurrPlottingIndex = max(self.signals[index].X[self.plottingIndex], self.maxXPerCurrPlottingIndex)
                    self.viewBox.setLimits(xMax=self.maxXPerCurrPlottingIndex)
                    allPlotted = False
        
        self.plottingIndex += 1
        if allPlotted:
            self.timer.stop()
            self.plottingStarted = True
            self.playPauseBtn.hide()
                  
    
    def replay(self):
        """clear plotted signals to start plotting again automatically\n
        for clearing graph and replaying upon user pressing play again:\n
        see resetGraph method"""
        if not self.plottingStarted or len(self.signals)==0:
            return
        
        self.timer.stop()
        self.plottingStarted = False
        self.togglePlayPauseBtn()
    
    
    def resetGraph(self):
        """clear plotted signals to start plotting again\n
        won't start unless play is pressed again"""
        
        if not self.plottingStarted or len(self.signals)==0:
            return
        
        self.timer.stop()
        self.plottingStarted = False
    
    
    def increasePlottingSpeed(self):
        currentInterval = self.timer.interval()
        newInterval = min(self.minInterval, currentInterval-self.deltaInterval)
        self.timer.setInterval(newInterval)
        
    
    def decreasePlottingSpeed(self):
        currentInterval = self.timer.interval()
        newInterval = max(self.maxInterval, currentInterval + self.deltaInterval)
        self.timer.setInterval(newInterval)
            
    
    def restrictPanningAndZooming(self):
        self.viewBox.setLimits(xMax=self.maxXPerCurrPlottingIndex, 
        maxXRange=self.maxXPerCurrPlottingIndex)    
    
    
    def selectSignalPoints(self, signalID:str):
        """returns two lists for the selected points"""
        
        index, selectedSignalItem = self.getSignal()
        self.showSignal(signalID=signalID, hideOtherSignals=True)
        
        if isinstance(selectedSignalItem, pg.PlotDataItem):
            X = list(selectedSignalItem.xData)
            Y = list(selectedSignalItem.yData)
        
        ROIBounds = self.ROI.boundingRect()
        xLeft = ROIBounds.left()
        xRight = ROIBounds.right()
        yBottom = ROIBounds.bottom()
        yTop = ROIBounds.top()
        
        selectedX, selectedY = [], []
        
        for i, x in enumerate(x):
            y = Y[i]
            if (x<=xLeft and x>=xRight) and (y<=yTop and y>=yBottom):       
                selectedX.append(x)
                selectedY.append(y)
                
        return selectedX, selectedY            
                
    
    def mountBtnsActions(self):        
        self.playPauseBtn.clicked.connect(self.togglePlayPauseBtn)
        self.replayBtn.clicked.connect(self.replay)
        self.speedUpBtn.clicked.connect(self.increasePlottingSpeed)
        self.slowDownBtn.clicked.connect(self.decreasePlottingSpeed)                                          