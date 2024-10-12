from PySide6.QtWidgets import QApplication

from GUI.RootWidget import RootWidget


if __name__ == "__main__":
    app = QApplication([])

    window = RootWidget()
    window.show()
    app.exec()
