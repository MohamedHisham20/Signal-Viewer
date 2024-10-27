from GUI.MainWindow import MainWindow
from GUI.Graph import Graph
from GUI.Signal import Signal
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QPointF
from PySide6.QtCharts import QLineSeries
from Controllers.FileManager import FileManager
from Controllers.GraphController import GraphController
import csv

class WindowManager:
    
    def __init__(self, window:MainWindow):
        self.graphs_and_signals_manager = GraphController()
        self.file_manager = FileManager()
        self.window = window
        
    
    def mount_btns_actions(self):    
        delete_btn = self.file_manager.managed_area.delete_btn
        delete_btn.clicked.connect(self.delete_file)
    
    
    #orange
    def upload_files(self):
        """connected to upload file button
        signals are stored automatically upon uploading their files"""
        
        file_path, _ = QFileDialog.getOpenFileName
        (
            None, 
            "Open CSV File", 
            "", 
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path: self.file_manager.managed_area.uploaded_files.append(file_path)
        self.file_manager.managed_area.signals_counter+=1
        order = self.file_manager.managed_area.signals_counter + 1
        new_signal = Signal(file_path=file_path, order=order)
        self.file_manager.managed_area.uploaded_signals.append(new_signal)
        
        self.store_signal(signal= new_signal)
    
    
    def store_signal(self, signal:Signal):
        self.file_manager.active_file = signal.file_path
        try:
            with open(signal.file_path, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    x, y = float(row[0]), float(row[1])
                    pnt = QPointF(x,y)
                    signal.data_pnts.append(pnt)
        except Exception as e:
                print(f"Error in reading CSV file:{e}")        
    
    
    #orange
    def delete_file(self, file_path:str):
        """connected with delete files button"""
        
        #remove the signal if attached to any graph
        for graph in self.window.graphs.values():
            for signal in graph.signals:
                if file_path == signal.file_path:
                    self.remove_signal_from_graph(graph)
                    
        self.file_manager.managed_area.uploaded_files.remove(file_path)            
    
    
    #orange
    def add_signal_to_graph(self, file_path:str, graph:Graph):
        #check if signal is already added to graph
        for signal in graph.signals:
            if signal.file_path == file_path:
                print("Signal has been added to that graph")
                return
            
        for signal in self.file_manager.managed_area.uploaded_signals:
            if signal.file_path == file_path:
                graph.signals.append(signal)
                
        graph.chart.addSeries(signal.series)
        graph.signals_counter+=1
        
    
    #will receive an index
    def remove_signal_from_graph(self,file_path:str, graph:Graph):
        """Detaches the signal from that graph\n
        The signal can not be drawn again unless attached once again"""
        
        if graph.signals_counter==0:
            print("Graph is empty")
            return
        
        #stops plotting if needed
        if graph.timer.isActive():
            graph.timer.stop()
        
        #get signal from uploaded files
        for signal in self.file_manager.managed_area.uploaded_signals:
            if file_path == signal.file_path:
                graph.signals.remove(file_path)        
        
        
        