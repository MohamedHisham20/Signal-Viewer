import os
import sys
import numpy as np
from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                               QTextEdit,
                               QDialog, QFileDialog, QInputDialog, QSizePolicy)
import pyqtgraph as pg
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pyqtgraph.exporters import ImageExporter

from Graph import Graph
from Signal import Signal


class GraphWindow(QWidget):
    def __init__(self, signals=None):
        super().__init__()
        self.setWindowTitle("Graph Cropping Example")
        self.setGeometry(100, 100, 600, 400)

        # Layout and plot widget
        self.layout = QVBoxLayout()
        self.graph = Graph()
        self.graph_widget = self.graph.plot_widget
        self.graph.custom_viewbox.crop = self.crop_graph_and_save
        
        

        self.layout.addWidget(self.graph_widget)
        self.data_dict = {}

        # Initial data and dataset dictionary
        for signal in signals:
            self.data_dict[signal.ID] = signal.get_y_values()
        self.data_key = signals[0].ID  # Default dataset
        self.data = self.data_dict[self.data_key]
        self.plot = self.graph_widget.plot(self.data, pen='b')

        self.graph.custom_viewbox.set_dynamic_limits(0, len(self.data) - 1, min(self.data), max(self.data))

        # Input fields to select cropping points
        self.start_label = QLabel("Start Point:")
        self.start_input = QLineEdit()
        self.end_label = QLabel("End Point:")
        self.end_input = QLineEdit()

        self.crop_button = QPushButton("Crop")
        self.crop_button.clicked.connect(self.crop_graph_and_save)

        # Button to create report
        self.report_button = QPushButton("Generate Report")
        self.report_button.clicked.connect(self.open_report_window)

        # Button to load a new graph from the dictionary
        self.new_graph_button = QPushButton("Load New Graph")
        self.new_graph_button.clicked.connect(self.load_new_graph)

        # Layout for cropping inputs and buttons
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.start_label)
        input_layout.addWidget(self.start_input)
        input_layout.addWidget(self.end_label)
        input_layout.addWidget(self.end_input)
        input_layout.addWidget(self.crop_button)

        # Add buttons to the main layout
        self.layout.addLayout(input_layout)
        self.layout.addWidget(self.new_graph_button)  # Add new graph button
        self.layout.addWidget(self.report_button)

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

            if start < 0 or end >= len(self.original_data) or start >= end:
                raise ValueError("Invalid crop range")

            # Crop the data from the original data
            cropped_data = self.original_data[start:end]
            self.cropped_data.append(cropped_data)  # Store the current cropped data
            self.all_cropped_data.append(cropped_data)

            # Plot the cropped data below the original graph
            cropped_graph_widget = pg.PlotWidget()
            cropped_graph_widget.plot(cropped_data, pen='r')
            cropped_graph_widget.setFixedHeight(150)  # Set smaller height for each cropped graph
            
            self.graph.custom_viewbox.set_dynamic_limits(0, len(cropped_data) - 1, min(cropped_data), max(cropped_data))
            self.layout.addWidget(cropped_graph_widget)

            print(f"Cropped data from {start} to {end} added")
        except Exception as e:
            print(f"Error: {e}")

    def load_new_graph(self):
        """Load a new graph from the dictionary of datasets."""
        try:
            # Prompt user to select a key from the dataset dictionary
            key, ok = QInputDialog.getItem(self, "Select Graph", "Select a graph key:", self.data_dict.keys(), 0, False)

            if ok and key in self.data_dict:
                self.data_key = key
                self.data = self.data_dict[self.data_key]
                self.original_data = self.data  # Update the original data reference

                # Clear the graph and plot the new data
                self.graph_widget.clear()
                self.plot = self.graph_widget.plot(self.data, pen='b')

                # Reset cropped data list (since this is a new graph)
                # self.all_cropped_data = []
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

        # Limit window size to a quarter of the screen
        self.setGeometry(200, 200, 600, 500)
        self.setMinimumSize(400, 300)

        self.all_cropped_data = all_cropped_data  # Data passed from the main window

        # Create a layout and text area for writing the report
        layout = QVBoxLayout()

        # Add a text area for the user to write the report
        self.report_text = QTextEdit(self)
        self.report_text.setPlaceholderText("Write your report here...")
        self.report_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.report_text)

        # Display the cropped data as graphs
        self.graph_widgets = []
        for cropped_data in self.all_cropped_data:
            graph_widget = pg.PlotWidget(self)
            graph_widget.plot(cropped_data, pen='black')
            graph_widget.setBackground('w')
            graph_widget.setFixedHeight(150)  # Set smaller height for each graph
            self.graph_widgets.append(graph_widget)
            layout.addWidget(graph_widget)

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
            logo_path = "D:/Eng/SBE/3rd/DSP/Signal-Viewer/Controllers/logo.png"
            if os.path.exists(logo_path):
                c.drawImage(logo_path, 30, height - 60, width=100, height=50)  # Adjust size/position of logo

            # Add a header
            c.setFont("Helvetica-Bold", 14)
            c.drawString(150, height - 50, "User Report")

            # Draw a line below the header
            c.line(30, height - 60, width - 30, height - 60)

            # Write the report text on the PDF with a border around it
            c.setFont("Helvetica", 12)
            c.drawString(100, height - 90, "Report Content:")
            text_lines = report_text.split('\n')
            y_pos = height - 120

            # Add text content with a subtle border
            c.rect(80, y_pos + 20, width - 160, -(len(text_lines) * 15 + 20))  # Border for the text area
            for line in text_lines:
                c.drawString(100, y_pos, line)
                y_pos -= 15

            y_pos -= 30
            c.drawString(100, y_pos, "Graphs of the cropped data:")
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

                # Load the image and draw it on the PDF
                c.drawImage(image_path, 100, y_pos - 150, width=300, height=150)
                os.remove(image_path)  # Remove the image file after drawing it

                # Add label and statistics for the graph, with a border
                c.rect(90, y_pos - 180, 320, 30)  # Draw a border around the label
                c.drawString(100, y_pos - 170, f"Graph {idx + 1}")
                c.drawString(100, y_pos - 200,
                             f"Mean: {mean:.2f}, Std: {std:.2f}, Max: {max_point:.2f}, Min: {min_point:.2f}")
                y_pos -= 220  # Move down to leave space for next image

                if y_pos < 150:
                    c.showPage()  # Create a new page if needed
                    y_pos = height - 60  # Reset y position

            # Add a footer with page numbers
            c.setFont("Helvetica", 10)
            c.drawString(width - 100, 50, "Page 1")  # Adjust as needed for multiple pages

            # Save the PDF
            c.save()
            print(f"Report saved to {file_name}")


def open_report_window():
    graph_window = GraphWindow(Signal.get_all_signals(True))
    graph_window.show()
    # graph_window.exec()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     main_window = GraphWindow(Signal.get_all_signals(True))
#     main_window.show()
#     sys.exit(app.exec())
