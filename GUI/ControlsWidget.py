from PySide6.QtWidgets import QWidget, QMenu
from PySide6.QtCore import Qt

from GUI.UI.UI_controls_widget import Ui_Controls_Widget
from Controllers.GlueController import GlueController


class ControlsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Controls_Widget()
        self.ui.setupUi(self)
        self.root_widget = self.parent()
        self.signals = []
        self.ui.signals_list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.signals_list_widget.customContextMenuRequested.connect(self.show_signal_list_context_menu)

        self.ui.glue_btn.setEnabled(True)  # Set enabled when 2 signals are selected
        self.connect_all_graphs_btns()

    def show_signal_list_context_menu(self, position):
        item = self.ui.signals_list_widget.itemAt(position)
        if item is None:
            self.show_add_signal_context_menu(position)
            return

        menu = QMenu(self)
        add_to_submenu = QMenu("Add to", self)

        add_to_graph = []
        if hasattr(self.root_widget, 'graphs'):
            for graph in self.root_widget.graphs:
                graph_title = graph.ui.graph_title_lbl.text()
                add_to_graph.append(add_to_submenu.addAction(graph_title))

        menu.addMenu(add_to_submenu)
        menu.addSeparator()

        report = menu.addAction("Report")
        remove = menu.addAction("Remove")

        action = menu.exec(self.ui.signals_list_widget.mapToGlobal(position))

        if action in add_to_graph:
            for graph in self.root_widget.graphs:
                if graph.ui.graph_title_lbl.text() == action.text():
                    graph.add_signal(self.signals[self.ui.signals_list_widget.currentRow()])

    def show_add_signal_context_menu(self, position):
        menu = QMenu(self)
        from_file = menu.addAction("Add Signal from File")
        from_web = menu.addAction("Add Signal from Web")
        action = menu.exec(self.ui.signals_list_widget.mapToGlobal(position))

        if action == from_file:
            self.root_widget.load_signal()

    def add_signal(self, signal):
        self.signals.append(signal)
        self.ui.signals_list_widget.addItem(signal.ID)
        self.enable_control_btns()

    def connect_all_graphs_btns(self):
        self.ui.zoom_in_btn.clicked.connect(lambda: self.root_widget.zoom_in_all_graphs())
        self.ui.zoom_out_btn.clicked.connect(lambda: self.root_widget.zoom_out_all_graphs())
        self.ui.speed_up_btn.clicked.connect(lambda: self.root_widget.speed_up_all_graphs())
        self.ui.slow_down_btn.clicked.connect(lambda: self.root_widget.slow_down_all_graphs())
        self.ui.pause_play_btn.clicked.connect(lambda: self.root_widget.toggle_play_pause_all_graphs())

    def enable_control_btns(self):
        self.ui.pause_play_btn.setEnabled(True)
        self.ui.zoom_in_btn.setEnabled(True)
        self.ui.zoom_out_btn.setEnabled(True)
        self.ui.speed_up_btn.setEnabled(True)
        self.ui.slow_down_btn.setEnabled(True)
