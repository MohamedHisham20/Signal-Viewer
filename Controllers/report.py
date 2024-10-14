import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit,
                             QDialog, QFileDialog)
import pyqtgraph as pg
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pyqtgraph.exporters import ImageExporter


class GraphWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graph Cropping Example")
        self.setGeometry(100, 100, 600, 400)

        # Layout and plot widget
        self.layout = QVBoxLayout()
        self.graph_widget = pg.PlotWidget()
        self.layout.addWidget(self.graph_widget)

        # Create some random data
        self.data = np.random.randn(100)
        self.plot = self.graph_widget.plot(self.data, pen='b')

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

        # Use another graph to show another signal
        self.new_graph_button = QPushButton("New Graph")
        self.new_graph_button.clicked.connect(self.show_new_graph)

        # Layout for cropping inputs
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.start_label)
        input_layout.addWidget(self.start_input)
        input_layout.addWidget(self.end_label)
        input_layout.addWidget(self.end_input)
        input_layout.addWidget(self.crop_button)
        input_layout.addWidget(self.new_graph_button)

        # Add input layout and report button to main layout
        self.layout.addLayout(input_layout)
        self.layout.addWidget(self.report_button)

        self.setLayout(self.layout)

        # Store all graphs and cropped data
        self.graphs = [self.graph_widget]
        self.all_data = [self.data]
        self.all_cropped_data = [[]]  # To store cropped data for each graph

    def show_new_graph(self):
        """Add a new graph with random data and store it."""
        new_data = np.random.randn(100)
        new_graph_widget = pg.PlotWidget()

        # Plot the new data on the new graph
        new_graph_widget.plot(new_data, pen='b')

        # Store new graph widget and data
        self.graphs.append(new_graph_widget)
        self.all_data.append(new_data)
        self.all_cropped_data.append([])

        # Add the new graph to the layout
        self.layout.addWidget(new_graph_widget)

    def crop_graph_and_save(self):
        """Crop the selected graph based on start and end inputs."""
        try:
            start = int(self.start_input.text())
            end = int(self.end_input.text())
            current_graph_index = len(self.graphs) - 1  # Get the current graph index

            if start < 0 or end >= len(self.all_data[current_graph_index]) or start >= end:
                raise ValueError("Invalid crop range")

            # Crop the data for the current graph
            cropped_data = self.all_data[current_graph_index][start:end]
            self.all_cropped_data[current_graph_index].append(cropped_data.tolist())

            # Update the current graph to show only the cropped data
            self.graphs[current_graph_index].clear()
            self.graphs[current_graph_index].plot(cropped_data, pen='r')

            print(f"Cropped data from {start} to {end} for graph {current_graph_index + 1}")
        except Exception as e:
            print(f"Error: {e}")

    def open_report_window(self):
        """Open a window to write and generate a report."""
        if all(not data for data in self.all_cropped_data):
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
        self.report_text.setSizePolicy(self.report_text.sizePolicy().horizontalPolicy(),
                                       self.report_text.sizePolicy().Preferred)  # Stretchable
        layout.addWidget(self.report_text)

        # Display the cropped data as graphs
        self.graph_widgets = []
        for graph_data in self.all_cropped_data:
            for cropped_data in graph_data:
                graph_widget = pg.PlotWidget(self)
                graph_widget.plot(cropped_data, pen='r')
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

            # Write the report text on the PDF
            c.drawString(100, height - 100, "User Report:")
            text_lines = report_text.split('\n')
            y_pos = height - 120
            for line in text_lines:
                c.drawString(100, y_pos, line)
                y_pos -= 15

            c.drawString(100, y_pos - 10, "Graphs of the cropped data:")
            y_pos -= 40

            # Save each graph as an image and add it to the PDF
            for idx, graph_widget in enumerate(self.graph_widgets):
                # Save each graph as a PNG image
                exporter = ImageExporter(graph_widget.plotItem)
                image_path = f"graph_{idx}.png"
                exporter.export(image_path)

                # Load the image and draw it on the PDF
                c.drawImage(image_path, 100, y_pos - 150, width=300, height=150)
                y_pos -= 180  # Move down to leave space for next image

                if y_pos < 150:
                    c.showPage()  # Create a new page if needed
                    y_pos = height - 100  # Reset y position

            # Save the PDF
            c.save()
            print(f"Report saved to {file_name}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = GraphWindow()
    main_window.show()
    sys.exit(app.exec_())
