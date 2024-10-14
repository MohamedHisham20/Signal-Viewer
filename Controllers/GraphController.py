from PySide6.QtWidgets import (QFileDialog)
from PySide6.QtCore import QPointF
import sys
import csv
import os

from GUI.UI.Graph import Graph
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))              

                       
class GraphController:
    """Methods marked with double underscore (__) as a prefix
    are of internal behaviour and should not be accessed by other developers
    outside this class.\n\n
    Hover over a function name for info
    """        
    @staticmethod
    def connect_btns_actions(graph:Graph):
        graph.upload_btn.clicked.connect(lambda:GraphController.upload_signal_file(graph))
        graph.play_pause_btn.clicked.connect(lambda:GraphController.toggle_play_pause_btn(graph))
        
    @staticmethod
    def upload_signal_file(graph:Graph):
        """loads a csv file\n
        connected with upload button"""        
        file_path, _ = QFileDialog.getOpenFileName(None, "Open Signal File", "", "CSV Files (*.csv);;All Files (*)")
        
        if file_path in graph.uploaded_files:
            print("File already exists")
            return
        
        if file_path:
            graph.uploaded_files.append(file_path)
            graph.active_file = file_path
            GraphController.load_signal(graph, file_path)
        else: print("Error in uploading file")    
    
    
    @staticmethod
    def delete_file(graph:Graph,file_path:str):
        """connected with delete button"""
        if not file_path in graph.uploaded_files:
            print("File does not exist already")
            return
        graph.uploaded_files.remove(file_path)

    def load_signal_fromNP(graph:Graph,signal):
        """Loads the signal data points into graph\n
        """
        if GraphController.is_graph_loaded(graph):
            GraphController.unload_signal(graph)
         
        try:
            for row in signal:
                x, y = float(row[0]), float(row[1])
                pnt = QPointF(x,y)
                graph.data_pnts.append(pnt)
            graph.is_loaded =True    
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
        
        GraphController.__play_loaded_signal(graph,interval=100)
        graph.signal_is_running = True
    
    
    @staticmethod
    def load_signal(graph:Graph,file_path:str):
        """Loads the signal data points into graph\n
        """
        if GraphController.is_graph_loaded(graph):
            GraphController.unload_signal(graph)
         
        try:
            with open(file_path, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    x, y = float(row[0]), float(row[1])
                    pnt = QPointF(x,y)
                    graph.data_pnts.append(pnt)
                graph.is_loaded =True    
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
        
        GraphController.__play_loaded_signal(graph)
        graph.signal_is_running = True    
            
    @staticmethod        
    def unload_signal(graph:Graph):
        """clears the graph from the previous loaded signal\n
        but does not delete the signal file\n
        connected with reset button"""
        graph.series.clear()
        graph.is_loaded = False
    
        
    @staticmethod
    def is_graph_loaded(graph:Graph):
        """checks if a graph has been loaded with a signal"""
        return graph.is_loaded
    
    
    staticmethod
    def get_loaded_files(graph:Graph):
        """returns a list of all csv files uploaded by the user"""
        return graph.uploaded_files
    
    
    @staticmethod
    def get_active_file(graph:Graph):
        """returns the file path of the current active file"""
        return graph.active_file
    
    
    @staticmethod
    def toggle_play_pause_btn(graph:Graph):
        """Cotrols playing and pausing\n
        connected to play and pause button"""
        if not graph.is_loaded: return
            
        if graph.timer.isActive():
            graph.timer.stop()
            graph.play_pause_btn.setText("play")
            graph.signal_is_running = False
        else:
            graph.timer.start(graph.timer.interval())
            graph.play_pause_btn.setText("pause")
            graph.signal_is_running = True     

    @staticmethod
    def replay_signal(graph:Graph,interval:int=5):
        """connected with replay button"""
        if not GraphController.is_graph_loaded(graph):
            print("Load a signal first")
            return
        
        GraphController.__play_loaded_signal(graph)

 
    @staticmethod
    def increase_plotting_speed(graph:Graph):
        """connected with + button"""
        GraphController.__control_speed(graph,graph.delta_speed)
    
    
    @staticmethod
    def decrease_plotting_speed(graph:Graph):
        """connected with - button"""
        GraphController.__control_speed(graph, -(graph.delta_speed)) 
    

    @staticmethod
    def __play_loaded_signal(graph:Graph,interval:int =5):
        """plots the signal of the active file\n
        The interval controls the plotting speed.\n
        smaller intervals correspond to faster plotting\n
        """
        if not GraphController.is_graph_loaded(graph):
            print("Load a signal first")
            return  
        graph.chart.addSeries(graph.series)
        graph.signal_curr_indx=0
        
        graph.chart.setAxisX(graph.x_axis, graph.series)
        graph.chart.setAxisY(graph.y_axis, graph.series)
        
        GraphController.__set_full_view_port(graph)
                
        graph.timer.timeout.connect(lambda: GraphController.__animate_signal(graph))
        graph.timer.start(interval)
        GraphController.__animate_signal(graph)

    
    @staticmethod
    def __animate_signal(graph:Graph):
        if graph.signal_curr_indx < len(graph.data_pnts):
            graph.series.append(graph.data_pnts[graph.signal_curr_indx])
            graph.signal_curr_indx += 1
        else:
            graph.timer.stop()
    
    
    @staticmethod
    def __set_full_view_port(graph: Graph):
        """Sets the view port to fit the whole signal in real time\n
        No need for the user to pan the signal.
        """
        if not graph.data_pnts:
            return

        x_min = graph.data_pnts[0].x()
        x_max = graph.data_pnts[-1].x()

        y_values = [point.y() for point in graph.data_pnts]
        y_min = min(y_values) if y_values else 0
        y_max = max(y_values) if y_values else 0

        graph.chart.axisX().setRange(x_min, x_max)
        graph.chart.axisY().setRange(y_min, y_max)
        
            
    @staticmethod
    def __control_speed(graph:Graph, delta_speed:int):
        current_interval = graph.timer.interval()
        if delta_speed > 0 : 
            new_interval = max(graph.min_plotting_interval, current_interval+delta_speed)
        else : new_interval = min(graph.max_plotting_interval, current_interval+delta_speed)
        graph.timer.setInterval(new_interval)
        
        

        