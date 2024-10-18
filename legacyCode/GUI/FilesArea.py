from PySide6.QtWidgets import QWidget,QPushButton, QVBoxLayout
from GUI.Signal import Signal
from typing import List

class FilesArea(QWidget):
    def __init__(self):
        super().__init__()
        self.Layout = QVBoxLayout(self)
        
        self.uploaded_files: List[str] = []
        self.uploaded_signals: List[Signal] = []
        self.active_file = ""
        self.signals_counter = 0
        self.upload_btn = QPushButton("upload",self)
        self.delete_btn = QPushButton("delete",self)
        
        self.Layout.addWidget(self.upload_btn)
        self.Layout.addWidget(self.delete_btn)