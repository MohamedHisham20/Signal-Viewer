from PySide6.QtWidgets import QWidget, QVBoxLayout

from GUI.UI.UI_root_widget import Ui_root_widget
from GUI.GraphWidget import GraphWidget
from GUI.ControlsWidget import ControlsWidget


class RootWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_root_widget()
        self.ui.setupUi(self)
        self.ui.new_graph_btn.clicked.connect(self.add_graph)
        self.graphs = []

        self.controls_widget = ControlsWidget(self)

        controls_placeholder_widget = self.ui.controls_widget
        if controls_placeholder_widget.layout() is None:
            placeholder_layout = QVBoxLayout()
            controls_placeholder_widget.setLayout(placeholder_layout)

        graph_placeholder_widget = self.ui.graph_placeholder_widget
        if graph_placeholder_widget.layout() is None:
            placeholder_layout = QVBoxLayout()
            graph_placeholder_widget.setLayout(placeholder_layout)

        controls_placeholder_widget.layout().addWidget(self.controls_widget)

        self.add_graph()
        self.add_graph()

    def add_graph(self):
        graph_widget = GraphWidget(self)
        self.graphs.append(graph_widget)
        self.ui.graph_placeholder_widget.layout().addWidget(graph_widget)

    # Reordering doesn't work :(
    # def dragEnterEvent(self, event):
    #     if event.mimeData().hasText():
    #         event.acceptProposedAction()
    #
    # def dropEvent(self, event):
    #     if event.mimeData().hasText():
    #         print("here")
    #         widget_name = event.mimeData().text()
    #         graph = None
    #         for graph in self.graphs:
    #             if graph.objectName() == widget_name:
    #                 self.graphs.remove(graph)
    #                 break
    #
    #         layout = self.ui.graph_placeholder_widget.layout()
    #         for i in range(layout.count()):
    #             _widget = layout.itemAt(i).widget()
    #             if _widget is graph:
    #                 layout.removeWidget(graph)
    #                 layout.addWidget(graph, i)
    #                 break
    #
    #         event.acceptProposedAction()
