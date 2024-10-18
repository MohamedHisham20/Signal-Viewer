from PySide6.QtWidgets import QWidget, QFileDialog
from GUI.FilesArea import FilesArea
from GUI.Signal import Signal

class FileManager():
    def __init__(self,FilesArea:FilesArea):
        self.managed_area = FilesArea
        self.active_file = ""
        self.mount_btns_actions()
    
            
    #orange
    def get_uploaded_files(self):
        """get all uploaded files in Files Area so far"""
        return self.managed_area.uploaded_files         