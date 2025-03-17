import os
import sys
import logging

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS_PATH = os.path.join(BASE_DIR, 'src', 'style.css')
MEDIA_PATH = os.path.join(BASE_DIR, "media")
KALIMA_PATH = os.path.join(BASE_DIR, 'assets', "kalima-white.png")
FILE_PRAYER_TIMES_PATH = os.path.join(BASE_DIR, 'data', "prayer_times.xlsx")
FILE_RAMADAN_PLAN = os.path.join(BASE_DIR, 'data', "ramadan2025.xlsx")
LOG_PATH = os.path.join(BASE_DIR, 'application.log')

# Logge die aktuellen Pfade
logging.debug(f"BASE_DIR: {BASE_DIR}")
logging.debug(f"MEDIA_PATH: {MEDIA_PATH}")
logging.debug(f"FILE_PRAYER_TIMES_PATH: {FILE_PRAYER_TIMES_PATH}")
logging.debug(f"LOG_PATH: {LOG_PATH}")

# Größen und Dimensionen
WIDTH = 1920
HEIGHT = 1080

MEDIA_PLAYER_WIDTH = 1520
MEDIA_PLAYER_HEIGHT = 950

FOOTER_HEIGHT = 50
HEADER_HEIGHT = HEIGHT - MEDIA_PLAYER_HEIGHT - FOOTER_HEIGHT

IMAGE_TIMER = 10000