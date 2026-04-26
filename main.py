import sys
from PySide6.QtWidgets import QApplication
from ui.app_window import BicoApp


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = BicoApp()
    win.show()
    sys.exit(app.exec())