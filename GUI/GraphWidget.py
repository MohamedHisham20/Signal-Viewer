from PySide6.QtGui import QDrag, QIcon
from PySide6.QtWidgets import QApplication, QWidget, QMenu, QVBoxLayout
from PySide6.QtCore import Qt, QMimeData

from GUI.UI.UI_graph_widget import Ui_graph_widget
from GUI.UI.Graph import Graph
from Controllers.GraphController import GraphController


class GraphWidget(QWidget):
    instance_count = 0

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_graph_widget()
        self.ui.setupUi(self)

        self.playing_state = True
        self.play_icon = QIcon('./Icons/play.png')
        self.pause_icon = QIcon('./Icons/pause.png')

        self.graphController = GraphController()
        self.graph = Graph()
        if self.ui.graph_placeholder.layout() is None:
            self.ui.graph_placeholder.setLayout(QVBoxLayout())
        self.ui.graph_placeholder.layout().addWidget(self.graph)

        GraphWidget.instance_count += 1
        self.setObjectName(f"graph_widget_{GraphWidget.instance_count}")
        self.ui.graph_title_lbl.setText(f"Graph {GraphWidget.instance_count}")

        self.drag_start_position = None
        self.is_dragging = False
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.connect_buttons()

    def connect_buttons(self):
        self.ui.pause_play_btn.clicked.connect(lambda: self.toggle_pause_play())
        self.ui.fast_backward_btn.clicked.connect(lambda: self.graphController.increase_plotting_speed(self.graph))
        self.ui.fast_forward_btn.clicked.connect(lambda: self.graphController.decrease_plotting_speed(self.graph))
        # self.ui.beginning_btn.clicked.connect(lambda: self.graphController.pan_to_start(self.graph))
        # self.ui.end_btn.clicked.connect(lambda: self.graphController.pan_to_end(self.graph))

    def show_context_menu(self, position):
        menu = QMenu(self)
        change_title = menu.addAction("Change Title")
        menu.addSeparator()

        add_signal_submenu = QMenu("Add Signal", self)
        signal_from_file = add_signal_submenu.addAction("From File")
        signal_from_web = add_signal_submenu.addAction("From the Web")
        menu.addMenu(add_signal_submenu)
        menu.addSeparator()

        pause_play = menu.addAction("Pause/Play")
        speed_up = menu.addAction("Speed Up")
        slow_down = menu.addAction("Slow Down")
        pan_begin = menu.addAction("Pan To Start")
        pan_end = menu.addAction("Pan To End")
        menu.addSeparator()

        remove = menu.addAction("Remove Graph")

        if not self.graph.is_loaded:
            pause_play.setEnabled(False)
            speed_up.setEnabled(False)
            slow_down.setEnabled(False)
            pan_begin.setEnabled(False)
            pan_end.setEnabled(False)

        action = menu.exec(self.mapToGlobal(position))

        if action == change_title:
            self.ui.graph_title_lbl.setFocus()
        elif action == signal_from_file:
            self.graphController.upload_signal_file(self.graph)
            self.enable_controls()
        elif action == signal_from_web:
            pass
        elif action == pause_play:
            self.toggle_pause_play()
        elif action == speed_up:
            self.graphController.increase_plotting_speed(self.graph)
        elif action == slow_down:
            self.graphController.decrease_plotting_speed(self.graph)
        elif action == pan_begin:
            pass
        elif action == pan_end:
            pass
        elif action == remove:
            self.deleteLater()

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

    def toggle_pause_play(self):
        try:
            self.graphController.toggle_play_pause_btn(self.graph)
        except AttributeError:
            pass
        self.playing_state = not self.playing_state
        if self.playing_state:
            self.ui.pause_play_btn.setIcon(self.pause_icon)
        else:
            self.ui.pause_play_btn.setIcon(self.play_icon)

    def enable_controls(self):
        self.ui.pause_play_btn.setEnabled(True)
        self.ui.beginning_btn.setEnabled(True)
        self.ui.end_btn.setEnabled(True)
        self.ui.fast_forward_btn.setEnabled(True)
        self.ui.fast_backward_btn.setEnabled(True)
