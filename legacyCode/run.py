import main
from PyQt5.QtWidgets import QApplication
import sys
from Controllers import controlController

app = QApplication(sys.argv)    
window = main.MainWindow()
controller = controlController.controlController()
window.btn.clicked.connect(lambda: controller.change(window))

window.show()
sys.exit(app.exec_())
