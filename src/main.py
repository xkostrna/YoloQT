import sys

from gui.mainwindow import AppMainWindow
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication()
    widget = AppMainWindow()
    widget.show()
    sys.exit(app.exec())
