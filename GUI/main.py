from PySide6.QtGui import QDrag
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QFrame
from PySide6.QtCore import Qt, QMimeData, QPoint

from UI_root_widget import Ui_root_widget
from UI_controls_widget import Ui_Controls_Widget
from UI_graph_widget import Ui_graph_widget


class ControlsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Controls_Widget()
        self.ui.setupUi(self)


class GraphWidget(QWidget):
    instance_count = 0

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_graph_widget()
        self.ui.setupUi(self)
        GraphWidget.instance_count += 1
        self.setObjectName(f"graph_widget_{GraphWidget.instance_count}")
        self.ui.graph_title_lbl.setText(f"Graph {GraphWidget.instance_count}")
        self.drag_start_position = None
        self.is_dragging = False

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.ui.reorder_label.geometry().contains(event.position().toPoint()):
                self.drag_start_position = event.position().toPoint()
                self.is_dragging = True

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_start_position is not None and self.is_dragging:
            if (event.position() - self.drag_start_position).manhattanLength() >= QApplication.startDragDistance():
                mime_data = QMimeData()
                mime_data.setText(self.objectName())
                drag = QDrag(self)
                drag.setMimeData(mime_data)

                pixmap = self.grab()
                drag.setPixmap(pixmap)
                drag.setHotSpot(event.position().toPoint() - self.rect().topLeft())

                drag.exec(Qt.MoveAction)
                self.is_dragging = False

    def mouseReleaseEvent(self, event):
        self.is_dragging = False
        self.drag_start_position = None

    def dropEvent(self, event):
        if event.mimeData().hasText():
            event.accept()


class MainWindow(QWidget):
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

    def update_graphs(self):
        graph_placeholder_widget = self.ui.graph_placeholder_widget
        if graph_placeholder_widget.layout() is None:
            placeholder_layout = QVBoxLayout()
            graph_placeholder_widget.setLayout(placeholder_layout)

        for i in reversed(range(graph_placeholder_widget.layout().count())):
            widget_to_remove = graph_placeholder_widget.layout().itemAt(i).widget()
            if widget_to_remove:
                widget_to_remove.setParent(None)

        for graph in self.graphs:
            graph_placeholder_widget.layout().addWidget(graph)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            print("here")
            widget_name = event.mimeData().text()
            graph = None
            for graph in self.graphs:
                if graph.objectName() == widget_name:
                    self.graphs.remove(graph)
                    break

            layout = self.ui.graph_placeholder_widget.layout()
            for i in range(layout.count()):
                _widget = layout.itemAt(i).widget()
                if _widget is graph:
                    layout.removeWidget(graph)
                    layout.addWidget(graph, i)
                    break

            event.acceptProposedAction()


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()
    app.exec()
