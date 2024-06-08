import logging
import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import *
from subhan_tv_app import SubhanTvApp
from config import BASE_DIR, CSS_PATH, LOG_PATH

os.environ["QT_QPA_PLATFORM"] = "xcb"

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
                        ])

if __name__ == "__main__":
    setup_logging()
    print("Logging to:", LOG_PATH)
    logging.info("Application started.")

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
