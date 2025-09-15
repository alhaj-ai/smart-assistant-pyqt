from smart_assistant.gui.app import create_app
from smart_assistant.gui.main_window import MainWindow

def main():
    app = create_app()
    win = MainWindow()
    win.show()
    return app.exec()

if __name__ == "__main__":
    raise SystemExit(main())
