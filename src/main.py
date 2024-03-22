import sys

from gui.mainwindow import AppMainWindow
from PySide6.QtWidgets import QApplication

__authors__ = ["Bc. Tomas Kostrna", "Ing. Pavol Marak, PhD."]
__license__ = "MIT"
__faculty__ = "Faculty of Electrical Engineering and Information Technology of STU in Bratislava"
__institute__ = "Department of Informatics and Mathematics"

if __name__ == "__main__":
    app = QApplication()
    widget = AppMainWindow()
    widget.show()
    sys.exit(app.exec())
