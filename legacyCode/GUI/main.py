from PySide6.QtWidgets import QApplication
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from GUI.RootWidget import RootWidget


if __name__ == "__main__":
    app = QApplication([])

    window = RootWidget()
    window.show()
    app.exec()
