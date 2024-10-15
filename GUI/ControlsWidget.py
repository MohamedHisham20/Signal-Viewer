from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget, QMenu
from PySide6.QtCore import Qt

from Controllers.report import GraphWindow
from GUI.Signal import Signal
from GUI.UI.UI_controls_widget import Ui_Controls_Widget
from Controllers.GlueController import GlueController


class ControlsWidget(QWidget):
    def __init__(self, parent=None, non_rect_graph=None):
        super().__init__(parent)
        self.non_rect_graph = non_rect_graph
        self.ui = Ui_Controls_Widget()
        self.ui.setupUi(self)
        self.root_widget = self.parent()
        self.signals = []
        self.ui.signals_list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.signals_list_widget.customContextMenuRequested.connect(self.show_signal_list_context_menu)

        self.ui.glue_btn.setEnabled(True)  # Set enabled when 2 signals are selected
        self.connect_all_graphs_btns()
        self.ui.report_btn.setEnabled(True) 
        self.ui.report_btn.clicked.connect(self.show_report_popup)

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
        non_rect = menu.addAction("load NonRect Graph")
        report = menu.addAction("Report")
        remove = menu.addAction("Remove")

        action = menu.exec(self.ui.signals_list_widget.mapToGlobal(position))

        if action in add_to_graph:
            for graph in self.root_widget.graphs:
                if graph.ui.graph_title_lbl.text() == action.text():
                    graph.add_signal(self.signals[self.ui.signals_list_widget.currentRow()])
        if action == non_rect:
            self.load_non_rect_graph()

    def show_add_signal_context_menu(self, position):
        menu = QMenu(self)
        from_file = menu.addAction("Add Signal from File")
        from_web = menu.addAction("Add Signal from Web")
        action = menu.exec(self.ui.signals_list_widget.mapToGlobal(position))

        if action == from_file:
            self.root_widget.load_signal()
        if action == from_web:
            self.load_from_web()
        

    def load_from_web(self):
        signal = GlueController.real_time_signal()
        signal = GlueController.process_data(signal)
        close = Signal.from_NP_array(signal['close'] , 'close')
        self.add_signal(close,)
        open = Signal.from_NP_array(signal['open'] ,'open')
        self.add_signal(open)
        high = Signal.from_NP_array(signal['high'],'high')
        self.add_signal(high)
        low = Signal.from_NP_array(signal['low'] ,'low')
        self.add_signal(low)
        # #add to graph
        # self.root_widget.add_graph()
        # graph = self.root_widget.graphs[-1]
        # graph.add_signal(close)
        # graph.add_signal(open)
        # graph.add_signal(high)
        # graph.add_signal(low)

    def load_non_rect_graph(self):
        self.non_rect_graph.signal_to_nonRect(self.signals[self.ui.signals_list_widget.currentRow()])


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

    def show_report_popup(self):
        all_signals = self.signals
        print(all_signals)
        # create a window to add the report widget to it
        self.report_window = QWidget()
        self.report_widget = GraphWindow(data_dict=all_signals)
        # set layout and add the widget to the window
        layout = QVBoxLayout()
        layout.addWidget(self.report_widget)
        self.report_window.setLayout(layout)
        # show the window
        self.report_window.show()