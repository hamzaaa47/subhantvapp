import logging
import sys
import platform
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import *
from subhan_tv_app import SubhanTvApp
from logging_signals import log_signals  # ✅ Wichtig: hier importieren!
from config import BASE_DIR, CSS_PATH, LOG_PATH

system_name = platform.system().lower()

if "windows" in system_name:
    os.environ["QT_QPA_PLATFORM"] = "windows"

elif "linux" in system_name:
    # Prüfe, ob Wayland-Session läuft
    if os.environ.get("WAYLAND_DISPLAY"):
        os.environ.setdefault("QT_QPA_PLATFORM", "wayland")
        os.environ.setdefault("QT_WAYLAND_DISABLE_WINDOWDECORATION", "1")


def setup_logging():
    log_directory = os.path.dirname(LOG_PATH)
    if not os.path.exists(log_directory):
        os.makedirs(log_directory, exist_ok=True)
    
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[
                            logging.FileHandler(LOG_PATH),
                            logging.StreamHandler(sys.stdout)
                        ]
                    )

    class QtLogHandler(logging.Handler):
        def emit(self, record):
            msg = self.format(record)
            level = record.levelname
            log_signals.log_message.emit(level, msg)

    qt_handler = QtLogHandler()
    qt_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(qt_handler)

if __name__ == "__main__":
    setup_logging()
    print("Logging to:", LOG_PATH)
    logging.info("Application started.")

    QCoreApplication.setAttribute(Qt.AA_UseOpenGLES)
    app = QApplication(sys.argv)
    try:
        with open(CSS_PATH, "r", encoding='utf-8') as file:
            css = file.read()
            app.setStyleSheet(css)
    except Exception as e:
        error_message = f"Fehler beim Laden des Stylesheets: {e}" 
        logging.error(error_message)
        #print(error_message)
        
    window = SubhanTvApp()
    #window.showMaximized()
    #window.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
    window.showFullScreen()
    sys.exit(app.exec())
