import os
import sys
import numpy as np
from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                               QTextEdit,
                               QDialog, QFileDialog, QInputDialog, QSizePolicy, QComboBox, QScrollArea)
import pyqtgraph as pg
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pyqtgraph.exporters import ImageExporter

from Graph import Graph
from styleSheet import styleSheet
from Signal import Signal


class GraphWindow(QWidget):
    def __init__(self, signals=None):
        super().__init__()
        styleSheet(self)

        self.setWindowTitle("Graph Cropping Example")
        self.setGeometry(50, 30, 1080, 780)

        # Layout and plot widget
        self.layout = QVBoxLayout()
        self.graph = Graph()
        self.graph_widget = self.graph.plot_widget
        self.graph.custom_viewbox.crop = self.crop_graph_and_save

        self.layout.addWidget(self.graph_widget)
        self.data_dict = {}

        # Initial data and dataset dictionary
        for signal in signals:
            self.data_dict[signal.label] = signal.get_y_values()
        self.data_key = signals[0].label  # Default dataset
        self.data = self.data_dict[self.data_key]
        self.plot = self.graph_widget.plot(self.data, pen='b')

        self.graph.custom_viewbox.set_dynamic_limits(0, len(self.data), min(self.data), max(self.data))

        # set the range of the graph to open on the signal filling the screen
        self.graph.custom_viewbox.setRange(xRange=(0, len(self.data)), yRange=(min(self.data), max(self.data)),
                                           padding=0)

        # Dropdown menu for loading new graphs
        self.graph_dropdown = QComboBox(self)
        self.graph_dropdown.addItems(self.data_dict.keys())
        self.graph_dropdown.currentIndexChanged.connect(self.load_new_graph)
        self.layout.addWidget(self.graph_dropdown)

        # Button to create report
        self.report_button = QPushButton("Generate Report")
        self.report_button.clicked.connect(self.open_report_window)
        self.layout.addWidget(self.report_button)

        # Layout for cropping inputs and buttons
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QHBoxLayout(self.scroll_content)  # Set to horizontal layout
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)

        self.setLayout(self.layout)

        # Store all graphs and cropped data
        self.all_cropped_data = []  # Store cropped data here
        self.cropped_data = []  # Store the current cropped data
        self.original_data = self.data  # Keep the original data intact

    def crop_graph_and_save(self):
        """Crop the selected graph based on start and end inputs."""
        try:
            start = int(self.graph.custom_viewbox.selectfirstX)
            end = int(self.graph.custom_viewbox.selectseoncdX)

            if start < 0:
                start = 0
            if end < 0:
                end = 0
            if end >= len(self.original_data):
                end = len(self.original_data) - 1
            if start >= len(self.original_data):
                start = len(self.original_data) - 1
            if start > end:
                start, end = end, start

            # Crop the data from the original data
            cropped_data = self.original_data[start:end]
            self.cropped_data.append(cropped_data)  # Store the current cropped data
            self.all_cropped_data.append(cropped_data)

            # Create a widget to hold the cropped graph and delete button
            cropped_graph_container = QWidget()
            cropped_graph_layout = QVBoxLayout(cropped_graph_container)

            # Plot the cropped data in a new graph
            cropped_graph_widget = Graph()
            cropped_graph_widget.plot_widget.plot(cropped_data, pen='r')
            cropped_graph_widget.setFixedWidth(400)  # Increase the width for larger appearance
            cropped_graph_widget.custom_viewbox.set_dynamic_limits(0, len(cropped_data), min(cropped_data),
                                                                   max(cropped_data))
            cropped_graph_widget.custom_viewbox.setRange(xRange=(0, len(cropped_data)),
                                                         yRange=(min(cropped_data), max(cropped_data)), padding=0)

            # Create a delete button for this graph
            delete_button = QPushButton("Delete", self)
            delete_button.setFixedWidth(50)

            # Connect the delete button to a function to remove the graph
            delete_button.clicked.connect(lambda: self.delete_cropped_graph(cropped_graph_container, cropped_data))

            # Add the cropped graph and delete button to the layout
            cropped_graph_layout.addWidget(cropped_graph_widget)
            cropped_graph_layout.addWidget(delete_button)

            # # Add a double-click event to remove the graph
            # cropped_graph_widget.mouseDoubleClickEvent = lambda event: self.delete_cropped_graph(cropped_graph_widget,
            #                                                                                      cropped_data)

            # Add the container widget to the scroll layout
            self.scroll_layout.addWidget(cropped_graph_container)

            print(f"Cropped data from {start} to {end} added")
        except Exception as e:
            print(f"Error: {e}")

    def delete_cropped_graph(self, graph_container, cropped_data):
        """Remove the selected cropped graph and its data."""
        # Remove the cropped graph widget from the layout
        self.scroll_layout.removeWidget(graph_container)
        graph_container.deleteLater()  # Delete the widget from memory

        # Remove the corresponding data from the arrays
        if cropped_data in self.cropped_data:
            self.cropped_data.remove(cropped_data)
        if cropped_data in self.all_cropped_data:
            self.all_cropped_data.remove(cropped_data)

        print("Cropped graph and data removed")

    def load_new_graph(self):
        """Load a new graph from the dictionary of datasets."""
        try:
            key = self.graph_dropdown.currentText()

            if key in self.data_dict:
                self.data_key = key
                self.data = self.data_dict[self.data_key]
                self.original_data = self.data  # Update the original data reference

                # Clear the graph and plot the new data
                self.graph_widget.clear()
                self.plot = self.graph_widget.plot(self.data, pen='b')
                self.graph.custom_viewbox.set_dynamic_limits(0, len(self.data), min(self.data), max(self.data))

                # Reset cropped data list (since this is a new graph)
                self.cropped_data = []
                print(f"New graph '{self.data_key}' loaded.")
            else:
                print(f"Graph key '{key}' not found in dataset dictionary.")
        except Exception as e:
            print(f"Error loading new graph: {e}")

    def open_report_window(self):
        """Open a window to write and generate a report."""
        if not self.all_cropped_data:
            print("No data to generate report.")
            return

        self.report_window = ReportWindow(self.all_cropped_data)
        self.report_window.show()


class ReportWindow(QDialog):
    def __init__(self, all_cropped_data):
        super().__init__()
        self.setWindowTitle("Generate Report")
        styleSheet(self)
        # Limit window size to a quarter of the screen
        self.setGeometry(100, 100, 800, 600)  # Increase size for better display

        self.all_cropped_data = all_cropped_data  # Data passed from the main window

        # Create a layout and text area for writing the report
        layout = QVBoxLayout()

        # Add a text area for the user to write the report
        self.report_text = QTextEdit(self)
        self.report_text.setPlaceholderText("Write your report here...")
        self.report_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.report_text)

        # Scrollable area for the graphs
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QHBoxLayout(self.scroll_content)  # Horizontal layout for graphs
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)

        # Display the cropped data as graphs horizontally
        self.graph_widgets = []
        for cropped_data in self.all_cropped_data:
            graph_widget = pg.PlotWidget(self)
            graph_widget.plot(cropped_data, pen='r')
            graph_widget.setBackground('#2b2b2b')
            graph_widget.setFixedHeight(250)  # Adjusted height for a better display
            graph_widget.setFixedWidth(400)  # Wider graphs for horizontal layout
            self.graph_widgets.append(graph_widget)
            self.scroll_layout.addWidget(graph_widget)

        # Button to save the report
        save_button = QPushButton("Save Report")
        save_button.clicked.connect(self.save_report)
        layout.addWidget(save_button)

        self.setLayout(layout)


def save_report(self):
    """Save the report as a PDF file with graphs."""
    report_text = self.report_text.toPlainText()

    if not report_text:
        print("No report text to save.")
        return

    # File dialog to select where to save the PDF
    file_name, _ = QFileDialog.getSaveFileName(self, "Save Report", "", "PDF Files (*.pdf)")

    if file_name:
        # Create a PDF canvas
        c = canvas.Canvas(file_name, pagesize=letter)
        width, height = letter

        # Add a logo (make sure to replace 'logo.png' with your actual logo file)
        logo_path = os.path.join(os.path.dirname(__file__), 'Controllers', 'logo.png')
        if os.path.exists(logo_path):
            c.drawImage(logo_path, 30, height - 60, width=100, height=50)  # Adjust size/position of logo

        # Add a header
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width / 2, height - 50, "User Report")

        # Draw a line below the header
        c.line(30, height - 60, width - 30, height - 60)

        # Write the report text on the PDF with a border around it
        c.setFont("Helvetica", 12)
        c.drawCentredString(width / 2, height - 90, "Report Content:")
        text_lines = report_text.split('\n')
        y_pos = height - 120

        # Add text content with a subtle border
        c.rect(80, y_pos + 20, width - 160, -(len(text_lines) * 15 + 20))  # Border for the text area
        for line in text_lines:
            c.drawCentredString(width / 2, y_pos, line)
            y_pos -= 15

        y_pos -= 30
        c.drawCentredString(width / 2, y_pos, "Graphs of the cropped data:")
        y_pos -= 40

        # Save each graph as an image and add it to the PDF
        for idx, graph_widget in enumerate(self.graph_widgets):
            # Get the data from the plotted curve
            curve = graph_widget.plotItem.curves[0]  # Assuming each widget has one curve
            data = curve.getData()[1]  # Get the y-values (data)

            # Calculate the mean, std, maximum point, and minimum point of the graph
            mean = np.mean(data)
            std = np.std(data)
            max_point = np.max(data)
            min_point = np.min(data)

            # Save each graph as a PNG image
            exporter = ImageExporter(graph_widget.plotItem)
            image_path = f"graph_{idx}.png"
            exporter.export(image_path)

            # Calculate the center position for the image
            image_width = 300
            image_height = 150
            image_x = (width - image_width) / 2

            # Load the image and draw it on the PDF
            c.drawImage(image_path, image_x, y_pos - image_height, width=image_width, height=image_height)
            os.remove(image_path)  # Remove the image file after drawing it

            # Add label and statistics for the graph, with a border
            rect_width = 320
            rect_height = 30
            rect_x = (width - rect_width) / 2
            c.rect(rect_x, y_pos - image_height - rect_height, rect_width,
                   rect_height)  # Draw a border around the label
            c.drawCentredString(width / 2, y_pos - image_height - 20, f"Graph {idx + 1}")
            c.drawCentredString(width / 2, y_pos - image_height - 50,
                                f"Mean: {mean:.2f}, Std: {std:.2f}, Max: {max_point:.2f}, Min: {min_point:.2f}")
            y_pos -= (image_height + 70)  # Move down to leave space for the next image

            if y_pos < 150:
                c.showPage()  # Create a new page if needed
                y_pos = height - 60  # Reset y position

        # Add a footer with page numbers
        c.setFont("Helvetica", 10)
        c.drawCentredString(width - 100, 50, "Page 1")  # Adjust as needed for multiple pages

        # Save the PDF
        c.save()
        print(f"Report saved to {file_name}")


def open_report_window(signals):
    graph_window = GraphWindow(signals)
    graph_window.show()
