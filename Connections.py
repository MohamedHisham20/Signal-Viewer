from MainWindow import DragDropList, Ui_MainWindow
from NonRectGraphController import NonRectGraph
from PySide6 import QtWidgets
from Signal import Signal
from Graph import Graph
from report import open_report_window


def add_lists(ui, graph_C1, graph_C2, graph_C3, signals):
    horizontalLayout = QtWidgets.QHBoxLayout()
    ui.horizontalLayout.setObjectName("horizontalLayout")
    ui.C1_list = DragDropList()
    ui.C1_list.setupParameters(ui, graph_C1, graph_C2, graph_C3, signals)
    ui.C1_list.setObjectName("C1_list")
    ui.horizontalLayout.addWidget(ui.C1_list)
    ui.C2_list = DragDropList()
    ui.C2_list.setupParameters(ui, graph_C1, graph_C2, graph_C3, signals)
    ui.C2_list.setObjectName("C2_list")
    ui.horizontalLayout.addWidget(ui.C2_list)
    ui.C3_list = DragDropList()
    ui.C3_list.setupParameters(ui, graph_C1, graph_C2, graph_C3, signals)
    ui.C3_list.setObjectName("C3_list")
    ui.horizontalLayout.addWidget(ui.C3_list)
    ui.verticalLayout_13.addLayout(ui.horizontalLayout)
    ui.verticalLayout_4.addLayout(ui.verticalLayout_13)
    ui.C1_widget.layout().addWidget(graph_C1.plot_widget)
    ui.C2_widget.layout().addWidget(graph_C2.plot_widget)
    ui.C3_widget.layout().addWidget(graph_C3.plot_widget)


def NonRect_connections(graph: NonRectGraph, ui: Ui_MainWindow, signals: list[Signal]):
    ui.Channels.setFixedHeight(400)
    if ui.nonRect_widget.layout() is None:
        layout = QtWidgets.QHBoxLayout(ui.nonRect_widget)
        ui.nonRect_widget.setLayout(layout)
    graph.pause_radar()
    ui.nonRect_widget.layout().addWidget(graph)
    ui.stop_c4.clicked.connect(lambda: graph.pause_radar())
    ui.play_c4.clicked.connect(lambda: graph.play_radar())
    ui.replay_c4.clicked.connect(lambda: graph.rewind_radar())
    ui.dial_slide_c4.valueChanged.connect(lambda: graph.scroll_radar(ui.dial_slide_c4.value()))
    ui.dial_slide_c4.sliderPressed.connect(lambda: graph.pause_radar())

    ui.dial_slide_c4.setRange(0, 360)
    ui.dial_speed_c4.valueChanged.connect(lambda: graph.change_speed(ui.dial_speed_c4.value()))
    ui.dial_speed_c4.setRange(1, 20)
    ui.addsignalc4_combo.addItems([signal.label for signal in signals])
    ui.addsignal_c4.clicked.connect(lambda: {
        graph.clear(),
        graph.signal_to_nonRect(signals[ui.addsignalc4_combo.currentIndex()]),
        graph.play_radar()
    })


def Graph_connections(graph: Graph, ui: Ui_MainWindow, signals: list[Signal], channel: int):
    if channel == 1:
        ui.addsignalc1_combo.addItems([signal.label for signal in signals])

        def add_signal():
            # update_signal_list(ui,signals)
            signal = signals[ui.addsignalc1_combo.currentIndex()]
            # check what is the last point of any ploted signal

            last_point = graph.get_last_point()
            if signal.label not in [ui.choosesignalc1_combo.itemText(i) for i in
                                    range(ui.choosesignalc1_combo.count())]:
                plot = graph.plot_signal(signal, shift=last_point)

                if plot.signal.label not in [ui.choosesignalc1_combo.itemText(i) for i in
                                             range(ui.choosesignalc1_combo.count())]:
                    ui.choosesignalc1_combo.addItem(plot.signal.label)
                ui.C1_list.addItem(plot.signal.label)
            else:
                print("Signal already exists in the combo box")

        ui.addsignal_c1.clicked.connect(add_signal)

        def play():
            if ui.checkBox_c1.isChecked():
                label = ui.choosesignalc1_combo.currentText()
                plot = next((plot for plot in graph.plots if plot.signal.label == label), None)
                graph.play_pause(plot, True)
            else:
                graph.play_pause(play=True)

        def stop():
            if ui.checkBox_c1.isChecked():
                label = ui.choosesignalc1_combo.currentText()
                plot = next((plot for plot in graph.plots if plot.signal.label == label), None)
                graph.play_pause(plot, False)
            else:
                graph.play_pause(play=False)

        ui.playc1.clicked.connect(play)
        ui.stopc1.clicked.connect(stop)
        ui.dial_speed_c1.setRange(10, 100)
        ui.dial_speed_c1.setValue(10)
        ui.dial_speed_c1.valueChanged.connect(lambda: graph.change_speed(100 - ui.dial_speed_c1.value()))

        # ui.addsignal_c1.clicked.connect(lambda: graph.plot_signal(signals[ui.addsignalc1_combo.currentIndex()]))
        def rewind():
            if ui.checkBox_c1.isChecked():
                label = ui.choosesignalc1_combo.currentText()
                plot = next((plot for plot in graph.plots if plot.signal.label == label), None)
                graph.rewind(plot)
            else:
                graph.rewind()

        ui.replayc1.clicked.connect(rewind)
        ui.dial_slide_c1.setRange(0, 100)

        def change_pan():

            label = ui.choosesignalc1_combo.currentText()
            plot = next((plot for plot in graph.plots if plot.signal.label == label), None)
            if plot is not None:
                graph.change_pan_window(plot, ui.dial_slide_c1.value() / 100)

        ui.choosesignalc1_combo.currentIndexChanged.connect(change_pan)
        ui.dial_slide_btn.setValue(0)
        # ui.dial_slide_c1.valueChanged.connect(change_pan)
        ui.dial_slide_c1.valueChanged.connect(lambda : graph.sihftX(ui.dial_slide_c1.value()/100.0))

    elif channel == 2:
        ui.addsignalc2_combo.addItems([signal.label for signal in signals])

        # ui.choosesignalc2_combo.addItems()
        # ui.C2_list.addItems([signal.label for signal in signals])

        # ui.C2_widget.layout().addWidget(graph.plot_widget)
        def add_signal():
            signal = signals[ui.addsignalc2_combo.currentIndex()]
            # Check if the signal already exists in the combo box
            last_point = graph.get_last_point()
            if signal.label not in [ui.choosesignalc2_combo.itemText(i) for i in
                                    range(ui.choosesignalc2_combo.count())]:
                plot = graph.plot_signal(signal, shift=last_point)
                if plot.signal.label not in [ui.choosesignalc2_combo.itemText(i) for i in
                                             range(ui.choosesignalc2_combo.count())]:
                    ui.choosesignalc2_combo.addItem(plot.signal.label)
                ui.C2_list.addItem(plot.signal.label)
            else:
                print("Signal already exists in the combo box")

        ui.addsignalc2_btn.clicked.connect(add_signal)

        def play():
            if ui.checkBox_c2.isChecked():
                label = ui.choosesignalc2_combo.currentText()
                plot = next((plot for plot in graph.plots if plot.signal.label == label), None)
                graph.play_pause(plot, True)
            else:
                graph.play_pause(play=True)

        def stop():
            if ui.checkBox_c2.isChecked():
                label = ui.choosesignalc2_combo.currentText()
                plot = next((plot for plot in graph.plots if plot.signal.label == label), None)
                graph.play_pause(plot, False)
            else:
                graph.play_pause(play=False)

        ui.playc2.clicked.connect(play)
        ui.stopc2.clicked.connect(stop)
        ui.dial_speed_c2.setRange(10, 100)
        ui.dial_speed_c2.setValue(10)
        ui.dial_speed_c2.valueChanged.connect(lambda: graph.change_speed(100 - ui.dial_speed_c2.value()))

        # ui.addsignal_c2.clicked.connect(lambda: graph.plot_signal(signals[ui.addsignalc2_combo.currentIndex()]))
        def rewind():
            if ui.checkBox_c2.isChecked():
                label = ui.choosesignalc2_combo.currentText()
                plot = next((plot for plot in graph.plots if plot.signal.label == label), None)
                graph.rewind(plot)
            else:
                graph.rewind()

        ui.replayc2.clicked.connect(rewind)
        ui.dial_slide_c2.setRange(0, 100)

        def change_pan():

            label = ui.choosesignalc2_combo.currentText()
            plot = next((plot for plot in graph.plots if plot.signal.label == label), None)
            if plot is not None:
                graph.change_pan_window(plot, ui.dial_slide_c2.value() / 100)

        ui.choosesignalc2_combo.currentIndexChanged.connect(change_pan)
        ui.dial_slide_c2.setValue(0)
        ui.dial_slide_c2.valueChanged.connect(change_pan)

    elif channel == 3:
        ui.addsignalc3_combo.addItems([signal.label for signal in signals])

        # ui.choosesignalc3_combo.addItems()
        # ui.C3_list.addItems([signal.label for signal in signals])

        # ui.C3_widget.layout().addWidget(graph.plot_widget)
        def add_signal():
            signal = signals[ui.addsignalc3_combo.currentIndex()]
            # Check if the signal already exists in the combo box
            last_point = graph.get_last_point()
            if signal.label not in [ui.choosesignalc3_combo.itemText(i) for i in
                                    range(ui.choosesignalc3_combo.count())]:

                plot = graph.plot_signal(signal, shift=last_point)
                if plot.signal.label not in [ui.choosesignalc3_combo.itemText(i) for i in
                                             range(ui.choosesignalc3_combo.count())]:
                    ui.choosesignalc3_combo.addItem(plot.signal.label)
                ui.C3_list.addItem(plot.signal.label)
            else:
                print("Signal already exists in the combo box")

        ui.addsignal_c3.clicked.connect(add_signal)

        def play():
            if ui.checkBox_c3.isChecked():
                label = ui.choosesignalc3_combo.currentText()
                plot = next((plot for plot in graph.plots if plot.signal.label == label), None)
                graph.play_pause(plot, True)
            else:
                graph.play_pause(play=True)

        def stop():
            if ui.checkBox_c3.isChecked():
                label = ui.choosesignalc3_combo.currentText()
                plot = next((plot for plot in graph.plots if plot.signal.label == label), None)
                graph.play_pause(plot, False)
            else:
                graph.play_pause(play=False)

        ui.play_c3.clicked.connect(play)
        ui.play_c3.clicked.connect(stop)
        ui.dial_speed_c3.setRange(10, 100)
        ui.dial_speed_c3.setValue(10)
        ui.dial_speed_c3.valueChanged.connect(lambda: graph.change_speed(100 - ui.dial_speed_c3.value()))

        # ui.addsignal_c3.clicked.connect(lambda: graph.plot_signal(signals[ui.addsignalc3_combo.currentIndex()]))
        def rewind():
            if ui.checkBox_c3.isChecked():
                label = ui.choosesignalc3_combo.currentText()
                plot = next((plot for plot in graph.plots if plot.signal.label == label), None)
                graph.rewind(plot)
            else:
                graph.rewind()

        ui.replay_c3.clicked.connect(rewind)
        ui.dial_slide_c3.setRange(0, 100)

        def change_pan():

            label = ui.choosesignalc3_combo.currentText()
            plot = next((plot for plot in graph.plots if plot.signal.label == label), None)
            if plot is not None:
                graph.change_pan_window(plot, ui.dial_slide_c3.value() / 100)

        ui.choosesignalc3_combo.currentIndexChanged.connect(change_pan)
        ui.dial_slide_c3.setValue(0)
        ui.dial_slide_c3.valueChanged.connect(change_pan)


def all_channels_connections(graph1: Graph, graph2: Graph, graph3: Graph, ui: Ui_MainWindow, signals: list[Signal]):
    def play_all():
        graph1.play_pause(play=True)
        graph2.play_pause(play=True)
        graph3.play_pause(play=True)

    def stop_all():
        graph1.play_pause(play=False)
        graph2.play_pause(play=False)
        graph3.play_pause(play=False)

    def rewind_all():
        graph1.rewind()
        graph2.rewind()
        graph3.rewind()

    def change_speed_all(speed):
        graph1.change_speed(speed)
        graph2.change_speed(speed)
        graph3.change_speed(speed)

    def change_pan_all(value):
        if graph1.plot_to_track is not None:
            graph1.change_pan_window(graph1.plot_to_track, value / 100)
        if graph2.plot_to_track is not None:
            graph2.change_pan_window(graph2.plot_to_track, value / 100)
        if graph3.plot_to_track is not None:
            graph3.change_pan_window(graph3.plot_to_track, value / 100)

    ui.play_all_btn.clicked.connect(play_all)
    ui.stop_all_btn.clicked.connect(stop_all)
    ui.replay_all_btn.clicked.connect(rewind_all)
    ui.dial_speed_btn.setRange(10, 100)
    ui.dial_speed_btn.setValue(50)
    ui.dial_speed_btn.valueChanged.connect(lambda: change_speed_all(140 - ui.dial_speed_btn.value()))
    ui.dial_slide_btn.setRange(0, 100)
    ui.dial_slide_btn.setValue(0)
    ui.dial_slide_btn.valueChanged.connect(change_pan_all)


def general_connections(ui: Ui_MainWindow, graph1: Graph, graph2: Graph, graph3: Graph, signals: list[Signal]):
    def crop_signal():
        # print("Cropping")
        # selected_channel = ui.crop_combo.currentIndex()+1
        from_c1 = graph1.crop_signal()
        from_c2 = graph2.crop_signal()
        from_c3 = graph3.crop_signal()

        # print(from_c1)
        # print(from_c2)
        # print(from_c3)
        def add_signal(graph: Graph, combo: QtWidgets.QComboBox, signal, list):
            signals.append(signal)
            if signal.label not in [combo.itemText(i) for i in range(combo.count())]:
                shift = graph.get_last_point()
                plot = graph.plot_signal(signal)

                if plot.signal.label not in [combo.itemText(i) for i in range(combo.count())]:
                    combo.addItem(plot.signal.label)
                list.addItem(plot.signal.label)
                update_signal_list(ui, signals)
            else:
                print("Signal already exists in the combo box")

        if from_c1 is not None:
            add_signal(graph1, ui.addsignalc1_combo, from_c1, ui.C1_list)
        if from_c2 is not None:
            add_signal(graph2, ui.addsignalc2_combo, from_c2, ui.C2_list)
        if from_c3 is not None:
            add_signal(graph3, ui.addsignalc3_combo, from_c3, ui.C3_list)

    graph1.custom_viewbox.crop = crop_signal
    graph2.custom_viewbox.crop = crop_signal
    graph3.custom_viewbox.crop = crop_signal

    def add_real_time():
        selected_graph = ui.real_time_combo.currentIndex()
        # print(selected_graph)
        if selected_graph == 0:
            graph = graph1
            list = ui.C1_list
            combo = ui.choosesignalc1_combo
        elif selected_graph == 1:
            graph = graph2
            list = ui.C2_list
            combo = ui.choosesignalc2_combo
        elif selected_graph == 2:
            graph = graph3
            list = ui.C3_list
            combo = ui.choosesignalc3_combo
        graph.plot_real_time(label="Real Time")
        # print("Real Time" , graph.plots[0])
        list.addItem("Real Time")
        combo.addItem("Real Time")
        # print("Real Time")

    ui.real_time_btn.clicked.connect(lambda: add_real_time())

    # ui.real_time_btn.clicked.connect()


def update_signal_list(ui: Ui_MainWindow, signals: list[Signal]):
    ui.addsignalc1_combo.clear()
    ui.addsignalc2_combo.clear()
    ui.addsignalc3_combo.clear()
    ui.addsignalc4_combo.clear()

    ui.addsignalc1_combo.addItems([signal.label for signal in signals])
    ui.addsignalc2_combo.addItems([signal.label for signal in signals])
    ui.addsignalc3_combo.addItems([signal.label for signal in signals])
    ui.addsignalc4_combo.addItems([signal.label for signal in signals])


def report_connections(ui: Ui_MainWindow, signals: list[Signal]):
    ui.report_btn.clicked.connect(open_report_window)

def glue_connections(ui: Ui_MainWindow,graph1: Graph, graph2: Graph, graph3: Graph ,signals: list[Signal]):
    
    pass
