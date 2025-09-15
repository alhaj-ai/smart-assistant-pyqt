from PyQt6.QtWidgets import QApplication
import sys

def create_app():
    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName("Smart Assistant")
    return app
