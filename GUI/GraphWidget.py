from PySide6.QtGui import QDrag, QIcon
from PySide6.QtWidgets import QApplication, QWidget, QMenu, QVBoxLayout
from PySide6.QtCore import Qt, QMimeData

from GUI.UI.UI_graph_widget import Ui_graph_widget
from GUI.UI.Graph import Graph
from GUI.UI.NewGraph import NewGraph
from Controllers.GraphController import GraphController


class GraphWidget(QWidget):
    instance_count = 0

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.ui = Ui_graph_widget()
        self.ui.setupUi(self)
        self.initial_position = None
        self.playing_state = False
        self.play_icon = QIcon('./Icons/play.png')
        self.pause_icon = QIcon('./Icons/pause.png')
        self.ChangeOrder = 'no'
        self.graphController = GraphController()
        self.graph = Graph()
        self.new_graph = NewGraph()
        if self.ui.graph_placeholder.layout() is None:
            self.ui.graph_placeholder.setLayout(QVBoxLayout())
        # self.ui.graph_placeholder.layout().addWidget(self.graph)
        self.ui.graph_placeholder.layout().addWidget(self.new_graph)
        self.swapAction = lambda: None

        GraphWidget.instance_count += 1
        self.setObjectName(f"graph_widget_{GraphWidget.instance_count}")
        self.ui.graph_title_lbl.setText(f"Graph {GraphWidget.instance_count}")

        self.drag_start_position = None
        self.is_dragging = False
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.connect_buttons()

    def connect_buttons(self):
        # Change this
        self.ui.pause_play_btn.clicked.connect(lambda: self.toggle_pause_play())
        self.ui.speed_up_btn.clicked.connect(lambda: self.graphController.increase_plotting_speed(self.graph))
        self.ui.slow_down_btn.clicked.connect(lambda: self.graphController.decrease_plotting_speed(self.graph))
        self.ui.zoom_in_btn.clicked.connect(lambda: self.graphController.zoom_in(self.graph))
        self.ui.zoom_out_btn.clicked.connect(lambda: self.graphController.zoom_out(self.graph))

    def show_context_menu(self, position):
        root_widget = self.parent().parent().parent().parent().parent().parent()
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
        zoom_in = menu.addAction("Zoom In")
        zoom_out = menu.addAction("Zoom Out")
        menu.addSeparator()

        remove = menu.addAction("Remove Graph")

        if self.graph.signals_counter == 0:
            pause_play.setEnabled(False)
            speed_up.setEnabled(False)
            slow_down.setEnabled(False)
            zoom_out.setEnabled(False)
            zoom_in.setEnabled(False)

        action = menu.exec(self.mapToGlobal(position))

        if action == change_title:
            self.ui.graph_title_lbl.setFocus()
        elif action == signal_from_file:
            signal = root_widget.load_signal()
            self.add_signal(signal)
        elif action == signal_from_web:
            pass
        elif action == pause_play:
            self.toggle_pause_play()
        elif action == speed_up:
            # self.graphController.increase_plotting_speed(self.graph)
            self.new_graph.speed_up()
        elif action == slow_down:
            # self.graphController.decrease_plotting_speed(self.graph)
            self.new_graph.slow_down()
        elif action == zoom_in:
            # self.graphController.zoom_in(self.graph)
            self.new_graph.zoom_in()
        elif action == zoom_out:
            # self.graphController.zoom_out(self.graph)
            self.new_graph.zoom_out()
        elif action == remove:
            self.deleteLater()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.position().toPoint() if hasattr(event, 'position') else event.pos()
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
        print('Mouse released.')
        self.is_dragging = False
        self.drag_start_position = None

    def dragEnterEvent(self, event):
        """Accept the drag event."""
        self.initial_position = self.drag_start_position.y()  # Store the initial Y-position

        if event.mimeData().hasText():
            event.acceptProposedAction()  # Accept the action so the drop can happen

    def dropEvent(self, event):
        print(self.initial_position)
        if event.mimeData().hasText():
            drop_position = event.position().toPoint() if hasattr(event, 'position') else event.pos()
            event.acceptProposedAction()
            self.calculate_y_distance(drop_position.y())  # Calculate the Y-axis movement

    def calculate_y_distance(self, drop_y_position):
        """Calculate how far the object has moved in the Y-axis."""
        if self.initial_position is not None:
            y_distance = drop_y_position - self.initial_position
            print(f'The object moved {y_distance} pixels in the Y-axis.')
            threshold = 10
            if y_distance < -threshold:
                self.ChangeOrder = 'up'
                self.swapAction()
            elif y_distance > threshold:
                self.ChangeOrder = 'down'
                self.swapAction()
        else:
            print('Initial position not set.')

    def toggle_pause_play(self):
        try:
            self.new_graph.toggle_play_pause()
            # self.graphController.toggle_play_pause_btn(self.graph)
        except AttributeError:
            pass
        self.playing_state = not self.playing_state
        if self.playing_state:
            self.ui.pause_play_btn.setIcon(self.pause_icon)
        else:
            self.ui.pause_play_btn.setIcon(self.play_icon)

    def enable_controls(self):
        self.ui.pause_play_btn.setEnabled(True)
        self.ui.zoom_in_btn.setEnabled(True)
        self.ui.zoom_out_btn.setEnabled(True)
        self.ui.slow_down_btn.setEnabled(True)
        self.ui.speed_up_btn.setEnabled(True)

    def add_signal(self, signal):
        self.graphController.add_signal_to_graph(signal, self.graph)
        self.enable_controls()
        self.toggle_pause_play()
        self.new_graph.add_signal(signal)
