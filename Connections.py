import pyqtgraph as pg
import copy
from PySide6 import QtCore
from MainWindow import DragDropList, Ui_MainWindow
from NonRectGraphController import NonRectGraph
from PySide6 import QtWidgets
from Signal import Signal
from Graph import Graph
from report import open_report_window
from Glue import GluePopUp, glue_signals
from WeatherDataFetcher import WeatherDataFetcher


def add_lists(ui, graph_Channel1, graph_Channel2, graph_C3, signals):
    horizontalLayout = QtWidgets.QHBoxLayout()
    ui.horizontalLayout.setObjectName("horizontalLayout")
    ui.Channel1_list = DragDropList()
    ui.Channel1_list.setMaximumSize(QtCore.QSize(1000, 70))
    ui.Channel1_list.setupParameters(ui, graph_Channel1, graph_Channel2, graph_C3, signals)
    ui.Channel1_list.setObjectName("Channel1_list")
    ui.horizontalLayout.addWidget(ui.Channel1_list)
    ui.Channel2_list = DragDropList()
    ui.Channel2_list.setMaximumSize(QtCore.QSize(1000, 70))
    ui.Channel2_list.setupParameters(ui, graph_Channel1, graph_Channel2, graph_C3, signals)
    ui.Channel2_list.setObjectName("Channel2_list")
    ui.horizontalLayout.addWidget(ui.Channel2_list)
    ui.C3_list = DragDropList()
    ui.C3_list.setupParameters(ui, graph_Channel1, graph_Channel2, graph_C3, signals)
    ui.C3_list.setObjectName("C3_list")
    # ui.horizontalLayout.addWidget(ui.C3_list)
    ui.verticalLayout_13.addLayout(ui.horizontalLayout)
    ui.verticalLayout_4.addLayout(ui.verticalLayout_13)
    ui.Channel1_widget.layout().addWidget(graph_Channel1.plot_widget)
    ui.Channel2_widget.layout().addWidget(graph_Channel2.plot_widget)
    #add line 
    ui.line = QtWidgets.QFrame()
    ui.line.setFrameShape(QtWidgets.QFrame.HLine)
    ui.line.setFrameShadow(QtWidgets.QFrame.Sunken)
    #add lable 
    ui.operations_label = QtWidgets.QLabel()
    ui.operations_label.setObjectName("label")
    ui.operations_label.setText("Operations")
    ui.verticalLayout_4.addWidget(ui.operations_label)
    ui.verticalLayout_4.addWidget(ui.line)
    ui.verticalLayout_4.addLayout(ui.glue_report_layout)
    # ui.C3_widget.layout().addWidget(graph_C3.plot_widget)


def NonRect_connections(graph: NonRectGraph, ui: Ui_MainWindow, signals: list[Signal]):
    ui.Channels.setFixedHeight(390)
    ui.nonRect_widget.setFixedHeight(370)
    if ui.nonRect_widget.layout() is None:
        layout = QtWidgets.QVBoxLayout(ui.nonRect_widget)
        ui.nonRect_widget.setLayout(layout)
    graph.pause_radar()
    ui.nonRect_widget.layout().addWidget(graph)

    # Create play/pause button
    play_pause_button = QtWidgets.QPushButton("Play")
    # ui.nonRect_widget.layout().addWidget(play_pause_button)
    def toggle_play_pause():
        if graph.isRunning:
            graph.pause_radar()
            play_pause_button.setText("Play")
        else:
            graph.play_radar()
            play_pause_button.setText("Pause")

    play_pause_button.clicked.connect(toggle_play_pause)

    plot_siganl = QtWidgets.QPushButton("Plot")
    siganls_combo = QtWidgets.QComboBox()
    rewind_button = QtWidgets.QPushButton("Rewind")
    plot_signal_layout = QtWidgets.QHBoxLayout()
    plot_signal_layout.addWidget(play_pause_button)
    plot_signal_layout.addWidget(rewind_button)
    plot_signal_layout.addWidget(plot_siganl)
    plot_signal_layout.addWidget(siganls_combo)
    ui.nonRect_widget.layout().addLayout(plot_signal_layout)

    siganls_combo.addItems([signal.label for signal in signals])

    def plot_signal():
        signal = copy.deepcopy(signals[siganls_combo.currentIndex() -1])
        graph.signal_to_nonRect(signal)
        toggle_play_pause()

    plot_siganl.clicked.connect(plot_signal)

    def rewind():
        graph.rewind_radar()
        play_pause_button.setText("Pause")

    rewind_button.clicked.connect(rewind)


    speed_label = QtWidgets.QLabel("Speed:")
    speed_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
    speed_slider.setRange(1, 10)
    speed_slider.setValue(3)
    
    speed_layout = QtWidgets.QHBoxLayout()
    speed_layout.addWidget(speed_label)
    speed_layout.addWidget(speed_slider)
    
    ui.nonRect_widget.layout().addLayout(speed_layout)

    speed_slider.valueChanged.connect(lambda: graph.change_speed(speed_slider.value()))

    pan_label = QtWidgets.QLabel("Pan:")
    pan_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
    pan_slider.setRange(0, 360)
    pan_slider.setValue(50)
    pan_layout = QtWidgets.QHBoxLayout()
    pan_layout.addWidget(pan_label)
    pan_layout.addWidget(pan_slider)    
    ui.nonRect_widget.layout().addLayout(pan_layout)
    def stop_radar_on_pan():
        graph.pause_radar()
        play_pause_button.setText("Play")
        graph.scroll_radar(pan_slider.value())

    pan_slider.valueChanged.connect(stop_radar_on_pan)



def Graph_connections(graph: Graph, ui: Ui_MainWindow, signals: list[Signal], Channel: int):
    if Channel == 1:
        ui.addsignalChannel1_combo.addItems([signal.label for signal in signals])

        def add_signal():
            if ui.addsignalChannel1_combo.currentIndex() == 0:
                return
            # signal = signals[ui.addsignalc3_combo.currentIndex()]
            signal = copy.deepcopy(signals[ui.addsignalChannel1_combo.currentIndex() -1])

            # Check if the signal already exists in the combo box
            last_point = graph.get_last_point()
            plot_labels = [plot.signal.label for plot in graph.plots]
            if signal.label not in plot_labels:

                plot = graph.plot_signal(signal, shift=graph.plot_to_track.signal.data_pnts[last_point][0] if graph.plot_to_track is not None else 0)
                ui.playChannel1.setText("Pause")

                ui.Channel1_list.addItem(plot.signal.label)
            else:
                print("Signal already exists in the combo box")

        ui.addsignal_Channel1.clicked.connect(add_signal)

        def play():
            graph.play_pause()
            if graph.plot_to_track is not None:
                ui.playChannel1.setText("Pause" if graph.plot_to_track.isRunning else "Play")


        ui.playChannel1.clicked.connect(play)
        ui.dial_speed_Channel1.setRange(1, 10)
        ui.dial_speed_Channel1.setValue(10)
        graph.change_speed(10)
        ui.dial_speed_Channel1.valueChanged.connect(lambda: graph.change_speed(ui.dial_speed_Channel1.value()))

        # ui.addsignal_Channel1.clicked.connect(lambda: graph.plot_signal(signals[ui.addsignalChannel1_combo.currentIndex() -1]))
        def rewind():
            graph.rewind()
            ui.playChannel1.setText("Pause")

        ui.replayChannel1.clicked.connect(rewind)
        ui.dial_slide_Channel1.setRange(0, 100)
        ui.dial_slide_Channel1.setValue(100)
        graph.x_zoom(1)
        ui.dial_slide_Channel1.valueChanged.connect(lambda: graph.x_zoom(ui.dial_slide_Channel1.value() / 100.0))

    elif Channel == 2:
        ui.addsignalChannel2_combo.addItems([signal.label for signal in signals])

        def add_signal():
            if ui.addsignalChannel2_combo.currentIndex() == 0:
                return
            signal = copy.deepcopy(signals[ui.addsignalChannel2_combo.currentIndex() -1])
            last_point = graph.get_last_point()
            plot_labels = [plot.signal.label for plot in graph.plots]
            if signal.label not in plot_labels:

                plot = graph.plot_signal(signal, shift=graph.plot_to_track.signal.data_pnts[last_point][0] if graph.plot_to_track is not None else 0)
                ui.playChannel2.setText("Pause")
                ui.Channel2_list.addItem(plot.signal.label)
            else:
                print("Signal already exists in the combo box")

        ui.addsignalChannel2_btn.clicked.connect(add_signal)

        def play():
            graph.play_pause()
            if graph.plot_to_track is not None:
                ui.playChannel2.setText("Pause" if graph.plot_to_track.isRunning else "Play")



        ui.playChannel2.clicked.connect(play)
        ui.dial_speed_Channel2.setRange(1, 10)
        ui.dial_speed_Channel2.setValue(10)
        graph.change_speed(10)
        ui.dial_speed_Channel2.valueChanged.connect(lambda: graph.change_speed(ui.dial_speed_Channel2.value()))

        # ui.addsignal_Channel2.clicked.connect(lambda: graph.plot_signal(signals[ui.addsignalChannel2_combo.currentIndex() -1]))
        def rewind():
            graph.rewind()
            ui.playChannel2.setText("Pause")

        ui.replayChannel2.clicked.connect(rewind)
        ui.dial_slide_Channel2.setRange(0, 100)
        ui.dial_slide_Channel2.setValue(100)
        graph.x_zoom(1)
        ui.dial_slide_Channel2.valueChanged.connect(lambda: graph.x_zoom(ui.dial_slide_Channel2.value() / 100.0))



def all_Channels_connections(graph1: Graph, graph2: Graph, graph3: Graph, ui: Ui_MainWindow, signals: list[Signal]):
    def play_all():
        if ui.play_all_btn.text() == "Pause":
            if graph1.plot_to_track is not None:
                if graph1.plot_to_track.isRunning:
                    graph1.play_pause()
            if graph2.plot_to_track is not None:
                if graph2.plot_to_track.isRunning:
                    graph2.play_pause()
            ui.play_all_btn.setText("Play")
        else:
            if graph1.plot_to_track is not None:
                if not graph1.plot_to_track.isRunning:
                    graph1.play_pause()
            if graph2.plot_to_track is not None:
                if not graph2.plot_to_track.isRunning:
                    graph2.play_pause()
            ui.play_all_btn.setText("Pause")


    def rewind_all():
        graph1.rewind()
        graph2.rewind()
        graph3.rewind()
        ui.play_all_btn.setText("Pause")

    def change_speed_all(speed):
        graph1.change_speed(speed)
        graph2.change_speed(speed)
        graph3.change_speed(speed)

    def change_pan_all(value):
        if graph1.plot_to_track is not None:
            graph1.x_zoom(value / 100)
        if graph2.plot_to_track is not None:
            graph2.x_zoom(value / 100)
        if graph3.plot_to_track is not None:
            graph3.x_zoom(value / 100)

    def play_init():
        ui.play_all_btn.setText("Pause")
        all_running = False
        all_paused = True
        if graph1.plot_to_track is not None:
            ui.playChannel1.setText("Pause" if graph1.plot_to_track.isRunning else "Play")
            all_running = all_running or graph1.plot_to_track.isRunning
            all_paused = all_paused and not graph1.plot_to_track.isRunning
        if graph2.plot_to_track is not None:
            ui.playChannel2.setText("Pause" if graph2.plot_to_track.isRunning else "Play")
            all_running = all_running or graph2.plot_to_track.isRunning
            all_paused = all_paused and not graph2.plot_to_track.isRunning

        if not all_running:
            ui.play_all_btn.setText("Play")
        if not all_paused:
            ui.play_all_btn.setText("Pause")

        if ui.Channels.currentIndex() != 2:
            graph1.linked = False
            graph2.linked = False
            return
        graph1.linked = True
        graph2.linked = True
        def link_view(source_viewbox, target_viewbox):
            if not graph1.custom_viewbox.is_user_panning and not graph2.custom_viewbox.is_user_panning:
                return
            if graph1.custom_viewbox.is_user_panning:
                graph2.custom_viewbox.is_user_panning = True
                graph2.custom_viewbox.elapsed_timer.start()
            else:
                graph2.custom_viewbox.is_user_panning = False
                
            if graph2.custom_viewbox.is_user_panning:
                graph1.custom_viewbox.is_user_panning = True
                graph1.custom_viewbox.elapsed_timer.start()
            else:
                graph1.custom_viewbox.is_user_panning = False

            if not graph1.linked:
                return
            if not graph2.linked:
                return
            
            # target_viewbox.setLimits(
            #     yMin=min(source_viewbox.viewRange()[1][0], target_viewbox.viewRange()[1][0]),
            #     yMax=max(source_viewbox.viewRange()[1][1], target_viewbox.viewRange()[1][1])
            # )
            target_viewbox.setXRange(*source_viewbox.viewRange()[0], padding=0)
            target_viewbox.setYRange(*source_viewbox.viewRange()[1], padding=0)

        graph1.plot_widget.getViewBox().sigXRangeChanged.connect(lambda: link_view(graph1.plot_widget.getViewBox(), graph2.plot_widget.getViewBox()))
        graph2.plot_widget.getViewBox().sigXRangeChanged.connect(lambda: link_view(graph2.plot_widget.getViewBox(), graph1.plot_widget.getViewBox()))
        graph1.plot_widget.getViewBox().sigYRangeChanged.connect(lambda: link_view(graph1.plot_widget.getViewBox(), graph2.plot_widget.getViewBox()))
        graph2.plot_widget.getViewBox().sigYRangeChanged.connect(lambda: link_view(graph2.plot_widget.getViewBox(), graph1.plot_widget.getViewBox()))

    def import_csv():
        signal = Signal.from_file_dialog(True)
        if signal:
            #if there is signal with the same label, remove it
            for i in range(len(signals)):
                if signals[i].label == signal.label:
                    signals.pop(i)
                    break
                
            signals.append(signal)
            update_signal_list(ui, signals)

    ui.import_Channel1_btn.clicked.connect(import_csv)
    ui.import_Channel2_btn.clicked.connect(import_csv)
    ui.play_all_btn.clicked.connect(play_all)
    ui.Channels.currentChanged.connect(play_init)
    # ui.stop_all_btn.clicked.connect(stop_all)
    ui.replay_all_btn.clicked.connect(rewind_all)
    ui.dial_speed_btn.setRange(1, 10)
    ui.dial_speed_btn.setValue(10)
    change_pan_all(100)
    ui.dial_speed_btn.valueChanged.connect(lambda: change_speed_all(ui.dial_speed_btn.value()))
    ui.dial_slide_btn.setRange(0, 100)
    ui.dial_slide_btn.setValue(100)
    change_speed_all(10)
    ui.dial_slide_btn.valueChanged.connect(lambda: change_pan_all(ui.dial_slide_btn.value()))
    def init_glue_popup():
        glue_popup = GluePopUp(signals=signals,ui=ui)
        glue_popup.set_signals(copy.deepcopy(signals[0]), copy.deepcopy(signals[1]))
        glue_popup.combo_signal1.setCurrentIndex(0)
        glue_popup.combo_signal2.setCurrentIndex(1)
        glue_popup.show()

    ui.all_glue_btn.clicked.connect(lambda: init_glue_popup())


def general_connections(ui: Ui_MainWindow, graph1: Graph, graph2: Graph, graph3: Graph, signals: list[Signal]):
    def crop_signal():

        from_Channel1 = graph1.crop_signal()
        from_Channel2 = graph2.crop_signal()
        from_c3 = graph3.crop_signal()
        def add_signal(graph: Graph, combo: QtWidgets.QComboBox, signal, list):
            signals.append(signal)
            plot_labels = [plot.signal.label for plot in graph.plots]
            if signal.label not in plot_labels:

                plot = graph.plot_signal(signal)
                
                list.addItem(plot.signal.label)
                update_signal_list(ui, signals)
            else:
                print("Signal already exists in the combo box")

        if from_Channel1 is not None:
            add_signal(graph1, ui.addsignalChannel1_combo, from_Channel1, ui.Channel1_list)
            ui.playChannel1.setText("Pause")
        if from_Channel2 is not None:
            add_signal(graph2, ui.addsignalChannel2_combo, from_Channel2, ui.Channel2_list)
            ui.playChannel2.setText("Pause")


    graph1.custom_viewbox.crop = crop_signal
    graph2.custom_viewbox.crop = crop_signal


    def fetch_weather_data(graph,list):
        weather_fetcher = WeatherDataFetcher()
        shift = graph.get_last_point()
        graph.plot_real_time(shift = graph.plot_to_track.signal.data_pnts[shift][0] if graph.plot_to_track is not None else 0)
        list.addItem("Wind Speed")

        def update_points_from_api(wind_speed, time):
            print("wind speed is ",wind_speed, time)
            # if graph1 have real time plot
            for plot in graph1.plots:
                if plot.isRealTime:
                    graph1.update_real_time(wind_speed)
                    break
            # if graph2 have real time plot
            for plot in graph2.plots:
                if plot.isRealTime:
                    graph2.update_real_time(wind_speed)
                    break


        weather_fetcher.weather_data_fetched.connect(update_points_from_api)
        weather_fetcher.start()
        ui.weather_fetchers.append(weather_fetcher)

    ui.plot_real_time_Channel1.clicked.connect(lambda: fetch_weather_data(graph1,ui.Channel1_list))
    ui.plot_real_time_Channel2.clicked.connect(lambda: fetch_weather_data(graph2,ui.Channel2_list))

def update_signal_list(ui: Ui_MainWindow, signals: list[Signal]):
    ui.addsignalChannel1_combo.clear()
    ui.addsignalChannel2_combo.clear()
    # ui.addsignalc3_combo.clear()
    # ui.addsignalc4_combo.clear()

    ui.addsignalChannel1_combo.addItem("Choose signal")
    ui.addsignalChannel2_combo.addItem("Choose signal")
    ui.addsignalChannel1_combo.addItems([signal.label for signal in signals])
    ui.addsignalChannel2_combo.addItems([signal.label for signal in signals])
    # ui.addsignalc3_combo.addItems([signal.label for signal in signals])
    # ui.addsignalc4_combo.addItems([signal.label for signal in signals])


def report_connections(ui: Ui_MainWindow, signals: list[Signal]):
    ui.all_report_btn.clicked.connect(lambda: open_report_window(signals))


def glue_connections(ui: Ui_MainWindow, graph1: Graph, graph2: Graph, graph3: Graph, signals: list[Signal]):
    def populate_combo_boxes(channel_index=0):
        ui.glue_signal1_combo.clear()
        ui.glue_singal2_combo.clear()
        graph = None
        if channel_index == 1:
            graph = graph1
        elif channel_index == 2:
            graph = graph2
        elif channel_index == 3:
            graph = graph3
        if not graph:
            return
        ui.glue_signal1_combo.addItems([plot.signal.label for plot in graph.plots])
        ui.glue_singal2_combo.addItems([plot.signal.label for plot in graph.plots])
        ui.glue_singal2_combo.setCurrentIndex(len(graph.plots) - 1)
    def save():
        graph:Graph = graph1
        if ui.glue_combo_Channel.currentIndex() == 1:
            graph = graph1
        elif ui.glue_combo_Channel.currentIndex() == 2:
            graph = graph2
        elif ui.glue_combo_Channel.currentIndex() == 3:
            graph = graph3
        for plot in graph.plots:
            if plot.dynamic_interpolation:
                plot.plot1_interpolation = None
                plot.plot2_interpolation = None
                plot.dynamic_interpolation = False
    def on_tab_changed(index):
        populate_combo_boxes(ui.glue_combo_Channel.currentIndex())
        if ui.glue_combo_Channel.currentIndex() == 0:
            save()

    def glue():

        graph:Graph = graph1
        if ui.glue_combo_Channel.currentIndex() == 1:
            graph = graph1
        elif ui.glue_combo_Channel.currentIndex() == 2:
            graph = graph2
        elif ui.glue_combo_Channel.currentIndex() == 3:
            graph = graph3
        if len(graph.plots) < 2:
            return
        plot1 = graph.plots[ui.glue_signal1_combo.currentIndex()]
        plot2 = graph.plots[ui.glue_singal2_combo.currentIndex()]
        glued_signal = glue_signals(plot1.signal,
                                    plot2.signal)
        channel_index = ui.glue_combo_Channel.currentIndex()
        if channel_index == 1:
            graph = graph1
            list = ui.Channel1_list
        elif channel_index == 2:
            graph = graph2
            list = ui.Channel2_list
        elif channel_index == 3:
            graph = graph3
            list = ui.C3_list

        maxX = max(plot1.signal.data_pnts[plot1.last_point][0], plot2.signal.data_pnts[plot2.last_point][0])
        def find_last_index(glued_signal, maxX):
            epsilon = 1e-9
            low, high = 0, len(glued_signal.data_pnts) - 1
            while low < high:
                mid = (low + high) // 2
                if glued_signal.data_pnts[mid][0] < maxX - epsilon:
                    low = mid + 1
                else:
                    high = mid
            if low < len(glued_signal.data_pnts) and glued_signal.data_pnts[low][0] > maxX + epsilon:
                low -= 1
            return low
        last_index = find_last_index(glued_signal, maxX)
        last_point = last_index / len(glued_signal.data_pnts)
        # print(last_point)
        signals.append(glued_signal)
        update_signal_list(ui, signals)
        plot = graph.plot_signal(glued_signal,last_point)
        graph.play_pause(plot, False)
        plot.plot1_interpolation = plot1
        plot.plot2_interpolation = plot2
        plot.dynamic_interpolation = True
        # combo.addItem(plot.signal.label)
        list.addItem(plot.signal.label)



    ui.glue_combo_Channel.currentTextChanged.connect(on_tab_changed)
    # ui.Channels.currentChanged.connect(on_tab_changed)
    ui.glue_combo_Channel.clear()
    ui.glue_combo_Channel.addItems(["No glue","Channel 1", "Channel 2", "Channel 3"])
    # ui.glue_combo_Channel.currentIndexChanged.connect(
    #     lambda: populate_combo_boxes(ui.glue_combo_Channel.currentIndex()))
    ui.glue_combo_Channel.setCurrentIndex(0)

    ui.glue_btn.clicked.connect(glue)


def api_connection(ui: Ui_MainWindow, graph1: Graph, graph2: Graph, graph3: Graph, signals: list[Signal]):
    def fetch_weather_data():
        weather_fetcher = WeatherDataFetcher()
        if ui.real_time_combo.currentIndex() == 0:
            graph = graph1
        elif ui.real_time_combo.currentIndex() == 1:
            graph = graph2
        elif ui.real_time_combo.currentIndex() == 2:
            graph = graph3
        # graph.plot_real_time()
        for plot in graph.plots:
            if plot.isRealTime:
                plot.signal.label = "wind_speed"

        def update_points_from_api(wind_speed, time):
            # print(wind_speed, time)
            graph.update_real_time(wind_speed)

        weather_fetcher.weather_data_fetched.connect(update_points_from_api)
        weather_fetcher.start()
        ui.weather_fetchers.append(weather_fetcher)

    ui.real_time_btn.clicked.connect(fetch_weather_data)
