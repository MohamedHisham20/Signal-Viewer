from PySide6.QtWidgets import QWidget, QMenu
from PySide6.QtCore import Qt
import numpy as np

from GUI.UI.UI_controls_widget import Ui_Controls_Widget
from Controllers.GlueController import GlueController
import Glue_popup


class ControlsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Controls_Widget()
        self.ui.setupUi(self)
        self.root = parent
        self.ui.signals_list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.signals_list_widget.customContextMenuRequested.connect(self.show_signal_list_context_menu)

        self.ui.glue_btn.clicked.connect(self.show_glue_popup)
        self.ui.glue_btn.setEnabled(True)  # Set enabled when 2 signals are selected

    def show_signal_list_context_menu(self, position):
        menu = QMenu(self)
        add_to_submenu = QMenu("Add to", self)

        main_window = self.parent().parent().parent().parent()  # This is so wrong, but necessary to get the graph names
        add_to_graph = []
        if hasattr(main_window, 'graphs'):
            for graph in main_window.graphs:
                graph_title = graph.ui.graph_title_lbl.text()
                add_to_graph.append(add_to_submenu.addAction(graph_title))

        menu.addMenu(add_to_submenu)
        menu.addSeparator()

        report = menu.addAction("Report")
        remove = menu.addAction("Remove")

        menu.exec(self.ui.signals_list_widget.mapToGlobal(position))

    def show_glue_popup(self):
        # signal1 = [[0, 0], [1, 3], [2, 4]]
        # signal2 = [[0, 5], [1, 6], [2, 7]]
        # sinusoidal signals
        signal1 = [[i, 5 * np.sin(i)] for i in range(5)]
        signal2 = [[i, 5 * np.cos(i)] for i in range(5)]
        glue_popup = Glue_popup.GlueSignalsPopup(signal1, signal2, None, None, self)
        glue_popup.exec()