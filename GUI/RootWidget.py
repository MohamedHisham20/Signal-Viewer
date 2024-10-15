from PySide6.QtWidgets import QWidget, QVBoxLayout, QFileDialog

from GUI.UI.UI_root_widget import Ui_root_widget
from GUI.GraphWidget import GraphWidget
from GUI.ControlsWidget import ControlsWidget
from GUI.Signal import Signal
from Controllers.NonRectGraphController import NonRectGraph
import Glue_popup

class RootWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_root_widget()
        self.ui.setupUi(self)
        self.ui.new_graph_btn.clicked.connect(self.add_graph)
        
        self.graphs = []
        
        self.controls_widget = ControlsWidget(self)
        self.controls_widget.ui.glue_btn.clicked.connect(self.show_glue_popup)
        self.non_rect_graph = NonRectGraph(self)

        controls_placeholder_widget = self.ui.controls_widget
        if controls_placeholder_widget.layout() is None:
            placeholder_layout = QVBoxLayout()
            controls_placeholder_widget.setLayout(placeholder_layout)

        graph_placeholder_widget = self.ui.graph_placeholder_widget
        if graph_placeholder_widget.layout() is None:
            placeholder_layout = QVBoxLayout()
            graph_placeholder_widget.setLayout(placeholder_layout)

        non_rect_graph_widget = self.ui.non_rectangle_graph_widget
        if non_rect_graph_widget.layout() is None:
            placeholder_layout = QVBoxLayout()
            non_rect_graph_widget.setLayout(placeholder_layout)

        controls_placeholder_widget.layout().addWidget(self.controls_widget)
        non_rect_graph_widget.layout().addWidget(self.non_rect_graph)

        self.add_graph()
        self.add_graph()

    def add_graph(self):
        graph_widget = GraphWidget(self)
        graph_widget.swapAction = self.swap
        self.graphs.append(graph_widget)
        self.ui.graph_placeholder_widget.layout().addWidget(graph_widget)

    def swap(self):
        print("done")
        for graph in self.graphs:
            if graph.ChangeOrder == 'up':
                graph.ChangeOrder = 'no'
                self.swapwithuppergraph(graph)
            elif graph.ChangeOrder == 'down':
                self.swapwithlowergraph(graph)
                graph.ChangeOrder = 'no'
        

    def swapwithuppergraph(self, graph):
        print("swapwithuppergraph")
        layout = self.ui.graph_placeholder_widget.layout()
        for i in range(layout.count()):
            _widget = layout.itemAt(i).widget()
            if _widget is graph:
                # Ensure i-1 is within bounds
                if i > 0:
                    layout.insertWidget(i-1, graph)
                break

    def swapwithlowergraph(self, graph):
        print("swapwithlowergraph")
        layout = self.ui.graph_placeholder_widget.layout()
        for i in range(layout.count()):
            _widget = layout.itemAt(i).widget()
            if _widget is graph:
                # Ensure i+1 is within bounds
                if i < layout.count() - 1:
                    layout.insertWidget(i+1, graph)
                break
            
    def swap(self):
        for graph in self.graphs:
            if graph.ChangeOrder == 'up':
                self.swapwithuppergraph(graph)
                graph.ChangeOrder = 'no'
            elif graph.ChangeOrder == 'down':
                self.swapwithlowergraph(graph)
                graph.ChangeOrder = 'no'

    def load_signal(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Open Signal File", "", "CSV Files (*.csv);;All Files (*)")
        signal = Signal.from_file(file_path)
        self.controls_widget.add_signal(signal)
        return signal

    def show_glue_popup(self):
        # signal1 = [[0, 0], [1, 3], [2, 4]]
        # signal2 = [[0, 5], [1, 6], [2, 7]]
        # sinusoidal signals
        signal1 = [[i, 5 * np.sin(i)] for i in range(5)]
        signal2 = [[i, 5 * np.cos(i)] for i in range(5)]
        glue_popup = Glue_popup.GlueSignalsPopup(signal1, signal2, None, None, self)
        glue_popup.exec()
